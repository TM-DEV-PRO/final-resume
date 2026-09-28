# 07. My projects deep dive (OCI framing)

For each project: the **30 second pitch**, the **2 minute walkthrough**, **architecture**, **key decisions and trade-offs**, **failure modes**, **OCI JD tie-ins**, **likely questions with answers**, and **honesty lines**. Numbers match the PyGo PDF.

<div class="callout warn">
<b>Honesty lines to keep (say these unprompted if they fuse numbers).</b>
<ul>
<li>80% is a CI promotion gate on 300 cases, not live accuracy across tenants.</li>
<li>73% cost cut and the 74% baseline come from the gold-200 bench.</li>
<li>15.5x is query time on a 250M-row harness. The 170 GB OOM fix is load time.</li>
<li>344k is rows per second, not RPS. It was measured on a 4.09B-row table while the copy was in flight.</li>
<li>Partition rollback is DROP PARTITION then recopy. It is not an atomic reader swap.</li>
<li>Uber roles are via EPAM. ANZ numbers are historical. Menu 98% is offline eval.</li>
<li>No Kafka, Flink, CDC, or Kubernetes cluster operations on AssortSmart. No HITL queue.</li>
</ul>
</div>

---

## 1. Impact Analytics: AssortSmart (Senior Software Engineer, Platform & AI), May 2026 to present

AssortSmart helps retail merchandise planners decide assortments: which articles to keep, drop, or add each season, per store cluster. I work on two things: the **core platform** (Go services, ClickHouse analytics, security) and the **agentic decision layer** (batch AI scoring + the Ask Iris copilot).

### 1A. Core Infrastructure & Pipeline

**30 second pitch**
> I built the Go/Gin platform layer that scales to 10k peak RPS as a self-protecting edge. I moved planner analytics onto ClickHouse rollups, which cut a 250M-row pivot from 189 seconds to 12. I fixed a 170 GB OOM in weekly rollups by slicing work into fiscal weeks. And I wrote a Go native-TLS pump that copies partitions between ClickHouse Cloud clusters at about 344k rows/s.

**Architecture**
```
planner UI / API clients
      │  HTTPS (LB) → h2c
      ▼
Go/Gin platform (stateless, Wire DI, nested ctx timeouts, Datadog tracing)
   ├─ auth waterfall: Redis cache → Firebase Admin → JWT / Google OIDC; constant-time API keys
   ├─ role + hierarchy (UAM) resolution from Postgres roles → tenant + hierarchy scope
   ├─ KPI configurator: tokenizer → parser → parameterized CH SQL (ifNotFinite guards)
   └─ reads ──► ClickHouse: 6 rollup tables (season + weekly grain; product/store/attr)
                 PARTITION BY season_code, bloom skip indexes
      Postgres: roles, config, OLTP cells
build path: loader (INSERT SELECT per fiscal week, caps + spill, TSV ledger)
copy path:  Go pump (source CH Cloud → native TLS → operator host → native TLS → target CH Cloud)
```

**Walkthrough and decisions**

1. **Go/Gin edge, no reverse proxy.** The process owns h2c, nested context timeouts (the edge sets the budget and inner calls inherit the remaining deadline), and Datadog traces. It's one less hop and one less ops surface.
   - *Trade-off:* no proxy-level features (WAF, connection limits) unless we add them in middleware or at the load balancer.
   - I don't claim an SLA number.
