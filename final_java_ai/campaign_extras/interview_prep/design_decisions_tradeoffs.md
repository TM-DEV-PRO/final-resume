# Design Decisions and Tradeoffs (resume-aligned)

Every major decision on `Tarun_Mittal_SSE_5yr_Java_AI.pdf` with how / why / alternatives. Canonical: `docs/ASSORTSMART_TAB_RESUME.md`.

## Impact Analytics — Platform

### Go/Gin HTTP edge (Wire, h2c, 10k peak RPS, Datadog)
**What:** Self-protecting multi-tenant edge without a reverse proxy.
**Why:** Compile-time DI, native h2c, nested timeouts, tracing at the process that serves peak RPS.
**Tradeoff:** You own body caps/SIGTERM drain vs inheriting nginx.
**Alt rejected:** Python monolith as the public edge; “just put it behind GFE/nginx and don’t think.”

### ClickHouse vs Postgres vs Snowflake (packet defense, PDF-honest)
**What:** 189s→12s on 250M; six ClickHouse rollup tables (product, store, attr at season and weekly grains).
**Why Postgres failed for planner pivots:** row store scans whole rows for multi-column GROUP BY; lock/IO.
**Why ClickHouse:** columnar + vectorized execution; only the pivot columns hit disk.
**Why not Snowflake/BQ for this UI:** interactive latency + cost of shared slots (BQ probes 1–20s+ MEASURED). Self-hosted CH matched the read pattern.
**Tradeoff:** CH is a poor keyed-UPDATE OLTP store — insert-only / ReplacingMergeTree, thin PG for roles.

### ifNotFinite KPI parser
**What:** Operator math → tokenized CH SQL fragments.
**Why:** KPI changes without deploys; NaN/Inf cannot poison rollups.
**Alt:** hard-coded SQL in releases.

### Firebase → JWT/OIDC waterfall + Redis + Postgres roles
**What:** UAM-scoped hierarchy; constant-time API keys.
**Why:** Multi-tenant bleed is a company-ending bug.
**Alt:** “trust the gateway header only.”

### 100% coverage / 1,200+ tests / SAST/SBOM
**What:** race+atomic CI gate.
**Why:** zero-regression on a 10k RPS edge.
**Honesty:** last committed profile may be 99.93% — say gate is 100%, last profile if asked.

## Impact Analytics — Agentic

### Deterministic KPI + 7 lenses vs LLM-only
**What:** 348k article-seasons; 88k/pass.
**Why:** Merch math must be auditable; LLM adds judgment, not the SoR.
**Alt:** free-form SQL tool.

### Air-gap LLM vs 2.11B fact + RMT two-phase
**What:** JSON payloads in; two-phase inserts; deterministic fallback.
**Why:** A hallucinated write on 2.11B rows is unrecoverable.
**Do not say:** you built Flink CDC on IA. `pg2ch_cdc` = Ashvin Sharma (DESIGN against, not authored).

### Ask Iris: Supervisor + Evaluator + frozen scopes
**What:** Shipped WebSocket copilot.
**Why:** Evaluator loop + socket-level freeze stop infinite loops and cross-tenant reads.
**Honesty:** shipped **capability**, no invented tenant SLA.

### 300-case / 80% gate vs 74% baseline
**What:** CI promotion gate.
**Why:** Free deterministic rule is the bar models must beat.
**Do not say:** all tenants live at ≥80%.

### Cluster Copilot / Hindsight
**Verbal only / not on PDF.** Do not list as resume bullets.

## Uber FRM
### Spring Boot / Spring Data JPA / Hibernate + 8-table SOADB + SHA-256 keys
**What:** 36 Spring Boot endpoints, 19M GL, L1–L4, optimistic locking.
**Why:** Sheets had no stable IDs or SOX-grade collaboration.
**PDF:** 70% from 14 days to 3; 100% coverage; SOX 50% delta-variance; led 3.

## Uber Menu
### Selenium → Kafka → Flink exactly-once + RAG/Milvus
**What:** 24h→2h, $600K, 30K+, 98% **offline**, 95%+.
**Backpressure (packet, Menu-only):** partition by vendor/tenant for ordering; Flink credit-based backpressure if CH/catalog sink slows — buffers fill, upstream Kafka consumption slows, avoid OOM.
**Spark:** not on PDF.

## Masters / GFG
Spring Boot strangler + Kafka/PG shard. GFG PHP→Django.\n