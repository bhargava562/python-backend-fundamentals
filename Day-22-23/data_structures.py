"""
Day 22: Core Data Structures Implementation
============================================

This module implements essential data structures used in backend development.
Each structure is optimized for specific use cases in FastAPI applications.

Core Concepts:
- Linear Structures: Arrays, Stacks, Queues
- Hash-Based Structures: Dictionaries, Sets
- Hierarchical Structures: Trees
- Network Structures: Graphs
"""

from collections import deque
from typing import Any, List, Optional, Dict, Set


# ==================== PHASE 1: LINEAR STRUCTURES ====================

class RequestStack:
    """
    Simulates a back-button or undo history for user actions.
    
    Use Case: Browser history, undo/redo functionality, expression evaluation
    Time Complexity:
    - push: O(1)
    - pop: O(1)
    - peek: O(1)
    Space Complexity: O(n)
    """
    
    def __init__(self):
        self.stack = []
    
    def push(self, action: str) -> None:
        """Add an action to the stack."""
        self.stack.append(action)
    
    def pop(self) -> str:
        """Remove and return the top action."""
        return self.stack.pop() if self.stack else "No history"
    
    def peek(self) -> str:
        """View the top action without removing it."""
        return self.stack[-1] if self.stack else "Stack is empty"
    
    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self.stack) == 0
    
    def size(self) -> int:
        """Return the number of items in stack."""
        return len(self.stack)


class BackgroundTaskQueue:
    """
    Simulates a basic background task processor (like Celery/Redis).
    
    Use Case: Task queues, request handling, event processing
    Time Complexity:
    - enqueue: O(1)
    - dequeue: O(1)
    Space Complexity: O(n)
    """
    
    def __init__(self):
        self.queue = deque()
    
    def enqueue_task(self, task_id: str) -> None:
        """Add a task to the back of the queue."""
        self.queue.append(task_id)
    
    def dequeue_task(self) -> str:
        """Remove and return a task from the front."""
        return self.queue.popleft() if self.queue else "No tasks pending"
    
    def peek_next_task(self) -> str:
        """View the next task without removing it."""
        return self.queue[0] if self.queue else "Queue is empty"
    
    def queue_size(self) -> int:
        """Return the number of tasks in queue."""
        return len(self.queue)
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.queue) == 0


# ==================== PHASE 2: HASH-BASED STRUCTURES ====================

class UserCache:
    """
    In-memory user cache using dictionaries (hash tables).
    
    Use Case: Session management, caching user profiles, fast lookups
    Time Complexity:
    - get: O(1) average
    - set: O(1) average
    - delete: O(1) average
    Space Complexity: O(n)
    """
    
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def set_user(self, user_id: str, user_data: Dict[str, Any]) -> None:
        """Store or update user data."""
        self.cache[user_id] = user_data
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user data."""
        return self.cache.get(user_id)
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user data."""
        if user_id in self.cache:
            del self.cache[user_id]
            return True
        return False
    
    def user_exists(self, user_id: str) -> bool:
        """Check if user exists."""
        return user_id in self.cache
    
    def get_all_users(self) -> Dict[str, Dict[str, Any]]:
        """Return all cached users."""
        return self.cache.copy()


class PermissionManager:
    """
    Manages permissions using sets for O(1) membership testing.
    
    Use Case: Role-based access control, permission checking, whitelists/blacklists
    Time Complexity:
    - add: O(1) average
    - remove: O(1) average
    - contains: O(1) average
    Space Complexity: O(n)
    """
    
    def __init__(self):
        self.permissions: Set[str] = set()
        self.role_permissions: Dict[str, Set[str]] = {}
    
    def add_permission(self, permission: str) -> None:
        """Add a permission."""
        self.permissions.add(permission)
    
    def remove_permission(self, permission: str) -> None:
        """Remove a permission."""
        self.permissions.discard(permission)
    
    def has_permission(self, permission: str) -> bool:
        """Check if permission exists."""
        return permission in self.permissions
    
    def assign_role_permissions(self, role: str, permissions: List[str]) -> None:
        """Assign multiple permissions to a role."""
        self.role_permissions[role] = set(permissions)
    
    def check_role_permission(self, role: str, permission: str) -> bool:
        """Check if role has specific permission."""
        return permission in self.role_permissions.get(role, set())
    
    def get_role_permissions(self, role: str) -> Set[str]:
        """Get all permissions for a role."""
        return self.role_permissions.get(role, set()).copy()


# ==================== PHASE 3: HIERARCHICAL STRUCTURES ====================

class CategoryNode:
    """
    Tree node for hierarchical category structure.
    
    Use Case: Product categories, organizational hierarchy, menu structure
    Time Complexity (for building): O(n)
    Space Complexity: O(n)
    """
    
    def __init__(self, name: str, category_id: int):
        self.name = name
        self.category_id = category_id
        self.children: List['CategoryNode'] = []
        self.parent: Optional['CategoryNode'] = None
    
    def add_child(self, child_node: 'CategoryNode') -> None:
        """Add a child category."""
        self.children.append(child_node)
        child_node.parent = self
    
    def get_children(self) -> List['CategoryNode']:
        """Get all child categories."""
        return self.children
    
    def get_path(self) -> List[str]:
        """Get the path from root to this node."""
        path = []
        current = self
        while current:
            path.append(current.name)
            current = current.parent
        return list(reversed(path))
    
    def traverse_dfs(self) -> List[str]:
        """Depth-first traversal of category tree."""
        result = [self.name]
        for child in self.children:
            result.extend(child.traverse_dfs())
        return result
    
    def traverse_bfs(self) -> List[str]:
        """Breadth-first traversal of category tree."""
        result = []
        queue = deque([self])
        while queue:
            node = queue.popleft()
            result.append(node.name)
            queue.extend(node.children)
        return result


