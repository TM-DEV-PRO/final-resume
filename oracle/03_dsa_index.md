# 03. DSA hub: patterns, how to recognize them, what to practice

Language for solutions: **Python** (fastest to write in interviews). Go is fine too. Tell the interviewer which you're using. OCI coding rounds are usually LeetCode medium, sometimes a hard, often with a follow-up ("what if the input doesn't fit in memory?", "make it thread safe").

## Topic files

1. [Arrays, strings, hashing, two pointers, sliding window, prefix sums, binary search](03_dsa_1_arrays_hashing_search.md)
2. [Linked list, stack, monotonic stack, queue, deque, heap](03_dsa_2_linkedlist_stack_queue_heap.md)
3. [Trees, BST, trie](03_dsa_3_trees_bst_trie.md)
4. [Graphs, BFS/DFS, topological sort, shortest paths, MST, DSU](03_dsa_4_graphs_dsu.md)
5. [Dynamic programming](03_dsa_5_dynamic_programming.md)
6. [Backtracking, greedy, intervals, matrix, bit manipulation, math](03_dsa_6_backtracking_greedy_intervals_matrix_bits.md)

---

## The 45 minute coding round, step by step

1. **Clarify (3 min).** Input size? Negative numbers? Duplicates? Sorted? Empty input? Return what, if there's no answer? Can I modify the input?
2. **Examples (2 min).** Walk one normal and one edge case by hand.
3. **Brute force out loud (2 min).** State its complexity. That shows you can always get *an* answer.
4. **Optimize (5 min).** Name the pattern. "This is a sliding window because we want the longest contiguous subarray with a property that is monotonic as the window grows."
5. **Code (15 min).** Clean names, helper functions, no clever one-liners.
6. **Test (5 min).** Trace your example through the code. Then edge cases: empty, one element, all same, max size.
7. **Complexity (1 min).** Time and space, with the reason.
8. **Follow-ups.** Scale, streaming, concurrency, memory.

---

## Pattern recognition table

| If the problem says... | Think | File |
|---|---|---|
| "subarray / substring", "contiguous", "longest/shortest with condition" | Sliding window | 1 |
| "sum of subarray equals k", "range sum", "count subarrays" | Prefix sum + hashmap | 1 |
| Sorted array, "pair with sum", "remove duplicates in place" | Two pointers | 1 |
| Sorted, or "minimum X such that feasible(X)" | Binary search (on index or on answer) | 1 |
| "Anagram", "frequency", "seen before", "group by" | Hashmap / counter | 1 |
| "next greater/smaller", "span", "histogram" | Monotonic stack | 2 |
| "Matching brackets", "undo", "evaluate expression" | Stack | 2 |
| "k-th largest", "top k", "merge k sorted", "median of stream" | Heap | 2 |
| "Sliding window max/min" | Monotonic deque | 2 |
| "Cycle in list", "middle", "k-th from end" | Fast/slow pointers | 2 |
| Tree traversal, "path", "depth", "LCA" | DFS recursion (return info up) | 3 |
| "Level by level", "right side view" | BFS on tree | 3 |
| "Prefix", "autocomplete", "word search many words" | Trie | 3 |
| "Shortest path, unweighted", "min steps" | BFS | 4 |
| "Weighted shortest path, non-negative" | Dijkstra | 4 |
| "Dependencies", "ordering", "course schedule" | Topological sort | 4 |
| "Connected components", "union", "redundant edge", "accounts merge" | DSU / union-find | 4 |
| "Number of ways", "min/max cost", "can you reach", overlapping subproblems | DP | 5 |
| "All combinations/permutations/subsets", "place N queens" | Backtracking | 6 |
| "Intervals", "meeting rooms", "merge" | Sort by start + sweep / heap | 6 |
| "Locally best choice works", "schedule to maximize" | Greedy (prove with exchange argument) | 6 |
| "Grid", "islands", "rotate" | Matrix traversal / BFS/DFS on grid | 6, 4 |
| "Single number", "XOR", "power of two", "subsets as masks" | Bit manipulation | 6 |

---

## Complexity cheat sheet

| n | Allowed complexity (~1 second) |
|---|---|
| ≤ 10 | O(n!) |
| ≤ 20 | O(2^n) |
| ≤ 500 | O(n^3) |
| ≤ 5,000 | O(n^2) |
| ≤ 10^6 | O(n log n) |
| ≤ 10^8 | O(n) |
| larger | O(log n) or O(1) |

