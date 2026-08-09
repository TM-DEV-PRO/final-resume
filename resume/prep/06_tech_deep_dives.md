# Tech deep-dives — every word on the resume, defensible

For each technology: fundamentals → how it works inside → why we used it → gotchas an interviewer probes. ClickHouse, BigQuery, Postgres, DuckDB, LangGraph/MCP, RAG/text-to-SQL, pgvector already have full treatments in `agentic_assort_playbook/05_tech_deep_dives.md` — this file covers the rest and adds the Go/Rust/streaming stack.

---

## 1. Go (Golang) + Gin

- **Fundamentals.** Compiled, GC'd, statically typed. Concurrency = **goroutines** (runtime-scheduled green threads, ~2KB stacks, M:N onto OS threads) + **channels** (CSP-style typed message passing) + `select`. `net/http` gives goroutine-per-request out of the box — no async/await split, blocking code just scales.
- **Runtime internals worth knowing:** GMP scheduler (G=goroutine, M=OS thread, P=processor/run-queue); work stealing; `GOMAXPROCS`; non-blocking netpoller under blocking syscall API; escape analysis decides stack vs heap; GC is concurrent tri-color mark-sweep with sub-ms pauses (tune with `GOGC`).
- **Gin specifically.** Radix-tree router (fast path params), middleware chain via `c.Next()`, `c.ShouldBindJSON` + validator tags for request validation, `gin.Context` pooled per request (don't retain it past the handler — classic bug).
- **Why we chose it (IA non-agentic tier):** throughput-shaped I/O plumbing; static binary + fast cold start; one obvious way to write things for a many-hands service tier. Gin over chi (batteries), Echo (parity, less team familiarity), fiber (fasthttp breaks `net/http` semantics — rejected).
- **Gotchas they probe:** goroutine leaks (always have cancel paths — `context.Context` everywhere); `sync.Mutex` vs channels ("share memory by communicating, but a mutex is fine for a counter"); nil maps panic on write; slices share backing arrays (append aliasing); error wrapping with `%w` + `errors.Is/As`; no exceptions — errors are values.

## 2. Rust + Axum

- **Fundamentals.** No GC — memory safety via **ownership** (each value has one owner; move semantics), **borrowing** (&T shared/immutable, &mut T exclusive), and **lifetimes** (compiler proves references don't outlive data). Data races are compile-time errors (`Send`/`Sync` marker traits).
- **Async model:** futures are lazy state machines; **Tokio** is the runtime (multi-threaded work-stealing executor + epoll/kqueue reactor). `async fn` compiles to a state machine; `.await` yields. Pinning exists because self-referential futures can't move.
- **Axum:** routing + extractors (typed request parts: `Json<T>`, `State<S>`, `Path<T>`) on top of **tower** middleware (`Service` trait — same middleware works for clients/servers/gRPC). Handlers are plain async fns; errors via `IntoResponse`.
- **Why we use it (IA hot paths only):** no GC pauses, predictable p99s, zero-cost abstractions, Arrow/Polars ecosystem for columnar shaping. Discipline: **"Go by default, Rust by measurement — an endpoint earns Rust with a profile."** In-house precedent: CortexEye's backend is Rust/Axum.
- **Gotchas they probe:** borrow-checker fights → restructure ownership (clone small, `Arc<Mutex<T>>` for shared mutable, channels for handoff); `Arc` vs `Rc` (atomic = thread-safe); blocking in async (use `spawn_blocking`); `unwrap()` in prod (don't — `?` + `thiserror`/`anyhow`).

## 3. Apache Kafka

- **Fundamentals.** Distributed, partitioned, replicated **commit log**. Topics → partitions (unit of parallelism + ordering); producers partition by key; consumer groups get exclusive partition assignment; offsets are consumer-owned progress markers.
- **Internals worth knowing:** sequential disk I/O + zero-copy sendfile = throughput; replication with leader/ISR, `acks=all` + `min.insync.replicas` for durability; **exactly-once** = idempotent producer (sequence numbers) + transactions (read-process-write atomically); log compaction for changelog topics; consumer rebalancing (cooperative sticky avoids stop-the-world).
- **Where I used it:** Uber menu ingestion bus (decouple bursty scrapers from consumers; replay for backfills; per-vendor key ordering). IA: async embedding jobs (`aiokafka`).
- **Numbers (Menu, ESTIMATED):** peak **~200–500 events/sec** during scraper fleet runs (30K menus/mo → ~1K/day, amplified by item-level events + retries). Steady-state lower. Do not invent partition counts without evidence — say "partitioned by vendor id; lag is the SLO."
- **Gotchas:** partition count is the parallelism ceiling; hot keys skew partitions; consumer lag monitoring is *the* health metric; ordering only within a partition; rebalance storms from slow consumers (`max.poll.interval.ms`).

## 4. Apache Flink

- **Fundamentals.** True **per-event streaming** (not micro-batch). Job = dataflow graph of operators; parallel subtasks; **keyed state** (per-key state backends — RocksDB for large state) is the superpower: dedup, aggregation, joins with state that survives failures.
- **Correctness machinery:** **event time vs processing time**; **watermarks** (assertion that no events older than T remain) drive window firing; **checkpoints** = distributed snapshots (Chandy-Lamport barrier alignment) giving exactly-once *state* semantics; end-to-end exactly-once needs transactional/idempotent sinks (two-phase commit sink to Kafka).
- **Where I used it:** Uber menu normalization — keyed dedup (vendor+content hash), event-time last-write-wins on out-of-order scrape retries, validation + routing (structured vs unstructured path).
- **Numbers (Menu, ESTIMATED):** sized for the Kafka peak (~200–500 events/sec); near-zero lag in steady state; state TTL on vendor keys. Checkpoint interval tuned so recovery does not exceed scrape retry windows.
- **vs Spark Streaming:** Flink = per-event latency + first-class state; Spark Structured Streaming = micro-batch, better for batch-parity code. Uber's standard stream engine is Flink.
- **Gotchas:** watermark skew from idle partitions (idleness markers); state growth → TTL it; checkpoint duration vs interval tension; backpressure propagates upstream (watch busy/backpressure metrics per operator).

## 5. Apache Spark

- **Fundamentals.** Distributed **batch** engine (also micro-batch streaming). Driver builds a DAG of transformations on DataFrames; **Catalyst** optimizes the logical plan; **Tungsten** does whole-stage codegen; stages split at **shuffle** boundaries; tasks per partition.
- **Where I used it:** Uber backfills/reprocessing (re-ingest a vendor's history after parser upgrades; large joins against catalog snapshots) + Databricks for exploratory pipeline work.
- **Numbers (Menu, ESTIMATED):** typical backfill / reprocess window **~1–2M item rows** — kept off Flink so real-time path is not starved.
- **Performance levers they probe:** shuffle is the enemy (partitioning, broadcast joins for small tables); skew handling (salting, AQE skew-join splitting); caching only reused intermediates; file sizes (small-files problem); predicate pushdown into Parquet.
- **vs Flink:** throughput-shaped, restart-a-stage recovery model — right for backfills; wrong for per-event latency.

## 6. Apache Pinot

- **Fundamentals.** Real-time **OLAP** store for user-facing analytics: sub-second filter/groupBy on high-cardinality data, at high QPS. Ingests **directly from Kafka** (real-time segments) + batch segments from files; columnar with inverted/sorted/star-tree indexes; scatter-gather query via brokers.
- **Where I used it:** Uber ingestion-health analytics — success/failure-rate by source/stage/error-class in near-real-time; alert rules on failure spikes; cut time-to-detect from hours to minutes. (Pinot is Uber's standard for real-time OLAP — it powers UberEats ops dashboards.)
- **Numbers:** sub-second filter/groupBy for ops dashboards (target); QPS is ops-dashboard scale, not public edge — do not invent a Pinot QPS number.
- **vs ClickHouse/Druid:** Pinot shines at high-QPS user-facing slices with upserts from Kafka; ClickHouse at heavy ad-hoc analytical scans. At Uber, Pinot was the paved road.
- **Gotchas:** segment sizing; upsert tables need primary keys + memory budget; star-tree index trades storage for pre-aggregation; real-time→offline segment handoff.

## 7. FastAPI + SQLAlchemy + Pydantic (the Python service kit)

- **FastAPI:** ASGI (Starlette) + Pydantic. Async-native handlers; `Depends()` DI (testable seams); auto OpenAPI. Sync handlers run in a threadpool — mixing blocking calls into async handlers is the classic pitfall.
- **SQLAlchemy 2.x:** Core (SQL expression language) + ORM (`Mapped[]` typed models, `select()` style). Session = unit of work + identity map. Why over raw SQL: refactor-safe column references (the Uber `IS_SELECT` aliasing bug was invisible in raw SQL), composability, type checking. N+1 → `selectinload`/`joinedload`.
- **Pydantic v2:** Rust-core validation; `model_config={"from_attributes": True}` to serialize ORM rows; validation at the boundary = the cheapest correctness you can buy.

## 8. Redis / Celery / Selenium (supporting cast)

- **Redis:** in-memory data structures; used for 24h-TTL financial-read caching (Uber FRM), Celery broker + hot caches (Masters India), semantic-cache TTL layer (IA). Probe answers: eviction policies (`allkeys-lru`), persistence (RDB/AOF), cache stampede (jittered TTLs, singleflight).
- **Celery:** task queue semantics — retries with backoff, rate limits, scheduled tasks, idempotency keys; vs Kafka: task semantics vs replayable stream semantics.
- **Selenium:** browser automation for scraping; the engineering is in the anti-bot layer (IP rotation, UA/fingerprint management, proxy pools, retry budgets) and in treating scraped output as an untrusted input stream (validate before bus).

## 9. One-line "why" for everything else on the page

- **gRPC:** binary protobuf contracts + HTTP/2 streaming for service-to-service; REST for public/browser surfaces.
- **WebSockets/SSE:** SSE for one-way agent progress streaming (copilot results streaming as they score); WebSockets when bidirectional.
- **Bazel:** hermetic, incremental monorepo builds (Uber standard); gazelle generates BUILD files.
- **ELK/New Relic/Grafana/Sentry:** logs/APM/metrics/errors — correlation IDs end-to-end was the triage unlock (70% faster).
- **Docker/Kubernetes:** container per service; K8s for orchestration.
- **pgvector:** cosine-distance ANN inside Postgres — semantic cache without new infra.
