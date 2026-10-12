# 03.5 Dynamic programming: all families

<div class="callout note">
<b>How to use this page</b>
<ul>
<li><b>What it covers:</b> a seven-step recipe that works on any DP problem, then each family in turn: 1D, grid, two strings, knapsack, interval, state machine, tree, bitmask and digit DP.</li>
<li><b>When to read it:</b> after the arrays and graphs files. DP is where people freeze, so practise saying the recipe out loud before you write code.</li>
<li><b>What to memorise:</b> the recipe in section A, the knapsack loop-order table in section E, and the sentence "the state is ..., the transition is ..., the base case is ...".</li>
<li><b>How each problem is laid out:</b> a one-line restatement, the key insight (usually the state definition), a dry run as a small table, code, complexity, and a 60-second spoken version.</li>
</ul>
</div>

Imports assumed by every snippet on this page:

```python
from collections import deque
from functools import cache
import bisect
```

---

## Words you need

- **Dynamic programming (DP):** solving a problem by combining answers to smaller versions of the same problem, and storing each smaller answer so it's computed only once.
- **Subproblem:** a smaller version of the problem, like "the best answer for the first i houses".
- **Overlapping subproblems:** plain recursion would solve the same subproblem many times. That repetition is what DP removes.
- **State:** the few numbers that identify a subproblem, like `i`, or `(i, j)`, or `(i, capacity)`.
- **Transition (recurrence):** the formula for a state's answer in terms of smaller states.
- **Memoization (top-down):** write the recursion and cache results. Python's `@cache` does it in one line.
- **Tabulation (bottom-up):** fill an array from the smallest states upward with loops.

**Analogy:** working out 1 + 1 + 1 + 1 + 1 = 5 on paper. If someone adds "+ 1" at the end, you don't recount from scratch, you say "6", because you remembered 5. DP is that habit applied systematically.

---

## A. How to solve any DP problem (say these steps out loud)

### The recipe

1. **Is it DP?** You're asked for a count, min/max, or yes/no over choices, and brute-force recursion recomputes the same subproblems.
2. **Define the state:** `dp[i]` = the answer for the prefix up to i / the suffix from i / a range i..j / with capacity w / with mask m. Say it in English: "`dp[i]` is the minimum coins to make amount i."
3. **Transition:** how does `dp[i]` come from smaller states? Enumerate the **last choice** (what was the last coin, the last step, the last character matched?).
4. **Base cases.** The smallest states whose answers are obvious (amount 0 needs 0 coins).
5. **Order:** compute smaller states before larger ones (bottom-up), or use memoized recursion (top-down).
6. **Answer location:** `dp[n]`, `max(dp)`, `dp[0][n-1]`...
7. **Optimize space** if each row only depends on the previous row.

**Top-down first** in an interview (fast to get right), then offer bottom-up and space optimization.

### When to recognise DP (signals)

- "Number of ways to...", "minimum cost", "maximum profit", "longest", "can you reach / is it possible".
- Choices at each step (take or skip, which coin, which direction) where a greedy choice can fail.
- Constraints around 10² to 10⁴ for 2D DP, or up to 10⁵ to 10⁶ for 1D DP.
- You can describe the answer for size n in terms of answers for smaller sizes.

### Hand-traced example (the template below)

The template is House Robber: you can't rob two adjacent houses, so `f(i) = max(skip house i, rob house i and jump to i + 2)`. On `[2, 7, 9, 3, 1]`, compute from the right:

```text
i   nums[i]  f(i+1)  nums[i] + f(i+2)  f(i)
4   1        0       1 + 0 = 1         1
3   3        1       3 + 0 = 3         3
2   9        3       9 + 1 = 10        10
1   7        10      7 + 3 = 10        10
0   2        10      2 + 10 = 12       12
answer 12 (houses 0, 2, 4)
```

Without `@cache`, `f(2)` would be computed from both `f(0)` and `f(1)`, and the call tree doubles at every level, which is O(2^n). With the cache each `f(i)` runs once.

### Template

```python
def solve(nums):
    @cache
    def f(i):
        if i >= len(nums):
            return 0
        return max(f(i + 1), nums[i] + f(i + 2))
    return f(0)
```

**Complexity = (number of states) × (work per state).** Here n states and O(1) work each, so O(n).

### Common mistakes