# ==================== PHASE 4: NETWORK STRUCTURES ====================

class SocialGraph:
    """
    Graph representation using adjacency list (undirected graph).
    
    Use Case: Social networks, friend recommendations, connection mapping
    Time Complexity:
    - add_user: O(1)
    - add_friendship: O(1)
    - get_friends: O(1)
    - find_path (BFS): O(V + E)
    Space Complexity: O(V + E)
    """
    
    def __init__(self):
        self.graph: Dict[str, List[str]] = {}
    
    def add_user(self, user: str) -> None:
        """Add a user to the graph."""
        if user not in self.graph:
            self.graph[user] = []
    
    def add_friendship(self, user1: str, user2: str) -> None:
        """Add a bidirectional friendship."""
        self.add_user(user1)
        self.add_user(user2)
        
        if user2 not in self.graph[user1]:
            self.graph[user1].append(user2)
        if user1 not in self.graph[user2]:
            self.graph[user2].append(user1)
    
    def remove_friendship(self, user1: str, user2: str) -> None:
        """Remove a friendship."""
        if user1 in self.graph:
            self.graph[user1] = [u for u in self.graph[user1] if u != user2]
        if user2 in self.graph:
            self.graph[user2] = [u for u in self.graph[user2] if u != user1]
    
    def get_friends(self, user: str) -> List[str]:
        """Get all friends of a user."""
        return self.graph.get(user, [])
    
    def find_path_bfs(self, start: str, end: str) -> Optional[List[str]]:
        """Find shortest path between two users using BFS."""
        if start not in self.graph or end not in self.graph:
            return None
        
        if start == end:
            return [start]
        
        visited = {start}
        queue = deque([(start, [start])])
        
        while queue:
            user, path = queue.popleft()
            
            for friend in self.graph[user]:
                if friend == end:
                    return path + [friend]
                
                if friend not in visited:
                    visited.add(friend)
                    queue.append((friend, path + [friend]))
        
        return None
    
    def get_mutual_friends(self, user1: str, user2: str) -> List[str]:
        """Find mutual friends between two users."""
        friends1 = set(self.get_friends(user1))
        friends2 = set(self.get_friends(user2))
        return list(friends1.intersection(friends2))
    
    def get_all_users(self) -> List[str]:
        """Get all users in the graph."""
        return list(self.graph.keys())


# ==================== PHASE 5: PRACTICAL ANALYSIS ====================

def analyze_list_operations():
    """
    Demonstrates time complexity of list operations.
    """
    # Access: O(1)
    items = [1, 2, 3, 4, 5]
    first = items[0]  # O(1)
    
    # Append: O(1) amortized
    items.append(6)  # O(1)
    
    # Insert at beginning: O(n) - SLOW!
    items.insert(0, 0)  # O(n)
    
    # Search: O(n)
    index = items.index(3)  # O(n)
    
    return items


def demonstrate_set_efficiency():
    """
    Demonstrates efficiency of set membership testing.
    """
    # Creating a set for fast lookups
    valid_tokens = {"token_abc123", "token_xyz789", "token_qwe456"}
    
    # Checking membership: O(1) average
    is_valid = "token_abc123" in valid_tokens  # True
    
    # vs. checking in a list: O(n)
    token_list = ["token_abc123", "token_xyz789", "token_qwe456"]
    is_valid_list = "token_abc123" in token_list  # O(n)
    
    return is_valid


if __name__ == "__main__":
    # Example: Stack usage
    print("=== Stack Example ===")
    undo_stack = RequestStack()
    undo_stack.push("Created user")
    undo_stack.push("Updated profile")
    undo_stack.push("Changed settings")
    print(f"Undo: {undo_stack.pop()}")
    print(f"Undo: {undo_stack.pop()}")
    print()
    
    # Example: Queue usage
    print("=== Queue Example ===")
    task_queue = BackgroundTaskQueue()
    task_queue.enqueue_task("send_email_1")
    task_queue.enqueue_task("send_email_2")
    task_queue.enqueue_task("generate_report")
    print(f"Processing: {task_queue.dequeue_task()}")
    print(f"Processing: {task_queue.dequeue_task()}")
    print()
    
    # Example: Graph usage
    print("=== Graph Example ===")
    social_graph = SocialGraph()
    social_graph.add_friendship("Alice", "Bob")
    social_graph.add_friendship("Bob", "Charlie")
    social_graph.add_friendship("Alice", "David")
    print(f"Alice's friends: {social_graph.get_friends('Alice')}")
    path = social_graph.find_path_bfs("Alice", "Charlie")
    print(f"Path from Alice to Charlie: {path}")
    print()
    
    # Example: Tree traversal
    print("=== Tree Example ===")
    root = CategoryNode("Electronics", 1)
    computers = CategoryNode("Computers", 2)
    phones = CategoryNode("Phones", 3)
    root.add_child(computers)
    root.add_child(phones)
    print(f"DFS traversal: {root.traverse_dfs()}")
    print(f"BFS traversal: {root.traverse_bfs()}")