2. **Google Wire compile-time DI.** Wiring errors fail the build, not a request. There's no runtime reflection.
3. **Multi-tenant isolation and access control.** Identity is resolved through a **Redis-fronted** waterfall (Firebase Admin → JWT → Google OIDC), and hot identities hit the cache. API keys are compared in **constant time** (no timing side channel). **Postgres-backed roles** give UAM-scoped hierarchy access. The tenant and hierarchy come from the verified identity, not request parameters. Isolation is enforced across both Postgres and ClickHouse.
4. **KPI configurator.** Operators write formulas like `(sales - cost) / sales`. A Go tokenizer and parser allowlist the functions, map logical names to physical columns, and emit **parameterized** SQL fragments wrapped in `ifNotFinite(toFloat64(expr), 0)` (division-by-zero protection). New KPIs don't need a release. *Security:* no string concatenation of user input into SQL; the grammar is an allowlist.
5. **ClickHouse migration: 15.5x.**
   - Planner pivots on Postgres hit 189s at 250M rows.
   - I wrote the RFC and a **row-identical harness**: same rows, same query, answers compared.
   - ClickHouse ran it in 12s.
   - We pay once at load (pre-aggregated rollups) and read cheap (partition pruning, bloom indexes).
   - Postgres stays for OLTP.
6. **Six rollup tables.** Season and weekly grain × product, store, and attr.
   - Store and attr drop SKU-level dims and **re-weight** so store totals equal SKU sums.
   - Attr is an unpivot (`ARRAY JOIN` over attribute pairs), so attr weekly is ~5x product weekly.
7. **170 GB OOM.**
   - Whole-season weekly `INSERT SELECT` needed ~110 `any()` states plus `argMax`/`argMin` over wide strings, around 170 GB of aggregator state. It failed at 80 GB and 200 GB caps on a ~59 core / ~236 GiB replica.
   - Fix: the unit of work became **one fiscal week**, with generated settings of 8 threads, a 55 GB cap, 16 GB spill, and 4 weeks in flight.
   - Product weeks peak at ~11 GB and attr weeks at over 40 GB.
8. **Go pump, ~344k rows/s.**
   - Why it exists: cluster-to-cluster pull was blocked by Cloud IP allowlists, while the operator IP was allowed.
   - How it's fast:
     - Native protocol over TLS.
     - 500k-row **columnar** buffers (`batch.Column(i).Append`, no per-row reflection).
     - **Double buffering**, so reading the next batch overlaps sending the previous one. That also cured the HTTP `unexpected EOF` when the SELECT sat idle during an INSERT.
   - Parallelism: `-workers N` copies N seasons in parallel with their own connections. Caps are per process (about 48 threads / 180 GiB split across workers).
   - Safety:
     - The per-season checkpoint ledger records only finished seasons.
     - An incomplete season means DROP PARTITION then recopy.
     - SIGINT finishes the batch without checkpointing.
     - A per-table flock prevents two terminals copying the same table.
     - Secrets come from env only.
9. **64.1M ghost rows (the loader, not the pump).**
   - A failed HTTP INSERT still commits the blocks it wrote. A half-loaded 64.1M-row partition passed "skip if the partition has rows."
   - Fix: a TSV ledger of finished `(kind, season_code)`, with success taken from `system.query_log` `QueryFinish`, and a missing entry means drop and rebuild.

**Failure catalog (this doubles as a runbook, and OCI loves it)**
1. OOM on weekly GROUP BY: shrink to one week and measure attr weeks before adding RAM.
2. A half-written partition looks complete: never use `count() > 0` as success.
3. An HTTP client timeout after the server committed: trust `system.query_log`.
4. HTTP SELECT EOF during INSERT: double buffer, or use the native protocol.
5. Retrying a spent batch: duplicates. Drop and restart the unit instead.
6. Native TLS reset: crash, and checkpoint only finished seasons.
7. Allowlists block cluster pull: the pump is the workaround, and the proper fix is allowlisting + server-side `INSERT SELECT` or object storage.
8. Oversubscribing workers: caps are per process.
9. Never commit Cloud passwords.

**OCI JD tie-ins:** large-scale data processing, data plane reads, performance testing (the row-identical harness), recovery-oriented design (ledgers, restartable units), automation tooling, multi-tenant access control, and correctness checks (parity sums).

**Likely questions**

- **Why not just add Postgres indexes or materialized views?**
  Pivots aggregate across huge slices with many dimensions. Row stores read whole rows. Columnar storage + compression + vectorized execution wins by an order of magnitude for this access pattern. We measured it instead of guessing, and Postgres stays for OLTP.
