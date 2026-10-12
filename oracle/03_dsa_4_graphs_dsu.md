# 03.4 Graphs: BFS, DFS, topological sort, shortest paths, MST, DSU

<div class="callout note">
<b>How to use this page</b>
<ul>
<li><b>What it covers:</b> how to represent a graph, BFS and DFS, cycle detection, topological sort, shortest paths (Dijkstra, Bellman-Ford, 0-1 BFS, Floyd-Warshall), minimum spanning trees, and union-find (DSU).</li>
<li><b>When to read it:</b> after trees. Graph problems are where OCI interviewers most often add a systems twist ("this is a dependency graph of services", "these are network links").</li>
<li><b>What to memorise:</b> the "which algorithm for which need" table, "mark visited when you enqueue", Kahn's algorithm, Dijkstra with lazy deletion, and the DSU class.</li>
<li><b>How each problem is laid out:</b> a one-line restatement, the key insight, a dry run, code, complexity, and a 60-second spoken version.</li>
</ul>
</div>

Imports assumed by every snippet on this page:

```python
from collections import defaultdict, deque
import heapq
```

---

## A. Representations and the three questions

### The idea

A **graph** is a set of **nodes** (also called vertices, V) connected by **edges** (E). Edges can be **directed** (one-way, like "A depends on B") or **undirected** (two-way, like a road), and **weighted** (a cost or distance) or unweighted.

**Analogy:** a city map. Intersections are nodes and roads are edges. One-way streets are directed edges, and travel time is the weight.

How to store one:

- **Adjacency list** `graph = defaultdict(list)`: each node maps to a list of its neighbours. O(V + E) space, the default.
- **Adjacency matrix:** a V × V grid where `m[u][v]` says whether there's an edge. O(V²), for dense graphs or quick edge checks.
- **Grid as a graph:** cell = node, 4 or 8 neighbors. You don't build anything, you compute neighbours on the fly.
- **Implicit graph:** states generated on the fly (Word Ladder, lock combinations). Each state is a node, and each legal move is an edge.

Ask: **directed or undirected? weighted? cycles possible? connected?** The answers pick the algorithm.

| Need | Algorithm | Complexity |
|---|---|---|
| Reachability, components, cycle detection | DFS / BFS / DSU | O(V + E) |
| Shortest path, unweighted | BFS | O(V + E) |
| Shortest path, weights 0/1 | 0-1 BFS (deque) | O(V + E) |
| Shortest path, non-negative weights | Dijkstra | O((V + E) log V) |
| Shortest path, negative weights / at most k edges | Bellman-Ford | O(V·E) or O(k·E) |
| All pairs | Floyd-Warshall | O(V³) |
| Ordering with dependencies | Topological sort (Kahn / DFS) | O(V + E) |
| Min spanning tree | Kruskal (DSU) / Prim (heap) | O(E log E) |
| Dynamic connectivity (only unions) | DSU | ~O(α(n)) per op |
| Strongly connected components | Tarjan / Kosaraju | O(V + E) |
| Bridges / articulation points | Tarjan low-link | O(V + E) |

### Building an adjacency list

```python
def build(n, edges, directed=False):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        if not directed:
            g[v].append(u)
    return g
```

### Common mistakes

- Adding only one direction for an undirected graph.
- Assuming the graph is connected. Loop over every node as a possible start.
- Recursion depth: a DFS on a 10⁵-node path graph overflows Python's default limit. Use an explicit stack.

---

## B. DFS and BFS templates

### The idea

**DFS (depth-first search)** goes as deep as it can along one path, then backs up and tries the next branch. It's natural with recursion or a stack. **BFS (breadth-first search)** explores in rings: all nodes 1 step away, then 2 steps, and so on. It uses a queue, and in an unweighted graph the first time BFS reaches a node is along a shortest path.

**Analogy:** DFS is exploring a maze by always taking the next unexplored corridor until you hit a dead end, then backing up. BFS is dropping a stone in a pond: the ripple reaches everything 1 metre away before anything 2 metres away.

### When to recognise it

- **BFS:** "minimum number of steps", "shortest path" (unweighted), "nearest", "level", "spreads each minute".
- **DFS:** "can you reach", "count connected regions", "explore all", "detect a cycle", "flood fill".

### Hand-traced example (and why "mark on enqueue")

Graph: `A → B, A → C, B → D, C → D`. BFS from A.

```text
pop  enqueue (mark now)   queue after  dist
A    B, C                 [B, C]       A0 B1 C1
B    D                    [C, D]       D2
C    D already marked     [D]
D    -                    []
```

If you marked nodes when you **pop** them instead, both B and C would enqueue D, and D would be processed twice. In a dense graph that duplication blows up the queue.

### Templates

