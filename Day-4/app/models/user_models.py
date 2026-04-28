from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    age: int = Field(gt=0, lt=120)

class UpdateUser(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, gt=0, lt=120)
