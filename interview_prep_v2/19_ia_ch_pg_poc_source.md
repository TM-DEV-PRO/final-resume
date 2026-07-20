ASSORTMENT PLANNING · DATA PLATFORM · ENGINE EVALUATION

ClickHouse vs PostgreSQL — POC Report

A consolidation of the controlled benchmark POCs and live-data decisions run to answer one question: should the Assortment-Planning read/write surfaces move from PostgreSQL to ClickHouse? Every figure below was executed on row-identical data and verified adversarially — magnitudes are corrected down from first-pass, not headline-inflated.

Verdict: HYBRID, per surface — not a wholesale swap  ·  Prepared from executed harnesses (pivot-poc, lineplan) + live BQ/PG evidence  ·  v1.0

§ 0   Executive summary

Across four POCs — two controlled engine benchmarks and two live-data architecture decisions — the answer is consistent: use both engines, one per surface. PostgreSQL owns interactive edits and system-of-record writes; ClickHouse owns large analytical reads. Neither replaces the other, and the biggest lever is not the engine at all — it is the schema.

HEADLINE VERDICT

Writes / interactive cell edits → PostgreSQL. Sub-millisecond keyed UPDATE, scale-flat. ClickHouse has a ~5 ms floor (HTTP round-trip) and is part-creation bound; it is append-first, not edit-first.

Large analytical / full-grid reads at scale → ClickHouse. ~2–3× faster typically, up to ~13–15× when the grid needs COUNT(DISTINCT) (option counts) that spills to disk on Postgres.

The schema is the real lever. Redesigning flat → aggregate + distribution profile + explode/derive-on-demand is a 100–450× win — larger than any engine swap. Don't materialize combinatorial explosions.

Honest, adversarially-corrected magnitudes

First-pass numbers overstated ClickHouse's edge. After tuning both engines fairly and using high-entropy (non-synthetic) data, the directions all held but the magnitudes came down:

PG was given every hardware advantage (48 GB host); CH ran constrained (10 CPU / 3.3 GB Docker VM). The corrections make the case against the constrained engine — i.e. conservative.

WHERE EACH POC LANDED

PG  Pivot benchmark — hybrid per surface; writes to PG, grid reads to CH; use-case 1.1.1 runs better on PG today.

PG  Line-planning benchmark — don't materialize the 12B store-week; store the small editable aggregate on PG, derive on demand; CH for cross-plan rollups.

PG  mtp-assort (existing app) — No to ClickHouse now; the real cost drivers are cheaper to fix inside BigQuery.

CH  Agentic clustering (new module) — ClickHouse chosen for the runtime read surface; writes still land in PG. This is where CH earns its place.

§ 1   Test harness & methodology

Both benchmarks used the same controlled rig, deliberately biased toward PostgreSQL so any ClickHouse advantage is a floor, not a ceiling.

Row-identical data across engines — aggregate fingerprints match; at 250M the float-derived sums reconcile to 2e-12.

Real-schema anchor — data modeled on the live assort_smart.line_plan_choice_launch_ia layout, not toy tables.

Adversarial verification — every headline magnitude was attacked and re-measured; overstatements were corrected downward before publication.

Reproducible harnesses live in POC/pivot-poc/ (SQL, generators, benchmark scripts, an 11-endpoint FastAPI service) and POC/pivot-poc/lineplan/.

§ 2   POC 1 — Assortment pivot engine benchmark

The dominant Assortment-Planning surface is the pivot grid (choice × cluster × fiscal-week, measures joined to product dims). We benchmarked reads, writes and storage at 5M / 50M / 250M rows.

Reads (warm median wall-clock, ms)

R1 CH advantage ~13–15× (option-count spills PG). R2 flips: PG wins at 5M (1.8×), CH wins at 250M (18.5×). R3/R4 widen from ~2.5× to ~10× with scale.

Writes

PG single-cell is scale-independent (0.35→0.94 ms). The raw ~82–216× gap shrinks to ~14× against a tuned CH (~16 ms). CH batch-append instead widens with scale (12× → 2,520×). CH also carries a FINAL read-tax (~4× with multiple parts).

Storage & modeling

The 54–138× is synthetic-favorable. Real-world anchor (briscoes PG ~5.3 GB vs arhaus CH ~112 MB, ~5M rows) ≈ 47×; high-entropy data collapses this to ~1.6–2.6×. JSONB modeling penalty = 2.06× (fact_flat 2,779 ms vs fact_json 5,719 ms); the live briscoes pivot at 11,298 ms is mostly modeling, not PG's ceiling. Bulk reload (5M): PG 19.3 s vs CH 6.0 s = 3.2×.

