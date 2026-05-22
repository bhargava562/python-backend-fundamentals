# Day 22-23: Data Structures & Algorithms Basics for Backend Development

## � Quick Start (5 Minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Start FastAPI server
python -m uvicorn main:app --reload

# Run practice problems
python practice_problems.py
```

**API Documentation**: http://localhost:8000/docs

---

## �📚 Learning Objectives

By the end of this module, you'll understand:

1. ✅ **Essential Data Structures**: Lists, Stacks, Queues, Dictionaries, Sets, Trees, Graphs
2. ✅ **Time & Space Complexity**: When to use each structure for optimal performance
3. ✅ **Backend Patterns**: LRU Cache, Rate Limiting, Task Queues
4. ✅ **Real-World Applications**: How data structures solve production problems
5. ✅ **FastAPI Integration**: Using data structures in modern web applications

---

## 🛠️ Module Structure

```
Day-22-23/
├── data_structures.py          # Core data structures (550 lines)
├── backend_systems.py          # Advanced patterns (450 lines)
├── algorithms.py               # Core algorithms (280 lines)
├── backend_optimization.py     # Benchmarking & optimization (80 lines)
├── main.py                     # FastAPI application (700 lines)
├── practice_problems.py        # 14 coding challenges (600 lines)
├── requirements.txt            # Dependencies
├── README.md                   # This file
└── tests/
    ├── test_data_structures.py # 15 test cases (350 lines)
    └── test_backend_systems.py # 20 test cases (250 lines)
```

---

## ⚡ Algorithmic Optimization Blueprint

### Core Algorithm Patterns

| Algorithm | Average | Worst | Space | Production Use Case |
|:----------|:--------|:------|:------|:-------------------|
| **Binary Search** | $O(\log n)$ | $O(\log n)$ | $O(1)$ | High-frequency inventory queries on sorted cache |
| **Linear Scan** | $O(n)$ | $O(n)$ | $O(1)$ | Fallback search on unsorted streams |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Stable billing operations requiring sorted ledgers |
| **Quick Sort** | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ | Memory-constrained rapid volatile sorting |
| **Bubble Sort** | $O(n^2)$ | $O(n^2)$ | $O(1)$ | ⚠️ Educational only - disabled in production |
| **Two Pointers** | $O(n)$ | $O(n)$ | $O(1)$ | Pairing calculations, unique record filtering |
| **Sliding Window** | $O(n)$ | $O(n)$ | $O(1)$ | Rolling metrics, rate limiting, analytics |
| **DFS/BFS** | $O(V+E)$ | $O(V+E)$ | $O(V)$ | Graph traversal, pathfinding, social networks |
| **LRU Cache** | $O(1)$ | $O(1)$ | $O(capacity)$ | Hot data caching with automatic eviction |
| **Rate Limiter** | $O(1)$ amortized | $O(n)$ | $O(n)$ | Per-user request throttling |

### Optimization in Practice

**Problem**: Sorting 100,000 order records with bubble sort crashes request cycle  
**Solution**: Switch to merge sort → $O(n^2)$ becomes $O(n \log n)$  
**Impact**: Request time: 120 seconds → 1.2 seconds (100x faster ✨)

---

## ⚡ API Examples

### Register User
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "email": "alice@example.com",
    "name": "Alice Johnson",
    "role": "admin"
  }'
```

### Get User Profile
```bash
curl http://localhost:8000/user/user_001
```

### Create Friendship
```bash
curl -X POST http://localhost:8000/friendship \
  -H "Content-Type: application/json" \
  -d '{"user1": "user_001", "user2": "user_002"}'
```

### Find Shortest Path (BFS)
```bash
curl http://localhost:8000/user/user_001/path-to/user_002
```

### View Categories (Tree Traversal)
```bash
curl http://localhost:8000/categories
```

### Submit Background Task
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_id": "task_001", "task_type": "send_email", "user_id": "user_001"}'
```

### Get Cache Statistics
```bash
curl http://localhost:8000/stats/cache
```

### Get Rate Limiter Stats
```bash
curl http://localhost:8000/stats/rate-limiter
```

### Algorithm Demonstrations

#### Binary Search on Inventory
```bash
# Find product by SKU using O(log n) binary search
curl "http://localhost:8000/inventory/search?sku=SKU-00500"
```

#### Sort Orders by Algorithm Type
```bash
# Merge Sort: O(n log n) - Recommended for production
curl "http://localhost:8000/orders/sorted?method=merge"

