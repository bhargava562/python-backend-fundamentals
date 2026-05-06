from fastapi import APIRouter, HTTPException
from app.core.logger import logger
import time

router = APIRouter(prefix="/debug", tags=["Debugging & Performance"])

@router.get("/success")
async def successful_endpoint():
    """Test endpoint that always succeeds"""
    logger.info("Success endpoint accessed.")
    return {"message": "Everything is working perfectly!", "status": "ok"}

@router.get("/slow")
async def slow_endpoint():
    """Simulates a slow database query for performance testing"""
    logger.debug("Slow endpoint hit. Simulating a heavy database query...")
    start_time = time.time()
    
    # Simulate slow operation (2.5 seconds)
    time.sleep(2.5) 
    
    process_time = time.time() - start_time
    logger.info(f"Slow operation completed in {process_time:.2f} seconds.")
    return {
        "message": "Data retrieved", 
        "processing_time": process_time,
        "status": "completed"
    }

@router.get("/intentional-error")
async def intentional_bug():
    """Demonstrates error handling with a deliberate bug"""
    logger.warning("A user triggered the intentional bug endpoint!")
    try:
        # Simulating a Division by Zero error to trigger the global exception handler
        faulty_calculation = 100 / 0
        return {"result": faulty_calculation}
    except ZeroDivisionError as e:
        logger.error(f"Division by zero error caught: {str(e)}")
        raise HTTPException(status_code=500, detail="Mathematical error occurred")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return {
        "status": "healthy",
        "message": "API is running"
    }

@router.get("/performance/{duration}")
async def performance_test(duration: float = 1.0):
    """Test performance with configurable duration"""
    logger.info(f"Performance test requested for {duration} seconds")
    start_time = time.time()
    time.sleep(duration)
    elapsed = time.time() - start_time
    logger.info(f"Performance test completed in {elapsed:.3f} seconds")
    return {
        "requested_duration": duration,
        "actual_duration": elapsed,
        "test_status": "completed"
    }

@router.get("/debug-info")
async def debug_info():
    """Returns debug information about the application"""
    logger.debug("Debug info endpoint accessed")
    return {
        "app_name": "Day 10: Debugging & API Testing",
        "version": "1.0.0",
        "debug_mode": True,
        "available_endpoints": [
            "/api/users",
            "/api/products",
            "/api/orders",
            "/debug/health",
            "/debug/success",
            "/debug/slow",
            "/debug/intentional-error"
        ]
    }