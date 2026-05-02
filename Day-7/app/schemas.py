from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"  # Default role is 'user'

class UserResponse(BaseModel):
    username: str
    email: EmailStr
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenResponse(BaseModel):
    """Enhanced token response with refresh token."""
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int  # in seconds

class RefreshTokenRequest(BaseModel):
    """Request body for token refresh."""
    refresh_token: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None