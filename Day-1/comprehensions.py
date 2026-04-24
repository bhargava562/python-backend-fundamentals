products = [
    {"name": "Laptop",  "price": 999, "stock": 5,  "category": "electronics"},
    {"name": "Phone",   "price": 599, "stock": 0,  "category": "electronics"},
    {"name": "Tablet",  "price": 349, "stock": 12, "category": "electronics"},
    {"name": "Notebook","price": 5,   "stock": 200,"category": "stationery"},
]

# ── List comprehensions ──
# Get all product names
names = [p["name"] for p in products]

# Only products that are in stock
in_stock = [p["name"] for p in products if p["stock"] > 0]

# Apply 10% discount to expensive items
discounted = [
    {"name": p["name"], "new_price": round(p["price"] * 0.9, 2)}
    for p in products
    if p["price"] > 100
]

# ── Dictionary comprehensions ──
# name → price mapping
price_map = {p["name"]: p["price"] for p in products}

# name → "IN STOCK" or "OUT OF STOCK"
availability = {
    p["name"]: "In Stock" if p["stock"] > 0 else "Out of Stock"
    for p in products
}

# ── Set comprehension: unique categories ──
categories = {p["category"] for p in products}

print("All names:",    names)
print("In stock:",     in_stock)
print("Discounted:",  discounted)
print("Price map:",    price_map)
print("Availability:",availability)
print("Categories:",  categories)