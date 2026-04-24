from typing import Any

# ── *args: variable positional arguments ──
def calculate_total(*prices: float) -> float:
    # prices is a TUPLE of whatever numbers were passed
    print(f"Received {len(prices)} prices: {prices}")
    return sum(prices)

print(calculate_total(99.0))                   # 1 item
print(calculate_total(99.0, 49.5, 149.99))      # 3 items
print(calculate_total(10, 20, 30, 40, 50))        # 5 items


# ── **kwargs: variable keyword arguments ──
def create_user_profile(**details: Any) -> dict:
    # details is a DICT of whatever key=value pairs were passed
    print(f"Building profile with: {list(details.keys())}")
    return details

profile = create_user_profile(
    name="Aravind",
    city="Chennai",
    age=25,
    premium=True
)
print(profile)


# ── Combined: *args + **kwargs ──
def place_order(user: str, *items: str, **options: Any) -> dict:
    """
    user    — required positional arg
    *items  — any number of product names
    **options — optional settings like express, gift_wrap, note
    """
    order = {
        "customer" : user,
        "items"    : list(items),
        "express"  : options.get("express",   False),
        "gift_wrap": options.get("gift_wrap", False),
        "note"     : options.get("note",      ""),
    }
    return order

order1 = place_order("Aravind", "Laptop", "Mouse")
order2 = place_order("Priya", "Phone", express=True, gift_wrap=True, note="Birthday!")

print("\nOrder 1:", order1)
print("Order 2:", order2)

# ── Unpacking with * and ** ──
nums     = [10, 20, 30]
settings = {"express": True, "note": "Urgent"}

order3 = place_order("Kumar", "Tablet", **settings)  # unpack dict
print("Order 3:", order3)