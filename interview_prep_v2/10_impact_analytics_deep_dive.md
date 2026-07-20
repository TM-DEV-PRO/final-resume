# Impact Analytics Deep Dive: Bullet-by-Bullet Interview Defense

**Role:** Senior Software Engineer · Impact Analytics, Bangalore · 14 May 2026 – Present  
**Project:** Agentic AssortSmart (FastAPI chat + Go doing layer) on **ClickHouse/GCS** (insert-only versioned planning store); POC evidence from Pivot / LinePlanning / consolidated CH-vs-PG report  
**Sources of truth:** `GROUND_TRUTH.md`, resume IA bullets, Jul 2026 stack direction (`10_stack_direction_jul2026.md`), HLD `final_agenticassort.png`, POC source extracts `19`/`20`/`21`  
**Honesty rule:** Every number below is tagged MEASURED / TARGET / ESTIMATED / design-only. Do not invent. **Resume direction = CH end-to-end for agentic planning data.** POC hybrid slides are decision history (legacy OLTP / why the write model had to change), not a contradiction if you tell the evolution story.

---

## 0. Role framing (30-second open)

I joined Impact Analytics as a Senior Software Engineer on 14 May 2026. My charter sits at the intersection of two workstreams:

1. **Agentic AssortSmart data plane:** ClickHouse/GCS as the end-to-end planning store — insert-only versioned writes (`ReplacingMergeTree` + `argMax`) so the doing layer is not stuck on classic OLTP mutations. BigQuery stays upstream historical truth (BQ→CH ingest). Thin Postgres metadata only if asked.
2. **Agentic product:** Cluster Recommendation Copilot — FastAPI/LangGraph owns chat; Go (Gin) is the doing layer for Hindsight / Clustering / Strategy; Datadog + LangSmith + PostHog share an OTEL `trace_id`.

I am an IC so far (no people lead at IA). CDC platform tooling (`pg2ch_cdc`) was authored by another engineer (Ashvin Sharma). Copilot: Phase 1 design approved (external review PASS); bring-up load test pending. Obs stack on the resume is **MEASURED design / instrumentation**, not sole SaaS ownership.

**Source tension to own unprompted:** The Jul 2026 POC report verdict is still **hybrid per surface** for assortment benchmarks and **no wholesale CH** for legacy mtp-assort. The **agentic-assort** build follows the Jul 2026 stack directive + HLD: planning data on ClickHouse end-to-end because we changed the write model. Do not collapse “no CH for legacy UPDATE/JSONB” into “no CH for agentic AssortSmart.”

---

## 1. End-to-end architecture (Order Batching CQRS + edit path)

This is the picture I draw on a whiteboard when asked how Order Batching moves to ClickHouse without breaking saves, locks, or edit sessions.

```
                         WRITE PATH (always PostgreSQL)
┌────────────┐   SPs / APIs    ┌─────────────────────────────────────────────┐
│   Client   │ ──────────────► │  PostgreSQL (system of record for writes)   │
└────────────┘                 │  CARFG, plan_master, plan_attributes,       │
                               │  order_batching_access_data (locks)         │
                               └──────────────────┬──────────────────────────┘
                                                  │  CDC mirrors (hot facts)
                                                  │  CARFG · plan_master ·
                                                  │  dc_pack_reserve_quantity
                                                  ▼
                               ┌─────────────────────────────────────────────┐
                               │  ClickHouse (analytical read plane)         │
                               │  ReplacingMergeTree mirrors + daily-refresh │
                               │  dims (product/store filters, DCs, etc.)    │
                               └──────────────────┬──────────────────────────┘
                                                  │
                         READ PATH                ▼
┌────────────┐   read SPs      ┌─────────────────────────────────────────────┐
│   Client   │ ◄────────────── │  Backend routing layer                      │
└────────────┘                 │  default → ClickHouse                       │
                               │  if Redis key ob:ryw:{l0_name} set (TTL~30s) │
                               │            → PostgreSQL (read-your-writes)  │
                               └─────────────────────────────────────────────┘


              EDIT SESSION (GCS parquet: no DB during in-memory edits)

┌────────────┐  /update-mode-toggle   ┌────┐  upload   ┌──────────────────┐
│   Client   │ ──────────────────────►│ PG │──────────►│ GCS parquet      │
└────────────┘  (seed from CARFG)     └────┘           │ ob-edits-{uid}   │
     │                                                  └────────┬─────────┘
     │  /session/updates  (pandas in-memory edits)               │
     │ ◄─────────────────────────────────────────────────────────┤
     │  re-upload edited parquet                                 │
     └──────────────────────────────────────────────────────────►│
     │
     │  /session/save  →  order_batching_session_save SP
     │ ──────────────────────────────────────────────────────────► PG (CARFG)
     │                                                              │
     │                                                              ▼ CDC ► CH
     │  Redis.set("ob:ryw:{l0_name}", ttl=30s)  ◄── after save/finalise
```

**Table sync strategy (MEASURED design: Order Batching migration arch):**

| Table | Churn | Sync |
|---|---|---|
| `create_allocation_result_flat_gurobi` (CARFG) | High (every save/finalise) | CDC mirror |
| `plan_master` | Moderate (status on finalise) | CDC mirror |
| `dc_pack_reserve_quantity` | Moderate | CDC mirror |
| `product_attributes_filter`, `store_attributes_filter` | Low | Daily full refresh |
| `store_current_inventory` | Daily batch | Daily full refresh |
| `distribution_centres`, `dc_pack_configuration` | Very low | Daily full refresh |
| Lock tables (`order_batching_access_data`, GCS locks) | N/A | PG-only (no CDC) |

---

## 2. ClickHouse planning / agentic schema sketch

Two related but distinct models show up in interviews. Keep them separate.

### 2a. Order Batching / inventory mirrors (migration plane)

```
PG OLTP                         CH OLAP mirrors
─────────────────               ─────────────────────────────────
CARFG (partitioned              CARFG_rmt  ENGINE = ReplacingMergeTree(_cdc_synced_at)
  by created_at)     ─CDC──►      ORDER BY (allocation_code, store, article, …)
                                  + _cdc_synced_at, _cdc_deleted

plan_master          ─CDC──►    plan_master_rmt  (same pattern)
dc_pack_reserve_*    ─CDC──►    dc_pack_reserve_*_rmt

product_attributes_filter  ─daily─►  product_attributes_filter (full replace / swap)
store_attributes_filter    ─daily─►  store_attributes_filter
distribution_centres       ─daily─►  distribution_centres
```

Pattern for hot facts: **insert-only updates** into ReplacingMergeTree; version column (e.g. `_cdc_synced_at`) collapses duplicates on merge. Soft deletes via `_cdc_deleted`. Reads that need exact latest may use `FINAL` (costly) or partition-scoped queries + application-level version awareness.

### 2b. Agentic Cluster ClickHouse model (copilot read plane)

**Summary (MEASURED design):** **63 tables / 8 layers / 624 columns**, one database per tenant, validated against ClickHouse 25.12. Zero row-level mutations by doctrine.

```
LAYER MAP (simplified)

1. FACTS (partition-swapped, never mutated in place)
   ┌─────────────────────────────────────────────────────────┐
   │ sales_fact / store_kpi_fact / attribute_coverage_fact   │
   │ PARTITION BY (season_or_week_key)                       │
   │ writer swaps whole partition atomically                 │
   └─────────────────────────────────────────────────────────┘

2. DIMS / REGISTRIES (tiny, versioned)
   ┌─────────────────────────────────────────────────────────┐
   │ hierarchy_registry · season_registry · store_dim        │
   │ metric_weight_policy_v{n}  (content-addressed versions) │
   └─────────────────────────────────────────────────────────┘

3. SERVING CUBES (pre-aggregations, also partition-swapped)
   ┌─────────────────────────────────────────────────────────┐
   │ significance_cube · store×attribute matrices            │
   └─────────────────────────────────────────────────────────┘

4. LIVE-PLAN MIRRORS (read projection of incumbent plans)
   ┌─────────────────────────────────────────────────────────┐
   │ cluster_plan_membership_mirror · strategy_binding_view  │
   └─────────────────────────────────────────────────────────┘

5. DECISION PLANE (append-only events + immutable snapshots)
   ┌─────────────────────────────────────────────────────────┐
   │ session_events · recommendation_runs                    │
   │ config_snapshot  (hash of recipe + data watermark)      │
   │ pin_events · approval_events                            │
   │ is_optimal (engine) ≠ is_final (human)                  │
   └─────────────────────────────────────────────────────────┘

6. OUTCOME LOOP (plan vs actuals)
   ┌─────────────────────────────────────────────────────────┐
   │ variance_cube  (plan-not-followed / re-planned /        │
   │                 world-changed / recommendation-wrong)   │
   └─────────────────────────────────────────────────────────┘

7. WRITE-BACK STAGING → transitional adapter → incumbent PG tables
8. TELEMETRY (tool calls, quotas, agent guardrail hits)
```

**Four physical patterns to recite:**

1. **Partition-swapped facts/cubes**: never `ALTER UPDATE` a cell; rebuild and swap the partition.
2. **Versioned registries**: policy/config rows are immutable versions; readers pin a version id.
3. **Append-only events**: decisions, pins, approvals; latest-state via views, not overwrites.
4. **Content-addressed configs**: hash of the clustering recipe + data watermark ⇒ bit-for-bit reproducibility (TARGET for product; schema supports it by design).

Agent DB profiles are **read-only**. The LLM never writes SQL ad-hoc; it calls **14 audited tools**. Human gates: grounding → search plan → approval → write-back.

---

## 3. Clustering copilot user flow (what I walk through)

Aligned to AssortSmart HLR v1.1 (behavioral + constraints) and Copilot Phase-1 FRD.

