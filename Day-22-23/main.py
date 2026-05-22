"""
Day 22: FastAPI Integration with Data Structures
==================================================

This module demonstrates how data structures are used in a real FastAPI application.
It shows practical backend scenarios and how to choose the right data structure.
"""

from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import uvicorn
import random

# Import our custom data structures and systems
from data_structures import (
    RequestStack,
    BackgroundTaskQueue,
    UserCache,
    PermissionManager,
    CategoryNode,
    SocialGraph
)
from backend_systems import LRUCache, SlidingWindowRateLimiter, DistributedCacheLayer

# Import algorithms and optimization modules
from algorithms import (
    binary_search_products,
    merge_sort_orders,
    bubble_sort_orders,
    max_revenue_sliding_window,
    find_user_pair_with_target_score
)
from backend_optimization import flatten_categories_iterative

# ==================== PYDANTIC MODELS ====================

class UserRegistration(BaseModel):
    """User registration request schema."""
    user_id: str = Field(..., min_length=1)
    email: EmailStr
    name: str = Field(..., min_length=1)
    role: str = "user"


class UserProfile(BaseModel):
    """User profile response schema."""
    user_id: str
    email: str
    name: str
    role: str
    created_at: str


class TaskRequest(BaseModel):
    """Background task request."""
    task_id: str
    task_type: str
    user_id: str
    data: Dict = {}


class FriendshipRequest(BaseModel):
    """Create friendship between two users."""
    user1: str
    user2: str


class CategoryRequest(BaseModel):
    """Create category."""
    name: str
    parent_id: Optional[int] = None


# ==================== FASTAPI APPLICATION ====================

app = FastAPI(
    title="Data Structures Backend Demo",
    description="FastAPI application demonstrating practical use of data structures",
    version="1.0.0"
)

# ==================== IN-MEMORY DATA STORES ====================
# These would be replaced with databases in production

# Using SET for O(1) uniqueness checks
email_registry: set = set()

# Using DICT for O(1) lookups
user_db: Dict[str, Dict] = {}

# Using QUEUE for task processing
background_tasks = BackgroundTaskQueue()

# Using LRU CACHE for hot user data
user_cache = LRUCache(capacity=50)

# Using DISTRIBUTED CACHE for multi-tier caching
distributed_cache = DistributedCacheLayer(l1_capacity=10, l2_capacity=100)

# Using RATE LIMITER for API protection
api_limiter = SlidingWindowRateLimiter(max_requests=10, window_size_seconds=60)

# Using STACK for undo/redo functionality
user_action_stack: Dict[str, RequestStack] = {}

# Using GRAPH for social connections
social_network = SocialGraph()

# Using TREE for category hierarchy
category_root: Optional[CategoryNode] = None
categories_map: Dict[int, CategoryNode] = {}

# Permission manager for RBAC
permission_manager = PermissionManager()

# --- Algorithm-Specific Data Structures ---
# Pre-sorted inventory for binary search (O(log n) operations)
INVENTORY_DB: List[Dict[str, any]] = sorted(
    [{"sku": f"SKU-{str(i).zfill(5)}", "name": f"Product Item {i}", "price": round(random.uniform(10.0, 500.0), 2)} 
     for i in range(1000)],
    key=lambda x: x["sku"]
)

# Sample historical revenue for sliding window analytics
HISTORICAL_REVENUE_STREAM: List[float] = [random.uniform(500.0, 15000.0) for _ in range(365)]


# ==================== INITIALIZATION ====================

@app.on_event("startup")
async def startup():
    """Initialize data structures on startup."""
    global category_root
    
    print("Initializing application data structures...")
    
    # Setup permissions
    permission_manager.assign_role_permissions("admin", [
        "read_users", "write_users", "delete_users",
        "manage_permissions", "view_analytics"
    ])
    permission_manager.assign_role_permissions("user", [
        "read_users", "read_own_profile", "update_own_profile"
    ])
    permission_manager.assign_role_permissions("guest", [
        "read_public_posts"
    ])
    
    # Setup category hierarchy
    category_root = CategoryNode("All Products", 0)
    categories_map[0] = category_root
    
    electronics = CategoryNode("Electronics", 1)
    clothing = CategoryNode("Clothing", 2)
    category_root.add_child(electronics)
    category_root.add_child(clothing)
    categories_map[1] = electronics
    categories_map[2] = clothing
    
    computers = CategoryNode("Computers", 3)
    phones = CategoryNode("Phones", 4)
    electronics.add_child(computers)
    electronics.add_child(phones)
    categories_map[3] = computers
    categories_map[4] = phones
    
    print("✓ Data structures initialized successfully")


