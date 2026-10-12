# 03.6 Backtracking, greedy, intervals, matrix, bit manipulation, math

<div class="callout note">
<b>How to use this page</b>
<ul>
<li><b>What it covers:</b> six smaller families that round out a coding round: backtracking (try everything with pruning), greedy (the locally best choice), intervals, matrix tricks, bit manipulation, and the math facts interviewers expect.</li>
<li><b>When to read it:</b> last among the DSA files. Intervals and Meeting Rooms are OCI favourites because they map to resource allocation.</li>
<li><b>What to memorise:</b> the choose / recurse / un-choose template, "sort by end for max non-overlapping", the min-heap of end times for meeting rooms, transpose-then-reverse for rotation, and the bit-trick table.</li>
<li><b>How each problem is laid out:</b> a one-line restatement, the key insight, a dry run, code, complexity, and a 60-second spoken version.</li>
</ul>
</div>

Imports assumed by every snippet on this page:

```python
from collections import Counter
from itertools import accumulate
import bisect
import heapq
import math
import random
```

---

## A. Backtracking

### The idea

**Backtracking** builds candidates one step at a time. At each step: choose an option, recurse to make the remaining choices, then **un-choose** (undo) so the next option starts from a clean state. **Prune** as early as possible: if a partial candidate already can't work, stop exploring that branch. Complexity is usually exponential, and you should say so (O(2^n) subsets, O(n!) permutations).

**Analogy:** exploring a maze while unrolling a ball of string. At each fork you pick a path. When you hit a dead end, you wind the string back to the last fork and try the next path. Pruning is noticing a "No Exit" sign before walking down a corridor.

### When to recognise it

- "Return **all** combinations / permutations / subsets / partitions".
- "Place N queens", "solve Sudoku", "find a word in a grid".
- Small input sizes (n ≤ 10 to 20), because the output itself can be exponential.

### Hand-traced example

All subsets of `[1, 2]`. Each level decides "what to add next, from index `start` onwards".

```text
bt(start=0, path=[])        record []
  add 1 -> bt(1, [1])       record [1]
    add 2 -> bt(2, [1,2])   record [1, 2]
    remove 2
  remove 1
  add 2 -> bt(2, [2])       record [2]
  remove 2
result [[], [1], [1, 2], [2]]
```

### Template

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

**Complexity:** O(number of candidates × cost to build each). Subsets are O(n · 2^n), permutations O(n · n!).

### Common mistakes

- Appending `path` instead of `path[:]`. Every saved answer then points to the same list, which ends up empty.
- Forgetting to undo (the `pop`, or restoring a grid cell).
- Producing duplicates when the input has duplicates. Sort first and skip equal values at the same depth.
- Not pruning, so a solvable problem times out.

---

### A1. Subsets (and Subsets II with duplicates)

**Problem in one sentence:** return every subset of the array; in version II the array has duplicates and the output must not.

**Key insight:** every node of the recursion tree is a valid subset, so record it on entry. For duplicates, sort, and at the same depth skip a value equal to the previous one, because choosing "the second 2" first would generate the same subsets as choosing "the first 2" first.

**Dry run** on `[1, 2, 2]` (sorted):

```text
[]  -> [1] -> [1,2] -> [1,2,2]
           (second 2 at this depth skipped)
    -> [2] -> [2,2]
    (second 2 at top depth skipped)
result [[], [1], [1,2], [1,2,2], [2], [2,2]]
```

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

Without duplicates, the same code works and the skip line simply never fires.

**Complexity:** O(n · 2^n) time and output size.

**Say it in 60 seconds:** "Each recursion level chooses the next element to add from a start index onward, and every path is itself a subset, so I record it on entry. Moving the start index forward means I never revisit earlier elements, so each subset is produced once. For duplicates I sort first, and within one level I skip a value equal to the one just tried, since it would produce identical subsets. There are 2^n subsets and copying each costs up to n, so O(n · 2^n)."

---

### A2. Permutations

**Problem in one sentence:** return every ordering of distinct numbers.

**Key insight:** unlike subsets, order matters and every element must be used. At each position, try every element not yet used, tracked with a `used` array.

**Dry run** on `[1, 2, 3]`: first position 1, then 2 then 3 gives `[1,2,3]`, then 3 then 2 gives `[1,3,2]`. First position 2 gives `[2,1,3]`, `[2,3,1]`. First position 3 gives `[3,1,2]`, `[3,2,1]`. Six total.

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

**Complexity:** O(n · n!) time and output.

**Permutations II** (with duplicates): sort, and skip `nums[i] == nums[i-1] and not used[i-1]`. That rule says equal values must be used in their original order, so swapped copies of identical numbers aren't generated twice.

**Say it in 60 seconds:** "For each position I try every number that isn't used yet, mark it used, recurse, then unmark it. When the path is as long as the input, I save a copy. There are n! permutations and each takes O(n) to copy. With duplicates, I sort and skip a number if it equals the previous one and the previous one isn't currently in use, which forces equal numbers to appear in a fixed order."

---

### A3. Combination Sum (reuse allowed)

**Problem in one sentence:** find all unique combinations of candidates that add up to a target, where each candidate can be used any number of times.

**Key insight:** recurse with the same index `i` (not `i + 1`) to allow reuse, and never go back to earlier indices, which prevents `[2, 3]` and `[3, 2]` both appearing. Sorting allows an early `break` once a candidate exceeds the remaining target.

**Dry run** on candidates `[2, 3, 6, 7]`, target 7:

```text
remain 7: try 2 -> remain 5: try 2 -> remain 3: try 2 -> remain 1: 2 > 1 break
                                              try 3 -> remain 0: record [2,2,3]
                             try 3 -> remain 2: 3 > 2 break
          try 3 -> remain 4: try 3 -> remain 1 break; 6 > 4 break
          try 6 -> remain 1 break
          try 7 -> remain 0: record [7]
result [[2, 2, 3], [7]]
```

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

**Complexity:** exponential, roughly O(n^(target / min candidate)) in the worst case.

