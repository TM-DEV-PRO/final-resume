# Impact Analytics — Agentic Assort Planner & Store-Clustering Copilot

**Role:** Senior Software Engineer · June 2026 – Present · Bangalore
**Resume header tech:** Python (FastAPI, LangGraph, MCP) · Go (Gin) · Rust (Axum) · ClickHouse (insert-only versioned, end-to-end) · BigQuery · pgvector · Redis · Kafka · GCP

> **This file is the index.** The full playbook for this project — every bullet's backing block, HLD/LLD, DB design, tech deep dives, Q&A bank, honesty tiers — lives in `../agentic_assort_playbook/` (§0–§10). Read that end-to-end before interviews. This file gives you the narrative spine and the July 2026 stack update in one place.

---

## 1. Elevator pitch (30 seconds)

"I work on the agentic rebuild of AssortSmart — a merchandise planning SaaS where enterprise retailers decide what products to buy, in what quantities, for which stores, a season ahead. The shift we're building: AI agents draft the plan — store clusters, assortment scenarios — and planners review, override, and approve, instead of configuring everything by hand. Architecturally it's one Python agentic microservice (FastAPI, LangGraph, MCP) that runs all agentic workflows, and a Go core backend — Gin microservices exposing the REST APIs for plan lifecycle, reference data, and bulk saves. In the agent tier I own the store-clustering agent: it selects features by statistical significance, optimizes cluster count with silhouette scoring, and presents 3 to 5 distinct ranked scenarios with plain-English rationale for planner approval — turnaround goes from days to under an hour. Under both sits ClickHouse with an append-only versioned write model where every planner override is an insert — which gives us version diff, undo/redo, and an immutable audit trail for free — plus the pivot-grid serving layer with sub-500 ms rollups and 80 ms optimistic cell edits."

## 2. The resume project (one block: Agentic AssortSmart)

The resume shows **one project** under Impact Analytics with five bullets. Sources: the **Agentic Store Clustering HLR v1.1**, the **Planning Platform Architecture v5 deck**, and the **Hindsight Module FRD** (copies in `../source_docs/`), plus the playbook.

| Resume bullet | What it covers | Where the defense lives |
|---|---|---|
| Platform intro (agents draft, planners approve) | What AssortSmart does for retailers and why the agentic rebuild exists | §3d below; Architecture deck slides 1–2 |
| Python agentic microservice (all agentic workflows) + clustering agent (3–5 scenarios, <1 h) | ONE agentic service owns every agentic workflow; the clustering agent is its flagship: autonomous feature selection, k optimization, multi-scenario compare, approval gating | §3d below; HLR-AG-001…006, HLR-SC-001…004 |
| Go (Gin) core backend microservices | The main backend: REST APIs for everything non-agentic | §3b below; playbook **§10** |
| ClickHouse append-only versioned store | Every override is an insert; version diff / undo-redo / audit trail | playbook §2 D2, §4, **§10** |
| Pivot grid serving layer + per-tenant config in PostgreSQL | <500 ms rollup/drill-down, <80 ms optimistic edits, config-driven tenant onboarding | §3e below; Architecture deck ARCH-06, NFR-01, ENG-01 |

**The service split, one line (say it exactly like this):** "One Python microservice (FastAPI, LangGraph, MCP) runs all agentic workflows — the agents, their tools, LLM orchestration. The core backend is Go: Gin microservices exposing the REST APIs for plan lifecycle, reference data, and bulk saves. The two talk over versioned API contracts, and the split lands on a natural deployment boundary — the agent tier scales with LLM latency, the Go tier scales with request volume."

## 3. The stack story you must tell in order (July 2026 direction)

This is the single most senior narrative you own. Tell it as an *evolution*, not a static choice:

1. **Live audit said "no ClickHouse"** for the legacy backend — and it was right: the legacy planner mutates in place (keyed UPDATEs, jsonb-merge, delete+reinsert), which ClickHouse mutations are genuinely bad at (async queue, degrades >500, stalls >1,000).
2. **I authored the reconciled verdict**: the objection is a property of the *write model*, not the engine. Made ClickHouse a *gated option* behind a versioned-write PoC.
3. **The PoC passed the gate**: insert-only/versioned semantics — `ReplacingMergeTree(version)`, `argMax(value, version)` reads, tombstone deletes, atomic `REPLACE PARTITION` re-seeds — hold `mutations_used = 0` at 1× and 10× with correct read-after-write.
4. **July 2026: the org committed** — ClickHouse end-to-end for both transactional and analytical planning workloads; Go (Gin) for all non-agentic flows; Rust (Axum) only for profile-proven hot paths; the Python/LangGraph agent tier unchanged.

