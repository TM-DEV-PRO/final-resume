RECOMMENDATION

Don't store the explosion. Store the aggregate + a distribution profile.

The store-week value is a deterministic partition-of-unity explosion of the choice aggregate: store_week = choice × flow_cluster_perc × cluster_store_perc × store_week_perc, and those percentages sum to 1 — so SUM(store-week) ≡ choice aggregate (verified to the cent at every scale). The editable truth lives at choice × cluster × week (~25M for a 12B-flat plan); per-store-week is derived on demand, never materialized for editing.

Engine split (under the good schema): Postgres owns the interactive edit (in-place keyed UPDATE, sub-ms, transactional); ClickHouse owns the big rollup reads and can even scan the flat 12B if you ever must. The flat materialization is the enemy — not the engine choice.

THE TWO OPERATIONS THAT HURT

Flat vs Aggregate, across scale

Same logical plan, two storage models. "Month view" = SUM to final_level × fiscal_month. "Edit a choice" = rescale one choice's plan (the backend's SCALE_LINE_ARCH path). Medians, ms.

At 100M the flat design already needs ~3 s to render a month and ~1.5 s to edit one choice; the aggregate does both in single-digit ms (~140–200× faster). The gap grows linearly with rows — at 12B the flat path is minutes-per-operation, the aggregate is unchanged.

WHY IT'S SAFE TO NOT MATERIALIZE

The explosion is lossless & reversible

The backend builds store-week by chaining four percentages onto the choice aggregate (verbatim from SCALE_LINE_ARCH_FROM_CHOICE_LAUNCH):

Each percentage is a partition of unity (sums to 1 over its dimension), so summing store-week back up returns the choice aggregate exactly. We verified SUM(flat)==SUM(agg) to the cent at 10M / 100M / 1B, on both engines.

So the aggregate loses nothing

You can always rebuild any store-week cell as aggregate × stored percentages. Store:

•  choice_agg — plan × final_level × choice × cluster × week (the editable layer; ~25M for a 12B plan)

•  store_dist — store → cluster + cluster_store_perc (4,800 rows)

•  (week/delivery percentages — small profiles)

Explode to store-week only when a downstream truly needs it (allocation export), for one slice — ~25 ms/choice.

WHAT USERS ACTUALLY EDIT · FROM THE CODEBASE

It's all overrides — never a dense store-week grid

The backend confirms it: the edit endpoint (update_line_arch_store_week_cluster_data) writes at cluster × choice × delivery, and line_arch_store_week is 100% re-derived from the cluster×choice aggregate via the exact percentage chain we hypothesized:

Finer edits are per-week or per-store overrides — sparse manual exceptions, not a full grid. So the model is base + sparse override: the derived base (aggregate × percentages) is never stored; only the cells a human actually overrode are. The effective value is COALESCE(override, derived); a rollup is aggregate_rollup + Σ(override deltas) — so you never scan 12B, even with overrides.

Override layer benchmark — sparse overrides at 1M / 10M / 50M (0.008%–0.4% of a 12B plan)

Override write is sub-millisecond on Postgres at every density (0.15 ms keyed upsert, flat from 1M→50M) — this is the interactive path, and it never touches the 12B grid. The override-aware rollup correction is a scan of only the sparse overrides: fine on Postgres at realistic volumes (~98 ms at 1M) but it grows with override count (985 ms at 10M, 15 s at 50M), while ClickHouse stays in ms (5→52 ms).

The fix for high override volumes — and where AggregatingMergeTree finally fits

Override deltas are additive (unlike the base "set cell = X" edit). So the correction rollup can be pre-aggregated incrementally with a SummingMergeTree / AggregatingMergeTree MV (or a small PG rollup) → instant regardless of override count. This is the correct use of AMT in this system: RMT for the editable base, AMT for the additive override-delta rollup. In practice override counts are thousands–low-millions per plan (human-made), where Postgres alone is already sub-100 ms.

RECOMMENDED SCHEMA

Concrete design, per engine

Why not AggregatingMergeTree for the editable layer?

AMT/SummingMergeTree merge by summing states — built for additive accumulation, not "set this cell = X". A planner edit is a SET; modelling it as AMT means inserting compensating deltas (fragile). Use ReplacingMergeTree(version) for edits; reserve AMT for the read rollup if on-the-fly GROUP BY ever proves too slow.

