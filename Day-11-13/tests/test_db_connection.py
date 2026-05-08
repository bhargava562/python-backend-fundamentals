#!/usr/bin/env python
"""Test PostgreSQL database connection and verify schema."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv(Path(__file__).parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

print("=" * 60)
print("PostgreSQL Connection Test")
print("=" * 60)
print(f"\n📌 Database URL: {DATABASE_URL}")

try:
    # Create engine
    engine = create_engine(DATABASE_URL, echo=False)
    print("\n✓ Engine created successfully")
    
    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✓ Connection successful")
    
    # Get database info
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"\n📊 Database Info:")
    print(f"  • Total tables: {len(tables)}")
    print(f"  • Tables: {', '.join(tables)}\n")
    
    # Verify all expected tables exist
    expected_tables = [
        'users', 
        'categories', 
        'products', 
        'carts', 
        'cart_items', 
        'orders', 
        'order_items', 
        'reviews'
    ]
    
    print("📋 Table Verification:")
    all_exist = True
    for table in expected_tables:
        exists = table in tables
        status = "✓" if exists else "✗"
        print(f"  {status} {table}")
        if not exists:
            all_exist = False
    
    if all_exist:
        print("\n✅ All expected tables exist!")
    else:
        print("\n⚠️ Some tables are missing!")
    
    # Show table schemas
    print("\n📐 Table Schemas:")
    for table in expected_tables:
        if table in tables:
            columns = inspector.get_columns(table)
            print(f"\n  {table}:")
            for col in columns:
                col_type = str(col['type'])
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                print(f"    • {col['name']}: {col_type} {nullable}")
    
    print("\n" + "=" * 60)
    print("✅ Database connection test completed successfully!")
    print("=" * 60)
    
    sys.exit(0)

except Exception as e:
    print(f"\n❌ Connection failed!")
    print(f"Error: {str(e)}")
    print("\n" + "=" * 60)
    print("Troubleshooting steps:")
    print("1. Verify PostgreSQL is running")
    print("2. Check username and password are correct")
    print("3. Verify database 'fastapi_demo' exists")
    print("4. Check .env file has correct DATABASE_URL")
    print("=" * 60)
    sys.exit(1)
