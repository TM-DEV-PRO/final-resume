# 03.3 Trees, BST, trie

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right
```

---

## A. How to think about tree problems

Almost every tree problem is one of two shapes:

1. **Return info up (post-order):** "what does my subtree tell my parent?" Height, whether it's balanced, max path through here, LCA found. Write `dfs(node) -> info`, combine the left and right results, and update a global answer if needed.
2. **Pass info down (pre-order):** "what does my parent tell me?" Current path sum, allowed min/max range (BST validation), depth, max so far (good nodes).

Level questions ("level order", "right view", "zigzag", "min depth") use **BFS** with a queue, processing `len(queue)` nodes per level.

Traversals: pre-order (node, L, R), in-order (L, node, R; **sorted for a BST**), post-order (L, R, node), level-order (BFS).

---

## B. Core problems

### B1. Max Depth, Invert, Same Tree, Symmetric

```python
def max_depth(root):
    return 0 if not root else 1 + max(max_depth(root.left), max_depth(root.right))

def invert(root):
    if root:
        root.left, root.right = invert(root.right), invert(root.left)
    return root

def is_same(p, q):
    if not p or not q:
        return p is q
    return p.val == q.val and is_same(p.left, q.left) and is_same(p.right, q.right)
```

### B2. Diameter of Binary Tree (return up, update global)
**Intuition:** the longest path through a node = left height + right height. Return height up.

```python
def diameter(root):
    best = 0
    def height(n):
        nonlocal best
        if not n:
            return 0
        l, r = height(n.left), height(n.right)
        best = max(best, l + r)
        return 1 + max(l, r)
    height(root)
    return best
```
O(n). The same shape gives **Balanced Binary Tree** (return -1 for unbalanced) and **Binary Tree Maximum Path Sum**:

```python
def max_path_sum(root):
    best = float("-inf")
    def gain(n):
        nonlocal best
        if not n:
            return 0
        l = max(gain(n.left), 0)       # drop negative branches
        r = max(gain(n.right), 0)
        best = max(best, n.val + l + r)
        return n.val + max(l, r)       # a path going up can use only one side
    gain(root)
    return best
```

### B3. Level Order Traversal (BFS)

```python
def level_order(root):
    if not root:
        return []
    res, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            n = q.popleft()
            level.append(n.val)
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
        res.append(level)
    return res
```
Right Side View: the last element of each level. Zigzag: reverse alternate levels.

### B4. Lowest Common Ancestor (binary tree)
**Intuition:** if p and q are in different subtrees of a node, that node is the LCA. Return a found node up.

```python
def lca(root, p, q):
    if not root or root is p or root is q:
        return root
    l, r = lca(root.left, p, q), lca(root.right, p, q)
    if l and r:
        return root
    return l or r
```
O(n). **BST version:** walk down. If both are smaller go left, if both are larger go right, else the current node is the LCA. O(h).

### B5. Validate BST (pass range down)

```python
def is_valid_bst(root, lo=float("-inf"), hi=float("inf")):
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return is_valid_bst(root.left, lo, root.val) and is_valid_bst(root.right, root.val, hi)
```
Common bug: only comparing with direct children.

### B6. Kth Smallest in BST (in-order, iterative)

```python
def kth_smallest(root, k):
    st, cur = [], root
    while st or cur:
        while cur:
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right
```
O(h + k). Follow-up, frequent queries with inserts: augment each node with its subtree size, giving O(h) per query.

### B7. Construct Tree from Preorder + Inorder
**Intuition:** `preorder[0]` is the root. Its index in inorder splits left and right. Use a hashmap for O(1) index lookups.

```python
def build_tree(preorder, inorder):
    idx = {v: i for i, v in enumerate(inorder)}
    it = iter(preorder)
    def build(lo, hi):
        if lo > hi:
            return None
        v = next(it)
        node = TreeNode(v)
        node.left = build(lo, idx[v] - 1)
        node.right = build(idx[v] + 1, hi)
        return node
    return build(0, len(inorder) - 1)
```
O(n).

### B8. Serialize / Deserialize Binary Tree
Pre-order with a null marker.

```python
class Codec:
    def serialize(self, root):
        out = []
        def dfs(n):
            if not n:
                out.append("#"); return
            out.append(str(n.val)); dfs(n.left); dfs(n.right)
        dfs(root)
        return ",".join(out)

    def deserialize(self, data):
        it = iter(data.split(","))
        def build():
            v = next(it)
            if v == "#":
                return None
            n = TreeNode(int(v))
            n.left, n.right = build(), build()
            return n
        return build()
