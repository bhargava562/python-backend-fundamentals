"""FastAPI application factory with complete configuration"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from sqlalchemy.exc import SQLAlchemyError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import settings
from app.database import init_db, close_db, get_db_session
from app.redis_client import close_redis
from app.middleware.logging_mw import ProductionLoggingMiddleware, RequestIDMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.exceptions.handlers import (
    global_sqlalchemy_exception_handler,
    global_validation_exception_handler,
    global_exception_handler,
    http_exception_handler
)
from app.routers import system, business

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("zenovox.main")


def create_application() -> FastAPI:
    """
    Application factory pattern implementation.
    
    Creates and configures a FastAPI instance with:
    - Middleware for logging, security, rate limiting
    - Exception handlers for standard error patterns
    - Router integration for all API endpoints
    - Startup and shutdown event handlers
    - OpenAPI documentation
    """
    
    # Initialize FastAPI with metadata
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Production-ready backend system with async tasks, caching, and comprehensive logging",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # ===== Rate Limiting Configuration =====
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[settings.RATE_LIMIT_RULE]
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    # ===== CORS Configuration =====
    # Security: Only allow specified origins in production
    allowed_origins = (
        [settings.ALLOWED_HOSTS]
        if settings.ALLOWED_HOSTS != "*"
        else ["*"]
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        max_age=3600,
    )

    # ===== Custom Middleware Stack =====
    # Order matters: applied in reverse order (bottom to top)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(ProductionLoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)

    # ===== Exception Handlers =====
    # Database exceptions
    app.add_exception_handler(SQLAlchemyError, global_sqlalchemy_exception_handler)
    
    # Validation errors
    app.add_exception_handler(RequestValidationError, global_validation_exception_handler)
    
    # General exceptions (catch-all)
    app.add_exception_handler(Exception, global_exception_handler)

    # ===== Router Registration =====
    # System endpoints (health, version, info)
    app.include_router(
        system.router,
        prefix="/api/v1/system",
        tags=["System Observability"]
    )
    
    # Business endpoints (operations, tasks)
    app.include_router(
        business.router,
        prefix="/api/v1/operations",
        tags=["Business Services"]
    )

    # ===== Root Endpoint =====
    @app.get("/", tags=["Root"])
    async def root():
        """API root endpoint with service information"""
        return {
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "environment": settings.ENV,
            "docs_url": "/docs",
            "health_url": "/api/v1/system/health"
        }

    # ===== Startup Event =====
    @app.on_event("startup")
    async def startup_event():
        """Initialize database tables and resources on startup"""
        try:
            logger.info(f"[STARTUP] Initializing {settings.PROJECT_NAME} v{settings.VERSION}")
            logger.info(f"[STARTUP] Environment: {settings.ENV}")
            
            await init_db()
            logger.info("[STARTUP] Database initialized successfully")
            
            logger.info("[STARTUP] Application startup complete")
        except Exception as exc:
            logger.error(f"[STARTUP] Initialization failed: {str(exc)}", exc_info=True)
            raise

    # ===== Shutdown Event =====
    @app.on_event("shutdown")
    async def shutdown_event():
        """Clean up resources on shutdown"""
        try:
            logger.info("[SHUTDOWN] Starting graceful shutdown")
            
            await close_redis()
            logger.info("[SHUTDOWN] Redis connections closed")
            
            await close_db()
            logger.info("[SHUTDOWN] Database connections closed")
            
            logger.info("[SHUTDOWN] Shutdown complete")
        except Exception as exc:
            logger.error(f"[SHUTDOWN] Error during shutdown: {str(exc)}", exc_info=True)

    # ===== Custom OpenAPI Schema =====
    def custom_openapi():
        """Customize OpenAPI schema"""
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title=settings.PROJECT_NAME,
            version=settings.VERSION,
            description="Complete production-ready backend system",
            routes=app.routes,
        )
        
        # Add custom servers
        openapi_schema["servers"] = [
            {"url": "http://localhost:8000", "description": "Development"},
            {"url": "https://api.example.com", "description": "Production"}
        ]
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    logger.info(f"[FACTORY] {settings.PROJECT_NAME} application created successfully")
    return app


# Create application instance
app = create_application()

# Health check endpoint for container orchestration
@app.get("/health")
async def quick_health():
    """Quick health check endpoint (replicated from system router for reliability)"""
    return {"status": "ok", "version": settings.VERSION}