```python
def dfs_iter(graph, start):
    seen, st = {start}, [start]
    while st:
        u = st.pop()
        for v in graph[u]:
            if v not in seen:
                seen.add(v)
                st.append(v)
    return seen

def bfs_dist(graph, start):
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

Mark visited **when you enqueue**, not when you pop. Otherwise nodes get enqueued many times.

**Complexity:** O(V + E) time, because each node is enqueued once and each edge is examined once (twice for undirected). O(V) space.

### Common mistakes

- Marking visited on pop (duplicates in the queue).
- Using `list.pop(0)` as the queue (O(n) per pop).
- Using DFS for "shortest path" in an unweighted graph. DFS finds **a** path, not the shortest.
- Forgetting bounds checks on grids (`0 <= nr < R`).

---

### B1. Number of Islands (grid DFS/BFS)

**Problem in one sentence:** count groups of connected '1' cells (land) in a grid, where cells connect up, down, left and right.

**Key insight:** scan every cell. Each time you find unvisited land, you've found a new island, so count it and **sink** the whole island (flood fill it to '0') so you never count it again.

**Dry run** on:

```text
1 1 0
0 1 0
0 0 1

scan (0,0): land -> count 1, sink (0,0), (0,1), (1,1)
scan (0,1), (1,1): already 0
scan (2,2): land -> count 2, sink it
answer 2
```

```python
def num_islands(grid):
    R, C = len(grid), len(grid[0])
    def sink(r, c):
        st = [(r, c)]
        grid[r][c] = "0"
        while st:
            r, c = st.pop()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == "1":
                    grid[nr][nc] = "0"
                    st.append((nr, nc))
    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count
```

**Complexity:** O(R·C) time, because each cell is sunk at most once. O(R·C) stack space in the worst case (all land).

**Variants:** Max Area of Island (return the size from `sink`), Surrounded Regions (flood from the border first, everything not reached gets flipped), Pacific Atlantic (reverse flow: BFS from each ocean "uphill", then intersect the two reachable sets).

**Say it in 60 seconds:** "Each island is a connected component of land cells. I scan the grid. When I find a '1', I increase the count and flood-fill from there, turning every connected land cell to '0' so it can't be counted again. I use an explicit stack instead of recursion so a huge island doesn't hit the recursion limit. Every cell is visited a constant number of times, so O(R·C). If I can't modify the input, I use a visited set."

---

### B2. Rotting Oranges (multi-source BFS)

**Problem in one sentence:** every minute, rotten oranges rot their fresh neighbours. How many minutes until none are fresh, or -1 if some never rot?

**Key insight:** the rot spreads from **all** rotten oranges at the same time. Put **all** rotten oranges in the queue at time 0, then BFS level by level. Each BFS level is one minute. The answer is the number of levels, or -1 if fresh oranges remain. Same idea: Walls and Gates, 01 Matrix, and distance from the nearest server.

**Dry run** on:

```text
2 1 1
1 1 0
0 1 1

minute 1: (0,0) rots (0,1) and (1,0)      fresh 6 -> 4
minute 2: rots (1,1) and (0,2)            fresh 2
minute 3: rots (2,1)                      fresh 1
minute 4: rots (2,2)                      fresh 0
answer 4
```

```python
def oranges_rotting(grid):
    R, C = len(grid), len(grid[0])
    q, fresh = deque(), 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2: q.append((r, c))
            elif grid[r][c] == 1: fresh += 1
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1
    return -1 if fresh else minutes
```

The loop condition `while q and fresh` stops as soon as nothing is fresh, so we don't count an extra empty minute.

**Complexity:** O(R·C) time and space.

**Say it in 60 seconds:** "Rot spreads from every rotten orange simultaneously, so I start a BFS with all of them in the queue at once. That's multi-source BFS. I also count fresh oranges. Each round processes exactly the current queue length, which is one minute, rotting fresh neighbours and decrementing the fresh count. I stop when the queue is empty or nothing is fresh. If fresh oranges remain, they're unreachable and I return -1. O(R·C)."

---

### B3. Clone Graph

**Problem in one sentence:** deep-copy a connected undirected graph given one node.

**Key insight:** DFS with a hashmap old → clone. Create the clone and store it in the map **before** recursing into neighbors. That handles cycles: when DFS comes back around to a node, the map already has its clone, so you reuse it instead of looping forever.

**Dry run** on a triangle 1 - 2 - 3 - 1:

```text
dfs(1): clone 1', map {1:1'}; neighbour 2
  dfs(2): clone 2', map {1,2}; neighbour 1 -> in map, use 1'; neighbour 3
    dfs(3): clone 3'; neighbour 1 -> 1' (in map); neighbour 2 -> 2' (in map)
  2'.neighbors = [1', 3']
1'.neighbors = [2', 3']
```

```python
def clone_graph(node):
    if not node:
        return None
    clones = {}
    def dfs(n):
        if n in clones:
            return clones[n]
        copy = Node(n.val)
        clones[n] = copy
        for nb in n.neighbors:
            copy.neighbors.append(dfs(nb))
        return copy
    return dfs(node)