- **How do you keep rollups consistent with source data?**
  Rebuild per partition at a captured watermark. Parity checks: `sum(product) = sum(store) = sum(attr)` at the same filters. Earlier season-grain parity was 0% difference across seasons 1 to 7. ReplacingMergeTree handles corrections by version.
- **What's the biggest risk in the pump?**
  No atomic swap. A crash leaves a truncated season until DROP + retry, and readers can see it partially. The better design is building into a scratch table and `REPLACE PARTITION`. I wrote it, but it wasn't executed. I'd do that before calling it production-grade.
- **How would you make this OCI-grade?**
  - Move the copy server-side (no operator host) and use atomic partition swaps.
  - Add a completeness check before publish.
  - Emit metrics per season (rows/s, lag, failures) with alarms.
  - Run it as a scheduled, idempotent job with the ledger in a durable store instead of local files.
- **How did you test the 10k RPS?**
  Load tests against the Gin edge and Datadog under peak traffic. I talk about p95/p99 and saturation, and I don't quote an SLA.

---

### 1B. Agentic Flows & Orchestration

**30 second pitch**
> I built a batch AI decision engine for merchandise planning: Keep/Drop, Missed Opportunities, and Top Style. It scores 348k article-seasons, 88k items per pass, by blending deterministic KPI math with structured LLM calls across 7 AI lenses. It's built to survive provider failures, with hard timeouts, circuit breakers, and durable checkpoints. I also shipped Ask Iris, a JWT-secured WebSocket copilot with tenant scope frozen at the handshake, and an eval gate so no model change ships without passing 80% on 300 cases.

**Architecture**
```
start (CLI / HTTP) → freeze config (guardrails, params, prompts, catalog) → config_hash (SHA-256)
   → deterministic KPI phase (Python) ──► det.json checkpoint
   → claim ledger → batch mapper (88k per pass, bounded parallel batches)
        packed JSON context (no DB access) → LLM (hard timeout) → schema-validated lens scores (7 lenses)
        circuit breaker per provider; on timeout/open → deterministic baseline score
        agent_progress.json appended per article
   → blend (frozen weights) → engine insert → ClickHouse ReplacingMergeTree (versioned; retries don't duplicate)
   → telemetry JSON per run: tokens, USD, step duration, batch fallbacks; config_hash on every row
Ask Iris: WebSocket (JWT on handshake) → plan_scope frozen → LangGraph supervisor → worker tools (scoped)
          → evaluator (MAX_ATTEMPTS = 3) → answer; LangSmith traces
Eval: 300-case proxy harness, 80% CI gate; gold-200 bench for model choice (74% det baseline)
```

**Decisions and trade-offs**
- **Deterministic math, LLM for judgment.** LLMs are bad at arithmetic, so KPIs are computed in code and the LLM sees them as JSON.
- **No SQL tool for the LLM.** At 88k items a SQL tool would be runaway queries, pool exhaustion, and injection risk against a 2.11B-row master.
- **ReplacingMergeTree** writes. Retries and overlapping waves can land twice, and RMT keeps the latest version per key. Reads use `argMax` / `LIMIT 1 BY`, not `FINAL`, as a runtime requirement.
- **Fallback to baseline** on timeout. The run always completes, and telemetry shows how much fell back.
- **Checkpoints.** A provider outage at item 70k doesn't redo the det phase or finished articles.
- **App-native orchestration, not Airflow/Temporal.** It needed tight coupling to CH inserts, config hashing, and per-run cost telemetry. I'd pick Temporal for cross-team, cross-service workflows with human steps.
- **Frozen weights.** On gold-200 the blended LLM scored ~63%, below the 74% deterministic baseline. I refused to retune weights on a small proxy set.
- **Model choice.** The chosen model completed 200/200 at 73% lower cost with 100% lens coverage. A cheaper option returned pending rows, so completion reliability won.
- **Ask Iris safety.**
  - JWT is checked on the handshake, via `Authorization: Bearer` or `?token=`.
  - `plan_scope` is frozen once, and tools inherit it.
  - The evaluator is capped at 3 attempts, with a recursion limit on the supervisor graph. It fails closed with a graceful response.

