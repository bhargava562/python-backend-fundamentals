from typing import Optional, Union
from collections.abc import Callable

# Basic: parameter types and return type
def add(a: int, b: int) -> int:
    return a + b

# Optional means the value can be the type OR None
def find_user(user_id: int) -> Optional[str]:
    db = {1: "Aravind", 2: "Priya"}
    return db.get(user_id)   # returns str or None

# Union means it can be one of multiple types
def display(value: Union[int, str, float]) -> str:
    return f"Value is: {value}"

# list[type], dict[key_type, value_type]
def total(prices: list[float]) -> float:
    return sum(prices)

def build_catalogue(items: list[str]) -> dict[str, int]:
    return {item: idx for idx, item in enumerate(items)}

# Callable[[input_types], return_type]
def apply_twice(fn: Callable[[int], int], x: int) -> int:
    return fn(fn(x))          # applies fn two times

# tuple with fixed types
def get_coordinates() -> tuple[float, float]:
    return (13.0827, 80.2707)   # Chennai lat, lng

# ── Running all examples ──
print(add(3, 4))
print(find_user(1))
print(find_user(99))
print(display(42))
print(total([99.0, 49.5, 150.0]))
print(build_catalogue(["Laptop", "Phone", "Tablet"]))
print(apply_twice(lambda x: x * 2, 3))
print(get_coordinates())