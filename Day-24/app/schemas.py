"""Request and response data validation schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ExecutionRequestSchema(BaseModel):
    """Request schema for initiating background operations"""
    reference_id: str = Field(..., min_length=5, max_length=100, examples=["TX-99817"])
    summary: str = Field(..., max_length=200, examples=["Execution initialization engine batch context transformation"])
    
    class Config:
        json_schema_extra = {
            "example": {
                "reference_id": "TX-12345",
                "summary": "Process user data batch"
            }
        }


class ExecutionResponseSchema(BaseModel):
    """Response schema for successful operation initiation"""
    reference_id: str
    task_id: str
    status: str = "queued_for_worker_processing"
    
    class Config:
        json_schema_extra = {
            "example": {
                "reference_id": "TX-12345",
                "task_id": "abc123def456",
                "status": "queued_for_worker_processing"
            }
        }


class OperationalLogSchema(BaseModel):
    """Schema for operational log data"""
    id: int
    reference_id: str
    payload_summary: Optional[str] = None
    status: str
    task_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    response_data: Optional[str] = None
    
    class Config:
        from_attributes = True


class HealthCheckSchema(BaseModel):
    """Schema for health check response"""
    status: str
    timestamp: float
    version: str
    checks: Dict[str, str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": 1700000000.0,
                "version": "1.0.0",
                "checks": {
                    "postgres": "healthy",
                    "redis": "healthy"
                }
            }
        }


class ErrorResponseSchema(BaseModel):
    """Schema for standardized error responses"""
    error_code: str
    message: str
    correlation_id: Optional[str] = None
    details: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error_code": "VALIDATION_ERROR",
                "message": "Input validation failed",
                "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
                "details": None
            }
        }


class TaskStatusSchema(BaseModel):
    """Schema for task status response"""
    task_id: str
    reference_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "abc123def456",
                "reference_id": "TX-12345",
                "status": "completed",
                "result": {"processed_records": 1000}
            }
        }
