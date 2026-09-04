# PDF bullet + tech defense (study this)

**Purpose:** Defend **every line on the current PDF** — claim, why that tech, what you rejected, what you must not say.

**PDF name:** `Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf`  
Canonical metrics: [`docs/ASSORTSMART_TAB_RESUME.md`](../../docs/ASSORTSMART_TAB_RESUME.md) · packs: [`23a`](23a_ia_interview_pack.md) · [`23b`](23b_uber_interview_packs.md) · [`23c`](23c_masters_gfg_interview_packs.md) · ER/why: [`34_er_tables_tech_why.md`](34_er_tables_tech_why.md)

<div class="callout warn">
<b>Hard no.</b> Do not fuse Kafka+Flink (Menu) with ClickHouse (IA) into one pipeline.
Do not say payments / money movement. Do not say encryption or a privacy program.
Do not say sub-second ClickHouse pivots (the PDF is 189s→12s). Do not say zero message loss.
Exactly-once on Menu = idempotent catalog upserts + Flink keyed state — not 2PC across Gemini.
Exactly-once on Masters = idempotency keys vs IRP (at-least-once + unique key). IRP is outside your transaction.
300-case / ≥80% is a <b>CI promotion gate</b>, not all tenants live. Menu 98% is <b>offline eval</b>. Uber <b>via EPAM</b>. ANZ is <b>HISTORICAL Mobility</b>.
Cluster Copilot / Hindsight / Spark / Pinot / K8s-ops / CDC authorship = not PDF claims.
</div>

How to answer any tech: **where → failure mode → rejected alternative → PDF number → what dies if it fails.**

---

## A. Three Google-vocab rewrites (Sep 2026)

### 1. Menu — “large-scale data ingestion and processing pipeline”

**PDF:** Selenium 95%+; then Kafka + Apache Flink keyed dedupe / schema normalize; exactly-once catalog upserts.

| Probe | Answer |
|---|---|
| What is the pipeline? | Acquire (Selenium) → Kafka (`vendor_id`) → Flink keyed state (dedupe, schema) → catalog upsert **or** RAG/Gemini for unstructured PDFs |
| Why Kafka? | Scrapers must not block on catalog; replay after a bad parser; multiple consumers |
| Why Flink, not Spark on the hot path? | Burst scrapes, per-vendor keyed state, event-time for late pages. Spark = verbal backfill only, **not on PDF** |
| Why not ClickHouse here? | ClickHouse is **IA analytics**. Menu land is catalog + Milvus for RAG |
| Exactly-once? | Idempotent upsert on catalog keys + Flink checkpoints. Not 2PC to Gemini or partner sites |
| Scale words | 30K+ menus/month is the PDF volume — do **not** say hundreds of millions of **transactions** |

### 2. Masters — “high-concurrency” / “idempotent” / “fault-tolerant state”

**PDF:** Kafka + PostgreSQL quarter-shard; 1M+ daily IRP submissions; 100K+ concurrent imports; idempotency + DLQ + bounded retries.

| Probe | Answer |
|---|---|
| High-concurrency of what? | Bulk **import workers** hitting IRP, not Google Pay money movement |
| Idempotency key? | `client + fileHash + batchIndex` (+ invoice refs). Unique constraint so replay cannot double-register |
| Fault-tolerant state? | In-flight Kafka offsets + PG job rows + DLQ for poison batches. Not a custom consensus store |
| Why Kafka? | Per-GSTIN order, durable replay for GST disputes, independent consumer groups |
| Why PG quarter shards? | GST returns are quarter-scoped; hot writes stay in current quarter |
| Stack on **this** PDF | **Spring Boot** (hybrid / Java). PyGo PDF = FastAPI. Never say Go for Masters |

### 3. IA — “multi-tenant data isolation” / “access control” / PG + ClickHouse

**PDF:** Isolation + UAM across PostgreSQL and ClickHouse; Redis-fronted Firebase Admin → JWT / Google OIDC; constant-time API keys; Postgres roles.

| Probe | Answer |
|---|---|
| Isolation vs encryption? | **Access control + tenant scope**, not an encryption product. Do not say you implemented encryption-at-rest |
| Why both PG and CH? | PG = identity / UAM / roles (ACID). CH = planner facts / pivots (columnar). Same tenant id on both; CH queries run under frozen tenant scope |
| Why not Milvus here? | Milvus is **Menu RAG**, not IA governance |
| Cache miss? | Redis miss falls through to Postgres — it does **not** degrade open |
| UAM? | Hierarchy intersects store/product scope. You did not build a generic RBAC product |

---

## B. Every PDF bullet (this track)

### Summary

