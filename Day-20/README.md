# Day 20: Celery & Background Tasks Implementation

## Overview

This project demonstrates a production-ready FastAPI application integrated with Celery for asynchronous background task processing, periodic scheduled jobs, and task monitoring using Flower.

### Architecture Components

- **FastAPI**: RESTful API web framework for handling HTTP requests
- **Celery**: Distributed task queue for asynchronous job processing
- **Redis**: Message broker for task queues and result backend for storing task outcomes
- **Celery Beat**: Scheduler for periodic/cron jobs
- **Flower**: Web-based monitoring dashboard for Celery tasks and workers

---

## Key Features Implemented

### 1. Background Tasks
- **Email Tasks**: Send single emails, bulk emails with retry logic and exponential backoff
- **Image Processing**: Resize, compress, and process images using task chains
- **Report Generation**: Generate PDF and CSV reports using chord patterns
- **Data Operations**: Import and export data with progress tracking
- **Periodic Tasks**: Scheduled database cleanup, hourly reports, daily summaries, weekly digests

### 2. Celery Patterns
- **Chain**: Sequential task execution (resize → compress → generate thumbnail)
- **Group**: Parallel task execution (process multiple images at once)
- **Chord**: Parallel tasks with final callback (generate PDF + CSV, then combine)

### 3. Error Handling & Resilience
- Automatic retry with exponential backoff (2s, 4s, 8s...)
- Maximum retry limits per task
- Proper error logging and tracking
- Dead letter queue handling for failed tasks

### 4. Task Routing & Queues
Tasks are routed to priority queues:
- **email** (priority 10): High-priority email sending
- **reports** (priority 5): Report generation tasks
- **images** (priority 3): Image processing tasks
- **data** (priority 2): Data import/export tasks
- **default**: System tasks and cleanup

### 5. Periodic Task Schedule
- **Every 5 minutes**: System health check
- **Daily at midnight**: Database cleanup
- **Every hour**: Generate hourly report
- **Daily at 1:00 AM**: Generate daily summary
- **Weekly (Monday 8:00 AM)**: Send email digest

### 6. Comprehensive Monitoring
- Task status checking endpoints
- Worker statistics and information
- Active and scheduled task listings
- Flower dashboard for real-time monitoring

---

## Project Structure

```
Day-20/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application with all endpoints
│   ├── celery_app.py        # Celery configuration and setup
│   └── tasks.py             # Background task definitions
├── docker-compose.yml       # Docker services configuration
├── Dockerfile               # Container image definition
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## Installation & Setup

### Prerequisites

- Docker Desktop (running)
- Docker Compose
- Python 3.11+
- Redis CLI (optional, for manual testing)

### Step 1: Build and Start Services

```bash
# Navigate to Day-20 directory
cd Day-20

# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

This will start:
- Redis server (port 6379)
- FastAPI application (port 8000)
- Celery worker (processing tasks)
- Celery Beat (scheduling periodic tasks)
- Flower monitoring dashboard (port 5555)

### Step 2: Verify Services

Check all containers are running:
```bash
docker ps
```

Expected output:
```
celery-redis      redis:7-alpine
celery-api        FastAPI app
celery-worker     Celery worker
celery-beat       Celery beat scheduler
celery-flower     Flower dashboard
```

### Step 3: Verify Health

Check API health:
```bash
curl http://localhost:8000/health
```

Check Flower dashboard:
```
http://localhost:5555/
```

---

## API Documentation

### Base URL
```
http://localhost:8000
```

### Interactive API Docs
```
http://localhost:8000/docs (Swagger UI)
http://localhost:8000/redoc (ReDoc)
```

### Health & Stats Endpoints

#### Health Check
```http
GET /health
```
Returns current API and worker health status.

#### Worker Statistics
```http
GET /stats/workers
```
Get detailed information about all active workers.

#### Queue Statistics
```http
GET /stats/queues
```
Get information about task queues.

#### Worker Info
```http
GET /system/worker-info
```
Get detailed worker information including active tasks.

---

### Email Task Endpoints

