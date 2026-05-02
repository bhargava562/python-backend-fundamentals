from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from jose import jwt, JWTError
from app.schemas import UserCreate, UserResponse, Token, TokenResponse, RefreshTokenRequest
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    create_refresh_token
)
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.fake_db import fake_users_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # IMPORTANT: Never save raw passwords!
    hashed_password = get_password_hash(user.password)
    
    user_db_obj = {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "hashed_password": hashed_password
    }
    
    fake_users_db[user.username] = user_db_obj
    return user_db_obj

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint that returns both access and refresh tokens."""
    # OAuth2PasswordRequestForm uses form-data instead of JSON
    user = fake_users_db.get(form_data.username)
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Store username in 'sub' (subject) and custom 'role' claim
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}, 
        expires_delta=access_token_expires
    )
    
    # Create refresh token
    refresh_token = create_refresh_token(
        data={"sub": user["username"]}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # in seconds
    }

@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(request: RefreshTokenRequest):
    """Refresh the access token using a valid refresh token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the refresh token
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if username is None or token_type != "refresh":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Fetch user from DB
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    
    # Create new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": new_access_token,
        "refresh_token": request.refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }