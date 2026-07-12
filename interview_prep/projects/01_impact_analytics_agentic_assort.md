# Impact Analytics — Agentic Assort Planner & Store-Clustering Copilot

**Role:** Senior Software Engineer · June 2026 – Present · Bangalore
**Resume header tech:** Python (FastAPI, LangGraph, MCP) · Go (Gin) · Rust (Axum) · ClickHouse (insert-only versioned, end-to-end) · BigQuery · pgvector · Redis · Kafka · GCP

> **This file is the index.** The full playbook for this project — every bullet's backing block, HLD/LLD, DB design, tech deep dives, Q&A bank, honesty tiers — lives in `../agentic_assort_playbook/` (§0–§10). Read that end-to-end before interviews. This file gives you the narrative spine and the July 2026 stack update in one place.

---

## 1. Elevator pitch (30 seconds)

"I build the AI and data backbone of an agentic retail assortment planner — the agentic rebuild of our AssortSmart product. Right now I'm shipping the store-clustering copilot: the planner states *what to cluster and for when*, a dedicated agent handles store scoping, attribute selection, and a 20-to-100-configuration exploration, with evidence packs and three human approval gates. It's spec'd against measured baselines — 8.5% run failures, one configuration tried per plan, zero reproducibility — with targets of under an hour to a finalized plan and sub-500 ms agent data probes. Alongside the agent tier I build the Go services for the non-agentic surface (plan lifecycle, reference data, bulk saves), and the data spine: ClickHouse as the unified transactional-plus-analytical planning store — made safe by an insert-only versioned write model I designed and proved in a PoC — fed by an ingestion pipeline from BigQuery, which stays the historical source of truth."

## 2. The resume project (one block: Agentic AssortSmart)

The resume shows **one project** under Impact Analytics with five bullets. Each maps to playbook material:

| Resume bullet | What it covers | Playbook sections |
|---|---|---|
| Multi-agent planning system (0.54→0.99) | Router→decomposer→validated DAG→specialist agents | §2 A1–A4, §3 |
| Store-clustering copilot (gates, <1 h, <2%) | Intent-first workflow, deterministic grounding, reproducibility/pins | §2 C1, C3–C5, §9 |
| Go (Gin) microservices | The non-agentic service surface you build (see §3b below) | **§10** |
| ClickHouse unified planning store | Insert-only versioned write model, zero mutation backlog | §2 D2, §4, **§10** |
| BigQuery→ClickHouse ingestion pipeline | The data lane feeding the store + agent read plane (p95 <500 ms target) | §2 C2, §9 |

## 3. The stack story you must tell in order (July 2026 direction)

This is the single most senior narrative you own. Tell it as an *evolution*, not a static choice:

1. **Live audit said "no ClickHouse"** for the legacy backend — and it was right: the legacy planner mutates in place (keyed UPDATEs, jsonb-merge, delete+reinsert), which ClickHouse mutations are genuinely bad at (async queue, degrades >500, stalls >1,000).
2. **I authored the reconciled verdict**: the objection is a property of the *write model*, not the engine. Made ClickHouse a *gated option* behind a versioned-write PoC.
3. **The PoC passed the gate**: insert-only/versioned semantics — `ReplacingMergeTree(version)`, `argMax(value, version)` reads, tombstone deletes, atomic `REPLACE PARTITION` re-seeds — hold `mutations_used = 0` at 1× and 10× with correct read-after-write.
4. **July 2026: the org committed** — ClickHouse end-to-end for both transactional and analytical planning workloads; Go (Gin) for all non-agentic flows; Rust (Axum) only for profile-proven hot paths; the Python/LangGraph agent tier unchanged.

**Precision on "transactional":** it's planning-grid transactionality — atomic batch inserts of one version, session read-after-write via version watermarks, idempotent replays, audit history for free — *not* bank-ledger OLTP. Cross-entity invariants that need true multi-statement ACID (auth, tenant config, workflow state) stay on a thin Postgres metadata plane. Say this unprompted; it shows judgment.

