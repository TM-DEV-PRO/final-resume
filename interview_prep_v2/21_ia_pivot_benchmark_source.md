RECOMMENDATION

Run the pivot as a hybrid, not a swap.

Neither engine wins outright — the workload splits cleanly. ClickHouse owns every read / aggregate / pivot and crushes storage; Postgres owns the interactive single-cell write-back by two orders of magnitude. The right design serves the grid from ClickHouse and keeps cell edits authoritative in Postgres — exactly the split the existing MTP backend already half-implements (BigQuery reads + Postgres OLTP).

The decision rule: if a surface aggregates many rows → ClickHouse. If it mutates a few cells and must read them back instantly → Postgres. The pivot needs both, so it needs both engines. (Headline magnitudes below are raw measurements; an adversarial pass corrected them — see Verification.)

WHO WINS WHAT

Scoreboard

Measured at 250M rows (current Briscoes is ~5M; the recommendation must survive growth). Magnitudes are medians of repeated warm runs — raw figures; the adversarial pass corrects several downward (CH reads ~2–3× typical, PG writes ~14× tuned, storage low-single-digits realistic).

THE READ CLIFF

The heavy pivot grid, across scale

The same query — pivot grid with contribution-% and option-count, joined across hierarchy, cluster, and calendar. Bars are log-scaled wall-clock; ClickHouse stays interactive while Postgres falls off a cliff.

5M rows

██████████████████  PG 3.86 s

████████████  CH 0.28 s

ClickHouse 13.8× faster

50M rows

██████████████████████  PG 35.1 s

█████████████████  CH 2.71 s

ClickHouse 13.0× faster

250M rows

██████████████████████████  PG 189 s · 42 GB spilled to disk

████████████████████  CH 12.3 s

ClickHouse 15.5× faster — Postgres is now unusable for an interactive grid

At 250M the Postgres pivot takes 3 minutes 9 seconds and spills 42 GB of sort files to disk. ClickHouse answers the same question in 12 seconds on a 3.3 GB VM. Even the “selective drill” — Postgres’s one early win at 5M — flips to a ClickHouse win (18.5×) once each subclass holds more SKUs.

THE WRITE SPLIT

Why Postgres still owns the keyboard

A planner tabbing through Wp cells does single-row edits and expects the value back instantly. That is the one thing a columnar append-store is built to be bad at — and the one thing a row store is built to be great at.

Single-cell edit cycle (p50)

5M

██  0.35 ms

████████████████  76 ms

50M

██  0.77 ms

███████████████  68 ms

250M

███  0.94 ms

█████████████████  77 ms

Postgres is sub-millisecond and flat with scale (indexed point update). ClickHouse is ~70–100 ms because each edit creates a new part + read-modify-write + dedup-on-read.

Batch block edit (one subclass×cluster)

5M·3k rows

██████████  503 ms

█████  40 ms

50M·31k

███████████████████  3,338 ms

████  18 ms

250M·156k

██████████████████████████  31,989 ms

███  13 ms

Inverts the story: ClickHouse append stays flat while Postgres in-place UPDATE scales with row count — CH ends up ~2,500× faster for bulk edits and reloads.

Implication: single-cell edits → Postgres; “apply +10% to a whole subclass”, rollups, and full reloads → ClickHouse. The write side is also a split, not a one-engine answer.

STORAGE & THE MODELING TRAP

Two findings that reframe the question

Storage: ClickHouse is ~50× leaner

Honest caveat (from verification): this synthetic data is wildly compressible — with realistic high-entropy measures, ClickHouse’s ratio collapses from 83.7× to ~1.6–2.6×. Postgres is genuinely not bloated (157.6 B/row = theoretical min). Expect a real-world storage edge of low-single-digits to ~10×, not 50× — still meaningful, not magical.

The 11-second query is mostly a modeling bug

The live Briscoes pivot takes 11.3 s on Postgres — but most of that is the JSONB layout, not Postgres itself. Same logical pivot, same data:

2.06× penalty just from JSONB extraction per row. Flattening the fact is the cheapest win available — independent of any ClickHouse decision.

HOW THIS WAS KEPT HONEST

Methodology & fairness

Fair-model vs fair-model

Row-identical data. Same deterministic row→(choice,cluster,week) mapping in both engines; aggregate fingerprints match exactly (250M float-derived sums agree to 2×10⁻¹²).

