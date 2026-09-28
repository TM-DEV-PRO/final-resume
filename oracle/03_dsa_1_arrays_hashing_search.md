# 03.1 Arrays, strings, hashing, two pointers, sliding window, prefix sums, binary search

Each section has the **intuition**, a **template**, and **top problems** with steps, code, and complexity.

---

## A. Hashing

**Intuition:** trade memory for time. "Have I seen X?" or "how many times?" goes from O(n) search to O(1).

### A1. Two Sum
**Steps:** walk once. For each `x`, check whether `target - x` is already in the map. If not, store `x → index`.

```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
```
Time O(n), space O(n). Follow-up, sorted input: two pointers with O(1) space.

### A2. Group Anagrams
**Steps:** the key is the sorted string (O(k log k)) or a 26-count tuple (O(k)).

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
Time O(n·k), space O(n·k).

### A3. Top K Frequent Elements
**Steps:** count, then **bucket sort** by frequency (frequency ≤ n), then walk buckets from high to low. The heap alternative is O(n log k).

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
Time O(n). Follow-up at scale (logs across machines): count per machine, merge counts, then a heap; or approximate with Count-Min Sketch + heap.

### A4. Longest Consecutive Sequence
**Steps:** put everything in a set. Only start counting from `x` if `x - 1` is not in the set (start of a run). Each number is visited at most twice.

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
Time O(n), space O(n).

### A5. Product of Array Except Self (no division)
**Steps:** `out[i]` = product of prefix before i × product of suffix after i. Two passes, reusing the output array.

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
Time O(n), space O(1) extra.

---

## B. Prefix sums

**Intuition:** `sum(i..j) = P[j+1] - P[i]`. If you need "count of subarrays with sum k," then `P[j] - P[i] = k` means you look up `P[j] - k` in a map of prefix counts.

### B1. Subarray Sum Equals K (works with negatives, so no sliding window)

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
Time O(n), space O(n). Variants: "divisible by k" uses `total % k` as the key. "Longest subarray with sum k" stores the *first* index of each prefix.

### B2. Range Sum Query 2D (immutable)
`P[r+1][c+1] = grid[r][c] + P[r][c+1] + P[r+1][c] - P[r][c]`. Query `(r1,c1,r2,c2) = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]`. Build O(mn), query O(1).

### B3. Contiguous Array (equal 0s and 1s)
Map 0 to -1. Find the longest subarray with sum 0, storing the first index of each prefix sum.

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

---

## C. Two pointers

**Intuition:** on sorted data (or for in-place compaction), two indices moving toward each other or in the same direction replace a nested loop.

### C1. 3Sum
**Steps:** sort. Fix `i`, then two pointers `l, r` on the rest. Skip duplicates for `i` and after each found triple.

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
Time O(n²), space O(1) besides the output.

### C2. Container With Most Water
**Intuition:** area is bounded by the shorter line. Moving the taller one can never help, so move the shorter one.

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
O(n).

### C3. Trapping Rain Water
**Intuition:** water at i = `min(maxLeft, maxRight) - h[i]`. With two pointers, the side with the smaller max is decided, so process it.

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
O(n) time, O(1) space.

### C4. Sort Colors (Dutch national flag)
Three pointers: `lo` (next 0 slot), `mid` (scan), `hi` (next 2 slot). Don't advance `mid` after swapping with `hi`.

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

### C5. Remove duplicates in place (same-direction pointers)
`write` is where the next unique element goes. `read` scans.

---

## D. Sliding window

**Intuition:** for contiguous ranges where the condition is **monotonic** (if a window is invalid, growing it stays invalid), expand the right side and shrink the left side while invalid. Each element enters and leaves once, so O(n).

**Template (variable window, longest valid):**

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

### D1. Longest Substring Without Repeating Characters

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
O(n) time, O(alphabet) space.

