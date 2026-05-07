# E-Commerce REST API 🛒

A comprehensive, scalable RESTful API built with FastAPI and PostgreSQL to power backend e-commerce operations. 

## 📋 Project Overview
This project serves as the backend for an e-commerce platform. It handles user authentication, product catalog management, shopping cart sessions, secure order processing, and customer reviews. 

### Core Features
* **Role-Based Authentication:** Secure JWT-based registration and login system (Admin vs. User).
* **Product Catalog:** Admin capabilities to manage products and categories.
* **Shopping Cart:** Session-based cart system to manage items before checkout.
* **Order Processing:** Checkout flow that converts cart items into permanent, trackable order records.
* **Social Proof:** A review and rating system tied to specific products.

---

## 🏗️ Project Structure
```text
app/
├── auth/       # JWT security, password hashing, and token generation
├── database/   # DB connection setup and session management
├── models/     # SQLAlchemy ORM models (Database tables)
├── routers/    # FastAPI route definitions (Endpoints)
├── schemas/    # Pydantic models (Data validation)
└── utils/      # Helper functions and external services
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

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd Day-11-13
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up Environment Variables**
Create a `.env` file in the root directory and add the following:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_db
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**5. Initialize the Database**
Run the `schema.sql` script in your PostgreSQL database to create the necessary tables.

**6. Run the Development Server**
```bash
uvicorn app.main:app --reload
```
Navigate to `http://localhost:8000/docs` to view the interactive Swagger UI.
