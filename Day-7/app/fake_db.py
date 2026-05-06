from app.core.security import get_password_hash

# Pre-populate the database so 'user1' always exists for Postman testing
fake_users_db = {
    "user1": {
        "username": "user1",
        "email": "user1@example.com",
        "role": "user",
        "hashed_password": get_password_hash("password123")
    }
}