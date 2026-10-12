# 03.3 Trees, BST, trie

<div class="callout note">
<b>How to use this page</b>
<ul>
<li><b>What it covers:</b> binary trees, binary search trees (BST), tries (prefix trees), and a short note on Fenwick and segment trees.</li>
<li><b>When to read it:</b> after the linked-list file. Tree problems are the most common "medium" in OCI loops, and almost all reduce to two recursive shapes described in section A.</li>
<li><b>What to memorise:</b> "return info up" versus "pass info down", BFS level loop with <code>len(queue)</code>, the BST range check, and the trie insert/search code.</li>
<li><b>How each problem is laid out:</b> a one-line restatement, the key insight, a dry run on a small tree, code, complexity, and a 60-second spoken version.</li>
</ul>
</div>

Imports and the node class assumed by every snippet on this page:

```python
from collections import defaultdict, deque
import bisect

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right
```

---

## Words you need

- **Binary tree:** each node has at most two children, called left and right. The top node is the **root**, and nodes with no children are **leaves**.
- **Height** of a node: the number of nodes on the longest path from it down to a leaf. **Depth**: how far it is from the root. The letter **h** in complexities means the tree's height: about log n for a balanced tree, but up to n for a skewed tree that looks like a linked list.
- **Subtree:** a node plus everything below it.
- **BST (binary search tree):** a binary tree where every value in a node's left subtree is smaller than the node, and every value in its right subtree is larger. Searching it is like a guessing game: go left if smaller, right if bigger.
- **Traversal:** visiting every node in a fixed order. **Pre-order** visits the node, then left, then right. **In-order** visits left, node, right, which gives **sorted order for a BST**. **Post-order** visits left, right, then node. **Level-order** (BFS) visits the tree row by row.
- **DFS (depth-first search):** go as deep as possible before backtracking, usually with recursion. **BFS (breadth-first search):** visit all nodes at distance 1, then distance 2, using a queue.

---

## A. How to think about tree problems

### The idea

Almost every tree problem is one of two shapes. Pick the shape first and the code nearly writes itself.

1. **Return info up (post-order):** "what does my subtree tell my parent?" Height, whether it's balanced, max path through here, LCA found. Write `dfs(node) -> info`, combine the left and right results, and update a global answer if needed.
2. **Pass info down (pre-order):** "what does my parent tell me?" Current path sum, allowed min/max range (BST validation), depth, max so far (good nodes).

Level questions ("level order", "right view", "zigzag", "min depth") use **BFS** with a queue, processing `len(queue)` nodes per level.

**Analogy:** a company org chart. "Return info up" is the CEO asking for headcount: each manager asks their reports, adds them up and adds one for themselves, then reports upward. "Pass info down" is the CEO setting a budget cap: each manager passes the remaining budget to their reports.

### When to recognise each shape

- **Return up:** "height", "depth", "diameter", "balanced", "maximum path sum", "lowest common ancestor", "count nodes with property", anything where a node's answer depends on its children's answers.
- **Pass down:** "root-to-leaf path", "path sum", "valid range", "good nodes (no bigger ancestor)", anything where a node needs to know about its ancestors.
- **BFS:** "level", "row", "right side view", "minimum depth", "nearest".

### Hand-traced example (return info up)

Height of this tree, where height of an empty node is 0:

```text
        1
       / \
      2   3
     /
    4

height(4) = 1 + max(0, 0) = 1
height(2) = 1 + max(height(4)=1, 0) = 2
height(3) = 1 + max(0, 0) = 1
height(1) = 1 + max(2, 1) = 3
```

Notice the order: children are finished before their parent, which is post-order.

### Templates

```python
def return_up(node):
    if not node:
        return BASE                        # e.g. 0 for height, True for balanced
    left = return_up(node.left)
    right = return_up(node.right)
    # optionally update a nonlocal "best" using left, right and node.val
    return combine(node.val, left, right)

def pass_down(node, state):
    if not node:
        return
    state = update(state, node.val)        # e.g. path sum so far, allowed range
    pass_down(node.left, state)
    pass_down(node.right, state)
```

