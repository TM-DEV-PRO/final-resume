# 03.1 Arrays, strings, hashing, two pointers, sliding window, prefix sums, binary search

<div class="callout note">
<b>How to use this page</b>
<ul>
<li><b>What it covers:</b> the seven patterns that solve most array and string problems: hashing, prefix sums, two pointers, sliding window, binary search, string tricks and Kadane's algorithm.</li>
<li><b>When to read it:</b> first among the topic files. These patterns show up inside harder problems in every other file.</li>
<li><b>What to memorise:</b> the sliding-window template, the binary-search "first true" template, the prefix-sum-plus-hashmap trick, and the rule "negative numbers break sliding window".</li>
<li><b>How each section is laid out:</b> the idea with an analogy, the signals that point to it, a hand-traced example, the template, complexity, common mistakes, then the problems. Each problem has a one-line restatement, the key insight, a dry run, code, complexity and a 60-second spoken version.</li>
</ul>
</div>

Imports assumed by every snippet on this page:

```python
from collections import Counter, defaultdict
import bisect
```

---

## A. Hashing

### The idea

A **hashmap** (a Python `dict`) stores key-value pairs and finds any key in O(1) time on average. A **hash set** (a Python `set`) is the same thing with keys only. The trick is to trade memory for time: instead of searching the whole array to answer "have I seen X before?" or "how many times has X appeared?", you keep a record as you go and look it up instantly.

**Analogy:** a coat check. You don't search every hook for your coat. You hand over a ticket number and the attendant goes straight to the right hook. The hash function is the rule that turns your key into a hook number.

### When to recognise it

- The problem says "seen before", "duplicate", "frequency", "count", "anagram" or "group by".
- The brute force has a nested loop where the inner loop is only searching for one value.
- You need to remember something about earlier elements while scanning once.

### Hand-traced example

Find whether any two numbers in `[3, 8, 5, 1]` add up to 9. Keep a set of numbers already seen, and for each new number check whether its partner (9 minus it) is already in the set.

```text
step  x   partner = 9 - x   seen before step   partner in seen?
1     3   6                 {}                 no, add 3
2     8   1                 {3}                no, add 8
3     5   4                 {3, 8}             no, add 5
4     1   8                 {3, 8, 5}          yes -> answer (8, 1)
```

### Template

```python
def scan_with_memory(items):
    seen = {}                       # key -> whatever you need later (index, count, ...)
    for i, x in enumerate(items):
        key = f(x)                  # what you would search for
        if key in seen:
            ...                     # found it in O(1)
        seen[x] = i                 # record x for future elements
```

**Complexity:** O(n) time, because each element does a constant amount of work. O(n) space, because the map can hold every element.

### Common mistakes

- Inserting the current element **before** checking for its partner, which lets an element pair with itself (target 6 and a single 3).
- Using a mutable `list` as a dict key. Lists can't be hashed. Convert to a `tuple` first.
- Forgetting that hashing is O(1) only on average. If asked, say worst case is O(n) per lookup with adversarial collisions, which is why some languages randomise their hash seed.

---

### A1. Two Sum

**Problem in one sentence:** given a list of numbers and a target, return the indices of the two numbers that add up to the target.

**Key insight:** for each number `x`, the only number that can complete it is `target - x`. So instead of trying every pair, ask a hashmap "have I already seen `target - x`?"

**Steps:** walk once. For each `x`, check whether `target - x` is already in the map. If not, store `x → index`.

**Dry run** on `nums = [3, 2, 4]`, `target = 6`:

```text
i  x  need = 6 - x  seen (before)    action
0  3  3             {}               3 not seen, store {3: 0}
1  2  4             {3: 0}           4 not seen, store {3: 0, 2: 1}
2  4  2             {3: 0, 2: 1}     2 seen at index 1 -> return [1, 2]
```

Notice step 0: `need` is 3 and `x` is 3, but the map is still empty, so we don't wrongly pair index 0 with itself.

```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
```

**Complexity:** O(n) time, one pass with O(1) lookups. O(n) space for the map.

**Follow-up, sorted input:** use two pointers with O(1) space (section C).

**Say it in 60 seconds:** "The brute force tries every pair, which is O(n²). The observation is that for each number there is exactly one partner that works, `target - x`. So I walk the array once and keep a map from value to index. Before inserting the current number, I check whether its partner is already in the map. If it is, I return both indices. Checking before inserting stops a number pairing with itself. That's O(n) time and O(n) space. If the input were sorted, I'd switch to two pointers for O(1) space."

---

### A2. Group Anagrams

**Problem in one sentence:** given a list of words, group together the words that are rearrangements of each other ("eat", "tea", "ate").

**Key insight:** two words are anagrams exactly when they have the same letter counts. So compute a **signature** for each word and use it as a hashmap key. Words with the same signature land in the same bucket.

**Steps:** the key is the sorted string (O(k log k)) or a 26-count tuple (O(k)), where k is the word length.

**Dry run** on `["eat", "tea", "tan", "ate", "nat", "bat"]`, writing the signature as letter counts:

```text
word  signature (non-zero counts)  bucket after this word
eat   a1 e1 t1                     {aet: [eat]}
tea   a1 e1 t1                     {aet: [eat, tea]}
tan   a1 n1 t1                     {aet: [...], ant: [tan]}
ate   a1 e1 t1                     aet bucket gets ate
nat   a1 n1 t1                     ant bucket gets nat
bat   a1 b1 t1                     new bucket abt: [bat]
result: [[eat, tea, ate], [tan, nat], [bat]]
```

```python
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - 97] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())
```

**Complexity:** O(n·k) time for n words of length k. O(n·k) space to store the groups. The count array assumes lowercase a to z. For Unicode, use `tuple(sorted(s))` or a `Counter` frozen into a sorted tuple.

**Say it in 60 seconds:** "Anagrams have identical letter counts, so I turn each word into a signature and group by it. I use a 26-length count tuple rather than sorting each word, which makes each signature O(k) instead of O(k log k). A defaultdict from signature to list collects the groups, and I return its values. Total time is O(n·k). The tuple is needed because lists can't be dict keys."

---

### A3. Top K Frequent Elements

**Problem in one sentence:** return the k values that appear most often in an array.

**Key insight:** a frequency can never exceed n, the length of the array. So instead of sorting by frequency (O(n log n)), drop each value into a bucket numbered by its frequency, then read buckets from highest to lowest. That is **bucket sort**, and it is O(n).

**Steps:** count, then bucket sort by frequency, then walk buckets from high to low. The heap alternative is O(n log k).

**Dry run** on `nums = [1, 1, 1, 2, 2, 3]`, `k = 2`:

```text
count    = {1: 3, 2: 2, 3: 1}
buckets  = index 0:[]  1:[3]  2:[2]  3:[1]  4:[]  5:[]  6:[]
walk f = 6, 5, 4: empty
f = 3: take 1   -> out = [1]
f = 2: take 2   -> out = [1, 2], length is k, return
```

