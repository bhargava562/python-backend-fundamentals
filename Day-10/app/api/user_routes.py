from fastapi import APIRouter, HTTPException, status
from typing import List
from app.core.logger import logger
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.database import db

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user"""
    try:
        logger.info(f"Creating user: {user.email}")
        user_dict = user.model_dump()
        created_user = db.create_user(user_dict)
        logger.info(f"User created successfully: {created_user['id']}")
        return created_user
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create user")

@router.get("/", response_model=List[UserResponse])
async def get_all_users():
    """Get all users"""
    try:
        logger.debug("Fetching all users")
        users = db.get_all_users()
        logger.info(f"Retrieved {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch users")

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get a specific user by ID"""
    try:
        logger.debug(f"Fetching user with ID: {user_id}")
        user = db.get_user(user_id)
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch user")

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    """Update an existing user"""
    try:
        logger.info(f"Updating user: {user_id}")
        user = db.get_user(user_id)
        if not user:
            logger.warning(f"User not found for update: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        
        update_data = user_update.model_dump(exclude_unset=True)
        updated_user = db.update_user(user_id, update_data)
        logger.info(f"User updated successfully: {user_id}")
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update user")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete a user"""
    try:
        logger.info(f"Deleting user: {user_id}")
        user = db.get_user(user_id)
        if not user:
            logger.warning(f"User not found for deletion: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete_user(user_id)
        logger.info(f"User deleted successfully: {user_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete user")