**Complexity:** O(n) time, because each node is visited once. O(h) space for the recursion stack.

### Common mistakes

- Forgetting the `None` base case, which crashes on `node.left.val`.
- Confusing "the value I return to my parent" with "the global best". In diameter and max path sum they are different, so you need a `nonlocal best`.
- Deep skewed trees (10⁵ nodes in a line) hitting Python's recursion limit. Use an explicit stack or raise the limit.
- Comparing only with direct children in BST validation (see B5).

---

## B. Core problems

### B1. Max Depth, Invert, Same Tree, Symmetric

**Problems in one sentence each:** find the tree's height; mirror the tree left to right; check two trees are identical; check a tree is a mirror of itself.

**Key insight:** all four are "return info up" in their simplest form. Each node does O(1) work with its children's results.

**Dry run (invert)** on:

```text
before        after
    4             4
   / \           / \
  2   7         7   2
 / \               / \
1   3             3   1
```

`invert(4)` sets `4.left = invert(7)` and `4.right = invert(2)`. `invert(2)` swaps 1 and 3. The tuple assignment computes both sides first, so nothing is lost.

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

**Symmetric** is `is_same` against a mirror: compare `a.left` with `b.right` and `a.right` with `b.left`.

```python
def is_symmetric(root):
    def mirror(a, b):
        if not a or not b:
            return a is b
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)
    return mirror(root.left, root.right) if root else True
```

**Complexity:** O(n) time, O(h) space for each.

**Say it in 60 seconds (Same Tree):** "Two trees are the same if both roots are empty, or both exist with equal values and their left subtrees match and their right subtrees match. The base case `p is q` handles both-empty as true and one-empty as false in one line. Each node is compared once, so O(n) time and O(h) stack. Symmetric is the same function, comparing left with right crosswise."

---

### B2. Diameter of Binary Tree (return up, update global)

**Problem in one sentence:** find the number of edges on the longest path between any two nodes.

**Key insight:** the longest path through a node = left height + right height. But a parent can only extend a path through **one** of a node's sides. So return height up to the parent, and update a global best with `left + right` at each node.

**Dry run** on:

```text
        1
       / \
      2   3
     / \
    4   5

node  left h  right h  best = max(best, l + r)  return 1 + max(l, r)
4     0       0        0                        1
5     0       0        0                        1
2     1       1        2                        2
3     0       0        2                        1
1     2       1        3                        3
answer 3 (path 4-2-1-3, three edges)
```

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

**Complexity:** O(n) time, O(h) space.

The same shape gives **Balanced Binary Tree** (return -1 for unbalanced, so a parent can short-circuit) and **Binary Tree Maximum Path Sum** (B2b below).

**Say it in 60 seconds:** "The longest path has some highest node, and at that node it goes down the left side and the right side. So at every node, the best path through it is left height plus right height. I compute heights bottom-up, update a global best with left plus right, and return one plus the bigger side, because a parent can only continue through one branch. One pass, O(n) time, O(h) stack."

---

### B2b. Binary Tree Maximum Path Sum (hard)

**Problem in one sentence:** find the maximum sum of node values along any path, where values can be negative.

**Key insight:** same shape as diameter, with two twists. A negative branch is worse than no branch, so clamp each child's gain at 0. And the value you return up can use only one side, while the global best can use both.

**Dry run** on:

```text
     -10
     /  \
    9    20
        /  \
       15   7

node  l gain  r gain  best = max(best, val + l + r)  return val + max(l, r)
9     0       0       9                              9
15    0       0       15                             15
7     0       0       15                             7
20    15      7       42                             35
-10   9       35      max(42, 34) = 42               25
answer 42 (path 15-20-7)
```

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

**Complexity:** O(n) time, O(h) space.

**Say it in 60 seconds:** "It's the diameter pattern with sums. Each node asks its children for the best downward path sum starting at them, and treats a negative result as zero, since skipping that branch is better. The best path that peaks at this node is its value plus both gains, so I update a global best. What I return to my parent is my value plus the better single gain, because a path can't fork. I start best at negative infinity so an all-negative tree returns its largest value."

