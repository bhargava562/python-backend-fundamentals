from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from . import models, schemas, database

app = FastAPI(
    title="Zenovox Task Manager",
    description="A simple task manager API built with FastAPI and in-memory database",
    version="1.0.0"
)

# Initialize database tables immediately on module load
database.Base.metadata.create_all(bind=database.engine)


# ============ CREATE ============
@app.post("/tasks/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    """
    Create a new task.
    
    - **title**: Task title (required)
    - **description**: Task description (optional)
    - **is_completed**: Completion status (default: False)
    """
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# ============ READ ============
@app.get("/tasks/", response_model=list[schemas.TaskResponse])
async def read_all_tasks(db: Session = Depends(database.get_db)):
    """Get all tasks from the database."""
    return db.query(models.Task).all()


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def read_task(task_id: int, db: Session = Depends(database.get_db)):
    """Get a specific task by ID."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with ID {task_id} not found"
        )
    return db_task


# ============ UPDATE ============
@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def update_task(task_id: int, task_update: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    """Update a task by ID."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with ID {task_id} not found"
        )
    
    # Update fields
    for key, value in task_update.model_dump().items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


# ============ DELETE ============
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    """Delete a task by ID."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with ID {task_id} not found"
        )
    
    db.delete(db_task)
    db.commit()
    return None


# ============ HEALTH CHECK ============
@app.get("/health/")
async def health_check():
    """Check if the API is running."""
    return {"status": "healthy", "service": "Task Manager API"}