# ==================== REGISTRATION ENDPOINTS ====================

@app.post("/register", response_model=Dict, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegistration):
    """
    Register a new user.
    
    Data Structures Used:
    - SET: Check email uniqueness in O(1)
    - DICT: Store user data with O(1) lookup
    - QUEUE: Queue welcome email task
    - GRAPH: Add user to social network
    
    Time Complexity: O(1) average
    """
    # Rate limiting check
    if not api_limiter.allow_request(user.user_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many registration attempts. Please try again later."
        )
    
    # SET: O(1) uniqueness check
    if user.email in email_registry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # DICT: O(1) storage
    user_data = {
        "user_id": user.user_id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "created_at": datetime.now().isoformat()
    }
    user_db[user.user_id] = user_data
    email_registry.add(user.email)
    
    # GRAPH: Add user to social network
    social_network.add_user(user.user_id)
    
    # STACK: Initialize action history for user
    user_action_stack[user.user_id] = RequestStack()
    user_action_stack[user.user_id].push(f"User created")
    
    # QUEUE: Queue welcome email task
    background_tasks.enqueue_task(f"send_email_welcome_{user.user_id}")
    
    return {
        "message": "User registered successfully",
        "user_id": user.user_id,
        "created_at": user_data["created_at"]
    }


# ==================== USER PROFILE ENDPOINTS ====================

@app.get("/user/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: str):
    """
    Get user profile with multi-tier caching.
    
    Data Structures Used:
    - LRU CACHE (L1): Hot data storage
    - LRU CACHE (L2): Warm data storage
    - DICT: Fallback to database
    - RATE LIMITER: Prevent abuse
    
    Time Complexity: O(1) cache hit, O(1) database lookup
    """
    # Rate limiting check
    if not api_limiter.allow_request(user_id):
        reset_time = api_limiter.get_reset_time(user_id)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limited. Reset in {reset_time:.1f}s"
        )
    
    # Try distributed cache first
    cached_profile = distributed_cache.get(user_id)
    if cached_profile != -1:
        return {**cached_profile, "source": "cache"}
    
    # Fallback to database (DICT)
    if user_id not in user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    profile = user_db[user_id]
    
    # Store in cache
    distributed_cache.put(user_id, profile, tier="L1")
    
    return profile


@app.get("/users/search", response_model=List[UserProfile])
async def search_users(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """
    Search users with pagination.
    
    Data Structures Used:
    - DICT: Iterate over stored users
    
    Time Complexity: O(n) where n = total users
    """
    users = list(user_db.values())[skip:skip + limit]
    return users


@app.put("/user/{user_id}")
async def update_user_profile(user_id: str, updates: Dict):
    """
    Update user profile.
    
    Data Structures Used:
    - DICT: Update user record
    - STACK: Track action
    - CACHE: Invalidate cache entry
    """
    if user_id not in user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update DICT
    user_db[user_id].update(updates)
    
    # Track action in STACK
    if user_id in user_action_stack:
        user_action_stack[user_id].push(f"Profile updated at {datetime.now().isoformat()}")
    
    # Invalidate cache
    distributed_cache.l1_cache.delete(user_id)
    distributed_cache.l2_cache.delete(user_id)
    
    return {"message": "Profile updated successfully", "user_id": user_id}


# ==================== SOCIAL NETWORK ENDPOINTS ====================

@app.post("/friendship")
async def create_friendship(request: FriendshipRequest):
    """
    Create a friendship between two users.
    
    Data Structures Used:
    - GRAPH: Add bidirectional edge
    
    Time Complexity: O(1)
    """
    if request.user1 not in user_db or request.user2 not in user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or both users not found"
        )
    
    # GRAPH: Add friendship (O(1))
    social_network.add_friendship(request.user1, request.user2)
    
    return {
        "message": "Friendship created",
        "user1": request.user1,
        "user2": request.user2
    }


@app.get("/user/{user_id}/friends", response_model=List[str])
async def get_friends(user_id: str):
    """
    Get friends of a user.
    
    Data Structures Used:
    - GRAPH: O(1) adjacency list lookup
    
    Time Complexity: O(f) where f = number of friends
    """
    if user_id not in user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # GRAPH: Get friends (O(1))
    friends = social_network.get_friends(user_id)
    return friends


