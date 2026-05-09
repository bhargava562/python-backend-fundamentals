# E-Commerce REST API 🛒

A comprehensive, production-ready RESTful API built with FastAPI and PostgreSQL for e-commerce backend operations.

## 📋 Project Overview

This project demonstrates building a scalable e-commerce backend with:
- **JWT-based Authentication** - Secure user registration and login with role-based access control
- **Product Management** - Admin features for managing products and categories
- **Shopping Cart** - Session-based cart system with add/remove functionality
- **Order Processing** - Complete checkout flow from cart to order
- **Reviews System** - Product ratings and reviews from customers

---

## 🎬 Workflow Demo

<video src="docs/workflow.mp4" controls width="100%">
  <a href="docs/workflow.mp4">Watch the workflow demo</a>
</video>

> Full walkthrough: Register → Browse → Add to Cart → Checkout → Review

---

## 📚 Documentation

All documentation is organized in the [`docs/`](docs/) directory for easy access and maintenance.

**Quick Links**:
- 📖 [Documentation Index](docs/INDEX.md) - Complete guide to all documentation files
- ✅ [Implementation Checklist](docs/IMPLEMENTATION_CHECKLIST.md) - Feature status and deliverables
- 🔐 [File Organization & Security](docs/FILE_ORGANIZATION.md) - Best practices and guidelines
- 📝 [Organization Summary](docs/ORGANIZATION_SUMMARY.md) - Changes and improvements made
- 🗄️ [PostgreSQL Connection Guide](docs/POSTGRES_CONNECTION.md) - Database setup and troubleshooting

**Start here**: Read [docs/INDEX.md](docs/INDEX.md) for documentation navigation and quick answers.

---

## 🏗️ Project Structure

```text
Day-11-13/
├── app/                      # Main application package
│   ├── __init__.py
│   ├── main.py               # FastAPI app factory & router setup
│   ├── auth/                 # Authentication & security
│   │   ├── __init__.py
│   │   └── security.py       # JWT, password hashing, role-based access
│   ├── database/             # Database configuration
│   │   ├── __init__.py
│   │   └── config.py         # Engine, session management
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   └── models.py         # 8 database entity definitions
│   ├── routers/              # API endpoint definitions
│   │   ├── __init__.py
│   │   ├── auth_routes.py    # Register, login endpoints
│   │   ├── categories_routes.py  # Category CRUD
│   │   └── products_routes.py    # Product CRUD + search/filter
│   ├── schemas/              # Pydantic validation models
│   │   ├── __init__.py
│   │   └── schemas.py        # Input/output validation
│   └── utils/                # Helper utilities
│       ├── __init__.py
│       └── seed.py           # Database seeding script
│
├── tests/                    # 🆕 Test Suite
│   ├── __init__.py
│   └── test_db_connection.py # Database connection & schema verification
│
├── postman/                  # API testing collection
│   └── Day12_API_Collection.json
│
├── docs/                     # 🆕 Documentation Hub
│   ├── INDEX.md              # Documentation index & navigation
│   ├── IMPLEMENTATION_CHECKLIST.md  # Feature checklist & status
│   ├── FILE_ORGANIZATION.md  # File organization & security guide
│   ├── ORGANIZATION_SUMMARY.md      # Changes summary & improvements
│   └── POSTGRES_CONNECTION.md      # PostgreSQL setup & troubleshooting
│
├── Configuration Files
│   ├── .env.example          # Environment template (safe to commit) ✅
│   ├── .env                  # Local environment (in .gitignore - DO NOT commit) 🔒
│   ├── .gitignore            # Git ignore patterns
│   └── requirements.txt      # Python dependencies (with pinned versions)
│
├── Database & Schema
│   └── schema.sql            # PostgreSQL schema SQL file
│
├── Documentation
│   └── README.md             # This file - setup & API documentation
│
└── Utility Scripts
    ├── seed_postgres.py      # Alternative database seeding script
    └── venv/                 # Virtual environment (in .gitignore)

Key Files Organized:
  ✓ Test files moved to /tests directory
  ✓ Secrets handled securely (.env in .gitignore)
  ✓ Configuration templates available (.env.example)
  ✓ All documentation consolidated
```