Each engine’s best physical model. Postgres: flat, partitioned by week, indexed. ClickHouse: MergeTree sorted on the pivot keys. The slow JSONB layout is reported separately, not as “Postgres”.

Realistic shape. The grid joins fact × hierarchy × cluster × calendar and computes contribution-% windows — not a toy single-table scan (joins are where ClickHouse is supposedly weak).

Postgres got every advantage

Postgres ran native on the host with 48 GB RAM, 12 GB shared buffers, 8 parallel workers, fast local NVMe.

ClickHouse was boxed in a 10-CPU / 3.3 GB Docker VM — and still won every read.

So the read wins are conservative; the Postgres-favorable findings (write-back, point reads) get full credit.

Warm medians over repeated runs; the 250M heavy grid run once (it takes minutes on PG).

Engines provisioned fresh and isolated for this study — the shared ClickHouse (Arhaus / ItemSmart) and read-only Briscoes Postgres were used only as real-world anchors, never as the head-to-head.

WHAT THE CURRENT BACKEND DOES — AND WHAT TO FIX

Reusing the existing pivot

The MTP AssortSmart backend already runs a de-facto hybrid: it aggregates the heavy “hindsight” grid in BigQuery (GROUP BY + window contribution-%) and keeps plan state + write-back in Postgres (in-place keyed UPDATE, JSONB merge, TRUNCATE+COPY syncs). The pivot’s row/column rotation is largely shaped by the GROUP BY + the front-end, not a SQL PIVOT.

Keep

The read/write split is already correct in spirit. Write-back as keyed Postgres UPDATE is the right primitive and matches this benchmark’s winner.

Optimise

(1) Flatten the JSONB fact → 2× immediately. (2) Put the interactive pivot on a ClickHouse MergeTree refreshed from the plan store, instead of paying BigQuery latency/cost per grid. (3) Replace per-row UPDATE loops + full TRUNCATE+COPY with block appends.

RECOMMENDED ARCHITECTURE

The hybrid pivot, concretely

A working POC of exactly this runs against the live 250M dataset: GET /pivot builds the grid from ClickHouse with contribution-%; POST /cell writes the edit to Postgres (authoritative) and mirrors it to the ClickHouse ReplacingMergeTree. The edited cell reads back correctly from both within one request.

The cost of hybrid (don’t gloss over it)

Two stores means a sync path and a freshness window between the Postgres edit and the ClickHouse copy. For a single editor this is invisible; for the grid’s correctness it must read the ClickHouse copy with dedup (argMax/FINAL) or read the just-edited cells from Postgres. This is the one real operational tax of the recommendation.

ADVERSARIAL VERIFICATION

We tried to break our own conclusions

Independent skeptics ran counter-tests against the live 250M engines to refute each headline. They confirmed every direction — but caught three overstated magnitudes. The honest, corrected picture:

Net: the recommendation (CH for reads/scale, PG for interactive write-back) holds — but the honest magnitudes are ClickHouse ~2–3× on typical aggregates (up to ~13× when grids include distinct-counts) and Postgres ~14× on tuned single-cell writes (not the eye-popping 90–283× from untuned defaults). The decision is real but less lopsided than raw numbers suggest.

THREE REAL USE CASES AT SCALE

Views 1.1.1 / 1.1.2 / 1.1.3 — where the verdict flips, and when

We built three actual wireframe screens end-to-end (schema, API, row-identical data at 5.76M / 50M / 250M) to test the recommendation on real surfaces. The split is consistent — but the read crossover point depends on the screen.

Full-cluster (cross-subclass) reads are ClickHouse at every scale on both views, widening to 13–15× at 250M. The selective read flips later when its output stays small (1.1.2’s threshold bucketing collapses to ~10 rows → Postgres holds to ~250M; 1.1.1 fetches thousands of rows + joins the growing product dim → flips at 50M).

The honest cross-view read: writes belong to Postgres at every scale (sub-ms, flat). Reads belong to ClickHouse for anything cross-cutting, and for selective screens once they grow — the crossover is 50M (1.1.1) to ~250M (1.1.2), set by output size + joins, not the engine. At Briscoes’ current ~5M, the selective screens still run fine on Postgres; the ClickHouse case is the full-grid views and the road to 50M+. Pick the engine per surface, not per product.