```
1. SCOPE SUBMIT
   Planner states intent: hierarchy + reference period
   (wizard pickers OR one chat prompt)
        │
        ▼
2. GROUNDING CARD  (human gate 1: confirm understanding)
   Agent resolves hierarchy paths, season dates, store cohort
   (active + sister-store substitutions, sample-size guards)
   Proposes attribute/feature set from significance ranking
        │
        ▼
3. FEATURE + k SELECTION  (deterministic plane)
   Autonomous feature weights from significance / coverage / redundancy
   Optimal k via elbow method + silhouette scoring
   Client min/max k and child-cluster cap (default 10) act as guardrails
        │
        ▼
4. SCENARIO GENERATION  (constraint: 3–5 scenarios)
   Distinct across: primary lens, time horizon, store scope, k
   Always include Baseline (Previous Plan) when one exists
   Batch explores many configs (TARGET ≥20 evaluated per plan; from 1 today)
        │
        ▼
5. COMPARISON + EVIDENCE
   Top recommendations with composite score, cluster composition,
   plain-English narrative; swing stores flagged
   Planner can pin/move stores with impact preview (pins persist)
        │
        ▼
6. APPROVAL  (human gates 2–3)
   Planner picks winner; optional governance sign-off
   Agent cannot write; is_optimal ≠ is_final
        │
        ▼
7. MASTER WRITE / WRITE-BACK
   Approved config document + membership written into today's
   cluster master / product tables (incumbent path unchanged)
```

**Measured baselines (kik tenant audit, MEASURED):** run failures **8.5% (37/437)**; median clustering job **~20s** (370 live runs); reproducibility **0%** (winning config/seed not persisted historically).

**Targets (TARGET: say "targeting"):** hierarchy-to-finalized-plan **days → under 1 hour**; configs evaluated **1 → ≥20**; failures **8.5% → under 2%**; reproducibility **0% → 100%**; CH read plane **sub-second** for tool queries.

**Platform NFRs (TARGET from Planning Platform Architecture):** grid p95 **<500ms**, cell edit **<80ms**, History Opt **<30s**, 3 scenarios **<60s**.

**Status honesty:** Phase 1 design complete; four internal adversarial passes + external review **PASS (approve to bring-up)**. Remaining gate: **bring-up load test** (cube sizing on real kik extract). Do not claim shipped production copilot.

---

## 4. Resume bullet 1: Cluster Recommendation Copilot

> Building the Cluster Recommendation Copilot for AssortSmart, an agentic store clustering module where an LLM agent (LangGraph, MCP) plans and calls 14 audited tools while a deterministic engine computes clusters, with human approval gates before any write. Targets are plan turnaround under 1 hour (from days), 20+ configurations evaluated per run (from 1), and run failures under 2% (from a measured 8.5%).

### 4.1 Exact story with numbers

**Problem:** Store clustering is the foundation for assortment strategy, but today the planner does four expert choices blind, then runs **one** configuration. The system already computes significance scores and then ignores them for recommendation. Measured on live tenant data: **8.5% of runs fail (37 of 437)**; most failures are avoidable input-boundary mistakes. Winning algorithm/hyperparameters/seed are not saved ⇒ **reproducibility 0%**. Compute itself is fine (median job **~20s**); the bottleneck is everything around the machine.

**Solution design:** Two planes. An **LLM (LangGraph + MCP)** orchestrates and explains. A **deterministic engine** does feature selection, k search (elbow + silhouette), clustering, and scoring via **14 audited tools**. The agent **cannot write**. Humans confirm at grounding, search-plan, approval, and write-back gates. Schema is agentic-first: **63 tables / 8 layers / 624 columns**, partition-swapped facts, append-only decisions, content-addressed configs.

**Targets (TARGET):** under **1 hour** turnaround (from days), **≥20** configs per run (from 1), failures **under 2%** (from 8.5%), reproducibility **100%**, CH read plane sub-second.

### 4.2 How it was done step by step

1. Audited live tenant pain (failure rate, one-shot config, non-reproducible runs, lost store swaps).
2. Wrote Phase-1 FRD: intent → grounding → search plan → batch compute → top recommendations → pins → approval → write-back.
3. Locked product constraints from HLR v1.1: **3–5 scenarios**, mandatory distinctness, baseline inclusion, child cluster cap default **10**.
4. Split responsibility: LLM plans/narrates; tools compute; DB profiles enforce read-only for the agent.
5. Designed CH DDL (63/8/624) with zero row-level mutations; validated statements on CH **25.12**.
6. Ran adversarial design reviews (engine idiom, concurrency, operation coverage, scale) + external pricing-team playbook review → **PASS**.
7. Remaining: bring-up load test before implementation cutover claims.

### 4.3 Design decisions and trade-offs

| Decision | Why | Trade-off |
|---|---|---|
| LLM orchestrates, tools compute | Numbers must be deterministic and auditable; LLM is bad at inventing stats | More engineering on tool contracts; less "magic" agent autonomy |
| 14 audited tools, no free SQL | Prevents hallucinated queries and uncontrolled warehouse load | New capability requires a new tool, not a prompt tweak |
| Human gates before any write | Clustering ships into strategy plans; silent auto-finalize is unacceptable | Latency of human-in-the-loop; need clear UX for gates |
| 3–5 scenarios (not 6–10) | Decision fatigue; HLR superseded earlier wider range | Less coverage of search space in the UI; breadth moves into batch under the hood (TARGET ≥20 evaluated) |
| Elbow + silhouette for k | Statistical fit inside client min/max + child-cap guardrails | Not business-optimal by itself; planner can override with evidence |
| CH as decision/read plane, PG identity + transitional write-back | OLAP + append-only decision history fits CH; auth/UAM and incumbent product still on PG | Dual-store complexity until write-back retirement |
| Content-addressed configs | Makes reproducibility a schema property | Storage of snapshots; must watermark data versions |

### 4.4 What breaks at 10x and gotchas

- **10× tenants / hierarchies:** nightly precompute and cube partition swaps become the bottleneck; need per-tenant quotas and concurrency budgets (design includes them; load test pending).
- **10× store universe:** significance matrices and what-if caches grow; partition strategy and retention must be proven on kik×10 sizing (in DDL sizing section; MEASURED design, not measured latency).
- **Gotcha:** agent proposes; human must still own intent. Autopilot (L2) and drift monitor (L3) are later phases: do not claim them as shipped.
- **Gotcha:** `is_optimal` (engine) must never overwrite `is_final` (human). Interviewers love this distinction.
- **Gotcha:** strategy doorway found **1 in 5** finalized plans on kik with **zero stores** attached: eligibility gates before scoring are not pedantry.

### 4.5 Honesty tags

| Claim | Tag |
|---|---|
| 14 audited tools, LangGraph/MCP orchestration, human gates | MEASURED design |
| Failures 8.5% (37/437), median ~20s, reproducibility 0% | MEASURED baseline |
| Under 1h, ≥20 configs, <2% failures, 100% reproducibility, sub-second CH reads | **TARGET** |
| 63 tables / 8 layers / 624 columns, zero row-level mutations | MEASURED design (DDL validated on CH 25.12) |
| External review PASS | MEASURED design status |
| Production copilot live / load-tested | **NO (load test pending)** |

**Say in interview:** "Phase 1 design is approved to bring-up. I am not claiming a production-shipped agent yet. Load test is the remaining gate."

---

## 5. Prep depth: Order Batching PG vs CH benchmarks (replaced on resume headline)

> **Resume now leads with hybrid pivot/line-plan (189s→12.3s, cell &lt;1ms, 12B avoided).** Keep this section for "what else did you measure?" — Order Batching metric over 23.7M joined rows: CH 3.86s vs PG 3m40s+ (~60×); inserts ~5.9M vs 250K rows/s; export ~43×.

### 5.1 Exact story with numbers (memorize these)

All MEASURED from older POC dump. Infra was **not** identical.

**Hardware caveat (say this first if challenged):**

| | PostgreSQL | ClickHouse |
|---|---|---|
| Setup | Tuned production-grade | Untuned / direct SQL port |
| RAM | **256 GB** | **64 GB** |
| vCPU | **32** | **16** (+ 2 replicas in some setups) |

CH often had **weaker** hardware and less tuning, and still won. Treat results as directional POC evidence, not a lab-perfect A/B.

**Headline numbers:**

| Workload | PG | CH | Multiple |
|---|---|---|---|
| Order Batching metric, **23,749,263** join rows | **3m 40s** (UTC) / **7m 48s** (Australia/Melbourne TZ) | **3.857s** (~3.86s) | **~60×** (docs; range ~57–120× depending on TZ path) |
| Insert effective throughput (30 promos × 10M = **3.9B** rows) | **250K** rows/s raw; **~417K** detach/attach | **~5.91M** rows/s | **~14–24×**; CH at **~30** connections vs PG **280** for detach/attach |
| Query → CSV export | **541s** / **607** rows/s (328,692 rows) | **~38s** / **26,442** rows/s (1M rows) | **~43×** export throughput |
| Small Order Batching join (~57K rows) | **2.043s** | **2.803s** | Parity (PG slightly faster) |
| Incremental MV: 100K insert | Full `REFRESH` **~4.013s** over ~1.69M source | INSERT+MV **0.646s** (~0.65s) | CH **~85%** faster incremental path |
| Fact compression (ISP POC) | 3.31 GiB raw | **432.81 MiB** compressed on **17.15M** rows | **~7.8×** |

### 5.2 How it was done step by step

1. **Frame the pain:** aggregation-heavy retail reads (promo loaders, MVs, Order Batching metric SP) degrade to minutes on PG; MV refresh is full-table.
2. **Hypothesis:** columnar CH + MergeTree family wins on analytical scans/joins/bulk loads; keep transactional writes on PG.
3. **Insert POC:** run `load_ps_reco_non_agg_parallel.py`; compute **effective** rows/s as `sum(expected_rows) / (max(ended) − min(started))` across successful parallel jobs: not sum of per-job times. Scale from single-promo 10M → 100M → **30×10M**.
4. **Export POC:** same analytical intent; time query vs CSV write separately; note PG used temp/unlogged materialization, CH used direct CTE.
5. **MV POC:** identical GROUP BY at 100K / 400K / full; compare CH incremental MV cost vs PG full refresh after 100K insert.
6. **Order Batching metric:** fixed reference date; warm/small (~57K) then full (**23.7M** join rows); measure PG with prod TZ and UTC to isolate timezone conversion cost (~2× on PG alone).
7. **Document caveats** in Confluence: unequal hardware, untuned CH, methodology.

