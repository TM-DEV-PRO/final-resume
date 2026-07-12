---

# 4. Database architecture (HLD + LLD)

## 4.1 HLD — the three-tier spine
```
                    ┌─────────────────────────────────────────────────────────┐
   RAW FACTS  ─────▶│  BigQuery  =  SOURCE OF TRUTH + batch cube/rollup builds │  (OLAP, scan-heavy, quota-limited DML)
                    └───────────────┬─────────────────────────────────────────┘
                                    │ scheduled ELT (build pre-aggregated cube)
                                    ▼
                    ┌─────────────────────────────────────────────────────────┐
   planner edits ──▶│  Postgres  =  EDITABLE SYSTEM-OF-RECORD (ACID, procs)    │  (OLTP writes, read-after-write)
                    └───────────────┬───────────────────────────▲─────────────┘
             hydrate plan slice     │ commit deltas             │
                                    ▼                           │
                    ┌───────────────────────────┐               │
                    │ DuckDB (in-process pivot)  │───────────────┘
                    └───────────────────────────┘
                                    │ (at scale, read-serving)
                                    ▼
                    ┌─────────────────────────────────────────────────────────┐
   fast pivots  ◀───│  ClickHouse = OLAP read/pivot serving (gated, insert-only)│
                    └─────────────────────────────────────────────────────────┘
   Invariant: BigQuery stays truth; Postgres stays the editable SoR — in every scenario.
```
**Why split:** the product is **OLTP-with-pivot** (editable grid, ACID, read-after-write) *and* **OLAP** (hindsight scans). No single engine is best at both, so each workload runs on the engine that's best at it. "Everything in one OLAP DB" breaks transactional writes + per-edit cost; "everything in BigQuery" hits DML quota/latency walls for interactive edits.

## 4.2 The tenant-unified derived schema
One common schema keyed by `tenant`, at the **derived (cube) grain** = `cluster × class × fiscal_week` — **not** per-tenant tables.

- **Postgres** (`planning_schema.sql`): `plan_cube` `PARTITION BY LIST (tenant)`, PK `(tenant, season, plan_id, cluster, class, fiscal_week)`; onboarding a client = `CREATE TABLE plan_cube_kik PARTITION OF plan_cube FOR VALUES IN ('kik')`. Same-shaped `plan_cell_edits` audit table.
- **ClickHouse** (`ch_planning_schema.sql`): `tenant` leads both `PARTITION BY (tenant, l1, fiscal_week)` and `ORDER BY (tenant, season, plan_id, l4, store_code, metric)`.
- The **cube-build SQL is tenant-parameterized and identical** across clients → one codebase/query set/procedures serves all tenants. Physical isolation (separate Postgres DB + BigQuery project per tenant) is retained; "unified" is a **schema/codebase standard at the derived level**, not a shared physical instance.

