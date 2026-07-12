---

# 8. Authoritative product specifics (NotebookLM — requirements notebook)

<div class="stage-badge stage-obs">Source: NotebookLM "AssortSmart Agentic Store Clustering & Module Requirements" (117 sources) · verified July 2026</div>

These are the **canonical product/engineering facts** straight from the requirements notebook — use them verbatim in interviews; they extend/confirm §3–§5. Where they differ from the offline PoC, prefer these for "what the product is," and keep the PoC framing (mock timings) for "what I personally ran."

## 8.1 Agents & orchestration
- **Five specialist agents:** `AssortmentDataAgent`, `ClusteringAgent`, `HindsightAgent`, `LinePlanAgent`, `RecommendationAgent`.
- **Orchestration:** **LangGraph** for multi-agent reasoning with **Planner → Executor → Solver** nodes, paired with **FastMCP (Model Context Protocol)** to **discover and execute tools safely**. (This is the production orchestration; the offline `agentic_assort_multiagent` PoC is a deterministic re-implementation of the same router/planner/executor shape.)
- **MCP tool layer** (`mcp-core`) is how agents call tools — worth naming: "agents don't hard-code integrations; they discover tools over MCP."

## 8.2 Governed autonomy (concrete thresholds)
- **High confidence 0.85–1.00** → auto-approve and proceed.
- **Medium 0.65–0.84** → proceed but **flag for planner review**.
- **Low 0.00–0.64** → **halt the pipeline and escalate** to a human planner.
- **HITL consent gate:** for highly consequential/destructive actions, the graph **interrupts** to request explicit confirmation.
- **Overrides:** require a **≥10-character reason code**, permanently written to the **audit trail**.

> Interview gold: "Autonomy is a banded policy — ≥0.85 auto, 0.65–0.84 act-and-flag, <0.65 halt-and-escalate — plus a hard consent gate on destructive actions and a mandatory reason code on every override."

## 8.3 Tech stack (as stated)
- **Backend:** Python **3.11–3.13**, **FastAPI**, **Uvicorn** (ASGI).
- **LLMs (multi-provider):** OpenAI **GPT-4.1 / GPT-4o / o4-mini**, Google **Gemini**, Anthropic **Claude**, **xAI**.
- **Databases:** **BigQuery** (historical facts/cubes) · **PostgreSQL** (editable transactional store) · **DuckDB** (in-memory pivot accelerator) · **ClickHouse** (`ReplacingMergeTree`, insert-only versioned OLAP/planning).
- **Memory / vector:** **Redis**, **Neo4j / Memgraph** (graph), and vector stores **pgvector / Qdrant / Chroma / FAISS**.
- **Streaming/messaging + Apache:** **Socket.IO (WebSockets) + SSE** (real-time); **Google Cloud Tasks + GCP Pub/Sub** (async queues); **Apache Parquet** (storage format); **Apache Kafka** (`aiokafka` / `confluent-kafka`) for **async embedding jobs**.

<div class="callout note">
<b>Correction to earlier "no Apache" caveat.</b> The product <b>does</b> use Apache tech — <b>Kafka</b> (async embedding jobs) and <b>Parquet</b> (columnar storage/interchange). What's still true: the planning-store *ingestion path* is batch ELT (BigQuery cube/rollup → Postgres/ClickHouse), not a streaming pipeline into the grid.
</div>

## 8.4 Database model & ClickHouse (as stated)
- **Tenant unification:** a **generic core with "flex fields"** absorbs each retailer's dynamic hierarchy **without schema changes**; **tenant isolation resolves via environment variables to separate schemas**, with **shared master tables + extension hooks** for per-client customization. (This is the mechanism behind "same codebase/queries/procedures across tenants.")
- **ClickHouse engines:** `ReplacingMergeTree` (upserts/latest-wins), `AggregatingMergeTree` (rollups), **`VersionedCollapsingMergeTree`** (out-of-order CDC). **Partition** `PARTITION BY toYYYYMM(week_date)`; **`ORDER BY (measure, hierarchy…)`** to exploit **sparse-index granule skipping**. **Production:** **`ReplicatedReplacingMergeTree` + sharding** (ClickHouse Keeper, or physical **L1-table sharding to eliminate hotspots**) and **Projections** for optimized rollups.
- **Edit / undo mechanics:** `ALTER UPDATE` mutations are **forbidden**; edits **insert new version rows** (ms-epoch); latest state read via **`FINAL`** or **`argMax(value, version) … GROUP BY key`**. **Up to 10 undo steps are cached in Redis** before async DB commit; **version-diffs render as dual-value cells**.
- **Store-clustering model:** **K-Means**, run **twice independently** — **Performance (numeric)** and **Product/attribute (alphabetic)** — then **intersected into composite grades like "A1"**, stored in **EAV tables**.