**Precision on "transactional":** it's planning-grid transactionality — atomic batch inserts of one version, session read-after-write via version watermarks, idempotent replays, audit history for free — *not* bank-ledger OLTP. Cross-entity invariants that need true multi-statement ACID (auth, tenant config, workflow state) stay on a thin Postgres metadata plane. Say this unprompted; it shows judgment.

**Go vs Rust discipline:** "Go by default, Rust by measurement — an endpoint earns Rust with a profile, not a preference." Gin chosen over chi/Echo/fiber for maturity + team familiarity (fiber rejected: fasthttp breaks `net/http` semantics). Rust precedent exists in-house (CortexEye backend is Rust/Axum). *(Rust is deliberately not on the resume — if asked about the stack, mention it as the escape hatch, don't claim Rust delivery.)*

## 3b. The Go services — what you actually build (defend the Go bullet)

The resume says: *"Building the core backend as Go (Gin) microservices exposing REST APIs for plan lifecycle, tenant configuration, and bulk saves, with JWT auth middleware, goroutine worker pools for concurrent writes, and context based timeouts."* Here is the concrete shape behind each phrase:

- **Plan lifecycle APIs** — create/copy/finalize/soft-delete plan endpoints; state transitions validated server-side (draft → in-review → finalized); finalize is a human signature, so the handler enforces role + confirmation token.
- **Reference data APIs** — hierarchy trees, fiscal calendars, store masters, tenant config. Read-heavy fan-out: handler issues concurrent ClickHouse/Postgres reads with `errgroup.WithContext`, returns partial-safe composites.
- **Bulk save APIs** — the versioned write path: a grid save arrives as a batch of cell edits; the service assigns one `version = epoch-ms` to the batch, validates rows (Gin `ShouldBindJSON` + validator tags), and a **goroutine worker pool** (bounded channel, N workers) fans batched inserts into ClickHouse via `clickhouse-go` v2 native-protocol batch inserts. Idempotency: batch id + content hash so retries don't double-insert versions.
- **Middleware chain** — JWT auth (tenant + role claims), request-scoped logging with correlation IDs, request validation, panic recovery, per-route rate limits. Standard Gin `c.Next()` chain.
- **Context discipline** — every handler derives `context.WithTimeout`; DB calls take the ctx; slow ClickHouse probes get cancelled instead of piling up. Graceful shutdown drains in-flight requests (`server.Shutdown(ctx)`).
- **Testing** — table-driven tests, `httptest` for handlers, interface-mocked repositories; `golangci-lint` in CI.
- **Why Go here (say it like a Go dev):** "This tier is straightforward request/response work at volume — bind, validate, authorize, fan out I/O, return. Goroutines give me cheap per-request concurrency without an async framework, the binary deploys as a single static artifact, and the code stays boring enough that anyone on the team can touch it."

## 3d. The clustering module — defend the scenarios bullet (HLR v1.1)

**What the product does (say this first, plainly):** AssortSmart is how a retail chain decides, months before a season, what products go into which stores and in what depth. Step one is always **store clustering** — grouping hundreds of stores into a handful of clusters that shop alike, so the assortment can differ per cluster instead of being one-size-fits-all. Today that clustering is manual: a planner picks KPIs off a significance table, sets a cluster-count range, runs once, takes what they get. The agentic module inverts it:

- **Autonomous feature selection (HLR-AG-001):** the agent picks the feature set and weights per scenario from statistical significance; the significance table becomes a read-only transparency panel, not a manual picker. The manual path stays available as a legacy option per client.
- **Autonomous k optimization (HLR-AG-002):** elbow method + silhouette scoring pick the cluster count per scenario; client-configured min/max bounds remain as guardrails the agent cannot exceed; all tested k values and scores are visible to the planner.
- **Multi-scenario comparison (HLR-AG-003, HLR-SC-001):** instead of one result, the agent presents **3–5 distinct ranked scenarios** (cap is a hard constraint; distinctness is mandatory; a baseline scenario mimicking the client's legacy configuration is always included), each with a composite score, cluster composition, and a plain-English narrative.
- **Approval gating (HLR-AG-004…006):** nothing finalizes without planner approval; outlier stores are surfaced and handled explicitly; clustering scope can be submitted in parallel across categories.
- **The turnaround claim (<1 h from days):** comes from the copilot FRD baseline work — measured 8.5% run failures and one configuration tried per plan in the legacy flow. The agent explores many configurations internally but *presents* 3–5 (that's the HLR constraint — don't confuse the two numbers).
- **Child cluster cap (HLR-SC-004):** default 10, configurable per client.

## 3e. The planning grid backend (defend the grid bullet)

The resume says: *"Designing the backend for the planning grid, an Excel like pivot surface where planners edit plans across product, store, and week hierarchies, serving rollups and drill downs from pre aggregated ClickHouse data at p95 under 500ms and cell edits under 80ms via async write back."*

**If asked "what is the planning grid?" — the plain answer:** it's the main working screen of the product, and it behaves like a giant Excel pivot table. Rows might be product categories, columns weeks, and each cell a number like planned sales or buy quantity. A planner can re-pivot it (swap product for store on the rows), drill from department down to subclass, and edit any cell. The difference from Excel: every cell shows both what the AI recommended and what the planner decided, every edit needs a reason, and everything rolls up correctly through the hierarchy. From the Planning Platform Architecture deck (ARCH-06, NFR-01, GRID-*):
- **The latency targets (design targets, own them as such):** rollup/drill-down **< 500 ms** because reads hit a pre-aggregated cube layer, never the transactional store; cell edits feel instant (**< 80 ms**) because writes go to a per-user view store first and cube invalidation + DB commit happen async ("optimistic write-back"). Stale-data warnings compare source commit timestamps against the view's saved-at.
- **Where ClickHouse fits:** the append-only versioned planning store is what makes the grid's version diff, undo/redo (50-deep stack), scenario copies (up to 5 per plan), and immutable audit trail cheap — every override is an insert with a version, never a mutation.
- **Per-tenant configuration in PostgreSQL:** which planning stages a retailer runs, stage sequence and skip rules, approval thresholds, metric catalogs, hierarchy names/levels — all tenant config, not code. Config edits deploy by config sync in minutes with schema validation, no code deployment (deck ENG-01; Hindsight FRD FR-1.3: tenant onboarding config applies without deployment). That is what "onboards retailers without code deployment" means.
- **The fixed-core principle (great senior talking point):** planning algorithms are Layer 1 — universal, never forked per retailer. Retailer differences live in Layer 2 config and Layer 3 isolated extension containers. A retailer requirement that would change core science becomes a platform roadmap item, never a fork.

## 3c. The BigQuery→ClickHouse ingestion pipeline (background — NOT a resume bullet anymore)

Be precise about what the BigQuery relationship is: **we don't build in BigQuery — it's the upstream historical source of truth, and I own the lane that ingests from it into ClickHouse.**

- **Flow:** scheduled exports of the needed fact/dimension slices from BigQuery → staging tables in ClickHouse → atomic `REPLACE PARTITION` promotion (no half-visible loads).
- **Nightly precompute:** attribute significance and top candidate sets for hierarchies with active plans, so ≥80% of copilot sessions start warm.
- **Reconciliation:** per-partition row-count and sum checks against the BigQuery source, 0.1% tolerance; a freshness sentinel stamps *data-as-of* into every agent recommendation so derived-data rot is visible, not silent.
- **Why this design:** agent probes need deterministic low latency (p95 <500 ms design target) and BigQuery's shared-slot variance (1–20 s) can't give that; a derived copy can rot, so the pipeline owns freshness + reconciliation as first-class features.

## 4. Architecture in one diagram

```
                        ┌────────────────────────────────┐
                        │   React planning workspace     │
                        │  (Signals / Pipeline / Log /   │
                        │   Ask / pivot grid)            │
                        └───────┬──────────────┬─────────┘
                                │              │
                 REST/SSE       │              │  chat / copilot
                                ▼              ▼
   ┌────────────────────────────────┐  ┌─────────────────────────────┐
   │  Non-agentic services — Go/Gin │  │  Agent tier — Python        │
   │  plan lifecycle CRUD, refdata, │  │  FastAPI · LangGraph        │
   │  scoping, write-back, tenant   │  │  Planner→Executor→Solver    │
   │  config  (hot paths: Rust/Axum)│  │  FastMCP tool discovery     │
   └───────────────┬────────────────┘  └──────────────┬──────────────┘
                   │                                   │
                   │   reads+versioned writes          │ deterministic tools
                   ▼                                   ▼
   ┌─────────────────────────────────────────────────────────────────┐
   │        ClickHouse — end-to-end planning store                   │
   │  insert-only versioned (ReplacingMergeTree · argMax · tombstones│
   │  · REPLACE PARTITION)  +  dedicated agent read plane            │
   └───────────────────────────────▲─────────────────────────────────┘
                                   │ proven BQ→CH ingestion lane
   ┌───────────────────────────────┴───────────────┐  ┌──────────────┐
   │  BigQuery — upstream historical source of     │  │ Postgres     │
   │  truth (we ingest FROM it; we don't build in  │  │ metadata/auth│
   │  it) — nightly precompute + reconciliation    │  │ + pgvector   │
   └───────────────────────────────────────────────┘  └──────────────┘
```

## 5. Every resume bullet → where its defense lives

| Bullet | Claim tier | Defense |
|---|---|---|
| Platform intro (agents draft, planners approve) | Product description — safe, no metric to defend | §3d; Architecture deck slides 1–2 |
| Clustering module: significance-based features, silhouette k, 3–5 ranked scenarios | **HLR-committed behavior** (v1.1, in build) — say "the module in build, spec'd in our HLR" | §3d; HLR-AG-001/002/003, HLR-SC-001 |
| Clustering turnaround: days → <1 h | **Design target** vs **measured baseline** (8.5% = 37/437 runs; 1 config/plan in legacy flow) | Playbook §2 C1, §9 |
| Go (Gin) microservices | Current build work — describe the concrete service shape | §3b above, Playbook §10 |
| ClickHouse append-only versioned store | **Verified PoC property** (latency ms are mock; the zero-mutation property is real) | Playbook §2 D2, §4, §10 |
| Pivot grid p95 <500 ms / edits <80 ms | **Architecture design targets** (NFR-01) — say "the targets the architecture is engineered to" | §3e; deck NFR-01 |
| Per-tenant config in PostgreSQL, no code deployment | Committed architecture (config vs extension vs core) | §3e; deck ENG-01, Hindsight FR-1.3 |

> **Dropped from the resume on purpose:** the BigQuery 280× cost-program claim (org audit finding, not your delivery — context only, never "I did"); the BQ→CH ingestion pipeline bullet (you can still describe the data lane as background, §3c); the "multi-agent system with 5 domain agents / 0.54→0.99" bullet (offline-eval work from the decomposition study — keep as a story about evaluation discipline, not a resume claim); and Rust (escape-hatch option only). If asked about BigQuery: "BigQuery is our upstream historical source of truth; data is ingested from it into ClickHouse through a pipeline."

## 6. Five questions you will definitely get

**"Isn't ClickHouse the wrong tool for transactional work?"**
Classically yes — and I wrote the audit position saying exactly that for the legacy mutation-heavy code. The unlock is changing the write model, not the engine: insert-only versions turn every edit into what ClickHouse is best at — appends and background merges. We proved the async-mutation queue stays at zero before committing, and the version history is not overhead — it's the feature that powers overrides, version-diff, and undo/redo the grid needs anyway. True multi-statement ACID stays on a thin Postgres plane.

**"Why Go for the non-agentic tier when the team knows Python?"**
The non-agentic surface is throughput-shaped I/O plumbing, not ML-shaped. Go gives a static binary, fast cold starts, goroutine-per-request concurrency with no async-framework tax, and one obvious way to write things. The language boundary lands on an existing service boundary — the agent tier and the CRUD tier were already separate deployables with an API contract between them.

**"What does the LLM actually do in the copilot?"**
It never computes. Deterministic tools compute — significance, coverage, redundancy, clustering runs, FitScore. The LLM orchestrates the conversation, arranges tool calls, and explains results. Same inputs + same scorer version ⇒ identical ranking. "The LLM arranges the conversation; a catalog search decides what the words mean."

**"How do you stop the agent from acting on a misparsed request?"**
Deterministic grounding: department mentions are backtracked to full hierarchy paths via catalog search, seasons resolve against the tenant's fiscal calendar, ambiguity raises a clarifying question, and a confirm-required grounding card (scope, cohort, substitutions, proposed attributes, each with a reason) gates execution. That kills the input-error class behind >80% of measured run failures.

**"What's real vs. aspirational in your numbers?"**
(Answer with the honesty table in §5 above — interviewers reward this candor. Lead with the REAL measured baselines: 8.5% run failures = 37/437 live runs, 1 config per plan, 0% reproducibility; the <1 h / <2% / p95 <500 ms figures are the committed design targets we build and test against.)

## 7. What I'd volunteer unprompted

- The **convergence rule**: agentic and manual wizard modes converge on the same config document, gates, and write-back — de-risks adoption, no fork in the data model.
- The **delegation ladder**: L1 copilot → L2 autopilot-with-approval → L3 standing drift monitor; nothing self-finalizes; `is_final` is a human signature.
- The **terminal-states contract** from auditing 19 workflows: every flow defines success/rejection/failure/expiry — nothing accumulates silently.
- Autonomy bands (from the requirements notebook): ≥0.85 auto-approve, 0.65–0.84 act-and-flag, <0.65 halt-and-escalate; overrides need a ≥10-char reason written to the audit trail.
