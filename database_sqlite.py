import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pharmacon.db')


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _table_exists(cursor, name):
    cursor.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,))
    return cursor.fetchone() is not None


def _columns(cursor, table):
    return [r[1] for r in cursor.execute("PRAGMA table_info(%s)" % table)]


def run_migrations():
    """Schema upgrades that ALTER existing tables.

    Kept separate from init_db() because init_db() only issues
    CREATE TABLE IF NOT EXISTS, which never changes an existing table.
    """
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = OFF")

    # --- stock_movements: snapshot the product name and stop cascading deletes ---
    # Bug CRITICAL-4: the column used to be
    #   FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    # so deleting a product wiped its entire stock trail, including the
    # 'Product Deleted' row that delete_product() had just inserted.
    # The table is rebuilt with ON DELETE SET NULL plus a product_name
    # snapshot, so history survives the product.
    if _table_exists(cur, 'stock_movements'):
        cols = _columns(cur, 'stock_movements')
        fk_sql = cur.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='stock_movements'"
        ).fetchone()[0] or ''
        needs_rebuild = ('ON DELETE CASCADE' in fk_sql) or ('product_name' not in cols)

        if 'product_name' not in cols:
            cur.execute("ALTER TABLE stock_movements ADD COLUMN product_name TEXT")

        if 'ON DELETE CASCADE' in fk_sql:
            cur.executescript("""
                CREATE TABLE stock_movements_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    movement_type VARCHAR(10) NOT NULL,
                    quantity INTEGER NOT NULL,
                    reason VARCHAR(100),
                    movement_date TEXT DEFAULT (datetime('now', 'localtime')),
                    product_name TEXT,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
                );
                INSERT INTO stock_movements_new
                    (id, product_id, movement_type, quantity, reason,
                     movement_date, product_name)
                SELECT sm.id, sm.product_id, sm.movement_type, sm.quantity,
                       sm.reason, sm.movement_date, p.product_name
                FROM stock_movements sm
                LEFT JOIN products p ON p.id = sm.product_id;
                DROP TABLE stock_movements;
                ALTER TABLE stock_movements_new RENAME TO stock_movements;
            """)

        # Backfill any movement whose name was never snapshotted.
        if 'product_name' in _columns(cur, 'stock_movements'):
            cur.execute("""
                UPDATE stock_movements
                   SET product_name = (SELECT p.product_name FROM products p
                                        WHERE p.id = stock_movements.product_id)
                 WHERE (product_name IS NULL OR product_name = '')
                   AND product_id IS NOT NULL
            """)

        cur.executescript("""
            CREATE INDEX IF NOT EXISTS idx_stock_movements_date
                ON stock_movements(movement_date);
            CREATE INDEX IF NOT EXISTS idx_stock_movements_reason
                ON stock_movements(reason);
            CREATE INDEX IF NOT EXISTS idx_admin_activity_time
                ON admin_activity(activity_time);
            CREATE INDEX IF NOT EXISTS idx_admin_activity_action
                ON admin_activity(action);
            CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date);
            CREATE INDEX IF NOT EXISTS idx_sales_status ON sales(sale_status);
        """)

    # --- products: remember the name of anything that gets deleted ---
    if _table_exists(cur, 'products') and 'deleted_at' not in _columns(cur, 'products'):
        cur.execute("ALTER TABLE products ADD COLUMN deleted_at TEXT")

    # Tombstone of removed products, so receipts and history can still name them.
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS products_deleted (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            product_name TEXT,
            barcode TEXT,
            stock INTEGER,
            deleted_at TEXT DEFAULT (datetime('now', 'localtime')),
            deleted_by INTEGER
        );
    """)

    # Security audit for both roles. admin_activity.admin_id is NOT NULL and
    # references admins, so cashier-side security events have nowhere to go
    # today (bug HIGH-4).
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type VARCHAR(20) NOT NULL,
            user_id INTEGER,
            username VARCHAR(100),
            event VARCHAR(50) NOT NULL,
            ip_address VARCHAR(45),
            details TEXT,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        );
    """)

    # Legacy rows from the old checkout flow, which only marked a sale
    # Completed once the receipt had printed. If printing failed, the stock was
    # already deducted and the 'Sale' movement already written, yet the sale
    # stayed Pending and was excluded from every report. Sales are now
    # Completed at commit, so complete the ones we can prove really happened:
    # they have line items AND a matching 'Sale' stock movement.
    #
    # A Pending row with no items proves nothing (it is an orphaned header) and
    # is deliberately left alone for a human to decide.
    if _table_exists(cur, 'sales') and _table_exists(cur, 'sale_items'):
        cur.execute("""
            UPDATE sales
               SET sale_status = 'Completed'
             WHERE sale_status = 'Pending'
               AND EXISTS (SELECT 1 FROM sale_items si WHERE si.sale_id = sales.id)
               AND EXISTS (
                    SELECT 1
                      FROM sale_items si
                      JOIN stock_movements sm
                        ON sm.product_id = si.product_id
                       AND sm.movement_type = 'OUT'
                       AND sm.reason = 'Sale'
                       AND sm.quantity = si.quantity
                     WHERE si.sale_id = sales.id
               )
        """)

    conn.commit()
    cur.execute("PRAGMA foreign_keys = ON")
    conn.close()