**Failure modes and handling**
| Failure | Handling |
|---|---|
| Provider 502/504 storm | Breaker opens; det fallback; run completes; fallback count in telemetry |
| Process crash mid-run | `--resume` reloads det.json and progress, and skips finished items |
| Duplicate writes on retry | RMT versioning + argMax reads |
| Prompt/config drift | config_hash on every row; eval gate on change |
| LLM loops in chat | 3-attempt evaluator cap + recursion limit |
| Cross-tenant question in chat | Scope frozen at handshake; tools can't widen it |
| Cost runaway | Per-run USD telemetry; model chosen by cost at 100% coverage |

**OCI JD tie-ins:** retries, circuit breakers, and timeouts; recovery-oriented design (checkpoints); telemetry (tokens, cost, fallbacks); tests as deployment guardrails (the eval gate); multi-tenant access control; change management for models (a promotion gate + config hash).

**Likely questions**
- **How do checkpoints work?**
  Det results land first. As LLM chunks complete, per-article progress is appended. On restart, det is reloaded, finished articles are skipped, and the LLM map continues.
- **How do you handle rate limits at 88k?**
  Bounded parallel batches, hard per-batch timeouts, backoff, and the breaker. A throttle doesn't wipe the run.
- **Is 80% your production accuracy?**
  No, it's the CI promotion gate on the 300-case file. The model comparison is gold-200.
- **Why 3 attempts?**
  It bounds cost and latency. Beyond 3 attempts, quality gains were not worth a stuck chat, so it fails closed with a helpful message.
- **What would you add for OCI scale?**
  - A durable job store instead of local JSON checkpoints.
  - Per-tenant quotas.
  - SLO alarms on fallback rate and run duration.
  - Canary rollout of prompt changes to one tenant before all.

**Do not say:** HITL review queue, LangSmith on the batch engine (LangSmith is Ask Iris), questions/week or tenant SLAs for Ask Iris, "all tenants live at 80%."

---

## 2. Uber (via EPAM Systems): FRM Scoping Platform (SDE 2), Jul 2024 to May 2026

**30 second pitch**
> At Uber Finance via EPAM, I owned the backend for Financial Risk Management scoping, the quarterly process that decides which financial line items are in audit scope. We moved it from a Google Sheets workbook to FastAPI and MySQL across 19M GL rows, with 36 endpoints and a nested L1 to L4 hierarchy. Reconciliation went from 14 days to 3 against a $340M materiality threshold. I also led 3 engineers on a SQLAlchemy 2.0 migration to 100% coverage with SOX gates.

**Architecture**
```
Fusion.js UI → FastAPI scoping service (Uber langfx, Bazel monorepo)
   router → service → repository / ORM classmethods (SQLAlchemy 2.0, typed Mapped[])
   → MySQL on SOADB: 8-table normalized schema
        level_mapping (L1–L4 FSLI spine) ← balance_sheet / income_statement / component_entity
        scoping_questions + scoping_assessments (qualitative answers)
        metrics (materiality, benchmarks), threshold setup, EMI data, recon tables
ETL (pipeline team) loads HFM GL balances → MySQL
```

**Key decisions**
- **Normalized 8-table schema** with `level_mapping` as the spine. Joins are always ANDed with the fiscal period and active flags.
- **Polymorphic review status** (Draft, Review, ReOpen, Closed) on the fact rows, driving FSM transitions.
- **Optimistic row locking:** a version column, so two reviewers editing the same line can't silently overwrite. One gets a conflict.
- **Atomic cross-table syncs:** updates to a line and its dependent rows happen in one transaction.
- **SHA-256 natural keys** (e.g. hashing the question text + normalized page name). Reloading the same data produces the same keys, so reloads are idempotent and there are no duplicates across quarters.
- **SQLAlchemy 2.0 migration** (I led 3 engineers):
  - The motivating bug was raw SQL reading income-statement rows with balance-sheet column lists (column aliasing). Typed ORM models make that impossible.
  - We shipped via **stacked Bazel PRs** (small, reviewable, reversible) with zero-downtime releases.
- **SOX controls:**
  - **Reporting SQL allowlists.**
  - **FSM gates with 50% delta-variance checks:** a quarter-over-quarter swing above 50% blocks the state transition until it's reviewed.
  - 100% statement coverage on the migrated module.

**Stories here:** the "pure refactor that wasn't" (my mistake, caught, and a process fix), "coverage that lied" (34.6% to 100%), and the rulebook disagreement (classmethods on models).

**OCI JD tie-ins:** compliance (SOX), change management (stacked PRs, gates), data integrity (optimistic locking, natural keys), code review for correctness, and leading a small team.

**Likely questions**
- **How does optimistic locking work here?**
  Read the row with its version. Then `UPDATE ... SET ..., version = version + 1 WHERE uuid = ? AND version = ?`. If 0 rows are affected, someone else changed it: return a conflict so the UI can refresh.
  - Why not pessimistic: reviewers hold rows open for minutes, so locks would block everyone.
- **What does 14 to 3 days actually come from?**
  Removing manual Sheets mapping and reconciliation steps: automated HFM vs 10-Q recon, computed materiality and thresholds, and collaboration with status history in one tool. It's framed in the design doc, and I defend the PDF number.
- **Why SHA-256 natural keys instead of auto-increment?**
  Deterministic identity across reloads. The same source row always maps to the same key, so reloads are upserts, and audit history across quarters lines up.
- **Zero-downtime releases?**
  Stacked PRs where each step is backwards compatible. Schema changes are additive first, and v1 endpoints stayed live while the v2 MySQL-backed endpoints rolled out.

**Honesty:** via EPAM, and the ETL from HFM is owned by the data pipeline team.

---

## 3. Uber (via EPAM): Menu Ingestion & Automation (Uber Eats)

**30 second pitch**
> I built an automated menu ingestion pipeline processing 30K+ menus a month. It cut restaurant onboarding from 24 hours to 2 and saved about $600K a year. Unstructured, multilingual PDFs are converted into a strict catalog schema at 98% field fidelity in offline eval, using Gemini 2.5 Pro with LangChain RAG over Milvus. Selenium scrapers were hardened to 95%+ success, and a Kafka + Flink pipeline does keyed dedup and schema normalization for exactly-once catalog upserts.

**Architecture**
```
partner sites / PDFs / images
  → Selenium fleet (GCP) + dynamic proxy pools + adaptive retries (per-source budgets)
  → Kafka (keyed by vendor_id: per-vendor ordering, replay, fan-out)
  → Flink (event time, watermarks, keyed dedup state by content hash / menu version, schema normalize)
       ├→ structured items → idempotent catalog upsert
       └→ unstructured → RAG path: retrieve similar labeled menus (Milvus) → Gemini 2.5 Pro → schema validate
```

**Decisions**
- **Kafka** decouples the bursty scrapers from slow catalog writes, gives replay after a bad parser deploy, and supports multiple consumers.
- **Flink** gives keyed state for per-vendor dedup, event-time handling for late pages, and checkpoints.
- **"Exactly-once" honestly:** end to end, it's at-least-once + idempotent upserts. Flink checkpoints + an idempotent sink make the effect exactly once. I never claim 2PC across third-party sites or the LLM.
- **RAG:** retrieving similar labeled menus as few-shot context + strict schema validation. 98% is field fidelity on offline eval.
- **Anti-bot:**
  - Per-source block signatures, then IP rotation, fingerprints, proxy pools, and retry budgets.
  - Block rate goes on the same dashboard as parse failures.
  - Success went from ~60% to 95%+.

**OCI JD tie-ins:** retries and backoff, streaming data processing, dedup and synchronization, and metrics dashboards.

