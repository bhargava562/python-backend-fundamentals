from pydantic import BaseModel
from typing import Optional, List

class ItemBase(BaseModel):
    title: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_deleted: bool
    items: List[Item] = []

    class Config:
        from_attributes = True
