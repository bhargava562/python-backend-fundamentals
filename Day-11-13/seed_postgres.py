#!/usr/bin/env python
"""Seed PostgreSQL database with initial test data."""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, User, Category, Product, Cart, CartItem, Order, OrderItem
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
    
    # Check if already seeded (make idempotent: only create missing data)
    user_count = session.query(User).count()
    if user_count == 0:
        # Create tables (fresh DB)
        print("📋 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created")
    else:
        print("⚠️  Some users already exist. Will ensure missing data is added (idempotent seed).")
    
    # Add admin and customer users if missing
    print("👤 Ensuring admin and customer users exist...")
    admin_user = session.query(User).filter(User.email == "admin@ecommerce.com").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@ecommerce.com",
            password=hash_password("Admin123"),
            role="admin"
        )
        session.add(admin_user)

    customer_user = session.query(User).filter(User.email == "customer@ecommerce.com").first()
    if not customer_user:
        customer_user = User(
            username="customer",
            email="customer@ecommerce.com",
            password=hash_password("Customer123"),
            role="customer"
        )
        session.add(customer_user)

    session.commit()
    print("✓ Users ensured")
    
    # Add categories
    print("📦 Ensuring categories exist...")
    categories_data = [
        ("Electronics", "Electronic devices and gadgets"),
        ("Clothing", "Fashion and apparel"),
        ("Books", "Digital and physical books"),
    ]
    categories = []
    for name, description in categories_data:
        category = session.query(Category).filter(Category.name == name).first()
        if not category:
            category = Category(name=name, description=description)
            session.add(category)
            session.flush()
        categories.append(category)
    session.commit()
    print("✓ Categories ensured")
    
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
        # check if product exists by name + category
        existing = session.query(Product).filter(
            Product.name == product_data["name"],
            Product.category_id == category.id
        ).first()
        if not existing:
            product = Product(**product_data, category_id=category.id)
            session.add(product)
    session.commit()
    print("✓ Products ensured")
    
    # Add sample carts and orders for testing
    print("🛒 Adding sample orders...")
    products = session.query(Product).all()
    
    # Create cart for customer if missing
    cart = session.query(Cart).filter(Cart.user_id == customer_user.id).first()
    if not cart:
        cart = Cart(user_id=customer_user.id)
        session.add(cart)
        session.commit()
    
    # Add items to cart (ensure at least one item)
    products = session.query(Product).all()
    if products:
        existing_item = session.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == products[0].id
        ).first()
        if not existing_item:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=products[0].id,  # Laptop
                quantity=1
            )
            session.add(cart_item)
            session.commit()
            print("✓ Cart created with sample item")
        else:
            print("✓ Cart already has sample item")
    else:
        print("⚠️  No products found to add to cart")
    
    # Create a completed order (for review testing) if missing
    products = session.query(Product).all()
    if products:
        existing_order = session.query(Order).filter(
            Order.user_id == customer_user.id,
            Order.status == "delivered"
        ).first()
        if not existing_order:
            order = Order(
                user_id=customer_user.id,
                total=products[0].price,
                status="delivered"  # Already delivered so customer can review
            )
            session.add(order)
            session.commit()

            # Add order items
            order_item = OrderItem(
                order_id=order.id,
                product_id=products[0].id,
                quantity=1,
                price=products[0].price
            )
            session.add(order_item)
            session.commit()
            print("✓ Completed order created (ready for reviews)")
        else:
            print("✓ Delivered order already exists")
    else:
        print("⚠️  No products found to create sample order")
    
    session.close()
    
    print("\n✅ Database successfully seeded!")
    print("\nTest Credentials:")
    print("  Admin Email: admin@ecommerce.com")
    print("  Admin Password: Admin123")
    print("  Customer Email: customer@ecommerce.com")
    print("  Customer Password: Customer123")
    print("\nSample Data:")
    print(f"  Products: {len(products)} products available")
    print(f"  Cart: 1 cart with Laptop ready to checkout")
    print(f"  Completed Order: 1 delivered order (can review)")
    print("\n" + "=" * 60 + "\n")

except Exception as e:
    print(f"\n❌ Error seeding database!")
    print(f"Error: {str(e)}")
    if session:
        session.rollback()
        session.close()
    print("\n" + "=" * 60 + "\n")
    exit(1)