- Starting to code before you can say the state in one English sentence.
- Missing a base case, or an off-by-one between "first i items" and "index i".
- Wrong loop order in bottom-up, so a state is read before it's computed.
- Putting `@cache` on a function that takes a list argument (lists aren't hashable). Pass indices instead.

---

## B. 1D linear DP

The state is a single index, usually "the best answer considering the first i elements" or "starting from i".

### B1. Climbing Stairs / Fibonacci

**Problem in one sentence:** how many ways can you climb n stairs taking 1 or 2 steps at a time?

**Key insight:** your last move was either a 1-step (from stair n-1) or a 2-step (from stair n-2). So `dp[i] = dp[i-1] + dp[i-2]`, which is the Fibonacci sequence. You only need the previous two values.

**Dry run** for n = 4:

```text
i      1  2  3  4
dp[i]  1  2  3  5
```

```python
def climb_stairs(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
```

**Complexity:** O(n) time, O(1) space.

**Say it in 60 seconds:** "The last step onto stair n came from n minus 1 or n minus 2, so the number of ways is the sum of those two, which is Fibonacci. I only need the previous two values, so I keep two variables and roll them forward. O(n) time, O(1) space. If n were huge, matrix exponentiation gives O(log n)."

---

### B2. House Robber I and II

**Problem in one sentence:** maximise money stolen from a row of houses without robbing two neighbours. Version II puts the houses in a circle.

**Key insight:** at each house you either rob it (and must have skipped the previous one) or skip it (and keep the best so far). Two running values are enough: `take` (best if I rob this house) and `skip` (best if I don't). For the circle, the first and last houses can't both be robbed, so solve two straight-line problems: without the first house, and without the last.

**Dry run** on `[2, 7, 9, 3, 1]`:

```text
x   take = skip + x   skip = max(old take, old skip)
2   2                 0
7   7                 2
9   11                7
3   10                11
1   12                11
answer max(12, 11) = 12
```

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

**Complexity:** O(n) time, O(1) space (the slices in `rob_circular` cost O(n) memory, which you can avoid with index bounds).

**Say it in 60 seconds:** "At each house I track two numbers: the best total if I rob this house, and the best if I skip it. Robbing it means I skipped the previous one, so take is the old skip plus this value. Skipping means I keep the better of the previous two. The answer is the larger at the end. For the circular version, the first and last houses conflict, so I run the linear version twice, once excluding the first house and once excluding the last, and take the max. O(n) time, O(1) space."

---

### B3. Decode Ways (`"226"` → 3)

**Problem in one sentence:** letters map to numbers 1 to 26. How many ways can a digit string be decoded?

**Key insight:** `dp[i]` = number of ways to decode `s[:i]`. The last letter used either one digit or two. Add `dp[i-1]` if `s[i-1] != '0'` (a single non-zero digit is a letter), and add `dp[i-2]` if `10 ≤ int(s[i-2:i]) ≤ 26` (a valid two-digit letter).

**Dry run** on `"226"`:

```text
i  last digit ok?   last two digits ok?   dp[i]
0                                         1 (empty string)
1  "2" yes                                1
2  "2" yes: +dp[1]  "22" yes: +dp[0]      1 + 1 = 2
3  "6" yes: +dp[2]  "26" yes: +dp[1]      2 + 1 = 3
answer 3: "2 2 6", "22 6", "2 26"
```

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

The first line reads as `prev2, prev1 = 1, (0 if s[0] == "0" else 1)`. A leading zero can't be decoded. "06" is not a valid two-digit code, which the `10 <=` check handles.

**Complexity:** O(n) time, O(1) space.

**Say it in 60 seconds:** "The number of ways to decode the first i digits depends on how the last letter was formed. If the last digit isn't zero, it can be a letter on its own, so I add the ways for i minus 1. If the last two digits form a number from 10 to 26, they can be one letter, so I add the ways for i minus 2. It's Fibonacci with conditions. I keep two rolling variables. Zeros are the edge case: a zero can only appear as the second digit of 10 or 20."

---

### B4. Coin Change (min coins, unbounded)

**Problem in one sentence:** using unlimited coins of given denominations, make an amount with as few coins as possible, or return -1.

**Key insight:** the last coin used was some coin c, so `dp[a] = min(dp[a - c] + 1)` over coins c. **Greedy fails** in general (coins [1, 3, 4], amount 6: greedy gives 4+1+1, optimal is 3+3), which is why we need DP.

**Dry run** on coins `[1, 3, 4]`, amount 6:

```text
a      0  1  2  3  4  5  6
dp[a]  0  1  2  1  1  2  2
dp[6] = min(dp[5]+1, dp[3]+1, dp[2]+1) = min(3, 2, 3) = 2  (3 + 3)
```

```python
def coin_change(coins, amount):
    dp = [0] + [float("inf")] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return -1 if dp[amount] == float("inf") else dp[amount]
```

**Complexity:** O(amount × coins) time, O(amount) space.

**Say it in 60 seconds:** "Greedy fails, for example with coins 1, 3 and 4 and amount 6, so I use DP. `dp[a]` is the fewest coins to make amount a. Whatever the optimal solution is, it has a last coin c, and the rest makes `a - c` optimally, so `dp[a]` is the minimum over coins of `dp[a - c] + 1`. Base case `dp[0] = 0`, everything else starts at infinity, which also marks unreachable amounts. O(amount × number of coins)."

---

### B5. Word Break

**Problem in one sentence:** can a string be split into a sequence of dictionary words?

**Key insight:** `dp[i]` is true if some `j < i` has `dp[j]` true and `s[j:i]` in the dictionary. In words: the first i characters are breakable if some earlier breakable prefix is followed by a dictionary word ending at i. Limit j by the max word length so you don't check impossible splits.

**Dry run** on `s = "leetcode"`, words `["leet", "code"]`:

```text
i      0  1  2  3  4  5  6  7  8
dp[i]  T  F  F  F  T  F  F  F  T
dp[4]: dp[0] and "leet" in words
dp[8]: dp[4] and "code" in words -> True
```

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

**Complexity:** O(n · maxlen · maxlen) time: n end positions, maxlen start positions, and O(maxlen) to slice and hash each substring. O(n) space.

**Say it in 60 seconds:** "`dp[i]` says whether the first i characters can be segmented. The empty prefix can, so `dp[0]` is true. For each i, I look back at split points j within the longest word length. If `dp[j]` is true and the substring from j to i is a word, then `dp[i]` is true. I break as soon as I find one. The answer is the last entry. Limiting j by the max word length keeps it fast."

---

### B6. Longest Increasing Subsequence

**Problem in one sentence:** find the length of the longest strictly increasing subsequence (not necessarily contiguous).

**Key insight (O(n²)):** `dp[i] = 1 + max(dp[j] for j < i if a[j] < a[i])`, the longest increasing subsequence ending at i.

**Key insight (O(n log n)), patience sorting:** `tails[k]` = the smallest tail of an increasing subsequence of length k+1. Keeping tails as small as possible leaves the most room to extend. `tails` is always sorted, so binary search the insert position: replace the first tail ≥ x, or append if x is bigger than all.

**Analogy:** dealing cards into piles where each card goes on the leftmost pile whose top card is at least as big. The number of piles is the LIS length.

**Dry run** on `[10, 9, 2, 5, 3, 7, 101, 18]`:

```text
x    tails after
10   [10]
9    [9]          replace 10
2    [2]          replace 9
5    [2, 5]       append
3    [2, 3]       replace 5
7    [2, 3, 7]    append
101  [2, 3, 7, 101]
18   [2, 3, 7, 18] replace 101
answer len = 4
```

`tails` is not itself a valid subsequence in general, only its length is the answer.

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

**Complexity:** O(n log n) time, O(n) space.

**Variants:** Russian Doll Envelopes (sort by width ascending and height descending, then LIS on height; the descending tie-break stops two envelopes of equal width from nesting), Number of LIS, Longest Chain.

**Say it in 60 seconds:** "The quadratic DP is: the LIS ending at i is one more than the best LIS ending at an earlier smaller element. To get n log n, I keep an array where position k holds the smallest possible tail of an increasing subsequence of length k plus 1. That array is sorted. For each number I binary search the first tail that's at least as big and replace it, or append if the number is bigger than every tail. The length of the array is the answer. `bisect_left` gives strictly increasing; `bisect_right` would allow equal values."

---

### B7. Maximum Product Subarray

**Problem in one sentence:** find the contiguous subarray with the largest product.

**Key insight:** a negative number turns the smallest (most negative) product into the largest. So track `hi` and `lo` (a negative number swaps them): the largest and smallest product of a subarray ending here. Each new value can start fresh, extend `hi`, or extend `lo`.

**Dry run** on `[-2, 3, -4]`:

```text
x    candidates (x, hi*x, lo*x)   hi   lo    best
-2   start                        -2   -2    -2
3    (3, -6, -6)                  3    -6    3
-4   (-4, -12, 24)                24   -12   24
answer 24
```

```python
def max_product(nums):
    hi = lo = best = nums[0]
    for x in nums[1:]:
        cands = (x, hi * x, lo * x)
        hi, lo = max(cands), min(cands)
        best = max(best, hi)
    return best
```

**Complexity:** O(n) time, O(1) space.

**Say it in 60 seconds:** "It's like Kadane's algorithm, but a negative number flips signs, so the smallest product so far could become the largest. I track both the max and min product of a subarray ending at the current position. For each number, the new max and min come from three candidates: the number alone, the old max times it, and the old min times it. I compute both from the old values before updating. The best max seen is the answer. O(n), O(1)."

---

### B8. Jump Game II / Min cost climbing stairs / Perfect Squares (unbounded knapsack over squares)

- **Jump Game II:** minimum jumps to reach the end. A greedy BFS-by-layers solution is in the [greedy file](03_dsa_6_backtracking_greedy_intervals_matrix_bits.md), section B1.
- **Min Cost Climbing Stairs:** `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`, and the answer is `min(dp[n-1], dp[n-2])`.
- **Perfect Squares:** fewest perfect squares summing to n. It's Coin Change where the coins are 1, 4, 9, 16, ...

```python
def num_squares(n):
    dp = [0] + [float("inf")] * n
    for a in range(1, n + 1):
        j = 1
        while j * j <= a:
            dp[a] = min(dp[a], dp[a - j * j] + 1)
            j += 1
    return dp[n]
```

**Dry run:** `num_squares(12)` gives 3 (4 + 4 + 4). Greedy would pick 9 first and need 9 + 1 + 1 + 1 = 4 squares.

**Complexity:** O(n√n) time, O(n) space.

**Say it in 60 seconds (Perfect Squares):** "It's coin change where the coins are the perfect squares up to n. `dp[a]` is the fewest squares summing to a, and it's one more than the best `dp[a - j²]` over every square that fits. Greedy fails, because 12 is 4 + 4 + 4, not 9 + 1 + 1 + 1. There are about √n squares per amount, so O(n√n)."

---

## C. 2D grid DP

### The idea

The state is a cell `(r, c)`, and the answer for a cell comes from the cells you could have arrived from, usually above and to the left. Because each row only needs the row above, you can keep a single 1D array and overwrite it.

**Analogy:** walking across a city grid that only lets you go right or down. The number of ways to reach a corner is the ways to reach the corner above it plus the corner to its left.

### When to recognise it

- "Grid", "move only right or down", "number of paths", "minimum path sum".
- "Largest square of 1s".
- Two strings compared character by character are also a grid (section D).

### C1. Unique Paths (with obstacles)

**Problem in one sentence:** count paths from the top-left to the bottom-right of a grid, moving only right or down, avoiding obstacle cells (1).

**Key insight:** `dp[r][c] = dp[r-1][c] + dp[r][c-1]` (0 on obstacles). Use one row of space: before updating, `dp[c]` still holds the value from the row above, and `dp[c-1]` has already been updated for this row.

**Dry run** on:

```text
0 0 0
0 1 0
0 0 0

row 0: dp = [1, 1, 1]
row 1: dp = [1, 0, 1]     middle is an obstacle
row 2: dp = [1, 1, 2]
answer 2
```

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

**Complexity:** O(R·C) time, O(C) space.

**Say it in 60 seconds:** "Every path into a cell comes from above or from the left, so the count is the sum of those two, and zero for an obstacle. I only ever need the previous row, so I keep one array. When I process cell c in a new row, `dp[c]` still holds the count from above and `dp[c - 1]` already holds the count from the left, so adding them in place is correct. O(R·C) time and O(C) space."

---

### C2. Minimum Path Sum, Triangle (bottom-up from the last row), Maximal Square

**Minimum Path Sum in one sentence:** find the smallest sum along a right/down path through a grid of costs. Same shape as unique paths with `min` instead of `+`.

```python
def min_path_sum(grid):
    R, C = len(grid), len(grid[0])
    dp = [float("inf")] * C
    dp[0] = 0
    for r in range(R):
        for c in range(C):
            left = dp[c - 1] if c else float("inf")
            dp[c] = grid[r][c] + min(dp[c], left)
    return dp[-1]
```

**Triangle in one sentence:** find the minimum path sum from the top of a number triangle to the bottom, moving to an adjacent number in the row below. Going **bottom-up** avoids edge cases: start with the last row, and each cell becomes its value plus the smaller of its two children.

```python
def minimum_total(triangle):
    dp = triangle[-1][:]
    for row in range(len(triangle) - 2, -1, -1):
        for i in range(row + 1):
            dp[i] = triangle[row][i] + min(dp[i], dp[i + 1])
    return dp[0]
```

**Maximal Square in one sentence:** find the area of the largest square containing only '1's. `dp[r][c] = 1 + min(top, left, top-left)` when the cell is '1'. The answer is `max²`. The square ending at a cell is limited by the smallest of the three squares it would extend.

**Dry run (Maximal Square):**

```text
matrix      dp (side of largest square ending here)
1 1 1       1 1 1
1 1 1       1 2 2
0 1 1       0 1 2
max side 2 -> area 4
```

```python
def maximal_square(matrix):
    R, C = len(matrix), len(matrix[0])
    dp = [[0] * (C + 1) for _ in range(R + 1)]
    best = 0
    for r in range(R):
        for c in range(C):
            if matrix[r][c] == "1":
                dp[r + 1][c + 1] = 1 + min(dp[r][c + 1], dp[r + 1][c], dp[r][c])
                best = max(best, dp[r + 1][c + 1])
    return best * best
```

**Complexity:** all three are O(R·C) time. Space is O(C) or O(R·C) as written.

**Say it in 60 seconds (Maximal Square):** "For each '1' cell, I compute the side of the largest all-ones square whose bottom-right corner is that cell. It's one more than the smallest of the squares ending above, to the left, and diagonally up-left, because the new square needs all three to be at least that big. I pad the table by one row and column to avoid bounds checks, track the largest side, and return its square. O(R·C)."

---

### C3. Dungeon Game (hard)

**Problem in one sentence:** a knight walks right or down through rooms that add or subtract health, must stay above 0, and wants to reach the princess at the bottom-right. What's the minimum starting health?

**Key insight:** going forward fails, because you'd need to know both the current health and the minimum along the way. Go **backwards** from the princess: `need[r][c]` is the minimum health required on entering `(r, c)`. `need[r][c] = max(1, min(need[r+1][c], need[r][c+1]) - dungeon[r][c])`.

**Dry run** on:

```text
dungeon            need (computed bottom-right first)
-2  -3   3          7  5  2
-5 -10   1          6 11  5
10  30  -5          1  1  6

need[2][2] = max(1, 1 - (-5)) = 6
need[0][0] = max(1, min(6, 5) - (-2)) = 7
answer 7
```

```python
def calculate_minimum_hp(dungeon):
    R, C = len(dungeon), len(dungeon[0])
    need = [[float("inf")] * (C + 1) for _ in range(R + 1)]
    need[R][C - 1] = need[R - 1][C] = 1
    for r in range(R - 1, -1, -1):
        for c in range(C - 1, -1, -1):
            need[r][c] = max(1, min(need[r + 1][c], need[r][c + 1]) - dungeon[r][c])
    return need[0][0]
```

The two cells set to 1 are virtual cells just past the princess, meaning "after the last room you need at least 1 health".

**Complexity:** O(R·C) time and space.

**Say it in 60 seconds:** "A forward DP doesn't work because the best path for health at the end isn't the same as the path that keeps health above zero along the way. Going backwards fixes that. `need[r][c]` is the minimum health on entering that room. From there I'll go to whichever neighbour needs less, so I need that amount minus this room's effect, but never less than 1. I seed the cells past the destination with 1 and fill from the bottom-right. The answer is `need[0][0]`."

---

## D. Two sequences (strings)

### The idea

State `dp[i][j]` = answer for `a[:i]` and `b[:j]` (the first i characters of a and the first j of b). The transition looks at the last characters `a[i-1]` and `b[j-1]`: if they match, you usually extend `dp[i-1][j-1]`. If not, you take the best of dropping one character from either string.

**Analogy:** lining up two versions of a document side by side, line by line, to see what stayed the same. That's exactly what `diff` does.

### When to recognise it

- Two strings, and the words "common", "edit", "transform", "match", "interleave", "subsequence".
- A pattern with wildcards matched against text.

### Common mistakes

- Mixing up "first i characters" (`a[i-1]` is the last one) with "index i".
- Forgetting the empty-string row and column, which hold the base cases.

---

### D1. Longest Common Subsequence

**Problem in one sentence:** find the length of the longest sequence of characters appearing in both strings in the same order (not necessarily contiguous).

**Key insight:** if the last characters match, they belong to the LCS: `dp[i-1][j-1] + 1`. If not, at least one of them isn't in the LCS, so take `max(dp[i-1][j], dp[i][j-1])`.

**Dry run** on `a = "abc"`, `b = "ac"`:

```text
       ""  a  c
  ""   0   0  0
  a    0   1  1
  b    0   1  1
  c    0   1  2
answer 2 ("ac")
```

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

**Complexity:** O(mn) time and space (O(min(m, n)) space with two rows). This is the core of `diff` tools (tie-in: config diffs, change review).

**Say it in 60 seconds:** "`dp[i][j]` is the LCS length of the first i characters of a and the first j of b. If the last characters match, they extend the LCS of both prefixes without them. If not, one of them can be dropped, so I take the better of dropping either. The empty prefixes give zeros. The answer is the bottom-right cell. O(m·n). It's the algorithm behind diff."

---

### D2. Edit Distance (Levenshtein)

**Problem in one sentence:** find the minimum number of single-character inserts, deletes and replacements to turn a into b.

**Key insight:** look at the last characters. If they're equal, no edit is needed: `dp[i-1][j-1]`. Otherwise, try each operation: insert `dp[i][j-1]`, delete `dp[i-1][j]`, replace `dp[i-1][j-1]`, each +1. Equal chars cost 0. Base cases: turning a prefix into the empty string takes i deletes, and the empty string into a prefix takes j inserts.

**Dry run** on `a = "horse"`, `b = "ros"`:

```text
       ""  r  o  s
  ""   0   1  2  3
  h    1   1  2  3
  o    2   2  1  2
  r    3   2  2  2
  s    4   3  3  2
  e    5   4  4  3
answer 3 (replace h->r, delete r, delete e)
```

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

**Complexity:** O(mn) time, O(n) space.

**Say it in 60 seconds:** "`dp[i][j]` is the edit distance between the first i characters of a and the first j of b. If the last characters are equal, it's the same as without them. Otherwise I pay one edit and take the cheapest of three: delete from a, which is the cell above; insert into a, the cell to the left; or replace, the diagonal. The first row and column are j and i, because you need that many inserts or deletes against an empty string. I keep two rows, so O(m·n) time and O(n) space. It's used in fuzzy matching and spell check."

---

### D3. Interleaving String, Distinct Subsequences, Shortest Common Supersequence

**Interleaving String in one sentence:** can s3 be formed by merging s1 and s2 while keeping each one's character order?

**Key insight:** `dp[i][j]` is true if the first i characters of s1 and the first j of s2 can form the first i + j characters of s3. The last character of that s3 prefix came from s1 or from s2.

**Dry run** on `s1 = "a"`, `s2 = "b"`, `s3 = "ab"`: `dp[0][0]` true. `dp[1][0]`: "a" from s1 matches s3[0], true. `dp[1][1]`: take "b" from s2, `dp[1][0]` is true and s2[0] == s3[1], so true.

```python
def is_interleave(s1, s2, s3):
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False
    dp = [False] * (n + 1)
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 and j == 0:
                dp[j] = True
            else:
                from_s1 = i > 0 and dp[j] and s1[i - 1] == s3[i + j - 1]
                from_s2 = j > 0 and dp[j - 1] and s2[j - 1] == s3[i + j - 1]
                dp[j] = from_s1 or from_s2
    return dp[n]
```

In the 1D array, `dp[j]` before the update is the row above (`i - 1, j`) and `dp[j - 1]` is already this row (`i, j - 1`).

**The other two, one line each:**
- **Distinct Subsequences:** count the ways b appears as a subsequence of a. `dp[i][j] = dp[i-1][j] + (dp[i-1][j-1] if a[i-1] == b[j-1] else 0)`: either skip a's last character, or use it to match b's last.
- **Shortest Common Supersequence:** the shortest string containing both as subsequences has length `m + n - LCS(a, b)`, because the common part only needs to be written once. To build it, walk the LCS table backwards.

**Complexity:** all O(mn).

**Say it in 60 seconds (Interleaving):** "First, lengths must add up. Then `dp[i][j]` asks whether i characters of s1 and j of s2 can form the first i plus j of s3. The last character came from either s1, if it matches and `dp[i-1][j]` is true, or from s2, if it matches and `dp[i][j-1]` is true. I roll it into one array. O(m·n) time, O(n) space."

---

### D4. Regular Expression Matching (`.` and `*`, hard)

**Problem in one sentence:** does the whole string s match pattern p, where `.` matches any character and `x*` matches zero or more of `x`?

**Key insight:** let `f(i, j)` mean "does `s[i:]` match `p[j:]`". If the next pattern token is followed by `*`, you have two choices: use it zero times (skip `p[j]` and the star) or, if the current characters match, consume one character of s and stay on the same pattern token. Otherwise, the current characters must match and both advance.

**Dry run** on `s = "aa"`, `p = "a*"`:

```text
f(0,0): 'a' matches, p[1] is '*'
        option zero: f(0,2) -> pattern done, string not -> False
        option one:  f(1,0): 'a' matches, '*'
                     option one: f(2,0): no char left, so zero: f(2,2) -> True
answer True
```

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

**Complexity:** O(mn) time and space: m·n states, O(1) each. Wildcard Matching (`?` and `*`) is similar, except `*` there matches any sequence by itself.

**Say it in 60 seconds:** "I define `f(i, j)` as whether the rest of the string from i matches the rest of the pattern from j, and memoize it. If the pattern is used up, the string must be too. I check whether the current characters match, where a dot matches anything. If the next pattern character is a star, I either skip the starred token entirely, or, if the current characters match, consume one string character and keep the same token. Without a star, both must match and both advance. There are m·n states with constant work each."

---

## E. Knapsack family

### The idea

A **knapsack** problem picks items, each with a size (and maybe a value), to hit or stay within a capacity. The state is "the capacity used so far", and the transition is "include this item or not". The loop order controls whether each item can be used once or many times, which is the most common bug.

**Analogy:** packing a suitcase with a weight limit. 0/1 knapsack means you have one of each item. Unbounded means you're shopping and can buy as many of each item as you want.

| Type | Loop order | Example |
|---|---|---|
| **0/1** (each item once) | items outer, capacity **descending** | Partition Equal Subset Sum, Target Sum, Last Stone Weight II |
| **Unbounded** (reuse items) | capacity **ascending** | Coin Change, Coin Change II, Perfect Squares |
| **Count combinations** | items outer, capacity inner | Coin Change II |
| **Count permutations** (order matters) | capacity outer, items inner | Combination Sum IV |

Why descending for 0/1: when you go downward, `dp[t - x]` still holds the value from **before** this item was considered, so the item can't be used twice. Going upward, `dp[t - x]` might already include this item.

### When to recognise it

- "Subset with sum", "partition into two equal halves", "assign + or - signs".
- "Number of ways to make an amount", "fewest items to reach a total".
- A capacity bound that is small enough to index an array (up to about 10⁴ to 10⁵).

---

### E1. Partition Equal Subset Sum (0/1, boolean)

**Problem in one sentence:** can the array be split into two subsets with equal sums?

**Key insight:** that's the same as "is there a subset summing to half the total?". `dp[t]` is true if some subset sums to t.

**Dry run** on `[1, 5, 11, 5]`, total 22, target 11:

```text
after item  reachable sums
start       {0}
1           {0, 1}
5           {0, 1, 5, 6}
11          {0, 1, 5, 6, 11, ...}  -> 11 reachable
answer True
```

Why descending matters: with item 5, going **up** would set `dp[5]` and then immediately `dp[10] = dp[5]`, using 5 twice.

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

**Complexity:** O(n · target) time, O(target) space. A bitset trick: `bits |= bits << x`, where bit t of an integer means "sum t is reachable", which does a whole row in one big-integer operation.

**Say it in 60 seconds:** "Two equal halves means one subset sums to half the total, so if the total is odd the answer is no. Then it's 0/1 subset sum. `dp[t]` says whether some subset reaches t. For each number I update t from the target down to the number, setting `dp[t]` if `dp[t - x]` was reachable. Going downward makes sure each number is used at most once. O(n · target)."

---

### E2. Target Sum (+/- each number)

**Problem in one sentence:** assign + or - to each number so the total equals target. How many ways?

**Key insight:** reduce to a subset sum. Let P be the sum of the "+" numbers and N the sum of the "-" numbers. `P - N = target`, `P + N = total`, so `P = (target + total) / 2`. Count subsets with that sum. If `target + total` is odd or `|target| > total`, the answer is 0.

**Dry run** on `[1, 1, 1, 1, 1]`, target 3: total 5, P = 4. Choose which four of the five 1s are positive: 5 ways.

```python
def find_target_sum_ways(nums, target):
    total = sum(nums)
    if abs(target) > total or (target + total) % 2:
        return 0
    p = (target + total) // 2
    dp = [1] + [0] * p
    for x in nums:
        for t in range(p, x - 1, -1):
            dp[t] += dp[t - x]
    return dp[p]
```

**Complexity:** O(n · P) time, O(P) space.

**Say it in 60 seconds:** "Split the numbers into the positive group with sum P and the negative group with sum N. P minus N is the target and P plus N is the total, so P is fixed at target plus total over two. Now I count subsets summing to P, which is 0/1 knapsack counting: `dp[t] += dp[t - x]`, iterating t downward so each number is used once. If target plus total is odd or the target is out of range, it's zero ways."

---

### E3. Coin Change II (number of combinations)

**Problem in one sentence:** how many different combinations of coins (order doesn't matter) make the amount?

**Key insight:** put coins in the **outer** loop. Then each combination is built in a fixed coin order (all 1s, then all 2s, ...), so `1 + 2` and `2 + 1` are counted once. Amount ascending because coins are reusable.

**Dry run** on `amount = 5`, coins `[1, 2, 5]`:

```text
amount        0  1  2  3  4  5
after coin 1  1  1  1  1  1  1
after coin 2  1  1  2  2  3  3
after coin 5  1  1  2  2  3  4
answer 4: 5, 2+2+1, 2+1+1+1, 1+1+1+1+1
```

```python
def change(amount, coins):
    dp = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]
```

**Contrast, Combination Sum IV (order matters):** swap the loops so every order is counted.

```python
def combination_sum4(nums, target):
    dp = [1] + [0] * target
    for a in range(1, target + 1):
        for x in nums:
            if x <= a:
                dp[a] += dp[a - x]
    return dp[target]
```

With `nums = [1, 2]` and target 3, `change` gives 2 (1+1+1, 1+2), while `combination_sum4` gives 3 (1+1+1, 1+2, 2+1).

**Complexity:** O(amount × coins) time, O(amount) space.

**Say it in 60 seconds:** "`dp[a]` counts the ways to make amount a. To count combinations rather than orderings, I loop over coins on the outside, so each combination is built in coin order and counted once. Inside, I go upward through amounts because each coin can be reused, adding `dp[a - c]`. If I swapped the loops, I'd count permutations instead, which is the Combination Sum IV problem. O(amount × coins)."

---

## F. Interval DP (range i..j)

### The idea

State `dp[i][j]` is the answer for the sub-range from i to j. The transition splits the range at some point k, or peels off the ends. Iterate by **length** so smaller ranges come first.

**Analogy:** deciding the order to merge piles of stones. The cost of merging the whole row depends on where the final merge splits it, and each side is a smaller version of the same question.

### When to recognise it

- Palindromes over substrings or subsequences.
- "Burst", "merge", "cut", "multiply a chain" where the order of operations matters.
- Constraints with n up to a few hundred (O(n³) is acceptable).

---

### F1. Longest Palindromic Substring (expand from center is simpler)

**Problem in one sentence:** find the longest contiguous palindrome in a string.

**Key insight:** every palindrome has a center, either one character (odd length) or a gap between two (even length). There are 2n - 1 centers. Expand outward from each while the ends match.

**Dry run** on `"babad"`:

```text
center 0 (b)       "b"
center 1 (gap b|a) mismatch
center 2 (a)       "bab"   -> best "bab"
center 4 (b)       "aba"   same length, keep "bab"
answer "bab"
```

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

**Palindromic Substrings (count)** uses the same loop, adding 1 for every successful expansion:

```python
def count_substrings(s):
    count = 0
    for center in range(2 * len(s) - 1):
        l, r = center // 2, center // 2 + center % 2
        while l >= 0 and r < len(s) and s[l] == s[r]:
            count += 1
            l -= 1; r += 1
    return count
```

`count_substrings("aaa")` is 6: three single letters, two "aa", one "aaa".

**Complexity:** O(n²) time, O(1) space.

**Say it in 60 seconds:** "A DP table over all substrings works but uses O(n²) space. Simpler: every palindrome is symmetric around a center, and there are 2n minus 1 centers counting the gaps between characters. For each center I expand while both ends match, and track the longest. After the loop, l and r are one step past the palindrome, so its length is `r - l - 1`. O(n²) time, O(1) space. Counting palindromic substrings is the same loop, adding one per expansion."

---

### F2. Longest Palindromic Subsequence

**Problem in one sentence:** find the length of the longest subsequence (not necessarily contiguous) that's a palindrome.

**Key insight:** `dp[i][j] = dp[i+1][j-1] + 2` if `s[i] == s[j]`, else `max(dp[i+1][j], dp[i][j-1])`. It equals LCS(s, reversed s).

**Dry run** on `"bbbab"`: the ends `b ... b` match, so `dp[0][4] = dp[1][3] + 2`. `dp[1][3]` is for "bba", whose best is "bb" (2). So the answer is 4 ("bbbb").

```python
def longest_palindrome_subseq(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]
```

Looping i downward guarantees `dp[i + 1][...]` is ready. When `j = i + 1`, `dp[i + 1][j - 1]` is below the diagonal and holds 0, which is correct for an empty middle.

**Complexity:** O(n²) time and space.

**Say it in 60 seconds:** "`dp[i][j]` is the longest palindromic subsequence inside s from i to j. If the ends match, they wrap the best answer for the inside, adding 2. If not, I drop one end or the other and take the better. Single characters are 1. I fill i from the end so the inner ranges are computed first. O(n²). It's also LCS of the string with its reverse."

---

### F3. Burst Balloons (hard, "last one to burst")

**Problem in one sentence:** bursting balloon k earns `left neighbour × k × right neighbour`. Choose the order to maximise total coins.

**Key insight:** thinking about the **first** balloon to burst fails, because the neighbours change afterwards. Instead pick k as the **last** balloon burst in (i, j). Its neighbors at that moment are i and j, because everything else between them is already gone. The two sides (i, k) and (k, j) are then independent subproblems. Pad the array with 1s at both ends.

**Dry run** on `[1, 5]`, padded to `a = [1, 1, 5, 1]`:

```text
range (0,2): last = index 1 -> 1*1*5 = 5
range (1,3): last = index 2 -> 1*5*1 = 5
range (0,3): last = index 1 -> 1*1*1 + dp(0,1)=0 + dp(1,3)=5 = 6
             last = index 2 -> 1*5*1 + dp(0,2)=5 + dp(2,3)=0 = 10
answer 10 (burst the 1 first for 5, then the 5 for 5)
```

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

**Complexity:** O(n³) time, O(n²) space. Same family: Matrix Chain Multiplication, Minimum Cost to Cut a Stick, Palindrome Partitioning II.

**Say it in 60 seconds:** "If I think about which balloon to burst first, the neighbours keep changing, so the subproblems aren't independent. Flip it: for an open range between i and j, choose which balloon k is burst last. At that moment its neighbours are exactly i and j, so it earns `a[i] × a[k] × a[j]`, and the ranges on either side are separate subproblems. I pad with 1s and fill by increasing range length. O(n³), fine for n up to a few hundred."

---

## G. State machine DP (stocks)

### The idea

Some problems have a small number of **modes** you can be in, like "holding a stock", "just sold", "resting". Each day you compute the best profit for each mode from the previous day's modes. Draw the modes as circles and the allowed moves as arrows, and each arrow becomes one term in the formulas.

**Analogy:** a traffic light. It can only be red, green or yellow, and it can only change in certain ways. You track the best outcome for each colour at each tick.

### G1. Best Time to Buy/Sell with Cooldown

**Problem in one sentence:** buy and sell a stock many times, but after selling you must wait one day before buying again. Maximise profit.

**Key insight:** states: `hold` (own a share), `sold` (just sold, cooldown), `rest` (no share and free to buy). Transitions: `hold` comes from holding or buying from rest. `sold` comes from selling a held share. `rest` comes from resting or finishing a cooldown.

```text
         buy (-p)
  rest ----------> hold
   ^  \              |
   |   (stay)        | sell (+p)
   |                 v
   +------------- sold   (cooldown, then rest)
```

**Dry run** on prices `[1, 2, 3, 0, 2]`:

```text
p   hold               sold            rest
    -inf               0               0
1   max(-inf, 0-1)=-1  -inf            0
2   -1                 -1+2=1          0
3   -1                 -1+3=2          1
0   max(-1, 1-0)=1     -1+0=-1         2
2   max(1, 2-2)=1      1+2=3           2
answer max(3, 2) = 3 (buy 1, sell 2, cool down, buy 0, sell 2)
```

```python
def max_profit_cooldown(prices):
    hold, sold, rest = float("-inf"), 0, 0
    for p in prices:
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return max(sold, rest)
```

The tuple assignment uses the previous day's values on the right side for all three, which is exactly what the state machine needs.

**Complexity:** O(n) time, O(1) space.

**Say it in 60 seconds:** "I model three states per day: holding a share, just sold and cooling down, and resting with no share. Holding today is either still holding or buying today from rest. Sold today means I sold a held share. Resting today is either still resting or coming out of cooldown. I update all three from yesterday's values at once, and the answer is the best non-holding state at the end. O(n) time, O(1) space."

---

### G2. With a transaction fee / at most k transactions

**Transaction fee:** two states. `cash` (no share) and `hold`. `hold = max(hold, cash - p)` and `cash = max(cash, hold + p - fee)`.

**At most k transactions:** `buy[j] = max(buy[j], sell[j-1] - p)` and `sell[j] = max(sell[j], buy[j] + p)`. `buy[j]` is the best balance while holding during the j-th transaction, and `sell[j]` after completing j transactions. O(n·k).

```python
def max_profit_k(k, prices):
    buy = [float("-inf")] * (k + 1)
    sell = [0] * (k + 1)
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]
```

**Dry run** on `k = 2`, prices `[3, 2, 6, 5, 0, 3]`: the best is buy at 2, sell at 6 (+4), buy at 0, sell at 3 (+3), so `sell[2] = 7`.

**Say it in 60 seconds:** "For at most k transactions I keep, for each j from 1 to k, the best balance while holding in the j-th transaction and the best after selling the j-th. Buying for transaction j starts from the profit after j minus 1 sells, minus today's price. Selling adds today's price to the j-th buy. Updating in increasing j within the same day is safe because buying and selling the same day nets zero. O(n·k). If k is at least n/2, it's the same as unlimited trades."

---

## H. Tree DP

### The idea

Return a tuple of states from children. Each node computes its answer for each state from its children's answers, in post-order. This is the "return info up" shape from the [trees file](03_dsa_3_trees_bst_trie.md), with more than one number returned.

### H1. House Robber III

**Problem in one sentence:** houses form a binary tree, and you can't rob a node and its direct child. Maximise the total.

**Key insight:** each node returns `(rob_this, skip_this)`. If you rob it, its children must be skipped. If you skip it, each child can be robbed or skipped, whichever is better.

**Dry run** on:

```text
      3
     / \
    2   3
     \   \
      3   1

leaf 3 -> (3, 0)        leaf 1 -> (1, 0)
node 2 -> (2 + 0 + 0, 0 + max(3, 0)) = (2, 3)
node 3 (right) -> (3 + 0 + 0, 0 + max(1, 0)) = (3, 1)
root 3 -> (3 + 3 + 1, max(2, 3) + max(3, 1)) = (7, 6)
answer 7 (root and both grandchildren)
```

```python
def rob_tree(root):
    def dfs(n):
        if not n:
            return (0, 0)
        l, r = dfs(n.left), dfs(n.right)
        return (n.val + l[1] + r[1], max(l) + max(r))
    return max(dfs(root))
```

**Complexity:** O(n) time, O(h) space. Binary Tree Cameras and Max Path Sum are also tree DP.

**Say it in 60 seconds:** "Each node returns two numbers: the best total for its subtree if it's robbed, and if it's skipped. If I rob a node, I add its value to both children's 'skipped' numbers. If I skip it, each child independently contributes its better option. One post-order pass, O(n). Returning a pair avoids recomputing grandchildren, which is what makes the naive recursion exponential."

---

## I. Bitmask DP (n ≤ 20)

### The idea

When the state needs to record **which items have been used** and there are at most about 20 items, store that set as the bits of an integer, called a **bitmask**. Bit i is 1 if item i is used. There are 2^n masks, about a million for n = 20.

State includes a bitmask of used items. Examples: TSP (the travelling salesman problem: visit every city once at minimum cost), Shortest Path Visiting All Nodes (BFS over `(node, mask)`), Partition to K Equal Sum Subsets, Minimum number of work sessions.

**Analogy:** a checklist with 20 boxes. The mask is a photo of which boxes are ticked.

### I1. Shortest Path Visiting All Nodes

**Problem in one sentence:** in an undirected graph, find the length of the shortest walk that visits every node (you may revisit nodes and edges).

**Key insight:** the state is `(current node, set of visited nodes)`. All edges cost 1, so BFS over these states finds the shortest. Start from every node at once (multi-source), because the walk can begin anywhere.

**Dry run** on a star: node 0 connected to 1, 2 and 3. The best walk is `1 → 0 → 2 → 0 → 3`, which is 4 edges. BFS reaches state `(3, mask 1111)` at distance 4.

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

**Complexity:** O(2^n · n²) time in the worst case (2^n · n states, each with up to n neighbours), O(2^n · n) space.

**Say it in 60 seconds:** "Revisiting is allowed, so plain BFS on nodes isn't enough. The state must include which nodes I've already seen. With up to 12 or so nodes, that set fits in a bitmask. I BFS over (node, mask) pairs starting from every node, and moving to a neighbour sets its bit. The first time I pop a state whose mask has every bit set, its distance is the answer. States are n times 2^n."

---

## J. Digit DP and DP on strings with counting (awareness)

### The idea

Count numbers ≤ N with a property: the state is `(position, tight, other)`. You build the number digit by digit from the left. **Tight** means "every digit so far equals N's digit", so the next digit can't exceed N's digit at this position. Once you place a smaller digit, you're no longer tight and any digit is allowed after that. "Other" is whatever the property needs (digit sum so far, whether you've started, the last digit).

**Analogy:** filling in a combination lock that must not exceed a given code. Once one wheel is lower than the code, the remaining wheels are free.

Examples: Numbers At Most N Given Digit Set, Count of digit one.

### J1. Numbers At Most N Given Digit Set

**Problem in one sentence:** using only digits from a given set (no zero), how many positive integers ≤ N can you write?

**Dry run** on digits `{1, 3, 5, 7}`, N = 100: one-digit numbers 4, two-digit numbers 4 × 4 = 16, and three-digit numbers would start with 1 and be at least 111 > 100, so 0. Total 20.

```python
def at_most_n_given_digit_set(digits, n):
    s = str(n)
    allowed = sorted(int(d) for d in digits)
    @cache
    def f(pos, tight, started):
        if pos == len(s):
            return 1 if started else 0
        total = 0
        if not started:
            total += f(pos + 1, False, False)          # leave this position blank (shorter number)
        limit = int(s[pos]) if tight else 9
        for d in allowed:
            if d > limit:
                break
            total += f(pos + 1, tight and d == limit, True)
        return total
    return f(0, True, False)
```

**Complexity:** O(len(N) × 2 × 2 × |digits|) time, which is tiny.

**Say it in 60 seconds:** "I count numbers digit by digit from the most significant position. The state is the position, whether I'm still tight against N's prefix, and whether I've started writing the number, which handles shorter numbers. If tight, the next digit can go up to N's digit there, and staying tight requires matching it exactly. Otherwise any allowed digit works. When I reach the end, I count one if I've written at least one digit. It's memoized, so the work is proportional to the number of digits."

---

## K. DP interview tips

- If stuck, write the brute-force recursion, then add `@cache`. That's already DP.
- Name the state in words before writing code.
- Check the loop order for knapsack (ascending vs descending).
- Mention space optimization even if you don't code it.
- Draw the table for a tiny input. Filling three or four cells by hand usually reveals the transition.
- Where DP shows up in real systems: edit distance (diffs, fuzzy matching), knapsack (bin packing and VM placement heuristics), LIS (version ordering), and interval DP (query plan join ordering is DP in database optimizers, which choose the cheapest order to join tables by solving sub-ranges of joins first).