**Say it in 60 seconds:** "I backtrack with a start index and the remaining target. At each level I try candidates from the start index onward, recursing with the same index so a number can repeat, and never going backward so I don't produce the same combination in a different order. Sorting lets me break out as soon as a candidate exceeds what's left. When the remainder hits zero I record the path."

---

### A4. Word Search (grid backtracking)

**Problem in one sentence:** can a word be traced through adjacent grid cells without reusing a cell?

**Key insight:** start a DFS from every cell matching the first letter. Mark the cell as visited (`board[r][c] = '#'`), recurse in 4 directions for the next letter, then restore it. Restoring is the "un-choose" step.

**Dry run** on the grid below looking for "SEE":

```text
A B C E
S F C S
A D E E

start at (1,3) 'S' -> up (0,3) 'E' -> next needs 'E': neighbours (0,2) 'C', (1,3) '#'
                   -> down (2,3) 'E' -> left (2,2) 'E' -> word complete -> True
```

```python
def exist(board, word):
    R, C = len(board), len(board[0])
    def bt(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[i]:
            return False
        board[r][c] = "#"
        found = any(bt(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = word[i]
        return found
    return any(bt(r, c, 0) for r in range(R) for c in range(C))
```

**Complexity:** O(R·C·4^L) where L is the word length (3^L after the first step, since you never go back the way you came). O(L) recursion space.

**Say it in 60 seconds:** "From each cell I try to match the word letter by letter with DFS. If the cell is out of bounds or the letter doesn't match, that branch fails. Otherwise I temporarily mark the cell so the path can't reuse it, try all four neighbours for the next letter, and restore the cell afterwards. `any` stops at the first success. For many words at once I'd switch to a trie, which is Word Search II."

---

### A5. N-Queens

**Problem in one sentence:** place n queens on an n × n board so that none attack each other, and return every arrangement.

**Key insight:** one queen per row, so place row by row. Track the sets `cols`, `diag1 = r - c`, and `diag2 = r + c`. Every cell on the same "\" diagonal has the same `r - c`, and on the same "/" diagonal the same `r + c`, so each check is O(1).

**Dry run** for n = 4 (one of the two solutions):

```text
row 0: col 1     . Q . .
row 1: col 3     . . . Q
row 2: col 0     Q . . .
row 3: col 2     . . Q .
(row 0 col 0 was tried first and failed at row 2 or 3, so the algorithm backtracked)
```

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

**Complexity:** O(n!) time roughly, because each row has fewer safe columns than the last. O(n) space besides the output.

**Say it in 60 seconds:** "Each row gets exactly one queen, so I place them row by row. For a candidate column I need to know in O(1) whether that column or either diagonal is taken. Cells on one diagonal share `r - c`, and on the other share `r + c`, so three sets are enough. I place the queen, recurse to the next row, then remove it. When all rows are filled I save the board. The search is roughly O(n!)."

---

### A6. Palindrome Partitioning, Letter Combinations of a Phone Number, Generate Parentheses (track open/close counts), Sudoku Solver

**Palindrome Partitioning:** split a string into pieces that are all palindromes, returning every way. At each start index, try every end index whose piece is a palindrome, and recurse from there.

```python
def partition(s):
    res, path = [], []
    def bt(start):
        if start == len(s):
            res.append(path[:]); return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece == piece[::-1]:
                path.append(piece)
                bt(end)
                path.pop()
    bt(0)
    return res
```

Dry run: `"aab"` gives `[["a", "a", "b"], ["aa", "b"]]`.

**Letter Combinations:** each digit maps to letters on a phone keypad. Choose one letter per digit.

```python
def letter_combinations(digits):
    if not digits:
        return []
    keys = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    res = []
    def bt(i, path):
        if i == len(digits):
            res.append(path); return
        for ch in keys[digits[i]]:
            bt(i + 1, path + ch)
    bt(0, "")
    return res
```

Dry run: `"23"` gives `ad ae af bd be bf cd ce cf`.

**Generate Parentheses:** produce every valid string of n pairs. You may add `(` while fewer than n are open, and `)` only while closes are fewer than opens, so the string never becomes invalid.

```python
def generate_parenthesis(n):
    res = []
    def bt(path, opened, closed):
        if len(path) == 2 * n:
            res.append(path); return
        if opened < n:
            bt(path + "(", opened + 1, closed)
        if closed < opened:
            bt(path + ")", opened, closed + 1)
    bt("", 0, 0)
    return res
```

Dry run: n = 2 gives `(())` and `()()`.

**Sudoku Solver:** find an empty cell, try digits 1 to 9 that don't break the row, column or 3 × 3 box (track with sets as in Valid Sudoku, D5 below), recurse, and undo on failure. Picking the empty cell with the fewest options first prunes dramatically.

**Say it in 60 seconds (Generate Parentheses):** "Instead of generating all strings and filtering, I only build valid prefixes. I can add an opening bracket while I've used fewer than n, and a closing bracket only when it would close an open one. When the string reaches length 2n it's guaranteed valid. The number of results is the n-th Catalan number."

---

## B. Greedy

### The idea

A **greedy** algorithm makes the locally best choice at each step and never reconsiders. It's fast and simple, but **only correct if you can argue it**. Two standard arguments:

- **Exchange argument:** take any optimal solution, and show that swapping its choice for the greedy choice doesn't make it worse. So some optimal solution agrees with greedy.
- **Greedy stays ahead:** show that after every step, greedy is at least as good as any other strategy.

If you can't argue it, it's probably DP (Coin Change is the classic greedy trap).

**Analogy:** filling your day with as many meetings as possible. Always picking the meeting that **ends earliest** leaves the most room for the rest of the day, and you can prove it.

### When to recognise it

- "Maximum number of non-overlapping...", "minimum number of arrows / rooms / boats".
- "Can you reach the end?", "minimum jumps".
- Sorting by one key (start, end, ratio) obviously helps.
- A small counterexample doesn't break the obvious choice. Always try one before committing.

### Common mistakes