#### Send Single Email
```http
POST /api/email/send

{
  "email": "user@example.com",
  "subject": "Hello from Celery",
  "body": "This is an async email"
}

Response:
{
  "message": "Email task queued",
  "task_id": "abc-123-def-456",
  "status_url": "/task/abc-123-def-456"
}
```

#### Send Bulk Emails
```http
POST /api/email/send-bulk

{
  "emails": ["user1@example.com", "user2@example.com"],
  "subject": "Bulk Email Campaign",
  "body": "Message for all recipients"
}

Response:
{
  "message": "Bulk email task queued",
  "task_id": "group-id",
  "recipient_count": 2,
  "status_url": "/task/group-id"
}
```

---

### Image Processing Endpoints

#### Process Images
```http
POST /api/images/process

{
  "image_ids": [1, 2, 3],
  "operation": "full"  # or "batch"
}

Response:
{
  "message": "Image processing group queued",
  "task_id": "task-id",
  "image_count": 3,
  "status_url": "/task/task-id"
}
```

---

### Report Generation Endpoints

#### Generate Report
```http
POST /api/reports/generate

{
  "report_type": "pdf",  # pdf, csv, or full
  "data_rows": 5000
}

Response:
{
  "message": "PDF report generation queued",
  "task_id": "task-id",
  "report_type": "pdf",
  "status_url": "/task/task-id"
}
```

#### Report Status
```http
GET /api/reports/status/{task_id}

Response:
{
  "task_id": "task-id",
  "status": "SUCCESS",
  "result": {
    "report_type": "pdf",
    "filename": "pdf_20240101_120000.pdf",
    "size_mb": 2.5
  }
}
```

---

### Data Import/Export Endpoints

#### Import Data
```http
POST /api/data/import

{
  "data_source": "external_api",
  "num_records": 10000
}

Response:
{
  "message": "Data import task queued",
  "task_id": "task-id",
  "data_source": "external_api",
  "num_records": 10000,
  "status_url": "/task/task-id"
}
```

#### Export Data
```http
POST /api/data/export

{
  "export_format": "csv",  # json, csv, or excel
  "table_name": "users",
  "filter_criteria": {"status": "active"}
}

Response:
{
  "message": "Data export task queued",
  "task_id": "task-id",
  "export_format": "csv",
  "table_name": "users",
  "status_url": "/task/task-id"
}
```

---

### Task Management Endpoints

#### Get Task Status
```http
GET /task/{task_id}

Response:
{
  "task_id": "task-id",
  "status": "SUCCESS",  # PENDING, STARTED, SUCCESS, FAILURE, RETRY, REVOKED
  "result": {...}
}
```

#### Cancel Task
```http
DELETE /task/{task_id}

Response:
{
  "message": "Task cancelled successfully",
  "task_id": "task-id"
}
```

#### List Active Tasks
```http
GET /tasks/active

Response:
{
  "active_tasks": {...},
  "total_active": 5
}
```

#### List Scheduled Tasks
```http
GET /tasks/scheduled

Response:
{
  "scheduled_tasks": {...},
  "total_scheduled": 3
}
```

---

### System Maintenance Endpoints

#### Manual Cleanup
```http
POST /system/cleanup

Response:
{
  "message": "Database cleanup task queued",
  "task_id": "task-id",
  "status_url": "/task/task-id"
}
```

#### System Health Check
```http
GET /system/health-check

Response:
{
  "message": "System health check queued",
  "task_id": "task-id",
  "status_url": "/task/task-id"
}
```

---

## Testing with cURL

### Test Email Task
```bash
curl -X POST "http://localhost:8000/api/email/send" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "subject": "Test Email",
    "body": "This is a test"
  }'
```

### Check Task Status
```bash
# First, capture task_id from response
# Then check status
curl http://localhost:8000/task/{task_id}
```

### View Worker Stats
```bash
curl http://localhost:8000/stats/workers | python -m json.tool
```

### List Active Tasks
```bash
curl http://localhost:8000/tasks/active | python -m json.tool
```

---

## Flower Monitoring Dashboard

Access the Flower dashboard at: **http://localhost:5555**