**Likely questions**
- **What's your SLO?**
  Consumer lag and freshness (menu available within minutes of a scrape), plus parse success rate.
- **Bad parser deploy?**
  Roll back the parser, rewind Kafka offsets to before the bad window, and reprocess. Idempotent upserts make the replay safe.
- **Backpressure?**
  A slow catalog backs up Flink's network buffers, and Kafka consumer lag rises. That's the alert.

**Honesty:** Spark isn't on the PDF. ClickHouse is not in this pipeline.

---

## 4. Uber (via EPAM): Document Compliance (Uber Mobility ANZ)

**Pitch:** automated driver and vehicle document verification for Uber Mobility in Australia/New Zealand against local authority requirements. 99.9% regulatory compliance, and it removed about 20 hours a week of manual review by replacing manual queues with a deterministic validation backend.

**Talking points:** deterministic rules (document type, expiry, jurisdiction-specific requirements), audit trails, and exception routing for what rules can't decide. The numbers are historical. Don't add Selenium or RAG here.

**OCI tie-in:** compliance, automation replacing manual toil, and deterministic guardrails.

---

## 5. Masters India: GST Compliance & E-Invoicing Platform (SDE 2), Dec 2022 to Jun 2024

**30 second pitch**
> Masters India is GST compliance and e-invoicing SaaS. Clients push invoices, we validate and register them with the government Invoice Registration Portal, and return signed e-invoices. I led the migration from a PHP monolith to FastAPI microservices, taking p95 from 1.2s to 300ms for 1,500+ clients and throughput from 700 to 4,000 requests per minute. I also built the bulk pipeline on Kafka and Postgres sharded by tax quarter: 1M+ submissions a day, idempotent 100K+ imports, dead-letter queues, and bounded retries against the flaky government portal. And I rolled out ELK + New Relic, which made triage 70% faster.

**Architecture**
```
clients → gateway (Nginx: per-endpoint canary routing, config rollback)
   ├→ legacy PHP (shrinking)
   └→ FastAPI services (auth, e-invoice submit, bulk import, reconciliation)
        → Redis cache-aside (client config, tax masters, auth context; TTL jitter; SETNX singleflight)
        → Postgres sharded by tax quarter
        → Kafka (partition key = client GSTIN: per-taxpayer ordering, replay)
             → Celery / consumer workers (bounded concurrency to IRP, exp backoff + jitter)
                  → IRP (government portal)
                  → DLQ for poison batches → operator replay
   observability: JSON logs + request_id → ELK; New Relic APM; alert rules on error rate / latency
```

**Walkthrough**
1. **Strangler, not big bang.** One domain at a time behind the gateway.
   - A canary percentage per endpoint, watching dashboards, with rollback as a config change.
   - A shared DB during cutover (no dual writes), and service-owned tables split out after traffic moved.
   - Contract tests pinned the PHP responses field by field.
   - Cutovers were frozen during GST deadline weeks.
2. **Latency win.** Async IO for IRP calls (no worker held hostage), connection pooling, composite index `(client_id, invoice_date)`, N+1 removal, pagination, and Redis for hot reads (−30% DB reads). Caching moved the median; async + query fixes moved the tail.
3. **Bulk pipeline.**
   - A file lands, validation runs in chunks (schema, GSTIN, duplicates).
   - Batches register with the IRP under bounded concurrency with backoff and jitter.
   - Progress streams to the client dashboard.
   - Idempotency key = `client + fileHash + batchIndex` + client invoice refs.
   - Poison batches go to a DLQ for replay.
   - Sharding by tax quarter matches the access pattern (filings are per quarter) and keeps hot data small.
4. **Observability and quality.**
   - Request IDs across services and workers.
   - ELK + New Relic APM with alerts on error rate and latency SLOs. Triage went from ~30 min to under 10 (the 70% is historical).
   - Coverage 35% → 82% as a CI gate, money paths first. 98% deploy success.
5. **Mentored 2 engineers** who each owned a service extraction.

