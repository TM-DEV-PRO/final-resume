# ClickHouse

## What
Columnar OLAP store. Per-tenant AssortSmart planning store design: 63 tables / 8 layers, insert-only / partition-swapped, agent `readonly=1` (DDL Phase-1).

## How used here
Pivot POC at 250M rows cut heavy grid 189s→12.3s (~15.5× MEASURED). Replaces high-variance shared BigQuery probes for agent p95 targets.

## Tradeoffs
OLAP speed vs mutation pain. Chose INSERT-only services + partition swap (P1) / append-only events (P3), not in-place updates. Agent `readonly=1`. Copying from BQ requires freshness reconciliation. Omit 624 columns.

## Failure modes
- Mutations and small updates
- Silent stale copies
- COUNT(DISTINCT) heavy plans (be honest ~2–3× if stripped)

## Likely questions
Why not Postgres for everything? How do you ingest from BigQuery? What is your consistency story? Explain MergeTree / partitions at a high level.
