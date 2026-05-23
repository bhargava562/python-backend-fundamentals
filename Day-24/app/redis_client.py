"""Redis connection pool and async client interface"""
import redis.asyncio as aioredis
from app.config import settings


# Create connection pool for efficient Redis management
redis_pool = aioredis.ConnectionPool.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    max_connections=50
)

# Shared Redis client instance with connection pooling
redis_client = aioredis.Redis(connection_pool=redis_pool)


async def close_redis():
    """Close Redis connection pool"""
    await redis_client.close()