- Using greedy where it fails (coins `[1, 3, 4]` for 6).
- Sorting by the wrong key (start versus end).
- Not explaining why greedy works. Interviewers ask.

---

### B1. Jump Game I and II

**Problem in one sentence:** each value says how far you can jump from that index. (I) Can you reach the last index? (II) What's the minimum number of jumps?

**Key insight (I):** track the farthest index reachable so far. If you ever stand at an index beyond it, you're stuck.

**Key insight (II):** think of it as BFS by layers. All indices reachable with j jumps form a range. While scanning that range, compute the farthest reach for the next jump. When you reach the end of the current range, you must jump.

**Dry run (II)** on `[2, 3, 1, 1, 4]`:

```text
i  far = max(far, i + nums[i])   i == end?             jumps  end
0  2                             yes, jump             1      2
1  4
2  4                             yes, jump             2      4
loop stops before the last index -> answer 2 (0 -> 1 -> 4)
```

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

**Complexity:** O(n) time, O(1) space for both.

**Say it in 60 seconds (Jump Game II):** "Every index reachable in j jumps forms a contiguous range, so this is BFS where each layer is a range. I scan left to right, tracking the farthest index the current layer can reach. When I reach the end of the current layer, I have to take another jump, and the new layer ends at that farthest point. I stop before the last index, because standing on it needs no further jump. O(n), O(1)."

---

### B2. Gas Station

**Problem in one sentence:** stations in a circle give gas and cost gas to reach the next one. Find the starting station that lets you complete the loop, or -1.

**Key insight:** if total gas < total cost, the answer is -1. Otherwise a solution exists. Reset the start whenever the running tank goes negative: if you can't get from `start` to `i`, then no station between them can be a valid start either, because each of them would arrive at `i` with even less gas.

**Dry run** on `gas = [1, 2, 3, 4, 5]`, `cost = [3, 4, 5, 1, 2]`:

```text
i  gain = gas - cost  tank  action
0  -2                 -2    reset, start = 1
1  -2                 -2    reset, start = 2
2  -2                 -2    reset, start = 3
3  3                  3
4  3                  6
answer 3
```

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

**Complexity:** O(n) time, O(1) space.

**Say it in 60 seconds:** "If total gas is less than total cost, no start works. Otherwise I scan once with a running tank from a candidate start. If the tank goes negative at station i, the candidate fails, and so does every station between it and i, since each would arrive at i with no more gas than I had. So I jump the candidate to i plus 1 and reset the tank. Because the total is non-negative, the last candidate standing works. O(n)."

---

### B3. Partition Labels

**Problem in one sentence:** split a string into as many parts as possible so that each letter appears in only one part. Return the part sizes.

**Key insight:** record the last index of each char. As you scan, extend the current partition's end to the max last-index seen, and cut when `i == end`, because every letter seen so far finishes inside this part.

**Dry run** on `"abaccd"` (last: a 2, b 1, c 4, d 5):

```text
i  c  end = max(end, last[c])  cut?
0  a  2
1  b  2
2  a  2                        yes, size 3
3  c  4
4  c  4                        yes, size 2
5  d  5                        yes, size 1
answer [3, 2, 1]
```

```python
def partition_labels(s):
    last = {c: i for i, c in enumerate(s)}
    res, start, end = [], 0, 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            res.append(end - start + 1)
            start = i + 1
    return res
```

**Complexity:** O(n) time, O(alphabet) space.

**Say it in 60 seconds:** "A part can't end before the last occurrence of any letter inside it. So I precompute each letter's last index, then scan while tracking the furthest last index of letters in the current part. When my position reaches that furthest index, every letter in the part is finished, so I cut there. Cutting as early as possible maximises the number of parts. Two passes, O(n)."

---

### B4. Hand of Straights, Task Scheduler (math greedy), Minimum Number of Arrows (sort by end), Boats to Save People (two pointers)

**Hand of Straights in one sentence:** can the cards be split into groups of w consecutive values? The smallest remaining card must **start** a group (nothing smaller can absorb it), so greedily build groups from the smallest value up.

```python
def is_n_straight_hand(hand, w):
    if len(hand) % w:
        return False
    count = Counter(hand)
    for x in sorted(count):
        if count[x]:
            need = count[x]
            for y in range(x, x + w):
                if count[y] < need:
                    return False
                count[y] -= need
    return True
```

Dry run: `[1, 2, 3, 6, 2, 3, 4, 7, 8]`, w = 3. From 1: use one each of 1, 2, 3. From 2: one each of 2, 3, 4. From 6: 6, 7, 8. True.

**Task Scheduler:** see the [heap file](03_dsa_2_linkedlist_stack_queue_heap.md), section E5. The most frequent task fixes the frame size.

**Minimum Number of Arrows:** balloons are intervals, an arrow at x bursts every balloon covering x. Sort by end and shoot at the end of the first balloon, which bursts everything overlapping it. Same exchange argument as activity selection.

```python
def find_min_arrow_shots(points):
    points.sort(key=lambda p: p[1])
    arrows, end = 0, float("-inf")
    for s, e in points:
        if s > end:
            arrows += 1
            end = e
    return arrows
```

Dry run: `[[10,16], [2,8], [1,6], [7,12]]` sorted by end is `[1,6], [2,8], [7,12], [10,16]`. Arrow at 6 bursts the first two, arrow at 12 bursts the last two. Answer 2.

**Boats to Save People:** each boat holds at most two people under a weight limit. Sort, then pair the heaviest person with the lightest if they fit. The heaviest must go in some boat, and the lightest is the best partner they could have.

```python
def num_rescue_boats(people, limit):
    people.sort()
    l, r, boats = 0, len(people) - 1, 0
    while l <= r:
        if people[l] + people[r] <= limit:
            l += 1
        r -= 1
        boats += 1
    return boats
```

Dry run: `[3, 2, 2, 1]`, limit 3, sorted `[1, 2, 2, 3]`: 3 alone, then 1 + 2, then 2 alone. Answer 3.

**Complexity:** all are O(n log n) for the sort.

