# Task Manager FastAPI - Quick Start Guide

## Setup & Installation

```bash
# Navigate to project
cd Day-17/task_manager_fastapi

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies (if needed)
pip install -r requirements.txt
```

## Running Tests

```bash
# Test database operations
python -m tests.test_implementation

# Test API endpoints
python -m tests.test_endpoints

# Or run directly from tests directory
cd tests
python test_implementation.py
python test_endpoints.py
```

## Running the Server

```bash
# Start development server with auto-reload
uvicorn app.main:app --reload

# Access API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## API Quick Reference

### Create a Task
```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "is_completed": false
  }'
```

### List All Tasks
```bash
curl http://localhost:8000/tasks/
```

### Get Single Task
```bash
curl http://localhost:8000/tasks/1
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries - Updated",
    "description": "Milk, eggs, bread, cheese",
    "is_completed": true
  }'
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

### Health Check
```bash
curl http://localhost:8000/health/
```

## Project Structure

```
Day-17/task_manager_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI app + all endpoints
│   ├── models.py       # SQLAlchemy models
│   ├── schemas.py      # Pydantic validation
│   └── database.py     # Database setup
├── test_implementation.py  # Database tests
├── test_endpoints.py       # API tests
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## Key Features

✅ **Complete CRUD API** - Create, read, update, delete tasks
✅ **In-Memory Database** - Fast, no persistence needed
✅ **Error Handling** - Proper HTTP status codes
✅ **Input Validation** - Pydantic schema validation
✅ **Auto Documentation** - Swagger UI at /docs
✅ **Testing Suite** - Comprehensive test coverage

## Database

- **Type**: SQLite In-Memory
- **ORM**: SQLAlchemy
- **No migration needed** - Tables created automatically on startup

## Troubleshooting

**Issue**: Virtual environment not activating
```bash
# Try alternative activation
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Issue**: Port 8000 already in use
```bash
# Use different port
uvicorn app.main:app --port 8001
```

**Issue**: Tests fail with import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## Development Tips

- Hot reload is enabled by default with `--reload`
- Access Swagger UI for interactive API testing at `/docs`
- All endpoints use dependency injection for database access
- Pydantic validation happens automatically before handler execution

---

For detailed implementation report, see [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md)
