from __future__ import annotations

import asyncio
import json
import time
import uuid
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Response

from ..database import get_redis


router = APIRouter(tags=["advanced"])


@router.post("/pubsub/publish")
async def publish_message(channel: str, message: str) -> Dict[str, object]:
    redis = await get_redis()
    subscribers = await redis.publish(channel, message)  # PUBLISH
    return {"channel": channel, "message": message, "subscribers": subscribers}


@router.get("/pubsub/subscribe")
async def subscribe_message(channel: str, timeout: int = 5) -> Dict[str, object]:
    redis = await get_redis()
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)

    start = time.monotonic()
    try:
        while time.monotonic() - start < timeout:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and "data" in message:
                return {
                    "channel": channel,
                    "message": message["data"],
                    "elapsed_seconds": round(time.monotonic() - start, 2),
                }
            await asyncio.sleep(0.1)
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()

    return {"channel": channel, "message": None, "elapsed_seconds": timeout}


@router.put("/sessions/{session_id}")
async def store_session(session_id: str, payload: Dict[str, Any]) -> Dict[str, object]:
    redis = await get_redis()
    key = f"session:{session_id}"
    mapping = {k: json.dumps(v) for k, v in payload.items()}

    await redis.hset(key, mapping=mapping)  # HSET
    await redis.expire(key, 3600)  # EXPIRE

    return {"session_id": session_id, "ttl_seconds": 3600}


@router.get("/sessions/{session_id}")
async def get_session(session_id: str) -> Dict[str, object]:
    redis = await get_redis()
    key = f"session:{session_id}"

    values = await redis.hgetall(key)  # HGETALL
    if not values:
        raise HTTPException(status_code=404, detail="Session not found")

    decoded: Dict[str, Any] = {}
    for k, v in values.items():
        try:
            decoded[k] = json.loads(v)
        except json.JSONDecodeError:
            decoded[k] = v

    return {"session_id": session_id, "data": decoded}


@router.post("/locks/{lock_name}/acquire")
async def acquire_lock(lock_name: str, ttl: int = 10) -> Dict[str, object]:
    redis = await get_redis()
    key = f"lock:{lock_name}"
    token = uuid.uuid4().hex

    acquired = await redis.set(key, token, nx=True, ex=ttl)  # SET NX EX
    if not acquired:
        raise HTTPException(status_code=409, detail="Lock already held")

    return {"lock": lock_name, "token": token, "ttl_seconds": ttl}


@router.post("/locks/{lock_name}/release")
async def release_lock(lock_name: str, token: str) -> Dict[str, object]:
    redis = await get_redis()
    key = f"lock:{lock_name}"
    script = (
        "if redis.call('get', KEYS[1]) == ARGV[1] then "
        "return redis.call('del', KEYS[1]) else return 0 end"
    )

    released = await redis.eval(script, 1, key, token)
    return {"lock": lock_name, "released": bool(released)}


@router.get("/metrics/cache")
async def cache_metrics() -> Dict[str, object]:
    redis = await get_redis()
    hits = int(await redis.get("metrics:cache:hits") or 0)
    misses = int(await redis.get("metrics:cache:misses") or 0)
    total = hits + misses
    hit_rate = round(hits / total, 4) if total else 0.0

    memory = await redis.info("memory")
    return {
        "hits": hits,
        "misses": misses,
        "hit_rate": hit_rate,
        "memory": {
            "used_memory": memory.get("used_memory"),
            "used_memory_human": memory.get("used_memory_human"),
            "maxmemory_human": memory.get("maxmemory_human"),
        },
    }


@router.get("/metrics/dashboard")
async def metrics_dashboard() -> Response:
        html = """
        <!DOCTYPE html>
        <html lang=\"en\">
        <head>
            <meta charset=\"UTF-8\" />
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
            <title>Redis Cache Metrics</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 32px; }
                .card { border: 1px solid #ddd; border-radius: 8px; padding: 16px; max-width: 520px; }
                .row { display: flex; justify-content: space-between; margin: 6px 0; }
                .muted { color: #666; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <h1>Redis Cache Metrics</h1>
            <div class=\"card\">
                <div class=\"row\"><strong>Hits</strong><span id=\"hits\">-</span></div>
                <div class=\"row\"><strong>Misses</strong><span id=\"misses\">-</span></div>
                <div class=\"row\"><strong>Hit Rate</strong><span id=\"hit_rate\">-</span></div>
                <div class=\"row\"><strong>Used Memory</strong><span id=\"memory\">-</span></div>
                <div class=\"muted\">Refreshes every 5 seconds.</div>
            </div>
            <script>
                async function refresh() {
                    const res = await fetch('/metrics/cache');
                    const data = await res.json();
                    document.getElementById('hits').textContent = data.hits;
                    document.getElementById('misses').textContent = data.misses;
                    document.getElementById('hit_rate').textContent = data.hit_rate;
                    document.getElementById('memory').textContent = data.memory.used_memory_human || '-';
                }
                refresh();
                setInterval(refresh, 5000);
            </script>
        </body>
        </html>
        """
    return Response(content=html, media_type="text/html")
