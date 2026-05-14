from pydantic import BaseModel, Field
from typing import Optional

# This is what the user SENDS us (for creating/updating tasks)
class TaskCreate(BaseModel):
    """Schema for creating or updating a task."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    is_completed: bool = Field(False, description="Whether the task is completed")


# This is what we SEND BACK to the user (includes ID)
class TaskResponse(TaskCreate):
    """Schema for task response (includes ID from database)."""
    id: int = Field(..., description="Unique task identifier")

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models