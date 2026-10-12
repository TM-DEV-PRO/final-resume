# 03.2 Linked list, stack, monotonic stack, queue, deque, heap

<div class="callout note">
<b>How to use this page</b>
<ul>
<li><b>What it covers:</b> the "linear" data structures beyond arrays: linked lists, stacks, monotonic stacks, queues, deques and heaps, with the problems interviewers ask most for each.</li>
<li><b>When to read it:</b> after the arrays file. Read the heap section again before any round with a "top k" or "merge logs" flavour, which OCI likes.</li>
<li><b>What to memorise:</b> the dummy-head trick, fast/slow pointers, the monotonic-stack template, "min-heap of size k for top k largest", and the two-heaps median.</li>
<li><b>How each section is laid out:</b> the idea with an analogy, signals, a hand-traced example, the template, complexity, common mistakes, then problems with a restatement, key insight, dry run, code, complexity and a 60-second spoken version.</li>
</ul>
</div>

Imports assumed by every snippet on this page:

```python
from collections import Counter, defaultdict, deque
import heapq
```

---

## A. Linked list

### The idea

A **linked list** is a chain of nodes where each node holds a value and a pointer to the next node. There is no index. To reach the fifth node you must walk from the head through the first four. In exchange, inserting or removing a node is O(1) once you're standing at the right place, because you only rewire pointers instead of shifting elements.

**Analogy:** a treasure hunt. Each clue tells you where the next clue is hidden. You can't jump to clue 5, but you can easily slip a new clue between clue 2 and clue 3 by changing what clue 2 says.

Two tricks solve most linked-list problems:

- **Dummy head:** a fake node placed before the real head. Whenever the head itself might be removed or replaced, the dummy gives you a stable node to hang the answer from, and you return `dummy.next`.
- **Fast/slow pointers:** two pointers that move at different speeds (fast moves two nodes per step, slow moves one). When fast reaches the end, slow is in the middle. If there is a cycle, fast eventually laps slow and they meet.

The real skill is pointer discipline: draw the boxes and arrows, and save `next` before you overwrite it.

### When to recognise it

- The input is a `ListNode`.
- "Reverse", "merge", "reorder", "remove the nth from the end", "find the middle", "detect a cycle".
- "O(1) extra space" on a list problem usually means fast/slow pointers or in-place reversal.

### Hand-traced example

Find the middle of `1 → 2 → 3 → 4 → 5` with fast/slow pointers.

```text
step  slow  fast
0     1     1
1     2     3
2     3     5      fast.next is None, stop. middle = 3
```

### Template

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow                         # second middle for even lengths
```

**Complexity:** O(n) time for one walk, O(1) space.

### Common mistakes

- Losing the rest of the list by overwriting `node.next` before saving it.
- Forgetting the dummy head, then writing special-case code for "remove the head".
- Checking `fast.next.next` without first checking `fast.next`, which crashes on `None`.
- Returning `head` after reversing. The new head is the old tail.

---

### A1. Reverse Linked List (iterative, then recursive)

**Problem in one sentence:** reverse a singly linked list and return the new head.

**Key insight:** walk the list once and flip each arrow to point backwards. You need three references at each step: the previous node (where the arrow should point), the current node, and the next node (saved before you overwrite the arrow).

**Dry run** on `1 → 2 → 3`:

```text
prev  head  action                        list state
None  1     1.next = None, prev=1, head=2  1 -> None
1     2     2.next = 1,    prev=2, head=3  2 -> 1 -> None
2     3     3.next = 2,    prev=3, head=None 3 -> 2 -> 1 -> None
return prev = 3
```

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

The one-line swap works because Python evaluates the whole right side (`prev, head, head.next`) before assigning anything, so `head.next` on the right is still the original next node.

**Complexity:** O(n) time. Iterative is O(1) space. Recursive is O(n) space for the call stack, and can hit Python's recursion limit on long lists.

**Say it in 60 seconds:** "I walk the list with a `prev` pointer that starts at None. For each node I save its next, point it back at `prev`, then advance `prev` and the current node. When the current node is None, `prev` is the new head. That's O(n) time and O(1) space. The recursive version reverses the rest first, then makes the next node point back at me, but it uses O(n) stack, so I'd use the iterative one in production."

---

### A2. Merge Two Sorted Lists

**Problem in one sentence:** merge two sorted linked lists into one sorted list.

**Key insight:** like merging two sorted piles of exam papers: always take the smaller top paper. A dummy head avoids special-casing the first node, and when one list runs out you attach the rest of the other in one step.

**Dry run** on `a = 1 → 3`, `b = 2 → 4`:

```text
a   b   pick  merged so far
1   2   1     1
3   2   2     1 2
3   4   3     1 2 3
None 4  attach rest of b -> 1 2 3 4
```

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

**Complexity:** O(m + n) time, O(1) extra space, because we relink existing nodes.

**Say it in 60 seconds:** "I keep a dummy head and a tail pointer. While both lists have nodes, I attach the smaller head to the tail and advance that list. Using `<=` keeps the merge stable. When one list is empty, I attach the remainder of the other in one assignment. I return `dummy.next`. Linear time, constant extra space."

---

### A3. Linked List Cycle and cycle start (Floyd)

**Problem in one sentence:** detect whether a linked list loops back on itself, and if so return the node where the loop begins.

**Key insight:** fast moves 2, slow moves 1. If there's a cycle, fast gains one node per step on slow inside the loop, so they must meet. To find the start, reset one pointer to the head and move both by 1; they meet at the cycle start.

Why the reset works, in words: let `a` be the distance from the head to the cycle start, `c` the cycle length, and `b` how far past the start they met. Slow walked `a + b`, fast walked twice that. The extra distance fast walked is a whole number of laps, which gives `a = k·c - b`. So walking `a` more steps from the meeting point lands exactly on the start, which is also `a` steps from the head.

**Analogy:** two runners on a track that starts with a straight road. The faster runner always catches the slower one on the loop.

**Dry run** on `1 → 2 → 3 → 4 → 5 → (back to 3)`:

```text
phase 1     slow  fast
start       1     1
step 1      2     3
step 2      3     5
step 3      4     4      meet at 4

phase 2 (slow reset to head)
            slow  fast
            1     4
