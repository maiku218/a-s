from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
import sqlite3
from database_sqlite import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
import json
import os
import subprocess
import tempfile
import csv
from io import BytesIO, StringIO

# Offline report generation libraries
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

app = Flask(__name__)
app.secret_key = "simple_secret_key"
app.config['SESSION_PERMANENT'] = True  # Session persists on browser close
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours - session lasts 24 hours

# Use separate cookies for admin and cashier
app.config['SESSION_COOKIE_NAME'] = 'pharmacon_session'

# Add datetime to template context
@app.context_processor
def inject_datetime():
    return dict(datetime=datetime, LOW_STOCK_THRESHOLD=LOW_STOCK_THRESHOLD, csrf_token=generate_csrf_token)

@app.template_filter('format_date')
def format_date(value, format='%Y-%m-%d %H:%M'):
    if not value:
        return '-'
    if isinstance(value, str):
        try:
            dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return dt.strftime(format)
        except:
            try:
                dt = datetime.strptime(value, '%Y-%m-%d')
                return dt.strftime(format)
            except:
                return value
    if hasattr(value, 'strftime'):
        return value.strftime(format)
    return value

def export_to_csv(data, headers, filename):
    """Export data to CSV file."""
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(headers)
    
    # Write data
    for row in data:
        writer.writerow(row)
    
    # Create response
    mem = BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    
    return send_file(
        mem,
        as_attachment=True,
        download_name=filename,
        mimetype='text/csv'
    )

# =============================
# SHARED SALES ANALYTICS ENGINE
# =============================

def get_date_filter_params(date_from=None, date_to=None):
    """Build SQL date filter clause and params from date_from/date_to strings."""
    params = []
    clause = ""
    if date_from and date_to:
        clause = " AND DATE(s.sale_date) >= ? AND DATE(s.sale_date) <= ?"
        params = [date_from, date_to]
    elif date_from:
        clause = " AND DATE(s.sale_date) >= ?"
        params = [date_from]
    elif date_to:
        clause = " AND DATE(s.sale_date) <= ?"
        params = [date_to]
    return clause, params


def get_product_type_filter(product_scope):
    """Return SQL filter for product_type scope: 'overall', 'medical', 'non_medical'."""
    if product_scope == 'medical':
        return " AND p.product_type = 'Medical'"
    elif product_scope == 'non_medical':
        return " AND p.product_type = 'Non-Medical'"
    return ""


def calculate_sales_analytics(conn, date_from=None, date_to=None, product_scope='overall'):
    """
    Reusable analytics calculation supporting three scopes:
    - overall: all sales
    - medical: medical products only (calculated from sale_items + products.product_type)
    - non_medical: non-medical products only

    Important: Category revenue is calculated from sale_items joined with products,
    NOT from sales.product_type, so mixed transactions are handled correctly.
    """
    cur = conn.cursor()

    date_clause, date_params = get_date_filter_params(date_from, date_to)
    type_filter = get_product_type_filter(product_scope)

    # Base query: sale_items joined with products and sales, filtered by Completed status
    base_from = """
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        JOIN sales s ON si.sale_id = s.id
        WHERE s.sale_status = 'Completed'
    """
    where_clause = base_from + date_clause + type_filter

    # Total Revenue (sum of line item subtotals)
    cur.execute(f"""
        SELECT IFNULL(SUM(si.quantity * si.price), 0) {where_clause}
    """, date_params)
    total_revenue = float(cur.fetchone()[0])

    # Total Quantity Sold
    cur.execute(f"""
        SELECT IFNULL(SUM(si.quantity), 0) {where_clause}
    """, date_params)
    total_quantity = int(cur.fetchone()[0])

    # Distinct Transaction Count (distinct sale IDs to avoid double-counting mixed transactions)
    cur.execute(f"""
        SELECT COUNT(DISTINCT s.id) {where_clause}
    """, date_params)
    total_transactions = int(cur.fetchone()[0])

    # Average Order Value
    avg_order_value = round(total_revenue / total_transactions, 2) if total_transactions > 0 else 0.0

    # Best-selling products (by quantity)
    cur.execute(f"""
        SELECT p.product_name, p.product_type,
               IFNULL(SUM(si.quantity), 0) as total_qty,
               IFNULL(SUM(si.quantity * si.price), 0) as total_rev
        {where_clause}
        GROUP BY p.id, p.product_name, p.product_type
        ORDER BY total_qty DESC
        LIMIT 10
    """, date_params)
    best_selling = [
        {'name': row[0], 'type': row[1], 'qty': int(row[2]), 'revenue': float(row[3])}
        for row in cur.fetchall()
    ]

    # Revenue trend (daily) for last 30 days or date range
    if date_from and date_to:
        trend_where = f"""
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            JOIN sales s ON si.sale_id = s.id
            WHERE s.sale_status = 'Completed'
            AND DATE(s.sale_date) >= ? AND DATE(s.sale_date) <= ?
            {type_filter}
            GROUP BY DATE(s.sale_date)
            ORDER BY DATE(s.sale_date) ASC
        """
        trend_params = [date_from, date_to]
    else:
        trend_where = f"""
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            JOIN sales s ON si.sale_id = s.id
            WHERE s.sale_status = 'Completed'
            AND DATE(s.sale_date) >= date('now', '-30 days', 'localtime')
            {type_filter}
            GROUP BY DATE(s.sale_date)
            ORDER BY DATE(s.sale_date) ASC
        """
        trend_params = []

    cur.execute(f"""
        SELECT DATE(s.sale_date) as day, IFNULL(SUM(si.quantity * si.price), 0) as daily_total
        {trend_where}
    """, trend_params)
    trend_data = cur.fetchall()
    trend_labels = [str(row[0]) for row in trend_data]
    trend_values = [float(row[1]) for row in trend_data]

    # Period comparison: current vs previous period
    # Determine period length from date range, default to 30 days
    if date_from and date_to:
        from datetime import datetime
        d1 = datetime.strptime(date_from, '%Y-%m-%d')
        d2 = datetime.strptime(date_to, '%Y-%m-%d')
        days = (d2 - d1).days + 1
    else:
        days = 30

    # Current period revenue
    cur.execute(f"""
        SELECT IFNULL(SUM(si.quantity * si.price), 0)
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        JOIN sales s ON si.sale_id = s.id
        WHERE s.sale_status = 'Completed'
        {date_clause}
        {type_filter}
    """, date_params)
    current_revenue = float(cur.fetchone()[0])

    # Previous period revenue (same length, before current period)
    if date_from and date_to:
        from datetime import datetime, timedelta
        d1 = datetime.strptime(date_from, '%Y-%m-%d')
        d2 = datetime.strptime(date_to, '%Y-%m-%d')
        days = (d2 - d1).days + 1
        prev_to = (d1 - timedelta(days=1)).strftime('%Y-%m-%d')
        prev_from = (d1 - timedelta(days=days)).strftime('%Y-%m-%d')
        prev_params = [prev_from, prev_to]
        prev_date_clause = " AND DATE(s.sale_date) >= ? AND DATE(s.sale_date) <= ?"
    else:
        prev_params = []
        prev_date_clause = " AND DATE(s.sale_date) >= date('now', '-60 days', 'localtime') AND DATE(s.sale_date) < date('now', '-30 days', 'localtime')"

    cur.execute("""
        SELECT IFNULL(SUM(si.quantity * si.price), 0)
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        JOIN sales s ON si.sale_id = s.id
        WHERE s.sale_status = 'Completed'
        """ + prev_date_clause + """
        """ + type_filter + """
    """, prev_params)
    previous_revenue = float(cur.fetchone()[0])

    # Sales growth percentage
    if previous_revenue > 0:
        sales_growth = round(((current_revenue - previous_revenue) / previous_revenue) * 100, 2)
    else:
        sales_growth = 100.0 if current_revenue > 0 else 0.0

    # Gross Profit (placeholder - no cost data available yet)
    # We estimate profit as revenue (no cost basis in current schema)
    gross_profit = total_revenue
    profit_margin = 100.0 if total_revenue > 0 else 0.0

    return {
        'scope': product_scope,
        'total_revenue': round(total_revenue, 2),
        'total_transactions': total_transactions,
        'total_quantity': total_quantity,
        'avg_order_value': avg_order_value,
        'gross_profit': round(gross_profit, 2),
        'profit_margin': round(profit_margin, 2),
        'sales_growth': sales_growth,
        'best_selling': best_selling,
        'trend_labels': trend_labels,
        'trend_values': trend_values,
        'current_revenue': round(current_revenue, 2),
        'previous_revenue': round(previous_revenue, 2),
    }


def generate_business_insights(analytics_data, scope_name):
    """Generate automated business insights from analytics data."""
    insights = []

    revenue = analytics_data['total_revenue']
    transactions = analytics_data['total_transactions']
    growth = analytics_data['sales_growth']
    best = analytics_data['best_selling']

    if transactions > 0:
        insights.append({
            'type': 'info',
            'title': f'{scope_name} Performance',
            'message': f'Total {scope_name.lower()} revenue of ₱{revenue:,.2f} across {transactions} transactions.'
        })

    if growth > 0:
        insights.append({
            'type': 'success',
            'title': 'Sales Growth',
            'message': f'{scope_name} sales grew by {growth}% compared to the previous period.'
        })
    elif growth < 0:
        insights.append({
            'type': 'warning',
            'title': 'Sales Decline',
            'message': f'{scope_name} sales declined by {abs(growth)}% compared to the previous period.'
        })
    else:
        insights.append({
            'type': 'info',
            'title': 'Sales Stable',
            'message': f'{scope_name} sales remained stable compared to the previous period.'
        })

    if best:
        top = best[0]
        insights.append({
            'type': 'info',
            'title': 'Top Product',
            'message': f'"{top["name"]}" is the best-selling {scope_name.lower()} product with {top["qty"]} units sold (₱{top["revenue"]:,.2f}).'
        })

    if len(best) > 1:
        second = best[1]
        if top['revenue'] > 0:
            pct = round((second['revenue'] / top['revenue']) * 100, 1)
            insights.append({
                'type': 'info',
                'title': 'Product Comparison',
                'message': f'{second["name"]} contributes {pct}% of the revenue of the top product.'
            })

    if revenue > 0 and transactions > 0:
        aov = analytics_data['avg_order_value']
        insights.append({
            'type': 'info',
            'title': 'Average Order Value',
            'message': f'Customers spend an average of ₱{aov:,.2f} per {scope_name.lower()} transaction.'
        })

    return insights


def export_to_pdf(data, headers, filename, title="Sales Report"):
    """Export data to PDF file using reportlab (offline)."""
    mem = BytesIO()
    doc = SimpleDocTemplate(mem, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Title'],
        fontSize=18, textColor=colors.HexColor('#1e293b'),
        spaceAfter=12, alignment=1
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#64748b'),
        spaceAfter=20, alignment=1
    )

    elements = []
    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", subtitle_style))
    elements.append(Spacer(1, 12))

    # Build table
    table_data = [headers] + [list(row) for row in data]
    col_widths = [max(len(str(h)) * 8, 80) for h in headers]
    total_width = sum(col_widths)
    if total_width > 500:
        scale = 500 / total_width
        col_widths = [w * scale for w in col_widths]

    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    elements.append(table)

    doc.build(elements)
    mem.seek(0)
    return send_file(
        mem, as_attachment=True, download_name=filename, mimetype='application/pdf'
    )