---

### B3. Level Order Traversal (BFS)

**Problem in one sentence:** return the node values level by level, as a list of lists.

**Key insight:** a queue visits nodes in order of distance from the root. To separate levels, snapshot `len(q)` at the start of each round. Exactly that many nodes belong to the current level, and everything they enqueue belongs to the next.

**Dry run** on `3(9, 20(15, 7))`:

```text
round  queue at start  len  popped      level      queue at end
1      [3]             1    3           [3]        [9, 20]
2      [9, 20]         2    9, 20       [9, 20]    [15, 7]
3      [15, 7]         2    15, 7       [15, 7]    []
answer [[3], [9, 20], [15, 7]]
```

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

**Variants:** Right Side View is the last element of each level. Zigzag reverses alternate levels. Minimum Depth returns the round number of the first leaf found.

**Complexity:** O(n) time, O(width) space, which can be up to n/2 for the last level of a full tree.

**Say it in 60 seconds:** "Level questions mean BFS. I start a queue with the root. Each round, I read the queue length once, because that's exactly the number of nodes on the current level. I pop that many, record their values, and push their children, which form the next level. I use a deque so popleft is O(1). Right side view is just the last value of each level."

---

### B4. Lowest Common Ancestor (binary tree)

**Problem in one sentence:** given two nodes p and q, find their deepest shared ancestor (a node can be its own ancestor).

**Key insight:** if p and q are in different subtrees of a node, that node is the LCA. Return a found node up: each call returns p or q if it found one in its subtree, or the LCA if it found both, or None.

**Dry run** on the tree below with `p = 6`, `q = 4`:

```text
          3
        /   \
       5     1
      / \   / \
     6   2 0   8
        / \
       7   4

lca(6) -> 6 (it is p)
lca(2) -> left lca(7) = None, right lca(4) = 4 -> returns 4
lca(5) -> left = 6, right = 4, both found -> returns 5
lca(1) -> None (neither below)
lca(3) -> left = 5, right = None -> returns 5
answer 5
```

```python
def lca(root, p, q):
    if not root or root is p or root is q:
        return root
    l, r = lca(root.left, p, q), lca(root.right, p, q)
    if l and r:
        return root
    return l or r
```

**Complexity:** O(n) time, O(h) space.

**BST version:** walk down. If both are smaller go left, if both are larger go right, else the current node is the LCA (the two values split here). O(h).

**Say it in 60 seconds:** "I recurse and return whatever I find: p or q if the current node is one of them, otherwise the results from both sides. If both sides return something, p and q are on different sides, so this node is the lowest common ancestor. If only one side returns something, I pass it up, because either the LCA is down there or I'm carrying one of the targets. If a node is p and q is below it, returning p immediately is still correct. O(n) time. For a BST I'd just walk down by comparing values, O(h)."

---

### B5. Validate BST (pass range down)

**Problem in one sentence:** check whether a binary tree satisfies the BST rule everywhere, not just between parent and child.

**Key insight:** every node must lie in a range set by **all** its ancestors. Going left tightens the upper bound to the parent's value. Going right tightens the lower bound. Pass the range down.

**Dry run** on a tree that fools the "compare with children" approach:

```text
      5
     / \
    4   6
       / \
      3   7

node  allowed range   ok?
5     (-inf, inf)     yes
4     (-inf, 5)       yes
6     (5, inf)        yes
3     (5, 6)          no, 3 < 5 -> False
```

Node 3 is a valid left child of 6, but it sits in 5's right subtree, so it must be greater than 5.

```python
def is_valid_bst(root, lo=float("-inf"), hi=float("inf")):
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return is_valid_bst(root.left, lo, root.val) and is_valid_bst(root.right, root.val, hi)
```

Common bug: only comparing with direct children. An equally good alternative is an in-order traversal that checks each value is strictly greater than the previous.

**Complexity:** O(n) time, O(h) space.

