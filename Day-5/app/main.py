import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from pydantic import ValidationError
from models.user import UserCreate
from models.blog import BlogPost
from datetime import date

def handle_request(data_func):
    try:
        return data_func()
    except ValidationError as e:
        print("\n--- 422 Unprocessable Entity ---")
        for error in e.errors():
            field = " -> ".join(str(loc) for loc in error['loc'])
            print(f"Error in [{field}]: {error['msg']}")

def demo():
    # 1. Triggering Password & Age Validation
    print("Test 1: User Validation")
    handle_request(lambda: UserCreate(
        login="bob", 
        email="not-an-email", 
        password="simple", 
        age=12
    ))

    # 2. Triggering Date Validation
    print("\nTest 2: Blog Date Validation")
    handle_request(lambda: BlogPost(
        title="Hi", 
        content="...", 
        author="Me", 
        pub_date=date(2030, 1, 1)
    ))

if __name__ == "__main__":
    demo()