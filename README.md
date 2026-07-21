# PharmaCon - Pharmacy Management System

PharmaCon is an integrated web-based pharmacy management and point-of-sale system designed to streamline day-to-day operations of a retail pharmacy. It provides two distinct user roles — Admin and Cashier — each with role-specific access and responsibilities.

---

## Key Features

### Admin Module

1. **Dashboard**
   - Real-time notification bell with live low-stock and expiry alerts
   - Cashier status monitor showing currently logged-in staff with login times
   - Recent activity logs and sales summaries at a glance

2. **Product / Catalog Management**
   - Add, edit, and delete pharmaceutical products
   - Organize products by Medical and Non-Medical categories
   - Track product barcodes, prices, expiry dates, and stock levels
   - Automatic stock consolidation when the same product is added again
   - Prevent duplicate barcode entries at insert time

3. **Sales Reporting & Analytics**
   - Medical Sales and Non-Medical Sales views with completed-transaction filtering
   - Sales Dashboard showing daily, weekly, monthly, yearly, and overall sales
   - Best-seller / top-product rankings
   - Daily sales trend charts tracked over the past 30 days

4. **Inventory Alerts**
   - Low Stock Alerts (items on or below the 10-unit threshold)
   - Expiry Date Monitoring (items expiring within 30 days)
   - Out-of-Stock product listing

5. **Staff / Cashier Management**
   - Register new cashier accounts
   - Edit cashier name, username, password, and account status (Active / Inactive)
   - Delete cashier accounts
   - View full cashier activity / login logs with IP address tracking
   - Real-time online/offline status per cashier

6. **Admin Security**
   - Change admin password with old-password verification
   - Track admin activity / API audit trail with IP addresses
   - Role-based session isolation

7. **Receipt Customization**
   - Customize receipt header, subtitle, footer message
   - Add store address and contact information
   - Changes apply instantly to printed thermal receipts

8. **Database Backup / Restore**
   - Create full SQL backups of the pharmacon database
   - Restore from previous backup files
   - Timestamped backup downloads

### Cashier Module

1. **POS / Transaction Processing**
   - Scan and add products via barcode search
   - Search products by name when barcode is unavailable
   - Live product catalog auto-refresh every 5 seconds
   - Full cart workflow with quantity controls and stock validation
   - Payment modal with amount tendered and change calculation
   - 58mm thermal receipt printing support

2. **Receipt Flow**
   - Sales are saved as **Pending** after payment confirmation
   - **Print** button opens browser print dialog
   - **Close** button cancels the pending sale and restores stock
   - **Mark as Printed** confirms the transaction and marks it as Completed
   - Receipt customization (header, subtitle, footer, address, contact) from admin settings

3. **Sales History & Performance**
   - View completed transactions with item-level details
   - Today's sales chart and transaction count on dashboard
   - 30-day daily sales and transaction count chart on history page

4. **Daily Operations**
   - Login / logout tracking with automatic shift logging
   - Stock movement logs (IN / OUT) for audit purposes
   - Session persists for 24 hours with HTTPOnly cookies

---

## OOP Architecture

The system is built using Object-Oriented Programming principles:

- **Encapsulation**: Product and StockMovement classes use private fields with validated property setters (e.g., stock cannot go negative).
- **Inheritance**: User is the base class; Admin and Cashier extend User with role-specific behavior.
- **Polymorphism**: Admin and Cashier have distinct authenticate() implementations. StockInProcessor and StockOutProcessor process stock differently.
- **Abstraction**: IAuthService, ISalesService, IRepository, and IEntity define contracts for authentication, sales, data access, and entities.
- **Factory Pattern**: get_movement_processor() returns the correct processor based on movement type (IN or OUT).

Key classes:
- `Product`: Represents a pharmaceutical product with validation rules.
- `StockMovement`: Tracks IN/OUT movements with reason and quantity.
- `User / Admin / Cashier`: User hierarchy with authentication and logging.
- `AuthService`: Handles polymorphic login/logout for Admin and Cashier.
- `ProductRepository`: Abstracts all product database operations.
- `SalesService`: Processes sales with automatic Medical/Non-Medical splitting.