## 8.5 PoC gating + benchmark numbers (as stated)
- **Gate:** **sub-second UI responsiveness over 250M synthetic rows.**
- **Result:** ClickHouse **meets it** — **8–130 ms filtered pivot reads**, **~160 ms flat-scale writes** — a **~140×–200× speedup over the legacy Postgres flat schemas.**

<div class="callout warn">
<b>How to cite these numbers honestly.</b> They are the <b>ClickHouse PoC benchmark documented in the requirements notebook</b> (250M synthetic rows). Say <b>"the ClickHouse PoC achieved 8–130 ms pivot reads and ~140–200× over the legacy Postgres flat schema on 250M rows"</b> — i.e. a <i>PoC benchmark result</i>, not a production SLA and not necessarily your personal measurement. It's stronger and safer than the offline `db_architecture_poc` mock ms; use these for the DB-performance story and keep <code>mutations_used = 0</code> as the correctness property you personally proved.
</div>

## 8.6 Official Confluence docs — audited, zero contradictions (July 2026)

The full internal **AssortSmart Docs** Confluence space (~480 pages: API validation docs, module HLDs/LLDs, modular flows, business workflows) was walked in three passes and reconciled against everything above. **No contradictions were found** — an interview-grade credibility point: *"every engine behaviour I derived from code and live traffic matched the official validation docs."* Facts worth quoting:

- **Architecture is officially four-layer** (`controller → service → data → data/query`, requests flow downward only), five modules — four in `assort_smart`, Cluster in its own `cluster_smart` package; async work via Cloud Tasks (Line-arch generation is a **3-stage fan-out**; edits propagate via a background worker).
- **The clustering spec confirms the composite-grade design** (attribute letters × performance numbers, user k-override band 2–8) and its versioning model is **copy-then-edit** — a cluster plan bound to an active strategy is immutable.
- **The scale rationale is documented, not folklore:** the Line table design budgeted **~468 M store-week rows** per worst-case tenant, which drove JSONB packing, ~2,000 LIST partitions and queue-based store-week updates — useful when defending the "per-row synchronous UPDATEs deviate from the module's own design" finding.
- **The C&A tenant already shipped the fix family I recommend** (BQ rollup tables, $3.8 → $0.30 per calc-attributes request, ~6× latency) — independent confirmation of the rollup strategy in §6.1's cost story.

## 8.7 Résumé bullets these unlock (add to §2)
- **"Orchestrated a 5-agent LangGraph pipeline (Planner→Executor→Solver) with a FastMCP tool layer, and a banded autonomy policy (auto ≥0.85 / act-and-flag 0.65–0.84 / halt <0.65) plus a human-in-the-loop consent gate + audited reason codes."**
- **"Proved ClickHouse as an insert-only/versioned planning store — sub-second pivots over 250M rows (8–130 ms reads, ~160 ms writes), ~140–200× over the legacy Postgres flat schema — using ReplacingMergeTree + argMax(version), Redis-cached 10-step undo, and REPLACE PARTITION bulk re-seeds (zero mutations)."**
- **"Designed a tenant-generic 'flex-field' core (env-var schema isolation + shared masters + extension hooks) so one codebase serves every retailer's hierarchy with no per-client schema."**
- **"Implemented composite store grades (A1/A2/…) by intersecting independent K-Means runs on performance (numeric) and attribute (alphabetic) features, persisted via an EAV model."**
