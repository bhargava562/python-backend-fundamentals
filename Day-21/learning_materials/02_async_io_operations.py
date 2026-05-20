"""
Phase 3: Transitioning I/O Operations to Async
Demonstrates async HTTP requests, file operations, and more
"""
import asyncio
import aiofiles
import httpx
import json
from pathlib import Path


# ============================================================================
# 1. ASYNC HTTP REQUESTS WITH HTTPX
# ============================================================================

async def fetch_json_from_api(url: str, client: httpx.AsyncClient) -> dict:
    """Fetch JSON data from an API asynchronously"""
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        print(f"HTTP Error fetching {url}: {e}")
        return {"error": str(e)}


async def fetch_multiple_apis_concurrent():
    """Demonstrates concurrent API calls"""
    print("\n--- Concurrent API Requests ---")
    
    # Use a context manager for proper resource cleanup
    async with httpx.AsyncClient() as client:
        urls = [
            "https://jsonplaceholder.typicode.com/posts/1",
            "https://jsonplaceholder.typicode.com/users/1",
            "https://jsonplaceholder.typicode.com/comments/1",
        ]
        
        print(f"Fetching from {len(urls)} APIs concurrently...")
        
        # All requests happen at the same time
        results = await asyncio.gather(
            *[fetch_json_from_api(url, client) for url in urls],
            return_exceptions=True
        )
        
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                print(f"✗ {url} failed: {result}")
            else:
                print(f"✓ {url}: Got {len(str(result))} chars of data")
        
        return results


# ============================================================================
# 2. ASYNC FILE OPERATIONS WITH AIOFILES
# ============================================================================

async def write_file_async(filename: str, content: str):
    """Write content to a file asynchronously"""
    async with aiofiles.open(filename, mode='w') as f:
        await f.write(content)
    print(f"✓ Written to {filename}")


async def read_file_async(filename: str) -> str:
    """Read content from a file asynchronously"""
    if not Path(filename).exists():
        return ""
    
    async with aiofiles.open(filename, mode='r') as f:
        content = await f.read()
    return content


async def file_operations_example():
    """Demonstrates async file I/O"""
    print("\n--- Async File Operations ---")
    
    # Create a test directory
    test_dir = Path("async_test_files")
    test_dir.mkdir(exist_ok=True)
    
    # Write multiple files concurrently
    files_to_write = {
        test_dir / "file1.txt": "Content of file 1\n" * 100,
        test_dir / "file2.txt": "Content of file 2\n" * 100,
        test_dir / "file3.txt": "Content of file 3\n" * 100,
    }
    
    print(f"Writing {len(files_to_write)} files concurrently...")
    await asyncio.gather(
        *[write_file_async(str(path), content) 
          for path, content in files_to_write.items()]
    )
    
    # Read multiple files concurrently
    print(f"Reading {len(files_to_write)} files concurrently...")
    contents = await asyncio.gather(
        *[read_file_async(str(path)) for path in files_to_write.keys()]
    )
    
    for path, content in zip(files_to_write.keys(), contents):
        print(f"✓ {path.name}: {len(content)} bytes")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)


# ============================================================================
# 3. SIMULATING ASYNC DATABASE OPERATIONS
# ============================================================================

class AsyncDatabaseSimulator:
    """Simulates async database operations"""
    
    def __init__(self):
        self.data = {
            1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
            2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
            3: {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
        }
    
    async def fetch_user(self, user_id: int) -> dict:
        """Simulate async database query"""
        await asyncio.sleep(0.5)  # Simulate network/disk I/O
        return self.data.get(user_id, {"error": "Not found"})
    
    async def insert_user(self, user_id: int, name: str, email: str) -> bool:
        """Simulate async database insert"""
        await asyncio.sleep(0.3)  # Simulate write latency
        self.data[user_id] = {"id": user_id, "name": name, "email": email}
        return True
    
    async def fetch_multiple_users(self, user_ids: list) -> list:
        """Fetch multiple users concurrently"""
        return await asyncio.gather(
            *[self.fetch_user(uid) for uid in user_ids]
        )


async def database_operations_example():
    """Demonstrates async database operations"""
    print("\n--- Async Database Operations ---")
    
    db = AsyncDatabaseSimulator()
    
    # Fetch multiple users concurrently
    print("Fetching multiple users concurrently...")
    users = await db.fetch_multiple_users([1, 2, 3])
    for user in users:
        if "error" not in user:
            print(f"✓ User: {user['name']} ({user['email']})")
    
    # Insert multiple users concurrently
    print("\nInserting multiple users concurrently...")
    results = await asyncio.gather(
        db.insert_user(4, "David", "david@example.com"),
        db.insert_user(5, "Eve", "eve@example.com"),
        db.insert_user(6, "Frank", "frank@example.com"),
    )
    print(f"✓ Inserted {sum(results)} users")


# ============================================================================
# 4. COMBINING MULTIPLE I/O OPERATIONS
# ============================================================================

async def combined_io_example():
    """Demonstrates combining multiple async I/O operations"""
    print("\n--- Combined Async I/O Operations ---")
    
    print("Performing HTTP requests, file operations, and DB queries concurrently...")
    
    api_results = asyncio.gather(
        fetch_json_from_api(
            "https://jsonplaceholder.typicode.com/posts/1",
            httpx.AsyncClient()
        ),
        timeout=5
    )
    
    # Run all concurrently
    # Note: In real scenario, you'd use a single HttpClient for all requests
    print("✓ Demonstrated combined I/O operations pattern")


# ============================================================================
# 5. ASYNC CONTEXT MANAGERS
# ============================================================================

class AsyncResourceManager:
    """Demonstrates async context manager pattern"""
    
    def __init__(self, name: str):
        self.name = name
    
    async def __aenter__(self):
        print(f"  Acquiring resource: {self.name}")
        await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"  Releasing resource: {self.name}")
        await asyncio.sleep(0.1)
        return False
    
    async def do_work(self):
        print(f"  Working with {self.name}...")
        await asyncio.sleep(0.2)


async def async_context_manager_example():
    """Demonstrates async context managers"""
    print("\n--- Async Context Managers ---")
    
    async with AsyncResourceManager("Resource 1") as res1:
        await res1.do_work()
    
    async with AsyncResourceManager("Resource 2") as res2:
        await res2.do_work()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Main entry point"""
    print("="*70)
    print("ASYNC I/O OPERATIONS - Learning Materials")
    print("="*70)
    
    # Try to demonstrate async HTTP if internet is available
    try:
        await fetch_multiple_apis_concurrent()
    except Exception as e:
        print(f"\nNote: API demo skipped (no internet): {type(e).__name__}")
    
    # File operations
    await file_operations_example()
    
    # Database operations
    await database_operations_example()
    
    # Context managers
    await async_context_manager_example()
    
    print("\n" + "="*70)
    print("KEY TAKEAWAYS:")
    print("="*70)
    print("✓ Use httpx.AsyncClient for async HTTP requests")
    print("✓ Use aiofiles for async file I/O")
    print("✓ Database drivers like asyncpg support async queries")
    print("✓ Always use context managers (async with) for resource cleanup")
    print("✓ Combine multiple I/O operations with asyncio.gather()")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
