from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

class Address(BaseModel):
    street: str
    city: str
    zip_code: str = Field(..., pattern=r"^\d{5}$")

class UserBase(BaseModel):
    # Alias example: incoming JSON can use 'username' or 'login'
    username: str = Field(..., min_length=3, max_length=20, alias="login")
    email: EmailStr
    
    model_config = ConfigDict(populate_by_name=True)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    age: int = Field(..., ge=18, le=100)

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class UserUpdate(BaseModel):
    # All fields optional for PATCH requests
    username: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=18)

class UserResponse(UserBase):
    id: int
    profile: Optional[Address] = None
    created_at: datetime = Field(default_factory=datetime.now)