### D2. Longest Repeating Character Replacement (at most k changes)
**Intuition:** window is valid if `len - maxFreq ≤ k`. `maxFreq` never has to decrease (a stale max only keeps the window from growing, never gives a wrong larger answer).

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

### D3. Minimum Window Substring
**Steps:** `need` counts of t. Track `have` = number of chars whose need is met. Expand right; when all are met, shrink left while still valid, recording the minimum.

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
O(|s| + |t|).

### D4. Permutation in String (fixed window)
Fixed window of `len(p)`. Compare 26-count arrays, or track the number of matching counts for O(n).

### D5. Max Consecutive Ones III, Fruit Into Baskets, Subarrays with K distinct
"Exactly K" = `atMost(K) - atMost(K - 1)`. That's a key trick.

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

**When sliding window fails:** negative numbers with a sum target. Use prefix sums + hashmap (B1).

---

## E. Binary search

**Intuition:** whenever there's a **monotonic predicate** over a range (false false false true true), binary search finds the boundary in O(log n). That works on an index, on an answer value ("minimum capacity such that feasible"), or on a rotated array.

**Template (first index where `ok(i)` is true):**

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
Always ask: is my range inclusive or exclusive? Does `mid` move toward both ends so the loop ends?

### E1. Search in Rotated Sorted Array
**Steps:** one half is always sorted. Check whether the target lies inside the sorted half; if yes go there, else go to the other.

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
O(log n).

### E2. Find Minimum in Rotated Sorted Array

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

### E3. Binary search on the answer: Koko Eating Bananas / Capacity to Ship Packages
**Steps:** the answer space is `[1, max]` (or `[max(w), sum(w)]` for shipping). `feasible(x)` is monotonic, so find the smallest feasible x.

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
O(n log(sum)). Same shape: Split Array Largest Sum, Minimum Days to Make Bouquets, Magnetic Force Between Balls (maximize the minimum).

### E4. Time Based Key-Value Store (OCI favorite)
`set(key, value, ts)` with increasing timestamps; `get(key, ts)` returns the value with the largest `ts' ≤ ts`.

```python
class TimeMap:
    def __init__(self):
        self.store = defaultdict(list)   # key -> [(ts, value)] sorted by ts

    def set(self, key, value, ts):
        self.store[key].append((ts, value))

    def get(self, key, ts):
        arr = self.store.get(key, [])
        i = bisect.bisect_right(arr, (ts, chr(127))) - 1
        return arr[i][1] if i >= 0 else ""
```
set O(1), get O(log n). Follow-ups: thread safety (lock per key or RW lock); unsorted timestamps (insort, or a sorted container); persistence (append-only log).

### E5. Median of Two Sorted Arrays (hard, O(log min(m, n)))
**Intuition:** partition both arrays so the left halves together hold `(m+n+1)//2` elements and every left element ≤ every right element. Binary search the cut in the smaller array.

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

---

## F. String essentials

- **Palindromes:** expand around center (2n - 1 centers), O(n²). Manacher's is O(n) but rarely required.
- **KMP / prefix function:** pattern search in O(n + m). Know the idea: longest proper prefix that is also a suffix.
- **Rabin-Karp rolling hash:** substring matching, duplicate substrings. Watch for collisions (double hash or verify).
- **Encode/Decode strings:** length-prefix each string `len#str`. Never use a delimiter that can appear in the data.

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

---

## G. Kadane (max subarray) and friends

```python
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)      # extend or restart
        best = max(best, cur)
    return best
```
Max product subarray: track both `max` and `min` (a negative flips them). Circular: `max(kadane, total - min_subarray)` unless all are negative.

---

## Common mistakes

- Sliding window with negative numbers (wrong pattern).
- Binary search infinite loops: `lo = mid` with `mid = (lo + hi) // 2` when `hi = lo + 1`.
- Mutating a dict while iterating it.
- Forgetting `count[0] = 1` in prefix-sum counting.
- Using `list.pop(0)` in a loop (O(n²)).
