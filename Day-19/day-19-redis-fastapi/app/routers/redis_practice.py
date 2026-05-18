from __future__ import annotations

import json
from typing import Dict, List

from fastapi import APIRouter

from ..database import get_redis


router = APIRouter(prefix="/practice", tags=["practice"])


@router.get("/strings")
async def practice_strings() -> Dict[str, object]:
    redis = await get_redis()
    key = "practice:string"
    json_key = "practice:json"

    await redis.set(key, "hello")  # SET
    value = await redis.get(key)  # GET
    exists = await redis.exists(key)  # EXISTS
    await redis.expire(key, 60)  # EXPIRE
    ttl = await redis.ttl(key)

    payload = {"type": "demo", "value": 123}
    await redis.set(json_key, json.dumps(payload))
    json_value = await redis.get(json_key)

    return {
        "value": value,
        "exists": bool(exists),
        "ttl_seconds": ttl,
        "json_string": json_value,
    }


@router.get("/lists")
async def practice_lists() -> Dict[str, List[str]]:
    redis = await get_redis()
    key = "practice:list"

    await redis.delete(key)
    await redis.lpush(key, "first")  # LPUSH
    await redis.rpush(key, "second")  # RPUSH
    await redis.rpush(key, "third")

    values = await redis.lrange(key, 0, -1)  # LRANGE
    return {"values": values}


@router.get("/sets")
async def practice_sets() -> Dict[str, List[str]]:
    redis = await get_redis()
    key = "practice:set"

    await redis.delete(key)
    await redis.sadd(key, "alpha", "beta", "alpha")  # SADD
    values = await redis.smembers(key)

    return {"values": sorted(values)}


@router.get("/hashes")
async def practice_hashes() -> Dict[str, Dict[str, str]]:
    redis = await get_redis()
    key = "practice:hash"

    await redis.delete(key)
    await redis.hset(key, mapping={"name": "Ava", "role": "admin"})  # HSET
    values = await redis.hgetall(key)  # HGETALL

    return {"values": values}


@router.get("/sorted-sets")
async def practice_sorted_sets() -> Dict[str, List[Dict[str, object]]]:
    redis = await get_redis()
    key = "practice:zset"

    await redis.delete(key)
    await redis.zadd(key, {"silver": 20, "gold": 50, "bronze": 10})  # ZADD
    values = await redis.zrange(key, 0, -1, withscores=True)  # ZRANGE

    return {
        "values": [
            {"member": member, "score": score} for member, score in values
        ]
    }