def init_db():
    run_migrations()
    conn = get_db()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            security_question VARCHAR(255),
            security_answer VARCHAR(255),
            force_password_change INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS cashiers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name VARCHAR(100),
            username VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            status VARCHAR(20) DEFAULT 'active',
            security_question VARCHAR(255),
            security_answer VARCHAR(255),
            force_password_change INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS cashier_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cashier_id INTEGER NOT NULL,
            login_time TEXT NOT NULL,
            logout_time TEXT DEFAULT NULL,
            ip_address VARCHAR(45) DEFAULT NULL,
            FOREIGN KEY (cashier_id) REFERENCES cashiers(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS admin_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL,
            action VARCHAR(100) NOT NULL,
            ip_address VARCHAR(45) DEFAULT NULL,
            details TEXT,
            activity_time TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address VARCHAR(45) DEFAULT NULL,
            username_attempted VARCHAR(100) DEFAULT NULL,
            attempted_at TEXT DEFAULT (datetime('now', 'localtime')),
            locked_until TEXT NULL DEFAULT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_ip_attempted ON login_attempts(ip_address, attempted_at);
        CREATE INDEX IF NOT EXISTS idx_username_attempted ON login_attempts(username_attempted, attempted_at);

        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type VARCHAR(20) NOT NULL,
            user_id INTEGER,
            username VARCHAR(100),
            event VARCHAR(50) NOT NULL,
            ip_address VARCHAR(45),
            details TEXT,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(100) NOT NULL,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name VARCHAR(200) NOT NULL,
            barcode VARCHAR(100) DEFAULT NULL,
            category_id INTEGER,
            product_type VARCHAR(50) DEFAULT 'medical',
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            expiration_date TEXT DEFAULT NULL,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );

        CREATE TABLE IF NOT EXISTS stock_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            movement_type VARCHAR(10) NOT NULL,
            quantity INTEGER NOT NULL,
            reason VARCHAR(100),
            movement_date TEXT DEFAULT (datetime('now', 'localtime')),
            product_name TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_number VARCHAR(50) UNIQUE NOT NULL,
            cashier_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            sale_status VARCHAR(20) DEFAULT 'Completed',
            product_type VARCHAR(20) DEFAULT 'medical',
            sale_date TEXT DEFAULT (datetime('now', 'localtime')),
            receipt_printed INTEGER DEFAULT 0,
            printed_at TEXT NULL DEFAULT NULL,
            voided_at TEXT NULL DEFAULT NULL,
            voided_by INTEGER NULL DEFAULT NULL,
            void_reason TEXT NULL DEFAULT NULL,
            refunded_at TEXT NULL DEFAULT NULL,
            refunded_by INTEGER NULL DEFAULT NULL,
            refund_reason TEXT NULL DEFAULT NULL,
            original_sale_id INTEGER NULL DEFAULT NULL,
            FOREIGN KEY (cashier_id) REFERENCES cashiers(id)
        );

        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        CREATE TABLE IF NOT EXISTS store_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key VARCHAR(100) NOT NULL UNIQUE,
            setting_value TEXT,
            updated_at TEXT DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS alert_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type VARCHAR(50) NOT NULL,
            alert_level VARCHAR(20) NOT NULL,
            product_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            acknowledged_by INTEGER DEFAULT NULL,
            acknowledged_at TEXT NULL DEFAULT NULL,
            dismissed_by INTEGER DEFAULT NULL,
            dismissed_at TEXT NULL DEFAULT NULL,
            dismiss_reason TEXT,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            UNIQUE(alert_type, product_id)
        );

        CREATE TABLE IF NOT EXISTS alert_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_name VARCHAR(100) NOT NULL UNIQUE,
            setting_value VARCHAR(255) NOT NULL,
            updated_at TEXT DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS alert_acknowledgments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            alert_type VARCHAR(50) NOT NULL,
            action VARCHAR(20) NOT NULL,
            reason TEXT,
            user_id INTEGER NOT NULL,
            user_type VARCHAR(20) NOT NULL,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            UNIQUE(alert_type, product_id)
        );

        CREATE TABLE IF NOT EXISTS alert_visibility (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            alert_type VARCHAR(50) NOT NULL,
            admin_id INTEGER NOT NULL,
            is_hidden INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            updated_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE,
            UNIQUE(product_id, alert_type, admin_id)
        );

        CREATE TABLE IF NOT EXISTS held_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cashier_id INTEGER NOT NULL,
            name VARCHAR(255) NOT NULL,
            cart TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (cashier_id) REFERENCES cashiers(id) ON DELETE CASCADE
        );
    """)

    cursor.execute("SELECT COUNT(*) FROM admins")
    if cursor.fetchone()[0] == 0:
        admin_hash = generate_password_hash('admin')
        answer_hash = generate_password_hash('generoso')
        cursor.execute(
            "INSERT INTO admins (username, password, full_name, security_question, security_answer, force_password_change) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ('admin', admin_hash, 'System Administrator', 'What is the name of the owner?', answer_hash, 0)
        )

    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO categories (category_name, description) VALUES "
            "('Medical', 'Medical products and medicines'), "
            "('Non-Medical', 'Supplies and hygiene products')"
        )

    cursor.execute("SELECT COUNT(*) FROM store_settings")
    if cursor.fetchone()[0] == 0:
        cursor.executescript("""
            INSERT INTO store_settings (setting_key, setting_value) VALUES
            ('receipt_header', 'PHARMACON'),
            ('receipt_subtitle', 'A''s PharmaHealth & Convenience'),
            ('receipt_footer', 'Thank you for your purchase!\nPlease come again.'),
            ('store_name', 'PharmaCon'),
            ('store_address', ''),
            ('store_contact', ''),
            ('return_policy', ''),
            ('website', ''),
            ('social_media', ''),
            ('currency_symbol', '₱'),
            ('tax_rate', '0'),
            ('tax_label', 'Tax'),
            ('discount_amount', '0'),
            ('discount_label', 'Discount'),
            ('font_size', 'medium'),
            ('paper_size', '80'),
            ('print_alignment', 'center'),
            ('line_style', 'dashed'),
            ('show_receipt_number', '1'),
            ('show_date', '1'),
            ('show_cashier', '1'),
            ('show_customer', '0'),
            ('show_medical_items', '1'),
            ('show_logo', '0'),
            ('show_footer', '1'),
            ('show_return_policy', '0'),
            ('show_website', '0'),
            ('show_social', '0'),
            ('show_barcode', '0'),
            ('show_subtotal', '0'),
            ('show_tax', '0'),
            ('show_discount', '0'),
            ('show_divider_after_header', '1'),
            ('show_divider_after_items', '1'),
            ('show_divider_after_total', '1'),
            ('show_divider_before_footer', '1'),
            ('tin', ''),
            ('vat_status', 'VAT Registered'),
            ('document_title', 'SALES INVOICE'),
            ('title_alignment', 'Center'),
            ('title_style', 'Bold'),
            ('invoice_prefix', 'INV-'),
            ('next_invoice_no', '0000123'),
            ('invoice_digits', '7'),
            ('show_date_time', 'Both'),
            ('date_format', 'MMM DD, YYYY'),
            ('time_format', '12-hour'),
            ('footer_alignment', 'Center'),
            ('footer_style', 'Normal'),
            ('show_item_header', '1'),
            ('show_tax_breakdown', '1'),
            ('show_cashier_name', '1'),
            ('show_payment_method', '1'),
            ('show_change', '1'),
            ('show_separator_lines', '1'),
            ('line_spacing', 'Compact'),
            ('print_density', 'Normal');
        """)

    cursor.execute("SELECT COUNT(*) FROM alert_settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO alert_settings (setting_name, setting_value) VALUES "
            "('low_stock_threshold', '10'), ('critical_stock_threshold', '5'), "
            "('expiry_critical_days', '7'), ('expiry_warning_days', '30')"
        )

    conn.commit()
    conn.close()
