# Impact Analytics Deep Dive: Bullet-by-Bullet Interview Defense

**Role:** Senior Software Engineer · Impact Analytics, Bangalore · 14 May 2026 – Present  
**Project:** Agentic AssortSmart Platform & PostgreSQL → ClickHouse Data Migration  
**Sources of truth:** `GROUND_TRUTH.md`, resume `experience.tex` IA bullets, ClickHouse POC dump, Agentic Cluster docs, AssortSmart clustering HLR v1.1  
**Honesty rule:** Every number below is tagged MEASURED / TARGET / ESTIMATED / design-only. Do not invent. Hardware for insert/export POC was **not** identical.

---

## 0. Role framing (30-second open)

I joined Impact Analytics as a Senior Software Engineer on 14 May 2026. My charter sits at the intersection of two workstreams:

1. **Data platform:** quantify where PostgreSQL breaks on retail OLAP workloads, then design a CQRS migration that keeps transactional writes on Postgres and moves aggregation-heavy reads to ClickHouse.
2. **Agentic product:** design the Cluster Recommendation Copilot for AssortSmart so an LLM orchestrates while a deterministic plane computes, with human approval before any write.

I am an IC so far (no people lead at IA). CDC platform tooling (`pg2ch_cdc`) was authored by another engineer (Ashvin Sharma). I designed Order Batching migration against it and integrated with its SLOs and mirror patterns. The Cluster Recommendation Copilot is Phase 1 design approved (external review PASS); bring-up load test is still pending.

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

## 5. Resume bullet 2: PostgreSQL vs ClickHouse benchmarks

> Benchmarked PostgreSQL vs ClickHouse on production retail workloads. The Order Batching metric over 23.7M joined rows ran in 3.86s on ClickHouse vs 3m 40s+ on PostgreSQL (60x), parallel bulk loads sustained 5.9M rows/sec vs 250K rows/sec, and query to CSV export throughput improved 43x (607 to 26,400 rows/sec).

### 5.1 Exact story with numbers (memorize these)

All MEASURED from POC docs. Infra was **not** identical.

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
- **Gotcha:** resume says **60x** and **3m 40s+**: defend with both PG times (3m40s UTC and 7m48s TZ) and CH **3.86s**.
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

"PostgreSQL is fine for transactional Order Batching writes and locks, but at tens of millions of join rows the analytical metric path goes to minutes. We proved ClickHouse on real workloads: about **60×** on the Order Batching metric at **23.7M** join rows, about **14–24×** insert throughput, about **43×** export rows/sec, even though CH had half the vCPUs and a quarter of the RAM and was untuned. From that evidence I designed a CQRS migration: PG remains system of record for writes, CDC mirrors hot facts into ReplacingMergeTree, dims refresh daily, and Redis gives a **30s** read-your-writes window so planners still see their own saves. Separately, on update strategy, partition-scoped merges cut **10K** updates on a **~29M** row table from **~39s** to **~7s**, and we documented OOM modes for naive full-table deltas. On the product side I am building toward the Cluster Recommendation Copilot: LangGraph/MCP agent, **14** tools, deterministic clustering, human gates, targeting under **1 hour** plans and under **2%** failures from a measured **8.5%** baseline: Phase 1 design approved, load test pending."

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

*End of IA deep dive. All figures trace to `GROUND_TRUTH.md` and the cited Confluence/PRD sources. If a number is not on this page, do not invent it in the interview.*