---

## � Database ERD

```mermaid
erDiagram
    USERS ||--o{ ORDERS : places
    USERS ||--o{ REVIEWS : writes
    USERS ||--o| CART : owns
    CATEGORIES ||--o{ PRODUCTS : contains
    PRODUCTS ||--o{ REVIEWS : receives
    PRODUCTS ||--o{ CART_ITEMS : added_to
    PRODUCTS ||--o{ ORDER_ITEMS : part_of
    CART ||--o{ CART_ITEMS : holds
    ORDERS ||--o{ ORDER_ITEMS : includes

    USERS {
        int id PK
        string username
        string email
        string password
        string role
        timestamp created_at
    }
    CATEGORIES {
        int id PK
        string name
        text description
    }
    PRODUCTS {
        int id PK
        string name
        text description
        float price
        int stock
        int category_id FK
        timestamp created_at
    }
    CART {
        int id PK
        int user_id FK
        timestamp created_at
    }
    CART_ITEMS {
        int id PK
        int cart_id FK
        int product_id FK
        int quantity
    }
    ORDERS {
        int id PK
        int user_id FK
        float total
        string status
        timestamp created_at
    }
    ORDER_ITEMS {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        float price
    }
    REVIEWS {
        int id PK
        int user_id FK
        int product_id FK
        int rating
        text comment
        timestamp created_at
    }
```

---

## 🛣️ API Endpoint Specification

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| **Authentication** |
| POST | `/auth/register` | Register a new user | ❌ Public |
| POST | `/auth/login` | Login and receive JWT token | ❌ Public |
| **Categories** |
| GET | `/categories` | List all categories | ❌ Public |
| GET | `/categories/{id}` | Get category by ID | ❌ Public |
| GET | `/categories/{id}/products` | Get products in category | ❌ Public |
| POST | `/categories` | Create category | 👨‍💼 Admin |
| PUT | `/categories/{id}` | Update category | 👨‍💼 Admin |
| DELETE | `/categories/{id}` | Delete category | 👨‍💼 Admin |
| **Products** |
| GET | `/products` | List all products (with search/filter/sort) | ❌ Public |
| GET | `/products/{id}` | Get product details | ❌ Public |
| POST | `/products` | Create product | 👨‍💼 Admin |
| PUT | `/products/{id}` | Update product | 👨‍💼 Admin |
| DELETE | `/products/{id}` | Delete product | 👨‍💼 Admin |
| **Shopping Cart** |
| GET | `/cart` | View user's cart (auto-creates if missing) | 👤 User |
| POST | `/cart/items` | Add item to cart | 👤 User |
| PUT | `/cart/items/{id}` | Update item quantity | 👤 User |
| DELETE | `/cart/items/{id}` | Remove item from cart | 👤 User |
| DELETE | `/cart` | Clear entire cart | 👤 User |
| **Orders** |
| POST | `/orders` | **Checkout & create order** *(ACID Transaction)* | 👤 User |
| GET | `/orders` | Get user's order history | 👤 User |
| PUT | `/orders/{id}/status` | Update order status | 👨‍💼 Admin |
| PUT | `/orders/{id}/cancel` | Cancel pending order (restore stock) | 👤 User |
| **Reviews** |
| GET | `/products/{id}/reviews` | Get reviews & avg rating | ❌ Public |
| POST | `/products/{id}/reviews` | Create review *(Purchase verified)* | 👤 User |
| PUT | `/reviews/{id}` | Update review | 👤 User (owner) |
| DELETE | `/reviews/{id}` | Delete review | 👤 User (owner) |

---

## 🆕 Day 13: Advanced Business Logic Features

### 1. Shopping Cart API
Manages user shopping sessions with stock validation and cart management.

