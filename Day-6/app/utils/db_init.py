import sys
import os

# Add the parent directory to sys.path so we can import 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.database import engine, Base
from app.models import User, Item # Import all models here

def initialize_database():
    print("--- Initializing Database ---")
    try:
        # This command creates all tables defined in models.py
        # If the tables already exist, it does nothing (safe to run multiple times)
        Base.metadata.create_all(bind=engine)
        print("Successfully created database tables.")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        exit(1)

if __name__ == "__main__":
    initialize_database()