| # | Claim | Defend | Do not say |
|---|---|---|---|
| S1 | 5 years; cloud-native high-throughput **distributed systems** | Tenure + IA 10k RPS + Masters/FRM services | Staff/principal |
| S2 | **Java, Python and Go** microservices; **AI-assisted** + **RAG** | Java=FRM/Masters; Go=IA edge; Python=IA agents + Menu RAG | All three languages on every project |
| S3 | Shipping, migrations, reliability | Masters strangler; FRM Sheets→MySQL; Menu 24h→2h | “I ran Uber production” — **via EPAM** |

### Skills (why the row exists)

| Row | Why on PDF | Rejected / trap |
|---|---|---|
| Languages | Java (FRM/Masters), Python (agents/Menu/GFG), Go (IA edge), SQL everywhere | Do not claim Rust/C++ production ownership |
| Backend | Spring (history), FastAPI/Gin/Django where the PDF says | Do not put Spring on IA on **this** hybrid PDF |
| AI | LangGraph/LangChain/RAG/Milvus/pgvector/Tool Calling/MCP/Prompt Eng/LangSmith/offline eval | MCP is **skills literacy**; not an IA PDF bullet |
| Data & streaming | Kafka+Flink = **Menu**; ClickHouse+BQ = **IA**; ETL = Masters/FRM | No Flink-on-IA, no Spark-on-PDF |
| Databases | PG/MySQL/Redis/Mongo/ES/Dynamo/S3 as used | Dynamo = literacy / AWS history, not IA SoR |
| Cloud | GCP (IA, Menu), AWS (Masters), Docker, K8s **literacy**, Maven/Bazel (FRM) | K8s ≠ you operated clusters |
| Architecture | HLD/LLD, DSA, caching, reliability, multithreading, sharding, concurrency, idempotency | Idempotency story = Masters (+ Menu upserts) |

### IA — Platform

| # | Claim | Why this tech | Rejected |
|---|---|---|---|
| P1 | Go/Gin 10k peak RPS, Wire, h2c, no reverse proxy, Datadog | Compile-time DI; process owns timeouts/h2c; traces at the edge | Python public edge; nginx as the only timeout story |
| P2 | 15.5×; 189s→12s / 250M; 1.6M article-seasons; 2.4B weekly rollups | Columnar CH for planner pivots | PG OLAP; Snowflake cost/latency for this UI; **sub-second** (false) |
| P3 | Dynamic KPI configurator; ifNotFinite SQL fragments | Operators change math without deploys; NaN must not poison rollups | Hard-coded SQL in Go |
| P4 | Isolation + UAM on **PG + CH**; OIDC waterfall; API keys | Tenant bleed is a career-ending bug | Encryption product; Milvus; “privacy program” |
| P5 | 100% statement coverage, race+atomic, 1200+ tests, SAST/SBOM | Zero-regression on a multi-tenant edge | Claiming the same gate for Python agents |

### IA — Agentic

| # | Claim | Why this tech | Rejected |
|---|---|---|---|
| A1 | Keep/Drop + Missed Opp + Top Style; 335K+; 88k/<$100; 7 lenses | Mix deterministic KPI math + structured LLM; named pipelines not a chatbot | One giant prompt |
| A2 | 2.11B fact; air-gap LLM vs DB; RMT two-phase; JSON; fallback | Hallucinated SQL must not write 2.11B rows | LLM-issued CH writes; you authored CDC |
| A3 | Resilient AI orchestration registry; breakers; checkpoints; LangSmith | Batch LLM must pause/resume and show token cost | Ad-hoc scripts; one APM for agents and HTTP |
| A4 | Shipped Ask Iris; WebSocket; Supervisor+Evaluator; frozen scopes | Interactive KPI/charts without unfreezing warehouse or looping | Tenant-wide SLA; questions/week |
| A5 | 300-case / ≥80% CI gate vs 74% baseline | Models must beat a **free** deterministic baseline | “All tenants live at 80%” |
| Tech | Go, Gin, Python, FastAPI, LangGraph, CH, BQ, Redis, PG, Datadog, LangSmith, GCP, Docker | Split: Go edge vs Python graph vs CH facts | Kafka/Flink on this line |

### Uber FRM (via EPAM) — Spring on this PDF

| # | Claim | Why | Rejected |
|---|---|---|---|
| F1 | 70% recon 14d→3d; $340M; 19M GL; 36 Spring Boot endpoints; L1–L4 | Automate Sheets math into MySQL; PwC work papers | Inventing you were an Uber FTE |
| F2 | 8-table SOADB; optimistic lock; SHA-256 natural keys; atomic syncs | Close-week lock contention; no duplicate audit rows | Pessimistic lock everywhere |
| F3 | Led 3; JPA/Hibernate 100% coverage; Bazel; SQL allowlists; SOX 50% delta-variance | SOX needs explainable SQL and coverage | Skipping allowlists |
| Tech | Java, Spring Boot, Spring Data JPA, Hibernate, MySQL, JUnit, Bazel, Docker | Uber JVM standard | FastAPI on **this** FRM line |

### Uber Menu + ANZ

