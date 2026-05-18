from __future__ import annotations

import functools
import json
from typing import Any, Awaitable, Callable, Dict, TypeVar

from fastapi import Request
from fastapi.responses import JSONResponse, Response

from .database import get_redis


F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def cache_response(ttl_seconds: int) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Response:
            request: Request | None = kwargs.get("request")
            if request is None:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if request is None:
                result = await func(*args, **kwargs)
                return JSONResponse(content=result)

            cache_key = f"cache:{request.url.path}"
            if request.url.query:
                cache_key = f"{cache_key}?{request.url.query}"

            redis = await get_redis()
            try:
                cached_payload = await redis.get(cache_key)  # GET
            except Exception:
                cached_payload = None

            if cached_payload is not None:
                try:
                    await redis.incr("metrics:cache:hits")  # INCR
                except Exception:
                    pass
                return JSONResponse(content=json.loads(cached_payload))

            try:
                await redis.incr("metrics:cache:misses")  # INCR
            except Exception:
                pass

            result = await func(*args, **kwargs)
            payload = json.dumps(result)

            try:
                await redis.set(cache_key, payload, ex=ttl_seconds)  # SET with EXPIRE
            except Exception:
                pass

            return JSONResponse(content=result)

        return wrapper  # type: ignore[return-value]

    return decorator
