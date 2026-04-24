from functools import reduce

products = [
    {"name": "Laptop",  "price": 999, "rating": 4.5},
    {"name": "Phone",   "price": 599, "rating": 4.2},
    {"name": "Tablet",  "price": 349, "rating": 3.8},
    {"name": "Watch",   "price": 199, "rating": 4.7},
]

# ── Lambda: one-line anonymous function ──
double   = lambda x: x * 2          # equivalent to def double(x): return x*2
get_name = lambda p: p["name"]
print(double(7))            # 14
print(get_name(products[0])) # Laptop

# ── map: transform every item ──
# Apply 15% GST to all prices
prices_with_gst = list(map(
    lambda p: {**p, "price_gst": round(p["price"] * 1.18, 2)},
    products
))
print("\nPrices with 18% GST:")
for p in prices_with_gst:
    print(f"  {p['name']}: ₹{p['price_gst']}")

# ── filter: keep only matching items ──
# Only highly-rated products (≥ 4.5)
top_rated = list(filter(
    lambda p: p["rating"] >= 4.5,
    products
))
print("\nTop rated products (≥4.5):")
for p in top_rated:
    print(f"  {p['name']} — {p['rating']}")

# ── reduce: collapse to a single value ──
# Sum of all prices
total_revenue = reduce(lambda acc, p: acc + p["price"], products, 0)
print(f"\nTotal catalogue value: ₹{total_revenue}")

# ── Sorting with lambda ──
# Sort by price (lowest first)
sorted_by_price = sorted(products, key=lambda p: p["price"])
print("\nSorted by price:")
for p in sorted_by_price:
    print(f"  {p['name']}: ₹{p['price']}")