### 5.3 Design decisions and trade-offs

| Decision | Why |
|---|---|
| Port real workloads, not synthetic TPC | Stakeholders trust Order Batching / promo paths they own |
| Report wall-clock effective throughput | Matches how loaders actually finish in production |
| Keep small-scale parity visible | Honesty: at ~57K rows PG ≈ CH; cliff appears at multi-million joins |
| Isolate TZ on PG | Prevents attributing pure conversion cost to "engine superiority" alone |

### 5.4 What breaks at 10x and gotchas

- **10× join cardinality:** memory for join build/probe; need stricter partition pruning and pre-aggregation (see exploded batch OOM at **133.7M** rows in update-metrics doc).
- **10× insert parallelism:** CH insert path still needs part-merge budget; uncontrolled small parts create merge storms.
- **Gotcha:** do not claim identical hardware. Interviewers who know CH will ask.
- **Gotcha:** if they cite older **60×** / **3m 40s+** from prep or prior PDF: defend with both PG times (3m40s UTC and 7m48s TZ) and CH **3.86s**. Lead interviews with Jul 2026 hybrid numbers first.
- **Gotcha:** export row counts differ (PG ~329K vs CH 1M in the recorded run). Defend on **rows/sec** and wall time methodology, not "same row count dump."

### 5.5 Honesty tags

| Claim | Tag |
|---|---|
| All table numbers above | MEASURED |
| Identical hardware A/B | **FALSE (do not claim)** |
| Production cutover complete because of these numbers | **FALSE (POC / architecture)** |
| ~60× / 43× / 14–24× | MEASURED multiples from documented runs |

---

## 6. Resume bullet 3: CQRS migration (Order Batching)

> Designed the ClickHouse read path for Order Batching, keeping writes on PostgreSQL, syncing hot fact tables in near real time, and routing post save reads through Redis (30s TTL) so planners see their own saves instantly.

Note: the resume now carries only ONE ClickHouse point, the PG to ClickHouse migration POC with benchmark numbers. The read path design below (CQRS, CDC mirrors, Redis read your writes) is prep-only depth: bring it up verbally when asked "what would the production migration look like".

### 6.1 Exact story with numbers

**Goal:** move aggregation-heavy **reads** for Order Batching to ClickHouse to cut PG load, while **all writes stay on Postgres**. GCS parquet edit sessions stay unchanged (no DB during in-memory edits).

**Sync:** CDC for high/moderate churn facts (CARFG, plan_master, dc_pack_reserve); daily full refresh for low-churn dims.

**RYW:** after `/session/save` or `/finalise`, set `Redis.set("ob:ryw:{l0_name}", ttl=30s)`. Router: if key present → PG; else → CH. **30s** covers typical CDC lag window.

**CDC platform SLOs I designed against / integrated with (MEASURED tool SLOs; tool authored by Ashvin Sharma):**

| SLO | Target |
|---|---|
| PG commit → CH visible | **p95 ≤ 10s** (low-throughput tables) |
| Initial snapshot | **≥ 25K rows/s** per mirror |
| Row-count drift | **≤ 0.5%** steady state (health diagnostics; note drift UI thresholds also use absolute+relative guards) |
| Reference: 1 mirror | ~**30K** rows/s snapshot, ~**5K** rows/s stream |
| Reference: 10 mirrors | ~**8K** rows/s aggregate stream |

**k6 POC (planned, not claimed done):** 50 concurrent users, 11 read SPs, pass if p95 < current PG baseline.

### 6.2 How it was done step by step

1. Classify every Order Batching table by change frequency → CDC vs daily refresh vs PG-only.
2. Draw dual paths: write APIs always hit PG SPs; read APIs go through a routing layer defaulting to CH.
3. Preserve GCS HLE parquet edit flow (`/session/updates` never touches DB mid-edit).
4. Solve read-your-writes with Redis TTL after save/finalise (not dual-write).
5. Call out lock atomicity fix before cutover: partial unique index on `order_batching_access_data(hierarchy_hash) WHERE status IN (1,2)`.
6. Align mirror list with `pg2ch_cdc` capabilities (logical replication, ReplacingMergeTree, apply-before-slot-commit).
7. Plan validation: k6 on 11 read SPs; SP equivalence harnesses elsewhere in the migration toolkit.

### 6.3 Design decisions and trade-offs (high-value interview meat)

#### Why CQRS, not dual-write?

- Dual-write (app writes PG and CH in one request) creates **split-brain** on partial failure, retries, and lock semantics.
- Order Batching writes need PG transactions, `l0_name` locks, finalise status transitions, and existing SPs.
- CQRS: **one writer (PG)**, async projection to CH, router absorbs lag. Operationally simpler and safer for this module.

#### Why CDC (not nightly-only for hot facts)?

- CARFG changes on every save/finalise. Nightly refresh would make analytical screens stale for a full day.
- CDC targets **seconds** of lag (SLO p95 ≤ 10s), which matches interactive planning if combined with RYW.

#### Why direct CDC (no Kafka) for this platform context?

- Volume is a handful of high-fidelity tables, not a company-wide event bus.
- Kafka + Debezium + sink would add brokers, schema registry, and multi-hop opacity for low-thousands rows/s peaks.
- `pg2ch_cdc` is a single-process gateway: PG logical slot (`pgoutput`) → apply to CH. I **designed against / integrated with** this tool; I did **not** author it.

#### Why Redis RYW with TTL fallback (not "wait for CDC" or "always read PG after write")?

- Waiting for CDC in the request path couples UX to replication health.
- Always reading PG after write defeats the migration (PG stays on the hot path forever).
- Redis flag for **~30s** is a bounded window: users see their own saves on PG immediately; everyone else (and the same user after TTL) rides CH. If CDC is healthy, window is usually more than enough; if CDC is sick, RYW still protects the writer while ops fix lag (though prolonged lag needs ops, not a longer TTL forever).

#### Why not move writes to ClickHouse?

- CH is poor for row-level transactional locks, session save semantics, and frequent point updates without a careful mutation strategy (see bullet 4).
- Retail planning UX still expects OLTP guarantees on save/finalise.

### 6.4 What breaks at 10x and gotchas

- **10× write QPS on CARFG:** CDC stream apply and CH part merges become the bottleneck; slot lag risk if CH slows (`SLOT_LAG` diagnostics at ≥1 GiB critical in the CDC tool).
- **10× concurrent planners on same hierarchy:** lock table must be atomically correct before cutover (partial unique index note).
- **Gotcha:** UPDATE on CH side in CDC is **DELETE + INSERT**; ReplacingMergeTree dedupes by version. Without `FINAL` or careful querying, you can briefly see duplicates.
- **Gotcha:** truncates default **off** in CDC (`apply_truncates=False`): accidental OLTP truncate must not wipe the warehouse.
- **Gotcha:** apply **CH first**, then commit PG slot → at-least-once + RMT dedupe. Never claim exactly-once without explaining merge-time dedupe.
- **Gotcha:** ownership language: say **"designed against / integrated with `pg2ch_cdc`"**, not "I built the CDC platform."

### 6.5 Honesty tags

| Claim | Tag |
|---|---|
| CQRS architecture, table sync matrix, Redis 30s RYW | MEASURED design doc |
| CDC SLOs (10s p95, 25K snapshot) | MEASURED platform SLOs |
| Authorship of `pg2ch_cdc` | **NOT MINE** (Ashvin Sharma) |
| Full production cutover of Order Batching reads | **Do not claim unless you personally cut over**: architecture + POC stage |
| k6 50-user pass | Planned validation, not a measured resume claim |

---

## 7. Resume bullet 4: Update strategies, ReplacingMergeTree, compression

> Cut 10K row update handling on a 29M row fact table from 39s to 7s using partition scoped merges over full table rewrites, and validated ReplacingMergeTree versioned updates, partition pruning, and dictionary lookups (17M row fact table compressed 7.8x to 433 MiB).

### 7.1 Exact story with numbers

**CARFG-scale update bake-off (~29M rows, MEASURED):**

| Approach | Result |
|---|---|
| Naive full-table read+insert | ~**24 GB** read; runs **33.8s / 73.5s / 77.9s** (high variance) |
| Full-table scope merge for **10K** updates | **~35.6–38.8s** (resume rounds to **39s**) |
| **Partition-scoped** merge (partition `20260512`, ~3.80M rows) | **7.309s** (~**7s**) |
| Delta join on one partition | **6.734s**, 3.08 GB processed, peak mem **2.39 GiB** |
| Full-table delta join (~29M delta) | **OOM** at **14.40 GiB** (Code 241) |

**Query cliffs (same doc):**

| Query | CARFG rows | Latency |
|---|---|---|
| order batching batch SP | 5.2M (1 partition) | 12.475s |
| order batching batch exploded | 133.7M (1 partition) | **OOM / server crash** |

**Compression (ISP / architecture review, MEASURED):** fact table **17.15M** rows, **432.81 MiB** compressed vs **3.31 GiB** raw ⇒ **~7.8×**.

### 7.2 How it was done step by step

1. Establish naive baseline: SELECT entire table + INSERT rewritten rows (proves cost of "update = rewrite everything").
2. Partition by `toYYYYMMDD(created_at)`; confirm which partition holds the 10K-change working set.
3. Re-run merge scoped to one partition only → ~7s.
4. Prototype delta table (`delta_carfg`) LEFT JOIN base with version `COALESCE` for ~24 metric columns.
5. Show delta join ≈ partition merge on single partition, but **OOM** when delta grows to full table.
6. Validate ReplacingMergeTree versioned insert patterns and partition pruning on analytical queries; note dictionary lookups as a CH-native acceleration pattern in the broader ISP POC.
7. Document failure modes for the team so migration SPs do not "just explode the join."

