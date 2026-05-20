"""
Performance Comparison: Synchronous vs Asynchronous
Demonstrates the performance benefits of async programming
"""

import time
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# SYNCHRONOUS IMPLEMENTATION
# ============================================================================

def sync_io_operation(task_id: int, duration: float = 1.0):
    """Simulates a blocking I/O operation"""
    print(f"[SYNC] Task {task_id}: Starting...")
    time.sleep(duration)  # Blocks the entire thread
    print(f"[SYNC] Task {task_id}: Completed")
    return f"Result {task_id}"


def sync_process_multiple_tasks(count: int = 5):
    """Process multiple tasks sequentially (synchronous)"""
    print(f"\n{'='*70}")
    print(f"SYNCHRONOUS: Processing {count} tasks sequentially")
    print(f"{'='*70}")
    
    start = time.time()
    results = []
    
    for i in range(1, count + 1):
        result = sync_io_operation(i)
        results.append(result)
    
    elapsed = time.time() - start
    throughput = count / elapsed
    
    print(f"\nResults: {results}")
    print(f"Total time: {elapsed:.2f} seconds")
    print(f"Throughput: {throughput:.2f} tasks/second")
    print(f"Average time per task: {elapsed/count:.2f} seconds")
    
    return elapsed, throughput


# ============================================================================
# ASYNCHRONOUS IMPLEMENTATION
# ============================================================================

async def async_io_operation(task_id: int, duration: float = 1.0):
    """Simulates a non-blocking I/O operation"""
    print(f"[ASYNC] Task {task_id}: Starting...")
    await asyncio.sleep(duration)  # Non-blocking - releases control
    print(f"[ASYNC] Task {task_id}: Completed")
    return f"Result {task_id}"


async def async_process_multiple_tasks(count: int = 5):
    """Process multiple tasks concurrently (asynchronous)"""
    print(f"\n{'='*70}")
    print(f"ASYNCHRONOUS: Processing {count} tasks concurrently")
    print(f"{'='*70}")
    
    start = time.time()
    
    # Create all tasks concurrently
    tasks = [async_io_operation(i) for i in range(1, count + 1)]
    results = await asyncio.gather(*tasks)
    
    elapsed = time.time() - start
    throughput = count / elapsed
    
    print(f"\nResults: {results}")
    print(f"Total time: {elapsed:.2f} seconds")
    print(f"Throughput: {throughput:.2f} tasks/second")
    print(f"Average time per task: {elapsed/count:.2f} seconds")
    
    return elapsed, throughput


# ============================================================================
# PERFORMANCE COMPARISON
# ============================================================================

def compare_performance(task_count: int = 10, duration: float = 0.5):
    """Compare sync vs async performance"""
    print("\n" + "="*70)
    print("PERFORMANCE COMPARISON: SYNC vs ASYNC")
    print("="*70)
    print(f"Configuration: {task_count} tasks, {duration}s per task")
    print(f"Expected sync time: {task_count * duration:.2f}s")
    print(f"Expected async time: {duration:.2f}s (approximately)")
    
    # Synchronous execution
    sync_time, sync_throughput = sync_process_multiple_tasks(task_count)
    
    # Asynchronous execution
    async_time, async_throughput = asyncio.run(
        async_process_multiple_tasks(task_count)
    )
    
    # Analysis
    print(f"\n{'='*70}")
    print("COMPARISON RESULTS")
    print(f"{'='*70}")
    print(f"Synchronous time:   {sync_time:.2f}s")
    print(f"Asynchronous time:  {async_time:.2f}s")
    print(f"Time saved:         {sync_time - async_time:.2f}s ({((sync_time - async_time)/sync_time)*100:.1f}%)")
    print(f"\nSync throughput:    {sync_throughput:.2f} tasks/sec")
    print(f"Async throughput:   {async_throughput:.2f} tasks/sec")
    print(f"Speedup:            {async_throughput/sync_throughput:.1f}x faster")
    print("="*70)
    
    return {
        "sync_time": sync_time,
        "async_time": async_time,
        "speedup_factor": sync_time / async_time,
        "time_saved_percent": ((sync_time - async_time) / sync_time) * 100
    }


# ============================================================================
# CONCURRENT LOAD SIMULATION
# ============================================================================

async def simulate_concurrent_load(concurrent_count: int = 20, duration: float = 0.5):
    """Simulate handling many concurrent operations"""
    print(f"\n{'='*70}")
    print(f"CONCURRENT LOAD TEST: {concurrent_count} concurrent operations")
    print(f"{'='*70}")
    
    start = time.time()
    
    # Create all operations concurrently
    tasks = [async_io_operation(i, duration) for i in range(concurrent_count)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    elapsed = time.time() - start
    throughput = concurrent_count / elapsed
    
    successful = sum(1 for r in results if not isinstance(r, Exception))
    
    print(f"\nConcurrent operations: {concurrent_count}")
    print(f"Successful: {successful}")
    print(f"Total time: {elapsed:.2f}s")
    print(f"Throughput: {throughput:.2f} ops/sec")
    print(f"Expected with sync: {concurrent_count * duration:.2f}s")
    print(f"Time saved: {(concurrent_count * duration) - elapsed:.2f}s")
    
    return {
        "concurrent_count": concurrent_count,
        "total_time": elapsed,
        "throughput": throughput,
        "expected_sync_time": concurrent_count * duration
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all performance tests"""
    print("\n" + "#"*70)
    print("# ASYNC vs SYNC PERFORMANCE COMPARISON")
    print("#"*70)
    
    # Test 1: Basic comparison
    print("\n\nTEST 1: Basic Performance Comparison")
    comparison = compare_performance(task_count=5, duration=1.0)
    
    # Test 2: Higher load
    print("\n\nTEST 2: Increased Load (10 tasks)")
    asyncio.run(async_process_multiple_tasks(10))
    
    # Test 3: Concurrent load
    print("\n\nTEST 3: High Concurrent Load")
    load_result = asyncio.run(simulate_concurrent_load(50, duration=0.5))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"✓ Async is {comparison['speedup_factor']:.1f}x faster for this workload")
    print(f"✓ Time saved: {comparison['time_saved_percent']:.1f}%")
    print(f"✓ Async throughput: {load_result['throughput']:.2f} ops/sec")
    print("\nKey Insight:")
    print("Asynchronous programming becomes even MORE valuable as")
    print("concurrent load increases. For 50 concurrent operations:")
    print(f"  - Sync would need: {load_result['expected_sync_time']:.1f}s")
    print(f"  - Async needs:    {load_result['total_time']:.2f}s")
    print("="*70)


if __name__ == "__main__":
    main()