**Endpoints:**

#### `GET /cart` - View Shopping Cart
- **Authorization:** User (requires JWT token)
- **Auto-creates:** Empty cart if user doesn't have one
- **Response:** Cart object with items array
```json
{
  "id": 1,
  "user_id": 5,
  "created_at": "2024-01-15T10:30:00",
  "items": [
    {
      "id": 1,
      "product_id": 3,
      "product_name": "Laptop",
      "quantity": 2,
      "price": 999.99
    }
  ]
}
```

#### `POST /cart/items` - Add Product to Cart
- **Authorization:** User
- **Validation:**
  - Product must exist (404 if not)
  - **Stock check:** quantity <= available stock (400 if insufficient)
  - If product already in cart, quantity is updated
- **Request:**
```json
{
  "product_id": 3,
  "quantity": 2
}
```
- **Response:** 201 Created with updated CartItem

#### `PUT /cart/items/{id}` - Update Item Quantity
- **Authorization:** User
- **Validation:** Quantity > 0 and <= available stock
- **Auto-delete:** If quantity set to 0, item is removed
- **Request:**
```json
{
  "quantity": 3
}
```

#### `DELETE /cart/items/{id}` - Remove Item
- **Authorization:** User
- **Response:** 204 No Content

#### `DELETE /cart` - Clear Entire Cart
- **Authorization:** User
- **Response:** 204 No Content

---

### 2. Order Management with ACID Transactions
Implements production-grade checkout with atomic transactions and inventory management.

**Key Features:**
- 🔒 **ACID Compliance:** All-or-nothing checkout (no partial orders)
- 📦 **Inventory Safety:** Stock deducted only on successful checkout
- 💰 **Price Snapshot:** Historical prices stored with OrderItems
- 🛡️ **Authorization:** Order ownership verification for status/cancel

**Transaction Flow:**
```
User Checkout Request
    ↓
BEGIN TRANSACTION
    ↓
Validate cart not empty
    ↓
Validate ALL products exist & stock sufficient
    ↓
Deduct stock from each product
    ↓
Calculate total from current prices
    ↓
Create Order & OrderItems with price snapshot
    ↓
Delete all CartItems
    ↓
COMMIT ✅
    ↓
Return OrderResponse

If ANY error: ROLLBACK ↩️
→ Cart unchanged
→ Stock unchanged
→ No Order created
```

**Endpoints:**

#### `POST /orders` - Checkout (Create Order)
- **Authorization:** User
- **Validation Steps:**
  1. Cart must have items (400 if empty)
  2. **Transaction:** Check all products in stock
  3. **Transaction:** Deduct stock
  4. **Transaction:** Create order with items
  5. **Transaction:** Clear cart
  6. All-or-nothing: Rollback on ANY failure
- **Error Responses:**
  - `400 Bad Request`: Empty cart or out of stock
  - `500 Internal Server Error`: Database error (stock unchanged)
- **Success Response:** 201 Created
```json
{
  "id": 1,
  "user_id": 5,
  "total": 2499.99,
  "status": "pending",
  "created_at": "2024-01-15T11:00:00",
  "items": [
    {
      "id": 1,
      "product_id": 3,
      "quantity": 2,
      "price": 999.99
    }
  ]
}
```

#### `GET /orders` - Order History
- **Authorization:** User (sees only own orders)
- **Query Parameters:**
  - `skip`: Offset for pagination (default: 0)
  - `limit`: Results per page (default: 10)
  - `status`: Filter by status (optional: "pending", "shipped", "delivered", "cancelled")
- **Response:** Array of OrderResponse objects
```bash
curl "http://localhost:8000/orders?skip=0&limit=10&status=delivered" \
  -H "Authorization: Bearer {token}"
```

