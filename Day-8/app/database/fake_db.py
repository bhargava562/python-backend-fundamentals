# Simulated Database
users_db = {
    "user1": {
        "username": "user1",
        "email": "user1@example.com",
        "hashed_password": "somehash",
        "role": "user",
        "provider": "local",
        "provider_id": None
    }
}

def get_user_by_email(email: str):
    for user in users_db.values():
        if user.get("email") == email:
            return user
    return None

def create_oauth_user(email: str, name: str, provider: str, provider_id: str):
    # If using OAuth, they don't have a local password
    username = email.split('@')[0]
    new_user = {
        "username": username,
        "email": email,
        "hashed_password": None, 
        "role": "user",
        "provider": provider,
        "provider_id": provider_id
    }
    users_db[username] = new_user
    return new_user