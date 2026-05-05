from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .pyobjectid import PyObjectId

# Embedded Document (Good for data accessed together)
class Review(BaseModel):
    user: str
    rating: int = Field(ge=1, le=5)
    comment: str

class Product(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    description: str
    price: float
    category: str
    # Embedded documents mapping
    reviews: List[Review] = []
    # Reference to another collection (e.g., users collection)
    seller_id: str 
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class ProductUpdate(BaseModel):
    """Schema for updating product fields (all fields optional)"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    reviews: Optional[List[Review]] = None
    seller_id: Optional[str] = None