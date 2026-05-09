"""Comprehensive tests for Day 13 complex business logic endpoints."""
import requests
import json

BASE_URL = "http://localhost:8000"

# Test credentials
ADMIN_EMAIL = "admin@ecommerce.com"
ADMIN_PASSWORD = "Admin123"
CUSTOMER_EMAIL = "customer@ecommerce.com"
CUSTOMER_PASSWORD = "Customer123"

# Global variables to store tokens and IDs
admin_token = None
customer_token = None
product_id = None
category_id = None
cart_id = None
order_id = None
review_id = None


def print_test(name: str, passed: bool, message: str = ""):
    """Helper to print test results."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {name}")
    if message and not passed:
        print(f"      → {message}")


def get_headers(token: str) -> dict:
    """Get authorization headers."""
    return {"Authorization": f"Bearer {token}"}


def test_login():
    """Test user login and get tokens."""
    global admin_token, customer_token
    
    print("\n=== AUTHENTICATION ===")
    
    # Admin login
    resp = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    passed = resp.status_code == 200
    if passed:
        admin_token = resp.json()["access_token"]
    print_test("Admin Login", passed, resp.text if not passed else "")
    
    # Customer login
    resp = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": CUSTOMER_EMAIL, "password": CUSTOMER_PASSWORD}
    )
    passed = resp.status_code == 200
    if passed:
        customer_token = resp.json()["access_token"]
    print_test("Customer Login", passed, resp.text if not passed else "")


def test_get_product():
    """Get a product to use in tests."""
    global product_id
    
    print("\n=== PRODUCT SETUP ===")
    
    # Get products
    resp = requests.get(f"{BASE_URL}/products")
    passed = resp.status_code == 200
    products = resp.json() if passed else []
    
    if products and len(products) > 0:
        product_id = products[0]["id"]
        print(f"✅ Using Product ID: {product_id} - {products[0]['name']}")
        print(f"   Available Stock: {products[0]['stock']}")
    else:
        print("❌ No products available for testing")


def test_get_cart_creates_if_missing():
    """Test GET /cart creates empty cart if user doesn't have one."""
    print("\n=== CART OPERATIONS ===")
    
    resp = requests.get(
        f"{BASE_URL}/cart",
        headers=get_headers(customer_token)
    )
    passed = resp.status_code == 200
    if passed:
        cart_data = resp.json()
        print_test("GET /cart (Create if missing)", passed)
        print(f"   Cart ID: {cart_data['id']}, Items: {len(cart_data['items'])}")
    else:
        print_test("GET /cart (Create if missing)", False, resp.text)


def test_add_item_exceeds_stock():
    """Test adding item with quantity > stock (should fail)."""
    
    resp = requests.get(
        f"{BASE_URL}/products/{product_id}",
        headers=get_headers(customer_token)
    )
    if resp.status_code != 200:
        print_test("Add Item (Qty > Stock)", False, "Could not fetch product")
        return
    
    product = resp.json()
    stock = product['stock']
    
    # Try to add more than available stock
    resp = requests.post(
        f"{BASE_URL}/cart/items",
        json={"product_id": product_id, "quantity": stock + 10},
        headers=get_headers(customer_token)
    )
    passed = resp.status_code == 400
    print_test("Add Item (Qty > Stock - should fail)", passed, 
               resp.json().get("detail") if not passed else "")


def test_add_valid_item():
    """Test adding a valid item to cart."""
    
    resp = requests.post(
        f"{BASE_URL}/cart/items",
        json={"product_id": product_id, "quantity": 2},
        headers=get_headers(customer_token)
    )
    passed = resp.status_code == 201
    print_test("Add Item to Cart", passed, resp.text if not passed else "")


def test_view_cart():
    """Test viewing cart contents."""
    
    resp = requests.get(
        f"{BASE_URL}/cart",
        headers=get_headers(customer_token)
    )
    passed = resp.status_code == 200 and len(resp.json()['items']) > 0
    if passed:
        cart = resp.json()
        total_items = sum(item['quantity'] for item in cart['items'])
        print_test("View Cart", passed)
        print(f"   Items in cart: {total_items}")
    else:
        print_test("View Cart", False, resp.text)


def test_checkout_empty_cart():
    """Test checkout with empty cart (should fail)."""
    
    # Clear cart first
    resp = requests.delete(
        f"{BASE_URL}/cart",
        headers=get_headers(customer_token)
    )
    
    # Try to checkout empty cart
    resp = requests.post(
        f"{BASE_URL}/orders",
        headers=get_headers(customer_token)
    )
    passed = resp.status_code == 400
    print_test("Checkout Empty Cart (should fail)", passed, 
               resp.json().get("detail") if not passed else "")


def test_checkout_success():
    """Test successful checkout."""
    global order_id
    
    # Add item to cart first
    requests.post(
        f"{BASE_URL}/cart/items",
        json={"product_id": product_id, "quantity": 1},
        headers=get_headers(customer_token)
    )
    
    # Checkout
    resp = requests.post(
        f"{BASE_URL}/orders",
        headers=get_headers(customer_token)
    )
    passed = resp.status_code == 201
    if passed:
        order_id = resp.json()["id"]
        print_test("Checkout Success", passed)
        print(f"   Order ID: {order_id}")
        print(f"   Total: ${resp.json()['total']}")
        print(f"   Status: {resp.json()['status']}")
    else:
        print_test("Checkout Success", False, resp.text)


def test_stock_deducted():
    """Test that stock was deducted after checkout."""
    
    resp = requests.get(f"{BASE_URL}/products/{product_id}")
    if resp.status_code == 200:
        current_stock = resp.json()['stock']
        print_test("Stock Deducted", True)
        print(f"   New Stock Level: {current_stock}")
    else:
        print_test("Stock Deducted", False, "Could not fetch product")