THREATS TO VALIDITY

Where these numbers could mislead

Synthetic data is compression-friendly. The 138× storage ratio at 250M is optimistic; trust the ~47–54× real-world anchor.

ClickHouse single-row write latency can be tuned. async_insert / buffering narrows it — but at the cost of read-after-write immediacy, which is the whole point of write-back. (See adversarial.)

The 5M “present” is small for OLAP. At today’s scale Postgres-only is survivable (4 s grid); the case for ClickHouse is about where Briscoes is heading (50–250M+ multi-tenant), where the grid becomes unusable on Postgres.

Contribution-% / option-count drive the gap. COUNT(DISTINCT) spills hard on Postgres; it’s a real wireframe measure, so it stays — but a pre-aggregated rollup narrows specific grids.

APPENDIX

Full results & reproducibility

Postgres 14.21 native (shared_buffers 12 GB, work_mem 512 MB, 8 workers). ClickHouse 26.5 in Docker (10 CPU / 3.3 GB). Fact grain: choice × cluster(8) × fiscal_week(52); measures flat float8/Float64; dims joined for the grid. Bulk reload (5M, 324 MB CSV): PG 19.3 s vs CH 6.0 s.

Benchmark executed on row-identical synthetic data modeled on assort_smart.line_plan_choice_launch_ia . All figures are real measurements from this run, not estimates. Postgres deliberately over-resourced and ClickHouse deliberately constrained, so engine wins are conservative in ClickHouse’s favor and generous to Postgres where it leads.


### Table 1

ASSORTMENT PLANNING · PIVOT FUNCTIONALITY · ENGINE BENCHMARK Postgres vs ClickHouse for the pivot grid A controlled, row-identical head-to-head across read, write-back, and storage — built to answer one question without bias: which engine should power the assortment-planning pivot, and at what scale. SCALES 5M · 50M · 250M rows   ·   DATA row-identical, fingerprint-verified   ·   PG 14.21 native · 48 GB host   ·   CH 26.5 · 10 CPU / 3.3 GB VM   ·   STATUS all numbers executed


### Table 2

CLICKHOUSE HANDLES   The pivot grid, rollups, contribution-%, treemaps, hindsight scans, bulk reloads. ~2–3× faster on typical aggregates (up to ~13× when grids include distinct-counts), far leaner storage, and the gap widens with scale. | POSTGRES HANDLES   Interactive cell edits / write-back and plan state. ~14× faster single-cell edit cycle (vs a tuned ClickHouse; ~90× vs its untuned default), transactional, sub-millisecond, instant read-after-write.


### Table 3

HEAVY PIVOT GRID · READ ● ClickHouse Group-by + contribution-% + option-count over the full fact, joined to hierarchy / cluster / calendar. 15.5× faster | SINGLE-CELL WRITE-BACK · WRITE ● Postgres Edit one Wp cell → persist → read it back. The core planning interaction. ~82× faster

STORAGE FOOTPRINT ● ClickHouse Same rows, columnar + compressed vs row-store + indexes. ~50–138× smaller | BULK / BATCH WRITE ● ClickHouse Append a whole edited block or reload the fact (the sync path). 3×–2,500× faster

CONCURRENT CELL EDITS ● Postgres 8 planners editing at once — MVCC row updates vs part-creation. ~26× higher throughput | READ-AFTER-WRITE CORRECTNESS ● Postgres CH pays a ~4× FINAL dedup tax to read its own fresh edits. instant & exact


### Table 4

SCALE | PG FLAT+IDX | CLICKHOUSE | RATIO

5M | 937 MB | 17.5 MB | 54×

50M | 9.3 GB | 173 MB | 54×

250M | 46 GB | 341 MB | 138×


### Table 5

POSTGRES LAYOUT | TIME

Flat numeric columns | 2,779 ms

JSONB measures (today’s table) | 5,719 ms


### Table 6

PATH | ENGINE | MECHANISM | WHY

Render grid / rollup / contribution-% | ClickHouse | MergeTree, sorted on pivot keys | 10–18× faster, 50× smaller, scales

Edit a Wp cell (write-back) | Postgres | keyed in-place UPDATE | sub-ms, transactional, exact read-back