```

`Node` is the problem's class with `val` and `neighbors`.

**Complexity:** O(V + E) time and O(V) space.

**Say it in 60 seconds:** "I walk the graph with DFS and keep a map from original node to its copy. When I visit a node, I first check the map. If it's there, I return the existing copy, which is what stops cycles from recursing forever. Otherwise I create the copy, register it in the map immediately, and then recursively clone each neighbour and attach it. Every node and edge is handled once, O(V + E)."

---

### B4. Word Ladder (implicit BFS)

**Problem in one sentence:** transform a begin word into an end word by changing one letter at a time, where every intermediate word must be in a list. Return the length of the shortest sequence.

**Key insight:** each word is a node, and there's an edge if words differ by one letter. "Shortest sequence" in an unweighted graph means BFS. Finding neighbours by comparing every pair is O(N²·L), so pre-build wildcard buckets: `h*t → [hot, hit]`. Words in the same bucket are neighbours. Bidirectional BFS (searching from both ends and meeting in the middle) halves the explored frontier.

**Dry run** on `begin = "hit"`, `end = "cog"`, `words = [hot, dot, dog, lot, log, cog]`:

```text
level 1: hit
level 2: hot          (via bucket h*t)
level 3: dot, lot     (via *ot)
level 4: dog, log     (via do*, lo*)
level 5: cog          (via *og) -> answer 5
```

```python
def ladder_length(begin, end, words):
    words = set(words)
    if end not in words:
        return 0
    buckets = defaultdict(list)
    for w in words | {begin}:
        for i in range(len(w)):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)
    q, seen = deque([(begin, 1)]), {begin}
    while q:
        w, d = q.popleft()
        if w == end:
            return d
        for i in range(len(w)):
            key = w[:i] + "*" + w[i + 1:]
            for nxt in buckets[key]:
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, d + 1))
            buckets[key] = []          # each bucket expanded once
    return 0
```

Emptying a bucket after it's used is safe because every word in it has been marked seen. It stops BFS from re-scanning large buckets.

**Complexity:** O(N · L²) time, where N is the number of words and L the word length (N·L patterns, each costing O(L) to build). O(N · L²) space for the buckets.

**Say it in 60 seconds:** "Words are nodes and one-letter changes are edges, and I want the fewest steps, so it's BFS. Comparing every pair of words to find edges is too slow, so I pre-group words by wildcard patterns like 'h*t'. Any two words sharing a pattern are neighbours. BFS from the begin word, tracking the level, and return the level when I reach the end word. I clear each bucket after using it so it's never scanned twice. To go faster, I'd run BFS from both ends and stop when the frontiers meet."

---

## C. Cycle detection

### The idea

A **cycle** is a path that starts and ends at the same node. In an undirected graph, any edge back to an already-visited node that isn't your parent closes a cycle. In a directed graph you need more care, because reaching an already-finished node from a different branch is not a cycle (two arrows into one node is fine). Only reaching a node that's **still on the current DFS path** is.

**Analogy (directed):** following a chain of "this task waits for that task". If you ever find yourself waiting for a task that's already in your own waiting chain, that's a deadlock, which is a cycle.

- **Undirected:** DFS where a visited neighbor that isn't the parent means a cycle. Or DSU: union returns false if both ends are already connected.
- **Directed:** three colors (white = unvisited, gray = on the current stack, black = done). An edge to a **gray** node means a cycle. Or Kahn's algorithm: if the topological order has fewer than V nodes, there's a cycle.

### When to recognise it

- "Can all courses be finished?", "is there a circular dependency?", "deadlock".
- "Is this graph a tree?" (connected and no cycle).
- "Find the redundant edge".

### Hand-traced example

Directed edges `0 → 1 → 2 → 0`:

```text
dfs(0): color 0 gray
  dfs(1): color 1 gray
    dfs(2): color 2 gray
      edge 2 -> 0, and 0 is gray (still on the path) -> cycle
```

Compare with `0 → 1`, `0 → 2`, `1 → 2`: when DFS from 0 reaches 2 the second time (via 0 → 2), node 2 is already **black** (finished), so it's not a cycle.

### Template

```python
def has_cycle_directed(n, edges):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
    color = [0] * n        # 0 white, 1 gray, 2 black
    def dfs(u):
        color[u] = 1
        for v in g[u]:
            if color[v] == 1 or (color[v] == 0 and dfs(v)):
                return True
        color[u] = 2
        return False
    return any(color[u] == 0 and dfs(u) for u in range(n))
