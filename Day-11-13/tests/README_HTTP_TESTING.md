# API Testing with REST Client HTTP Files

This directory contains comprehensive REST Client HTTP files for testing all Day 13 E-Commerce API endpoints.

## 📦 Setup Requirements

### Install REST Client Extension
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "REST Client" by Huachao Mao
4. Click Install

### Database & Server Setup
```bash
cd Day-11-13

# 1. Setup PostgreSQL database
python seed_postgres.py

# 2. Start FastAPI server (in separate terminal)
uvicorn app.main:app --reload
```

The server will run on `http://localhost:8000`

---

## 📝 HTTP Files Available

### 1. **auth.http** - Authentication
- Register new users (admin and customer)
- Login endpoints to get JWT tokens
- Health check

**Action Steps:**
1. Run admin registration
2. Run customer registration
3. Run admin login → Copy token to `@admin_token`
4. Run customer login → Copy token to `@token`

### 2. **products.http** - Product & Category Management
- Browse categories and products
- Search and filter products
- Admin operations (create, update, delete)

**Prerequisites:** Need `@admin_token` from auth.http

### 3. **cart.http** - Shopping Cart Operations
- View cart (auto-creates on first access)
- Add items to cart
- Update item quantities
- Delete items
- Clear entire cart
- Error scenarios (stock limits, unauthorized access)

**Prerequisites:** Need `@token` from auth.http

### 4. **orders.http** - Order Management
- Checkout with ACID transactions
- View order history
- Filter orders by status
- Admin status updates
- Cancel pending orders
- Transaction safety verification

**Prerequisites:** Need `@token` and `@admin_token`

### 5. **reviews.http** - Review System (Purchase Verified)
- Create reviews (only after product delivery)
- View product reviews with average rating
- Update own reviews
- Delete own reviews
- Error scenarios (unauthorized, unverified purchase)

**Prerequisites:** Need `@token` and order in "delivered" status

### 6. **admin.http** - Admin Operations
- Create categories
- Create products with stock
- Update product prices and stock
- Update order statuses
- Error scenarios (unauthorized access)

**Prerequisites:** Need `@admin_token` from auth.http

### 7. **workflow.http** - Complete End-to-End Workflow ⭐
Complete workflow covering the entire business logic:
```
1. Register new customer
2. Login to get token
3. Browse categories
4. Browse products in category
5. Add items to cart
6. Update cart quantities
7. Checkout (ACID transaction)
8. Attempt review before delivery (should fail)
9. Admin updates order to delivered
10. Create review after delivery
11. Update review
12. View reviews with average rating
13. Delete review
```

**Best file to test complete functionality!**

---

## 🚀 How to Use

### Method 1: Individual File Testing

1. **Open auth.http**
   - Click "Send Request" next to admin registration
   - Click "Send Request" next to customer registration
   - Run admin login, copy token to `@admin_token` variable
   - Run customer login, copy token to `@token` variable

2. **Open products.http**
   - Replace `<paste-admin-token-here>` with actual admin token
   - Run requests to browse products or create new ones

3. **Open cart.http**
   - Replace `<paste-customer-token-here>` with actual customer token
   - Run requests to add items, update quantities, etc.

4. **Open orders.http**
   - Replace tokens and test checkout flow

5. **Open reviews.http**
   - Replace token and test review creation after delivery

### Method 2: Complete Workflow Testing (Recommended)

1. **Open workflow.http** - This file contains the complete flow
2. Follow the steps in order:
   - Replace token placeholders after each login step
   - Execute requests sequentially to see the full workflow
   - Each step is numbered and commented

---

## 🔑 Token Management

### Copying Tokens
When you run a login request, the response will contain:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

1. Copy the entire `access_token` value (without quotes)
2. In the HTTP file, find the line: `@token = <paste-token-here>`
3. Replace `<paste-token-here>` with the copied token
4. Now all requests using `{{token}}` will use this bearer token

### Token Expiry
- Tokens are valid for 30 minutes
- If you get 401 Unauthorized, login again and get a fresh token

---

## 🧪 Testing Workflows

### Quick Smoke Test (5 minutes)
```
1. auth.http → Run both registrations and logins
2. products.http → Run "GET ALL PRODUCTS"
3. cart.http → Run "VIEW CART"
4. orders.http → Run checkout
5. reviews.http → Run "GET REVIEWS"
```

