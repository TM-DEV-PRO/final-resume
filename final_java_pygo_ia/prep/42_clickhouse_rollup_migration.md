# ClickHouse rollups and cluster copy (PDF P4 / P5)

**PDF:** `Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf` · Canonical: [`docs/ASSORTSMART_TAB_RESUME.md`](../../docs/ASSORTSMART_TAB_RESUME.md)

Interview-depth notes for the six rollup tables, the weekly `INSERT SELECT` OOM, and the Go copier. Snapshot of measured numbers: 8 Sep 2026 (generated SQL, pipeline comments, migrate checkpoints, live copy logs). If a figure is an estimate, say so.

**Do not** paste cluster passwords, hosts, or `.env` into interviews, GitHub, or commits. **Do not** open-source the copier. Whiteboard the design. KPI configurator is a different bullet (`P2`). Isolation is `P3`. These two are **P4** (pre-agg / OOM) and **P5** (pump).

<div class="callout warn">
<b>Split the jobs.</b> 15.5x pivot is request-time (250M harness). The 170 GB OOM is write-time (whole-season weekly GROUP BY). The Go pump is a Cloud to Cloud copy, not the reason pivots got faster.
<b>4.09B</b> is attr weekly, two seasons, one table. Not “all weekly rollups.” Copy of that set was measured in flight, not a finished cutover.
<b>64.1M</b> half-loaded partition is the POC <b>loader</b>, not the copier.
<b>100% Go coverage / 1,200+ tests</b> is still true, now <b>LinkedIn / verbal</b> (off this PDF).
<b>1.6M article-seasons</b> is still true catalog (product x season). Off this PDF for space. Say it if asked.
PDF does <b>not</b> name remoteSecure. You may explain the allowlist workaround if they ask why a laptop pump.
</div>

---

## PDF lines (memorize)

**P4.** Reduced planner pivot latency by 15.5× (189s to 12s on 250M-row operations) by building a ClickHouse pre-aggregation layer for season and weekly rollups. Prevented 170GB OOM crashes by slicing batch inserts into temporal chunks and enforcing strict distributed memory and disk-spill caps.

**P5.** Migrated ClickHouse rollups across Cloud clusters at ~344k rows/s by writing a custom Go native-TLS data pump to bypass strict cross-cluster IP allowlist restrictions. Processed partitions up to 4.09B rows using 500k-row double-buffered batches, and eliminated partial-commit ghost rows using TSV ledgers and atomic partition rollbacks.

PDF names allowlists and TSV on P5. Verbal knobs for P4: one fiscal week, 55 GB, 16 GB spill. In the loop still split: TSV = weekly loader. Copier = `.done`. Partition rollback = `DROP PARTITION` then recopy, not a live reader swap. 4.09B copy was in flight.

XYZ for P2: X = serve planners from pre-aggregated rollups. Z = 15.5x, 189s to 12s on 250M, plus surviving weekly builds after ~170 GB OOM. Y = six tables, one fiscal week per INSERT SELECT.

XYZ for P5: X = copy season-partitioned rollups between Cloud clusters. Z = about 344k rows/s combined, largest source object 4.09B attr weekly (two seasons). Y = Go native TLS, 500k columnar batches, double buffering, season checkpoints, DROP PARTITION replay.

---

## Six tables (draw this first)

Daily source is SKU x store x date. Planners cannot GROUP BY that on every chart. You pay once at load and read six MergeTree tables, all `PARTITION BY season_code`:

| Grain | Product (SKU dims) | Store (no SKU, two-pass totals) | Attr (unpivot, about 5x product weekly) |
|---|---|---|---|
| Season | product_season | store_season | attr_season |
| Weekly | product_weekly | store_weekly | attr_weekly |

Build order that ran: product then store then attr, per grain. Kik vs Briscoes is not a rename (hierarchy depth, store names, dedup identity). Load SQL is generated.

**Scale cheat sheet**

- 1.6M article-seasons: product x season catalog (verbal / LinkedIn)
- Product weekly, seasons 6+7: about 839M (569.4M + 269.8M)
- Attr weekly, seasons 6+7: **4.09B** (2,779,317,472 + 1,311,108,195)
- 2.11B: agentic fact table (A2), different table
- Weekly grain is roughly 2x season grain groups. Attr unpivot is why attr weekly is the largest object.

---

## Elevator (use this, not a slogan)

