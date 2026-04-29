# 📘 Day 5 — Pydantic Mastery: Advanced Data Validation

![Pydantic](https://img.shields.io/badge/Pydantic-v2.13-e92063?style=for-the-badge&logo=pydantic&logoColor=white)
![FastAPI](https://img.shields.io/badge/Focus-Data_Integrity-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Day](https://img.shields.io/badge/Day-5-orange?style=for-the-badge)

## 🎯 Overview
On Day 5, the focus shifted from core Python to **Data Validation and Type Safety** using Pydantic. This project implements a production-grade data modeling layer for an E-commerce and Blogging platform, ensuring that every piece of data entering the system is strictly validated against business rules.

---

## 📁 Project Structure
The code is organized into a modular structure to simulate a real-world backend application:
```text
Day-5/
├── app/
│   ├── main.py              # Validation error handling & demo
│   ├── models/              # Pydantic schema definitions
│   │   ├── user.py          # User & Address logic
│   │   ├── product.py       # Product constraints
│   │   ├── order.py         # Nested orders & business logic
│   │   └── blog.py          # Lists, Dates & Comments
│   └── database/
│       └── db_models.py     # Placeholder for ORM models
├── requirements.txt         # Dependencies
└── README.md                # (This file)
```

---

## 🛠️ What I Implemented & Why

### 1. The CRUD Model Pattern
**What:** Created separate models for `Create`, `Update`, and `Response` for the same resource (e.g., `UserCreate`, `UserUpdate`, `UserResponse`).
**Why:** In real APIs, you never want to return a user's password in a response. By separating models, we can require a password during creation but exclude it entirely when sending data back to the client.

### 2. Custom Business Logic Validators
**What:** Used `@field_validator` and `@model_validator` for complex checks.
- **Password Strength:** Rejects passwords without at least one digit and one uppercase letter.
- **Future Dates:** Prevents blog posts from being dated in the future.
- **Financial Calculation:** A root validator in the `Order` model automatically calculates the `total` price based on item quantities and unit prices, ensuring no "total mismatch" errors.

### 3. Field Aliases & Constraints
**What:** Used `Field(alias="...")` and specialized types like `EmailStr` and `HttpUrl`.
**Why:** Frontend developers might send a JSON field as `login`, but we want to store it as `username` in Python. Aliases bridge this gap without breaking code. Constraints like `gt=0` (greater than zero) for prices ensure data integrity at the entry point.

---

## 🚨 Error Handling Logic
In `main.py`, I implemented a global-style exception handler for `ValidationError`. Instead of a generic crash, it parses the Pydantic error object to show exactly which field failed and why. This mimics a **422 Unprocessable Entity** response from FastAPI.

### Example Output (Validation Failure)
When passing an age of `12` (minimum `18`) and an invalid email to `UserCreate`, the system returns:
```text
--- 422 Unprocessable Entity ---
Error in [email]: value is not a valid email address
Error in [password]: Password must contain at least one uppercase letter
Error in [age]: Input should be greater than or equal to 18
```

---

## 🚀 How to Run
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Demonstration:**
   ```bash
   python app/main.py
   ```

## ✅ Learning Outcomes
- Developed **10+ models** with deep nesting (e.g., Orders containing lists of OrderItems).
- Mastered **Regex validation** for zip codes and string formats.
- Implemented **Optional vs Required** fields for PATCH/PUT logic.
- Gained experience in handling and formatting **Pydantic ValidationErrors** for user-friendly feedback.
