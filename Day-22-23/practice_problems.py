"""
Day 22-23: Practice Problems
=============================

This module contains 10+ practice problems for mastering data structures.
Each problem has:
- Problem Statement
- Constraints
- Examples
- Solution Approach
- Time/Space Complexity
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import deque
import time


# ==================== PROBLEM 1: TWO SUM ====================
"""
Problem: Given a list of integers and a target sum, find two numbers 
that add up to the target.

Example:
    numbers = [2, 7, 11, 15]
    target = 9
    Output: [2, 7]  or indices [0, 1]

Constraints:
    - Only one valid pair exists
    - Can't use same element twice
    - Return either the pair or indices
"""

def two_sum_brute_force(numbers: List[int], target: int) -> List[int]:
    """Brute force approach - check all pairs."""
    # Time: O(n²), Space: O(1)
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return [numbers[i], numbers[j]]
    return []


def two_sum_optimized(numbers: List[int], target: int) -> List[int]:
    """Optimized with Set - single pass."""
    # Time: O(n), Space: O(n)
    seen = set()
    for num in numbers:
        complement = target - num
        if complement in seen:
            return [complement, num]
        seen.add(num)
    return []


# ==================== PROBLEM 2: REVERSE STACK ====================
"""
Problem: Reverse the order of elements in a stack without using any 
additional data structures (can use recursion).

Example:
    stack = [1, 2, 3, 4, 5]
    After reverse: [5, 4, 3, 2, 1]

Constraints:
    - No additional data structures
    - Can use recursion
    - Must reverse in-place conceptually
"""

def reverse_stack(stack: List[int]) -> None:
    """Reverse stack using recursion."""
    if len(stack) <= 1:
        return
    
    # Remove bottom element
    bottom = stack.pop(0)
    
    # Recursively reverse remaining
    reverse_stack(stack)
    
    # Push bottom element to top
    stack.append(bottom)


# ==================== PROBLEM 3: VALID PARENTHESES ====================
"""
Problem: Check if a string of parentheses is valid.

Rules:
    - Every opening bracket must have matching closing bracket
    - Brackets must be in correct order
    - Types: (), [], {}

Example:
    "()" -> True
    "([{}])" -> True
    "({[}])" -> False (mismatched)
"""

def is_valid_parentheses(s: str) -> bool:
    """Check if parentheses are balanced using Stack."""
    # Time: O(n), Space: O(n)
    stack = []
    matching = {'(': ')', '[': ']', '{': '}'}
    
    for char in s:
        if char in matching:
            stack.append(char)
        else:
            if not stack or matching[stack.pop()] != char:
                return False
    
    return len(stack) == 0


# ==================== PROBLEM 4: FIRST UNIQUE CHARACTER ====================
"""
Problem: Find the first unique character in a string.

Example:
    s = "leetcode" -> 'l'
    s = "loveleetcode" -> 'v'
    s = "aabb" -> -1 (no unique)

Constraints:
    - Return character or index
    - Case sensitive
"""

def first_unique_character(s: str) -> int:
    """Find first unique character using Dict and Set."""
    # Time: O(n), Space: O(1) [max 26 letters]
    char_count = {}
    
    # Count occurrences
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    # Find first with count 1
    for i, char in enumerate(s):
        if char_count[char] == 1:
            return i
    
    return -1


# ==================== PROBLEM 5: INTERSECTION OF ARRAYS ====================
"""
Problem: Find intersection of two arrays (common elements).

Example:
    array1 = [1, 2, 3, 4]
    array2 = [2, 3, 5, 6]
    Output: [2, 3]

Constraints:
    - Each element appears once
    - Return sorted result
    - Case-sensitive for strings
"""

def array_intersection(arr1: List[int], arr2: List[int]) -> List[int]:
    """Find intersection using Sets."""
    # Time: O(n + m), Space: O(min(n, m))
    set1 = set(arr1)
    set2 = set(arr2)
    return sorted(list(set1.intersection(set2)))


# ==================== PROBLEM 6: CYCLIC DETECTION IN GRAPH ====================
"""
Problem: Detect if a graph has a cycle (undirected).

Example:
    edges = [(1, 2), (2, 3), (3, 1)]  # Has cycle: 1-2-3-1
    edges = [(1, 2), (2, 3)]  # No cycle

Constraints:
    - Undirected graph
    - N nodes, M edges
"""

def has_cycle(n: int, edges: List[Tuple[int, int]]) -> bool:
    """Detect cycle using DFS."""
    # Time: O(V + E), Space: O(V + E)
    
    # Build adjacency list
    graph: Dict[int, List[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = set()
    
    def dfs(node: int, parent: int) -> bool:
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        
        return False
    
    for i in range(n):
        if i not in visited:
            if dfs(i, -1):
                return True
    
    return False


# ==================== PROBLEM 7: LEVEL ORDER TRAVERSAL ====================
"""
Problem: Given a tree, return level order traversal (BFS).

Example:
    Tree:     1
             / \
            2   3
           / \
          4   5
    
    Output: [[1], [2, 3], [4, 5]]