#### `PUT /orders/{id}/status` - Update Order Status
- **Authorization:** Admin only
- **Valid Transitions:** pending → shipped → delivered
- **Request:**
```json
{
  "new_status": "delivered"
}
```
- **Error Responses:**
  - `403 Forbidden`: Not admin
  - `404 Not Found`: Order doesn't exist
  - `400 Bad Request`: Invalid status transition

#### `PUT /orders/{id}/cancel` - Cancel Order
- **Authorization:** User (must own order)
- **Restrictions:** Only "pending" orders can be cancelled
- **Automatic Stock Restoration:** All products' stock is restored
- **Response:** 200 OK with updated status "cancelled"
- **Error Responses:**
  - `403 Forbidden`: Not order owner OR order already shipped/delivered
  - `404 Not Found`: Order doesn't exist

---

### 3. Review System with Purchase Verification
Implements verified reviews system ensuring only buyers can review products.

**Key Features:**
- ✅ **Purchase Verification:** Must have delivered order with product
- ⭐ **Rating System:** 1-5 star ratings (enforced)
- 🧮 **Average Calculation:** Automatic average rating per product
- 🔒 **Ownership Protection:** Users can only edit/delete own reviews
- 🚫 **Duplicate Prevention:** One review per user per product

**Endpoints:**

#### `POST /products/{id}/reviews` - Create Review
- **Authorization:** User (requires JWT token)
- **Complex Validation:**
  1. **Purchase Verification:** Query database for OrderItems where:
     - Order belongs to current user
     - Order status is "delivered"
     - OrderItem contains product_id
     - If not found → 403 Forbidden
  2. **Uniqueness Check:** Verify no existing review (user_id, product_id)
     - If exists → 400 Bad Request
  3. **Rating Validation:** 1 <= rating <= 5
- **Request:**
```json
{
  "rating": 5,
  "comment": "Excellent product, highly recommend!"
}
```
- **Response:** 201 Created
```json
{
  "id": 1,
  "user_id": 5,
  "product_id": 3,
  "rating": 5,
  "comment": "Excellent product, highly recommend!",
  "created_at": "2024-01-15T12:00:00"
}
```

#### `GET /products/{id}/reviews` - Get Product Reviews
- **Authorization:** Public (no auth required)
- **Query Parameters:**
  - `skip`: Offset (default: 0)
  - `limit`: Per page (default: 10)
- **Response:** Reviews list + calculated average rating
```json
{
  "total_reviews": 5,
  "average_rating": 4.6,
  "reviews": [
    {
      "id": 1,
      "user_id": 5,
      "product_id": 3,
      "rating": 5,
      "comment": "Great!",
      "created_at": "2024-01-15T12:00:00"
    }
  ]
}
```

#### `PUT /reviews/{id}` - Update Review
- **Authorization:** User (must be review owner)
- **Restrictions:** Can only update own review
- **Request:**
```json
{
  "rating": 4,
  "comment": "Good, but room for improvement"
}
```
- **Response:** 200 OK with updated review
- **Error Responses:**
  - `403 Forbidden`: Not review owner
  - `404 Not Found`: Review doesn't exist

#### `DELETE /reviews/{id}` - Delete Review
- **Authorization:** User (must be review owner)
- **Response:** 204 No Content
- **Error Responses:**
  - `403 Forbidden`: Not review owner
  - `404 Not Found`: Review doesn't exist

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- PostgreSQL 12+ (or use SQLite for local development)
- Postman (for API testing)

### Installation Steps

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd Day-11-13
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up Environment Variables**
Create a `.env` file in the root directory and add the following:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_db
SECRET_KEY=your_super_secret_key_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**For local development (SQLite), use:**
```env
DATABASE_URL=sqlite:///./ecommerce.db
SECRET_KEY=dev-secret-key-not-for-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**5. Seed the Database**
```bash
python -m app.utils.seed
```

This will:
- Create all database tables
- Add an admin user (admin@ecommerce.com / Admin123)
- Add a customer user (customer@ecommerce.com / Customer123)
- Populate sample categories and products

**6. Run the Development Server**
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

---

## 🧪 Testing the API

### Interactive API Documentation
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Using Postman

1. **Import the collection:**
   - Open Postman
   - Click **Import** → Select `postman/Day12_API_Collection.json`

2. **Set environment variables:**
   - Click the settings icon → **Manage Environments**
   - Create a new environment and set:
     - `base_url`: `http://localhost:8000`
     - `jwt_token`: (will be auto-populated after login)