**Say it in 60 seconds:** "Checking each node against its children isn't enough, because a node deep in the right subtree must still be bigger than the root. So I pass down an allowed open interval. The root allows anything. Going left, the upper bound becomes the parent's value. Going right, the lower bound becomes the parent's value. If any node falls outside its interval, it's invalid. O(n) time. Alternatively, an in-order walk must produce a strictly increasing sequence."

---

### B6. Kth Smallest in BST (in-order, iterative)

**Problem in one sentence:** return the k-th smallest value in a BST.

**Key insight:** in-order traversal of a BST visits values in sorted order, so the k-th node visited is the answer. Doing it iteratively lets you stop early without visiting the whole tree.

**Dry run** on `3(1(-, 2), 4)` with `k = 3`:

```text
action                         stack     k
push 3, push 1, left is None   [3, 1]
pop 1 (visit), k=2, go right   [3]       2
push 2, left is None           [3, 2]
pop 2 (visit), k=1             [3]       1
pop 3 (visit), k=0 -> return 3
```

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

**Complexity:** O(h + k) time, because we walk down to the smallest and then visit k nodes. O(h) space.

**Follow-up, frequent queries with inserts:** augment each node with its subtree size, giving O(h) per query: if the left subtree has `L` nodes and `k ≤ L`, go left; if `k == L + 1`, it's this node; otherwise go right with `k - L - 1`.

**Say it in 60 seconds:** "In-order traversal of a BST yields sorted values, so I want the k-th in-order node. I do it iteratively with a stack: push all the way left, pop and count, then move to the right child. When the count hits k, I return. That stops early, so it's O(h + k) rather than O(n). If the tree changes and queries are frequent, I'd store subtree sizes so each query is O(h)."

---

### B7. Construct Tree from Preorder + Inorder

**Problem in one sentence:** rebuild a binary tree from its pre-order and in-order traversals (values are unique).

**Key insight:** `preorder[0]` is the root. Its index in inorder splits left and right: everything before it in the in-order list is the left subtree, everything after is the right. Use a hashmap for O(1) index lookups, and consume the pre-order list in order with an iterator.

**Dry run** on `preorder = [3, 9, 20, 15, 7]`, `inorder = [9, 3, 15, 20, 7]`:

```text
call          next preorder value  inorder index  left range  right range
build(0, 4)   3                    1              (0, 0)      (2, 4)
build(0, 0)   9                    0              (0, -1)     (1, 0)    both empty
build(2, 4)   20                   3              (2, 2)      (4, 4)
build(2, 2)   15                   2              empty       empty
build(4, 4)   7                    4              empty       empty
tree: 3(9, 20(15, 7))
```

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

The left subtree must be built **before** the right, because pre-order lists the whole left subtree before any right node.

**Complexity:** O(n) time thanks to the index map (without it, searching the in-order list makes it O(n²)). O(n) space.

**Say it in 60 seconds:** "Pre-order gives roots first, and in-order tells me what's left and right of each root. I map each value to its in-order index. Then I recurse on an in-order range: take the next pre-order value as the root, split the range at that root's in-order position, build the left part, then the right part. Building left before right matters because pre-order lists the whole left subtree first. O(n) time with the map."

---

### B8. Serialize / Deserialize Binary Tree

**Problem in one sentence:** convert a tree to a string and back, exactly.

**Key insight:** pre-order with a null marker. Recording `#` for every missing child makes the shape unambiguous, so a single pre-order list is enough to rebuild the tree. The decoder reads tokens in the same order the encoder wrote them.

**Dry run** on `1(2, 3(4, 5))`:

```text
serialize: visit 1, 2, (2 has no children) #, #, 3, 4, #, #, 5, #, #
string: "1,2,#,#,3,4,#,#,5,#,#"
deserialize reads 1 -> left reads 2 -> left # , right # -> right reads 3 -> 4(#, #), 5(#, #)
```

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

In `n.left, n.right = build(), build()`, Python evaluates the left `build()` first, which is required here.

**Complexity:** O(n) time and space for both directions.

**Say it in 60 seconds:** "I write a pre-order traversal and emit a marker for every null child, joined by commas. Because nulls are explicit, the sequence uniquely describes the shape. To rebuild, I read tokens with an iterator in the same order: a marker means None, otherwise I create the node and recursively build its left then right. Both directions are O(n). BFS with null markers works too and is what LeetCode's display format uses."