POC 1 VERDICT

Hybrid, per surface. ClickHouse for grid/aggregate reads at scale; PostgreSQL for interactive cell write-back. The advantage is real but not a landslide — CH reads ~2–3× typical (~13× on distinct-counts); PG writes ~14× vs a tuned CH.

§ 3   POC 2 — Pivot POC (wireframe views 1.1.1 / 1.1.2 / 1.1.3)

To validate the benchmark against real product interactions, we built a working POC — schema h111, 5.76M rows, an 11-endpoint FastAPI service (hindsight_api.py on :8090) serving all three wireframe views with live read grids + Wp write-back. Full artifact in POC/pivot-poc/.

CROSS-VIEW FINDING

Writes (Wp cells, thresholds) → PostgreSQL at every scale (sub-ms, scale-flat). Full-grid reads → ClickHouse at every scale (widening to 13–15×). Selective reads → PostgreSQL while small, flipping to ClickHouse as they grow. So 1.1.1 — today's dominant surface — runs better on Postgres; the ClickHouse case is the cross-cutting analytical views plus catalog growth.

§ 4   POC 3 — Line-planning benchmark (store-week explosion)

The Line-Planning module's line_arch_store_week explodes to ~12B rows per plan for KiK (4,800 stores) — and ~50 plans exist. We benchmarked month-view reads + cell/choice edits, PG vs CH and flat-table vs a redesigned schema.

THE KEY INSIGHT — PARTITION OF UNITY

Store-week is a deterministic explosion of the choice aggregate: store_week = choice × flow_cluster_perc × cluster_store_perc × store_week_perc, where the percents sum to 1. So SUM(store-week) ≡ choice aggregate (reconciled to the cent at 10M/100M/1B on both engines). The editable truth is choice × cluster × week — ~25M rows for a 12B-flat plan, ~427× smaller. Store-week is derived on demand (~25 ms to explode one choice) and never materialized for editing. Users already edit at cluster × choice × delivery; there is no store-level edit path — finer edits are sparse per-week/per-store overrides.

Reads, edits & storage — flat vs aggregate

Aggregate is ~140–457× faster to read than flat. 12B-flat is infeasible on PG (~2–4 TB/plan); flat editing is bad on both engines (PG bulk UPDATE of 249,600 rows; CH part-rewrite mutation). @50 plans: flat PG ~70 TB / CH ~1.1 TB vs aggregate PG ~155 GB / CH ~940 MB.

ClickHouse technique deep-dive (@1B granular)

Multi-plan & sparse overrides

Multi-plan is a storage-at-rest problem, not a per-op one. Users edit one plan at a time → single-plan read is constant regardless of N (partition-pruned: PG 725 ms / CH 33 ms). Must PARTITION BY plan_code.

Clone-plan: aggregate PG 67.7 s / CH 0.85 s vs flat ~12 min/plan. Cross-plan portfolio rollup (rare, no pruning): PG 13.3 s / CH 0.19 s.

Sparse overrides (per-week/per-store exceptions, 0.008–0.4% of a 12B plan): point-upsert WRITE PG 0.15 ms flat / CH ~2 ms. Correction rollup grows on PG (98 ms → 15.5 s at 50M) but deltas are additive → pre-aggregate with SummingMergeTree/AggregatingMergeTree. Table stays MB-scale — the 12B is never materialized.

POC 3 VERDICT