**Say it in 60 seconds (Arrows):** "Sort balloons by their end. The first balloon must be hit by some arrow, and shooting at its right end is the best choice, because it hits every balloon that starts before that point. Then I skip all balloons that arrow covers and repeat with the next one that starts after it. That's activity selection, and the exchange argument says no other first shot can cover more."

---

## C. Intervals

### The idea

An **interval** is a pair `[start, end]`. Almost every interval problem starts by sorting: by start (to merge overlaps or sweep through time) or by end (to pick the maximum number of non-overlapping intervals). Then a single sweep with a small amount of state solves it. Two intervals `[a, b]` and `[c, d]` overlap when `a <= d and c <= b`.

**Analogy:** a meeting-room calendar. Sorting by start time lets you see conflicts as you read top to bottom. Sorting by end time tells you which meeting frees up a room first.

### When to recognise it

- "Merge overlapping", "insert an interval", "free time", "intersections".
- "Minimum rooms / servers / platforms needed".
- "Maximum number of events you can attend", "minimum removals to make non-overlapping".
- Log analysis: "maximum concurrent connections".

### Hand-traced example

Merge `[[1, 3], [2, 6], [8, 10], [15, 18]]` (already sorted):

```text
interval  overlaps last in output?   output
[1,3]     first                      [[1,3]]
[2,6]     2 <= 3 yes, extend         [[1,6]]
[8,10]    8 <= 6 no, append          [[1,6], [8,10]]
[15,18]   no, append                 [[1,6], [8,10], [15,18]]
```

### Template

The template is the Merge Intervals code below.

**Complexity:** O(n log n) for the sort, O(n) for the sweep.

### Common mistakes

- Deciding whether touching intervals (`[1, 2]` and `[2, 3]`) overlap. Read the problem. Merge Intervals treats them as overlapping. Meeting Rooms treats them as not conflicting.
- Sorting by start when the problem needs end (non-overlapping, arrows).
- Mutating the caller's input lists by accident.

---

### C1. Merge Intervals

**Problem in one sentence:** merge all overlapping intervals.

**Key insight:** after sorting by start, an interval overlaps the merged block only if it starts before that block ends. So compare with the last interval in the output only.

**Dry run:** see the hand-traced example above.

```python
def merge(intervals):
    if not intervals:
        return []
    intervals.sort()
    out = [list(intervals[0])]
    for s, e in intervals[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
```

An older version of this function crashed on an empty list (`intervals[0]`) and, because `out` started with the caller's own first interval, extending it silently changed the caller's data. The guard and `list(...)` copy fix both.

**Complexity:** O(n log n) time, O(n) for the output.

**Say it in 60 seconds:** "I sort by start time. Then any interval that overlaps the current merged block must start before the block ends, so I only compare with the last interval in my output. If it overlaps, I extend the end to the larger of the two ends. Otherwise it starts a new block. I copy the first interval so I don't mutate the caller's input. Sorting dominates at O(n log n)."

---

### C2. Insert Interval

**Problem in one sentence:** insert a new interval into a sorted list of non-overlapping intervals, merging as needed.

**Key insight:** the list is already sorted, so no sort is needed. Three phases: add everything that ends before the new one, merge the overlaps, then add the rest. O(n).

**Dry run** on `[[1,2], [3,5], [6,7], [8,10], [12,16]]`, new `[4, 8]`:

```text
phase 1: [1,2] ends before 4 -> keep
phase 2: [3,5] overlaps -> [3,8]; [6,7] overlaps -> [3,8]; [8,10] overlaps -> [3,10]
phase 3: [12,16] -> keep
answer [[1,2], [3,10], [12,16]]
```

```python
def insert(intervals, new):
    res, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < new[0]:
        res.append(intervals[i]); i += 1
    s, e = new
    while i < n and intervals[i][0] <= e:
        s, e = min(s, intervals[i][0]), max(e, intervals[i][1]); i += 1
    res.append([s, e])
    res.extend(intervals[i:])
    return res
```

**Complexity:** O(n) time and space.

**Say it in 60 seconds:** "The input is sorted and non-overlapping, so I can do it in one pass. First I copy every interval that ends before the new one starts. Then, while intervals start before the new one ends, I absorb them by widening the new interval. I add the merged interval and then copy everything left. O(n), no sorting needed."

---

### C3. Non-overlapping Intervals (min removals)

**Problem in one sentence:** remove the fewest intervals so the rest don't overlap.

**Key insight:** this is "keep the maximum number of non-overlapping intervals". **Greedy:** sort by **end**, and keep the interval that ends earliest, since it leaves the most room. That's classic activity selection. Every interval that starts before the last kept end must be removed.

**Dry run** on `[[1,2], [2,3], [3,4], [1,3]]`, sorted by end `[1,2], [2,3], [1,3], [3,4]`:

```text
interval  start >= end?  action    end  removed
[1,2]     yes            keep      2    0
[2,3]     2 >= 2 yes     keep      3    0
[1,3]     1 >= 3 no      remove    3    1
[3,4]     yes            keep      4    1
answer 1
```

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

**Complexity:** O(n log n).

**Say it in 60 seconds:** "Minimising removals is the same as keeping as many non-overlapping intervals as possible. Sorting by end time and always keeping the one that finishes first is optimal: if an optimal answer kept something that ends later, swapping in the earlier-ending one can't cause new overlaps. So I scan in end order, keep an interval if it starts at or after the last kept end, and count the rest as removals. O(n log n)."

---

### C4. Meeting Rooms II (min rooms, OCI-relevant: resource allocation)

**Problem in one sentence:** given meeting times, find the minimum number of rooms so no two overlapping meetings share a room.

**Key insight (heap):** sort by start. Keep a min-heap of end times for rooms in use. If the earliest end ≤ the current start, that room is free, so reuse it (replace its end time). Otherwise open a new room. The heap size at the end is the answer.

**Dry run** on `[[0, 30], [5, 10], [15, 20]]`:

```text
meeting  heap of end times before  earliest end <= start?  heap after
[0,30]   []                        no rooms                [30]
[5,10]   [30]                      30 <= 5? no, new room   [10, 30]
[15,20]  [10, 30]                  10 <= 15 yes, reuse     [20, 30]
answer 2 rooms
```

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

```python
def min_meeting_rooms_sweep(intervals):
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort()
    cur = best = 0
    for _, delta in events:
        cur += delta
        best = max(best, cur)
    return best
```

Sorting tuples puts `(t, -1)` before `(t, 1)` at the same time t, so a meeting that ends at 10 frees its room before one that starts at 10 needs it. That matches the heap's `<=`.

**Complexity:** O(n log n) for both.

**Say it in 60 seconds:** "I sort meetings by start time and keep a min-heap of end times, one per room in use. For each meeting, if the earliest-ending room is free by this meeting's start, I reuse it by replacing its end time. Otherwise I need a new room. The heap size is the answer. An equivalent sweep: plus one at every start, minus one at every end, and the maximum running total is the number of rooms. In cloud terms it's capacity planning: how many hosts so no job waits."

---

### C5. Employee Free Time, Interval List Intersections (two pointers), My Calendar I/II (sorted list or segment tree), Car Pooling (difference array)

**Interval List Intersections in one sentence:** two lists of sorted, disjoint intervals; return their intersections. The overlap of the current pair is `[max(starts), min(ends)]` if non-empty. Then advance whichever interval ends first, since it can't intersect anything further.

```python
def interval_intersection(a, b):
    i = j = 0
    res = []
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo <= hi:
            res.append([lo, hi])
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return res
```

Dry run: `a = [[0, 2], [5, 10]]`, `b = [[1, 5]]`. Pair 1: `[1, 2]`, advance a. Pair 2: `[5, 5]`, advance b. Answer `[[1, 2], [5, 5]]`.

**Car Pooling in one sentence:** can a car with fixed capacity complete all trips `(passengers, from, to)`? Use a **difference array**: add passengers at the pickup point and subtract at the drop-off point, then the running sum is the load at each location.

```python
def car_pooling(trips, capacity):
    diff = [0] * 1001
    for n, s, e in trips:
        diff[s] += n
        diff[e] -= n
    cur = 0
    for d in diff:
        cur += d
        if cur > capacity:
            return False
    return True
```

The size 1001 comes from the problem's bound on locations. Dry run: trips `[[2, 1, 5], [3, 3, 7]]`, capacity 4: at location 3 the load is 2 + 3 = 5 > 4, so False.

**Employee Free Time:** flatten everyone's busy intervals, merge them (C1), and the gaps between merged blocks are the common free time.

**My Calendar I/II:** book intervals and reject double (or triple) bookings. Keep bookings in a sorted list and check neighbours with `bisect` for I. For II, keep a list of single bookings and a list of overlaps, or use a sweep over a sorted map of `+1/-1` counts.

**Say it in 60 seconds (Car Pooling):** "Instead of simulating every passenger, I record changes: plus n at the pickup, minus n at the drop-off. A running sum over locations then gives the exact load at each point, and I fail if it ever exceeds capacity. That's O(n + range). It's the same trick as the meeting-rooms sweep, written as an array because the locations are small integers."

---

## D. Matrix

### The idea

Matrix problems are usually about **index arithmetic**: how a cell's coordinates change under a rotation, which boundary to shrink in a spiral, or how to reuse part of the matrix as scratch memory to get O(1) space.

**Analogy:** rotating a photo on your phone. Every pixel moves to a new position by a fixed formula, and you can do it in place by first flipping along the diagonal and then mirroring left to right.

### When to recognise it

- "Rotate", "spiral", "transpose", "in place".
- "Set rows and columns to zero", "game of life".
- "Search a sorted matrix".

---

### D1. Rotate Image 90° clockwise in place

**Problem in one sentence:** rotate an n × n matrix 90 degrees clockwise without another matrix.

**Key insight:** transpose (swap across the main diagonal), then reverse each row. A clockwise rotation sends `(r, c)` to `(c, n-1-r)`. Transpose gives `(c, r)`, and reversing the row gives `(c, n-1-r)`.

**Dry run:**

```text
original    transpose    reverse rows
1 2 3       1 4 7        7 4 1
4 5 6       2 5 8        8 5 2
7 8 9       3 6 9        9 6 3
```

```python
def rotate(m):
    n = len(m)
    for i in range(n):
        for j in range(i + 1, n):
            m[i][j], m[j][i] = m[j][i], m[i][j]
    for row in m:
        row.reverse()
```

**Complexity:** O(n²) time, O(1) extra space.

**Say it in 60 seconds:** "A 90-degree clockwise rotation moves cell (r, c) to (c, n minus 1 minus r). I get that in two in-place steps: transpose, which swaps r and c, then reverse each row, which mirrors the column. The transpose loop only touches cells above the diagonal so each pair swaps once. O(n²) time and O(1) extra space. Counter-clockwise is transpose then reverse each column."

---

### D2. Spiral Matrix

**Problem in one sentence:** return all elements of a matrix in clockwise spiral order.

**Key insight:** shrink four boundaries: top, bottom, left, right. Walk the top row, then the right column, then the bottom row backwards, then the left column upwards, shrinking each boundary after use. The two `if` checks stop a single remaining row or column from being walked twice.

**Dry run** on `[[1, 2, 3], [4, 5, 6], [7, 8, 9]]`:

```text
top row 0:     1 2 3     top = 1
right col 2:   6 9       right = 1
bottom row 2:  8 7       bot = 1
left col 0:    4         left = 1
top row 1:     5         top = 2
stop. answer [1, 2, 3, 6, 9, 8, 7, 4, 5]
```

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

**Complexity:** O(R·C) time, O(1) extra.

**Say it in 60 seconds:** "I keep four boundaries. Each loop peels one layer: the top row left to right, the right column top to bottom, then the bottom row right to left and the left column bottom to top, shrinking each boundary after I use it. Before the last two walks I recheck the boundaries, because a single remaining row or column would otherwise be visited twice. Every cell is visited once."