step 1      2     5
step 2      3     3      meet at 3 = cycle start
check: a = 2, c = 3, b = 1, and a = 1*3 - 1 = 2
```

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

**Complexity:** O(n) time, O(1) space. A hash set of visited nodes is the simpler O(n)-space alternative.

**Same trick:** Find the Duplicate Number. Treat the array as a linked list where index `i` points to `nums[i]`. The duplicate value is where two arrows point to the same node, which is the cycle start.

**Say it in 60 seconds:** "I run two pointers, one moving one step and one moving two. If fast hits None, there's no cycle. If there is a cycle, fast gains one step per move on slow inside the loop, so they meet. To find where the cycle starts, I put one pointer back at the head and move both one step at a time. The math says the distance from the head to the start equals the distance from the meeting point to the start, modulo the loop length, so they meet exactly at the start. O(n) time and O(1) space."

---

### A4. Remove Nth From End

**Problem in one sentence:** delete the nth node counted from the end of the list, in one pass.

**Key insight:** move `fast` n steps ahead, then move both until `fast.next` is None. The gap of n nodes means `slow` stops just **before** the node to delete. Use a dummy for the "remove head" case.

**Dry run** on `1 → 2 → 3 → 4 → 5`, `n = 2` (D is the dummy):

```text
fast moves 2 ahead: slow = D, fast = 2
both move:  slow 1, fast 3 | slow 2, fast 4 | slow 3, fast 5 (fast.next is None)
slow = 3, so remove 3.next (the 4) -> 1 2 3 5
```

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next
    return dummy.next
```

**Complexity:** O(L) time in one pass, O(1) space.

**Say it in 60 seconds:** "I want the node just before the target. I start two pointers at a dummy node, move the fast one n steps ahead, then move both together until fast is on the last node. Because they're n apart, slow is now right before the node to delete, so I skip over it. The dummy handles deleting the head without special code. One pass, O(1) space."

---

### A5. Reorder List (L0 → Ln → L1 → Ln-1)

**Problem in one sentence:** rearrange `1 2 3 4 5` into `1 5 2 4 3` in place.

**Key insight:** the result alternates between the front half in order and the back half in reverse. So: find the middle (fast/slow), reverse the second half, then merge alternately. Three building blocks you already know.

**Dry run** on `1 → 2 → 3 → 4`:

```text
middle: slow stops at 2 -> first half 1 2, second half 3 4
reverse second half -> 4 3
weave: 1 4 2 3
```

```python
def reorder_list(head):
    if not head or not head.next:
        return
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    second = reverse(slow.next)
    slow.next = None
    first = head
    while second:
        n1, n2 = first.next, second.next
        first.next = second
        second.next = n1
        first, second = n1, n2
```

**Complexity:** O(n) time, O(1) space.

**Say it in 60 seconds:** "The output alternates the front half with the back half reversed. So I find the middle with fast and slow pointers, cut the list there, reverse the second half in place, and then weave the two halves by alternating nodes. Each step is linear and none needs extra memory, so it's O(n) time and O(1) space."

---

### A6. Copy List with Random Pointer

**Problem in one sentence:** deep-copy a linked list where each node also has a `random` pointer to any node (or None).

**Key insight:** the hard part is that a random pointer may point to a node you haven't copied yet. Solve it in two passes: first create every copy, then wire up `next` and `random` using a map from original to copy. Use a hashmap old → new (O(n) space), or interleave copies `A → A' → B → B'`, set randoms, then split (O(1) extra).

**Dry run** on `A(random → B) → B(random → A)`:

```text
pass 1: m = {None: None, A: A', B: B'}
pass 2: A'.next = m[B] = B',  A'.random = m[B] = B'
        B'.next = m[None] = None, B'.random = m[A] = A'
return m[A] = A'
```

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

`Node` here is the problem's class with `val`, `next` and `random`. Seeding the map with `None: None` removes all the "if pointer is None" checks.

**Complexity:** O(n) time, O(n) space for the map. The interleaving version is O(1) extra space.

**Say it in 60 seconds:** "Random pointers can point forward to nodes I haven't copied yet, so I do two passes. First I create a copy of every node and store original-to-copy in a map. Second I set each copy's next and random by looking up the originals' targets in the map. I seed the map with None mapping to None so null pointers need no special case. O(n) time and space. To get O(1) extra space, I can interleave each copy right after its original, set randoms through `node.random.next`, then unzip the lists."

---

### A7. Reverse Nodes in k-Group (hard)

**Problem in one sentence:** reverse the list in chunks of k nodes, leaving a final chunk shorter than k unchanged.

**Key insight:** for each group: check that k nodes exist, reverse them, then connect the previous group's tail to the new head. The trick that makes the reversal clean is to start `prev` at the node **after** the group, so the group's old first node automatically points to the rest of the list once reversed.

**Dry run** on `1 → 2 → 3 → 4 → 5`, `k = 2`:

```text
group 1: nodes 1 2, next group starts at 3
         reverse with prev = 3 -> 2 1 3 ...
         dummy.next = 2, group_prev = 1
group 2: nodes 3 4, next group starts at 5
         reverse -> 4 3 5, 1.next = 4, group_prev = 3
group 3: only 1 node (5), fewer than k, stop
result 2 1 4 3 5
```

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

**Complexity:** O(n) time, because each node is visited a constant number of times. O(1) space.

**Say it in 60 seconds:** "I keep `group_prev`, the node just before the current group, starting at a dummy. I walk k steps to find the group's last node. If I run out, the remaining nodes stay as they are and I return. Otherwise I reverse the group with `prev` initialised to the node after the group, so the reversed group is already connected to what follows. Then I point `group_prev.next` at the new group head, and the old group head becomes the next `group_prev`. Linear time, constant space."

---

### A8. LRU Cache

See [LLD problems](05_lld_problems.md). The idea in one paragraph: an LRU (Least Recently Used) cache evicts the item that hasn't been touched for the longest time. A hashmap gives O(1) lookup from key to node, and a doubly linked list keeps nodes in order of last use, so moving a node to the front and removing the tail are both O(1). Together they give O(1) `get` and `put`. In Python, `OrderedDict` with `move_to_end` and `popitem(last=False)` does the same job.

---

## B. Stack

### The idea

A **stack** is last in, first out (LIFO): you can only add to or remove from the top. In Python, a list with `append` and `pop` is a stack.

**Analogy:** a stack of plates. You put clean plates on top and take from the top. The plate you put down last is the first one you use.

Stacks fit anything **nested**, because the most recently opened thing must be the first one closed: brackets, function calls, HTML tags, folders in a path. They also give undo history and let you write DFS without recursion.

### When to recognise it

- "Valid parentheses", "balanced", "nested", "decode `3[ab]`".
- "Evaluate an expression", "calculator".
- "Undo", "back button", "simplify a path".
- Collisions or cancellations between neighbours (asteroids).

### Hand-traced example

Is `"{[]}"` balanced?

```text
char  action          stack
{     push            {
[     push            { [
]     pop [ matches   {
}     pop { matches   (empty) -> valid
```

### Template

```python
def process(tokens):
    st = []
    for t in tokens:
        if opens(t):
            st.append(t)
        else:
            top = st.pop() if st else None
            combine(top, t)
    return st
```