**Stories:** the timeout canary (10s vs 60s, rolled back by config, moved to async 202), the double-filing near-miss (idempotency everywhere + DLQ + an incident template), and the migration under deadlines.

**OCI JD tie-ins:** almost every line.
- Zero-downtime migration (no maintenance windows).
- Retries, backoff, and a breaker against a flaky dependency.
- Idempotency and a DLQ (recovery).
- Alarms and dashboards.
- Incident reviews.
- Change management (canary + rollback + freezes).
- Scaling (sharding, queue-based load leveling, autoscaling workers on queue depth).
- Compliance (GST).

**Likely questions**
- **Derive TPS from your numbers.**
  1M/day ≈ 12 TPS average; peaks around 8 to 10x on filing deadlines, so ~100+ TPS (estimated). 700 → 4,000 rpm is ≈ 12 → 67 RPS at the API.
- **Why Kafka over SQS/RabbitMQ?**
  Per-client ordering (partition by GSTIN), replay for compliance disputes, and multiple consumer groups. The ops cost was the trade-off. RabbitMQ would have worked for task dispatch at our scale.
- **How do you protect against a cache stampede?**
  TTL jitter + a SETNX lock so one worker recomputes while the others wait or serve stale.
- **Circuit breaker on the IRP?**
  Open when the IRP error rate spikes. Clients see a degraded "queued" status instead of errors, and work resumes when it closes.

**Honesty:** say "on-call alerting and faster triage." Don't invent a formal pager rotation title.

---

## 6. GeeksforGeeks: Courses Platform and Influencer Dashboard (SDE), Aug 2021 to Nov 2022

**Pitch:** migrated the doubt-support platform from PHP to Django. It handles 10K+ daily queries and 10x spikes during live coding contests. I built REST APIs for voting, pinning, and locking threads on MySQL, MongoDB, Redis, and Elasticsearch, and the business attributes a 20% lift in premium subscriptions to it. I also built an influencer analytics and earnings dashboard (30% course-sales lift, by the business team's attribution), plus async scheduled workflows for video processing, reminders, and cleanup (70% ops efficiency).

**Talking points:**
- **Votes:** a unique `(user, content)` constraint for correctness, Redis counters for display, and async reconciliation to MySQL to avoid hot-row contention on popular posts.
- **Contest spikes:** caching, read/write separation, and pagination.
- **SMTP connection reuse:** it cut send time roughly in half, because TLS handshakes aren't repeated.
- **What I'd change today:** vote events on a queue and idempotent crons.

**OCI tie-in:** handling spikes, hot-row contention (distributed state), and automating toil.

---

## 7. Cross-project answers OCI asks

| Question | Best project | One-line answer |
|---|---|---|
| Most complex system you built | AssortSmart core + agentic | Go edge + ClickHouse rollups + batch AI with recovery built in |
| Hardest bug | 64.1M ghost rows or 170 GB OOM | The success signal came from the wrong place; shrink the unit of work |
| Scaling story | ClickHouse 15.5x / Masters 700 → 4,000 rpm | Measure, find the bottleneck, change the access pattern |
| Reliability story | Registry (timeouts, breakers, checkpoints) | Provider failures degrade, runs finish |
| Data integrity | FRM optimistic locking + SHA-256 keys; RMT | Concurrent reviewers and retries can't corrupt |
| Security | Ask Iris frozen scope; auth waterfall; KPI compiler allowlist | Structure beats instructions |
| Zero-downtime change | Masters strangler; FRM stacked PRs | Canary, config rollback, backwards compatible steps |
| Incident / RCA | Double-filing near-miss; ghost rows | Blameless review, systemic fix, template |
| Observability | Masters ELK + New Relic; IA Datadog + run telemetry | Request IDs; alert on symptoms |
| Leading people | FRM (3 engineers), Masters (mentored 2) | Conventions, ownership, reviews |
| Automation / tooling | Go pump + ledger; generated rollup settings | Idempotent, restartable, safe by default |
| Compliance | FRM SOX gates; GST | Allowlists, FSM gates, audit trails |
