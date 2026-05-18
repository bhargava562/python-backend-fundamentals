from __future__ import annotations

from typing import Any, Dict

from redis.asyncio import ConnectionPool, Redis


redis_pool: ConnectionPool | None = None

# Mock database data to simulate slow database calls.
USERS_DB: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "name": "Ava", "email": "ava@example.com"},
    2: {"id": 2, "name": "Liam", "email": "liam@example.com"},
    3: {"id": 3, "name": "Noah", "email": "noah@example.com"},
}

PRODUCTS_DB: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "name": "Wireless Mouse", "price": 29.99},
    2: {"id": 2, "name": "Mechanical Keyboard", "price": 89.0},
    3: {"id": 3, "name": "USB-C Hub", "price": 39.5},
}


def init_redis_pool() -> None:
    global redis_pool
    if redis_pool is None:
        redis_pool = ConnectionPool.from_url(
            "redis://localhost:6379",
            decode_responses=True,
            max_connections=10,
        )


def close_redis_pool() -> None:
    global redis_pool
    if redis_pool is not None:
        redis_pool.disconnect()
        redis_pool = None


async def get_redis() -> Redis:
    if redis_pool is None:
        init_redis_pool()
    return Redis(connection_pool=redis_pool)
