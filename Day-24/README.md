# Production-Ready Backend System - Complete Documentation

## 📖 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Project Structure](#project-structure)
5. [Configuration](#configuration)
6. [API Reference](#api-reference)
7. [Security Features](#security-features)
8. [Database Management](#database-management)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Monitoring & Logging](#monitoring--logging)
12. [Troubleshooting](#troubleshooting)
13. [Learning Resources](#learning-resources)

---

## Overview

**Zen** is a comprehensive, production-ready backend system demonstrating modern industry best practices for building scalable, secure, and maintainable APIs. This project synthesizes all Day 1-23 learning objectives into a complete, deployable system.

### Key Features

- ✅ **FastAPI** - Modern async web framework
- ✅ **PostgreSQL** - Reliable relational database with connection pooling
- ✅ **Redis** - In-memory caching and message broker
- ✅ **Celery** - Distributed background task processing
- ✅ **Structured Logging** - JSON-formatted logs with correlation tracking
- ✅ **Security** - CORS, rate limiting, secure headers, SQL injection prevention
- ✅ **Error Handling** - Global exception handlers with standardized responses
- ✅ **Health Monitoring** - Kubernetes-ready health check endpoints
- ✅ **Docker** - Multi-stage containerization with Compose orchestration
- ✅ **API Documentation** - Auto-generated Swagger/OpenAPI docs
- ✅ **Comprehensive Testing** - 20+ integration tests
- ✅ **Production Ready** - Designed for high-availability deployment

### Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Framework** | FastAPI | 0.104.1 |
| **Server** | Uvicorn | 0.24.0 |
| **Database** | PostgreSQL | 16-alpine |
| **Cache** | Redis | 7-alpine |
| **Tasks** | Celery | 5.3.4 |
| **Validation** | Pydantic | 2.5.0 |
| **Testing** | Pytest | 7.4.3 |
| **ORM** | SQLAlchemy | 2.0.23 |

---

## Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Applications                      │
│              (Web, Mobile, Third-Party Services)             │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │  Load Balancer/Proxy    │
        │  (Nginx/HAProxy)        │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────────────────────────┐
        │      FastAPI Web Application                │
        │  ┌──────────────────────────────────────┐   │
        │  │ • Request Middleware (Logging)      │   │
        │  │ • Security Middleware               │   │
        │  │ • Rate Limiting                     │   │
        │  │ • CORS Configuration                │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │ Routers (System & Business)         │   │
        │  │ • Health Checks                     │   │
        │  │ • Operations API                    │   │
        │  │ • Exception Handlers                │   │
        │  └──────────────────────────────────────┘   │
        └──────┬────────────────────────────────┬─────┘
               │                                │
    ┌──────────▼──────────┐         ┌──────────▼──────────┐
    │   PostgreSQL DB     │         │   Redis Cache       │
    │  ┌────────────────┐ │         │  ┌────────────────┐ │
    │  │ Connection     │ │         │  │ Connection     │ │
    │  │ Pool (20)      │ │         │  │ Pool (50)      │ │
    │  │ • Async Conn   │ │         │  │ • Message Q    │ │
    │  │ • Indices      │ │         │  │ • Cache Layer  │ │
    │  │ • Persistence  │ │         │  │ • Session      │ │
    │  └────────────────┘ │         │  └────────────────┘ │
    └─────────────────────┘         └────────────────────┘
                                             ▲
                                             │
                        ┌────────────────────┴────────────────┐
                        │                                     │
            ┌───────────▼──────────┐      ┌──────────────────▼──┐
            │  Celery Workers      │      │  Celery Beat       │
            │  (4 processes)       │      │  Scheduler         │
            │ • Background Tasks   │      │ • Periodic Tasks   │
            │ • Retry Logic        │      │ • Cron Jobs        │
            │ • Error Handling     │      │ • Task Management  │
            └──────────────────────┘      └────────────────────┘
```

### Request Flow

```
1. Client Request
   ↓
2. Middleware Pipeline
   - RequestID Assignment
   - Structured Logging
   ↓
3. Security & Rate Limiting
   - CORS Check
   - Rate Limit Check
   ↓
4. Router/Handler
   - Input Validation (Pydantic)
   - Database Operations
   - Cache Operations
   ↓
5. Background Tasks (Optional)
   - Dispatch to Celery
   ↓
6. Response
   - Structured Response
   - Correlation ID Header
   ↓
7. Logging & Monitoring
   - JSON Log Output
   - Metrics Collection
```

### Database Schema

```sql
Table: operational_logs
├── id (INT, PRIMARY KEY)
├── reference_id (VARCHAR(100), INDEX)
├── payload_summary (VARCHAR(500))
├── status (VARCHAR(50))
├── task_id (VARCHAR(100))
├── created_at (TIMESTAMP, INDEX)
├── updated_at (TIMESTAMP)
└── response_data (TEXT)

Indices:
├── idx_reference_id (reference_id)
└── idx_status_created (status, created_at)
```

---

## Quick Start

### Option 1: Docker Compose (Recommended - 5 minutes)

**Prerequisites**: Docker & Docker Compose installed

```bash
# 1. Navigate to project
cd Day-24

# 2. Start all services (PostgreSQL, Redis, FastAPI, Celery)
docker-compose up -d

# 3. Verify services are running
docker-compose ps

# 4. Check health
curl http://localhost:8000/api/v1/system/health

# 5. Access API documentation
open http://localhost:8000/docs
```

**Verify Setup:**
```bash
# Check database (using postgres_user credentials)
docker exec zenovox_postgres_prod psql -U postgres_user -d zenovox_db -c "SELECT 1"

# Check Redis
docker exec zenovox_redis_prod redis-cli ping

# Check API
curl http://localhost:8000/api/v1/system/version
```

### Option 2: Local Development (10 minutes)

**Prerequisites**: Python 3.12+, PostgreSQL 16+, Redis 7+

```bash
# 1. Navigate to project
cd Day-24

# 2. Activate virtual environment
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# 3. Ensure PostgreSQL and Redis are running
# Option A: Use Docker containers for DB/Redis only
docker run -d -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=myappdb \
  postgres:16-alpine

docker run -d -p 6379:6379 redis:7-alpine

# Option B: Use system-installed services
# Make sure postgres and redis services are running

# 4. Start FastAPI application
python run.py

# 5. In another terminal, start Celery worker
celery -A app.worker.celery_app worker --loglevel=info

# 6. In another terminal, start Celery Beat (optional)
celery -A app.worker.celery_app beat --loglevel=info

# 7. Access application
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Quick API Tests

**Test Health:**
```bash
curl http://localhost:8000/api/v1/system/health | python -m json.tool
```

**Create Operation:**
```bash
curl -X POST http://localhost:8000/api/v1/operations/process \
  -H "Content-Type: application/json" \
  -d '{
    "reference_id": "TX-001",
    "summary": "Test operation"
  }' | python -m json.tool
```

**List Operations:**
```bash
curl http://localhost:8000/api/v1/operations/operations | python -m json.tool
```

**Get Version:**
```bash
curl http://localhost:8000/api/v1/system/version
```

---

## Project Structure

```
Day-24/
│
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application factory
│   ├── config.py                # Environment configuration (Pydantic)
│   ├── database.py              # Async SQLAlchemy setup
│   ├── models.py                # Database ORM models
│   ├── redis_client.py          # Redis connection pool
│   ├── worker.py                # Celery configuration
│   ├── tasks.py                 # Background task definitions
│   ├── schemas.py               # Pydantic validation models
│   │
│   ├── middleware/              # Cross-cutting concerns
│   │   ├── __init__.py
│   │   ├── logging_mw.py       # Structured JSON logging
│   │   └── security_headers.py # Security headers middleware
│   │
│   ├── exceptions/              # Global error handling
│   │   ├── __init__.py
│   │   └── handlers.py         # Exception handlers
│   │
│   └── routers/                 # API route handlers
│       ├── __init__.py
│       ├── system.py           # Health, version, info endpoints
│       └── business.py         # Core business operations
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   └── test_api.py            # Integration tests (20+)
│
├── Configuration Files
│   ├── .env                    # Development environment (local values)
│   ├── .env.example            # Production template
│   ├── .gitignore             # Git ignore patterns
│   ├── requirements.txt        # Python dependencies
│   └── pytest.ini             # Pytest configuration
│
├── Deployment Files
│   ├── Dockerfile             # Multi-stage Docker build
│   ├── docker-compose.yml     # Complete stack orchestration
│   └── run.py                 # Development server runner
│
└── Documentation
    └── README.md              # This file - comprehensive guide

Key Statistics:
├── Python Files: 20+
├── Lines of Code: 2,500+
├── API Endpoints: 9
├── Test Cases: 20+
├── Docker Services: 5
└── Documentation: Complete
```

---

## Configuration

### Environment Variables

All configuration is managed through environment variables in `.env` file:

```bash
# Application Settings
ENV=development                    # Environment: development, staging, production
PROJECT_NAME="Zenovox..."         # Project display name
VERSION=1.0.0                      # Application version

# Database Configuration - MATCHES docker-compose.yml PostgreSQL service
DATABASE_URL=postgresql+asyncpg://postgres_user:postgres_password@localhost:5432/zenovox_db

# Redis Configuration - MATCHES docker-compose.yml Redis service
REDIS_URL=redis://localhost:6379/0

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Security
SECRET_KEY=dev-secret-key-change-in-production-12345678

# API Configuration
ALLOWED_HOSTS=*
RATE_LIMIT_RULE="1000 per minute"

# Database Connection Pool
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=1800
```

### Environment Profiles

**Development** (`.env`):
```env
ENV=development
ALLOWED_HOSTS=*
RATE_LIMIT_RULE="1000 per minute"
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/myappdb
```

**Production** (`.env.example` template):
```env
ENV=production
ALLOWED_HOSTS=api.example.com
RATE_LIMIT_RULE="100 per minute"
SECRET_KEY=<generate_random_32_char_string>
DATABASE_URL=postgresql+asyncpg://user:secure_password@db.example.com:5432/db
```

### Generate Production Secrets

```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Or using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## API Reference

### Base URL
```
http://localhost:8000/api/v1
```

### System Endpoints

#### GET /system/health
Full infrastructure health check

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": 1700000000.0,
  "version": "1.0.0",
  "checks": {
    "postgres": "healthy",
    "redis": "healthy"
  }
}
```

**Response (503 - degraded):**
```json
{
  "status": "degraded",
  "timestamp": 1700000000.0,
  "version": "1.0.0",
  "checks": {
    "postgres": "healthy",
    "redis": "unhealthy: ConnectionError"
  }
}
```

#### GET /system/version
Get application version and environment

**Response (200):**
```json
{
  "version": "1.0.0",
  "project_name": "Zenovox Production API",
  "environment": "development",
  "timestamp": 1700000000.0
}
```

#### GET /system/info
Get application configuration information

**Response (200):**
```json
{
  "project_name": "Zenovox Production API",
  "version": "1.0.0",
  "environment": "development",
  "database": {
    "pool_size": 5,
    "max_overflow": 10
  },
  "features": {
    "rate_limiting": true,
    "async_tasks": true,
    "caching": true,
    "structured_logging": true
  },
  "timestamp": 1700000000.0
}
```

#### GET /system/ready
Kubernetes readiness probe

**Response (200):**
```json
{
  "ready": true,
  "timestamp": 1700000000.0
}
```

#### GET /system/live
Kubernetes liveness probe

**Response (200):**
```json
{
  "alive": true,
  "timestamp": 1700000000.0
}
```

### Business Operations Endpoints

#### POST /operations/process
Dispatch a background operation

**Request:**
```json
{
  "reference_id": "TX-12345",
  "summary": "Process user data batch"
}
```

**Response (202):**
```json
{
  "reference_id": "TX-12345",
  "task_id": "abc123def456-ghi789-jkl",
  "status": "queued_for_worker_processing"
}
```

#### GET /operations/operations
List all operations with pagination

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 10, max: 100)
- `status_filter` (str): Filter by status (pending, success, failed)

**Response (200):**
```json
[
  {
    "id": 1,
    "reference_id": "TX-12345",
    "payload_summary": "Process user data batch",
    "status": "pending",
    "task_id": "abc123def456",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00",
    "response_data": null
  }
]
```

#### GET /operations/operations/{reference_id}
Get specific operation details

**Response (200):**
```json
{
  "id": 1,
  "reference_id": "TX-12345",
  "payload_summary": "Process user data batch",
  "status": "pending",
  "task_id": "abc123def456",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00",
  "response_data": null
}
```

**Response (404):**
```json
{
  "error": "Operation TX-NOTFOUND not found"
}
```

#### GET /operations/task-status/{task_id}
Get task execution status

**Response (200):**
```json
{
  "task_id": "abc123def456",
  "reference_id": "TX-12345",
  "status": "success",
  "result": {
    "status": "SUCCESS",
    "id": "TX-12345",
    "processed_at": 1700000000.0
  }
}
```

#### POST /operations/batch-process
Process multiple operations in batch

**Request:**
```json
[
  {
    "reference_id": "TX-001",
    "summary": "First batch item"
  },
  {
    "reference_id": "TX-002",
    "summary": "Second batch item"
  }
]
```

**Response (202):**
```json
{
  "batch_size": 2,
  "tasks": [
    {
      "reference_id": "TX-001",
      "task_id": "task-id-1"
    },
    {
      "reference_id": "TX-002",
      "task_id": "task-id-2"
    }
  ]
}
```

### Error Responses

#### 422 Validation Error
```json
{
  "error_code": "SCHEMA_VALIDATION_ERROR",
  "message": "Supplied input variables failed serialization bounds.",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "details": [
    {
      "field": "reference_id",
      "type": "string_too_short",
      "message": "String should have at least 5 characters"
    }
  ]
}
```

#### 500 Server Error
```json
{
  "error_code": "INTERNAL_SERVER_ERROR",
  "message": "An unexpected error occurred while processing your request.",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 503 Service Unavailable
```json
{
  "error_code": "SERVICE_UNAVAILABLE",
  "message": "Critical service degradation detected.",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "details": {
    "redis": "unhealthy: ConnectionError"
  }
}
```

---

## Security Features

### Implemented Protections

#### 1. CORS (Cross-Origin Resource Sharing)
```python
# Configured in app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

**Production Configuration:**
```python
allow_origins=["api.example.com", "www.example.com"]
```

#### 2. Rate Limiting
**Per-IP rate limiting using SlowAPI:**

```
60 requests per minute (development)
100 requests per minute (production)
```

**Applied to:** All endpoints
**Tracked by:** Client IP address

#### 3. SQL Injection Prevention
**Method:** Parameterized queries via SQLAlchemy

```python
# Safe - parameterized
await db.execute(
    select(OperationalLog).where(OperationalLog.reference_id == reference_id)
)

# Unsafe - DO NOT USE
query = f"SELECT * FROM operational_logs WHERE reference_id = '{reference_id}'"
```

#### 4. XSS (Cross-Site Scripting) Prevention
**Security Headers:**
- `Content-Security-Policy` - Restricts resource loading
- `X-XSS-Protection` - XSS protection in older browsers
- `X-Content-Type-Options: nosniff` - MIME type sniffing prevention

#### 5. Secure Headers
Implemented in `app/middleware/security_headers.py`:

| Header | Value | Purpose |
|--------|-------|---------|
| X-Frame-Options | DENY | Clickjacking protection |
| X-Content-Type-Options | nosniff | MIME sniffing prevention |
| X-XSS-Protection | 1; mode=block | XSS protection |
| Strict-Transport-Security | max-age=31536000 | Force HTTPS |
| Referrer-Policy | strict-origin-when-cross-origin | Referrer control |
| Permissions-Policy | camera=(), microphone=() | Browser feature access |

#### 6. Secrets Management
**Best Practices:**
- ✅ All secrets in environment variables
- ✅ `.env` file in `.gitignore`
- ✅ `.env.example` for templates
- ✅ Different secrets per environment

**Production:** Use AWS Secrets Manager, HashiCorp Vault, or similar

#### 7. Request Correlation Tracking
**Purpose:** Trace requests across system

```
Header: X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440000
```

**Benefits:**
- Link logs across services
- Debug request flows
- Monitor performance
- Troubleshoot issues

#### 8. Non-Root Container Execution
**Dockerfile:**
```dockerfile
RUN useradd -u 8888 apprunner
USER apprunner
```

**Benefit:** Limited privileges in case of container breach

### Security Checklist

- [ ] Generate new SECRET_KEY: `openssl rand -hex 32`
- [ ] Update ALLOWED_HOSTS for production domain
- [ ] Configure HTTPS/TLS certificate
- [ ] Set up Web Application Firewall (WAF)
- [ ] Enable database encryption at rest
- [ ] Configure database backups
- [ ] Set up monitoring and alerting
- [ ] Implement API authentication (JWT/OAuth2)
- [ ] Regular security audits
- [ ] Dependency vulnerability scanning (e.g., `safety`, `pip-audit`)

---

## Database Management

### PostgreSQL Setup

**Connection Details (from .env and docker-compose.yml):**
```
Host: localhost
Port: 5432
User: postgres_user
Password: postgres_password
Database: zenovox_db
```

**Connection String:**
```
postgresql+asyncpg://postgres_user:postgres_password@localhost:5432/zenovox_db
```

### Tables

#### operational_logs
```sql
CREATE TABLE operational_logs (
    id SERIAL PRIMARY KEY,
    reference_id VARCHAR(100) NOT NULL,
    payload_summary VARCHAR(500),
    status VARCHAR(50) DEFAULT 'pending',
    task_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    response_data TEXT
);

CREATE INDEX idx_reference_id ON operational_logs(reference_id);
CREATE INDEX idx_status_created ON operational_logs(status, created_at);
```

### Connection Pooling

**Configuration:**
```
Pool Size: 5 (development), 20 (production)
Max Overflow: 10
Pool Timeout: 30 seconds
Pool Recycle: 1800 seconds (30 minutes)
```

**Benefits:**
- Reuse connections
- Prevent connection exhaustion
- Improve performance
- Handle concurrent requests

### Database Operations

**Initialize Database:**
```bash
# Using Docker Compose
docker-compose exec web python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"

# Or using Python script
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
```

**Backup Database:**
```bash
# Docker container
docker exec zenovox_postgres_prod pg_dump -U postgres_user zenovox_db > backup.sql

# System-installed PostgreSQL
pg_dump -U postgres_user zenovox_db > backup.sql
```

**Restore Database:**
```bash
# Docker container
docker exec -i zenovox_postgres_prod psql -U postgres_user zenovox_db < backup.sql

# System-installed PostgreSQL
psql -U postgres_user zenovox_db < backup.sql
```

**Connect to Database:**
```bash
# Docker container
docker exec -it zenovox_postgres_prod psql -U postgres_user -d zenovox_db

# System-installed PostgreSQL
psql -U postgres_user -d zenovox_db
```

---

## Testing

### Run Tests

```bash
# All tests
pytest

# With coverage report
pytest --cov=app

# Verbose output
pytest -v

# Specific test file
pytest tests/test_api.py

# Specific test class
pytest tests/test_api.py::TestSystemEndpoints -v

# Specific test
pytest tests/test_api.py::TestSystemEndpoints::test_health_endpoint -v

# Watch mode (requires pytest-watch)
pytest-watch

# Stop on first failure
pytest -x

# Show print statements
pytest -s
```

### Test Coverage

**Current Coverage:**
- System endpoints: 5 tests
- Business endpoints: 7 tests
- Error handling: 4 tests
- Security: 4 tests
- Total: 20+ tests

**Coverage Report:**
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

### Test Structure

```
tests/
├── conftest.py           # Fixtures and configuration
│   ├── test_db()        # In-memory SQLite database
│   ├── async_test_client()  # AsyncClient fixture
│
└── test_api.py           # Test cases
    ├── TestSystemEndpoints  # Health, version, info tests
    ├── TestBusinessEndpoints # Operations, tasks tests
    ├── TestErrorHandling  # Error response tests
    ├── TestCORSHeaders    # CORS header tests
    └── TestSecurityHeaders # Security header tests
```

### Example Test

```python
@pytest.mark.asyncio
async def test_health_endpoint(async_test_client):
    """Test deep infrastructure health check"""
    response = await async_test_client.get("/api/v1/system/health")
    assert response.status_code in [200, 503]
    
    data = response.json()
    assert "status" in data
    assert "checks" in data
```

---

## Deployment

### Docker Compose Deployment (Development/Staging)

**Start Services:**
```bash
docker-compose up -d
```

**Stop Services:**
```bash
docker-compose down
```

**Scale Services:**
```bash
# Multiple API instances
docker-compose up -d --scale web=3

# Multiple Celery workers
docker-compose up -d --scale celery_worker=8
```

**View Logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery_worker

# Follow recent logs
docker-compose logs --tail=100 -f
```

**Access Services:**
| Service | Port | URL |
|---------|------|-----|
| FastAPI | 8000 | http://localhost:8000 |
| PostgreSQL | 5432 | localhost:5432 |
| Redis | 6379 | localhost:6379 |
| Swagger UI | 8000 | http://localhost:8000/docs |

### Docker Compose File

**Services Included:**
1. **PostgreSQL** - Database (port 5432)
2. **Redis** - Cache & broker (port 6379)
3. **FastAPI Web** - API server (port 8000)
4. **Celery Worker** - Background task processor
5. **Celery Beat** - Task scheduler

**Key Configuration:**
- Health checks for each service
- Service dependencies (web depends on db & redis)
- Volume persistence
- Network isolation
- Logging configuration
- Environment variables

### Manual Deployment

**Prerequisites:**
- Python 3.12+
- PostgreSQL 16+
- Redis 7+

**Steps:**
```bash
# 1. Clone repository
cd Day-24

# 2. Create venv
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with production values

# 5. Initialize database
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"

# 6. Run application
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# 7. Run Celery (separate terminal)
celery -A app.worker.celery_app worker --loglevel=info
```

### Kubernetes Deployment

**Health Check Configuration:**

```yaml
livenessProbe:
  httpGet:
    path: /api/v1/system/live
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /api/v1/system/ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
```

**Resource Limits:**
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "500m"
  limits:
    memory: "512Mi"
    cpu: "1000m"
```

### Health Verification

**Immediate Checks:**
```bash
# Health check
curl http://localhost:8000/api/v1/system/health

# Version
curl http://localhost:8000/api/v1/system/version

# Readiness
curl http://localhost:8000/api/v1/system/ready

# Liveness
curl http://localhost:8000/api/v1/system/live
```

**Verify Services:**
```bash
# Docker compose
docker-compose ps

# Database connection
docker exec zenovox_postgres_prod psql -U postgres -c "SELECT 1"

# Redis connection
docker exec zenovox_redis_prod redis-cli ping

# API endpoint
curl -X POST http://localhost:8000/api/v1/operations/process \
  -H "Content-Type: application/json" \
  -d '{"reference_id": "TEST-001", "summary": "Test"}'
```

---

## Monitoring & Logging

### Structured Logging

**Format:** JSON to stdout

```json
{
  "timestamp": 1700000000.0,
  "level": "INFO",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "method": "POST",
  "path": "/api/v1/operations/process",
  "status_code": 202,
  "latency_ms": 45.23,
  "client_ip": "192.168.1.1",
  "user_agent": "Mozilla/5.0..."
}
```

**Log Levels:**
- **DEBUG** - Detailed diagnostic info
- **INFO** - General informational messages
- **WARNING** - Warning messages for potential issues
- **ERROR** - Error messages for failures
- **CRITICAL** - Critical errors requiring immediate attention

### Correlation ID Tracking

**Purpose:** Link requests across system

```
Request Header: X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440000
Response Header: X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440000
```

### Metrics to Monitor

#### Application Metrics
- HTTP request rate (requests/sec)
- Response time (p50, p95, p99)
- Error rate (errors/sec)
- Error distribution by type

#### Database Metrics
- Connection pool usage
- Active connections
- Query execution time
- Query count per endpoint

#### Cache Metrics
- Cache hit rate
- Cache miss rate
- Memory usage
- Keys in cache

#### Background Tasks
- Queue depth
- Task processing time
- Failed task rate
- Worker utilization

### Log Aggregation

**Docker Compose Logging:**
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "5"
```

**Collect Logs:**
```bash
# Real-time stream
docker-compose logs -f

# View recent logs
docker-compose logs --tail=100

# Export logs
docker-compose logs > logs.txt
```

### Monitoring Tools

**Recommended:**
- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **ELK Stack** - Log aggregation (Elasticsearch, Logstash, Kibana)
- **Splunk** - Enterprise logging
- **DataDog** - APM and monitoring
- **New Relic** - Performance monitoring

---

## Troubleshooting

### Service Won't Start

**Check Logs:**
```bash
docker-compose logs web
docker-compose logs db
docker-compose logs redis
```

**Verify Dependencies:**
```bash
# Check if ports are in use
lsof -i :8000  # FastAPI
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis

# Or on Windows
netstat -ano | findstr :8000
```

**Solution:**
```bash
# Kill process on port
# Linux/Mac
kill -9 <PID>

# Windows
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### Database Connection Issues

**Test Connection:**
```bash
# Docker container
docker exec zenovox_postgres_prod psql -U postgres_user -d zenovox_db -c "SELECT 1"

# System PostgreSQL
psql -U postgres_user -d zenovox_db -c "SELECT 1"
```

**Common Issues:**
1. **Wrong credentials** - Check DATABASE_URL in .env
2. **Connection refused** - Ensure PostgreSQL is running
3. **Pool exhausted** - Increase DB_POOL_SIZE
4. **Connection timeout** - Increase DB_POOL_TIMEOUT

**Solutions:**
```bash
# Restart database
docker-compose restart db

# Increase pool size
# Edit .env: DB_POOL_SIZE=20

# Check PostgreSQL status
docker logs zenovox_postgres_prod

# Reset database
docker-compose down -v  # WARNING: Deletes data!
docker-compose up -d db
```

### Redis Connection Issues

**Test Connection:**
```bash
docker exec zenovox_redis_prod redis-cli ping
```

**Common Issues:**
1. **Connection refused** - Redis not running
2. **Out of memory** - Increase Redis memory limit
3. **Key expired** - Check TTL settings

**Solutions:**
```bash
# Restart Redis
docker-compose restart redis

# Clear Redis (WARNING: loses data)
docker exec zenovox_redis_prod redis-cli FLUSHDB

# Check memory
docker exec zenovox_redis_prod redis-cli INFO memory

# Monitor keys
docker exec zenovox_redis_prod redis-cli MONITOR
```

### High Memory/CPU Usage

**Identify Problem:**
```bash
# Check container stats
docker stats

# Check process inside container
docker exec zenovox_api_service top

# Check database connections
docker exec zenovox_postgres_prod psql -U postgres_user -d zenovox_db -c "SELECT count(*) FROM pg_stat_activity"
```

**Solutions:**
```bash
# Scale API instances
docker-compose up -d --scale web=5

# Reduce connection pool
# Edit .env: DB_POOL_SIZE=5

# Restart container
docker-compose restart web

# Check for memory leaks
docker logs zenovox_api_service | grep -i memory
```

### Task Processing Issues

**Check Celery Worker:**
```bash
docker-compose logs celery_worker

# Check task queue
docker exec zenovox_redis_prod redis-cli LLEN celery
```

**Common Issues:**
1. **Tasks not processing** - Worker not running
2. **Task queue backing up** - Need more workers
3. **Tasks failing** - Check error logs

**Solutions:**
```bash
# Start worker
docker-compose up -d celery_worker

# Scale workers
docker-compose up -d --scale celery_worker=8

# Clear failed tasks
docker exec zenovox_redis_prod redis-cli DEL celery_failed

# Restart workers
docker-compose restart celery_worker
```

### API Response Issues

**Test Endpoint:**
```bash
curl -v http://localhost:8000/api/v1/system/health

# With timing
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/v1/system/health
```

**Common Issues:**
1. **Connection refused** - API not running
2. **Timeout** - Slow database/cache
3. **Invalid response** - Check logs

**Solutions:**
```bash
# Restart API
docker-compose restart web

# Check logs
docker-compose logs -f web

# Test database
curl http://localhost:8000/api/v1/system/health | jq '.checks.postgres'

# Load testing
ab -n 100 -c 10 http://localhost:8000/api/v1/system/health
```

### Rollback Deployment

**Steps:**
```bash
# 1. Stop current version
docker-compose down

# 2. Restore previous image
docker tag zenovox:v1.0.0_backup zenovox:latest

# 3. Restore database backup
docker-compose up -d db
docker exec -i zenovox_postgres_prod psql -U postgres < backup_v1.0.0.sql

# 4. Start services
docker-compose up -d

# 5. Verify health
curl http://localhost:8000/api/v1/system/health
```

---

## Learning Resources

### FastAPI
- [Official Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/deployment/concepts/)
- [Async SQLAlchemy Guide](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

### PostgreSQL
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Connection Pooling Guide](https://wiki.postgresql.org/wiki/Number_Of_Database_Connections)
- [Query Optimization](https://www.postgresql.org/docs/current/performance-tips.html)

### Redis
- [Redis Documentation](https://redis.io/documentation)
- [Redis Best Practices](https://redis.io/docs/management/admin-guide/)
- [Redis CLI Reference](https://redis.io/commands/)

### Celery
- [Celery Documentation](https://docs.celeryproject.org/)
- [Task Patterns](https://docs.celeryproject.org/en/stable/userguide/canvas/)
- [Celery Beat Scheduler](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html)

### Docker
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### Architecture & Design
- [12 Factor App](https://12factor.net/)
- [Backend Architecture Patterns](https://github.com/donnemartin/system-design-primer)
- [Production Readiness Checklist](https://www.gruntwork.io/blog/production-grade-infrastructure/)

### Testing
- [Pytest Documentation](https://docs.pytest.org/)
- [Async Testing Guide](https://docs.pytest.org/en/7.1.x/how-to-pytest-async-tests.html)

---

## Summary

**Zenovox** is a complete, production-ready backend system that brings together all learning objectives from Days 1-23:

✅ Modern async framework (FastAPI)  
✅ Reliable database (PostgreSQL with pooling)  
✅ High-performance caching (Redis)  
✅ Background task processing (Celery)  
✅ Comprehensive security  
✅ Structured logging and monitoring  
✅ Full containerization  
✅ Production deployment readiness  
✅ Complete test coverage  
✅ Professional documentation  

**Ready for Production?** Check the deployment section and follow the health verification checklist.

**Need Help?** See the Troubleshooting section or consult the Learning Resources.

---

**Last Updated**: May 2024  
**Version**: 1.0.0  
**Status**: Production Ready ✅