### Features:
- **Real-time task monitoring**: View active, completed, and failed tasks
- **Worker status**: Monitor worker availability and capacity
- **Task statistics**: View success/failure rates
- **Task details**: Inspect individual task results and errors
- **Queue monitoring**: Check queue depths and routing
- **Rate limiting**: Adjust worker concurrency

---

## Celery Concepts Explained

### Message Broker (Redis)
- **Role**: Central hub for task queues
- **Purpose**: Stores pending tasks and distributes them to workers
- **Benefit**: Decouples task producers from consumers
- **In this project**: Redis running on port 6379

### Workers
- **Role**: Process background tasks
- **Configuration**: `celery_worker` service with 4 concurrent workers
- **Queues**: Listen to email, reports, images, data, and default queues
- **Auto-restart**: Configured to restart after 1000 tasks (prevents memory leaks)

### Task Queues & Routing
- **Default**: Tasks sent to appropriate queue based on `task_routes`
- **Priority**: email queue has highest priority (10)
- **Worker assignment**: Different workers can specialize in specific queues

### Result Backend
- **Role**: Stores task execution results
- **Storage**: Results stored in Redis with 1-hour expiration
- **Benefits**: Can retrieve results after task completion

### Asynchronous Execution
- **Pattern**: API returns immediately with task_id
- **Client**: Polls `/task/{task_id}` endpoint for status
- **Benefits**: Non-blocking requests, improved scalability

---

## Task Patterns

### 1. Chain Pattern
Sequential execution of tasks:
```python
workflow = chain(
    task1.s(arg1),
    task2.s(arg2),
    task3.s(arg3)
)
result = workflow.apply_async()
```
**Use case**: Image resizing → compression → thumbnail generation

### 2. Group Pattern
Parallel execution of tasks:
```python
job = group(task.s(arg) for arg in args_list)
result = job.apply_async()
```
**Use case**: Send emails to multiple recipients simultaneously

### 3. Chord Pattern
Parallel tasks + callback:
```python
callback = final_task.s()
workflow = chord([task1.s(), task2.s()])(callback)
```
**Use case**: Generate PDF + CSV in parallel, then combine results

---

## Error Handling & Retry Logic

### Exponential Backoff
```python
@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, email, subject):
    try:
        # Task logic
        pass
    except Exception as exc:
        countdown = 2 ** self.request.retries  # 2s, 4s, 8s
        raise self.retry(exc=exc, countdown=countdown)
```

### Retry Configuration
- **max_retries**: 3 attempts per task
- **countdown**: Exponential backoff (2^retries seconds)
- **auto_retry**: Automatic retry on exception

---

## Periodic Tasks (Celery Beat)

### Current Schedule

| Task | Schedule | Purpose |
|------|----------|---------|
| check_system_health | Every 5 minutes | Monitor system resources |
| cleanup_database | Daily @ 00:00 UTC | Remove old records |
| generate_hourly_report | Every hour @ :00 | System metrics report |
| generate_daily_summary | Daily @ 01:00 UTC | Daily metrics aggregation |
| send_weekly_digest | Monday @ 08:00 UTC | Weekly email summary |

### Modify Schedule
Edit `app/celery_app.py` in the `beat_schedule` section to adjust timing.

---

## Docker Compose Services

### Redis Service
- **Image**: redis:7-alpine
- **Port**: 6379
- **Volume**: redis_data (persistent storage)
- **Healthcheck**: Every 5 seconds

### API Service
- **Image**: Custom (built from Dockerfile)
- **Port**: 8000
- **Command**: Runs FastAPI with uvicorn
- **Reload**: Enabled for development
- **Healthcheck**: Checks /health endpoint

### Celery Worker
- **Image**: Custom (built from Dockerfile)
- **Command**: Celery worker with 4 concurrent processes
- **Queues**: Listens to all queues (email, reports, images, data, default)
- **Logging**: Info level

### Celery Beat
- **Image**: Custom (built from Dockerfile)
- **Command**: Celery Beat scheduler
- **Purpose**: Triggers periodic tasks on schedule

### Flower
- **Image**: Custom (built from Dockerfile)
- **Port**: 5555
- **Purpose**: Web-based monitoring dashboard
- **Healthcheck**: Checks /api/workers endpoint