```

**Complexity:** O(V + E) time, O(V) space.

### Common mistakes

- Using a single visited set for directed graphs, which reports false cycles on "diamond" shapes.
- In undirected DFS, forgetting to skip the edge back to the parent, which reports every edge as a cycle.

**Say it in 60 seconds:** "For a directed graph I use three colours. White is unvisited, gray means it's on the current DFS path, black means fully explored. If I ever follow an edge to a gray node, I've looped back into my own path, which is a cycle. An edge to a black node is fine, it's just another route to a finished node. I start DFS from every white node to cover disconnected parts. O(V + E). For undirected graphs I'd use DSU: if an edge connects two nodes already in the same set, it closes a cycle."

---

## D. Topological sort

### The idea

A **topological order** lists the nodes so that every edge points forward: each task comes after everything it depends on. It only exists in a DAG (directed acyclic graph, a directed graph with no cycles).

**Analogy:** getting dressed. Socks before shoes, shirt before tie, but socks and shirt can be in either order. A topological order is any valid dressing sequence.

**Kahn's algorithm** counts each node's **in-degree** (how many prerequisites it still waits on). Start with every node at in-degree 0. Each time you "complete" a node, decrement its dependents, and any dependent that hits 0 becomes ready.

This maps directly to build systems (Bazel), deployment ordering, and package managers. Mention that.

### When to recognise it

- "Prerequisites", "dependencies", "order of tasks", "build order", "course schedule".
- "Derive an ordering from comparisons" (Alien Dictionary).
- "Minimum number of semesters / rounds" (process by levels).

### Hand-traced example

See the Course Schedule II dry run below.

### Template

The template is the Course Schedule II code below. Complexity O(V + E).

### Common mistakes

- Getting the edge direction backwards. An edge must go from prerequisite to dependent.
- Forgetting to detect a cycle: if the output has fewer than V nodes, some nodes never reached in-degree 0.
- Forgetting nodes with no edges at all. They must still appear in the order.

---

### D1. Course Schedule II (Kahn's algorithm, BFS on in-degree)

**Problem in one sentence:** given n courses and prerequisite pairs, return an order to take all courses, or an empty list if impossible.

**Key insight:** a course is ready when all its prerequisites are done, meaning its in-degree is 0. Repeatedly take a ready course and release its dependents.

**Dry run** on `n = 4`, `prereqs = [[1, 0], [2, 0], [3, 1], [3, 2]]` (course 1 needs 0, and so on):

```text
edges: 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
indeg: 0:0  1:1  2:1  3:2
queue [0]
pop 0 -> order [0];  indeg 1 = 0, 2 = 0 -> queue [1, 2]
pop 1 -> order [0,1]; indeg 3 = 1
pop 2 -> order [0,1,2]; indeg 3 = 0 -> queue [3]
pop 3 -> order [0,1,2,3]
4 nodes in order = n -> valid
```

```python
def find_order(n, prereqs):
    g = defaultdict(list)
    indeg = [0] * n
    for course, pre in prereqs:
        g[pre].append(course)
        indeg[course] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []     # [] means a cycle
```

**Complexity:** O(V + E) time and space.

**Follow-ups:** parallel scheduling (process a level at a time, and the number of levels is the minimum semesters, like how many waves a parallel build needs) and lexicographically smallest order (use a min-heap instead of a queue).

**Say it in 60 seconds:** "This is topological sort. I build edges from prerequisite to course and count in-degrees. Every course with in-degree zero is ready, so it starts in the queue. I pop a course, append it to the order, and decrement its dependents. Any that drop to zero join the queue. If the final order contains all n courses, it's valid. If not, the leftover courses are stuck in a cycle and I return empty. O(V + E). It's the same thing Bazel does to decide what to build first."

---

### D2. Alien Dictionary (hard)

**Problem in one sentence:** given words sorted in an unknown alphabet, deduce a valid letter order.

**Key insight:** only **adjacent** words give information, and only at their first differing letter. If "wrt" comes before "wrf", then t comes before f. That gives edges, and the letter order is a topological sort.

**Steps:** compare adjacent words. The first differing char gives an edge `a → b`. Edge case: if the prefix is longer than the next word (`abc` before `ab`), it's invalid. Then run a topological sort over all chars that appear.

**Dry run** on `["wrt", "wrf", "er", "ett", "rftt"]`:

```text
wrt vs wrf  -> t before f
wrf vs er   -> w before e
er  vs ett  -> r before t
ett vs rftt -> e before r
in-degree 0: w
order: w, e, r, t, f -> "wertf"
```

```python
def alien_order(words):
    g = {c: set() for w in words for c in w}
    indeg = {c: 0 for c in g}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in g[x]:
                    g[x].add(y)
                    indeg[y] += 1
                break
        else:
            if len(a) > len(b):
                return ""
    q = deque(c for c in g if indeg[c] == 0)
    out = []
    while q:
        c = q.popleft()
        out.append(c)
        for d in g[c]:
            indeg[d] -= 1
            if indeg[d] == 0:
                q.append(d)
    return "".join(out) if len(out) == len(g) else ""