**Complexity:** O(n) time, because each item is pushed and popped at most once. O(n) space in the worst case.

### Common mistakes

- Popping from an empty stack. Always check `if st` first.
- Forgetting to check the stack is empty at the end (`"(("` has no mismatch but is invalid).
- Popping operands in the wrong order for `-` and `/`. The first pop is the **right** operand.

---

### B1. Valid Parentheses

**Problem in one sentence:** check that every bracket in a string is closed by the right type in the right order.

**Key insight:** the most recent unclosed bracket must be closed first, which is exactly LIFO. Push openers. For each closer, the top of the stack must be its matching opener.

**Dry run** on `"([)]"`:

```text
char  action                       stack
(     push                         (
[     push                         ( [
)     pop [, but ) needs (  -> False
```

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

**Complexity:** O(n) time, O(n) space.

**Say it in 60 seconds:** "Brackets nest, so the latest opener must close first, which is a stack. I map each closer to its opener. Openers get pushed. On a closer, if the stack is empty or the popped opener doesn't match, it's invalid. At the end the stack must be empty, otherwise something was left open. One pass, O(n)."

---

### B2. Min Stack (O(1) getMin)

**Problem in one sentence:** build a stack that also returns its current minimum in O(1).

**Key insight:** the minimum only changes when you push or pop, so store "the minimum so far" alongside every value. Push `(value, current_min)` pairs. When you pop, the previous minimum is automatically restored.

**Dry run:**

```text
op        stack (value, min)            get_min
push 5    (5,5)                         5
push 3    (5,5) (3,3)                   3
push 7    (5,5) (3,3) (7,3)             3
pop       (5,5) (3,3)                   3
pop       (5,5)                         5
```

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

**Complexity:** every operation O(1). O(n) space (two numbers per element).

**Say it in 60 seconds:** "A single 'current min' variable breaks when you pop the minimum, because you don't know the previous one. So each stack entry stores the value and the minimum of everything at or below it. Push computes the new min from the top entry. Pop just removes the top, and the entry below already knows its own minimum. Everything is O(1)."

---

### B3. Evaluate Reverse Polish Notation

**Problem in one sentence:** evaluate an expression written in postfix form, like `["2", "1", "+", "3", "*"]`, which means `(2 + 1) * 3`.

**Key insight:** in postfix, an operator always applies to the two most recent values, so a stack holds the pending values. Push numbers. On an operator, pop b, then a, and push `a op b`. Use `int(a / b)` for truncation toward zero, because Python's `//` rounds toward negative infinity (`-7 // 2` is -4, but the problem wants -3).

**Dry run** on `["2", "1", "+", "3", "*"]`:

```text
token  stack
2      2
1      2 1
+      3
3      3 3
*      9      -> answer 9
```

```python
def eval_rpn(tokens):
    st = []
    for t in tokens:
        if t in {"+", "-", "*", "/"}:
            b, a = st.pop(), st.pop()
            if t == "+":
                st.append(a + b)
            elif t == "-":
                st.append(a - b)
            elif t == "*":
                st.append(a * b)
            else:
                st.append(int(a / b))
        else:
            st.append(int(t))
    return st[0]
```

**Complexity:** O(n) time, O(n) space.

**Say it in 60 seconds:** "Postfix means each operator acts on the two most recent values, so I keep a stack of numbers. Numbers are pushed. For an operator I pop the right operand first, then the left, apply the operator, and push the result. Order matters for minus and divide. For division I use `int(a / b)` so it truncates toward zero, since Python's floor division rounds negatives down. The final stack holds the answer."

---

### B4. Decode String `3[a2[c]]` → `accaccacc`

**Problem in one sentence:** expand an encoded string where `k[...]` means "repeat the inside k times", and brackets can nest.

**Key insight:** when you hit `[`, you are starting a new inner string, but you must remember the outer string built so far and the repeat count. Push both. When you hit `]`, pop them and combine: `outer + inner * count`.

**Dry run** on `"3[a2[c]]"`:

```text
char  action                               cur     stack
3     num = 3                              ""      []
[     push ("", 3), reset                  ""      [("",3)]
a     cur += a                             "a"     [("",3)]
2     num = 2                              "a"
[     push ("a", 2), reset                 ""      [("",3), ("a",2)]
c     cur += c                             "c"
]     pop ("a",2): "a" + "c"*2             "acc"   [("",3)]
]     pop ("",3):  "" + "acc"*3            "accaccacc"
```

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

**Complexity:** O(output length) time and space. The output can be much longer than the input.

**Say it in 60 seconds:** "Nesting means a stack. I build the current string and the current number as I scan. On an open bracket I push the string so far and the repeat count, then start fresh. On a close bracket I pop, and the new current string is the popped prefix plus the inner string repeated. Digits accumulate with `num * 10 + digit` so multi-digit counts like 12 work. Time is proportional to the output size."

---

### B5. Basic Calculator (with + - and parentheses)

**Problem in one sentence:** evaluate a string like `"1 - (2 + 3)"` containing numbers, plus, minus, parentheses and spaces.

**Key insight:** without parentheses you just keep a running `result` and the `sign` of the next number. A parenthesis starts a fresh sub-expression, so keep `result`, `sign`, and a stack of `(result, sign)` pushed at `(`. At `)`, the inner result is combined with what you saved: `saved_result + saved_sign * inner`.

**Dry run** on `"1 - (2 + 3)"` (spaces skipped):

```text
char  action                                       result  sign  num  stack
1     num = 1                                      0       +1    1
-     result += 1, sign = -1                       1       -1    0
(     push (1, -1), reset                          0       +1    0    [(1,-1)]
2     num = 2                                      0       +1    2
+     result += 2, sign = +1                       2       +1    0
3     num = 3                                      2       +1    3
)     result = 2 + 3 = 5, pop -> 1 + (-1)*5 = -4   -4                 []
end   -4 + sign*0 = -4
```

```python
def calculate(s):
    result, num, sign = 0, 0, 1
    st = []
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c in "+-":
            result += sign * num
            num, sign = 0, (1 if c == "+" else -1)
        elif c == "(":
            st.append((result, sign))
            result, sign = 0, 1
        elif c == ")":
            result += sign * num
            num = 0
            prev_result, prev_sign = st.pop()
            result = prev_result + prev_sign * result
    return result + sign * num
```

**Complexity:** O(n) time, O(depth of nesting) space.

**Say it in 60 seconds:** "I scan once keeping a running result, the sign for the next number, and the number being read. When I see plus or minus, I fold the pending number into the result and set the new sign. An open parenthesis pushes the current result and sign and starts a clean sub-expression. A close parenthesis finishes the inner result and folds it into the saved one with the saved sign. Spaces are ignored. O(n) time."