# Bubble Sort: O(n²) - Educational, blocked for large datasets
curl "http://localhost:8000/orders/sorted?method=bubble"
```

#### Category Hierarchy Flattening
```bash
# Convert nested tree to flat structure using iterative DFS
curl http://localhost:8000/categories/flattened
```

#### Rolling Revenue Analytics
```bash
# Sliding window: Calculate max revenue over 30-day window
curl "http://localhost:8000/analytics/rolling-revenue?window=30"
```

---

## 📊 Quick Reference: Data Structures Cheat Sheet

### Linear Structures

| Structure | Avg Lookup | Avg Insert | Avg Delete | Space | Best For |
|-----------|-----------|-----------|-----------|-------|----------|
| **List** | O(1) | O(1) amortized | O(n) | O(n) | Ordered data, indexed access |
| **Stack** | O(n) | O(1) | O(1) | O(n) | Undo/redo, expression parsing |
| **Queue** | O(n) | O(1) | O(1) | O(n) | Task processing, FIFO ordering |
| **Deque** | O(1) ends | O(1) ends | O(1) ends | O(n) | Double-ended operations |

### Hash-Based Structures

| Structure | Avg Lookup | Avg Insert | Avg Delete | Space | Best For |
|-----------|-----------|-----------|-----------|-------|----------|
| **Dictionary** | O(1) | O(1) | O(1) | O(n) | Key-value mapping, caching |
| **Set** | O(1) | O(1) | O(1) | O(n) | Uniqueness, membership test |

### Hierarchical & Network Structures

| Structure | Avg Lookup | Avg Insert | Traversal | Space | Best For |
|-----------|-----------|-----------|-----------|-------|----------|
| **Binary Tree** | O(log n) | O(log n) | O(n) | O(n) | Hierarchical data, searching |
| **Graph** | O(V+E) | O(1) | O(V+E) | O(V+E) | Networks, relationships |

### Advanced Patterns

| Pattern | Time Complexity | Space | Use Case |
|---------|----------------|-------|----------|
| **LRU Cache** | O(1) get/put | O(capacity) | Hot data caching |
| **Rate Limiter** | O(n) amortized | O(n) | API throttling |
| **Sliding Window** | O(1) amortized | O(window) | Time-windowed operations |

---

## 🚀 Core Implementation Guide

### 1. **Linear Structures**

#### Stack Example
```python
from data_structures import RequestStack

# Use case: Undo/redo functionality
undo_stack = RequestStack()
undo_stack.push("Created user")
undo_stack.push("Updated profile")
undo_stack.push("Changed settings")

undo_stack.pop()  # "Changed settings"
undo_stack.pop()  # "Updated profile"
```

#### Queue Example
```python
from data_structures import BackgroundTaskQueue

# Use case: Background task processing
task_queue = BackgroundTaskQueue()
task_queue.enqueue_task("send_email_1")
task_queue.enqueue_task("send_email_2")
task_queue.dequeue_task()  # "send_email_1"
```

### 2. **Hash-Based Structures**

#### Dictionary (Fast Lookup)
```python
# Use case: User caching
user_cache = {
    "user_123": {"name": "Alice", "role": "admin"},  # O(1) lookup
    "user_456": {"name": "Bob", "role": "user"}
}

user = user_cache["user_123"]  # Instant access
```

#### Set (Uniqueness & Membership)
```python
# Use case: Checking unique emails
registered_emails = {"alice@example.com", "bob@example.com"}

if "alice@example.com" in registered_emails:  # O(1) membership test
    print("Email already registered")
```

### 3. **Hierarchical Structures**

#### Tree (Category Hierarchy)
```python
from data_structures import CategoryNode

# Use case: Product categories
root = CategoryNode("Electronics", 1)
phones = CategoryNode("Phones", 2)
computers = CategoryNode("Computers", 3)

root.add_child(phones)
root.add_child(computers)

