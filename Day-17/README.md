# Day 17 - Task Manager API in FastAPI and Django

## Executive Summary
This day includes the same Task Manager API implemented in two frameworks:

- FastAPI implementation: lightweight, async-friendly API with in-memory SQLite.
- Django implementation: Django REST Framework API with SQLite and standard Django project structure.

Both implementations expose the same core CRUD behavior and health endpoint, enabling direct comparison of development style, ecosystem fit, and runtime characteristics.

## Project Scope

Implemented API capabilities (both stacks):

- Create task
- List tasks
- Get task by ID
- Update task by ID
- Delete task by ID
- Health check endpoint
- Input validation and error handling (404 for missing resources, 422-style validation responses)

Task schema used in both:

- id: integer
- title: string (required, min length 1, max length 200)
- description: string (optional, max length 1000)
- is_completed: boolean (default false)

## Directory Layout

- Day-17/task_manager_fastapi: FastAPI version
- Day-17/task_manager_django: Django + DRF version

## Unified API Contract (Implemented in Both)

| Method | Route | Purpose | Success Code | Error Cases |
|---|---|---|---|---|
| GET | /health/ | Health check | 200 | - |
| POST | /tasks/ | Create task | 201 | 422 invalid payload |
| GET | /tasks/ | List tasks | 200 | - |
| GET | /tasks/{id} | Get one task | 200 | 404 not found |
| PUT | /tasks/{id} | Update one task | 200 | 404 not found, 422 invalid payload |
| DELETE | /tasks/{id} | Delete one task | 204 | 404 not found |

Notes:

- Django detail route is defined as /tasks/<int:task_id> (works as /tasks/1).
- FastAPI detail route is /tasks/{task_id} (works as /tasks/1).

## Implementation Notes

### FastAPI Version

- Framework: FastAPI
- ORM/DB: SQLAlchemy with SQLite in-memory database using StaticPool
- Validation: Pydantic schemas
- Pattern: dependency injection via get_db
- Key strength in this implementation: very explicit API-first structure and concise endpoint code

### Django Version

- Framework: Django + Django REST Framework
- ORM/DB: Django ORM with SQLite database
- Validation: DRF serializers
- Pattern: APIView-based endpoints
- Key strength in this implementation: batteries-included architecture and extensibility into full web platform features

## Performance Comparison Report (Measured)

### Methodology

Benchmark type:

- Local in-process benchmark using framework test clients
- Same machine, sequential request loop
- Not a network benchmark (no reverse proxy, no multi-worker server)
- Primary goal: relative comparison inside this project setup

Runs:

- 500 iterations for read/update endpoints
- 300 iterations for POST+DELETE write cycle

Environment snapshot:

- Windows local dev machine
- FastAPI app from Day-17/task_manager_fastapi
- Django app from Day-17/task_manager_django

### Metrics

| Framework | Endpoint | Iterations | Avg (ms) | P50 (ms) | P95 (ms) | Throughput (req/s) |
|---|---|---:|---:|---:|---:|---:|
| FastAPI | GET /health/ | 500 | 4.629 | 2.764 | 15.392 | 216.01 |
| Django | GET /health/ | 500 | 1.108 | 0.908 | 2.088 | 902.21 |
| FastAPI | GET /tasks/ | 500 | 8.791 | 6.778 | 24.266 | 113.75 |
| Django | GET /tasks/ | 500 | 1.416 | 1.236 | 2.415 | 706.33 |
| FastAPI | GET /tasks/{id} | 500 | 12.661 | 12.595 | 15.081 | 78.98 |
| Django | GET /tasks/{id} | 500 | 1.792 | 1.416 | 3.761 | 557.97 |
| FastAPI | PUT /tasks/{id} | 500 | 15.228 | 15.049 | 17.088 | 65.67 |
| Django | PUT /tasks/{id} | 500 | 3.449 | 3.384 | 5.303 | 289.90 |
| FastAPI | POST+DELETE cycle | 300 | 27.106 | 27.138 | 33.011 | 36.89 |
| Django | POST+DELETE cycle | 300 | 23.372 | 23.278 | 26.810 | 42.79 |

### Interpretation

- In this local in-process benchmark, Django is faster across measured endpoints.
- The absolute values should not be treated as production SLO metrics.
- For production-grade conclusions, rerun with real HTTP load tooling, concurrency, warmed workers, and identical deployment topology.

## Feature Comparison Matrix

| Capability | FastAPI Implementation | Django Implementation | Notes |
|---|---|---|---|
| CRUD endpoints | Yes | Yes | Functionally aligned |
| Health endpoint | Yes | Yes | Functionally aligned |
| Input validation | Pydantic | DRF Serializer | Both enforce required title and field limits |
| Error handling | HTTPException responses | DRF Response with status | Both return 404 for missing task |
| ORM layer | SQLAlchemy | Django ORM | Both straightforward for this scope |
| Data store used here | In-memory SQLite | SQLite file DB | FastAPI data resets with process |
| Automatic docs UI | Native Swagger/ReDoc | Not enabled by default here | DRF browsable API available with additional setup |
| Async-first ergonomics | Strong | Moderate | FastAPI is async-native |
| Built-in admin/auth ecosystem | Minimal by default | Strong | Django includes admin/auth stack |
| Learning curve for simple API | Low to moderate | Moderate | Depends on prior framework exposure |

## Use Case Recommendations (FastAPI vs Django)

### Choose FastAPI when

- You are building API-first microservices.
- You need async endpoints and high developer productivity for typed APIs.
- You want automatic OpenAPI docs out of the box with minimal setup.
- Your architecture favors smaller focused services over monolith features.

### Choose Django when

- You expect to need admin panels, auth workflows, permissions, and mature built-in modules.
- You are building a larger full-stack business app where web + API concerns coexist.
- You prefer convention-driven structure and long-term maintainability in a larger codebase.
- Your team already has strong Django expertise.

### Practical guidance for this project

- For interview/demo of modern API-first development: FastAPI is excellent.
- For enterprise-style extensibility with admin/users/permissions likely to grow: Django is safer.
- If API performance is a priority, validate in production-like benchmarks before deciding solely from local test-client results.

## How to Run

### FastAPI app

1. Open directory: Day-17/task_manager_fastapi
2. Activate environment
3. Install dependencies from requirements.txt
4. Run: uvicorn app.main:app --reload

### Django app

1. Open directory: Day-17/task_manager_django
2. Activate local environment at task_manager_django/venv
3. Install dependencies from requirements.txt
4. Run migrations: python manage.py migrate
5. Run server: python manage.py runserver

## Deliverables Completed

- Same API implemented in FastAPI and Django
- Performance comparison report with measured metrics
- Feature comparison matrix
- Use-case recommendation guide (FastAPI vs Django)

This README serves as the consolidated professional documentation for the Day 17 dual-framework implementation.
