from fastapi import APIRouter, HTTPException
from typing import Optional
from app.models.user_models import User, UpdateUser
from app.database.fake_db import users_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users(age: Optional[int] = None, skip: int = 0, limit: int = 10):
    results = users_db

    if age:
        results = [u for u in results if u["age"] == age]

    return results[skip : skip + limit]

@router.get("/{user_id}")
def get_user(user_id: int):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@router.post("/", status_code=201)
def create_user(user: User):
    # duplicate email check
    for u in users_db:
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    users_db.append(user.dict())
    return {"message": "User created"}

@router.put("/{user_id}")
def update_user(user_id: int, user: User):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user.dict()
    return {"message": "User updated"}

@router.patch("/{user_id}")
def patch_user(user_id: int, user: UpdateUser):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")

    stored = users_db[user_id]
    stored.update(user.dict(exclude_unset=True))
    return {"message": "User patched"}

@router.delete("/{user_id}")
def delete_user(user_id: int):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")

    users_db.pop(user_id)
    return {"message": "User deleted"}
