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
