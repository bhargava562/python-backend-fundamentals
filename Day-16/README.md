# Day 16: DRF Authentication & Permissions (JWT Identity Management)

## 📌 Executive Summary
This module implements a robust, secure, and stateless identity management system using the **Django REST Framework (DRF)** and **JSON Web Tokens (JWT)**. The project abandons basic session authentication in favor of enterprise-standard token-based architecture, featuring complex endpoint security, custom object-level permissions, and secure password handling.

---

## 🏗️ Architectural Highlights
- **Stateless Authentication:** Implemented `djangorestframework-simplejwt` to handle short-lived Access Tokens (60 mins) and long-lived Refresh Tokens (1 day).
- **Global Security Enforcement:** The API defaults to strict `IsAuthenticated` access globally, forcibly rejecting any requests lacking valid Bearer tokens.
- **Custom Object-Level Permissions:** Engineered a custom `IsOwnerOrReadOnly` permission class to ensure data integrity at the database row level.
- **Modular App Design:** - `accounts`: Handles registration, profile retrieval, and password mutations.
  - `notes`: Serves as the testing ground for ownership-based CRUD operations.

---

## 🔐 Permissions Matrix

| Endpoint | HTTP Method | Permission Class | Description |
| :--- | :--- | :--- | :--- |
| `/api/auth/register/` | `POST` | `AllowAny` | Overrides global settings to allow public onboarding. |
| `/api/auth/login/` | `POST` | `AllowAny` | Public endpoint to exchange credentials for JWTs. |
| `/api/profile/` | `GET`, `PUT`, `PATCH` | `IsAuthenticated` | Requires valid token. Automatically derives user ID from token payload. |
| `/api/notes/` | `GET` | `IsAuthenticatedOrReadOnly` | Publicly accessible for reading (Safe Methods). |
| `/api/notes/` | `POST` | `IsAuthenticated` | Only logged-in users can create notes. |
| `/api/notes/{id}/` | `PUT`, `DELETE` | `IsOwnerOrReadOnly` | **Custom:** Only the specific user who created the note can modify or delete it. |

---

## 🚀 Setup & Installation

**1. Initialize Environment**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows

```

**2. Install Dependencies**

```bash
pip install django djangorestframework djangorestframework-simplejwt

```

**3. Run Migrations & Start Server**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```

---

## 🧪 Testing Flow & Output Logs

Testing was conducted using VS Code REST Client (`tests/authflow.http`) to document the complete lifecycle of a user session. Below are the execution steps and the verified outputs.

### 1. User Registration

* **Action:** Sent `POST` to `/api/auth/register/` with user details. Password was securely hashed via `create_user` overriding the serializer's `create` method.
* **Result:** `201 Created`
* **Output:**

```json
{
  "username": "admin_user",
  "email": "admin@example.com",
  "first_name": "System",
  "last_name": "Admin"
}

```

### 2. Token Generation (Login)

* **Action:** Sent `POST` to `/api/auth/login/` with username and password.
* **Result:** `200 OK`
* **Output:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR...",
  "access": "eyJhbGciOiJIUzI1NiIsInR..."
}

```

*(The `access` token was then copied and used as the Bearer token for subsequent requests).*

### 3. Profile Access (Authenticated)

* **Action:** Sent `GET` to `/api/profile/` passing the Bearer token in the `Authorization` header.
* **Result:** `200 OK`
* **Output:**

```json
{
  "id": 1,
  "username": "admin_user",
  "email": "admin@example.com",
  "first_name": "System",
  "last_name": "Admin"
}

```

### 4. Creating a Note (Authenticated)

* **Action:** Sent `POST` to `/api/notes/` with the Bearer token. The `perform_create` method in the ViewSet automatically linked the note to the authenticated user.
* **Result:** `201 Created`
* **Output:**

```json
{
  "id": 1,
  "title": "Secret System Architecture",
  "content": "This note belongs strictly to admin_user.",
  "owner": "admin_user",
  "created_at": "2026-05-12T10:00:00.000Z"
}

```

### 5. Error Handling: Missing Token

* **Action:** Sent `POST` to `/api/notes/` *without* an Authorization header to test the global security enforcement.
* **Result:** `401 Unauthorized`
* **Output:**

```json
{
  "detail": "Authentication credentials were not provided."
}

```

### 6. Error Handling: Invalid Password Change

* **Action:** Sent `PATCH` to `/api/profile/change-password/` with an incorrect `old_password`.
* **Result:** `400 Bad Request`
* **Output:**

```json
{
  "old_password": [
    "Wrong password."
  ]
}

```

---

## 📁 Project Structure

```text
Day-16/
├── core/                   # Project configurations & global JWT settings
├── accounts/               # User identity, registration, and profile views
│   ├── serializers.py      # Contains RegisterSerializer with password hashing
│   └── views.py            # Generics for auth operations
├── notes/                  # Domain logic for testing permissions
│   ├── permissions.py      # Custom IsOwnerOrReadOnly class
│   └── views.py            # ModelViewSet applying dual permission classes
├── tests/                  
│   └── authflow.http       # Automated REST client testing suite
├── manage.py
└── db.sqlite3

```