```python
def top_k_frequent(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for x, f in count.items():
        buckets[f].append(x)
    out = []
    for f in range(len(buckets) - 1, 0, -1):
        for x in buckets[f]:
            out.append(x)
            if len(out) == k:
                return out
    return out
```

**Complexity:** O(n) time, because counting is one pass and the buckets have n + 1 slots. O(n) space.

**Follow-up at scale (logs across machines):** count per machine, merge counts, then use a heap. Or approximate with a **Count-Min Sketch** (a small fixed-size table of counters that over-estimates but never under-estimates frequencies) plus a heap of the current top k.

**Say it in 60 seconds:** "First I count frequencies with a Counter. Sorting by count would be O(n log n), but frequencies are bounded by n, so I can bucket sort: bucket i holds the values that appear i times. Then I walk buckets from n down to 1 and collect values until I have k. That's O(n) time and space. A min-heap of size k is the alternative at O(n log k), and it's the better choice when the data is streaming and I can't hold all buckets."

---

### A4. Longest Consecutive Sequence

**Problem in one sentence:** in an unsorted array, find the length of the longest run of consecutive integers (like 1, 2, 3, 4), in O(n).

**Key insight:** only start counting from a number that is the **beginning** of a run, meaning `x - 1` is not present. That way each run is walked exactly once, from its start.

**Steps:** put everything in a set. Only start counting from `x` if `x - 1` is not in the set. Each number is visited at most twice: once in the outer loop and once while extending a run.

**Dry run** on `[100, 4, 200, 1, 3, 2]`:

```text
x     x - 1 in set?   action                     best
100   99: no          count 100 -> length 1      1
4     3: yes          skip (not a run start)     1
200   199: no         length 1                   1
1     0: no           1, 2, 3, 4 -> length 4     4
3     2: yes          skip                       4
2     1: yes          skip                       4
```

```python
def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 not in s:
            y = x
            while y + 1 in s:
                y += 1
            best = max(best, y - x + 1)
    return best
```

**Complexity:** O(n) time. The inner `while` looks like it makes this O(n²), but it only runs from run starts, so across the whole loop it advances at most n times in total. O(n) space for the set.

**Say it in 60 seconds:** "Sorting would give O(n log n), but they want O(n). I put all numbers in a set. Then for each number I check if `x - 1` exists. If it does, x is in the middle of a run and I skip it. If not, x starts a run, and I walk `x + 1`, `x + 2` while they exist. Each number is touched at most twice, once as a candidate and once while extending, so it's O(n) overall."

---

### A5. Product of Array Except Self (no division)

**Problem in one sentence:** return an array where each position holds the product of every other element, without using division.

**Key insight:** the answer at i is (product of everything to the left of i) × (product of everything to the right of i). Both can be built with running products in two passes.

**Steps:** `out[i]` = product of prefix before i × product of suffix after i. Two passes, reusing the output array.

**Dry run** on `[1, 2, 3, 4]`:

```text
forward pass (out[i] = product of everything left of i)
i  out[i] = pre  then pre *= nums[i]
0  1             pre = 1
1  1             pre = 2
2  2             pre = 6
3  6             pre = 24
out = [1, 1, 2, 6]

backward pass (multiply by product of everything right of i)
i  out[i] *= suf      then suf *= nums[i]
3  6 * 1  = 6         suf = 4
2  2 * 4  = 8         suf = 12
1  1 * 12 = 12        suf = 24
0  1 * 24 = 24        suf = 24
out = [24, 12, 8, 6]
```

```python
def product_except_self(nums):
    n = len(nums)
    out = [1] * n
    pre = 1
    for i in range(n):
        out[i] = pre
        pre *= nums[i]
    suf = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suf
        suf *= nums[i]
    return out
```

**Complexity:** O(n) time for two passes. O(1) extra space, because the output array doesn't count.

**Say it in 60 seconds:** "Division fails when there's a zero, and they ban it anyway. The value at i is the left product times the right product. In a forward pass I write the running product of everything before i into the output. In a backward pass I keep a running product of everything after i and multiply it in. Two passes, O(n) time, and no extra array besides the output."

---

## B. Prefix sums

### The idea

A **prefix sum** array `P` stores the running total: `P[0] = 0`, `P[1] = a[0]`, `P[2] = a[0] + a[1]`, and so on. Then the sum of any range is one subtraction: `sum(i..j) = P[j+1] - P[i]`.

**Analogy:** a car's odometer. To know how far you drove between Delhi and Agra, you don't add up every kilometre. You subtract the odometer reading at Delhi from the reading at Agra.

The powerful extension: if you need to count subarrays with sum k, then a subarray ending at j has sum k exactly when some earlier prefix equals `P[j] - k`. So keep a hashmap of "how many times have I seen each prefix sum" and look up `P[j] - k`.

### When to recognise it

- "Sum of subarray equals k", "count subarrays", "range sum query".
- The array has **negative numbers**, so sliding window doesn't work.
- "Longest subarray with equal 0s and 1s" (turn it into a sum problem).
- Many range-sum queries on an array that doesn't change.

### Hand-traced example

Array `[2, -1, 3, 1]`. Prefix sums: `P = [0, 2, 1, 4, 5]`. Sum of indices 1 to 3 is `P[4] - P[1] = 5 - 2 = 3`, which matches `-1 + 3 + 1 = 3`.

### Template

```python
def count_subarrays_with_sum(nums, k):
    seen = defaultdict(int)
    seen[0] = 1            # the empty prefix, so a subarray starting at index 0 is counted
    total = ans = 0
    for x in nums:
        total += x
        ans += seen[total - k]
        seen[total] += 1
    return ans
```

**Complexity:** O(n) time, one pass with O(1) map operations. O(n) space for the map.

### Common mistakes

- Forgetting `seen[0] = 1`. Without it, subarrays that start at index 0 are never counted.
- Updating the map **before** looking up, which can count an empty subarray when k is 0.
- For "longest subarray" variants, overwriting the stored index. Store only the **first** index for each prefix so the subarray is as long as possible.

---

### B1. Subarray Sum Equals K (works with negatives, so no sliding window)

**Problem in one sentence:** count how many contiguous subarrays add up to exactly k, where numbers may be negative.

**Key insight:** a subarray from i+1 to j has sum k exactly when `prefix[j] - prefix[i] = k`, which means `prefix[i] = prefix[j] - k`. So at each step, the number of good subarrays ending here equals how many earlier prefixes equalled `total - k`.

**Dry run** on `nums = [1, -1, 1]`, `k = 1`:

```text
x    total  look up count[total - k]   ans  count after update
                                             {0: 1} (start)
1    1      count[0] = 1               1    {0: 1, 1: 1}
-1   0      count[-1] = 0              1    {0: 2, 1: 1}
1    1      count[0] = 2               3    {0: 2, 1: 2}
answer 3: [1], [1, -1, 1], and the last [1]
```

The negative number made the running total go down, which is exactly the case where sliding window fails.

```python
def subarray_sum(nums, k):
    count = defaultdict(int)
    count[0] = 1           # empty prefix
    total = ans = 0
    for x in nums:
        total += x
        ans += count[total - k]
        count[total] += 1
    return ans
```