Keep grid fresh after edits | ClickHouse | version-append → ReplacingMergeTree | cheap append; dedup on read

“Refresh rollup” / batch apply / reload | ClickHouse | INSERT…SELECT block append | 3×–2,500× faster than PG bulk UPDATE


### Table 7

CLAIM | VERDICT | WHAT THE REFUTATION FOUND

CH wins heavy read ~13× | HOLDS | Reproduced at 250M against PG's best flat layout (query-log proves CH scans all 249.6M rows, no caching). ~90% of the 13× is one thing: PG's grouped COUNT(DISTINCT) (Option Count) can't parallelize, while CH runs parallel uniqExact. Strip the distinct → CH lead is ~2–3× (pure columnar scan). 1.1.1's grid includes Option Count, so the larger figure applies to it; a PG rollup can't materialize around distinct (non-additive).

PG wins single-cell write ~90× | OVERSTATED | ~62 ms of CH's 77 ms was the untuned async_insert buffer-flush (CH 26.5 default). With async_insert=0 + fsync durability parity, the CH cycle drops to ~16 ms → PG wins ~14×, not 90× (still a clear PG win, still correct read-after-write).

Storage CH ~50–138× | OVERSTATED | PG is not bloated (157.6 B/row = theoretical minimum). But the synthetic measures are wildly compressible: with realistic high-entropy data, CH compression collapses from 83.7× to ~1.6–2.6×. Real-world advantage is low-single-digits to ~10×, not 50×.

Architecture should be hybrid | HOLDS* | The read/write split is real and survives tuning; hybrid stands. *Caveat: a tuned ClickHouse narrows both gaps, so a ClickHouse-only design (async_insert off, ReplacingMergeTree) is more viable than the raw numbers implied — at the cost of read-after-write complexity and concurrency (tuned CH still ~6.5× below PG on concurrent edits).


### Table 8

INTERACTIVE READ (THE SELECTIVE SLICE) | 5.76M | 50M | 250M

1.1.1 item grid (rows fetched + product join) | PG 5.5× | CH 3.8× | CH 4.3×

1.1.2 attribute grid (z_other → ~10 rows out) | PG 10× | PG 6.2× | CH 2.0×


### Table 9

WRITE-BACK | 5.76M | 50M | 250M

1.1.1 Wp cell edit (p50) — PG / CH | 0.25 / 69 PG | 0.83 / 76 PG | 0.75 / 71 PG

1.1.3 threshold edit (p50) — PG / CH | 0.21 / 66.6 ms → PG ~300×, scale-independent (config table; 250M not meaningful) | 0.21 / 66.6 ms → PG ~300×, scale-independent (config table; 250M not meaningful) | 0.21 / 66.6 ms → PG ~300×, scale-independent (config table; 250M not meaningful)


### Table 10

WORKLOAD (WALL-CLOCK MS UNLESS NOTED) | 5M PG | 5M CH | 50M PG | 50M CH | 250M PG | 250M CH

READS | READS | READS | READS | READS | READS | READS

Heavy grid + contrib% + option-count | 3,859 | 280 | 35,132 | 2,708 | 189,408 | 12,256

Selective drill (1 subclass×cluster) | 2.8 | 5.0 | 30 | 4.8 | 170 | 9.2

Wide pivot (channels→columns) | 175 | 73 | 1,726 | 650 | 29,235 | 2,963

Top-N treemap | 155 | 59 | 1,475 | 535 | 27,635 | 2,522

WRITES | WRITES | WRITES | WRITES | WRITES | WRITES | WRITES

Single-cell edit cycle (p50) | 0.35 | 76 | 0.77 | 68 | 0.94 | 77

Batch block edit | 503 | 40 | 3,338 | 18 | 31,989 | 13

Concurrent 8-thread (edits/sec) | 633 | 37 | 1,066 | 37 | 970 | 38

CH FINAL read-tax (×) | — | 4.2× | — | 4.2× | — | 4.1×

STORAGE / FOOTPRINT | STORAGE / FOOTPRINT | STORAGE / FOOTPRINT | STORAGE / FOOTPRINT | STORAGE / FOOTPRINT | STORAGE / FOOTPRINT | STORAGE / FOOTPRINT

Fact size on disk | 937 MB | 17.5 MB | 9.3 GB | 173 MB | 46 GB | 341 MB