| # | Claim | Why | Rejected |
|---|---|---|---|
| M1 | 24h→2h; $600K; 30K+/mo; 98% Gemini+LangChain RAG+Milvus | Unstructured PDFs need retrieve→generate→schema gate | 98% as **online** prod SLA |
| M2 | 95%+ Selenium; **Kafka+Flink ingestion/processing**; exactly-once upserts | See section A.1 | ClickHouse on Menu; Spark on PDF; zero message loss |
| ANZ | 99.9% Mobility docs; 20h/week | Deterministic validation vs local authorities | Calling it Eats; claiming Selenium/RAG here |
| Tech | Python, Selenium, Kafka, Flink, LangChain, Gemini, RAG, Milvus, GCP, Docker | Acquire vs bus vs RAG vs catalog | Mixing Masters Kafka into this story |

### Masters GST — Spring on this PDF

| # | Claim | Why | Rejected |
|---|---|---|---|
| G1 | p95 1.2s→300ms; 1500+ clients; PHP→Spring Boot; 700→4000 rpm; mentored 2 | Strangler/canary; async IRP so workers do not pin | Big-bang rewrite |
| G2 | High-concurrency Kafka+PG quarter shard; 1M+/day; 100K+ idempotent imports; DLQ | See section A.2 | Payments; Go; Flink |
| G3 | ELK+New Relic; triage −70%; Redis −30% reads; 35%→82% coverage; 98% deploy | Request-ID across API/consumer; cache hot GSTIN | Invented SEV commander title |
| Tech | Java, Spring Boot, Hibernate, Kafka, PG, Mongo, Redis, ES, Docker, ELK, New Relic, AWS | JVM ATS track | FastAPI on **this** PDF |

### GFG

| # | Claim | Why | Rejected |
|---|---|---|---|
| Title | Courses Platform and Influencer Dashboard | Two products under one role | Inventing a third GFG product |
| C1 | Django; 10K+ queries; 10x contest; MySQL/Mongo/Redis/ES; 20% premium | Contest spikes; vote/pin/lock APIs | Claiming Kafka here |
| C2 | Influencer dashboard; 30% course sales; 70% ops via async jobs | Affiliate coupons + video/reminder crons | Claiming Flink/CH |

### Education / Achievements

B.Tech IT, IET Lucknow (2017–2021). Code Jam 2260/37k; SIH 2020 top-3 nationally; EPAM Global AI Hackathon; HackerRank + LangChain certs (links on PDF). Do not inflate ranks.

---

## C. “Why this tech?” cheat card

| Tech | Home | Because | Not because |
|---|---|---|---|
| **Go/Gin** | IA edge | 10k RPS, Wire, h2c in-process | “Go is faster” as a slogan |
| **Python/FastAPI/LangGraph** | IA agents, Ask Iris | Graph + typed steps + WS copilot | Replacing the Go edge |
| **ClickHouse** | IA facts/pivots | Columnar 250M-row grids | OLTP mutations; Menu ingest |
| **PostgreSQL** | IA roles; Masters shards | ACID identity / quarter GST tables | Planner cube store |
| **Redis** | IA auth cache; Masters GSTIN | Stampede/TTL; not source of truth | “We used Redis so we are scaled” |
| **Kafka** | Menu ingest; Masters IRP | Replay + ordering + fan-out | One bus across all companies |
| **Flink** | Menu only | Keyed dedupe / event-time | IA; Masters; Spark-on-PDF |
| **Milvus + Gemini + LangChain** | Menu unstructured | Retrieve similar menus → generate → schema gate | IA privacy store |
| **Spring Boot / JPA / Hibernate** | FRM + Masters (this PDF) | Uber/Masters JVM | IA on this hybrid PDF |
| **MySQL** | FRM SOADB | Existing Uber store; optimistic lock | ClickHouse for GL |
| **Bazel / JUnit** | FRM | Uber release graph; SOX coverage | Claiming Bazel at IA |
| **Firebase / OIDC / JWT** | IA | Tenant IdP waterfall | Homegrown auth |
| **Datadog vs LangSmith** | IA HTTP vs agent | Different questions | One tool for both |
| **Docker** | everywhere | Reproducible deploys | “I ran prod K8s” |
| **GCP vs AWS** | IA+Menu vs Masters | Where the workload lived | Multi-cloud hero story |
| **Django** | GFG | Fast product APIs on existing Python | Spring at GFG |

---

## D. 30-second traps

1. “You built a data platform with Kafka, Flink, **and** ClickHouse.” → **Two jobs.** Menu stream vs IA OLAP.  
2. “So you did payments.” → **GST IRP + FRM recon**, not money movement.  
3. “Encryption and privacy.” → **Isolation + SOX + ANZ docs.** No encryption bullet.  
4. “Sub-second analytics.” → **12s** pivot after 189s. Masters **300ms** is an **API p95**, not CH.  
5. “Is Ask Iris GA for every tenant?” → **Shipped capability**; ≥80% is a **gate**.