---

### B6. Asteroid Collision, Simplify Path (`/a/./b/../../c` → `/c`): classic stack simulations

**Asteroid Collision in one sentence:** asteroids move right (positive) or left (negative) at the same speed. When a right-mover meets a left-mover, the smaller one explodes, and equal sizes both explode. Return what survives.

**Key insight:** only a new left-mover can collide, and it collides with the most recent right-movers first, which is the top of the stack.

**Dry run** on `[5, 10, -5]`:

```text
a    stack before  collision                   stack after
5    []            none                        [5]
10   [5]           none                        [5, 10]
-5   [5, 10]       10 > 5, -5 explodes          [5, 10]
```

```python
def asteroid_collision(asteroids):
    st = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and st and st[-1] > 0:
            if st[-1] < -a:
                st.pop()
            elif st[-1] == -a:
                st.pop()
                alive = False
            else:
                alive = False
        if alive:
            st.append(a)
    return st
```

**Simplify Path in one sentence:** turn a Unix path with `.`, `..` and repeated slashes into its shortest equivalent.

**Key insight:** split on `/`. A folder name is pushed, `..` pops (go up one folder), and `.` or empty parts are ignored.

**Dry run** on `"/a/./b/../../c"`: parts are `a . b .. .. c`, so the stack goes `[a]`, `[a]`, `[a, b]`, `[a]`, `[]`, `[c]`, and the answer is `/c`.

```python
def simplify_path(path):
    st = []
    for part in path.split("/"):
        if part == "..":
            if st:
                st.pop()
        elif part and part != ".":
            st.append(part)
    return "/" + "/".join(st)
```

**Complexity:** both O(n) time and space.

**Say it in 60 seconds (asteroids):** "Only a left-moving asteroid can hit something, and it hits the most recent right-movers first, so I keep survivors on a stack. For each left-mover, while the top is a right-mover, I compare sizes: if the top is smaller it explodes and I keep checking, if equal both explode, if bigger my asteroid explodes. If my asteroid survives, I push it. Each asteroid is pushed and popped at most once, so O(n)."

---

## C. Monotonic stack

### The idea

A **monotonic stack** is a stack you keep sorted, either always increasing or always decreasing from bottom to top. When a new element would break the order, you pop elements until it fits. The key fact: every element you pop has just found its **next greater (or smaller)** element, which is the new one. Each index is pushed and popped once, so O(n).

**Analogy:** people standing in a line, each waiting to see someone taller than them arrive. When a tall person walks up, every shorter person at the back of the line says "that's my answer" and leaves. People taller than the newcomer keep waiting. So the people still waiting are always sorted from tallest (front) to shortest (back).

### When to recognise it

- "Next greater element", "next smaller element", "previous smaller".
- "How many days until a warmer temperature", "stock span".
- "Largest rectangle", "maximal rectangle", "trapping water" (stack version).
- "Remove k digits to make the smallest number" (greedy with a stack).

### Hand-traced example (and the template below)

Next greater element for `[2, 1, 2, 4, 3]`. The stack holds indices whose answer is still unknown, with values decreasing.

```text
i  x  pops (they found x)        stack (values)  res
0  2  none                       [2]             [-1,-1,-1,-1,-1]
1  1  none                       [2, 1]
2  2  index 1 (1 < 2) -> res[1]=2 [2, 2]          [-1, 2,-1,-1,-1]
3  4  index 2, index 0 -> 4      [4]             [ 4, 2, 4,-1,-1]
4  3  none                       [4, 3]
answer [4, 2, 4, -1, -1]
```

### Template (next greater element to the right)

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

Store **indices**, not values, so you can compute distances and look up values.

**Complexity:** O(n) time, because each index is pushed once and popped at most once. O(n) space.

### Common mistakes

- Storing values instead of indices, then being unable to compute distances.
- Choosing the wrong direction. Popping smaller elements finds the next **greater**. Popping greater elements finds the next **smaller**.
- Using `<` versus `<=` carelessly. With duplicates, decide whether "equal" counts as greater.
- Forgetting a sentinel to flush the stack at the end (histogram).

---

### C1. Daily Temperatures

**Problem in one sentence:** for each day, how many days until a warmer temperature (0 if never)?

**Key insight:** this is "next greater element", but you record the distance. Same template: `res[j] = i - j`.

**Dry run** on `[73, 74, 75, 71, 72]`:

```text
i  t   pops                    stack (temps)  res
0  73                          [73]
1  74  73 -> res[0] = 1        [74]
2  75  74 -> res[1] = 1        [75]
3  71                          [75, 71]
4  72  71 -> res[3] = 1        [75, 72]
answer [1, 1, 0, 1, 0]
```

```python
def daily_temperatures(t):
    res = [0] * len(t)
    st = []
    for i, x in enumerate(t):
        while st and t[st[-1]] < x:
            j = st.pop()
            res[j] = i - j
        st.append(i)
    return res
```

**Complexity:** O(n) time and space.

**Say it in 60 seconds:** "This is next-greater-element with distances. I keep a stack of indices of days still waiting for a warmer day, so their temperatures are decreasing. When today is warmer than the top, that day's wait is today's index minus its index, and I pop it. I keep popping while today is warmer, then push today. Anything left in the stack never warms up and stays 0. Each day is pushed and popped once, so O(n)."

---

### C2. Largest Rectangle in Histogram (hard, very common)

**Problem in one sentence:** given bar heights of width 1, find the area of the largest rectangle that fits under the bars.

**Key insight:** for each bar, the widest rectangle using its height extends to the first shorter bar on each side. With an increasing stack, when bar i is shorter than the top, the top's right boundary is i and its left boundary is the new top after popping. A sentinel 0 at the end forces every bar to be popped and measured.

**Dry run** on `[2, 1, 5, 6, 2, 3]` (with sentinel 0 at index 6):

```text
i  h  pops: height x (i - left - 1) = area            stack after  best
0  2                                                   [0]          0
1  1  pop 0: 2 x (1 - (-1) - 1) = 2                    [1]          2
2  5                                                   [1,2]        2
3  6                                                   [1,2,3]      2
4  2  pop 3: 6 x (4 - 2 - 1) = 6                                    6
      pop 2: 5 x (4 - 1 - 1) = 10                      [1,4]        10
5  3                                                   [1,4,5]      10
6  0  pop 5: 3 x 1 = 3, pop 4: 2 x 4 = 8, pop 1: 1 x 6 = 6           10
answer 10 (bars 5 and 6, height 5, width 2)
```

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

**Complexity:** O(n) time and space.

**Extension:** Maximal Rectangle in a binary matrix is this per row, over accumulated column heights (each row turns the matrix above it into a histogram).