def export_to_excel(data, headers, filename, title="Sales Report"):
    """Export data to Excel file using openpyxl (offline)."""
    mem = BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = title[:31]

    # Title row
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
    title_cell = ws.cell(row=1, column=1, value=title)
    title_cell.font = Font(bold=True, size=16, color="1E293B")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # Subtitle row
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(headers))
    sub_cell = ws.cell(row=2, column=1, value=f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    sub_cell.font = Font(size=10, color="64748B")
    sub_cell.alignment = Alignment(horizontal="center", vertical="center")

    # Header row
    header_row = 4
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col_idx, value=header)
        cell.font = Font(bold=True, color="FFFFFF", size=10)
        cell.fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = Border(
            left=Side(style="thin", color="CBD5E1"),
            right=Side(style="thin", color="CBD5E1"),
            top=Side(style="thin", color="CBD5E1"),
            bottom=Side(style="thin", color="CBD5E1")
        )

    # Data rows
    for row_idx, row in enumerate(data, header_row + 1):
        for col_idx, value in enumerate(row, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.font = Font(size=10, color="334155")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = Border(
                left=Side(style="thin", color="CBD5E1"),
                right=Side(style="thin", color="CBD5E1"),
                top=Side(style="thin", color="CBD5E1"),
                bottom=Side(style="thin", color="CBD5E1")
            )
            if row_idx % 2 == 0:
                cell.fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")

    # Auto column widths
    for col_idx in range(1, len(headers) + 1):
        max_len = max(len(str(headers[col_idx - 1])), 10)
        for row in data:
            max_len = max(max_len, len(str(row[col_idx - 1])))
        ws.column_dimensions[get_column_letter(col_idx)].width = min(max_len + 2, 50)

    wb.save(mem)
    mem.seek(0)
    return send_file(
        mem, as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

def clean_input(value):
    if not value:
        return ""
    return value.strip()

# Security: CSRF Protection
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = os.urandom(32).hex()
    return session['csrf_token']

def validate_csrf_token():
    token = request.form.get('csrf_token') or request.headers.get('X-CSRFToken')
    if not token or token != session.get('csrf_token'):
        return False
    return True

@app.before_request
def csrf_protect():
    if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
        exempt_routes = ['cashier_login', 'admin_login', 'admin_login_oop', 'cashier_login_oop']
        if request.endpoint not in exempt_routes:
            if not validate_csrf_token():
                if request.is_json:
                    return jsonify({'success': False, 'message': 'CSRF token missing or invalid'}), 403
                flash('CSRF token missing or invalid. Please refresh and try again.', 'error')
                return redirect(request.referrer or url_for('admin_login'))

# Security: Login Attempt Tracking
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_MINUTES = 15

# SQLite config
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pharmacon.db')

# Low stock threshold
LOW_STOCK_THRESHOLD = 10

# OOP Imports and Service Instances
from models import Product, StockMovement, Cashier
from services import AuthService, ProductRepository, SalesService
auth_service = AuthService()
product_repository = ProductRepository()
sales_service = SalesService()

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_user' not in session or session.get('role') != 'admin':
            if request.path.startswith('/api/'):
                return jsonify({'success': False, 'message': 'Session expired. Please login again.'}), 401
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def cashier_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        is_api = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if 'role' not in session or session['role'] != 'cashier':
            if is_api:
                return jsonify({'success': False, 'message': 'Session expired. Please login again.'}), 401
            return redirect(url_for('cashier_login'))
        if 'cashier_id' not in session:
            session.pop('cashier_user', None)
            session.pop('cashier_id', None)
            session.pop('role', None)
            if is_api:
                return jsonify({'success': False, 'message': 'Session expired. Please login again.'}), 401
            return redirect(url_for('cashier_login'))

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("SELECT status FROM cashiers WHERE id=?", (session['cashier_id'],))
            cashier_status = cur.fetchone()
        finally:
            conn.close()

        if not cashier_status or (cashier_status[0] or 'active').lower() != 'active':
            session.pop('cashier_user', None)
            session.pop('cashier_id', None)
            session.pop('role', None)
            if is_api:
                return jsonify({'success': False, 'message': 'Cashier account is inactive. Please login with an active account.'}), 401
            flash("Cashier account is inactive. Contact the administrator.", "error")
            return redirect(url_for('cashier_login'))

        return f(*args, **kwargs)
    return decorated_function

# =============================
# ADMIN LOGIN (Default)
# =============================

@app.route('/')
def index():
    return redirect(url_for('admin_login'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if 'admin_user' in session and session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = clean_input(request.form.get('username'))
        password = clean_input(request.form.get('password'))

        if username == "" or password == "":
            flash("All fields are required", "error")
            return redirect(url_for('admin_login'))

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, username, password FROM admins WHERE username=?", (username,))
        admin = cur.fetchone()
        conn.close()

        # Create default admin if none exists, or patch security fields if missing
        if not admin:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM admins")
            count = cur.fetchone()[0]
            conn.close()
            if count == 0:
                hashed = generate_password_hash('admin123')
                from werkzeug.security import generate_password_hash as gen_hash
                answer_hashed = gen_hash('admin123')
                conn = get_db()
                cur = conn.cursor()
                cur.execute("INSERT INTO admins (username, password, full_name, security_question, security_answer) VALUES (?, ?, ?, ?, ?)", ('admin', hashed, 'System Administrator', 'What is the name of the owner?', 'pbkdf2:sha256:600000$BlhM6ndrgPIj0Eui$8c0c6511b8af1f42401c742e1da56b34bfb60e56d703087fcc4f013f2cc2ecae'))
                conn.commit()
                conn.close()
                conn = get_db()
                cur = conn.cursor()
                cur.execute("SELECT id, username, password FROM admins WHERE username='admin'")
                admin = cur.fetchone()
                conn.close()
            else:
                flash("Invalid username or password", "error")
                return redirect(url_for('admin_login'))
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT security_question, security_answer FROM admins WHERE id=?", (admin[0],))
            sq = cur.fetchone()
            conn.close()
            if not sq or not sq[0] or not sq[1]:
                hashed_answer = generate_password_hash('generoso')
                conn = get_db()
                cur = conn.cursor()
                cur.execute("UPDATE admins SET security_question=?, security_answer=? WHERE id=?", ('What is the name of the owner?', hashed_answer, admin[0]))
                conn.commit()
                conn.close()
        
        if admin and (password == admin[2] or check_password_hash(admin[2], password)):
            session['admin_user'] = admin[1]
            session['admin_id'] = admin[0]
            session['role'] = 'admin'
            session.permanent = True  # Session persists on refresh
            
            # Log admin login activity
            conn = get_db()
            cur = conn.cursor()
            ip_address = request.remote_addr
            if request.headers.get('X-Forwarded-For'):
                ip_address = request.headers.get('X-Forwarded-For')
            
            try:
                cur.execute("""
                    INSERT INTO admin_activity (admin_id, action, ip_address, details)
                    VALUES (?, ?, ?, ?)
                """, (admin[0], 'Admin Login', ip_address, f'Admin {admin[1]} logged in'))
                conn.commit()
            except:
                pass  # Table might not exist yet
            conn.close()
            
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid login credentials", "error")
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

# =============================
# ADMIN DASHBOARD
# =============================

@app.route('/admin')
@admin_required
def admin_dashboard():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM cashiers")
    cashiers = cur.fetchall()

    cur.execute("""
        SELECT c.id, c.full_name, c.username, ca.login_time
        FROM cashiers c
        JOIN cashier_activity ca ON c.id = ca.cashier_id
        WHERE ca.logout_time IS NULL
        ORDER BY ca.login_time DESC
    """)
    active_cashiers = cur.fetchall()

    cur.execute("""
        SELECT c.full_name, c.username, ca.login_time, ca.logout_time
        FROM cashier_activity ca
        JOIN cashiers c ON c.id = ca.cashier_id
        ORDER BY ca.login_time DESC
        LIMIT 10
    """)
    activity_logs = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date < date('now', 'localtime') AND expiration_date IS NOT NULL")
    expired_count = cur.fetchone()[0]

    conn.close()
    return render_template('admin_dashboard.html',
                           cashiers=cashiers,
                           active_cashiers=active_cashiers,
                           activity_logs=activity_logs,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           expired_count=expired_count,
                           active_main='admin',
                           active_sub='dashboard')

@app.route('/alert_history')
@admin_required
def alert_history():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT al.id, al.alert_type, al.alert_level, p.product_name, 
               al.message, al.created_at, al.acknowledged_by, al.dismissed_by,
               al.dismiss_reason
        FROM alert_logs al
        JOIN products p ON al.product_id = p.id
        ORDER BY al.created_at DESC
    """)
    logs = cur.fetchall()
    
    conn.close()
    return render_template('alert_history.html', logs=logs,
                           active_main='alerts', active_sub='alert_history')

@app.route('/api/alert/acknowledge', methods=['POST'])
def api_alert_acknowledge():
    if session.get('role') not in ('admin', 'cashier'):
        return jsonify({'success': False, 'message': 'Session expired. Please login again.'}), 401

    user_type = 'admin' if session.get('role') == 'admin' else 'cashier'
    user_id = session.get('admin_id') if user_type == 'admin' else session.get('cashier_id')

    data = request.get_json()
    alert_type = data.get('alert_type')
    product_id = data.get('product_id')

    if not alert_type or not product_id:
        return jsonify({'success': False, 'message': 'Missing data'})

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT OR IGNORE INTO alert_logs (alert_type, alert_level, product_id, message, created_at)
            VALUES (?, 'info', ?, ?, datetime('now', 'localtime'))
        """, (alert_type, product_id, f'{alert_type} alert for product {product_id}'))

        cur.execute("""
            UPDATE alert_logs
            SET acknowledged_by = ?, acknowledged_at = datetime('now', 'localtime')
            WHERE alert_type = ? AND product_id = ?
        """, (user_id, alert_type, product_id))

        cur.execute("""
            INSERT INTO alert_acknowledgments (product_id, alert_type, action, user_id, user_type)
            VALUES (?, ?, 'acknowledge', ?, ?)
            ON CONFLICT(alert_type, product_id) DO UPDATE SET
                action = excluded.action,
                user_id = excluded.user_id,
                user_type = excluded.user_type,
                created_at = datetime('now', 'localtime')
        """, (product_id, alert_type, user_id, user_type))

        conn.commit()
        return jsonify({'success': True, 'message': 'Alert acknowledged'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()

@app.route('/api/alert/dismiss', methods=['POST'])
def api_alert_dismiss():
    if session.get('role') not in ('admin', 'cashier'):
        return jsonify({'success': False, 'message': 'Session expired. Please login again.'}), 401

    user_type = 'admin' if session.get('role') == 'admin' else 'cashier'
    user_id = session.get('admin_id') if user_type == 'admin' else session.get('cashier_id')

    data = request.get_json()
    alert_type = data.get('alert_type')
    product_id = data.get('product_id')
    reason = data.get('reason', '')

    if not alert_type or not product_id:
        return jsonify({'success': False, 'message': 'Missing data'})
    if not reason:
        return jsonify({'success': False, 'message': 'Reason is required'})

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT OR IGNORE INTO alert_logs (alert_type, alert_level, product_id, message, created_at)
            VALUES (?, 'info', ?, ?, datetime('now', 'localtime'))
        """, (alert_type, product_id, f'{alert_type} alert for product {product_id}'))

        cur.execute("""
            UPDATE alert_logs
            SET dismissed_by = ?, dismissed_at = datetime('now', 'localtime'), dismiss_reason = ?
            WHERE alert_type = ? AND product_id = ?
        """, (user_id, reason, alert_type, product_id))

        cur.execute("""
            INSERT INTO alert_acknowledgments (product_id, alert_type, action, reason, user_id, user_type)
            VALUES (?, ?, 'dismiss', ?, ?, ?)
            ON CONFLICT(alert_type, product_id) DO UPDATE SET
                action = excluded.action,
                reason = excluded.reason,
                user_id = excluded.user_id,
                user_type = excluded.user_type,
                created_at = datetime('now', 'localtime')
        """, (product_id, alert_type, reason, user_id, user_type))

        conn.commit()
        return jsonify({'success': True, 'message': 'Alert dismissed'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()

@app.route('/cashier_metrics')
@cashier_required
def cashier_metrics():
    conn = get_db()
    cur = conn.cursor()
    cashier_id = session.get('cashier_id')

    cur.execute("""
        SELECT COUNT(s.id) as total_sales,
               COALESCE(SUM(s.total_amount), 0) as total_revenue,
               COUNT(DISTINCT DATE(s.sale_date)) as days_active
        FROM sales s
        WHERE s.cashier_id = ? AND s.sale_status = 'Completed'
    """, (cashier_id,))
    my = cur.fetchone()
    my_total = my[1] if my else 0
    my_count = my[0] if my else 0
    my_avg = (my_total / my_count) if my_count > 0 else 0

    cur.execute("""
        SELECT c.full_name, c.username,
               COALESCE(SUM(s.total_amount), 0) as total_revenue,
               COUNT(s.id) as total_sales
        FROM cashiers c
        LEFT JOIN sales s ON c.id = s.cashier_id AND s.sale_status = 'Completed'
        GROUP BY c.id, c.full_name, c.username
        ORDER BY total_revenue DESC
    """)
    rankings = cur.fetchall()
    
    conn.close()
    return render_template('cashier_metrics.html',
                           my_total=my_total, my_count=my_count, my_avg=my_avg,
                           rankings=rankings,
                           active_main='reports', active_sub='cashier_metrics')

@app.route('/admin/cashier_logs')
@admin_required
def cashier_logs():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT c.full_name, c.username, ca.login_time, ca.logout_time, ca.ip_address
        FROM cashier_activity ca
        JOIN cashiers c ON c.id = ca.cashier_id
        ORDER BY ca.login_time DESC
    """)
    activity_logs = cur.fetchall()
    activity_logs = [
        (row[0], row[1], datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S') if row[2] else None,
         datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S') if row[3] else None, row[4])
        for row in activity_logs
    ]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    conn.close()

    return render_template('admin_cashier_logs.html', 
                           activity_logs=activity_logs,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='dashboard', 
                           active_sub='cashier_logs')

@app.route('/admin/activity_logs')
@admin_required
def admin_activity_logs():
    """View detailed admin activity logs"""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT a.username, aa.action, aa.ip_address, aa.details, aa.activity_time
        FROM admin_activity aa
        JOIN admins a ON aa.admin_id = a.id
        ORDER BY aa.activity_time DESC
        LIMIT 50
    """)
    admin_logs = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    conn.close()

    return render_template('admin_activity_logs.html', 
                           admin_logs=admin_logs,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='dashboard',
                           active_sub='activity_logs')

# =============================
# HISTORY NAVIGATION
# =============================

@app.route('/admin/history')
@admin_required
def admin_history():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]

    conn.close()
    return render_template('admin_history.html',
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='activity_history', active_sub='activity_history')

@app.route('/cashier/history')
@cashier_required
def cashier_history_page():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    conn.close()
    return render_template('cashier_transaction_history.html',
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='history', active_sub='history')

@app.route('/admin/transaction_history')
@admin_required
def transaction_history():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    conn.close()
    return render_template('transaction_history.html',
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='activity_history', active_sub='transaction_history')

@app.route('/api/transactions')
@admin_required
def api_transactions():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.id, s.receipt_number, s.sale_date, s.total_amount, s.sale_status,
               s.product_type, c.full_name as cashier_name,
               (SELECT COUNT(*) FROM sale_items WHERE sale_id = s.id) as items_count
        FROM sales s
        LEFT JOIN cashiers c ON s.cashier_id = c.id
        ORDER BY s.sale_date DESC
    """)
    sales = cur.fetchall()
    conn.close()

    transactions = []
    for s in sales:
        transactions.append({
            'id': s[0],
            'receipt_number': s[1],
            'sale_date': s[2],
            'total_amount': s[3],
            'sale_status': s[4],
            'product_type': s[5],
            'cashier_name': s[6] if s[6] else 'pharmacon',
            'items_count': s[7]
        })

    return jsonify({'success': True, 'transactions': transactions})

@app.route('/api/transaction_items/<int:transaction_id>')
@admin_required
def api_transaction_items(transaction_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT si.quantity, si.price, p.product_name, p.product_type
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        WHERE si.sale_id = ?
    """, (transaction_id,))
    items = cur.fetchall()
    conn.close()

    items_list = []
    for item in items:
        items_list.append({
            'quantity': item[0],
            'price': item[1],
            'product_name': item[2],
            'product_type': item[3]
        })

    return jsonify({'success': True, 'items': items_list})

@app.route('/api/history')
@admin_required
def api_history():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 50, type=int)
    offset = (page - 1) * limit

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT sm.id, sm.movement_date as datetime, p.product_name,
               sm.movement_type, sm.quantity, sm.reason, 'stock' as source
        FROM stock_movements sm
        JOIN products p ON sm.product_id = p.id
        ORDER BY sm.movement_date DESC
    """)
    stock_entries = cur.fetchall()

    cur.execute("""
        SELECT aa.id, aa.activity_time as datetime, a.username,
               aa.action, aa.ip_address, aa.details, 'admin' as source
        FROM admin_activity aa
        JOIN admins a ON aa.admin_id = a.id
        ORDER BY aa.activity_time DESC
    """)
    admin_entries = cur.fetchall()

    conn.close()

    combined = []

    for entry in stock_entries:
        direction = entry[3]
        product = entry[2]
        qty = entry[4]
        reason = entry[5]

        if direction == 'IN':
            if reason == 'Stock Addition':
                desc = f"Added {qty} units of {product} to stock"
            elif reason == 'Restock':
                desc = f"Restocked {qty} units of {product}"
            elif reason == 'Shipment Received':
                desc = f"Received shipment of {qty} units of {product}"
            elif reason == 'Return':
                desc = f"Returned {qty} units of {product}"
            elif reason == 'Transfer In':
                desc = f"Transferred {qty} units of {product} into inventory"
            elif reason == 'Inventory Adjustment':
                desc = f"Adjusted {product} stock by +{qty} units"
            elif reason == 'Change Quantity':
                desc = f"Changed {product} stock by +{qty} units"
            elif reason == 'Void Sale':
                desc = f"VOIDED - Restored {qty} units of {product}"
            elif reason == 'Refund Sale':
                desc = f"REFUNDED - Restored {qty} units of {product}"
            else:
                desc = f"+{qty} {product} ({reason})"
        else:
            if reason == 'Sale':
                desc = f"Sold {qty} units of {product}"
            elif reason == 'Product Deleted':
                desc = f"Deleted {product} ({qty} units removed)"
            elif reason == 'Change Quantity':
                desc = f"Changed {product} stock by -{qty} units"
            else:
                desc = f"-{qty} {product} ({reason})"

        combined.append({
            'id': entry[0],
            'datetime': entry[1],
            'product_name': product,
            'action': reason,
            'quantity': qty,
            'display_qty': f"+{qty}" if direction == 'IN' else f"-{qty}",
            'movement_type': direction,
            'direction': direction,
            'reason': reason,
            'description': desc,
            'actor': 'admin',
            'source': 'stock',
        })

    for entry in admin_entries:
        action = entry[3] if entry[3] else 'Unknown'
        details = entry[6] if entry[6] else ''
        username = entry[2]
        dt = entry[1]

        if action == 'Admin Login':
            desc = f"Admin {username} logged in"
        elif action == 'Admin Logout':
            desc = f"Admin {username} logged out"
        elif action == 'Add New Product':
            desc = f"Added new product: {details}"
        elif action == 'Edit Product':
            desc = f"Edited product: {details}"
        elif action == 'Delete Product':
            desc = f"Deleted product: {details}"
        elif action == 'Register Cashier':
            desc = f"Registered cashier: {details}"
        elif action == 'Delete Cashier':
            desc = f"Deleted cashier: {details}"
        elif action == 'Stock In':
            desc = f"Stock In: {details}"
        else:
            desc = f"{action}: {details}"

        combined.append({
            'id': entry[0],
            'datetime': entry[1],
            'product_name': '-' if action in ('Admin Login', 'Admin Logout', 'Register Cashier', 'Delete Cashier', 'Change Password') else 'System',
            'action': action,
            'quantity': None,
            'display_qty': '',
            'movement_type': None,
            'direction': None,
            'reason': action,
            'description': desc,
            'actor': username,
            'source': 'admin',
        })

    combined.sort(key=lambda x: x['datetime'], reverse=True)

    total = len(combined)
    entries = combined[offset:offset + limit]

    return jsonify({
        'success': True,
        'entries': entries,
        'total': total,
        'page': page,
        'limit': limit
    })

@app.route('/api/cashier/history')
@cashier_required
def api_cashier_history():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 50, type=int)
    offset = (page - 1) * limit
    cashier_id = session.get('cashier_id')

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT sm.id, sm.movement_date as datetime, p.product_name,
               sm.movement_type, sm.quantity, sm.reason
        FROM stock_movements sm
        JOIN products p ON sm.product_id = p.id
        WHERE sm.reason IN ('Sale', 'Void Sale', 'Refund Sale')
        ORDER BY sm.movement_date DESC
    """)
    stock_entries = cur.fetchall()

    combined = []
    for entry in stock_entries:
        direction = entry[3]
        product = entry[2]
        qty = entry[4]
        reason = entry[5]

        if direction == 'IN':
            if reason == 'Void Sale':
                desc = f"VOIDED - Restored {qty} units of {product}"
            elif reason == 'Refund Sale':
                desc = f"REFUNDED - Restored {qty} units of {product}"
            else:
                desc = f"+{qty} {product} ({reason})"
        else:
            if reason == 'Sale':
                desc = f"Sold {qty} units of {product}"
            else:
                desc = f"-{qty} {product} ({reason})"

        combined.append({
            'id': entry[0],
            'datetime': entry[1],
            'product_name': product,
            'action': reason,
            'quantity': qty,
            'display_qty': f"+{qty}" if direction == 'IN' else f"-{qty}",
            'movement_type': direction,
            'direction': direction,
            'reason': reason,
            'description': desc,
            'actor': session.get('cashier_user', 'cashier'),
            'source': 'cashier_stock',
        })

    combined.sort(key=lambda x: x['datetime'], reverse=True)
    total = len(combined)
    entries = combined[offset:offset + limit]
    conn.close()

    return jsonify({
        'success': True,
        'entries': entries,
        'total': total,
        'page': page,
        'limit': limit
    })

# =============================
# NOTIFICATIONS API
# =============================

@app.route('/api/notifications')
@admin_required
def get_notifications():
    conn = get_db()
    cur = conn.cursor()

    # Out of stock (stock = 0)
    cur.execute("""
        SELECT id, product_name, stock, barcode 
        FROM products 
        WHERE stock = 0
        AND NOT EXISTS (
            SELECT 1 FROM alert_acknowledgments aa 
            WHERE aa.product_id = products.id AND aa.alert_type = 'out_of_stock'
        )
        ORDER BY product_name ASC
    """)
    out_of_stock = cur.fetchall()

    # Low stock (0 < stock <= threshold)
    cur.execute("""
        SELECT id, product_name, stock, barcode 
        FROM products 
        WHERE stock > 0 AND stock <= ?
        AND NOT EXISTS (
            SELECT 1 FROM alert_acknowledgments aa 
            WHERE aa.product_id = products.id AND aa.alert_type = 'low_stock'
        )
        ORDER BY stock ASC
    """, (LOW_STOCK_THRESHOLD,))
    low_stock = cur.fetchall()

    # Expired
    cur.execute("""
        SELECT id, product_name, stock, barcode, expiration_date
        FROM products 
        WHERE expiration_date < date('now', 'localtime')
        AND expiration_date IS NOT NULL
        AND NOT EXISTS (
            SELECT 1 FROM alert_acknowledgments aa 
            WHERE aa.product_id = products.id AND aa.alert_type = 'expired'
        )
        ORDER BY expiration_date ASC
    """)
    expired = cur.fetchall()

    # Expiring critical (within 7 days)
    cur.execute("""
        SELECT id, product_name, stock, barcode, expiration_date
        FROM products 
        WHERE expiration_date BETWEEN date('now', 'localtime') AND date('now', '+7 days', 'localtime')
        AND expiration_date IS NOT NULL
        AND NOT EXISTS (
            SELECT 1 FROM alert_acknowledgments aa 
            WHERE aa.product_id = products.id AND aa.alert_type = 'expiring_critical'
        )
        ORDER BY expiration_date ASC
    """)
    expiring_critical = cur.fetchall()

    # Expiring warning (within 30 days, not critical)
    cur.execute("""
        SELECT id, product_name, stock, barcode, expiration_date
        FROM products 
        WHERE expiration_date > date('now', '+7 days', 'localtime')
        AND expiration_date <= date('now', '+30 days', 'localtime')
        AND expiration_date IS NOT NULL
        AND NOT EXISTS (
            SELECT 1 FROM alert_acknowledgments aa 
            WHERE aa.product_id = products.id AND aa.alert_type = 'expiring_warning'
        )
        ORDER BY expiration_date ASC
    """)
    expiring_warning = cur.fetchall()

    conn.close()

    return jsonify({
        'out_of_stock': [{'id': p[0], 'name': p[1], 'stock': p[2], 'barcode': p[3]} for p in out_of_stock],
        'low_stock': [{'id': p[0], 'name': p[1], 'stock': p[2], 'barcode': p[3]} for p in low_stock],
        'expired': [{'id': p[0], 'name': p[1], 'stock': p[2], 'barcode': p[3], 'expiry': str(p[4]) if p[4] else None} for p in expired],
        'expiring_critical': [{'id': p[0], 'name': p[1], 'stock': p[2], 'barcode': p[3], 'expiry': str(p[4]) if p[4] else None, 'days_left': 0} for p in expiring_critical],
        'expiring_warning': [{'id': p[0], 'name': p[1], 'stock': p[2], 'barcode': p[3], 'expiry': str(p[4]) if p[4] else None, 'days_left': 0} for p in expiring_warning]
    })

@app.route('/api/cashier/notifications')
@cashier_required
def get_cashier_notifications():
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, product_name, stock, barcode
            FROM products
            WHERE stock <= ?
            AND NOT EXISTS (
                SELECT 1 FROM alert_acknowledgments aa 
                WHERE aa.product_id = products.id AND aa.alert_type = 'low_stock'
            )
            ORDER BY stock ASC
            LIMIT 10
        """, (LOW_STOCK_THRESHOLD,))
        low_stock = cur.fetchall()

        cur.execute("""
            SELECT id, product_name, expiration_date, barcode
            FROM products
            WHERE expiration_date <= date('now', '+30 days', 'localtime')
              AND expiration_date IS NOT NULL
              AND NOT EXISTS (
                  SELECT 1 FROM alert_acknowledgments aa 
                  WHERE aa.product_id = products.id AND aa.alert_type = 'expiring_medical'
              )
            ORDER BY expiration_date ASC
            LIMIT 10
        """)
        expiring = cur.fetchall()

        cur.execute("""
            SELECT id, product_name, expiration_date, barcode
            FROM products
            WHERE expiration_date < date('now', 'localtime')
              AND expiration_date IS NOT NULL
              AND NOT EXISTS (
                  SELECT 1 FROM alert_acknowledgments aa 
                  WHERE aa.product_id = products.id AND aa.alert_type = 'expired'
              )
            ORDER BY expiration_date ASC
            LIMIT 10
        """)
        expired = cur.fetchall()

        return jsonify({
            'low_stock': [{'id': p[0], 'name': p[1], 'stock': p[2], 'barcode': p[3]} for p in low_stock],
            'expiring': [{'id': p[0], 'name': p[1], 'expiry': str(p[2]), 'barcode': p[3]} for p in expiring],
            'expired': [{'id': p[0], 'name': p[1], 'expiry': str(p[2]), 'barcode': p[3]} for p in expired]
        })
    finally:
        conn.close()

# =============================
# CATALOG
# =============================

@app.route('/all_products')
@admin_required
def all_products():
    conn = get_db()
    cur = conn.cursor()
    
    search = request.args.get('search', '').strip()
    query = "SELECT * FROM products"
    params = []
    if search:
        query += " WHERE product_name LIKE ? OR barcode LIKE ?"
        params = [f"%{search}%", f"%{search}%"]
    cur.execute(query, params)
    products = cur.fetchall()
    parsed_products = []
    for p in products:
        expiry = p[7]
        expiry_obj = None
        if expiry:
            try:
                date_part = expiry.split(' ')[0]
                if len(date_part) == 10:
                    expiry_obj = datetime.strptime(date_part, '%Y-%m-%d').date()
            except Exception:
                expiry_obj = None
        parsed_products.append(tuple(p) + (expiry_obj,))
    products = parsed_products
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    conn.close()
    return render_template('all_products.html', products=products,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='inventory', active_sub='all_products',
                           today=datetime.now().date(),
                           search=search)

@app.route('/add_product', methods=['GET', 'POST'])
@admin_required
def add_product():
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        # Check if it's an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.form.get('ajax') == 'true'
        
        barcode = request.form.get('barcode')
        name = request.form.get('product_name')
        category_name = request.form.get('category')  # From template: category
        
        # Validate required fields
        errors = []
        if not barcode or barcode.strip() == '':
            errors.append('Barcode is required')
        if not name or name.strip() == '':
            errors.append('Product name is required')
        if not category_name:
            errors.append('Category is required')
        if not request.form.get('price'):
            errors.append('Price is required')
        if not request.form.get('stock'):
            errors.append('Stock is required')
        
        if errors:
            error_msg = 'Error: ' + ', '.join(errors)
            if is_ajax:
                return jsonify({'success': False, 'message': error_msg})
            else:
                flash(error_msg, 'error')
                # Re-render page
                cur.execute("SELECT id, category_name FROM categories ORDER BY category_name ASC")
                categories = cur.fetchall()
                cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
                low_stock_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
                expiring_count = cur.fetchone()[0]
                conn.close()
                return render_template('add_product.html', 
                               categories=categories, 
                               low_stock_count=low_stock_count,
                               expiring_count=expiring_count,
                               active_main='inventory', 
                               active_sub='add_product')
        
        p_type = category_name  # 'Medical' or 'Non-Medical'
        
        # Convert to proper types
        try:
            price = float(request.form.get('price')) if request.form.get('price') else 0
            stock = int(request.form.get('stock')) if request.form.get('stock') else 0
        except ValueError as e:
            error_msg = f'Invalid price or stock value: {str(e)}'
            if is_ajax:
                return jsonify({'success': False, 'message': error_msg})
            else:
                flash(error_msg, 'error')
                cur.execute("SELECT id, category_name FROM categories ORDER BY category_name ASC")
                categories = cur.fetchall()
                cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
                low_stock_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
                expiring_count = cur.fetchone()[0]
                conn.close()
                return render_template('add_product.html', 
                               categories=categories, 
                               low_stock_count=low_stock_count,
                               expiring_count=expiring_count,
                               active_main='inventory', 
                               active_sub='add_product')
        
        expiry = request.form.get('expiration_date') or None  # From template: expiration_date

        # Get category_id from category name
        cur.execute("SELECT id FROM categories WHERE category_name=?", (category_name,))
        cat_result = cur.fetchone()
        category_id = cat_result[0] if cat_result else None
        
        try:
            # Check if product exists with same name AND expiration date (barcode can be empty or same)
            if barcode:
                cur.execute("""
                    SELECT id, stock FROM products 
                    WHERE product_name = ? AND barcode = ? AND expiration_date = ?
                """, (name, barcode, expiry))
            else:
                cur.execute("""
                    SELECT id, stock FROM products 
                    WHERE product_name = ? AND (barcode IS NULL OR barcode = '') AND expiration_date = ?
                """, (name, expiry))
            existing = cur.fetchone()
            
            if existing:
                # Update stock if product exists with same expiry
                new_stock = existing[1] + int(stock)
                cur.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, existing[0]))
                product_id = existing[0]
                message = f"Stock updated! Added {stock} units. Total: {new_stock}"
                action = 'Stock Update'
            else:
                # Insert new product if different expiry or new product
                query = """
                    INSERT INTO products (product_name, barcode, category_id, product_type, price, stock, expiration_date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                # Set barcode to None if empty
                barcode_value = barcode if barcode else None
                cur.execute(query, (name, barcode_value, category_id, p_type, price, stock, expiry))
                product_id = cur.lastrowid
                message = "Product registered and stock movement logged!"
                action = 'Add New Product'
            
            # Log stock movement
            movement_query = """
                INSERT INTO stock_movements (product_id, movement_type, quantity, reason) 
                VALUES (?, 'IN', ?, 'Stock Addition')
            """
            cur.execute(movement_query, (product_id, stock))
            
            # Log admin activity
            ip_address = request.remote_addr
            if request.headers.get('X-Forwarded-For'):
                ip_address = request.headers.get('X-Forwarded-For')
            
            try:
                cur.execute("""
                    INSERT INTO admin_activity (admin_id, action, ip_address, details)
                    VALUES (?, ?, ?, ?)
                """, (session.get('admin_id'), action, ip_address, f'{name} - {stock} units added'))
            except:
                pass  # Table might not exist yet
            
            conn.commit()
            conn.close()
            
            # Return JSON response for AJAX, render same page for normal form submission (to show flash message)
            if is_ajax:
                return jsonify({'success': True, 'message': message})
            else:
                flash(message, "success")
                # Create new cursor for rendering page
                conn = get_db()
                cur = conn.cursor()
                try:
                    cur.execute("SELECT id, category_name FROM categories ORDER BY category_name ASC")
                    categories = cur.fetchall()
                except Exception as e:
                    categories = []
                    flash(f"Error loading categories: {str(e)}", "error")
                
                cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
                low_stock_count = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
                expiring_count = cur.fetchone()[0]
                conn.close()
                
                return render_template('add_product.html', 
                               categories=categories, 
                               low_stock_count=low_stock_count,
                               expiring_count=expiring_count,
                               active_main='inventory', 
                               active_sub='add_product')
            
        except Exception as e:
            conn.rollback()
            error_str = str(e)
            
            # Provide more specific error messages
            if 'Duplicate entry' in error_str:
                error_message = 'Error: Product with this barcode already exists! Use a different barcode or update the existing product.'
            elif 'foreign key constraint fails' in error_str.lower():
                error_message = 'Error: Invalid category selected. Please select a valid category.'
            elif 'stock_movements' in error_str.lower():
                error_message = 'Error: Could not log stock movement. Please try again.'
            else:
                error_message = f'Database Error: {error_str}'
            
            if is_ajax:
                return jsonify({'success': False, 'message': error_message})
            else:
                flash(error_message, "error")
                # Create new cursor for rendering page after error
                conn = get_db()
                cur = conn.cursor()
                try:
                    cur.execute("SELECT id, category_name FROM categories ORDER BY category_name ASC")
                    categories = cur.fetchall()
                except Exception as ex:
                    categories = []
                    
                cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
                low_stock_count = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
                expiring_count = cur.fetchone()[0]
                conn.close()
                
                return render_template('add_product.html', 
                               categories=categories, 
                               low_stock_count=low_stock_count,
                               expiring_count=expiring_count,
                               active_main='inventory', 
                               active_sub='add_product')
    else:
        # GET request - load categories and counts
        try:
            cur.execute("SELECT id, category_name FROM categories ORDER BY category_name ASC")
            categories = cur.fetchall()
        except Exception as e:
            categories = []
            flash(f"Error loading categories: {str(e)}", "error")
        finally:
            conn.close()
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
        low_stock_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
        expiring_count = cur.fetchone()[0]
        conn.close()
        
        return render_template('add_product.html', 
                               categories=categories, 
                               low_stock_count=low_stock_count,
                               expiring_count=expiring_count,
                               active_main='inventory', 
                               active_sub='add_product')

@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
@admin_required
def delete_product(id):
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'GET':
        cur.execute("SELECT id, product_name, barcode, stock FROM products WHERE id=?", (id,))
        product = cur.fetchone()
        if not product:
            flash("Product not found", "error")
            return redirect(url_for('all_products'))
        
        cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
        low_stock_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
        expiring_count = cur.fetchone()[0]
        
        conn.close()
        return render_template('confirm_delete_product.html', product=product,
                               low_stock_count=low_stock_count,
                               expiring_count=expiring_count,
                               active_main='inventory', active_sub='all_products')
    
    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()
        
        # Get product info before deleting
        cur.execute("SELECT product_name FROM products WHERE id=?", (id,))
        product_info = cur.fetchone()
        product_name = product_info[0] if product_info else "Unknown"
        
        # Delete related records first (stock_movements and sale_items)
        cur.execute("DELETE FROM stock_movements WHERE product_id=?", (id,))
        cur.execute("DELETE FROM sale_items WHERE product_id=?", (id,))
        
        # Now delete the product
        cur.execute("DELETE FROM products WHERE id=?", (id,))
        conn.commit()
        
        # Log admin activity
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            cur.execute("""
                INSERT INTO admin_activity (admin_id, action, ip_address, details)
                VALUES (?, ?, ?, ?)
            """, (session.get('admin_id'), 'Delete Product', ip_address, f'Deleted product: {product_name}'))
            conn.commit()
        except:
            pass
        
        conn.close()
        flash("Product deleted successfully", "success")
        return redirect(url_for('all_products'))

@app.route('/stock_in', methods=['GET', 'POST'])
@admin_required
def stock_in():
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        reason = request.form.get('reason', 'Stock Addition')
        transaction_type = request.form.get('transaction_type', 'IN')
        
        if not product_id or not quantity:
            conn.close()
            flash("Product and quantity are required", "error")
            return redirect(url_for('stock_in'))
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                conn.close()
                flash("Quantity must be greater than 0", "error")
                return redirect(url_for('stock_in'))
        except ValueError:
            conn.close()
            flash("Invalid quantity value", "error")
            return redirect(url_for('stock_in'))
        
        if transaction_type not in ('IN', 'OUT'):
            conn.close()
            flash("Invalid transaction type", "error")
            return redirect(url_for('stock_in'))
        
        cur.execute("SELECT product_name, stock FROM products WHERE id=?", (product_id,))
        product = cur.fetchone()
        if not product:
            conn.close()
            flash("Product not found", "error")
            return redirect(url_for('stock_in'))
        
        product_name = product[0]
        old_stock = product[1]
        
        if transaction_type == 'OUT':
            if quantity > old_stock:
                conn.close()
                flash(f"Cannot remove {quantity} units. Only {old_stock} units available.", "error")
                return redirect(url_for('stock_in'))
            new_stock = old_stock - quantity
            movement_type = 'OUT'
        else:
            new_stock = old_stock + quantity
            movement_type = 'IN'
        
        cur.execute("UPDATE products SET stock=? WHERE id=?", (new_stock, product_id))
        
        cur.execute("""
            INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
            VALUES (?, ?, ?, ?)
        """, (product_id, movement_type, quantity, reason))
        
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        action = "Stock In" if transaction_type == 'IN' else "Stock Out"
        action_type = "Added" if transaction_type == 'IN' else "Removed"
        
        # Verify admin_id exists in admins table before logging
        admin_id = session.get('admin_id')
        cur.execute("SELECT 1 FROM admins WHERE id=?", (admin_id,))
        if cur.fetchone():
            cur.execute("""
                INSERT INTO admin_activity (admin_id, action, ip_address, details)
                VALUES (?, ?, ?, ?)
            """, (admin_id, action, ip_address, f"{product_name} | {action_type}: {quantity} units | Reason: {reason} | Old Stock: {old_stock} | New Stock: {new_stock}"))
        
        conn.commit()
        conn.close()
        flash(f"{action_type} {quantity} units of {product_name} (Total: {new_stock})", "success")
        return redirect(url_for('stock_in'))
    
    cur.execute("""
        SELECT id, product_name, barcode, stock, price
        FROM products
        ORDER BY product_name ASC
    """)
    products = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    conn.close()
    return render_template('stock_in.html', products=products,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='inventory', active_sub='stock_in')

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        barcode = request.form.get('barcode')
        category = request.form.get('category')
        price = request.form.get('price')
        stock = request.form.get('stock')
        expiration_date = request.form.get('expiration_date') or None
        
        if not product_name or not barcode or not category:
            flash("Product name, barcode, and category are required", "error")
            return redirect(url_for('edit_product', id=id))
        
        try:
            price = float(price) if price else 0
            stock = int(stock) if stock else 0
        except ValueError:
            flash("Invalid price or stock value", "error")
            return redirect(url_for('edit_product', id=id))
        
        cur.execute("SELECT id FROM categories WHERE category_name=?", (category,))
        cat_result = cur.fetchone()
        category_id = cat_result[0] if cat_result else None
        
        cur.execute("""
            UPDATE products 
            SET product_name=?, barcode=?, category_id=?, product_type=?, price=?, stock=?, expiration_date=?
            WHERE id=?
        """, (product_name, barcode, category_id, category, price, stock, expiration_date, id))
        
        conn.commit()
        
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            cur.execute("""
                INSERT INTO admin_activity (admin_id, action, ip_address, details)
                VALUES (?, ?, ?, ?)
            """, (session.get('admin_id'), 'Edit Product', ip_address, f'Edited product: {product_name}'))
            conn.commit()
        except:
            pass
        
        conn.close()
        flash("Product updated successfully", "success")
        return redirect(url_for('all_products'))
    
    cur.execute("SELECT * FROM products WHERE id=?", (id,))
    product = cur.fetchone()
    
    cur.execute("SELECT id, category_name FROM categories ORDER BY category_name ASC")
    categories = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    conn.close()
    
    return render_template('edit_product.html', product=product, categories=categories,
                         low_stock_count=low_stock_count,
                         expiring_count=expiring_count,
                         active_main='inventory', active_sub='all_products')

# =============================
# SALES
# =============================

@app.route('/medical_sales')
@admin_required
def medical_sales():
    conn = get_db()
    cur = conn.cursor()

    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    date_clause, date_params = get_date_filter_params(date_from, date_to)

    # Get sales with product names (Medical only, line-item level)
    cur.execute(f"""
        SELECT s.id, s.receipt_number, GROUP_CONCAT(p.product_name, ', ') as products,
               IFNULL(SUM(si.quantity * si.price), 0) as line_total,
               s.sale_status, s.sale_date
        FROM sales s
        LEFT JOIN sale_items si ON s.id = si.sale_id
        LEFT JOIN products p ON si.product_id = p.id
        WHERE s.sale_status = 'Completed'
        AND p.product_type = 'Medical'
        {date_clause}
        GROUP BY s.id
        ORDER BY s.sale_date DESC
    """, date_params)
    sales = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]

    # Use shared analytics engine for medical scope
    conn2 = get_db()
    analytics = calculate_sales_analytics(conn2, date_from, date_to, 'medical')
    conn2.close()

    # Generate business insights
    insights = generate_business_insights(analytics, 'Medical')

    # Check if export is requested
    export_format = request.args.get('export')
    if export_format == 'csv':
        headers = ['ID', 'Receipt Number', 'Products', 'Line Total', 'Status', 'Sale Date']
        filename = f"medical_sales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        conn.close()
        return export_to_csv(sales, headers, filename)

    if export_format == 'excel':
        headers = ['ID', 'Receipt Number', 'Products', 'Line Total', 'Status', 'Sale Date']
        filename = f"medical_sales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        conn.close()
        return export_to_excel(sales, headers, filename, "Medical Sales Report")

    if export_format == 'pdf':
        headers = ['ID', 'Receipt Number', 'Products', 'Line Total', 'Status', 'Sale Date']
        filename = f"medical_sales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        conn.close()
        return export_to_pdf(sales, headers, filename, "Medical Sales Report")

    conn.close()
    return render_template('sales_medical.html', sales=sales,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           date_from=date_from, date_to=date_to,
                           # Analytics variables
                           total_revenue=analytics['total_revenue'],
                           total_transactions=analytics['total_transactions'],
                           total_quantity=analytics['total_quantity'],
                           gross_profit=analytics['gross_profit'],
                           profit_margin=analytics['profit_margin'],
                           sales_growth=analytics['sales_growth'],
                           avg_order_value=analytics['avg_order_value'],
                           best_selling=analytics['best_selling'],
                           trend_labels=analytics['trend_labels'],
                           trend_values=analytics['trend_values'],
                           insights=insights,
                           active_main='sales', active_sub='medical_sales')

@app.route('/sales_dashboard')
@admin_required
def sales_dashboard():
    """Admin sales dashboard with all views"""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    use_custom_range = bool(date_from or date_to)
    
    if use_custom_range and date_from and date_to:
        date_filter = f"AND DATE(s.sale_date) >= '{date_from}' AND DATE(s.sale_date) <= '{date_to}'"
        chart_date_filter = f"AND DATE(s.sale_date) >= '{date_from}' AND DATE(s.sale_date) <= '{date_to}'"
    else:
        date_filter = ""
        chart_date_filter = ""

    # Helper: build WHERE clause for line-item level filtering
    def build_where(extra="", params=None):
        if params is None:
            params = []
        where = f"""
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            JOIN sales s ON si.sale_id = s.id
            WHERE s.sale_status = 'Completed'
            {date_filter}
            {extra}
        """
        return where, params

    # Daily sales (today)
    cur.execute(f"""
        SELECT IFNULL(SUM(CASE WHEN p.product_type = 'Medical' THEN si.quantity * si.price ELSE 0 END), 0),
               IFNULL(SUM(CASE WHEN p.product_type = 'Non-Medical' THEN si.quantity * si.price ELSE 0 END), 0),
               COUNT(DISTINCT s.id)
        {build_where(" AND DATE(s.sale_date) = date('now', 'localtime')")[0]}
    """, build_where(" AND DATE(s.sale_date) = date('now', 'localtime')")[1])
    daily_row = cur.fetchone()
    daily_medical_sales = float(daily_row[0]) if daily_row[0] else 0
    daily_nonmedical_sales = float(daily_row[1]) if daily_row[1] else 0
    daily_sales = daily_medical_sales + daily_nonmedical_sales
    daily_count = int(daily_row[2]) if daily_row[2] else 0

    # Weekly sales (last 7 days)
    cur.execute(f"""
        SELECT IFNULL(SUM(CASE WHEN p.product_type = 'Medical' THEN si.quantity * si.price ELSE 0 END), 0),
               IFNULL(SUM(CASE WHEN p.product_type = 'Non-Medical' THEN si.quantity * si.price ELSE 0 END), 0),
               COUNT(DISTINCT s.id)
        {build_where(" AND s.sale_date >= date('now', '-7 days', 'localtime')")[0]}
    """, build_where(" AND s.sale_date >= date('now', '-7 days', 'localtime')")[1])
    weekly_row = cur.fetchone()
    weekly_medical_sales = float(weekly_row[0]) if weekly_row[0] else 0
    weekly_nonmedical_sales = float(weekly_row[1]) if weekly_row[1] else 0
    weekly_sales = weekly_medical_sales + weekly_nonmedical_sales
    weekly_count = int(weekly_row[2]) if weekly_row[2] else 0

    # Monthly sales (this month)
    cur.execute(f"""
        SELECT IFNULL(SUM(CASE WHEN p.product_type = 'Medical' THEN si.quantity * si.price ELSE 0 END), 0),
               IFNULL(SUM(CASE WHEN p.product_type = 'Non-Medical' THEN si.quantity * si.price ELSE 0 END), 0),
               COUNT(DISTINCT s.id)
        {build_where(" AND strftime('%m', s.sale_date) = strftime('%m', 'now') AND strftime('%Y', s.sale_date) = strftime('%Y', 'now')")[0]}
    """, build_where(" AND strftime('%m', s.sale_date) = strftime('%m', 'now') AND strftime('%Y', s.sale_date) = strftime('%Y', 'now')")[1])
    monthly_row = cur.fetchone()
    monthly_medical_sales = float(monthly_row[0]) if monthly_row[0] else 0
    monthly_nonmedical_sales = float(monthly_row[1]) if monthly_row[1] else 0
    monthly_sales = monthly_medical_sales + monthly_nonmedical_sales
    monthly_count = int(monthly_row[2]) if monthly_row[2] else 0

    # Yearly sales (this year)
    cur.execute(f"""
        SELECT IFNULL(SUM(CASE WHEN p.product_type = 'Medical' THEN si.quantity * si.price ELSE 0 END), 0),
               IFNULL(SUM(CASE WHEN p.product_type = 'Non-Medical' THEN si.quantity * si.price ELSE 0 END), 0),
               COUNT(DISTINCT s.id)
        {build_where(" AND strftime('%Y', s.sale_date) = strftime('%Y', 'now')")[0]}
    """, build_where(" AND strftime('%Y', s.sale_date) = strftime('%Y', 'now')")[1])
    yearly_row = cur.fetchone()
    yearly_medical_sales = float(yearly_row[0]) if yearly_row[0] else 0
    yearly_nonmedical_sales = float(yearly_row[1]) if yearly_row[1] else 0
    yearly_sales = yearly_medical_sales + yearly_nonmedical_sales
    yearly_count = int(yearly_row[2]) if yearly_row[2] else 0

    # Overall sales
    cur.execute(f"""
        SELECT IFNULL(SUM(CASE WHEN p.product_type = 'Medical' THEN si.quantity * si.price ELSE 0 END), 0),
               IFNULL(SUM(CASE WHEN p.product_type = 'Non-Medical' THEN si.quantity * si.price ELSE 0 END), 0),
               COUNT(DISTINCT s.id)
        {build_where()[0]}
    """, build_where()[1])
    overall_row = cur.fetchone()
    overall_medical_sales = float(overall_row[0]) if overall_row[0] else 0
    overall_nonmedical_sales = float(overall_row[1]) if overall_row[1] else 0
    overall_sales = overall_medical_sales + overall_nonmedical_sales
    overall_count = int(overall_row[2]) if overall_row[2] else 0
    
    # Popular products (top 10)
    cur.execute(f"""
        SELECT p.product_name, SUM(si.quantity) as total_qty, SUM(si.quantity * si.price) as total_sales
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        JOIN sales s ON si.sale_id = s.id
        WHERE s.sale_status = 'Completed' {date_filter if use_custom_range else ''}
        GROUP BY p.id, p.product_name
        ORDER BY total_qty DESC
        LIMIT 10
    """)
    popular = cur.fetchall()
    
    # Daily sales for chart - Medical (last 30 days or custom range)
    if use_custom_range and date_from and date_to:
        cur.execute(f"""
            SELECT DATE(s.sale_date) as day, IFNULL(SUM(si.quantity * si.price), 0) as daily_total
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            JOIN sales s ON si.sale_id = s.id
            WHERE s.sale_status = 'Completed' AND p.product_type = 'Medical' {date_filter}
            GROUP BY DATE(s.sale_date)
            ORDER BY day ASC
        """)
    else:
        cur.execute(f"""
            SELECT DATE(s.sale_date) as day, IFNULL(SUM(si.quantity * si.price), 0) as daily_total
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            JOIN sales s ON si.sale_id = s.id
            WHERE s.sale_status = 'Completed' AND p.product_type = 'Medical'
            AND s.sale_date >= date('now', '-30 days', 'localtime')
            GROUP BY DATE(s.sale_date)
            ORDER BY day ASC
        """)
    chart_medical = cur.fetchall()
    medical_labels = [str(row[0]) for row in chart_medical]
    medical_values = [float(row[1]) for row in chart_medical]
    
    # Daily sales for chart - Non-Medical (last 30 days or custom range)
    if use_custom_range and date_from and date_to:
        cur.execute(f"""
            SELECT DATE(s.sale_date) as day, IFNULL(SUM(si.quantity * si.price), 0) as daily_total
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            JOIN sales s ON si.sale_id = s.id
            WHERE s.sale_status = 'Completed' AND p.product_type = 'Non-Medical' {date_filter}
            GROUP BY DATE(s.sale_date)
            ORDER BY day ASC
        """)
    else:
        cur.execute(f"""
            SELECT DATE(s.sale_date) as day, IFNULL(SUM(si.quantity * si.price), 0) as daily_total
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            JOIN sales s ON si.sale_id = s.id
            WHERE s.sale_status = 'Completed' AND p.product_type = 'Non-Medical'
            AND s.sale_date >= date('now', '-30 days', 'localtime')
            GROUP BY DATE(s.sale_date)
            ORDER BY day ASC
        """)
    chart_nonmedical = cur.fetchall()
    nonmedical_labels = [str(row[0]) for row in chart_nonmedical]
    nonmedical_values = [float(row[1]) for row in chart_nonmedical]
    
    # Use medical labels as primary
    chart_labels = medical_labels
    chart_values = medical_values
    
    # Check if CSV export is requested
    if request.args.get('export') == 'csv':
        # Export all sales with details (line-item level for mixed transactions)
        cur.execute(f"""
            SELECT s.id, s.receipt_number, 
                   IFNULL(SUM(si.quantity * si.price), 0) as total_amount,
                   s.sale_status,
                   CASE 
                     WHEN SUM(CASE WHEN p.product_type = 'Medical' THEN 1 ELSE 0 END) > 0 
                          AND SUM(CASE WHEN p.product_type = 'Non-Medical' THEN 1 ELSE 0 END) > 0 THEN 'Mixed'
                     WHEN SUM(CASE WHEN p.product_type = 'Medical' THEN 1 ELSE 0 END) > 0 THEN 'Medical'
                     WHEN SUM(CASE WHEN p.product_type = 'Non-Medical' THEN 1 ELSE 0 END) > 0 THEN 'Non-Medical'
                     ELSE 'Unknown'
                   END as product_type,
                   s.sale_date,
                   c.full_name as cashier_name
            FROM sales s
            LEFT JOIN sale_items si ON s.id = si.sale_id
            LEFT JOIN products p ON si.product_id = p.id
            LEFT JOIN cashiers c ON s.cashier_id = c.id
            WHERE s.sale_status = 'Completed' {date_filter if use_custom_range else ''}
            GROUP BY s.id
            ORDER BY s.sale_date DESC
        """)
        all_sales = cur.fetchall()
        headers = ['ID', 'Receipt Number', 'Total Amount', 'Status', 'Product Type', 'Sale Date', 'Cashier']
        filename = f"all_sales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        conn.close()
        return export_to_csv(all_sales, headers, filename)

    if request.args.get('export') == 'excel':
        cur.execute(f"""
            SELECT s.id, s.receipt_number, 
                   IFNULL(SUM(si.quantity * si.price), 0) as total_amount,
                   s.sale_status,
                   CASE 
                     WHEN SUM(CASE WHEN p.product_type = 'Medical' THEN 1 ELSE 0 END) > 0 
                          AND SUM(CASE WHEN p.product_type = 'Non-Medical' THEN 1 ELSE 0 END) > 0 THEN 'Mixed'
                     WHEN SUM(CASE WHEN p.product_type = 'Medical' THEN 1 ELSE 0 END) > 0 THEN 'Medical'
                     WHEN SUM(CASE WHEN p.product_type = 'Non-Medical' THEN 1 ELSE 0 END) > 0 THEN 'Non-Medical'
                     ELSE 'Unknown'
                   END as product_type,
                   s.sale_date,
                   c.full_name as cashier_name
            FROM sales s
            LEFT JOIN sale_items si ON s.id = si.sale_id
            LEFT JOIN products p ON si.product_id = p.id
            LEFT JOIN cashiers c ON s.cashier_id = c.id
            WHERE s.sale_status = 'Completed' {date_filter if use_custom_range else ''}
            GROUP BY s.id
            ORDER BY s.sale_date DESC
        """)
        all_sales = cur.fetchall()
        headers = ['ID', 'Receipt Number', 'Total Amount', 'Status', 'Product Type', 'Sale Date', 'Cashier']
        filename = f"all_sales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        conn.close()
        return export_to_excel(all_sales, headers, filename, "All Sales Report")

    if request.args.get('export') == 'pdf':
        cur.execute(f"""
            SELECT s.id, s.receipt_number, 
                   IFNULL(SUM(si.quantity * si.price), 0) as total_amount,
                   s.sale_status,
                   CASE 
                     WHEN SUM(CASE WHEN p.product_type = 'Medical' THEN 1 ELSE 0 END) > 0 
                          AND SUM(CASE WHEN p.product_type = 'Non-Medical' THEN 1 ELSE 0 END) > 0 THEN 'Mixed'
                     WHEN SUM(CASE WHEN p.product_type = 'Medical' THEN 1 ELSE 0 END) > 0 THEN 'Medical'
                     WHEN SUM(CASE WHEN p.product_type = 'Non-Medical' THEN 1 ELSE 0 END) > 0 THEN 'Non-Medical'
                     ELSE 'Unknown'
                   END as product_type,
                   s.sale_date,
                   c.full_name as cashier_name
            FROM sales s
            LEFT JOIN sale_items si ON s.id = si.sale_id
            LEFT JOIN products p ON si.product_id = p.id
            LEFT JOIN cashiers c ON s.cashier_id = c.id
            WHERE s.sale_status = 'Completed' {date_filter if use_custom_range else ''}
            GROUP BY s.id
            ORDER BY s.sale_date DESC
        """)
        all_sales = cur.fetchall()
        headers = ['ID', 'Receipt Number', 'Total Amount', 'Status', 'Product Type', 'Sale Date', 'Cashier']
        filename = f"all_sales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        conn.close()
        return export_to_pdf(all_sales, headers, filename, "All Sales Report")

    conn.close()

    # Use shared analytics engine for overall scope
    conn2 = get_db()
    analytics = calculate_sales_analytics(conn2, date_from, date_to, 'overall')
    conn2.close()

    # Generate business insights
    insights = generate_business_insights(analytics, 'Overall')

    return render_template('sales_dashboard.html',
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           daily_sales=daily_sales, daily_count=daily_count,
                           daily_medical_sales=daily_medical_sales,
                           daily_nonmedical_sales=daily_nonmedical_sales,
                           weekly_sales=weekly_sales, weekly_count=weekly_count,
                           weekly_medical_sales=weekly_medical_sales,
                           weekly_nonmedical_sales=weekly_nonmedical_sales,
                           monthly_sales=monthly_sales, monthly_count=monthly_count,
                           monthly_medical_sales=monthly_medical_sales,
                           monthly_nonmedical_sales=monthly_nonmedical_sales,
                           yearly_sales=yearly_sales, yearly_count=yearly_count,
                           yearly_medical_sales=yearly_medical_sales,
                           yearly_nonmedical_sales=yearly_nonmedical_sales,
                           overall_sales=overall_sales, overall_count=overall_count,
                           overall_medical_sales=overall_medical_sales,
                           overall_nonmedical_sales=overall_nonmedical_sales,
                           popular=popular,
                           chart_labels=chart_labels, chart_values=chart_values,
                           medical_labels=medical_labels, medical_values=medical_values,
                           nonmedical_labels=nonmedical_labels, nonmedical_values=nonmedical_values,
                           date_from=date_from, date_to=date_to,
                           # New analytics variables
                           total_quantity=analytics['total_quantity'],
                           gross_profit=analytics['gross_profit'],
                           profit_margin=analytics['profit_margin'],
                           sales_growth=analytics['sales_growth'],
                           avg_order_value=analytics['avg_order_value'],
                           best_selling=analytics['best_selling'],
                           trend_labels=analytics['trend_labels'],
                           trend_values=analytics['trend_values'],
                           insights=insights,
                           active_main='sales', active_sub='sales_dashboard')

@app.route('/non_medical_sales')
@admin_required
def non_medical_sales():
    conn = get_db()
    cur = conn.cursor()

    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    date_clause, date_params = get_date_filter_params(date_from, date_to)

    # Get sales with product names (Non-Medical only, line-item level)
    cur.execute(f"""
        SELECT s.id, s.receipt_number, GROUP_CONCAT(p.product_name, ', ') as products,
               IFNULL(SUM(si.quantity * si.price), 0) as line_total,
               s.sale_status, s.sale_date
        FROM sales s
        LEFT JOIN sale_items si ON s.id = si.sale_id
        LEFT JOIN products p ON si.product_id = p.id
        WHERE s.sale_status = 'Completed'
        AND p.product_type = 'Non-Medical'
        {date_clause}
        GROUP BY s.id
        ORDER BY s.sale_date DESC
    """, date_params)
    sales = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]

    # Use shared analytics engine for non_medical scope
    conn2 = get_db()
    analytics = calculate_sales_analytics(conn2, date_from, date_to, 'non_medical')
    conn2.close()

    # Generate business insights
    insights = generate_business_insights(analytics, 'Non-Medical')

    # Check if export is requested
    export_format = request.args.get('export')
    if export_format == 'csv':
        headers = ['ID', 'Receipt Number', 'Products', 'Line Total', 'Status', 'Sale Date']
        filename = f"non_medical_sales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        conn.close()
        return export_to_csv(sales, headers, filename)

    if export_format == 'excel':
        headers = ['ID', 'Receipt Number', 'Products', 'Line Total', 'Status', 'Sale Date']
        filename = f"non_medical_sales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        conn.close()
        return export_to_excel(sales, headers, filename, "Non-Medical Sales Report")

    if export_format == 'pdf':
        headers = ['ID', 'Receipt Number', 'Products', 'Line Total', 'Status', 'Sale Date']
        filename = f"non_medical_sales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        conn.close()
        return export_to_pdf(sales, headers, filename, "Non-Medical Sales Report")

    conn.close()
    return render_template('sales_non_medical.html', sales=sales,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           date_from=date_from, date_to=date_to,
                           # Analytics variables
                           total_revenue=analytics['total_revenue'],
                           total_transactions=analytics['total_transactions'],
                           total_quantity=analytics['total_quantity'],
                           gross_profit=analytics['gross_profit'],
                           profit_margin=analytics['profit_margin'],
                           sales_growth=analytics['sales_growth'],
                           avg_order_value=analytics['avg_order_value'],
                           best_selling=analytics['best_selling'],
                           trend_labels=analytics['trend_labels'],
                           trend_values=analytics['trend_values'],
                           insights=insights,
                            active_main='sales', active_sub='non_medical_sales')

# =============================
# MANUAL SALES ENTRY
# =============================

@app.route('/manual_sales_entry')
@admin_required
def manual_sales_entry():
    conn = get_db()
    cur = conn.cursor()

    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    date_clause, date_params = get_date_filter_params(date_from, date_to)
    source_filter = ""
    source_params = []
    source = request.args.get('source', '').strip()
    if source:
        source_filter = " AND s.source = ?"
        source_params = [source]

    # Get manual sales records
    cur.execute(f"""
        SELECT s.id, s.receipt_number, s.sale_date, s.customer_name,
               s.total_amount, s.sale_status, s.source, s.date_encoded,
               a.username as encoded_by, s.payment_method, s.discount, s.notes,
               (SELECT COUNT(*) FROM sale_items si WHERE si.sale_id = s.id) as item_count
        FROM sales s
        LEFT JOIN admins a ON s.cashier_id = a.id
        WHERE s.source = 'MANUAL'
        {date_clause}
        {source_filter}
        ORDER BY s.sale_date DESC, s.id DESC
    """, date_params + source_params)
    manual_sales = cur.fetchall()

    # Get all products for the form dropdown
    cur.execute("SELECT id, product_name, product_type, price FROM products WHERE stock >= 0 ORDER BY product_name")
    products = cur.fetchall()

    conn.close()
    return render_template('manual_sales_entry.html',
                           manual_sales=manual_sales,
                           products=products,
                           date_from=date_from, date_to=date_to,
                           source=source,
                           active_main='sales', active_sub='manual_sales_entry')


@app.route('/api/manual_sales_entry', methods=['POST'])
@admin_required
def api_manual_sales_entry():
    """Save a manual historical sale without inventory deduction."""
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format'})

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data received'})

    # Validate required fields
    transaction_date = data.get('transaction_date', '').strip()
    receipt_number = data.get('receipt_number', '').strip()
    items = data.get('items', [])
    payment_method = data.get('payment_method', '').strip()
    customer_name = data.get('customer_name', '').strip()
    discount = float(data.get('discount', 0) or 0)
    notes = data.get('notes', '').strip()

    if not transaction_date:
        return jsonify({'success': False, 'message': 'Transaction date is required'})
    if not receipt_number:
        return jsonify({'success': False, 'message': 'Receipt number is required'})
    if not items or len(items) == 0:
        return jsonify({'success': False, 'message': 'At least one product is required'})
    if not payment_method:
        return jsonify({'success': False, 'message': 'Payment method is required'})

    # Check for duplicate receipt number
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM sales WHERE receipt_number = ?", (receipt_number,))
        if cur.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': f'Receipt number {receipt_number} already exists'})

        # Calculate totals from line items
        total_amount = 0.0
        validated_items = []
        for item in items:
            product_id = int(item.get('product_id'))
            quantity = int(item.get('quantity'))
            unit_price = float(item.get('unit_price', 0))

            if product_id <= 0 or quantity <= 0 or unit_price < 0:
                conn.close()
                return jsonify({'success': False, 'message': 'Invalid item data'})

            # Verify product exists
            cur.execute("SELECT product_name, product_type FROM products WHERE id = ?", (product_id,))
            prod = cur.fetchone()
            if not prod:
                conn.close()
                return jsonify({'success': False, 'message': f'Product ID {product_id} not found'})

            subtotal = round(quantity * unit_price, 2)
            total_amount += subtotal
            validated_items.append({
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'subtotal': subtotal,
                'product_name': prod[0],
                'product_type': prod[1]
            })

        # Apply discount
        total_amount = round(total_amount - discount, 2)
        if total_amount < 0:
            total_amount = 0.0

        # Generate a unique receipt prefix for manual sales
        manual_receipt = receipt_number

        # Determine product_type for the sale header (mixed = 'Mixed')
        has_medical = any(i['product_type'] == 'Medical' for i in validated_items)
        has_nonmedical = any(i['product_type'] == 'Non-Medical' for i in validated_items)
        if has_medical and has_nonmedical:
            sale_product_type = 'Mixed'
        elif has_medical:
            sale_product_type = 'Medical'
        else:
            sale_product_type = 'Non-Medical'

        # Insert sale header (NO inventory deduction)
        admin_id = session.get('admin_id')
        # For manual sales, need a valid cashier_id (FK constraint)
        cur.execute("SELECT id FROM cashiers LIMIT 1")
        cashier_row = cur.fetchone()
        if cashier_row:
            cashier_id_for_sale = cashier_row[0]
        else:
            from werkzeug.security import generate_password_hash
            cur.execute("INSERT INTO cashiers (full_name, username, password, status) VALUES ('Manual Entry', 'manual_system', ?, 'active')", (generate_password_hash('manual_system'),))
            cashier_id_for_sale = cur.lastrowid
        cur.execute("""
            INSERT INTO sales (receipt_number, cashier_id, total_amount, sale_status,
                               product_type, sale_date, source, date_encoded,
                               customer_name, discount, payment_method, notes)
            VALUES (?, ?, ?, 'Completed', ?, ?, 'MANUAL', datetime('now', 'localtime'),
                    ?, ?, ?, ?)
        """, (manual_receipt, cashier_id_for_sale, total_amount, sale_product_type, transaction_date,
              customer_name, discount, payment_method, notes))

        sale_id = cur.lastrowid

        # Insert sale items
        for item in validated_items:
            cur.execute("""
                INSERT INTO sale_items (sale_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            """, (sale_id, item['product_id'], item['quantity'], item['unit_price']))

        # Log admin activity
        cur.execute("""
            INSERT INTO admin_activity (admin_id, action, ip_address, details)
            VALUES (?, ?, ?, ?)
        """, (admin_id, 'Manual Sale Entry', request.remote_addr,
              f"Receipt: {manual_receipt}, Date: {transaction_date}, Total: ₱{total_amount:,.2f}, Source: MANUAL"))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Manual sale recorded successfully',
            'sale_id': sale_id,
            'receipt_number': manual_receipt,
            'total_amount': total_amount
        })

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/manual_sales/<int:sale_id>', methods=['GET'])
@admin_required
def api_get_manual_sale(sale_id):
    """Get details of a manual sale."""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.id, s.receipt_number, s.sale_date, s.customer_name,
               s.total_amount, s.sale_status, s.source, s.date_encoded,
               s.payment_method, s.discount, s.notes,
               a.username as encoded_by
        FROM sales s
        LEFT JOIN admins a ON s.cashier_id = a.id
        WHERE s.id = ? AND s.source = 'MANUAL'
    """, (sale_id,))
    sale = cur.fetchone()

    if not sale:
        conn.close()
        return jsonify({'success': False, 'message': 'Manual sale not found'}), 404

    cur.execute("""
        SELECT si.id, si.product_id, p.product_name, p.product_type,
               si.quantity, si.price, (si.quantity * si.price) as subtotal
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        WHERE si.sale_id = ?
    """, (sale_id,))
    items = cur.fetchall()

    conn.close()

    return jsonify({
        'success': True,
        'sale': {
            'id': sale[0],
            'receipt_number': sale[1],
            'transaction_date': sale[2],
            'customer_name': sale[3],
            'total_amount': sale[4],
            'sale_status': sale[5],
            'source': sale[6],
            'date_encoded': sale[7],
            'payment_method': sale[8],
            'discount': sale[9],
            'notes': sale[10],
            'encoded_by': sale[11]
        },
        'items': [
            {
                'id': row[0],
                'product_id': row[1],
                'product_name': row[2],
                'product_type': row[3],
                'quantity': row[4],
                'unit_price': row[5],
                'subtotal': row[6]
            } for row in items
        ]
    })


