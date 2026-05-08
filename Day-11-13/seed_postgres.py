#!/usr/bin/env python
"""Seed PostgreSQL database with initial test data."""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, User, Category, Product
from app.auth.security import hash_password

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("\n" + "=" * 60)
print("PostgreSQL Database Seeding")
print("=" * 60)

try:
    # Create engine and session
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    print("\n✓ Connected to PostgreSQL database")
    
    # Check if already seeded
    user_count = session.query(User).count()
    if user_count > 0:
        print("⚠️  Database already seeded (users exist). Skipping...")
        session.close()
        print("=" * 60 + "\n")
        exit(0)
    
    # Create tables
    print("📋 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")
    
    # Add admin user
    print("👤 Adding users...")
    admin_user = User(
        username="admin",
        email="admin@ecommerce.com",
        password=hash_password("Admin123"),
        role="admin"
    )
    customer_user = User(
        username="customer",
        email="customer@ecommerce.com",
        password=hash_password("Customer123"),
        role="customer"
    )
    session.add(admin_user)
    session.add(customer_user)
    session.commit()
    print("✓ Users created")
    
    # Add categories
    print("📦 Adding categories...")
    categories_data = [
        ("Electronics", "Electronic devices and gadgets"),
        ("Clothing", "Fashion and apparel"),
        ("Books", "Digital and physical books"),
    ]
    categories = []
    for name, description in categories_data:
        category = Category(name=name, description=description)
        session.add(category)
        categories.append(category)
    session.commit()
    print("✓ Categories created")
    
    # Add products
    print("🛍️  Adding products...")
    products_data = [
        {
            "name": "Laptop",
            "description": "High-performance laptop for professionals",
            "price": 1299.99,
            "stock": 10,
            "image_url": "https://via.placeholder.com/300x300?text=Laptop",
            "category": categories[0]
        },
        {
            "name": "Smartphone",
            "description": "Latest smartphone with advanced features",
            "price": 899.99,
            "stock": 25,
            "image_url": "https://via.placeholder.com/300x300?text=Smartphone",
            "category": categories[0]
        },
        {
            "name": "Headphones",
            "description": "Wireless noise-canceling headphones",
            "price": 199.99,
            "stock": 50,
            "image_url": "https://via.placeholder.com/300x300?text=Headphones",
            "category": categories[0]
        },
        {
            "name": "T-Shirt",
            "description": "Comfortable cotton t-shirt",
            "price": 29.99,
            "stock": 100,
            "image_url": "https://via.placeholder.com/300x300?text=T-Shirt",
            "category": categories[1]
        },
        {
            "name": "Jeans",
            "description": "Classic blue jeans",
            "price": 59.99,
            "stock": 80,
            "image_url": "https://via.placeholder.com/300x300?text=Jeans",
            "category": categories[1]
        },
        {
            "name": "Python Programming",
            "description": "Learn Python from beginner to advanced",
            "price": 39.99,
            "stock": 200,
            "image_url": "https://via.placeholder.com/300x300?text=Python+Book",
            "category": categories[2]
        },
        {
            "name": "FastAPI Guide",
            "description": "Complete guide to building APIs with FastAPI",
            "price": 49.99,
            "stock": 150,
            "image_url": "https://via.placeholder.com/300x300?text=FastAPI",
            "category": categories[2]
        },
    ]
    
    for product_data in products_data:
        category = product_data.pop("category")
        product = Product(**product_data, category_id=category.id)
        session.add(product)
    session.commit()
    print("✓ Products created")
    
    session.close()
    
    print("\n✅ Database successfully seeded!")
    print("\nTest Credentials:")
    print("  Admin Email: admin@ecommerce.com")
    print("  Admin Password: Admin123")
    print("  Customer Email: customer@ecommerce.com")
    print("  Customer Password: Customer123")
    print("\n" + "=" * 60 + "\n")

except Exception as e:
    print(f"\n❌ Error seeding database!")
    print(f"Error: {str(e)}")
    if session:
        session.rollback()
        session.close()
    print("\n" + "=" * 60 + "\n")
    exit(1)
