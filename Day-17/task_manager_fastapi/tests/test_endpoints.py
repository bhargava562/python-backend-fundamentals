"""
FastAPI Integration Test Script
Tests all endpoints of the Task Manager API
"""

import asyncio
import sys
import os
# Add parent directory to path so we can import app module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Handle encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    print("\n" + "="*60)
    print("TEST: Health Check")
    print("="*60)
    response = client.get("/health/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("[PASS] Health check passed")


def test_create_task():
    print("\n" + "="*60)
    print("TEST: Create Task (POST /tasks/)")
    print("="*60)
    
    task_data = {
        "title": "Complete project",
        "description": "Finish the task manager implementation",
        "is_completed": False
    }
    
    response = client.post("/tasks/", json=task_data)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    assert data["title"] == "Complete project"
    assert "id" in data
    print(f"[PASS] Task created with ID: {data['id']}")
    return data["id"]


def test_get_all_tasks():
    print("\n" + "="*60)
    print("TEST: Get All Tasks (GET /tasks/)")
    print("="*60)
    
    response = client.get("/tasks/")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert response.status_code == 200
    print(f"[PASS] Retrieved {len(data)} tasks")
    return data


def test_get_single_task(task_id):
    print("\n" + "="*60)
    print(f"TEST: Get Single Task (GET /tasks/{task_id})")
    print("="*60)
    
    response = client.get(f"/tasks/{task_id}")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert response.status_code == 200
    assert data["id"] == task_id
    print(f"[PASS] Retrieved task: {data['title']}")


def test_get_nonexistent_task():
    print("\n" + "="*60)
    print("TEST: Get Non-existent Task (Error Handling)")
    print("="*60)
    
    response = client.get("/tasks/99999")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert response.status_code == 404
    print("[PASS] Correctly returned 404 for non-existent task")


def test_update_task(task_id):
    print("\n" + "="*60)
    print(f"TEST: Update Task (PUT /tasks/{task_id})")
    print("="*60)
    
    updated_data = {
        "title": "Complete project - UPDATED",
        "description": "This has been updated",
        "is_completed": True
    }
    
    response = client.put(f"/tasks/{task_id}", json=updated_data)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert response.status_code == 200
    assert data["title"] == "Complete project - UPDATED"
    assert data["is_completed"] == True
    print("[PASS] Task updated successfully")


def test_update_nonexistent_task():
    print("\n" + "="*60)
    print("TEST: Update Non-existent Task (Error Handling)")
    print("="*60)
    
    response = client.put("/tasks/99999", json={"title": "Test"})
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert response.status_code == 404
    print("[PASS] Correctly returned 404 for update non-existent task")


def test_delete_task(task_id):
    print("\n" + "="*60)
    print(f"TEST: Delete Task (DELETE /tasks/{task_id})")
    print("="*60)
    
    response = client.delete(f"/tasks/{task_id}")
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 204
    print("[PASS] Task deleted successfully")
    
    # Verify deletion
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    print("[PASS] Verified task no longer exists")


def test_delete_nonexistent_task():
    print("\n" + "="*60)
    print("TEST: Delete Non-existent Task (Error Handling)")
    print("="*60)
    
    response = client.delete("/tasks/99999")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert response.status_code == 404
    print("[PASS] Correctly returned 404 for delete non-existent task")


def test_validation_errors():
    print("\n" + "="*60)
    print("TEST: Input Validation")
    print("="*60)
    
    # Test empty title
    response = client.post("/tasks/", json={"title": "", "description": "Test"})
    print(f"Empty title - Status Code: {response.status_code}")
    assert response.status_code == 422  # Validation error
    print("[PASS] Correctly rejected empty title")
    
    # Test missing title
    response = client.post("/tasks/", json={"description": "Test"})
    print(f"Missing title - Status Code: {response.status_code}")
    assert response.status_code == 422
    print("[PASS] Correctly rejected missing title")


def test_multiple_tasks():
    print("\n" + "="*60)
    print("TEST: Multiple Tasks Operations")
    print("="*60)
    
    # Create 3 tasks
    task_ids = []
    for i in range(3):
        response = client.post("/tasks/", json={
            "title": f"Task {i+1}",
            "description": f"Description for task {i+1}",
            "is_completed": i % 2 == 0
        })
        assert response.status_code == 201
        task_ids.append(response.json()["id"])
    
    print(f"[PASS] Created {len(task_ids)} tasks: {task_ids}")
    
    # Get all tasks
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    print(f"[PASS] Retrieved {len(tasks)} total tasks")
    
    # Verify all tasks exist
    for task_id in task_ids:
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
    
    print(f"[PASS] All {len(task_ids)} tasks verified")


def main():
    print("\n" + "="*60)
    print("FASTAPI TASK MANAGER - ENDPOINT TESTS")
    print("="*60)
    
    try:
        # Health check
        test_health_check()
        
        # Create and test single task
        task_id = test_create_task()
        test_get_single_task(task_id)
        test_update_task(task_id)
        
        # Test deletion
        test_delete_task(task_id)
        
        # Test error handling
        test_get_nonexistent_task()
        test_update_nonexistent_task()
        test_delete_nonexistent_task()
        test_validation_errors()
        
        # Test multiple operations
        test_get_all_tasks()
        test_multiple_tasks()
        
        print("\n" + "="*60)
        print("ALL ENDPOINT TESTS PASSED!!!")
        print("="*60)
        print("\nSummary:")
        print("[PASS] Create (POST /tasks/) - Working")
        print("[PASS] Read All (GET /tasks/) - Working")
        print("[PASS] Read One (GET /tasks/{id}) - Working")
        print("[PASS] Update (PUT /tasks/{id}) - Working")
        print("[PASS] Delete (DELETE /tasks/{id}) - Working")
        print("[PASS] Error Handling (404, 422) - Working")
        print("[PASS] Input Validation - Working")
        print("[PASS] Health Check - Working")
        print("\nThe FastAPI Task Manager is fully functional!")
        
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        raise
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()
