# 05. Low-level design foundations: zero to hero

Problems with full designs: [05 LLD problems](05_lld_problems.md). Concurrency primitives: [06 concurrency](06_concurrency.md).

---

## Level 0. What an LLD round is

You get a vague prompt ("design a parking lot", "design an LRU cache", "design a rate limiter library") and 45 minutes. They grade:
1. **Requirements:** you clarify and scope.
2. **Modeling:** the right classes and responsibilities, and clean relationships.
3. **Extensibility:** adding a new vehicle type, pricing rule, or eviction policy doesn't need edits everywhere (open/closed).
4. **Code quality:** working, readable code for the core parts.
5. **Concurrency** (common at OCI): what if two threads call this at once?
6. **Testing:** how would you test it?

### Step-by-step approach
1. **Clarify (5 min):** actors, core use cases, what's out of scope. Write 4–6 requirements down.
2. **Identify entities (5 min):** nouns become classes, verbs become methods. Find what **varies** (it becomes an interface/strategy).
3. **Relationships (5 min):** has-a (composition), is-a (inheritance, used sparingly), uses (dependency).
4. **Class diagram / interfaces (5 min):** method signatures before bodies.
5. **Code the core (20 min):** the main flow end to end, then the most interesting class in detail.
6. **Concurrency and edge cases (5 min).**
7. **Extensions (rest):** "to add X, I'd add a new Strategy class; nothing else changes."

---

## Level 1. OOP fundamentals

| Pillar | Meaning | Example |
|---|---|---|
| **Encapsulation** | Hide state behind methods; enforce invariants | `Account.withdraw()` checks the balance; the balance isn't public |
| **Abstraction** | Expose what, hide how | `Storage.put(key, value)` without saying whether it's disk or S3 |
| **Inheritance** | Reuse via is-a | `Car(Vehicle)`. Use it sparingly |
| **Polymorphism** | Same call, different behavior | `pricing.calculate(ticket)` for hourly vs flat |

**Composition over inheritance:** "has-a" beats "is-a" for flexibility. A `Car` *has* an `Engine`; you swap engines without new subclasses. Inheritance hierarchies get rigid (the "fragile base class" problem).

**Go has no inheritance.** It uses **interfaces** (implicit: a type implements an interface by having the methods) and **struct embedding** (composition). That forces good design. Say so if you code LLD in Go.

```go
type Notifier interface {
    Notify(ctx context.Context, userID string, msg string) error
}

type EmailNotifier struct{ client *smtp.Client }
func (e *EmailNotifier) Notify(ctx context.Context, userID, msg string) error { /* ... */ return nil }

type SMSNotifier struct{ gateway string }
func (s *SMSNotifier) Notify(ctx context.Context, userID, msg string) error { /* ... */ return nil }
```

In Python, use `abc.ABC` + `@abstractmethod`, or `typing.Protocol` for structural typing (like Go).

```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def notify(self, user_id: str, msg: str) -> None: ...

class EmailNotifier(Notifier):
    def notify(self, user_id, msg):
        ...
```

---

## Level 2. SOLID (with a violation and a fix for each)

### S: Single Responsibility
A class has one reason to change.
- ✗ `Invoice` computes totals, saves to the DB, and sends email.
- ✓ `Invoice` (data + totals), `InvoiceRepository` (persistence), `InvoiceNotifier` (email).
- My example: at Masters I set **router / service / repository** layering for every new FastAPI service. Routers handle HTTP, services hold business rules, and repositories handle SQL.

### O: Open/Closed
Open for extension, closed for modification.
- ✗ `if vehicle_type == "car": ... elif "truck": ...` spread across the code.
- ✓ A `PricingStrategy` interface; add `EVPricing` without touching the existing code.
- My example: the **KPI configurator**. New KPIs are data (formulas), not code changes.

### L: Liskov Substitution
Subtypes must be usable wherever the base is expected, without surprises.
- ✗ `Square(Rectangle)` where `set_width` also changes the height, which breaks callers.
- ✗ A `ReadOnlyRepository` subclass that throws on `save()`.
- ✓ Separate interfaces: `Reader` and `Writer`.

### I: Interface Segregation
Many small interfaces beat one fat one.
- ✗ `Worker` with `work()`, `eat()`, `sleep()` forced on robots.
- ✓ Go's `io.Reader`, `io.Writer`, `io.Closer`, composed as `io.ReadWriteCloser`.

