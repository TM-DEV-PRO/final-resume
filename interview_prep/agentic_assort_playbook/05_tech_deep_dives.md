---

# 5. Technology deep dives (funda · architecture · why it solves the problem · gotchas)

Each entry is what you should be able to say if an interviewer points at a word on your résumé.

## 5.1 ClickHouse
- **Fundamentals.** Open-source **columnar OLAP** DB. Column-oriented storage + vectorized execution → aggregations scan only needed columns, compress well, and run SIMD-fast. Data lives in immutable **parts** (sorted by the table's `ORDER BY`); a background process **merges** parts (the "MergeTree" family).
- **Architecture (engines).** `MergeTree` = base (sorted parts, partitioning, sparse primary index). `ReplacingMergeTree(version)` = on merge, keep the **highest `version`** per sort key → dedup by newest. `AggregatingMergeTree` = store partial aggregate states (`AggregateFunction`) merged incrementally. `Distributed`/`Replicated*` = sharding/replication (we defer to ClickHouse Cloud). **Partitioning** (`PARTITION BY`) prunes at query time; **`ORDER BY`** is the primary/sort key that clustering + the sparse index rely on. **Projections & materialized views** precompute alternative sort orders/rollups.
- **How it solves our problem.** Pivot + hindsight are scan-and-aggregate → columnar is ideal. Its weakness — **async mutations** (`ALTER UPDATE/DELETE` degrade >500, stop >1000) — is avoided by our **insert-only/versioned** model: edit = insert a new `version`, read = `argMax(version)`, bulk = `REPLACE PARTITION`. So we use the engine only where it's strong and never touch the mutation queue.
- **Deep-dive/gotchas.** `argMax` (or `FINAL`) is needed on read because dedup only happens *eventually* on merge; keep partitions from getting too many parts (hot-partition churn) — we partition by `(tenant, l1, fiscal_week)`; `SELECT FINAL` is convenient but costs a merge-on-read; `AggregatingMergeTree` requires `-State`/`-Merge` function discipline. It is **not** for per-row transactional read-after-write with locks — that's Postgres's job.

## 5.2 BigQuery
- **Fundamentals.** Serverless columnar warehouse; storage (Capacitor columnar) separate from compute (**slots**). You're billed **on-demand by bytes scanned** (or by slot reservations). No secondary indexes.
- **Architecture.** **Partitioning** (usually by date) + **clustering** (sort within partitions by up to 4 cols) are the only "indexes." Query cost = columns read × partitions touched. DML (`UPDATE/MERGE`) is quota-limited and rewrite-oriented → not for interactive edits.
- **How it solves our problem.** Perfect **source of truth** + batch cube/rollup builder: cheap, scalable scans; scheduled ELT. We keep planner edits *out* of BigQuery.
- **Deep-dive/gotchas.** The three levers that gave ~3×/~74×/~280×: (1) read the **clustered** copy not the raw fact, (2) always pass a **partition/date predicate** (a bypass floor like `date > '1999-01-01'` *defeats* pruning), (3) **never `SELECT *`** (one `SELECT * LIMIT 2` billed 38.8 TiB / $327). Set `require_partition_filter=TRUE` so un-pruned scans fail loudly.

## 5.3 PostgreSQL
- **Fundamentals.** Row-store RDBMS, **MVCC** (each write creates a new tuple version; `VACUUM` reclaims dead tuples), full ACID, rich indexing (btree, GIN, partial, expression), declarative **partitioning**, `jsonb`.
- **Architecture in our stack.** The **editable system-of-record**: plan masters + the editable grid as row tables with stored procs; LIST-partitioned by tenant / `final_level`; **PgBouncer** pools connections (`aiopg` async). GIN index on `jsonb` attribute bags; composite btrees for hot filters.
- **How it solves our problem.** ACID + read-after-write + locking = exactly what a per-cell planning edit needs (the thing OLAP engines are bad at).
- **Deep-dive/gotchas.** MVCC + del+reinsert = **dead-tuple bloat** (needs VACUUM); a `jsonb ->>` filter can't use a `jsonb_path_ops` GIN (rewrite as `@>`); **always include the partition key** or you scan every partition; cascade-delete FK columns must be indexed or each parent delete seq-scans children; prefer **set-based `UPDATE … FROM json_to_recordset`** over N+1 per-row loops; over-partitioning (5,503 partitions for 298K rows) hurts planning time.

## 5.4 DuckDB
- **Fundamentals.** Embedded ("SQLite for analytics") **columnar, vectorized** OLAP engine; runs in-process, reads Arrow/Parquet zero-copy.
- **How it solves our problem.** Per-plan/per-session **pivot accelerator**: hydrate the plan's small cube slice into DuckDB, run native `PIVOT … USING sum() GROUP BY`, commit deltas to Postgres — fast cross-tabs without a server round-trip or rescanning facts.
- **Deep-dive/gotchas.** Great single-node/embedded; not a multi-user server (that's why it's session-scoped and Postgres/ClickHouse own durability + concurrency).

## 5.5 Agent orchestration (router / planner-executor / supervisor) & LangGraph
- **Fundamentals.** **LangGraph** models an agent app as a **state graph** (nodes = steps/agents, edges = control flow, a shared typed **state** object) — good for cyclic, multi-step, human-in-the-loop flows vs. a linear chain. The classic patterns: **router** (classify then dispatch), **planner-executor** (plan a DAG, then execute), **supervisor/orchestrator** (a controller delegates to workers and synthesizes).
- **Architecture (ours).** Router → Decomposer (emits a validated DAG) → Orchestrator executes stages (parallel within stage) → synthesize. CortexEye's production brains are LangGraph; our multi-agent PoC is a **custom** Python router/orchestrator (stdlib `concurrent.futures`) that mirrors that shape deterministically for testability.
- **How it solves our problem.** A planning question needs several specialized data pulls with dependencies; a validated DAG + supervisor gives parallelism, dependency passing (`<A_n>`), partial-failure tolerance, and an auditable trace.
- **Deep-dive/gotchas.** The **#1 failure is a malformed plan** → a hard structural validator + one self-repair pass is the fix; guard against forward references; keep stages ≤3 agents wide, ≤8 sub-questions; make each agent's `answer()` non-throwing so one failure yields a *partial*, not a crash.

## 5.6 LLM plumbing (text-to-SQL, decomposition, confidence, RAG, cache)
- **Text-to-SQL.** LLM emits SQL from NL + schema (LlamaIndex RAG over schema in CortexEye). **Guardrails are the engineering:** SELECT-only, `LIMIT` caps, `NULLIF` denominators, no `SELECT *`, validate before execute. Solves "let business users ask in English" without runaway scans.
- **Query decomposition.** One strong prompt (18 worked examples) → `{sub_queries[], path[][]}` DAG + `<A_n>` dependency rephrasing + a reflection/repair loop. Solves multi-hop questions ("why did margin drop and which clusters?") that a single query can't.
- **Intent classification / confidence.** A deterministic rules prompt at `temperature=0` (chosen over a RAG/few-shot classifier for **latency, cost, determinism on novel queries**); confidence via **rules + LLM logprobs + intent-match + error detection**. Solves routing + "should we trust/show this answer."
- **RAG (hybrid).** `text-embedding-3-small` → **pgvector**; **BM25 (sparse) + dense** retrieval fused, then **Cohere rerank**. Hybrid beats either alone (lexical + semantic); rerank fixes ordering.
- **Semantic cache.** Embed the query; return a cached answer when cosine-sim ≥ threshold within TTL (pgvector `<=>` in prod). Solves repeat/near-duplicate questions → skip the whole pipeline. Gotcha: threshold too loose returns wrong-but-similar answers — tune + TTL-bound.

## 5.7 Rust / Axum (CortexEye data API)
- **Fundamentals.** Rust = memory-safe, no-GC, high-throughput; **Axum** (on **Tokio** async runtime, **SQLx** compile-checked queries) is the HTTP framework.
- **How it solves our problem.** A **deterministic, fast data API** layer (BigQuery/GCS access, TTS streaming) separate from the probabilistic Python LLM services — clean separation of "deterministic data" vs "AI reasoning," and Rust's throughput/safety for the hot data path.
- **Deep-dive.** Compile-time-checked SQL (SQLx) prevents a class of query bugs; async I/O (Tokio) for high concurrency; keeps LLM latency/cost out of the core data path.

## 5.8 Supporting infra
- **FastAPI + asyncio** — async Python services; `asyncio.gather` to run classification + entity-extraction (or independent reads) concurrently.
- **Redis** — chat history, **semantic cache**, and **abort flags** (cancel a running task across Cloud Run replicas). Fundamentals: in-memory key-value, sub-ms, TTL, pub/sub.
- **Socket.IO / WebSockets (WSS)** — stream agent progress/partial tokens to the UI (long LLM calls need incremental feedback).
- **Google Cloud Tasks + Scheduler** — async job offload + cron for ELT/cube builds (keeps heavy work off the request path).
- **Secret management** — Google Secret Manager, IA convention `{client}_ms_ce_chatbot_{provider}_{env}`; ADC auth; no keys in code.
- **Apache tech (what the product actually uses).** **Apache Kafka** (`aiokafka` / `confluent-kafka`) drives **async embedding jobs**, and **Apache Parquet** is the columnar storage/interchange format (§8.3). The **planning-store ingestion path** itself is **batch ELT** (BigQuery cube/rollup → Postgres/ClickHouse), not a streaming pipeline into the grid — so be precise: "Kafka for async embedding work + Parquet for storage; the grid's data lands via batch ELT." Kafka fundamentals to know: distributed append-only commit log, topics→partitions, consumer groups, at-least-once + offsets. If asked "where else would Kafka fit?": streaming POS/inventory events into the fact, or a CDC→ClickHouse path (ClickPipes / Kafka engine).
