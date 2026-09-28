# 03.5 Dynamic programming: all families

---

## A. How to solve any DP problem (say these steps out loud)

1. **Is it DP?** You're asked for a count, min/max, or yes/no over choices, and brute-force recursion recomputes the same subproblems.
2. **Define the state:** `dp[i]` = the answer for the prefix up to i / the suffix from i / a range i..j / with capacity w / with mask m. Say it in English: "`dp[i]` is the minimum coins to make amount i."
3. **Transition:** how does `dp[i]` come from smaller states? Enumerate the **last choice**.
4. **Base cases.**
5. **Order:** compute smaller states before larger ones (bottom-up), or use memoized recursion (top-down).
6. **Answer location:** `dp[n]`, `max(dp)`, `dp[0][n-1]`...
7. **Optimize space** if each row only depends on the previous row.

**Top-down first** in an interview (fast to get right), then offer bottom-up and space optimization.

```python
from functools import cache

def solve(nums):
    @cache
    def f(i):
        if i >= len(nums):
            return 0
        return max(f(i + 1), nums[i] + f(i + 2))
    return f(0)
```

Complexity = (number of states) × (work per state).

---

## B. 1D linear DP

### B1. Climbing Stairs / Fibonacci
`dp[i] = dp[i-1] + dp[i-2]`. O(n) time, O(1) space.

### B2. House Robber I and II

```python
def rob(nums):
    take = skip = 0
    for x in nums:
        take, skip = skip + x, max(take, skip)
    return max(take, skip)

def rob_circular(nums):
    if len(nums) == 1:
        return nums[0]
    return max(rob(nums[1:]), rob(nums[:-1]))    # can't take both first and last
```

### B3. Decode Ways (`"226"` → 3)
`dp[i]` = number of ways to decode `s[:i]`. Add `dp[i-1]` if `s[i-1] != '0'`, and add `dp[i-2]` if `10 ≤ int(s[i-2:i]) ≤ 26`.

```python
def num_decodings(s):
    prev2, prev1 = 1, 0 if s[0] == "0" else 1
    for i in range(2, len(s) + 1):
        cur = 0
        if s[i - 1] != "0":
            cur += prev1
        if 10 <= int(s[i - 2:i]) <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1
```

### B4. Coin Change (min coins, unbounded)
`dp[a] = min(dp[a - c] + 1)` over coins c.

```python
def coin_change(coins, amount):
    dp = [0] + [float("inf")] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return -1 if dp[amount] == float("inf") else dp[amount]
```
O(amount × coins). **Greedy fails** in general (coins [1, 3, 4], amount 6: greedy gives 4+1+1, optimal is 3+3).

### B5. Word Break
`dp[i]` is true if some `j < i` has `dp[j]` true and `s[j:i]` in the dictionary. Limit j by the max word length.

```python
def word_break(s, words):
    ws, maxlen = set(words), max(map(len, words), default=0)
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(max(0, i - maxlen), i):
            if dp[j] and s[j:i] in ws:
                dp[i] = True
                break
    return dp[-1]
```

### B6. Longest Increasing Subsequence
O(n²) DP: `dp[i] = 1 + max(dp[j] for j < i if a[j] < a[i])`.
O(n log n) with **patience sorting**: `tails[k]` = the smallest tail of an increasing subsequence of length k+1. Binary search the insert position.

```python
def length_of_lis(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```
Variants: Russian Doll Envelopes (sort by width ascending and height descending, then LIS on height), Number of LIS, Longest Chain.

### B7. Maximum Product Subarray
Track `hi` and `lo` (a negative number swaps them).

### B8. Jump Game II / Min cost climbing stairs / Perfect Squares (unbounded knapsack over squares).

---

## C. 2D grid DP

### C1. Unique Paths (with obstacles)
`dp[r][c] = dp[r-1][c] + dp[r][c-1]` (0 on obstacles). Use one row of space.

```python
def unique_paths_obstacles(grid):
    C = len(grid[0])
    dp = [0] * C
    dp[0] = 1
    for row in grid:
        for c in range(C):
            if row[c] == 1:
                dp[c] = 0
            elif c:
                dp[c] += dp[c - 1]
    return dp[-1]
```

### C2. Minimum Path Sum, Triangle (bottom-up from the last row), Maximal Square

Maximal Square: `dp[r][c] = 1 + min(top, left, top-left)` when the cell is '1'. The answer is `max² `.

### C3. Dungeon Game (hard)
Go **backwards** from the princess: `need[r][c] = max(1, min(need[r+1][c], need[r][c+1]) - dungeon[r][c])`.

---

## D. Two sequences (strings)

State `dp[i][j]` = answer for `a[:i]` and `b[:j]`.

### D1. Longest Common Subsequence

```python
def lcs(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]
```
O(mn). This is the core of `diff` tools (tie-in: config diffs, change review).

### D2. Edit Distance (Levenshtein)
Operations: insert `dp[i][j-1]`, delete `dp[i-1][j]`, replace `dp[i-1][j-1]`, each +1. Equal chars cost 0.

```python
def min_distance(a, b):
    m, n = len(a), len(b)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        cur = [i] + [0] * n
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
        prev = cur
    return prev[n]
```
O(mn) time, O(n) space.

