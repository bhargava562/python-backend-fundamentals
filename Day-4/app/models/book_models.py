from pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    author: str = Field(min_length=2)
    isbn: str = Field(min_length=5, max_length=20)
    price: float = Field(gt=0)

class UpdateBook(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2)
    author: Optional[str] = None
    isbn: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