@app.route('/api/manual_sales/<int:sale_id>', methods=['PUT'])
@admin_required
def api_edit_manual_sale(sale_id):
    """Edit a manual sale."""
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format'})

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data received'})

    transaction_date = data.get('transaction_date', '').strip()
    receipt_number = data.get('receipt_number', '').strip()
    items = data.get('items', [])
    payment_method = data.get('payment_method', '').strip()
    customer_name = data.get('customer_name', '').strip()
    discount = float(data.get('discount', 0) or 0)
    notes = data.get('notes', '').strip()
    reason = data.get('reason', '').strip()

    if not transaction_date:
        return jsonify({'success': False, 'message': 'Transaction date is required'})
    if not receipt_number:
        return jsonify({'success': False, 'message': 'Receipt number is required'})
    if not items or len(items) == 0:
        return jsonify({'success': False, 'message': 'At least one product is required'})
    if not payment_method:
        return jsonify({'success': False, 'message': 'Payment method is required'})
    if not reason:
        return jsonify({'success': False, 'message': 'Reason for correction is required'})

    conn = get_db()
    cur = conn.cursor()
    try:
        # Verify sale exists and is manual
        cur.execute("""
            SELECT s.id, s.receipt_number, s.sale_date, s.customer_name,
                   s.total_amount, s.sale_status, s.source, s.payment_method,
                   s.discount, s.notes
            FROM sales s
            WHERE s.id = ? AND s.source = 'MANUAL'
        """, (sale_id,))
        sale = cur.fetchone()
        if not sale:
            conn.close()
            return jsonify({'success': False, 'message': 'Manual sale not found'}), 404

        # Block editing if already voided
        if sale[5] == 'Voided':
            conn.close()
            return jsonify({'success': False, 'message': 'Cannot edit a voided transaction. Restore it first.'}), 400

        old_receipt = sale[1]

        # Capture previous values for audit
        previous_values = {
            'receipt_number': sale[1],
            'sale_date': sale[2],
            'customer_name': sale[3],
            'total_amount': sale[4],
            'sale_status': sale[5],
            'payment_method': sale[7],
            'discount': sale[8],
            'notes': sale[9]
        }

        # Get previous items for audit
        cur.execute("""
            SELECT si.product_id, si.quantity, si.price
            FROM sale_items si
            WHERE si.sale_id = ?
        """, (sale_id,))
        prev_items = cur.fetchall()
        previous_values['items'] = [
            {'product_id': row[0], 'quantity': row[1], 'unit_price': row[2]}
            for row in prev_items
        ]

        # Check for duplicate receipt (excluding current sale)
        cur.execute("SELECT id FROM sales WHERE receipt_number = ? AND id != ?", (receipt_number, sale_id))
        if cur.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': f'Receipt number {receipt_number} already exists'})

        # Calculate totals from line items
        total_amount = 0.0
        validated_items = []
        for item in items:
            product_id = int(item.get('product_id'))
            quantity = int(item.get('quantity'))
            unit_price = float(item.get('unit_price', 0))

            if product_id <= 0 or quantity <= 0 or unit_price < 0:
                conn.close()
                return jsonify({'success': False, 'message': 'Invalid item data'})

            cur.execute("SELECT product_name, product_type FROM products WHERE id = ?", (product_id,))
            prod = cur.fetchone()
            if not prod:
                conn.close()
                return jsonify({'success': False, 'message': f'Product ID {product_id} not found'})

            subtotal = round(quantity * unit_price, 2)
            total_amount += subtotal
            validated_items.append({
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'subtotal': subtotal,
                'product_name': prod[0],
                'product_type': prod[1]
            })

        total_amount = round(total_amount - discount, 2)
        if total_amount < 0:
            total_amount = 0.0

        has_medical = any(i['product_type'] == 'Medical' for i in validated_items)
        has_nonmedical = any(i['product_type'] == 'Non-Medical' for i in validated_items)
        if has_medical and has_nonmedical:
            sale_product_type = 'Mixed'
        elif has_medical:
            sale_product_type = 'Medical'
        else:
            sale_product_type = 'Non-Medical'

        admin_id = session.get('admin_id')

        # Update sale header
        cur.execute("""
            UPDATE sales
            SET receipt_number = ?, total_amount = ?, product_type = ?, sale_date = ?,
                customer_name = ?, discount = ?, payment_method = ?, notes = ?
            WHERE id = ? AND source = 'MANUAL'
        """, (receipt_number, total_amount, sale_product_type, transaction_date,
              customer_name, discount, payment_method, notes, sale_id))

        # Delete old items and re-insert
        cur.execute("DELETE FROM sale_items WHERE sale_id = ?", (sale_id,))
        for item in validated_items:
            cur.execute("""
                INSERT INTO sale_items (sale_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            """, (sale_id, item['product_id'], item['quantity'], item['unit_price']))

        # Capture updated values for audit
        updated_values = {
            'receipt_number': receipt_number,
            'sale_date': transaction_date,
            'customer_name': customer_name,
            'total_amount': total_amount,
            'sale_status': 'Completed',
            'payment_method': payment_method,
            'discount': discount,
            'notes': notes,
            'items': [
                {'product_id': item['product_id'], 'quantity': item['quantity'], 'unit_price': item['unit_price']}
                for item in validated_items
            ]
        }

        # Log detailed audit trail in manual_sales_audit table
        import json
        cur.execute("""
            INSERT INTO manual_sales_audit (sale_id, action, previous_values, updated_values, admin_id, reason)
            VALUES (?, 'EDITED', ?, ?, ?, ?)
        """, (sale_id, json.dumps(previous_values), json.dumps(updated_values), admin_id, reason))

        # Also log to admin_activity for backward compatibility
        cur.execute("""
            INSERT INTO admin_activity (admin_id, action, ip_address, details)
            VALUES (?, ?, ?, ?)
        """, (admin_id, 'Manual Sale Edited', request.remote_addr,
              f"Sale ID: {sale_id}, Old Receipt: {old_receipt}, New Receipt: {receipt_number}, "
              f"Date: {transaction_date}, Total: ₱{total_amount:,.2f}, Reason: {reason}"))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Manual sale updated successfully',
            'sale_id': sale_id,
            'total_amount': total_amount
        })

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/manual_sales/<int:sale_id>', methods=['DELETE'])
@admin_required
def api_void_manual_sale(sale_id):
    """Void a manual sale (soft delete)."""
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format'})

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data received'})

    reason = data.get('reason', '').strip()
    if not reason:
        return jsonify({'success': False, 'message': 'Void reason is required'})

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT s.id, s.receipt_number, s.sale_date, s.total_amount, s.source, s.sale_status
            FROM sales s
            WHERE s.id = ? AND s.source = 'MANUAL'
        """, (sale_id,))
        sale = cur.fetchone()
        if not sale:
            conn.close()
            return jsonify({'success': False, 'message': 'Manual sale not found'}), 404

        # Block voiding if already voided
        if sale[5] == 'Voided':
            conn.close()
            return jsonify({'success': False, 'message': 'Transaction is already voided'}), 400

        admin_id = session.get('admin_id')

        # Capture previous values for audit
        import json
        previous_values = {
            'receipt_number': sale[1],
            'sale_date': sale[2],
            'total_amount': sale[3],
            'source': sale[4],
            'sale_status': sale[5]
        }
        updated_values = {
            'sale_status': 'Voided',
            'voided_reason': reason,
            'voided_by': admin_id
        }

        cur.execute("""
            UPDATE sales
            SET sale_status = 'Voided', voided_at = datetime('now', 'localtime'),
                voided_by = ?, void_reason = ?
            WHERE id = ? AND source = 'MANUAL'
        """, (admin_id, reason, sale_id))

        # Log detailed audit trail in manual_sales_audit table
        cur.execute("""
            INSERT INTO manual_sales_audit (sale_id, action, previous_values, updated_values, admin_id, reason)
            VALUES (?, 'VOIDED', ?, ?, ?, ?)
        """, (sale_id, json.dumps(previous_values), json.dumps(updated_values), admin_id, reason))

        # Also log to admin_activity for backward compatibility
        cur.execute("""
            INSERT INTO admin_activity (admin_id, action, ip_address, details)
            VALUES (?, ?, ?, ?)
        """, (admin_id, 'Manual Sale Voided', request.remote_addr,
              f"Sale ID: {sale_id}, Receipt: {sale[1]}, Total: ₱{float(sale[3]):,.2f}, Reason: {reason}"))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Manual sale voided successfully',
            'sale_id': sale_id
        })

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/manual_sales/<int:sale_id>/restore', methods=['POST'])
@admin_required
def api_restore_manual_sale(sale_id):
    """Restore a voided manual sale."""
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format'})

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data received'})

    reason = data.get('reason', '').strip()
    if not reason:
        return jsonify({'success': False, 'message': 'Restoration reason is required'})

    conn = get_db()
    cur = conn.cursor()
    try:
        # Verify sale exists, is manual, and is voided
        cur.execute("""
            SELECT s.id, s.receipt_number, s.sale_date, s.source, s.sale_status
            FROM sales s
            WHERE s.id = ? AND s.source = 'MANUAL'
        """, (sale_id,))
        sale = cur.fetchone()
        if not sale:
            conn.close()
            return jsonify({'success': False, 'message': 'Manual sale not found'}), 404

        # Block restoring if not voided
        if sale[4] != 'Voided':
            conn.close()
            return jsonify({'success': False, 'message': 'Only voided transactions can be restored'}), 400

        admin_id = session.get('admin_id')

        # Check for duplicate receipt number (another active sale with same receipt)
        cur.execute("SELECT id FROM sales WHERE receipt_number = ? AND id != ? AND sale_status != 'Voided'", (sale[1], sale_id))
        if cur.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': f'Cannot restore: receipt number {sale[1]} is already in use by an active transaction'})

        # Capture previous values for audit
        import json
        previous_values = {
            'receipt_number': sale[1],
            'sale_date': sale[2],
            'source': sale[3],
            'sale_status': sale[4]
        }
        updated_values = {
            'sale_status': 'Completed',
            'restored_reason': reason,
            'restored_by': admin_id
        }

        cur.execute("""
            UPDATE sales
            SET sale_status = 'Completed', voided_at = NULL,
                voided_by = NULL, void_reason = NULL
            WHERE id = ? AND source = 'MANUAL'
        """, (sale_id,))

        # Log detailed audit trail in manual_sales_audit table
        cur.execute("""
            INSERT INTO manual_sales_audit (sale_id, action, previous_values, updated_values, admin_id, reason)
            VALUES (?, 'RESTORED', ?, ?, ?, ?)
        """, (sale_id, json.dumps(previous_values), json.dumps(updated_values), admin_id, reason))

        # Also log to admin_activity for backward compatibility
        cur.execute("""
            INSERT INTO admin_activity (admin_id, action, ip_address, details)
            VALUES (?, ?, ?, ?)
        """, (admin_id, 'Manual Sale Restored', request.remote_addr,
              f"Sale ID: {sale_id}, Receipt: {sale[1]}, Reason: {reason}"))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Manual sale restored successfully',
            'sale_id': sale_id
        })

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/products_search')
@admin_required
def api_products_search():
    """Search products for manual sales entry form."""
    q = request.args.get('q', '').strip()
    conn = get_db()
    cur = conn.cursor()
    if q:
        cur.execute("SELECT id, product_name, product_type, price FROM products WHERE product_name LIKE ? ORDER BY product_name LIMIT 20", (f'%{q}%',))
    else:
        cur.execute("SELECT id, product_name, product_type, price FROM products ORDER BY product_name LIMIT 50")
    products = cur.fetchall()
    conn.close()
    return jsonify({
        'success': True,
        'products': [
            {
                'id': row[0],
                'name': row[1],
                'type': row[2],
                'price': row[3]
            } for row in products
        ]
    })


@app.route('/api/manual_sales_audit/<int:sale_id>', methods=['GET'])
@admin_required
def api_manual_sales_audit(sale_id):
    """Get audit history for a manual sale."""
    # Verify sale exists and is manual
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, receipt_number FROM sales WHERE id = ? AND source = 'MANUAL'", (sale_id,))
    sale = cur.fetchone()
    if not sale:
        conn.close()
        return jsonify({'success': False, 'message': 'Manual sale not found'}), 404

    cur.execute("""
        SELECT msa.id, msa.action, msa.previous_values, msa.updated_values,
               msa.admin_id, msa.action_timestamp, msa.reason,
               a.username as admin_name
        FROM manual_sales_audit msa
        LEFT JOIN admins a ON msa.admin_id = a.id
        WHERE msa.sale_id = ?
        ORDER BY msa.action_timestamp DESC
    """, (sale_id,))
    audits = cur.fetchall()
    conn.close()

    import json
    audit_list = []
    for row in audits:
        audit_list.append({
            'id': row[0],
            'action': row[1],
            'previous_values': json.loads(row[2]) if row[2] else None,
            'updated_values': json.loads(row[3]) if row[3] else None,
            'admin_id': row[4],
            'admin_name': row[7] or 'Unknown',
            'action_timestamp': row[5],
            'reason': row[6]
        })

    return jsonify({
        'success': True,
        'sale': {
            'id': sale[0],
            'receipt_number': sale[1]
        },
        'audits': audit_list
    })


# =============================
# INVENTORY
# =============================

@app.route('/out_of_stock')
@admin_required
def out_of_stock():
    category_filter = request.args.get('category', 'all')
    tab = request.args.get('tab', 'active')

    conn = get_db()
    cur = conn.cursor()

    base_query = "SELECT p.* FROM products p"
    where = " WHERE p.stock <= ?"
    params = [LOW_STOCK_THRESHOLD]

    if category_filter == 'Medical':
        where += " AND p.product_type = 'Medical'"
    elif category_filter == 'Non-Medical':
        where += " AND p.product_type = 'Non-Medical'"

    if tab == 'acknowledged':
        where += " AND EXISTS (SELECT 1 FROM alert_acknowledgments aa WHERE aa.product_id = p.id AND aa.alert_type = 'out_of_stock' AND aa.action = 'acknowledge')"
    elif tab == 'dismissed':
        where += " AND EXISTS (SELECT 1 FROM alert_acknowledgments aa WHERE aa.product_id = p.id AND aa.alert_type = 'out_of_stock' AND aa.action = 'dismiss')"
    else:
        where += " AND NOT EXISTS (SELECT 1 FROM alert_acknowledgments aa WHERE aa.product_id = p.id AND aa.alert_type = 'out_of_stock')"

    cur.execute(base_query + where + " ORDER BY p.stock ASC", params)
    products = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]

    conn.close()
    return render_template('inventory_out_of_stock.html', products=products,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='alerts', active_sub='out_of_stock',
                           category_filter=category_filter, tab=tab)

@app.route('/low_stock')
@admin_required
def low_stock():
    category_filter = request.args.get('category', 'all')
    tab = request.args.get('tab', 'active')

    conn = get_db()
    cur = conn.cursor()

    base_query = "SELECT p.* FROM products p"
    where = " WHERE p.stock > 0 AND p.stock <= ?"
    params = [LOW_STOCK_THRESHOLD]

    if category_filter == 'Medical':
        where += " AND p.product_type = 'Medical'"
    elif category_filter == 'Non-Medical':
        where += " AND p.product_type = 'Non-Medical'"

    if tab == 'acknowledged':
        where += " AND EXISTS (SELECT 1 FROM alert_acknowledgments aa WHERE aa.product_id = p.id AND aa.alert_type = 'low_stock' AND aa.action = 'acknowledge')"
    elif tab == 'dismissed':
        where += " AND EXISTS (SELECT 1 FROM alert_acknowledgments aa WHERE aa.product_id = p.id AND aa.alert_type = 'low_stock' AND aa.action = 'dismiss')"
    else:
        where += " AND NOT EXISTS (SELECT 1 FROM alert_acknowledgments aa WHERE aa.product_id = p.id AND aa.alert_type = 'low_stock')"

    cur.execute(base_query + where + " ORDER BY p.stock ASC", params)
    products = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock > 0 AND stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]

    conn.close()
    return render_template('inventory_low_stock.html', products=products,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='alerts', active_sub='low_stock',
                           category_filter=category_filter, tab=tab)

@app.route('/expired_products')
@admin_required
def expired_products():
    category_filter = request.args.get('category', 'all')
    tab = request.args.get('tab', 'active')

    conn = get_db()
    cur = conn.cursor()

    base_query = "SELECT p.* FROM products p"
    where = " WHERE p.expiration_date IS NOT NULL AND p.expiration_date < date('now', 'localtime')"
    params = []

    if category_filter == 'Medical':
        where += " AND p.product_type = 'Medical'"
    elif category_filter == 'Non-Medical':
        where += " AND p.product_type = 'Non-Medical'"

    if tab == 'acknowledged':
        where += " AND EXISTS (SELECT 1 FROM alert_acknowledgments aa WHERE aa.product_id = p.id AND aa.alert_type = 'expired' AND aa.action = 'acknowledge')"
    elif tab == 'dismissed':
        where += " AND EXISTS (SELECT 1 FROM alert_acknowledgments aa WHERE aa.product_id = p.id AND aa.alert_type = 'expired' AND aa.action = 'dismiss')"
    else:
        where += " AND NOT EXISTS (SELECT 1 FROM alert_acknowledgments aa WHERE aa.product_id = p.id AND aa.alert_type = 'expired')"

    cur.execute(base_query + where + " ORDER BY p.expiration_date ASC", params)
    products = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]

    conn.close()
    return render_template('inventory_expired.html', products=products,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='alerts', active_sub='expired_products',
                           category_filter=category_filter, tab=tab)

@app.route('/expiring_medical')
@admin_required
def expiring_medical():
    from datetime import date, timedelta
    category_filter = request.args.get('category', 'all')
    level = request.args.get('level', 'all')
    tab = request.args.get('tab', 'active')

    conn = get_db()
    cur = conn.cursor()

    base_query = "SELECT p.* FROM products p"
    where = " WHERE p.expiration_date IS NOT NULL"
    params = []

    if level == 'expired':
        where += " AND p.expiration_date < date('now', 'localtime')"
    elif level == 'critical':
        where += " AND p.expiration_date >= date('now', 'localtime') AND p.expiration_date <= date('now', '+7 days', 'localtime')"
    elif level == 'warning':
        where += " AND p.expiration_date > date('now', '+7 days', 'localtime') AND p.expiration_date <= date('now', '+30 days', 'localtime')"
    else:
        where += " AND p.expiration_date <= date('now', '+30 days', 'localtime')"

    if category_filter != 'all':
        where += " AND p.product_type = ?"
        params.append(category_filter)

    if tab == 'acknowledged':
        where += " AND EXISTS (SELECT 1 FROM alert_acknowledgments aa WHERE aa.product_id = p.id AND aa.alert_type = 'expiring_medical' AND aa.action = 'acknowledge')"
    elif tab == 'dismissed':
        where += " AND EXISTS (SELECT 1 FROM alert_acknowledgments aa WHERE aa.product_id = p.id AND aa.alert_type = 'expiring_medical' AND aa.action = 'dismiss')"
    else:
        where += " AND NOT EXISTS (SELECT 1 FROM alert_acknowledgments aa WHERE aa.product_id = p.id AND aa.alert_type = 'expiring_medical')"

    cur.execute(base_query + where + " ORDER BY p.expiration_date ASC", params)
    products = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]

    conn.close()
    return render_template('inventory_expiring.html', products=products,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='alerts', active_sub='expiring_medical',
                           now=date.today(), category_filter=category_filter,
                           level=level, tab=tab)

# =============================
# ADMIN MANAGEMENT
# =============================

@app.route('/register_cashier', methods=['GET','POST'])
@admin_required
def register_cashier():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    if request.method == 'POST':
        username = clean_input(request.form.get('username'))
        full_name = clean_input(request.form.get('full_name'))
        password = clean_input(request.form.get('password'))
        security_question = clean_input(request.form.get('security_question'))
        security_answer = clean_input(request.form.get('security_answer'))

        if username == "" or full_name == "" or password == "" or security_question == "" or security_answer == "":
            flash("All fields are required", "error")
            return redirect(url_for('register_cashier'))

        cur.execute("SELECT id FROM cashiers WHERE username=?", (username,))
        if cur.fetchone():
            conn.close()
            flash("Username already exists", "error")
            return redirect(url_for('register_cashier'))

        hashed_password = generate_password_hash(password)
        hashed_answer = generate_password_hash(security_answer)

        cur.execute("""
            INSERT INTO cashiers (full_name, username, password, security_question, security_answer)
            VALUES (?, ?, ?, ?, ?)
        """, (full_name, username, hashed_password, security_question, hashed_answer))

        conn.commit()
        
        # Log admin activity
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            cur.execute("""
                INSERT INTO admin_activity (admin_id, action, ip_address, details)
                VALUES (?, ?, ?, ?)
            """, (session.get('admin_id'), 'Register Cashier', ip_address, f'Registered cashier: {username}'))
            conn.commit()
        except:
            pass
        
        conn.close()

        flash("Cashier registered successfully", "success")
        return redirect(url_for('register_cashier'))

    conn.close()
    return render_template('register_cashier.html',
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='management', 
                           active_sub='register_cashier')


@app.route('/delete_cashier', methods=['GET','POST'])
@admin_required
def delete_cashier():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    if request.method == 'POST':
        cashier_id = request.form['id']
        
        # Get cashier info before deleting
        cur.execute("SELECT username FROM cashiers WHERE id=?", (cashier_id,))
        cashier_info = cur.fetchone()
        cashier_username = cashier_info[0] if cashier_info else 'Unknown'
        
        cur.execute("DELETE FROM cashiers WHERE id=?", (cashier_id,))
        conn.commit()
        
        # Log admin activity
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            cur.execute("""
                INSERT INTO admin_activity (admin_id, action, ip_address, details)
                VALUES (?, ?, ?, ?)
            """, (session.get('admin_id'), 'Delete Cashier', ip_address, f'Deleted cashier: {cashier_username}'))
            conn.commit()
        except:
            pass
        
        flash("Cashier deleted successfully", "success")

    cur.execute("SELECT * FROM cashiers")
    cashiers = cur.fetchall()
    conn.close()
    return render_template('delete_cashier.html', cashiers=cashiers,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='management', active_sub='delete_cashier')

@app.route('/edit_cashier', methods=['POST'])
@admin_required
def edit_cashier():
    cashier_id = request.form.get('id')
    full_name = clean_input(request.form.get('full_name'))
    username = clean_input(request.form.get('username'))
    status = request.form.get('status')
    password = clean_input(request.form.get('password'))

    if full_name == "" or username == "" or status == "":
        flash("Full name, username, and status are required", "error")
        return redirect(url_for('delete_cashier'))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id FROM cashiers WHERE username=? AND id!=?", (username, cashier_id))
    if cur.fetchone():
        conn.close()
        flash("Username already exists", "error")
        return redirect(url_for('delete_cashier'))

    try:
        if password != "":
            hashed_pw = generate_password_hash(password)
            cur.execute("""
                UPDATE cashiers 
                SET full_name=?, username=?, password=?, status=?
                WHERE id=?
            """, (full_name, username, hashed_pw, status, cashier_id))
        else:
            cur.execute("""
                UPDATE cashiers 
                SET full_name=?, username=?, status=?
                WHERE id=?
            """, (full_name, username, status, cashier_id))

        conn.commit()
        
        # Log admin activity
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            cur.execute("""
                INSERT INTO admin_activity (admin_id, action, ip_address, details)
                VALUES (?, ?, ?, ?)
            """, (session.get('admin_id'), 'Update Cashier', ip_address, f'Updated cashier: {username}'))
            conn.commit()
        except:
            pass
        
        flash("Cashier updated successfully!", "success")

    except Exception as e:
        conn.rollback()
        flash(f"Error: {str(e)}", "error")

    finally:
        conn.close()

    return redirect(url_for('delete_cashier'))

@app.route('/admin/change_password', methods=['GET','POST'])
@admin_required
def admin_change_password():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    conn.close()
    admin_id = session.get('admin_id')

    if request.method == 'POST':
        old_password = request.form.get('old_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not old_password or not new_password or not confirm_password:
            flash("All fields are required", "error")
            return render_template('change_admin_password.html', low_stock_count=low_stock_count, expiring_count=expiring_count, active_main='management', active_sub='change_admin_password')

        if new_password != confirm_password:
            flash("New passwords do not match", "error")
            return render_template('change_admin_password.html', low_stock_count=low_stock_count, expiring_count=expiring_count, active_main='management', active_sub='change_admin_password')

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM admins WHERE id=?", (admin_id,))
        admin = cur.fetchone()

        if not admin or not check_password_hash(admin[1], old_password):
            flash("Current password is incorrect", "error")
            conn.close()
            return render_template('change_admin_password.html', low_stock_count=low_stock_count, expiring_count=expiring_count, active_main='management', active_sub='change_admin_password')

        hashed = generate_password_hash(new_password)
        cur.execute("UPDATE admins SET password=? WHERE id=?", (hashed, admin_id))
        conn.commit()
        
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            cur.execute("""INSERT INTO admin_activity (admin_id, action, ip_address, details) VALUES (?, ?, ?, ?)""", (admin_id, 'Change Password', ip_address, 'Admin changed password from dashboard'))
            conn.commit()
        except:
            pass
        
        conn.close()
        flash("Password updated successfully", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('change_admin_password.html', low_stock_count=low_stock_count, expiring_count=expiring_count, active_main='management', active_sub='change_admin_password')

@app.route('/cashier/change_password', methods=['GET', 'POST'])
@cashier_required
def cashier_change_password():
    cashier_id = session.get('cashier_id')

    if request.method == 'POST':
        old_password = request.form.get('old_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not old_password or not new_password or not confirm_password:
            flash("All fields are required", "error")
            return render_template('change_cashier_password.html')

        if new_password != confirm_password:
            flash("New passwords do not match", "error")
            return render_template('change_cashier_password.html')

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM cashiers WHERE id=?", (cashier_id,))
        cashier = cur.fetchone()

        if not cashier or not check_password_hash(cashier[1], old_password):
            flash("Current password is incorrect", "error")
            conn.close()
            return render_template('change_cashier_password.html')

        hashed = generate_password_hash(new_password)
        cur.execute("UPDATE cashiers SET password=? WHERE id=?", (hashed, cashier_id))
        conn.commit()
        
        try:
            ip_address = request.remote_addr
            if request.headers.get('X-Forwarded-For'):
                ip_address = request.headers.get('X-Forwarded-For')
            cur.execute("""INSERT INTO cashier_activity (cashier_id, login_time, ip_address) VALUES (?, datetime('now', 'localtime'), ?)""", (cashier_id, ip_address))
            conn.commit()
        except:
            pass
        
        conn.close()
        flash("Password updated successfully", "success")
        return redirect(url_for('cashier_dashboard'))

    return render_template('change_cashier_password.html')

@app.route('/change_admin_password', methods=['GET','POST'])
def change_admin_password():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    conn.close()
    
    security_question = None

    if request.method == 'POST':
        step = request.form.get('step', '1')
        username = request.form.get('username', '').strip()

        if not username:
            flash("Username is required", "error")
            return redirect(url_for('change_admin_password'))

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, security_question, security_answer FROM admins WHERE username=?", (username,))
        admin = cur.fetchone()

        if not admin:
            flash("Invalid username", "error")
            conn.close()
            return redirect(url_for('change_admin_password'))

        if step == '1':
            security_question = admin[1] if len(admin) > 1 and admin[1] else None
            if not security_question:
                hashed_answer = generate_password_hash('generoso')
                cur.execute("UPDATE admins SET security_question=?, security_answer=? WHERE id=?", ('What is the name of the owner?', hashed_answer, admin[0]))
                conn.commit()
                security_question = 'What is the name of the owner?'
        elif step == '2':
            security_answer = request.form.get('security_answer', '').strip()
            new_pass = request.form.get('new_password', '').strip()

            if not security_answer or not new_pass:
                flash("All fields are required", "error")
                conn.close()
                return redirect(url_for('change_admin_password'))

            stored_answer = admin[2] if len(admin) > 2 else None
            if stored_answer and check_password_hash(stored_answer, security_answer):
                hashed = generate_password_hash(new_pass)
                cur.execute("UPDATE admins SET password=? WHERE username=?", (hashed, username))
                conn.commit()
                
                ip_address = request.remote_addr
                if request.headers.get('X-Forwarded-For'):
                    ip_address = request.headers.get('X-Forwarded-For')
                
                try:
                    cur.execute("""
                        INSERT INTO admin_activity (admin_id, action, ip_address, details)
                        VALUES (?, ?, ?, ?)
                    """, (admin[0], 'Change Password', ip_address, 'Admin changed password via forgot password'))
                    conn.commit()
                except:
                    pass
                
                flash("Password updated successfully", "success")
            else:
                flash("Security answer is incorrect", "error")
        conn.close()

    return render_template('forgot_admin_password.html',
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           security_question=security_question)

@app.route('/change_cashier_password', methods=['GET', 'POST'])
def change_cashier_password():
    conn = get_db()
    cur = conn.cursor()
    try:
        security_question = None

        if request.method == 'POST':
            step = request.form.get('step', '1')
            username = request.form.get('username', '').strip()

            if not username:
                flash("Username is required", "error")
                return redirect(url_for('change_cashier_password'))

            cur.execute("SELECT id, password, security_question, security_answer FROM cashiers WHERE username=?", (username,))
            row = cur.fetchone()

            if not row:
                flash("Invalid username", "error")
                return redirect(url_for('change_cashier_password'))

            if step == '1':
                security_question = row[2] if row[2] else None
                if not security_question:
                    hashed_answer = generate_password_hash('generoso')
                    cur.execute("UPDATE cashiers SET security_question=?, security_answer=? WHERE id=?", ('What is the name of the owner?', hashed_answer, row[0]))
                    conn.commit()
                    security_question = 'What is the name of the owner?'
            elif step == '2':
                security_answer = request.form.get('security_answer', '').strip()
                new_password = request.form.get('new_password', '').strip()

                if not security_answer or not new_password:
                    flash("All fields are required", "error")
                    return redirect(url_for('change_cashier_password'))

                if check_password_hash(row[3], security_answer):
                    hashed = generate_password_hash(new_password)
                    cur.execute("UPDATE cashiers SET password=? WHERE id=?", (hashed, row[0]))
                    conn.commit()
                    flash("Password updated successfully", "success")
                else:
                    flash("Security answer is incorrect", "error")
    finally:
        conn.close()

    return render_template('forgot_cashier_password.html', security_question=security_question)

# =============================
# CASHIER LOGIN
# =============================

@app.route('/cashier_login', methods=['GET', 'POST'])
def cashier_login():
    if 'cashier_user' in session and session.get('role') == 'cashier':
        return redirect(url_for('cashier_dashboard'))

    if request.method == 'POST':
        username = clean_input(request.form.get('username'))
        password = clean_input(request.form.get('password'))

        if username == "" or password == "":
            flash("All fields are required", "error")
            return redirect(url_for('cashier_login'))

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, full_name, username, password, status FROM cashiers WHERE username=?", (username,))
        cashier = cur.fetchone()
        conn.close()

        if not cashier or not check_password_hash(cashier[3], password):
            flash("Invalid login credentials", "error")
            return redirect(url_for('cashier_login'))

        cashier_status = ((cashier[4] or 'active')).lower()
        if cashier_status != 'active':
            flash("Cashier account is inactive. Contact the administrator.", "error")
            return redirect(url_for('cashier_login'))

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT security_question, security_answer FROM cashiers WHERE id=?", (cashier[0],))
        sq = cur.fetchone()
        if not sq or not sq[0] or not sq[1]:
            hashed_answer = generate_password_hash('generoso')
            cur.execute("UPDATE cashiers SET security_question=?, security_answer=? WHERE id=?", ('What is the name of the owner?', hashed_answer, cashier[0]))
            conn.commit()
        conn.close()

        session['cashier_user'] = cashier[1]
        session['cashier_id'] = cashier[0]
        session['role'] = 'cashier'
        session.permanent = True  # Session persists on refresh

        conn = get_db()
        cur = conn.cursor()

        # Get IP address
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')

        # Log cashier login with IP address
        cur.execute("""
            INSERT INTO cashier_activity (cashier_id, login_time, ip_address)
            VALUES (?, datetime('now', 'localtime'), ?)
        """, (cashier[0], ip_address))
        conn.commit()
        conn.close()

        return redirect(url_for('cashier_dashboard'))

    return render_template('cashier_login.html')


@app.route('/active_cashiers')
@admin_required
def get_active_cashiers():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT id, full_name, username FROM cashiers")
    cashiers = cur.fetchall()
    
    cur.execute("""
        SELECT c.username, ca.login_time
        FROM cashiers c
        JOIN cashier_activity ca ON c.id = ca.cashier_id
        WHERE ca.logout_time IS NULL
    """)
    active_data = {row[0]: row[1] for row in cur.fetchall()}
    conn.close()

    cashier_list = []
    for c in cashiers:
        login_time = active_data.get(c[2], None)
        cashier_list.append({
            'id': c[0],
            'full_name': c[1],
            'username': c[2],
            'status': 'Online' if c[2] in active_data else 'Offline',
            'login_time': str(login_time) if login_time else None
        })

    return jsonify(cashier_list)

# =============================
# CASHIER DASHBOARD
# =============================

@app.route('/cashier')
@cashier_required
def cashier_dashboard():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT IFNULL(SUM(total_amount), 0) as total, COUNT(*) as count
        FROM sales 
        WHERE cashier_id = ? AND DATE(sale_date) = date('now', 'localtime') AND sale_status = 'Completed'
    """, (session['cashier_id'],))
    today_data = cur.fetchone()
    today_total = today_data[0] if today_data else 0
    today_count = today_data[1] if today_data else 0

    cur.execute("""
        SELECT sale_date, receipt_number, total_amount, sale_status 
        FROM sales 
        WHERE cashier_id = ?
        ORDER BY sale_date DESC 
        LIMIT 5
    """, (session['cashier_id'],))

    recent_sales = cur.fetchall()

    settings = get_store_settings()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    conn.close()

    return render_template('cashier_dashboard.html', 
                           recent_sales=recent_sales,
                           today_total=today_total,
                           today_count=today_count,
                           settings=settings,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count)