---

### B9. Path Sum III (count paths with sum k, any downward path)

**Problem in one sentence:** count downward paths (not necessarily from root or to a leaf) whose values add up to a target.

**Key insight:** along any root-to-node path, this is exactly "count subarrays with sum k" from the [arrays file](03_dsa_1_arrays_hashing_search.md) (section B1). Keep prefix sums of the current path in a hashmap. Add on entry, remove on exit (backtrack), so sibling branches don't see each other's sums.

**Dry run** on `1(2, 3)` with `target = 3`:

```text
count starts {0: 1}
visit 1: cur = 1, count[1 - 3 = -2] = 0, res 0, count {0:1, 1:1}
  visit 2: cur = 3, count[0] = 1, res 1 (path 1-2), count adds 3
           leave 2: remove 3
  visit 3: cur = 4, count[1] = 1, res 1 (path 3 alone)
           leave 3: remove 4
leave 1: remove 1
answer 2
```

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

**Complexity:** O(n) time, O(h) space for the map and stack. The brute force (start a search at every node) is O(n²) on a skewed tree.

**Say it in 60 seconds:** "Any downward path is a contiguous piece of some root-to-node path, so it's subarray-sum-equals-k on a tree. As I go down, I keep a running prefix sum and a map of how many times each prefix sum has appeared on the current path. At each node, paths ending here with the target sum equal the count of `cur - target`. I add the current prefix before going into children and remove it on the way back out, so other branches don't see it. O(n) time."

---

### B10. Count Good Nodes, Subtree of Another Tree, Binary Tree Cameras (greedy post-order), Vertical Order (BFS with column index), Flatten to Linked List (reverse post-order)

One sentence of insight for each, so you can attempt them cold:

- **Count Good Nodes:** a node is good if no ancestor is larger. Pass the max-so-far **down** and count nodes with `val >= max_so_far`.
- **Subtree of Another Tree:** at each node of the big tree, run `is_same` against the small tree. O(m·n). For O(m + n), serialize both with null markers and do a substring search.
- **Binary Tree Cameras:** post-order returns one of three states (needs a camera, has a camera, covered). Place a camera at a parent only when a child needs one. Greedy works because placing cameras as high as possible covers more nodes.
- **Vertical Order:** BFS carrying a column index (left child is column - 1, right child is column + 1), group values by column, then output columns from left to right.
- **Flatten to Linked List:** visit in reverse pre-order (right, left, node) and keep a `prev` pointer. Set `node.right = prev` and `node.left = None`. Each node gets linked to the one that comes after it in pre-order.

```python
def good_nodes(root):
    def dfs(n, mx):
        if not n:
            return 0
        good = 1 if n.val >= mx else 0
        mx = max(mx, n.val)
        return good + dfs(n.left, mx) + dfs(n.right, mx)
    return dfs(root, float("-inf"))
```

**Say it in 60 seconds (Good Nodes):** "A node is good if it's at least as large as every ancestor. That's a pass-down problem: I carry the maximum value seen on the path from the root. At each node I count it if its value is at least that max, update the max, and recurse into both children. O(n) time, O(h) stack."

---

## C. BST operations

### The idea

A BST keeps the "left smaller, right larger" rule at every node, so search, insert and delete each follow one root-to-leaf path. That's O(h), which is O(log n) only if the tree stays balanced.

**Analogy:** a dictionary you open in the middle, then flip left or right depending on whether your word comes before or after the page you landed on.

- **Search / insert:** O(h). h = log n when balanced, n when skewed (insert 1, 2, 3, 4 in order and you get a linked list).
- **Delete:** if the node has 0 or 1 child, replace it with that child. If the node has 2 children, replace its value with its in-order successor (min of the right subtree) and delete that successor, which has at most one child.
- **Balanced trees:** AVL (strict balance, faster lookups), red-black (looser balance, cheaper inserts; used by Java TreeMap and C++ std::map), and B-trees / B+ trees (databases). A B+ tree node holds hundreds of keys, so the tree is very shallow and a lookup needs only a few disk reads. Oracle DB and MySQL InnoDB indexes are B+ trees. Mention that in system design.
- In Python there's no built-in TreeMap. Use `bisect` on a sorted list (O(n) insert) or `sortedcontainers.SortedList` if allowed.