@app.get("/user/{user1}/mutual-friends/{user2}")
async def get_mutual_friends(user1: str, user2: str):
    """
    Find mutual friends between two users.
    
    Data Structures Used:
    - GRAPH: Get friends lists
    - SET: Find intersection
    
    Time Complexity: O(f1 + f2) where f1, f2 = friend counts
    """
    if user1 not in user_db or user2 not in user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or both users not found"
        )
    
    # GRAPH + SET: Find mutual friends
    mutual = social_network.get_mutual_friends(user1, user2)
    return {"mutual_friends": mutual, "count": len(mutual)}


@app.get("/user/{user1}/path-to/{user2}")
async def find_connection_path(user1: str, user2: str):
    """
    Find shortest connection path between two users (BFS).
    
    Data Structures Used:
    - GRAPH: Network traversal
    - QUEUE: BFS traversal (implicit in find_path_bfs)
    
    Time Complexity: O(V + E) where V = users, E = friendships
    """
    if user1 not in user_db or user2 not in user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or both users not found"
        )
    
    path = social_network.find_path_bfs(user1, user2)
    
    if path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No connection path found between {user1} and {user2}"
        )
    
    return {"path": path, "distance": len(path) - 1}


# ==================== TASK QUEUE ENDPOINTS ====================

@app.post("/tasks")
async def submit_task(task: TaskRequest):
    """
    Submit a background task.
    
    Data Structures Used:
    - QUEUE: FIFO task processing
    
    Time Complexity: O(1)
    """
    if task.user_id not in user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # QUEUE: Enqueue task (O(1))
    background_tasks.enqueue_task(task.task_id)
    
    return {
        "message": "Task submitted",
        "task_id": task.task_id,
        "queue_position": background_tasks.queue_size()
    }


@app.get("/tasks/next")
async def get_next_task():
    """
    Get next task from queue (for worker process).
    
    Data Structures Used:
    - QUEUE: FIFO retrieval
    
    Time Complexity: O(1)
    """
    next_task = background_tasks.dequeue_task()
    
    if next_task == "No tasks pending":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tasks in queue"
        )
    
    return {"task_id": next_task}


@app.get("/tasks/queue-status")
async def get_queue_status():
    """Get current queue status."""
    return {
        "pending_tasks": background_tasks.queue_size(),
        "is_empty": background_tasks.is_empty()
    }


# ==================== CATEGORY ENDPOINTS ====================

@app.get("/categories")
async def get_category_hierarchy():
    """
    Get all categories in hierarchy.
    
    Data Structures Used:
    - TREE: Traverse hierarchy
    
    Time Complexity: O(n) where n = total categories
    """
    if category_root is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Category hierarchy not initialized"
        )
    
    # TREE: DFS traversal
    categories = category_root.traverse_dfs()
    
    return {
        "categories": categories,
        "count": len(categories),
        "traversal_method": "depth-first"
    }


@app.get("/categories/bfs")
async def get_categories_bfs():
    """
    Get categories in breadth-first order.
    
    Data Structures Used:
    - TREE: BFS traversal using implicit QUEUE
    
    Time Complexity: O(n)
    """
    if category_root is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Category hierarchy not initialized"
        )
    
    # TREE: BFS traversal
    categories = category_root.traverse_bfs()
    
    return {
        "categories": categories,
        "count": len(categories),
        "traversal_method": "breadth-first"
    }


# ==================== CACHE STATISTICS ENDPOINTS ====================

@app.get("/stats/cache")
async def get_cache_stats():
    """Get cache performance statistics."""
    return {
        "distributed_cache": distributed_cache.get_stats(),
        "user_cache_direct": user_cache.get_stats()
    }


@app.get("/stats/rate-limiter")
async def get_rate_limiter_stats():
    """Get rate limiter statistics."""
    return api_limiter.get_stats()


@app.get("/stats/background-tasks")
async def get_task_queue_stats():
    """Get background task queue statistics."""
    return {
        "pending_tasks": background_tasks.queue_size(),
        "is_empty": background_tasks.is_empty()
    }


# ==================== ADMIN ENDPOINTS ====================

@app.get("/admin/users")
async def list_all_users():
    """
    List all users (admin only in production).
    
    Data Structures Used:
    - DICT: Iterate all users
    
    Time Complexity: O(n)
    """
    return {
        "total_users": len(user_db),
        "users": list(user_db.keys())
    }


@app.delete("/admin/cache/clear")
async def clear_cache():
    """Clear all caches."""
    distributed_cache.l1_cache.clear()
    distributed_cache.l2_cache.clear()
    user_cache.clear()
    
    return {"message": "All caches cleared"}


