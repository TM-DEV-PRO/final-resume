# 03.4 Graphs: BFS, DFS, topological sort, shortest paths, MST, DSU

---

## A. Representations and the three questions

- **Adjacency list** `graph = defaultdict(list)`: O(V + E) space, the default.
- **Adjacency matrix:** O(V²), for dense graphs or quick edge checks.
- **Grid as a graph:** cell = node, 4 or 8 neighbors.
- **Implicit graph:** states generated on the fly (Word Ladder, lock combinations).

Ask: **directed or undirected? weighted? cycles possible? connected?**

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

---

## B. DFS and BFS templates

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

### B1. Number of Islands (grid DFS/BFS)

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
O(R·C). Variants: Max Area of Island, Surrounded Regions (flood from the border first), Pacific Atlantic (reverse flow: BFS from each ocean, then intersect).

### B2. Rotting Oranges (multi-source BFS)
Put **all** rotten oranges in the queue at time 0, then BFS level by level. The answer is the number of levels, or -1 if fresh oranges remain. Same idea: Walls and Gates, 01 Matrix, and distance from the nearest server.

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

### B3. Clone Graph
DFS with a hashmap old → clone. Create the clone before recursing into neighbors (handles cycles).

### B4. Word Ladder (implicit BFS)
**Intuition:** each word is a node, and there's an edge if words differ by one letter. Pre-build wildcard buckets: `h*t → [hot, hit]`. BFS from the begin word. Bidirectional BFS halves the explored frontier.

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
O(N · L²).

---

## C. Cycle detection

- **Undirected:** DFS where a visited neighbor that isn't the parent means a cycle. Or DSU: union returns false if both ends are already connected.
- **Directed:** three colors (white = unvisited, gray = on the current stack, black = done). An edge to a **gray** node means a cycle. Or Kahn's algorithm: if the topological order has fewer than V nodes, there's a cycle.

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

---

## D. Topological sort

**Intuition:** order tasks so every dependency comes first. Only possible in a DAG. This maps directly to build systems (Bazel), deployment ordering, and package managers. Mention that.

### D1. Course Schedule II (Kahn's algorithm, BFS on in-degree)

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
O(V + E). Follow-ups: parallel scheduling (process a level at a time, and the number of levels is the minimum semesters) and lexicographically smallest order (use a min-heap instead of a queue).

### D2. Alien Dictionary (hard)
**Steps:** compare adjacent words. The first differing char gives an edge `a → b`. Edge case: if the prefix is longer than the next word (`abc` before `ab`), it's invalid. Then run a topological sort over all chars that appear.

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

---

## E. Shortest paths

### E1. Dijkstra: Network Delay Time

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
O((V + E) log V). **Why no negative weights:** once a node is popped it's final, and a negative edge could later make it shorter. Variants: Path with Minimum Effort (the weight is the max edge on the path), Swim in Rising Water, Cheapest route by cost.

### E2. Cheapest Flights Within K Stops (Bellman-Ford limited to k+1 edges)

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
O(k · E).

### E3. 0-1 BFS
If weights are only 0 or 1: use a deque, pushing 0-weight edges to the front and 1-weight edges to the back. O(V + E). Example: Minimum Cost to Make at Least One Valid Path in a Grid.

### E4. Floyd-Warshall (all pairs, small V)
`for k: for i: for j: d[i][j] = min(d[i][j], d[i][k] + d[k][j])`. O(V³). Example: Find the City With the Smallest Number of Neighbors.

---

## F. DSU (Union-Find)

**Intuition:** keep a forest where each set has a representative. `find` with **path compression** plus `union` by **rank/size** gives nearly O(1) (inverse Ackermann) per operation. Use it when edges arrive over time and you only ask "are these connected?" or "how many groups?"

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

### F1. Number of Connected Components / Graph Valid Tree
Valid tree: exactly n - 1 edges **and** every union succeeds (no cycle).

### F2. Redundant Connection
Return the first edge whose union returns False.

### F3. Accounts Merge
Union emails that appear in the same account (map each email to an id). Group emails by root, sort, and attach the name.

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
O(N·α + N log N) for the sorting.

### F4. Number of Islands II (islands added over time)
Each new land cell unions with its land neighbors. Record the component count after each addition. That's online connectivity, which BFS can't do efficiently.

### F5. Min Cost to Connect All Points (Kruskal)
Sort all edges by weight and union greedily. Stop at n - 1 edges. For dense graphs, Prim's O(V²) without a heap is better.

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

### DSU uses in systems (good talking points)
- Grouping duplicate records (entity resolution). The same idea as my SHA-256 natural keys at Uber FRM, but for fuzzy matches.
- Network partition detection: which nodes can still reach each other.
- Kruskal for cheap network links.

---

## G. Advanced (know the idea)

- **Tarjan SCC / bridges:** `low[u] = min(disc[u], low of children, disc of back edges)`. An edge u-v is a bridge if `low[v] > disc[u]`. Example: Critical Connections in a Network. That's **single points of failure** in a network, a nice OCI tie-in.
- **Bipartite check:** BFS 2-coloring. Example: Is Graph Bipartite, Possible Bipartition.
- **Eulerian path:** Hierholzer's algorithm. Example: Reconstruct Itinerary (use a min-heap for lexical order).
- **A\*:** Dijkstra plus an admissible heuristic.

---

## Graph problem checklist

1. Build the graph correctly (directed? both directions for undirected).
2. Choose BFS for fewest steps, Dijkstra for weights, topo for dependencies, DSU for dynamic grouping.
3. Visited set: mark on push.
4. Disconnected graphs: loop over all nodes as possible starts.
5. Complexity: O(V + E) for traversal. State it with V and E defined.
