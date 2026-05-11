# Django Fundamentals: Product Catalog System (Days 14-17)

## 📌 Overview
This project is a foundational Django web application built to demonstrate the core principles of the Django web framework. It implements a fully functional Product Catalog system using Django's Model-View-Template (MVT) architecture, an embedded SQLite database configured via Django's ORM, and the built-in Admin interface for seamless data management.

## 🎯 Learning Objectives Achieved
- **Framework Initialization:** Set up a Django project (`core`) with modular, multi-app architecture (`catalog`, `accounts`).
- **MVT Architecture:** Implemented separation of concerns across Data Models, View Logic, and HTML Templates.
- **Django ORM:** Designed relational database schemas utilizing `ForeignKey` for Many-to-One relationships.
- **Admin Integration:** Registered models to the Django Admin panel for instant CRUD capabilities.
- **Routing & Views:** Created custom URL patterns and function-based views to render dynamic database content to the frontend.

---

## 🏗️ Project Structure
The project is split into the main configuration directory and functional applications:

```text
Day-14-17/
├── core/                   # Main project configuration (settings, urls, wsgi/asgi)
├── catalog/                # Primary application for product management
│   ├── models.py           # Defines Category and Product tables
│   ├── views.py            # Contains the product_list logic
│   └── templates/          # Contains the list.html presentation layer
├── accounts/               # Secondary application for user profile management
├── comparison.md           # Technical comparison between Django and FastAPI
├── manage.py               # Django's command-line utility
└── db.sqlite3              # Auto-generated SQLite database

```

---

## 🚀 Setup & Installation Instructions

To run this project locally, ensure you have Python 3.10+ installed.

**1. Clone and Navigate to the Directory**

```bash
cd Day-14-17

```

**2. Create and Activate a Virtual Environment**

```bash
# Windows
python -m venv venv
source venv/Scripts/activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

```

**3. Install Dependencies**

```bash
pip install django

```

**4. Apply Database Migrations**
This will generate the SQLite database and create the necessary tables defined in `models.py`.

```bash
python manage.py makemigrations
python manage.py migrate

```

**5. Create an Admin Superuser**
You will be prompted to enter a username, email, and password.

```bash
python manage.py createsuperuser

```

**6. Start the Development Server**

```bash
python manage.py runserver

```

---

## 🖥️ Usage & Endpoints

Once the server is running at `http://127.0.0.1:8000/`, you can access the following routes:

### 1. The Admin Panel (`/admin/`)

Log in using the superuser credentials created during setup. Here you can:

* Add, update, and delete **Categories**.
* Add, update, and delete **Products**, assigning them to specific categories.

### 2. The Product Catalog (`/products/`)

A dynamically generated view that fetches all products from the database via the ORM and renders them using the Django Template Language (DTL). If no products exist, it will prompt the user to add them via the Admin panel.

---

## 💻 Django Shell Operations (ORM Practice)

The assignment required interaction with the Django database via the interactive shell. The following operations were tested and verified:

```python
# Accessed via: python manage.py shell

from catalog.models import Category, Product

# Create
tech_category = Category.objects.create(name="Electronics")
product = Product(title="Mechanical Keyboard", price=99.99, description="RGB lighting", category=tech_category)
product.save()

# Read/Query
all_products = Product.objects.all()
filtered_products = Product.objects.filter(price__lt=100.00)

# Update
product.price = 89.99
product.save()

# Delete
# product.delete()

```

