# 05. LLD problems with full designs and code

Each problem: requirements, entities, key decisions, code for the core, concurrency, and extensions. Foundations: [05 LLD foundations](05_lld_foundations.md).

---

## 1. LRU cache (most asked, often with "make it thread safe")

**Requirements:** `get(key)` and `put(key, value)` in O(1). Capacity limit; evict the least recently used.

**Design:** hashmap key → node, plus a doubly linked list ordered by recency (head = most recent). Sentinel head/tail nodes remove edge cases.

```python
import threading

class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key=None, val=None):
        self.key, self.val, self.prev, self.next = key, val, None, None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map = {}
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head
        self.lock = threading.Lock()

    def _remove(self, n):
        n.prev.next, n.next.prev = n.next, n.prev

    def _add_front(self, n):
        n.prev, n.next = self.head, self.head.next
        self.head.next.prev = n
        self.head.next = n

    def get(self, key):
        with self.lock:
            n = self.map.get(key)
            if not n:
                return None
            self._remove(n)
            self._add_front(n)
            return n.val

    def put(self, key, val):
        with self.lock:
            n = self.map.get(key)
            if n:
                n.val = val
                self._remove(n)
                self._add_front(n)
                return
            if len(self.map) >= self.cap:
                lru = self.tail.prev
                self._remove(lru)
                del self.map[lru.key]
            n = Node(key, val)
            self.map[key] = n
            self._add_front(n)
```

Python shortcut (say you know it): `collections.OrderedDict` with `move_to_end` and `popitem(last=False)`.

**Go version with a mutex** (uses `container/list`):

```go
type entry struct {
    key string
    val []byte
}

type LRU struct {
    mu    sync.Mutex
    cap   int
    ll    *list.List
    items map[string]*list.Element
}

func NewLRU(cap int) *LRU {
    return &LRU{cap: cap, ll: list.New(), items: make(map[string]*list.Element)}
}

func (c *LRU) Get(k string) ([]byte, bool) {
    c.mu.Lock()
    defer c.mu.Unlock()
    if e, ok := c.items[k]; ok {
        c.ll.MoveToFront(e)
        return e.Value.(*entry).val, true
    }
    return nil, false
}

func (c *LRU) Put(k string, v []byte) {
    c.mu.Lock()
    defer c.mu.Unlock()
    if e, ok := c.items[k]; ok {
        e.Value.(*entry).val = v
        c.ll.MoveToFront(e)
        return
    }
    if c.ll.Len() >= c.cap {
        old := c.ll.Back()
        c.ll.Remove(old)
        delete(c.items, old.Value.(*entry).key)
    }
    c.items[k] = c.ll.PushFront(&entry{k, v})
}
```

