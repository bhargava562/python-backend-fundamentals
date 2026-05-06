from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.api.debug_routes import router as debug_router
from app.api.user_routes import router as user_router
from app.api.product_routes import router as product_router
from app.api.order_routes import router as order_router
from app.exceptions.handlers import global_exception_handler, validation_exception_handler
from app.core.logger import logger

app = FastAPI(
    title="Day 10: Debugging & API Testing",
    description="Complete FastAPI application with debugging, logging, and testing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include Routes
app.include_router(debug_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)

@app.on_event("startup")
async def startup_event():
    logger.info("Application is starting up... Environments loaded.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application is shutting down. Cleaning up resources.")