### 7.3 Design decisions and trade-offs

#### Why ReplacingMergeTree?

- CH in-place `ALTER UPDATE` mutations are expensive and queue poorly for interactive planning.
- Insert-only "updates" with a version column let background merges collapse to latest row.
- Fits CDC apply path (DELETE+INSERT / new version row) and analytical rebuilds.

**Cost:** readers may need `FINAL`, argMax patterns, or partition-local logic to see latest before merge. `FINAL` forces merge-on-read and can be expensive at scale: use sparingly, prefer query shapes that naturally prune.

#### Why partition-scoped updates over full rewrites?

- Full rewrite reads **~24 GB** and sits in the **36–39s** band for 10K changes on ~30M rows.
- Same logical update scoped to one day partition finishes in **~7s** because IO and merge work track partition size (~3.8M rows), not table size.
- Retail facts already have natural time/partition keys (`created_at`).

#### Why consider delta join, and when to reject it?

- Comparable latency to partition merge on a hot partition (**6.7s vs 7.3s**) with less IO.
- Reject unbounded deltas: at full-table delta size the join **OOMs at 14.4 GiB**. Delta must stay small or be compacted/partitioned.

#### Why dictionary lookups (where used)?

- Dim attributes that would otherwise explode joins can be served as CH dictionaries for low-latency enrichment on large facts (ISP-style analytical path). Trade-off: dictionary refresh semantics and memory residency must be owned.

### 7.4 What breaks at 10x and gotchas

- **10× partition size:** partition-scoped "win" shrinks; re-evaluate partition granularity (day → hour is not free either: too many parts).
- **10× concurrent mutations:** merge pressure and memory; exploded queries already crash at **133.7M** rows today.
- **Gotcha:** ReplacingMergeTree is eventually consistent until merge/`FINAL`. Demo queries without `FINAL` can confuse QA comparing PG vs CH row-for-row.
- **Gotcha:** resume "39s → 7s" maps to full-table scope **~36–39s** vs partition **7.309s** for **10K** updates on ~**29–30M** rows.
- **Gotcha:** compression **7.8× to ~433 MiB** is on the **17.15M** fact table example: do not mix it with the 29M CARFG update story as the same table unless asked carefully.

### 7.5 Honesty tags

| Claim | Tag |
|---|---|
| 39s → 7s, 10K updates, ~29M rows, delta 6.7s, OOM 14.4 GiB | MEASURED |
| 17.15M rows, 432.81 MiB, ~7.8× | MEASURED |
| ReplacingMergeTree / partition pruning validation | MEASURED POC + design |
| Production mutation framework fully rolled out | Do not overclaim: bake-off + architecture guidance |

---

## 8. Cross-cutting talking track (2-minute narrative)

"On AssortSmart I am building the agentic path: FastAPI owns chat (LangGraph/MCP); Go owns the doing layer so manual REST and agent tools hit the same Hindsight/Clustering/Strategy APIs against **ClickHouse/GCS**; Datadog, LangSmith, and PostHog share an OTEL trace id. Planning data is **ClickHouse end-to-end** via insert-only versioned writes — that is the Jul 2026 stack + HLD, unlocked after POCs showed classic OLTP mutations are the wrong CH model. Evidence we measured: on a **250M-row** pivot harness ClickHouse cut heavy grids from **189s to 12.3s** (~**15×** on DISTINCT option-count; honest typical aggregates ~**2–3×**), and line-planning refused to materialize **~12B** store-week rows via a **~25M** aggregate (**100–450×**). Legacy mtp-assort stays off wholesale CH — fix BigQuery first. Copilot targets under **1 hour** and under **2%** failures from measured **8.5%**; Phase 1 design approved, load test pending."

---

## 9. Rapid-fire Q&A (12+)

### Q1. Why ClickHouse over Postgres for this?

**A:** Columnar scans, partition pruning, and incremental MVs win on aggregation-heavy retail reads. We measured Order Batching at **23.7M** join rows: CH **3.86s** vs PG **3m40s–7m48s** (~**60×**). Inserts hit ~**5.9M** rows/s vs PG **250K** raw. PG stays SoT for transactional writes. At small scale (~57K) they are comparable: the cliff is large joins/aggs.

### Q2. Why not Druid or Pinot?

**A:** Our path was driven by existing CH investment, SQL familiarity for porting PG SPs, MergeTree family fit for CDC mirrors (ReplacingMergeTree), and operational simplicity for a handful of mirrored facts plus agentic decision tables. Pinot I have used elsewhere for ops dashboards; for this migration the team standardized on ClickHouse Cloud / CH-native DDL already in flight. I would reopen Druid/Pinot only if we needed their specific ingestion or concurrency characteristics and the org wanted a second OLAP stack: not for this POC scope.

### Q3. How does CDC handle updates and deletes?

**A:** On the platform CDC I integrated with: PG logical replication (`pgoutput`). An UPDATE is applied as CH **DELETE by PK + INSERT** of the new row (or insert of a newer version row into ReplacingMergeTree). Deletes set/apply delete semantics with `_cdc_deleted`. Truncates are parsed but **default not applied** to CH. Slot advances only after CH apply succeeds (apply-first).

### Q4. What is the cost of `ReplacingMergeTree` + `FINAL`?

**A:** RMT defers deduplication to background merges: cheap writes, eventually one row per key. `FINAL` forces merge-on-read so you see the latest version immediately, but it burns CPU/IO and scales poorly on huge unpartitioned scans. Prefer partition filters, `argMax`, or query shapes that avoid full-table `FINAL`. CDC and analytics should be designed so interactive paths prune first.

### Q5. How would you cut over safely?

**A:** (1) Fix lock atomicity on PG. (2) Stand up CDC mirrors; verify snapshot + drift. (3) Shadow-read: run CH queries in parallel, compare to PG (row counts + checksum samples). (4) Route a fraction of read SPs via the router with kill switch. (5) Keep Redis RYW. (6) k6 at 50 users on 11 read SPs; p95 must beat PG baseline. (7) Expand routing; keep PG write path untouched. (8) Hold rollback: router defaults back to PG in one config flag.

### Q6. What OOM failure modes did you see?

**A:** Full-table delta join on ~**29M** rows exceeded **14.40 GiB**. Order Batching "batch exploded" shaped query on **133.7M** rows in one partition crashed the server. Lesson: bound working sets with partition scope or compact deltas; never assume a join that works on 5M rows works when exploded 20×.

### Q7. How do you guarantee correctness between PG and CH?

**A:** PG is source of truth. CDC is at-least-once with RMT dedupe. Health checks for row-count drift (platform target ≤**0.5%** steady state). After writes, RYW forces the writer onto PG for **~30s**. For cutover, SP equivalence tests (same inputs, compare outputs) and shadow reads. I do not claim byte-identical every millisecond under lag: I claim bounded lag + explicit fallback + drift alarms.

### Q8. Benchmark fairness challenge: "your CH box was different"?

**A:** Agreed: and documented. PG was **32 vCPU / 256 GB** tuned; CH was **16 vCPU / 64 GB** untuned. That makes the CH wins **more** persuasive, not less, but I still call them POC-directional, not a perfect lab A/B. I also show the small-scale case where PG was slightly faster, so I am not hiding counter-evidence.

### Q9. Why CQRS instead of dual-write?

**A:** Dual-write splits failure domains: PG succeeds, CH fails (or vice versa), retries create duplicates, and lock/finalise semantics live in PG SPs today. CQRS keeps one writer, projects asynchronously, and uses Redis RYW to hide projection lag for the user who just saved.

### Q10. Why Redis TTL ~30s: why not 5s or 5 minutes?

**A:** Tuned to **typical CDC lag** under the platform SLO (p95 ≤ **10s** commit-to-visible) with margin for blips. Too short ⇒ users occasionally miss their own writes. Too long ⇒ writers keep hammering PG and you never shed load. 30s is the design default in the Order Batching architecture; it is a knob, not a law of physics.

### Q11. Why daily refresh for dims instead of CDC everything?

**A:** Product/store filters and DC reference data change rarely. CDC slots and worker threads are not free; daily full refresh is simpler and good enough for low-churn dims. Hot facts that change on every save get CDC.

### Q12. Copilot: can the agent write the cluster master?

**A:** No. Engine-enforced read-only profiles; write-back only after human approval gates. `is_optimal` never becomes `is_final` without a human signature. Phase 1 is design-approved; load test pending: I do not claim production autonomy.

### Q13. What does "14 audited tools" mean?

**A:** A fixed registry of templated tool calls (scope grounding, significance, candidate generation, scoring, comparison, pins/impact, etc.). The LLM selects and sequences them; it does not invent SQL. Every number in an evidence pack should be traceable to a tool call.

### Q14. How does elbow + silhouette interact with business guardrails?

**A:** Statistical k search runs inside client min/max and the child-cluster cap (default **10**, configurable). If the unconstrained optimum exceeds the cap, the agent picks the best k within the cap and records the constraint in the scenario summary (HLR-SC-004).

### Q15. What were insert concurrency differences?

**A:** CH hit ~**5.9M** rows/s with roughly **30** concurrent promos/connections. PG detach/attach baseline used **280** connections for ~**417K** rows/s. Higher aggregate throughput at far lower client concurrency: important when connection limits matter.

### Q16. Incremental MV vs PG refresh: one liner?

**A:** CH INSERT of 100K with MV ~**0.65s** vs PG full `REFRESH` ~**4s** over ~**1.69M** source rows: about **85%** faster incremental path, and CH stays fresh on insert instead of stale until manual refresh.

---

## 10. Numbers cheat sheet (flash card)

