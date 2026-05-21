"""
Unit tests for data_structures.py
"""

import pytest
from data_structures import (
    RequestStack,
    BackgroundTaskQueue,
    UserCache,
    PermissionManager,
    CategoryNode,
    SocialGraph
)


class TestStack:
    """Test Stack implementation."""
    
    def test_stack_push_pop(self):
        stack = RequestStack()
        stack.push("action1")
        stack.push("action2")
        assert stack.pop() == "action2"
        assert stack.pop() == "action1"
    
    def test_stack_empty_pop(self):
        stack = RequestStack()
        assert stack.pop() == "No history"
    
    def test_stack_peek(self):
        stack = RequestStack()
        stack.push("action1")
        stack.push("action2")
        assert stack.peek() == "action2"
        assert stack.size() == 2
    
    def test_stack_is_empty(self):
        stack = RequestStack()
        assert stack.is_empty() == True
        stack.push("action")
        assert stack.is_empty() == False
    
    def test_stack_size(self):
        stack = RequestStack()
        assert stack.size() == 0
        stack.push("a")
        stack.push("b")
        assert stack.size() == 2


class TestQueue:
    """Test Queue implementation."""
    
    def test_queue_enqueue_dequeue(self):
        queue = BackgroundTaskQueue()
        queue.enqueue_task("task1")
        queue.enqueue_task("task2")
        assert queue.dequeue_task() == "task1"
        assert queue.dequeue_task() == "task2"
    
    def test_queue_empty_dequeue(self):
        queue = BackgroundTaskQueue()
        assert queue.dequeue_task() == "No tasks pending"
    
    def test_queue_peek_next(self):
        queue = BackgroundTaskQueue()
        queue.enqueue_task("task1")
        queue.enqueue_task("task2")
        assert queue.peek_next_task() == "task1"
        assert queue.queue_size() == 2
    
    def test_queue_is_empty(self):
        queue = BackgroundTaskQueue()
        assert queue.is_empty() == True
        queue.enqueue_task("task")
        assert queue.is_empty() == False


class TestUserCache:
    """Test Dictionary-based user cache."""
    
    def test_set_and_get_user(self):
        cache = UserCache()
        user_data = {"name": "Alice", "role": "admin"}
        cache.set_user("user1", user_data)
        assert cache.get_user("user1") == user_data
    
    def test_user_exists(self):
        cache = UserCache()
        assert cache.user_exists("user1") == False
        cache.set_user("user1", {"name": "Alice"})
        assert cache.user_exists("user1") == True
    
    def test_delete_user(self):
        cache = UserCache()
        cache.set_user("user1", {"name": "Alice"})
        assert cache.delete_user("user1") == True
        assert cache.user_exists("user1") == False
    
    def test_delete_nonexistent_user(self):
        cache = UserCache()
        assert cache.delete_user("user1") == False
    
    def test_get_all_users(self):
        cache = UserCache()
        cache.set_user("user1", {"name": "Alice"})
        cache.set_user("user2", {"name": "Bob"})
        users = cache.get_all_users()
        assert len(users) == 2


class TestPermissionManager:
    """Test Set-based permission management."""
    
    def test_add_and_check_permission(self):
        manager = PermissionManager()
        manager.add_permission("read")
        assert manager.has_permission("read") == True
    
    def test_remove_permission(self):
        manager = PermissionManager()
        manager.add_permission("write")
        manager.remove_permission("write")
        assert manager.has_permission("write") == False
    
    def test_role_permissions(self):
        manager = PermissionManager()
        manager.assign_role_permissions("admin", ["read", "write", "delete"])
        assert manager.check_role_permission("admin", "read") == True
        assert manager.check_role_permission("admin", "execute") == False
    
    def test_get_role_permissions(self):
        manager = PermissionManager()
        perms = ["read", "write"]
        manager.assign_role_permissions("user", perms)
        result = manager.get_role_permissions("user")
        assert result == set(perms)


