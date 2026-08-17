# Uber Menu — streaming numbers (v2 pointer)

v2 resume uses the same Menu bullets as the main track. Do not duplicate the full HLD here.

**Study:**

1. [`../resume/prep/projects/03_uber_menu_ingestion.md`](../../resume/prep/projects/03_uber_menu_ingestion.md) §3–4 (why Kafka/Flink/Spark/Pinot **with numbers**)
2. [`../resume/prep/06_tech_deep_dives.md`](../../resume/prep/06_tech_deep_dives.md) §§3–6
3. [`09_metrics_derivations.md`](09_metrics_derivations.md) §3

| Component | Why | Number (ESTIMATED unless noted) |
|---|---|---|
| Kafka | Burst scrape bus, replay, per-vendor order | ~200–500 peak events/sec |
| Flink | Keyed dedup, event-time LWW, checkpoints | Same peak; near-zero lag steady state |
| Spark | Backfills without starving real-time | ~1–2M item rows per typical window |
| Pinot | Ops health OLAP from Kafka | Sub-second queries; hours→minutes detect |
| Anti-bot | Proxy/IP rotation | +95% success (~60–65% → 95%+) |
