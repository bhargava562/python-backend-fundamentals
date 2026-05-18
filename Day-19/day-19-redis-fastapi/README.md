# Day 19: Redis & Caching Strategies

Production-style FastAPI service that demonstrates Redis caching, cache invalidation, and rate limiting. The project uses Docker for Redis and the Cache-Aside pattern to speed up repeated reads.

## Features

- Redis connection pool with dependency injection
- Cache-Aside pattern with a reusable decorator and TTL configuration
- Cached product and user endpoints with simulated slow database reads
- Explicit cache invalidation on user updates
- Write-through and write-behind cache strategy demos
- Search endpoint caching with query-aware cache keys
- IP-based rate limiting backed by Redis
- Redis basics practice endpoints (strings, lists, sets, hashes, sorted sets)
- Pub/Sub, session store, and distributed lock examples
- Cache hit-rate tracking and memory usage metrics
- Optional HTML cache metrics dashboard

## Project Structure

```
day-19-redis-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── decorators.py
│   └── routers/
│       ├── __init__.py
│       ├── advanced.py
│       ├── products.py
│       ├── redis_practice.py
│       ├── search.py
│       └── users.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10+
- Docker Desktop

## Setup and Run

1. Start Redis using Docker Compose:

```bash
docker-compose up -d
```

Alternatively, run Redis directly with Docker:

```bash
docker run -d -p 6379:6379 redis:7-alpine
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Run the API server:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000

## How Caching Works

This project implements the Cache-Aside pattern:

1. The endpoint checks Redis for a cached response (`GET`).
2. If the cache is a hit, the response is returned immediately.
3. If the cache is a miss, the endpoint executes its logic, then stores the result with a TTL (`SET` with `EXPIRE`).

### Cache Keys

Cache keys are generated from the request path:

```
cache:/products
cache:/products/1
cache:/users/1
cache:/search/products?q=mouse
```

### TTLs

- Products: 60 seconds
- Users: 120 seconds

## Cache Invalidation

The `PUT /users/{id}` endpoint updates the mock user store and deletes the cached entry (`DELETE`). This prevents stale data from being served on subsequent `GET` requests.

## Write-Through and Write-Behind

- **Write-through** updates the mock database and immediately refreshes the cache.
- **Write-behind** updates the cache immediately and queues the database write in Redis for later processing.

Use these endpoints to compare behavior:

- `PUT /users/{id}/write-through`
- `PUT /users/{id}/write-behind`
- `POST /users/jobs/write-behind/process`

## Rate Limiting

The `/limited-endpoint` route uses Redis to count requests per client IP:

- `INCR` to increment the counter
- `EXPIRE` to create a 60-second window
- Requests above 5 per minute return `429 Too Many Requests`

## API Endpoints

- `GET /products`
- `GET /products/{id}`
- `GET /search/products?q=term`
- `GET /users/{id}`
- `PUT /users/{id}`
- `PUT /users/{id}/write-through`
- `PUT /users/{id}/write-behind`
- `POST /users/jobs/write-behind/process`
- `GET /limited-endpoint`

### Redis Basics Practice

- `GET /practice/strings`
- `GET /practice/lists`
- `GET /practice/sets`
- `GET /practice/hashes`
- `GET /practice/sorted-sets`

### Advanced Redis Features

- `POST /pubsub/publish?channel=demo&message=hello`
- `GET /pubsub/subscribe?channel=demo&timeout=5`
- `PUT /sessions/{session_id}`
- `GET /sessions/{session_id}`
- `POST /locks/{lock_name}/acquire?ttl=10`
- `POST /locks/{lock_name}/release?token=...`
- `GET /metrics/cache`
- `GET /metrics/dashboard`

## Example Requests

```bash
curl http://127.0.0.1:8000/products
curl http://127.0.0.1:8000/products/1
curl http://127.0.0.1:8000/users/1
curl http://127.0.0.1:8000/search/products?q=mouse

curl -X PUT http://127.0.0.1:8000/users/1 \
	-H "Content-Type: application/json" \
	-d '{"name":"Ava Updated"}'

curl -X PUT http://127.0.0.1:8000/users/1/write-through \
	-H "Content-Type: application/json" \
	-d '{"email":"ava.new@example.com"}'

curl -X PUT http://127.0.0.1:8000/users/1/write-behind \
	-H "Content-Type: application/json" \
	-d '{"name":"Queued Update"}'

curl -X POST http://127.0.0.1:8000/users/jobs/write-behind/process

curl http://127.0.0.1:8000/limited-endpoint

curl http://127.0.0.1:8000/practice/strings
curl http://127.0.0.1:8000/practice/lists
curl http://127.0.0.1:8000/practice/sets
curl http://127.0.0.1:8000/practice/hashes
curl http://127.0.0.1:8000/practice/sorted-sets

curl -X POST "http://127.0.0.1:8000/pubsub/publish?channel=demo&message=hello"
curl "http://127.0.0.1:8000/pubsub/subscribe?channel=demo&timeout=5"

curl -X PUT http://127.0.0.1:8000/sessions/demo \
	-H "Content-Type: application/json" \
	-d '{"user_id":1,"role":"admin"}'

curl http://127.0.0.1:8000/sessions/demo
curl "http://127.0.0.1:8000/locks/report/acquire?ttl=10"
curl "http://127.0.0.1:8000/metrics/cache"
curl "http://127.0.0.1:8000/metrics/dashboard"
```

## Performance Comparison

These are expected values based on a 2-second simulated database delay:

| Scenario | Expected Response Time |
| --- | --- |
| No cache (cold) | ~2000 ms |
| Cache hit | ~5-70 ms |

## Monitoring

Cache hit and miss counts are tracked in Redis:

- `metrics:cache:hits`
- `metrics:cache:misses`

Use `GET /metrics/cache` for JSON output and `GET /metrics/dashboard` for a lightweight HTML view.

## Troubleshooting

- If Redis is not reachable, confirm Docker is running and port 6379 is published.
- If the API cannot import `app`, run Uvicorn from the project directory or use:

```bash
uvicorn app.main:app --reload --app-dir ./
```

## Notes

- The data store is a mock in-memory dictionary to keep focus on caching behavior.
- Redis is used for caching, rate limiting, session storage, and demo features.