---

## Troubleshooting

### Issue: Tasks not being processed
```bash
# Check if Redis is running
docker exec celery-redis redis-cli ping
# Expected output: PONG

# Check worker logs
docker logs celery-worker

# Check if worker is connected
curl http://localhost:8000/stats/workers
```

### Issue: Flower dashboard not loading
```bash
# Restart Flower
docker restart celery-flower

# Check Flower logs
docker logs celery-flower
```

### Issue: Task stuck in PENDING state
```bash
# Check Redis memory
docker exec celery-redis redis-cli INFO memory

# Clear Redis if needed
docker exec celery-redis redis-cli FLUSHALL  # CAUTION: Clears all data
```

### Issue: High memory usage
- Reduce `worker_max_tasks_per_child` value
- Increase concurrency level in worker
- Review task result retention time

---

## Performance Tuning

### Worker Configuration
```bash
# Current: 4 concurrent workers
command: celery -A app.celery_app worker --concurrency=4

# Increase for I/O-bound tasks
--concurrency=8

# Decrease for CPU-bound tasks
--concurrency=2
```

### Result Expiration
```python
result_expires=3600  # 1 hour (increase for longer retention)
```

### Worker Prefetch
```python
worker_prefetch_multiplier=4  # Tasks fetched at once
```

---

## Production Considerations

### 1. Deployment
- Use managed Redis (AWS ElastiCache, Redis Cloud)
- Deploy workers separately from API
- Use multi-worker setup with load balancer

### 2. Monitoring
- Set up alerts for failed tasks
- Monitor Redis memory usage
- Track task execution times

### 3. Security
- Enable Redis authentication
- Use encrypted broker URLs
- Implement rate limiting on API endpoints

### 4. Scaling
- Horizontal scaling: Add more worker containers
- Vertical scaling: Increase concurrency per worker
- Task routing: Use dedicated workers for critical tasks

---

## Quick Command Reference

```bash
# Build and start services
docker-compose up --build

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f celery_worker
docker-compose logs -f celery_beat
docker-compose logs -f api

# Access Flower
http://localhost:5555

# Access API docs
http://localhost:8000/docs

# Scale workers (add 2 more workers)
docker-compose up -d --scale celery_worker=3

# Remove volumes (clean Redis data)
docker-compose down -v

# Restart specific service
docker-compose restart celery_worker
```

---

## Learning Resources

### Key Topics Covered
1. ✅ Message broker role and setup
2. ✅ Celery workers and task execution
3. ✅ Task queues and routing patterns
4. ✅ Result backends for task results
5. ✅ Async vs sync execution
6. ✅ Celery Beat for periodic tasks
7. ✅ Task patterns (chain, group, chord)
8. ✅ Error handling and retries
9. ✅ Celery monitoring with Flower
10. ✅ Docker containerization

### Next Steps
- Implement additional task types
- Add task progress tracking
- Set up alerts for failed tasks
- Implement custom result backend
- Add authentication to API endpoints

---

## Deliverables Checklist

- ✅ Celery integrated with FastAPI application
- ✅ Multiple background tasks implemented (email, reports, images, data)
- ✅ Task status checking API endpoints
- ✅ Periodic tasks with Celery Beat
- ✅ Error handling and retry logic with exponential backoff
- ✅ Celery configuration in Docker Compose
- ✅ Background task examples (email, reports, image processing, data operations)
- ✅ README documenting task queue setup
- ✅ Flower monitoring dashboard integration
- ✅ Task routing and priority queues
- ✅ Comprehensive API documentation

---

## Summary

This Day-20 project provides a complete, production-ready implementation of Celery with FastAPI, demonstrating:

- **Scalable architecture** for handling asynchronous tasks
- **Reliable execution** with error handling and retries
- **Flexible task patterns** (chain, group, chord)
- **Comprehensive monitoring** via Flower dashboard
- **Production-grade setup** with Docker Compose
- **Well-documented API** with extensive examples

The implementation serves as a template for building distributed task queues in any FastAPI/Python application.