**Complexity:** O(n) time, O(n) space.

**Variants:** "divisible by k" uses `total % k` as the key. "Longest subarray with sum k" stores the *first* index of each prefix.

**Say it in 60 seconds:** "Sliding window doesn't work because negatives mean the sum isn't monotonic as the window grows. Instead I use prefix sums. A subarray ending at j sums to k when an earlier prefix equals the current prefix minus k. So I keep a map from prefix sum to how many times I've seen it, seeded with 0 seen once for the empty prefix. At each element I add `count[total - k]` to the answer, then record the current total. One pass, O(n) time and space."

---

### B2. Range Sum Query 2D (immutable)

**Problem in one sentence:** given a fixed grid of numbers, answer many queries "what is the sum of this rectangle?" in O(1) each.

**Key insight:** build a 2D prefix sum where `P[r][c]` is the sum of the rectangle from the top-left corner to just before `(r, c)`. Any rectangle is then four lookups, using inclusion-exclusion: take the big rectangle, subtract the strip above and the strip to the left, and add back the corner you subtracted twice.

Build: `P[r+1][c+1] = grid[r][c] + P[r][c+1] + P[r+1][c] - P[r][c]`. Query `(r1, c1, r2, c2) = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]`.

**Dry run** on `grid = [[1, 2], [3, 4]]`:

```text
P (3 x 3, row 0 and column 0 are zeros)
      c=0  c=1  c=2
r=0   0    0    0
r=1   0    1    3        P[1][2] = 2 + 0 + 1 - 0 = 3
r=2   0    4    10       P[2][2] = 4 + 3 + 4 - 1 = 10
query the single cell (1, 1): P[2][2] - P[1][2] - P[2][1] + P[1][1] = 10 - 3 - 4 + 1 = 4
```

```python
class NumMatrix:
    def __init__(self, grid):
        R, C = len(grid), len(grid[0])
        self.P = [[0] * (C + 1) for _ in range(R + 1)]
        for r in range(R):
            for c in range(C):
                self.P[r + 1][c + 1] = grid[r][c] + self.P[r][c + 1] + self.P[r + 1][c] - self.P[r][c]

    def sum_region(self, r1, c1, r2, c2):
        P = self.P
        return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]
```

**Complexity:** build O(m·n), each query O(1). O(m·n) space.

**Say it in 60 seconds:** "Because the grid never changes, I precompute a 2D prefix sum with one extra row and column of zeros so I never go out of bounds. Each cell of P is the sum of the rectangle above-left of it. A query takes the big rectangle, subtracts the part above and the part to the left, and adds back the top-left corner that was subtracted twice. Build is O(m·n) once, then every query is O(1). If the grid could change, I'd switch to a 2D Fenwick tree."

---

### B3. Contiguous Array (equal 0s and 1s)

**Problem in one sentence:** in a binary array, find the longest contiguous subarray with equal numbers of 0s and 1s.

**Key insight:** replace every 0 with -1. Now "equal counts" means "sum is 0". A subarray has sum 0 when the prefix sum at its end equals the prefix sum just before its start. So remember the **first** index where each prefix sum appeared.

**Dry run** on `[0, 1, 0]`:

```text
i  x  total (0 counts as -1)  first index seen?        best
                               first = {0: -1}
0  0  -1                       new, first[-1] = 0       0
1  1  0                        seen at -1 -> 1-(-1)=2   2
2  0  -1                       seen at 0  -> 2-0=2      2
answer 2
```

```python
def find_max_length(nums):
    first = {0: -1}
    total = best = 0
    for i, x in enumerate(nums):
        total += 1 if x else -1
        if total in first:
            best = max(best, i - first[total])
        else:
            first[total] = i
    return best
```

**Complexity:** O(n) time, O(n) space.

**Say it in 60 seconds:** "I map 0 to -1 so equal counts becomes sum zero. Then it's 'longest subarray with sum zero', which is a prefix-sum problem. I keep the first index where each running total appeared, seeded with total 0 at index -1. When I see a total again, the stretch between the two positions sums to zero, so I measure it. I never overwrite the first index, because the earliest one gives the longest subarray. O(n) time and space."

---

## C. Two pointers

### The idea

Use two indices into the same array instead of a nested loop. Either they start at both ends and move **toward each other**, or they both start at the left and move in the **same direction** at different speeds. Each step moves at least one pointer, so the total work is O(n).

**Analogy:** two people searching a sorted bookshelf for two books whose page counts add to 500. One starts at the thin end, one at the thick end. If the total is too small, the thin-end person steps toward thicker books. If too big, the thick-end person steps toward thinner ones. Neither ever needs to go back.

### When to recognise it

- The array is **sorted**, or sorting it doesn't break the problem.
- "Pair (or triple) with a given sum", "closest sum".
- "In place", "remove duplicates", "partition", "move zeros".
- Comparing from both ends: palindromes, container or water problems.

### Hand-traced example

Sorted `[1, 3, 4, 6, 9]`, find a pair summing to 10.

```text
l  r  a[l] + a[r]   decision
0  4  1 + 9 = 10    found (1, 9)
```

Target 7 instead:

```text
l  r  sum          decision
0  4  1 + 9 = 10   too big, r -= 1
0  3  1 + 6 = 7    found (1, 6)
```

### Template

```python
def pair_with_sum(a, target):           # a is sorted
    l, r = 0, len(a) - 1
    while l < r:
        s = a[l] + a[r]
        if s == target:
            return l, r
        if s < target:
            l += 1                      # need bigger, so move the small side up
        else:
            r -= 1                      # need smaller, so move the big side down
    return None
```

**Complexity:** O(n) time, because each step moves a pointer and they meet after at most n steps. O(1) space. Add O(n log n) if you have to sort first.

### Common mistakes

- Using two pointers on unsorted data when the logic depends on order.
- Forgetting to skip duplicates, which produces repeated answers in 3Sum.
- Off-by-one in the loop condition: `l < r` for pairs (two different elements), `l <= r` when a single middle element matters.

---

### C1. 3Sum

**Problem in one sentence:** find all unique triples in an array that add up to zero.

**Key insight:** sort the array, fix the first number, and the remaining problem is "find pairs summing to minus that number" in a sorted range, which is two pointers. Sorting also puts duplicates next to each other so they are easy to skip.

**Steps:** sort. Fix `i`, then two pointers `l, r` on the rest. Skip duplicates for `i` and after each found triple.

**Dry run** on `[-1, 0, 1, 2, -1, -4]`, sorted to `[-4, -1, -1, 0, 1, 2]`:

```text
i=0 (-4): best pair sum reachable is 1 + 2 = 3, never reaches 4, no triples
i=1 (-1): l=2 (-1), r=5 (2): -1 - 1 + 2 = 0  -> record [-1, -1, 2], l=3, r=4
          l=3 (0),  r=4 (1): -1 + 0 + 1 = 0  -> record [-1, 0, 1],  l=4, r=3, stop
i=2 (-1): same value as i=1, skip
i=3 (0):  l=4, r=5: 0 + 1 + 2 = 3 > 0, r=4, stop
result [[-1, -1, 2], [-1, 0, 1]]
```