| Structure | Access | Search | Insert | Delete |
|---|---|---|---|---|
| Array / list | O(1) | O(n) | O(n) (O(1) amortized append) | O(n) |
| Hashmap / set | n/a | O(1) avg | O(1) avg | O(1) avg |
| Heap | O(1) top | O(n) | O(log n) | O(log n) pop |
| Balanced BST | O(log n) | O(log n) | O(log n) | O(log n) |
| Linked list | O(n) | O(n) | O(1) at a node | O(1) at a node |
| Trie | n/a | O(L) | O(L) | O(L) |
| DSU | n/a | ~O(α(n)) | ~O(α(n)) union | n/a |

Sorting: O(n log n) (Python's Timsort is stable). Heap building: O(n). BFS/DFS: O(V + E). Dijkstra: O((V + E) log V).

---

## Python tools you should use without thinking

```python
from collections import Counter, defaultdict, deque, OrderedDict
import heapq          # min-heap; push -x for max-heap
import bisect         # bisect_left / bisect_right on sorted lists
from functools import lru_cache, cache
from itertools import accumulate, combinations, permutations, product
import math           # math.inf, math.gcd, math.isqrt
```

- `heapq.heappush(h, (priority, tiebreak, item))`: add a tiebreak counter if items aren't comparable.
- `deque.popleft()` is O(1); `list.pop(0)` is O(n).
- Recursion limit: use `sys.setrecursionlimit(10**6)` or convert to an iterative loop for deep DFS.
- `@cache` on a nested function is the fastest way to write top-down DP.

---

## Top 100 list (do in this order, grouped)

**Arrays and hashing:** Two Sum, Group Anagrams, Top K Frequent, Product of Array Except Self, Longest Consecutive Sequence, Valid Sudoku, Encode/Decode Strings, Subarray Sum Equals K.

**Two pointers:** Valid Palindrome, 3Sum, Container With Most Water, Trapping Rain Water, Sort Colors.

**Sliding window:** Best Time to Buy/Sell Stock, Longest Substring Without Repeating, Longest Repeating Character Replacement, Permutation in String, Minimum Window Substring, Sliding Window Maximum.

**Binary search:** Binary Search, Search in Rotated Sorted Array, Find Min in Rotated, Koko Eating Bananas, Time Based Key-Value Store, Median of Two Sorted Arrays, Capacity to Ship Packages.

**Stack:** Valid Parentheses, Min Stack, Evaluate RPN, Daily Temperatures, Car Fleet, Largest Rectangle in Histogram, Decode String, Asteroid Collision.

**Linked list:** Reverse List, Merge Two Sorted, Linked List Cycle, Reorder List, Remove Nth From End, Copy List with Random Pointer, Add Two Numbers, LRU Cache, Merge K Sorted, Reverse Nodes in K-Group.

**Trees:** Invert, Max Depth, Diameter, Balanced, Same Tree, Subtree, LCA of BST, Level Order, Right Side View, Good Nodes, Validate BST, Kth Smallest in BST, Build from Preorder+Inorder, Max Path Sum, Serialize/Deserialize.

**Trie:** Implement Trie, Add and Search Words, Word Search II.

**Heap:** Kth Largest in Stream, Last Stone Weight, K Closest Points, Task Scheduler, Design Twitter, Find Median from Data Stream.

**Graphs:** Number of Islands, Clone Graph, Max Area of Island, Pacific Atlantic, Surrounded Regions, Rotting Oranges, Course Schedule I/II, Redundant Connection, Number of Connected Components, Graph Valid Tree, Word Ladder, Network Delay Time, Cheapest Flights Within K Stops, Min Cost to Connect Points, Alien Dictionary, Accounts Merge.

**DP:** Climbing Stairs, House Robber I/II, Longest Palindromic Substring, Palindromic Substrings, Decode Ways, Coin Change, Max Product Subarray, Word Break, LIS, Partition Equal Subset Sum, Unique Paths, LCS, Best Time with Cooldown, Coin Change II, Target Sum, Interleaving String, Edit Distance, Burst Balloons, Regular Expression Matching.

**Backtracking:** Subsets, Combination Sum, Permutations, Subsets II, Word Search, Palindrome Partitioning, Letter Combinations, N-Queens.

**Intervals and greedy:** Merge Intervals, Insert Interval, Non-overlapping Intervals, Meeting Rooms II, Jump Game I/II, Gas Station, Hand of Straights, Partition Labels.

**Bits:** Single Number, Number of 1 Bits, Counting Bits, Reverse Bits, Missing Number, Sum of Two Integers.

**OCI-flavored (seen in cloud interviews):** LRU/LFU Cache, Design Hit Counter, Rate Limiter, Time Based Key-Value Store, Merge K Sorted (log merge), Top K Frequent (logs), Meeting Rooms II (resource allocation), Course Schedule (dependency resolution), Word Ladder, Network Delay Time, Snapshot Array, File System design, Logger Rate Limiter.