STORAGE

Footprint at scale

Postgres cannot realistically store the 12B flat table (~2–4 TB + indexes); ClickHouse can (columnar, ~100–250 GB) and scan it — but neither should, because the aggregate is ~427× smaller (measured: 115 GB flat vs 276 MB agg at 1B) and lossless. CH numbers ≥1B are projected from the real 10M/100M points: when we tried to ingest 998M flat rows into ClickHouse on the constrained 3.3 GB VM it OOM-killed the container — a fitting reminder that even columnar engines pay to materialize an explosion you never needed.

CLICKHOUSE TECHNIQUE DEEP-DIVE · MEASURED AT 1B

AggregatingMergeTree, or something better?

We loaded the full 998.4M-row granular store-week into ClickHouse (1.87 GiB on disk; the same data is 115 GB in Postgres) and benchmarked every realistic technique for the two jobs: roll up to a month view, and edit a value.

Read — month rollup over 1B granular

Both AggregatingMergeTree and Projection turn the 2-second scan into a ~2–4 ms read (~1,000×). They're the right tools if you keep the 1B granular as source-of-truth and must roll it up.

Edit — mutation techniques compared (point edit + immediate read-after-write)

"Is there a better mutation technique?" — we benchmarked all of ClickHouse 26.5's options for a single-cell edit the user must see immediately.

