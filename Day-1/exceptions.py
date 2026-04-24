# ── Part 1: Custom exception classes ──
class AppError(Exception):
    """Base exception for our entire application."""
    pass

class UserNotFoundError(AppError):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"No user found with id={user_id}")

class InsufficientStockError(AppError):
    def __init__(self, item: str, need: int, have: int) -> None:
        super().__init__(f"{item}: need {need} but only {have} in stock")

class InvalidPriceError(AppError):
    def __init__(self, value: float) -> None:
        super().__init__(f"Price {value} is invalid — must be > 0")


# ── Part 2: try / except / else / finally ──
USER_DB = {1: "Aravind", 2: "Priya"}
STOCK   = {"Laptop": 3, "Phone": 0}

def place_order(user_id: int, item: str, qty: int) -> str:
    try:
        # Step 1: Check user exists
        if user_id not in USER_DB:
            raise UserNotFoundError(user_id)

        # Step 2: Check stock
        available = STOCK.get(item, 0)
        if available < qty:
            raise InsufficientStockError(item, qty, available)

        # Step 3: Place order
        STOCK[item] -= qty
        result = f"Order placed for {USER_DB[user_id]}: {qty}x {item}"

    except UserNotFoundError as e:
        print(f"[USER ERROR] {e}")
        result = "Order failed: user not found"

    except InsufficientStockError as e:
        print(f"[STOCK ERROR] {e}")
        result = "Order failed: insufficient stock"

    except Exception as e:          # safety net for unexpected errors
        print(f"[UNKNOWN ERROR] {e}")
        result = "Order failed: unknown error"

    else:
        print(f"[SUCCESS] {result}")   # runs ONLY if no exception

    finally:
        print("[LOG] Order attempt recorded.\n")  # ALWAYS runs

    return result


# Test all three scenarios
place_order(1, "Laptop", 2)   # success
place_order(99, "Laptop", 1)  # user not found
place_order(2, "Phone", 3)   # insufficient stock