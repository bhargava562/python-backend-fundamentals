# Deployment Guide - Zenovox Production System

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Database Migration](#database-migration)
4. [Deployment Methods](#deployment-methods)
5. [Health Verification](#health-verification)
6. [Monitoring & Logging](#monitoring--logging)
7. [Scaling](#scaling)
8. [Incident Response](#incident-response)

## Pre-Deployment Checklist

### Infrastructure Requirements
- [ ] PostgreSQL 14+ installed and running
- [ ] Redis 7+ installed and running
- [ ] Docker & Docker Compose installed
- [ ] Sufficient disk space (min 50GB recommended)
- [ ] Network connectivity verified
- [ ] Firewall rules configured

### Application Checklist
- [ ] All tests passing: `pytest --cov=app`
- [ ] Code review completed
- [ ] Security scan completed
- [ ] Performance benchmarks recorded
- [ ] Rollback procedure documented
- [ ] Backup created

### Configuration Checklist
- [ ] SECRET_KEY generated: `openssl rand -hex 32`
- [ ] DATABASE_URL verified
- [ ] REDIS_URL verified
- [ ] ALLOWED_HOSTS updated for target environment
- [ ] Rate limiting rules configured
- [ ] SSL/TLS certificates ready (if applicable)
- [ ] Environment-specific .env prepared

## Environment Setup

### Generate Secrets
```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Store securely in secrets manager
# Examples: AWS Secrets Manager, HashiCorp Vault, Kubernetes Secrets
```

### Create Production Environment File
```bash
cp .env.example .env.production
# Update values in .env.production
```

### Database Preparation
```bash
# Create database user
psql -U postgres -c "CREATE USER zenovox_prod WITH PASSWORD 'secure_password';"

# Create database
psql -U postgres -c "CREATE DATABASE zenovox_prod OWNER zenovox_prod;"

# Grant privileges
psql -U postgres zenovox_prod -c "GRANT ALL PRIVILEGES ON SCHEMA public TO zenovox_prod;"

# Verify connection
psql -U zenovox_prod -d zenovox_prod -c "SELECT version();"
```

### Redis Configuration
```bash
# Test Redis connection
redis-cli -h your_redis_host ping

# Configure persistence
# Add to redis.conf:
# save 900 1
# save 300 10
# save 60 10000
# appendonly yes

# Restart Redis
sudo systemctl restart redis-server
```

## Database Migration

### Initial Setup
```bash
# Using Docker Compose
docker-compose up -d db
docker-compose run --rm web alembic upgrade head

# Or manually with Python
python -c "import asyncio; from app.database import init_db; asyncio.run(init_db())"
```

### Data Import
```bash
# Import seed data if available
psql -U zenovox_prod -d zenovox_prod < seed_data.sql

# Verify data
psql -U zenovox_prod -d zenovox_prod -c "SELECT COUNT(*) FROM operational_logs;"
```

### Backup Before Deployment
```bash
# Full database backup
pg_dump -U zenovox_prod -d zenovox_prod > backup_pre_deploy_$(date +%Y%m%d).sql

# Compressed backup
pg_dump -U zenovox_prod -d zenovox_prod | gzip > backup_pre_deploy_$(date +%Y%m%d).sql.gz

# Verify backup
gunzip -t backup_pre_deploy_*.sql.gz
```

## Deployment Methods

### Method 1: Docker Compose (Recommended for Development/Staging)

#### Step 1: Build Images
```bash
docker-compose build
```

#### Step 2: Start Services
```bash
docker-compose up -d
```

#### Step 3: Verify Services
```bash
# Check all services
docker-compose ps

# Expected output:
# NAME                    STATUS
# zenovox_postgres_prod   Up (healthy)
# zenovox_redis_prod      Up (healthy)
# zenovox_api_service     Up (healthy)
# zenovox_celery_worker   Up
```

### Method 2: Kubernetes (Production Recommended)

#### Create Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zenovox-api
  labels:
    app: zenovox
spec:
  replicas: 3
  selector:
    matchLabels:
      app: zenovox
  template:
    metadata:
      labels:
        app: zenovox
    spec:
      containers:
      - name: api
        image: zenovox:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENV
          valueFrom:
            configMapKeyRef:
              name: zenovox-config
              key: env
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
        resources:
          requests:
            memory: "256Mi"
            cpu: "500m"
          limits:
            memory: "512Mi"
            cpu: "1000m"
```

### Method 3: Manual Installation

#### Step 1: Install Dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env with production values
```

#### Step 3: Run Application
```bash
# Web service
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Celery worker (separate terminal)
celery -A app.worker.celery_app worker --loglevel=info --concurrency=4

# Celery beat (separate terminal, optional)
celery -A app.worker.celery_app beat --loglevel=info
```

## Health Verification

### Immediate Checks (First 5 minutes)
```bash
# Check health endpoint
curl http://localhost:8000/api/v1/system/health

# Check version
curl http://localhost:8000/api/v1/system/version

# Check readiness
curl http://localhost:8000/api/v1/system/ready

# Check liveness
curl http://localhost:8000/api/v1/system/live

# Access Swagger UI
open http://localhost:8000/docs
```

### Extended Checks (First 30 minutes)
```bash
# Test database connection
curl http://localhost:8000/api/v1/system/health | jq '.checks.postgres'

# Test Redis connection
curl http://localhost:8000/api/v1/system/health | jq '.checks.redis'

# Create test operation
curl -X POST http://localhost:8000/api/v1/operations/process \
  -H "Content-Type: application/json" \
  -d '{"reference_id": "TEST-001", "summary": "Deployment test"}'

# Verify task processing
docker-compose logs celery_worker | grep "TEST-001"
```

### Performance Baseline
```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/v1/system/health

# Metrics to record:
# - Requests per second
# - Response time (average, min, max)
# - Error rate
# - P95, P99 latencies
```

## Monitoring & Logging

### Log Aggregation Setup

#### Using ELK Stack
```bash
# Pull logs from container
docker logs zenovox_api_service | tee api.log

# Or setup filebeat
# Configuration (filebeat.yml):
filebeat.inputs:
- type: container
  paths:
    - '/var/lib/docker/containers/*/*.log'

output.elasticsearch:
  hosts: ["elasticsearch:9200"]

setup.kibana:
  host: "kibana:5601"
```

#### Using Splunk
```bash
# Install Splunk Universal Forwarder
# Configure to forward logs from Docker
# Search and visualize in Splunk UI
```

### Metrics Collection

#### Prometheus Configuration
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'zenovox'
    static_configs:
      - targets: ['localhost:8000']
```

#### Key Metrics to Monitor
- HTTP request rate
- Response time (p50, p95, p99)
- Error rate
- Database connection pool usage
- Redis memory usage
- Celery task queue depth
- Background task processing time

### Alerting Rules
```yaml
# Example Prometheus alert rules
groups:
  - name: zenovox
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
          
      - alert: SlowResponseTime
        expr: histogram_quantile(0.95, http_request_duration_seconds) > 1
        for: 10m
        annotations:
          summary: "P95 response time > 1s"
```

## Scaling

### Horizontal Scaling

#### Scale API Replicas
```bash
# Docker Compose
docker-compose up -d --scale web=3

# Kubernetes
kubectl scale deployment zenovox-api --replicas=5
```

#### Scale Workers
```bash
# Docker Compose
docker-compose up -d --scale celery_worker=8

# Kubernetes
kubectl scale deployment zenovox-worker --replicas=10
```

### Vertical Scaling
```bash
# Increase container resources
# Edit docker-compose.yml or Kubernetes deployment:
resources:
  requests:
    memory: "512Mi"
    cpu: "1000m"
  limits:
    memory: "1Gi"
    cpu: "2000m"
```

### Database Optimization for Scale
```sql
-- Add partitioning for large tables
CREATE TABLE operational_logs_partitioned (
    id SERIAL,
    reference_id VARCHAR(100),
    created_at TIMESTAMP
) PARTITION BY RANGE (EXTRACT(YEAR FROM created_at));

-- Create indexes for common queries
CREATE INDEX idx_operational_logs_ref_id ON operational_logs(reference_id);
CREATE INDEX idx_operational_logs_created ON operational_logs(created_at DESC);

-- Analyze table for query planner
ANALYZE operational_logs;
```

## Incident Response

### High CPU Usage
```bash
# Identify problematic container
docker stats

# Check process inside container
docker exec zenovox_api_service ps aux

# Scale up to distribute load
docker-compose up -d --scale web=5

# Check for infinite loops or memory leaks
docker logs zenovox_api_service | tail -100
```

### High Memory Usage
```bash
# Monitor memory
docker stats --no-stream zenovox_api_service

# Restart container if memory leak detected
docker-compose restart web

# Reduce connection pool size
# Edit .env: DB_POOL_SIZE=10

# Clear Redis cache if necessary
redis-cli FLUSHDB
```

### Database Connection Issues
```bash
# Test database connectivity
psql -U zenovox_prod -d zenovox_prod -c "SELECT 1"

# Check connection pool status
psql -U postgres -d zenovox_prod -c "SELECT count(*) FROM pg_stat_activity;"

# Restart database
docker-compose restart db

# Increase pool size if needed
# Edit .env: DB_POOL_SIZE=30
```

### Task Processing Backlog
```bash
# Check queue depth
redis-cli LLEN celery

# Monitor worker status
docker-compose logs celery_worker | tail -50

# Scale workers
docker-compose up -d --scale celery_worker=10

# Or restart workers to clear stuck tasks
docker-compose restart celery_worker
```

### Deployment Rollback
```bash
# Stop current version
docker-compose down

# Restore previous image tag
docker tag zenovox:v1.0.0_rollback zenovox:latest

# Restore database backup
docker-compose up -d db
docker exec -i zenovox_postgres_prod psql < backup_v1.0.0.sql

# Start services
docker-compose up -d

# Verify health
curl http://localhost:8000/api/v1/system/health
```

## Post-Deployment

### Day 1 Actions
- [ ] Monitor all metrics
- [ ] Review logs for errors
- [ ] Verify all features working
- [ ] Test failover scenarios
- [ ] Document any issues
- [ ] Gather team feedback

### Week 1 Actions
- [ ] Analyze performance metrics
- [ ] Fine-tune resource allocation
- [ ] Review and optimize database queries
- [ ] Update documentation with actual findings
- [ ] Schedule optimization tasks

### Ongoing
- [ ] Daily health checks
- [ ] Weekly backup verification
- [ ] Monthly performance reviews
- [ ] Quarterly security audits
- [ ] Annual disaster recovery drills

---

**Last Updated**: 2024
**Deployment Version**: 1.0.0
