import time
import random
import json
from datetime import datetime
from app.celery_app import celery_app
from celery.utils.log import get_task_logger
from celery import chain, group, chord

logger = get_task_logger(__name__)

# EMAIL TASKS
# ============================================================================

@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, email_address: str, subject: str, body: str = ""):
    """
    Send email with exponential backoff retry on failure.
    
    Args:
        email_address: Recipient email
        subject: Email subject
        body: Email body content
    
    Returns:
        dict: Task result with status and email info
    """
    try:
        logger.info(f"Starting to send email to {email_address} with subject '{subject}'...")
        time.sleep(2)  # Simulate network delay
        
        # Simulate occasional failures to test retry logic
        if random.random() < 0.3:  # 30% failure rate
            raise Exception("Simulated SMTP Server Error")
            
        logger.info(f"Email '{subject}' sent successfully to {email_address}")
        return {
            "status": "success",
            "email": email_address,
            "subject": subject,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as exc:
        logger.error(f"Failed to send email to {email_address}. Error: {str(exc)}")
        # Exponential backoff: 2s, 4s, 8s...
        countdown = 2 ** self.request.retries
        logger.info(f"Retrying in {countdown}s (attempt {self.request.retries + 1}/3)...")
        raise self.retry(exc=exc, countdown=countdown)


@celery_app.task(bind=True, max_retries=2)
def send_bulk_email_task(self, email_list: list, subject: str, body: str):
    """
    Send emails in bulk using group pattern for parallel execution.
    
    Args:
        email_list: List of email addresses
        subject: Email subject
        body: Email body
    
    Returns:
        dict: Summary of sent emails
    """
    try:
        logger.info(f"Starting bulk email task for {len(email_list)} recipients...")
        
        # Create group of tasks to run in parallel
        job = group(send_email_task.s(email, subject, body) for email in email_list)
        result = job.apply_async()
        
        logger.info(f"Bulk email group created with ID: {result.id}")
        return {
            "status": "bulk_email_queued",
            "recipient_count": len(email_list),
            "group_id": result.id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as exc:
        logger.error(f"Bulk email task failed: {str(exc)}")
        raise self.retry(exc=exc, countdown=5)


# ============================================================================
# IMAGE PROCESSING TASKS
# ============================================================================

@celery_app.task(bind=True, max_retries=2)
def resize_image(self, image_id: int, width: int, height: int):
    """Resize image to specified dimensions."""
    try:
        logger.info(f"Resizing image {image_id} to {width}x{height}...")
        time.sleep(3)
        logger.info(f"Image {image_id} resized successfully.")
        return {
            "image_id": image_id,
            "operation": "resize",
            "dimensions": f"{width}x{height}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as exc:
        logger.error(f"Failed to resize image {image_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=5)


@celery_app.task(bind=True, max_retries=2)
def compress_image(self, image_id: int, quality: int = 85):
    """Compress image to specified quality."""
    try:
        logger.info(f"Compressing image {image_id} to {quality}% quality...")
        time.sleep(2)
        logger.info(f"Image {image_id} compressed successfully.")
        return {
            "image_id": image_id,
            "operation": "compress",
            "quality": quality,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as exc:
        logger.error(f"Failed to compress image {image_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=5)


@celery_app.task()
def process_image_task(image_id: int):
    """
    Process image using chain pattern (sequential operations).
    1. Resize image
    2. Compress image
    3. Generate thumbnail
    """
    logger.info(f"Starting image processing workflow for image {image_id}...")
    
    # Chain: resize -> compress -> generate_thumbnail
    workflow = chain(
        resize_image.s(image_id, 1920, 1080),
        compress_image.s(85),
    )
    
    result = workflow.apply_async()
    logger.info(f"Image processing chain created with ID: {result.id}")
    
    return {
        "image_id": image_id,
        "status": "processing",
        "chain_id": result.id,
        "timestamp": datetime.now().isoformat()
    }


@celery_app.task()
def process_multiple_images(image_ids: list):
    """
    Process multiple images in parallel using group pattern.
    Each image goes through the full processing workflow.
    """
    logger.info(f"Starting batch image processing for {len(image_ids)} images...")
    
    # Group: process each image in parallel
    job = group(process_image_task.s(img_id) for img_id in image_ids)
    result = job.apply_async()
    
    logger.info(f"Batch image processing group created with ID: {result.id}")
    return {
        "batch_id": result.id,
        "image_count": len(image_ids),
        "status": "batch_processing",
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# REPORT GENERATION TASKS
# ============================================================================

@celery_app.task(bind=True, max_retries=2)
def generate_pdf_report(self, report_type: str, data: dict = None):
    """Generate PDF report with specified data."""
    try:
        logger.info(f"Generating {report_type} PDF report...")
        time.sleep(4)  # Simulate PDF generation
        
        filename = f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        logger.info(f"PDF report generated: {filename}")
        
        return {
            "report_type": report_type,
            "format": "PDF",
            "filename": filename,
            "size_mb": round(random.uniform(0.5, 5), 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as exc:
        logger.error(f"Failed to generate PDF report: {str(exc)}")
        raise self.retry(exc=exc, countdown=5)


@celery_app.task(bind=True, max_retries=2)
def generate_csv_report(self, report_type: str, rows: int = 1000):
    """Generate CSV report with specified number of rows."""
    try:
        logger.info(f"Generating {report_type} CSV report with {rows} rows...")
        time.sleep(2)  # Simulate CSV generation
        
        filename = f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        logger.info(f"CSV report generated: {filename}")
        
        return {
            "report_type": report_type,
            "format": "CSV",
            "filename": filename,
            "rows": rows,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as exc:
        logger.error(f"Failed to generate CSV report: {str(exc)}")
        raise self.retry(exc=exc, countdown=5)


@celery_app.task()
def generate_full_report(report_type: str):
    """
    Generate full report using chord pattern (parallel + final callback).
    Generate both PDF and CSV, then combine results.
    """
    logger.info(f"Starting full report generation for {report_type}...")
    
    # Chord: generate both in parallel, then combine results
    callback = combine_reports.s(report_type)
    workflow = chord([
        generate_pdf_report.s(report_type),
        generate_csv_report.s(report_type, 5000)
    ])(callback)
    
    logger.info(f"Full report generation chord created")
    return {
        "report_type": report_type,
        "status": "generating",
        "task_id": workflow.id,
        "timestamp": datetime.now().isoformat()
    }


@celery_app.task()
def combine_reports(results, report_type: str):
    """Combine PDF and CSV report results."""
    logger.info(f"Combining reports for {report_type}...")
    time.sleep(1)
    
    return {
        "report_type": report_type,
        "status": "completed",
        "reports": results,
        "combined_file": f"{report_type}_combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# DATA IMPORT/EXPORT TASKS
# ============================================================================

@celery_app.task(bind=True, max_retries=3)
def import_data(self, data_source: str, num_records: int):
    """
    Import data from external source.
    
    Args:
        data_source: Source of data (file, API, database, etc.)
        num_records: Number of records to import
    """
    try:
        logger.info(f"Starting data import from {data_source} ({num_records} records)...")
        
        # Simulate import delay based on record count
        time.sleep(min(num_records / 1000, 10))
        
        imported_count = random.randint(num_records - 100, num_records)
        logger.info(f"Successfully imported {imported_count}/{num_records} records")
        
        return {
            "data_source": data_source,
            "requested_records": num_records,
            "imported_records": imported_count,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as exc:
        logger.error(f"Data import failed: {str(exc)}")
        raise self.retry(exc=exc, countdown=10)


@celery_app.task(bind=True, max_retries=2)
def export_data(self, export_format: str, table_name: str, filter_criteria: dict = None):
    """
    Export data in specified format (JSON, CSV, Excel).
    
    Args:
        export_format: Format for export (json, csv, excel)
        table_name: Name of table to export
        filter_criteria: Optional filter criteria
    """
    try:
        logger.info(f"Exporting {table_name} to {export_format} format...")
        time.sleep(3)
        
        filename = f"{table_name}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format}"
        logger.info(f"Data export completed: {filename}")
        
        return {
            "table_name": table_name,
            "export_format": export_format,
            "filename": filename,
            "records_exported": random.randint(100, 5000),
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as exc:
        logger.error(f"Data export failed: {str(exc)}")
        raise self.retry(exc=exc, countdown=5)


# ============================================================================
# PERIODIC/SCHEDULED TASKS
# ============================================================================

@celery_app.task()
def cleanup_database():
    """Run scheduled database cleanup - removes old records and optimizes tables."""
    logger.info("Running scheduled database cleanup...")
    time.sleep(5)
    
    cleaned_records = random.randint(100, 1000)
    logger.info(f"Database cleanup completed. Removed {cleaned_records} old records.")
    
    return {
        "task": "database_cleanup",
        "cleaned_records": cleaned_records,
        "timestamp": datetime.now().isoformat()
    }


@celery_app.task()
def generate_hourly_report():
    """Generate hourly system report with metrics."""
    logger.info("Generating hourly system report...")
    time.sleep(2)
    
    report = {
        "report_type": "hourly_metrics",
        "cpu_usage": round(random.uniform(20, 90), 2),
        "memory_usage": round(random.uniform(40, 80), 2),
        "requests_processed": random.randint(1000, 5000),
        "errors": random.randint(0, 50),
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"Hourly report generated: {json.dumps(report)}")
    return report


@celery_app.task()
def generate_daily_summary():
    """Generate daily summary report."""
    logger.info("Generating daily summary report...")
    time.sleep(3)
    
    summary = {
        "report_type": "daily_summary",
        "total_requests": random.randint(50000, 100000),
        "total_errors": random.randint(50, 500),
        "average_response_time_ms": round(random.uniform(50, 500), 2),
        "unique_users": random.randint(1000, 5000),
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"Daily summary generated: {json.dumps(summary)}")
    return summary


@celery_app.task()
def send_weekly_digest():
    """Send weekly digest email."""
    logger.info("Sending weekly digest email...")
    time.sleep(2)
    
    return {
        "task": "weekly_digest",
        "recipients": random.randint(100, 1000),
        "status": "sent",
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# SYSTEM HEALTH TASKS
# ============================================================================

@celery_app.task()
def check_system_health():
    """Check system health and resource usage."""
    logger.info("Running system health check...")
    
    health_status = {
        "status": "healthy",
        "checks": {
            "database": "ok",
            "redis": "ok",
            "disk_space": "ok",
            "memory": "ok",
        },
        "metrics": {
            "cpu_usage": round(random.uniform(10, 50), 2),
            "memory_usage": round(random.uniform(30, 70), 2),
            "active_workers": random.randint(1, 10),
            "queued_tasks": random.randint(0, 100),
        },
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"Health check completed: {json.dumps(health_status)}")
    return health_status