### Hand-traced example (delete with two children)

```text
delete 5 from:      5                 6
                   / \               / \
                  3   8     ->      3   8
                     / \               / \
                    6   9          (6 gone) 9

successor of 5 = leftmost node of the right subtree = 6
copy 6 into the root, then delete 6 from the right subtree
```

### Template

```python
def insert(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root

def delete(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete(root.right, succ.val)
    return root
```

**Complexity:** O(h) time each, O(h) recursion space.

### Common mistakes

- Assuming O(log n) without saying "if balanced".
- Forgetting to return the (possibly new) subtree root from `insert` and `delete`, so the parent never gets relinked.
- Ignoring duplicates. Decide up front whether they go left, right, or are rejected.

**Say it in 60 seconds (delete):** "I walk down comparing keys. When I find the node, there are three cases. No left child: replace it with its right child. No right child: replace it with its left child. Two children: copy the in-order successor's value, which is the leftmost node in the right subtree, and then delete that successor from the right subtree. It has no left child, so that second delete is an easy case. Every step returns the new subtree root so parents relink correctly. O(h)."

---

## D. Trie (prefix tree)

### The idea

A **trie** stores words character by character, so words with a common prefix share the same path from the root. Each node has a map from character to child and a flag saying "a word ends here". Insert and search are O(L), where L is the word length, independent of how many words are stored.

**Analogy:** a phone's contact search. As you type "Ta", the list narrows to everyone starting with "Ta", then "Tar". Each letter you type moves one step down the trie.

Use it for autocomplete, prefix counts, spell check, IP routing (longest prefix match: a router picks the most specific matching network prefix), and searching many words in a grid.

### When to recognise it

- "Prefix", "starts with", "autocomplete", "typeahead".
- "Search for many words at once" (in a grid, in a stream).
- "Wildcard search" with `.`.
- Bitwise problems that compare numbers from the top bit down (maximum XOR).

### Hand-traced example

Insert "car" and "cat", then query.

```text
root
 └ c
   └ a
     ├ r (end)
     └ t (end)

search("ca")      walk c, a -> node exists but end is False -> False
starts_with("ca") walk c, a -> node exists -> True
search("cat")     walk c, a, t -> end is True -> True
```

### Template

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

`__slots__` stops Python creating a per-object dict, which saves a lot of memory when there are millions of nodes.

**Complexity:** insert, search and starts_with are O(L). Space is O(total characters inserted) in the worst case, less when prefixes are shared.

### Common mistakes

- Treating "path exists" as "word exists". You need the `end` flag ("ca" is a prefix, not a word).
- Using a fixed 26-slot array when the input may contain other characters.
- Forgetting that a trie can use more memory than a hash set when words share few prefixes.

**Say it in 60 seconds (Implement Trie):** "Each node holds a dict of children and a flag for 'a word ends here'. Insert walks the word, creating missing children, and sets the flag on the last node. Search walks the word and returns true only if the path exists and the flag is set. Starts-with only needs the path to exist. Everything is O(L) in the word length, regardless of how many words are stored."

---

### D1. Add and Search Words (`.` is a wildcard)

**Problem in one sentence:** support adding words and searching where `.` matches any single letter.

**Key insight:** for normal letters, follow one child. When you hit `.`, try every child (DFS) and succeed if any branch succeeds. Worst case O(26^L), typical O(L).

**Dry run** with words "bad", "dad", "mad", searching ".ad":

```text
root has children b, d, m
'.' -> try b: then 'a' -> 'd' -> end True -> found, return True
(d and m are never needed thanks to short-circuit any())
```

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

**Complexity:** O(L) without wildcards. With wildcards, worst case O(26^L), but real dictionaries are sparse, so it's much less.