```python
def three_sum(nums):
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if i and nums[i] == nums[i - 1]:
            continue
        if nums[i] > 0:
            break
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                l += 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
                r -= 1
    return res
```

**Complexity:** O(n²) time, because each of n choices of `i` runs an O(n) two-pointer scan. Sorting is O(n log n), which is smaller. O(1) space besides the output.

**Say it in 60 seconds:** "Brute force is O(n³) over all triples. I sort first, which lets me fix one number and then find the other two with two pointers in linear time, so O(n²) total. If the sum is too small I move the left pointer right, if too big I move the right pointer left. For uniqueness, I skip an `i` equal to the previous one, and after recording a triple I advance `l` past equal values. I also break early once `nums[i]` is positive, because three positives can't sum to zero."

---

### C2. Container With Most Water

**Problem in one sentence:** given vertical lines of different heights, pick two that, together with the x-axis, hold the most water.

**Key insight:** the water level is limited by the **shorter** line. If you move the taller line inward, the width shrinks and the height can't go up (it's still capped by the shorter line), so the area can only get worse. So always move the shorter line.

**Dry run** on `h = [1, 8, 6, 2, 5, 4, 8, 3, 7]` (first few steps):

```text
l  r  width  min height  area  best  move
0  8  8      1           8     8     h[0]=1 < h[8]=7, l += 1
1  8  7      7           49    49    h[1]=8 > 7, r -= 1
1  7  6      3           18    49    r -= 1
1  6  5      8           40    49    equal heights, r -= 1
... continues, best stays 49
```

```python
def max_area(h):
    l, r, best = 0, len(h) - 1, 0
    while l < r:
        best = max(best, (r - l) * min(h[l], h[r]))
        if h[l] < h[r]:
            l += 1
        else:
            r -= 1
    return best
```

**Complexity:** O(n) time, O(1) space.

**Say it in 60 seconds:** "Brute force checks all pairs in O(n²). I start with the widest container, both ends. The area is width times the shorter height. Moving the taller side inward can never help, because the width shrinks and the height is still capped by the shorter side. So I always move the shorter side and track the best area. Each step discards one line for good, so it's O(n)."

---

### C3. Trapping Rain Water

**Problem in one sentence:** given bar heights, compute how much rain water gets trapped between the bars.

**Key insight:** the water above bar i is `min(tallest on the left, tallest on the right) - h[i]`. With two pointers, whichever side currently has the smaller maximum is the limiting side, so its water amount is already decided and you can process it.

**Dry run** on `h = [3, 0, 2, 0, 4]`:

```text
l  r  h[l] < h[r]?  update               water
0  4  3 < 4 yes     lmax = 3, +0         0
1  4  0 < 4 yes     lmax = 3, +3         3
2  4  2 < 4 yes     lmax = 3, +1         4
3  4  0 < 4 yes     lmax = 3, +3         7
l == r, stop. answer 7
```

```python
def trap(h):
    l, r = 0, len(h) - 1
    lmax = rmax = water = 0
    while l < r:
        if h[l] < h[r]:
            lmax = max(lmax, h[l])
            water += lmax - h[l]
            l += 1
        else:
            rmax = max(rmax, h[r])
            water += rmax - h[r]
            r -= 1
    return water
```

**Complexity:** O(n) time, O(1) space.

**Say it in 60 seconds:** "Water above a bar is the smaller of the tallest bar to its left and the tallest to its right, minus its own height. The simple version precomputes left-max and right-max arrays in O(n) space. To get O(1) space I use two pointers. If the left bar is shorter than the right bar, then the right side has something at least as tall as the left max, so the left max is the limit, and I can add `lmax - h[l]` and move left. Otherwise I do the mirror on the right."

---

### C4. Sort Colors (Dutch national flag)

**Problem in one sentence:** sort an array that contains only 0s, 1s and 2s, in place, in one pass.

**Key insight:** keep three regions: everything before `lo` is 0, everything after `hi` is 2, and `mid` scans the unknown middle. A 0 goes to the front, a 2 goes to the back, a 1 stays.

Three pointers: `lo` (next 0 slot), `mid` (scan), `hi` (next 2 slot). Don't advance `mid` after swapping with `hi`, because the value that came from `hi` hasn't been examined yet.

**Dry run** on `[2, 0, 1]`:

```text
array      lo mid hi  a[mid]  action
[2, 0, 1]  0  0   2   2       swap with hi -> [1, 0, 2], hi = 1 (mid stays)
[1, 0, 2]  0  0   1   1       mid = 1
[1, 0, 2]  0  1   1   0       swap with lo -> [0, 1, 2], lo = 1, mid = 2
mid > hi, stop. result [0, 1, 2]
```

```python
def sort_colors(a):
    lo = mid = 0
    hi = len(a) - 1
    while mid <= hi:
        if a[mid] == 0:
            a[lo], a[mid] = a[mid], a[lo]; lo += 1; mid += 1
        elif a[mid] == 1:
            mid += 1
        else:
            a[mid], a[hi] = a[hi], a[mid]; hi -= 1
```

**Complexity:** O(n) time in one pass, O(1) space.

**Say it in 60 seconds:** "Counting sort works in two passes, but one pass is the classic ask. I keep three regions: zeros before `lo`, twos after `hi`, and an unknown middle scanned by `mid`. A zero swaps to `lo` and both advance. A one just advances `mid`. A two swaps with `hi` and `hi` shrinks, but `mid` stays because the swapped-in value is still unknown. The loop ends when `mid` passes `hi`."

---

### C5. Remove duplicates in place (same-direction pointers)

**Problem in one sentence:** in a sorted array, remove duplicates in place and return how many unique values remain at the front.

**Key insight:** `write` is where the next unique element goes. `read` scans. Because the array is sorted, a value is new exactly when it differs from the last value written.

**Dry run** on `[1, 1, 2, 3, 3]`:

```text
read  nums[read]  last written  action               write  array front
                                                     1      [1]
1     1           1             duplicate, skip      1      [1]
2     2           1             copy to index 1      2      [1, 2]
3     3           2             copy to index 2      3      [1, 2, 3]
4     3           3             duplicate, skip      3      [1, 2, 3]
return 3
```

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write
```

**Complexity:** O(n) time, O(1) space.

**Say it in 60 seconds:** "Since the array is sorted, duplicates are adjacent. I keep a slow `write` pointer for where the next unique value goes and a fast `read` pointer that scans. When `read` finds a value different from the last one written, I copy it to `write` and advance. At the end, `write` is the count of unique values. This same shape solves 'move zeros' and 'remove element'."

---

## D. Sliding window

### The idea

A **window** is a contiguous stretch `[l, r]` of the array or string. You grow it by moving `r` right, and shrink it by moving `l` right. You never move either pointer backwards, so each element enters the window once and leaves once, giving O(n).

This only works when the condition is **monotonic**: if a window is invalid, making it bigger keeps it invalid (or, for "shortest" problems, if a window is valid, making it bigger keeps it valid). That property lets you safely discard the left side.

**Analogy:** a caterpillar crawling along a branch. The head stretches forward to eat. When the body gets too long (the window breaks the rule), the tail pulls in. The caterpillar never walks backwards.

### When to recognise it

- "Longest / shortest / count of **contiguous** subarray or substring" with a condition.
- "At most k distinct", "without repeating", "at most k replacements".
- Fixed size: "every window of size k" (permutation in string, moving average).
- **Not** when numbers can be negative and the condition is a sum. Use prefix sums then.

### Hand-traced example

Longest substring of `"eceba"` with at most 2 distinct characters. The state is a count of characters in the window, and "valid" means at most 2 characters have a non-zero count.

```text
r  char  counts after adding   valid?  shrink                     window   best
0  e     e1                    yes                                "e"      1
1  c     e1 c1                 yes                                "ec"     2
2  e     e2 c1                 yes                                "ece"    3
3  b     e2 c1 b1              no      drop e (l=1), still 3 keys
                                       drop c (l=2), now e1 b1     "eb"     3
4  a     e1 b1 a1              no      drop e (l=3)                "ba"     3
answer 3 ("ece")
```

### Template (variable window, longest valid)

```python
def longest_valid(s):
    state = defaultdict(int)
    l = best = 0
    for r, c in enumerate(s):
        state[c] += 1                 # add s[r]
        while not valid(state):       # shrink until valid
            state[s[l]] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best
```

For "shortest valid window", flip it: expand until valid, then shrink **while still valid**, recording the minimum inside the loop.

**Complexity:** O(n) time, because `l` and `r` each move at most n times. O(alphabet) or O(k) space for the counts.

### Common mistakes

- Using sliding window on sums with negative numbers. The window sum can drop when you add an element, so shrinking is not safe.
- Recording the answer in the wrong place: for "longest", record after the shrink loop. For "shortest", record inside it.
- Counting distinct keys with `len(state)` but never deleting keys whose count drops to 0.
- Off-by-one in window length. It is `r - l + 1`.

---

### D1. Longest Substring Without Repeating Characters

**Problem in one sentence:** find the length of the longest substring with no repeated character.

**Key insight:** remember the last index where each character appeared. When you see a character that is already inside the current window, jump `l` to just past its previous position, in one move instead of shrinking one step at a time.

**Dry run** on `"abba"` (the tricky case):

```text
r  c  last[c] before  inside window?          l  last after       best
0  a  none            no                      0  {a:0}            1
1  b  none            no                      0  {a:0, b:1}       2
2  b  1               1 >= l=0 yes, l = 2     2  {a:0, b:2}       2
3  a  0               0 >= l=2? no, keep l    2  {a:3, b:2}       2
answer 2
```

At r = 3, the old `a` at index 0 is outside the window already. Without the `last[c] >= l` check, `l` would jump **backwards** to 1, which is wrong.

```python
def length_of_longest_substring(s):
    last = {}
    l = best = 0
    for r, c in enumerate(s):
        if c in last and last[c] >= l:
            l = last[c] + 1           # jump left past the duplicate
        last[c] = r
        best = max(best, r - l + 1)
    return best
```

**Complexity:** O(n) time, O(alphabet) space.

**Say it in 60 seconds:** "This is a sliding window where the window must contain distinct characters. I store the last index of each character. When the new character was last seen inside the window, I jump the left edge to one past that index. The `>= l` check matters: if the earlier occurrence is already outside the window, I must not move `l` backwards. I update the best length at every step. One pass, O(n)."

---

### D2. Longest Repeating Character Replacement (at most k changes)

**Problem in one sentence:** you may change up to k characters in a string. Find the longest substring that can be made of one repeated letter.

**Key insight:** in a window, keep the most common letter and change the rest. The window is valid if `length - maxFreq ≤ k`. `maxFreq` never has to decrease, because a stale (too high) maximum only stops the window from growing. It can never produce a wrong, larger answer, since the best answer only improves when a real higher frequency appears.

**Dry run** on `s = "AABABBA"`, `k = 1`:

```text
r  c  counts       maxf  len  len - maxf  action          best
0  A  A1           1     1    0           ok              1
1  A  A2           2     2    0           ok              2
2  B  A2 B1        2     3    1           ok              3
3  A  A3 B1        3     4    1           ok              4
4  B  A3 B2        3     5    2 > 1       drop A, l=1     4
5  B  A2 B3        3     5    2 > 1       drop A, l=2     4
6  A  A2 B3        3     5    2 > 1       drop B, l=3     4
answer 4
```

```python
def character_replacement(s, k):
    count = defaultdict(int)
    l = maxf = best = 0
    for r, c in enumerate(s):
        count[c] += 1
        maxf = max(maxf, count[c])
        while (r - l + 1) - maxf > k:
            count[s[l]] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best
```

**Complexity:** O(n) time, O(26) space.

**Say it in 60 seconds:** "In any window I'd keep the most frequent letter and replace the others, so the window is valid when its length minus the max frequency is at most k. I grow the right side and shrink the left while it's invalid. The subtle part is that I never decrease `maxf` when shrinking. That's safe because a stale max only stops the window from growing, and the answer only gets bigger when a genuinely larger frequency shows up. It's O(n)."

---

### D3. Minimum Window Substring

**Problem in one sentence:** find the shortest substring of s that contains every character of t, including repeats.

**Key insight:** track how many distinct characters of t are fully satisfied (`have`) versus how many need to be (`required`). Expand right until all are satisfied, then shrink left as far as possible while still satisfied, recording the shortest window.

**Steps:** `need` counts of t. Track `have` = number of chars whose need is met. Expand right; when all are met, shrink left while still valid, recording the minimum.

**Dry run** on `s = "ADOBECODEBANC"`, `t = "ABC"` (key moments only; need is A1 B1 C1, required 3):

```text
r   char  event                                          best
5   C     first time have = 3, window "ADOBEC" (len 6)   6
          shrink: dropping A breaks it, have = 2, l = 1
10  A     have = 3 again, window [1..10] (len 10)
          shrink past D, O, B (B still 1), E -> "CODEBA" (len 6, not better)
          dropping C breaks it, l = 6
12  C     have = 3, window [6..12] "ODEBANC" (len 7)
          shrink: "DEBANC" 6, "EBANC" 5 -> best 5, "BANC" 4 -> best 4
          dropping B breaks it
answer "BANC"
```

```python
def min_window(s, t):
    if not t:
        return ""
    need = Counter(t)
    window = defaultdict(int)
    have, required = 0, len(need)
    best = (float("inf"), 0, 0)
    l = 0
    for r, c in enumerate(s):
        window[c] += 1
        if c in need and window[c] == need[c]:
            have += 1
        while have == required:
            if r - l + 1 < best[0]:
                best = (r - l + 1, l, r)
            window[s[l]] -= 1
            if s[l] in need and window[s[l]] < need[s[l]]:
                have -= 1
            l += 1
    return "" if best[0] == float("inf") else s[best[1]:best[2] + 1]
