# Day 13: API Endpoints Reference

## Quick Endpoint Summary

### 🛒 Shopping Cart (5 endpoints)
```
GET    /cart                      → View user's cart (auto-create)
POST   /cart/items                → Add item to cart
PUT    /cart/items/{id}           → Update item quantity
DELETE /cart/items/{id}           → Remove item from cart
DELETE /cart                      → Clear entire cart
```

### 📦 Orders (4 endpoints)
```
POST   /orders                    → Checkout (ACID transaction)
GET    /orders                    → Get order history
PUT    /orders/{id}/status        → Update status (admin only)
PUT    /orders/{id}/cancel        → Cancel order (user owned)
```

### ⭐ Reviews (4 endpoints)
```
POST   /products/{id}/reviews     → Create review (purchase verified)
GET    /products/{id}/reviews     → Get reviews + average rating
PUT    /reviews/{id}              → Update own review
DELETE /reviews/{id}              → Delete own review
```

---

## All 33 API Endpoints

### Authentication (2)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login & get JWT token |

### Categories (6)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/categories` | List all categories |
| GET | `/categories/{id}` | Get category details |
| GET | `/categories/{id}/products` | Get products in category |
| POST | `/categories` | Create category (admin) |
| PUT | `/categories/{id}` | Update category (admin) |
| DELETE | `/categories/{id}` | Delete category (admin) |

### Products (5)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/products` | List products (search/filter/sort) |
| GET | `/products/{id}` | Get product details |
| POST | `/products` | Create product (admin) |
| PUT | `/products/{id}` | Update product (admin) |
| DELETE | `/products/{id}` | Delete product (admin) |

### Shopping Cart (5) ✨
| Method | Endpoint | Purpose | New |
|--------|----------|---------|-----|
| GET | `/cart` | View cart (auto-create) | ✨ |
| POST | `/cart/items` | Add to cart | ✨ |
| PUT | `/cart/items/{id}` | Update quantity | ✨ |
| DELETE | `/cart/items/{id}` | Remove item | ✨ |
| DELETE | `/cart` | Clear cart | ✨ |

### Orders (4) ✨
| Method | Endpoint | Purpose | New |
|--------|----------|---------|-----|
| POST | `/orders` | Checkout (ACID) | ✨ |
| GET | `/orders` | Order history | ✨ |
| PUT | `/orders/{id}/status` | Update status | ✨ |
| PUT | `/orders/{id}/cancel` | Cancel order | ✨ |

### Reviews (4) ✨
| Method | Endpoint | Purpose | New |
|--------|----------|---------|-----|
| POST | `/products/{id}/reviews` | Create review | ✨ |
| GET | `/products/{id}/reviews` | Get reviews | ✨ |
| PUT | `/reviews/{id}` | Update review | ✨ |
| DELETE | `/reviews/{id}` | Delete review | ✨ |

### Health Check (2)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Root (welcome) |
| GET | `/health` | Health check |

**Total: 33 Endpoints (12 new for Day 13)**

---

## Request/Response Examples

### 🛒 Cart Examples

**GET /cart**
```bash
curl "http://localhost:8000/cart" \
  -H "Authorization: Bearer {token}"
```

**Response:**
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

**POST /cart/items**
```bash
curl -X POST "http://localhost:8000/cart/items" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 3, "quantity": 2}'
```

**Response:** 201 Created
```json
{
  "id": 1,
  "product_id": 3,
  "quantity": 2,
  "message": "Item added to cart"
}
```

---

### 📦 Order Examples

**POST /orders** (Checkout - ACID Transaction)
```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json"
```

**Response:** 201 Created
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

**GET /orders**
```bash
curl "http://localhost:8000/orders?skip=0&limit=10&status=delivered" \
  -H "Authorization: Bearer {token}"
```

**PUT /orders/{id}/status** (Admin Only)
```bash
curl -X PUT "http://localhost:8000/orders/1/status?new_status=delivered" \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json"
```

**PUT /orders/{id}/cancel** (User Owned)
```bash
curl -X PUT "http://localhost:8000/orders/1/cancel" \
  -H "Authorization: Bearer {token}"
```

---

### ⭐ Review Examples

**POST /products/{id}/reviews** (Purchase Verified)
```bash
curl -X POST "http://localhost:8000/products/3/reviews" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "comment": "Excellent product!"}'
```

**Response:** 201 Created
```json
{
  "id": 1,
  "user_id": 5,
  "product_id": 3,
  "rating": 5,
  "comment": "Excellent product!",
  "created_at": "2024-01-15T12:00:00"
}
```

