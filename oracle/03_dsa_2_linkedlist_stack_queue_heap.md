# 03.2 Linked list, stack, monotonic stack, queue, deque, heap

---

## A. Linked list

**Intuition:** pointer manipulation. Draw it. Use a **dummy head** whenever the head might change. Use **fast/slow** pointers for middle, cycles, and k-th from the end.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next
```

### A1. Reverse Linked List (iterative, then recursive)

```python
def reverse(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev

def reverse_rec(head):
    if not head or not head.next:
        return head
    new_head = reverse_rec(head.next)
    head.next.next = head
    head.next = None
    return new_head
```
O(n) time. Iterative is O(1) space, recursive O(n) stack.

### A2. Merge Two Sorted Lists

```python
def merge(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next
```

### A3. Linked List Cycle and cycle start (Floyd)
**Intuition:** fast moves 2, slow moves 1. If there's a cycle they meet. To find the start, reset one pointer to the head and move both by 1; they meet at the cycle start (distance math: `a = k·c - b`).

```python
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            slow = head
            while slow is not fast:
                slow, fast = slow.next, fast.next
            return slow
    return None
```
O(n) time, O(1) space. Same trick: Find the Duplicate Number (array as a linked list).

### A4. Remove Nth From End
Move `fast` n steps ahead, then move both until `fast.next` is None. Use a dummy for the "remove head" case.

### A5. Reorder List (L0 → Ln → L1 → Ln-1)
Find the middle (fast/slow), reverse the second half, then merge alternately. O(n), O(1).

### A6. Copy List with Random Pointer
Hashmap old → new (O(n) space), or interleave copies `A → A' → B → B'`, set randoms, then split (O(1) extra).

```python
def copy_random_list(head):
    m = {None: None}
    cur = head
    while cur:
        m[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:
        m[cur].next = m[cur.next]
        m[cur].random = m[cur.random]
        cur = cur.next
    return m[head]
```

### A7. Reverse Nodes in k-Group (hard)
For each group: check that k nodes exist, reverse them, then connect the previous group's tail to the new head.

```python
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next
        group_next = kth.next
        prev, cur = group_next, group_prev.next
        while cur is not group_next:
            cur.next, prev, cur = prev, cur, cur.next
        first = group_prev.next
        group_prev.next = kth
        group_prev = first
```

### A8. LRU Cache: see [LLD problems](05_lld_problems.md) (hashmap + doubly linked list, O(1) get/put).

---

## B. Stack

**Intuition:** last in, first out. Use it for nesting (brackets, expressions, directories), undo, and DFS without recursion.

### B1. Valid Parentheses

```python
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    st = []
    for c in s:
        if c in pairs:
            if not st or st.pop() != pairs[c]:
                return False
        else:
            st.append(c)
    return not st
```

### B2. Min Stack (O(1) getMin)
Push `(value, current_min)` pairs.

```python
class MinStack:
    def __init__(self):
        self.st = []
    def push(self, x):
        self.st.append((x, min(x, self.st[-1][1]) if self.st else x))
    def pop(self):
        self.st.pop()
    def top(self):
        return self.st[-1][0]
    def get_min(self):
        return self.st[-1][1]
```

### B3. Evaluate Reverse Polish Notation
Push numbers. On an operator, pop b, then a, and push `a op b`. Use `int(a / b)` for truncation toward zero.

### B4. Decode String `3[a2[c]]` → `accaccacc`

```python
def decode_string(s):
    st = []            # (prev_string, repeat)
    cur, num = "", 0
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c == "[":
            st.append((cur, num))
            cur, num = "", 0
        elif c == "]":
            prev, k = st.pop()
            cur = prev + cur * k
        else:
            cur += c
    return cur
```

### B5. Basic Calculator (with + - and parentheses)
Keep `result`, `sign`, and a stack of `(result, sign)` pushed at `(`.

### B6. Asteroid Collision, Simplify Path (`/a/./b/../../c` → `/c`): classic stack simulations.

---

## C. Monotonic stack

**Intuition:** keep the stack increasing (or decreasing). When a new element breaks the order, everything it pops has just found its **next greater (or smaller)** element. Each index is pushed and popped once, so O(n).

**Template (next greater element to the right):**

```python
def next_greater(nums):
    res = [-1] * len(nums)
    st = []                       # indices, values decreasing
    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            res[st.pop()] = x
        st.append(i)
    return res
```

### C1. Daily Temperatures
Same template: `res[j] = i - j`.

### C2. Largest Rectangle in Histogram (hard, very common)
**Intuition:** for each bar, the widest rectangle using its height extends to the first shorter bar on each side. With an increasing stack, when bar i is shorter than the top, the top's right boundary is i and its left boundary is the new top after popping.

```python
def largest_rectangle(heights):
    st = []                  # indices, heights increasing
    best = 0
    for i, h in enumerate(heights + [0]):     # sentinel flushes the stack
        while st and heights[st[-1]] > h:
            height = heights[st.pop()]
            left = st[-1] if st else -1
            best = max(best, height * (i - left - 1))
        st.append(i)
    return best
```
O(n). Extension: Maximal Rectangle in a binary matrix is this per row, over accumulated column heights.

### C3. Car Fleet
Sort by position descending. Compute time to reach the target. A car forms a new fleet only if its time is greater than the fleet ahead of it.

### C4. Sum of Subarray Minimums, Stock Span, Remove K Digits
Remove K Digits: pop while the top is greater than the current digit and k > 0, which makes the smallest number greedily.

---

## D. Queue and deque

**Queue:** FIFO, used for BFS, producer/consumer, and task scheduling. In Python use `collections.deque`.

### D1. Sliding Window Maximum (monotonic deque)
**Intuition:** keep a deque of indices with decreasing values. The front is the max. Pop the front when it leaves the window, and pop the back while it's smaller than the new element (it can never be a max again).

```python
def max_sliding_window(nums, k):
    dq, res = deque(), []
    for i, x in enumerate(nums):
        if dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] < x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res
```
O(n). Related: Shortest Subarray with Sum at Least K (prefix sums + monotonic deque, handles negatives).

### D2. Implement a Queue using two stacks
`in` stack for push, `out` stack for pop. Refill `out` only when it's empty. Amortized O(1).

### D3. Design Circular Queue
A fixed array with `head` and `count`. `tail = (head + count) % cap`. This is also the core of a bounded ring buffer (see [concurrency](06_concurrency.md)).

### D4. Design Hit Counter (hits in the last 300s)
A deque of timestamps, popping old ones from the left. Or, for high volume, 300 buckets of `(timestamp, count)` indexed by `ts % 300`, which is O(1) memory per second. That's a rate limiter warmup.

---

## E. Heap / priority queue

**Intuition:** always need the min or max of a changing set. Push/pop O(log n), peek O(1). **Top K largest:** keep a *min*-heap of size k (the smallest of the top k is on top, and you evict it).

### E1. Kth Largest Element in an Array
Min-heap of size k: O(n log k). Quickselect: O(n) average, O(n²) worst.

```python
def find_kth_largest(nums, k):
    h = nums[:k]
    heapq.heapify(h)
    for x in nums[k:]:
        if x > h[0]:
            heapq.heapreplace(h, x)
    return h[0]
```

### E2. K Closest Points to Origin
Max-heap of size k on distance (push the negative distance). O(n log k).

### E3. Merge K Sorted Lists (also "merge k sorted log files")

```python
def merge_k_lists(lists):
    h = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(h, (node.val, i, node))
    dummy = tail = ListNode()
    while h:
        _, i, node = heapq.heappop(h)
        tail.next = tail = node
        if node.next:
            heapq.heappush(h, (node.next.val, i, node.next))
    return dummy.next
```
O(N log k). The index `i` breaks ties because nodes aren't comparable. At scale this is **external merge sort**: sort chunks that fit in memory, write them, then k-way merge with a heap and buffered IO.

### E4. Find Median from Data Stream (two heaps)
**Intuition:** a max-heap for the lower half and a min-heap for the upper half. Keep sizes balanced (lower can have one extra).

```python
class MedianFinder:
    def __init__(self):
        self.lo = []   # max-heap (negated)
        self.hi = []   # min-heap

    def add_num(self, x):
        heapq.heappush(self.lo, -x)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def find_median(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2
```
add O(log n), median O(1). Follow-ups: sliding-window median (lazy deletion with a hashmap of to-delete counts). For p99 latency at scale use histograms or t-digest, not exact medians.

### E5. Task Scheduler (cooldown n)
**Math answer:** `max(len(tasks), (maxFreq - 1) * (n + 1) + countOfMaxFreq)`. The simulation uses a max-heap plus a cooldown queue.

### E6. Reorganize String (no two adjacent the same)
Max-heap by count. Pop the top, append it, and hold it back one step (push the previous one back).

### E7. Meeting Rooms II: see [intervals](03_dsa_6_backtracking_greedy_intervals_matrix_bits.md) (min-heap of end times).

### E8. Dijkstra and Prim use heaps: see [graphs](03_dsa_4_graphs_dsu.md).

### E9. Design Twitter (news feed of top 10)
Per-user tweet lists with timestamps. The feed is a k-way merge over the user and their followees with a heap, taking 10. That's the same idea as fan-out-on-read in system design.

---

## Heap facts to say out loud

- `heapify` is O(n), not O(n log n).
- Python has only a min-heap. Negate for max, or push `(-priority, ...)`.
- There's no decrease-key in heapq. Push a new entry and skip stale ones on pop (lazy deletion). Dijkstra does exactly this.
