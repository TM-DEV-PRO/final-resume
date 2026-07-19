# Uber Menu Ingestion Deep Dive (v2 resume defense)

Numbers match `GROUND_TRUTH.md` and `09_metrics_derivations.md`. Streaming rates tagged ESTIMATED.

---

## What the system does

Uber Eats onboards restaurant menus from third party platforms and unstructured PDFs/images into the catalog. Scrapers emit events, Flink normalizes and dedups in real time, Spark handles backfills, Pinot powers ops health dashboards, and a Python RAG plus Gemini path extracts structured items from messy menus. Success criteria: time to onboard, ingestion success rate, extraction fidelity, and ops time to detect failures.

---

## Bullet defenses

### 1. Kafka (200 to 500 peak events/sec), Flink, Spark, 30K menus/month, 24h to 2h, $600K+/yr

**Why Kafka.** Scrapers are bursty and flaky. Direct HTTP into the catalog couples scrape timing to write path and has no replay. Kafka gives per vendor key ordering, durable buffering, and consumer isolation. Peak rate ESTIMATED from 30K menus/month (~1K/day) times item level events and retries during fleet runs.

**Why Flink.** Per event dedup keyed by vendor plus content hash, event time last write wins for out of order scrape retries, checkpoints for exactly once state. Spark Structured Streaming would add micro batch latency; at Uber, Flink is the stream engine for this class of work.

**Why Spark.** Parser upgrades and 90 day reprocess windows would starve the real time path if run through Flink. Spark batch windows are about 1 to 2M item rows (ESTIMATED).

**Impact.** Onboarding 24h to 2h. Eliminated a $2 per menu third party tool at 30K menus/month = $600K+/yr (HISTORICAL).

### 2. RAG + Gemini, 98% fidelity, 100% schema consistency

Unstructured PDFs and images defeat rule based parsers. Pipeline: chunk menu, retrieve similar labeled menus, generate structured items with Gemini, validate against schema (prices, currency, locale), low confidence goes to human review. SFT enforces schema. 98% fidelity and 100% schema consistency are offline/eval numbers. Say that.

### 3. +95% success (about 60% to 95%+), Pinot sub-second dashboards

Anti bot: IP rotation, user agent spoofing, dynamic proxy pools, per source retry budgets. Baseline from about 60 to 65% to 95%+ (baseline ESTIMATED). Pinot ingests health events from Kafka for filter and groupBy on source, stage, error class in sub seconds, cutting detection from hours to minutes.

---

## End to end flow

```
Scrapers (Selenium + proxies)
        |
        v
   Kafka topics (per vendor key)
        |
        +--> Flink (normalize, dedup, route structured vs unstructured)
        |         |
        |         +--> Catalog upsert (idempotent)
        |         +--> AI extraction queue (async, separate consumer group)
        |
        +--> Pinot (health events) --> ops dashboards + alerts
        |
        +--> Spark (backfills / parser upgrades)
```

---

## Rapid fire

- Why not run LLM inside Flink? Latency and cost isolation. LLM calls are seconds and can fail; streaming job must stay hot.
- Event time or processing time? Event time with bounded lateness so latest menu version wins.
- What breaks at 10x? Proxy pool and per source rate limits first. Streaming scales by partitions.
- Pinot vs ClickHouse for health? Pinot is Uber paved road for high QPS real time OLAP from Kafka.
- Exactly once story? Idempotent producer plus Flink checkpoints plus idempotent catalog upserts.

Full production pattern notes: see research brief in session (Kafka/Flink/Spark/Pinot section of tech production practices).