### D: Dependency Inversion
Depend on abstractions; inject concrete implementations.
- ✗ `OrderService` creates `MySQLRepository()` inside.
- ✓ `OrderService(repo: OrderRepository)`: pass in MySQL in production and a fake in tests.
- My example: **Google Wire** compile-time DI on the Go platform. Constructors declare dependencies; Wire generates the wiring, so a missing dependency fails the **build**, not a request.

```go
// Dependency inversion with constructor injection (what Wire wires)
type OrderRepo interface {
    Save(ctx context.Context, o Order) error
}

type OrderService struct {
    repo  OrderRepo
    clock func() time.Time
}

func NewOrderService(repo OrderRepo) *OrderService {
    return &OrderService{repo: repo, clock: time.Now}
}
```

### Other principles to name-drop correctly
- **DRY:** one source of truth for each piece of knowledge (not "never repeat two lines").
- **KISS / YAGNI:** don't build extension points nobody asked for. In an interview, *mention* the extension point and build it only if it's cheap.
- **Law of Demeter:** talk to friends, not strangers (`a.b().c().d()` is a smell).
- **Tell, don't ask:** `account.withdraw(x)` instead of `if account.balance > x: account.balance -= x`.
- **Fail fast:** validate at the boundary (Pydantic at the FastAPI edge, in my case).
- **Immutability:** immutable value objects are thread-safe by default.

---

## Level 3. Relationships and UML (just enough)

| Relationship | Meaning | UML | Code |
|---|---|---|---|
| Association | Uses / knows | line | holds a reference |
| Aggregation | Has-a, parts can live alone | hollow diamond | `Team` has `Player`s |
| Composition | Has-a, parts die with the whole | filled diamond | `Order` has `OrderLine`s |
| Inheritance | Is-a | hollow triangle | `class Car(Vehicle)` |
| Realization | Implements | dashed triangle | implements an interface |
| Dependency | Uses temporarily | dashed arrow | parameter |

In interviews, a quick text diagram is enough:

```
ParkingLot 1──* Floor 1──* Spot
Spot <|── CompactSpot, LargeSpot, EVSpot
Ticket ──> Spot, Vehicle
PricingStrategy <|── HourlyPricing, FlatPricing
```

---

## Level 4. Design patterns (the ones that actually come up)

### Creational

**Singleton:** one instance (config, connection pool). In Python a module-level instance is enough. It's thread-safe via import locking. Singletons hide dependencies and hurt tests, so prefer injecting.

```go
var (
    once     sync.Once
    instance *Config
)

func GetConfig() *Config {
    once.Do(func() { instance = loadConfig() })
    return instance
}
```

**Factory method / simple factory:** create objects without the caller knowing the concrete class.

```python
class VehicleFactory:
    _registry = {"car": Car, "bike": Bike, "truck": Truck}

    @classmethod
    def create(cls, kind: str, plate: str):
        try:
            return cls._registry[kind](plate)
        except KeyError:
            raise ValueError(f"unknown vehicle {kind}")
```

**Abstract factory:** families of related objects (`AWSFactory` makes `AWSStorage` + `AWSQueue`; `OCIFactory` makes `OCIStorage` + `OCIQueue`).

**Builder:** step-by-step construction for objects with many optional parameters. In Go, the **functional options** pattern:

```go
type Server struct {
    addr    string
    timeout time.Duration
    maxConn int
}

type Option func(*Server)

func WithTimeout(d time.Duration) Option { return func(s *Server) { s.timeout = d } }
func WithMaxConn(n int) Option          { return func(s *Server) { s.maxConn = n } }

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{addr: addr, timeout: 10 * time.Second, maxConn: 1000}
    for _, o := range opts {
        o(s)
    }
    return s
}
```

**Prototype:** clone an existing configured object.

**Object pool:** reuse expensive objects (DB connections, `sync.Pool` for buffers in Go).

### Structural

**Adapter:** make an incompatible interface fit. Example: wrap a third-party SMS SDK behind your `Notifier` interface.

**Decorator:** add behavior by wrapping, keeping the interface. HTTP middleware is decorators: logging, auth, timeouts, metrics.

```go
type Handler func(ctx context.Context, req Request) (Response, error)

func WithTimeout(d time.Duration, next Handler) Handler {
    return func(ctx context.Context, req Request) (Response, error) {
        ctx, cancel := context.WithTimeout(ctx, d)
        defer cancel()
        return next(ctx, req)
    }
}

func WithLogging(log *slog.Logger, next Handler) Handler {
    return func(ctx context.Context, req Request) (Response, error) {
        start := time.Now()
        resp, err := next(ctx, req)
        log.Info("request", "dur", time.Since(start), "err", err)
        return resp, err
    }
}
```