**30s.** I am a Senior Software Engineer who owns high throughput backends and data platforms. At Impact Analytics I moved planner reads onto six ClickHouse rollup tables after a 250M pivot dropped from 189s to 12s. Weekly grain is built one fiscal week at a time because a full-season weekly aggregate sat around 170 GB and OOM'd. I also wrote a Go native TLS pump that copies season partitions between ClickHouse Cloud clusters at about 344k rows/s combined, measured on a 4.09B row attr weekly set.

**Hook if they want data infra.** I spend a lot of my time on memory-bound ClickHouse builds and moving billion-row partitions without pretending a crash is an atomic swap.

Kafka and Flink stay on Uber Menu. Do not put stateful event streaming on AssortSmart.

---

## Hero story (170 GB OOM)

Use for “hardest technical hurdle,” “failure,” “how you debug scale.”

- **S:** Weekly rollups need ~110 `any()` states plus `argMax` / `argMin` over wide strings. A whole-season weekly INSERT SELECT estimated around 170 GB aggregator state. It failed `MEMORY_LIMIT_EXCEEDED` at 80 GB and again at 200 GB. Replica is about 59 cores / 234 to 236 GiB.
- **T:** Keep weekly grain (planners need `fiscal_year_week`) without melting the box.
- **A:** Unit of work became one fiscal week, not one season. Generated weekly settings: 8 threads, 55 GB cap, 16 GB spill, 4 weeks in flight. Product week peaked around 11 GB. Briscoes attr week peaked over 40 GB (40 GB cap was too low). Do not raise season parallel and week parallel together on the same box.
- **R:** Weekly grain builds. Request path stays partition-pruned reads. 15.5x is a different harness (250M pivot). Say that unprompted.

**Trap:** “So you fixed OOM and that is why latency is 15.5x.” No. OOM is load time. 15.5x is query time.

---

## Interview questions

### 1. How did you design the rollup schema, and why not query daily facts on every request?

Daily `GROUP BY` with many `any()` / `argMax` states on a wide row is the wrong SLO. `FINAL` on ReplacingMergeTree does not use projections. We pay once at load (bounded memory, partition publish) and read cheap (`PARTITION BY season_code`, bloom on product / store / attr). Product keeps SKU dims. Store and attr drop style/color/size leftovers and re-weight so store totals match the sum of SKUs. Attr is an unpivot (`ARRAY JOIN` on attr pairs), which is why attr weekly is about 5x product weekly on Briscoes seasons 6 and 7.

### 2. Walk through a time you hit severe resource limits. How did you debug and fix the OOM?

See hero story. Profile by grain. Do not raise memory first. Shrink the unit to one week, then cap threads and spill. Attr weeks are the memory hog.

### 3. How did you get about 344k rows/s in Go? Was that an HTTP API?

No. That is ingest rate, not request RPS. Two season streams on one laptop, native TLS, about 150 to 190k rows/s each, about 344k combined at a live snapshot (~34m, dual workers, 500k batches). Batch commit rate is about 0.3 to 0.4 `Send()` per second per worker. If they hear “344k TPS,” correct them.

Why a Go pump: cluster-to-cluster pull was not available (Cloud allowlists). The operator IP is. The copier is an allowlisted pump, not a shard-to-shard design goal. PDF does not name the Cloud function that failed.

How 344k: `batchSize = 500_000`, columnar `[]T` buffers, `batch.Column(i).Append` then `Send()`, no per-row `reflect`. Two buffer sets so SELECT of the next 500k overlaps INSERT of the previous. That overlap is what stopped HTTP unexpected EOF when SELECT sat idle during INSERT. Do not retry `Send` on a spent batch.

### 4. How did you handle failure and idempotency on billion-row copies?

Partition unit is `season_code`. Copier ledger is `migrate-checkpoints/<table>.done`. Incomplete season: if the target already has rows, DROP PARTITION (or DELETE) then recopy. No full TRUNCATE unless `-reset`. SIGINT finishes the in-flight batch and does **not** checkpoint that season. Per-table flock so two terminals cannot copy the same table.

**64.1M is the loader, not this copier.** A failed weekly HTTP INSERT still commits blocks. A half-loaded partition of 64.1M rows once passed “skip if the partition has rows.” Weekly resume is a TSV ledger of finished `(kind, season_code)`. If missing, DROP PARTITION that season and rebuild. Completion of each HTTP INSERT is query-id / `QueryFinish` in `system.query_log`, not curl exit.

