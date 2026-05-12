# Django Fundamentals & REST Framework (Days 14-17)

## 📌 Overview
This project serves as a comprehensive introduction to the Django ecosystem. It begins with a foundational web application utilizing Django's Model-View-Template (MVT) architecture for a Product Catalog, and evolves into a headless, robust REST API powered by the Django REST Framework (DRF) for a Blog management system.

## 🎯 Learning Objectives Achieved
- **Framework Initialization:** Set up a core Django project with modular, multi-app architecture (`catalog`, `accounts`, `blog`).
- **MVT Architecture:** Implemented separation of concerns across Data Models, View Logic, and HTML Templates for server-rendered views.
- **REST API Architecture:** Transitioned to headless backend logic using DRF Serializers, ViewSets, and Routers.
- **Django ORM:** Designed relational schemas utilizing `ForeignKey` for Many-to-One relationships across multiple domains.
- **Admin Integration:** Registered models to the built-in Admin panel for instant CMS capabilities.
- **Advanced Querying:** Implemented pagination, text searching, and exact-match filtering for API endpoints.

---

## 🏗️ Project Structure
The project is split into the main configuration directory and domain-specific applications:

```text
Day-14-17/
├── core/                   # Main project configuration (settings, global urls)
├── catalog/                # Day 14: MVT application for product management
│   ├── models.py           # Defines Category and Product tables
│   ├── views.py            # Contains the product_list logic
│   └── templates/          # Contains the list.html presentation layer
├── accounts/               # Secondary MVT application for user management
├── blog/                   # Day 15: DRF application for headless API
│   ├── models.py           # Defines Author, Post, and Comment entities
│   ├── serializers.py      # Transforms complex QuerySets into JSON 
│   ├── views.py            # Contains ViewSets for rapid CRUD operations
│   └── urls.py             # DRF DefaultRouter configurations
├── tests/                  # Directory containing REST client HTTP test files
│   └── day15_blog.http     # Test suite for the Blog API
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
pip install django djangorestframework django-filter

```

**4. Apply Database Migrations**
This will generate the SQLite database and create the necessary tables defined in all apps.

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

Once the server is running at `http://127.0.0.1:8000/`, you can access the following systems:

### 1. The Admin Panel (`/admin/`)

Log in using the superuser credentials. Here you can perform manual CRUD operations on Categories, Products, Authors, Posts, and Comments.

### 2. The Product Catalog (MVT) (`/products/`)

A dynamically generated server-rendered view that fetches all products via the ORM and displays them using the Django Template Language (DTL).

### 3. The Blog API (DRF) (`/api/v1/`)

Fully functional RESTful endpoints featuring nested serialization, search, and pagination. Access these via the DRF Browsable API or a REST Client:

* **Authors:** `/api/v1/authors/`
* **Posts:** `/api/v1/posts/` (Supports `?search=` and `?is_published=true`)
* **Comments:** `/api/v1/comments/`

---

## 💻 Database Interaction & Testing

### Django Shell Operations (ORM Practice)

Interaction with the standard Django database via the interactive shell:

```python
# Accessed via: python manage.py shell

from catalog.models import Category, Product

# Create
tech = Category.objects.create(name="Electronics")
product = Product(title="Mechanical Keyboard", price=99.99, description="RGB", category=tech)
product.save()

# Read/Query
all_products = Product.objects.all()
filtered = Product.objects.filter(price__lt=100.00)

# Update
product.price = 89.99
product.save()

```

### DRF API Testing Suite

Postman was bypassed in favor of VS Code REST Client files for better version control. The complete testing suite for creating, retrieving, updating, and deleting Authors, Posts, and Comments is located in `tests/day15_blog.http`.