| # | Number | Context | Tag |
|---|---|---|---|
| 1 | 3.86s vs 3m40s–7m48s | Order Batching metric, 23.7M join rows | MEASURED |
| 2 | ~60× | Same | MEASURED |
| 3 | 5.9M vs 250K rows/s | Insert (also vs ~417K detach/attach → ~14–24×) | MEASURED |
| 4 | 30 vs 280 connections | CH vs PG insert concurrency | MEASURED |
| 5 | 607 → 26.4K rows/s (~43×) | Export path | MEASURED |
| 6 | 0.65s vs ~4s | CH MV insert vs PG full refresh | MEASURED |
| 7 | 39s → 7s | 10K updates on ~29M rows, partition scope | MEASURED |
| 8 | 6.7s / OOM 14.4 GiB | Delta join single partition vs full | MEASURED |
| 9 | 17.15M · 433 MiB · 7.8× | Fact compression | MEASURED |
| 10 | Redis TTL ~30s | RYW routing | MEASURED design |
| 11 | CDC p95 ≤10s · snapshot ≥25K/s | Platform SLOs | MEASURED (tool by other) |
| 12 | 8.5% (37/437) · ~20s median · 0% repro | Copilot baselines | MEASURED |
| 13 | <1h · ≥20 configs · <2% failures | Copilot targets | **TARGET** |
| 14 | 63 / 8 / 624 | Agentic CH schema | MEASURED design |
| 15 | 14 tools | Copilot tool registry | MEASURED design |
| 16 | 3–5 scenarios · elbow+silhouette | Clustering HLR flow | MEASURED PRD |
| 17 | PG 32vCPU/256GB vs CH 16vCPU/64GB | Hardware caveat | MEASURED |
| 18 | Grid <500ms · cell <80ms · HistOpt <30s · 3 scen <60s | Platform NFRs | **TARGET** |

---

## 11. Phrases to use / avoid

**Use:**
- "We measured…"
- "Design targets are…"
- "I designed the Order Batching CQRS migration against the platform CDC…"
- "Phase 1 design approved; load test pending…"
- "Hardware was not identical; CH was weaker and still faster…"

**Avoid:**
- "I built `pg2ch_cdc` end to end"
- "We fully cut over production Order Batching to CH" (unless you personally did)
- "Identical benchmark hardware"
- "Shipped the copilot to all tenants"
- Em dashes and hedged mush: speak in clean sentences with tags when needed

---

## 12. Suggested 45-minute drill order

1. Draw the ASCII architecture (5 min).  
2. Recite the 6 headline benchmark numbers + hardware caveat (5 min).  
3. Defend CQRS vs dual-write and Redis RYW (8 min).  
4. Walk update strategies 39s→7s + OOM story (7 min).  
5. Copilot flow + honesty (Phase 1 / TARGET vs MEASURED) (10 min).  
6. Rapid-fire from §9 (10 min).

---

*End of IA deep dive core. Mock interview Q&A below. All figures still trace to `GROUND_TRUTH.md` and the cited Confluence/PRD sources. If a number is not on this page, do not invent it in the interview.*

---

## Mock interview: hardest questions with answers

Format: skeptical engineering manager asks; candidate answers. Tags match `GROUND_TRUTH.md`. Do not soften TARGET into measured. No production cutover claim. Hardware for the insert/metric POC was not identical (PG 32 vCPU / 256 GB vs CH 16 vCPU / 64 GB).

### Q1. You say you are "building" AssortSmart with AI agents. What ships today versus what is design?

**A:** AssortSmart is the merchandise planning SaaS: retailers decide what to buy, in what depth, for which stores, a season ahead. Store clustering is the foundation every strategy plan binds to. The agentic rebuild inverts today's flow (four expert choices up front, one config run) into: planner states intent (hierarchy + reference period), the agent proposes scope and features, batch-explores configs, and a human approves before write-back. Phase 1 of the Cluster Recommendation Copilot is design-complete: four internal adversarial passes plus external review **PASS, approve to bring-up**. Bring-up load test is still pending. So I own present-tense design and build work, not a claim that every tenant already runs the shipped copilot in production.

### Q2. Why LangGraph instead of a plain function-calling loop in FastAPI?

**A:** Clustering is a multi-step stateful workflow: ground scope, confirm a search plan, fan out batch compute, stream scored candidates, pause for pins and what-ifs, then hit approval gates. LangGraph makes that graph explicit (nodes, edges, checkpointable state, human-in-the-loop interrupts) instead of burying control flow in ad-hoc `while` loops around chat messages. Plain function calling is fine for one-shot tool use; it gets brittle when you need durable session state, gate pauses that survive a reconnect, and the same graph driving both wizard Mode A and chat Mode B under the convergence rule (same config document, same gates, same write-back). Trade-off: more framework surface; payoff is auditable orchestration that matches product gates rather than prompt spaghetti.

### Q3. Why MCP on top of LangGraph? Isn't that two frameworks for one agent?

**A:** They solve different layers. LangGraph orchestrates *when* to call tools and *when* to stop for a human. MCP is the tool delivery contract: a fixed registry of **14 audited tools** lives behind an MCP server so the agent discovers schemas at runtime and cannot invent SQL. That decoupling matters for tenancy and ops: tool versioning, read-only enforcement, and reuse across clients without hardcoding tool implementations into the graph. Function-calling schemas alone would couple tool code to the orchestrator process. Trade-off: an extra process boundary and discovery handshake; payoff is a hard boundary between "LLM may select a tool" and "only these templated tools run."

### Q4. Walk the Cluster Recommendation Copilot. Where do the 20 to 100 configs and "under 1 hour" come from?

**A:** Today the pipeline evaluates **exactly 1** configuration the planner chose by hand, inside a search space of roughly 12 algorithms × k 3–10 × any attribute subset (MEASURED live audit). The FRD designs a pruned batch of **20–100** configs against an isolated scratch plan, with results streaming as they score; the headline product target is **≥20** configs evaluated per plan (TARGET). Hierarchy-to-finalized-plan **days → under 1 hour** is also TARGET, not a production measurement yet. Compute itself is already fast: median clustering job **~20s** over 370 live runs (MEASURED). The bottleneck is everything around the machine: blind expert choices, one shot, no reproducibility. UI still presents **3–5** distinct scenarios (HLR-SC-001 constraint); batch breadth under the hood is the 20–100 / ≥20 story. Say "targeting under 1 hour" and "batch evaluating 20 to 100 in design / ≥20 as the success bar."

### Q5. Failures 8.5% to under 2%, reproducibility 0% to 100%. Prove the baselines and stop claiming the targets as done.

**A:** On the kik tenant: **8.5% run failures (37 of 437)**; **>80%** of those are input mistakes at the data boundary (MEASURED). Winning algorithm, hyperparameters, and seed were never persisted ⇒ **reproducibility 0%** (MEASURED). Manual store swaps also die on re-run (0% survival). Targets are **failures under 2%** and **100% reproducible shipped clusterings** via content-addressed config documents (hash of recipe + data watermark) and append-only decision events (TARGET). Mechanism for the failure cut: deterministic grounding (catalog backtrack for hierarchy, fiscal calendar for seasons), sample-size guards, and machine-composed requests so the input-error class never reaches the engine. I will not say "we cut failures to under 2%" until post-load-test metrics exist. Correct phrase: "designed to cut from a measured 8.5% toward under 2%."

### Q6. Why only three human approval gates? Overview docs mention grounding, search plan, approval, and write-back.

**A:** The Phase-1 FRD product story is **three confirm gates** after intent: Gate 1 search plan (attributes + 20–100 config plan), Gate 2 approve the winning recommendation, Gate 3 governance sign-off where required; write-back then lands in today's tables. The grounding card is the confirm-what-was-understood step before compute (Mode B clubs cohort + attributes on that card). Module overview language lists grounding → search plan → approval → write-back as the consequential human stops. In the room I say: "Three product confirm gates plus write-back that never happens without an approved config; the agent physically cannot write." Resume "3 human approval gates" maps to the FRD's three confirms. If pressed on four stops, acknowledge grounding and write-back as the bookends without inventing a fourth numbered gate beyond the FRD.

### Q7. Why read-only agent tools at the database profile, not just a prompt that says "don't write"?

**A:** Prompts are not a control plane. The agent runs with a **read-only DB profile**; exploration writes only to isolated scratch plans; write-back is a separate path after human approval. That matches the FRD non-goal: no silent auto-finalize, and `is_optimal` (engine) never overwrites `is_final` (human). Schema reinforces it: **63 tables / 8 layers / 624 columns**, partition-swapped facts, append-only events, zero row-level mutations by doctrine (MEASURED design, DDL validated on ClickHouse 25.12). Failure mode if you skip this: an LLM tool that can `INSERT` into cluster master under prompt drift. Trade-off: new capability needs a new audited tool, not a prompt tweak.

### Q8. Why dedicated ClickHouse for agent probes instead of shared BigQuery?

**A:** Measured agent data-probe latency on shared BigQuery slots is **1–20s+** with uncontrolled variance (MEASURED live audit). Interactive copilot UX and platform NFRs need deterministic probes; design target is agent probe **p95 under 500ms** on a dedicated ClickHouse read plane (TARGET), with nightly precompute aiming to move **≥80%** of sessions cold→warm (TARGET). Feed is the org's existing BQ→CH ingestion lane (ItemSmart-proven pattern): BigQuery stays historical truth; agent load is isolated so ad-hoc probes do not burn shared slots. Cube reconciliation target within **0.1%** of BigQuery (TARGET). Explicit FRD non-goal: not moving transactional/plan data to ClickHouse for this module's Phase 1 read plane. Trade-off: a derived copy can rot; mitigate with owned ingestion, freshness sentinel, and data-as-of stamped on every recommendation.

### Q9. Why Go (Gin) for plan lifecycle and bulk save instead of keeping everything in Python FastAPI?

**A:** Service split is intentional. One Python microservice (FastAPI, LangGraph, MCP) owns agentic workflows that scale with LLM latency. The non-agentic core is throughput-shaped I/O: plan lifecycle CRUD (create/copy/finalize/soft-delete with server-side state transitions), reference data fan-out, and bulk save of versioned cell batches. Go gives goroutine-per-request concurrency without an async framework tax, a static binary, and boring code many engineers can touch. Gin: radix-tree router, middleware chain (`c.Next()`), `ShouldBindJSON` validation. Rejected fiber because fasthttp breaks standard `net/http` semantics; chi/Echo were fine but Gin won on team familiarity. JWT middleware carries tenant + role claims. Bulk save: bounded goroutine worker pool fans validated batches (design: version = epoch-ms, idempotency via batch id + content hash). This is **current build / stack direction**, not a MEASURED production RPS claim in ground truth. Do not invent peak RPS unless you label it estimated capacity from prep.

