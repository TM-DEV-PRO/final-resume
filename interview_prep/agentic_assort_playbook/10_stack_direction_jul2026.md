---

# 10. Engineering stack direction — July 2026 (authoritative)

<div class="stage-badge stage-obs">Manager directive, agentic-assort · July 2026 · supersedes earlier "Postgres-SoR + gated ClickHouse" framing in §4/§5 where they conflict</div>

This is the **current, committed technology direction** for the agentic-assort build. Use this when describing the stack on the résumé and in interviews. Earlier chapters (§2 D1–D2, §4, §5) remain correct as the **decision history** that led here — and that history is exactly what makes this defensible.

## 10.1 The directive (verbatim intent)

1. **All non-agentic flows → GoLang.** Traditional backend services (plan lifecycle CRUD, reference-data reads, scoping/write-back APIs, tenant config) are built in **Go**, using **Gin** as the HTTP framework.
2. **Agentic workflows → unchanged.** Python 3.11+ · FastAPI · **LangGraph** (Planner→Executor→Solver) · **FastMCP** tool discovery · multi-provider LLMs (OpenAI/Gemini/Claude). Nothing about the agent brain moves.
3. **Performance-critical APIs that Go cannot satisfy → Rust.** Where a specific endpoint needs performance Go can't reach (allocation-heavy hot loops, large columnar result shaping, very high fan-out concurrency), that endpoint is built in **Rust** (Axum on Tokio). Precedent exists in-house: the CortexEye backend is already Rust/Axum.
4. **ClickHouse end-to-end — both transactional and analytical.** ClickHouse is the platform's operational **and** analytical engine for planning data: the OLAP pivot/hindsight serving layer **and** the transactional-style planning store, made safe by the **insert-only / versioned write model** (§2 D2): every edit is an INSERT with `version = epoch-ms`, reads take `argMax(value, version)`, deletes are tombstones, bulk re-seeds are atomic `REPLACE PARTITION` — the async-mutation queue stays at **zero**.

## 10.2 Why each choice holds up (interview defense)

### Go + Gin for non-agentic flows
- **Why Go:** the non-agentic surface is high-QPS, low-logic I/O plumbing — auth, validation, fan-out reads, write-back orchestration. Go gives a small static binary, fast cold start, goroutine-per-request concurrency without an async framework, and a single obvious way to do things — right for a service tier many engineers touch.
- **Why Gin specifically:** the most battle-tested Go HTTP framework (radix-tree router, middleware chain, `c.ShouldBindJSON` validation); boring in the good way. Alternatives considered: **chi** (closer to stdlib, but less batteries), **Echo** (comparable; Gin chosen for team familiarity + ecosystem), **fiber** (fasthttp-based — non-standard `net/http` semantics, rejected).
- **Supporting kit:** `clickhouse-go` v2 (native protocol, columnar blocks) for ClickHouse; `pgx` where Postgres metadata remains; `sqlc` for typed queries; OpenTelemetry middleware; golangci-lint.
- **The tradeoff to admit:** Python had all the team's data tooling; Go splits the codebase into two languages. Accepted because the agentic and non-agentic tiers were already separate deployables with an API contract between them — the language boundary lands on an existing service boundary.

### Rust for the hot paths (exception, not default)
- **Scope discipline:** Rust is *not* the default backend language — it's the escape hatch for endpoints where profiling shows Go's GC/allocation profile or FFI overhead is the bottleneck (e.g. wide pivot-grid assembly over millions of versioned cells, evidence-pack aggregation under fan-out).
- **Why Rust when needed:** no GC pauses, zero-cost abstractions, fearless concurrency (Tokio), `Arrow`/`polars` ecosystem for columnar shaping; Axum shares the tower middleware ecosystem.
- **The one-liner:** "Go by default, Rust by measurement — an endpoint earns Rust with a profile, not a preference."

### ClickHouse end-to-end (the big one)
- **The evolution story (tell it in this order):**
  1. Live audit of the legacy backend said **"no ClickHouse"** — correct, because the legacy planner does in-place OLTP mutations (keyed UPDATE, jsonb-merge, delete+reinsert), which ClickHouse mutations are genuinely bad at (async, degrade >500 queued, stall >1,000).
  2. My reconciled verdict (§2 L1): that objection is a property of the *legacy write model*, not of planning — so ClickHouse stayed a **gated option** behind a versioned-write PoC.
  3. The PoC proved the gate: **insert-only/versioned** semantics (`ReplacingMergeTree(version)`, `argMax` reads, tombstones, `REPLACE PARTITION`) hold `mutations_used = 0` at 1× and 10× scale with correct read-after-write.
  4. **July 2026: the org committed** — ClickHouse end-to-end for both transactional and analytical planning workloads. The versioned model is no longer a proposal; it's the adopted write contract, and it natively powers overrides, version-diff and undo/redo that the product grid needs anyway.
- **What "transactional" means here (be precise):** not bank-ledger OLTP — it's **planning-grid transactionality**: atomic multi-row saves (batch INSERT of one version), read-after-write within a session (client-side `version` watermark + `argMax`), idempotent replays (deterministic version keys), and audit-grade history for free. Cross-entity invariants that truly need ACID multi-statement transactions (auth, tenant config, workflow state) stay on a thin Postgres metadata plane — say this unprompted; it shows judgment.
- **What we gave up:** engine-enforced constraints/FKs (moved to service-layer validation in Go), instant hard deletes (tombstones + TTL merges instead), and storage amplification until background merges collapse versions. All accepted consciously.
- **BigQuery stays upstream** as the historical source of truth feeding ClickHouse through the proven BQ→CH ingestion lane (§2 C2); the read plane and the planning store are now the same engine, which kills a whole class of cross-engine reconciliation.

## 10.3 Résumé phrasing (paste-ready)
- *Stack line for the IA project header:* **Python (FastAPI, LangGraph, FastMCP) · Go (Gin) · Rust (Axum) · ClickHouse (insert-only versioned) · BigQuery · pgvector · GCP.*
- *Bullet (stack architecture):* "Defined the platform's polyglot service architecture — Go/Gin for all non-agentic backend flows, Rust for profile-proven hot-path APIs, Python/LangGraph unchanged for agent orchestration — and led the adoption of ClickHouse as the end-to-end transactional + analytical planning store by designing an insert-only/versioned write model (`ReplacingMergeTree` + `argMax` reads + `REPLACE PARTITION`) that keeps the async-mutation queue at zero while natively powering overrides, version-diff and undo/redo."

## 10.4 Q&A for this directive
- **"Why not keep everything Python?"** The agent tier stays Python — that's where the ecosystem lives. The non-agentic tier is throughput-shaped, not ML-shaped; Go halves its infra footprint and removes the async-framework tax.
- **"Why not everything Rust?"** Team throughput. Rust's compile-time rigor pays on hot paths; on CRUD it just slows delivery. Hence "Rust by measurement."
- **"Isn't ClickHouse for analytics only?"** Classically yes — and I authored the audit position saying exactly that for the legacy mutation-heavy code. The unlock is changing the write model, not the engine: insert-only versions turn edits into what ClickHouse is best at (appends + background merges). We proved the mutation queue stays at zero before committing.
- **"Where's Postgres now?"** A thin metadata/auth/config plane and pgvector for the semantic cache. Planning data — writes and reads — is ClickHouse.