**Say it in 60 seconds:** "I store words in a trie. Searching is a recursive walk with an index into the pattern. A normal letter follows its single child. A dot tries every child and returns true if any branch matches the rest. At the end of the pattern I check the end-of-word flag. Without dots it's O(L). With dots the worst case branches 26 ways per dot, but `any` short-circuits on the first match."

---

### D2. Word Search II (find all dictionary words in a grid, hard)

**Problem in one sentence:** given a letter grid and a list of words, return every word that can be traced through adjacent cells without reusing a cell.

**Key insight:** running Word Search per word is too slow. Build a trie of the words and DFS the grid once, walking the trie alongside. If the current path isn't a prefix of any word, stop immediately. Prune: remove trie leaves once found, so later searches don't re-explore dead branches.

**Dry run** on the grid below with words `["oat", "ate", "eat"]`:

```text
o a
e t

start at o: o -> a (right) -> t (down): node.end = "oat", record it
start at a: a -> t (down) -> e (left): node.end = "ate", record it
start at e: e's neighbours are o and t, neither is 'a' after 'e', stop
answer ["oat", "ate"]
```

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

Marking the cell `#` while it's on the current path prevents reusing it, and restoring it afterwards is the backtracking step.

**Complexity:** O(R·C·4·3^(L-1)) in the worst case, where L is the longest word: the first step has 4 directions and later steps 3 (you can't go back). Pruning makes it much faster in practice. Trie space is O(total letters in words).

**Say it in 60 seconds:** "Searching each word separately repeats the same grid walks. Instead I put all words in a trie and run one DFS from each cell, moving down the trie as I move through the grid. If the next letter isn't a child in the trie, no word can continue, so I stop. When I reach a node that ends a word, I record it and clear the flag so it isn't found twice. I mark cells while they're on the path and restore them after. Once a trie node has no children and no word, I delete it, which prunes future searches."

---

### D3. Autocomplete top 3 (Search Suggestions System)

**Problem in one sentence:** after each character typed, return up to three lexicographically smallest products starting with the typed prefix.

**Key insight:** store the top-3 suggestions at each trie node during insert (sorted words), or sort the words and use binary search for the prefix range. In a sorted list, all words with a given prefix sit next to each other, starting at `bisect_left(prefix)`.

**Dry run** on products `["mobile", "mouse", "moneypot", "monitor", "mousepad"]`, typing "mou":

```text
sorted: mobile, moneypot, monitor, mouse, mousepad
"m"    bisect -> 0 -> mobile, moneypot, monitor
"mo"   bisect -> 0 -> mobile, moneypot, monitor
"mou"  bisect -> 3 -> mouse, mousepad
```

```python
def suggested_products(products, search_word):
    products.sort()
    res, prefix = [], ""
    for c in search_word:
        prefix += c
        i = bisect.bisect_left(products, prefix)
        res.append([p for p in products[i:i + 3] if p.startswith(prefix)])
    return res
```

**Complexity:** O(n log n) to sort, then O(L log n) for L typed characters.

At system-design scale: precompute top-k per prefix offline, serve from a cache, and update in batches. Popularity (not alphabetical order) usually decides the ranking there.

**Say it in 60 seconds:** "Sorting the products puts every word with a given prefix in one contiguous block. For each typed prefix I binary search where that block starts and take up to three words that still match. That's O(log n) per keystroke after sorting. The trie version stores the top three at every node during insert, which makes each keystroke O(1) after walking one step. In a real typeahead service I'd precompute top-k per prefix offline and serve it from a cache."

---

### D4. Maximum XOR of Two Numbers (bitwise trie)

**Problem in one sentence:** find the largest `a XOR b` among all pairs in an array.

**Key insight:** XOR is maximised by making the highest bits differ. Insert numbers bit by bit from the MSB (most significant bit) into a trie with two children per node, 0 and 1. For each number, greedily walk the opposite bit whenever it exists, because a 1 in a higher bit beats any combination of lower bits.

**Dry run** on `[3, 5]` using 3 bits (3 = 011, 5 = 101):

```text
query 3 (011) against the trie:
bit 2: 3 has 0, want 1 -> exists (from 5), cur = 100
bit 1: 3 has 1, want 0 -> exists (5 has 0), cur = 110
bit 0: 3 has 1, want 0 -> not on this path (5 has 1), take 1, cur = 110
best = 6 (3 XOR 5 = 110)
```

```python
def find_maximum_xor(nums):
    root = {}
    for x in nums:
        node = root
        for b in range(31, -1, -1):
            bit = (x >> b) & 1
            node = node.setdefault(bit, {})
    best = 0
    for x in nums:
        node, cur = root, 0
        for b in range(31, -1, -1):
            bit = (x >> b) & 1
            if 1 - bit in node:
                cur |= 1 << b
                node = node[1 - bit]
            else:
                node = node[bit]
        best = max(best, cur)
    return best
```

**Complexity:** O(n · 32) time and space.

**Say it in 60 seconds:** "Brute force is O(n²) over pairs. XOR is largest when the highest possible bit differs, so I insert every number into a binary trie from bit 31 down. For each number, I walk the trie preferring the opposite bit at each level, because a 1 in a higher position outweighs everything below it. The bits where I got the opposite form the XOR value for the best partner. That's 32 steps per number, so O(32n)."

---

### D5. Longest word in dictionary, Replace Words, Palindrome Pairs (hard)

- **Longest Word in Dictionary:** find the longest word that can be built one letter at a time from other words. Insert all words, then DFS or BFS only through nodes with `end = True`, tracking the longest (and lexicographically smallest) path.
- **Replace Words:** replace each word in a sentence with its shortest root from a dictionary. Insert the roots, then for each word walk the trie and stop at the first node with `end = True`.
- **Palindrome Pairs (hard):** find pairs i, j where `words[i] + words[j]` is a palindrome. Insert reversed words into a trie. For each word, walk it and check whether the remaining part of either the word or the trie branch is itself a palindrome.

---

## E. Segment tree and Fenwick tree (know the idea, rarely coded)

### The idea

Both answer **range queries on an array that changes**. Plain prefix sums give O(1) queries but O(n) updates, because changing one value shifts every later prefix. These trees split the array into overlapping blocks so both updates and queries touch only O(log n) blocks.

**Analogy:** a company's expense reports. Rather than re-adding every receipt each time you're asked "how much did we spend through March?", you keep monthly and quarterly subtotals. Changing one receipt updates just a few subtotals, and a question combines just a few subtotals.

- **Fenwick (BIT, binary indexed tree):** prefix sums with point updates, O(log n) each. `i += i & -i` to update, `i -= i & -i` to query. `i & -i` isolates the lowest set bit of i, which is the size of the block that index i is responsible for.
- **Segment tree:** range queries (sum, min, max) with updates, O(log n). Each node covers a range and stores the answer for it. Lazy propagation for range updates (defer pushing a change down until a query needs it).
- **When to use:** "range sum with updates", "count of smaller numbers after self" (BIT on ranks), "my calendar" (booking intervals).

### Hand-traced example

BIT over `[1, 2, 3, 4, 5]` (1-indexed). Index 4 (binary 100) covers positions 1 to 4, index 3 (011) covers only 3, index 2 (010) covers 1 and 2.

```text
query(3): i=3 add t[3] (=3), i = 3 - 1 = 2, add t[2] (=1+2=3), i = 0 -> 6
check: 1 + 2 + 3 = 6
update(2, +10): i=2 t[2] += 10, i = 2 + 2 = 4, t[4] += 10, i = 8 > n, stop
```

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

A range sum `[l..r]` is `query(r) - query(l - 1)`.

**Complexity:** update and query O(log n). O(n) space.

**Say it in 60 seconds:** "When an array changes and I still need fast range sums, prefix sums fail because one update shifts O(n) prefixes. A Fenwick tree stores partial sums where index i covers a block whose size is i's lowest set bit. A prefix query adds O(log n) blocks by repeatedly stripping the lowest bit, and an update touches O(log n) blocks by repeatedly adding it. Range sum is two prefix queries subtracted. For min or max, or for range updates, I'd use a segment tree with lazy propagation."
