# 03.6 Backtracking, greedy, intervals, matrix, bit manipulation, math

---

## A. Backtracking

**Intuition:** build candidates step by step. At each step choose, recurse, then **un-choose**. Prune as early as possible. Complexity is usually exponential: say it (O(2^n) subsets, O(n!) permutations).

**Template:**

```python
def backtrack(path, choices):
    if is_solution(path):
        res.append(path[:])          # copy!
        return
    for c in choices:
        if not valid(c, path):
            continue
        path.append(c)
        backtrack(path, next_choices)
        path.pop()
```

### A1. Subsets (and Subsets II with duplicates)

```python
def subsets_with_dup(nums):
    nums.sort()
    res, path = [], []
    def bt(start):
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue                     # skip duplicate at the same depth
            path.append(nums[i])
            bt(i + 1)
            path.pop()
    bt(0)
    return res
```
O(n · 2^n).

### A2. Permutations

```python
def permute(nums):
    res, path, used = [], [], [False] * len(nums)
    def bt():
        if len(path) == len(nums):
            res.append(path[:]); return
        for i, x in enumerate(nums):
            if not used[i]:
                used[i] = True; path.append(x)
                bt()
                path.pop(); used[i] = False
    bt()
    return res
```
O(n · n!). Permutations II: sort, and skip `nums[i] == nums[i-1] and not used[i-1]`.

### A3. Combination Sum (reuse allowed)

```python
def combination_sum(cands, target):
    cands.sort()
    res, path = [], []
    def bt(start, remain):
        if remain == 0:
            res.append(path[:]); return
        for i in range(start, len(cands)):
            if cands[i] > remain:
                break                        # sorted, so prune
            path.append(cands[i])
            bt(i, remain - cands[i])         # i, not i + 1: reuse allowed
            path.pop()
    bt(0, target)
    return res
```

### A4. Word Search (grid backtracking)
Mark the cell as visited (`board[r][c] = '#'`), recurse in 4 directions, then restore it. O(R·C·4^L).

### A5. N-Queens
Track the sets `cols`, `diag1 = r - c`, and `diag2 = r + c`. Place row by row. O(n!).

```python
def solve_n_queens(n):
    res, cols, d1, d2 = [], set(), set(), set()
    board = [["."] * n for _ in range(n)]
    def bt(r):
        if r == n:
            res.append(["".join(row) for row in board]); return
        for c in range(n):
            if c in cols or r - c in d1 or r + c in d2:
                continue
            cols.add(c); d1.add(r - c); d2.add(r + c); board[r][c] = "Q"
            bt(r + 1)
            cols.remove(c); d1.remove(r - c); d2.remove(r + c); board[r][c] = "."
    bt(0)
    return res
```

### A6. Palindrome Partitioning, Letter Combinations of a Phone Number, Generate Parentheses (track open/close counts), Sudoku Solver.

---

## B. Greedy

**Intuition:** take the locally best choice. **Only correct if you can argue it**: the exchange argument ("swapping any optimal solution's choice for the greedy one doesn't make it worse") or "greedy stays ahead." If you can't argue it, it's probably DP.

### B1. Jump Game I and II

```python
def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True

def jump(nums):                       # min jumps, BFS by layers
    jumps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            end = far
    return jumps
```

### B2. Gas Station
If total gas < total cost, the answer is -1. Otherwise, reset the start whenever the running tank goes negative.

```python
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    tank = start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start, tank = i + 1, 0
    return start
```

### B3. Partition Labels
Record the last index of each char. Extend the current partition's end to the max last-index seen, and cut when `i == end`.

### B4. Hand of Straights, Task Scheduler (math greedy), Minimum Number of Arrows (sort by end), Boats to Save People (two pointers).

---

## C. Intervals

**Intuition:** sort by start (or by end for "max non-overlapping"). Then sweep.

### C1. Merge Intervals

```python
def merge(intervals):
    intervals.sort()
    out = [intervals[0]]
    for s, e in intervals[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
```
O(n log n).

### C2. Insert Interval
Add everything that ends before the new one, merge the overlaps, then add the rest. O(n).

### C3. Non-overlapping Intervals (min removals)
**Greedy:** sort by **end**, and keep the interval that ends earliest. That's classic activity selection.

```python
def erase_overlap_intervals(intervals):
    intervals.sort(key=lambda x: x[1])
    end, removed = float("-inf"), 0
    for s, e in intervals:
        if s >= end:
            end = e
        else:
            removed += 1
    return removed
```

### C4. Meeting Rooms II (min rooms, OCI-relevant: resource allocation)
**Heap:** sort by start. A min-heap of end times. If the earliest end ≤ the current start, reuse that room.