3. **Test the endpoints:**
   - Start with **Login** to get a JWT token
   - Token will automatically be saved to `{{jwt_token}}`
   - Use token for protected endpoints (Create/Update/Delete)

### Example API Calls

**Login (get JWT token):**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ecommerce.com","password":"Admin123"}'
```

**List Products:**
```bash
curl "http://localhost:8000/products?skip=0&limit=10"
```

**Search Products:**
```bash
curl "http://localhost:8000/products?search=laptop&skip=0&limit=10"
```

**Create Product (admin only):**
```bash
curl -X POST "http://localhost:8000/products" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Keyboard",
    "description":"Mechanical keyboard",
    "price":89.99,
    "stock":50,
    "category_id":1
  }'
```

---

## 📚 API Implementation Summary

### ✅ Completed Components

1. **Database Models**
   - User, Category, Product, Cart, CartItem, Order, OrderItem, Review
   - Foreign keys and relationships
   - Constraints (price > 0, stock >= 0, unique product names per category, rating 1-5)
   - CheckConstraints and unique constraints for data integrity
   - Cascade/restrict delete policies

2. **Authentication System**
   - User registration with password validation
   - Login with JWT token generation
   - Password hashing with bcrypt
   - Protected routes with Bearer token authentication
   - Role-based access (admin, customer)
   - Security functions: `hash_password()`, `verify_password()`, `create_access_token()`

3. **Products API**
   - Create product (admin only)
   - List products with pagination
   - Get single product by ID
   - Update product (admin only)
   - Delete product (admin only)
   - Search by name/description (case-insensitive)
   - Filter by category, price range
   - Sort by price, name, or date

4. **Categories API**
   - Create category (admin only)
   - List all categories
   - Get products by category
   - Update category (admin only)
   - Delete category (admin only)

5. **Shopping Cart API** ✨ **NEW**
   - Session-based cart management
   - Auto-create cart on first access (unique per user)
   - Add/update/remove items with stock validation
   - Prevents overselling (quantity > stock → 400 error)
   - Clear entire cart
   - Update quantity (auto-delete if qty = 0)

6. **Order Management with ACID Transactions** ✨ **NEW**
   - **All-or-nothing checkout:** Complete transaction atomicity
   - Stock validation before purchase
   - Automatic inventory deduction
   - Price snapshot (historical prices in OrderItems)
   - Order status workflow: pending → shipped → delivered
   - User can cancel pending orders (stock restored)
   - Admin can update order status
   - Rollback on ANY error (stock, order, cart all unchanged)
   - Order history with filtering and pagination

7. **Review System with Purchase Verification** ✨ **NEW**
   - **Purchase Verification:** Only delivered order customers can review
   - Database query validation for purchase authenticity
   - One review per user per product (unique constraint)
   - Rating validation (1-5 stars enforced)
   - Auto-calculate average rating per product
   - Ownership protection (users can only edit/delete own reviews)
   - Optional comment field
   - Public reviews endpoint with pagination

8. **Error Handling**
   - Validation errors (400 Bad Request)
   - Unauthorized access (401 Unauthorized)
   - Admin-only access (403 Forbidden)
   - Not found errors (404 Not Found)
   - Database error handling with transaction rollback
   - Purchase verification failures
   - Stock insufficiency errors

9. **Testing & Documentation**
   - Postman collection with all endpoints
   - Auto-save JWT token in Postman
   - Seed script with test data
   - Swagger/OpenAPI documentation
   - Python test suite (`tests/test_day13_complex_logic.py`) with 18+ test scenarios

---

## 🧪 Day 13: Testing Advanced Features

### Running the Comprehensive Test Suite

A complete test suite for all Day 13 features has been created at [`tests/test_day13_complex_logic.py`](tests/test_day13_complex_logic.py).

**Run the tests:**
```bash
# Make sure the server is running:
# uvicorn app.main:app --reload

