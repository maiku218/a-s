from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash


# ================================================
# PILLAR 4: ABSTRACTION
# ================================================

class IEntity(ABC):
    @property
    @abstractmethod
    def id(self) -> int:
        ...


class IRepository(ABC):
    @abstractmethod
    def get_all(self):
        ...

    @abstractmethod
    def get_by_id(self, entity_id: int):
        ...

    @abstractmethod
    def save(self, entity):
        ...

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        ...


# ================================================
# PILLAR 1: ENCAPSULATION (3 examples)
# ================================================

class StockMovement:
    """Example 1 of Encapsulation: all fields are private (_movement_type, _quantity, _reason).
    They can ONLY be changed through the constructor or dedicated methods.
    This prevents an external caller from setting an invalid movement type."""

    IN = 'IN'
    OUT = 'OUT'

    def __init__(self, movement_id: int, product_id: int, movement_type: str,
                 quantity: int, reason: str):
        self._id = movement_id
        self._product_id = product_id
        self._movement_type = movement_type  # validated through constructor
        self._quantity = quantity
        self._reason = reason

    @property
    def id(self) -> int:
        return self._id

    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def movement_type(self) -> str:
        return self._movement_type

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def reason(self) -> str:
        return self._reason

    def is_inbound(self) -> bool:
        return self._movement_type == self.IN

    def is_outbound(self) -> bool:
        return self._movement_type == self.OUT

    def to_dict(self) -> dict:
        return {
            'movement_id': self._id,
            'product_id': self._product_id,
            'movement_type': self._movement_type,
            'quantity': self._quantity,
            'reason': self._reason,
        }

    def __repr__(self):
        return f"<StockMovement id={self._id} type={self._movement_type} qty={self._quantity}>"


class Product(IEntity):
    """Example 2 of Encapsulation: _price and _stock are private.
    Changing them requires going through the property setter, which validates
    the value (e.g., negative price is rejected)."""

    def __init__(self, product_id: int, name: str, barcode: str, category_id: int,
                 product_type: str, price: Decimal, stock: int,
                 expiration_date: Optional[datetime]):
        self._id = product_id
        self._name = name
        self._barcode = barcode
        self._category_id = category_id
        self._product_type = product_type
        self._price = Decimal(str(price))
        self._stock = int(stock)
        self._expiration_date = expiration_date

    # --- IEntity ---
    @property
    def id(self) -> int:
        return self._id

    # --- Read-only properties for data that should not be reassigned externally ---
    @property
    def barcode(self) -> str:
        return self._barcode

    @property
    def category_id(self) -> int:
        return self._category_id

    @property
    def product_type(self) -> str:
        return self._product_type

    @property
    def expiration_date(self) -> Optional[datetime]:
        return self._expiration_date

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Product name cannot be empty.")
        self._name = value.strip()

    # --- Example 2: encapsulated price with validation ---
    @property
    def price(self) -> Decimal:
        return self._price

    @price.setter
    def price(self, value):
        if value is None or Decimal(str(value)) < 0:
            raise ValueError("Price cannot be negative or null.")
        self._price = Decimal(str(value))

    # --- Example 3: encapsulated stock with business rule ---
    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value):
        value = int(value)
        if value < 0:
            raise ValueError("Stock cannot be negative.")
        self._stock = value

    @property
    def is_low_stock(self) -> bool:
        """Derived state: low stock if <= 10 units."""
        return self._stock <= 10

    @property
    def is_expiring_soon(self) -> bool:
        """Derived state: expiring within 30 days."""
        if self._expiration_date is None:
            return False
        return self._expiration_date.date() <= (datetime.now() + timedelta(days=30)).date()

    def apply_movement(self, quantity: int, movement_type: str = StockMovement.IN):
        """Encapsulated business rule: stock is changed through a controlled method."""
        if movement_type == StockMovement.IN:
            self._stock += quantity
        elif movement_type == StockMovement.OUT:
            if self._stock < quantity:
                raise ValueError(
                    f"Insufficient stock for '{self._name}'. "
                    f"Available: {self._stock}, Requested: {quantity}"
                )
            self._stock -= quantity
        else:
            raise ValueError(f"Invalid movement type: {movement_type}")

    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'name': self._name,
            'barcode': self._barcode,
            'product_type': self._product_type,
            'price': float(self._price),
            'stock': self._stock,
        }

    def __repr__(self):
        return (
            f"<Product id={self._id} name='{self._name}' "
            f"price={float(self._price)} stock={self._stock}>"
        )


# ================================================
# PILLAR 2: INHERITANCE (3 examples)
# ================================================

class User(IEntity):
    """Base User class. Admin and Cashier INHERIT from this."""

    def __init__(self, user_id: int, username: str, full_name: str, password_hash: str):
        self._id = user_id
        self._username = username
        self._full_name = full_name
        self._password_hash = password_hash

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def full_name(self) -> str:
        return self._full_name

    def verify_password(self, password: str) -> bool:
        """Shared method for both Admin and Cashier."""
        return check_password_hash(self._password_hash, password)

    def authenticate(self, password: str) -> bool:
        """Polymorphic authentication method."""
        return self.verify_password(password)


