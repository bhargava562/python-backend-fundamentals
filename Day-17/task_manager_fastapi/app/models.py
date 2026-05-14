from sqlalchemy import Column, Integer, String, Boolean
from . import database

# Use the Base from database module
Base = database.Base


class Task(Base):
    """
    Task model for the in-memory database.
    Represents a single task with title, description, and completion status.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, default="")
    is_completed = Column(Boolean, default=False)