# In another terminal, run the test suite:
python tests/test_day13_complex_logic.py
```

### Test Coverage

The test suite verifies all critical business logic:

#### 1. Authentication
- ✅ Admin login
- ✅ Customer login

#### 2. Shopping Cart Operations
- ✅ Auto-create cart on first access
- ✅ Add item to cart
- ✅ Reject quantity > available stock
- ✅ View cart contents
- ✅ Stock tracking

#### 3. Transaction Safety (ACID)
- ✅ **Empty cart checkout** → 400 error (cart still has items)
- ✅ **Insufficient stock** → 400 error (all stock unchanged)
- ✅ **Successful checkout**:
  - Cart becomes empty
  - Stock decreases
  - Order created with status "pending"
  - OrderItems have price snapshot
- ✅ **Failed checkout** → ROLLBACK:
  - Cart untouched
  - Stock unchanged
  - No Order created

#### 4. Order Management
- ✅ Create order (successful checkout)
- ✅ Get order history with pagination
- ✅ Admin updates order status (pending → shipped → delivered)
- ✅ Cancel pending order (stock restored)
- ✅ Cannot cancel shipped/delivered orders

#### 5. Review System (Purchase Verification)
- ✅ **Cannot review before delivery** → 403 Forbidden
- ✅ **Cannot review without purchase** → 403 Forbidden
- ✅ **Review after delivery** → 201 Created
- ✅ **Duplicate review prevention** → 400 Bad Request
- ✅ **Update own review** → 200 OK
- ✅ **Cannot update others' reviews** → 403 Forbidden
- ✅ **Average rating calculation**
- ✅ **Delete own review** → 204 No Content

### Manual Testing Workflow

**Test Scenario: Complete Customer Journey**

```bash
# 1. Start the server
uvicorn app.main:app --reload

# 2. Login as customer
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"customer@ecommerce.com","password":"Customer123"}' \
  | jq -r '.access_token' > token.txt

TOKEN=$(cat token.txt)

# 3. Get initial stock
curl "http://localhost:8000/products/1" | jq '.stock'

# 4. View empty cart
curl "http://localhost:8000/cart" \
  -H "Authorization: Bearer $TOKEN" | jq

# 5. Add item to cart
curl -X POST "http://localhost:8000/cart/items" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'

# 6. View cart with items
curl "http://localhost:8000/cart" \
  -H "Authorization: Bearer $TOKEN" | jq

# 7. Checkout (create order)
curl -X POST "http://localhost:8000/orders" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  | jq '.id' > order_id.txt

ORDER_ID=$(cat order_id.txt)

# 8. Verify stock decreased
curl "http://localhost:8000/products/1" | jq '.stock'

# 9. Verify cart is empty
curl "http://localhost:8000/cart" \
  -H "Authorization: Bearer $TOKEN" | jq '.items'

# 10. Try to review (should fail - order still pending)
curl -X POST "http://localhost:8000/products/1/reviews" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "comment": "Great product!"}' \
  | jq '.detail'

# 11. Login as admin and update order status
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ecommerce.com","password":"Admin123"}' \
  | jq -r '.access_token' > admin_token.txt

ADMIN_TOKEN=$(cat admin_token.txt)

curl -X PUT "http://localhost:8000/orders/$ORDER_ID/status?new_status=delivered" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq '.status'

# 12. Now try to review (should succeed)
curl -X POST "http://localhost:8000/products/1/reviews" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "comment": "Excellent product, highly recommend!"}' \
  | jq