@app.route('/cashier_history')
@cashier_required
def cashier_history():
    conn = get_db()
    cur = conn.cursor()

    receipt_search = request.args.get('receipt_number', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()

    # Build filters for the transaction list
    conditions = ["cashier_id = ?", "sale_status = 'Completed'"]
    params = [session['cashier_id']]

    if receipt_search:
        conditions.append("receipt_number LIKE ?")
        params.append(f"%{receipt_search}%")
    if date_from:
        conditions.append("DATE(sale_date) >= ?")
        params.append(date_from)
    if date_to:
        conditions.append("DATE(sale_date) <= ?")
        params.append(date_to)

    where_clause = " AND ".join(conditions)

    # Get filtered transactions for the history list
    cur.execute(f"""
        SELECT id, receipt_number, total_amount, sale_date
        FROM sales
        WHERE {where_clause}
        ORDER BY sale_date DESC
    """, params)
    sales = cur.fetchall()

    sales_data = []
    for sale in sales:
        sale_id = sale[0]
        cur.execute("""
            SELECT si.quantity, si.price, p.product_name
            FROM sale_items si
            LEFT JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = ?
        """, (sale_id,))
        items = cur.fetchall()
        sales_data.append({
            "id": sale[0],
            "receipt_number": sale[1],
            "total_amount": float(sale[2]),
            "sale_date": sale[3],
            "items": items
        })

    # Summary stats based on the current filter
    cur.execute(f"""
        SELECT IFNULL(SUM(total_amount), 0), COUNT(id)
        FROM sales
        WHERE {where_clause}
    """, params)
    summary = cur.fetchone()
    filtered_total = float(summary[0])
    filtered_count = int(summary[1])

    # Daily sales (today only for chart)
    cur.execute("""
        SELECT DATE(sale_date) as sale_day,
               IFNULL(SUM(total_amount),0) as total_sales,
               COUNT(id) as total_transactions
        FROM sales
        WHERE cashier_id = ?
        AND sale_status = 'Completed'
        AND DATE(sale_date) = date('now', 'localtime')
        GROUP BY DATE(sale_date)
        ORDER BY sale_day ASC
    """, (session['cashier_id'],))
    daily_data = cur.fetchall()

    labels = [str(row[0]) for row in daily_data]
    sales_values = [float(row[1]) for row in daily_data]
    transaction_counts = [int(row[2]) for row in daily_data]

    conn.close()
    return render_template(
        "cashier_history.html",
        sales=sales_data,
        chart_labels=labels,
        chart_sales=sales_values,
        chart_transactions=transaction_counts,
        receipt_search=receipt_search,
        date_from=date_from,
        date_to=date_to,
        filtered_total=filtered_total,
        filtered_count=filtered_count
    )

@app.route('/search_product')
@cashier_required
def search_product():
    query = request.args.get('q')
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, product_name, price, stock, barcode, expiration_date
        FROM products
        WHERE (product_name LIKE ? OR barcode LIKE ?)
        AND stock > 0
        ORDER BY product_name, expiration_date
        LIMIT 10
    """, (f"%{query}%", f"%{query}%"))

    products = cur.fetchall()
    conn.close()

    result = []
    for p in products:
        expiry_date = None
        if p[5]:
            try:
                expiry_date = datetime.strptime(p[5], '%Y-%m-%d').date()
            except Exception:
                expiry_date = None
        expiry = expiry_date.strftime('%m/%d/%Y') if expiry_date else 'N/A'
        is_expired = expiry_date is not None and expiry_date < datetime.now().date()
        result.append({
            "id": p[0],
            "name": p[1],
            "price": float(p[2]),
            "stock": p[3],
            "barcode": p[4],
            "expiry": expiry,
            "is_expired": is_expired
        })

    return jsonify(result)

@app.route('/api/products')
@cashier_required
def api_products():
    """API endpoint for live product updates"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, product_name, price, stock, barcode, expiration_date FROM products WHERE stock > 0 ORDER BY product_name, expiration_date")
    products = cur.fetchall()
    conn.close()
    
    result = []
    for p in products:
        expiry_date = None
        if p[5]:
            try:
                expiry_date = datetime.strptime(p[5], '%Y-%m-%d').date()
            except Exception:
                expiry_date = None
        expiry = expiry_date.strftime('%m/%d/%Y') if expiry_date else 'N/A'
        is_expired = expiry_date is not None and expiry_date < datetime.now().date()
        result.append({
            "id": p[0],
            "name": p[1],
            "price": float(p[2]),
            "stock": p[3],
            "barcode": p[4],
            "expiry": expiry,
            "is_expired": is_expired
        })
    return jsonify(result)

