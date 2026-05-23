# Zenovox: Production-Ready Backend System

Complete end-to-end implementation of a production-ready backend system with modern architecture, comprehensive logging, security, and deployment best practices.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                 Client Applications                  │
├─────────────────────────────────────────────────────┤
│  API Gateway / Load Balancer (Nginx/HAProxy)        │
├──────────────────┬──────────────────────────────────┤
│   FastAPI Web    │    System Monitoring & Health    │
│   Services (4)   │    - Health Checks              │
│   - CORS         │    - Readiness/Liveness        │
│   - Rate Limit   │    - Version Info              │
│   - Logging      │                                 │
├──────────────────┴──────────────────────────────────┤
│  Application Services                                │
│  ├─ Business Routers                                │
│  ├─ Exception Handlers                              │
│  ├─ Middleware Stack                                │
│  └─ Database Session Management                     │
├──────────────────┬──────────────────────────────────┤
│   PostgreSQL     │  Redis Cluster                   │
│   (Primary DB)   │  - Caching Layer               │
│   - Connection   │  - Message Broker              │
│     Pool (20)    │  - Session Store               │
│   - Async Conn   │  - Rate Limit State            │
├──────────────────┴──────────────────────────────────┤
│  Celery Worker Pool (4-8 processes)                │
│  ├─ Background Task Execution                      │
│  ├─ Async Job Processing                           │
│  ├─ Retry & Error Handling                         │
│  └─ Result Backend (Redis)                         │
└─────────────────────────────────────────────────────┘
```

## 📋 Project Structure

```
day24_production_system/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application factory
│   ├── config.py               # Environment configuration (Pydantic)
│   ├── database.py             # Async SQLAlchemy setup
│   ├── models.py               # Database models
│   ├── redis_client.py         # Redis connection pool
│   ├── worker.py               # Celery configuration
│   ├── tasks.py                # Background tasks
│   ├── schemas.py              # Request/Response schemas
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── logging_mw.py       # Structured JSON logging
│   │   └── security_headers.py # Security headers
│   │
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── handlers.py         # Global exception handlers
│   │
│   └── routers/
│       ├── __init__.py
│       ├── system.py           # Health, version, info endpoints
│       └── business.py         # Core business operations
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures and configuration
│   └── test_api.py            # Integration tests
│
├── .env                        # Environment variables (development)
├── .env.example               # Environment template
├── Dockerfile                 # Multi-stage production build
├── docker-compose.yml         # Complete stack orchestration
├── requirements.txt           # Python dependencies
│
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.12+
- PostgreSQL 14+
- Redis 7+

### Local Development Setup

1. **Clone and navigate to directory:**
   ```bash
   cd Day-24
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

5. **Run application (requires PostgreSQL and Redis running):**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access API:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - API: http://localhost:8000

### Docker Compose Deployment

**Start complete stack:**
```bash
docker-compose up -d
```

**Stop stack:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f web
```

**Access services:**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## 🔧 Configuration Management

### Environment Variables

Configure via `.env` file (template: `.env.example`):

```env
# Application
ENV=production
PROJECT_NAME="Zenovox Production System"
VERSION=1.0.0

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=generate_with_openssl_rand_hex_32

# Hosting
ALLOWED_HOSTS=api.example.com,localhost

# Rate Limiting
RATE_LIMIT_RULE="100 per minute"
```

### Environment Profiles

**Development:**
```env
ENV=development
ALLOWED_HOSTS=*
RATE_LIMIT_RULE="1000 per minute"
```

**Production:**
```env
ENV=production
ALLOWED_HOSTS=api.zenovox.com
RATE_LIMIT_RULE="100 per minute"
SECRET_KEY=<generate_new_random_key>
```

## 📚 API Documentation

### Core Endpoints

