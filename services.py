from abc import abstractmethod
from typing import Optional, List, Dict
import random
from datetime import datetime
from models import (
    User, Admin, Cashier, Product, StockMovement,
    StockInProcessor, StockOutProcessor, get_movement_processor,
    StockMovementProcessor
)

# ================================================
# ABSTRACTION: Service interfaces
# ================================================

class IAuthService(ABC):
    """Abstraction: defines the contract for authentication."""

    @abstractmethod
    def login(self, username: str, password: str, request) -> tuple[bool, Optional[User]]:

        ...

    @abstractmethod
    def logout(self, user: User, mysql) -> bool:

        ...

    @abstractmethod
    def get_session_data(self, user: User) -> dict:

        ...



class ISalesService(ABC):
    """Abstraction: defines the contract for sales operations."""

    @abstractmethod
    def process_sale(self, items: list, cashier: Cashier) -> dict:

        ...


# ================================================
# IMPLEMENTATIONS (Inheritance + Polymorphism)
# ================================================

class AuthService(IAuthService):
    """Polymorphism: different login/logout behavior for admin vs cashier."""

    def login(self, username: str, password: str, request, mysql,
              user_type: str = 'admin') -> tuple[bool, Optional[User]]:
        user = self._fetch_user(username, user_type, mysql)
        if not user:
            # Create default admin if none exists (admin-specific logic)
            if user_type == 'admin':
                user = self._create_default_admin(mysql)
            if not user:
                return False, None

        user_from_db = self._hydrate_user(user, user_type, mysql)
        if not user_from_db:
            return False, None

        success, result_user = user_from_db.authenticate(password, mysql, request)
        return success, result_user

    def logout(self, user: User, mysql) -> bool:
        try:
            if isinstance(user, Cashier):
                user.log_logout(mysql)
            return True
        except Exception:
            return False

    def get_session_data(self, user: User) -> dict:
        if isinstance(user, Admin):
            return {
                'admin_user': user.username,
                'admin_id': user.id,
                'role': 'admin'
            }
        elif isinstance(user, Cashier):
            return {
                'cashier_user': user.username,
                'cashier_id': user.id,
                'role': 'cashier'
            }
        return {}

    # --- Private methods (Encapsulation) ---
    def _fetch_user(self, username: str, user_type: str, mysql):
        cur = mysql.connection.cursor()
        try:
            table = 'admins' if user_type == 'admin' else 'cashiers'
            cur.execute(f"SELECT * FROM {table} WHERE username=%s", (username,))
            return cur.fetchone()
        finally:
            cur.close()

    def _create_default_admin(self, mysql):
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM admins")
            count = cur.fetchone()[0]
            if count == 0:
                hashed = self._generate_password('admin123')
                cur.execute(
                    "INSERT INTO admins (username, password, full_name) "
                    "VALUES (%s, %s, %s)",
                    ('admin', hashed, 'System Administrator')
                )
                mysql.connection.commit()
                return {'id': 1, 'username': 'admin',
                        'full_name': 'System Administrator',
                        'password': hashed}
        finally:
            cur.close()
        return None

    def _hydrate_user(self, row, user_type: str, mysql):
        if not row:
            return None
        password_hash = row[2]
        if user_type == 'admin':
            return Admin(row[0], row[1],
                         row[3] if len(row) > 3 else 'Administrator',
                         password_hash)
        else:
            status = row[4] if len(row) > 4 else 'Active'
            return Cashier(row[0], row[1], row[2], password_hash, status)

    def _generate_password(self, password: str) -> str:
        from werkzeug.security import generate_password_hash
        return generate_password_hash(password)