**Say it in 60 seconds:** "Every candidate rectangle has some bar as its shortest bar, and it extends left and right until a shorter bar. I keep a stack of indices with increasing heights. When the current bar is shorter than the top, the top bar's rectangle ends here: its right edge is the current index, and its left edge is the new top after popping, because that's the nearest shorter bar to its left. Width is `i - left - 1`. A zero sentinel at the end flushes everything. Each bar is pushed and popped once, so O(n)."

---

### C3. Car Fleet

**Problem in one sentence:** cars drive toward a target on a one-lane road and can't pass. A faster car that catches a slower one joins it as a fleet. How many fleets arrive?

**Key insight:** sort by position descending (closest to the target first). Compute each car's time to reach the target alone. A car behind can only catch up with the fleet in front, never pass it. So a car forms a new fleet only if its time is greater than the fleet ahead of it. Otherwise it joins that fleet. (This is a monotonic stack where you only need the top, so a single variable is enough.)

**Dry run** on `target = 12`, `position = [10, 8, 0, 5, 3]`, `speed = [2, 4, 1, 1, 3]`:

```text
car (pos, speed)  time to target  slower than fleet ahead?  fleets  slowest
(10, 2)           1               yes (nothing ahead)       1       1
(8, 4)            1               no, joins                 1       1
(5, 1)            7               yes                       2       7
(3, 3)            3               no, joins                 2       7
(0, 1)            12              yes                       3       12
answer 3
```

```python
def car_fleet(target, position, speed):
    cars = sorted(zip(position, speed), reverse=True)
    fleets, slowest = 0, 0.0
    for p, s in cars:
        t = (target - p) / s
        if t > slowest:
            fleets += 1
            slowest = t
    return fleets
```

**Complexity:** O(n log n) for the sort, then O(n).

**Say it in 60 seconds:** "Cars can't pass, so I process them from closest to the target backwards. For each car I compute how long it would take alone. If a car would arrive later than the fleet in front of it, it can never catch up and becomes a new fleet, and its time becomes the new bar to beat. If it would arrive sooner, it catches up and merges. Sorting is O(n log n), the scan is linear."

---

### C4. Sum of Subarray Minimums, Stock Span, Remove K Digits

**Remove K Digits in one sentence:** delete k digits from a number string to make the smallest possible number.

**Key insight:** a smaller digit earlier always beats a larger digit earlier. So pop while the top is greater than the current digit and k > 0, which makes the smallest number greedily. If deletions remain at the end, cut from the right (the stack is non-decreasing, so the largest digits are at the end). Strip leading zeros.

**Dry run** on `num = "1432219"`, `k = 3`:

```text
digit  pops (k after)     stack
1                         1
4                         1 4
3      pop 4 (k=2)        1 3
2      pop 3 (k=1)        1 2
2                         1 2 2
1      pop 2 (k=0)        1 2 1
9                         1 2 1 9
answer "1219"
```

```python
def remove_k_digits(num, k):
    st = []
    for d in num:
        while k and st and st[-1] > d:
            st.pop()
            k -= 1
        st.append(d)
    st = st[:-k] if k else st
    return "".join(st).lstrip("0") or "0"
```

**Complexity:** O(n) time and space.

**The other two, in one line each:**
- **Stock Span:** for each day, count consecutive previous days with price ≤ today. Keep a decreasing stack of `(price, span)`. Pop smaller-or-equal prices and add their spans.
- **Sum of Subarray Minimums:** for each element, count how many subarrays it is the minimum of, which is `(distance to previous smaller) × (distance to next smaller)`. Both distances come from monotonic stacks. Multiply by the value and sum.

**Say it in 60 seconds (Remove K Digits):** "To minimise a number, the leftmost digits matter most, so whenever the current digit is smaller than the previous kept digit, deleting the previous one helps. I keep a stack of kept digits and pop while the top is bigger and I still have deletions. If deletions are left over, the stack is non-decreasing, so I remove from the end. Finally I strip leading zeros and return '0' if nothing is left. O(n)."

---

## D. Queue and deque

### The idea

A **queue** is first in, first out (FIFO). It's used for BFS, producer/consumer, and task scheduling. A **deque** (double-ended queue, pronounced "deck") lets you add and remove at both ends in O(1). In Python use `collections.deque` for both, never `list.pop(0)`.

**Analogy:** a queue is the line at a ticket counter. A deque is a line where people can also join or leave from the back, like a bus with doors at both ends.

### When to recognise it

- "Level by level", "shortest number of steps" (BFS uses a queue, see the [graphs file](03_dsa_4_graphs_dsu.md)).
- "Sliding window maximum or minimum" (monotonic deque).
- "Recent requests in the last N seconds" (hit counter, rate limiter).
- Fixed-size buffers (circular queue, ring buffer).

### Hand-traced example

Sliding window maximum with k = 3 on `[1, 3, -1, -3, 5]`. The deque holds indices with decreasing values, so the front is always the max.

```text
i  x   expire front?   pop back smaller   deque (values)  output
0  1                                      [1]
1  3                   pop 1              [3]
2  -1                                     [3, -1]         3
3  -3                                     [3, -1, -3]     3
4  5   index 1 expires pop -3, -1         [5]             5
```

### Template

The template is the Sliding Window Maximum code in D1 below.

**Complexity:** queue and deque operations are O(1). A monotonic deque over n elements is O(n) total, because each index enters and leaves once.

### Common mistakes

- Using `list.pop(0)`, which is O(n).
- In the monotonic deque, forgetting to expire the front when it falls out of the window.
- Storing values instead of indices, which makes it impossible to tell when the front has expired.

---

### D1. Sliding Window Maximum (monotonic deque)

**Problem in one sentence:** for every window of size k, report the maximum.

**Key insight:** keep a deque of indices with decreasing values. The front is the max. Pop the front when it leaves the window, and pop the back while it's smaller than the new element (it can never be a max again, because the new element is both larger and will stay in the window longer).

**Dry run** on `nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`:

```text
i  x   deque after (values)  output
0  1   [1]
1  3   [3]
2  -1  [3, -1]               3
3  -3  [3, -1, -3]           3
4  5   [5]                   5     (3 expired, -1 and -3 popped)
5  3   [5, 3]                5
6  6   [6]                   6
7  7   [7]                   7
answer [3, 3, 5, 5, 6, 7]
```

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

**Complexity:** O(n) time, O(k) space.

**Related:** Shortest Subarray with Sum at Least K (prefix sums + monotonic deque, handles negatives).

**Say it in 60 seconds:** "A heap would give O(n log k). For O(n) I keep a deque of indices whose values are decreasing, so the front is always the current max. For each new element, I drop the front if it's slid out of the window, then pop from the back every element smaller than the new one, because those can never be the max again. Then I append the new index and, once the first window is full, record the front's value. Each index enters and leaves once."