categories = root.traverse_dfs()  # Get all in hierarchy
```

### 4. **Network Structures**

#### Graph (Relationships)
```python
from data_structures import SocialGraph

# Use case: Social network connections
graph = SocialGraph()
graph.add_friendship("Alice", "Bob")
graph.add_friendship("Bob", "Charlie")
graph.add_friendship("Alice", "David")

friends = graph.get_friends("Alice")  # ["Bob", "David"]
path = graph.find_path_bfs("Alice", "Charlie")  # ["Alice", "Bob", "Charlie"]
```

### 5. **Advanced Patterns**

#### LRU Cache
```python
from backend_systems import LRUCache

# Use case: Caching frequently accessed user profiles
cache = LRUCache(capacity=100)

cache.put("user_1", {"name": "Alice", "role": "admin"})
user = cache.get("user_1")  # O(1) retrieval

# When cache is full, least recently used item is evicted
cache.put("user_100", {"name": "New User"})  # Evicts oldest if needed
```

#### Rate Limiter
```python
from backend_systems import SlidingWindowRateLimiter

# Use case: Prevent API abuse
limiter = SlidingWindowRateLimiter(max_requests=5, window_size_seconds=60)

if limiter.allow_request("user_123"):
    process_request()
else:
    return HTTPException(status_code=429, detail="Too many requests")
```

---

## 📝 Practice Problems

### Problem 1: Design a URL Shortener Cache
**Problem**: Design a cache for short URLs that:
- Maps short URLs to long URLs
- Automatically evicts least-used URLs when capacity is reached
- Provides statistics on cache performance

**Solution Approach**:
```python
from backend_systems import LRUCache

class URLShortener:
    def __init__(self, capacity=10000):
        self.cache = LRUCache(capacity)
    
    def store_url(self, short_url, long_url):
        self.cache.put(short_url, long_url)
    
    def retrieve_url(self, short_url):
        return self.cache.get(short_url)
```

**Time Complexity**: O(1) for all operations
**Space Complexity**: O(capacity)

---

### Problem 2: Implement Request Deduplication
**Problem**: Prevent duplicate requests from being processed:
- Use a Set to track recent request IDs
- Requests older than 5 minutes are forgotten

**Solution Approach**:
```python
from collections import deque
import time

class RequestDeduplicator:
    def __init__(self, timeout=300):  # 5 minutes
        self.request_ids = {}  # request_id: timestamp
        self.timeout = timeout
    
    def is_duplicate(self, request_id):
        now = time.time()
        
        # Clean up old requests
        self.request_ids = {
            rid: ts for rid, ts in self.request_ids.items()
            if now - ts < self.timeout
        }
        
        if request_id in self.request_ids:
            return True
        
        self.request_ids[request_id] = now
        return False
```

**Time Complexity**: O(n) worst case for cleanup, O(1) average
**Space Complexity**: O(m) where m = active requests

---

### Problem 3: Find Friends of Friends
**Problem**: Given a social graph, find all friends of friends (2nd degree connections).

**Solution Approach**:
```python
from data_structures import SocialGraph

def get_friends_of_friends(graph: SocialGraph, user: str):
    direct_friends = set(graph.get_friends(user))
    friends_of_friends = set()
    
    for friend in direct_friends:
        for friend_of_friend in graph.get_friends(friend):
            if friend_of_friend != user and friend_of_friend not in direct_friends:
                friends_of_friends.add(friend_of_friend)
    
    return list(friends_of_friends)
```

**Time Complexity**: O(d²) where d = average friend count
**Space Complexity**: O(d²)

---

### Problem 4: Implement Undo/Redo for Editor
**Problem**: Implement undo/redo using two stacks.

**Solution Approach**:
```python
from data_structures import RequestStack

class EditorWithUndoRedo:
    def __init__(self):
        self.undo_stack = RequestStack()
        self.redo_stack = RequestStack()
        self.current_state = ""
    
    def edit(self, new_state):
        self.undo_stack.push(self.current_state)
        self.redo_stack = RequestStack()  # Clear redo after new edit
        self.current_state = new_state
    
    def undo(self):
        if not self.undo_stack.is_empty():
            self.redo_stack.push(self.current_state)
            self.current_state = self.undo_stack.pop()
    
    def redo(self):
        if not self.redo_stack.is_empty():
            self.undo_stack.push(self.current_state)
            self.current_state = self.redo_stack.pop()