class TestCategoryTree:
    """Test Tree structure for categories."""
    
    def test_create_tree(self):
        root = CategoryNode("Electronics", 1)
        assert root.name == "Electronics"
        assert len(root.children) == 0
    
    def test_add_children(self):
        root = CategoryNode("Electronics", 1)
        phones = CategoryNode("Phones", 2)
        computers = CategoryNode("Computers", 3)
        
        root.add_child(phones)
        root.add_child(computers)
        
        assert len(root.children) == 2
        assert phones.parent == root
    
    def test_get_path(self):
        root = CategoryNode("Electronics", 1)
        phones = CategoryNode("Phones", 2)
        flagship = CategoryNode("Flagship", 3)
        
        root.add_child(phones)
        phones.add_child(flagship)
        
        path = flagship.get_path()
        assert path == ["Electronics", "Phones", "Flagship"]
    
    def test_dfs_traversal(self):
        root = CategoryNode("Root", 1)
        child1 = CategoryNode("Child1", 2)
        child2 = CategoryNode("Child2", 3)
        grandchild = CategoryNode("GrandChild", 4)
        
        root.add_child(child1)
        root.add_child(child2)
        child1.add_child(grandchild)
        
        result = root.traverse_dfs()
        assert result == ["Root", "Child1", "GrandChild", "Child2"]
    
    def test_bfs_traversal(self):
        root = CategoryNode("Root", 1)
        child1 = CategoryNode("Child1", 2)
        child2 = CategoryNode("Child2", 3)
        grandchild = CategoryNode("GrandChild", 4)
        
        root.add_child(child1)
        root.add_child(child2)
        child1.add_child(grandchild)
        
        result = root.traverse_bfs()
        assert result == ["Root", "Child1", "Child2", "GrandChild"]


class TestSocialGraph:
    """Test Graph structure for social networks."""
    
    def test_add_user(self):
        graph = SocialGraph()
        graph.add_user("Alice")
        assert graph.get_all_users() == ["Alice"]
    
    def test_add_friendship(self):
        graph = SocialGraph()
        graph.add_friendship("Alice", "Bob")
        friends_alice = graph.get_friends("Alice")
        assert "Bob" in friends_alice
    
    def test_get_friends(self):
        graph = SocialGraph()
        graph.add_friendship("Alice", "Bob")
        graph.add_friendship("Alice", "Charlie")
        friends = graph.get_friends("Alice")
        assert len(friends) == 2
    
    def test_remove_friendship(self):
        graph = SocialGraph()
        graph.add_friendship("Alice", "Bob")
        graph.remove_friendship("Alice", "Bob")
        assert "Bob" not in graph.get_friends("Alice")
    
    def test_find_path_bfs_direct(self):
        graph = SocialGraph()
        graph.add_friendship("Alice", "Bob")
        path = graph.find_path_bfs("Alice", "Bob")
        assert path == ["Alice", "Bob"]
    
    def test_find_path_bfs_indirect(self):
        graph = SocialGraph()
        graph.add_friendship("Alice", "Bob")
        graph.add_friendship("Bob", "Charlie")
        path = graph.find_path_bfs("Alice", "Charlie")
        assert path == ["Alice", "Bob", "Charlie"]
    
    def test_find_path_bfs_not_connected(self):
        graph = SocialGraph()
        graph.add_friendship("Alice", "Bob")
        graph.add_friendship("Charlie", "David")
        path = graph.find_path_bfs("Alice", "Charlie")
        assert path is None
    
    def test_mutual_friends(self):
        graph = SocialGraph()
        graph.add_friendship("Alice", "Charlie")
        graph.add_friendship("Bob", "Charlie")
        mutual = graph.get_mutual_friends("Alice", "Bob")
        assert mutual == ["Charlie"]
    
    def test_mutual_friends_none(self):
        graph = SocialGraph()
        graph.add_friendship("Alice", "Bob")
        graph.add_friendship("Charlie", "David")
        mutual = graph.get_mutual_friends("Alice", "Charlie")
        assert mutual == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
