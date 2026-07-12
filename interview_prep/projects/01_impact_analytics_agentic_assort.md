# Impact Analytics — Agentic Assort Planner & Store-Clustering Copilot

**Role:** Senior Software Engineer · June 2026 – Present · Bangalore
**Resume header tech:** Python (FastAPI, LangGraph, MCP) · Go (Gin) · Rust (Axum) · ClickHouse (insert-only versioned, end-to-end) · BigQuery · pgvector · Redis · Kafka · GCP

> **This file is the index.** The full playbook for this project — every bullet's backing block, HLD/LLD, DB design, tech deep dives, Q&A bank, honesty tiers — lives in `../agentic_assort_playbook/` (§0–§10). Read that end-to-end before interviews. This file gives you the narrative spine and the July 2026 stack update in one place.

---

## 1. Elevator pitch (30 seconds)

"I build the AI and data backbone of an agentic retail assortment planner — the agentic rebuild of our AssortSmart product. Right now I'm shipping the store-clustering copilot: the planner states *what to cluster and for when*, a dedicated agent handles store scoping, attribute selection, and a 20-to-100-configuration exploration on a dedicated ClickHouse read plane, with evidence packs and three human approval gates. It's spec'd against measured baselines — 8.5% run failures, one configuration tried per plan, zero reproducibility — with targets of under an hour to a finalized plan and sub-500 ms agent data probes. Under it sits a polyglot service architecture I helped define — Go for non-agentic services, Rust for hot paths, Python for the agent tier — and ClickHouse as the end-to-end transactional-plus-analytical planning store, made safe by an insert-only versioned write model I designed and proved in a PoC."

## 2. The two-project split on the resume

| Resume project | What it covers | Playbook sections |
|---|---|---|
| **Agentic Assort Planner** (platform) | Multi-agent orchestration (router→decomposer→DAG→specialists), polyglot stack, ClickHouse end-to-end decision, BigQuery cost program | §2 A1–A4, D1–D4, P1–P3, §3, §4, **§10** |
| **Agentic Store-Clustering Copilot** (flagship module) | The shipping module: intent-first workflow, dedicated CH read plane, deterministic grounding, reproducibility/pins, strategy doorway | §2 C1–C5, §9 |

## 3. The stack story you must tell in order (July 2026 direction)

This is the single most senior narrative you own. Tell it as an *evolution*, not a static choice:

1. **Live audit said "no ClickHouse"** for the legacy backend — and it was right: the legacy planner mutates in place (keyed UPDATEs, jsonb-merge, delete+reinsert), which ClickHouse mutations are genuinely bad at (async queue, degrades >500, stalls >1,000).
2. **I authored the reconciled verdict**: the objection is a property of the *write model*, not the engine. Made ClickHouse a *gated option* behind a versioned-write PoC.
3. **The PoC passed the gate**: insert-only/versioned semantics — `ReplacingMergeTree(version)`, `argMax(value, version)` reads, tombstone deletes, atomic `REPLACE PARTITION` re-seeds — hold `mutations_used = 0` at 1× and 10× with correct read-after-write.
4. **July 2026: the org committed** — ClickHouse end-to-end for both transactional and analytical planning workloads; Go (Gin) for all non-agentic flows; Rust (Axum) only for profile-proven hot paths; the Python/LangGraph agent tier unchanged.

**Precision on "transactional":** it's planning-grid transactionality — atomic batch inserts of one version, session read-after-write via version watermarks, idempotent replays, audit history for free — *not* bank-ledger OLTP. Cross-entity invariants that need true multi-statement ACID (auth, tenant config, workflow state) stay on a thin Postgres metadata plane. Say this unprompted; it shows judgment.

**Go vs Rust discipline:** "Go by default, Rust by measurement — an endpoint earns Rust with a profile, not a preference." Gin chosen over chi/Echo/fiber for maturity + team familiarity (fiber rejected: fasthttp breaks `net/http` semantics). Rust precedent exists in-house (CortexEye backend is Rust/Axum).

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
   │  BigQuery — historical source of truth, cubes │  │ Postgres     │
   │  (partitioned+clustered, cost-guarded)        │  │ metadata/auth│
   └───────────────────────────────────────────────┘  │ + pgvector   │
                                                      └──────────────┘
```

## 5. Every resume bullet → where its defense lives

| Bullet | Claim tier | Defense |
|---|---|---|
| Multi-agent DAG, 0.54→0.99 | **EVAL** (offline, 12 gold queries) — say "offline evaluation harness" | Playbook §2 A1, §3 |
| Polyglot Go/Rust/Python architecture | Committed direction | Playbook §10 |
| ClickHouse end-to-end, mutations = 0 at 10× | **Verified PoC property** (latency ms are mock; the zero-mutation property is real) | Playbook §2 D2, §4, §10 |
| BigQuery 280× (2.9 TiB → 3.3 GiB), 38.8 TiB/$327 leak | **REAL** — live audit; defend as measured | Playbook §2 P1–P2 |
| Copilot targets (<1 h, 20+ configs, <2% failures) | **FRD targets** vs **measured baselines** (8.5% = 37/437 runs; 1 config/plan; 0% reproducible) | Playbook §2 C1, §9 |
| p95 <500 ms read plane, 80%+ warm | **FRD target** — say "design target we're building against" | Playbook §2 C2 |
| Deterministic grounding, 80%+ of failures were input errors | Baseline **measured**, mechanism designed | Playbook §2 C3 |
| 100% reproducible via config documents + pins | Design-you-own + spec'd acceptance criteria | Playbook §2 C4 |

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
(Answer with the honesty table in §5 above — interviewers reward this candor. Lead with the REAL audit numbers: 280×, 38.8 TiB/$327, 8.5% = 37/437.)

## 7. What I'd volunteer unprompted

- The **convergence rule**: agentic and manual wizard modes converge on the same config document, gates, and write-back — de-risks adoption, no fork in the data model.
- The **delegation ladder**: L1 copilot → L2 autopilot-with-approval → L3 standing drift monitor; nothing self-finalizes; `is_final` is a human signature.
- The **terminal-states contract** from auditing 19 workflows: every flow defines success/rejection/failure/expiry — nothing accumulates silently.
- Autonomy bands (from the requirements notebook): ≥0.85 auto-approve, 0.65–0.84 act-and-flag, <0.65 halt-and-escalate; overrides need a ≥10-char reason written to the audit trail.
