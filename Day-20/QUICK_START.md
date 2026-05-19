# Day-20 Celery Quick Start Guide

## Prerequisites

- Docker Desktop running
- Python 3.11+
- curl or REST client

## Quick Start (30 seconds)

### 1. Navigate to Day-20
```bash
cd d:\Linkific_Modules\python-backend-fundamentals\Day-20
```

### 2. Start All Services
```bash
docker-compose up --build -d
```

### 3. Verify Services Are Running
```bash
docker-compose ps
```

Expected output: All 5 containers should be running:
- `celery-redis` (healthy)
- `celery-api` (healthy)
- `celery-worker` (running)
- `celery-beat` (running)
- `celery-flower` (running)

### 4. Test API
```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "workers": {
    "count": 1,
    "active_tasks": 0
  }
}
```

## Access Points

| Service | URL |
|---------|-----|
| **API Documentation** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **Flower Dashboard** | http://localhost:5555 |
| **Health Check** | http://localhost:8000/health |

## Common Tasks

### Send an Email Task
```bash
curl -X POST "http://localhost:8000/api/email/send" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "subject": "Hello",
    "body": "Test email"
  }'
```

### Check Task Status
```bash
# Replace {task_id} with the ID from previous response
curl http://localhost:8000/task/{task_id}
```

### View Active Tasks
```bash
curl http://localhost:8000/tasks/active
```

### Process Images (Batch)
```bash
curl -X POST "http://localhost:8000/api/images/process" \
  -H "Content-Type: application/json" \
  -d '{
    "image_ids": [1, 2, 3],
    "operation": "batch"
  }'
```

### Generate Report
```bash
curl -X POST "http://localhost:8000/api/reports/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "pdf",
    "data_rows": 5000
  }'
```

## View Logs

### API Logs
```bash
docker-compose logs -f celery-api
```

### Worker Logs
```bash
docker-compose logs -f celery-worker
```

### Beat Logs
```bash
docker-compose logs -f celery-beat
```

### Redis Logs
```bash
docker-compose logs -f celery-redis
```

## Stop Services

```bash
docker-compose down
```

## Clean Everything (including data)

```bash
docker-compose down -v
```

## Run Test Suite

```bash
python test_celery_api.py
```

This will run 21 comprehensive tests covering all major endpoints.

## Flower Monitoring Dashboard

Access at: **http://localhost:5555**

Features:
- View active tasks in real-time
- Monitor worker status
- Check task execution history
- View task results
- Monitor queues

## Key Features Demonstrated

✅ Email sending with retry logic  
✅ Bulk email operations (group pattern)  
✅ Image processing with chains  
✅ Report generation (PDF, CSV) with chords  
✅ Data import/export  
✅ Periodic tasks with Celery Beat  
✅ Task status checking API  
✅ Worker monitoring  
✅ Celery Flower dashboard  
✅ Task routing and priority queues  

## Troubleshooting

### Services won't start
```bash
# Stop conflicting services
docker stop day-18-redis-1 day-18-db-1

# Then try again
docker-compose up --build -d
```

### API shows 500 error
```bash
# Check API logs
docker logs celery-api

# Restart API
docker-compose restart celery-api
```

### Tasks not processing
```bash
# Check worker is running
docker exec celery-worker celery -A app.celery_app inspect active

# Check Redis connection
docker exec celery-redis redis-cli ping
```

### Flower dashboard not loading
```bash
# Restart Flower
docker-compose restart celery-flower

# Check logs
docker logs celery-flower
```

## Documentation

For detailed documentation, see [README.md](README.md)

## API Endpoints Quick Reference

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /stats/workers` - Worker statistics
- `GET /stats/queues` - Queue statistics
- `POST /api/email/send` - Send single email
- `POST /api/email/send-bulk` - Send bulk emails
- `POST /api/images/process` - Process images
- `POST /api/reports/generate` - Generate reports
- `POST /api/data/import` - Import data
- `POST /api/data/export` - Export data
- `GET /task/{task_id}` - Get task status
- `DELETE /task/{task_id}` - Cancel task
- `GET /tasks/active` - List active tasks
- `GET /tasks/scheduled` - List scheduled tasks
- `POST /system/cleanup` - Trigger cleanup
- `POST /system/health-check` - Run health check
- `GET /system/worker-info` - Get worker information

## Performance Tips

1. **Scale workers for high load:**
   ```bash
   docker-compose up -d --scale celery_worker=3
   ```

2. **Monitor Redis memory:**
   ```bash
   docker exec celery-redis redis-cli INFO memory
   ```

3. **Check task queues:**
   ```bash
   docker exec celery-redis redis-cli KEYS "celery*"
   ```

4. **View Redis database:**
   ```bash
   docker exec celery-redis redis-cli DBSIZE
   ```

## Next Steps

1. Customize tasks in `app/tasks.py`
2. Add authentication to API endpoints
3. Implement task progress tracking
4. Set up alerts for failed tasks
5. Deploy to production with multiple workers
6. Use managed Redis service in cloud
7. Implement custom result backend
8. Add task scheduling UI

Happy async processing! 🚀
