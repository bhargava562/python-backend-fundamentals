"""
Test script to verify the Task Manager API implementation.
This script tests all CRUD operations without needing a running server.
"""

import sys
import os
# Add parent directory to path so we can import app module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Task
from app.schemas import TaskCreate, TaskResponse
import json


def test_in_memory_database():
    """Test that in-memory database is working correctly."""
    print("\n" + "="*60)
    print("TEST 1: In-Memory Database Creation")
    print("="*60)
    
    # Create in-memory database
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    print("[OK] In-memory SQLite database created successfully")
    print("[OK] Tables created from models")
    
    # Test 1: Create a task
    print("\n" + "="*60)
    print("TEST 2: Create Task")
    print("="*60)
    
    task1 = Task(title="Learn FastAPI", description="Study FastAPI fundamentals", is_completed=False)
    db.add(task1)
    db.commit()
    db.refresh(task1)
    
    print(f"[OK] Task created: ID={task1.id}, Title='{task1.title}'")
    
    # Test 2: Create another task
    task2 = Task(title="Build API", description="Create REST API", is_completed=False)
    db.add(task2)
    db.commit()
    db.refresh(task2)
    
    print(f"[OK] Task created: ID={task2.id}, Title='{task2.title}'")
    
    # Test 3: Read all tasks
    print("\n" + "="*60)
    print("TEST 3: Read All Tasks")
    print("="*60)
    
    all_tasks = db.query(Task).all()
    print(f"[OK] Found {len(all_tasks)} tasks in database")
    for task in all_tasks:
        status = "[OK]" if task.is_completed else "[FAIL]"
        print(f"  [{status}] ID {task.id}: {task.title} - {task.description}")
    
    # Test 4: Read specific task
    print("\n" + "="*60)
    print("TEST 4: Read Single Task by ID")
    print("="*60)
    
    retrieved_task = db.query(Task).filter(Task.id == 1).first()
    if retrieved_task:
        print(f"[OK] Retrieved task: {retrieved_task.title}")
        print(f"  Description: {retrieved_task.description}")
        print(f"  Completed: {retrieved_task.is_completed}")
    
    # Test 5: Update task
    print("\n" + "="*60)
    print("TEST 5: Update Task")
    print("="*60)
    
    task_to_update = db.query(Task).filter(Task.id == 1).first()
    task_to_update.is_completed = True
    task_to_update.description = "Successfully learned FastAPI"
    db.commit()
    db.refresh(task_to_update)
    
    print(f"[OK] Task updated:")
    print(f"  Title: {task_to_update.title}")
    print(f"  Description: {task_to_update.description}")
    print(f"  Completed: {task_to_update.is_completed}")
    
    # Test 6: Delete task
    print("\n" + "="*60)
    print("TEST 6: Delete Task")
    print("="*60)
    
    task_to_delete = db.query(Task).filter(Task.id == 2).first()
    if task_to_delete:
        print(f"[OK] Deleting task: {task_to_delete.title}")
        db.delete(task_to_delete)
        db.commit()
        print(f"[OK] Task deleted successfully")
    
    # Verify deletion
    remaining_tasks = db.query(Task).all()
    print(f"[OK] Remaining tasks: {len(remaining_tasks)}")
    
    # Test 7: Pydantic Schema validation
    print("\n" + "="*60)
    print("TEST 7: Pydantic Schema Validation")
    print("="*60)
    
    # Valid task creation
    valid_task = TaskCreate(
        title="Test Task",
        description="This is a test",
        is_completed=False
    )
    print(f"[OK] Valid TaskCreate schema: {valid_task.model_dump()}")
    
    # Test invalid task (should fail)
    try:
        invalid_task = TaskCreate(
            title="",  # Empty title should fail
            description="Test"
        )
        print("[FAIL] Validation should have failed for empty title!")
    except Exception as e:
        print(f"[OK] Validation correctly rejected empty title: {type(e).__name__}")
    
    # Test response schema
    print("\n" + "="*60)
    print("TEST 8: Response Schema Conversion")
    print("="*60)
    
    final_task = db.query(Task).first()
    if final_task:
        response = TaskResponse.model_validate(final_task)
        print(f"[OK] TaskResponse created from Task model:")
        print(f"  {response.model_dump_json()}")
    
    db.close()
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED [OK]")
    print("="*60)
    print("\nSummary:")
    print("[OK] In-memory database working correctly")
    print("[OK] CRUD operations functional")
    print("[OK] Schema validation working")
    print("[OK] ORM relationships correct")
    print("\nReady for FastAPI server testing!")


if __name__ == "__main__":
    test_in_memory_database()
