from __future__ import annotations

import time
from typing import Dict

from fastapi import FastAPI, HTTPException, Request

from .database import close_redis_pool, get_redis, init_redis_pool
from .routers import advanced, products, redis_practice, search, users


app = FastAPI(title="Day 19: Redis & Caching Strategies")

app.include_router(products.router)
app.include_router(users.router)
app.include_router(search.router)
app.include_router(redis_practice.router)
app.include_router(advanced.router)


@app.on_event("startup")
async def on_startup() -> None:
    init_redis_pool()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    close_redis_pool()


@app.get("/limited-endpoint")
async def limited_endpoint(request: Request) -> Dict[str, object]:
    client_ip = request.client.host if request.client else "unknown"
    rate_key = f"ratelimit:{client_ip}"

    redis = await get_redis()
    try:
        current_count = await redis.incr(rate_key)  # INCR
        if current_count == 1:
            await redis.expire(rate_key, 60)  # EXPIRE
    except Exception:
        current_count = 0

    if current_count > 5:
        raise HTTPException(status_code=429, detail="Too Many Requests")

    return {
        "message": "Request accepted",
        "remaining": max(0, 5 - current_count),
        "reset_in_seconds": 60,
        "timestamp": int(time.time()),
    }
