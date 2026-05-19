from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from celery.result import AsyncResult
from celery import chain, group, chord
from datetime import datetime
import logging

from app.celery_app import celery_app
from app.tasks import (
    send_email_task, send_bulk_email_task,
    process_image_task, process_multiple_images,
    generate_pdf_report, generate_csv_report, generate_full_report,
    import_data, export_data,
    cleanup_database, generate_hourly_report, 
    generate_daily_summary, send_weekly_digest,
    check_system_health
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(
    title="Celery Background Tasks API",
    description="Comprehensive Celery integration with FastAPI for async task management",
    version="1.0.0"
)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class EmailRequest(BaseModel):
    email: str
    subject: str
    body: str = ""

class BulkEmailRequest(BaseModel):
    emails: list[str]
    subject: str
    body: str = ""

class ImageProcessingRequest(BaseModel):
    image_ids: list[int]
    operation: str = "full"  # resize, compress, or full

class ReportRequest(BaseModel):
    report_type: str  # pdf, csv, or full
    data_rows: int = 1000

class DataImportRequest(BaseModel):
    data_source: str
    num_records: int

class DataExportRequest(BaseModel):
    export_format: str  # json, csv, or excel
    table_name: str
    filter_criteria: dict = None

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: dict = None
    error: str = None

# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Celery Background Tasks API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "worker_stats": "/stats/workers",
            "queue_info": "/stats/queues",
            "email": "/api/email",
            "reports": "/api/reports",
            "images": "/api/images",
            "data": "/api/data"
        }
    }

@app.get("/health")
async def health_check():
    """Check API and Celery health."""
    inspector = celery_app.control.inspect()
    active_tasks = inspector.active()
    registered_tasks = inspector.registered()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "workers": {
            "count": len(active_tasks) if active_tasks else 0,
            "active_tasks": sum(len(v) for v in active_tasks.values()) if active_tasks else 0,
            "registered_tasks": len(registered_tasks) if registered_tasks else 0
        }
    }

