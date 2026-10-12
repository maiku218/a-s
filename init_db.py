#!/usr/bin/env python3
"""
Database initialization script.
Run this once after cloning to create the database with default admin/cashier accounts.
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pharmacon.db')

def init_database():
    """Initialize database with schema and default accounts."""
    # Import the migration/init logic from database_sqlite
    import database_sqlite
    database_sqlite.init_db()
    database_sqlite.run_migrations()
    
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    
    # Create default admin if not exists
    cur.execute("SELECT COUNT(*) FROM admins WHERE username=?", ('admin',))
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO admins (username, password, full_name, security_question, security_answer, force_password_change)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            'admin',
            generate_password_hash('admin123'),
            'System Administrator',
            'What is the name of the pharmacy?',
            generate_password_hash('pharmacon'),
            0  # No forced password change
        ))
        print("Created default admin: admin / admin123")
    else:
        # Ensure existing admin doesn't have force_password_change
        cur.execute("UPDATE admins SET force_password_change=0 WHERE username=?", ('admin',))
    
    # Create default cashier if not exists (same password as admin)
    cur.execute("SELECT COUNT(*) FROM cashiers WHERE username=?", ('cashier',))
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO cashiers (full_name, username, password, security_question, security_answer, status, force_password_change)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            'Default Cashier',
            'cashier',
            generate_password_hash('admin123'),
            'What is the name of the owner?',
            generate_password_hash('generoso'),
            'active',
            0
        ))
        print("Created default cashier: cashier / admin123")
    
    # Seed alert settings if empty
    cur.execute("SELECT COUNT(*) FROM alert_settings")
    if cur.fetchone()[0] == 0:
        settings = [
            ('low_stock_threshold', '10'),
            ('critical_stock_threshold', '5'),
            ('expiry_critical_days', '7'),
            ('expiry_warning_days', '30'),
        ]
        cur.executemany("INSERT OR IGNORE INTO alert_settings (setting_name, setting_value) VALUES (?, ?)", settings)
        print("Seeded alert settings")
    
    con.commit()
    con.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()