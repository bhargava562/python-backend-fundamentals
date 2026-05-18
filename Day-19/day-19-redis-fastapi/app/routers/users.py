from __future__ import annotations

import asyncio
import json
from typing import Dict

from fastapi import APIRouter, HTTPException, Request

from ..database import USERS_DB, get_redis
from ..decorators import cache_response


router = APIRouter(prefix="/users", tags=["users"])

WRITE_BEHIND_QUEUE = "queue:users:write-behind"


@router.get("/{user_id}")
@cache_response(ttl_seconds=120)
async def get_user(user_id: int, request: Request) -> Dict[str, object]:
    await asyncio.sleep(2)
    user = USERS_DB.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}")
async def update_user(user_id: int, payload: Dict[str, object], request: Request) -> Dict[str, object]:
    user = USERS_DB.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.update(payload)
    USERS_DB[user_id] = user

    cache_key = f"cache:{request.url.path}"
    redis = await get_redis()
    try:
        await redis.delete(cache_key)  # DELETE
    except Exception:
        pass

    return user


@router.put("/{user_id}/write-through")
async def update_user_write_through(
    user_id: int, payload: Dict[str, object], request: Request
) -> Dict[str, object]:
    user = USERS_DB.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.update(payload)
    USERS_DB[user_id] = user

    cache_key = f"cache:/users/{user_id}"
    redis = await get_redis()
    try:
        await redis.set(cache_key, json.dumps(user), ex=120)  # SET with EXPIRE
    except Exception:
        pass

    return user


@router.put("/{user_id}/write-behind")
async def update_user_write_behind(
    user_id: int, payload: Dict[str, object], request: Request
) -> Dict[str, object]:
    user = USERS_DB.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated = dict(user)
    updated.update(payload)

    cache_key = f"cache:/users/{user_id}"
    redis = await get_redis()
    try:
        await redis.set(cache_key, json.dumps(updated), ex=120)  # SET with EXPIRE
        await redis.rpush(WRITE_BEHIND_QUEUE, json.dumps({"id": user_id, "data": payload}))
    except Exception:
        pass

    return {"queued": True, "user": updated}


@router.post("/jobs/write-behind/process")
async def process_write_behind() -> Dict[str, object]:
    redis = await get_redis()
    processed = 0

    while True:
        item = await redis.lpop(WRITE_BEHIND_QUEUE)
        if item is None:
            break

        try:
            payload = json.loads(item)
        except json.JSONDecodeError:
            continue

        user_id = int(payload.get("id", 0))
        updates = payload.get("data", {})
        user = USERS_DB.get(user_id)
        if user is None:
            continue

        user.update(updates)
        USERS_DB[user_id] = user
        processed += 1

    return {"processed": processed}
