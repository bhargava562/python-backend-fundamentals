# Quick Start Guide - Day 24: Production Backend System

## 🚀 Start in 5 Minutes

### Option 1: Docker Compose (Recommended)

```bash
# 1. Navigate to directory
cd Day-24

# 2. Start all services (database, cache, API, workers)
docker-compose up -d

# 3. Verify health
curl http://localhost:8000/api/v1/system/health

# 4. Access API documentation
open http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# 1. Navigate to directory
cd Day-24

# 2. Activate virtual environment (already created)
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# 3. Start local servers
# Terminal 1: PostgreSQL + Redis (or Docker)
docker run -d -p 5432:5432 postgres:16-alpine
docker run -d -p 6379:6379 redis:7-alpine

# Terminal 2: FastAPI server
python run.py  # or: uvicorn app.main:app --reload

# Terminal 3: Celery worker
celery -A app.worker.celery_app worker --loglevel=info

# 4. Access API
open http://localhost:8000/docs
```

## 📍 Key URLs

| Service | URL |
|---------|-----|
| **API Docs** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **Health Check** | http://localhost:8000/api/v1/system/health |
| **Operations API** | http://localhost:8000/api/v1/operations |
| **PostgreSQL** | localhost:5432 |
| **Redis** | localhost:6379 |

## 🔥 Quick API Tests

### Test Health
```bash
curl http://localhost:8000/api/v1/system/health | python -m json.tool
```

### Create Operation
```bash
curl -X POST http://localhost:8000/api/v1/operations/process \
  -H "Content-Type: application/json" \
  -d '{
    "reference_id": "TX-001",
    "summary": "Test batch processing"
  }' | python -m json.tool
```

### List Operations
```bash
curl http://localhost:8000/api/v1/operations/operations | python -m json.tool
```

### Get Task Status
```bash
# Use the task_id from create operation response
curl http://localhost:8000/api/v1/operations/task-status/TASK_ID
```

## 📊 Monitoring

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery_worker

# Search logs
docker-compose logs web | grep ERROR
```

### Check Service Status
```bash
docker-compose ps
```

### View Metrics
```bash
# Real-time stats
docker stats

# Container resource usage
docker-compose stats
```

## 🧪 Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_api.py::TestSystemEndpoints::test_health_endpoint -v

# Watch mode
pytest-watch
```

## 🔧 Common Commands

### Start/Stop Services
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart specific service
docker-compose restart web
```

### View Configuration
```bash
# Current environment
cat .env

# Docker compose config
docker-compose config

# Check running containers
docker ps
```

### Database Operations
```bash
# Connect to database
docker exec -it zenovox_postgres_prod psql -U postgres_user -d zenovox_db

# Backup database
docker exec zenovox_postgres_prod pg_dump -U postgres_user zenovox_db > backup.sql

# View logs
docker-compose logs db
```

### Scale Services
```bash
# Run multiple API instances
docker-compose up -d --scale web=3

# Run more workers
docker-compose up -d --scale celery_worker=4
```

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check logs
docker-compose logs

# Check specific service
docker-compose logs web

# View error details
docker-compose up  # Run without -d to see output
```

### Port Already in Use
```bash
# Kill process using port
# Windows: netstat -ano | findstr :8000
# Linux: lsof -i :8000

# Or change port in docker-compose.yml:
# ports:
#   - "8001:8000"
```

### Database Connection Error
```bash
# Verify PostgreSQL is running
docker-compose logs db

# Test connection
docker exec zenovox_postgres_prod psql -U postgres_user -c "SELECT 1"

# Reset database
docker-compose down -v  # Remove volumes!
docker-compose up -d db
```

### Out of Memory
```bash
# Check memory usage
docker stats

# Reduce pool size in .env
DB_POOL_SIZE=10

# Or restart services
docker-compose restart
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Complete architecture and features |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Production deployment procedures |
| [.env.example](.env.example) | Environment variables template |
| [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md) | What was implemented |

## ✅ Features Checklist

- ✅ FastAPI with async support
- ✅ PostgreSQL with connection pooling
- ✅ Redis for caching
- ✅ Celery for background tasks
- ✅ Structured JSON logging
- ✅ Global exception handlers
- ✅ Rate limiting
- ✅ Security headers
- ✅ CORS support
- ✅ Health checks
- ✅ Docker Compose stack
- ✅ Comprehensive tests
- ✅ API documentation (Swagger)

## 🆘 Need Help?

1. **Check logs**: `docker-compose logs web`
2. **Review docs**: See README.md and DEPLOYMENT_GUIDE.md
3. **Run tests**: `pytest -v` to check system health
4. **API docs**: http://localhost:8000/docs (interactive)

## 🎯 Next Steps

1. Explore API docs at http://localhost:8000/docs
2. Create test operations via API
3. Monitor task processing in worker logs
4. Run test suite: `pytest -v`
5. Read DEPLOYMENT_GUIDE.md for production setup
6. Configure monitoring and alerting
7. Set up backups and disaster recovery

---

**Ready?** Start with: `docker-compose up -d` then visit http://localhost:8000/docs 🚀
