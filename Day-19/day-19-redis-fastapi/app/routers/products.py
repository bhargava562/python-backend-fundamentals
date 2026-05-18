from __future__ import annotations

import asyncio
from typing import Dict, List

from fastapi import APIRouter, HTTPException, Request

from ..database import PRODUCTS_DB
from ..decorators import cache_response


router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
@cache_response(ttl_seconds=60)
async def list_products(request: Request) -> List[Dict[str, object]]:
    await asyncio.sleep(2)
    return list(PRODUCTS_DB.values())


@router.get("/{product_id}")
@cache_response(ttl_seconds=60)
async def get_product(product_id: int, request: Request) -> Dict[str, object]:
    await asyncio.sleep(2)
    product = PRODUCTS_DB.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