### Q10. Goroutine worker pools for bulk save: what problem, what failure mode?

**A:** A grid save arrives as a large batch of cell edits that must become one versioned insert wave, not N serial round-trips. A bounded worker pool (channel + N workers) caps concurrency into ClickHouse native batch inserts so you do not open unbounded goroutines under a save spike. Context timeouts cancel slow probes instead of piling up. Failure modes to own: goroutine leaks if cancel paths are missing; unbounded fan-out melting merge pressure on ClickHouse parts; retries without idempotency double-inserting versions. Mitigations: `context.WithTimeout` on every handler, pool size as a hard cap, batch id + content hash for safe replay, graceful `Shutdown` that drains in-flight work.

### Q11. Why ClickHouse over staying on PostgreSQL for the Order Batching analytics POC?

**A:** PostgreSQL is excellent OLTP; at multi-million join/agg scale it becomes the wrong engine for this read shape. We ported real workloads, not synthetic TPC. Order Batching metric at **23,749,263** join rows: ClickHouse **3.857s (~3.86s)** vs PostgreSQL **3m 40s** (UTC) / **7m 48s** (`Australia/Melbourne`) ⇒ about **~60×** (docs; range ~57–120× depending on TZ path) (MEASURED). At small scale (~57K join rows) PG was slightly faster (2.04s vs 2.80s), so we do not hide the parity case. Insert POC: CH **~5.91M rows/s** effective on **3.9B** rows (30 promos × 10M) vs PG **250K** raw / **~417K** detach-attach ⇒ **~14–24×**, and CH did it at **~30** connections vs PG **280** (MEASURED). Hardware caveat first: PG **32 vCPU / 256 GB** tuned; CH **16 vCPU / 64 GB** untuned. POC evidence, not production cutover.

### Q12. Why not Apache Druid or Pinot (or BigQuery directly) for that OLAP path?

**A:** For the Order Batching migration POC the team standardized on ClickHouse: SQL familiarity when porting PG stored procedures, MergeTree / ReplacingMergeTree fit for CDC mirrors, and existing CH investment / Cloud DDL already in flight. BigQuery remains upstream historical truth for agentic cubes, but shared-slot variance (**1–20s+**) fails the interactive agent-probe budget; dedicated CH is the gated read plane. Pinot I know from Uber-style high-QPS ops dashboards; Druid is strong at certain ingest/concurrency shapes. I would reopen Druid/Pinot only if we needed those specific characteristics and wanted a second OLAP stack. For this POC scope, a second engine was unjustified complexity. ReplacingMergeTree behavior matches our CDC apply pattern (versioned inserts, background dedupe; `FINAL` or `argMax` when latest-before-merge matters).

### Q13. Defend the 24× bulk load claim. How was throughput measured?

**A:** Effective rows/sec = `sum(expected_rows) / (max(ended) − min(started))` across successful parallel jobs, not the sum of per-job times. Best CH run: **30 promos × 10M = 3.9B** rows in **660.184s** ⇒ **5,907,446 ~5.9M rows/s** (MEASURED). Against PG raw **250K rows/s** that is **~23.6×** (resume rounds to **24×**). Against PG detach/attach **~417K** it is **~14×**. Resume "24× (250K to 5.9M)" is the raw-insert comparison; if challenged on detach/attach, cite both multiples honestly. Export path separately: PG **541s / 607 rows/s** vs CH **~38s / 26.4K rows/s** (~**43×** throughput) (MEASURED); note export row counts differed (~329K vs 1M), so defend rows/sec and wall methodology, not identical dump size.

### Q14. ReplacingMergeTree and partition updates: what broke, and why still CH?

**A:** ClickHouse mutations (`ALTER UPDATE`) are async and expensive for interactive planning; insert-only versioned rows fit both CDC and analytical rebuilds. On ~**29M**-row CARFG: full-table scope merge for **10K** updates sat **~35.6–38.8s**; partition-scoped merge on day partition `20260512` (~3.8M rows) finished in **7.309s** (MEASURED). Delta join on one partition **6.734s**; full-table delta **OOM at 14.40 GiB**. Exploded Order Batching query at **133.7M** rows in one partition crashed the server. Lesson: bound working sets; prefer partition swap / scoped merge over unbounded joins. `FINAL` forces merge-on-read for latest visibility but costs CPU/IO; prefer prune-first query shapes. Compression example (separate fact): **17.15M** rows, **432.81 MiB** compressed vs **3.31 GiB** raw (~**7.8×**) (MEASURED).

### Q15. CQRS for Order Batching: why not dual-write PG and CH in one request?

**A:** Dual-write splits the failure domain: PG commit succeeds, CH fails (or the reverse), retries create duplicates, and lock/finalise semantics live in PG stored procedures today. Design: PG remains system of record for writes (CARFG, locks, session save); CDC mirrors hot facts (CARFG, plan_master, dc_pack_reserve); low-churn dims refresh daily; router defaults reads to CH; after save/finalise Redis key `ob:ryw:{l0_name}` TTL **~30s** forces the writer onto PG for read-your-writes (MEASURED design). CDC platform SLOs I designed against / integrated with (tool authored by Ashvin Sharma, not me): commit-to-visible **p95 ≤ 10s**, snapshot **≥ 25K rows/s**. Apply CH first, then advance PG slot: at-least-once + ReplacingMergeTree dedupe. This is architecture + POC stage; do not claim full production cutover unless you personally cut over.

### Q16. Elbow + silhouette for k, but business wants actionable assortments. How do you not optimize the wrong objective?

**A:** HLR-AG-002: agent picks k via elbow + silhouette inside client min/max guardrails; HLR-SC-004 adds a default **max 10** child clusters per parent (configurable). If unconstrained optimum exceeds the cap, pick best k within the cap and record the constraint in the scenario summary. HLR-SC-001 caps UI scenarios at **3–5** with mandatory distinctness across lens, time horizon, store scope, and k; HLR-SC-003 always includes Baseline (Previous Plan) when one exists. Statistical fit is necessary but not sufficient; planner approval and pins inject business knowledge the dataset does not contain. That is why this is a gated decision agent, not AutoML that ships a loss minimum silently.

### Q17. What would make you discard the POC numbers in a design review?

**A:** Three things I already document. (1) Non-identical hardware: CH often weaker and still faster, so treat as directional, not lab-perfect A/B. (2) Small-scale parity: at ~57K join rows PG can win; the cliff is tens of millions of rows. (3) Methodology differences: export row counts differed; insert throughput is wall-clock effective across parallel jobs. Separately, ML fit median **~9s/config** is accepted physics (MEASURED); we parallelize and precompute around it rather than claiming we made the model faster. If load test on real kik extract fails cube sizing or p95 probe budgets, we revisit precompute and concurrency quotas before claiming agent latency targets.

### Q18. Ownership challenge: did you build `pg2ch_cdc` and ship the copilot?

**A:** No on both overclaims. `pg2ch_cdc` was authored by Ashvin Sharma; I designed Order Batching migration against its SLOs and mirror patterns and integrated with them. Copilot: Phase 1 design approved to bring-up; load test pending; L2 autopilot and L3 drift monitor are later phases. Correct ownership language: "designed / developing / designed against," not "I built the CDC platform end to end" or "shipped the copilot to all tenants."

---

## New POC + HLD mock interview (Jul 2026)

**Sources:** Pivot-Engine-Benchmark, LinePlanning-Benchmark, ClickHouse-vs-Postgres-POCs (consolidated v1.0), Agentic HLD (`final_agenticassort.png`).  
**Honesty rule:** Every number is tagged **MEASURED** / **TARGET** / **ESTIMATED**. Adversarial pass corrected first-pass magnitudes downward — defend the corrected figures, not the raw scoreboard. Hardware was deliberately PG-favorable (PG native **48 GB** host; CH **10 CPU / 3.3 GB** Docker VM) — MEASURED harness config.

---

### 1. Hybrid PG writes / CH reads (corrected magnitudes)

**Interviewer Q:** Your first slide said ClickHouse was 15× faster on the pivot and Postgres was 80–90× faster on cell edits. Then you walked it back to 2–3× and 14×. Which story is real, and why isn't this just "stay on Postgres"?

**Candidate A:** Both stories are real; the second is the one you should hire me for. We ran a controlled, row-identical harness at **5M / 50M / 250M** (MEASURED). Raw heavy-grid wall-clock at 250M: PG **189.4 s** with **42 GB** spill vs CH **12.3 s** ⇒ **~15.5×** (MEASURED). Adversarial re-measure showed ~**90%** of that gap is `COUNT(DISTINCT)` / option-count: PG's grouped distinct cannot parallelize and spills; CH runs parallel `uniqExact`. Strip the distinct and the CH lead collapses to **~2–3×** on typical aggregates (MEASURED, adversarial). Keep option-count (wireframe 1.1.1) and you honestly cite **~13–15×** (MEASURED). So: **2–3× typical, 13–15× only on DISTINCT grids** — that is the corrected pitch.

**Attack vector (recruiter/persona loop):** "Is 12B measured or projected?" — answer: combinatorial product from **4,800** stores × levels × choices × **52** weeks; flat loads at ~1B already OOM'd the **3.3 GB** CH VM (MEASURED). "Targeting vs shipped?" — under 1h / under 2% are TARGET; 8.5% and BQ 1–20s are MEASURED. "Two POCs one bullet?" — pivot and line-plan are different surfaces under one hybrid design rule.

