"""Production logging middleware with structured JSON output"""
import time
import json
import logging
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send

logger = logging.getLogger("zenovox.structured.api")


class ProductionLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for structured JSON logging with correlation tracking.
    Logs all requests/responses in JSON format to stdout.
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id
        
        # Capture request context details
        client_ip = request.client.host if request.client else "unknown"
        request_body_preview = ""
        
        try:
            # Attempt to capture request body for logging (if applicable)
            if request.method in ["POST", "PUT", "PATCH"]:
                body = await request.body()
                request_body_preview = body[:200].decode("utf-8", errors="ignore") if body else ""
                # Re-attach body to request for route handlers
                async def receive() -> dict:
                    return {
                        "type": "http.request",
                        "body": body,
                        "more_body": False
                    }
                request._receive = receive
        except Exception:
            pass
        
        # Process request through handlers
        response: Response = await call_next(request)
        process_time_ms = (time.perf_counter() - start_time) * 1000

        # Build structured log payload
        log_level = "INFO" if response.status_code < 400 else ("ERROR" if response.status_code >= 500 else "WARNING")
        
        log_payload = {
            "timestamp": time.time(),
            "level": log_level,
            "correlation_id": correlation_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params) if request.query_params else {},
            "status_code": response.status_code,
            "latency_ms": round(process_time_ms, 2),
            "client_ip": client_ip,
            "user_agent": request.headers.get("user-agent", "unknown")[:100],
        }
        
        # Output structured JSON log to stdout
        print(json.dumps(log_payload))
        
        # Attach correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to attach request ID to all responses"""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response
