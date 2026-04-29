from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0, description="Price must be positive")
    stock: int = Field(..., ge=0)
    category: str = Field(..., examples=["Electronics", "Home", "Fashion"])
    image_url: Optional[HttpUrl] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

class ProductResponse(ProductBase):
    id: int