```

The `for ... else` runs the `else` only when the inner loop finished without `break`, meaning one word is a prefix of the other. The `if y not in g[x]` check stops a duplicate edge from double-counting in-degree.

**Complexity:** O(C) time, where C is the total number of characters across all words. O(1) space for 26 letters (O(U + edges) for U unique characters).

**Say it in 60 seconds:** "Sorted order tells me about letters only where two adjacent words first differ, so each adjacent pair gives at most one edge. I add every letter that appears as a node, add those edges without duplicates, and run Kahn's algorithm. Two invalid cases: a longer word appearing before its own prefix, like 'abc' before 'ab', and a cycle, which shows up as fewer letters in the output than nodes. O(total characters)."

---

## E. Shortest paths

### The idea

With weights, the shortest path is the cheapest, not the one with the fewest edges, so plain BFS no longer works. **Dijkstra** always expands the closest unfinished node next, using a min-heap. With non-negative weights, the first time a node is popped its distance is final, because any other route would have to pass through something farther away first.

**Analogy:** water spreading through pipes from a source. It reaches nearer junctions first. Once water reaches a junction, no later route can get there sooner, as long as no pipe runs "backwards in time" (a negative weight).

### When to recognise it

- "Minimum cost", "minimum time", "cheapest", "network delay" with weights: Dijkstra.
- "At most k stops" or negative weights: Bellman-Ford.
- Weights are only 0 or 1: 0-1 BFS.
- "Shortest distances between all pairs" with small V: Floyd-Warshall.

### Common mistakes

- Using Dijkstra with negative edges.
- Not skipping stale heap entries, which makes Dijkstra much slower (and wrong if you relax from stale distances).
- For "at most k edges", updating distances in place within a round, which lets one round use several edges.

---

### E1. Dijkstra: Network Delay Time

**Problem in one sentence:** a signal starts at node k and travels along weighted directed edges. How long until every node has it, or -1 if some never do?

**Key insight:** the time a node receives the signal is its shortest-path distance from k. The answer is the largest of those distances. Use Dijkstra with **lazy deletion**: heapq can't decrease a key, so push duplicates and skip any popped node already finalised.

**Dry run** on edges `1→2 (4)`, `1→3 (1)`, `3→2 (1)`, `n = 3`, `k = 1`:

```text
heap               pop     dist after           push
[(0,1)]            (0,1)   {1:0}                (4,2), (1,3)
[(1,3), (4,2)]     (1,3)   {1:0, 3:1}           (2,2)
[(2,2), (4,2)]     (2,2)   {1:0, 3:1, 2:2}
[(4,2)]            (4,2)   2 already final -> skip (stale)
answer max(0, 1, 2) = 2
```

The stale `(4, 2)` entry shows lazy deletion: the direct edge looked like 4, but the route through 3 is cheaper.

```python
def network_delay_time(times, n, k):
    g = defaultdict(list)
    for u, v, w in times:
        g[u].append((v, w))
    dist = {}
    h = [(0, k)]
    while h:
        d, u = heapq.heappop(h)
        if u in dist:
            continue                # stale entry (lazy deletion)
        dist[u] = d
        for v, w in g[u]:
            if v not in dist:
                heapq.heappush(h, (d + w, v))
    return max(dist.values()) if len(dist) == n else -1
```

**Complexity:** O((V + E) log V) time, O(V + E) space.

**Why no negative weights:** once a node is popped it's final, and a negative edge could later make it shorter.

**Variants:** Path with Minimum Effort (the weight is the max edge on the path, so the "distance" is a max instead of a sum), Swim in Rising Water, Cheapest route by cost.

**Say it in 60 seconds:** "Each node receives the signal at its shortest distance from the source, and the answer is the maximum of those. With non-negative weights that's Dijkstra. I keep a min-heap of (distance, node). When I pop a node for the first time, its distance is final, so I record it and push its neighbours with the added edge weight. Python's heap has no decrease-key, so I allow duplicates and skip nodes already finalised. If not every node got a distance, I return -1. O((V + E) log V)."

---

### E2. Cheapest Flights Within K Stops (Bellman-Ford limited to k+1 edges)

**Problem in one sentence:** find the cheapest flight price from src to dst using at most k stops (so at most k + 1 flights).

**Key insight:** **Bellman-Ford** relaxes every edge in rounds, and after round r the distances are the cheapest using at most r edges. So run exactly k + 1 rounds. The crucial detail is to read from the **previous** round's distances (a copy), so one round can't chain several flights.

**Dry run** on flights `0→1 (100)`, `1→2 (100)`, `0→2 (500)`, `src 0`, `dst 2`:

```text
start          dist = [0, inf, inf]
round 1 (k=0)  0->1: 100   1->2: uses old dist[1]=inf, no   0->2: 500
               dist = [0, 100, 500]
round 2 (k=1)  1->2: 100 + 100 = 200 < 500
               dist = [0, 100, 200]
k = 0 answer: 500 (one round)    k = 1 answer: 200 (two rounds)
```

Without the copy, round 1 could use the fresh `dist[1] = 100` immediately and report 200 for k = 0, which breaks the stop limit.

```python
def find_cheapest_price(n, flights, src, dst, k):
    dist = [float("inf")] * n
    dist[src] = 0
    for _ in range(k + 1):
        nxt = dist[:]                     # copy so one round = one more edge
        for u, v, w in flights:
            if dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt
    return -1 if dist[dst] == float("inf") else dist[dst]