---

### D2. Implement a Queue using two stacks

**Problem in one sentence:** build a FIFO queue using only two LIFO stacks.

**Key insight:** pouring one stack into another reverses the order, which turns LIFO into FIFO. Use an `in` stack for push and an `out` stack for pop. Refill `out` only when it's empty. Each element is moved at most once, so the cost is amortized O(1).

**Dry run:**

```text
push 1, push 2   inbox [1, 2]  outbox []
pop              outbox empty, pour -> outbox [2, 1], pop 1
push 3           inbox [3]     outbox [2]
pop              outbox not empty, pop 2
pop              outbox empty, pour -> [3], pop 3
```

```python
class MyQueue:
    def __init__(self):
        self.inbox, self.outbox = [], []
    def push(self, x):
        self.inbox.append(x)
    def pop(self):
        self.peek()
        return self.outbox.pop()
    def peek(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox[-1]
    def empty(self):
        return not self.inbox and not self.outbox
```

**Complexity:** amortized O(1) per operation, worst case O(n) for a single pop that triggers a pour.

**Say it in 60 seconds:** "Pushes go onto an inbox stack. Pops come from an outbox stack. When the outbox is empty, I pour the whole inbox into it, which reverses the order so the oldest element is on top. I only pour when the outbox is empty, so every element moves exactly once from inbox to outbox. That makes each operation amortized O(1), even though one pop can occasionally cost O(n)."

---

### D3. Design Circular Queue

**Problem in one sentence:** build a fixed-capacity queue on top of an array, reusing slots as items leave.

**Key insight:** a fixed array with `head` and `count`. `tail = (head + count) % cap`. The modulo wraps around the end of the array like a clock face. This is also the core of a bounded ring buffer (see [concurrency](06_concurrency.md)).

**Dry run** with capacity 3:

```text
op          buf          head  count  note
enqueue 1   [1, _, _]    0     1      slot (0+0)%3 = 0
enqueue 2   [1, 2, _]    0     2
enqueue 3   [1, 2, 3]    0     3
enqueue 4   full -> False
dequeue     [x, 2, 3]    1     2
enqueue 4   [4, 2, 3]    1     3      slot (1+2)%3 = 0, wrapped
front = buf[1] = 2, rear = buf[(1+3-1)%3] = buf[0] = 4
```

```python
class MyCircularQueue:
    def __init__(self, k):
        self.buf = [0] * k
        self.head = self.count = 0
        self.cap = k
    def en_queue(self, x):
        if self.count == self.cap:
            return False
        self.buf[(self.head + self.count) % self.cap] = x
        self.count += 1
        return True
    def de_queue(self):
        if self.count == 0:
            return False
        self.head = (self.head + 1) % self.cap
        self.count -= 1
        return True
    def front(self):
        return -1 if self.count == 0 else self.buf[self.head]
    def rear(self):
        return -1 if self.count == 0 else self.buf[(self.head + self.count - 1) % self.cap]
```

**Complexity:** every operation O(1). O(k) space, fixed.

**Say it in 60 seconds:** "I use a fixed array, a head index, and a count. The next free slot is head plus count, modulo capacity, so the queue wraps around the end of the array. Enqueue fails when count equals capacity. Dequeue just advances head modulo capacity. Keeping a count instead of a separate tail avoids the classic ambiguity where head equals tail could mean either full or empty. All operations are O(1), and it's exactly the ring buffer used in bounded producer-consumer queues."

---

### D4. Design Hit Counter (hits in the last 300s)

**Problem in one sentence:** record hits with timestamps in seconds and return how many happened in the last 300 seconds.

**Key insight:** the simple version is a deque of timestamps, popping old ones from the left. That uses memory proportional to traffic. For high volume, use 300 buckets of `(timestamp, count)` indexed by `ts % 300`. Memory stays fixed at 300 slots no matter how many hits arrive, which is O(1) memory per second of window. When a bucket's stored timestamp is old, it's reset before reuse. That's a rate limiter warmup.

**Dry run** (window shortened to 3 seconds to keep it small):

```text
op            slot = ts % 3   times      counts
hit(1)        1               [0,1,0]    [0,1,0]
hit(1)        1               [0,1,0]    [0,2,0]
hit(2)        2               [0,1,2]    [0,2,1]
get_hits(3)   count slots with 3 - t < 3: t=1 (2 hits), t=2 (1 hit) -> 3
hit(4)        1, stale (1 != 4), reset   [0,4,2]  [0,1,1]
get_hits(4)   t=4 (1), t=2 (1) -> 2
```

```python
class HitCounter:
    def __init__(self, window=300):
        self.window = window
        self.times = [0] * window
        self.counts = [0] * window
    def hit(self, ts):
        i = ts % self.window
        if self.times[i] != ts:
            self.times[i] = ts
            self.counts[i] = 0
        self.counts[i] += 1
    def get_hits(self, ts):
        return sum(c for t, c in zip(self.times, self.counts) if ts - t < self.window)
```

**Complexity:** `hit` O(1), `get_hits` O(window) which is a constant 300. Fixed memory.

**Say it in 60 seconds:** "The deque version stores every timestamp, which grows with traffic. Instead I keep 300 buckets, one per second of the window, indexed by timestamp modulo 300. Each bucket stores which second it currently represents and a count. On a hit, if the bucket holds an older second, I reset it first. To count, I sum buckets whose second is within the last 300. Memory is fixed regardless of QPS. To make it thread safe I'd lock per bucket or use atomic counters, and at scale it becomes a sliding-window rate limiter."

---

## E. Heap / priority queue

### The idea

A **heap** (priority queue) is a structure that always gives you the smallest (min-heap) or largest (max-heap) item quickly. Push and pop are O(log n), and peeking at the top is O(1). It doesn't keep everything sorted, only enough order that the top is always the extreme. Python's `heapq` is a min-heap stored in a plain list, with the smallest item at index 0.

**Analogy:** a hospital emergency room. Patients arrive in any order, but the most urgent one is always seen next. Nobody sorts the whole waiting room, the triage nurse just knows who is most urgent.

**Top K largest trick:** keep a *min*-heap of size k. The smallest of the top k is on top, and when a bigger item arrives you evict it. This uses O(k) memory, which matters when the data is a stream or huge.

### When to recognise it

- "k-th largest", "top k", "k closest", "k most frequent".
- "Merge k sorted lists or files".
- "Median of a stream".
- "Always process the cheapest or earliest next" (Dijkstra, scheduling, meeting rooms).

### Hand-traced example

Keep the 2 largest numbers from the stream `5, 1, 8, 3, 9` with a min-heap of size 2.

