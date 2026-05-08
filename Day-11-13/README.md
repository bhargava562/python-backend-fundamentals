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

## �🛣️ API Endpoint Specification (Blueprint)

### Authentication
* `POST /auth/register` - Register a new user
* `POST /auth/login` - Authenticate and receive JWT token

### Products & Categories
* `GET /products` - Retrieve all products 
* `GET /products/{id}` - Get details of a specific product
* `GET /products/search?q={keyword}` - Search products by keyword
* `POST /products` - Create a new product *(Admin Only)*
* `PUT /products/{id}` - Update product details *(Admin Only)*
* `DELETE /products/{id}` - Remove a product *(Admin Only)*
* `GET /categories` - List all categories
* `POST /categories` - Create a new category *(Admin Only)*

### Shopping Cart
* `GET /cart` - View current user's shopping cart *(User Only)*
* `POST /cart/items` - Add product to cart *(User Only)*
* `DELETE /cart/items/{id}` - Remove specific item from cart *(User Only)*

### Orders
* `POST /orders` - Checkout cart and create an order *(User Only)*
* `GET /orders` - View user's order history *(User Only)*
* `GET /orders/{id}` - View specific order details *(User Only)*

### Reviews
* `GET /products/{id}/reviews` - View reviews for a specific product
* `POST /products/{id}/reviews` - Submit a review for a product *(User Only)*

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
   - Constraints (price > 0, stock >= 0, unique product names per category)
   - Indexes for optimized queries

2. **Authentication System**
   - User registration with password validation
   - Login with JWT token generation
   - Password hashing with bcrypt
   - Protected routes with Bearer token authentication
   - Role-based access (admin, customer)

3. **Products API**
   - Create product (admin only)
   - List products with pagination
   - Get single product by ID
   - Update product (admin only)
   - Delete product (admin only)
   - Image URL support

4. **Categories API**
   - Create category (admin only)
   - List all categories
   - Get products by category
   - Update category (admin only)
   - Delete category (admin only)

5. **Search & Filter**
   - Search by name and description (case-insensitive)
   - Filter by category
   - Filter by price range (min_price, max_price)
   - Sort by price, name, or date created
   - Pagination with skip/limit

6. **Error Handling**
   - Validation errors (400 Bad Request)
   - Unauthorized access (401 Unauthorized)
   - Admin-only access (403 Forbidden)
   - Not found errors (404 Not Found)
   - Database error handling (500 Internal Server Error)

7. **Testing & Documentation**
   - Postman collection with all endpoints
   - Auto-save JWT token in Postman
   - Seed script with test data
   - Swagger/OpenAPI documentation