```

### B9. Path Sum III (count paths with sum k, any downward path)
Prefix sums on the root-to-node path, using a hashmap (same idea as subarray sum = k). Add on entry, remove on exit (backtrack).

```python
def path_sum(root, target):
    count = defaultdict(int); count[0] = 1
    def dfs(n, cur):
        if not n:
            return 0
        cur += n.val
        res = count[cur - target]
        count[cur] += 1
        res += dfs(n.left, cur) + dfs(n.right, cur)
        count[cur] -= 1
        return res
    return dfs(root, 0)
```

### B10. Count Good Nodes, Subtree of Another Tree, Binary Tree Cameras (greedy post-order), Vertical Order (BFS with column index), Flatten to Linked List (reverse post-order).

---

## C. BST operations

- **Search / insert:** O(h). h = log n when balanced, n when skewed.
- **Delete:** if the node has 2 children, replace it with its in-order successor (min of the right subtree) and delete that.
- **Balanced trees:** AVL (strict), red-black (used by Java TreeMap and C++ std::map), and B-trees / B+ trees (databases; high fan-out means few disk reads). Oracle DB and MySQL InnoDB indexes are B+ trees. Mention that in system design.
- In Python there's no built-in TreeMap. Use `bisect` on a sorted list (O(n) insert) or `sortedcontainers.SortedList` if allowed.

---

## D. Trie (prefix tree)

**Intuition:** share common prefixes. Insert and search are O(L), independent of how many words are stored. Use it for autocomplete, prefix counts, spell check, IP routing (longest prefix match), and searching many words in a grid.

```python
class TrieNode:
    __slots__ = ("children", "end")
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            node = node.children.setdefault(c, TrieNode())
        node.end = True

    def _walk(self, s):
        node = self.root
        for c in s:
            node = node.children.get(c)
            if not node:
                return None
        return node

    def search(self, word):
        n = self._walk(word)
        return bool(n and n.end)

    def starts_with(self, prefix):
        return self._walk(prefix) is not None
```

### D1. Add and Search Words (`.` is a wildcard)
DFS over children when you hit `.`. Worst case O(26^L), typical O(L).

```python
def search_wild(node, word, i=0):
    if i == len(word):
        return node.end
    c = word[i]
    if c == ".":
        return any(search_wild(ch, word, i + 1) for ch in node.children.values())
    nxt = node.children.get(c)
    return bool(nxt) and search_wild(nxt, word, i + 1)
```

### D2. Word Search II (find all dictionary words in a grid, hard)
**Intuition:** running Word Search per word is too slow. Build a trie of the words and DFS the grid once, walking the trie alongside. Prune: remove trie leaves once found.

```python
def find_words(board, words):
    root = TrieNode()
    for w in words:
        node = root
        for c in w:
            node = node.children.setdefault(c, TrieNode())
        node.end = w                      # store the word itself
    R, C, res = len(board), len(board[0]), []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent.children[ch]
        if node.end:
            res.append(node.end)
            node.end = False              # avoid duplicates
        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and board[nr][nc] in node.children:
                dfs(nr, nc, node)
        board[r][c] = ch
        if not node.children and not node.end:
            parent.children.pop(ch)       # prune

    for r in range(R):
        for c in range(C):
            if board[r][c] in root.children:
                dfs(r, c, root)
    return res
```

### D3. Autocomplete top 3 (Search Suggestions System)
Store the top-3 suggestions at each trie node during insert (sorted words), or sort the words and use binary search for the prefix range. At system-design scale: precompute top-k per prefix offline, serve from a cache, and update in batches.

### D4. Maximum XOR of Two Numbers (bitwise trie)
Insert numbers bit by bit from the MSB. For each number, greedily walk the opposite bit. O(n · 32).

### D5. Longest word in dictionary, Replace Words, Palindrome Pairs (hard).

---

## E. Segment tree and Fenwick tree (know the idea, rarely coded)

- **Fenwick (BIT):** prefix sums with point updates, O(log n) each. `i += i & -i` to update, `i -= i & -i` to query.
- **Segment tree:** range queries (sum, min, max) with updates, O(log n). Lazy propagation for range updates.
- When to use: "range sum with updates," "count of smaller numbers after self" (BIT on ranks), "my calendar."

```python
class BIT:
    def __init__(self, n):
        self.t = [0] * (n + 1)
    def update(self, i, delta):      # 1-indexed
        while i < len(self.t):
            self.t[i] += delta
            i += i & -i
    def query(self, i):              # sum of [1..i]
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s
```