```text
x  heap before  action                     heap after (min on left)
5  []           push                       [5]
1  [5]          push                       [1, 5]
8  [1, 5]       8 > 1, replace top         [5, 8]
3  [5, 8]       3 < 5, ignore              [5, 8]
9  [5, 8]       9 > 5, replace top         [8, 9]
2nd largest = top = 8
```

### Template

```python
def top_k_largest(stream, k):
    h = []
    for x in stream:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heapreplace(h, x)     # pop the smallest and push x, in one O(log k) step
    return h
```

**Complexity:** O(n log k) time, O(k) space.

### Common mistakes

- Using a max-heap of everything for "top k largest" (O(n log n) and O(n) memory) instead of a min-heap of size k.
- Forgetting that Python only has a min-heap. Negate values for a max-heap.
- Pushing tuples whose second element isn't comparable. Add a tiebreak counter.
- Thinking `heapq` supports "decrease key". It doesn't. Push a new entry and skip stale ones.

---

### E1. Kth Largest Element in an Array

**Problem in one sentence:** return the k-th largest value in an unsorted array.

**Key insight:** a min-heap of size k: O(n log k). The top of a size-k min-heap of the largest values seen is exactly the k-th largest. Quickselect: O(n) average, O(n²) worst.

**Dry run** on `[3, 2, 1, 5, 6, 4]`, `k = 2`:

```text
heapify [3, 2] -> [2, 3]
x=1: not > 2, skip      [2, 3]
x=5: > 2, replace       [3, 5]
x=6: > 3, replace       [5, 6]
x=4: not > 5, skip      [5, 6]
answer top = 5
```

```python
def find_kth_largest(nums, k):
    h = nums[:k]
    heapq.heapify(h)
    for x in nums[k:]:
        if x > h[0]:
            heapq.heapreplace(h, x)
    return h[0]
```

**Complexity:** O(n log k) time, O(k) space.

**Say it in 60 seconds:** "Sorting is O(n log n). I keep a min-heap of the k largest values seen so far. I heapify the first k elements, then for every other element, if it's bigger than the heap's smallest, I replace the smallest. At the end, the top is the k-th largest. That's O(n log k) time and O(k) memory, which also works on a stream. If they want average O(n), I'd mention quickselect, with the caveat that its worst case is O(n²) unless the pivot is randomised."

---

### E2. K Closest Points to Origin

**Problem in one sentence:** return the k points nearest to (0, 0).

**Key insight:** this is "top k smallest distances", so keep a **max**-heap of size k on distance (push the negative distance). The farthest of the current k is on top and gets evicted when a closer point arrives. Compare squared distances, no square root needed.

**Dry run** on `points = [[1, 3], [-2, 2], [2, -2]]`, `k = 2` (squared distances 10, 8, 8):

```text
point    d   heap (stores -d)       action
(1,3)    10  [-10]                  push
(-2,2)   8   [-10, -8]              push
(2,-2)   8   top is -10 (farthest)  -8 > -10, replace -> [-8, -8]
answer [[-2, 2], [2, -2]]
```

```python
def k_closest(points, k):
    h = []
    for x, y in points:
        d = x * x + y * y
        if len(h) < k:
            heapq.heappush(h, (-d, x, y))
        elif -d > h[0][0]:
            heapq.heapreplace(h, (-d, x, y))
    return [[x, y] for _, x, y in h]
```

**Complexity:** O(n log k) time, O(k) space.

**Say it in 60 seconds:** "I want the k smallest distances, so I keep a max-heap of size k, where the top is the farthest of my current best k. Python only has min-heaps, so I store negative distances. For each new point, if the heap isn't full I push it. Otherwise, if it's closer than the top, I replace the top. I compare squared distances to avoid square roots. O(n log k) time, O(k) space."

---

### E3. Merge K Sorted Lists (also "merge k sorted log files")

**Problem in one sentence:** merge k sorted linked lists into one sorted list.

**Key insight:** the next output is always the smallest of the k current heads. A min-heap of the k heads gives that in O(log k). After taking a node, push its successor from the same list.

**Dry run** on `[1 → 4], [1 → 3], [2]`:

```text
heap (val, list index)        pop       push next      output
(1,0) (1,1) (2,2)             (1,0)     (4,0)          1
(1,1) (2,2) (4,0)             (1,1)     (3,1)          1 1
(2,2) (3,1) (4,0)             (2,2)     none           1 1 2
(3,1) (4,0)                   (3,1)     none           1 1 2 3
(4,0)                         (4,0)     none           1 1 2 3 4
```

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

`tail.next = tail = node` assigns left to right: first the old tail's `next` becomes `node`, then `tail` moves to `node`.

**Complexity:** O(N log k) time, where N is the total number of nodes, because each node is pushed and popped once on a heap of size at most k. O(k) heap space. The index `i` breaks ties because nodes aren't comparable.

**At scale, this is external merge sort:** sort chunks that fit in memory, write them to disk, then k-way merge them with a heap and buffered IO (read a block from each file at a time, not one line). The same shape merges time-ordered logs from many servers.

**Say it in 60 seconds:** "At any moment the next node in the output is the smallest among the k list heads. I put all k heads in a min-heap keyed by value, with the list index as a tiebreaker since nodes can't be compared. I pop the smallest, append it, and push that node's successor. Each of the N nodes goes through a heap of size k once, so O(N log k). It's the same algorithm as merging sorted log files from many machines, or the merge phase of external sort."

---

### E4. Find Median from Data Stream (two heaps)

**Problem in one sentence:** numbers arrive one at a time. Support adding a number and asking for the current median, both fast.

**Key insight:** split the numbers into a lower half and an upper half. A max-heap for the lower half shows its largest, and a min-heap for the upper half shows its smallest. The median is at the boundary. Keep sizes balanced (lower can have one extra).

**Analogy:** two piles of exam papers, low scores and high scores, where you can always see the best of the low pile and the worst of the high pile. The median is one of those, or their average.

**Dry run** adding `1, 2, 3`:

```text
add  lo (max-heap, shown as values)  hi (min-heap)  median
1    [1]                              []             1
2    [1]                              [2]            (1 + 2) / 2 = 1.5
3    [2, 1]                           [3]            2
```

The `add_num` steps: push to `lo`, move `lo`'s largest to `hi` (so every element of `lo` ≤ every element of `hi`), then if `hi` became bigger, move its smallest back.

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

**Complexity:** `add_num` O(log n), `find_median` O(1). O(n) space.

**Follow-ups:** sliding-window median (lazy deletion with a hashmap of to-delete counts, removing entries only when they reach the top). For p99 latency at scale use histograms or t-digest (a compact summary that estimates percentiles accurately with small memory), not exact medians.

