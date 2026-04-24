import json
from datetime import datetime

class Product:
    def __init__(self, name: str, price: float, stock: int) -> None:
        self.name   = name
        self._price = price   # _ prefix = treat as private
        self.stock  = stock

    # ── @property: controlled attribute access ──
    @property
    def price(self) -> float:
        # Called when you READ:  product.price
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        # Called when you WRITE: product.price = 500
        if value < 0:
            raise ValueError("Price cannot be negative!")
        self._price = value

    @property
    def discounted_price(self) -> float:
        # Computed property — no setter needed
        return round(self._price * 0.9, 2)   # always 10% off

    # ── @staticmethod: utility that needs no self or cls ──
    @staticmethod
    def is_valid_price(value: float) -> bool:
        # A helper — doesn't touch the object, belongs to the class
        return isinstance(value, (int, float)) and value >= 0

    # ── @classmethod: alternative constructor (factory method) ──
    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        # cls refers to Product itself — creates a new instance
        return cls(data["name"], data["price"], data["stock"])

    @classmethod
    def from_json(cls, json_str: str) -> "Product":
        return cls.from_dict(json.loads(json_str))


# ── Using the decorators ──
p = Product("Laptop", 999.99, 10)

print(p.price)              # 999.99   — calls @property getter
p.price = 899.99           # calls @price.setter (validates)
print(p.price)              # 899.99
print(p.discounted_price)   # 809.99   — computed property

print(Product.is_valid_price(50))    # True  — staticmethod
print(Product.is_valid_price(-10))   # False

data = {"name": "Phone", "price": 599, "stock": 25}
phone = Product.from_dict(data)      # classmethod constructor
print(phone.name, phone.price)        # Phone 599