"""System observability and health check endpoints"""
import time
import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db_session
from app.redis_client import redis_client
from app.config import settings
from app.schemas import HealthCheckSchema

logger = logging.getLogger("zenovox.routers.system")

router = APIRouter()


@router.get("/health", response_model=HealthCheckSchema, status_code=status.HTTP_200_OK)
async def deep_infrastructure_health_check(db: AsyncSession = Depends(get_db_session)):
    """
    Performs full cross-check evaluation across active dependencies.
    
    Returns health status of:
    - PostgreSQL database
    - Redis cache broker
    
    Returns 503 if any critical dependency is unhealthy.
    """
    health_report = {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.VERSION,
        "checks": {
            "postgres": "unhealthy",
            "redis": "unhealthy"
        }
    }
    
    # 1. Evaluate relational database layer connectivity
    try:
        await db.execute(text("SELECT 1"))
        health_report["checks"]["postgres"] = "healthy"
        logger.info("PostgreSQL health check: passed")
    except Exception as e:
        health_report["status"] = "degraded"
        health_report["checks"]["postgres"] = f"unhealthy: {type(e).__name__}"
        logger.error(f"PostgreSQL health check failed: {str(e)}")

    # 2. Evaluate caching broker pool connection
    try:
        if await redis_client.ping():
            health_report["checks"]["redis"] = "healthy"
            logger.info("Redis health check: passed")
    except Exception as e:
        health_report["status"] = "degraded"
        health_report["checks"]["redis"] = f"unhealthy: {type(e).__name__}"
        logger.error(f"Redis health check failed: {str(e)}")

    # If critical services are down, return 503
    if health_report["status"] == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_report
        )
        
    return health_report


@router.get("/version", status_code=status.HTTP_200_OK)
async def get_version():
    """Get application version and environment information"""
    return {
        "version": settings.VERSION,
        "project_name": settings.PROJECT_NAME,
        "environment": settings.ENV,
        "timestamp": time.time()
    }


@router.get("/info", status_code=status.HTTP_200_OK)
async def get_application_info():
    """Get application configuration information (non-sensitive)"""
    return {
        "project_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENV,
        "database": {
            "pool_size": settings.DB_POOL_SIZE,
            "max_overflow": settings.DB_MAX_OVERFLOW
        },
        "features": {
            "rate_limiting": True,
            "async_tasks": True,
            "caching": True,
            "structured_logging": True
        },
        "timestamp": time.time()
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check(db: AsyncSession = Depends(get_db_session)):
    """
    Readiness check for orchestration platforms (Kubernetes, Docker, etc).
    Returns 200 only when service is ready to accept traffic.
    """
    try:
        # Quick database connectivity check
        await db.execute(text("SELECT 1"))
        
        # Quick Redis connectivity check
        await redis_client.ping()
        
        return {
            "ready": True,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"ready": False, "error": str(e)}
        )


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_check():
    """
    Liveness check for orchestration platforms.
    Indicates if the application process is still running.
    """
    return {
        "alive": True,
        "timestamp": time.time()
    }
