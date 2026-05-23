"""Global exception handlers for standardized error responses"""
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from pydantic_core import ValidationError

logger = logging.getLogger("zenovox.exceptions")


async def global_sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Handle SQLAlchemy database exceptions.
    Hides internal database details from API consumers.
    """
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    logger.error(f"[{correlation_id}] Database exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "PERSISTENCE_TRANSACTION_FAILED",
            "message": "A system persistence exception occurred. Operations safely aborted.",
            "correlation_id": correlation_id
        }
    )


async def global_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors.
    Returns detailed validation error information.
    """
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    logger.warning(f"[{correlation_id}] Validation error: {str(exc)}")
    
    error_details = []
    for error in exc.errors():
        error_details.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "type": error["type"],
            "message": error["msg"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error_code": "SCHEMA_VALIDATION_ERROR",
            "message": "Supplied input variables failed serialization bounds.",
            "correlation_id": correlation_id,
            "details": error_details
        }
    )


async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all handler for unexpected exceptions.
    Logs error and returns generic error response.
    """
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    logger.error(f"[{correlation_id}] Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred while processing your request.",
            "correlation_id": correlation_id
        }
    )


async def http_exception_handler(request: Request, exc: Exception):
    """Handle HTTP exceptions"""
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    
    # Try to extract status code and detail
    status_code = getattr(exc, "status_code", 500)
    detail = getattr(exc, "detail", "An error occurred")
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error_code": f"HTTP_{status_code}",
            "message": detail,
            "correlation_id": correlation_id
        }
    )