@app.route('/api/search_by_name')
@cashier_required
def search_by_name():
    """API to search product by name for auto-fill"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, product_name, barcode, price, category_id, expiration_date 
        FROM products 
        WHERE product_name LIKE ? 
        ORDER BY product_name, expiration_date
        LIMIT 5
    """, (f"%{query}%",))
    products = cur.fetchall()
    conn.close()
    
    result = []
    for p in products:
        expiry = p[5].strftime('%m/%d/%Y') if p[5] else 'N/A'
        result.append({
            "id": p[0],
            "name": p[1],
            "barcode": p[2],
            "price": float(p[3]) if p[3] else 0,
            "category_id": p[4],
            "expiry": expiry
        })
    return jsonify(result)

@app.route('/api/product/<int:product_id>')
@admin_required
def api_get_product(product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, product_name, barcode, category_id, product_type, price, stock, expiration_date FROM products WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    
    if row:
        return jsonify({
            'success': True,
            'product': {
                'id': row[0],
                'product_name': row[1],
                'barcode': row[2],
                'category_id': row[3],
                'product_type': row[4],
                'price': float(row[5]) if row[5] else 0,
                'stock': row[6],
                'expiration_date': str(row[7]) if row[7] else None
            }
        })
    return jsonify({'success': False})

@app.route('/api/update_product', methods=['POST'])
@admin_required
def api_update_product():
    data = request.get_json()
    product_id = data.get('id')
    product_name = data.get('product_name')
    barcode = data.get('barcode')
    category = data.get('category')
    price = data.get('price')
    expiration_date = data.get('expiration_date') or None
    
    if not product_name or not barcode or not category:
        return jsonify({'success': False, 'message': 'All fields are required'})
    
    try:
        price = float(price) if price else 0
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid price value'})
    
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM categories WHERE category_name=?", (category,))
    cat_result = cur.fetchone()
    category_id = cat_result[0] if cat_result else None
    if not category_id:
        conn.close()
        return jsonify({'success': False, 'message': 'Invalid category'})
    
    # Stock is intentionally not updated here - stock changes go through the
    # Stock In page (/stock_in) so every movement is logged in stock_movements.
    cur.execute("""
        UPDATE products 
        SET product_name=?, barcode=?, category_id=?, product_type=?, price=?, expiration_date=?
        WHERE id=?
    """, (product_name, barcode, category_id, category, price, expiration_date, product_id))
    
    conn.commit()
    
    ip_address = request.remote_addr
    if request.headers.get('X-Forwarded-For'):
        ip_address = request.headers.get('X-Forwarded-For')
    
    try:
        cur.execute("""
            INSERT INTO admin_activity (admin_id, action, ip_address, details)
            VALUES (?, ?, ?, ?)
        """, (session.get('admin_id'), 'Edit Product', ip_address, f'Edited product: {product_name}'))
        conn.commit()
    except:
        pass
    
    conn.close()
    return jsonify({'success': True, 'message': 'Product updated successfully!'})

@app.route('/get_product/<barcode>')
@cashier_required
def get_product(barcode):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, product_name, price, stock, barcode, expiration_date
        FROM products
        WHERE barcode = ? AND stock > 0
        LIMIT 1
    """, (barcode,))

    row = cur.fetchone()
    conn.close()

    if row:
        expiry_date = None
        if row[5]:
            try:
                expiry_date = datetime.strptime(row[5], '%Y-%m-%d').date()
            except Exception:
                expiry_date = None
        expiry = expiry_date.strftime('%m/%d/%Y') if expiry_date else 'N/A'
        is_expired = expiry_date is not None and expiry_date < datetime.now().date()
        return jsonify({
            "success": True,
            "product": {
                "id": row[0],
                "name": row[1],
                "price": float(row[2]),
                "stock": row[3],
                "barcode": row[4],
                "expiry": expiry,
                "is_expired": is_expired
            }
        })

    return jsonify({"success": False})

@app.route('/complete_sale', methods=['POST'])
@cashier_required
def complete_sale():
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format'})

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data received'})

    items = data.get('items', [])
    tendered = data.get('tendered', 0)

    try:
        tendered = float(tendered)
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'Invalid tendered amount'})

    if not items:
        return jsonify({'success': False, 'message': 'No items in cart'})

    quantity_by_product = {}
    for item in items:
        if not isinstance(item, dict):
            return jsonify({'success': False, 'message': 'Invalid item data'})
        try:
            product_id = int(item.get('id'))
            quantity = int(item.get('quantity'))
        except (TypeError, ValueError):
            return jsonify({'success': False, 'message': 'Invalid item data'})

        if product_id <= 0 or quantity <= 0:
            return jsonify({'success': False, 'message': 'Invalid item data'})

        quantity_by_product[product_id] = quantity_by_product.get(product_id, 0) + quantity

    product_ids = list(quantity_by_product.keys())
    placeholders = ','.join(['?'] * len(product_ids))

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(f"""
            SELECT id, product_name, product_type, price, stock, expiration_date
            FROM products
            WHERE id IN ({placeholders})
        """, tuple(product_ids))
        products = {row[0]: row for row in cur.fetchall()}

        if len(products) != len(product_ids):
            return jsonify({'success': False, 'message': 'One or more products no longer exist'})

        medical_items = []
        non_medical_items = []
        receipt_items = []
        total_amount = 0.0
        expired_items = []

        for product_id, requested_quantity in quantity_by_product.items():
            row = products[product_id]
            name = row[1]
            product_type = row[2] or 'Non-Medical'
            product_type_key = product_type.lower()
            price = float(row[3])
            stock = int(row[4])
            expiry_date_str = row[5]
            expiry_date = None
            if expiry_date_str:
                try:
                    expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                except Exception:
                    expiry_date = None

            if price < 0:
                return jsonify({'success': False, 'message': f'Invalid price for {name}'})

            if stock < requested_quantity:
                return jsonify({
                    'success': False,
                    'message': f'Not enough stock for {name}. Available: {stock}'
                })

            if expiry_date is not None and expiry_date < datetime.now().date():
                expired_items.append(name)
                continue

            subtotal = round(price * requested_quantity, 2)
            total_amount += subtotal
            receipt_items.append({
                'name': name,
                'quantity': requested_quantity,
                'price': price,
                'subtotal': subtotal
            })

            if product_type_key == 'medical':
                medical_items.append(row[:1] + (requested_quantity, price))
            else:
                non_medical_items.append(row[:1] + (requested_quantity, price))

        if expired_items:
            return jsonify({
                'success': False,
                'message': f'Cannot complete sale. The following products are expired: {", ".join(expired_items)}'
            })

        if tendered < total_amount:
            return jsonify({'success': False, 'message': 'Amount tendered is less than total'})

        receipt_numbers = []

        if medical_items:
            receipt_number = f"REC-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            receipt_numbers.append(receipt_number)
            medical_total = round(sum(item[2] * item[1] for item in medical_items), 2)
            change = round(tendered - total_amount, 2)

            cur.execute("""
                INSERT INTO sales (receipt_number, cashier_id, total_amount, sale_status, product_type, sale_date, amount_tendered, change_amount)
                VALUES (?, ?, ?, 'Completed', 'Medical', datetime('now', 'localtime'), ?, ?)
            """, (receipt_number, session['cashier_id'], medical_total, tendered, change))

            sale_id = cur.lastrowid

            for product_id, quantity, price in medical_items:
                cur.execute("""
                    INSERT INTO sale_items (sale_id, product_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                """, (sale_id, product_id, quantity, price))

                cur.execute("""
                    UPDATE products SET stock = stock - ? WHERE id = ?
                """, (quantity, product_id))

                cur.execute("""
                    INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                    VALUES (?, 'OUT', ?, 'Sale')
                """, (product_id, quantity))

        if non_medical_items:
            receipt_number = f"REC-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            receipt_numbers.append(receipt_number)
            non_medical_total = round(sum(item[2] * item[1] for item in non_medical_items), 2)
            change = round(tendered - total_amount, 2)

            cur.execute("""
                INSERT INTO sales (receipt_number, cashier_id, total_amount, sale_status, product_type, sale_date, amount_tendered, change_amount)
                VALUES (?, ?, ?, 'Completed', 'Non-Medical', datetime('now', 'localtime'), ?, ?)
            """, (receipt_number, session['cashier_id'], non_medical_total, tendered, change))

            sale_id = cur.lastrowid

            for product_id, quantity, price in non_medical_items:
                cur.execute("""
                    INSERT INTO sale_items (sale_id, product_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                """, (sale_id, product_id, quantity, price))

                cur.execute("""
                    UPDATE products SET stock = stock - ? WHERE id = ?
                """, (quantity, product_id))

                cur.execute("""
                    INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                    VALUES (?, 'OUT', ?, 'Sale')
                """, (product_id, quantity))

        conn.commit()
        main_receipt = receipt_numbers[0] if receipt_numbers else 'N/A'
        change = round(tendered - total_amount, 2)

        return jsonify({
            'success': True,
            'receipt_number': main_receipt,
            'total': round(total_amount, 2),
            'tendered': round(tendered, 2),
            'change': change,
            'items': receipt_items,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    except Exception as e:
        try:
            conn.rollback()
        except:
            pass
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})
    finally:
        conn.close()

# =============================
# LOGOUT
# =============================

# Route to setup remote database access (run once)
@app.route('/setup_remote_db')
def setup_remote_db():
    """Grant remote access to root user - run this once from Computer 1"""
    try:
        conn = get_db()
        cur = conn.cursor()
        # Create user for remote access with all privileges
        try:
            cur.execute("CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY ''")
        except Exception:
            conn.rollback()
        cur.execute("GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION")
        cur.execute("FLUSH PRIVILEGES")
        conn.close()
        return "Database remote access granted! You can now connect from other computers."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin_logout')
@app.route('/admin_logout')
@admin_required
def admin_logout():
    """Admin logout - only clears admin session, does not affect cashier"""
    # Log admin activity
    if 'admin_user' in session:
        conn = get_db()
        cur = conn.cursor()
        # Get IP address
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            # Verify admin still exists before logging
            cur.execute("SELECT id FROM admins WHERE id = ?", (session.get('admin_id'),))
            if cur.fetchone():
                cur.execute("""
                    INSERT INTO admin_activity (admin_id, action, ip_address, details)
                    VALUES (?, ?, ?, ?)
                """, (session.get('admin_id'), 'Admin Logout', ip_address, 'Admin logged out'))
                conn.commit()
        except Exception:
            pass  # Silently ignore activity logging errors
        finally:
            conn.close()
    
    # Only clear admin session keys, keep cashier session intact
    session.pop('admin_user', None)
    session.pop('admin_id', None)
    session.pop('role', None)
    
    return redirect(url_for('admin_login'))

@app.route('/cashier_logout')
def cashier_logout():
    """Cashier logout - clears cashier session and logs activity"""
    if 'cashier_user' in session:
        conn = get_db()
        cur = conn.cursor()
        cashier_id = session.get('cashier_id')
        
        # Get IP address
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        # Log the logout time in cashier_activity
        cur.execute("""
            UPDATE cashier_activity
            SET logout_time = datetime('now', 'localtime'),
                ip_address = COALESCE(ip_address, ?)
            WHERE cashier_id = ? AND logout_time IS NULL
        """, (ip_address, cashier_id))
        conn.commit()
        conn.close()
    
    # Only clear cashier session keys, keep admin session intact
    session.pop('cashier_user', None)
    session.pop('cashier_id', None)
    session.pop('role', None)
    
    return redirect(url_for('cashier_login'))

@app.route('/logout')
def logout():
    """Legacy logout - determines role and logs out appropriately"""
    role = session.get('role')
    
    if role == 'admin':
        return redirect(url_for('admin_logout'))
    elif role == 'cashier':
        return redirect(url_for('cashier_logout'))
    
    # If no role, just clear everything
    session.clear()
    return redirect(url_for('admin_login'))

# =============================
# OOP INTEGRATION: REFACTORED ROUTES
# =============================

# --- Example 1: Encapsulation via Product model ---
@app.route('/add_product_oop', methods=['POST'])
@admin_required
def add_product_oop():
    """Add product using OOP models and services."""
    try:
        product = Product(
            product_id=0,
            name=request.form.get('product_name', '').strip(),
            barcode=request.form.get('barcode', '').strip(),
            category_id=int(request.form.get('category', 0) or 0),
            product_type=request.form.get('category', ''),
            price=float(request.form.get('price', 0)),
            stock=int(request.form.get('stock', 0)),
            expiration_date=request.form.get('expiration_date') or None
        )
        movement = StockMovement(
            0, product.id,
            StockMovement.IN,
            product.stock,
            'Stock Addition'
        )
        product_repository.link_stock_movement(product, movement)
        product_repository.save(product)
        flash("Product registered successfully via OOP!", "success")
    except ValueError as e:
        flash(f"Validation error: {str(e)}", "error")
    except Exception as e:
        conn.rollback()
        flash(f"Database error: {str(e)}", "error")
    return redirect(url_for('add_product'))

# --- Example 2: Polymorphism via SalesService ---
@app.route('/complete_sale_oop', methods=['POST'])
@cashier_required
def complete_sale_oop():
    """Complete sale using SalesService (polymorphism + abstraction)."""
    try:
        data = request.get_json()
        items = data.get('items', [])
        if not items:
            return jsonify({'success': False, 'message': 'No items in cart'})
        conn = get_db()
        cur = conn.cursor()
        try:
            enriched_items = []
            for item in items:
                cur.execute(
                    "SELECT product_name, product_type, price FROM products WHERE id=?",
                    (item['id'],)
                )
                row = cur.fetchone()
                if row:
                    enriched_items.append({
                        'id': item['id'],
                        'name': row[0],
                        'product_type': row[1],
                        'price': row[2],
                        'quantity': item['quantity']
                    })
        finally:
            conn.close()
        cashier = Cashier(
            user_id=session['cashier_id'],
            username=session['cashier_user'],
            full_name='Cashier',
            password_hash=''
        )
        result = sales_service.process_sale(enriched_items, cashier)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# --- Example 3: Polymorphism via AuthService (Admin login) ---
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_oop():
    """Admin login using AuthService (polymorphic authentication)."""
    if request.method == 'POST':
        username = clean_input(request.form.get('username'))
        password = clean_input(request.form.get('password'))
        if not username or not password:
            flash("All fields are required", "error")
            return redirect(url_for('admin_login'))
        success, user = auth_service.login(username, password, request, 'admin')
        if success and user:
            session_data = auth_service.get_session_data(user)
            session.update(session_data)
            session.permanent = True
            return redirect(url_for('admin_dashboard'))
        flash("Invalid login credentials", "error")
    return render_template('admin_login.html')

# --- Example 4: Polymorphism via AuthService (Cashier login) ---
@app.route('/cashier/login', methods=['GET', 'POST'])
def cashier_login_oop():
    """Cashier login using AuthService (same interface, different behavior)."""
    if request.method == 'POST':
        username = clean_input(request.form.get('username'))
        password = clean_input(request.form.get('password'))
        if not username or not password:
            flash("All fields are required", "error")
            return redirect(url_for('cashier_login'))
        success, user = auth_service.login(username, password, request, 'cashier')
        if success and user:
            session_data = auth_service.get_session_data(user)
            session.update(session_data)
            session.permanent = True
            return redirect(url_for('cashier_dashboard'))
        flash("Invalid login credentials", "error")
    return render_template('cashier_login.html')

# =============================
# STORE SETTINGS & UTILITIES
# =============================

def get_store_settings():
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT setting_key, setting_value FROM store_settings")
        rows = cur.fetchall()
        settings = {row[0]: row[1] for row in rows}
        return settings
    finally:
        conn.close()

def get_setting(key, default=''):
    settings = get_store_settings()
    return settings.get(key, default)

# =============================
# RECEIPT CUSTOMIZATION
# =============================

@app.route('/receipt_customization', methods=['GET', 'POST'])
@admin_required
def receipt_customization():
    conn = get_db()
    cur = conn.cursor()
    try:
        if request.method == 'POST':
            receipt_header = request.form.get('receipt_header', '').strip()
            receipt_subtitle = request.form.get('receipt_subtitle', '').strip()
            receipt_footer = request.form.get('receipt_footer', '').strip()
            store_address = request.form.get('store_address', '').strip()
            store_contact = request.form.get('store_contact', '').strip()

            settings_to_update = [
                ('receipt_header', receipt_header),
                ('receipt_subtitle', receipt_subtitle),
                ('receipt_footer', receipt_footer),
                ('store_address', store_address),
                ('store_contact', store_contact),
            ]

            for key, value in settings_to_update:
                cur.execute("""
                    INSERT INTO store_settings (setting_key, setting_value)
                    VALUES (?, ?)
                    ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value)
                """, (key, value))

            conn.commit()
            flash("Receipt settings saved successfully!", "success")

        cur.execute("SELECT setting_key, setting_value FROM store_settings")
        rows = cur.fetchall()
        settings = {row[0]: row[1] for row in rows}
    finally:
        conn.close()

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    conn.close()

    return render_template('receipt_customization.html',
                           settings=settings,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='management',
                           active_sub='receipt_customization')

# =============================
# RECEIPT PRINT CONFIRMATION
# =============================

@app.route('/api/mark_receipt_printed', methods=['POST'])
@cashier_required
def mark_receipt_printed():
    try:
        data = request.get_json()
        receipt_number = data.get('receipt_number')
        if not receipt_number:
            return jsonify({'success': False, 'message': 'Receipt number is required'}), 400

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE sales 
            SET receipt_printed = 1, printed_at = datetime('now', 'localtime')
            WHERE receipt_number = ? AND cashier_id = ? AND sale_status = 'Completed'
        """, (receipt_number, session['cashier_id']))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Receipt marked as printed'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/cancel_pending_sale', methods=['POST'])
