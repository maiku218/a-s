-- PharmaCon Database Schema
-- Run this SQL to create the database and tables

-- Create database
CREATE DATABASE IF NOT EXISTS pharmacon;
USE pharmacon;

-- Admins table
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    security_question VARCHAR(255),
    security_answer VARCHAR(255),
    force_password_change TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cashiers table
CREATE TABLE IF NOT EXISTS cashiers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    security_question VARCHAR(255),
    security_answer VARCHAR(255),
    force_password_change TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cashier Activity (login/logout tracking) - UPDATED with IP address
CREATE TABLE IF NOT EXISTS cashier_activity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cashier_id INT NOT NULL,
    login_time DATETIME NOT NULL,
    logout_time DATETIME DEFAULT NULL,
    ip_address VARCHAR(45) DEFAULT NULL,
    FOREIGN KEY (cashier_id) REFERENCES cashiers(id) ON DELETE CASCADE
);

-- Admin Activity (detailed admin actions tracking) - NEW
CREATE TABLE IF NOT EXISTS admin_activity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    action VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45) DEFAULT NULL,
    details TEXT,
    activity_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE
);

-- Login Attempts (rate limiting and lockout tracking)
CREATE TABLE IF NOT EXISTS login_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_address VARCHAR(45) DEFAULT NULL,
    username_attempted VARCHAR(100) DEFAULT NULL,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    locked_until TIMESTAMP NULL DEFAULT NULL,
    INDEX idx_ip_attempted (ip_address, attempted_at),
    INDEX idx_username_attempted (username_attempted, attempted_at)
);

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    barcode VARCHAR(100) DEFAULT NULL,
    category_id INT,
    product_type VARCHAR(50) DEFAULT 'medical',
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    expiration_date DATE DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Stock Movements table
CREATE TABLE IF NOT EXISTS stock_movements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    movement_type VARCHAR(10) NOT NULL,
    quantity INT NOT NULL,
    reason VARCHAR(100),
    movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Sales table
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receipt_number VARCHAR(50) UNIQUE NOT NULL,
    cashier_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    sale_status VARCHAR(20) DEFAULT 'Completed',
    product_type VARCHAR(20) DEFAULT 'medical',
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    receipt_printed TINYINT(1) DEFAULT 0,
    printed_at TIMESTAMP NULL DEFAULT NULL,
    voided_at TIMESTAMP NULL DEFAULT NULL,
    voided_by INT NULL DEFAULT NULL,
    void_reason TEXT NULL DEFAULT NULL,
    refunded_at TIMESTAMP NULL DEFAULT NULL,
    refunded_by INT NULL DEFAULT NULL,
    refund_reason TEXT NULL DEFAULT NULL,
    original_sale_id INT NULL DEFAULT NULL,
    FOREIGN KEY (cashier_id) REFERENCES cashiers(id)
);

-- Sale Items table
CREATE TABLE IF NOT EXISTS sale_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Insert default admin (username: admin, password: admin123)
INSERT INTO admins (username, password, full_name, security_question, security_answer, force_password_change) 
VALUES ('admin', 'pbkdf2:sha256:600000$azTbU7sExjOzKtbr$392d9a3215fd515a6f540498d6c47b386a404b52adad96ce9d419cdde1513482', 'System Administrator', 'What is the name of the owner?', 'pbkdf2:sha256:600000$BlhM6ndrgPIj0Eui$8c0c6511b8af1f42401c742e1da56b34bfb60e56d703087fcc4f013f2cc2ecae', 1);

-- Insert sample categories
INSERT INTO categories (category_name, description) VALUES 
('Medical', 'Medical products and medicines'),
('Non-Medical', 'Supplies and hygiene products');

-- Fix: Update product types to use correct case ('Medical', 'Non-Medical')
-- This fixes the case sensitivity issue where products were stored as lowercase
UPDATE products SET product_type = 'Medical' WHERE product_type = 'medical';
UPDATE products SET product_type = 'Non-Medical' WHERE product_type = 'non_medical';

-- Fix: Update sales product_type to use correct case
-- This ensures sales are properly categorized in reports
UPDATE sales SET product_type = 'Medical' WHERE product_type = 'medical';
UPDATE sales SET product_type = 'Non-Medical' WHERE product_type = 'non_medical';

-- Store Settings (receipt customization, store info)
CREATE TABLE IF NOT EXISTS store_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO store_settings (setting_key, setting_value) VALUES
('receipt_header', 'PHARMACON'),
('receipt_subtitle', 'A\'s PharmaHealth & Convenience'),
('receipt_footer', 'Thank you for your purchase!\nPlease come again.'),
('store_name', 'PharmaCon'),
('store_address', ''),
('store_contact', '');

-- Alert Logs (track alert history and acknowledgments) - NEW
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
);

-- Alert Settings (configurable thresholds) - NEW
CREATE TABLE IF NOT EXISTS alert_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_name VARCHAR(100) NOT NULL UNIQUE,
    setting_value VARCHAR(255) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO alert_settings (setting_name, setting_value) VALUES
('low_stock_threshold', '10'),
('critical_stock_threshold', '5'),
('expiry_critical_days', '7'),
('expiry_warning_days', '30');

-- Alert Acknowledgment Tracking
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
);

-- Alert Visibility per Admin (hide dismissed alerts)
CREATE TABLE IF NOT EXISTS alert_visibility (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    admin_id INT NOT NULL,
    is_hidden TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE,
    UNIQUE KEY unique_visibility (product_id, alert_type, admin_id)
);