```

**Complexity:** O(|s| + |t|) time, because each pointer crosses s once and building `need` is O(|t|). O(alphabet) space.

**Say it in 60 seconds:** "I count what t needs. While scanning s with the right pointer, I count what the window has, and I keep a single number `have` for how many distinct characters are fully satisfied. When `have` equals the number of distinct characters in t, the window is valid, so I record it if it's the shortest and then shrink from the left. The moment a needed count drops below its requirement, `have` goes down and I resume expanding. Tracking `have` avoids comparing two whole maps every step, so it's linear."

---

### D4. Permutation in String (fixed window)

**Problem in one sentence:** does s contain any rearrangement of p as a contiguous substring?

**Key insight:** a permutation of p has exactly p's letter counts and exactly p's length. So slide a window of fixed size `len(p)` over s and compare 26-count arrays. Or track the number of matching counts for O(n).

**Dry run** on `p = "ab"`, `s = "eidbaooo"`:

```text
window  counts       equals need {a1, b1}?
"ei"    e1 i1        no
"id"    i1 d1        no
"db"    d1 b1        no
"ba"    b1 a1        yes -> True
```

```python
def check_inclusion(p, s):
    if len(p) > len(s):
        return False
    need = [0] * 26
    window = [0] * 26
    for c in p:
        need[ord(c) - 97] += 1
    for r, c in enumerate(s):
        window[ord(c) - 97] += 1
        if r >= len(p):
            window[ord(s[r - len(p)]) - 97] -= 1
        if window == need:
            return True
    return False
```

**Complexity:** O(26·n) time, which is O(n), because each comparison is 26 entries. O(1) space. The "matches counter" version avoids the 26-entry compare and is strictly O(n).

**Say it in 60 seconds:** "Any permutation of p has p's length and p's letter counts. So I slide a window of exactly `len(p)` over s, adding the new character on the right and removing the one that falls off the left. After each step I compare the window's 26 counts with p's counts. Comparing 26 numbers is constant, so the whole thing is O(n). For a tighter version I keep a count of how many letters currently match and update it incrementally."

---

### D5. Max Consecutive Ones III, Fruit Into Baskets, Subarrays with K distinct

**Problem in one sentence (the hard one):** count subarrays that contain **exactly** k distinct numbers.

**Key insight:** "exactly K" is hard to slide directly, because adding an element can move you from too few to just right to too many. But "at most K" is easy to slide. And `exactly(K) = atMost(K) - atMost(K - 1)`. That's a key trick worth memorising.

Inside `at_most`, `res += r - l + 1` counts every valid subarray **ending at r**: they start at `l`, `l + 1`, ..., `r`.

The two easier relatives use the plain template. **Max Consecutive Ones III** is "longest window with at most k zeros". **Fruit Into Baskets** is "longest window with at most 2 distinct values".

**Dry run** on `nums = [1, 2, 1, 2, 3]`, `k = 2`:

```text
at_most(2):
r  x  window after shrink  subarrays ending at r  running total
0  1  [1]                  1                      1
1  2  [1,2]                2                      3
2  1  [1,2,1]              3                      6
3  2  [1,2,1,2]            4                      10
4  3  3 distinct, shrink to [2,3]   2             12

at_most(1):
r  window   count  total
0  [1]      1      1
1  [2]      1      2
2  [1]      1      3
3  [2]      1      4
4  [3]      1      5

exactly(2) = 12 - 5 = 7
```

```python
def subarrays_with_k_distinct(nums, k):
    def at_most(k):
        count = defaultdict(int)
        l = res = 0
        for r, x in enumerate(nums):
            if count[x] == 0:
                k -= 1
            count[x] += 1
            while k < 0:
                count[nums[l]] -= 1
                if count[nums[l]] == 0:
                    k += 1
                l += 1
            res += r - l + 1       # all subarrays ending at r
        return res
    return at_most(k) - at_most(k - 1)
```

Here `k` inside `at_most` is used as "distinct slots still free". It goes negative when the window holds too many distinct values.

**Complexity:** O(n) time, two linear passes. O(n) space for counts.

**Say it in 60 seconds:** "Counting windows with exactly k distinct values doesn't slide cleanly, but 'at most k' does. So I compute atMost(k) minus atMost(k-1). In atMost, I grow the window, shrink while it has more than k distinct values, and then add `r - l + 1`, because every subarray ending at r and starting anywhere from l to r is valid. Two linear passes, O(n)."

**When sliding window fails:** negative numbers with a sum target. Use prefix sums + hashmap (B1).

---

## E. Binary search

### The idea

Binary search finds a boundary by halving the search range each step. It works whenever there is a **monotonic predicate**: a yes/no question whose answers, in order, look like `false false false true true true`. You want the first `true`.

That predicate can be about an **index** ("is `a[i] >= target`?"), about an **answer value** ("can we ship everything in D days with capacity X?"), or about a rotated array ("is this half sorted?").

**Analogy:** guessing a number between 1 and 100 when the other person says "higher" or "lower". You always guess the middle, and you never need more than 7 guesses, because 2⁷ = 128 > 100.

### When to recognise it

- The input is sorted, or "rotated sorted".
- "Find the minimum X such that ...", "maximize the minimum", "minimize the maximum".
- The constraints allow a value range up to 10⁹, too big to try each value, but checking one value is cheap.
- The expected complexity contains a log.

### Hand-traced example

Find the first index in `[1, 3, 5, 7, 9]` where the value is at least 5. The predicate `a[i] >= 5` reads `F F T T T`.

```text
lo  hi  mid  a[mid]  ok?   update
0   5   2    5       yes   hi = 2
0   2   1    3       no    lo = 2
lo == hi == 2 -> answer index 2
```

### Template (first index where `ok(i)` is true)

```python
def first_true(lo, hi, ok):     # search in [lo, hi); returns hi if none
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

Always ask: is my range inclusive or exclusive? Does `mid` move toward both ends so the loop ends? In this template `hi` is exclusive, `ok(mid)` true keeps `mid` as a candidate (`hi = mid`), and false discards it (`lo = mid + 1`). Since `mid` rounds down, `hi = mid` always shrinks the range, so the loop can't get stuck.

**Complexity:** O(log n) calls to `ok`. If `ok` costs O(n) (as in "binary search on the answer"), the total is O(n log range).

### Common mistakes

- Infinite loops from writing `lo = mid` while `mid` rounds down. When `hi = lo + 1`, `mid` equals `lo` forever.
- Mixing inclusive and exclusive bounds in the same function.
- Choosing a search range that doesn't contain the answer, such as starting capacity at 1 when it must be at least the heaviest package.
- Forgetting the predicate must be monotonic. If it isn't, binary search gives nonsense.

---

### E1. Search in Rotated Sorted Array

**Problem in one sentence:** a sorted array was rotated at an unknown point (for example `[4, 5, 6, 7, 0, 1, 2]`). Find a target's index in O(log n).

**Key insight:** when you cut a rotated array in the middle, at least one half is always properly sorted. You can tell which by comparing the ends. Then check whether the target lies inside the sorted half's range. If it does, search there. If not, search the other half.