**Say it in 60 seconds:** "I keep the smaller half in a max-heap and the larger half in a min-heap, with the lower heap allowed one extra element. To add, I push into the lower heap, move its max to the upper heap to keep the ordering correct, and if the upper heap is now larger, I move its min back. The median is the top of the lower heap for odd counts, or the average of both tops for even. Add is O(log n), median is O(1). For latency percentiles in production I wouldn't store every value. I'd use a histogram or t-digest."

---

### E5. Task Scheduler (cooldown n)

**Problem in one sentence:** CPU tasks are letters. The same letter needs n idle slots between runs. What's the minimum total time?

**Key insight:** the most frequent task decides the shape. If A appears `maxFreq` times, there are `maxFreq - 1` gaps of length `n + 1` (one A plus n slots), followed by a final row containing every task that ties for the max frequency. If there are enough other tasks to fill all gaps, there's no idle time and the answer is just the number of tasks.

**Math answer:** `max(len(tasks), (maxFreq - 1) * (n + 1) + countOfMaxFreq)`. The simulation uses a max-heap plus a cooldown queue.

**Dry run** on `["A","A","A","B","B","B"]`, `n = 2`:

```text
maxFreq = 3 (A and B), countOfMaxFreq = 2
frame: A B _ | A B _ | A B
(3 - 1) * (2 + 1) + 2 = 8, max(6, 8) = 8
```

```python
def least_interval(tasks, n):
    freq = Counter(tasks).values()
    max_f = max(freq)
    count_max = sum(1 for f in freq if f == max_f)
    return max(len(tasks), (max_f - 1) * (n + 1) + count_max)
```

**Complexity:** O(len(tasks)) time, O(26) space.

**Say it in 60 seconds:** "The most frequent task forces the schedule. With frequency f, I need f minus 1 full frames of length n plus 1, and then a last frame holding every task that shares the max frequency. If other tasks fill all the idle slots, the answer is just the number of tasks, so I take the max of the two. That's linear time. If they want the actual schedule, I'd simulate with a max-heap of counts and a queue of tasks cooling down."

---

### E6. Reorganize String (no two adjacent the same)

**Problem in one sentence:** rearrange a string so no two neighbouring characters are equal, or return "" if impossible.

**Key insight:** always place the most frequent remaining character, but never the same one twice in a row. Max-heap by count. Pop the top, append it, and hold it back one step (push the previous one back).

**Dry run** on `"aab"`:

```text
heap (count, char)   pop    out    held back
(-2,a) (-1,b)        a      a      (-1,a)
(-1,b)               b      ab     push (-1,a) back, b now used up
(-1,a)               a      aba    none
answer "aba"
```

For `"aaab"` the heap empties while `a` is still held back, so the output has 3 characters instead of 4, and the function returns "".

```python
def reorganize_string(s):
    h = [(-c, ch) for ch, c in Counter(s).items()]
    heapq.heapify(h)
    out, prev = [], None
    while h:
        c, ch = heapq.heappop(h)
        out.append(ch)
        if prev:
            heapq.heappush(h, prev)
        c += 1
        prev = (c, ch) if c < 0 else None
    return "".join(out) if len(out) == len(s) else ""
```

**Complexity:** O(n log 26) which is O(n) time, O(26) space.

**Say it in 60 seconds:** "Greedily, I should place the character with the most copies left, as long as it differs from the last one placed. I keep a max-heap of counts. Each step I pop the most frequent character, append it, and push back the character I held from the previous step. The one I just used is held out for one turn so it can't repeat immediately. If the heap runs dry while a character is still waiting, it's impossible. A quick check up front: if any count exceeds (n + 1) / 2, return empty."

---

### E7. Meeting Rooms II

See [intervals](03_dsa_6_backtracking_greedy_intervals_matrix_bits.md) (a min-heap of end times). The one-line idea: sort meetings by start time, keep the end times of rooms in use in a min-heap, and reuse the room that frees up earliest if it's free by the time the next meeting starts.

### E8. Dijkstra and Prim use heaps

See [graphs](03_dsa_4_graphs_dsu.md). Both repeatedly take the cheapest frontier option, which is exactly what a min-heap provides.

---

### E9. Design Twitter (news feed of top 10)

**Problem in one sentence:** support posting tweets, following and unfollowing, and getting the 10 most recent tweets from yourself and the people you follow.

**Key insight:** each user's tweets are already in time order. The feed is a k-way merge over the user and their followees with a heap, taking 10. That's the same idea as fan-out-on-read in system design: build the feed when it's requested, by merging the sources.

**Dry run:** user 1 posts tweet 5 (time 1). User 2 posts tweet 6 (time 2). User 1 follows 2. Feed for user 1: push the newest tweet of each source, `(time 2, tweet 6)` and `(time 1, tweet 5)`. Pop the newest, tweet 6, then tweet 5. Feed `[6, 5]`.

```python
class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)     # user -> [(time, tweet_id)]
        self.follows = defaultdict(set)

    def post_tweet(self, user, tweet_id):
        self.time += 1
        self.tweets[user].append((self.time, tweet_id))

    def get_news_feed(self, user):
        h = []
        for u in self.follows[user] | {user}:
            if self.tweets[u]:
                i = len(self.tweets[u]) - 1
                t, tid = self.tweets[u][i]
                heapq.heappush(h, (-t, tid, u, i))
        feed = []
        while h and len(feed) < 10:
            _, tid, u, i = heapq.heappop(h)
            feed.append(tid)
            if i > 0:
                t, nid = self.tweets[u][i - 1]
                heapq.heappush(h, (-t, nid, u, i - 1))
        return feed

    def follow(self, a, b):
        if a != b:
            self.follows[a].add(b)

    def unfollow(self, a, b):
        self.follows[a].discard(b)
```

**Complexity:** `get_news_feed` is O(F + 10 log F) for F followees. Posting and following are O(1).

**Say it in 60 seconds:** "Each user has a time-ordered list of tweets. To build a feed, I put the newest tweet from the user and every followee into a max-heap by time, then pop up to 10 times, each time pushing the next-older tweet from the same author. That's a k-way merge that stops after 10. In system design terms this is fan-out on read. For celebrity accounts with millions of followers, real systems mix this with fan-out on write, pushing tweets into followers' precomputed feeds."

---

## Heap facts to say out loud

- `heapify` is O(n), not O(n log n). Most nodes are near the bottom and only move a little, so the total work sums to linear.
- Python has only a min-heap. Negate for max, or push `(-priority, ...)`.
- There's no decrease-key in heapq. Push a new entry and skip stale ones on pop (lazy deletion). Dijkstra does exactly this.
- `heapreplace(h, x)` pops then pushes in one O(log n) step. `heappushpop(h, x)` pushes then pops, which is faster when `x` would be popped immediately.