---

### D3. Set Matrix Zeroes (O(1) space)

**Problem in one sentence:** if a cell is 0, set its entire row and column to 0, in place.

**Key insight:** you need to remember which rows and columns to clear. Instead of extra arrays, use the first row and first column as markers, with a separate flag for the first column (because `m[0][0]` can only mark one of row 0 or column 0).

**Dry run:**

```text
input      after marking (row 1 has a zero at column 1)   result
1 1 1      1 0 1                                          1 0 1
1 0 1      0 0 1                                          0 0 0
1 1 1      1 1 1                                          1 0 1
```

```python
def set_zeroes(m):
    R, C = len(m), len(m[0])
    first_col_zero = any(m[r][0] == 0 for r in range(R))
    for r in range(R):
        for c in range(1, C):
            if m[r][c] == 0:
                m[r][0] = 0
                m[0][c] = 0
    for r in range(1, R):
        for c in range(1, C):
            if m[r][0] == 0 or m[0][c] == 0:
                m[r][c] = 0
    if m[0][0] == 0:
        for c in range(1, C):
            m[0][c] = 0
    if first_col_zero:
        for r in range(R):
            m[r][0] = 0
```

**Complexity:** O(R·C) time, O(1) extra space.

**Say it in 60 seconds:** "The simple way stores sets of zero rows and zero columns, O(R + C) space. To get O(1), I reuse the first row and first column as those sets. First I note whether column 0 itself has a zero, since `m[0][0]` will be busy marking row 0. Then I mark: a zero at (r, c) sets `m[r][0]` and `m[0][c]`. Then I clear the inner cells using the markers, and finally the first row and first column, in that order so the markers aren't destroyed early."

---

### D4. Search a 2D Matrix

**Problem in one sentence (I):** each row is sorted and each row starts after the previous row ends. **(II):** rows are sorted and columns are sorted separately. Find a target.

- **Fully sorted (I):** it's really one sorted array, so binary search as a 1D array, `r, c = divmod(mid, C)`.
- **Rows and columns sorted separately (II):** start at the top-right. Go left if too big, down if too small. O(R + C). From the top-right, everything to the left is smaller and everything below is larger, so each comparison eliminates a whole row or column.

```python
def search_matrix(m, target):
    R, C = len(m), len(m[0])
    lo, hi = 0, R * C - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        r, c = divmod(mid, C)
        if m[r][c] == target:
            return True
        if m[r][c] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False

def search_matrix_ii(m, target):
    r, c = 0, len(m[0]) - 1
    while r < len(m) and c >= 0:
        if m[r][c] == target:
            return True
        if m[r][c] > target:
            c -= 1
        else:
            r += 1
    return False
```

**Dry run (II)** on target 5 in `[[1, 4, 7], [2, 5, 8], [3, 6, 9]]`: start at 7, too big, go left to 4. Too small, go down to 5. Found.

**Complexity:** O(log(R·C)) for I, O(R + C) for II.

**Say it in 60 seconds (II):** "I start at the top-right corner, where values get smaller as I move left and larger as I move down. If the value is bigger than the target, the whole column below is bigger too, so I move left. If it's smaller, the whole row to the left is smaller, so I move down. Each step discards a row or a column, so it's O(R + C)."

---

### D5. Valid Sudoku

**Problem in one sentence:** check that no digit repeats in any row, column or 3 × 3 box of a partially filled board.

**Key insight:** sets per row, column, and box, where `box = (r // 3) * 3 + c // 3` numbers the boxes 0 to 8 left to right, top to bottom.

```python
def is_valid_sudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == ".":
                continue
            b = (r // 3) * 3 + c // 3
            if v in rows[r] or v in cols[c] or v in boxes[b]:
                return False
            rows[r].add(v); cols[c].add(v); boxes[b].add(v)
    return True
```

**Dry run:** cell (4, 7) is in box `(4 // 3) * 3 + 7 // 3 = 3 + 2 = 5`, the middle-right box.

**Complexity:** O(81), constant.

**Say it in 60 seconds:** "I keep 27 sets: one per row, column and box. The box index for a cell is three times its box row plus its box column, which numbers the nine boxes. For each filled cell, if the digit is already in its row, column or box set, it's invalid. Otherwise I add it to all three. It's a fixed 81 cells, so constant time."

---

### D6. Game of Life (in place)

**Problem in one sentence:** update a grid of live and dead cells to the next generation in place, where every cell's fate depends on its eight neighbours' **current** state.

**Key insight:** you can't overwrite cells as you go, because neighbours still need the old values. Encode the next state in extra bits: `2` = alive to dead, `3` = dead to alive, or use bit 1 for the next state. In the bit version, bit 0 is the current state and bit 1 the next. Count neighbours with `& 1`, then shift everything right by one at the end.

**Rules:** a live cell with 2 or 3 live neighbours stays alive. A dead cell with exactly 3 live neighbours becomes alive. Everything else is dead next round.

**Dry run** (a "blinker"): a horizontal row of three live cells becomes a vertical column of three. The middle cell has 2 neighbours and stays alive. The cells above and below the middle have 3 neighbours and come alive. The two end cells have 1 neighbour and die.

```python
def game_of_life(board):
    R, C = len(board), len(board[0])
    for r in range(R):
        for c in range(C):
            live = sum(board[nr][nc] & 1
                       for nr in range(max(0, r - 1), min(R, r + 2))
                       for nc in range(max(0, c - 1), min(C, c + 2))
                       if (nr, nc) != (r, c))
            if board[r][c] & 1 and live in (2, 3):
                board[r][c] |= 2
            elif not board[r][c] & 1 and live == 3:
                board[r][c] |= 2
    for r in range(R):
        for c in range(C):
            board[r][c] >>= 1
```

**Complexity:** O(R·C) time, O(1) extra space.

**Say it in 60 seconds:** "Every cell's next state depends on its neighbours' current states, so I can't overwrite in one pass. I store the next state in the second bit of each cell and keep the current state in the first bit. When counting neighbours, I read only bit 0, so updates don't interfere. After the pass, shifting every cell right by one makes the next state current. O(R·C) time and O(1) extra memory."

