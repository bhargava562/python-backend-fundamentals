from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logger import logger

async def global_exception_handler(request: Request, exc: Exception):
    # Log the exact error with traceback info
    logger.error(f"Global Exception Caught: {str(exc)} on {request.method} {request.url}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong. Please check the logs.",
            "path": str(request.url)
        }
    )

async def validation_exception_handler(request: Request, exc: Exception):
    logger.warning(f"Validation Error: {str(exc)} on {request.method} {request.url}")
    return JSONResponse(
        status_code=422,
        content={"error": "Unprocessable Entity", "details": exc.errors()}
    )