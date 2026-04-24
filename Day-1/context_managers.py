import time

# ── Example 1: Built-in file context manager ──
with open("orders.txt", "w") as f:
    f.write("Order #1: Laptop x2\n")
    f.write("Order #2: Phone x1\n")
# File is automatically closed here — even if write() failed!

with open("orders.txt", "r") as f:
    content = f.read()
print("File content:\n", content)


# ── Example 2: Custom context manager class ──
# Must implement __enter__ and __exit__ methods
class Timer:
    def __enter__(self) -> "Timer":
        # SETUP: runs when 'with Timer()' starts
        self.start = time.perf_counter()
        print("Timer started...")
        return self               # this becomes 'as t'

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # CLEANUP: runs when the 'with' block ends
        self.elapsed = time.perf_counter() - self.start
        print(f"Timer stopped. Elapsed: {self.elapsed:.4f}s")
        return False  # False = don't suppress exceptions


class DatabaseConnection:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name

    def __enter__(self) -> "DatabaseConnection":
        print(f"Connecting to {self.db_name}...")
        return self

    def query(self, sql: str) -> str:
        return f"Results for: {sql}"

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        print(f"Closing connection to {self.db_name}.")
        return False


# ── Using the custom context managers ──
with Timer() as t:
    total = sum(i**2 for i in range(500_000))
    print(f"Sum of squares: {total}")

with DatabaseConnection("orders_db") as db:
    result = db.query("SELECT * FROM orders")
    print(result)