---

### D7. Grid BFS/DFS problems (islands, rotting oranges, shortest path in a binary matrix)

See [graphs](03_dsa_4_graphs_dsu.md). A grid is a graph where each cell is a node and its 4 (or 8) neighbours are edges.

---

## E. Bit manipulation

### The idea

Integers are stored as binary digits (bits), and bitwise operators work on all bits at once in a single CPU instruction. A few identities replace loops and extra memory.

- `&` (AND) is 1 where both bits are 1. `|` (OR) is 1 where either is. `^` (XOR) is 1 where they differ. `~` flips every bit. `<<` and `>>` shift bits left or right (multiply or divide by 2).
- **XOR is the star:** `a ^ a = 0` and `a ^ 0 = a`, and order doesn't matter. So XOR-ing a list cancels every value that appears twice.

**Analogy:** a row of light switches. AND asks "are both on?", OR asks "is either on?", XOR asks "are they different?", and shifting slides the whole row of switches one place.

| Trick | Code |
|---|---|
| Check bit i | `(x >> i) & 1` |
| Set / clear / toggle | `x | (1<<i)`, `x & ~(1<<i)`, `x ^ (1<<i)` |
| Lowest set bit | `x & -x` |
| Clear lowest set bit | `x & (x - 1)` |
| Power of two | `x > 0 and x & (x - 1) == 0` |
| Count bits | `bin(x).count("1")` or `x.bit_count()` |
| XOR facts | `a ^ a = 0`, `a ^ 0 = a`, commutative |

Worked example of `x & (x - 1)`: x = 12 is `1100`. x - 1 = 11 is `1011`. AND gives `1000` = 8, which is 12 with its lowest 1-bit removed.

### When to recognise it

- "Every element appears twice except one", "find the missing number".
- "Without using + or *", "in O(1) extra space".
- "Power of two", "count set bits", "reverse bits".
- n ≤ 20 and "all subsets" (masks).

### Common mistakes

- Python integers have unlimited size and negative numbers have infinitely many leading 1s, so 32-bit tricks need a mask like `0xFFFFFFFF`.
- Operator precedence: `x & 1 == 0` parses as `x & (1 == 0)`. Write `(x & 1) == 0`.

---

### E1. Single Number (every other number appears twice)

**Key insight:** XOR everything. Pairs cancel to 0, leaving the single number. O(n), O(1).

**Dry run** on `[4, 1, 2, 1, 2]`: 4 ^ 1 = 5, ^ 2 = 7, ^ 1 = 6, ^ 2 = 4. Answer 4.

```python
def single_number(nums):
    x = 0
    for v in nums:
        x ^= v
    return x
```

**Say it in 60 seconds:** "XOR of a number with itself is zero, XOR with zero leaves a number unchanged, and order doesn't matter. So XOR-ing the whole array cancels every pair and leaves the unique number. One pass, constant space, no hashmap."

---

### E2. Single Number II (others appear three times)

**Key insight:** count each bit mod 3, or use the `ones/twos` state machine. For each bit, `ones` holds it if it has appeared once (mod 3) and `twos` if twice. On the third appearance both clear.

```python
def single_number_ii(nums):
    ones = twos = 0
    for x in nums:
        ones = (ones ^ x) & ~twos
        twos = (twos ^ x) & ~ones
    return ones
```

**Dry run** on `[2, 2, 3, 2]`:

```text
x (binary)  ones  twos  what happened per bit
2 (10)      10    00    bit 1 seen once
2 (10)      00    10    bit 1 seen twice
3 (11)      01    00    bit 1 seen a third time, so cleared; bit 0 seen once
2 (10)      11    00    bit 1 seen a fourth time, which is once mod 3
answer ones = 11 = 3
```

The masks track individual bits, not whole numbers, so trace it bit by bit as above.

**Say it in 60 seconds:** "Every bit position sees the triplicated numbers a multiple of three times, plus the unique number once. So I track, per bit, whether its count mod 3 is one or two, using two masks. Adding a number toggles it into `ones` unless it's already in `twos`, and into `twos` unless it's now in `ones`. On the third occurrence it clears from both. What's left in `ones` is the answer. O(n), O(1)."

---

### E3. Counting Bits

**Problem in one sentence:** for every i from 0 to n, return the number of 1 bits.

**Key insight:** `dp[i] = dp[i >> 1] + (i & 1)`. Shifting right drops the last bit, so i has the same bits as `i // 2` plus its own last bit.

**Dry run:** `dp[5]` (101) = `dp[2]` (10, one bit) + 1 = 2.

```python
def count_bits(n):
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

**Number of 1 Bits** for a single integer (Kernighan's trick, one loop per set bit):

```python
def hamming_weight(x):
    count = 0
    while x:
        x &= x - 1
        count += 1
    return count
```

**Reverse Bits** (32-bit): take the lowest bit of x and push it onto the result, 32 times.

```python
def reverse_bits(x):
    res = 0
    for _ in range(32):
        res = (res << 1) | (x & 1)
        x >>= 1
    return res
```

**Complexity:** Counting Bits O(n). Hamming weight O(number of set bits). Reverse Bits O(32).

**Say it in 60 seconds (Counting Bits):** "The bit count of i equals the bit count of i shifted right by one, plus whether i's last bit is 1. Since i shifted right is smaller, it's already computed, so it's a one-line DP and O(n) overall."

---

### E4. Missing Number

**Problem in one sentence:** an array holds n distinct numbers from 0 to n with one missing. Find it.

**Key insight:** `XOR of 0..n` XOR `XOR of nums`, or `n(n+1)/2 - sum`. Every present number cancels with its index, leaving the missing one. XOR avoids overflow in fixed-width languages.

**Dry run** on `[3, 0, 1]`: start with x = 3 (n). Index 0, value 3: x = 3 ^ 0 ^ 3 = 0. Index 1, value 0: x = 0 ^ 1 ^ 0 = 1. Index 2, value 1: x = 1 ^ 2 ^ 1 = 2. Answer 2.

```python
def missing_number(nums):
    x = len(nums)
    for i, v in enumerate(nums):
        x ^= i ^ v
    return x
