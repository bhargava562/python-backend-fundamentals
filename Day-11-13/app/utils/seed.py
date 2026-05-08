"""Database seed script to populate initial data."""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.config import engine, SessionLocal
from app.models.models import Base, User, Category, Product
from app.auth.security import hash_password


def seed_database():
    """Seed the database with initial data."""
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        user_count = db.query(User).count()
        if user_count > 0:
            print("\n⚠ Database already seeded. Skipping...")
            return
        
        print("\nSeeding database with initial data...")
        
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@ecommerce.com",
            password=hash_password("Admin123"),
            role="admin"
        )
        db.add(admin_user)
        print("✓ Admin user created")
        
        # Create customer user
        customer_user = User(
            username="customer",
            email="customer@ecommerce.com",
            password=hash_password("Customer123"),
            role="customer"
        )
        db.add(customer_user)
        print("✓ Customer user created")
        
        db.flush()  # Ensure users are created before creating categories
        
        # Create categories
        electronics = Category(
            name="Electronics",
            description="Electronic devices and gadgets"
        )
        db.add(electronics)
        
        clothing = Category(
            name="Clothing",
            description="Apparel and fashion items"
        )
        db.add(clothing)
        
        books = Category(
            name="Books",
            description="Physical and digital books"
        )
        db.add(books)
        
        print("✓ Categories created")
        db.flush()
        
        # Create products
        products_data = [
            {
                "name": "Laptop Pro",
                "description": "High-performance laptop for professionals",
                "price": 1299.99,
                "stock": 50,
                "category_id": electronics.id,
                "image_url": "https://via.placeholder.com/300?text=Laptop+Pro"
            },
            {
                "name": "Wireless Mouse",
                "description": "Ergonomic wireless mouse with long battery life",
                "price": 29.99,
                "stock": 200,
                "category_id": electronics.id,
                "image_url": "https://via.placeholder.com/300?text=Wireless+Mouse"
            },
            {
                "name": "USB-C Cable",
                "description": "Fast charging USB-C cable",
                "price": 12.99,
                "stock": 500,
                "category_id": electronics.id,
                "image_url": "https://via.placeholder.com/300?text=USB+Cable"
            },
            {
                "name": "T-Shirt",
                "description": "Comfortable cotton t-shirt",
                "price": 19.99,
                "stock": 150,
                "category_id": clothing.id,
                "image_url": "https://via.placeholder.com/300?text=T-Shirt"
            },
            {
                "name": "Jeans",
                "description": "Classic denim jeans",
                "price": 49.99,
                "stock": 100,
                "category_id": clothing.id,
                "image_url": "https://via.placeholder.com/300?text=Jeans"
            },
            {
                "name": "Python Programming",
                "description": "Learn Python from beginner to advanced",
                "price": 39.99,
                "stock": 75,
                "category_id": books.id,
                "image_url": "https://via.placeholder.com/300?text=Python+Book"
            },
            {
                "name": "FastAPI Guide",
                "description": "Complete guide to building APIs with FastAPI",
                "price": 44.99,
                "stock": 60,
                "category_id": books.id,
                "image_url": "https://via.placeholder.com/300?text=FastAPI+Book"
            },
        ]
        
        for product_data in products_data:
            product = Product(**product_data)
            db.add(product)
        
        print("✓ Products created")
        
        # Commit all changes
        db.commit()
        print("\n✅ Database successfully seeded!")
        print("\nTest Credentials:")
        print("  Admin Email: admin@ecommerce.com")
        print("  Admin Password: Admin123")
        print("  Customer Email: customer@ecommerce.com")
        print("  Customer Password: Customer123")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding database: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