#### System Health & Info

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/system/health` | Deep infrastructure health check |
| GET | `/api/v1/system/version` | Get application version |
| GET | `/api/v1/system/info` | Application configuration info |
| GET | `/api/v1/system/ready` | Kubernetes readiness check |
| GET | `/api/v1/system/live` | Kubernetes liveness check |

#### Business Operations

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/operations/process` | Dispatch background operation |
| GET | `/api/v1/operations/operations` | List all operations |
| GET | `/api/v1/operations/operations/{ref_id}` | Get operation details |
| GET | `/api/v1/operations/task-status/{task_id}` | Get task status |
| POST | `/api/v1/operations/batch-process` | Process multiple operations |

### Example Requests

**Dispatch Operation:**
```bash
curl -X POST http://localhost:8000/api/v1/operations/process \
  -H "Content-Type: application/json" \
  -d '{
    "reference_id": "TX-12345",
    "summary": "Process user batch data"
  }'
```

**Check Health:**
```bash
curl http://localhost:8000/api/v1/system/health
```

**List Operations:**
```bash
curl http://localhost:8000/api/v1/operations/operations?skip=0&limit=10
```

## 🔐 Security Features

### Implemented Protections

- ✅ **CORS Configuration** - Restricted origin handling
- ✅ **Rate Limiting** - Configurable per-IP rate limiting (SlowAPI)
- ✅ **SQL Injection Prevention** - Parameterized queries via SQLAlchemy
- ✅ **XSS Prevention** - Secure headers middleware
- ✅ **Secure Headers**:
  - X-Frame-Options: DENY
  - X-Content-Type-Options: nosniff
  - CSP: Restrictive content security policy
  - HSTS: Strict transport security
- ✅ **Secrets Management** - Environment variables only
- ✅ **Non-root Containers** - Docker runs as unprivileged user
- ✅ **Request Correlation** - X-Correlation-ID tracking

### Security Checklist

- [ ] Generate new SECRET_KEY: `openssl rand -hex 32`
- [ ] Update ALLOWED_HOSTS for production
- [ ] Use HTTPS in production (reverse proxy)
- [ ] Enable database backups
- [ ] Configure monitoring and alerting
- [ ] Implement API authentication (JWT/OAuth2)
- [ ] Set up Web Application Firewall (WAF)
- [ ] Enable database encryption at rest

## 📊 Logging & Monitoring

### Structured Logging

All requests and errors are logged in JSON format:

```json
{
  "timestamp": 1700000000.0,
  "level": "INFO",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "method": "POST",
  "path": "/api/v1/operations/process",
  "status_code": 202,
  "latency_ms": 45.23,
  "client_ip": "192.168.1.1"
}
```

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical errors requiring immediate attention

### Monitoring Endpoints

```bash
# Health check (Kubernetes)
curl http://localhost:8000/api/v1/system/health

# Readiness check
curl http://localhost:8000/api/v1/system/ready

# Liveness check
curl http://localhost:8000/api/v1/system/live
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

### Test Coverage

- System endpoints (health, version, info)
- Business operations (dispatch, list, get)
- Error handling (validation, 404, 500)
- CORS headers
- Rate limiting
- Security headers

## 🔄 Database Management

### Migrations (Alembic)

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Connection Pooling

Configured for production:
- Pool size: 20
- Max overflow: 10
- Pool timeout: 30 seconds
- Pool recycle: 1800 seconds

## 🚢 Deployment

### Docker Build

```bash
# Build image
docker build -t zenovox:latest .

# Run container
docker run -p 8000:8000 --env-file .env zenovox:latest
```

### Docker Compose Production

```bash
# Start stack
docker-compose up -d

# Scale workers
docker-compose up -d --scale celery_worker=4

# View metrics
docker stats
```

### Kubernetes Deployment

Health check configuration:
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

## 💾 Backup & Recovery

### PostgreSQL Backup

```bash
# Full backup
docker exec zenovox_postgres_prod pg_dumpall -U postgres_user > backup.sql