### D3. Interleaving String, Distinct Subsequences, Shortest Common Supersequence.

### D4. Regular Expression Matching (`.` and `*`, hard)

```python
def is_match(s, p):
    @cache
    def f(i, j):
        if j == len(p):
            return i == len(s)
        first = i < len(s) and p[j] in (s[i], ".")
        if j + 1 < len(p) and p[j + 1] == "*":
            return f(i, j + 2) or (first and f(i + 1, j))   # zero or more
        return first and f(i + 1, j + 1)
    return f(0, 0)
```
O(mn). Wildcard Matching (`?` and `*`) is similar.

---

## E. Knapsack family

| Type | Loop order | Example |
|---|---|---|
| **0/1** (each item once) | items outer, capacity **descending** | Partition Equal Subset Sum, Target Sum, Last Stone Weight II |
| **Unbounded** (reuse items) | capacity **ascending** | Coin Change, Coin Change II, Perfect Squares |
| **Count combinations** | items outer, capacity inner | Coin Change II |
| **Count permutations** (order matters) | capacity outer, items inner | Combination Sum IV |

### E1. Partition Equal Subset Sum (0/1, boolean)

```python
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [True] + [False] * target
    for x in nums:
        for t in range(target, x - 1, -1):      # descending: each x used once
            dp[t] = dp[t] or dp[t - x]
    return dp[target]
```
O(n · target). A bitset trick: `bits |= bits << x`.

### E2. Target Sum (+/- each number)
Reduce to a subset sum: `P - N = target`, `P + N = total`, so `P = (target + total) / 2`. Count subsets with that sum.

### E3. Coin Change II (number of combinations)

```python
def change(amount, coins):
    dp = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]
```

---

## F. Interval DP (range i..j)

State `dp[i][j]` over a range. Iterate by **length** so smaller ranges come first.

### F1. Longest Palindromic Substring (expand from center is simpler)

```python
def longest_palindrome(s):
    best = ""
    for center in range(2 * len(s) - 1):
        l, r = center // 2, center // 2 + center % 2
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        if r - l - 1 > len(best):
            best = s[l + 1:r]
    return best
```
O(n²), O(1) space. Palindromic Substrings (count) uses the same loop.

### F2. Longest Palindromic Subsequence
`dp[i][j] = dp[i+1][j-1] + 2` if `s[i] == s[j]`, else `max(dp[i+1][j], dp[i][j-1])`. Equals LCS(s, reversed s).

### F3. Burst Balloons (hard, "last one to burst")
**Intuition:** pick k as the **last** balloon burst in (i, j). Its neighbors at that moment are i and j.

```python
def max_coins(nums):
    a = [1] + nums + [1]
    n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):
                dp[i][j] = max(dp[i][j], a[i] * a[k] * a[j] + dp[i][k] + dp[k][j])
    return dp[0][n - 1]
```
O(n³). Same family: Matrix Chain Multiplication, Minimum Cost to Cut a Stick, Palindrome Partitioning II.

---

## G. State machine DP (stocks)

### G1. Best Time to Buy/Sell with Cooldown
States: `hold`, `sold` (just sold, cooldown), `rest`.

```python
def max_profit_cooldown(prices):
    hold, sold, rest = float("-inf"), 0, 0
    for p in prices:
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return max(sold, rest)
```

### G2. With a transaction fee / at most k transactions
k transactions: `buy[j] = max(buy[j], sell[j-1] - p)` and `sell[j] = max(sell[j], buy[j] + p)`. O(n·k).

---

## H. Tree DP

Return a tuple of states from children. **House Robber III:** each node returns `(rob_this, skip_this)`.

```python
def rob_tree(root):
    def dfs(n):
        if not n:
            return (0, 0)
        l, r = dfs(n.left), dfs(n.right)
        return (n.val + l[1] + r[1], max(l) + max(r))
    return max(dfs(root))
```
Binary Tree Cameras and Max Path Sum are also tree DP.

---

## I. Bitmask DP (n ≤ 20)

State includes a bitmask of used items. Examples: TSP, Shortest Path Visiting All Nodes (BFS over `(node, mask)`), Partition to K Equal Sum Subsets, Minimum number of work sessions.

```python
def shortest_path_length(graph):
    n = len(graph)
    full = (1 << n) - 1
    q = deque((i, 1 << i, 0) for i in range(n))
    seen = {(i, 1 << i) for i in range(n)}
    while q:
        u, mask, d = q.popleft()
        if mask == full:
            return d
        for v in graph[u]:
            nm = mask | (1 << v)
            if (v, nm) not in seen:
                seen.add((v, nm))
                q.append((v, nm, d + 1))
```
O(2^n · n²).

---

## J. Digit DP and DP on strings with counting (awareness)

Count numbers ≤ N with a property: the state is `(position, tight, other)`. Examples: Numbers At Most N Given Digit Set, Count of digit one.

---

## K. DP interview tips

- If stuck, write the brute-force recursion, then add `@cache`. That's already DP.
- Name the state in words before writing code.
- Check the loop order for knapsack (ascending vs descending).
- Mention space optimization even if you don't code it.
- Where DP shows up in real systems: edit distance (diffs, fuzzy matching), knapsack (bin packing and VM placement heuristics), LIS (version ordering), and interval DP (query plan join ordering is DP in database optimizers).