**Dry run** on `nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 0`:

```text
lo  hi  mid  nums[mid]  sorted half          target in it?        move
0   6   3    7          left [4..7]          4 <= 0 < 7? no       lo = 4
4   6   5    1          left [0..1]          0 <= 0 < 1? yes      hi = 4
4   4   4    0          found                                     return 4
```

```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:               # left half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                   # right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

**Complexity:** O(log n) time, O(1) space. With duplicates allowed, the worst case becomes O(n), because `nums[lo] == nums[mid]` can't tell you which half is sorted.

**Say it in 60 seconds:** "Even after rotation, splitting at the middle leaves at least one sorted half. If `nums[lo] <= nums[mid]`, the left half is sorted, otherwise the right half is. I check whether the target falls within the sorted half's range using its two endpoints. If yes, I discard the other half. If no, I discard the sorted half. Each step halves the range, so O(log n)."

---

### E2. Find Minimum in Rotated Sorted Array

**Problem in one sentence:** find the smallest element of a rotated sorted array (no duplicates) in O(log n).

**Key insight:** compare the middle with the **right end**. If `nums[mid] > nums[hi]`, the drop (where the minimum lives) is to the right of mid. Otherwise the minimum is at mid or to its left.

**Dry run** on `[4, 5, 6, 7, 0, 1, 2]`:

```text
lo  hi  mid  nums[mid] vs nums[hi]  move
0   6   3    7 > 2                  lo = 4
4   6   5    1 > 2? no              hi = 5
4   5   4    0 > 1? no              hi = 4
lo == hi = 4 -> minimum is 0
```

```python
def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]
```

**Complexity:** O(log n) time, O(1) space.

**Say it in 60 seconds:** "The minimum is where the rotation 'drops'. If the middle is bigger than the last element, the drop must be to the right, so I move `lo` past mid. Otherwise mid could itself be the minimum, so I set `hi = mid` and keep it. When the range collapses to one index, that's the minimum. I compare with the right end rather than the left because the left comparison can't distinguish an unrotated array."

---

### E3. Binary search on the answer: Koko Eating Bananas / Capacity to Ship Packages

**Problem in one sentence (shipping):** packages must ship in order within D days. Find the smallest ship capacity that makes it possible.

**Key insight:** you can't easily compute the answer directly, but you can easily **check** a guess: "with capacity X, how many days do I need?" Bigger capacity never needs more days, so "feasible(X)" is monotonic (`F F F T T T`). Binary search the smallest feasible X.

**Steps:** the answer space is `[1, max]` (Koko) or `[max(w), sum(w)]` (shipping). The lower bound is the heaviest package, because a ship smaller than that can never carry it. The upper bound ships everything in one day.

**Dry run** on `weights = [3, 2, 2, 4, 1, 4]`, `days = 3`:

```text
lo  hi  mid  greedy loading with cap = mid       days  feasible?  move
4   16  10   [3,2,2] [4,1,4]                     2     yes        hi = 10
4   10  7    [3,2,2] [4,1] [4]                   3     yes        hi = 7
4   7   5    [3,2] [2] [4,1] [4]                 4     no         lo = 6
6   7   6    [3,2] [2,4] [1,4]                   3     yes        hi = 6
lo == hi -> answer 6
```

```python
def ship_within_days(weights, days):
    def feasible(cap):
        need, cur = 1, 0
        for w in weights:
            if cur + w > cap:
                need += 1
                cur = 0
            cur += w
        return need <= days
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**Complexity:** O(n log(sum)) time: each feasibility check is O(n), and there are O(log(sum - max)) checks. O(1) space.

**Same shape:** Split Array Largest Sum, Minimum Days to Make Bouquets, Magnetic Force Between Balls (maximize the minimum, so you search for the **last** true instead of the first).

**Say it in 60 seconds:** "Computing the capacity directly is hard, but checking a given capacity is easy: load packages greedily and count days. More capacity never needs more days, so feasibility is monotonic and I can binary search the smallest feasible capacity. The range starts at the heaviest package, since anything smaller can't carry it, and ends at the total weight, which ships in one day. Each check is O(n) and there are log(sum) checks."

---

### E4. Time Based Key-Value Store (OCI favorite)

**Problem in one sentence:** build a store where `set(key, value, ts)` records a value at a time, and `get(key, ts)` returns the value set at the latest time not after `ts`.

**Key insight:** timestamps for a key arrive in increasing order, so each key's list is already sorted by time. `get` becomes "find the last entry with timestamp ≤ ts", which is `bisect_right` minus one.

**Dry run:**

```text
set("foo", "bar", 1)      store["foo"] = [(1, "bar")]
get("foo", 3)             last ts <= 3 is 1 -> "bar"
set("foo", "bar2", 4)     store["foo"] = [(1, "bar"), (4, "bar2")]
get("foo", 4)             bisect_right(ts=4) = 2, minus 1 -> index 1 -> "bar2"
get("foo", 0)             bisect_right(ts=0) = 0, minus 1 = -1 -> ""
```

```python
class TimeMap:
    def __init__(self):
        self.store = defaultdict(list)   # key -> [(ts, value)] sorted by ts

    def set(self, key, value, ts):
        self.store[key].append((ts, value))

    def get(self, key, ts):
        arr = self.store.get(key, [])
        i = bisect.bisect_right(arr, ts, key=lambda p: p[0]) - 1   # key= needs Python 3.10+
        return arr[i][1] if i >= 0 else ""
```

An older version of this page searched with `bisect_right(arr, (ts, chr(127)))`. That compares values as strings and breaks when a value sorts above `chr(127)` (any non-ASCII text, for example), so the lookup now compares only the timestamp. On Python older than 3.10, keep a separate list of timestamps per key and bisect that.

**Complexity:** `set` O(1), `get` O(log n) for n versions of that key. O(total entries) space.

**Follow-ups:** thread safety (a lock per key, or a read-write lock, see [concurrency](06_concurrency.md)). Unsorted timestamps (insert in sorted position with `insort`, or use a sorted container). Persistence (an append-only log, replayed on restart).

**Say it in 60 seconds:** "Each key maps to a list of (timestamp, value) pairs. Because the problem guarantees increasing timestamps, appending keeps each list sorted, so `set` is O(1). For `get`, I binary search for the first timestamp greater than the query and step back one, which gives the latest version at or before that time. If that index is negative, nothing existed yet and I return an empty string. That's O(log n) per get. It's essentially how a multi-version store answers 'what was the value at time T'."

---

### E5. Median of Two Sorted Arrays (hard, O(log min(m, n)))

**Problem in one sentence:** find the median of two sorted arrays combined, in logarithmic time.

**Key insight:** the median splits the combined data into a left half and a right half of equal size. Choose how many elements `i` to take from the smaller array; then the number from the other array is forced: `j = half - i`. The split is correct when everything on the left is ≤ everything on the right, which you check with just the four elements at the cut. Binary search `i`.

