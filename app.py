from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import os
import subprocess
import html as html_module
import csv
from io import BytesIO, StringIO

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400
app.config['SESSION_COOKIE_NAME'] = 'pharmacon_session'

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

def check_login_lockout(ip_address, username):
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT COUNT(*) FROM login_attempts 
            WHERE (ip_address = %s OR username_attempted = %s)
            AND locked_until IS NOT NULL AND locked_until > NOW()
        """, (ip_address, username))
        return cur.fetchone()[0] > 0
    finally:
        cur.close()

def record_login_attempt(ip_address, username, success):
    cur = mysql.connection.cursor()
    try:
        if success:
            cur.execute("""
                DELETE FROM login_attempts 
                WHERE (ip_address = %s OR username_attempted = %s)
            """, (ip_address, username))
        else:
            cur.execute("""
                INSERT INTO login_attempts (ip_address, username_attempted, attempted_at)
                VALUES (%s, %s, NOW())
            """, (ip_address, username))
            cur.execute("""
                SELECT COUNT(*) FROM login_attempts 
                WHERE (ip_address = %s OR username_attempted = %s)
                AND attempted_at > NOW() - INTERVAL 1 HOUR
            """, (ip_address, username))
            attempts = cur.fetchone()[0]
            if attempts >= MAX_LOGIN_ATTEMPTS:
                cur.execute("""
                    UPDATE login_attempts 
                    SET locked_until = NOW() + INTERVAL %s MINUTE
                    WHERE (ip_address = %s OR username_attempted = %s)
                    AND attempted_at > NOW() - INTERVAL 1 HOUR
                """, (LOCKOUT_MINUTES, ip_address, username))
        mysql.connection.commit()
    finally:
        cur.close()

# Add datetime to template context
@app.context_processor
def inject_datetime():
    return dict(datetime=datetime, LOW_STOCK_THRESHOLD=LOW_STOCK_THRESHOLD, csrf_token=generate_csrf_token)

def clean_input(value):
    if not value:
        return ""
    return value.strip()

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pharmacon'

mysql = MySQL(app)

# Low stock threshold
LOW_STOCK_THRESHOLD = 10

# OOP Imports and Service Instances
from models import Product, StockMovement, Cashier
from services import AuthService, ProductRepository, SalesService
auth_service = AuthService()
product_repository = ProductRepository(mysql)
sales_service = SalesService(mysql)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_user' not in session or session.get('role') != 'admin':
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

        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT status FROM cashiers WHERE id=%s", (session['cashier_id'],))
            cashier_status = cur.fetchone()
        finally:
            cur.close()

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
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')

        if check_login_lockout(ip_address, username):
            flash("Account temporarily locked due to too many failed attempts. Please try again later.", "error")
            return redirect(url_for('admin_login'))

        if username == "" or password == "":
            flash("All fields are required", "error")
            return redirect(url_for('admin_login'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, password FROM admins WHERE username=%s", (username,))
        admin = cur.fetchone()
        cur.close()

        # Create default admin if none exists, or patch security fields if missing
        if not admin:
            cur = mysql.connection.cursor()
            cur.execute("SELECT COUNT(*) FROM admins")
            count = cur.fetchone()[0]
            cur.close()
            if count == 0:
                hashed = generate_password_hash('admin123')
                from werkzeug.security import generate_password_hash as gen_hash
                answer_hashed = gen_hash('admin123')
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO admins (username, password, full_name, security_question, security_answer, force_password_change) VALUES (%s, %s, %s, %s, %s, %s)", ('admin', hashed, 'System Administrator', 'What is the name of the owner?', 'pbkdf2:sha256:600000$BlhM6ndrgPIj0Eui$8c0c6511b8af1f42401c742e1da56b34bfb60e56d703087fcc4f013f2cc2ecae', 1))
                mysql.connection.commit()
                cur.close()
                cur = mysql.connection.cursor()
                cur.execute("SELECT id, username, password FROM admins WHERE username='admin'")
                admin = cur.fetchone()
                cur.close()
            else:
                flash("Invalid username or password", "error")
                return redirect(url_for('admin_login'))
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT security_question, security_answer FROM admins WHERE id=%s", (admin[0],))
            sq = cur.fetchone()
            cur.close()
            if not sq or not sq[0] or not sq[1]:
                hashed_answer = generate_password_hash('generoso')
                cur = mysql.connection.cursor()
                cur.execute("UPDATE admins SET security_question=%s, security_answer=%s WHERE id=%s", ('What is the name of the owner?', hashed_answer, admin[0]))
                mysql.connection.commit()
                cur.close()
        
        if admin and (password == admin[2] or check_password_hash(admin[2], password)):
            force_change = False
            try:
                cur = mysql.connection.cursor()
                cur.execute("SELECT force_password_change FROM admins WHERE id=%s", (admin[0],))
                fc_row = cur.fetchone()
                cur.close()
                if fc_row and fc_row[0]:
                    force_change = True
            except Exception:
                pass
            
            if force_change:
                session['pending_admin_id'] = admin[0]
                session['pending_admin_user'] = admin[1]
                flash("You must change your password before continuing.", "error")
                return redirect(url_for('admin_change_password'))
            
            session['admin_user'] = admin[1]
            session['admin_id'] = admin[0]
            session['role'] = 'admin'
            session.permanent = True  # Session persists on refresh
            
            # Log admin login activity
            cur = mysql.connection.cursor()
            ip_address = request.remote_addr
            if request.headers.get('X-Forwarded-For'):
                ip_address = request.headers.get('X-Forwarded-For')
            
            try:
                cur.execute("""
                    INSERT INTO admin_activity (admin_id, action, ip_address, details)
                    VALUES (%s, %s, %s, %s)
                """, (admin[0], 'Admin Login', ip_address, f'Admin {admin[1]} logged in'))
                mysql.connection.commit()
            except:
                pass  # Table might not exist yet
            cur.close()
            record_login_attempt(ip_address, username, True)
            return redirect(url_for('admin_dashboard'))
        else:
            record_login_attempt(ip_address, username, False)
            flash("Invalid login credentials", "error")
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

# =============================
# ADMIN DASHBOARD
# =============================

@app.route('/admin')
@admin_required
def admin_dashboard():
    cur = mysql.connection.cursor()
    
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
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock = 0")
    total_out_of_stock = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(DISTINCT p.id) FROM products p
        LEFT JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'out_of_stock'
        WHERE p.stock = 0 AND (al.id IS NULL OR (al.acknowledged_by IS NULL AND al.dismissed_by IS NULL))
    """)
    out_of_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock > 0 AND stock <= %s", (LOW_STOCK_THRESHOLD,))
    total_low_stock = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(DISTINCT p.id) FROM products p
        LEFT JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'low_stock'
        WHERE p.stock > 0 AND p.stock <= %s AND (al.id IS NULL OR (al.acknowledged_by IS NULL AND al.dismissed_by IS NULL))
    """, (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date < CURDATE() AND expiration_date IS NOT NULL")
    total_expired = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(DISTINCT p.id) FROM products p
        LEFT JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'expired'
        WHERE p.expiration_date < CURDATE() AND p.expiration_date IS NOT NULL AND (al.id IS NULL OR (al.acknowledged_by IS NULL AND al.dismissed_by IS NULL))
    """)
    expired_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date >= CURDATE() AND expiration_date <= CURDATE() + INTERVAL 7 DAY AND expiration_date IS NOT NULL")
    total_expiring_critical = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(DISTINCT p.id) FROM products p
        LEFT JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'expiring_medical'
        WHERE p.expiration_date >= CURDATE() AND p.expiration_date <= CURDATE() + INTERVAL 7 DAY AND p.expiration_date IS NOT NULL AND (al.id IS NULL OR (al.acknowledged_by IS NULL AND al.dismissed_by IS NULL))
    """)
    expiring_critical_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date > CURDATE() + INTERVAL 7 DAY AND expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    total_expiring_warning = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(DISTINCT p.id) FROM products p
        LEFT JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'expiring_medical'
        WHERE p.expiration_date > CURDATE() + INTERVAL 7 DAY AND p.expiration_date <= CURDATE() + INTERVAL 30 DAY AND p.expiration_date IS NOT NULL AND (al.id IS NULL OR (al.acknowledged_by IS NULL AND al.dismissed_by IS NULL))
    """)
    expiring_warning_count = cur.fetchone()[0]
    
    total_alert_count = out_of_stock_count + low_stock_count + expired_count + expiring_critical_count + expiring_warning_count
    
    cur.close()

    return render_template('admin_dashboard.html',
                           cashiers=cashiers,
                           active_cashiers=active_cashiers,
                           activity_logs=activity_logs,
                           out_of_stock_count=out_of_stock_count,
                           low_stock_count=low_stock_count,
                           expired_count=expired_count,
                           expiring_critical_count=expiring_critical_count,
                           expiring_warning_count=expiring_warning_count,
                           total_alert_count=total_alert_count,
                           active_main='admin',
                           active_sub='dashboard')

@app.route('/admin/cashier_logs')
@admin_required
def cashier_logs():
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT c.full_name, c.username, ca.login_time, ca.logout_time, ca.ip_address
        FROM cashier_activity ca
        JOIN cashiers c ON c.id = ca.cashier_id
        ORDER BY ca.login_time DESC
    """)
    activity_logs = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    cur.close()

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
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT a.username, aa.action, aa.ip_address, aa.details, aa.activity_time
        FROM admin_activity aa
        JOIN admins a ON aa.admin_id = a.id
        ORDER BY aa.activity_time DESC
        LIMIT 50
    """)
    admin_logs = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    cur.close()

    return render_template('admin_activity_logs.html', 
                           admin_logs=admin_logs,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='dashboard', 
                           active_sub='activity_logs')

# =============================
# NOTIFICATIONS API
# =============================

@app.route('/api/notifications')
@admin_required
def get_notifications():
    cur = mysql.connection.cursor()
    admin_id = session.get('admin_id')
    
    hidden_products = set()
    if admin_id:
        cur.execute("SELECT product_id, alert_type FROM alert_visibility WHERE admin_id = %s AND is_hidden = 1", (admin_id,))
        for row in cur.fetchall():
            hidden_products.add(f"{row[0]}_{row[1]}")
    
    cur.execute("""
        SELECT id, product_name, stock, barcode 
        FROM products 
        WHERE stock = 0
        ORDER BY stock ASC
        LIMIT 10
    """)
    out_of_stock = [p for p in cur.fetchall() if f"{p[0]}_out_of_stock" not in hidden_products]
    
    cur.execute("""
        SELECT id, product_name, stock, barcode 
        FROM products 
        WHERE stock > 0 AND stock <= %s
        ORDER BY stock ASC
        LIMIT 10
    """, (LOW_STOCK_THRESHOLD,))
    low_stock = [p for p in cur.fetchall() if f"{p[0]}_low_stock" not in hidden_products]
    
    cur.execute("""
        SELECT id, product_name, expiration_date, barcode,
               DATEDIFF(expiration_date, CURDATE()) as days_left
        FROM products 
        WHERE expiration_date < CURDATE()
        AND expiration_date IS NOT NULL
        ORDER BY expiration_date ASC
        LIMIT 10
    """)
    expired = [p for p in cur.fetchall() if f"{p[0]}_expired" not in hidden_products]
    
    cur.execute("""
        SELECT id, product_name, expiration_date, barcode,
               DATEDIFF(expiration_date, CURDATE()) as days_left
        FROM products 
        WHERE expiration_date >= CURDATE()
        AND expiration_date <= CURDATE() + INTERVAL 7 DAY
        AND expiration_date IS NOT NULL
        ORDER BY expiration_date ASC
        LIMIT 10
    """)
    expiring_critical = [p for p in cur.fetchall() if f"{p[0]}_expiring_critical" not in hidden_products]
    
    cur.execute("""
        SELECT id, product_name, expiration_date, barcode,
               DATEDIFF(expiration_date, CURDATE()) as days_left
        FROM products 
        WHERE expiration_date > CURDATE() + INTERVAL 7 DAY
        AND expiration_date <= CURDATE() + INTERVAL 30 DAY
        AND expiration_date IS NOT NULL
        ORDER BY expiration_date ASC
        LIMIT 10
    """)
    expiring_warning = [p for p in cur.fetchall() if f"{p[0]}_expiring_warning" not in hidden_products]
    
    cur.close()
    
    return jsonify({
        'out_of_stock': [{'id': p[0], 'name': p[1], 'stock': p[2], 'barcode': p[3]} for p in out_of_stock],
        'low_stock': [{'id': p[0], 'name': p[1], 'stock': p[2], 'barcode': p[3]} for p in low_stock],
        'expired': [{'id': p[0], 'name': p[1], 'expiry': str(p[2]), 'barcode': p[3], 'days_left': p[4]} for p in expired],
        'expiring_critical': [{'id': p[0], 'name': p[1], 'expiry': str(p[2]), 'barcode': p[3], 'days_left': p[4]} for p in expiring_critical],
        'expiring_warning': [{'id': p[0], 'name': p[1], 'expiry': str(p[2]), 'barcode': p[3], 'days_left': p[4]} for p in expiring_warning]
    })

