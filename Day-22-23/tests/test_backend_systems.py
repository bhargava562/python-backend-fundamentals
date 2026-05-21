"""
Unit tests for backend_systems.py
"""

import pytest
import time
from backend_systems import LRUCache, SlidingWindowRateLimiter, DistributedCacheLayer


class TestLRUCache:
    """Test LRU Cache implementation."""
    
    def test_put_and_get(self):
        cache = LRUCache(capacity=2)
        cache.put("key1", "value1")
        assert cache.get("key1") == "value1"
    
    def test_eviction_on_capacity(self):
        cache = LRUCache(capacity=2)
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")  # Should evict key1
        
        assert cache.get("key1") == -1
        assert cache.get("key3") == "value3"
    
    def test_lru_eviction(self):
        cache = LRUCache(capacity=2)
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.get("key1")  # Make key1 recently used
        cache.put("key3", "value3")  # Should evict key2
        
        assert cache.get("key2") == -1
        assert cache.get("key1") == "value1"
    
    def test_cache_miss(self):
        cache = LRUCache(capacity=2)
        assert cache.get("nonexistent") == -1
    
    def test_cache_size(self):
        cache = LRUCache(capacity=3)
        cache.put("a", 1)
        cache.put("b", 2)
        assert cache.size() == 2
    
    def test_delete(self):
        cache = LRUCache(capacity=2)
        cache.put("key1", "value1")
        assert cache.delete("key1") == True
        assert cache.get("key1") == -1
    
    def test_delete_nonexistent(self):
        cache = LRUCache(capacity=2)
        assert cache.delete("nonexistent") == False
    
    def test_cache_clear(self):
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.clear()
        assert cache.size() == 0
    
    def test_cache_stats(self):
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.get("a")  # Hit
        cache.get("b")  # Miss
        stats = cache.get_stats()
        
        assert stats["hits"] == 1
        assert stats["misses"] == 1
    
    def test_display_cache_order(self):
        cache = LRUCache(capacity=3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        
        display = cache.display_cache()
        assert display == ["a", "b", "c"]
    
    def test_capacity_validation(self):
        with pytest.raises(ValueError):
            LRUCache(capacity=0)
        
        with pytest.raises(ValueError):
            LRUCache(capacity=-1)


class TestRateLimiter:
    """Test Sliding Window Rate Limiter."""
    
    def test_allow_request_within_limit(self):
        limiter = SlidingWindowRateLimiter(max_requests=3, window_size_seconds=10)
        assert limiter.allow_request("user1") == True
        assert limiter.allow_request("user1") == True
        assert limiter.allow_request("user1") == True
    
    def test_block_request_over_limit(self):
        limiter = SlidingWindowRateLimiter(max_requests=2, window_size_seconds=10)
        limiter.allow_request("user1")
        limiter.allow_request("user1")
        assert limiter.allow_request("user1") == False
    
    def test_different_users_independent(self):
        limiter = SlidingWindowRateLimiter(max_requests=1, window_size_seconds=10)
        assert limiter.allow_request("user1") == True
        assert limiter.allow_request("user2") == True
        assert limiter.allow_request("user1") == False
    
    def test_request_count(self):
        limiter = SlidingWindowRateLimiter(max_requests=5, window_size_seconds=10)
        limiter.allow_request("user1")
        limiter.allow_request("user1")
        assert limiter.get_user_requests_count("user1") == 2
    
    def test_reset_user(self):
        limiter = SlidingWindowRateLimiter(max_requests=2, window_size_seconds=10)
        limiter.allow_request("user1")
        limiter.allow_request("user1")
        limiter.reset_user("user1")
        assert limiter.get_user_requests_count("user1") == 0
    
    def test_reset_all_users(self):
        limiter = SlidingWindowRateLimiter(max_requests=2, window_size_seconds=10)
        limiter.allow_request("user1")
        limiter.allow_request("user2")
        limiter.reset_all()
        assert limiter.get_user_requests_count("user1") == 0
        assert limiter.get_user_requests_count("user2") == 0
    
    def test_get_reset_time_available(self):
        limiter = SlidingWindowRateLimiter(max_requests=2, window_size_seconds=10)
        limiter.allow_request("user1")
        reset_time = limiter.get_reset_time("user1")
        assert reset_time is None
    
    def test_get_reset_time_limited(self):
        limiter = SlidingWindowRateLimiter(max_requests=1, window_size_seconds=10)
        limiter.allow_request("user1")
        reset_time = limiter.get_reset_time("user1")
        assert reset_time is not None
        assert reset_time > 0
    
    def test_window_expiry(self):
        limiter = SlidingWindowRateLimiter(max_requests=1, window_size_seconds=1)
        limiter.allow_request("user1")
        assert limiter.allow_request("user1") == False
        
        # Wait for window to expire
        time.sleep(1.1)
        assert limiter.allow_request("user1") == True
    
    def test_rate_limiter_stats(self):
        limiter = SlidingWindowRateLimiter(max_requests=5, window_size_seconds=60)
        limiter.allow_request("user1")
        limiter.allow_request("user2")
        stats = limiter.get_stats()
        
        assert stats["max_requests"] == 5
        assert stats["window_size_seconds"] == 60
        assert stats["tracked_users"] == 2
    
    def test_capacity_validation(self):
        with pytest.raises(ValueError):
            SlidingWindowRateLimiter(max_requests=0, window_size_seconds=10)
        
        with pytest.raises(ValueError):
            SlidingWindowRateLimiter(max_requests=5, window_size_seconds=0)


class TestDistributedCache:
    """Test multi-tier cache layer."""
    
    def test_l1_cache_hit(self):
        cache = DistributedCacheLayer(l1_capacity=2, l2_capacity=5)
        cache.put("key1", "value1", tier="L1")
        assert cache.get("key1") == "value1"
    
    def test_l2_cache_hit(self):
        cache = DistributedCacheLayer(l1_capacity=2, l2_capacity=5)
        cache.put("key1", "value1", tier="L2")
        assert cache.get("key1") == "value1"
    
    def test_promotion_l2_to_l1(self):
        cache = DistributedCacheLayer(l1_capacity=2, l2_capacity=5)
        cache.put("key1", "value1", tier="L2")
        
        # First get from L2
        result = cache.get("key1")
        assert result == "value1"
        
        # Check it's now in L1
        l1_display = cache.l1_cache.display_cache()
        assert "key1" in l1_display
    
    def test_cache_miss(self):
        cache = DistributedCacheLayer(l1_capacity=2, l2_capacity=5)
        assert cache.get("nonexistent") == -1
    
    def test_stats(self):
        cache = DistributedCacheLayer(l1_capacity=2, l2_capacity=5)
        cache.put("a", 1, tier="L1")
        cache.put("b", 2, tier="L2")
        
        stats = cache.get_stats()
        assert "L1" in stats
        assert "L2" in stats
        assert stats["L1"]["current_size"] == 1
        assert stats["L2"]["current_size"] == 1


# Integration Tests

class TestIntegration:
    """Integration tests combining multiple components."""
    
    def test_cache_with_rate_limiting(self):
        """Test using cache to store rate limit info."""
        cache = LRUCache(capacity=100)
        limiter = SlidingWindowRateLimiter(max_requests=5, window_size_seconds=60)
        
        # Store user info in cache
        cache.put("user1", {"requests": 3})
        
        # Check rate limit
        allowed = limiter.allow_request("user1")
        assert allowed == True
    
    def test_realistic_scenario(self):
        """Simulate real backend scenario."""
        # User cache
        user_cache = LRUCache(capacity=50)
        
        # API rate limiter
        api_limiter = SlidingWindowRateLimiter(max_requests=100, window_size_seconds=60)
        
        # Simulate user operations
        user_data = {"id": "user1", "name": "Alice", "role": "admin"}
        user_cache.put("user1", user_data)
        
        for _ in range(5):
            if api_limiter.allow_request("user1"):
                result = user_cache.get("user1")
                assert result == user_data
        
        # Check stats
        cache_stats = user_cache.get_stats()
        assert cache_stats["hits"] == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