@app.post("/admin/rate-limiter/reset")
async def reset_rate_limiter(user_id: Optional[str] = None):
    """Reset rate limiter for user or all users."""
    if user_id:
        api_limiter.reset_user(user_id)
        return {"message": f"Rate limit reset for {user_id}"}
    else:
        api_limiter.reset_all()
        return {"message": "Rate limit reset for all users"}


# ==================== ALGORITHM OPTIMIZATION ENDPOINTS ====================

@app.get("/inventory/search")
async def ordered_sku_lookup(sku: str = Query(..., description="Target stock keeping unit barcode format identifier")):
    """
    Performs an O(log n) Binary Search across the pre-sorted internal array.
    
    Algorithm: Binary Search
    Time Complexity: O(log n)
    Space Complexity: O(1)
    Use Case: High-frequency inventory lookups against cached product database
    """
    product = binary_search_products(INVENTORY_DB, sku)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target tracking asset not found"
        )
    return {
        "execution_strategy": "Binary Search O(log n)",
        "data": product
    }


@app.get("/orders/sorted")
async def sorted_orders_ledger(method: str = Query("merge", description="Sorting algorithm type: 'merge' or 'bubble'")):
    """
    Returns sorted billing distributions via the selected sorting technique.
    
    Demonstrates algorithm trade-offs:
    - merge: Stable, O(n log n) - recommended for production
    - bubble: Educational, O(n²) - disabled for large datasets
    
    Time Complexity: O(n log n) for merge, O(n²) for bubble
    """
    # Generate sample orders
    sample_orders = [
        {"order_id": f"ORD-{i}", "timestamp": random.uniform(1700000000, 1710000000), "amount": round(random.uniform(20, 1000), 2)}
        for i in range(min(500, len(background_tasks.queue)))  # Use reasonable dataset size
    ]
    if not sample_orders:
        sample_orders = [
            {"order_id": f"ORD-{i}", "timestamp": random.uniform(1700000000, 1710000000), "amount": round(random.uniform(20, 1000), 2)}
            for i in range(100)
        ]
    
    if method == "merge":
        sorted_data = merge_sort_orders(sample_orders)
        strategy = "Merge Sort O(n log n)"
    elif method == "bubble":
        # Bounded guard rails to prevent local server locks
        if len(sample_orders) > 1000:
            raise HTTPException(
                status_code=400,
                detail="Payload configuration too large for quadratic processing loops"
            )
        sorted_data = bubble_sort_orders(sample_orders)
        strategy = "Bubble Sort O(n²)"
    else:
        # Default fallback optimization mechanism
        sorted_data = sorted(sample_orders, key=lambda x: x["timestamp"])
        strategy = "Built-in Timsort O(n log n)"
        
    return {
        "strategy": strategy,
        "total_records": len(sorted_data),
        "sample": sorted_data[:5]
    }


@app.get("/categories/flattened")
async def flat_catalog_manifest():
    """
    Processes deep hierarchical object maps into flat structures using iterative stack traversal.
    
    Algorithm: Iterative DFS Traversal
    Time Complexity: O(n) where n is total categories
    Space Complexity: O(n)
    Use Case: Converting nested category hierarchies to flat structures for APIs
    """
    if category_root is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Category hierarchy not initialized"
        )
    
    flattened_manifest = flatten_categories_iterative(category_root.__dict__)
    return {
        "execution_strategy": "Iterative Depth-First Traversal O(n)",
        "catalog": flattened_manifest
    }


@app.get("/analytics/rolling-revenue")
async def analytics_rolling_window(window: int = Query(7, ge=1, le=90)):
    """
    Applies fixed sliding window calculation logic to extract maximum historical sales data.
    
    Algorithm: Sliding Window Pointer Technique
    Time Complexity: O(n)
    Space Complexity: O(1)
    Use Case: Rolling metrics, financial analytics dashboards, streaming throughput
    """
    max_val = max_revenue_sliding_window(HISTORICAL_REVENUE_STREAM, window)
    return {
        "execution_strategy": "Sliding Window Pointer Matrix O(n)",
        "timeframe_days_window": window,
        "max_peak_revenue": round(max_val, 2),
        "dataset_size": len(HISTORICAL_REVENUE_STREAM)
    }


# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_users": len(user_db),
        "pending_tasks": background_tasks.queue_size()
    }


if __name__ == "__main__":
    # Run with: python main.py
    # Or: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
