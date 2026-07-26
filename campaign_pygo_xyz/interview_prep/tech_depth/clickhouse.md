# ClickHouse

## What
Columnar OLAP store. Per-tenant AssortSmart planning store design: 63 tables / 8 layers append-only agent read-only.

## How used here
Pivot POC at 250M rows cut heavy grid 189s→12.3s (~15.5× MEASURED). Replaces high-variance shared BigQuery probes for agent p95 targets.

## Tradeoffs
OLAP speed vs mutation pain. Chose append-only / partition swap not in-place updates. Copying from BQ requires freshness reconciliation.

## Failure modes
- Mutations and small updates
- Silent stale copies
- COUNT(DISTINCT) heavy plans (be honest ~2–3× if stripped)

## Likely questions
Why not Postgres for everything? How do you ingest from BigQuery? What is your consistency story? Explain MergeTree / partitions at a high level.
