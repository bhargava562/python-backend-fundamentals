"""
Day 22: Advanced Backend System Designs
========================================

This module implements critical backend patterns used in production systems:
1. LRU Cache - Memory-efficient caching strategy
2. Sliding Window Rate Limiter - API request throttling

These patterns combine multiple data structures to solve real-world problems.
"""

from collections import OrderedDict, deque
import time
from typing import Any, Optional, Dict


# ==================== PATTERN 1: LRU CACHE ====================

class LRUCache:
    """
    Least Recently Used Cache using OrderedDict and Hash Map.
    
    This combines:
    - Hash Map: O(1) lookup
    - Doubly Linked List: O(1) removal/insertion (via OrderedDict)
    
    Problem it solves:
    - Limited memory capacity
    - Need to keep most-used data accessible
    - Automatic eviction of unused data
    
    Use Case: Database query caching, API response caching, session storage
    
    Example (Backend):
    ```
    user_cache = LRUCache(capacity=100)
    user_cache.put("user_123", {"name": "Alice", "role": "admin"})
    user = user_cache.get("user_123")  # Returns data and marks as recent
    ```
    
    Time Complexity:
    - get: O(1)
    - put: O(1)
    Space Complexity: O(capacity)
    """
    
    def __init__(self, capacity: int):
        """Initialize cache with given capacity."""
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.cache: OrderedDict[str, Any] = OrderedDict()
        self.capacity = capacity
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Any:
        """
        Retrieve value and mark as recently used.
        Returns -1 if key not found.
        """
        if key not in self.cache:
            self.misses += 1
            return -1
        
        # Move to end (mark as recently used)
        self.cache.move_to_end(key)
        self.hits += 1
        return self.cache[key]
    
    def put(self, key: str, value: Any) -> None:
        """Store key-value pair, evict oldest if at capacity."""
        if key in self.cache:
            # Update existing key and move to end
            self.cache.move_to_end(key)
        
        self.cache[key] = value
        
        # Evict least recently used (first) item if over capacity
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
    
    def delete(self, key: str) -> bool:
        """Manually delete an entry."""
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all entries."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def size(self) -> int:
        """Get current number of items in cache."""
        return len(self.cache)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total_requests": total,
            "hit_rate": f"{hit_rate:.2f}%",
            "current_size": len(self.cache),
            "capacity": self.capacity
        }
    
    def display_cache(self) -> list:
        """Return current cache contents in order (most recent last)."""
        return list(self.cache.keys())


# ==================== PATTERN 2: SLIDING WINDOW RATE LIMITER ====================

class SlidingWindowRateLimiter:
    """
    Rate limiter using sliding time window with deque.
    
    Problem it solves:
    - Prevent API abuse by limiting requests per time period
    - Distribute load evenly across time windows
    - Fairer than fixed window (avoids burst at window boundaries)
    
    How it works:
    1. Track all request timestamps for each user in a deque
    2. Remove timestamps outside current time window
    3. Allow request if count < max_requests
    4. Add new timestamp if allowed
    
    Use Case: API rate limiting, DDoS protection, fair resource allocation
    
    Example (Backend):
    ```
    limiter = SlidingWindowRateLimiter(max_requests=5, window_size_seconds=60)
    if limiter.allow_request("user_123"):
        process_request()
    else:
        raise HTTPException(status_code=429, detail="Too many requests")
    ```
    
    Time Complexity:
    - allow_request: O(n) worst case (n = requests in window, typically small)
    - average: O(1) amortized
    Space Complexity: O(n) where n = total requests tracked
    """
    
    def __init__(self, max_requests: int, window_size_seconds: int):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed in time window
            window_size_seconds: Size of sliding window in seconds
        """
        if max_requests <= 0 or window_size_seconds <= 0:
            raise ValueError("max_requests and window_size must be positive")
        
        self.max_requests = max_requests
        self.window_size = window_size_seconds
        self.user_requests: Dict[str, deque] = {}
    
    def allow_request(self, user_id: str) -> bool:
        """
        Check if user is allowed to make a request.
        Returns True if allowed, False if rate limited.
        """
        now = time.time()
        
        # Initialize user if not seen before
        if user_id not in self.user_requests:
            self.user_requests[user_id] = deque()
        
        requests = self.user_requests[user_id]
        
        # Remove timestamps outside the current window
        # Window = [now - window_size, now]
        while requests and now - requests[0] > self.window_size:
            requests.popleft()
        
        # Check if request is allowed
        if len(requests) < self.max_requests:
            requests.append(now)
            return True
        
        return False
    
    def get_user_requests_count(self, user_id: str) -> int:
        """Get number of requests for user in current window."""
        if user_id not in self.user_requests:
            return 0
        
        now = time.time()
        requests = self.user_requests[user_id]
        
        # Count requests within window
        count = 0
        for timestamp in requests:
            if now - timestamp <= self.window_size:
                count += 1
        
        return count
    
    def get_reset_time(self, user_id: str) -> Optional[float]:
        """
        Get time (in seconds) until user can make another request.
        Returns None if user has requests available.
        """
        if user_id not in self.user_requests:
            return None
        
        requests = self.user_requests[user_id]
        if len(requests) < self.max_requests:
            return None
        
        # Oldest request in window
        oldest_request = requests[0]
        now = time.time()
        reset_time = (oldest_request + self.window_size) - now
        
        return max(0, reset_time)
    
    def reset_user(self, user_id: str) -> None:
        """Reset rate limit for specific user."""
        if user_id in self.user_requests:
            self.user_requests[user_id].clear()
    
    def reset_all(self) -> None:
        """Reset rate limits for all users."""
        self.user_requests.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiter statistics."""
        return {
            "max_requests": self.max_requests,
            "window_size_seconds": self.window_size,
            "tracked_users": len(self.user_requests),
            "total_requests_tracked": sum(len(reqs) for reqs in self.user_requests.values())
        }


