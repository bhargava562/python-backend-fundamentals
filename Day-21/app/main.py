"""
FastAPI Application - Async Implementation
Main application setup with database connection and startup/shutdown events
"""

from fastapi import FastAPI, HTTPException, WebSocket
from contextlib import asynccontextmanager
import asyncio
import logging
from typing import Optional
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# SIMULATED DATABASE - For demonstration without PostgreSQL
# ============================================================================

class AsyncDatabase:
    """Simulated async database for demonstration"""
    
    def __init__(self):
        self.data = {
            "documents": {
                1: {"id": 1, "title": "Document 1", "content": "Content 1", "category": "tech"},
                2: {"id": 2, "title": "Document 2", "content": "Content 2", "category": "business"},
                3: {"id": 3, "title": "Document 3", "content": "Content 3", "category": "tech"},
            },
            "users": {
                1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
                2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
                3: {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
            }
        }
        self.is_connected = False
    
    async def connect(self):
        """Simulate database connection"""
        await asyncio.sleep(0.5)
        self.is_connected = True
        logger.info("Database connected")
    
    async def disconnect(self):
        """Simulate database disconnection"""
        await asyncio.sleep(0.2)
        self.is_connected = False
        logger.info("Database disconnected")
    
    async def fetch_document(self, doc_id: int) -> dict:
        """Fetch a document from database"""
        await asyncio.sleep(0.2)  # Simulate I/O
        return self.data["documents"].get(doc_id, None)
    
    async def fetch_user(self, user_id: int) -> dict:
        """Fetch a user from database"""
        await asyncio.sleep(0.2)  # Simulate I/O
        return self.data["users"].get(user_id, None)
    
    async def fetch_all_documents(self) -> list:
        """Fetch all documents"""
        await asyncio.sleep(0.3)
        return list(self.data["documents"].values())
    
    async def fetch_all_users(self) -> list:
        """Fetch all users"""
        await asyncio.sleep(0.3)
        return list(self.data["users"].values())


# Initialize database
database = AsyncDatabase()


# ============================================================================
# LIFESPAN CONTEXT MANAGER - FastAPI 0.93+
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages app lifespan - startup and shutdown events
    This is the modern way instead of @app.on_event decorators
    """
    # STARTUP
    logger.info("Starting up FastAPI application...")
    await database.connect()
    logger.info("Application startup complete")
    
    yield  # App runs here
    
    # SHUTDOWN
    logger.info("Shutting down FastAPI application...")
    await database.disconnect()
    logger.info("Application shutdown complete")


# ============================================================================
# FASTAPI APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Day 21: Async FastAPI Application",
    description="Comprehensive async programming implementation with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# For older FastAPI versions (< 0.93), use these decorators instead:
# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database_connected": database.is_connected
    }


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Day 21 - Async FastAPI Application",
        "endpoints": {
            "health": "/health",
            "simple_fetch": "/documents/{doc_id}",
            "concurrent_fetch": "/documents/{doc_id}/enriched",
            "batch_fetch": "/batch/documents",
            "batch_users": "/batch/users",
            "concurrent_apis": "/external-data",
            "websocket": "/ws"
        },
        "docs": "/docs"
    }


# ============================================================================
# REGISTER ENDPOINTS
# ============================================================================

from . import endpoints
endpoints.setup_endpoints(app, database)