# 13. View product reviews with average rating
curl "http://localhost:8000/products/1/reviews" | jq
```

### Testing Transaction Atomicity

To verify ACID properties, create a test scenario with insufficient stock:

```bash
# Get a product with limited stock
curl "http://localhost:8000/products" | jq '.[] | {id, name, stock}' | grep -A 2 "stock"

# Add quantity that exceeds stock
curl -X POST "http://localhost:8000/cart/items" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 999}' \
  | jq '.detail'  # Should be 400 error

# Verify cart and stock are unchanged
curl "http://localhost:8000/cart" \
  -H "Authorization: Bearer $TOKEN" | jq '.items'

curl "http://localhost:8000/products/1" | jq '.stock'
```

### Testing Authorization

**Admin-only endpoints:**
```bash
# Try to update order status as customer (should fail)
curl -X PUT "http://localhost:8000/orders/1/status?new_status=delivered" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.detail'  # Should be 403 Forbidden
```

**Purchase verification:**
```bash
# Try to review a product without purchasing (should fail)
curl -X POST "http://localhost:8000/products/999/reviews" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "comment": "Fake review"}' \
  | jq '.detail'  # Should be 403 Forbidden
```

---

## 🔐 Security & Data Integrity Features

### Password Security
- Bcrypt hashing with salting
- Never store plain passwords
- Verification on login

### JWT Authentication
- 30-minute token expiry
- Bearer token in Authorization header
- Role-based access control (admin vs customer)

### Database Constraints
- **CheckConstraints:** Product price > 0, stock >= 0, review rating 1-5
- **UniqueConstraints:**
  - User: email, username
  - Category: name
  - Product: name per category
  - CartItem: (cart_id, product_id) - one per product per cart
  - Review: (user_id, product_id) - one per user per product
- **ForeignKeys:** Cascade delete for orphaned items

### ACID Transaction Safety
- All-or-nothing checkout
- No partial orders
- Stock never oversold
- Automatic rollback on error

### Authorization
- User can only see own cart and orders
- Admin-only endpoints protected
- Review ownership verified
- Order ownership verified

---

## 📖 Quick Reference

### Test Credentials
- **Admin:** admin@ecommerce.com / Admin123
- **Customer:** customer@ecommerce.com / Customer123

### API Base URL
```
http://localhost:8000
```

### Key Files
- Models: [`app/models/models.py`](app/models/models.py)
- Schemas: [`app/schemas/schemas.py`](app/schemas/schemas.py)
- Routers: 
  - [`app/routers/auth_routes.py`](app/routers/auth_routes.py)
  - [`app/routers/cart_routes.py`](app/routers/cart_routes.py) (NEW)
  - [`app/routers/orders_routes.py`](app/routers/orders_routes.py) (NEW)
  - [`app/routers/reviews_routes.py`](app/routers/reviews_routes.py) (NEW)
- Tests: [`tests/test_day13_complex_logic.py`](tests/test_day13_complex_logic.py) (NEW)
- Database: [`app/database/config.py`](app/database/config.py)
- Seeds: [`app/utils/seed.py`](app/utils/seed.py)

### Useful Commands
```bash
# Run server with auto-reload
uvicorn app.main:app --reload

# Run test suite
python tests/test_day13_complex_logic.py

# Seed database
python -m app.utils.seed

# View API docs
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

---

## ✨ Key Achievements

✅ **Shopping Cart Management** - Session-based with stock validation
✅ **ACID Transactions** - All-or-nothing checkout with automatic rollback  
✅ **Inventory Management** - No overselling, automatic deduction
✅ **Order Lifecycle** - Full workflow from pending to delivered
✅ **Purchase Verification** - Reviews only from verified buyers
✅ **Role-Based Access** - Admin vs customer permissions
✅ **Comprehensive Error Handling** - Clear error messages and status codes
✅ **Complete Test Coverage** - 18+ scenarios covering all features
✅ **Production-Ready** - Security, data integrity, and scalability

---

**Created with ❤️ for learning e-commerce backend architecture**
