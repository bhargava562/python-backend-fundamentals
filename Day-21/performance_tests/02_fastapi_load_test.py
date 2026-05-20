"""
FastAPI Load Testing
Demonstrates performance under concurrent HTTP load
"""

import asyncio
import time
import httpx
import statistics
from typing import List, Dict
import json


class LoadTester:
    """Load testing utility for FastAPI endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[Dict] = []
    
    async def test_endpoint(self, endpoint: str, concurrent_requests: int = 10):
        """Test an endpoint with concurrent requests"""
        print(f"\n{'='*70}")
        print(f"LOAD TEST: {endpoint}")
        print(f"Concurrent requests: {concurrent_requests}")
        print(f"{'='*70}")
        
        url = f"{self.base_url}{endpoint}"
        self.results = []
        
        start = time.time()
        
        async with httpx.AsyncClient() as client:
            # Create concurrent requests
            tasks = [
                self._make_request(client, url, request_id)
                for request_id in range(concurrent_requests)
            ]
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start
        
        # Analyze results
        successful = sum(1 for r in responses if not isinstance(r, Exception))
        failed = len(responses) - successful
        
        response_times = [r["time"] for r in responses if not isinstance(r, Exception)]
        
        if response_times:
            avg_time = statistics.mean(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
            median_time = statistics.median(response_times)
        else:
            avg_time = min_time = max_time = median_time = 0
        
        throughput = concurrent_requests / total_time
        
        # Print results
        print(f"\nResults:")
        print(f"  Total time: {total_time:.3f}s")
        print(f"  Successful: {successful}/{concurrent_requests}")
        print(f"  Failed: {failed}")
        print(f"  Throughput: {throughput:.2f} req/sec")
        print(f"\nResponse Times:")
        print(f"  Average: {avg_time*1000:.2f}ms")
        print(f"  Min: {min_time*1000:.2f}ms")
        print(f"  Max: {max_time*1000:.2f}ms")
        print(f"  Median: {median_time*1000:.2f}ms")
        
        return {
            "endpoint": endpoint,
            "concurrent_requests": concurrent_requests,
            "total_time": total_time,
            "successful": successful,
            "failed": failed,
            "throughput": throughput,
            "avg_response_time": avg_time,
            "min_response_time": min_time,
            "max_response_time": max_time,
            "median_response_time": median_time
        }
    
    async def _make_request(self, client: httpx.AsyncClient, url: str, request_id: int) -> Dict:
        """Make a single HTTP request and measure time"""
        try:
            start = time.time()
            response = await client.get(url, timeout=30.0)
            elapsed = time.time() - start
            
            return {
                "request_id": request_id,
                "status": response.status_code,
                "time": elapsed,
                "success": True
            }
        except Exception as e:
            return {
                "request_id": request_id,
                "error": str(e),
                "success": False
            }
    
    async def run_multiple_tests(self, endpoint: str, loads: List[int]):
        """Run multiple load tests with increasing concurrent requests"""
        print(f"\n{'#'*70}")
        print(f"# LOAD TEST SERIES: {endpoint}")
        print(f"{'#'*70}")
        
        results = []
        for load in loads:
            result = await self.test_endpoint(endpoint, load)
            results.append(result)
            await asyncio.sleep(1)  # Wait between tests
        
        # Print summary
        print(f"\n{'='*70}")
        print("LOAD TEST SUMMARY")
        print(f"{'='*70}")
        print(f"{'Concurrent':<15} {'Time (s)':<12} {'RPS':<12} {'Avg Resp (ms)':<15}")
        print("-"*70)
        
        for result in results:
            print(
                f"{result['concurrent_requests']:<15} "
                f"{result['total_time']:<12.3f} "
                f"{result['throughput']:<12.2f} "
                f"{result['avg_response_time']*1000:<15.2f}"
            )
        
        return results


async def test_async_endpoint_performance():
    """Test async endpoint performance"""
    tester = LoadTester()
    
    print("\n" + "#"*70)
    print("# FASTAPI ASYNC ENDPOINT LOAD TESTING")
    print("#"*70)
    
    print("\nNote: Make sure FastAPI app is running on http://localhost:8000")
    print("Run: python -m uvicorn app.main:app --reload")
    
    # Test basic endpoint
    print("\n" + "="*70)
    print("Testing simple async endpoint: /health")
    print("="*70)
    await tester.test_endpoint("/health", 5)
    
    # Test endpoints with increasing load
    print("\n" + "="*70)
    print("Testing with increasing concurrent loads")
    print("="*70)
    loads = [5, 10, 20, 50]
    
    try:
        await tester.run_multiple_tests("/documents/1", loads)
    except Exception as e:
        print(f"\nError: Could not reach server at http://localhost:8000")
        print(f"Details: {e}")
        print("\nTo test, run the FastAPI app first:")
        print("  cd app")
        print("  python -m uvicorn main:app --reload")


async def main():
    """Main entry point"""
    await test_async_endpoint_performance()


if __name__ == "__main__":
    asyncio.run(main())