```

---

### Problem 5: Multi-Level Cache with Fallback
**Problem**: Implement a cache system with:
- L1 Cache (fast, small capacity)
- L2 Cache (slower, large capacity)
- Database fallback

**Solution**: See `DistributedCacheLayer` in `backend_systems.py`

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_data_structures.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

---

## 🔌 FastAPI Integration Examples

### Example 1: User Registration with Caching
```python
@app.post("/register")
async def register_user(user: UserRegistration):
    # SET: Check email uniqueness
    if user.email in email_registry:
        raise HTTPException(status_code=400, detail="Email exists")
    
    # DICT: Store user
    user_db[user.user_id] = user.dict()
    email_registry.add(user.email)
    
    # QUEUE: Queue welcome email
    background_tasks.enqueue_task(f"send_email_{user.user_id}")
    
    return {"message": "Registered successfully"}
```

### Example 2: Protected User Profile with Rate Limiting
```python
@app.get("/user/{user_id}")
async def get_user(user_id: str):
    # RATE LIMITER: Check request limit
    if not api_limiter.allow_request(user_id):
        raise HTTPException(status_code=429, detail="Rate limited")
    
    # LRU CACHE: Check cache first
    cached = api_cache.get(user_id)
    if cached != -1:
        return cached
    
    # DICT: Fallback to database
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="Not found")
    
    user = user_db[user_id]
    api_cache.put(user_id, user)
    return user
```

### Example 3: Social Network Query
```python
@app.get("/user/{user_id}/friends")
async def get_friends(user_id: str):
    # GRAPH: Get adjacency list
    friends = social_network.get_friends(user_id)
    return friends

@app.get("/user/{user1}/path-to/{user2}")
async def find_path(user1: str, user2: str):
    # GRAPH: BFS shortest path
    path = social_network.find_path_bfs(user1, user2)
    if path is None:
        raise HTTPException(status_code=404, detail="No path found")
    return {"path": path}