# Point-in-time backup
docker exec zenovox_postgres_prod pg_dump -U postgres_user zenovox_db > backup_point.sql

# Restore
psql -U postgres_user < backup.sql
```

### Recovery Procedure

1. **Stop services:**
   ```bash
   docker-compose down
   ```

2. **Restore database:**
   ```bash
   docker-compose up -d db redis
   docker exec -i zenovox_postgres_prod psql -U postgres_user < backup.sql
   ```

3. **Verify integrity:**
   ```bash
   curl http://localhost:5432
   ```

4. **Restart services:**
   ```bash
   docker-compose up -d
   ```

## 🔄 Rollback Strategy

### Pre-Deployment

1. Tag current image: `docker tag zenovox:latest zenovox:v1.0.0`
2. Backup database: `pg_dumpall > backup_v1.sql`
3. Document changes and rollback procedure

### Post-Deployment Rollback

```bash
# Stop current version
docker-compose down

# Restore previous image
docker tag zenovox:v1.0.0 zenovox:latest

# Restore database
docker-compose up -d db
docker exec -i zenovox_postgres_prod psql < backup_v1.sql

# Start services
docker-compose up -d
```

## 📈 Performance Optimization

### Database Optimization

- ✅ Connection pooling enabled (20 pool size)
- ✅ Query indices on frequently accessed columns
- ✅ Async connections for non-blocking I/O
- ✅ Statement caching via SQLAlchemy

### Application Optimization

- ✅ Response compression (gzip)
- ✅ Redis caching layer
- ✅ Async background task processing
- ✅ Database query result caching
- ✅ Connection reuse via pooling

### Monitoring Query Performance

```bash
# Enable slow query logging
# In docker-compose.yml, add:
# -c log_min_duration_statement=1000
```

## 🎯 Production Checklist

### Pre-Deployment

- [ ] All environment variables configured
- [ ] Database backups tested
- [ ] SSL/TLS certificates installed
- [ ] Monitoring and alerting configured
- [ ] Log aggregation setup (ELK, Splunk)
- [ ] Rate limiting values tuned
- [ ] Cache TTLs configured appropriately
- [ ] Database migration strategy defined

### Post-Deployment

- [ ] Health checks passing
- [ ] Logs being collected
- [ ] Metrics being collected
- [ ] Alerts configured and tested
- [ ] Incident runbook prepared
- [ ] Rollback plan documented
- [ ] Team trained on procedures
- [ ] 24/7 on-call rotation established

## 🆘 Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs web

# Check dependencies
docker-compose logs db redis

# Verify environment variables
docker-compose config | grep -E "DATABASE_URL|REDIS"
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
docker exec zenovox_postgres_prod psql -U postgres_user -d zenovox_db -c "SELECT 1"

# Test Redis connection
docker exec zenovox_redis_prod redis-cli ping
```

### High Memory Usage

```bash
# Check process memory
docker stats zenovox_api_service

# Reduce pool size in .env
DB_POOL_SIZE=10
```

### Task Processing Issues

```bash
# Check Celery worker logs
docker-compose logs celery_worker

# Inspect task queue
docker exec zenovox_redis_prod redis-cli LLEN celery

# Clear failed tasks
docker exec zenovox_redis_prod redis-cli DEL celery
```

## 📚 Additional Resources

### Learning Materials

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [12 Factor App](https://12factor.net/)

### Tools & Utilities

- **Postman**: API testing and documentation
- **pgAdmin**: PostgreSQL management
- **Redis Commander**: Redis GUI
- **Grafana**: Metrics visualization
- **Prometheus**: Metrics collection

## 📝 License

Proprietary - Zenovox Production System

## 👥 Support

For issues or questions:
1. Check logs: `docker-compose logs web`
2. Review troubleshooting section
3. Consult team documentation
4. Contact DevOps team

---

**Last Updated**: 2024
**Version**: 1.0.0
**Status**: Production Ready ✅