```

**Complexity:** O(k · E) time, O(V) space.

**Say it in 60 seconds:** "Dijkstra optimises cost but ignores the number of stops, so I use Bellman-Ford with a fixed number of rounds. Each round relaxes every flight once, and after r rounds I have the cheapest prices using at most r flights. With k stops I need k + 1 rounds. The important detail is that each round reads from a copy of the previous round's prices, so a single round can't chain two flights. O(k·E)."

---

### E3. 0-1 BFS

**Problem in one sentence (the pattern):** shortest path when every edge costs 0 or 1.

**Key insight:** use a deque, pushing 0-weight edges to the front and 1-weight edges to the back. The deque then always stays sorted by distance (it holds at most two distinct distance values at a time), so it behaves like Dijkstra's heap at O(1) per operation. O(V + E). Example: Minimum Cost to Make at Least One Valid Path in a Grid (following the arrow in a cell is free, changing it costs 1).

**Dry run:** edges `A→B (0)`, `A→C (1)`, `B→C (0)` from A. Pop A (0): B gets 0 and goes to the front, C gets 1 and goes to the back. Pop B (0): C improves to 0 and goes to the front. Pop C (0). Final distances A 0, B 0, C 0.

```python
def zero_one_bfs(n, adj, src):          # adj[u] = [(v, w)] with w in {0, 1}
    dist = [float("inf")] * n
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dist
```

**Complexity:** O(V + E) time, O(V) space.

**Say it in 60 seconds:** "When weights are only 0 or 1, I don't need a heap. I use a deque: if an edge is free, the neighbour is as close as the current node, so it goes to the front. If it costs 1, it goes to the back. That keeps the deque ordered by distance, so popping the front always gives the closest node, just like Dijkstra, but each operation is O(1). Total O(V + E)."

---

### E4. Floyd-Warshall (all pairs, small V)

**Problem in one sentence (the pattern):** shortest distances between every pair of nodes.

**Key insight:** allow intermediate nodes one at a time. After considering node k as a possible stop, every distance is the best using stops from {0..k}. `for k: for i: for j: d[i][j] = min(d[i][j], d[i][k] + d[k][j])`. The k loop must be outermost. O(V³). Example: Find the City With the Smallest Number of Neighbors at a Threshold Distance.

**Dry run:** edges `0→1 (3)`, `1→2 (1)`, `0→2 (10)`. Initially `d[0][2] = 10`. With k = 1: `d[0][1] + d[1][2] = 4 < 10`, so `d[0][2] = 4`.

```python
def floyd_warshall(n, edges):
    d = [[float("inf")] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d
```

**Complexity:** O(V³) time, O(V²) space. Fine for V up to about 400.

**Say it in 60 seconds:** "Floyd-Warshall is a DP over which nodes I'm allowed to stop at. Start with direct edges. Then for each node k, check every pair i, j to see if going through k is shorter. The k loop has to be outermost, because each phase builds on paths that only used earlier stops. It's O(V³), so I'd use it only for a few hundred nodes. It also handles negative edges, and a negative value on the diagonal reveals a negative cycle."

---

## F. DSU (Union-Find)

### The idea

A **DSU (disjoint set union)**, also called **union-find**, keeps track of which items are in the same group, and supports two operations: `union(a, b)` merges two groups, and `find(x)` returns the group's representative (its "leader"). Two items are connected exactly when they have the same leader.

Internally it's a forest where each set has a representative. Each item points to a parent, and the root is the leader. Two tricks keep the trees almost flat: **path compression** (while finding the root, point nodes closer to it) and **union by rank/size** (attach the smaller tree under the bigger one). Together they give nearly O(1) (inverse Ackermann, α(n)) per operation.

Use it when edges arrive over time and you only ask "are these connected?" or "how many groups?"

**Analogy:** companies merging. Every employee knows their boss, and the CEO at the top represents the company. To check whether two people work for the same company, follow both chains up to the CEO. When two companies merge, the smaller company's CEO starts reporting to the bigger company's CEO. Path compression is people learning to email the CEO directly next time.

### When to recognise it

- "Connected components", "number of provinces", "groups".
- "Redundant connection", "does adding this edge create a cycle?"
- Items merged by shared attributes (accounts with a shared email).
- Edges arrive one at a time and you must answer after each (online connectivity).
- Kruskal's minimum spanning tree.

### Hand-traced example

Five items, `0..4`, each its own group.

```text
op           parent             components
start        [0, 1, 2, 3, 4]    5
union(0,1)   [0, 0, 2, 3, 4]    4      (1's root now 0)
union(2,3)   [0, 0, 2, 2, 4]    3
union(1,3)   find(1)=0, find(3)=2, equal sizes, attach 2 under 0
             [0, 0, 0, 2, 4]    2
union(0,3)   find(0)=0, find(3)=0, same root -> returns False (would be a cycle)
```

### Template

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True
```

**Path halving** (pointing each node to its grandparent while walking up) is a simple form of path compression that is iterative, so it can't overflow the recursion stack.

**Complexity:** O(α(n)) amortized per operation, which is effectively constant. O(n) space.

### Common mistakes

- Comparing `parent[a] == parent[b]` instead of `find(a) == find(b)`. Parents aren't necessarily roots.
- Forgetting union by size, which can produce long chains and O(n) finds.
- Mapping non-integer items (emails, coordinates) to indices inconsistently.

---

### F1. Number of Connected Components / Graph Valid Tree

**Problems in one sentence:** count the connected groups in an undirected graph; decide whether the graph is a single tree.

**Key insight:** components = n minus the number of successful unions. A tree on n nodes has exactly n - 1 edges **and** every union succeeds (no cycle). With n - 1 edges and no cycle, it must also be connected.

**Dry run (valid tree)** on `n = 4`, edges `(0,1), (0,2), (0,3)`: 3 edges = n - 1, and all three unions succeed, so it's a tree. Add edge `(1,2)`: now 4 edges, fails the count check immediately.

```python
def count_components(n, edges):
    dsu = DSU(n)
    for a, b in edges:
        dsu.union(a, b)
    return dsu.components

def valid_tree(n, edges):
    if len(edges) != n - 1:
        return False
    dsu = DSU(n)
    return all(dsu.union(a, b) for a, b in edges)
```

**Complexity:** O(E · α(n)) time, O(n) space.

**Say it in 60 seconds:** "Each successful union merges two components, so the component count is n minus the successful unions, which my DSU tracks directly. For valid tree, a tree has exactly n minus 1 edges and no cycles. I check the edge count first, then union every edge. If any union fails, both ends were already connected, so that edge closes a cycle. With the right count and no cycle, the graph is connected too. Near-linear time."

---

### F2. Redundant Connection

**Problem in one sentence:** a tree had one extra edge added. Return the edge that can be removed to restore a tree (the last one in input order that creates a cycle).

**Key insight:** process edges in order. Return the first edge whose union returns False, because its two ends were already connected.

**Dry run** on `[[1, 2], [1, 3], [2, 3]]`: union(1,2) succeeds, union(1,3) succeeds, union(2,3) fails because 2 and 3 already share root 1, so the answer is `[2, 3]`.

```python
def find_redundant_connection(edges):
    dsu = DSU(len(edges) + 1)            # nodes are 1-indexed
    for a, b in edges:
        if not dsu.union(a, b):
            return [a, b]
```

**Complexity:** O(n · α(n)) time, O(n) space.

**Say it in 60 seconds:** "I add edges one at a time with union-find. The first edge whose endpoints already share a root would create a cycle, and since there's exactly one extra edge, that's the answer. Nodes are numbered from 1, so I size the DSU one bigger. Near-linear time."

---

### F3. Accounts Merge

**Problem in one sentence:** each account is a name plus emails. Accounts sharing any email belong to the same person. Merge them.

**Key insight:** union emails that appear in the same account (map each email to an id). Here the account index is the id: the first time an email is seen, record which account owns it. If a later account has the same email, union the two accounts. Then group emails by root, sort, and attach the name.

**Dry run** on `[["John", "a", "b"], ["John", "c"], ["John", "b", "d"]]`:

```text
account 0: a -> owner 0, b -> owner 0
account 1: c -> owner 1
account 2: b already owned by 0 -> union(2, 0); d -> owner 2
groups by root: {root of 0 and 2: [a, b, d], root of 1: [c]}
answer [["John", "a", "b", "d"], ["John", "c"]]
```

```python
def accounts_merge(accounts):
    dsu = DSU(len(accounts))
    owner = {}
    for i, acc in enumerate(accounts):
        for email in acc[1:]:
            if email in owner:
                dsu.union(i, owner[email])
            else:
                owner[email] = i
    groups = defaultdict(list)
    for email, i in owner.items():
        groups[dsu.find(i)].append(email)
    return [[accounts[i][0]] + sorted(es) for i, es in groups.items()]
```

**Complexity:** O(N·α + N log N) for N total emails, where the log factor is the sorting.

**Say it in 60 seconds:** "Two accounts are the same person if they share an email, and that relation is transitive, so it's connected components. I give each account an index in a DSU and record the first account that owns each email. When another account lists an email that's already owned, I union the two accounts. Afterwards I group every email under its account's root, sort each group, and prefix the name. The sort dominates, O(N log N)."

---

### F4. Number of Islands II (islands added over time)

**Problem in one sentence:** cells of an all-water grid turn into land one at a time. Report the island count after each addition.

**Key insight:** each new land cell unions with its land neighbors. Start by counting it as a new island, and subtract one for every successful union with a neighbouring island. Record the component count after each addition. That's online connectivity, which BFS can't do efficiently (re-running BFS after every addition would be O(k · R · C)).

**Dry run** on a 3 × 3 grid, adding `(0,0), (0,1), (1,2), (2,1), (1,1)`:

```text
add    new island  unions with neighbours          islands
(0,0)  +1                                          1
(0,1)  +1          (0,0) merges, -1                1
(1,2)  +1                                          2
(2,1)  +1                                          3
(1,1)  +1          (0,1) -1, (1,2) -1, (2,1) -1    1
answer [1, 1, 2, 3, 1]
```

```python
def num_islands2(m, n, positions):
    dsu = DSU(m * n)
    land = set()
    res, islands = [], 0
    for r, c in positions:
        if (r, c) in land:
            res.append(islands)
            continue
        land.add((r, c))
        islands += 1
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if (nr, nc) in land and dsu.union(r * n + c, nr * n + nc):
                islands -= 1
        res.append(islands)
    return res
```

Cell `(r, c)` is index `r * n + c` in the DSU. I keep a separate island counter because `dsu.components` would also count water cells.

**Complexity:** O(k · α(m·n)) for k additions, plus O(m·n) to initialise.

**Say it in 60 seconds:** "Re-running BFS after each addition would be far too slow, so I use union-find, which handles merges incrementally. When a cell becomes land, it starts as its own island, so the count goes up by one. Then I try to union it with each land neighbour, and every successful union merges two islands, so the count goes down by one. Duplicate additions don't change anything. Each addition is near-constant time."

---

### F5. Min Cost to Connect All Points (Kruskal)

**Problem in one sentence:** connect all points with the minimum total Manhattan-distance wiring.

**Key insight:** a **minimum spanning tree (MST)** connects all nodes with the smallest total edge weight and no cycles. **Kruskal's algorithm**: sort all edges by weight and union greedily, skipping any edge whose ends are already connected. Stop at n - 1 edges. Greedy is correct because the cheapest edge crossing any split of the nodes is always safe to take. For dense graphs, Prim's O(V²) without a heap is better.

**Dry run** on points `(0,0), (1,1), (3,0)`:

```text
edges: (0-1, 2), (0-2, 3), (1-2, 3)   sorted
take 0-1 (2): union ok, cost 2
take 0-2 (3): union ok, cost 5, used 2 = n - 1, stop
answer 5
```

```python
def min_cost_connect_points(points):
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            edges.append((d, i, j))
    edges.sort()
    dsu, cost, used = DSU(n), 0, 0
    for d, i, j in edges:
        if dsu.union(i, j):
            cost += d
            used += 1
            if used == n - 1:
                break
    return cost
```

**Complexity:** O(n² log n) time, because there are n² edges to sort. O(n²) space for the edge list.

**Say it in 60 seconds:** "This is a minimum spanning tree. With Kruskal's algorithm I list every pair's distance, sort them, and take edges cheapest first, using union-find to skip any edge that would join two already-connected points. After n minus 1 edges, everything is connected. Here every pair is an edge, so the graph is dense, n² edges, and sorting costs O(n² log n). Prim's algorithm with an array instead of a heap is O(n²) and uses less memory, so I'd mention that as the better choice for dense graphs."

---

### DSU uses in systems (good talking points)

- **Grouping duplicate records (entity resolution).** The same idea as my SHA-256 natural keys at Uber FRM (a deterministic key built from the record's content so the same record always gets the same id), but for fuzzy matches: if record A matches B and B matches C, union them so all three become one entity.
- **Network partition detection:** which nodes can still reach each other after links fail.
- **Kruskal for cheap network links:** connecting data centres or racks with minimum total cable or link cost.

---

## G. Advanced (know the idea)

- **Tarjan SCC / bridges:** a **bridge** is an edge whose removal disconnects the graph. Tarjan's DFS records `disc[u]` (when u was discovered) and `low[u]` (the earliest discovery time reachable from u's subtree using one back edge): `low[u] = min(disc[u], low of children, disc of back edges)`. An edge u-v is a bridge if `low[v] > disc[u]`, meaning v's subtree has no other way back. Example: Critical Connections in a Network. That's **single points of failure** in a network, a nice OCI tie-in.
- **Bipartite check:** a graph is **bipartite** if you can colour every node one of two colours with no edge joining same-coloured nodes. BFS 2-coloring. Example: Is Graph Bipartite, Possible Bipartition.
- **Eulerian path:** a path that uses every **edge** exactly once. Hierholzer's algorithm. Example: Reconstruct Itinerary (use a min-heap for lexical order).
- **A\*:** Dijkstra plus an admissible heuristic (an estimate of remaining distance that never overestimates, like straight-line distance on a map), which steers the search toward the goal.

### G1. Critical Connections in a Network (bridges)

**Dry run** on `n = 4`, edges `0-1, 1-2, 2-0, 1-3`:

```text
dfs(0) disc 0
  dfs(1) disc 1
    dfs(2) disc 2, back edge to 0 -> low[2] = 0
    low[1] = min(1, 0) = 0; low[2]=0 > disc[1]=1? no
    dfs(3) disc 3, no back edges -> low[3] = 3
    low[3]=3 > disc[1]=1 -> bridge [1, 3]
answer [[1, 3]]
```

```python
def critical_connections(n, connections):
    g = defaultdict(list)
    for a, b in connections:
        g[a].append(b); g[b].append(a)
    disc = [-1] * n
    low = [0] * n
    res, timer = [], [0]
    def dfs(u, parent):
        disc[u] = low[u] = timer[0]; timer[0] += 1
        for v in g[u]:
            if v == parent:
                continue
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    res.append([u, v])
            else:
                low[u] = min(low[u], disc[v])
    for u in range(n):
        if disc[u] == -1:
            dfs(u, -1)
    return res
```

Skipping the parent by node id assumes there are no parallel edges, which the LeetCode problem guarantees.

**Say it in 60 seconds:** "A bridge is an edge that, if cut, disconnects the graph. During DFS I record each node's discovery time and the lowest discovery time its subtree can reach through a back edge. For a tree edge from u to child v, if v's low value is still greater than u's discovery time, nothing under v can get back above u except through that edge, so it's a bridge. One DFS, O(V + E). In infrastructure terms these are single points of failure."

### G2. Is Graph Bipartite

```python
def is_bipartite(graph):
    color = {}
    for s in range(len(graph)):
        if s in color:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True
```

**Dry run:** a square `0-1-2-3-0` colours 0, 1, 0, 1 with no clash, so it's bipartite. A triangle `0-1-2-0` colours 0, 1, then node 2 must differ from both, which is impossible, so it isn't. Any odd cycle makes a graph non-bipartite.

**Say it in 60 seconds:** "I try to 2-colour the graph with BFS. The start node gets colour 0, each neighbour gets the opposite colour, and if I ever find an edge between two nodes of the same colour, it's not bipartite. I restart BFS from every uncoloured node to cover disconnected parts. O(V + E)."

---

## Graph problem checklist

1. Build the graph correctly (directed? both directions for undirected).
2. Choose BFS for fewest steps, Dijkstra for weights, topo for dependencies, DSU for dynamic grouping.
3. Visited set: mark on push.
4. Disconnected graphs: loop over all nodes as possible starts.
5. Complexity: O(V + E) for traversal. State it with V and E defined ("V is the number of courses, E the number of prerequisite pairs").
