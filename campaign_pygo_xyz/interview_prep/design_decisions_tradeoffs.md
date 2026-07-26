# Design Decisions and Tradeoffs (resume-aligned)

Every major decision on the campaign resume with how / why / what / alternatives.

## Impact Analytics

### Planner copilot on FastAPI + LangGraph + MCP with Go doing layer
**What:** Chat agent plans tool calls. Deterministic Go engines execute clustering/hindsight/strategy.
**Why:** LLMs are good at intent and narration, bad at correct merch math. Shared Go layer keeps Manual UI and Agent on one auth surface.
**Tradeoff:** Two runtimes (Python + Go) vs one. Chose correctness and reuse over language purity.
**Alt rejected:** Giving the LLM a raw SQL shell. Pure Python rewrite of merch engines.

### 14 audited read tools + 3 human confirm gates
**What:** Agent tools only **read** planning data. Writes go through human gates then product write-back APIs.
**Why:** Measured failures were mostly input-boundary mistakes. Buy decisions move real money.
**Say in interview:** Do not say "never writes SQL" as a slogan. Say tools are read-scoped and writes are gated.
**Tradeoff:** Slower full autonomy vs auditability.

### Hindsight prior-season decision layer
**What:** Carry-forward / underperformance flags (FR-6.1), Keep/Shop/Drop on item grid (FR-16.5), scorecard + contribution, overnight narration grounded in metrics (FR-8.1), tenant catalogs without code deploy (FR-1.3).
**Why:** First stage of planning pipeline — next-season buys need last-season evidence.
**Safety:** Narration number-checked before save; visuals deterministic (FR-9.1); permission-scoped filters (FR-0.1).
**Defense file:** `projects/01b_hindsight_defense.md`

### Choice-cluster-week aggregates (~25M) for interactive edits
**What:** Editable plan grain stays aggregate so cell edits ~0.4 ms and month rollups stay sub-second (MEASURED on aggregate path).
**Why:** Flat store-week grids are not interactive for planners.
**Honesty:** Do **not** put projected 12B on the PDF. If asked verbally, 12B is a projected flat explosion used in internal benchmarks, not a shipped table size claim.

### Per-tenant ClickHouse (63 tables / 8 layers)
**What:** Append-only planning store after pivot POC 250M 189s→12.3s (~15.5×).
**Why:** Shared BigQuery probe variance 1–20s+ kills agent UX.
**Kafka on IA tech line:** Product uses Kafka for async embedding jobs (playbook). Planning-store ingest remains batch ELT. Be precise in interview.

## Uber FRM
### FastAPI + MySQL SSOT replacing Sheets
**What:** 8 screens, 30+ APIs, HFM↔10-Q recon as durable MySQL SoR for PwC.
**Why:** Sheets had no stable line IDs, history, or real-time collaboration for audit.
**Removed from PDF:** “11-table” and “18-file migration” wording — keep as verbal depth.
### Group/component/residual/EMI auto-flag
**What:** Auto-flag material FSLIs/entities vs $340M materiality and $170M residual (Q4 2025 sample), 55 lines / 14 entities.
**Why:** Scoping correctness is the SOX-style control PwC consumes.
### Leadership + 1,100+ tests
**What:** Led 3 via design reviews/API contracts/CI; Bazel pytest suite ~1,100+.
**Honesty:** 70% recon cut is TARGET. Do not claim collab-service ownership.

## Uber Menu
### Selenium + Kafka ingest bus + RAG/Gemini
Scrapers on GCP cut 24h→2h and $600K+/yr on 30K+ menus/month. Kafka holds replayable ordered scrape events before downstream extract/catalog write-back (HISTORICAL streaming path from prior resume materials / prep). RAG + Gemini + SFT for unstructured menus (98%/100% offline).
**Flink:** On Menu PDF (hot-path normalize/dedupe after Kafka). **Spark:** Study/verbal backfill only unless a JD needs it on the PDF.

## Masters India
### PHP → FastAPI strangler + Kafka IRP + on-call
p95 1.2s→300ms, 1500+ clients, mentored 2. Kafka + PG quarter shard for 1M+/day and 700→4000 req/min. Idempotency/DLQ. ELK/New Relic triage −70%.

## GeeksforGeeks
### PHP → Django
10K+ daily queries, 10× contest spikes, voting/pinning, influencer analytics.