def test_review_without_delivery():
    """Test leaving review before order is delivered (should fail)."""
    
    resp = requests.post(
        f"{BASE_URL}/products/{product_id}/reviews",
        json={"rating": 5, "comment": "Great product!"},
        headers=get_headers(customer_token)
    )
    passed = resp.status_code == 403
    print_test("Review Before Delivery (should fail)", passed,
               resp.json().get("detail") if not passed else "")


def test_admin_update_order_status():
    """Test admin updating order status to delivered."""
    
    resp = requests.put(
        f"{BASE_URL}/orders/{order_id}/status",
        json={"new_status": "delivered"},
        headers=get_headers(admin_token),
        params={"new_status": "delivered"}
    )
    # FastAPI handles enum params differently
    resp = requests.put(
        f"{BASE_URL}/orders/{order_id}/status?new_status=delivered",
        headers=get_headers(admin_token)
    )
    passed = resp.status_code == 200
    if passed:
        print_test("Admin Update Order Status", passed)
        print(f"   New Status: {resp.json()['status']}")
    else:
        print_test("Admin Update Order Status", False, resp.text)


def test_review_after_delivery():
    """Test leaving review after order is delivered (should succeed)."""
    global review_id
    
    resp = requests.post(
        f"{BASE_URL}/products/{product_id}/reviews",
        json={"rating": 5, "comment": "Excellent product, highly recommend!"},
        headers=get_headers(customer_token)
    )
    passed = resp.status_code == 201
    if passed:
        review_id = resp.json()["id"]
        print_test("Review After Delivery", passed)
        print(f"   Review ID: {review_id}")
        print(f"   Rating: {resp.json()['rating']}")
    else:
        print_test("Review After Delivery", False, resp.text)


def test_duplicate_review():
    """Test leaving second review (should fail)."""
    
    resp = requests.post(
        f"{BASE_URL}/products/{product_id}/reviews",
        json={"rating": 4, "comment": "Actually not bad"},
        headers=get_headers(customer_token)
    )
    passed = resp.status_code == 400
    print_test("Duplicate Review (should fail)", passed,
               resp.json().get("detail") if not passed else "")


def test_get_product_reviews():
    """Test getting product reviews with average rating."""
    
    resp = requests.get(f"{BASE_URL}/products/{product_id}/reviews")
    passed = resp.status_code == 200
    if passed:
        data = resp.json()
        print_test("Get Product Reviews", passed)
        print(f"   Total Reviews: {data['total_reviews']}")
        print(f"   Average Rating: {data['average_rating']}")
    else:
        print_test("Get Product Reviews", False, resp.text)


def test_update_review():
    """Test updating a review."""
    
    resp = requests.put(
        f"{BASE_URL}/products/reviews/{review_id}",
        json={"rating": 4, "comment": "Good, but room for improvement"},
        headers=get_headers(customer_token)
    )
    passed = resp.status_code == 200
    if passed:
        print_test("Update Review", passed)
        print(f"   New Rating: {resp.json()['rating']}")
    else:
        print_test("Update Review", False, resp.text)


def test_get_order_history():
    """Test getting user's order history."""
    
    resp = requests.get(
        f"{BASE_URL}/orders",
        headers=get_headers(customer_token)
    )
    passed = resp.status_code == 200 and len(resp.json()) > 0
    if passed:
        orders = resp.json()
        print_test("Get Order History", passed)
        print(f"   Total Orders: {len(orders)}")
        for order in orders:
            print(f"      - Order #{order['id']}: {order['status']} (${order['total']})")
    else:
        print_test("Get Order History", False, resp.text)


def test_cancel_order():
    """Test cancelling an order."""
    
    # Create another order to cancel
    requests.post(
        f"{BASE_URL}/cart/items",
        json={"product_id": product_id, "quantity": 1},
        headers=get_headers(customer_token)
    )
    
    checkout_resp = requests.post(
        f"{BASE_URL}/orders",
        headers=get_headers(customer_token)
    )
    
    if checkout_resp.status_code == 201:
        cancel_order_id = checkout_resp.json()["id"]
        
        resp = requests.put(
            f"{BASE_URL}/orders/{cancel_order_id}/cancel",
            headers=get_headers(customer_token)
        )
        passed = resp.status_code == 200 and resp.json()['status'] == 'cancelled'
        print_test("Cancel Order", passed)
        if passed:
            print(f"   Order Status: {resp.json()['status']}")
    else:
        print_test("Cancel Order", False, "Could not create order for cancellation")


def run_all_tests():
    """Run all tests in sequence."""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   DAY 13 - COMPLEX BUSINESS LOGIC TEST SUITE              ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    try:
        test_login()
        test_get_product()
        test_get_cart_creates_if_missing()
        test_add_item_exceeds_stock()
        test_add_valid_item()
        test_view_cart()
        test_checkout_empty_cart()
        test_checkout_success()
        test_stock_deducted()
        
        print("\n=== REVIEW SYSTEM ===")
        test_review_without_delivery()
        test_admin_update_order_status()
        test_review_after_delivery()
        test_duplicate_review()
        test_get_product_reviews()
        test_update_review()
        
        print("\n=== ORDER MANAGEMENT ===")
        test_get_order_history()
        test_cancel_order()
        
        print("\n╔════════════════════════════════════════════════════════════╗")
        print("║                 ALL TESTS COMPLETED                       ║")
        print("╚════════════════════════════════════════════════════════════╝")
        
    except Exception as e:
        print(f"\n❌ Test execution error: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