class Admin(User):
    """Inheritance Example 1: Admin extends User."""

    Role = 'admin'

    def __init__(self, user_id: int, username: str, full_name: str, password_hash: str):
        super().__init__(user_id, username, full_name, password_hash)

    def authenticate(self, password: str, mysql, request) -> tuple:
        """Polymorphism Example 1: Admin authentication includes activity logging."""
        if not self.verify_password(password):
            return False, None
        self._log_login(mysql, request)
        return True, self

    def _log_login(self, mysql, request):
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO admin_activity (admin_id, action, ip_address, details)
                VALUES (%s, %s, %s, %s)
            """, (self._id, 'Admin Login', ip_address,
                  f"Admin {self._username} logged in"))
            mysql.connection.commit()
        except Exception:
            mysql.connection.rollback()
        finally:
            cur.close()

    def create_default_if_none(self, mysql):
        """Admin-specific method: creates the default admin account if no admins exist."""
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM admins")
            count = cur.fetchone()[0]
            if count == 0:
                hashed = generate_password_hash('admin123')
                cur.execute(
                    "INSERT INTO admins (username, password, full_name) "
                    "VALUES (%s, %s, %s)",
                    ('admin', hashed, 'System Administrator')
                )
                try:
                    cur.execute(
                        "ALTER TABLE admins ADD COLUMN force_password_change TINYINT(1) DEFAULT 0"
                    )
                except Exception:
                    pass
                cur.execute(
                    "UPDATE admins SET force_password_change=1 WHERE username='admin'"
                )
                mysql.connection.commit()
                return Admin(1, 'admin', 'System Administrator', hashed)
        finally:
            cur.close()
        return None


class Cashier(User):
    """Inheritance Example 2: Cashier extends User with additional 'status' field."""

    Role = 'cashier'

    def __init__(self, user_id: int, username: str, full_name: str,
                 password_hash: str, status: str = 'Active'):
        super().__init__(user_id, username, full_name, password_hash)
        self._status = status

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in ('Active', 'Inactive'):
            raise ValueError("Status must be Active or Inactive.")
        self._status = value

    def authenticate(self, password: str, mysql, request) -> tuple:
        """Polymorphism Example 2: Cashier authentication logs into cashier_activity table."""
        if not self.verify_password(password):
            return False, None
        self._log_login(mysql, request)
        return True, self

    def _log_login(self, mysql, request):
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For')
        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO cashier_activity (cashier_id, login_time, ip_address)
                VALUES (%s, NOW(), %s)
            """, (self._id, ip_address))
            mysql.connection.commit()
        except Exception:
            mysql.connection.rollback()
        finally:
            cur.close()

    def log_logout(self, mysql):
        """Cashier-specific method: records logout time."""
        ip_address = 'unknown'
        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                UPDATE cashier_activity
                SET logout_time = NOW()
                WHERE cashier_id = %s AND logout_time IS NULL
            """, (self._id,))
            mysql.connection.commit()
        finally:
            cur.close()


# ================================================
# PILLAR 3: POLYMORPHISM (3 examples)
# ================================================

class StockMovementProcessor:
    """Example 1 of Polymorphism: different processors handle stock differently."""

    def __init__(self, movement: StockMovement, mysql):
        self.movement = movement
        self.mysql = mysql

    def process(self, product: Product):
        raise NotImplementedError  # subclasses must override


class StockInProcessor(StockMovementProcessor):
    """Polymorphic implementation: adds stock."""

    def process(self, product: Product):
        product.apply_movement(self.movement.quantity, StockMovement.IN)
        self._record_movement(product)

    def _record_movement(self, product: Product):
        cur = self.mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                VALUES (%s, 'IN', %s, %s)
            """, (product.id, self.movement.quantity, self.movement.reason))
            self.mysql.connection.commit()
        finally:
            cur.close()


class StockOutProcessor(StockMovementProcessor):
    """Polymorphic implementation: removes stock."""

    def process(self, product: Product):
        product.apply_movement(self.movement.quantity, StockMovement.OUT)
        self._record_movement(product)

    def _record_movement(self, product: Product):
        cur = self.mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                VALUES (%s, 'OUT', %s, %s)
            """, (product.id, self.movement.quantity, self.movement.reason))
            self.mysql.connection.commit()
        finally:
            cur.close()


def get_movement_processor(movement: StockMovement, mysql) -> StockMovementProcessor:
    """Factory function that returns the correct polymorphic processor."""
    if movement.is_inbound():
        return StockInProcessor(movement, mysql)
    elif movement.is_outbound():
        return StockOutProcessor(movement, mysql)
    raise ValueError(f"Unknown movement type: {movement.movement_type}")