**Concurrency discussion:**
- Even `get` mutates the list, so a read-write lock doesn't help (every op writes). Use one mutex.
- To scale: **shard** the cache into N segments by `hash(key) % N`, each with its own lock (like Java's old ConcurrentHashMap). That's approximate LRU globally, which is fine.
- Or sample-based LRU (Redis evicts the oldest of 5 random keys), which has no list and less contention.
- **Extensions:** TTL per entry (store an expiry, check on get, plus a background sweeper), size-based capacity (track bytes), eviction callbacks, and metrics (hit rate).

---

## 2. LFU cache (O(1))

**Design:** `key → (value, freq)`, `freq → OrderedDict of keys` (LRU order within a frequency), and a `min_freq` pointer.

```python
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.vals = {}                         # key -> (val, freq)
        self.buckets = defaultdict(OrderedDict)
        self.min_freq = 0

    def _touch(self, key):
        val, f = self.vals[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq += 1
        self.vals[key] = (val, f + 1)
        self.buckets[f + 1][key] = None

    def get(self, key):
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key][0]

    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.vals:
            self.vals[key] = (value, self.vals[key][1])
            self._touch(key)
            return
        if len(self.vals) >= self.cap:
            old, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.vals[old]
        self.vals[key] = (value, 1)
        self.buckets[1][key] = None
        self.min_freq = 1
```

---

## 3. Rate limiter library (Strategy + thread safety)

**Requirements:** `allow(key) -> bool`. Pluggable algorithms (token bucket, sliding window). Per-key limits. Thread-safe. An injectable clock for tests.

```python
import threading, time
from abc import ABC, abstractmethod
from collections import deque

class RateLimiter(ABC):
    @abstractmethod
    def allow(self, key: str) -> bool: ...

class TokenBucketLimiter(RateLimiter):
    def __init__(self, rate: float, capacity: int, clock=time.monotonic):
        self.rate, self.cap, self.clock = rate, capacity, clock
        self.buckets = {}                     # key -> [tokens, last]
        self.lock = threading.Lock()

    def allow(self, key):
        now = self.clock()
        with self.lock:
            tokens, last = self.buckets.get(key, (self.cap, now))
            tokens = min(self.cap, tokens + (now - last) * self.rate)
            if tokens >= 1:
                self.buckets[key] = (tokens - 1, now)
                return True
            self.buckets[key] = (tokens, now)
            return False

class SlidingWindowLogLimiter(RateLimiter):
    def __init__(self, limit: int, window_s: float, clock=time.monotonic):
        self.limit, self.window, self.clock = limit, window_s, clock
        self.logs = {}
        self.lock = threading.Lock()

    def allow(self, key):
        now = self.clock()
        with self.lock:
            q = self.logs.setdefault(key, deque())
            while q and q[0] <= now - self.window:
                q.popleft()
            if len(q) < self.limit:
                q.append(now)
                return True
            return False
```

**Go token bucket** (per-key, lock striping would be the next step):

```go
type bucket struct {
    tokens float64
    last   time.Time
}

type TokenBucket struct {
    mu      sync.Mutex
    rate    float64 // tokens per second
    cap     float64
    buckets map[string]*bucket
    now     func() time.Time
}

func (tb *TokenBucket) Allow(key string) bool {
    tb.mu.Lock()
    defer tb.mu.Unlock()
    t := tb.now()
    b, ok := tb.buckets[key]
    if !ok {
        b = &bucket{tokens: tb.cap, last: t}
        tb.buckets[key] = b
    }
    b.tokens = math.Min(tb.cap, b.tokens+t.Sub(b.last).Seconds()*tb.rate)
    b.last = t
    if b.tokens >= 1 {
        b.tokens--
        return true
    }
    return false
}
```

**Discussion:** a global lock is a bottleneck, so use a lock per key (a map of locks, itself guarded) or striped locks. Evict idle keys (LRU/TTL) so memory doesn't grow forever. Distributed version: [system design Q1](04_system_design_questions.md).

---

## 4. Parking lot

**Requirements (clarify):** multiple floors; spot types (motorcycle, compact, large, EV); vehicles park in a fitting spot; tickets on entry; pay on exit with pluggable pricing; show free spots per type; multiple entry gates at once (concurrency).

**Entities:** `ParkingLot`, `Floor`, `Spot` (type, id, occupied), `Vehicle` (type, plate), `Ticket`, `SpotAssignmentStrategy`, `PricingStrategy`, `Payment`.

```python
from dataclasses import dataclass, field
from enum import Enum
import itertools, threading, time, uuid

class VehicleType(Enum):
    BIKE = 1; CAR = 2; TRUCK = 3

class SpotType(Enum):
    SMALL = 1; MEDIUM = 2; LARGE = 3

FITS = {
    VehicleType.BIKE: [SpotType.SMALL, SpotType.MEDIUM, SpotType.LARGE],
    VehicleType.CAR: [SpotType.MEDIUM, SpotType.LARGE],
    VehicleType.TRUCK: [SpotType.LARGE],
}

@dataclass
class Spot:
    id: str
    floor: int
    type: SpotType
    vehicle: "Vehicle | None" = None

@dataclass(frozen=True)
class Vehicle:
    plate: str
    type: VehicleType

@dataclass
class Ticket:
    id: str
    vehicle: Vehicle
    spot: Spot
    entry_ts: float

class PricingStrategy:
    def price(self, ticket: Ticket, exit_ts: float) -> float:
        raise NotImplementedError

class HourlyPricing(PricingStrategy):
    RATES = {SpotType.SMALL: 1.0, SpotType.MEDIUM: 2.0, SpotType.LARGE: 4.0}
    def price(self, ticket, exit_ts):
        hours = max(1, -(-int(exit_ts - ticket.entry_ts) // 3600))   # ceil
        return hours * self.RATES[ticket.spot.type]

class ParkingLot:
    def __init__(self, spots, pricing: PricingStrategy, clock=time.time):
        self.free = {t: [] for t in SpotType}       # free spot stacks per type
        for s in spots:
            self.free[s.type].append(s)
        self.active = {}                            # ticket_id -> Ticket
        self.pricing, self.clock = pricing, clock
        self.lock = threading.Lock()

    def park(self, vehicle: Vehicle) -> Ticket:
        with self.lock:                             # two gates can't grab the same spot
            for st in FITS[vehicle.type]:
                if self.free[st]:
                    spot = self.free[st].pop()
                    spot.vehicle = vehicle
                    t = Ticket(str(uuid.uuid4()), vehicle, spot, self.clock())
                    self.active[t.id] = t
                    return t
        raise RuntimeError("lot full for this vehicle type")

    def leave(self, ticket_id: str) -> float:
        with self.lock:
            t = self.active.pop(ticket_id)
            fee = self.pricing.price(t, self.clock())
            t.spot.vehicle = None
            self.free[t.spot.type].append(t.spot)
            return fee

    def availability(self):
        with self.lock:
            return {t.name: len(v) for t, v in self.free.items()}
```

**Talking points:**
- Spot assignment is a **strategy** (nearest to the gate: a min-heap per type keyed by distance).
- Pricing is a **strategy** (hourly, flat, weekend, EV surcharge).
- **Concurrency:** one lock is simple and correct at gate throughput. At scale: a lock per spot type, or a DB with `SELECT ... FOR UPDATE SKIP LOCKED` to claim a free spot.
- **Extensions:** reservations, display boards (**observer** on availability changes), and payment methods (strategy).

---

## 5. In-memory key-value store with TTL and transactions

**Requirements:** `set`, `get`, `delete`, `set(key, val, ttl)`, `begin`, `commit`, `rollback` (nested transactions). Thread-safe.

```python
import heapq, threading, time

class KVStore:
    def __init__(self, clock=time.monotonic):
        self.data = {}              # key -> (value, expires_at or None)
        self.expiry = []            # heap of (expires_at, key)
        self.tx = []                # stack of dicts: key -> old value or _MISSING
        self.clock = clock
        self.lock = threading.RLock()

    _MISSING = object()

    def _expired(self, key):
        v = self.data.get(key)
        return v is not None and v[1] is not None and v[1] <= self.clock()

    def get(self, key):
        with self.lock:
            if self._expired(key):
                del self.data[key]                  # lazy expiry
            v = self.data.get(key)
            return None if v is None else v[0]

    def _record(self, key):
        if self.tx and key not in self.tx[-1]:
            self.tx[-1][key] = self.data.get(key, self._MISSING)

    def set(self, key, value, ttl=None):
        with self.lock:
            self._record(key)
            exp = self.clock() + ttl if ttl else None
            self.data[key] = (value, exp)
            if exp:
                heapq.heappush(self.expiry, (exp, key))

    def delete(self, key):
        with self.lock:
            self._record(key)
            self.data.pop(key, None)

    def begin(self):
        with self.lock:
            self.tx.append({})

    def rollback(self):
        with self.lock:
            if not self.tx:
                raise RuntimeError("no transaction")
            for key, old in self.tx.pop().items():
                if old is self._MISSING:
                    self.data.pop(key, None)
                else:
                    self.data[key] = old

    def commit(self):
        with self.lock:
            if not self.tx:
                raise RuntimeError("no transaction")
            changes = self.tx.pop()
            if self.tx:                         # nested: merge undo info into the parent
                for k, old in changes.items():
                    self.tx[-1].setdefault(k, old)

    def sweep(self):
        """Active expiry, run by a background thread."""
        with self.lock:
            now = self.clock()
            while self.expiry and self.expiry[0][0] <= now:
                exp, key = heapq.heappop(self.expiry)
                v = self.data.get(key)
                if v and v[1] == exp:           # skip stale heap entries
                    del self.data[key]
```

**Talking points:** lazy + active expiry (like Redis). The undo log per transaction level makes rollback O(changes). Note this transaction model is single-client (global); multi-client isolation would need MVCC or per-session write sets with commit-time conflict checks (optimistic concurrency). Persistence: an append-only log (AOF) + snapshots.

---

## 6. Logger / logging framework

**Requirements:** levels (DEBUG, INFO, WARN, ERROR), multiple sinks (console, file, remote), formatting, async (don't block callers), and thread-safe.

**Design:**
- `Logger` has a level filter and a list of `Handler`s (chain of responsibility / observer).
- `Formatter` is a strategy (JSON, text).
- `AsyncHandler` decorates another handler: a bounded queue + a worker thread. When the queue is full, it drops DEBUG and blocks or drops with a counter for others. Say which you choose.

```python
import queue, threading, json, time, sys

class Handler:
    def emit(self, record: dict): raise NotImplementedError

class ConsoleHandler(Handler):
    def emit(self, record):
        sys.stdout.write(json.dumps(record) + "\n")

class AsyncHandler(Handler):
    def __init__(self, inner: Handler, maxsize=10_000):
        self.inner, self.q = inner, queue.Queue(maxsize)
        self.dropped = 0
        threading.Thread(target=self._run, daemon=True).start()

    def emit(self, record):
        try:
            self.q.put_nowait(record)
        except queue.Full:
            self.dropped += 1                   # never block the request path

    def _run(self):
        while True:
            self.inner.emit(self.q.get())

class Logger:
    LEVELS = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40}

    def __init__(self, name, level="INFO", handlers=()):
        self.name, self.level, self.handlers = name, self.LEVELS[level], list(handlers)

    def log(self, level, msg, **fields):
        if self.LEVELS[level] < self.level:
            return
        rec = {"ts": time.time(), "level": level, "logger": self.name, "msg": msg, **fields}
        for h in self.handlers:
            h.emit(rec)

    def info(self, msg, **f): self.log("INFO", msg, **f)
    def error(self, msg, **f): self.log("ERROR", msg, **f)
```

My tie-in: structured JSON logs with a `request_id` field is what made ELK triage 70% faster at Masters.

---

## 7. In-memory pub-sub / message broker

**Requirements:** topics, publish, subscribe with a callback or pull; each subscriber gets every message (fan-out); consumer offsets (replay); bounded memory.

```python
import threading
from collections import defaultdict

class Topic:
    def __init__(self, retention=100_000):
        self.log, self.retention = [], retention
        self.base = 0                    # offset of log[0]
        self.cond = threading.Condition()

    def publish(self, msg):
        with self.cond:
            self.log.append(msg)
            if len(self.log) > self.retention:
                drop = len(self.log) - self.retention
                del self.log[:drop]
                self.base += drop
            self.cond.notify_all()

    def read(self, offset, max_n=100, timeout=1.0):
        with self.cond:
            if offset >= self.base + len(self.log):
                self.cond.wait(timeout)
            start = max(offset, self.base) - self.base
            batch = self.log[start:start + max_n]
            return batch, self.base + start + len(batch)

class Broker:
    def __init__(self):
        self.topics = defaultdict(Topic)
        self.offsets = defaultdict(int)          # (topic, group) -> offset

    def publish(self, topic, msg):
        self.topics[topic].publish(msg)

    def poll(self, topic, group):
        batch, nxt = self.topics[topic].read(self.offsets[(topic, group)])
        return batch, nxt

    def commit(self, topic, group, offset):     # commit after processing = at-least-once
        self.offsets[(topic, group)] = offset
```

**Talking points:** offsets committed after processing give at-least-once delivery. Retention drops old messages, and a slow group can fall behind retention (detect it and alert). Partitioning for parallelism. Backpressure: bounded logs. It's Kafka in miniature ([SD Q9](04_system_design_questions.md)).

---

## 8. Circuit breaker class (State pattern)

```python
import threading, time

class CircuitOpen(Exception):
    pass

class CircuitBreaker:
    CLOSED, OPEN, HALF_OPEN = "closed", "open", "half_open"

    def __init__(self, failure_threshold=5, cooldown_s=30, clock=time.monotonic):
        self.threshold, self.cooldown, self.clock = failure_threshold, cooldown_s, clock
        self.state, self.failures, self.opened_at = self.CLOSED, 0, 0.0
        self.lock = threading.Lock()

    def call(self, fn, *args, **kwargs):
        with self.lock:
            if self.state == self.OPEN:
                if self.clock() - self.opened_at >= self.cooldown:
                    self.state = self.HALF_OPEN      # allow one trial
                else:
                    raise CircuitOpen()
            elif self.state == self.HALF_OPEN:
                raise CircuitOpen()                  # trial already in flight
        try:
            result = fn(*args, **kwargs)
        except Exception:
            with self.lock:
                self.failures += 1
                if self.state == self.HALF_OPEN or self.failures >= self.threshold:
                    self.state, self.opened_at = self.OPEN, self.clock()
            raise
        with self.lock:
            self.state, self.failures = self.CLOSED, 0
        return result
```

Fallback belongs to the caller: `try: breaker.call(llm) except (CircuitOpen, TimeoutError): score = deterministic_score(item)`. That's exactly the Keep/Drop registry behavior.

---

## 9. Consistent hashing ring

```python
import bisect, hashlib

class HashRing:
    def __init__(self, vnodes=100):
        self.vnodes = vnodes
        self.ring = []            # sorted hashes
        self.owner = {}           # hash -> node

    @staticmethod
    def _h(s: str) -> int:
        return int(hashlib.md5(s.encode()).hexdigest(), 16)

    def add(self, node):
        for i in range(self.vnodes):
            h = self._h(f"{node}#{i}")
            bisect.insort(self.ring, h)
            self.owner[h] = node

    def remove(self, node):
        for i in range(self.vnodes):
            h = self._h(f"{node}#{i}")
            self.ring.remove(h)
            del self.owner[h]

    def get(self, key):
        if not self.ring:
            return None
        i = bisect.bisect(self.ring, self._h(key)) % len(self.ring)
        return self.owner[self.ring[i]]

    def get_n(self, key, n):                 # replicas: next n distinct nodes clockwise
        out, i = [], bisect.bisect(self.ring, self._h(key))
        while len(out) < n and len(out) < len(set(self.owner.values())):
            node = self.owner[self.ring[i % len(self.ring)]]
            if node not in out:
                out.append(node)
            i += 1
        return out
```

---

## 10. Vending machine (State pattern)

**States:** Idle → HasMoney → Dispensing → Idle, plus an OutOfStock check. Each state class handles `insert_coin`, `select`, `refund`, and `dispense`, and returns the next state. That replaces nested ifs. Inventory is a map of slot → (product, count). Change-making is greedy for canonical coin systems.

```python
class State:
    def insert(self, m, amount): raise RuntimeError("invalid")
    def select(self, m, slot): raise RuntimeError("invalid")
    def refund(self, m): raise RuntimeError("invalid")

class Idle(State):
    def insert(self, m, amount):
        m.balance += amount
        m.state = HasMoney()

class HasMoney(State):
    def insert(self, m, amount):
        m.balance += amount
    def select(self, m, slot):
        product, price, count = m.inventory[slot]
        if count == 0:
            raise RuntimeError("out of stock")
        if m.balance < price:
            raise RuntimeError("insufficient funds")
        m.inventory[slot] = (product, price, count - 1)
        change, m.balance = m.balance - price, 0
        m.state = Idle()
        return product, change
    def refund(self, m):
        amount, m.balance = m.balance, 0
        m.state = Idle()
        return amount

class VendingMachine:
    def __init__(self, inventory):
        self.inventory, self.balance, self.state = inventory, 0, Idle()
    def insert(self, amount): return self.state.insert(self, amount)
    def select(self, slot): return self.state.select(self, slot)
    def refund(self): return self.state.refund(self)
```

---

## 11. Elevator system

**Requirements:** N elevators, M floors, hall calls (up/down) and car calls (floor buttons), minimize wait time, and concurrency (requests arrive anytime).

**Entities:** `Elevator` (current floor, direction, stop set, state: IDLE/MOVING_UP/MOVING_DOWN/DOORS_OPEN/MAINTENANCE), `Request` (floor, direction), `Dispatcher` with a pluggable `SchedulingStrategy`, and a `Controller` loop per elevator.

**Scheduling:**
- **SCAN / LOOK** per elevator: keep moving in the current direction serving stops (two heaps: up-stops as a min-heap, down-stops as a max-heap), and reverse when none remain.
- **Dispatch** a hall call to the elevator with the lowest cost: an idle elevator's distance; the distance if moving toward the call in the same direction; otherwise the distance to the turnaround plus back.

**Concurrency:** a request queue (thread-safe) feeds the dispatcher; each elevator runs in its own thread/goroutine with a lock on its stop set. In Go: a channel per elevator for assigned requests and a `select` loop with a ticker for movement.

---

## 12. Movie ticket booking (BookMyShow): the concurrency part

**Hard part:** two users selecting the same seat.

- **Temporary hold:** `hold(show_id, seats, user)` sets the seat status to HELD with `hold_expires_at = now + 10 min`, atomically:
  - DB: `UPDATE seats SET status='HELD', user=?, expires=? WHERE show_id=? AND seat_id IN (...) AND (status='FREE' OR expires < now)`, and check that the affected row count equals the seat count, otherwise roll back.
  - Or optimistic versions per seat, or Redis `SET seat:{show}:{id} user NX PX 600000` per seat (then all-or-nothing with a Lua script).
- **Confirm** after payment: HELD by this user and not expired → BOOKED. Payment uses an idempotency key.
- **Expiry:** lazy (the condition in the UPDATE) plus a sweeper.
- **Entities:** Movie, Theater, Screen, Show, Seat, Booking, Payment. Pricing strategy per seat class.

This is the same **optimistic row locking** idea I used at Uber FRM so concurrent reviewers never overwrite each other.

---

## 13. Splitwise (expense sharing)

- Entities: User, Group, Expense (payer, amount, split strategy: EQUAL, EXACT, PERCENT), and a Balance sheet `balances[a][b]`.
- The split strategy is a **Strategy** that validates the sums (percentages add to 100).
- **Simplify debts:** compute each user's net balance. Then greedily match the largest creditor with the largest debtor (two heaps). That gives at most n-1 transactions. (The true minimum is NP-hard in general, so say greedy.)
- Use integer cents, never floats, for money. Distribute rounding remainders deterministically.

---

## 14. In-memory file system

- A `Node` base with `Directory` (children map) and `File` (content) (**Composite**).
- `mkdir -p`, `ls` (sorted), `addContentToFile`, `readContentFromFile`: path parsing by `/`, walking from the root.
- Extensions: permissions, size (composite `size()`), search by name (DFS), and a trie-shaped path index.

---

## 15. Task scheduler / delayed job executor (LLD version)

**Requirements:** `schedule(task, delay)`, `schedule_at_fixed_rate(task, period)`, cancel, and a worker pool.

**Design:** a min-heap of `(run_at, seq, task)` guarded by a `Condition`. A scheduler thread waits until the earliest `run_at` (`cond.wait(timeout=run_at - now)`), wakes early when a sooner task is added, and hands due tasks to a worker pool (a `ThreadPoolExecutor`). Recurring tasks re-push themselves. Cancel by marking a flag (lazy deletion).

```python
import heapq, itertools, threading, time
from concurrent.futures import ThreadPoolExecutor

class Scheduler:
    def __init__(self, workers=4):
        self.heap, self.seq = [], itertools.count()
        self.cond = threading.Condition()
        self.pool = ThreadPoolExecutor(workers)
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def schedule(self, fn, delay, period=None):
        job = {"fn": fn, "period": period, "cancelled": False}
        with self.cond:
            heapq.heappush(self.heap, (time.monotonic() + delay, next(self.seq), job))
            self.cond.notify()
        return job

    def cancel(self, job):
        job["cancelled"] = True

    def _loop(self):
        while self.running:
            with self.cond:
                while not self.heap:
                    self.cond.wait()
                run_at, _, job = self.heap[0]
                now = time.monotonic()
                if run_at > now:
                    self.cond.wait(run_at - now)     # may wake early on a new job
                    continue
                heapq.heappop(self.heap)
                if job["period"] and not job["cancelled"]:
                    heapq.heappush(self.heap, (run_at + job["period"], next(self.seq), job))
            if not job["cancelled"]:
                self.pool.submit(job["fn"])
```

---

## LLD answer checklist (say it at the end)

1. Which parts vary, and which interface hides them.
2. Which objects are shared across threads, and how they're protected.
3. How it fails (invalid input, full capacity, timeouts) and what the caller sees.
4. How I'd test it (fakes via DI, a concurrency stress test, property tests).
5. How it would become distributed (sharding, persistence, replication), which connects to system design.