## 4.3 LLD — ClickHouse insert-only / versioned model
```sql
-- main planning cube: INSERT-ONLY VERSIONED (no ALTER UPDATE/DELETE)
CREATE TABLE plan_cube (
  tenant String, season String, plan_id String,
  l1 String, l4 String, store_code String,
  fiscal_week UInt16,
  metric String, value Float64,           -- 80–90 metrics modelled long (metric,value)
  version UInt64,                          -- monotonic epoch-ms; newest wins
  is_deleted UInt8 DEFAULT 0               -- soft delete (no hard DELETE)
) ENGINE = ReplacingMergeTree(version)
PARTITION BY (tenant, l1, fiscal_week)     -- week/L1 anchor avoids hot-partition churn
ORDER BY (tenant, season, plan_id, l4, store_code, metric);

-- EDIT  = insert a new version (never UPDATE)
INSERT INTO plan_cube VALUES (..., metric, new_value, toUnixTimestamp64Milli(now64()), 0);

-- READ latest = argMax over version (or FINAL on small partitions)
SELECT l4, store_code, argMax(value, version) AS value
FROM plan_cube WHERE tenant=? AND plan_id=? AND is_deleted=0
GROUP BY l4, store_code;

-- SOFT DELETE = insert a tombstone version
INSERT INTO plan_cube VALUES (..., metric, 0.0, <ver>, 1);

-- BULK re-seed (LY/LLY across a slice) = atomic partition swap, NOT a mutation
ALTER TABLE plan_cube REPLACE PARTITION (tenant,l1,week) FROM plan_cube_staging;

-- incremental brand/L1 rollups without rescans
CREATE TABLE plan_cube_l1_rollup ( ..., value_state AggregateFunction(sum, Float64) )
ENGINE = AggregatingMergeTree ...;
```
**Why this is the crux:** ClickHouse `ALTER UPDATE/DELETE` **mutations are async — they degrade past ~500 and stop accepting past ~1,000**. A planning grid is edit-heavy, which is why the legacy audit said "no ClickHouse." The insight: **model an edit as an INSERT of a new `version`**, read the latest with `argMax(version)`, tombstone for deletes, partition-swap for bulk re-seeds. A guard asserts `mutations_used == 0`. This also gives **undo / version-diff for free** (older versions retained until merge; the product caches **up to 10 undo steps in Redis** before async commit, rendering diffs as dual-value cells). Production hardens it with **`ReplicatedReplacingMergeTree` + sharding** (ClickHouse Keeper, or physical **L1-table sharding to kill hotspots**), **`AggregatingMergeTree`** rollups, **`VersionedCollapsingMergeTree`** for out-of-order CDC, and **Projections**; partition `PARTITION BY toYYYYMM(week_date)`, `ORDER BY (measure, hierarchy…)` for sparse-index granule skipping. **PoC results (requirements notebook):** `mutations_used = 0` at every scale, and **sub-second pivots over 250M synthetic rows — 8–130 ms filtered reads, ~160 ms writes, ~140–200× vs the legacy Postgres flat schema** (see §8.4–8.5).

## 4.4 Cube / rollup / pivot (fast reads)
- **cube_builder** — runs the tenant-parameterized `CUBE_BUILD_SQL` on BigQuery (aggregates fact → `cluster×class×week`), upserts to Postgres `plan_cube`.
- **rollup_builder** — CTAS a store×category×week rollup **from the clustered fact** (`PARTITION BY RANGE_BUCKET(fiscal_week) CLUSTER BY store_code,l3_name`): reads ~3.3 GiB instead of ~2.9 TiB (**~280–880× cheaper**; ~$8 once, ~$0.008/day).
- **pivot_service** — loads the plan's cube slice into DuckDB (Arrow) and runs native `PIVOT … USING sum() GROUP BY`; pivots track the *slice* size, not the fact.

## 4.5 The reconciled verdict + decision gates
The decision was **not** "adopt ClickHouse now" — it was a staged gate:
1. **In-stack BigQuery fixes first** (certain, no new infra): clustered `_assort` (~3×), store×cat×week rollup (~280×), forbid `SELECT *` + require date filter (kills the 38.8 TiB / $327 leak), fix cross-tenant hardcodes.
2. **Postgres discipline**: transaction-wrap multi-table ops, set-based `UPDATE … FROM`, repartition `size_split_master` (5,503 LIST partitions for 298K rows), purge soft-delete debris, normalize the EAV spine.
3. **Versioned-write + pivot PoC at 10×**: measure Postgres+DuckDB vs ClickHouse on the *same* insert-only cube; **only then** decide if ClickHouse earns a place.

**Two end-states:** (1) **ClickHouse-unified** if the insert-only model meets the pivot+update SLA at 100–200 users; (2) **split SoR** (BigQuery truth + Postgres strict-edit SoR + DuckDB pivot; CH read-only) if strict in-transaction per-cell read-after-write is required. *Anti-pattern explicitly rejected: "everything in one OLAP DB."*

## 4.6 Ingestion (be precise in the room)
Ingestion into the serving/planning stores is **batch ELT, not streaming**: BigQuery cube/rollup builds → upsert/COPY into Postgres; ClickHouse fed by HTTP `INSERT … FORMAT JSONEachRow` + `REPLACE PARTITION` from staging. **No Kafka/Airflow/Spark/Flink in the Agentic-Assort DB path.** (Elsewhere in the org: the *data-fabric* platform uses an **aiokafka** consumer for async embeddings and **Cloud Tasks + Cloud Scheduler** for orchestration; legacy AssortSmart uses **Pub/Sub** for MDM sync — mention these as adjacent, not as this product's pipeline.)