On writes: raw single-cell edit cycle p50 at 250M was PG **0.94 ms** vs CH **~77 ms** ⇒ ~**82×** (MEASURED, untuned). ~**62 ms** of CH's cycle was CH 26.5's default `async_insert` buffer flush. With `async_insert=0` + fsync durability parity, CH drops to **~16 ms** ⇒ PG wins **~14×**, not 90× (MEASURED, adversarial). PG stays **sub-millisecond and scale-flat** across 5→250M (**0.35 → 0.94 ms**, MEASURED) — that is the interactive Wp-cell keyboard path. CH batch append inverts: at 250M / **156k** rows, PG **31,989 ms** vs CH **13 ms** ⇒ ~**2,500×** (MEASURED) — so bulk apply / reload belongs to CH.

**Design decision:** hybrid per surface, not a swap. Render grid / rollup / contribution-% from CH MergeTree sorted on pivot keys; authoritative cell write-back is keyed PG UPDATE; keep CH fresh via version-append into ReplacingMergeTree; after edit, either `argMax`/`FINAL` on CH or read just-edited cells from PG. Working POC: `GET /pivot` from CH, `POST /cell` → PG then mirror to CH RMT (MEASURED design, live against 250M harness).

**Tradeoffs:** two stores ⇒ sync lag + freshness window; CH pays **~4× FINAL** dedup tax when reading its own fresh parts (MEASURED). Storage first-pass **50–138×** was synthetic-modulo artifact; realistic high-entropy collapses to **~1.6–2.6×**, expect low-single-digits to **~10×** (MEASURED adversarial / ESTIMATED production band). Cheapest independent win: flatten JSONB fact — **2.06×** penalty on PG alone (**2,779 ms** flat vs **5,719 ms** JSONB, MEASURED); live Briscoes pivot **11.3 s** is mostly modeling, not PG's ceiling (MEASURED anchor).

**Why not "stay on Postgres"?** At Briscoes today **~5M**, selective screens still win on PG (MEASURED). At **250M** the heavy grid is **3m9s** and unusable for interactive planning (MEASURED). The recommendation must survive growth to multi-tenant **50–250M+**, not today's comfort zone. Decision rule: aggregates many rows → CH; mutates few cells with instant RYW → PG.

---

### 2. Why not wholesale ClickHouse for mtp-assort

**Interviewer Q:** You just proved CH wins big reads. Why did POC 4 still say "No to ClickHouse now" for the shipping mtp-assort app? Isn't that inconsistent with adopting CH for agentic clustering?

**Candidate A:** Consistent once you separate *surface* from *product*. mtp-assort's edit model is OLTP-mutable: keyed UPDATE, JSONB `||` merge, scoped delete-where-`plan_code` + reinsert, upsert, soft-delete. ClickHouse is append-first; its mutation queue is the wrong hammer for that write model. The analytical scans *look* CH-shaped, but the live cost drivers we measured are BigQuery hygiene problems, not "wrong OLAP engine": one job billed **38.8 TiB** via `SELECT *` / LIMIT with no date filter (MEASURED live BQ evidence, briscoes-01082024 / australia-southeast1); recurring full-category rollups re-scan **~2.9 TiB** (MEASURED). Fix tiers inside BQ: (1) kill `SELECT *`, force `require_partition_filter=TRUE`; (2) point heavy reads at already-clustered `_assort` (~**3×** cheaper, MEASURED free win); (3) materialize one store × category × fiscal-week rollup → MB instead of **2.9 TiB** (~**284×** less, MEASURED/ESTIMATED from that rollup sizing). Adding CH now creates a **third** engine (BQ + CH + PG) plus sync + dialect translation, replacing neither SoR nor the batch plane.

**Contrast — agentic clustering (POC 5):** greenfield read plane, new dedicated CH instance, writes still land in PG (cluster results must join strategy-flow tables). Decision dated **2026-07-06** (MEASURED design). Same hybrid principle applied forward: CH where determinism + interactive probes matter; PG remains SoR. Wholesale swap of mtp-assort fails the "replace neither" test; gated CH for a new module passes it.

**Tradeoff I own:** saying "no" to CH on the legacy app while saying "yes" to CH on the copilot looks political. The defense is workload shape: mutate-heavy legacy vs read-only analytical probes with insert-only BQ→CH feed.

---

### 3. Line-planning: why not materialize 12B store-week; aggregate + explode; partition of unity

**Interviewer Q:** KiK needs store-week. Your team already has `line_arch_store_week`. Why refuse to materialize **~12B** rows/plan? Isn't "derive on demand" just kicking the can — and won't explode latency kill allocation export?

**Candidate A:** **~12B** = **4,800** stores × final-levels × choices × **52** weeks per plan (MEASURED anchors / ESTIMATED combinatorial product for KiK). With **~50** plans, flat PG at rest is **~70 TB** (ESTIMATED from per-plan **~1.4 TB** × 50); even CH flat is **~1.1 TB** at 50 plans (ESTIMATED). Per operation: month view SUMs billions; a choice edit fires a **249,600**-row UPDATE on the flat path at the 10M-scale harness shape (MEASURED). At **100M** flat: month PG **2,923 ms** / CH **1,335 ms**; edit-one-choice PG **1,454 ms** / CH mutation **1,823 ms** (MEASURED). Projected to **12B**: flat month **~380 s** PG / **~160 s** CH; edits minutes (ESTIMATED linear projection — tagged PROJ in the POC).

**What we store instead:** editable truth at choice × cluster × week ≈ **~25M** for a 12B-flat plan (~**427×** smaller; MEASURED at 1B: flat PG **115 GB** vs agg **276 MB**). Formula (verbatim from `SCALE_LINE_ARCH_FROM_CHOICE_LAUNCH`):

```text
store_week = choice × flow_cluster_perc × cluster_store_perc × store_week_perc
```

Each percentage is a **partition of unity** (sums to 1 on its dimension), so `SUM(store-week) ≡ choice aggregate`. We reconciled `SUM(flat)==SUM(agg)` **to the cent** at **10M / 100M / 1B** on both engines (MEASURED). Explode one choice to store-week on demand in **~25 ms** (MEASURED). Month view on the **25M** aggregate: PG **690 ms** / CH **512 ms** (MEASURED at 25M = 12B-plan equivalent). Single-cell edit on aggregate PG **0.35–0.44 ms** (MEASURED) — scale-flat.

**Product reality check:** users never edit a dense store-week grid. Backend `update_line_arch_store_week_cluster_data` writes at cluster × choice × delivery; `line_arch_store_week` is 100% re-derived. Finer edits are **sparse overrides** (base + exception). Effective = `COALESCE(override, derived)`; rollup = aggregate_rollup + Σ(override deltas) — never scan 12B. Override point-upsert PG **0.15 ms** flat from **1M→50M** overrides (MEASURED); correction rollup at **1M** overrides: CH **5 ms** / PG **98 ms** (MEASURED). At **50M** overrides (0.4% of 12B — stress, not typical): PG correction **15.5 s** vs CH **52 ms** (MEASURED) — then AMT/SummingMergeTree earns its keep because deltas are additive.

**Tradeoffs:** if a downstream truly needs full store-week, materialize a **slice for export**, not the SoR. Trying to load **998M** flat into CH on the **3.3 GB** VM OOM-killed the container (MEASURED) — even columnar engines punish explosions you do not need. Schema first: flat→aggregate is **~140–200×** at 100M on read/edit (MEASURED), larger than any engine swap (**100–450×** band across scales, MEASURED/ESTIMATED). Multi-plan: partition by `plan_code`; single-plan month with 10 plans resident stays constant (PG **725 ms** / CH **33 ms**, MEASURED). Clone-plan: aggregate PG **67.7 s** / CH **0.85 s** vs flat ~**12 min** (MEASURED / ESTIMATED from 1B copy **60 s** ×12).

---

### 4. ClickHouse edit techniques: why not AMT for set-a-cell; RMT vs lightweight UPDATE vs EmbeddedRocksDB

**Interviewer Q:** ClickHouse 26.5 has lightweight UPDATE and AggregatingMergeTree. Why is your editable layer ReplacingMergeTree — and when would you actually use AMT or RocksDB?

**Candidate A:** Because a planner edit is **SET cell = X**, not **ADD delta**. AggregatingMergeTree / SummingMergeTree merge by summing states — the right tool for additive accumulation (override-delta rollups, pre-agg month views), the wrong tool for set-a-cell. Modelling SET as AMT forces compensating deltas — fragile under concurrent editors and undo.

**Measured bake-off at ~1B granular (MEASURED, CH 26.5):**

| Technique | Latency / behavior | Verdict |
|---|---|---|
| Heavyweight `ALTER UPDATE` (274M MT) | **1,618 ms** p50, consistent | Never for point edits — rewrites the part |
| Lightweight UPDATE (patch parts, experimental) | **4.4 ms** issue, RYW correct only **~11–22%** (consolidated) / ~**20%** (lineplan) | Unsafe for interactive write-back in 26.5 |
| ReplacingMergeTree append + `argMax`/`FINAL` | **~4.9–6.3 ms** tuned, consistent | Best MergeTree-family option for set-a-cell |
| EmbeddedRocksDB upsert + point get | **4.9 ms**, consistent, no parts/FINAL | Most PG-like KV editable layer; not for analytic scans |
| Postgres keyed UPDATE (reference) | **0.15–0.35 ms**, consistent | Nothing in CH family beats it |
| AMT as editable layer | — | ✗ wrong semantics (models "add") |
| AMT / Projection for *read* rollup over 1B | AMT **2 ms** (build **2 s**); Projection **4 ms** (build **30 s**) vs plain GROUP BY **2,058 ms** | Right when granular SoR must stay; ~**1000×** read win |

**CH floor:** ~**5 ms** is mostly HTTP round-trip + part creation (MEASURED / ESTIMATED split). So: interactive typing stays on PG (or EmbeddedRocksDB if you insist CH-native KV); pair RocksDB editable with MergeTree analytics. For editable aggregate in CH use **RMT(version)** — never AMT, never heavyweight mutation, avoid lightweight UPDATE until RYW is reliable. AMT belongs on **additive override-delta** MVs once override counts leave the human thousands–low-millions band where PG alone is already sub-100 ms (MEASURED design rule).

