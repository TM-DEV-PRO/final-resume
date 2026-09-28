# 06. Multithreading and concurrency in depth (Python + Go)

---

## 1. Core concepts

- **Concurrency:** dealing with many things at once (structure). **Parallelism:** doing many things at the same instant (execution on multiple cores). Concurrency is possible on one core.
- **CPU-bound vs IO-bound:** IO-bound work (network, disk) benefits from concurrency even on one core. CPU-bound work needs parallelism (multiple cores, and in Python, multiple processes).
- **Process:** its own memory space; heavy; isolation; IPC needed. **Thread:** shares the process's memory; OS-scheduled; ~1 MB stack. **Goroutine:** a user-space thread managed by the Go runtime; starts at ~2 KB of stack; millions possible. **Coroutine (asyncio):** cooperative; yields at `await`; one thread.
- **Context switch:** saving and restoring registers and the stack. OS thread switches cost ~µs; goroutine and coroutine switches are much cheaper.
- **Preemptive vs cooperative scheduling:** OS threads and goroutines (since Go 1.14, async preemption) are preempted. Asyncio coroutines are not, so one blocking call freezes everything.

---

## 2. What goes wrong

### Race condition
The result depends on timing. The classic is **read-modify-write**: `count += 1` is load, add, store. Two threads interleave and one increment is lost.

**Check-then-act** is the other classic: `if key not in cache: cache[key] = compute()`. Two threads both see a miss and both compute (a cache stampede; fix with singleflight).

### Data race (Go term)
Two goroutines access the same memory concurrently, at least one writes, and there's no synchronization. It's undefined behavior in Go's memory model. Detect with `go test -race`.

### Visibility and ordering (memory model)
CPUs and compilers reorder instructions and cache values. Without synchronization, one thread may **never see** another's write, or see writes out of order. Synchronization primitives (mutex unlock/lock, channel send/receive, atomics) create **happens-before** edges.
- Go: a send on a channel happens before the corresponding receive completes. An unlock happens before the next lock.
- Java: `volatile` and `synchronized`. Python: the GIL makes most single bytecode operations appear atomic, but compound operations aren't.

### Deadlock
Four **Coffman conditions**, all required:
1. Mutual exclusion.
2. Hold and wait.
3. No preemption.
4. Circular wait.

Break any one:
- **Lock ordering** (always acquire locks in a global order, e.g. by account ID) breaks circular wait. This is the most common fix.
- **Try-lock with timeout** and back off.
- Acquire all locks at once.
- Avoid holding locks while calling unknown code or doing IO.

```python
def transfer(a, b, amount):
    first, second = (a, b) if a.id < b.id else (b, a)    # global lock order
    with first.lock, second.lock:
        a.balance -= amount
        b.balance += amount
```

### Livelock
Threads keep responding to each other and make no progress (two people stepping aside in a corridor). Fix: randomized backoff.

### Starvation
A thread never gets the resource (writers starved by a stream of readers). Fix: fair locks, writer preference, aging.

### Priority inversion
A low-priority thread holds a lock needed by a high-priority one while a medium one runs. Fix: priority inheritance.

### Thundering herd
Many waiters are woken for one resource. Fix: `notify()` instead of `notify_all()` where correct; in distributed locks, watch only your predecessor.

---

## 3. Synchronization primitives

| Primitive | What it does | Use for |
|---|---|---|
| **Mutex / Lock** | One holder at a time | Protect shared state |
| **Reentrant lock (RLock)** | The same thread can re-acquire | Recursive code paths |
| **Read-write lock** | Many readers OR one writer | Read-heavy data (config, routing tables) |
| **Semaphore(n)** | n permits | Bound concurrency (connection pools, max parallel calls) |
| **Condition variable** | Wait until a predicate is true; signal | Bounded queues, producer/consumer |
| **Barrier** | N threads wait until all arrive | Phased computation |
| **Latch / WaitGroup** | Wait for N events | Wait for workers to finish |
| **Atomic / CAS** | Lock-free single-word update | Counters, flags, lock-free structures |
| **Spinlock** | Busy-wait | Very short sections in kernels; rarely in app code |
| **Future / Promise** | A placeholder for a result | Async results |
| **Channel** | Typed pipe with synchronization | Go communication |