**Intuition, stated precisely:** partition both arrays so the left halves together hold `(m+n+1)//2` elements and every left element ≤ every right element. Binary search the cut in the smaller array.

**Dry run** on `a = [1, 3]`, `b = [2]` (swapped so `a` is the shorter: `a = [2]`, `b = [1, 3]`, half = 2):

```text
i  j  a_left  a_right  b_left  b_right  valid cut?                     move
0  2  -inf    2        3       +inf     b_left 3 <= a_right 2? no      lo = 1
1  1  2       +inf     1       3        2 <= 3 and 1 <= inf, yes
total 3 is odd -> median = max(a_left, b_left) = max(2, 1) = 2
```

```python
def find_median_sorted_arrays(a, b):
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i
        a_left = a[i - 1] if i > 0 else float("-inf")
        a_right = a[i] if i < m else float("inf")
        b_left = b[j - 1] if j > 0 else float("-inf")
        b_right = b[j] if j < n else float("inf")
        if a_left <= b_right and b_left <= a_right:
            if (m + n) % 2:
                return max(a_left, b_left)
            return (max(a_left, b_left) + min(a_right, b_right)) / 2
        if a_left > b_right:
            hi = i - 1
        else:
            lo = i + 1
```

**Complexity:** O(log min(m, n)) time, because we binary search the shorter array. O(1) space.

**Say it in 60 seconds:** "Merging is O(m + n), but they want logarithmic. The median is defined by a cut that puts half the elements on the left. If I take i from the shorter array, I must take `half - i` from the other. The cut is right when the largest left element of each array is no bigger than the smallest right element of the other. If a's left side is too big, I move i left; otherwise right. Infinity sentinels handle cuts at the edges. Once valid, the median is the max of the lefts for odd totals, or the average of max-left and min-right for even."

---

## F. String essentials

These are ideas to know by name and explain in one or two sentences. Only Encode/Decode is commonly coded in full.

- **Palindromes:** a palindrome reads the same forwards and backwards. Expand around each center (there are 2n - 1 centers: every character and every gap between characters), which is O(n²). Manacher's algorithm is O(n) but rarely required. Full code is in the [DP file](03_dsa_5_dynamic_programming.md), section F1.
- **KMP / prefix function:** pattern search in O(n + m). The idea: for each position in the pattern, precompute the longest proper prefix that is also a suffix. On a mismatch you jump back to that length instead of restarting, so the text pointer never moves backwards. Analogy: if you were reading "ABAB" and hit a mismatch, you already know the last "AB" could be the start of a new match.
- **Rabin-Karp rolling hash:** turn each window of the text into a number, and update it in O(1) as the window slides (remove the left character's contribution, add the right one). Used for substring matching and finding duplicate substrings. Watch for collisions: two different strings can share a hash, so use a double hash or verify the match.
- **Encode/Decode strings:** length-prefix each string as `len#str`. Never use a delimiter that can appear in the data.

### F1. Encode and Decode Strings

**Problem in one sentence:** turn a list of strings into one string and back, where the strings may contain any character.

**Key insight:** a delimiter alone fails because the data can contain it. Writing the **length** first tells the decoder exactly how many characters to read, so a `#` inside the data is harmless. This is how many network protocols frame messages.

**Dry run** on `["ab", "c#d"]`:

```text
encode -> "2#ab3#c#d"
decode:
i=0: next '#' at 1, length = "2" -> read s[2:4] = "ab", i = 4
i=4: next '#' at 5, length = "3" -> read s[6:9] = "c#d", i = 9
i = 9 = len, done -> ["ab", "c#d"]
```

```python
def encode(strs):
    return "".join(f"{len(s)}#{s}" for s in strs)

def decode(s):
    out, i = [], 0
    while i < len(s):
        j = s.index("#", i)
        n = int(s[i:j])
        out.append(s[j + 1:j + 1 + n])
        i = j + 1 + n
    return out
```

**Complexity:** O(total characters) for both directions.

**Say it in 60 seconds:** "Any delimiter can appear inside the data, so I use length-prefixing. Each string becomes its length, a hash sign, then the string. The decoder reads digits up to the first hash, parses the length, and slices exactly that many characters, so a hash inside the payload is never misread. Then it continues from just after the slice. It's linear in the total size, and it's the same framing idea used by many wire protocols."

---

## G. Kadane (max subarray) and friends

### The idea

**Kadane's algorithm** finds the contiguous subarray with the largest sum. At each element you make one decision: extend the best subarray ending at the previous element, or start fresh here. You start fresh when the running sum has become a burden (negative).

**Analogy:** walking with a backpack of coins, some of them debts. If the backpack's total value becomes negative, you're better off dropping it and starting with an empty one at the next step.

### When to recognise it

- "Maximum (or minimum) sum contiguous subarray".
- "Best time to buy and sell once" is the same idea on price differences.
- Variants: maximum product subarray, circular maximum subarray.

### G1. Maximum Subarray

**Problem in one sentence:** find the largest sum of any non-empty contiguous subarray.

**Key insight:** the best subarray ending at position i is either just `x` or the best ending at i-1 plus `x`. Keep the better one, and track the best seen overall.

**Dry run** on `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`:

```text
x    cur = max(x, cur + x)   best
-2   -2 (start)              -2
1    max(1, -1) = 1          1
-3   max(-3, -2) = -2        1
4    max(4, 2) = 4           4
-1   3                       4
2    5                       5
1    6                       6
-5   1                       6
4    5                       6
answer 6 (subarray [4, -1, 2, 1])
```

```python
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)      # extend or restart
        best = max(best, cur)
    return best
```

**Complexity:** O(n) time, O(1) space.

**Friends:**
- **Max product subarray:** track both `max` and `min` ending here, because multiplying by a negative number turns the smallest product into the largest. Full code idea is in the [DP file](03_dsa_5_dynamic_programming.md), section B7.
- **Circular:** the answer is `max(kadane, total - min_subarray)` unless all numbers are negative (then `total - min_subarray` would be an empty subarray, so just return kadane). The wrap-around subarray is "everything except a middle chunk", and removing the most negative middle chunk maximises it.

**Say it in 60 seconds:** "At each element, the best subarray ending here is either the element alone or the element added to the best subarray ending just before. If the previous running sum is negative, it only hurts, so I restart. I keep the overall best as I go. I initialise with the first element rather than zero so an all-negative array returns its largest element. O(n) time, O(1) space."

---

## Common mistakes (the whole page)

- Sliding window with negative numbers (wrong pattern). Use prefix sums and a hashmap.
- Binary search infinite loops: `lo = mid` with `mid = (lo + hi) // 2` when `hi = lo + 1`.
- Mutating a dict while iterating it. Python raises `RuntimeError: dictionary changed size during iteration`. Iterate over `list(d.items())` if you must modify.
- Forgetting `count[0] = 1` in prefix-sum counting.
- Using `list.pop(0)` in a loop (O(n²)). Use `collections.deque`.
- Forgetting to skip duplicates in 3Sum-style problems.
- Recording the window answer in the wrong place (after the shrink loop for "longest", inside it for "shortest").
