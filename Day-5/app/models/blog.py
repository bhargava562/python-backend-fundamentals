from typing import List
from datetime import date
from pydantic import BaseModel, Field, field_validator

class Comment(BaseModel):
    author: str
    content: str = Field(..., max_length=500)
    likes: int = Field(default=0)

class BlogPost(BaseModel):
    title: str = Field(..., min_length=5)
    content: str
    author: str
    tags: List[str] = Field(default_factory=list)
    pub_date: date
    comments: List[Comment] = []

    @field_validator('pub_date')
    @classmethod
    def no_future_posts(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Publication date cannot be in the future")
        return v