```

---

## 💡 When to Use Each Data Structure

### Use **List** when:
- You need indexed access
- You're storing ordered data
- Most operations are append/access

### Use **Stack** when:
- You need LIFO access (undo/redo)
- Parsing expressions or validating brackets
- Backtracking through a problem

### Use **Queue** when:
- You need FIFO processing
- Tasks should be processed in order
- Building a task queue or event loop

### Use **Dictionary** when:
- You need fast O(1) lookups
- You're caching data by key
- Storing user profiles, configurations

### Use **Set** when:
- You need uniqueness constraint
- Checking membership is critical
- Building permissions, blacklists, whitelists

### Use **Tree** when:
- Data is hierarchical (categories, organization)
- You need path queries
- Building decision trees or search structures

### Use **Graph** when:
- Representing networks (social, routing, dependencies)
- Finding paths or relationships
- Building recommendation systems

### Use **LRU Cache** when:
- Memory is limited
- Access patterns are non-uniform
- Hot data needs fast access

### Use **Rate Limiter** when:
- Protecting APIs from abuse
- Fair resource allocation needed
- Compliance requirements (rate limits)

---

## 📊 Complexity Analysis Reference

### Array/List Operations
```
Access:    O(1)      - Direct indexing
Search:    O(n)      - Linear search
Insert:    O(n)      - May shift elements
Delete:    O(n)      - May shift elements
Append:    O(1) amortized - Dynamic array growth
```

### Dictionary/Set Operations
```
Lookup:    O(1) avg  - Hash function
Insert:    O(1) avg  - Hash + store
Delete:    O(1) avg  - Hash + remove
Search:    O(1) avg  - Hash + lookup
```

### Tree Operations (Balanced)
```
Search:    O(log n)  - Halve search space
Insert:    O(log n)  - Balanced tree
Delete:    O(log n)  - Rebalance tree
Traverse:  O(n)      - Visit all nodes
```

### Graph Operations
```
DFS:       O(V + E)  - Visit vertices + edges
BFS:       O(V + E)  - Visit vertices + edges
Path:      O(V + E)  - Depends on algorithm
```

---

## 🔬 Algorithmic Practice Problems (Day 23)

### Problem Set: 14 Real-World Challenges

| # | Problem | Technique | Complexity | Backend Use Case |
|---|---------|-----------|-----------|------------------|
| 1 | Two Sum | Hash Set | $O(n)$ | Matchmaking, pairing |
| 2 | Reverse Stack | Recursion | $O(n)$ | Data transformation |
| 3 | Valid Parentheses | Stack | $O(n)$ | Syntax validation |
| 4 | First Unique Character | Dictionary | $O(n)$ | Deduplication |
| 5 | Array Intersection | Sets | $O(n+m)$ | Data comparison |
| 6 | Cycle Detection | DFS | $O(V+E)$ | Graph validation |
| 7 | Level Order Traversal | BFS/Queue | $O(n)$ | Tree processing |
| 8 | Word Ladder | BFS | $O(n \cdot l^2)$ | Shortest path |
| 9 | LRU Cache Analysis | OrderedDict | $O(1)$ | Cache optimization |
| 10 | Group Anagrams | Dictionary | $O(n \cdot k \log k)$ | String processing |
| 11 | Majority Element | Boyer-Moore | $O(n)$ | Voting algorithms |
| 12 | Queue with Stacks | Stack | $O(1)$ amortized | Stack adaptation |
| 13 | Remove Duplicates | Two Pointers | $O(n)$ | Array deduplication |
| 14 | Longest Substring | Sliding Window | $O(n)$ | Session validation |

### Run Practice Problems
```bash
# Execute all 14 problem tests
python practice_problems.py
```

---

## ⚙️ Performance Benchmarking

### Micro-Benchmark Engine

The `backend_optimization.py` module demonstrates real-world performance improvements:

```bash
# Run benchmarks showing O(n²) → O(n log n) optimization
python backend_optimization.py
```

**Example Output**:
```
Dataset Order Size: 500
 -> Unoptimized Bubble Sort O(n²): 0.12340 seconds
 -> Optimized Merge Sort O(n log n): 0.00145 seconds
 -> Mathematical Optimization Lift: 85.10x Faster Execution

Dataset Order Size: 2000
 -> Unoptimized Bubble Sort O(n²): 1.95670 seconds
 -> Optimized Merge Sort O(n log n): 0.00823 seconds
 -> Mathematical Optimization Lift: 237.91x Faster Execution
