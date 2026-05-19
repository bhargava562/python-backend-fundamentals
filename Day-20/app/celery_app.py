from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue
import os
from datetime import timedelta

# Initialize Celery
# Using 'redis' as the hostname for Docker Compose networking
# Initialize Celery
# Using 'redis' as the hostname for Docker Compose networking
celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
)

# Import tasks module to register tasks with Celery
import app.tasks  # noqa: F401

# ============================================================================
# CELERY CONFIGURATION
# ============================================================================

celery_app.conf.update(
    # Task serialization
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Timezone and time settings
    timezone='UTC',
    enable_utc=True,
    
    # Task execution settings
    task_acks_late=True,  # Worker acknowledges task only after completion
    task_reject_on_worker_lost=True,  # Requeue task if worker disconnects
    worker_prefetch_multiplier=4,  # Workers fetch 4 tasks at a time
    worker_max_tasks_per_child=1000,  # Restart worker after 1000 tasks (prevents memory leaks)
    
    # Result backend settings
    result_expires=3600,  # Results expire after 1 hour
    result_extended=True,  # Store extended result info
    
    # Retry settings
    task_autoretry_for=(Exception,),
    task_max_retries=3,
    
    # Broker settings
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=10,
)

# ============================================================================
# TASK ROUTING & QUEUES
# ============================================================================

# Define custom queues for different task types
email_exchange = Exchange('email', type='direct', durable=True)
reports_exchange = Exchange('reports', type='direct', durable=True)
images_exchange = Exchange('images', type='direct', durable=True)
data_exchange = Exchange('data', type='direct', durable=True)
default_exchange = Exchange('celery', type='direct', durable=True)

celery_app.conf.task_queues = (
    Queue('email', exchange=email_exchange, routing_key='email', queue_arguments={'x-max-priority': 10}),
    Queue('reports', exchange=reports_exchange, routing_key='reports', queue_arguments={'x-max-priority': 5}),
    Queue('images', exchange=images_exchange, routing_key='images', queue_arguments={'x-max-priority': 3}),
    Queue('data', exchange=data_exchange, routing_key='data', queue_arguments={'x-max-priority': 2}),
    Queue('default', exchange=default_exchange, routing_key='default'),
)

# Task routing configuration
celery_app.conf.task_routes = {
    # Email tasks to email queue
    'app.tasks.send_email_task': {'queue': 'email', 'routing_key': 'email'},
    'app.tasks.send_bulk_email_task': {'queue': 'email', 'routing_key': 'email'},
    
    # Report tasks to reports queue
    'app.tasks.generate_pdf_report': {'queue': 'reports', 'routing_key': 'reports'},
    'app.tasks.generate_csv_report': {'queue': 'reports', 'routing_key': 'reports'},
    'app.tasks.generate_full_report': {'queue': 'reports', 'routing_key': 'reports'},
    'app.tasks.combine_reports': {'queue': 'reports', 'routing_key': 'reports'},
    'app.tasks.generate_hourly_report': {'queue': 'reports', 'routing_key': 'reports'},
    'app.tasks.generate_daily_summary': {'queue': 'reports', 'routing_key': 'reports'},
    
    # Image tasks to images queue
    'app.tasks.process_image_task': {'queue': 'images', 'routing_key': 'images'},
    'app.tasks.resize_image': {'queue': 'images', 'routing_key': 'images'},
    'app.tasks.compress_image': {'queue': 'images', 'routing_key': 'images'},
    'app.tasks.process_multiple_images': {'queue': 'images', 'routing_key': 'images'},
    
    # Data tasks to data queue
    'app.tasks.import_data': {'queue': 'data', 'routing_key': 'data'},
    'app.tasks.export_data': {'queue': 'data', 'routing_key': 'data'},
    
    # Periodic/system tasks to default queue
    'app.tasks.cleanup_database': {'queue': 'default'},
    'app.tasks.check_system_health': {'queue': 'default'},
    'app.tasks.send_weekly_digest': {'queue': 'email', 'routing_key': 'email'},
}

# ============================================================================
# CELERY BEAT SCHEDULE (PERIODIC TASKS)
# ============================================================================

celery_app.conf.beat_schedule = {
    # System Health Check - Every 5 minutes
    'check-system-health-every-5min': {
        'task': 'app.tasks.check_system_health',
        'schedule': timedelta(minutes=5),
        'options': {'queue': 'default'}
    },
    
    # Database Cleanup - Daily at midnight (00:00 UTC)
    'daily-database-cleanup': {
        'task': 'app.tasks.cleanup_database',
        'schedule': crontab(minute=0, hour=0),
        'options': {'queue': 'default'},
        'kwargs': {}
    },
    
    # Hourly Report - Every hour at minute 0
    'hourly-report-generation': {
        'task': 'app.tasks.generate_hourly_report',
        'schedule': crontab(minute=0),
        'options': {'queue': 'reports'},
        'kwargs': {}
    },
    
    # Daily Summary - Daily at 1:00 AM UTC
    'daily-summary-report': {
        'task': 'app.tasks.generate_daily_summary',
        'schedule': crontab(minute=0, hour=1),
        'options': {'queue': 'reports'},
        'kwargs': {}
    },
    
    # Weekly Digest - Every Monday at 8:00 AM UTC
    'weekly-email-digest': {
        'task': 'app.tasks.send_weekly_digest',
        'schedule': crontab(minute=0, hour=8, day_of_week=1),
        'options': {'queue': 'email'},
        'kwargs': {}
    },
}