```python
def min_meeting_rooms(intervals):
    intervals.sort()
    ends = []
    for s, e in intervals:
        if ends and ends[0] <= s:
            heapq.heapreplace(ends, e)
        else:
            heapq.heappush(ends, e)
    return len(ends)
```
**Sweep alternative:** +1 at each start, -1 at each end, sorted. The max running sum is the answer. That's the same idea as "max concurrent connections" from logs.

### C5. Employee Free Time, Interval List Intersections (two pointers), My Calendar I/II (sorted list or segment tree), Car Pooling (difference array).

---

## D. Matrix

### D1. Rotate Image 90° clockwise in place
Transpose, then reverse each row.

```python
def rotate(m):
    n = len(m)
    for i in range(n):
        for j in range(i + 1, n):
            m[i][j], m[j][i] = m[j][i], m[i][j]
    for row in m:
        row.reverse()
```

### D2. Spiral Matrix
Shrink four boundaries: top, bottom, left, right.

```python
def spiral_order(m):
    res = []
    top, bot, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
    while top <= bot and left <= right:
        for c in range(left, right + 1): res.append(m[top][c])
        top += 1
        for r in range(top, bot + 1): res.append(m[r][right])
        right -= 1
        if top <= bot:
            for c in range(right, left - 1, -1): res.append(m[bot][c])
            bot -= 1
        if left <= right:
            for r in range(bot, top - 1, -1): res.append(m[r][left])
            left += 1
    return res
```

### D3. Set Matrix Zeroes (O(1) space)
Use the first row and first column as markers, with a separate flag for the first column.

### D4. Search a 2D Matrix
- Fully sorted (each row starts after the previous ends): binary search as a 1D array, `r, c = divmod(mid, C)`.
- Rows and columns sorted separately (II): start at the top-right. Go left if too big, down if too small. O(R + C).

### D5. Valid Sudoku
Sets per row, column, and box, where `box = (r // 3) * 3 + c // 3`.

### D6. Game of Life (in place)
Encode the next state in extra bits: `2` = alive to dead, `3` = dead to alive, or use bit 1 for the next state.

### D7. Grid BFS/DFS problems (islands, rotting oranges, shortest path in a binary matrix): see [graphs](03_dsa_4_graphs_dsu.md).

---

## E. Bit manipulation

| Trick | Code |
|---|---|
| Check bit i | `(x >> i) & 1` |
| Set / clear / toggle | `x | (1<<i)`, `x & ~(1<<i)`, `x ^ (1<<i)` |
| Lowest set bit | `x & -x` |
| Clear lowest set bit | `x & (x - 1)` |
| Power of two | `x > 0 and x & (x - 1) == 0` |
| Count bits | `bin(x).count("1")` or `x.bit_count()` |
| XOR facts | `a ^ a = 0`, `a ^ 0 = a`, commutative |

### E1. Single Number (every other number appears twice)
XOR everything. O(n), O(1).

### E2. Single Number II (others appear three times)
Count each bit mod 3, or use the `ones/twos` state machine.

### E3. Counting Bits
`dp[i] = dp[i >> 1] + (i & 1)`.

### E4. Missing Number
`XOR of 0..n` XOR `XOR of nums`, or `n(n+1)/2 - sum`.

### E5. Sum of Two Integers without + (Python needs a 32-bit mask)

```python
def get_sum(a, b):
    mask = 0xFFFFFFFF
    while b & mask:
        a, b = a ^ b, (a & b) << 1
    return a & mask if b > 0 else a
```

### E6. Subsets via bitmask
`for m in range(1 << n): [nums[i] for i in range(n) if m >> i & 1]`.

Systems tie-in: bitmaps and Bloom filters (ClickHouse bloom skip indexes, which I used on product/store/attr), permission bitmasks, and consistent-hash ring positions.

---

## F. Math essentials

- GCD: `math.gcd`. LCM = `a * b // gcd`.
- Sieve of Eratosthenes for primes ≤ n: O(n log log n).
- Fast power: `pow(a, b, mod)`.
- Modular arithmetic: `(a + b) % m`. In Python, integers don't overflow; in Go they do.
- Reservoir sampling (pick k from a stream of unknown length): keep item i with probability k/i. Good for "sample logs uniformly."
- Random pick with weight: prefix sums + binary search.
- Pow(x, n), Sqrt(x) by binary search, Happy Number (cycle detection), Plus One, Multiply Strings.

```python
def reservoir_sample(stream, k):
    res = []
    for i, x in enumerate(stream, 1):
        if i <= k:
            res.append(x)
        else:
            j = random.randint(1, i)
            if j <= k:
                res[j - 1] = x
    return res
```