**Go vs Rust discipline:** "Go by default, Rust by measurement — an endpoint earns Rust with a profile, not a preference." Gin chosen over chi/Echo/fiber for maturity + team familiarity (fiber rejected: fasthttp breaks `net/http` semantics). Rust precedent exists in-house (CortexEye backend is Rust/Axum). *(Rust is deliberately not on the resume — if asked about the stack, mention it as the escape hatch, don't claim Rust delivery.)*

## 3b. The Go services — what you actually build (defend the Go bullet)

The resume says: *"Building Go (Gin) microservices for plan lifecycle, reference data, and bulk save APIs, with JWT auth and validation middleware, goroutine worker pools for concurrent writes, and context-based timeouts."* Here is the concrete shape behind each phrase:

- **Plan lifecycle APIs** — create/copy/finalize/soft-delete plan endpoints; state transitions validated server-side (draft → in-review → finalized); finalize is a human signature, so the handler enforces role + confirmation token.
- **Reference data APIs** — hierarchy trees, fiscal calendars, store masters, tenant config. Read-heavy fan-out: handler issues concurrent ClickHouse/Postgres reads with `errgroup.WithContext`, returns partial-safe composites.
- **Bulk save APIs** — the versioned write path: a grid save arrives as a batch of cell edits; the service assigns one `version = epoch-ms` to the batch, validates rows (Gin `ShouldBindJSON` + validator tags), and a **goroutine worker pool** (bounded channel, N workers) fans batched inserts into ClickHouse via `clickhouse-go` v2 native-protocol batch inserts. Idempotency: batch id + content hash so retries don't double-insert versions.
- **Middleware chain** — JWT auth (tenant + role claims), request-scoped logging with correlation IDs, request validation, panic recovery, per-route rate limits. Standard Gin `c.Next()` chain.
- **Context discipline** — every handler derives `context.WithTimeout`; DB calls take the ctx; slow ClickHouse probes get cancelled instead of piling up. Graceful shutdown drains in-flight requests (`server.Shutdown(ctx)`).
- **Testing** — table-driven tests, `httptest` for handlers, interface-mocked repositories; `golangci-lint` in CI.
- **Why Go here (say it like a Go dev):** "This tier is straightforward request/response work at volume — bind, validate, authorize, fan out I/O, return. Goroutines give me cheap per-request concurrency without an async framework, the binary deploys as a single static artifact, and the code stays boring enough that anyone on the team can touch it."

## 3c. The BigQuery→ClickHouse ingestion pipeline (defend the pipeline bullet)

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
| Multi-agent DAG, 0.54→0.99 | **EVAL** (offline, 12 gold queries) — say "offline evaluation harness" | Playbook §2 A1, §3 |
| Copilot targets (<1 h, <2% failures) | **FRD targets** vs **measured baselines** (8.5% = 37/437 runs; 1 config/plan; 0% reproducible) | Playbook §2 C1, §9 |
| Go (Gin) microservices | Current build work — describe the concrete service shape | §3b above, Playbook §10 |
| ClickHouse unified store, zero mutation backlog | **Verified PoC property** (latency ms are mock; the zero-mutation property is real) | Playbook §2 D2, §4, §10 |
| BQ→CH ingestion pipeline, p95 <500 ms probes | Pipeline is the real work; p95 is a **design target** — say "design target we're building against" | §3c above, Playbook §2 C2 |
| Deterministic grounding, 80%+ of failures were input errors | Baseline **measured**, mechanism designed | Playbook §2 C3 |
| 100% reproducible via config documents + pins | Design-you-own + spec'd acceptance criteria | Playbook §2 C4 |

> **Dropped from the resume on purpose:** the BigQuery 280× cost-program claim (that was an org audit finding, not your delivery — keep it as *context* you can cite about the platform's history, never as "I did") and Rust (escape-hatch option only). If an interviewer asks about BigQuery, your line is: "BigQuery is our upstream historical source of truth; my work is the ingestion lane from it into ClickHouse and the freshness/reconciliation guarantees on that lane."

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