```

**Say it in 60 seconds:** "If I XOR all indices 0 to n together with all values, every number that's present appears twice and cancels, so only the missing number remains. I start with n because indices only go to n minus 1. The sum formula works too, but XOR can't overflow in languages with fixed-size integers. O(n), O(1)."

---

### E5. Sum of Two Integers without + (Python needs a 32-bit mask)

**Key insight:** `a ^ b` adds without carries, and `(a & b) << 1` is the carries. Repeat until there are no carries. Python integers never overflow, so a negative carry would loop forever. The 32-bit mask stops the loop, and the last line converts a 32-bit result back to a Python negative number when needed.

**Dry run** on `a = 1`, `b = 2`: `a ^ b = 3`, carry `(1 & 2) << 1 = 0`. No carry, answer 3.

```python
def get_sum(a, b):
    mask = 0xFFFFFFFF
    while b & mask:
        a, b = a ^ b, (a & b) << 1
    return a & mask if b > 0 else a
```

**Say it in 60 seconds:** "XOR adds two numbers bit by bit while ignoring carries, and AND shifted left by one gives exactly the carries. I repeat, adding the carries back in, until there are none. In Java or Go that's the whole solution. In Python integers are unbounded, so I limit the loop to 32 bits with a mask, and if the carry ran off the top, I return the masked value, which gives the right two's-complement answer."

---

### E6. Subsets via bitmask

`for m in range(1 << n): [nums[i] for i in range(n) if m >> i & 1]`. Each integer from 0 to 2^n - 1 is one subset: bit i says whether `nums[i]` is included.

**Dry run** on `[a, b]`: masks 00, 01, 10, 11 give `[]`, `[a]`, `[b]`, `[a, b]`.

```python
def subsets_bitmask(nums):
    n = len(nums)
    return [[nums[i] for i in range(n) if m >> i & 1] for m in range(1 << n)]
```

**Systems tie-in:** bitmaps and Bloom filters (ClickHouse bloom skip indexes, which I used on product/store/attr), permission bitmasks, and consistent-hash ring positions. A **Bloom filter** is a bit array plus a few hash functions that answers "definitely not present" or "maybe present" using a few bits per key. A ClickHouse skip index uses it to skip blocks of rows that can't contain a filtered value. A **permission bitmask** stores many yes/no flags in one integer, checked with `&`.

---

## F. Math essentials

### The idea

A handful of number facts come up as building blocks or follow-ups. Know the name, the one-line idea, and the complexity.

- **GCD:** `math.gcd`. The greatest common divisor, found by Euclid's algorithm (`gcd(a, b) = gcd(b, a % b)`), O(log min(a, b)). LCM = `a * b // gcd`.
- **Sieve of Eratosthenes** for primes ≤ n: O(n log log n). Cross out multiples of each prime starting from its square.
- **Fast power:** `pow(a, b, mod)`. Square-and-multiply in O(log b).
- **Modular arithmetic:** `(a + b) % m`. In Python, integers don't overflow; in Go they do, so reduce after every multiplication.
- **Reservoir sampling** (pick k from a stream of unknown length): keep item i with probability k/i. Good for "sample logs uniformly".
- **Random pick with weight:** prefix sums + binary search.
- Pow(x, n), Sqrt(x) by binary search, Happy Number (cycle detection with fast/slow pointers), Plus One, Multiply Strings (grade-school multiplication into a result array of length m + n).

```python
def primes_up_to(n):
    is_prime = [True] * (n + 1)
    is_prime[0:2] = [False, False]
    for i in range(2, math.isqrt(n) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i, p in enumerate(is_prime) if p]

def fast_pow(a, b, mod):
    result = 1
    a %= mod
    while b:
        if b & 1:
            result = result * a % mod
        a = a * a % mod
        b >>= 1
    return result
```

**Dry run (fast power)** for 3^5 mod 7: b = 5 (101). Bit 0 is 1, so result = 3, a = 9 % 7 = 2. Bit 1 is 0, a = 4. Bit 2 is 1, result = 3 × 4 % 7 = 5. Check: 3^5 = 243, and 243 % 7 = 5.

### F1. Random Pick with Weight

**Problem in one sentence:** pick index i with probability proportional to `w[i]`.

**Key insight:** lay the weights end to end on a number line using prefix sums. A uniform random point on that line lands in segment i with probability `w[i] / total`. Binary search finds the segment.

**Dry run:** `w = [1, 3]`, prefix `[1, 4]`. A random x in [0, 4): below 1 picks index 0 (probability 1/4), otherwise index 1 (3/4).

```python
class WeightedPicker:
    def __init__(self, w):
        self.prefix = list(accumulate(w))
    def pick(self):
        x = random.random() * self.prefix[-1]
        return bisect.bisect_right(self.prefix, x)
```

**Complexity:** O(n) setup, O(log n) per pick.

### F2. Reservoir sampling

**Problem in one sentence:** choose k items uniformly at random from a stream whose length you don't know in advance, using O(k) memory.

**Key insight:** keep the first k items. For item i (counting from 1), replace a random slot with probability k/i. Every item ends up in the sample with probability k/n.

**Dry run** with k = 1 on a stream `a, b, c`: keep a. At b, replace with probability 1/2. At c, replace with probability 1/3. So c is kept with probability 1/3, and b with probability 1/2 × 2/3 = 1/3, and a with 1/2 × 2/3 = 1/3.

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

**Complexity:** O(n) time, O(k) space.

**Say it in 60 seconds:** "I can't store the stream, so I keep a reservoir of k items. The first k go straight in. For the i-th item after that, I draw a random number from 1 to i, and if it's at most k, the new item replaces that slot. By induction, after i items each one has been kept with probability k over i. It's the standard way to sample logs uniformly from a stream of unknown size."