@cashier_required
def cancel_pending_sale():
    try:
        data = request.get_json()
        receipt_number = data.get('receipt_number')
        if not receipt_number:
            return jsonify({'success': False, 'message': 'Receipt number is required'}), 400

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id FROM sales 
                WHERE receipt_number = ? AND cashier_id = ? AND sale_status = 'Pending'
                LIMIT 1
            """, (receipt_number, session['cashier_id']))
            sale_row = cur.fetchone()
            if not sale_row:
                return jsonify({'success': True, 'message': 'No pending sale found'})

            sale_id = sale_row[0]

            cur.execute("""
                SELECT product_id, quantity FROM sale_items WHERE sale_id = ?
            """, (sale_id,))
            items = cur.fetchall()

            for product_id, quantity in items:
                cur.execute("""
                    UPDATE products SET stock = stock + ? WHERE id = ?
                """, (quantity, product_id))

                cur.execute("""
                    DELETE FROM stock_movements 
                    WHERE product_id = ? AND movement_type = 'OUT' 
                    AND reason = 'Sale' AND movement_date >= (
                        SELECT sale_date FROM sales WHERE id = ?
                    )
                    LIMIT 1
                """, (product_id, sale_id))

            cur.execute("DELETE FROM sale_items WHERE sale_id = ?", (sale_id,))
            cur.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
            conn.commit()
            return jsonify({'success': True, 'message': 'Pending sale cancelled'})
        finally:
            conn.close()
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/reprint_receipt/<int:sale_id>')
@cashier_required
def reprint_receipt(sale_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT receipt_number, total_amount, sale_date, cashier_id, amount_tendered, change_amount FROM sales WHERE id = ?", (sale_id,))
    sale = cur.fetchone()
    if not sale:
        conn.close()
        return "Sale not found", 404
    cur.execute("""
        SELECT p.product_name, si.quantity, si.price
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        WHERE si.sale_id = ?
    """, (sale_id,))
    items = cur.fetchall()
    conn.close()
    return render_template('reprint_receipt.html', sale=sale, items=items)

@app.route('/api/void_sale', methods=['POST'])
@cashier_required
def api_void_sale():
    data = request.get_json()
    sale_id = data.get('sale_id')
    reason = data.get('reason', '')

    if not sale_id:
        return jsonify({'success': False, 'message': 'Sale ID is required'})
    if not reason:
        return jsonify({'success': False, 'message': 'Reason is required'})

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT sale_status FROM sales WHERE id = ? AND cashier_id = ?", (sale_id, session['cashier_id']))
        row = cur.fetchone()
        if not row:
            return jsonify({'success': False, 'message': 'Sale not found'})
        if row[0] == 'Voided':
            return jsonify({'success': False, 'message': 'Sale is already voided'})

        cur.execute("""
            UPDATE sales
            SET sale_status = 'Voided', voided_at = datetime('now', 'localtime'),
                voided_by = ?, void_reason = ?
            WHERE id = ? AND cashier_id = ?
        """, (session['cashier_id'], reason, sale_id, session['cashier_id']))

        cur.execute("SELECT product_id, quantity FROM sale_items WHERE sale_id = ?", (sale_id,))
        items = cur.fetchall()
        for product_id, quantity in items:
            cur.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (quantity, product_id))
            cur.execute("""
                INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                VALUES (?, 'IN', ?, 'Void Sale')
            """, (product_id, quantity))

        conn.commit()
        return jsonify({'success': True, 'message': 'Sale voided successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()

@app.route('/api/refund_sale', methods=['POST'])
@cashier_required
def api_refund_sale():
    data = request.get_json()
    sale_id = data.get('sale_id')
    reason = data.get('reason', '')

    if not sale_id:
        return jsonify({'success': False, 'message': 'Sale ID is required'})
    if not reason:
        return jsonify({'success': False, 'message': 'Reason is required'})

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT sale_status FROM sales WHERE id = ? AND cashier_id = ?", (sale_id, session['cashier_id']))
        row = cur.fetchone()
        if not row:
            return jsonify({'success': False, 'message': 'Sale not found'})
        if row[0] in ('Voided', 'Refunded'):
            return jsonify({'success': False, 'message': 'Sale is already voided or refunded'})

        cur.execute("""
            UPDATE sales
            SET sale_status = 'Refunded', refunded_at = datetime('now', 'localtime'),
                refunded_by = ?, refund_reason = ?
            WHERE id = ? AND cashier_id = ?
        """, (session['cashier_id'], reason, sale_id, session['cashier_id']))

        cur.execute("SELECT product_id, quantity FROM sale_items WHERE sale_id = ?", (sale_id,))
        items = cur.fetchall()
        for product_id, quantity in items:
            cur.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (quantity, product_id))
            cur.execute("""
                INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                VALUES (?, 'IN', ?, 'Refund Sale')
            """, (product_id, quantity))

        conn.commit()
        return jsonify({'success': True, 'message': 'Sale refunded successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()

@app.route('/api/hold_transaction', methods=['POST'])
@cashier_required
def api_hold_transaction():
    data = request.get_json()
    name = data.get('name', '').strip()
    cart = data.get('cart', [])

    if not name:
        return jsonify({'success': False, 'message': 'Hold name is required'})

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO held_transactions (cashier_id, name, cart)
            VALUES (?, ?, ?)
        """, (session['cashier_id'], name, json.dumps(cart)))
        conn.commit()
        return jsonify({'success': True, 'message': 'Transaction held'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()

@app.route('/api/held_transactions')
@cashier_required
def api_held_transactions():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, cart, created_at
        FROM held_transactions
        WHERE cashier_id = ?
        ORDER BY created_at DESC
    """, (session['cashier_id'],))
    rows = cur.fetchall()
    conn.close()

    holds = []
    for row in rows:
        holds.append({
            'id': row[0],
            'name': row[1],
            'cart': json.loads(row[2]) if row[2] else [],
            'timestamp': row[3]
        })
    return jsonify({'holds': holds})

@app.route('/api/resume_transaction', methods=['POST'])
@cashier_required
def api_resume_transaction():
    data = request.get_json()
    hold_id = data.get('id')

    if hold_id is None:
        return jsonify({'success': False, 'message': 'Hold ID is required'})

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT cart FROM held_transactions
            WHERE id = ? AND cashier_id = ?
        """, (hold_id, session['cashier_id']))
        row = cur.fetchone()
        if not row:
            return jsonify({'success': False, 'message': 'Held transaction not found'})

        cart = json.loads(row[0]) if row[0] else []
        cur.execute("DELETE FROM held_transactions WHERE id = ?", (hold_id,))
        conn.commit()
        return jsonify({'success': True, 'cart': cart})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()

# =============================
# BACKUP & RESTORE
# =============================

@app.route('/backup_restore')
@admin_required
def backup_restore():
    from database_sqlite import init_db
    init_db()  # Ensure all tables exist before querying

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
        low_stock_count = cur.fetchone()[0]
    except Exception:
        low_stock_count = 0
    try:
        cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= date('now', '+30 days', 'localtime') AND expiration_date IS NOT NULL")
        expiring_count = cur.fetchone()[0]
    except Exception:
        expiring_count = 0
    conn.close()

    return render_template('backup_restore.html',
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='management',
                           active_sub='backup_restore')

@app.route('/backup_database', methods=['POST'])
@admin_required
def backup_database():
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"pharmacon_backup_{timestamp}.sql"
        conn = get_db()
        sql_dump = '\n'.join(conn.iterdump())
        
        # Modify dump to include DROP TABLE IF EXISTS before CREATE TABLE
        # This allows restoring to an existing database
        modified_dump = []
        for line in sql_dump.split('\n'):
            if line.startswith('CREATE TABLE '):
                table_name = line.split('CREATE TABLE ')[1].split('(')[0].strip().strip('"')
                modified_dump.append(f'DROP TABLE IF EXISTS {table_name};')
            modified_dump.append(line)
        modified_dump = '\n'.join(modified_dump)
        
        # Exclude admin and cashier credentials (username, password) from backup
        # Filter out INSERT statements for admins and cashiers that contain credentials
        filtered_dump = []
        skip_insert = False
        for line in modified_dump.split('\n'):
            # Check if this is an INSERT for admins or cashiers table
            if line.strip().upper().startswith('INSERT INTO "ADMINS"') or line.strip().upper().startswith('INSERT INTO "CASHIERS"'):
                skip_insert = True
                # Replace with INSERT that excludes username and password columns
                if 'INSERT INTO "ADMINS"' in line.upper():
                    # Extract values and create new INSERT without username, password
                    filtered_dump.append('-- Admin credentials excluded from backup')
                elif 'INSERT INTO "CASHIERS"' in line.upper():
                    filtered_dump.append('-- Cashier credentials excluded from backup')
                continue
            elif skip_insert and line.strip().endswith(';'):
                skip_insert = False
                continue
            elif skip_insert:
                continue
            
            filtered_dump.append(line)
        
        final_dump = '\n'.join(filtered_dump)
        
        mem = BytesIO()
        mem.write(final_dump.encode('utf-8'))
        mem.seek(0)
        return send_file(mem, as_attachment=True, download_name=filename, mimetype='application/sql')
    except Exception as e:
        flash(f"Backup error: {str(e)}", "error")
        return redirect(url_for('backup_restore'))

def convert_mysql_to_sqlite(sql_content):
    """Convert MySQL SQL syntax to SQLite-compatible syntax."""
    
    # Remove CREATE DATABASE and USE statements
    lines = sql_content.split('\n')
    filtered_lines = []
    for line in lines:
        upper_line = line.strip().upper()
        if upper_line.startswith('CREATE DATABASE') or upper_line.startswith('USE '):
            continue
        filtered_lines.append(line)
    sql_content = '\n'.join(filtered_lines)
    
    # Replace data types
    sql_content = sql_content.replace('INT AUTO_INCREMENT PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
    sql_content = sql_content.replace('TINYINT(1)', 'INTEGER')
    sql_content = sql_content.replace('DECIMAL(10,2)', 'REAL')
    sql_content = sql_content.replace('DATETIME', 'TEXT')
    sql_content = sql_content.replace('TIMESTAMP DEFAULT CURRENT_TIMESTAMP', "TEXT DEFAULT (datetime('now', 'localtime'))")
    sql_content = sql_content.replace('TIMESTAMP NULL DEFAULT NULL', "TEXT NULL DEFAULT NULL")
    sql_content = sql_content.replace('TIMESTAMP', 'TEXT')
    
    # Remove ENGINE and CHARSET clauses
    import re
    sql_content = re.sub(r'\)\s*ENGINE=\w+.*?;', ');', sql_content)
    sql_content = re.sub(r'\)\s*DEFAULT CHARSET=\w+.*?;', ');', sql_content)
    sql_content = re.sub(r'COLLATE=\w+', '', sql_content)
    
    # Replace UNIQUE KEY with UNIQUE
    sql_content = re.sub(r'UNIQUE KEY\s+\w+\s*\(([^)]+)\)', r'UNIQUE(\1)', sql_content)
    
    # Replace INDEX with CREATE INDEX
    def replace_index(match):
        index_name = match.group(1)
        columns = match.group(2)
        table_name = match.group(3)
        return f'CREATE INDEX {index_name} ON {table_name}({columns})'
    
    sql_content = re.sub(
        r'INDEX\s+(\w+)\s*\(([^)]+)\)\s*ON\s+(\w+)',
        replace_index,
        sql_content
    )
    
    # Replace ON DUPLICATE KEY UPDATE with ON CONFLICT DO UPDATE SET
    sql_content = sql_content.replace('ON DUPLICATE KEY UPDATE', 'ON CONFLICT DO UPDATE SET')
    sql_content = sql_content.replace('VALUES(', 'excluded.')
    
    # Replace date functions
    sql_content = sql_content.replace('NOW()', "datetime('now', 'localtime')")
    sql_content = sql_content.replace('CURDATE()', "date('now', 'localtime')")
    
    # Replace date arithmetic
    sql_content = re.sub(
        r'CURDATE\(\)\s*\+\s*INTERVAL\s+(\d+)\s+DAY',
        r"date('now', '+\1 days', 'localtime')",
        sql_content
    )
    sql_content = re.sub(
        r'CURDATE\(\)\s*-\s*INTERVAL\s+(\d+)\s+DAY',
        r"date('now', '-\1 days', 'localtime')",
        sql_content
    )
    sql_content = re.sub(
        r'CURDATE\(\)\s*\+\s*INTERVAL\s+(\d+)\s+HOUR',
        r"datetime('now', '+\1 hours', 'localtime')",
        sql_content
    )
    sql_content = re.sub(
        r'CURDATE\(\)\s*-\s*INTERVAL\s+(\d+)\s+HOUR',
        r"datetime('now', '-\1 hours', 'localtime')",
        sql_content
    )
    
    # Replace DATEDIFF
    sql_content = re.sub(
        r'DATEDIFF\(([^,]+),\s*([^)]+)\)',
        r"CAST(julianday(\1) - julianday(\2) AS INTEGER)",
        sql_content
    )
    
    # Replace GROUP_CONCAT SEPARATOR
    sql_content = re.sub(
        r'GROUP_CONCAT\(([^)]+)\s+SEPARATOR\s+\', \'\)',
        r"GROUP_CONCAT(\1, ', ')",
        sql_content
    )
    
    # Replace MONTH() and YEAR()
    sql_content = re.sub(
        r'MONTH\(([^)]+)\)',
        r"strftime('%m', \1)",
        sql_content
    )
    sql_content = re.sub(
        r'YEAR\(([^)]+)\)',
        r"strftime('%Y', \1)",
        sql_content
    )
    
    return sql_content


@app.route('/restore_database', methods=['POST'])
@admin_required
def restore_database():
    try:
        if 'backup_file' not in request.files:
            flash("No file uploaded", "error")
            return redirect(url_for('backup_restore'))

        file = request.files['backup_file']
        if file.filename == '':
            flash("No file selected", "error")
            return redirect(url_for('backup_restore'))

        if not file.filename.endswith('.sql'):
            flash("Please upload a .sql file", "error")
            return redirect(url_for('backup_restore'))

        conn = get_db()
        cur = conn.cursor()

        # Read SQL content
        sql_content = file.read().decode('utf-8', errors='ignore')

        # Detect MySQL syntax and convert to SQLite if needed
        is_mysql = any(marker in sql_content.upper() for marker in [
            'CREATE DATABASE', 'AUTO_INCREMENT', 'ENGINE=', 'USE ',
            'TINYINT(1)', 'DECIMAL(10,2)', 'ON DUPLICATE KEY', '`'
        ])

        if is_mysql:
            sql_content = convert_mysql_to_sqlite(sql_content)
            flash("Converted MySQL format to SQLite-compatible syntax.", "info")

        # Disable foreign keys during restore
        cur.execute("PRAGMA foreign_keys = OFF")

        # Drop all existing tables EXCEPT admins and cashiers (preserve login accounts & credentials)
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row[0] for row in cur.fetchall()]
        for table_name in tables:
            if table_name in ('admins', 'cashiers'):
                continue
            try:
                cur.execute(f'DROP TABLE IF EXISTS "{table_name}"')
            except Exception:
                pass

        # Clean SQL: remove transaction control and skip admins/cashiers statements entirely
        # so registered admin/cashier credentials are never modified or overwritten
        sql_lines = []
        skip = False
        for line in sql_content.split('\n'):
            upper = line.strip().upper()

            # Strip transaction control (executescript manages its own transaction)
            if upper in ('BEGIN TRANSACTION;', 'COMMIT;', 'BEGIN;', 'ROLLBACK;'):
                continue

            # Skip admins/cashiers DDL/DML entirely — credentials stay as registered
            if upper.startswith('DROP TABLE IF EXISTS "ADMINS"') or upper.startswith("DROP TABLE IF EXISTS 'ADMINS'") or upper.startswith('DROP TABLE IF EXISTS ADMINS'):
                continue
            if upper.startswith('DROP TABLE IF EXISTS "CASHIERS"') or upper.startswith("DROP TABLE IF EXISTS 'CASHIERS'") or upper.startswith('DROP TABLE IF EXISTS CASHIERS'):
                continue
            if upper.startswith('CREATE TABLE "ADMINS"') or upper.startswith("CREATE TABLE 'ADMINS'") or upper.startswith('CREATE TABLE ADMINS'):
                continue
            if upper.startswith('CREATE TABLE "CASHIERS"') or upper.startswith("CREATE TABLE 'CASHIERS'") or upper.startswith('CREATE TABLE CASHIERS'):
                continue
            if upper.startswith('INSERT INTO "ADMINS"') or upper.startswith("INSERT INTO 'ADMINS'") or upper.startswith('INSERT INTO ADMINS'):
                skip = True
                continue
            if upper.startswith('INSERT INTO "CASHIERS"') or upper.startswith("INSERT INTO 'CASHIERS'") or upper.startswith('INSERT INTO CASHIERS'):
                skip = True
                continue
            if upper.startswith('DELETE FROM "ADMINS"') or upper.startswith("DELETE FROM 'ADMINS'") or upper.startswith('DELETE FROM ADMINS'):
                continue
            if upper.startswith('DELETE FROM "CASHIERS"') or upper.startswith("DELETE FROM 'CASHIERS'") or upper.startswith('DELETE FROM CASHIERS'):
                continue
            if upper.startswith('UPDATE "ADMINS"') or upper.startswith("UPDATE 'ADMINS'") or upper.startswith('UPDATE ADMINS'):
                continue
            if upper.startswith('UPDATE "CASHIERS"') or upper.startswith("UPDATE 'CASHIERS'") or upper.startswith('UPDATE CASHIERS'):
                continue

            if skip:
                if upper.endswith(';'):
                    skip = False
                continue

            sql_lines.append(line)

        sql_content_clean = '\n'.join(sql_lines)

        # Execute the cleaned SQL script
        cur.executescript(sql_content_clean)
        conn.commit()

        cur.execute("PRAGMA foreign_keys = ON")
        flash("Database restored successfully! Admin and cashier accounts and credentials are preserved as registered.", "success")
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        flash(f"Restore failed: {str(e)}", "error")

    return redirect(url_for('backup_restore'))

if __name__ == '__main__':
    from database_sqlite import init_db
    init_db()
    app.run(debug=True)