Constraints:
    - Use BFS with Queue
    - Return as list of lists (one per level)
"""

class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left = None
        self.right = None


def level_order_traversal(root: Optional[TreeNode]) -> List[List[int]]:
    """Level order traversal using Queue."""
    # Time: O(n), Space: O(n)
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result


# ==================== PROBLEM 8: WORD LADDER ====================
"""
Problem: Find shortest transformation sequence from start word to end word.

Example:
    beginWord = "hit"
    endWord = "cog"
    wordList = ["hot","dot","dog","lot","log","cog"]
    
    Output: 5  (path: hit -> hot -> dot -> dog -> cog)

Constraints:
    - Only one letter can change at a time
    - Each intermediate word must be in wordList
    - Use BFS for shortest path
"""

def word_ladder_length(
    begin_word: str,
    end_word: str,
    word_list: List[str]
) -> int:
    """Find shortest word ladder using BFS."""
    # Time: O(n * l²), Space: O(n) where n=words, l=word_length
    
    word_set = set(word_list)
    if end_word not in word_set:
        return 0
    
    queue = deque([(begin_word, 1)])
    visited = {begin_word}
    
    while queue:
        word, length = queue.popleft()
        
        if word == end_word:
            return length
        
        # Try changing each letter
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c != word[i]:
                    new_word = word[:i] + c + word[i+1:]
                    
                    if new_word in word_set and new_word not in visited:
                        visited.add(new_word)
                        queue.append((new_word, length + 1))
    
    return 0


# ==================== PROBLEM 9: LRU CACHE OPERATIONS ====================
"""
Problem: Track cache hit rate and performance.

Example:
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")        # Hit
    cache.put("c", 3)     # Evicts "b"
    cache.get("b")        # Miss
"""

def analyze_cache_performance(operations: List[Tuple[str, str, int]], capacity: int) -> Dict:
    """Simulate cache and track statistics."""
    from collections import OrderedDict
    
    cache = OrderedDict()
    hits = 0
    misses = 0
    
    for op, key, *val in operations:
        if op == "get":
            if key in cache:
                hits += 1
                cache.move_to_end(key)
                result = cache[key]
            else:
                misses += 1
                result = -1
        
        elif op == "put":
            if key in cache:
                cache.move_to_end(key)
            cache[key] = val[0]
            if len(cache) > capacity:
                cache.popitem(last=False)
    
    total = hits + misses
    hit_rate = (hits / total * 100) if total > 0 else 0
    
    return {
        "hits": hits,
        "misses": misses,
        "hit_rate": f"{hit_rate:.2f}%",
        "total_operations": total
    }


# ==================== PROBLEM 10: GROUPING ANAGRAMS ====================
"""
Problem: Group anagrams from a list of strings.

Example:
    words = ["eat","tea","tan","ate","nat","bat"]
    Output: [["eat","tea","ate"],["tan","nat"],["bat"]]

Constraints:
    - Use Dictionary for grouping
    - Order doesn't matter
    - Case-sensitive
"""

def group_anagrams(words: List[str]) -> List[List[str]]:
    """Group anagrams using Dictionary."""
    # Time: O(n * k log k), Space: O(n * k)
    # where n = number of words, k = avg word length
    
    groups: Dict[str, List[str]] = {}
    
    for word in words:
        # Sort letters to create key
        key = ''.join(sorted(word))
        
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    
    return list(groups.values())


# ==================== PROBLEM 11: MAJORITY ELEMENT ====================
"""
Problem: Find element appearing more than n/2 times.

Example:
    nums = [3, 2, 3]
    Output: 3 (appears 2 times > 3/2)

Constraints:
    - Guaranteed majority element exists
    - Use optimal approach (Boyer-Moore)
"""

def find_majority_element(nums: List[int]) -> int:
    """Find majority element using Boyer-Moore voting."""
    # Time: O(n), Space: O(1)
    
    candidate = None
    count = 0
    
    for num in nums:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)
    
    return candidate


# ==================== PROBLEM 12: IMPLEMENT QUEUE WITH STACKS ====================
"""
Problem: Implement a Queue using only Stacks.

Constraints:
    - Only use two stacks
    - Enqueue: O(1)
    - Dequeue: O(1) amortized
"""

class QueueWithStacks:
    def __init__(self):
        self.stack1 = []  # Input stack
        self.stack2 = []  # Output stack
    
    def enqueue(self, x: int) -> None:
        """Add element to queue."""
        self.stack1.append(x)
    
    def dequeue(self) -> int:
        """Remove and return front element."""
        if not self.stack2:
            # Transfer all from stack1 to stack2
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        
        return self.stack2.pop() if self.stack2 else -1


# ==================== PROBLEM 13: REMOVE DUPLICATES FROM SORTED ARRAY ====================
"""
Problem: Remove duplicates from sorted array in-place.

Example:
    nums = [1, 1, 2, 2, 3, 4, 4, 5]
    After: [1, 2, 3, 4, 5, ...]
    Return: 5 (number of unique elements)