class ProductRepository:
    """Abstraction: hides all raw SQL from the rest of the codebase.
    Clients work with Product objects, never raw tuples."""

    def __init__(self, mysql):
        self.mysql = mysql

    def find_by_id(self, product_id: int) -> Optional[Product]:
        cur = self.mysql.connection.cursor()
        try:
            cur.execute(
                "SELECT id, product_name, barcode, category_id, "
                "product_type, price, stock, expiration_date "
                "FROM products WHERE id=%s", (product_id,)
            )
            row = cur.fetchone()
            if not row:
                return None
            return self._row_to_product(row)
        finally:
            cur.close()

    def find_by_barcode(self, barcode: str) -> Optional[Product]:
        cur = self.mysql.connection.cursor()
        try:
            cur.execute(
                "SELECT id, product_name, barcode, category_id, "
                "product_type, price, stock, expiration_date "
                "FROM products WHERE barcode=%s LIMIT 1", (barcode,)
            )
            row = cur.fetchone()
            if not row:
                return None
            return self._row_to_product(row)
        finally:
            cur.close()

    def find_all(self) -> List[Product]:
        cur = self.mysql.connection.cursor()
        try:
            cur.execute("SELECT id, product_name, barcode, category_id, "
                        "product_type, price, stock, expiration_date "
                        "FROM products ORDER BY product_name ASC")
            rows = cur.fetchall()
            return [self._row_to_product(r) for r in rows]
        finally:
            cur.close()

    def find_low_stock(self, threshold: int = 10) -> List[Product]:
        products = self.find_all()
        return [p for p in products if p.is_low_stock]

    def link_stock_movement(self, product: Product, movement: StockMovement):
        processor = get_movement_processor(movement, self.mysql)
        processor.process(product)

    def save(self, product: Product):
        cur = self.mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO products (product_name, barcode, category_id, product_type,
                                     price, stock, expiration_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                product.name, product.barcode, product.category_id,
                product.product_type, float(product.price),
                product.stock, product.expiration_date
            ))
            self.mysql.connection.commit()
        finally:
            cur.close()

    def update_stock(self, product_id: int, new_stock: int):
        cur = self.mysql.connection.cursor()
        try:
            cur.execute("UPDATE products SET stock=%s WHERE id=%s",
                        (new_stock, product_id))
            self.mysql.connection.commit()
        finally:
            cur.close()

    def delete(self, product_id: int):
        cur = self.mysql.connection.cursor()
        try:
            cur.execute("DELETE FROM stock_movements WHERE product_id=%s", (product_id,))
            cur.execute("DELETE FROM sale_items WHERE product_id=%s", (product_id,))
            cur.execute("DELETE FROM products WHERE id=%s", (product_id,))
            self.mysql.connection.commit()
        finally:
            cur.close()

    def count_low_stock(self, threshold: int = 10) -> int:
        cur = self.mysql.connection.cursor()
        try:
            cur.execute(
                "SELECT COUNT(*) FROM products WHERE stock <= %s", (threshold,)
            )
            return cur.fetchone()[0]
        finally:
            cur.close()

    def count_expiring(self) -> int:
        cur = self.mysql.connection.cursor()
        try:
            cur.execute(
                "SELECT COUNT(*) FROM products WHERE expiration_date <= "
                "CURDATE() + INTERVAL 30 DAY AND expiration_date IS NOT NULL"
            )
            return cur.fetchone()[0]
        finally:
            cur.close()

    def _row_to_product(self, row) -> Product:
        return Product(
            product_id=row[0],
            name=row[1],
            barcode=row[2] if row[2] else '',
            category_id=row[3] if row[3] else 0,
            product_type=row[4],
            price=row[5],
            stock=row[6],
            expiration_date=row[7]
        )

    def search(self, query: str) -> List[Dict]:
        all_products = self.find_all()
        q = query.lower().strip()
        return [
            {
                'id': p.id,
                'name': p.name,
                'price': float(p.price),
                'stock': p.stock,
                'barcode': p.barcode,
                'expiry': p.expiration_date.strftime('%m/%d/%Y')
                if p.expiration_date else 'N/A'
            }
            for p in all_products
            if q in p.name.lower() or q in p.barcode.lower()
        ]


class SalesService(ISalesService):
    """Polymorphism Example 3: different sale processors for Medical vs Non-Medical."""

    def __init__(self, mysql):
        self.mysql = mysql

    def process_sale(self, items: list, cashier: Cashier) -> dict:
        try:
            items = self._validate_items(items)
            cur = self.mysql.connection.cursor()
            try:
                return self._process_sale_impl(items, cashier, cur)
            finally:
                cur.close()
        except Exception as e:
            self.mysql.connection.rollback()
            return {'success': False, 'message': str(e)}

    def _validate_items(self, items: list):
        if not items:
            raise ValueError("No items in cart.")
        for item in items:
            if 'id' not in item or 'quantity' not in item:
                raise ValueError("Invalid item data.")
        return items

    def _process_sale_impl(self, items: list, cashier: Cashier, cur) -> dict:
        medical_items = []
        non_medical_items = []

        for item in items:
            cur.execute("SELECT product_type FROM products WHERE id = %s", (item['id'],))
            result = cur.fetchone()
            product_type = result[0] if result else 'Non-Medical'
            if product_type == 'Medical':
                medical_items.append(item)
            else:
                non_medical_items.append(item)

        receipt_numbers = []
        receipt_items = []
        total_amount = 0.0

        if medical_items:
            receipt_number, sale_total, sale_items = self._create_sale(
                cur, medical_items, cashier.id, 'Medical'
            )
            receipt_numbers.append(receipt_number)
            total_amount += sale_total
            receipt_items.extend(sale_items)

        if non_medical_items:
            receipt_number, sale_total, sale_items = self._create_sale(
                cur, non_medical_items, cashier.id, 'Non-Medical'
            )
            receipt_numbers.append(receipt_number)
            total_amount += sale_total
            receipt_items.extend(sale_items)

        self.mysql.connection.commit()
        return {
            'success': True,
            'receipt_number': receipt_numbers[0] if receipt_numbers else 'N/A',
            'total': total_amount,
            'items': receipt_items,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def _create_sale(self, cur, items: list, cashier_id: int,
                     product_type: str):
        receipt_number = (f"REC-{datetime.now().strftime('%Y%m%d')}"
                          f"-{random.randint(1000, 9999)}")
        sale_total = sum(item['price'] * item['quantity'] for item in items)

        cur.execute("""
            INSERT INTO sales (receipt_number, cashier_id, total_amount,
                               sale_status, product_type, sale_date)
            VALUES (%s, %s, %s, 'Completed', %s, NOW())
        """, (receipt_number, cashier_id, sale_total, product_type))
        sale_id = cur.lastrowid

        sale_items = []
        for item in items:
            cur.execute("""
                INSERT INTO sale_items (sale_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (sale_id, item['id'], item['quantity'], item['price']))

            cur.execute("""
                UPDATE products SET stock = stock - %s WHERE id = %s
            """, (item['quantity'], item['id']))

            cur.execute("""
                INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                VALUES (%s, 'OUT', %s, 'Sale')
            """, (item['id'], item['quantity']))

            sale_items.append({
                'name': item['name'],
                'quantity': item['quantity'],
                'price': item['price'],
                'subtotal': item['price'] * item['quantity']
            })
        return receipt_number, sale_total, sale_items
