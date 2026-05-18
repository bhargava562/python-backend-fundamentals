from __future__ import annotations

import asyncio
from typing import Dict, List

from fastapi import APIRouter, Request

from ..database import PRODUCTS_DB
from ..decorators import cache_response


router = APIRouter(prefix="/search", tags=["search"])


@router.get("/products")
@cache_response(ttl_seconds=45)
async def search_products(q: str = "", request: Request | None = None) -> List[Dict[str, object]]:
    await asyncio.sleep(2)
    query = q.strip().lower()
    if not query:
        return list(PRODUCTS_DB.values())

    results: List[Dict[str, object]] = []
    for product in PRODUCTS_DB.values():
        name = str(product.get("name", "")).lower()
        if query in name:
            results.append(product)

    return results
