from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from app.schemas import TokenData
from app.fake_db import fake_users_db

# This tells FastAPI where the login endpoint is for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validates the JWT token and returns the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        
        if username is None:
            raise credentials_exception
            
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
        
    # Fetch user from DB
    user = fake_users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
        
    return user

async def get_admin_user(current_user: dict = Depends(get_current_user)):
    """Role-Based Access Control (RBAC): Check if user is an Admin."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have enough privileges (Admin required)"
        )
    return current_user

async def get_moderator_user(current_user: dict = Depends(get_current_user)):
    """Role-Based Access Control (RBAC): Check if user is a Moderator."""
    if current_user.get("role") not in ["moderator", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have enough privileges (Moderator or Admin required)"
        )
    return current_user