Drop PARTITION is **not** an atomic swap. A crash leaves a truncated season. Readers can see partial seasons. The incremental design (`REPLACE PARTITION` from scratch tables) was written and **not executed**. Do not claim it ran.

### 5. What is the scale?

Largest timed object: Briscoes attr weekly seasons 6+7 = 4.09B rows in one table, two partitions. Product weekly same seasons = 839M. Season grain is smaller. Replica about 59 cores / 234 to 236 GiB. 15.5x is 250M row-identical pivot (PDF rounds 12.3s to 12s).

### 6. Why not one INSERT of the whole season at weekly grain?

About 170 GB aggregator state. OOM at 80 GB and 200 GB. One week: ~11 GB product, over 40 GB attr.

### 7. How do store totals stay consistent with SKUs?

Two-pass weighted sums, then re-weight. Validate `sum(product)` vs `sum(store)` vs `sum(attr)` at the same filters. Earlier Briscoes season-grain parity: product and store revenue vs weekly spine 0% across seasons 1 to 7.

### 8. ReplacingMergeTree corrections?

New INSERT versions keyed by `updated_at`. Rebuild at a captured watermark. Do not `FINAL` if you want projections. Dirty arrival token on the MV is not the same clock as the build watermark. Incremental pipeline is design only.

### 9. Biggest production risk in the copier?

No atomic swap. Crash = truncated season until DROP + retry. Target readers can see partial seasons. Do not copy through a laptop for prod if you can allowlist and INSERT SELECT, or freeze via object storage.

### 10. Whiteboard the Go copier

```
source CH Cloud  --native TLS-->  laptop Go process  --native TLS-->  target CH Cloud
                     SELECT stream                    INSERT Send()
                     500k columnar                    500k columnar
                     buffer A while B sends           checkpoint season_code
```

`-workers N` = N seasons in parallel, each with its own source and target connections. Caps are **per process**. Two terminals of `-workers 2` double the budget. Host assumed 59 CPU / 236 GiB. Copier splits about 48 threads / 180 GiB across workers (example: 2 workers, 24 threads / 90 GiB each query).

Draw double buffering: read next 500k while previous `Send` runs.

Hindsight tables on this path are tiny (season 7 on source): keep_drop_score 4,150 rows, missed 360, top style 360. Verbal if they ask. Hindsight is still not a PDF headline.

Checkpoint status at the 8 Sep snapshot (say this if they ask “did 4.09B finish?”):

| Table | Status |
|---|---|
| product_season | seasons 3 to 7 done |
| attr_season | 3, 6, 7 done |
| store_weekly | 6, 7 done |
| product_weekly | empty ledger, failed mid-copy, partitions dirty |
| attr_weekly | empty ledger, in flight 6+7 (the 4.09B object) |
| hindsight three | season 7 done |

So you say **measured on** a 4.09B-row set, not **migrated 4.09B**.

---

## Failure catalog (say out loud)

1. OOM on weekly GROUP BY: shrink to one week, measure attr weeks before raising RAM.
2. Half-written partition looks complete: never `count() > 0` for weekly success.
3. HTTP client timeout after server commit: trust `system.query_log`.
4. HTTP SELECT EOF during INSERT: double buffer, or native protocol.
5. Retrying a spent batch: duplicates or a second failure. DROP PARTITION, restart the unit.
6. Connection reset on native TLS: crash. Checkpoint only finished seasons.
7. Cluster-to-cluster pull blocked by allowlists: laptop pump is a workaround.
8. Oversubscribe workers: caps are per process.
9. Never commit Cloud passwords. Env only. Binary does not read `.env` for you.

---

## LinkedIn / outreach honesty

Safe: six tables, 170 GB OOM and week slicing, Go pump, about 344k rows/s combined, 4.09B attr weekly as the largest object timed, 500k batches, double buffering.

Not safe: “I streamed 4.09 billion rows at 344,000 rows/s” as a finished job. “Atomic DROP PARTITION.” “OOM fix caused 15.5x.” Kafka/Flink on IA. Open-sourcing the copier.

CI gate (100% statement coverage, 1,200+ Go tests, SAST/SBOM) is fine on LinkedIn. It left the PDF for the copier bullet.

---

## Code map (verbal)

`docs/scripts/gen_rollup_from_imputed.py` generator. `docs/scripts/{kik,briscoes}/run_pipeline.sh` POC loader that ran. `cmd/migrate-rollup-table/` Cloud copy. `docs/scripts/automated_rollup/` incremental design, not run.
