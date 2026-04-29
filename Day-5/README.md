# Pydantic Mastery: Advanced Data Validation

This repository contains a production-ready implementation of Pydantic models for an E-commerce/Blogging platform.

## Features Covered
- **10+ Comprehensive Models:** Including User, Product, Order, and Blog Post.
- **CRUD Pattern:** Separate models for `Create`, `Update`, and `Response` to handle sensitive data like passwords.
- **Advanced Constraints:** Regex for zip codes, numeric ranges for prices, and date range checks.
- **Deep Nesting:** Orders containing items, Blog posts containing comments.
- **Custom Logic:** Model-level validators for total price calculations and password complexity.

## Installation
```bash
pip install -r requirements.txt
python app/main.py
```