"""
Phase 2: Python asyncio Fundamentals
Basic Syntax and Sleep - Understanding async/await
"""
import asyncio
import time


# ============================================================================
# 1. BASIC ASYNC/AWAIT SYNTAX
# ============================================================================

async def fetch_data(id: int, delay: int = 2):
    """Simulates a network request using async sleep (non-blocking)"""
    print(f"Task {id}: Starting fetch...")
    await asyncio.sleep(delay)  # Non-blocking sleep - releases control to event loop
    print(f"Task {id}: Fetch complete.")
    return f"Data {id}"


# ============================================================================
# 2. SYNCHRONOUS VS ASYNCHRONOUS EXECUTION
# ============================================================================

def sync_version():
    """This takes 4 seconds total (2 + 2)"""
    start = time.time()
    time.sleep(2)  # Blocks entire thread
    print(f"Sync task 1 done")
    time.sleep(2)  # Must wait for first task
    print(f"Sync task 2 done")
    print(f"Sync total time: {time.time() - start:.2f}s")


async def async_version():
    """This takes ~2 seconds total - both run concurrently"""
    start = time.time()
    
    # Create tasks that will run concurrently
    task1 = asyncio.create_task(fetch_data(1, delay=2))
    task2 = asyncio.create_task(fetch_data(2, delay=2))
    
    # Await both tasks - they run at the same time!
    result1 = await task1
    result2 = await task2
    
    elapsed = time.time() - start
    print(f"\nAsync Results: {result1}, {result2}")
    print(f"Async total time: {elapsed:.2f}s")  # Takes ~2s, not 4s!
    return elapsed


# ============================================================================
# 3. ASYNCIO.GATHER() - AGGREGATING RESULTS FROM MULTIPLE TASKS
# ============================================================================

async def gather_example():
    """Using gather to run multiple tasks concurrently and collect results"""
    start = time.time()
    
    # Run all three fetch_data calls concurrently and wait for all
    results = await asyncio.gather(
        fetch_data(1, delay=2),
        fetch_data(2, delay=2),
        fetch_data(3, delay=2)
    )
    
    elapsed = time.time() - start
    print(f"\nGather Results: {results}")
    print(f"Gather total time: {elapsed:.2f}s")  # Takes ~2s, not 6s!


# ============================================================================
# 4. ERROR HANDLING WITH GATHER
# ============================================================================

async def failing_task(id: int):
    """A task that may fail"""
    await asyncio.sleep(1)
    if id == 2:
        raise ValueError(f"Task {id} failed!")
    return f"Success {id}"


async def gather_with_error_handling():
    """Using return_exceptions=True to handle errors gracefully"""
    print("\n--- Gather with error handling ---")
    
    # Without return_exceptions=True, the first exception crashes the gather
    results = await asyncio.gather(
        failing_task(1),
        failing_task(2),  # This will raise an error
        failing_task(3),
        return_exceptions=True  # Capture exceptions as results instead of raising
    )
    
    print(f"Results (with exceptions as values): {results}")
    
    # Process results and exceptions
    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"Task {i} failed with error: {result}")
        else:
            print(f"Task {i} succeeded: {result}")


# ============================================================================
# 5. ASYNCIO.CREATE_TASK() VS AWAIT
# ============================================================================

async def task_creation_example():
    """Demonstrates create_task vs direct await"""
    print("\n--- Task Creation Example ---")
    
    # Method 1: Direct await (sequential)
    print("Sequential execution:")
    start = time.time()
    result1 = await fetch_data(1, delay=1)
    result2 = await fetch_data(2, delay=1)
    print(f"Sequential time: {time.time() - start:.2f}s")  # Takes ~2s
    
    # Method 2: Create tasks (concurrent)
    print("\nConcurrent execution with create_task:")
    start = time.time()
    task1 = asyncio.create_task(fetch_data(3, delay=1))
    task2 = asyncio.create_task(fetch_data(4, delay=1))
    result3 = await task1
    result4 = await task2
    print(f"Concurrent time: {time.time() - start:.2f}s")  # Takes ~1s


# ============================================================================
# 6. RUNNING ASYNC CODE WITH ASYNCIO.RUN()
# ============================================================================

async def main():
    """Main entry point - uses asyncio.run() to execute"""
    print("="*70)
    print("ASYNCIO FUNDAMENTALS - Learning Materials")
    print("="*70)
    
    # Example 1: Basic async/await
    print("\n1. Basic Async/Await:")
    result = await fetch_data(1, delay=2)
    print(f"Result: {result}")
    
    # Example 2: Async vs Sync comparison
    print("\n2. Synchronous version (blocking):")
    sync_version()
    
    print("\n3. Asynchronous version (concurrent):")
    async_time = await async_version()
    
    # Example 3: Gather
    print("\n4. Using asyncio.gather():")
    await gather_example()
    
    # Example 4: Error handling
    print("\n5. Error Handling with gather:")
    await gather_with_error_handling()
    
    # Example 5: Task creation
    await task_creation_example()
    
    print("\n" + "="*70)
    print("KEY TAKEAWAYS:")
    print("="*70)
    print("✓ async def defines an async function")
    print("✓ await pauses execution until a coroutine completes")
    print("✓ asyncio.create_task() schedules concurrent execution")
    print("✓ asyncio.gather() runs multiple tasks concurrently")
    print("✓ asyncio.sleep() is non-blocking (unlike time.sleep())")
    print("✓ return_exceptions=True allows graceful error handling")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