### Condition variable rule
**Always wait in a `while` loop**, not an `if`. There are spurious wakeups, and another thread may take the item first.

```python
with cond:
    while not predicate():
        cond.wait()
    # predicate true and lock held
```

### Compare-and-swap (CAS)
`CAS(addr, expected, new)`: atomically set it to `new` if it currently equals `expected`. Lock-free algorithms loop on CAS. The **ABA problem**: the value changes A → B → A and CAS succeeds wrongly. Fix: version tags. The same idea is **optimistic concurrency** in databases (a version column), which I used at Uber FRM.

```go
func incrementMax(addr *int64, v int64) {
    for {
        old := atomic.LoadInt64(addr)
        if v <= old || atomic.CompareAndSwapInt64(addr, old, v) {
            return
        }
    }
}
```

---

## 4. Python concurrency

### The GIL
- CPython's **Global Interpreter Lock** lets only one thread execute Python bytecode at a time.
- So **threads don't speed up CPU-bound Python**. They do help IO-bound work, because the GIL is released during blocking IO and in many C extensions (NumPy, hashlib, compression).
- The GIL does **not** make your code thread-safe. `x += 1` is several bytecodes and can interleave. Compound operations on dicts/lists need locks.
- Python 3.13+ has an experimental **free-threaded** build (PEP 703) without the GIL. Mention it as awareness.

### Choosing the tool
| Workload | Tool |
|---|---|
| Many network calls | `asyncio` (best), or threads |
| Blocking library (no async version) | `ThreadPoolExecutor`, or `asyncio.to_thread` |
| CPU-heavy pure Python | `multiprocessing` / `ProcessPoolExecutor` |
| CPU-heavy in NumPy / C | Threads can work (the GIL is released) |
| Distributed tasks | Celery workers (I used this at Masters), a queue |

### threading and concurrent.futures

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_all(urls, max_workers=16):
    results = {}
    with ThreadPoolExecutor(max_workers) as ex:
        futs = {ex.submit(fetch, u): u for u in urls}
        for f in as_completed(futs):
            u = futs[f]
            try:
                results[u] = f.result()
            except Exception as e:
                results[u] = e
    return results
```

### asyncio in depth
- One thread and an **event loop**. `async def` defines a coroutine; `await` yields control until the awaited thing is ready.
- `asyncio.create_task` schedules concurrently. `asyncio.gather` waits for many. `asyncio.TaskGroup` (3.11+) gives structured concurrency: if one fails, the others are cancelled.
- **Timeouts:** `asyncio.timeout(5)` (3.11+) or `asyncio.wait_for`.
- **Bounded concurrency:** `asyncio.Semaphore(n)`.
- **Cancellation:** raises `CancelledError` inside the task at the next await. Clean up in `finally`. Don't swallow it.
- **Never block the loop:** `time.sleep`, sync DB drivers, CPU loops, and `requests.get` freeze every request. Use `await asyncio.sleep`, async drivers, or `await asyncio.to_thread(fn)`.
- **Resource lifetime:** always `async with` for clients, sessions, and cursors. My packet story: a FastAPI worker leaked DB/HTTP clients created inside a long-lived async loop without context managers, so memory climbed and 504s followed. Fixed with `async with`, pool limits/timeouts, and backpressure.

```python
import asyncio

async def fetch_with_limits(session, urls, concurrency=20, timeout_s=5):
    sem = asyncio.Semaphore(concurrency)

    async def one(url):
        async with sem:
            async with asyncio.timeout(timeout_s):
                async with session.get(url) as r:
                    return await r.text()

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(one(u)) for u in urls]
    return [t.result() for t in tasks]