Constraints:
    - In-place modification
    - Return count of unique elements
    - Can't use extra data structures

Technique: Two-Pointer
Time Complexity: O(n)
Space Complexity: O(1)
"""

def remove_duplicates_from_sorted_array(nums: List[int]) -> int:
    """
    Two-Pointer Deduplication.
    Modifies input array in-place to remove duplicates.
    """
    if not nums:
        return 0
    
    write_index = 1
    for read_index in range(1, len(nums)):
        if nums[read_index] != nums[read_index - 1]:
            nums[write_index] = nums[read_index]
            write_index += 1
    
    return write_index


# ==================== PROBLEM 14: LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS ====================
"""
Problem: Find length of longest substring without repeating characters.

Example:
    s = "abcabcbb" -> 3 (substring "abc")
    s = "bbbbb" -> 1
    s = "pwwkew" -> 3

Technique: Variable Sliding Window
Time Complexity: O(n)
Space Complexity: O(min(m, n)) for character set (m=alphabet size)

Backend Use Case:
- Session token validation
- Cache key uniqueness
- Token deduplication in streams
"""

def length_of_longest_substring_variable_window(s: str) -> int:
    """
    Finds the length of the longest substring without repeating characters.
    Uses variable sliding window technique with character set tracking.
    """
    seen_chars = set()
    left_pointer = 0
    max_length = 0
    
    for right_pointer in range(len(s)):
        while s[right_pointer] in seen_chars:
            seen_chars.remove(s[left_pointer])
            left_pointer += 1
        
        seen_chars.add(s[right_pointer])
        max_length = max(max_length, right_pointer - left_pointer + 1)
    
    return max_length


# ==================== TEST CASES ====================

def run_tests():
    """Run all test cases."""
    print("=" * 50)
    print("Running Practice Problem Tests")
    print("=" * 50)
    
    # Problem 1: Two Sum
    print("\n✓ Problem 1: Two Sum")
    assert two_sum_optimized([2, 7, 11, 15], 9) == [2, 7]
    assert two_sum_optimized([3, 2, 4], 6) == [2, 4]
    print("  Passed!")
    
    # Problem 2: Reverse Stack
    print("\n✓ Problem 2: Reverse Stack")
    stack = [1, 2, 3, 4, 5]
    reverse_stack(stack)
    assert stack == [5, 4, 3, 2, 1]
    print("  Passed!")
    
    # Problem 3: Valid Parentheses
    print("\n✓ Problem 3: Valid Parentheses")
    assert is_valid_parentheses("()") == True
    assert is_valid_parentheses("([{}])") == True
    assert is_valid_parentheses("({[}])") == False
    print("  Passed!")
    
    # Problem 4: First Unique Character
    print("\n✓ Problem 4: First Unique Character")
    assert first_unique_character("leetcode") == 0
    assert first_unique_character("loveleetcode") == 2
    assert first_unique_character("aabb") == -1
    print("  Passed!")
    
    # Problem 5: Array Intersection
    print("\n✓ Problem 5: Array Intersection")
    assert array_intersection([1, 2, 3, 4], [2, 3, 5, 6]) == [2, 3]
    print("  Passed!")
    
    # Problem 6: Cycle Detection
    print("\n✓ Problem 6: Cycle Detection")
    assert has_cycle(3, [(0, 1), (1, 2), (2, 0)]) == True
    assert has_cycle(3, [(0, 1), (1, 2)]) == False
    print("  Passed!")
    
    # Problem 10: Group Anagrams
    print("\n✓ Problem 10: Group Anagrams")
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert len(result) == 3
    print("  Passed!")
    
    # Problem 11: Majority Element
    print("\n✓ Problem 11: Majority Element")
    assert find_majority_element([3, 2, 3]) == 3
    assert find_majority_element([2, 2, 1, 1, 1, 2, 2]) == 2
    print("  Passed!")
    
    # Problem 12: Queue with Stacks
    print("\n✓ Problem 12: Queue with Stacks")
    q = QueueWithStacks()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    print("  Passed!")
    
    # Problem 13: Remove Duplicates from Sorted Array
    print("\n✓ Problem 13: Remove Duplicates from Sorted Array")
    arr = [1, 1, 2, 2, 3, 4, 4, 5]
    count = remove_duplicates_from_sorted_array(arr)
    assert count == 5
    assert arr[:count] == [1, 2, 3, 4, 5]
    print("  Passed!")
    
    # Problem 14: Longest Substring Without Repeating Characters
    print("\n✓ Problem 14: Longest Substring Without Repeating Characters")
    assert length_of_longest_substring_variable_window("abcabcbb") == 3
    assert length_of_longest_substring_variable_window("bbbbb") == 1
    assert length_of_longest_substring_variable_window("pwwkew") == 3
    print("  Passed!")
    
    print("\n" + "=" * 50)
    print("✓ All tests passed! 🎉")
    print("=" * 50)


if __name__ == "__main__":
    run_tests()
