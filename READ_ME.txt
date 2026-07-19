========================================
          PHARMACON SYSTEM README
========================================

PROJECT NAME  : PharmaCon
LANGUAGE      : Python (Flask Framework)
DATABASE      : MySQL
PURPOSE       : Pharmacy Management System with Point-of-Sale (POS) capabilities

========================================
          SYSTEM PURPOSE
========================================

PharmaCon is an integrated web-based pharmacy management and point-of-sale
system designed to streamline day-to-day operations of a retail pharmacy.
It provides two distinct user roles — Admin and Cashier — each with
role-specific access and responsibilities.

========================================
          KEY FEATURES
========================================

--- ADMIN MODULE ---
1. Dashboard
   - Real-time notification bell with live low-stock and expiry alerts
   - Cashier status monitor showing currently logged-in staff with login times
   - Recent activity logs and sales summaries at a glance

2. Product / Catalog Management
   - Add, edit, and delete pharmaceutical products
   - Organize products by Medical and Non-Medical categories
   - Track product barcodes, prices, expiry dates, and stock levels
   - Automatic stock consolidation when the same product (name + barcode + expiry) is added again
   - Prevent duplicate barcode entries at insert time
   - AJAX-supported product registration with instant validation feedback
   - API-driven product updates without page reload

3. Sales Reporting & Analytics
   - Medical Sales and Non-Medical Sales views with completed-transaction filtering
   - Sales Dashboard showing daily, weekly, monthly, yearly, and overall sales
   - Separate Medical vs Non-Medical breakdown for every time period
   - Best-seller / top-product rankings by quantity sold
   - Daily sales trend charts tracked over the past 30 days (Chart.js)
   - Separate receipt numbers generated for Medical and Non-Medical items per transaction

4. Inventory Alerts
   - Low Stock Alerts (items on or below the 10-unit threshold)
   - Expiry Date Monitoring (items expiring within 30 days, filterable by category)
   - Out-of-Stock product listing

5. Staff / Cashier Management
   - Register new cashier accounts
   - Edit cashier name, username, password, and account status (Active / Inactive)
   - Delete cashier accounts
   - View full cashier activity / login logs with IP address tracking
   - Real-time online/offline status per cashier

6. Admin Security
   - Change admin password with old-password verification
   - Track admin activity / API audit trail with IP addresses
   - Role-based session isolation (admin sessions do not interfere with cashier sessions)

--- CASHIER MODULE ---
1. POS / Transaction Processing
   - Scan and add products via barcode search
   - Search products by name when barcode is unavailable
   - Live product catalog auto-refresh every 5 seconds
   - Full cart workflow with quantity controls and stock validation
   - Separate Medical and Non-Medical receipt generation per transaction
   - 58mm thermal receipt printing support
   - Receipt modal with itemized breakdown and totals

2. Sales History & Performance
   - View completed transactions with item-level details
   - 30-day daily sales and transaction count chart
   - Today's sales summary and transaction count on dashboard

3. Daily Operations
   - Login / logout tracking with automatic shift logging
   - Stock movement logs (IN / OUT) for audit purposes
   - Session persists for 24 hours with HTTPOnly cookies

========================================
          OOP ARCHITECTURE
========================================

The system is built using Object-Oriented Programming principles:

  - Encapsulation  : Product and StockMovement classes use private fields with
                     validated property setters (e.g., stock cannot go negative).
  - Inheritance    : User is the base class; Admin and Cashier extend User with
                     role-specific behavior.
  - Polymorphism   : Admin and Cashier have distinct authenticate() implementations.
                     StockInProcessor and StockOutProcessor process stock differently.
  - Abstraction    : IAuthService, ISalesService, IRepository, and IEntity define
                     contracts for authentication, sales, data access, and entities.
  - Factory Pattern: get_movement_processor() returns the correct processor based
                     on movement type (IN or OUT).

Key classes:
  - Product            : Represents a pharmaceutical product with validation rules.
  - StockMovement      : Tracks IN/OUT movements with reason and quantity.
  - User / Admin / Cashier : User hierarchy with authentication and logging.
  - AuthService        : Handles polymorphic login/logout for Admin and Cashier.
  - ProductRepository  : Abstracts all product database operations.
  - SalesService       : Processes sales with automatic Medical/Non-Medical splitting.

========================================
          DATABASE SCHEMA OVERVIEW
========================================

Key Tables:
  - admins              : Admin login credentials
  - cashiers            : Cashier login credentials with status
  - products            : Product details (name, barcode, category, price, stock, expiry)
  - categories          : Category name lookup (Medical / Non-Medical)
  - sales               : Sale / transaction headers
  - sale_items          : Individual line items per sale
  - stock_movements     : Stock IN / OUT history log
  - cashier_activity    : Cashier login/logout tracking with IP and timestamps
  - admin_activity      : Admin action audit log with IP and timestamps

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
  - Chart.js (sales analytics charts)
  - Session-based authentication with HTTPOnly cookies

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
  |-- models.py                      # OOP models (Product, User, StockMovement, etc.)
  |-- services.py                    # OOP services (AuthService, SalesService, ProductRepository)
  |-- READ_ME.txt                    # This file
  |-- templates/                     # HTML templates
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
  - Cashier module supports CASH tendering with separate Medical/Non-Medical receipts.
  - Products with zero stock are retained in the database for historical sales records.
  - IP addresses are captured for admin and cashier login/logout actions.
  - OOP routes are available at /add_product_oop, /complete_sale_oop,
    /admin/login, and /cashier/login for demonstration purposes.

========================================
          END OF README
========================================