# ==================== ADVANCED PATTERN: DISTRIBUTED CACHE ====================

class DistributedCacheLayer:
    """
    Combines multiple caching strategies for backend systems.
    
    Strategy:
    1. L1 Cache: Fast in-memory LRU cache for hot data
    2. L2 Cache: Larger capacity for warm data
    3. Fallback: Database query (not implemented here)
    
    Use Case: Production systems where single cache insufficient
    """
    
    def __init__(self, l1_capacity: int = 100, l2_capacity: int = 1000):
        self.l1_cache = LRUCache(capacity=l1_capacity)
        self.l2_cache = LRUCache(capacity=l2_capacity)
    
    def get(self, key: str) -> Any:
        """Retrieve from L1 first, then L2, then -1 if not found."""
        # Check L1
        result = self.l1_cache.get(key)
        if result != -1:
            return result
        
        # Check L2
        result = self.l2_cache.get(key)
        if result != -1:
            # Promote to L1
            self.l1_cache.put(key, result)
            return result
        
        return -1
    
    def put(self, key: str, value: Any, tier: str = "L1") -> None:
        """Store in specified tier."""
        if tier == "L1":
            self.l1_cache.put(key, value)
        elif tier == "L2":
            self.l2_cache.put(key, value)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics from both cache layers."""
        return {
            "L1": self.l1_cache.get_stats(),
            "L2": self.l2_cache.get_stats()
        }


if __name__ == "__main__":
    # ===== LRU Cache Demo =====
    print("=== LRU Cache Demo ===")
    cache = LRUCache(capacity=3)
    
    cache.put("user_1", {"name": "Alice"})
    cache.put("user_2", {"name": "Bob"})
    cache.put("user_3", {"name": "Charlie"})
    print(f"Cache after 3 puts: {cache.display_cache()}")
    
    # Access user_1 (makes it recently used)
    cache.get("user_1")
    print(f"After accessing user_1: {cache.display_cache()}")
    
    # Add user_4 (should evict user_2, the least recently used)
    cache.put("user_4", {"name": "David"})
    print(f"After adding user_4: {cache.display_cache()}")
    print(f"Stats: {cache.get_stats()}")
    print()
    
    # ===== Rate Limiter Demo =====
    print("=== Rate Limiter Demo ===")
    limiter = SlidingWindowRateLimiter(max_requests=3, window_size_seconds=10)
    
    user_id = "user_123"
    for i in range(5):
        allowed = limiter.allow_request(user_id)
        print(f"Request {i+1}: {'ALLOWED' if allowed else 'BLOCKED'}")
    
    remaining_requests = limiter.max_requests - limiter.get_user_requests_count(user_id)
    print(f"Remaining requests: {remaining_requests}")
    print(f"Reset time: {limiter.get_reset_time(user_id):.2f}s")
    print(f"Stats: {limiter.get_stats()}")
    print()
    
    # ===== Distributed Cache Demo =====
    print("=== Distributed Cache Layer Demo ===")
    dist_cache = DistributedCacheLayer(l1_capacity=2, l2_capacity=5)
    
    for i in range(4):
        dist_cache.put(f"key_{i}", f"value_{i}")
    
    # Retrieve (demonstrates promotion from L2 to L1)
    print(f"Retrieved key_0: {dist_cache.get('key_0')}")
    print(f"Stats: {dist_cache.get_stats()}")
