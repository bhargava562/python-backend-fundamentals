from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: Optional[int] = Field(None, ge=18, le=120)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "age": 28
            }
        }

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=18, le=120)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "age": 28,
                "created_at": "2024-01-01T12:00:00"
            }
        }

# Product Schemas
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "High performance laptop",
                "price": 999.99,
                "stock": 50
            }
        }

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Laptop",
                "description": "High performance laptop",
                "price": 999.99,
                "stock": 50,
                "created_at": "2024-01-01T12:00:00"
            }
        }

# Order Schemas
class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(..., ge=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "product_id": 1,
                "quantity": 2
            }
        }

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    created_at: datetime
    
    class Config:
        from_attributes = True
