"""Business operations endpoints with rate limiting"""
import json
import logging
from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db_session
from app.schemas import (
    ExecutionRequestSchema,
    ExecutionResponseSchema,
    OperationalLogSchema,
    TaskStatusSchema
)
from app.models import OperationalLog
from app.tasks import execute_heavy_data_transform
from app.redis_client import redis_client

logger = logging.getLogger("zenovox.routers.business")

router = APIRouter()


@router.post(
    "/process",
    response_model=ExecutionResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Dispatch background operation",
    description="Accepts business payload actions securely, indexes trace details inside PostgreSQL, "
                "and hands off execution context to the background Celery cluster."
)
async def dispatch_background_operation(
    payload: ExecutionRequestSchema,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Initiates a long-running background operation.
    
    - **reference_id**: Unique transaction identifier
    - **summary**: Description of the operation
    
    Returns: Task ID and status for tracking
    """
    try:
        # 1. Create audit log entry
        new_log = OperationalLog(
            reference_id=payload.reference_id,
            payload_summary=payload.summary,
            status="pending"
        )
        db.add(new_log)
        await db.flush()
        
        logger.info(f"Created operation log for reference_id: {payload.reference_id}")
        
        # 2. Hand off context processing tasks asynchronously
        task_signature = execute_heavy_data_transform.delay(
            transaction_id=payload.reference_id,
            context={"action_scope": payload.summary}
        )
        
        # 3. Update log with task ID
        new_log.task_id = task_signature.id
        await db.flush()
        
        logger.info(f"Dispatched Celery task {task_signature.id} for {payload.reference_id}")
        
        # 4. Cache task reference for quick lookup
        await redis_client.setex(
            f"task:{task_signature.id}",
            3600,  # 1 hour expiration
            json.dumps({
                "reference_id": payload.reference_id,
                "created_at": str(new_log.created_at)
            })
        )
        
        return {
            "reference_id": payload.reference_id,
            "task_id": task_signature.id,
            "status": "queued_for_worker_processing"
        }
        
    except Exception as exc:
        logger.error(f"Failed to dispatch operation for {payload.reference_id}: {str(exc)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to dispatch operation", "reference_id": payload.reference_id}
        )


@router.get(
    "/operations",
    response_model=list[OperationalLogSchema],
    status_code=status.HTTP_200_OK,
    summary="List operations"
)
async def list_operations(
    db: AsyncSession = Depends(get_db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status_filter: Optional[str] = Query(None, description="Filter by status (pending, success, failed)")
):
    """
    List all operational logs with pagination.
    
    Query Parameters:
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return (max 100)
    - **status_filter**: Filter by operation status
    """
    try:
        query = select(OperationalLog).order_by(desc(OperationalLog.created_at))
        
        if status_filter:
            query = query.where(OperationalLog.status == status_filter)
        
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        operations = result.scalars().all()
        
        logger.info(f"Retrieved {len(operations)} operations (skip={skip}, limit={limit})")
        return operations
        
    except Exception as exc:
        logger.error(f"Failed to retrieve operations: {str(exc)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to retrieve operations"}
        )


@router.get(
    "/operations/{reference_id}",
    response_model=OperationalLogSchema,
    status_code=status.HTTP_200_OK,
    summary="Get operation details"
)
async def get_operation(
    reference_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Retrieve details of a specific operation by reference ID.
    """
    try:
        query = select(OperationalLog).where(OperationalLog.reference_id == reference_id)
        result = await db.execute(query)
        operation = result.scalars().first()
        
        if not operation:
            logger.warning(f"Operation not found: {reference_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Operation {reference_id} not found"}
            )
        
        logger.info(f"Retrieved operation: {reference_id}")
        return operation
        
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Failed to retrieve operation {reference_id}: {str(exc)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to retrieve operation"}
        )


@router.get(
    "/task-status/{task_id}",
    response_model=TaskStatusSchema,
    status_code=status.HTTP_200_OK,
    summary="Get task execution status"
)
async def get_task_status(task_id: str):
    """
    Retrieve the execution status of a background task.
    
    Returns task state and result if completed.
    """
    try:
        task = execute_heavy_data_transform.AsyncResult(task_id)
        
        # Try to get reference_id from cache
        cached_info = await redis_client.get(f"task:{task_id}")
        reference_id = "unknown"
        if cached_info:
            reference_id = json.loads(cached_info).get("reference_id", "unknown")
        
        result = {
            "task_id": task_id,
            "reference_id": reference_id,
            "status": task.state.lower(),
            "result": None
        }
        
        if task.successful():
            result["result"] = task.result
        elif task.failed():
            result["result"] = {"error": str(task.info)}
        
        logger.info(f"Retrieved task status for {task_id}: {task.state}")
        return result
        
    except Exception as exc:
        logger.error(f"Failed to retrieve task status {task_id}: {str(exc)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to retrieve task status"}
        )


@router.post(
    "/batch-process",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Dispatch batch operations"
)
async def batch_process(
    payloads: list[ExecutionRequestSchema],
    db: AsyncSession = Depends(get_db_session)
):
    """
    Dispatch multiple operations in a single batch.
    
    Useful for processing multiple items simultaneously.
    Returns array of task IDs.
    """
    try:
        if len(payloads) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Batch size cannot exceed 100 items"}
            )
        
        results = []
        for payload in payloads:
            task_signature = execute_heavy_data_transform.delay(
                transaction_id=payload.reference_id,
                context={"action_scope": payload.summary}
            )
            
            # Create log entry
            new_log = OperationalLog(
                reference_id=payload.reference_id,
                payload_summary=payload.summary,
                status="pending",
                task_id=task_signature.id
            )
            db.add(new_log)
            
            results.append({
                "reference_id": payload.reference_id,
                "task_id": task_signature.id
            })
        
        await db.flush()
        logger.info(f"Dispatched batch of {len(payloads)} operations")
        
        return {
            "batch_size": len(payloads),
            "tasks": results
        }
        
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Failed to dispatch batch: {str(exc)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to dispatch batch operations"}
        )