The schema (flat → aggregate + distribution profile + explode-on-demand, plus base + sparse-override) is the 100–450× lever, not the engine. Writes → Postgres (sub-ms keyed UPDATE, scale-flat). Big rollup reads → ClickHouse (or PG at the aggregate's ~25M size, already sub-second). For an editable aggregate in CH use ReplacingMergeTree(version) — never AggregatingMergeTree (it sums states, wrong for set-a-cell), never heavyweight mutation, and not lightweight UPDATE (unreliable in 26.5).

§ 5   POC 4 — mtp-assort (existing app): should we move to ClickHouse?

Beyond the synthetic benchmarks, we evaluated the live existing application against real BigQuery + Postgres evidence (briscoes-01082024, australia-southeast1). The question: does the shipping mtp-assort backend belong on ClickHouse?

The edit model is fundamentally OLTP-mutable — keyed UPDATE, JSONB merge (||), scoped delete-where-plan_code + reinsert, upsert, soft-delete. ClickHouse (append-first, non-keyed async mutations) cannot replace this.

The analytical scans are ClickHouse-shaped, but the real cost drivers — SELECT * / LIMIT with no date filter (one job billed 38.8 TiB), recurring full-category rollups re-scanning ~2.9 TiB — are cheaper to fix inside BigQuery.

ClickHouse would become a third engine (BigQuery + CH + PG + sync + dialect translation), replacing neither.

POC 4 VERDICT — NO, NOT NOW

Fix it in BigQuery instead, in three tiers: (1) kill SELECT * and force a date filter (require_partition_filter=TRUE); (2) point heavy reads at the already-clustered _assort table (~3× cheaper, free win); (3) materialize one store × category × fiscal-week rollup → MB instead of 2.9 TiB (~284× less). ClickHouse only makes sense later if a high-concurrency, sub-second interactive BI product emerges.

§ 6   POC 5 — Agentic clustering (new module): where ClickHouse wins

For the greenfield Agentic Assort clustering module, the calculus is different — and this is where ClickHouse earns its place. The decision (2026-07-06) was to serve the entire runtime read surface (including clustering-job feature pulls) from a new dedicated ClickHouse instance.

Rationale = slot-determinism. BigQuery's shared STANDARD-edition slots make latency depend on org-wide load; a dedicated ClickHouse gives deterministic response and near-zero marginal probe cost — exactly what an interactive, agentic copilot needs.

Writes still land in PostgreSQL. Cluster results must join the strategy-flow tables, so the system of record stays PG; ClickHouse is the read/analytics plane only.

Greenfield schema, new instance, reusing an existing BQ→CH ingestion pipeline. This is a new build with an analytical read plane, not a swap of a transactional system.

POC 5 VERDICT — YES, FOR THE READ PLANE

The same hybrid principle, applied forward: ClickHouse for the analytical/interactive read surface of a new module where determinism matters; PostgreSQL remains the system of record for edits. This is the natural conclusion of the benchmark arc — CH is adopted exactly where the POCs said it belongs.

§ 7   Consolidated recommendations

DESIGN RULES THAT OUTRANK THE ENGINE CHOICE

1. Schema first. Flat → aggregate + distribution profile + explode/derive-on-demand is 100–450×. Never materialize a combinatorial explosion (store-week, full grids) for editing.

2. Base + sparse override. Store the derived base as a formula; persist only the exceptions; effective = COALESCE(override, derived). Keeps 12B-row plans at MB scale.

3. If you do put an editable layer in ClickHouse: ReplacingMergeTree(version) for set-a-cell edits; AggregatingMergeTree/SummingMergeTree only for additive rollups & override-deltas; EmbeddedRocksDB for a PG-like KV path; Projection/AMT for read rollups; never heavyweight ALTER UPDATE; avoid lightweight UPDATE until read-after-write is reliable.

Bottom line: the engine debate is real but secondary. Run PostgreSQL and ClickHouse side by side, each on the surface it wins — and invest first in the schema, which pays more than either engine ever could.


### Table 1

DIMENSION | FIRST-PASS CLAIM | HONEST, CORRECTED FIGURE

Aggregate / pivot reads | up to 138× | CH ~2–3× typical; ~13–15× only on COUNT(DISTINCT) grids that spill on PG

Single-cell write-back | 90–283× (PG faster) | PG ~14× vs a tuned CH (async_insert=0+fsync → ~16 ms); raw gap was CH 26.5's untuned insert buffer

Storage compression | 50–138× (CH smaller) | low single digits to ~10× on realistic high-entropy data; the 50–138× was a synthetic-modulo artifact

Batch / bulk writes + reload | CH wins | Held — CH append beats PG in-place UPDATE, widening with scale


### Table 2

ENGINE | CONFIGURATION | RESOURCING

PG  PostgreSQL 14 (native) | 12 GB shared_buffers, 512 MB work_mem, 8 parallel workers; indexed + hash-partitioned facts | 48 GB host — every hardware advantage

CH  ClickHouse 26.5 (Docker) | MergeTree family; tuned variants (async_insert, ReplacingMergeTree, AggregatingMergeTree, Projection, EmbeddedRocksDB) tested explicitly | 10 CPU / 3.3 GB VM — constrained


### Table 3

WORKLOAD | 5M PG | 5M CH | 50M PG | 50M CH | 250M PG | 250M CH

R1 · heavy grid + contrib% + option-count | 3,859 | 280 | 35,132 | 2,708 | 189,408 | 12,256

R2 · selective drill (1 subclass × cluster) | 2.8 | 5.0 | 30 | 4.8 | 170 | 9.2

R3 · wide pivot (channels → columns) | 175 | 73 | 1,726 | 650 | 29,235 | 2,963

R4 · top-N treemap | 155 | 59 | 1,475 | 535 | 27,635 | 2,522


### Table 4

WORKLOAD (PG / CH) | 5M | 50M | 250M

W1 · single-cell edit cycle, p50 (ms) | 0.35 / 75.6 | 0.77 / 68.5 | 0.94 / 77.2

W2 · batch block edit (ms) | 503 / 40 | 3,338 / 18.5 | 31,989 / 12.7

W5 · concurrent 8-thread (edits/s) | 633 / 37 | 1,066 / 37 | 970 / 38


### Table 5

SCALE | PG FLAT | PG JSONB | CH MERGETREE | CH SMALLER BY

5M | 937 MB | 2,285 MB | 17.5 MB | ~54×

50M | 9,334 MB | — | 173 MB | ~54×

250M | 46 GB | — | 341 MB | ~138×


### Table 6

VIEW | INTERACTION | WINNER & CROSSOVER

1.1.1 Hindsight-Item | One subclass slice + Wp cell edits (the dominant interaction) | PG  wins both — read 7.9× (1.3 ms vs 10.3 ms), write large. CH only wins the full-cluster cross-subclass slice (4.5×). Crossover ~50M.

1.1.2 Hindsight-Attribute | Read-only attribute pivot + z_other threshold bucketing | Selective reads flip to  CH  ~250M (z_other collapses output to ~10 rows).

1.1.3 Thresholds | Bounded config write | PG  — write is scale-independent; 250M is synthetic/irrelevant here.


### Table 7

OPERATION | FLAT PG | FLAT CH | AGGREGATE PG | AGGREGATE CH

Month READ @100M | 2,923 ms | 1,335 ms | 21 ms | 6.4 ms

Month READ @1B | 31,510 ms | — | 69 ms | —

Month READ @25M (=12B plan) | — | — | 690 ms | 512 ms

EDIT one choice @1B | 4,618 ms | 1,823 ms | 9–13 ms | ~60–70 ms

EDIT single cell | — | — | 0.35–0.44 ms | ~6 ms

Storage @1B | 115 GB | 1.87 GiB | 276 MB | ~ tens MB


### Table 8

TECHNIQUE | MONTH-ROLLUP READ | EDIT ONE VALUE | VERDICT

Plain MergeTree GROUP BY | 2,058 ms | — | Baseline

AggregatingMergeTree (sumState MV) | 2 ms | — | ~1000× on reads; but models "add", not "set = X"

Projection | 4 ms | — | Best read path — transparent, same SQL auto-routes

ReplacingMergeTree (FINAL) | 17 ms | 6.3 ms (tuned) | Right for editable/set-a-cell aggregate

Flat mutation (ALTER UPDATE) | — | 10,000 ms | Never — rewrites the part

Lightweight UPDATE (26.5) | — | 4.4 ms | Read-after-write unreliable (~11–22% correct) — unsafe

EmbeddedRocksDB (upsert) | — | 4.9 ms | Most PG-like editable layer; no parts, no FINAL

PG  keyed UPDATE (reference) | — | 0.15–0.35 ms | Nothing in the CH family beats it; ~5 ms CH floor is HTTP


### Table 9

SURFACE | ENGINE | WHY

Interactive cell / Wp write-back, config writes | PostgreSQL | Sub-ms keyed UPDATE, scale-flat; CH has a ~5 ms floor and is part-creation bound

System of record / transactional edits | PostgreSQL | OLTP-mutable model (upsert, JSONB merge, soft-delete) that CH cannot express

Large full-grid / aggregate reads at scale | ClickHouse | ~2–3× typical, up to ~13–15× on COUNT(DISTINCT) grids that spill on PG

Cross-plan / portfolio rollups, analytical read plane | ClickHouse | No partition pruning needed; CH wins by ~70× on unpruned scans

Existing BigQuery-backed batch workload | Fix in BQ | Cheaper to fix SELECT*/clustering/rollups in place than add a third engine