**Deeper point:** if you already stored the **~2M–25M** aggregate, plain GROUP BY is **~17 ms** (MEASURED on RMT aggregate) and you may not need AMT/projections at all. They earn keep when someone forces the 1B granular to remain SoR — which we refuse.

---

### 5. Agentic architecture: why FastAPI owns chat, Go is doing layer, dual Path A vs Path M

**Interviewer Q:** Why is chat FE → FastAPI directly? Why not put Go in front of everything like a normal BFF? And what are Path A and Path M actually for?

**Candidate A:** From the Jul 2026 Agentic HLD: **chat is FE → FastAPI directly; Go is not the chat gateway.** Two paths, one doing layer.

**Path A — agent chat (FastAPI Agent Service):**
1. **A1** Chat UI → `POST /chat` (routing, reasoning, tool selection).
2. **A2** Agent ↔ LLM (OpenAI / etc.) for reason / plan.
3. **A3** Tool call → Go doing layer when an action needs product APIs / deterministic compute.
4. **A4** Reply → Chat UI.

**Path M — manual work:** Manual screens → Go REST (`create` / `update` / `delete`) → same doing modules (Manual/REST, Hindsight, Clustering, Strategy) → ClickHouse / GCS. No LLM in the loop.

**WHY FastAPI owns chat:** agentic workflows are LLM-latency-shaped (LangGraph / MCP / prompt+tool loops, streaming tokens, run trees). Python owns that ecosystem; putting Go as a dumb chat proxy adds a hop without buying throughput. **WHY Go is the doing layer:** non-agentic work is throughput-shaped I/O — plan lifecycle, bulk saves, clustering/hindsight/strategy engines, CH/GCS access. Goroutine-per-request, static binary, boring code many engineers touch. Manual UI and agent tools **converge on the same Go APIs** (M1 and A3), so authorization, validation, and audit logic are not duplicated in the LLM path.

**Design decisions / tradeoffs:**
- Dual language is a real tax; accepted because the service boundary already existed (agent tier vs core backend).
- Agent never bypasses Go for mutations — tools call Go; DB profiles for agent probes stay read-only. Failure mode if skipped: prompt-drifted `INSERT` into cluster master.
- Notification service sits beside FE for core-api hits; not on the chat critical path.
- Do not claim MEASURED production RPS for this split — it is **MEASURED design / stack direction**. Scale story: agent replicas scale with LLM concurrency; Go replicas scale with request volume — independent axes.

**Adversarial push — "why not one Python monolith?"** Because Path M traffic (grid saves, strategy CRUD) should not share a GIL/async pool with multi-second LLM turns. Separating chat ownership from doing ownership is the load and blast-radius decision, not a fashion choice.

---

### 6. Observability split: LangSmith vs Datadog vs PostHog; shared OTEL `trace_id`

**Interviewer Q:** Three observability products is vendor sprawl. Why not one Datadog for everything? How do you debug "agent said X but Go returned Y"?

**Candidate A:** They answer three different questions; collapsing them loses signal.

| Layer | Tool | Owns | Emits from |
|---|---|---|---|
| L1 Agent quality | **LangSmith** | run trees, replay, evals, tokens, cost | FastAPI Agent Service (Agent → L1) |
| L2 Platform health | **Datadog** | HTTP/DB latency, errors, infra, Go doing-layer SLOs | Agent → L2 **and** Go → L2 (HTTP/DB) |
| Product analytics | **PostHog** | user behaviour (chat vs manual screens, funnel) | Frontend |

**Shared OTEL `trace_id`** stitches L1 ↔ L2: one planner utterance → LangSmith run tree (which tool, which prompt version, token/cost) ↔ Datadog spans (Go REST timing, CH query, GCS I/O). Without shared trace IDs you get two timelines that cannot be joined when the LLM "succeeded" but the tool timed out.

**WHY not Datadog-only for agents:** Datadog sees HTTP and infra; it does not natively give prompt replay, dataset evals, or token attribution the way LangSmith does for LangGraph runs. **WHY not LangSmith-only:** it will not page you on Go p99 or CH part merges. **WHY PostHog:** product questions ("did planners abandon chat for manual?") are neither span metrics nor prompt traces.

**Tradeoffs:** three bills, three UIs, discipline required to propagate `trace_id` on A3 tool calls into Go. Mitigation: OTEL middleware on FastAPI and Gin; reject tools that drop context. Alerting: Datadog pages on SLO burn; LangSmith feeds offline eval / regression; PostHog informs UX, not paging. This split is **MEASURED design** from the HLD — do not invent production MTTR numbers.

---

### 7. Slot-determinism: why dedicated CH vs BigQuery for agent probes

**Interviewer Q:** BigQuery is already your historical truth and you already pay for slots. Why stand up a dedicated ClickHouse just so an agent can run `SELECT`s?

**Candidate A:** Because interactive copilots need **deterministic** probe latency, and shared BQ STANDARD-edition slots make latency a function of **org-wide** load. Live audit of agent data-probe latency on shared BQ: **1–20 s+** with uncontrolled variance (MEASURED). Interactive UX + platform NFRs need agent probe **p95 < 500 ms** on a dedicated CH read plane (TARGET). Nightly precompute aims to move **≥80%** of sessions cold→warm (TARGET). Cube reconciliation within **0.1%** of BigQuery (TARGET). Feed = existing BQ→CH ingestion lane (ItemSmart-proven pattern, MEASURED design reuse). BQ stays historical truth; agent load is isolated so ad-hoc probes do not burn shared slots or surprise finance with another **TiB**-scanned job.

**WHY this is not a contradiction of "no CH for mtp-assort":** Phase 1 FRD non-goal — do **not** move transactional/plan data to CH for this module. Read plane only; PG remains editable SoR for cluster write-back after human gates. Greenfield schema + new instance ≠ swapping the mutation-heavy legacy app.

**Tradeoffs / failure modes:** derived copy can rot → owned ingestion, freshness sentinel, **data-as-of** stamped on every recommendation. If load test on real kik extract misses p95, revisit precompute and concurrency quotas before claiming the TARGET. Slot-determinism is the buying criterion; raw CH-vs-BQ scan benchmarks are secondary.

**One-liner under pressure:** "BQ is truth with shared-slot variance; dedicated CH is a deterministic probe cache for the agent — hybrid again, not a religion."

---

### Cross-cutting adversarial closes (use if they chain topics)

**Q: Your Jul 2026 stack note said ClickHouse end-to-end with insert-only versions. The POC report says hybrid PG writes. Which is it?**  
**A:** Both, at different scopes. The **POC consolidated verdict** is hybrid for *legacy assortment surfaces* and classic OLTP-mutable edits — and **no wholesale CH** for shipping mtp-assort (fix BQ first). The **agentic-assort** build follows the Jul 2026 stack directive + HLD: planning data on **ClickHouse/GCS end-to-end** because we changed the write model to insert-only versions (`mutations_used=0`). Thin Postgres metadata (auth/tenant/workflow) is fine to admit. I will not pretend CH beats PG at keyed UPDATE without that write-model unlock — that is exactly the mistake the adversarial pass prevents.

**Q: Give me the corrected number card only.**  
**A:** CH reads **~2–3×** typical; **~13–15×** on DISTINCT grids (MEASURED adversarial). PG single-cell **<1 ms** (**0.35–0.94 ms**, MEASURED). PG vs tuned CH write **~14×** (MEASURED). Schema flat→agg **100–450×** (MEASURED/ESTIMATED). Agent probes BQ **1–20 s+** MEASURED → CH **p95 <500 ms** TARGET. Storage real-world low-single-digits–**~10×**, not 50–138× (MEASURED adversarial).

---

## Confidence audit

| Resume bullet | Verdict | If pushed, say exactly |
|---|---|---|
| 1. Architecting AssortSmart; gated write-back | **SOLID** | Product framing + FRD non-goal (no silent auto-finalize). Present-tense; Phase 1 design PASS; not "already live for every tenant." |
| 2. Cluster Recommendation Copilot (FastAPI, LangGraph, MCP); 20–100 configs vs 1; days → under 1 hour | **NEEDS CARE** | Baseline **1 config/plan** MEASURED. Batch **20–100** is FRD design range; success bar **≥20** is TARGET. **Under 1 hour** is TARGET. Stack (FastAPI/LangGraph/MCP, 14 tools) is MEASURED design. "Developing / targeting," never "we already cut turnaround to under an hour in prod." |
| 3. Read-only tools + 3 human gates; 8.5% → under 2%; 100% reproducible | **NEEDS CARE** | **8.5% (37/437)** and **0% reproducibility** MEASURED. **Under 2%** and **100% reproducible** TARGET. Read-only profiles + gates MEASURED design. Phrase: "designed to cut failures from a measured 8.5% toward under 2%." Align "3 gates" with FRD confirm gates; mention grounding/write-back as bookends if asked. |
| 4. Go (Gin) microservices; manual REST + agent tools (Hindsight/Clustering/Strategy); Datadog + LangSmith + PostHog + OTEL | **NEEDS CARE** | HLD diagram design. Claim instrumentation model and dual Path A/M, not sole ownership of Datadog/PostHog/LangSmith products. |
| 5. ClickHouse/GCS end-to-end planning store; 250M 189s→12.3s (~15×); avoided 12B (100–450×) | **SOLID with care** | HLD + Jul 2026 stack = CH planning store (insert-only versions). Numbers MEASURED from POCs. Say **~2–3× typical** if they strip DISTINCT. Do **not** claim wholesale CH for legacy mtp-assort. If they wave the POC “hybrid” slide: that is decision history for OLTP mutations — agentic unlock was changing the write model. |

---

## Order Batching 60× (prep depth — replaced on resume headline)

Still MEASURED and interview-ready: 23.7M join rows, CH **3.86 s** vs PG **3m40s–7m48s**, insert **5.9M vs 250K rows/s**. Prefer leading with the Jul 2026 hybrid pivot/line-plan story on the resume; keep Order Batching as deeper evidence when asked "what else did you measure?"