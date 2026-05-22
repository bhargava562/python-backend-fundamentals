import time
import random
from typing import List, Dict, Any
from algorithms import bubble_sort_orders, merge_sort_orders

# =====================================================================
# RECURSIVE FILE SYSTEM / CATEGORY FLATTENER
# =====================================================================

def flatten_categories_recursive(node: Dict[str, Any], current_path: str = "") -> List[Dict[str, str]]:
    """
    Uses recursion to flatten a deeply nested hierarchical category structure into absolute paths.
    Time Complexity: O(N) where N is total number of categories
    Space Complexity: O(H) call stack depth where H is tree height. Risk of Stack Overflow if H > 1000.
    """
    results = []
    new_path = f"{current_path}/{node['name']}" if current_path else node["name"]
    results.append({"id": node["id"], "path": new_path})
    
    for child in node.get("children", []):
        results.extend(flatten_categories_recursive(child, new_path))
        
    return results

def flatten_categories_iterative(root_node: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Iterative stack-based variation to bypass recursion limits completely.
    Time Complexity: O(N)
    Space Complexity: O(N) heap memory storage instead of application execution stack frame limits.
    """
    results = []
    stack = [(root_node, "")]
    
    while stack:
        node, current_path = stack.pop()
        new_path = f"{current_path}/{node['name']}" if current_path else node["name"]
        results.append({"id": node["id"], "path": new_path})
        
        # Reverse children addition to maintain matching execution order to DFS recursion
        for child in reversed(node.get("children", [])):
            stack.append((child, new_path))
            
    return results

# =====================================================================
# MICRO-BENCHMARKING ENGINE
# =====================================================================

def execute_performance_benchmark():
    """
    Generates dynamic mock data blocks to track, contrast, and log algorithmic performance.
    """
    print("====== STARTING BACKEND RUNTIME OPTIMIZATION BENCHMARK ======")
    
    # 1. Sort Benchmarks
    dataset_sizes = [500, 2000]
    
    for size in dataset_sizes:
        mock_orders = [{"id": f"ord_{i}", "timestamp": random.random()} for i in range(size)]
        
        # Measure Bubble Sort
        start_time = time.perf_counter()
        _ = bubble_sort_orders(mock_orders)
        bubble_duration = time.perf_counter() - start_time
        
        # Measure Merge Sort
        start_time = time.perf_counter()
        _ = merge_sort_orders(mock_orders)
        merge_duration = time.perf_counter() - start_time
        
        improvement_factor = bubble_duration / merge_duration if merge_duration > 0 else 1
        print(f"\nDataset Order Size: {size}")
        print(f" -> Unoptimized Bubble Sort O(n²): {bubble_duration:.5f} seconds")
        print(f" -> Optimized Merge Sort O(n log n): {merge_duration:.5f} seconds")
        print(f" -> Mathematical Optimization Lift: {improvement_factor:.2f}x Faster Execution")

if __name__ == "__main__":
    execute_performance_benchmark()
