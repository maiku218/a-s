Pharmancon is an integrated web-based pharmacy management and point-of-sale
system designed to streamline day-to-day operations of a retail pharmacy.
It provides two distinct user roles — Admin and Cashier — each with
role-specific access and responsibilities.

========================================
         KEY FEATURES
========================================

--- ADMIN MODULE ---
1. Dashboard
   - View real-time stock alerts and pharmacy activity monitor
   - See currently logged-in cashiers, activity logs, and sales summaries

2. Product / Catalog Management
   - Add, edit, and delete pharmaceutical products
   - Organize products by Medical and Non-Medical categories
   - Track product barcodes, prices, expiry dates, and stock levels
   - Automatic stock consolidation when the same product is added again
   - Prevent duplicate barcode entries at insert time

3. Sales Reporting & Analytics
   - Medical Sales and Non-Medical Sales views with completed-transaction filtering
   - Sales Dashboard showing daily, weekly, monthly, yearly, and overall sales
   - Best-seller / top-product rankings
   - Daily sales trend charts tracked over the past 30 days

4. Inventory Alerts
   - Low Stock Alerts (items on or below the 10-unit threshold)
   - Expiry Date Monitoring (items expiring within 30 days)
   - Out-of-Stock product listing

5. Staff / Cashier Management
   - Register new cashier accounts
   - Edit cashier name, username, password, and account status
   - Delete cashier accounts
   - View full cashier activity / login logs

6. Admin Security
   - Change admin password
   - Track admin activity / API audit trail

--- CASHIER MODULE ---
1. POS / Transaction Processing
   - Scan and add products via barcode search
   - Search products by name when barcode is unavailable
   - Full cart or direct-checkout workflow (no cart intermediary)
   - Discounts at item level (percentage or fixed amount)
   - VAT exclusive and VAT inclusive receipt modes
   - Tender validation: amount tendered must be at least the grand total
   - Cash drawer amount change for correct/incorrect tender descrepancies

2. SLA / Point-of-Sale Tender System
   - Cash tendering: only cash payments supported (no credit/debit/e-wallet)
   - Grand total is auto-calculated and displayed to the cashier
   - Payment succeeds only with sufficient customer funds (amount tendered ≥ grand total)
   - Per-transaction cash drawer tally is adjusted by the difference paid versus grand total

3. Sales History
   - View completed, cancelled (walk-out), and refunded transactions
   - Sort and filter by date; export history to CSV

4. Daily Operations
   - Start Shift / End Shift log-in tracking
   - Stock movement logs for audit purposes

========================================
         DATABASE SCHEMA OVERVIEW
========================================

Key Tables:
  - admins              : Admin login credentials
  - cashiers            : Cashier login credentials
  - products            : Product details (name, barcode, category, price, stock, expiry)
  - categories          : Category name lookup (Medical / Non-Medical)
  - sales               : Sale / transaction headers
  - sale_items          : Individual line items per sale
  - stock_movements     : Stock IN / OUT history log
  - cashier_activity    : Cashier login/logout tracking
  - admin_activity      : Admin action audit log

========================================
         DEFAULT CREDENTIALS
========================================

Admin  : username = admin  /  password = admin123
         (Created automatically on first run if no admin exists)

Cashier: Registered by the admin via the Staff Management page

========================================
         TECHNOLOGY STACK
========================================

  - Python 3.x + Flask (backend)
  - MySQL / MariaDB (data persistence)
  - HTML5 + CSS3 + JavaScript (frontend / templates)
  - SweetAlert2 (notification dialogs)
  - Session-based authentication

========================================
         INSTALLATION & SETUP
========================================

1. Ensure XAMPP / WAMP is installed and MySQL is running
2. Create the database  "pharmacon"  in phpMyAdmin or via MySQL CLI
3. Execute the SQL schema (CREATE TABLE statements) to set up all tables
4. Install Python dependencies: flask, flask_mysqldb, mysql-connector-python
5. Run the application: python app.py
6. Open a browser and navigate to: http://localhost:5000/admin_login
7. Login with the default admin credentials (see above)

========================================
         DIRECTORY STRUCTURE
========================================

  pharmacon - Finalv4/
  |-- app.py                        # Main application entry point
  |-- READ_ME.txt                   # This file
  |-- templates/                    # HTML templates
  |     |-- admin_dashboard.html
  |     |-- admin_login.html
  |     |-- add_product.html
  |     |-- all_products.html
  |     |-- edit_product.html
  |     |-- confirm_delete_product.html
  |     |-- cashier_dashboard.html
  |     |-- cashier_login.html
  |     |-- cashier_history.html
  |     |-- register_cashier.html
  |     |-- delete_cashier.html
  |     |-- change_admin_password.html
  |     |-- admin_cashier_logs.html
  |     |-- admin_activity_logs.html
  |     |-- sales_dashboard.html
  |     |-- sales_medical.html
  |     |-- sales_non_medical.html
  |     |-- inventory_out_of_stock.html
  |     |-- inventory_expiring.html

========================================
         NOTES
========================================

  - SESSION_PERMANENT is enabled; sessions survive browser refreshes for
    24 hours by default.
  - Low stock threshold is hardcoded at 10 units.
  - Expiring products are flagged when their expiry date is within 30 days.
  - All admin actions are logged to the admin_activity table.
  - All cashier actions are logged to the cashier_activity table.
  - Passwords are hashed using werkzeug.security before storage.
  - Cashier module supports only CASH tendering in this version.

========================================
         END OF README
========================================
