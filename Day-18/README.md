# Day 18 FastAPI CRUD API

This directory contains a small FastAPI application with in-memory CRUD endpoints.

## Endpoints

- `GET /` - basic status message
- `GET /health` - health check
- `GET /items` - list all items
- `GET /items/{item_id}` - get one item
- `POST /items` - create an item
- `PUT /items/{item_id}` - update an item
- `DELETE /items/{item_id}` - delete an item

## Run locally

```bash
uvicorn app.main:app --reload
```

## Run with Docker Compose (Production Ready)

To run the application along with its PostgreSQL database and Redis cache using Docker:

1. Ensure Docker and Docker Desktop/Engine are installed and running.
2. Build and start the containers:
	```bash
	docker-compose up -d --build
	```
3. Access the API documentation at http://localhost:8000/docs.

To stop the application and tear down the containers:

```bash
docker-compose down
```