@app.route('/api/cashier/notifications')
@cashier_required
def get_cashier_notifications():
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT id, product_name, stock, barcode
            FROM products
            WHERE stock = 0
            ORDER BY stock ASC
            LIMIT 10
        """)
        out_of_stock = cur.fetchall()

        cur.execute("""
            SELECT id, product_name, stock, barcode
            FROM products
            WHERE stock > 0 AND stock <= %s
            ORDER BY stock ASC
            LIMIT 10
        """, (LOW_STOCK_THRESHOLD,))
        low_stock = cur.fetchall()

        cur.execute("""
            SELECT id, product_name, expiration_date, barcode,
                   DATEDIFF(expiration_date, CURDATE()) as days_left
            FROM products
            WHERE expiration_date < CURDATE()
              AND expiration_date IS NOT NULL
            ORDER BY expiration_date ASC
            LIMIT 10
        """)
        expired = cur.fetchall()

        cur.execute("""
            SELECT id, product_name, expiration_date, barcode,
                   DATEDIFF(expiration_date, CURDATE()) as days_left
            FROM products
            WHERE expiration_date >= CURDATE()
              AND expiration_date <= CURDATE() + INTERVAL 7 DAY
              AND expiration_date IS NOT NULL
            ORDER BY expiration_date ASC
            LIMIT 10
        """)
        expiring_critical = cur.fetchall()

        cur.execute("""
            SELECT id, product_name, expiration_date, barcode,
                   DATEDIFF(expiration_date, CURDATE()) as days_left
            FROM products
            WHERE expiration_date > CURDATE() + INTERVAL 7 DAY
              AND expiration_date <= CURDATE() + INTERVAL 30 DAY
              AND expiration_date IS NOT NULL
            ORDER BY expiration_date ASC
            LIMIT 10
        """)
        expiring_warning = cur.fetchall()

        return jsonify({
            'out_of_stock': [{'id': p[0], 'name': p[1], 'stock': p[2], 'barcode': p[3]} for p in out_of_stock],
            'low_stock': [{'id': p[0], 'name': p[1], 'stock': p[2], 'barcode': p[3]} for p in low_stock],
            'expired': [{'id': p[0], 'name': p[1], 'expiry': str(p[2]), 'barcode': p[3], 'days_left': p[4]} for p in expired],
            'expiring_critical': [{'id': p[0], 'name': p[1], 'expiry': str(p[2]), 'barcode': p[3], 'days_left': p[4]} for p in expiring_critical],
            'expiring_warning': [{'id': p[0], 'name': p[1], 'expiry': str(p[2]), 'barcode': p[3], 'days_left': p[4]} for p in expiring_warning]
        })
    finally:
        cur.close()

@app.route('/api/alert/acknowledge', methods=['POST'])
def acknowledge_alert():
    if 'admin_user' not in session and 'cashier_user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.get_json() or {}
    alert_type = clean_input(data.get('alert_type', ''))
    product_id = data.get('product_id')
    if not alert_type or not product_id:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400
    user_id = session.get('admin_id') or session.get('cashier_id')
    user_type = 'admin' if 'admin_user' in session else 'cashier'
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO alert_logs (alert_type, alert_level, product_id, message, acknowledged_by, acknowledged_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE acknowledged_by = VALUES(acknowledged_by), acknowledged_at = VALUES(acknowledged_at)
        """, (alert_type, 'info', product_id, f'{alert_type} alert acknowledged', user_id))
        if user_type == 'admin':
            cur.execute("""
                INSERT INTO alert_visibility (product_id, alert_type, admin_id, is_hidden)
                VALUES (%s, %s, %s, 1)
                ON DUPLICATE KEY UPDATE is_hidden = 1, updated_at = NOW()
            """, (product_id, alert_type, user_id))
        mysql.connection.commit()
        return jsonify({'success': True, 'message': 'Alert acknowledged'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cur.close()

@app.route('/api/alert/dismiss', methods=['POST'])
def dismiss_alert():
    if 'admin_user' not in session and 'cashier_user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.get_json() or {}
    alert_type = clean_input(data.get('alert_type', ''))
    product_id = data.get('product_id')
    reason = clean_input(data.get('reason', ''))
    if not alert_type or not product_id:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400
    user_id = session.get('admin_id') or session.get('cashier_id')
    user_type = 'admin' if 'admin_user' in session else 'cashier'
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO alert_logs (alert_type, alert_level, product_id, message, dismissed_by, dismissed_at, dismiss_reason)
            VALUES (%s, %s, %s, %s, %s, NOW(), %s)
            ON DUPLICATE KEY UPDATE dismissed_by = VALUES(dismissed_by), dismissed_at = VALUES(dismissed_at), dismiss_reason = VALUES(dismiss_reason)
        """, (alert_type, 'info', product_id, f'{alert_type} alert dismissed', user_id, reason))
        if user_type == 'admin':
            cur.execute("""
                INSERT INTO alert_visibility (product_id, alert_type, admin_id, is_hidden)
                VALUES (%s, %s, %s, 1)
                ON DUPLICATE KEY UPDATE is_hidden = 1, updated_at = NOW()
            """, (product_id, alert_type, user_id))
        mysql.connection.commit()
        return jsonify({'success': True, 'message': 'Alert dismissed'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cur.close()

@app.route('/api/alert/resolve', methods=['POST'])
def resolve_alert():
    if 'admin_user' not in session and 'cashier_user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.get_json() or {}
    alert_type = clean_input(data.get('alert_type', ''))
    product_id = data.get('product_id')
    if not alert_type or not product_id:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400
    user_id = session.get('admin_id') or session.get('cashier_id')
    user_type = 'admin' if 'admin_user' in session else 'cashier'
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO alert_logs (alert_type, alert_level, product_id, message, acknowledged_by, acknowledged_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE acknowledged_by = VALUES(acknowledged_by), acknowledged_at = VALUES(acknowledged_at)
        """, (alert_type, 'info', product_id, f'{alert_type} alert resolved', user_id))
        if user_type == 'admin':
            cur.execute("""
                INSERT INTO alert_visibility (product_id, alert_type, admin_id, is_hidden)
                VALUES (%s, %s, %s, 1)
                ON DUPLICATE KEY UPDATE is_hidden = 1, updated_at = NOW()
            """, (product_id, alert_type, user_id))
        mysql.connection.commit()
        return jsonify({'success': True, 'message': 'Alert resolved'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cur.close()

@app.route('/api/alert/bulk_acknowledge', methods=['POST'])
def bulk_acknowledge_alert():
    if 'admin_user' not in session and 'cashier_user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.get_json() or {}
    alert_type = clean_input(data.get('alert_type', ''))
    product_ids = data.get('product_ids', [])
    if not alert_type or not product_ids:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400
    user_id = session.get('admin_id') or session.get('cashier_id')
    cur = mysql.connection.cursor()
    try:
        for pid in product_ids:
            cur.execute("""
                INSERT INTO alert_logs (alert_type, alert_level, product_id, message, acknowledged_by, acknowledged_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE acknowledged_by = VALUES(acknowledged_by), acknowledged_at = VALUES(acknowledged_at)
            """, (alert_type, 'info', pid, f'{alert_type} alert bulk acknowledged', user_id))
        mysql.connection.commit()
        return jsonify({'success': True, 'message': f'{len(product_ids)} alerts acknowledged'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cur.close()

@app.route('/api/alert/bulk_dismiss', methods=['POST'])
def bulk_dismiss_alert():
    if 'admin_user' not in session and 'cashier_user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.get_json() or {}
    alert_type = clean_input(data.get('alert_type', ''))
    product_ids = data.get('product_ids', [])
    reason = clean_input(data.get('reason', ''))
    if not alert_type or not product_ids:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400
    user_id = session.get('admin_id') or session.get('cashier_id')
    user_type = 'admin' if 'admin_user' in session else 'cashier'
    cur = mysql.connection.cursor()
    try:
        for pid in product_ids:
            cur.execute("""
                INSERT INTO alert_logs (alert_type, alert_level, product_id, message, dismissed_by, dismissed_at, dismiss_reason)
                VALUES (%s, %s, %s, %s, %s, NOW(), %s)
                ON DUPLICATE KEY UPDATE dismissed_by = VALUES(dismissed_by), dismissed_at = VALUES(dismissed_at), dismiss_reason = VALUES(dismiss_reason)
            """, (alert_type, 'info', pid, f'{alert_type} alert bulk dismissed', user_id, reason))
            if user_type == 'admin':
                cur.execute("""
                    INSERT INTO alert_visibility (product_id, alert_type, admin_id, is_hidden)
                    VALUES (%s, %s, %s, 1)
                    ON DUPLICATE KEY UPDATE is_hidden = 1, updated_at = NOW()
                """, (pid, alert_type, user_id))
        mysql.connection.commit()
        return jsonify({'success': True, 'message': f'{len(product_ids)} alerts dismissed'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cur.close()

@app.route('/api/alert/status')
def alert_status():
    if 'admin_user' not in session and 'cashier_user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    admin_id = session.get('admin_id')
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM alert_logs WHERE acknowledged_by IS NULL AND dismissed_by IS NULL")
        unacknowledged = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM alert_logs WHERE acknowledged_by IS NOT NULL")
        acknowledged = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM alert_logs WHERE dismissed_by IS NOT NULL")
        dismissed = cur.fetchone()[0]
        return jsonify({
            'unacknowledged': unacknowledged,
            'acknowledged': acknowledged,
            'dismissed': dismissed
        })
    finally:
        cur.close()

# =============================
# CATALOG
# =============================

@app.route('/all_products')
@admin_required
def all_products():
    from datetime import date
    cur = mysql.connection.cursor()
    search = request.args.get('search', '').strip()
    if search:
        cur.execute("SELECT * FROM products WHERE product_name LIKE %s OR barcode LIKE %s", (f'%{search}%', f'%{search}%'))
    else:
        cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    cur.close()
    return render_template('all_products.html', products=products,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='inventory', active_sub='all_products',
                           search=search, today=date.today())

@app.route('/add_product', methods=['GET', 'POST'])
@admin_required
def add_product():
    cur = mysql.connection.cursor()

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
                cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
                low_stock_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
                expiring_count = cur.fetchone()[0]
                cur.close()
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
                cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
                low_stock_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
                expiring_count = cur.fetchone()[0]
                cur.close()
                return render_template('add_product.html', 
                               categories=categories, 
                               low_stock_count=low_stock_count,
                               expiring_count=expiring_count,
                               active_main='inventory', 
                               active_sub='add_product')
        
        expiry = request.form.get('expiration_date') or None  # From template: expiration_date

        # Get category_id from category name
        cur.execute("SELECT id FROM categories WHERE category_name=%s", (category_name,))
        cat_result = cur.fetchone()
        category_id = cat_result[0] if cat_result else None
        
        try:
            # Check if product exists with same name AND expiration date (barcode can be empty or same)
            if barcode:
                cur.execute("""
                    SELECT id, stock FROM products 
                    WHERE product_name = %s AND barcode = %s AND expiration_date = %s
                """, (name, barcode, expiry))
            else:
                cur.execute("""
                    SELECT id, stock FROM products 
                    WHERE product_name = %s AND (barcode IS NULL OR barcode = '') AND expiration_date = %s
                """, (name, expiry))
            existing = cur.fetchone()
            
            if existing:
                # Update stock if product exists with same expiry
                new_stock = existing[1] + int(stock)
                cur.execute("UPDATE products SET stock = %s WHERE id = %s", (new_stock, existing[0]))
                product_id = existing[0]
                message = f"Stock updated! Added {stock} units. Total: {new_stock}"
                action = 'Stock Update'
            else:
                # Insert new product if different expiry or new product
                query = """
                    INSERT INTO products (product_name, barcode, category_id, product_type, price, stock, expiration_date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
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
                VALUES (%s, 'IN', %s, 'Stock Addition')
            """
            cur.execute(movement_query, (product_id, stock))
            
            # Log admin activity
            ip_address = request.remote_addr
            if request.headers.get('X-Forwarded-For'):
                ip_address = request.headers.get('X-Forwarded-For')
            
            try:
                cur.execute("""
                    INSERT INTO admin_activity (admin_id, action, ip_address, details)
                    VALUES (%s, %s, %s, %s)
                """, (session.get('admin_id'), action, ip_address, f'{name} - {stock} units added'))
            except:
                pass  # Table might not exist yet
            
            mysql.connection.commit()
            cur.close()
            
            # Return JSON response for AJAX, render same page for normal form submission (to show flash message)
            if is_ajax:
                return jsonify({'success': True, 'message': message})
            else:
                flash(message, "success")
                # Create new cursor for rendering page
                cur = mysql.connection.cursor()
                try:
                    cur.execute("SELECT id, category_name FROM categories ORDER BY category_name ASC")
                    categories = cur.fetchall()
                except Exception as e:
                    categories = []
                    flash(f"Error loading categories: {str(e)}", "error")
                
                cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
                low_stock_count = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
                expiring_count = cur.fetchone()[0]
                cur.close()
                
                return render_template('add_product.html', 
                               categories=categories, 
                               low_stock_count=low_stock_count,
                               expiring_count=expiring_count,
                               active_main='inventory', 
                               active_sub='add_product')
            
        except Exception as e:
            mysql.connection.rollback()
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
                cur = mysql.connection.cursor()
                try:
                    cur.execute("SELECT id, category_name FROM categories ORDER BY category_name ASC")
                    categories = cur.fetchall()
                except Exception as ex:
                    categories = []
                    
                cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
                low_stock_count = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
                expiring_count = cur.fetchone()[0]
                cur.close()
                
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
            cur.close()
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
        low_stock_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
        expiring_count = cur.fetchone()[0]
        cur.close()
        
        return render_template('add_product.html', 
                               categories=categories, 
                               low_stock_count=low_stock_count,
                               expiring_count=expiring_count,
                               active_main='inventory', 
                               active_sub='add_product')

@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
@admin_required
def delete_product(id):
    cur = mysql.connection.cursor()
    
    if request.method == 'GET':
        cur.execute("SELECT id, product_name, barcode, stock FROM products WHERE id=%s", (id,))
        product = cur.fetchone()
        if not product:
            flash("Product not found", "error")
            return redirect(url_for('all_products'))
        
        cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
        low_stock_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
        expiring_count = cur.fetchone()[0]
        
        cur.close()
        return render_template('confirm_delete_product.html', product=product,
                               low_stock_count=low_stock_count,
                               expiring_count=expiring_count,
                               active_main='inventory', active_sub='all_products')
    
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        
        # Get product info before deleting
        cur.execute("SELECT product_name FROM products WHERE id=%s", (id,))
        product_info = cur.fetchone()
        product_name = product_info[0] if product_info else "Unknown"
        
        # Delete related records first (stock_movements and sale_items)
        cur.execute("DELETE FROM stock_movements WHERE product_id=%s", (id,))
        cur.execute("DELETE FROM sale_items WHERE product_id=%s", (id,))
        
        # Now delete the product
        cur.execute("DELETE FROM products WHERE id=%s", (id,))
        mysql.connection.commit()
        
        # Log admin activity
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            cur.execute("""
                INSERT INTO admin_activity (admin_id, action, ip_address, details)
                VALUES (%s, %s, %s, %s)
            """, (session.get('admin_id'), 'Delete Product', ip_address, f'Deleted product: {product_name}'))
            mysql.connection.commit()
        except:
            pass
        
        cur.close()
        flash("Product deleted successfully", "success")
        return redirect(url_for('all_products'))

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    cur = mysql.connection.cursor()
    
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
        
        cur.execute("SELECT id FROM categories WHERE category_name=%s", (category,))
        cat_result = cur.fetchone()
        category_id = cat_result[0] if cat_result else None
        
        cur.execute("""
            UPDATE products 
            SET product_name=%s, barcode=%s, category_id=%s, product_type=%s, price=%s, stock=%s, expiration_date=%s
            WHERE id=%s
        """, (product_name, barcode, category_id, category, price, stock, expiration_date, id))
        
        mysql.connection.commit()
        
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            cur.execute("""
                INSERT INTO admin_activity (admin_id, action, ip_address, details)
                VALUES (%s, %s, %s, %s)
            """, (session.get('admin_id'), 'Edit Product', ip_address, f'Edited product: {product_name}'))
            mysql.connection.commit()
        except:
            pass
        
        cur.close()
        flash("Product updated successfully", "success")
        return redirect(url_for('all_products'))
    
    cur.execute("SELECT * FROM products WHERE id=%s", (id,))
    product = cur.fetchone()
    
    cur.execute("SELECT id, category_name FROM categories ORDER BY category_name ASC")
    categories = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    cur.close()
    
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
    cur = mysql.connection.cursor()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    export = request.args.get('export', '').strip()

    where = ["s.sale_status = 'Completed'"]
    params = []
    if date_from:
        where.append("DATE(s.sale_date) >= %s")
        params.append(date_from)
    if date_to:
        where.append("DATE(s.sale_date) <= %s")
        params.append(date_to)
    where_clause = " AND ".join(where)

    cur.execute(f"""
        SELECT s.id, s.receipt_number, 
               GROUP_CONCAT(DISTINCT CASE WHEN p.product_type = 'Medical' THEN p.product_name END SEPARATOR ', ') as products, 
               s.total_amount, s.sale_status, s.product_type, s.sale_date
        FROM sales s
        LEFT JOIN sale_items si ON s.id = si.sale_id
        LEFT JOIN products p ON si.product_id = p.id
        WHERE p.product_type = 'Medical' AND {where_clause}
        GROUP BY s.id
        ORDER BY s.sale_date DESC
    """, tuple(params))
    sales = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]

    chart_labels = []
    chart_values = []
    if not export:
        cur.execute(f"""
            SELECT DATE(sale_date) as day, SUM(total_amount) as daily_total
            FROM sales s
            WHERE s.sale_status = 'Completed' 
            AND s.product_type = 'Medical'
            AND s.sale_date >= CURDATE() - INTERVAL 30 DAY
            GROUP BY DATE(sale_date)
            ORDER BY day ASC
        """)
        chart_data = cur.fetchall()
        chart_labels = [str(row[0]) for row in chart_data]
        chart_values = [float(row[1]) for row in chart_data]

    if export == 'csv':
        cur.execute("""
            SELECT s.receipt_number, s.sale_date, s.total_amount, s.sale_status,
                   GROUP_CONCAT(DISTINCT p.product_name SEPARATOR ', ') as products
            FROM sales s
            JOIN sale_items si ON s.id = si.sale_id
            JOIN products p ON si.product_id = p.id
            WHERE s.sale_status = 'Completed' AND p.product_type = 'Medical'
            GROUP BY s.id
            ORDER BY s.sale_date DESC
        """)
        export_data = cur.fetchall()
        cur.close()

        from io import StringIO, BytesIO
        text_output = StringIO()
        writer = csv.writer(text_output)
        writer.writerow(['Receipt #', 'Products', 'Total', 'Date', 'Status'])
        for s in export_data:
            writer.writerow([s[0], s[4] or '', f"{s[2]:.2f}", s[1].strftime('%Y-%m-%d %H:%M') if s[1] else '', s[3]])
        csv_bytes = text_output.getvalue().encode('utf-8-sig')
        output = BytesIO(csv_bytes)
        output.seek(0)
        return send_file(output, mimetype='text/csv; charset=utf-8', as_attachment=True, download_name=f"medical_sales_{datetime.now().strftime('%Y%m%d')}.csv")

    cur.close()

    return render_template('sales_medical.html', sales=sales,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           chart_labels=chart_labels, chart_values=chart_values,
                           date_from=date_from, date_to=date_to,
                           active_main='sales', active_sub='medical_sales')

@app.route('/sales_dashboard')
@admin_required
def sales_dashboard():
    """Admin sales dashboard with all views"""
    cur = mysql.connection.cursor()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    export = request.args.get('export', '').strip()

    custom_range = bool(date_from or date_to)
    if custom_range:
        date_filter = "DATE(sale_date) >= %s AND DATE(sale_date) <= %s"
        date_params = [date_from or '2000-01-01', date_to or '2099-12-31']
    else:
        date_filter = "DATE(sale_date) = CURDATE()"
        date_params = []

    def exec_with_date(sql):
        if custom_range:
            return cur.execute(sql, tuple(date_params))
        return cur.execute(sql)

    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]

    if custom_range:
        cur.execute(f"""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE {date_filter} AND sale_status = 'Completed' AND product_type = 'Medical'
        """, tuple(date_params))
        daily_medical = cur.fetchone()
        daily_medical_sales = float(daily_medical[0]) if daily_medical[0] else 0

        cur.execute(f"""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE {date_filter} AND sale_status = 'Completed' AND product_type = 'Non-Medical'
        """, tuple(date_params))
        daily_nonmedical = cur.fetchone()
        daily_nonmedical_sales = float(daily_nonmedical[0]) if daily_nonmedical[0] else 0

        daily_sales = daily_medical_sales + daily_nonmedical_sales
        daily_count = daily_medical[1] if daily_medical[1] else 0

        cur.execute(f"""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE {date_filter} AND sale_status = 'Completed' AND product_type = 'Medical'
        """, tuple(date_params))
        weekly_medical = cur.fetchone()
        weekly_medical_sales = float(weekly_medical[0]) if weekly_medical[0] else 0

        cur.execute(f"""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE {date_filter} AND sale_status = 'Completed' AND product_type = 'Non-Medical'
        """, tuple(date_params))
        weekly_nonmedical = cur.fetchone()
        weekly_nonmedical_sales = float(weekly_nonmedical[0]) if weekly_nonmedical[0] else 0

        weekly_sales = weekly_medical_sales + weekly_nonmedical_sales
        weekly_count = weekly_medical[1] if weekly_medical[1] else 0

        cur.execute(f"""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE {date_filter} AND sale_status = 'Completed' AND product_type = 'Medical'
        """, tuple(date_params))
        monthly_medical = cur.fetchone()
        monthly_medical_sales = float(monthly_medical[0]) if monthly_medical[0] else 0

        cur.execute(f"""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE {date_filter} AND sale_status = 'Completed' AND product_type = 'Non-Medical'
        """, tuple(date_params))
        monthly_nonmedical = cur.fetchone()
        monthly_nonmedical_sales = float(monthly_nonmedical[0]) if monthly_nonmedical[0] else 0

        monthly_sales = monthly_medical_sales + monthly_nonmedical_sales
        monthly_count = monthly_medical[1] if monthly_medical[1] else 0

        cur.execute(f"""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE {date_filter} AND sale_status = 'Completed' AND product_type = 'Medical'
        """, tuple(date_params))
        yearly_medical = cur.fetchone()
        yearly_medical_sales = float(yearly_medical[0]) if yearly_medical[0] else 0

        cur.execute(f"""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE {date_filter} AND sale_status = 'Completed' AND product_type = 'Non-Medical'
        """, tuple(date_params))
        yearly_nonmedical = cur.fetchone()
        yearly_nonmedical_sales = float(yearly_nonmedical[0]) if yearly_nonmedical[0] else 0

        yearly_sales = yearly_medical_sales + yearly_nonmedical_sales
        yearly_count = yearly_medical[1] if yearly_medical[1] else 0

        cur.execute(f"""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales WHERE sale_status = 'Completed' AND product_type = 'Medical'
        """)
        overall_medical = cur.fetchone()
        overall_medical_sales = float(overall_medical[0]) if overall_medical[0] else 0

        cur.execute(f"""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales WHERE sale_status = 'Completed' AND product_type = 'Non-Medical'
        """)
        overall_nonmedical = cur.fetchone()
        overall_nonmedical_sales = float(overall_nonmedical[0]) if overall_nonmedical[0] else 0

        overall_sales = overall_medical_sales + overall_nonmedical_sales
        overall_count = overall_medical[1] if overall_medical[1] else 0
    else:
        cur.execute("""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE DATE(sale_date) = CURDATE() AND sale_status = 'Completed' AND product_type = 'Medical'
        """)
        daily_medical = cur.fetchone()
        daily_medical_sales = float(daily_medical[0]) if daily_medical[0] else 0

        cur.execute("""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE DATE(sale_date) = CURDATE() AND sale_status = 'Completed' AND product_type = 'Non-Medical'
        """)
        daily_nonmedical = cur.fetchone()
        daily_nonmedical_sales = float(daily_nonmedical[0]) if daily_nonmedical[0] else 0

        daily_sales = daily_medical_sales + daily_nonmedical_sales
        daily_count = daily_medical[1] if daily_medical[1] else 0

        cur.execute("""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE sale_date >= CURDATE() - INTERVAL 7 DAY AND sale_status = 'Completed' AND product_type = 'Medical'
        """)
        weekly_medical = cur.fetchone()
        weekly_medical_sales = float(weekly_medical[0]) if weekly_medical[0] else 0

        cur.execute("""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE sale_date >= CURDATE() - INTERVAL 7 DAY AND sale_status = 'Completed' AND product_type = 'Non-Medical'
        """)
        weekly_nonmedical = cur.fetchone()
        weekly_nonmedical_sales = float(weekly_nonmedical[0]) if weekly_nonmedical[0] else 0

        weekly_sales = weekly_medical_sales + weekly_nonmedical_sales
        weekly_count = weekly_medical[1] if weekly_medical[1] else 0

        cur.execute("""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE MONTH(sale_date) = MONTH(CURDATE()) AND YEAR(sale_date) = YEAR(CURDATE()) AND sale_status = 'Completed' AND product_type = 'Medical'
        """)
        monthly_medical = cur.fetchone()
        monthly_medical_sales = float(monthly_medical[0]) if monthly_medical[0] else 0

        cur.execute("""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE MONTH(sale_date) = MONTH(CURDATE()) AND YEAR(sale_date) = YEAR(CURDATE()) AND sale_status = 'Completed' AND product_type = 'Non-Medical'
        """)
        monthly_nonmedical = cur.fetchone()
        monthly_nonmedical_sales = float(monthly_nonmedical[0]) if monthly_nonmedical[0] else 0

        monthly_sales = monthly_medical_sales + monthly_nonmedical_sales
        monthly_count = monthly_medical[1] if monthly_medical[1] else 0

        cur.execute("""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE YEAR(sale_date) = YEAR(CURDATE()) AND sale_status = 'Completed' AND product_type = 'Medical'
        """)
        yearly_medical = cur.fetchone()
        yearly_medical_sales = float(yearly_medical[0]) if yearly_medical[0] else 0

        cur.execute("""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales 
            WHERE YEAR(sale_date) = YEAR(CURDATE()) AND sale_status = 'Completed' AND product_type = 'Non-Medical'
        """)
        yearly_nonmedical = cur.fetchone()
        yearly_nonmedical_sales = float(yearly_nonmedical[0]) if yearly_nonmedical[0] else 0

        yearly_sales = yearly_medical_sales + yearly_nonmedical_sales
        yearly_count = yearly_medical[1] if yearly_medical[1] else 0

        cur.execute("""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales WHERE sale_status = 'Completed' AND product_type = 'Medical'
        """)
        overall_medical = cur.fetchone()
        overall_medical_sales = float(overall_medical[0]) if overall_medical[0] else 0

        cur.execute("""
            SELECT IFNULL(SUM(total_amount), 0), COUNT(*) 
            FROM sales WHERE sale_status = 'Completed' AND product_type = 'Non-Medical'
        """)
        overall_nonmedical = cur.fetchone()
        overall_nonmedical_sales = float(overall_nonmedical[0]) if overall_nonmedical[0] else 0

        overall_sales = overall_medical_sales + overall_nonmedical_sales
        overall_count = overall_medical[1] if overall_medical[1] else 0

    cur.execute("""
        SELECT p.product_name, SUM(si.quantity) as total_qty, SUM(si.quantity * si.price) as total_sales
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        GROUP BY p.id, p.product_name
        ORDER BY total_qty DESC
        LIMIT 10
    """)
    popular = cur.fetchall()

    if custom_range:
        cur.execute(f"""
            SELECT DATE(sale_date) as day, SUM(total_amount) as daily_total
            FROM sales
            WHERE {date_filter} AND sale_status = 'Completed' AND product_type = 'Medical'
            GROUP BY DATE(sale_date)
            ORDER BY day ASC
        """, tuple(date_params))
        chart_medical = cur.fetchall()
        medical_labels = [str(row[0]) for row in chart_medical]
        medical_values = [float(row[1]) for row in chart_medical]

        cur.execute(f"""
            SELECT DATE(sale_date) as day, SUM(total_amount) as daily_total
            FROM sales
            WHERE {date_filter} AND sale_status = 'Completed' AND product_type = 'Non-Medical'
            GROUP BY DATE(sale_date)
            ORDER BY day ASC
        """, tuple(date_params))
        chart_nonmedical = cur.fetchall()
        nonmedical_labels = [str(row[0]) for row in chart_nonmedical]
        nonmedical_values = [float(row[1]) for row in chart_nonmedical]
    else:
        cur.execute("""
            SELECT DATE(sale_date) as day, SUM(total_amount) as daily_total
            FROM sales
            WHERE sale_date >= CURDATE() - INTERVAL 30 DAY AND sale_status = 'Completed' AND product_type = 'Medical'
            GROUP BY DATE(sale_date)
            ORDER BY day ASC
        """)
        chart_medical = cur.fetchall()
        medical_labels = [str(row[0]) for row in chart_medical]
        medical_values = [float(row[1]) for row in chart_medical]

        cur.execute("""
            SELECT DATE(sale_date) as day, SUM(total_amount) as daily_total
            FROM sales
            WHERE sale_date >= CURDATE() - INTERVAL 30 DAY AND sale_status = 'Completed' AND product_type = 'Non-Medical'
            GROUP BY DATE(sale_date)
            ORDER BY day ASC
        """)
        chart_nonmedical = cur.fetchall()
        nonmedical_labels = [str(row[0]) for row in chart_nonmedical]
        nonmedical_values = [float(row[1]) for row in chart_nonmedical]

    chart_labels = medical_labels
    chart_values = medical_values

    if export == 'csv':
        if custom_range:
            cur.execute("""
                SELECT s.receipt_number, s.sale_date, s.total_amount, s.sale_status, s.product_type,
                       GROUP_CONCAT(DISTINCT p.product_name SEPARATOR ', ') as products
                FROM sales s
                JOIN sale_items si ON s.id = si.sale_id
                JOIN products p ON si.product_id = p.id
                WHERE s.sale_status = 'Completed'
                AND DATE(s.sale_date) >= %s AND DATE(s.sale_date) <= %s
                GROUP BY s.id
                ORDER BY s.sale_date DESC
            """, tuple(date_params))
        else:
            cur.execute("""
                SELECT s.receipt_number, s.sale_date, s.total_amount, s.sale_status, s.product_type,
                       GROUP_CONCAT(DISTINCT p.product_name SEPARATOR ', ') as products
                FROM sales s
                JOIN sale_items si ON s.id = si.sale_id
                JOIN products p ON si.product_id = p.id
                WHERE s.sale_status = 'Completed'
                GROUP BY s.id
                ORDER BY s.sale_date DESC
            """)
        export_data = cur.fetchall()
        cur.close()

        from io import StringIO, BytesIO
        text_output = StringIO()
        writer = csv.writer(text_output)
        writer.writerow(['Receipt #', 'Date', 'Total', 'Status', 'Type', 'Products'])
        for row in export_data:
            writer.writerow([
                row[0],
                row[1].strftime('%Y-%m-%d %H:%M') if row[1] else '',
                f"{row[2]:.2f}",
                row[3],
                row[4],
                row[5] or ''
            ])
        csv_bytes = text_output.getvalue().encode('utf-8-sig')
        output = BytesIO(csv_bytes)
        output.seek(0)
        return send_file(output, mimetype='text/csv; charset=utf-8', as_attachment=True, download_name=f"sales_report_{datetime.now().strftime('%Y%m%d')}.csv")

    cur.close()

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
                           active_main='sales', active_sub='sales_dashboard')

@app.route('/non_medical_sales')
@admin_required
def non_medical_sales():
    cur = mysql.connection.cursor()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    export = request.args.get('export', '').strip()

    where = ["s.sale_status = 'Completed'"]
    params = []
    if date_from:
        where.append("DATE(s.sale_date) >= %s")
        params.append(date_from)
    if date_to:
        where.append("DATE(s.sale_date) <= %s")
        params.append(date_to)
    where_clause = " AND ".join(where)

    cur.execute(f"""
        SELECT s.id, s.receipt_number, 
               GROUP_CONCAT(DISTINCT CASE WHEN p.product_type = 'Non-Medical' THEN p.product_name END SEPARATOR ', ') as products, 
               s.total_amount, s.sale_status, s.product_type, s.sale_date
        FROM sales s
        LEFT JOIN sale_items si ON s.id = si.sale_id
        LEFT JOIN products p ON si.product_id = p.id
        WHERE p.product_type = 'Non-Medical' AND {where_clause}
        GROUP BY s.id
        ORDER BY s.sale_date DESC
    """, tuple(params))
    sales = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]

    chart_labels = []
    chart_values = []
    if not export:
        cur.execute(f"""
            SELECT DATE(sale_date) as day, SUM(total_amount) as daily_total
            FROM sales s
            WHERE s.sale_status = 'Completed' 
            AND s.product_type = 'Non-Medical'
            AND s.sale_date >= CURDATE() - INTERVAL 30 DAY
            GROUP BY DATE(sale_date)
            ORDER BY day ASC
        """)
        chart_data = cur.fetchall()
        chart_labels = [str(row[0]) for row in chart_data]
        chart_values = [float(row[1]) for row in chart_data]

    if export == 'csv':
        cur.execute("""
            SELECT s.receipt_number, s.sale_date, s.total_amount, s.sale_status,
                   GROUP_CONCAT(DISTINCT p.product_name SEPARATOR ', ') as products
            FROM sales s
            JOIN sale_items si ON s.id = si.sale_id
            JOIN products p ON si.product_id = p.id
            WHERE s.sale_status = 'Completed' AND p.product_type = 'Non-Medical'
            GROUP BY s.id
            ORDER BY s.sale_date DESC
        """)
        export_data = cur.fetchall()
        cur.close()

        from io import StringIO, BytesIO
        text_output = StringIO()
        writer = csv.writer(text_output)
        writer.writerow(['Receipt #', 'Products', 'Total', 'Date', 'Status'])
        for s in export_data:
            writer.writerow([s[0], s[4] or '', f"{s[2]:.2f}", s[1].strftime('%Y-%m-%d %H:%M') if s[1] else '', s[3]])
        csv_bytes = text_output.getvalue().encode('utf-8-sig')
        output = BytesIO(csv_bytes)
        output.seek(0)
        return send_file(output, mimetype='text/csv; charset=utf-8', as_attachment=True, download_name=f"non_medical_sales_{datetime.now().strftime('%Y%m%d')}.csv")

    cur.close()

    return render_template('sales_non_medical.html', sales=sales,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           chart_labels=chart_labels, chart_values=chart_values,
                           date_from=date_from, date_to=date_to,
                           active_main='sales', active_sub='non_medical_sales')

# =============================
# INVENTORY
# =============================

@app.route('/out_of_stock')
@admin_required
def out_of_stock():
    category_filter = request.args.get('category', 'all')
    tab = request.args.get('tab', 'active')
    admin_id = session.get('admin_id')

    cur = mysql.connection.cursor()
    
    base_query = "SELECT * FROM products WHERE stock = 0"
    if category_filter == 'Medical':
        base_query += " AND product_type = 'Medical'"
    elif category_filter == 'Non-Medical':
        base_query += " AND product_type = 'Non-Medical'"
    base_query += " ORDER BY stock ASC"
    
    if tab == 'acknowledged':
        cur.execute(f"""
            SELECT p.* FROM products p
            JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'out_of_stock'
            WHERE al.acknowledged_by IS NOT NULL
            {f"AND p.product_type = '{category_filter}'" if category_filter in ['Medical', 'Non-Medical'] else ""}
            ORDER BY al.acknowledged_at DESC
        """)
    elif tab == 'dismissed':
        cur.execute(f"""
            SELECT p.* FROM products p
            JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'out_of_stock'
            WHERE al.dismissed_by IS NOT NULL
            {f"AND p.product_type = '{category_filter}'" if category_filter in ['Medical', 'Non-Medical'] else ""}
            ORDER BY al.dismissed_at DESC
        """)
    else:
        if admin_id:
            cur.execute(f"""
                SELECT p.* FROM products p
                WHERE p.stock = 0
                AND p.id NOT IN (
                    SELECT product_id FROM alert_visibility WHERE admin_id = {admin_id} AND alert_type = 'out_of_stock' AND is_hidden = 1
                )
                {f"AND p.product_type = '{category_filter}'" if category_filter in ['Medical', 'Non-Medical'] else ""}
                ORDER BY p.stock ASC
            """)
        else:
            cur.execute(base_query)
    products = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock = 0")
    out_of_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE stock > 0 AND stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date < CURDATE() AND expiration_date IS NOT NULL")
    expired_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date >= CURDATE() AND expiration_date <= CURDATE() + INTERVAL 7 DAY AND expiration_date IS NOT NULL")
    expiring_critical_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date > CURDATE() + INTERVAL 7 DAY AND expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_warning_count = cur.fetchone()[0]

    cur.close()
    return render_template('inventory_out_of_stock.html', products=products,
                           out_of_stock_count=out_of_stock_count,
                           low_stock_count=low_stock_count,
                           expired_count=expired_count,
                           expiring_critical_count=expiring_critical_count,
                           expiring_warning_count=expiring_warning_count,
                           active_main='alerts', active_sub='out_of_stock',
                           category_filter=category_filter, tab=tab)

@app.route('/low_stock')
@admin_required
def low_stock():
    category_filter = request.args.get('category', 'all')
    tab = request.args.get('tab', 'active')
    admin_id = session.get('admin_id')

    cur = mysql.connection.cursor()
    
    base_query = "SELECT * FROM products WHERE stock > 0 AND stock <= %s"
    params = (LOW_STOCK_THRESHOLD,)
    
    if tab == 'acknowledged':
        placeholders = ','.join(['%s'] * len(params))
        cur.execute(f"""
            SELECT p.* FROM products p
            JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'low_stock'
            WHERE al.acknowledged_by IS NOT NULL
            {f"AND p.product_type = '{category_filter}'" if category_filter in ['Medical', 'Non-Medical'] else ""}
            ORDER BY al.acknowledged_at DESC
        """)
    elif tab == 'dismissed':
        cur.execute(f"""
            SELECT p.* FROM products p
            JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'low_stock'
            WHERE al.dismissed_by IS NOT NULL
            {f"AND p.product_type = '{category_filter}'" if category_filter in ['Medical', 'Non-Medical'] else ""}
            ORDER BY al.dismissed_at DESC
        """)
    else:
        if admin_id:
            cur.execute(f"""
                SELECT p.* FROM products p
                WHERE p.stock > 0 AND p.stock <= %s
                AND p.id NOT IN (
                    SELECT product_id FROM alert_visibility WHERE admin_id = {admin_id} AND alert_type = 'low_stock' AND is_hidden = 1
                )
                {f"AND p.product_type = '{category_filter}'" if category_filter in ['Medical', 'Non-Medical'] else ""}
                ORDER BY p.stock ASC
            """, (LOW_STOCK_THRESHOLD,))
        else:
            if category_filter == 'Medical':
                cur.execute("SELECT * FROM products WHERE stock > 0 AND stock <= %s AND product_type = 'Medical' ORDER BY stock ASC", (LOW_STOCK_THRESHOLD,))
            elif category_filter == 'Non-Medical':
                cur.execute("SELECT * FROM products WHERE stock > 0 AND stock <= %s AND product_type = 'Non-Medical' ORDER BY stock ASC", (LOW_STOCK_THRESHOLD,))
            else:
                cur.execute("SELECT * FROM products WHERE stock > 0 AND stock <= %s ORDER BY stock ASC", (LOW_STOCK_THRESHOLD,))
    products = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock = 0")
    out_of_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE stock > 0 AND stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date < CURDATE() AND expiration_date IS NOT NULL")
    expired_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date >= CURDATE() AND expiration_date <= CURDATE() + INTERVAL 7 DAY AND expiration_date IS NOT NULL")
    expiring_critical_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date > CURDATE() + INTERVAL 7 DAY AND expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_warning_count = cur.fetchone()[0]

    cur.close()
    return render_template('inventory_low_stock.html', products=products,
                           out_of_stock_count=out_of_stock_count,
                           low_stock_count=low_stock_count,
                           expired_count=expired_count,
                           expiring_critical_count=expiring_critical_count,
                           expiring_warning_count=expiring_warning_count,
                           active_main='alerts', active_sub='low_stock',
                           category_filter=category_filter, tab=tab)

@app.route('/expired_products')
@admin_required
def expired_products():
    category_filter = request.args.get('category', 'all')
    tab = request.args.get('tab', 'active')
    admin_id = session.get('admin_id')

    cur = mysql.connection.cursor()
    
    if tab == 'acknowledged':
        cur.execute(f"""
            SELECT p.* FROM products p
            JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'expired'
            WHERE al.acknowledged_by IS NOT NULL
            {f"AND p.product_type = '{category_filter}'" if category_filter in ['Medical', 'Non-Medical'] else ""}
            ORDER BY al.acknowledged_at DESC
        """)
    elif tab == 'dismissed':
        cur.execute(f"""
            SELECT p.* FROM products p
            JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'expired'
            WHERE al.dismissed_by IS NOT NULL
            {f"AND p.product_type = '{category_filter}'" if category_filter in ['Medical', 'Non-Medical'] else ""}
            ORDER BY al.dismissed_at DESC
        """)
    else:
        if admin_id:
            cur.execute(f"""
                SELECT p.* FROM products p
                WHERE p.expiration_date < CURDATE() AND p.expiration_date IS NOT NULL
                AND p.id NOT IN (
                    SELECT product_id FROM alert_visibility WHERE admin_id = {admin_id} AND alert_type = 'expired' AND is_hidden = 1
                )
                {f"AND p.product_type = '{category_filter}'" if category_filter in ['Medical', 'Non-Medical'] else ""}
                ORDER BY p.expiration_date ASC
            """)
        else:
            if category_filter == 'Medical':
                cur.execute("SELECT * FROM products WHERE expiration_date < CURDATE() AND expiration_date IS NOT NULL AND product_type = 'Medical' ORDER BY expiration_date ASC")
            elif category_filter == 'Non-Medical':
                cur.execute("SELECT * FROM products WHERE expiration_date < CURDATE() AND expiration_date IS NOT NULL AND product_type = 'Non-Medical' ORDER BY expiration_date ASC")
            else:
                cur.execute("SELECT * FROM products WHERE expiration_date < CURDATE() AND expiration_date IS NOT NULL ORDER BY expiration_date ASC")
    products = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM products WHERE stock = 0")
    out_of_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE stock > 0 AND stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date < CURDATE() AND expiration_date IS NOT NULL")
    expired_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date >= CURDATE() AND expiration_date <= CURDATE() + INTERVAL 7 DAY AND expiration_date IS NOT NULL")
    expiring_critical_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date > CURDATE() + INTERVAL 7 DAY AND expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_warning_count = cur.fetchone()[0]

    cur.close()
    return render_template('inventory_expired.html', products=products,
                           out_of_stock_count=out_of_stock_count,
                           low_stock_count=low_stock_count,
                           expired_count=expired_count,
                           expiring_critical_count=expiring_critical_count,
                           expiring_warning_count=expiring_warning_count,
                           active_main='alerts', active_sub='expired_products',
                           category_filter=category_filter, tab=tab)

@app.route('/expiring_medical')
@admin_required
def expiring_medical():
    from datetime import date
    category_filter = request.args.get('category', 'all')
    level = request.args.get('level', 'all')
    tab = request.args.get('tab', 'active')
    admin_id = session.get('admin_id')
    
    cur = mysql.connection.cursor()
    
    base_level = level if level != 'all' else None
    
    if tab == 'acknowledged':
        cur.execute(f"""
            SELECT p.*, DATEDIFF(p.expiration_date, CURDATE()) as days_left FROM products p
            JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'expiring_medical'
            WHERE al.acknowledged_by IS NOT NULL
            {f"AND p.product_type = '{category_filter}'" if category_filter in ['Medical', 'Non-Medical'] else ""}
            ORDER BY al.acknowledged_at DESC
        """)
    elif tab == 'dismissed':
        cur.execute(f"""
            SELECT p.*, DATEDIFF(p.expiration_date, CURDATE()) as days_left FROM products p
            JOIN alert_logs al ON al.product_id = p.id AND al.alert_type = 'expiring_medical'
            WHERE al.dismissed_by IS NOT NULL
            {f"AND p.product_type = '{category_filter}'" if category_filter in ['Medical', 'Non-Medical'] else ""}
            ORDER BY al.dismissed_at DESC
        """)
    else:
        if level == 'expired':
            if category_filter == 'Medical':
                cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date < CURDATE() AND expiration_date IS NOT NULL AND product_type = 'Medical' ORDER BY expiration_date ASC")
            elif category_filter == 'Non-Medical':
                cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date < CURDATE() AND expiration_date IS NOT NULL AND product_type = 'Non-Medical' ORDER BY expiration_date ASC")
            else:
                cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date < CURDATE() AND expiration_date IS NOT NULL ORDER BY expiration_date ASC")
        elif level == 'critical':
            if category_filter == 'Medical':
                cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date >= CURDATE() AND expiration_date <= CURDATE() + INTERVAL 7 DAY AND expiration_date IS NOT NULL AND product_type = 'Medical' ORDER BY expiration_date ASC")
            elif category_filter == 'Non-Medical':
                cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date >= CURDATE() AND expiration_date <= CURDATE() + INTERVAL 7 DAY AND expiration_date IS NOT NULL AND product_type = 'Non-Medical' ORDER BY expiration_date ASC")
            else:
                cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date >= CURDATE() AND expiration_date <= CURDATE() + INTERVAL 7 DAY AND expiration_date IS NOT NULL ORDER BY expiration_date ASC")
        elif level == 'warning':
            if category_filter == 'Medical':
                cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date > CURDATE() + INTERVAL 7 DAY AND expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL AND product_type = 'Medical' ORDER BY expiration_date ASC")
            elif category_filter == 'Non-Medical':
                cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date > CURDATE() + INTERVAL 7 DAY AND expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL AND product_type = 'Non-Medical' ORDER BY expiration_date ASC")
            else:
                cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date > CURDATE() + INTERVAL 7 DAY AND expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL ORDER BY expiration_date ASC")
        else:
            if admin_id:
                cur.execute(f"""
                    SELECT p.*, DATEDIFF(p.expiration_date, CURDATE()) as days_left FROM products p
                    WHERE p.expiration_date <= CURDATE() + INTERVAL 30 DAY AND p.expiration_date IS NOT NULL
                    AND p.id NOT IN (
                        SELECT product_id FROM alert_visibility WHERE admin_id = {admin_id} AND alert_type = 'expiring_medical' AND is_hidden = 1
                    )
                    {f"AND p.product_type = '{category_filter}'" if category_filter in ['Medical', 'Non-Medical'] else ""}
                    ORDER BY p.expiration_date ASC
                """)
            else:
                if category_filter == 'all':
                    cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL ORDER BY expiration_date ASC")
                elif category_filter == 'Medical':
                    cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL AND product_type = 'Medical' ORDER BY expiration_date ASC")
                elif category_filter == 'Non-Medical':
                    cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL AND product_type = 'Non-Medical' ORDER BY expiration_date ASC")
                else:
                    cur.execute("SELECT *, DATEDIFF(expiration_date, CURDATE()) as days_left FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL ORDER BY expiration_date ASC")
    products = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock = 0")
    out_of_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock > 0 AND stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date < CURDATE() AND expiration_date IS NOT NULL")
    expired_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date >= CURDATE() AND expiration_date <= CURDATE() + INTERVAL 7 DAY AND expiration_date IS NOT NULL")
    expiring_critical_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date > CURDATE() + INTERVAL 7 DAY AND expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_warning_count = cur.fetchone()[0]
    
    cur.close()
    return render_template('inventory_expiring.html', products=products,
                           out_of_stock_count=out_of_stock_count,
                           low_stock_count=low_stock_count,
                           expired_count=expired_count,
                           expiring_critical_count=expiring_critical_count,
                           expiring_warning_count=expiring_warning_count,
                            active_main='alerts', active_sub='expiring_medical',
                            now=date.today, category_filter=category_filter, level=level, tab=tab)

@app.route('/alert_history')
@admin_required
def alert_history():
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT al.id, al.alert_type, al.alert_level, al.product_id, p.product_name, 
               al.message, al.acknowledged_by, al.acknowledged_at, 
               al.dismissed_by, al.dismissed_at, al.dismiss_reason, al.created_at
        FROM alert_logs al
        JOIN products p ON al.product_id = p.id
        ORDER BY al.created_at DESC
        LIMIT 100
    """)
    logs = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock = 0")
    out_of_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock > 0 AND stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date < CURDATE() AND expiration_date IS NOT NULL")
    expired_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date >= CURDATE() AND expiration_date <= CURDATE() + INTERVAL 7 DAY AND expiration_date IS NOT NULL")
    expiring_critical_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date > CURDATE() + INTERVAL 7 DAY AND expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_warning_count = cur.fetchone()[0]
    
    cur.close()
    return render_template('alert_history.html', logs=logs,
                           out_of_stock_count=out_of_stock_count,
                           low_stock_count=low_stock_count,
                           expired_count=expired_count,
                           expiring_critical_count=expiring_critical_count,
                           expiring_warning_count=expiring_warning_count,
                           active_main='alerts', active_sub='alert_history')

# =============================
# ADMIN MANAGEMENT
# =============================

@app.route('/register_cashier', methods=['GET','POST'])
@admin_required
def register_cashier():
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
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

        cur.execute("SELECT id FROM cashiers WHERE username=%s", (username,))
        if cur.fetchone():
            cur.close()
            flash("Username already exists", "error")
            return redirect(url_for('register_cashier'))

        hashed_password = generate_password_hash(password)
        hashed_answer = generate_password_hash(security_answer)

        cur.execute("""
            INSERT INTO cashiers (full_name, username, password, security_question, security_answer)
            VALUES (%s, %s, %s, %s, %s)
        """, (full_name, username, hashed_password, security_question, hashed_answer))

        mysql.connection.commit()
        
        # Log admin activity
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            cur.execute("""
                INSERT INTO admin_activity (admin_id, action, ip_address, details)
                VALUES (%s, %s, %s, %s)
            """, (session.get('admin_id'), 'Register Cashier', ip_address, f'Registered cashier: {username}'))
            mysql.connection.commit()
        except:
            pass
        
        cur.close()

        flash("Cashier registered successfully", "success")
        return redirect(url_for('register_cashier'))

    cur.close()
    return render_template('register_cashier.html',
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='management', 
                           active_sub='register_cashier')


@app.route('/delete_cashier', methods=['GET','POST'])
@admin_required
def delete_cashier():
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    
    if request.method == 'POST':
        cashier_id = request.form['id']
        
        # Get cashier info before deleting
        cur.execute("SELECT username FROM cashiers WHERE id=%s", (cashier_id,))
        cashier_info = cur.fetchone()
        cashier_username = cashier_info[0] if cashier_info else 'Unknown'
        
        cur.execute("DELETE FROM cashiers WHERE id=%s", (cashier_id,))
        mysql.connection.commit()
        
        # Log admin activity
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            cur.execute("""
                INSERT INTO admin_activity (admin_id, action, ip_address, details)
                VALUES (%s, %s, %s, %s)
            """, (session.get('admin_id'), 'Delete Cashier', ip_address, f'Deleted cashier: {cashier_username}'))
            mysql.connection.commit()
        except:
            pass
        
        flash("Cashier deleted successfully", "success")

    cur.execute("SELECT * FROM cashiers")
    cashiers = cur.fetchall()
    cur.close()
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

    cur = mysql.connection.cursor()

    cur.execute("SELECT id FROM cashiers WHERE username=%s AND id!=%s", (username, cashier_id))
    if cur.fetchone():
        cur.close()
        flash("Username already exists", "error")
        return redirect(url_for('delete_cashier'))

    try:
        if password != "":
            hashed_pw = generate_password_hash(password)
            cur.execute("""
                UPDATE cashiers 
                SET full_name=%s, username=%s, password=%s, status=%s
                WHERE id=%s
            """, (full_name, username, hashed_pw, status, cashier_id))
        else:
            cur.execute("""
                UPDATE cashiers 
                SET full_name=%s, username=%s, status=%s
                WHERE id=%s
            """, (full_name, username, status, cashier_id))

        mysql.connection.commit()
        
        # Log admin activity
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            cur.execute("""
                INSERT INTO admin_activity (admin_id, action, ip_address, details)
                VALUES (%s, %s, %s, %s)
            """, (session.get('admin_id'), 'Update Cashier', ip_address, f'Updated cashier: {username}'))
            mysql.connection.commit()
        except:
            pass
        
        flash("Cashier updated successfully!", "success")

    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error: {str(e)}", "error")

    finally:
        cur.close()

    return redirect(url_for('delete_cashier'))

@app.route('/admin/change_password', methods=['GET','POST'])
def admin_change_password():
    if 'admin_user' not in session and 'pending_admin_id' not in session:
        return redirect(url_for('admin_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    cur.close()
    admin_id = session.get('admin_id') or session.get('pending_admin_id')

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

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password FROM admins WHERE id=%s", (admin_id,))
        admin = cur.fetchone()

        if not admin or not check_password_hash(admin[1], old_password):
            flash("Current password is incorrect", "error")
            cur.close()
            return render_template('change_admin_password.html', low_stock_count=low_stock_count, expiring_count=expiring_count, active_main='management', active_sub='change_admin_password')

        hashed = generate_password_hash(new_password)
        cur.execute("UPDATE admins SET password=%s, force_password_change=0 WHERE id=%s", (hashed, admin_id))
        mysql.connection.commit()
        
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        try:
            cur.execute("""INSERT INTO admin_activity (admin_id, action, ip_address, details) VALUES (%s, %s, %s, %s)""", (admin_id, 'Change Password', ip_address, 'Admin changed password from dashboard'))
            mysql.connection.commit()
        except:
            pass
        
        cur.close()
        session.clear()
        flash("Password updated successfully. Please login again.", "success")
        return redirect(url_for('admin_login'))

    return render_template('change_admin_password.html', low_stock_count=low_stock_count, expiring_count=expiring_count, active_main='management', active_sub='change_admin_password')

@app.route('/cashier/change_password', methods=['GET', 'POST'])
def cashier_change_password():
    if 'cashier_user' not in session and 'pending_cashier_id' not in session:
        return redirect(url_for('cashier_login'))
    cashier_id = session.get('cashier_id') or session.get('pending_cashier_id')

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

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password FROM cashiers WHERE id=%s", (cashier_id,))
        cashier = cur.fetchone()

        if not cashier or not check_password_hash(cashier[1], old_password):
            flash("Current password is incorrect", "error")
            cur.close()
            return render_template('change_cashier_password.html')

        hashed = generate_password_hash(new_password)
        cur.execute("UPDATE cashiers SET password=%s, force_password_change=0 WHERE id=%s", (hashed, cashier_id))
        mysql.connection.commit()
        
        try:
            ip_address = request.remote_addr
            if request.headers.get('X-Forwarded-For'):
                ip_address = request.headers.get('X-Forwarded-For')
            cur.execute("""INSERT INTO cashier_activity (cashier_id, login_time, ip_address) VALUES (%s, NOW(), %s)""", (cashier_id, ip_address))
            mysql.connection.commit()
        except:
            pass
        
        cur.close()
        session.clear()
        flash("Password updated successfully. Please login again.", "success")
        return redirect(url_for('cashier_login'))

    return render_template('change_cashier_password.html')

@app.route('/change_admin_password', methods=['GET','POST'])
def change_admin_password():
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    cur.close()
    
    security_question = None

    if request.method == 'POST':
        step = request.form.get('step', '1')
        username = request.form.get('username', '').strip()

        if not username:
            flash("Username is required", "error")
            return redirect(url_for('change_admin_password'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, security_question, security_answer FROM admins WHERE username=%s", (username,))
        admin = cur.fetchone()

        if not admin:
            flash("Invalid username", "error")
            cur.close()
            return redirect(url_for('change_admin_password'))

        if step == '1':
            security_question = admin[1] if len(admin) > 1 and admin[1] else None
            if not security_question:
                hashed_answer = generate_password_hash('generoso')
                cur.execute("UPDATE admins SET security_question=%s, security_answer=%s WHERE id=%s", ('What is the name of the owner?', hashed_answer, admin[0]))
                mysql.connection.commit()
                security_question = 'What is the name of the owner?'
        elif step == '2':
            security_answer = request.form.get('security_answer', '').strip()
            new_pass = request.form.get('new_password', '').strip()

            if not security_answer or not new_pass:
                flash("All fields are required", "error")
                cur.close()
                return redirect(url_for('change_admin_password'))

            stored_answer = admin[2] if len(admin) > 2 else None
            if stored_answer and check_password_hash(stored_answer, security_answer):
                hashed = generate_password_hash(new_pass)
                cur.execute("UPDATE admins SET password=%s, force_password_change=0 WHERE username=%s", (hashed, username))
                mysql.connection.commit()
                
                ip_address = request.remote_addr
                if request.headers.get('X-Forwarded-For'):
                    ip_address = request.headers.get('X-Forwarded-For')
                
                try:
                    cur.execute("""
                        INSERT INTO admin_activity (admin_id, action, ip_address, details)
                        VALUES (%s, %s, %s, %s)
                    """, (admin[0], 'Change Password', ip_address, 'Admin changed password via forgot password'))
                    mysql.connection.commit()
                except:
                    pass
                
                flash("Password updated successfully", "success")
            else:
                flash("Security answer is incorrect", "error")
        cur.close()

    return render_template('forgot_admin_password.html',
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           security_question=security_question)

@app.route('/change_cashier_password', methods=['GET', 'POST'])
def change_cashier_password():
    cur = mysql.connection.cursor()
    try:
        security_question = None

        if request.method == 'POST':
            step = request.form.get('step', '1')
            username = request.form.get('username', '').strip()

            if not username:
                flash("Username is required", "error")
                return redirect(url_for('change_cashier_password'))

            cur.execute("SELECT id, password, security_question, security_answer FROM cashiers WHERE username=%s", (username,))
            row = cur.fetchone()

            if not row:
                flash("Invalid username", "error")
                return redirect(url_for('change_cashier_password'))

            if step == '1':
                security_question = row[2] if row[2] else None
                if not security_question:
                    hashed_answer = generate_password_hash('generoso')
                    cur.execute("UPDATE cashiers SET security_question=%s, security_answer=%s WHERE id=%s", ('What is the name of the owner?', hashed_answer, row[0]))
                    mysql.connection.commit()
                    security_question = 'What is the name of the owner?'
            elif step == '2':
                security_answer = request.form.get('security_answer', '').strip()
                new_password = request.form.get('new_password', '').strip()

                if not security_answer or not new_password:
                    flash("All fields are required", "error")
                    return redirect(url_for('change_cashier_password'))

                if check_password_hash(row[3], security_answer):
                    hashed = generate_password_hash(new_password)
                    cur.execute("UPDATE cashiers SET password=%s, force_password_change=0 WHERE id=%s", (hashed, row[0]))
                    mysql.connection.commit()
                    flash("Password updated successfully", "success")
                else:
                    flash("Security answer is incorrect", "error")
    finally:
        cur.close()

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
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')

        if check_login_lockout(ip_address, username):
            flash("Account temporarily locked due to too many failed attempts. Please try again later.", "error")
            return redirect(url_for('cashier_login'))

        if username == "" or password == "":
            flash("All fields are required", "error")
            return redirect(url_for('cashier_login'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, full_name, username, password, status FROM cashiers WHERE username=%s", (username,))
        cashier = cur.fetchone()
        cur.close()

        if not cashier or not check_password_hash(cashier[3], password):
            record_login_attempt(ip_address, username, False)
            flash("Invalid login credentials", "error")
            return redirect(url_for('cashier_login'))

        cashier_status = ((cashier[4] or 'active')).lower()
        if cashier_status != 'active':
            record_login_attempt(ip_address, username, False)
            flash("Cashier account is inactive. Contact the administrator.", "error")
            return redirect(url_for('cashier_login'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT security_question, security_answer FROM cashiers WHERE id=%s", (cashier[0],))
        sq = cur.fetchone()
        if not sq or not sq[0] or not sq[1]:
            hashed_answer = generate_password_hash('generoso')
            cur.execute("UPDATE cashiers SET security_question=%s, security_answer=%s WHERE id=%s", ('What is the name of the owner?', hashed_answer, cashier[0]))
            mysql.connection.commit()
        cur.close()

        force_change = False
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT force_password_change FROM cashiers WHERE id=%s", (cashier[0],))
            fc_row = cur.fetchone()
            cur.close()
            if fc_row and fc_row[0]:
                force_change = True
        except Exception:
            pass
        
        if force_change:
            session['pending_cashier_id'] = cashier[0]
            session['pending_cashier_user'] = cashier[1]
            flash("You must change your password before continuing.", "error")
            return redirect(url_for('cashier_change_password'))

        session['cashier_user'] = cashier[1]
        session['cashier_id'] = cashier[0]
        session['role'] = 'cashier'
        session.permanent = True  # Session persists on refresh

        cur = mysql.connection.cursor()

        # Get IP address
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')

        # Log cashier login with IP address
        cur.execute("""
            INSERT INTO cashier_activity (cashier_id, login_time, ip_address)
            VALUES (%s, NOW(), %s)
        """, (cashier[0], ip_address))
        mysql.connection.commit()
        cur.close()
        record_login_attempt(ip_address, username, True)

        return redirect(url_for('cashier_dashboard'))

    return render_template('cashier_login.html')


@app.route('/active_cashiers')
@admin_required
def get_active_cashiers():
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT id, full_name, username FROM cashiers")
    cashiers = cur.fetchall()
    
    cur.execute("""
        SELECT c.username, ca.login_time
        FROM cashiers c
        JOIN cashier_activity ca ON c.id = ca.cashier_id
        WHERE ca.logout_time IS NULL
    """)
    active_data = {row[0]: row[1] for row in cur.fetchall()}
    cur.close()

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
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT IFNULL(SUM(total_amount), 0) as total, COUNT(*) as count
        FROM sales 
        WHERE cashier_id = %s AND DATE(sale_date) = CURDATE() AND sale_status = 'Completed'
    """, (session['cashier_id'],))
    today_data = cur.fetchone()
    today_total = today_data[0] if today_data else 0
    today_count = today_data[1] if today_data else 0

    cur.execute("""
        SELECT sale_date, receipt_number, total_amount, sale_status 
        FROM sales 
        WHERE cashier_id = %s
        ORDER BY sale_date DESC 
        LIMIT 5
    """, (session['cashier_id'],))

    recent_sales = cur.fetchall()

    settings = get_store_settings(mysql)

    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    cur.close()

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
    cur = mysql.connection.cursor()
    cashier_id = session.get('cashier_id')
    receipt_search = request.args.get('receipt_number', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    where = ["cashier_id = %s", "sale_status = 'Completed'"]
    params = [cashier_id]
    if receipt_search:
        where.append("receipt_number LIKE %s")
        params.append(f"%{receipt_search}%")
    if date_from:
        where.append("DATE(sale_date) >= %s")
        params.append(date_from)
    if date_to:
        where.append("DATE(sale_date) <= %s")
        params.append(date_to)
    where_clause = " AND ".join(where)
    cur.execute(f"""
        SELECT DATE(sale_date) as sale_day,
               IFNULL(SUM(total_amount),0) as total_sales,
               COUNT(id) as total_transactions
        FROM sales
        WHERE {where_clause}
        GROUP BY DATE(sale_date)
        ORDER BY sale_day ASC
    """, tuple(params))
    daily_data = cur.fetchall()
    labels = [str(row[0]) for row in daily_data]
    sales_values = [float(row[1]) for row in daily_data]
    transaction_counts = [int(row[2]) for row in daily_data]
    cur.execute(f"""
        SELECT id, receipt_number, total_amount, sale_date
        FROM sales
        WHERE {where_clause}
        ORDER BY sale_date DESC
    """, tuple(params))
    sales = cur.fetchall()
    sales_data = []
    for sale in sales:
        sale_id = sale[0]
        cur.execute("""
            SELECT si.quantity, si.price, p.product_name
            FROM sale_items si
            LEFT JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = %s
        """, (sale_id,))
        items = cur.fetchall()
        sales_data.append({
            "id": sale[0],
            "receipt_number": sale[1],
            "total_amount": float(sale[2]),
            "sale_date": sale[3],
            "items": items
        })
    cur.close()
    return render_template(
        "cashier_history.html",
        sales=sales_data,
        chart_labels=labels,
        chart_sales=sales_values,
        chart_transactions=transaction_counts,
        receipt_search=receipt_search,
        date_from=date_from,
        date_to=date_to
    )

@app.route('/search_product')
@cashier_required
def search_product():
    query = request.args.get('q')
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id, product_name, price, stock, barcode, expiration_date
        FROM products
        WHERE (product_name LIKE %s OR barcode LIKE %s)
        AND stock > 0
        ORDER BY product_name, expiration_date
        LIMIT 10
    """, (f"%{query}%", f"%{query}%"))

    products = cur.fetchall()
    cur.close()

    result = []
    for p in products:
        expiry = p[5].strftime('%m/%d/%Y') if p[5] else 'N/A'
        is_expired = p[5] is not None and p[5] < datetime.now().date()
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
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, product_name, price, stock, barcode, expiration_date FROM products WHERE stock > 0 ORDER BY product_name, expiration_date")
    products = cur.fetchall()
    cur.close()
    
    result = []
    for p in products:
        expiry = p[5].strftime('%m/%d/%Y') if p[5] else 'N/A'
        is_expired = p[5] is not None and p[5] < datetime.now().date()
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
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, product_name, barcode, price, category_id, expiration_date 
        FROM products 
        WHERE product_name LIKE %s 
        ORDER BY product_name, expiration_date
        LIMIT 5
    """, (f"%{query}%",))
    products = cur.fetchall()
    cur.close()
    
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
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, product_name, barcode, category_id, product_type, price, stock, expiration_date FROM products WHERE id = %s", (product_id,))
    row = cur.fetchone()
    cur.close()
    
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
    stock = data.get('stock')
    expiration_date = data.get('expiration_date')
    
    if not product_name or not barcode or not category:
        return jsonify({'success': False, 'message': 'All fields are required'})
    
    try:
        price = float(price) if price else 0
        stock = int(stock) if stock else 0
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid price or stock value'})
    
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT id FROM categories WHERE category_name=%s", (category,))
    cat_result = cur.fetchone()
    category_id = cat_result[0] if cat_result else None
    
    cur.execute("""
        UPDATE products 
        SET product_name=%s, barcode=%s, category_id=%s, product_type=%s, price=%s, stock=%s, expiration_date=%s
        WHERE id=%s
    """, (product_name, barcode, category_id, category, price, stock, expiration_date, product_id))
    
    mysql.connection.commit()
    
    ip_address = request.remote_addr
    if request.headers.get('X-Forwarded-For'):
        ip_address = request.headers.get('X-Forwarded-For')
    
    try:
        cur.execute("""
            INSERT INTO admin_activity (admin_id, action, ip_address, details)
            VALUES (%s, %s, %s, %s)
        """, (session.get('admin_id'), 'Edit Product', ip_address, f'Edited product: {product_name}'))
        mysql.connection.commit()
    except:
        pass
    
    cur.close()
    return jsonify({'success': True, 'message': 'Product updated successfully!'})

@app.route('/get_product/<barcode>')
@cashier_required
def get_product(barcode):
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id, product_name, price, stock, barcode, expiration_date
        FROM products
        WHERE barcode = %s AND stock > 0
        LIMIT 1
    """, (barcode,))

    row = cur.fetchone()
    cur.close()

    if row:
        expiry = row[5].strftime('%m/%d/%Y') if row[5] else 'N/A'
        is_expired = row[5] is not None and row[5] < datetime.now().date()
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
    placeholders = ','.join(['%s'] * len(product_ids))

    cur = mysql.connection.cursor()
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
            expiry_date = row[5]

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

        receipt_number = f"REC-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        sale_product_type = 'Medical' if medical_items else 'Non-Medical'

        cur.execute("""
            INSERT INTO sales (receipt_number, cashier_id, total_amount, sale_status, product_type, sale_date)
            VALUES (%s, %s, %s, 'Pending', %s, NOW())
        """, (receipt_number, session['cashier_id'], total_amount, sale_product_type))

        sale_id = cur.lastrowid

        for product_id, requested_quantity in quantity_by_product.items():
            row = products[product_id]
            price = float(row[3])
            cur.execute("""
                INSERT INTO sale_items (sale_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (sale_id, product_id, requested_quantity, price))

            cur.execute("""
                UPDATE products SET stock = stock - %s WHERE id = %s
            """, (requested_quantity, product_id))

            cur.execute("""
                INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                VALUES (%s, 'OUT', %s, 'Sale')
            """, (product_id, requested_quantity))

        mysql.connection.commit()
        change = round(tendered - total_amount, 2)

        return jsonify({
            'success': True,
            'receipt_number': receipt_number,
            'total': round(total_amount, 2),
            'tendered': round(tendered, 2),
            'change': change,
            'items': receipt_items,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    except Exception as e:
        try:
            mysql.connection.rollback()
        except:
            pass
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})
    finally:
        cur.close()

# =============================
# TRANSACTION HOLD / RESUME
# =============================

@app.route('/api/hold_transaction', methods=['POST'])
@cashier_required
def hold_transaction():
    data = request.get_json() or {}
    name = data.get('name', f'Hold {datetime.now().strftime("%H:%M")}')
    cart = data.get('cart', [])
    if not cart:
        return jsonify({'success': False, 'message': 'Cart is empty'}), 400
    if 'held_transactions' not in session:
        session['held_transactions'] = []
    session['held_transactions'].append({
        'name': name,
        'cart': cart,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
    })
    session.modified = True
    return jsonify({'success': True, 'message': f'Transaction held: {name}'})

@app.route('/api/resume_transaction', methods=['POST'])
@cashier_required
def resume_transaction():
    data = request.get_json() or {}
    index = data.get('index')
    held = session.get('held_transactions', [])
    if index is None or int(index) < 0 or int(index) >= len(held):
        return jsonify({'success': False, 'message': 'Invalid hold index'}), 400
    transaction = held.pop(int(index))
    session.modified = True
    return jsonify({'success': True, 'cart': transaction['cart']})

@app.route('/api/held_transactions', methods=['GET'])
@cashier_required
def get_held_transactions():
    held = session.get('held_transactions', [])
    return jsonify({'success': True, 'holds': held})

# =============================
# VOID TRANSACTION (Admin Override Required)
# =============================

@app.route('/api/void_sale', methods=['POST'])
def void_sale():
    if 'admin_user' not in session:
        return jsonify({'success': False, 'message': 'Admin override required. Please login as admin first.'}), 403
    data = request.get_json() or {}
    sale_id = data.get('sale_id')
    reason = clean_input(data.get('reason', ''))
    if not sale_id:
        return jsonify({'success': False, 'message': 'Sale ID is required'}), 400
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id, receipt_number, sale_status, total_amount, cashier_id FROM sales WHERE id=%s", (sale_id,))
        sale = cur.fetchone()
        if not sale:
            return jsonify({'success': False, 'message': 'Sale not found'}), 404
        if sale[2] == 'Voided':
            return jsonify({'success': False, 'message': 'Sale is already voided'}), 400
        if sale[2] == 'Refunded':
            return jsonify({'success': False, 'message': 'Sale is already refunded'}), 400
        cur.execute("SELECT product_id, quantity FROM sale_items WHERE sale_id=%s", (sale_id,))
        items = cur.fetchall()
        for product_id, quantity in items:
            cur.execute("UPDATE products SET stock = stock + %s WHERE id = %s", (quantity, product_id))
            cur.execute("INSERT INTO stock_movements (product_id, movement_type, quantity, reason) VALUES (%s, 'IN', %s, %s)", (product_id, quantity, f'Void - {reason or "No reason"}'))
        voided_by = session.get('admin_id') or session.get('cashier_id')
        cur.execute("UPDATE sales SET sale_status='Voided', voided_at=NOW(), voided_by=%s, void_reason=%s WHERE id=%s", (voided_by, reason, sale_id))
        mysql.connection.commit()
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        try:
            if 'admin_id' in session:
                cur.execute("INSERT INTO admin_activity (admin_id, action, ip_address, details) VALUES (%s, %s, %s, %s)", (session['admin_id'], 'Void Sale', ip_address, f'Voided sale {sale[1]} (ID: {sale_id})'))
            else:
                cur.execute("INSERT INTO cashier_activity (cashier_id, login_time, ip_address) VALUES (%s, NOW(), %s)", (session['cashier_id'], ip_address))
            mysql.connection.commit()
        except Exception:
            pass
        return jsonify({'success': True, 'message': f'Sale {sale[1]} has been voided. Stock restored.'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cur.close()

# =============================
# REFUND / RETURN PROCESSING
# =============================

@app.route('/api/refund_sale', methods=['POST'])
def refund_sale():
    if 'admin_user' not in session and 'cashier_user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.get_json() or {}
    sale_id = data.get('sale_id')
    reason = clean_input(data.get('reason', ''))
    if not sale_id:
        return jsonify({'success': False, 'message': 'Sale ID is required'}), 400
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id, receipt_number, sale_status, total_amount, cashier_id FROM sales WHERE id=%s", (sale_id,))
        sale = cur.fetchone()
        if not sale:
            return jsonify({'success': False, 'message': 'Sale not found'}), 404
        if sale[2] == 'Voided':
            return jsonify({'success': False, 'message': 'Sale is already voided'}), 400
        if sale[2] == 'Refunded':
            return jsonify({'success': False, 'message': 'Sale is already refunded'}), 400
        cur.execute("SELECT product_id, quantity FROM sale_items WHERE sale_id=%s", (sale_id,))
        items = cur.fetchall()
        for product_id, quantity in items:
            cur.execute("UPDATE products SET stock = stock + %s WHERE id = %s", (quantity, product_id))
            cur.execute("INSERT INTO stock_movements (product_id, movement_type, quantity, reason) VALUES (%s, 'IN', %s, %s)", (product_id, quantity, f'Refund - {reason or "No reason"}'))
        refunded_by = session.get('admin_id') or session.get('cashier_id')
        cur.execute("UPDATE sales SET sale_status='Refunded', refunded_at=NOW(), refunded_by=%s, refund_reason=%s WHERE id=%s", (refunded_by, reason, sale_id))
        mysql.connection.commit()
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        try:
            if 'admin_id' in session:
                cur.execute("INSERT INTO admin_activity (admin_id, action, ip_address, details) VALUES (%s, %s, %s, %s)", (session['admin_id'], 'Refund Sale', ip_address, f'Refunded sale {sale[1]} (ID: {sale_id})'))
            else:
                cur.execute("INSERT INTO cashier_activity (cashier_id, login_time, ip_address) VALUES (%s, NOW(), %s)", (session['cashier_id'], ip_address))
            mysql.connection.commit()
        except Exception:
            pass
        return jsonify({'success': True, 'message': f'Sale {sale[1]} has been refunded. Stock restored.'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cur.close()

# =============================
# REPRINT RECEIPT
# =============================

@app.route('/reprint_receipt/<int:sale_id>')
@cashier_required
def reprint_receipt(sale_id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT receipt_number, total_amount, sale_date, sale_status FROM sales WHERE id=%s AND cashier_id=%s", (sale_id, session.get('cashier_id')))
        sale = cur.fetchone()
        if not sale:
            cur.close()
            return jsonify({'success': False, 'message': 'Sale not found'}), 404
        cur.execute("SELECT si.quantity, si.price, p.product_name FROM sale_items si JOIN products p ON si.product_id = p.id WHERE si.sale_id=%s", (sale_id,))
        items = cur.fetchall()
        receipt_items = []
        for qty, price, name in items:
            receipt_items.append({'name': name, 'quantity': qty, 'price': float(price), 'subtotal': round(float(price) * int(qty), 2)})
        data = {
            'receipt_number': sale[0],
            'total': float(sale[1]),
            'tendered': float(sale[1]),
            'change': 0,
            'items': receipt_items,
            'date': sale[2].strftime('%Y-%m-%d %H:%M:%S') if sale[2] else ''
        }
        return render_template('reprint_receipt.html', data=data)
    finally:
        cur.close()

@app.route('/api/receipt_data/<int:sale_id>')
@cashier_required
def receipt_data(sale_id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT receipt_number, total_amount, sale_date FROM sales WHERE id=%s AND cashier_id=%s", (sale_id, session.get('cashier_id')))
        sale = cur.fetchone()
        if not sale:
            return jsonify({'success': False, 'message': 'Sale not found'}), 404
        cur.execute("SELECT si.quantity, si.price, p.product_name FROM sale_items si JOIN products p ON si.product_id = p.id WHERE si.sale_id=%s", (sale_id,))
        items = cur.fetchall()
        receipt_items = []
        for qty, price, name in items:
            receipt_items.append({'name': name, 'quantity': qty, 'price': float(price), 'subtotal': round(float(price) * int(qty), 2)})
        return jsonify({'success': True, 'data': {'receipt_number': sale[0], 'total': float(sale[1]), 'tendered': float(sale[1]), 'change': 0, 'items': receipt_items, 'date': sale[2].strftime('%Y-%m-%d %H:%M:%S') if sale[2] else ''}})
    finally:
        cur.close()

# =============================
# CASHIER METRICS
# =============================

@app.route('/cashier_metrics')
@cashier_required
def cashier_metrics():
    cur = mysql.connection.cursor()
    cashier_id = session.get('cashier_id')
    cur.execute("SELECT IFNULL(SUM(total_amount),0), COUNT(*) FROM sales WHERE cashier_id=%s AND sale_status='Completed'", (cashier_id,))
    my_total, my_count = cur.fetchone()
    my_avg = round(float(my_total) / my_count, 2) if my_count > 0 else 0
    cur.execute("""
        SELECT c.full_name, c.username, IFNULL(SUM(s.total_amount),0) as total, COUNT(s.id) as txn_count
        FROM sales s
        JOIN cashiers c ON s.cashier_id = c.id
        WHERE s.sale_status = 'Completed'
        GROUP BY s.cashier_id
        ORDER BY total DESC
    """)
    rankings = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    cur.close()
    return render_template('cashier_metrics.html',
                           my_total=my_total, my_count=my_count, my_avg=my_avg,
                           rankings=rankings,
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='performance', active_sub='cashier_metrics')

# =============================
# LOGOUT
# =============================

# Route to setup remote database access (run once)
@app.route('/setup_remote_db')
def setup_remote_db():
    """Grant remote access to root user - run this once from Computer 1"""
    try:
        cur = mysql.connection.cursor()
        # Create user for remote access with all privileges
        try:
            cur.execute("CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY ''")
        except Exception:
            mysql.connection.rollback()
        cur.execute("GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION")
        cur.execute("FLUSH PRIVILEGES")
        cur.close()
        return "Database remote access granted! You can now connect from other computers."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin_logout')
def admin_logout():
    """Admin logout - only clears admin session, does not affect cashier"""
    # Log admin activity
    if 'admin_user' in session:
        cur = mysql.connection.cursor()
        # Get IP address
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        cur.execute("""
            INSERT INTO admin_activity (admin_id, action, ip_address, details)
            VALUES (%s, %s, %s, %s)
        """, (session.get('admin_id'), 'Admin Logout', ip_address, 'Admin logged out'))
        mysql.connection.commit()
        cur.close()
    
    # Only clear admin session keys, keep cashier session intact
    session.pop('admin_user', None)
    session.pop('admin_id', None)
    session.pop('role', None)
    session.pop('pending_admin_id', None)
    session.pop('pending_admin_user', None)
    
    return redirect(url_for('admin_login'))

@app.route('/cashier_logout')
def cashier_logout():
    """Cashier logout - clears cashier session and logs activity"""
    if 'cashier_user' in session:
        cur = mysql.connection.cursor()
        cashier_id = session.get('cashier_id') or session.get('pending_cashier_id')
        
        # Get IP address
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        
        # Log the logout time in cashier_activity
        cur.execute("""
            UPDATE cashier_activity
            SET logout_time = NOW(),
                ip_address = COALESCE(ip_address, %s)
            WHERE cashier_id = %s AND logout_time IS NULL
        """, (ip_address, cashier_id))
        mysql.connection.commit()
        cur.close()
    
    # Only clear cashier session keys, keep admin session intact
    session.pop('cashier_user', None)
    session.pop('cashier_id', None)
    session.pop('role', None)
    session.pop('pending_cashier_id', None)
    session.pop('pending_cashier_user', None)
    
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
        mysql.connection.rollback()
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
        cur = mysql.connection.cursor()
        try:
            enriched_items = []
            for item in items:
                cur.execute(
                    "SELECT product_name, product_type, price FROM products WHERE id=%s",
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
            cur.close()
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
        success, user = auth_service.login(username, password, request, mysql, 'admin')
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
        success, user = auth_service.login(username, password, request, mysql, 'cashier')
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

def get_store_settings(mysql):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT setting_key, setting_value FROM store_settings")
        rows = cur.fetchall()
        settings = {row[0]: row[1] for row in rows}
        return settings
    finally:
        cur.close()

def get_setting(mysql, key, default=''):
    settings = get_store_settings(mysql)
    return settings.get(key, default)

# =============================
# RECEIPT CUSTOMIZATION
# =============================

@app.route('/receipt_customization', methods=['GET', 'POST'])
@admin_required
def receipt_customization():
    cur = mysql.connection.cursor()
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
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value)
                """, (key, value))

            mysql.connection.commit()
            flash("Receipt settings saved successfully!", "success")

        cur.execute("SELECT setting_key, setting_value FROM store_settings")
        rows = cur.fetchall()
        settings = {row[0]: row[1] for row in rows}
    finally:
        cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    cur.close()

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

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE sales 
            SET receipt_printed = 1, printed_at = NOW(), sale_status = 'Completed'
            WHERE receipt_number = %s AND cashier_id = %s AND sale_status = 'Pending'
        """, (receipt_number, session['cashier_id']))
        mysql.connection.commit()
        cur.close()

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

        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                SELECT id FROM sales 
                WHERE receipt_number = %s AND cashier_id = %s AND sale_status = 'Pending'
                LIMIT 1
            """, (receipt_number, session['cashier_id']))
            sale_row = cur.fetchone()
            if not sale_row:
                return jsonify({'success': True, 'message': 'No pending sale found'})

            sale_id = sale_row[0]

            cur.execute("""
                SELECT product_id, quantity FROM sale_items WHERE sale_id = %s
            """, (sale_id,))
            items = cur.fetchall()

            for product_id, quantity in items:
                cur.execute("""
                    UPDATE products SET stock = stock + %s WHERE id = %s
                """, (quantity, product_id))

                cur.execute("""
                    DELETE FROM stock_movements 
                    WHERE product_id = %s AND movement_type = 'OUT' 
                    AND reason = 'Sale' AND movement_date >= (
                        SELECT sale_date FROM sales WHERE id = %s
                    )
                    LIMIT 1
                """, (product_id, sale_id))

            cur.execute("DELETE FROM sale_items WHERE sale_id = %s", (sale_id,))
            cur.execute("DELETE FROM sales WHERE id = %s", (sale_id,))
            mysql.connection.commit()
            return jsonify({'success': True, 'message': 'Pending sale cancelled'})
        finally:
            cur.close()
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# =============================
# BACKUP & RESTORE
# =============================

@app.route('/backup_restore')
@admin_required
def backup_restore():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
    low_stock_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
    expiring_count = cur.fetchone()[0]
    cur.close()

    return render_template('backup_restore.html',
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count,
                           active_main='management',
                           active_sub='backup_restore')

@app.route('/backup_database', methods=['POST'])
@admin_required
def backup_database():
    try:
        db_name = app.config['MYSQL_DB']
        db_user = app.config['MYSQL_USER']
        db_pass = app.config['MYSQL_PASSWORD']
        db_host = app.config['MYSQL_HOST']

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"pharmacon_backup_{timestamp}.sql"

        mysqldump_path = r"C:\xampp\mysql\bin\mysqldump.exe"
        if not os.path.exists(mysqldump_path):
            mysqldump_path = "mysqldump"

        cmd = [
            mysqldump_path,
            f"--host={db_host}",
            f"--user={db_user}",
            db_name
        ]
        if db_pass:
            cmd.append(f"--password={db_pass}")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            flash(f"Backup failed: {result.stderr}", "error")
            return redirect(url_for('backup_restore'))

        sql_dump = result.stdout
        if sql_dump is None:
            sql_dump = ""
        mem = BytesIO()
        mem.write(sql_dump.encode('utf-8'))
        mem.seek(0)

        try:
            return send_file(
                mem,
                as_attachment=True,
                download_name=filename,
                mimetype='application/sql'
            )
        except TypeError:
            return send_file(
                mem,
                as_attachment=True,
                attachment_filename=filename,
                mimetype='application/sql'
            )
    except Exception as e:
        flash(f"Backup error: {str(e)}", "error")
        return redirect(url_for('backup_restore'))

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

        db_name = app.config['MYSQL_DB']
        db_user = app.config['MYSQL_USER']
        db_pass = app.config['MYSQL_PASSWORD']
        db_host = app.config['MYSQL_HOST']

        mysql_path = r"C:\xampp\mysql\bin\mysql.exe"
        if not os.path.exists(mysql_path):
            mysql_path = "mysql"

        sql_content = file.read().decode('utf-8')

        cmd = [
            mysql_path,
            f"--host={db_host}",
            f"--user={db_user}",
            db_name
        ]
        if db_pass:
            cmd.append(f"--password={db_pass}")

        result = subprocess.run(cmd, input=sql_content, capture_output=True, text=True)

        if result.returncode != 0:
            flash(f"Restore failed: {result.stderr}", "error")
        else:
            flash("Database restored successfully!", "success")

    except Exception as e:
        flash(f"Restore error: {str(e)}", "error")

    return redirect(url_for('backup_restore'))

if __name__ == '__main__':
    with app.app_context():
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS store_settings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    setting_key VARCHAR(100) NOT NULL UNIQUE,
                    setting_value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                INSERT INTO store_settings (setting_key, setting_value) VALUES
                ('receipt_header', 'PHARMACON'),
                ('receipt_subtitle', 'A\\'s PharmaHealth & Convenience'),
                ('receipt_footer', 'Thank you for your purchase!\\nPlease come again.'),
                ('store_name', 'PharmaCon'),
                ('store_address', ''),
                ('store_contact', '')
                ON DUPLICATE KEY UPDATE setting_value = setting_value
            """)
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'sales' AND column_name = 'receipt_printed'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE sales ADD COLUMN receipt_printed TINYINT(1) DEFAULT 0")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'sales' AND column_name = 'printed_at'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE sales ADD COLUMN printed_at TIMESTAMP NULL DEFAULT NULL")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'admins' AND column_name = 'security_question'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE admins ADD COLUMN security_question VARCHAR(255)")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'admins' AND column_name = 'security_answer'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE admins ADD COLUMN security_answer VARCHAR(255)")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'cashiers' AND column_name = 'security_question'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE cashiers ADD COLUMN security_question VARCHAR(255)")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'cashiers' AND column_name = 'security_answer'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE cashiers ADD COLUMN security_answer VARCHAR(255)")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'admins' AND column_name = 'force_password_change'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE admins ADD COLUMN force_password_change TINYINT(1) DEFAULT 0")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'cashiers' AND column_name = 'force_password_change'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE cashiers ADD COLUMN force_password_change TINYINT(1) DEFAULT 0")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'sales' AND column_name = 'voided_at'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE sales ADD COLUMN voided_at TIMESTAMP NULL DEFAULT NULL")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'sales' AND column_name = 'voided_by'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE sales ADD COLUMN voided_by INT NULL DEFAULT NULL")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'sales' AND column_name = 'void_reason'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE sales ADD COLUMN void_reason TEXT NULL DEFAULT NULL")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'sales' AND column_name = 'refunded_at'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE sales ADD COLUMN refunded_at TIMESTAMP NULL DEFAULT NULL")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'sales' AND column_name = 'refunded_by'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE sales ADD COLUMN refunded_by INT NULL DEFAULT NULL")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'sales' AND column_name = 'refund_reason'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE sales ADD COLUMN refund_reason TEXT NULL DEFAULT NULL")
            cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'sales' AND column_name = 'original_sale_id'")
            if cur.fetchone()[0] == 0:
                cur.execute("ALTER TABLE sales ADD COLUMN original_sale_id INT NULL DEFAULT NULL")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS login_attempts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ip_address VARCHAR(45) DEFAULT NULL,
                    username_attempted VARCHAR(100) DEFAULT NULL,
                    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    locked_until TIMESTAMP NULL DEFAULT NULL,
                    INDEX idx_ip_attempted (ip_address, attempted_at),
                    INDEX idx_username_attempted (username_attempted, attempted_at)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS alert_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    alert_type VARCHAR(50) NOT NULL,
                    alert_level VARCHAR(20) NOT NULL,
                    product_id INT NOT NULL,
                    message TEXT NOT NULL,
                    acknowledged_by INT DEFAULT NULL,
                    acknowledged_at TIMESTAMP NULL DEFAULT NULL,
                    dismissed_by INT DEFAULT NULL,
                    dismissed_at TIMESTAMP NULL DEFAULT NULL,
                    dismiss_reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_alert (alert_type, product_id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS alert_settings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    setting_name VARCHAR(100) NOT NULL UNIQUE,
                    setting_value VARCHAR(255) NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            cur.execute("SELECT COUNT(*) FROM alert_settings")
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO alert_settings (setting_name, setting_value) VALUES ('low_stock_threshold', '10'), ('critical_stock_threshold', '5'), ('expiry_critical_days', '7'), ('expiry_warning_days', '30')")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS alert_acknowledgments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    alert_type VARCHAR(50) NOT NULL,
                    action VARCHAR(20) NOT NULL,
                    reason TEXT,
                    user_id INT NOT NULL,
                    user_type VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_ack (alert_type, product_id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS alert_visibility (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    alert_type VARCHAR(50) NOT NULL,
                    admin_id INT NOT NULL,
                    is_hidden TINYINT(1) DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE
                )
            """)
            try:
                cur.execute("ALTER TABLE alert_logs ADD UNIQUE KEY unique_alert (alert_type, product_id)")
            except Exception:
                pass
            try:
                cur.execute("ALTER TABLE alert_acknowledgments ADD UNIQUE KEY unique_ack (alert_type, product_id)")
            except Exception:
                pass
            try:
                cur.execute("ALTER TABLE alert_visibility ADD UNIQUE KEY unique_visibility (product_id, alert_type, admin_id)")
            except Exception:
                pass
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            print(f"Store settings init error: {e}")

@app.route('/help_tour')
def help_tour_guide():
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM products WHERE stock <= %s", (LOW_STOCK_THRESHOLD,))
        low_stock_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM products WHERE expiration_date <= CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL")
        expiring_count = cur.fetchone()[0]
    except Exception:
        low_stock_count = 0
        expiring_count = 0
    finally:
        cur.close()
    return render_template('help_tour.html',
                           low_stock_count=low_stock_count,
                           expiring_count=expiring_count)

app.run(debug=True)