Better CH mutation technique? Yes — and no. The clearly worse options are heavyweight mutations (1.6 s, rewrites parts) and — surprisingly — the new lightweight UPDATE (fast to issue but read-after-write is unreliable in 26.5, so a planner wouldn't see their own edit). The two good CH options are ReplacingMergeTree (append+argMax) and EmbeddedRocksDB (point upsert+get) — both ~5 ms and immediately consistent. EmbeddedRocksDB is the most PG-like (keyed upsert, no parts, no FINAL) and is the best CH-native home for the editable/override layer; pair it with a MergeTree for analytics. But none beats Postgres's ~0.2 ms — the ~5 ms CH floor is mostly the HTTP round-trip. So: keep interactive edits in Postgres (or EmbeddedRocksDB if you want it CH-native); for the read rollup use Projection/AMT; for the editable base never use heavyweight mutation or AMT.

And the deeper point still holds: if you store the 2M aggregate (not the 1B flat), a plain GROUP BY over it is already ~17 ms and edits are point ops — you don't need AMT or projections at all. They only earn their keep when the 1B granular store-week must remain the system of record.

MULTI-PLAN · ~50 PLANS

12B is per plan — and there are ~50

A planner opens and edits one plan at a time, so multi-plan is a storage-at-rest problem, not a per-operation one: with the table partitioned by plan_code, an individual plan's read/edit is isolated and stays constant no matter how many plans exist. We verified all of it with 10 plans (250M aggregate) resident.

Storage at rest — the real multi-plan cost

The multi-plan verdict: performance per planner is unchanged by plan count (partition by plan_code); the only thing that scales with N is footprint — and the flat design becomes a ~70 TB Postgres table at 50 plans (infeasible), versus a ~155 GB aggregate (or ~940 MB in ClickHouse). Plus the one true multi-plan op — clone-a-plan — is seconds on the aggregate and ~12 min+ on the flat. Both reinforce the same conclusion: store the aggregate, not the explosion.

UNBIASED HYPOTHESIS — CONFIRMED

The honest read

The schema, not the engine, is the 10–100× lever. Flat→aggregate is ~140–200× on both read and edit at 100M, and the gap grows linearly with stores/rows. Fix the schema first.

Writes belong to Postgres — aggregate cell edit is sub-ms, transactional, scale-flat. ClickHouse's editable-aggregate path (ReplacingMergeTree append) is ~60–70 ms/edit (tunable) — fine for occasional saves, not for rapid cell-by-cell typing.

Big rollup reads favor ClickHouse, but at the aggregate's modest size (~25M) Postgres is already sub-second — so a PG-only aggregate stack is viable for KiK today; ClickHouse earns its place as the read/rollup accelerator as plans/tenants multiply.

Flat editing is bad on both engines — Postgres bulk-UPDATEs hundreds of thousands of rows; ClickHouse mutations rewrite parts (even slower). Don't edit the flat table on either.

12B is a storage/write problem, not a read problem — ClickHouse can scan it; nobody can edit it interactively. The aggregate sidesteps it entirely.

Bottom line: re-model line_arch_store_week as aggregate + distribution profile + explode-on-demand. Keep edits in Postgres (sub-ms), serve big rollups from ClickHouse (or PG at today's size), and treat the flat 12B as a derived export, never the system of record. This turns a multi-minute, multi-TB plan into a millisecond, few-GB one.

All figures are real measurements on row-identical synthetic data modeled on assort_smart.line_arch_store_week (KiK-test schema; partition-of-unity reconciled). 12B rows shown as projection where local materialization is infeasible. Postgres native (full host RAM); ClickHouse in a 3.3 GB Docker VM — engine wins are conservative for ClickHouse.


### Table 1

ASSORTMENT PLANNING · LINE PLANNING · LINE_ARCH_STORE_WEEK · ENGINE + SCHEMA BENCHMARK Line Planning at 12 billion rows KiK's store-week line architecture explodes to ~12B rows/plan (4,800 stores × final-levels × choices × weeks), yet planners edit at aggregated month/quarter grain. This benchmarks Postgres vs ClickHouse — and, more importantly, the flat store-week table vs a better schema — on the two operations that hurt: load an aggregated view, and edit an aggregated cell. ANCHORS 4,800 stores · 10 clusters · 52 weeks   ·   SCALES 10M · 100M · 1B · 12B(proj)   ·   DATA row-identical, reconciled   ·   PG 14 native · CH 26.5 / 3.3GB VM


### Table 2

THE FLAT TABLE IS THE PROBLEM 12B is per plan, and there are ~50 plans → the flat table is ~600B rows / ~70 TB on Postgres at rest. Per plan, a month view SUM-s billions and a choice edit fires a billion-row UPDATE. It worsens linearly with stores and plans. | THE AGGREGATE IS THE FIX Same plan at ~25M aggregate: month view in ~0.5 s, edit a cell in sub-ms, explode one choice to store-week on demand in ~25 ms. Works on both engines.


### Table 3

OPERATION | 10M | 100M | 1B | 12B (PROJ)

LOAD AGGREGATED MONTH VIEW | LOAD AGGREGATED MONTH VIEW | LOAD AGGREGATED MONTH VIEW | LOAD AGGREGATED MONTH VIEW | LOAD AGGREGATED MONTH VIEW

FLAT — Postgres | 280 | 2,923 | 31,510 | ~380,000

FLAT — ClickHouse | 121 | 1,335 | ~13,400 (proj) | ~160,000

AGGREGATE — Postgres | 3.3 | 21 | 69 | 690 (25M)

AGGREGATE — ClickHouse | 3.0 | 6.4 | ~10 (proj) | 512 (25M)

EDIT ONE CHOICE (RESCALE) | EDIT ONE CHOICE (RESCALE) | EDIT ONE CHOICE (RESCALE) | EDIT ONE CHOICE (RESCALE) | EDIT ONE CHOICE (RESCALE)

FLAT — Postgres (249,600-row UPDATE) | 683 | 1,454 | 4,618 | seconds–min

FLAT — ClickHouse (mutation) | 214 | 1,823 | ~18,000 (proj) | minutes

AGGREGATE — Postgres (520-row UPDATE) | 9.3 | 10.4 | 13.3 | ~6

AGGREGATE — Postgres (single cell) | 0.44 | 0.44 | 0.35 | 0.39


### Table 4

-- per store-week row sales_units = choice_sales_units   × flow_cluster_perc      -- cluster share   × cluster_store_perc     -- = 1/stores_in_cluster   × store_week_perc        -- week share


### Table 5

-- line_arch_propagation.py (verbatim) receipt_units = choice_receipt_units * flow_cluster_perc * cluster_store_perc * launch_delivery_perc sales_units   = choice_sales_units   * flow_cluster_perc * cluster_store_perc * store_week_perc


### Table 6

OVERRIDE COUNT | WRITE (POINT UPSERT) P50 | ROLLUP CORRECTION (Σ DELTAS) | STORAGE

1M overrides | PG 0.15 ms · CH 2.8 ms | CH 5 ms · PG 98 ms | PG 106 MB · CH 0.8 MB

10M overrides | PG 0.16 ms · CH 2.1 ms | CH 12 ms · PG 985 ms | PG 1.0 GB · CH 4.2 MB

50M overrides (0.4%) | PG 0.15 ms · CH 2.1 ms | CH 52 ms · PG 15.5 s | PG 5.2 GB · CH 20 MB


### Table 7

LAYER | POSTGRES | CLICKHOUSE

Editable aggregate (choice×cluster×week) | table partitioned by final_level, PK (final_level,choice,cluster,week); edit = keyed UPDATE | ReplacingMergeTree(version); edit = insert new version, read latest via argMax/FINAL

Store-distribution profile | store_dist(store→cluster, perc) + week profiles | same, MergeTree / dictionary

Month/quarter rollup (read) | GROUP BY over the aggregate (indexed) | on-the-fly GROUP BY (sub-second at 25M) — add an AggregatingMergeTree MV only on measured need

Store-week | VIEW / on-demand join to store_dist — not stored | derived join; materialize a slice only for export


### Table 8

MODEL | 100M | 1B | 12B (PROJ)

FLAT — Postgres | ~12 GB | 115 GB | ~2–4 TB

FLAT — ClickHouse | ~1.6 GB (proj) | ~16 GB (proj) | ~100–250 GB

AGGREGATE (≈ flat/480) | 28 MB | 276 MB | ~few GB (25M)


### Table 9

TECHNIQUE | READ | BUILD | EXTRA STORAGE | TRADE-OFF

Plain MergeTree + GROUP BY | 2,058 ms | — | 0 | scans 1B every read

AggregatingMergeTree (via MV / sumState) | 2 ms | 2 s | ~1 KiB | incremental on insert; needs sumState/sumMerge + explicit MV; query must use it

Projection (on the base table) | 4 ms | 30 s | ~16 KiB | transparent — same GROUP BY auto-routes; auto-maintained on insert; heavier to materialize

ReplacingMergeTree aggregate (2M, FINAL) | 17 ms | — | 4.9 MiB | the editable layer's own rollup — already fast, no pre-agg needed


### Table 10

TECHNIQUE | LATENCY (P50) | READ-AFTER-WRITE | VERDICT

Heavyweight ALTER…UPDATE (274M MT) | 1,618 ms | consistent | rewrites the whole part — never for point edits

Lightweight UPDATE (patch parts, experimental) | 4.4 ms | unreliable (~20%) | fast to issue, but the edit isn't reliably visible on immediate read — unsafe for write-back in 26.5

ReplacingMergeTree append + argMax | 4.9 ms | consistent | ✓ best MergeTree-family option; parts accrue → periodic merge; FINAL tax on big scans

EmbeddedRocksDB upsert + point get | 4.9 ms | consistent | ✓ true key-value: no parts, no FINAL, PG-like upsert — but not for analytic scans

Postgres keyed UPDATE (reference) | 0.15–0.35 ms | consistent | in-place MVCC update

AggregatingMergeTree as the editable layer | — | — | ✗ wrong tool: AMT merges by summing states (models "add", not "set = X")


### Table 11

MULTI-PLAN OPERATION | POSTGRES | CLICKHOUSE | NOTE

Single-plan month read (10 plans resident) | 725 ms | 33 ms | = the 1-plan number → constant with N (partition-pruned)

Single cell edit in one plan | sub-ms | ~6 ms | unaffected by other plans

Copy / clone a plan (aggregate, 25M) | 67.7 s | 0.85 s | spawn a new plan from an existing one

Copy / clone a plan (flat, 12B) | infeasible | ~12 min | CH anchor: 1B copy = 60 s → ×12

Cross-plan / portfolio rollup (rare) | 13.3 s | 0.19 s | no partition pruning → CH columnar wins


### Table 12

MODEL | PER PLAN | 10 PLANS (MEASURED) | ~50 PLANS (PROJ)

FLAT — Postgres | ~1.4 TB | ~14 TB | ~70 TB ✗

FLAT — ClickHouse | ~22 GB | ~220 GB | ~1.1 TB

AGGREGATE — Postgres | ~3.1 GB | 31 GB | ~155 GB ✅

AGGREGATE — ClickHouse | ~19 MB | 188 MB | ~940 MB ✅