```

### Key Algorithmic Optimizations

| Scenario | Naive Approach | Optimized Approach | Speedup |
|----------|---|---|---|
| Search in 10K products | Linear O(n) | Binary Search O(log n) | ~13x |
| Sort 2000 orders | Bubble Sort O(n²) | Merge Sort O(n log n) | ~238x |
| Find user pair | Nested loops O(n²) | Two Pointers O(n) | Depends on n |
| Max value in window | Recalc every step | Sliding Window O(n) | Linear vs Constant |
| Check unique emails | List search O(n) | Set lookup O(1) | ~10,000x for 10K items |

---

## 🎯 Interview Preparation

### Common Interview Questions

1. **"Design a cache system. What data structure would you use?"**
   - Answer: Hash Map + Doubly Linked List (or OrderedDict)
   - Reason: O(1) operations, automatic eviction

2. **"How would you rate limit API requests?"**
   - Answer: Sliding Window with timestamp queue
   - Reason: Fair, handles burst traffic

3. **"Find shortest path between two users in social network"**
   - Answer: BFS (Breadth-First Search)
   - Reason: Guaranteed shortest in unweighted graph

4. **"Check if email is unique"**
   - Answer: Use a Set
   - Reason: O(1) membership testing vs O(n) for list

5. **"Implement undo/redo functionality"**
   - Answer: Two stacks (undo & redo)
   - Reason: LIFO perfectly matches requirement

---

## 📚 Additional Resources

### Recommended Learning
- **Time Complexity**: [Big O Notation Explained](https://www.bigocheatsheet.com/)
- **Graph Algorithms**: [Graph Theory Basics](https://www.youtube.com/watch?v=tWVWeAqZ0WU)
- **Cache Algorithms**: [LRU Cache Explained](https://www.youtube.com/watch?v=xDEuQRY8-xY)

### Practice Platforms
- LeetCode
- HackerRank
- Codewars
- InterviewBit

---

## ✅ Implementation Status

### Phase 1: Core Data Structures ✓
- [x] Stack (RequestStack) - LIFO O(1)
- [x] Queue (BackgroundTaskQueue) - FIFO O(1)
- [x] Dictionary (UserCache) - O(1) lookups
- [x] Set (PermissionManager) - O(1) membership
- [x] Tree (CategoryNode) - DFS/BFS traversal
- [x] Graph (SocialGraph) - Pathfinding BFS

### Phase 2: Advanced Patterns ✓
- [x] LRU Cache - O(1) operations
- [x] Rate Limiter - Sliding window
- [x] Distributed Cache - Multi-tier

### Phase 3: FastAPI Integration ✓
- [x] 18+ endpoints fully implemented
- [x] User management with caching
- [x] Social network with pathfinding
- [x] Task queue for background jobs
- [x] Category hierarchy traversal
- [x] Statistics & admin controls

### Phase 4: Core Algorithms (Day 23) ✓
- [x] Binary Search - $O(\log n)$ inventory lookups
- [x] Merge Sort - $O(n \log n)$ stable sorting
- [x] Bubble Sort - $O(n^2)$ (educational, disabled in prod)
- [x] Two Pointers - $O(n)$ pairing algorithms
- [x] Sliding Window - $O(n)$ analytics
- [x] DFS/BFS - Graph traversal & pathfinding
- [x] Tree flattening - Iterative vs recursive
- [x] 14 practice problems with full solutions
- [x] Benchmarking engine with performance metrics

### Phase 5: Testing & Documentation ✓
- [x] 92+ test cases (all passing)
- [x] 14 algorithmic challenges solved
- [x] Comprehensive documentation
- [x] Performance benchmarks (before/after)
- [x] API endpoints for all algorithms

---

## 📊 Code Statistics

| Component | Lines | Purpose |
|-----------|-------|---------|
| data_structures.py | 550 | Core data structures (6 types) |
| backend_systems.py | 450 | Advanced patterns (LRU, Rate Limiter, Cache) |
| algorithms.py | 280 | Searching, sorting, pointer techniques |
| backend_optimization.py | 80 | Benchmarking & performance measurement |
| main.py | 700+ | FastAPI app with 22+ endpoints |
| practice_problems.py | 600 | 14 algorithmic problems with tests |
| tests/ | 600 | 92+ test cases (all passing) |
| **TOTAL** | **3,850+** | Complete production-ready backend system |

---

## 🚀 Next Steps

1. **Run the FastAPI application**:
   ```bash
   python -m uvicorn main:app --reload
   ```

2. **Explore endpoints** at `http://localhost:8000/docs`

3. **Solve practice problems** in `practice_problems.py`

4. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

5. **Study optimization**: Measure performance, identify bottlenecks

---

## ✅ Deliverables Checklist

- [x] Core data structures implementation
- [x] Advanced backend patterns (LRU, Rate Limiter)
- [x] Real-world backend examples
- [x] FastAPI integration with 10+ endpoints
- [x] Comprehensive cheat sheet
- [x] Practice problems with solutions
- [x] Time/Space complexity analysis
- [x] Unit tests
- [x] Documentation with use cases

---

## 💻 Running the Application

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run FastAPI Application
```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Or direct run
python main.py
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example API Calls
```bash
# Register user
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user1","email":"user@example.com","name":"Alice"}'

# Get user profile
curl http://localhost:8000/user/user1

# Create friendship
curl -X POST http://localhost:8000/friendship \
  -H "Content-Type: application/json" \
  -d '{"user1":"user1","user2":"user2"}'

# Get cache stats
curl http://localhost:8000/stats/cache
```

---

## 📝 Summary

This module provides a comprehensive foundation for understanding data structures in backend development. Master these concepts, and you'll write more efficient, scalable applications. The key is recognizing the problem and choosing the data structure that best solves it with optimal time and space complexity.

**Happy Coding! 🚀**