### Full Business Logic Test (15 minutes)
Run all requests in **workflow.http** sequentially from Step 1 to Step 29.

### ACID Transaction Testing
In orders.http:
1. Run "TRANSACTION SAFETY TEST: Get product details before checkout"
2. Run "TRANSACTION SAFETY TEST: Checkout"
3. Run "TRANSACTION SAFETY TEST: Get product details after checkout" (stock should decrease)
4. Run "TRANSACTION SAFETY TEST: Verify cart is empty" (cart auto-cleared)

### Purchase Verification Testing
In reviews.http:
1. Run "ATTEMPT REVIEW BEFORE DELIVERY" (Should get 403 error)
2. Have admin run order status update to "delivered"
3. Run "CREATE REVIEW AFTER DELIVERY" (Should succeed)

### Authorization Testing
In each file, look for "ERROR TEST" sections to verify:
- ❌ Unauthorized access (no token)
- ❌ Invalid tokens
- ❌ Wrong permissions (customer trying admin operations)
- ❌ Resource ownership (updating someone else's review)

---

## 📊 Expected Responses

### Successful Requests
- **200 OK** - Successful GET/PUT/DELETE
- **201 Created** - Successful POST (new resource)
- **204 No Content** - Successful DELETE (empty response)

### Error Responses
- **400 Bad Request** - Invalid input, insufficient stock, duplicate review
- **401 Unauthorized** - Missing or invalid token
- **403 Forbidden** - Permission denied, not purchase verified
- **404 Not Found** - Resource doesn't exist
- **500 Server Error** - Database error (with automatic rollback)

---

## 💡 Tips & Tricks

### Save Request Variables
After running login requests, the response JSON can be parsed. Click the response to select variables you want to reuse.

### Batch Run Multiple Requests
Select multiple requests with Ctrl+Click, then use "Run All" to execute them sequentially.

### View Full Request/Response
Click on the request/response in the output panel to see detailed headers and body.

### Debug Failed Requests
- Check error message in response
- Verify token is valid and not expired
- Ensure database is running
- Check server logs for detailed errors

### Test Error Scenarios
Each file contains "ERROR TEST" sections to verify:
- Invalid inputs are rejected
- Unauthorized access is blocked
- Duplicate resources are prevented
- Permission checks work correctly

---

## 🔄 Full Workflow Sequence

```
STEP 1: Register → Get user created
STEP 2: Login → Get JWT token
STEP 3: Browse products (public, no auth)
STEP 4: View empty cart (auto-created)
STEP 5: Add product to cart
STEP 6: Checkout (ACID transaction) ✅ Stock decreased, Cart cleared
STEP 7: Try review (fails) ❌ Order still pending
STEP 8: Admin updates order to "delivered"
STEP 9: Create review ✅ Purchase verified
STEP 10: View review with avg rating
STEP 11: Update review
STEP 12: Delete review
STEP 13: Verify review deleted
```

---

## 🛠️ Troubleshooting

### "Cannot POST /orders" Error
- Ensure server is running: `uvicorn app.main:app --reload`
- Check base URL in file: Should be `http://localhost:8000`

### "401 Unauthorized" on Protected Endpoints
- Token is missing or invalid
- Copy token correctly from login response
- Token may be expired (get a new one)

### "403 Forbidden" on Admin Endpoints
- Using customer token instead of admin token
- Ensure you used admin login, not customer login

### "400 Bad Request - Insufficient stock"
- Product doesn't have enough inventory
- Add fewer items to cart
- Admin can update product stock

### "400 Bad Request - Already reviewed"
- User already has a review for this product
- Delete existing review first or use different product

### Database Connection Errors
- Ensure PostgreSQL is running
- Check .env file has correct connection string
- Run `python seed_postgres.py` to setup database

### Port Already in Use
- Another process is using port 8000
- Change port: `uvicorn app.main:app --reload --port 8001`
- Update base URL in HTTP files to `http://localhost:8001`

---

## 📚 Additional Resources

- [REST Client Documentation](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)
- [API Documentation](./docs/API_ENDPOINTS_REFERENCE.md)
- [Day 13 Implementation Guide](./docs/DAY_13_COMPLETION_SUMMARY.md)
- [Full Endpoint Reference](./docs/INDEX.md)

---

**Happy Testing! 🚀**