@app.get("/stats/workers")
async def worker_stats():
    """Get Celery worker statistics."""
    inspector = celery_app.control.inspect()
    
    return {
        "active": inspector.active(),
        "registered": inspector.registered(),
        "stats": inspector.stats(),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/stats/queues")
async def queue_stats():
    """Get task queue statistics."""
    inspector = celery_app.control.inspect()
    active_queues = inspector.active_queues()
    
    return {
        "active_queues": active_queues,
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# EMAIL TASK ENDPOINTS
# ============================================================================

@app.post("/api/email/send")
async def send_email(request: EmailRequest):
    """
    Send a single email asynchronously.
    
    Returns task ID immediately for status checking.
    """
    try:
        task = send_email_task.delay(request.email, request.subject, request.body)
        logger.info(f"Email task queued: {task.id}")
        return {
            "message": "Email task queued",
            "task_id": task.id,
            "status_url": f"/task/{task.id}"
        }
    except Exception as e:
        logger.error(f"Failed to queue email task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/email/send-bulk")
async def send_bulk_email(request: BulkEmailRequest):
    """
    Send emails to multiple recipients in bulk.
    Uses group pattern for parallel execution.
    """
    try:
        task = send_bulk_email_task.delay(request.emails, request.subject, request.body)
        logger.info(f"Bulk email task queued: {task.id}")
        return {
            "message": "Bulk email task queued",
            "task_id": task.id,
            "recipient_count": len(request.emails),
            "status_url": f"/task/{task.id}"
        }
    except Exception as e:
        logger.error(f"Failed to queue bulk email task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# IMAGE PROCESSING ENDPOINTS
# ============================================================================

@app.post("/api/images/process")
async def process_images(request: ImageProcessingRequest):
    """
    Process images with specified operation.
    
    Operations:
    - full: Complete processing pipeline (resize + compress)
    - batch: Process multiple images in parallel
    """
    try:
        if request.operation == "batch":
            task = process_multiple_images.delay(request.image_ids)
            message = "Batch image processing queued"
        else:
            job = group(process_image_task.s(img_id) for img_id in request.image_ids)
            result = job.apply_async()
            task = result
            message = "Image processing group queued"
        
        logger.info(f"Image processing task queued: {task.id}")
        return {
            "message": message,
            "task_id": task.id,
            "image_count": len(request.image_ids),
            "status_url": f"/task/{task.id}"
        }
    except Exception as e:
        logger.error(f"Failed to queue image processing task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# REPORT GENERATION ENDPOINTS
# ============================================================================

@app.post("/api/reports/generate")
async def generate_report(request: ReportRequest):
    """
    Generate reports in different formats.
    
    Formats:
    - pdf: Generate PDF report
    - csv: Generate CSV report
    - full: Generate both PDF and CSV using chord pattern
    """
    try:
        if request.report_type == "pdf":
            task = generate_pdf_report.delay(request.report_type)
            message = "PDF report generation queued"
        elif request.report_type == "csv":
            task = generate_csv_report.delay(request.report_type, request.data_rows)
            message = "CSV report generation queued"
        elif request.report_type == "full":
            task = generate_full_report.delay(request.report_type)
            message = "Full report (PDF + CSV) generation queued"
        else:
            raise ValueError(f"Unknown report type: {request.report_type}")
        
        logger.info(f"Report generation task queued: {task.id}")
        return {
            "message": message,
            "task_id": task.id,
            "report_type": request.report_type,
            "status_url": f"/task/{task.id}"
        }
    except Exception as e:
        logger.error(f"Failed to queue report generation task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/status/{task_id}")
async def report_status(task_id: str):
    """Get status of report generation task."""
    task_result = AsyncResult(task_id, app=celery_app)
    
    response = {
        "task_id": task_id,
        "status": task_result.status,
        "timestamp": datetime.now().isoformat()
    }
    
    if task_result.status == 'SUCCESS':
        response["result"] = task_result.result
    elif task_result.status == 'FAILURE':
        response["error"] = str(task_result.result)
    
    return response

# ============================================================================
# DATA IMPORT/EXPORT ENDPOINTS
# ============================================================================

@app.post("/api/data/import")
async def import_data_endpoint(request: DataImportRequest):
    """
    Import data from external source asynchronously.
    """
    try:
        task = import_data.delay(request.data_source, request.num_records)
        logger.info(f"Data import task queued: {task.id}")
        return {
            "message": "Data import task queued",
            "task_id": task.id,
            "data_source": request.data_source,
            "num_records": request.num_records,
            "status_url": f"/task/{task.id}"
        }
    except Exception as e:
        logger.error(f"Failed to queue data import task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/data/export")
async def export_data_endpoint(request: DataExportRequest):
    """
    Export data in specified format asynchronously.
    """
    try:
        task = export_data.delay(request.export_format, request.table_name, request.filter_criteria)
        logger.info(f"Data export task queued: {task.id}")
        return {
            "message": "Data export task queued",
            "task_id": task.id,
            "export_format": request.export_format,
            "table_name": request.table_name,
            "status_url": f"/task/{task.id}"
        }
    except Exception as e:
        logger.error(f"Failed to queue data export task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# TASK STATUS & MANAGEMENT ENDPOINTS
# ============================================================================

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """
    Get the status of a Celery task by ID.
    
    Statuses:
    - PENDING: Task not yet executed
    - STARTED: Task execution started
    - SUCCESS: Task completed successfully
    - FAILURE: Task failed
    - RETRY: Task is being retried
    - REVOKED: Task has been revoked/cancelled
    """
    task_result = AsyncResult(task_id, app=celery_app)
    
    response = {
        "task_id": task_id,
        "status": task_result.status,
        "timestamp": datetime.now().isoformat()
    }
    
    if task_result.status == 'SUCCESS':
        response["result"] = task_result.result
    elif task_result.status == 'FAILURE':
        response["error"] = str(task_result.result)
    elif task_result.status == 'RETRY':
        response["retry_info"] = {
            "retries": getattr(task_result, 'retries', None),
            "exc_info": str(task_result.result)
        }
    
    return response

@app.delete("/task/{task_id}")
async def cancel_task(task_id: str):
    """Cancel/revoke a pending or running task."""
    try:
        celery_app.control.revoke(task_id, terminate=True)
        logger.info(f"Task revoked: {task_id}")
        return {
            "message": "Task cancelled successfully",
            "task_id": task_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to cancel task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/active")
async def get_active_tasks():
    """Get list of all active tasks being processed."""
    inspector = celery_app.control.inspect()
    active_tasks = inspector.active()
    
    return {
        "active_tasks": active_tasks,
        "total_active": sum(len(v) for v in active_tasks.values()) if active_tasks else 0,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/tasks/scheduled")
async def get_scheduled_tasks():
    """Get list of scheduled/reserved tasks."""
    inspector = celery_app.control.inspect()
    reserved_tasks = inspector.reserved()
    
    return {
        "scheduled_tasks": reserved_tasks,
        "total_scheduled": sum(len(v) for v in reserved_tasks.values()) if reserved_tasks else 0,
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# SYSTEM & MAINTENANCE ENDPOINTS
# ============================================================================

@app.post("/system/cleanup")
async def trigger_cleanup():
    """Manually trigger database cleanup task."""
    try:
        task = cleanup_database.delay()
        logger.info(f"Cleanup task queued: {task.id}")
        return {
            "message": "Database cleanup task queued",
            "task_id": task.id,
            "status_url": f"/task/{task.id}"
        }
    except Exception as e:
        logger.error(f"Failed to queue cleanup task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/health-check")
async def system_health_check():
    """Manually trigger system health check."""
    try:
        result = check_system_health.delay()
        logger.info(f"Health check task queued: {result.id}")
        return {
            "message": "System health check queued",
            "task_id": result.id,
            "status_url": f"/task/{result.id}"
        }
    except Exception as e:
        logger.error(f"Failed to queue health check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/worker-info")
async def worker_info():
    """Get detailed information about Celery workers."""
    inspector = celery_app.control.inspect()
    
    stats = inspector.stats()
    active_tasks = inspector.active()
    registered = inspector.registered()
    
    workers_info = {}
    if stats:
        for worker_name, worker_stats in stats.items():
            workers_info[worker_name] = {
                "stats": worker_stats,
                "active_tasks": len(active_tasks.get(worker_name, [])) if active_tasks else 0,
                "registered_tasks": len(registered.get(worker_name, [])) if registered else 0
            }
    
    return {
        "workers": workers_info,
        "total_workers": len(workers_info),
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        },
    )