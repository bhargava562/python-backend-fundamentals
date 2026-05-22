import time
from typing import List, Dict, Any, Optional, Tuple
from collections import deque

# =====================================================================
# 1. SEARCHING ALGORITHMS
# =====================================================================

def linear_search_products(products: List[Dict[str, Any]], target_sku: str) -> Optional[Dict[str, Any]]:
    """
    Scans a list sequentially for a matching SKU.
    Time Complexity: Worst O(n), Best O(1)
    Space Complexity: O(1)
    Use Case: Unsorted datasets, small datasets, or stream processing.
    """
    for product in products:
        if product["sku"] == target_sku:
            return product
    return None

def binary_search_products(sorted_products: List[Dict[str, Any]], target_sku: str) -> Optional[Dict[str, Any]]:
    """
    Divides and conquers a sorted array to locate a matching SKU.
    Time Complexity: Worst/Average O(log n), Best O(1)
    Space Complexity: O(1)
    Use Case: Read-heavy cached inventory lookup where data is pre-sorted.
    """
    low, high = 0, len(sorted_products) - 1
    
    while low <= high:
        mid = (low + high) // 2
        mid_sku = sorted_products[mid]["sku"]
        
        if mid_sku == target_sku:
            return sorted_products[mid]
        elif mid_sku < target_sku:
            low = mid + 1
        else:
            high = mid - 1
    return None

# =====================================================================
# 2. SORTING ALGORITHMS
# =====================================================================

def bubble_sort_orders(orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Repeatedly steps through the list, compares adjacent elements, and swaps them.
    Time Complexity: Worst/Average O(n²), Best O(n) if pre-sorted
    Space Complexity: O(1) (In-place)
    Use Case: Educational. Highly inefficient for any live production backend payload.
    """
    arr = list(orders) # Create copy to prevent modifying in-place unexpectedly
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j]["timestamp"] > arr[j + 1]["timestamp"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def quick_sort_orders(orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Selects a pivot element and partitions the array around it.
    Time Complexity: Average O(n log n), Worst O(n²) if pivot selections are poor
    Space Complexity: O(log n) stack space due to recursion
    Use Case: Memory-constrained systems needing rapid, volatile sorting. Unstable.
    """
    if len(orders) <= 1:
        return orders
    else:
        pivot = orders[len(orders) // 2]
        left = [x for x in orders if x["timestamp"] < pivot["timestamp"]]
        middle = [x for x in orders if x["timestamp"] == pivot["timestamp"]]
        right = [x for x in orders if x["timestamp"] > pivot["timestamp"]]
        return quick_sort_orders(left) + middle + quick_sort_orders(right)

def merge_sort_orders(orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Recursively divides the array in half, sorts them, and merges back together.
    Time Complexity: All cases O(n log n)
    Space Complexity: O(n) auxiliary memory allocation
    Use Case: Stable sorting required for data structures (preserves original order of duplicates).
    """
    if len(orders) <= 1:
        return orders
        
    mid = len(orders) // 2
    left = merge_sort_orders(orders[:mid])
    right = merge_sort_orders(orders[mid:])
    
    return _merge(left, right)

def _merge(left: List[Dict[str, Any]], right: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i]["timestamp"] <= right[j]["timestamp"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# =====================================================================
# 3. POINTER AND WINDOW TECHNIQUES
# =====================================================================

def find_user_pair_with_target_score(sorted_users: List[Tuple[str, int]], target_score: int) -> Optional[Tuple[str, str]]:
    """
    Two-pointer technique to find two users whose scores sum exactly to a target.
    Time Complexity: O(n)
    Space Complexity: O(1)
    Use Case: Matchmaking algorithms, processing pre-aggregated user metrics.
    """
    left = 0
    right = len(sorted_users) - 1
    
    while left < right:
        current_sum = sorted_users[left][1] + sorted_users[right][1]
        if current_sum == target_score:
            return (sorted_users[left][0], sorted_users[right][0])
        elif current_sum < target_score:
            left += 1
        else:
            right -= 1
    return None

def max_revenue_sliding_window(sales: List[float], window_size: int) -> float:
    """
    Computes maximum revenue over a fixed continuous timeframe window.
    Time Complexity: O(n)
    Space Complexity: O(1)
    Use Case: Rolling metrics, financial analytics dashboards, streaming throughput evaluation.
    """
    if len(sales) < window_size or window_size <= 0:
        return 0.0
        
    current_window_sum = sum(sales[:window_size])
    max_sum = current_window_sum
    
    for i in range(len(sales) - window_size):
        current_window_sum = current_window_sum - sales[i] + sales[i + window_size]
        if current_window_sum > max_sum:
            max_sum = current_window_sum
            
    return max_sum
