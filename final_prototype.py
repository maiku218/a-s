from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
from pathlib import Path
import json


DATA_FILE = Path(__file__).with_name("final_prototype_data.json")
LOW_STOCK_LIMIT = 10


def format_money(value):
    return f"PHP {value:,.2f}"


def input_text(prompt):
    return input(prompt).strip()


def input_number(prompt):
    while True:
        value = input_text(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid number. Try again.")


def input_int(prompt):
    while True:
        value = input_text(prompt)
        try:
            return int(value)
        except ValueError:
            print("Invalid number. Try again.")


def print_header(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def is_expiring_soon(expiration_date):
    exp_date = parse_date(expiration_date)
    if not exp_date:
        return False
    return exp_date <= date.today() + timedelta(days=30)


class Entity(ABC):
    @property
    @abstractmethod
    def id(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass


class Product(Entity):
    def __init__(self, product_id, name, barcode, product_type, price, stock, expiration_date):
        self._id = product_id
        self.name = name
        self.barcode = barcode
        self.product_type = product_type
        self.price = price
        self.stock = stock
        self.expiration_date = expiration_date

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Product name is required.")
        self._name = value

    @property
    def barcode(self):
        return self._barcode

    @barcode.setter
    def barcode(self, value):
        if not value:
            raise ValueError("Barcode is required.")
        self._barcode = value

    @property
    def product_type(self):
        return self._product_type

    @product_type.setter
    def product_type(self, value):
        if value not in ["Medical", "Non-Medical"]:
            raise ValueError("Product type must be Medical or Non-Medical.")
        self._product_type = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        value = int(value)
        if value < 0:
            raise ValueError("Stock cannot be negative.")
        self._stock = value

    @property
    def expiration_date(self):
        return self._expiration_date

    @expiration_date.setter
    def expiration_date(self, value):
        self._expiration_date = value

    @property
    def is_low_stock(self):
        return self.stock <= LOW_STOCK_LIMIT

    @property
    def is_expiring_soon(self):
        return is_expiring_soon(self.expiration_date)

    def subtotal(self, quantity):
        return self.price * quantity

    def decrease_stock(self, quantity):
        self.stock = self.stock - quantity

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "barcode": self.barcode,
            "type": self.product_type,
            "price": self.price,
            "stock": self.stock,
            "expiration_date": self.expiration_date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["name"],
            data["barcode"],
            data["type"],
            data["price"],
            data["stock"],
            data["expiration_date"]
        )


class User(Entity):
    def __init__(self, user_id, username, password, full_name, role):
        self._id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.role = role

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not value:
            raise ValueError("Username is required.")
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not value:
            raise ValueError("Password is required.")
        self._password = value

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        if not value:
            raise ValueError("Full name is required.")
        self._full_name = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if not value:
            raise ValueError("Role is required.")
        self._role = value

    def authenticate(self, password):
        return self.password == password

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "role": self.role
        }


class AdminUser(User):
    def __init__(self, user_id, username, password, full_name):
        super().__init__(user_id, username, password, full_name, "admin")


class CashierUser(User):
    def __init__(self, user_id, username, password, full_name):
        super().__init__(user_id, username, password, full_name, "cashier")


class IRepository(ABC):
    @abstractmethod
    def all_products(self):
        pass

    @abstractmethod
    def find_product_by_barcode(self, barcode):
        pass

    @abstractmethod
    def get_product_by_id(self, product_id):
        pass

    @abstractmethod
    def get_next_product_id(self):
        pass

    @abstractmethod
    def add_product(self, product):
        pass

    @abstractmethod
    def update_stock(self, product_id, new_stock):
        pass

    @abstractmethod
    def all_sales(self):
        pass

    @abstractmethod
    def get_next_sale_id(self):
        pass

    @abstractmethod
    def create_sale(self, sale):
        pass

    @abstractmethod
    def get_cashier(self, username):
        pass

    @abstractmethod
    def admin_user(self):
        pass


class JsonRepository(IRepository):
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = self._load()

    def _load(self):
        if not self.data_path.exists():
            return self._seed_data()
        try:
            with self.data_path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return self._seed_data()

    def _save(self):
        with self.data_path.open("w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=2)

    def _seed_data(self):
        data = {
            "products": [
                {"id": 1, "name": "Paracetamol 500mg", "barcode": "1001", "type": "Medical", "price": 5.00, "stock": 25, "expiration_date": "2027-01-15"},
                {"id": 2, "name": "Vitamin C 1000mg", "barcode": "1002", "type": "Medical", "price": 8.50, "stock": 8, "expiration_date": "2026-08-20"},
                {"id": 3, "name": "Alcohol 70%", "barcode": "1003", "type": "Non-Medical", "price": 35.00, "stock": 12, "expiration_date": "2028-05-01"},
            ],
            "cashiers": [
                {"id": 1, "username": "cashier", "password": "cashier123", "full_name": "Demo Cashier"}
            ],
            "sales": []
        }
        self.data = data
        self._save()
        return data

    def all_products(self):
        return [Product.from_dict(product) for product in self.data["products"]]

    def find_product_by_barcode(self, barcode):
        for product in self.data["products"]:
            if product["barcode"] == barcode:
                return Product.from_dict(product)
        return None

    def get_product_by_id(self, product_id):
        for product in self.data["products"]:
            if product["id"] == product_id:
                return Product.from_dict(product)
        return None

    def get_next_product_id(self):
        if not self.data["products"]:
            return 1
        return max(product["id"] for product in self.data["products"]) + 1

    def add_product(self, product):
        self.data["products"].append(product.to_dict())
        self._save()

    def update_stock(self, product_id, new_stock):
        for product in self.data["products"]:
            if product["id"] == product_id:
                product["stock"] = int(new_stock)
                self._save()
                return True
        return False

    def all_sales(self):
        return self.data["sales"]

    def get_next_sale_id(self):
        if not self.data["sales"]:
            return 1
        return max(sale["id"] for sale in self.data["sales"]) + 1

    def create_sale(self, sale):
        self.data["sales"].append(sale)
        self._save()

    def get_cashier(self, username):
        for index, cashier in enumerate(self.data["cashiers"], start=1):
            if cashier["username"] == username:
                cashier_id = cashier.get("id", index)
                full_name = cashier.get("full_name", "Cashier")
                return CashierUser(
                    cashier_id,
                    cashier["username"],
                    cashier["password"],
                    full_name
                )
        return None

    def admin_user(self):
        return AdminUser(1, "admin", "admin123", "System Administrator")


class ReceiptFormatter(ABC):
    @abstractmethod
    def format(self, cart, total, tendered, change):
        pass


class DetailedReceiptFormatter(ReceiptFormatter):
    def format(self, cart, total, tendered, change):
        lines = ["RECEIPT"]
        for item in cart:
            lines.append(f"{item['name']} x {item['quantity']} = {format_money(item['subtotal'])}")
        lines.append(f"Total: {format_money(total)}")
        lines.append(f"Tendered: {format_money(tendered)}")
        lines.append(f"Change: {format_money(change)}")
        return "\n".join(lines)


class SimpleReceiptFormatter(ReceiptFormatter):
    def format(self, cart, total, tendered, change):
        return f"Total: {format_money(total)} | Change: {format_money(change)}"


class PillarDemo:
    def run(self):
        print_header("OOP PILLARS IN THIS PROTOTYPE")
        print("1. Encapsulation: Product hides data and validates price/stock.")
        try:
            product = Product(999, "Demo Product", "999", "Medical", 10.00, 0, "2027-01-01")
            product.stock = -1
        except ValueError as error:
            print(f"Validation result: {error}")

        print("\n2. Inheritance: AdminUser and CashierUser inherit from User.")
        print(f"Admin role: {AdminUser(1, 'admin', 'admin123', 'System Administrator').role}")
        print(f"Cashier role: {CashierUser(1, 'cashier', 'cashier123', 'Demo Cashier').role}")

        print("\n3. Polymorphism: Different receipt formatters use format().")
        cart = [{"name": "Paracetamol 500mg", "quantity": 1, "subtotal": 5.00}]
        formatters = [DetailedReceiptFormatter(), SimpleReceiptFormatter()]
        for formatter in formatters:
            print(formatter.format(cart, 5.00, 10.00, 5.00))

        print("\n4. Abstraction: JsonRepository follows the IRepository interface.")
        print(f"Repository interface: {IRepository.__name__}")
        print(f"Repository implementation: {JsonRepository.__name__}")


def login(repository):
    print_header("PHARMACON TERMINAL PROTOTYPE")
    print("1. Admin")
    print("2. Cashier")
    print("0. Exit")
    choice = input_text("Choose role: ")

    if choice == "0":
        return None

    username = input_text("Username: ")
    password = input_text("Password: ")

    if choice == "1":
        user = repository.admin_user()
        if user.authenticate(password):
            return user
        print("Invalid admin login.")
        return None

    if choice == "2":
        user = repository.get_cashier(username)
        if user and user.authenticate(password):
            return user
        print("Invalid cashier login.")
        return None

    print("Invalid role.")
    return None


def admin_menu(repository):
    while True:
        print_header("ADMIN MENU")
        print("1. Dashboard")
        print("2. View Products")
        print("3. Add Product")
        print("4. Update Stock")
        print("5. Inventory Alerts")
        print("6. Sales Report")
        print("7. OOP Pillars Demo")
        print("0. Back")
        choice = input_text("Choose action: ")

        if choice == "1":
            show_dashboard(repository)
        elif choice == "2":
            show_products(repository)
        elif choice == "3":
            add_product(repository)
        elif choice == "4":
            update_stock(repository)
        elif choice == "5":
            show_alerts(repository)
        elif choice == "6":
            show_sales_report(repository)
        elif choice == "7":
            PillarDemo().run()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def cashier_menu(repository):
    while True:
        print_header("CASHIER MENU")
        print("1. New Sale")
        print("2. Sales History")
        print("3. OOP Pillars Demo")
        print("0. Back")
        choice = input_text("Choose action: ")

        if choice == "1":
            process_sale(repository)
        elif choice == "2":
            show_sales_history(repository)
        elif choice == "3":
            PillarDemo().run()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def show_dashboard(repository):
    products = repository.all_products()
    sales = repository.all_sales()
    total_products = len(products)
    low_stock = [product for product in products if product.is_low_stock]
    expiring = [product for product in products if product.is_expiring_soon]
    total_sales = sum(sale["total"] for sale in sales)

    print_header("DASHBOARD")
    print(f"Total Products : {total_products}")
    print(f"Low Stock      : {len(low_stock)}")
    print(f"Expiring Soon  : {len(expiring)}")
    print(f"Total Sales    : {format_money(total_sales)}")


def show_products(repository):
    products = repository.all_products()
    print_header("PRODUCT LIST")
    if not products:
        print("No products yet.")
        return

    print(f"{'ID':<5} {'Barcode':<10} {'Name':<28} {'Type':<15} {'Price':<10} {'Stock':<8} {'Expiry':<12}")
    for product in products:
        print(
            f"{product.id:<5} {product.barcode:<10} {product.name:<28} "
            f"{product.product_type:<15} {product.price:<10.2f} {product.stock:<8} "
            f"{product.expiration_date:<12}"
        )


def add_product(repository):
    print_header("ADD PRODUCT")
    name = input_text("Product name: ")
    barcode = input_text("Barcode: ")
    product_type = input_text("Type (Medical/Non-Medical): ").title()
    price = input_number("Price: ")
    stock = input_int("Stock: ")
    expiration_date = input_text("Expiration date (YYYY-MM-DD): ")

    try:
        product = Product(
            repository.get_next_product_id(),
            name,
            barcode,
            product_type,
            price,
            stock,
            expiration_date
        )
    except ValueError as error:
        print(error)
        return

    if repository.find_product_by_barcode(barcode):
        print("Barcode already exists.")
        return

    repository.add_product(product)
    print("Product added.")


def update_stock(repository):
    print_header("UPDATE STOCK")
    barcode = input_text("Product barcode: ")
    product = repository.find_product_by_barcode(barcode)

    if not product:
        print("Product not found.")
        return

    print(f"Current stock for {product.name}: {product.stock}")
    new_stock = input_int("New stock: ")

    try:
        product.stock = new_stock
    except ValueError as error:
        print(error)
        return

    repository.update_stock(product.id, product.stock)
    print("Stock updated.")


def show_alerts(repository):
    products = repository.all_products()
    print_header("INVENTORY ALERTS")

    low_stock = [product for product in products if product.is_low_stock]
    expiring = [product for product in products if product.is_expiring_soon]

    print("Low Stock:")
    if low_stock:
        for product in low_stock:
            print(f"- {product.name} ({product.barcode}), Stock: {product.stock}")
    else:
        print("- None")

    print("\nExpiring Soon:")
    if expiring:
        for product in expiring:
            print(f"- {product.name} ({product.barcode}), Expiry: {product.expiration_date}")
    else:
        print("- None")


def process_sale(repository):
    print_header("NEW SALE")
    cart = []

    while True:
        barcode = input_text("Scan barcode (or press Enter to checkout): ")
        if not barcode:
            break

        product = repository.find_product_by_barcode(barcode)
        if not product:
            print("Product not found.")
            continue

        quantity = input_int(f"Quantity for {product.name}: ")
        if quantity <= 0:
            print("Quantity must be greater than 0.")
            continue
        if quantity > product.stock:
            print("Not enough stock.")
            continue

        cart.append({
            "product_id": product.id,
            "name": product.name,
            "barcode": product.barcode,
            "price": product.price,
            "quantity": quantity,
            "subtotal": product.subtotal(quantity)
        })
        print(f"Added: {product.name} x {quantity}")

    if not cart:
        print("No items sold.")
        return

    total = sum(item["subtotal"] for item in cart)
    tendered = input_number("Amount tendered: ")

    if tendered < total:
        print("Insufficient payment.")
        return

    change = tendered - total

    for item in cart:
        product = repository.find_product_by_barcode(item["barcode"])
        try:
            product.decrease_stock(item["quantity"])
        except ValueError as error:
            print(error)
            return
        repository.update_stock(product.id, product.stock)

    sale = {
        "id": repository.get_next_sale_id(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": cart,
        "total": total,
        "tendered": tendered,
        "change": change
    }
    repository.create_sale(sale)
    print(DetailedReceiptFormatter().format(cart, total, tendered, change))
    print("Sale completed.")


def show_sales_history(repository):
    sales = repository.all_sales()
    print_header("SALES HISTORY")
    if not sales:
        print("No sales yet.")
        return

    for sale in reversed(sales):
        print(f"Sale #{sale['id']} | {sale['date']} | Total: {format_money(sale['total'])}")


def show_sales_report(repository):
    sales = repository.all_sales()
    print_header("SALES REPORT")
    if not sales:
        print("No sales yet.")
        return

    total_sales = sum(sale["total"] for sale in sales)
    print(f"Transactions : {len(sales)}")
    print(f"Total Sales  : {format_money(total_sales)}")
    print("\nRecent Sales:")
    for sale in reversed(sales[-10:]):
        print(f"Sale #{sale['id']} | {sale['date']} | Total: {format_money(sale['total'])}")


def main():
    repository = JsonRepository(DATA_FILE)

    while True:
        user = login(repository)
        if user is None:
            print("Exited.")
            break

        if isinstance(user, AdminUser):
            admin_menu(repository)
        elif isinstance(user, CashierUser):
            cashier_menu(repository)
        else:
            print("Unsupported role.")


if __name__ == "__main__":
    main()