---

## Database Schema Overview

Key Tables:
- `admins`: Admin login credentials
- `cashiers`: Cashier login credentials with status
- `products`: Product details (name, barcode, category, price, stock, expiry)
- `categories`: Category name lookup (Medical / Non-Medical)
- `sales`: Sale / transaction headers (includes `receipt_printed`, `printed_at`, `sale_status`)
- `sale_items`: Individual line items per sale
- `stock_movements`: Stock IN / OUT history log
- `cashier_activity`: Cashier login/logout tracking with IP and timestamps
- `admin_activity`: Admin action audit log with IP and timestamps
- `store_settings`: Receipt customization and store information

---

## Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |

> Admin account is created automatically on first run if no admin exists.

Cashier accounts are registered by the admin via the Staff Management page.

---

## Technology Stack

- **Backend**: Python 3.x + Flask
- **Database**: MySQL / MariaDB (data persistence)
- **Frontend**: HTML5 + CSS3 + JavaScript (Jinja2 templates)
- **Libraries**: SweetAlert2, Chart.js
- **Authentication**: Session-based with HTTPOnly cookies

---

## Installation & Setup

1. Ensure XAMPP / WAMP is installed and MySQL is running
2. Create the database `pharmacon` in phpMyAdmin or via MySQL CLI
3. Execute the SQL schema (`database.sql`) to set up all tables
4. Install Python dependencies:
   ```bash
   pip install flask flask-mysqldb mysql-connector-python
   ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Open a browser and navigate to: `http://localhost:5000/admin_login`
7. Login with the default admin credentials

---

## Directory Structure

```
pharmacon - Finalv4/
├── app.py                        # Main application entry point
├── models.py                      # OOP models (Product, User, StockMovement, etc.)
├── services.py                    # OOP services (AuthService, SalesService, ProductRepository)
├── README.md                      # This file
├── READ_ME.txt                    # Project documentation
├── SUGGESTIONS.txt                # Feature improvement ideas
├── MOBILE_SYSTEM_PROMPT.txt       # Mobile/Android version development guide
├── database.sql                   # Database schema and seed data
├── templates/                     # HTML templates
│   ├── admin_dashboard.html
│   ├── admin_login.html
│   ├── add_product.html
│   ├── all_products.html
│   ├── edit_product.html
│   ├── confirm_delete_product.html
│   ├── cashier_dashboard.html
│   ├── cashier_login.html
│   ├── cashier_history.html
│   ├── register_cashier.html
│   ├── delete_cashier.html
│   ├── change_admin_password.html
│   ├── admin_cashier_logs.html
│   ├── admin_activity_logs.html
│   ├── sales_dashboard.html
│   ├── sales_medical.html
│   ├── sales_non_medical.html
│   ├── inventory_out_of_stock.html
│   ├── inventory_expiring.html
│   ├── receipt_customization.html
│   └── backup_restore.html
```

---

## Notes

- **Pending Sales**: Transactions are saved as `Pending` after payment. They only become `Completed` when the cashier clicks **Mark as Printed**. Closing the receipt modal without marking cancels the sale and restores stock.
- **Receipt Printing**: Supports 58mm thermal receipts. The print dialog opens separately from the receipt modal, allowing the cashier to print and then confirm.
- **Session Management**: `SESSION_PERMANENT` is enabled; sessions survive browser refreshes for 24 hours by default.
- **Stock Thresholds**: Low stock threshold is 10 units. Expiring products are flagged within 30 days.
- **Logging**: All admin actions are logged to `admin_activity`. All cashier actions are logged to `cashier_activity`. IP addresses are captured.
- **Receipt Customization**: Admin can customize receipt header, subtitle, footer, store address, and contact via Management > Receipt Customization.
- **Backup**: Admin can create full SQL backups or restore from backup via Management > Database Backup / Restore.

---

## Related Documentation

- `README_ME.txt` — Detailed system features and OOP documentation
- `SUGGESTIONS.txt` — Feature improvement suggestions for POS and Inventory
- `MOBILE_SYSTEM_PROMPT.txt` — Guide to build a mobile/Android version of the system