**GET /products/{id}/reviews**
```bash
curl "http://localhost:8000/products/3/reviews?skip=0&limit=10"
```

**Response:** 200 OK
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
      "comment": "Excellent product!",
      "created_at": "2024-01-15T12:00:00"
    },
    {
      "id": 2,
      "user_id": 6,
      "product_id": 3,
      "rating": 4,
      "comment": "Good value",
      "created_at": "2024-01-15T13:00:00"
    }
  ]
}
```

**PUT /reviews/{id}** (Update Own)
```bash
curl -X PUT "http://localhost:8000/reviews/1" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"rating": 4, "comment": "Good, but room for improvement"}'
```

**DELETE /reviews/{id}** (Delete Own)
```bash
curl -X DELETE "http://localhost:8000/reviews/1" \
  -H "Authorization: Bearer {token}"
```

---

## Error Response Examples

### 400 Bad Request (Invalid Input)
```json
{
  "detail": "Quantity 999 exceeds available stock of 50"
}
```

### 401 Unauthorized (No Token)
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden (Permission Denied)
```json
{
  "detail": "Must purchase and receive product before reviewing"
}
```

### 404 Not Found
```json
{
  "detail": "Product with id 999 not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Database error occurred. Please try again later."
}
```

---

## Status Codes Reference

| Code | Meaning | Use Cases |
|------|---------|-----------|
| 200 | OK | Successful GET/PUT/DELETE |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE (empty response) |
| 400 | Bad Request | Validation error, insufficient stock |
| 401 | Unauthorized | Missing/invalid JWT token |
| 403 | Forbidden | Permission denied, not owner, not verified |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Database error (automatic rollback) |

---

## Authorization Levels

### Public (No Auth Required) ❌
- GET /products
- GET /products/{id}
- GET /categories
- GET /categories/{id}
- GET /categories/{id}/products
- GET /products/{id}/reviews
- POST /auth/register
- POST /auth/login
- GET /
- GET /health

### User Only (JWT Required) 👤
- GET /cart
- POST /cart/items
- PUT /cart/items/{id}
- DELETE /cart/items/{id}
- DELETE /cart
- POST /orders
- GET /orders
- PUT /orders/{id}/cancel
- POST /products/{id}/reviews
- PUT /reviews/{id}
- DELETE /reviews/{id}

### Admin Only (JWT + Admin Role) 👨‍💼
- POST /categories
- PUT /categories/{id}
- DELETE /categories/{id}
- POST /products
- PUT /products/{id}
- DELETE /products/{id}
- PUT /orders/{id}/status

---

## Test Credentials

```
Admin User:
  Email: admin@ecommerce.com
  Password: Admin123
  Role: admin

Customer User:
  Email: customer@ecommerce.com
  Password: Customer123
  Role: customer
```

---

## Query Parameters

### GET /products
```
- search: string (search name/description)
- category_id: integer
- min_price: float
- max_price: float
- sort_by: string (name|price|created_at)
- sort_order: string (asc|desc)
- skip: integer (default: 0)
- limit: integer (default: 10)
```

### GET /orders
```
- skip: integer (default: 0)
- limit: integer (default: 10)
- status: string (pending|shipped|delivered|cancelled)
```

### GET /products/{id}/reviews
```
- skip: integer (default: 0)
- limit: integer (default: 10)
```

---

## Transaction Flow Diagram

```
POST /orders (Checkout)
    ↓
[Validate cart not empty]
    ↓ (400 if empty)
[BEGIN TRANSACTION]
    ↓
[Check all products exist & stock sufficient]
    ↓ (400 if insufficient)
[Deduct stock from each product]
    ↓
[Calculate total from current prices]
    ↓
[Create Order + OrderItems]
    ↓
[Delete all CartItems]
    ↓
[COMMIT] ✅
    ↓
[Return OrderResponse]

If ANY error:
    ↓
[ROLLBACK] ↩️
    ↓
[Cart unchanged]
[Stock unchanged]
[No Order created]
```

---

## Integration Notes

All endpoints are integrated in `app/main.py`:
```python
app.include_router(auth_routes.router)
app.include_router(categories_routes.router)
app.include_router(products_routes.router)
app.include_router(cart_routes.router)        # NEW
app.include_router(orders_routes.router)      # NEW
app.include_router(reviews_routes.router)     # NEW
```

No conflicts. All routes work together seamlessly.

---

**Last Updated:** January 2024  
**API Version:** 1.0.0  
**Status:** Production Ready ✅