```

Retry with backoff and jitter in async:

```python
async def call_with_retry(fn, attempts=3, base=0.1, cap=2.0):
    for i in range(attempts):
        try:
            return await fn()
        except (asyncio.TimeoutError, ConnectionError):
            if i == attempts - 1:
                raise
            await asyncio.sleep(random.uniform(0, min(cap, base * 2 ** i)))
```

An async producer/consumer with a bounded `asyncio.Queue` (backpressure built in):

```python
async def pipeline(items, workers=8):
    q = asyncio.Queue(maxsize=100)

    async def producer():
        for it in items:
            await q.put(it)            # blocks when full = backpressure
        for _ in range(workers):
            await q.put(None)          # poison pills

    async def worker():
        while (it := await q.get()) is not None:
            await process(it)

    await asyncio.gather(producer(), *(worker() for _ in range(workers)))
```

**FastAPI note:** `async def` endpoints run on the event loop, so they must not block. Plain `def` endpoints run in a threadpool. That's why IRP calls at Masters moved to async IO plus Celery workers.

### multiprocessing
- Separate interpreters, so no GIL contention. Data is pickled between processes (overhead).
- Use `ProcessPoolExecutor` for CPU work. Shared memory via `multiprocessing.shared_memory` or `Manager` (slow).
- The start method matters (`fork` vs `spawn`): don't fork after starting threads.

---

## 5. Go concurrency in depth

### The scheduler (GMP)
- **G** = goroutine, **M** = OS thread, **P** = processor (a logical CPU context, `GOMAXPROCS` of them).
- Each P has a local run queue of Gs, with **work stealing** between Ps.
- On a blocking syscall, the M is detached and the P gets another M. Network IO uses the **netpoller** (epoll/kqueue), so goroutines waiting on sockets don't hold threads.
- That's why a Go server can hold 100k+ connections with cheap goroutines per connection.

### Channels
- **Unbuffered:** send blocks until a receiver takes it (synchronous handoff).
- **Buffered(n):** send blocks only when full. That gives bounded queues and semaphores.
- `close(ch)` signals no more values. Receivers get the zero value with `ok == false`. `for v := range ch` stops at close. **Only the sender closes.** Closing twice or sending on a closed channel panics.
- A **nil channel** blocks forever. That's useful in `select` to disable a case.
- "Don't communicate by sharing memory; share memory by communicating." But a mutex is fine and often simpler for protecting a map.

### select

```go
select {
case msg := <-in:
    handle(msg)
case <-ctx.Done():
    return ctx.Err()
case <-time.After(2 * time.Second):
    return errTimeout
}
```

### context
- Carries **cancellation, deadlines, and request-scoped values** down the call tree.
- `context.WithTimeout(parent, d)`: children inherit the *earlier* deadline. That's how nested timeouts work on my Go/Gin edge. The edge sets the budget and every DB/HTTP call beneath gets the remaining time.
- Always `defer cancel()`. Pass `ctx` as the first parameter. Check `ctx.Err()` in long loops.

### sync package
| Type | Notes |
|---|---|
| `sync.Mutex` | Don't copy after first use (pass pointers). Not reentrant |
| `sync.RWMutex` | `RLock` for readers. Writers get priority once waiting |
| `sync.WaitGroup` | `Add` before starting the goroutine, `Done` in a defer, `Wait` |
| `sync.Once` | Lazy init, thread-safe |
| `sync.Cond` | Rarely needed; channels usually replace it |
| `sync.Pool` | Reuse temporary objects (buffers) to cut GC. Items may be dropped at any GC |
| `sync.Map` | For write-once/read-many or disjoint key sets. Otherwise a map + mutex is better |
| `sync/atomic` | `atomic.Int64`, `atomic.Bool`, `atomic.Pointer[T]` (Go 1.19+) |
| `golang.org/x/sync/errgroup` | Run goroutines, return the first error, cancel the others via ctx. `SetLimit(n)` bounds concurrency |
| `golang.org/x/sync/singleflight` | Coalesce duplicate concurrent calls for the same key (stampede protection) |
| `golang.org/x/sync/semaphore` | Weighted semaphore |

### Worker pool (bounded parallelism)

```go
func WorkerPool(ctx context.Context, jobs []Job, workers int) ([]Result, error) {
    in := make(chan Job)
    out := make(chan Result, len(jobs))
    g, ctx := errgroup.WithContext(ctx)

    for i := 0; i < workers; i++ {
        g.Go(func() error {
            for j := range in {
                r, err := process(ctx, j)
                if err != nil {
                    return err            // cancels ctx for everyone
                }
                out <- r
            }
            return nil
        })
    }

    g.Go(func() error {
        defer close(in)
        for _, j := range jobs {
            select {
            case in <- j:
            case <-ctx.Done():
                return ctx.Err()
            }
        }
        return nil
    })

    err := g.Wait()
    close(out)
    var results []Result
    for r := range out {
        results = append(results, r)
    }
    return results, err
}
```

### Pipeline and fan-out / fan-in

```go
func gen(ctx context.Context, nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

func square(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case out <- n * n:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

func merge(ctx context.Context, cs ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)
    wg.Add(len(cs))
    for _, c := range cs {
        go func(c <-chan int) {
            defer wg.Done()
            for v := range c {
                select {
                case out <- v:
                case <-ctx.Done():
                    return
                }
            }
        }(c)
    }
    go func() { wg.Wait(); close(out) }()
    return out
}
```

### Double buffering: the pattern behind my Go pump (~344k rows/s)
Read batch N+1 while batch N is being sent. Two buffers alternate through channels, so the SELECT stream never sits idle. That was the fix for HTTP `unexpected EOF`.

```go
func pump(ctx context.Context, src Reader, dst Writer, batchSize int) error {
    free := make(chan *Batch, 2)
    full := make(chan *Batch, 2)
    free <- NewBatch(batchSize)
    free <- NewBatch(batchSize)

    g, ctx := errgroup.WithContext(ctx)

    g.Go(func() error {                       // reader
        defer close(full)
        for {
            var b *Batch
            select {
            case b = <-free:
            case <-ctx.Done():
                return ctx.Err()
            }
            b.Reset()
            n, err := src.Fill(ctx, b)        // columnar append, no per-row reflection
            if n > 0 {
                full <- b
            }
            if err == io.EOF {
                return nil
            }
            if err != nil {
                return err
            }
        }
    })

    g.Go(func() error {                       // writer
        for b := range full {
            if err := dst.Send(ctx, b); err != nil {
                return err                    // never retry a spent batch; the unit is restarted
            }
            free <- b
        }
        return nil
    })

    return g.Wait()
}
```

### Rate limiting in Go
`golang.org/x/time/rate`: `limiter := rate.NewLimiter(rate.Limit(100), 200)`, then `limiter.Wait(ctx)` or `limiter.Allow()`. Or a `time.Ticker` for simple pacing.

### Goroutine leaks (very common interview topic)
A goroutine is blocked forever on a channel nobody will read or write.
- Cause: returning early from the consumer while the producer is still sending on an unbuffered channel.
- Fix: every goroutine must have an exit path, via `ctx.Done()`, closing the input, or a buffered result channel of the right size.
- Detect with `runtime.NumGoroutine()` in tests, `pprof` goroutine profiles, or `go.uber.org/goleak`.

### Common Go concurrency bugs
- Loop variable capture (fixed in Go 1.22: each iteration has its own variable. Before that, pass it as a parameter).
- Concurrent map writes (a runtime fatal error): use a mutex.
- `wg.Add` inside the goroutine (races with `Wait`).
- Copying a struct that contains a mutex.
- Forgetting `cancel()` (leaks timers/contexts).
- Holding a mutex while sending on a channel (deadlock risk).

---

## 6. Classic concurrency problems with code

### 6.1 Bounded blocking queue (the most asked)

**Python (Condition variables):**

```python
import threading
from collections import deque

class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.q = deque()
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def put(self, item, timeout=None):
        with self.not_full:
            while len(self.q) >= self.cap:
                if not self.not_full.wait(timeout):
                    raise TimeoutError
            self.q.append(item)
            self.not_empty.notify()

    def take(self, timeout=None):
        with self.not_empty:
            while not self.q:
                if not self.not_empty.wait(timeout):
                    raise TimeoutError
            item = self.q.popleft()
            self.not_full.notify()
            return item

    def size(self):
        with self.lock:
            return len(self.q)
```

Why two conditions on one lock: producers wait on `not_full` and consumers on `not_empty`, so `notify()` wakes the right kind of thread.

**Go:** a buffered channel *is* a bounded blocking queue. If asked to build it with a mutex:

```go
type BQueue[T any] struct {
    mu       sync.Mutex
    notEmpty *sync.Cond
    notFull  *sync.Cond
    items    []T
    cap      int
}

func NewBQueue[T any](cap int) *BQueue[T] {
    q := &BQueue[T]{cap: cap}
    q.notEmpty = sync.NewCond(&q.mu)
    q.notFull = sync.NewCond(&q.mu)
    return q
}

func (q *BQueue[T]) Put(v T) {
    q.mu.Lock()
    defer q.mu.Unlock()
    for len(q.items) == q.cap {
        q.notFull.Wait()
    }
    q.items = append(q.items, v)
    q.notEmpty.Signal()
}

func (q *BQueue[T]) Take() T {
    q.mu.Lock()
    defer q.mu.Unlock()
    for len(q.items) == 0 {
        q.notEmpty.Wait()
    }
    v := q.items[0]
    q.items = q.items[1:]
    q.notFull.Signal()
    return v
}
```

### 6.2 Print in order (first, second, third across threads)

```python
class Foo:
    def __init__(self):
        self.e1, self.e2 = threading.Event(), threading.Event()
    def first(self, f):
        f(); self.e1.set()
    def second(self, f):
        self.e1.wait(); f(); self.e2.set()
    def third(self, f):
        self.e2.wait(); f()
```
Go: two unbuffered channels, or a `sync.WaitGroup` per stage.

### 6.3 Print FooBar alternately (n times)

```python
class FooBar:
    def __init__(self, n):
        self.n = n
        self.foo_sem, self.bar_sem = threading.Semaphore(1), threading.Semaphore(0)
    def foo(self, p):
        for _ in range(self.n):
            self.foo_sem.acquire(); p(); self.bar_sem.release()
    def bar(self, p):
        for _ in range(self.n):
            self.bar_sem.acquire(); p(); self.foo_sem.release()
```

Go ping-pong:

```go
func fooBar(n int) {
    foo, bar := make(chan struct{}), make(chan struct{})
    done := make(chan struct{})
    go func() {
        for i := 0; i < n; i++ {
            <-foo
            fmt.Print("foo")
            bar <- struct{}{}
        }
    }()
    go func() {
        for i := 0; i < n; i++ {
            <-bar
            fmt.Print("bar")
            if i < n-1 {
                foo <- struct{}{}
            }
        }
        close(done)
    }()
    foo <- struct{}{}
    <-done
}
```

### 6.4 Zero Even Odd, FizzBuzz Multithreaded, Building H2O
The same technique: semaphores gating whose turn it is.
- **H2O:** `h_sem = Semaphore(2)`, `o_sem = Semaphore(1)`, and a `Barrier(3)` so each molecule forms together, then release the permits.

```python
class H2O:
    def __init__(self):
        self.h, self.o = threading.Semaphore(2), threading.Semaphore(1)
        self.barrier = threading.Barrier(3)
    def hydrogen(self, release):
        with self.h:
            self.barrier.wait()
            release()
    def oxygen(self, release):
        with self.o:
            self.barrier.wait()
            release()
```

### 6.5 Dining philosophers
Five philosophers, five forks. Everyone picking up the left fork first leads to deadlock (circular wait). Fixes:
1. **Resource ordering:** always pick up the lower-numbered fork first.
2. **Waiter/arbitrator:** a semaphore allowing at most 4 to try.
3. Try-lock and back off (risks livelock without randomness).

```python
def philosopher(i, forks, meals):
    left, right = i, (i + 1) % len(forks)
    first, second = min(left, right), max(left, right)
    for _ in range(meals):
        with forks[first], forks[second]:
            eat(i)
```

### 6.6 Implement a read-write lock (writer preference)

```python
class RWLock:
    def __init__(self):
        self.lock = threading.Lock()
        self.readers_ok = threading.Condition(self.lock)
        self.writers_ok = threading.Condition(self.lock)
        self.readers = 0
        self.writer = False
        self.waiting_writers = 0

    def acquire_read(self):
        with self.lock:
            while self.writer or self.waiting_writers:
                self.readers_ok.wait()
            self.readers += 1

    def release_read(self):
        with self.lock:
            self.readers -= 1
            if self.readers == 0:
                self.writers_ok.notify()

    def acquire_write(self):
        with self.lock:
            self.waiting_writers += 1
            while self.writer or self.readers:
                self.writers_ok.wait()
            self.waiting_writers -= 1
            self.writer = True

    def release_write(self):
        with self.lock:
            self.writer = False
            if self.waiting_writers:
                self.writers_ok.notify()
            else:
                self.readers_ok.notify_all()
```

### 6.7 Thread-safe singleton / lazy init
Python: a module-level instance, or double-checked locking:

```python
class Config:
    _instance, _lock = None, threading.Lock()
    @classmethod
    def get(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
```
Go: `sync.Once` (see [LLD foundations](05_lld_foundations.md)).

### 6.8 Concurrent web crawler (LeetCode 1242, a Go favorite)
Requirements: start URL, crawl the same hostname only, visit each once, in parallel.

```go
func Crawl(ctx context.Context, start string, fetch func(context.Context, string) []string, workers int) []string {
    host := hostname(start)
    var (
        mu   sync.Mutex
        seen = map[string]bool{start: true}
        wg   sync.WaitGroup
        sem  = make(chan struct{}, workers)   // bound parallel fetches
    )
    var visit func(u string)
    visit = func(u string) {
        defer wg.Done()
        sem <- struct{}{}
        links := fetch(ctx, u)
        <-sem
        for _, l := range links {
            if hostname(l) != host {
                continue
            }
            mu.Lock()
            if !seen[l] {
                seen[l] = true
                wg.Add(1)
                go visit(l)
            }
            mu.Unlock()
        }
    }
    wg.Add(1)
    go visit(start)
    wg.Wait()

    out := make([]string, 0, len(seen))
    for u := range seen {
        out = append(out, u)
    }
    return out
}
```
Points: check-and-mark `seen` under one lock (avoid check-then-act races), `wg.Add` before `go`, and a semaphore bounds parallelism. The semaphore is released before spawning children, so there's no deadlock.

### 6.9 Thread-safe counter / hit counter at high QPS
- A mutex works. An atomic counter is faster.
- At very high contention: **striped counters** (N slots, each thread picks one, and the sum is taken on read), like Java's `LongAdder`.
- Hit counter over 5 minutes: 300 buckets of `(second, count)` with atomic updates.

### 6.10 Connection pool
A bounded set of connections. `acquire(timeout)` takes an idle one or creates one if under max, otherwise waits (semaphore + queue). `release` returns it (check health first). Close idle ones after a TTL. Always use `with pool.connection() as c:` so leaks are impossible. (The leak story: resources must have a lifetime owner.)

### 6.11 Singleflight (stampede protection)

```python
class SingleFlight:
    def __init__(self):
        self.lock = threading.Lock()
        self.calls = {}                    # key -> (event, result holder)

    def do(self, key, fn):
        with self.lock:
            if key in self.calls:
                ev, holder = self.calls[key]
                leader = False
            else:
                ev, holder = threading.Event(), {}
                self.calls[key] = (ev, holder)
                leader = True
        if leader:
            try:
                holder["val"] = fn()
            except Exception as e:
                holder["err"] = e
            finally:
                with self.lock:
                    del self.calls[key]
                ev.set()
        else:
            ev.wait()
        if "err" in holder:
            raise holder["err"]
        return holder["val"]
```

### 6.12 CountDownLatch / barrier / cyclic barrier
Python: `threading.Barrier(n)`. A latch is a Condition + counter, or in Go a `WaitGroup`.

---

## 7. Concurrency across machines (connect to system design)

| Local concept | Distributed equivalent |
|---|---|
| Mutex | Distributed lock (etcd lease + **fencing token**) |
| CAS | Conditional write (`UPDATE ... WHERE version = ?`, conditional PUT with ETag) |
| Atomic counter | Redis `INCR`, a sharded counter |
| Bounded queue | Queue with max depth + backpressure / 429 |
| Idempotent retry | Idempotency keys (Masters: `client + fileHash + batchIndex`) |
| Deadlock avoidance | Lock ordering; timeouts; avoid distributed locks by partitioning ownership |
| Double-checked locking | Singleflight / request coalescing at the cache |
| Worker pool | Consumer group; autoscaled workers on queue depth |

### From my work
- **Copier:** caps per process (threads, memory), a flock per table so two terminals can't copy the same table, and `-workers N` seasons in parallel with separate connections per worker.
- **Keep/Drop:** bounded parallel LLM batches, hard per-batch timeouts, and a circuit breaker shared across workers.
- **Uber FRM:** optimistic row locking between concurrent reviewers.
- **Masters:** bounded concurrency against the IRP with backoff and jitter; Celery workers autoscaled on queue depth.
- **ClickHouse builds:** "never raise season parallelism and week parallelism together on the same box." That's a concurrency budget.

---

## 8. Rapid-fire Q&A

| Question | Answer |
|---|---|
| Thread vs process? | Threads share memory (fast communication, need synchronization). Processes are isolated (safer, IPC cost). |
| Why not threads for CPU-bound Python? | The GIL; use processes. |
| Is `dict[k] = v` thread-safe in Python? | A single assignment is atomic under the GIL. Check-then-set is not. Use a lock for invariants. |
| Goroutine vs thread? | User-space, 2 KB growable stacks, multiplexed on OS threads by the runtime (GMP), cheap to create and switch. |
| Buffered vs unbuffered channel? | Unbuffered = synchronous handoff; buffered = queue up to n. |
| How do you stop a goroutine? | Cancel its context, or close its input channel. You can't kill it from outside. |
| How do you find races? | `go test -race`; in Python, stress tests + code review. Keep shared state minimal. |
| Mutex vs channel in Go? | Mutex for protecting state (a map, a counter). Channels for passing ownership or signaling, and for pipelines. |
| What is a memory barrier? | It prevents reordering across it; synchronization primitives include them. |
| Optimistic vs pessimistic locking? | Optimistic: no lock, check the version at commit, retry on conflict (low contention). Pessimistic: lock first (high contention). |
| How do you size a thread pool? | CPU-bound: ≈ number of cores. IO-bound: cores × (1 + wait time / compute time). Then measure. |
| What's backpressure? | Slowing producers when consumers can't keep up (bounded queues, blocking puts, 429s) instead of buffering without limit. |
| async vs threads in Python for 10k connections? | asyncio: cheaper per connection, no thread stacks. |
| What causes asyncio latency spikes? | Blocking calls on the loop, CPU work, or huge JSON parsing. Offload with `to_thread` or processes. |