Python decorator for retries:

```python
import functools, random, time

def retry(attempts=3, base=0.1, cap=2.0, retry_on=(TimeoutError,)):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except retry_on:
                    if i == attempts - 1:
                        raise
                    time.sleep(random.uniform(0, min(cap, base * 2 ** i)))
        return wrapper
    return deco
```

**Proxy:** same interface, controls access (caching proxy, auth proxy, lazy loading, remote proxy / RPC stub).

**Facade:** a simple interface over a complex subsystem (`CheckoutService.place_order()` hides inventory, payment, and shipping).

**Composite:** treat a group like a single item (a file system: `Directory` and `File` both implement `size()`).

**Flyweight:** share immutable state to save memory (glyphs, interned strings).

**Bridge:** separate an abstraction from its implementation so both vary (`Notification` × `Channel`).

### Behavioral

**Strategy:** swap algorithms at runtime. The most useful pattern in LLD interviews: pricing, eviction, rate limiting algorithms, load-balancing algorithms, payment methods.

```python
class EvictionPolicy(ABC):
    @abstractmethod
    def record_access(self, key): ...
    @abstractmethod
    def evict(self): ...
```

**Observer / pub-sub:** subjects notify subscribers of events (order placed → email, analytics, inventory).

**Command:** encapsulate a request as an object (undo/redo, job queues, transaction logs).

**State:** behavior changes with internal state (vending machine, order lifecycle, TCP connection, circuit breaker closed/open/half-open). Replaces big `if state == ...` blocks.

**Chain of responsibility:** a request passes along handlers until one handles it (middleware, approval chains, log levels).

**Template method:** the base class defines the algorithm skeleton; subclasses fill in steps (`DataImporter.run()` = read → validate → transform → write).

**Iterator:** traverse without exposing the internals (Python generators).

**Mediator:** central coordination instead of many-to-many links (air traffic control, a chat room).

**Memento:** snapshot and restore state (undo, checkpoints).

**Visitor:** add operations to a class hierarchy without changing it (AST processing; my KPI formula parser could use a visitor to compile the AST to SQL).

### Where I've used patterns (use these in answers)
| Pattern | Where |
|---|---|
| Strategy | LLM model selection behind one interface; det vs LLM scoring |
| Decorator / middleware | Go Gin middleware for auth, timeouts, tracing |
| State machine | FRM review status (Draft → Review → ReOpen → Closed) with FSM gates; circuit breaker |
| Repository | FastAPI services (Masters, Uber FRM) |
| Factory + DI | Wire providers on the Go platform |
| Command + Memento | Checkpoints and resume in the orchestration registry |
| Interpreter / Visitor | KPI formula tokenizer + parser compiling to SQL |
| Observer | Webhooks and status updates at Masters |
| Chain of responsibility | Auth waterfall: Redis cache → Firebase → JWT/OIDC |

---

## Level 5. Designing for change and failure

- **Identify what varies** and put it behind an interface.
- **Value objects** (Money, Email, TimeRange) with validation in the constructor.
- **Error handling:** domain errors vs infrastructure errors; don't swallow; wrap with context (`fmt.Errorf("save order %s: %w", id, err)` in Go).
- **Idempotency** in methods that can be retried (pass a request ID).
- **Clock and randomness injection** for testability (`clock func() time.Time`).
- **Thread safety:** say which classes are shared and how they're protected (a lock per object, a lock per key, immutable data, or confinement to one goroutine).

---

## Level 6. Testing an LLD

- Unit tests per class with fakes for dependencies (that's why DI matters).
- Table-driven tests in Go.
- Concurrency tests: many goroutines/threads hammering an object, then assert invariants. Run Go with `-race`.
- Property tests: "the cache never exceeds capacity," "total tokens never exceed the bucket size."
- **Test where the code lives** (my lesson from the Uber coverage story: mocks can hide the layer you think you're testing).

---

## Level 7. Clean architecture in services (senior-level talk)

```
handlers (HTTP/gRPC/WebSocket) → services (use cases, business rules) → repositories (DB) / clients (external APIs)
                                   ↑ depend on interfaces, not concrete stores
domain models (pure, no framework imports)
```
- Business rules don't import the web framework or the ORM.
- Adapters at the edges (hexagonal / ports and adapters).
- This is how I structured the FastAPI services at Masters and the Uber FRM scoping service, and the Go platform uses the same shape with Wire providers.
