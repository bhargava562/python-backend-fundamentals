"""FastAPI main application."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.database.config import engine
from app.models.models import Base
from app.routers import auth_routes, categories_routes, products_routes, cart_routes, orders_routes, reviews_routes

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="E-Commerce REST API",
    description="A comprehensive REST API for e-commerce operations",
    version="1.0.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for database errors
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    """Handle database errors gracefully."""
    raise HTTPException(
        status_code=500,
        detail="Database error occurred. Please try again later."
    )


# Include routers
app.include_router(auth_routes.router)
app.include_router(categories_routes.router)
app.include_router(products_routes.router)
app.include_router(cart_routes.router)
app.include_router(orders_routes.router)
app.include_router(reviews_routes.router)
app.include_router(reviews_routes.review_router)


@app.get("/", tags=["Health Check"])
def root():
    """Root endpoint - health check."""
    return {
        "message": "Welcome to E-Commerce REST API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health Check"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
