# Uber (via EPAM Systems) — Menu Ingestion & Automation Platform (Uber Eats)

**Role:** Software Engineer · July 2024 – May 2026 · Bangalore
**Resume tech line:** Python, Apache Kafka, Apache Flink, Apache Spark, Apache Pinot, Selenium, Gemini, RAG, GCP, Docker

> **Read this first.** This project on the resume weaves the Apache streaming stack (Kafka/Flink/Spark/Pinot) into the menu-ingestion work. Uber genuinely runs one of the world's largest deployments of exactly this stack (Kafka fleet, Flink for stream processing, Pinot for real-time OLAP — all heavily used at Uber Eats), so the story is credible **only if you can defend every component in depth**. This doc is that defense. Do not claim team sizes or org details you can't back; keep the narrative scoped to *your* pipeline.

---

## 1. Elevator pitch

"Uber Eats onboards restaurant menus from third-party platforms. Doing it manually — or paying a third-party tool $2 per menu — was slow and expensive: ~24 hours per vendor. I built the ingestion platform: scrapers feed raw menu events onto Kafka; a Flink job normalizes and validates them in real time; unstructured menus (PDFs, images) go through an agentic AI extraction pipeline (RAG + Gemini 2.5 Pro); Spark handles batch backfills and reprocessing; and ingestion-health metrics stream into Pinot for real-time dashboards and alerting. Onboarding went from 24 hours to about 2, at 30,000+ menus a month, saving $600K+ a year."

## 2. Architecture

```
 3rd-party platforms (vendor menus: HTML, PDF, images)
        │  Selenium scrapers + anti-bot layer
        │  (IP rotation, UA spoofing, dynamic proxy pools)
        ▼
 ┌─────────────────────┐   raw menu events (JSON, one per menu/section)
 │   Kafka (ingest bus)│◄──────────────────────────────┐
 └─────────┬───────────┘                               │
           │ real-time path                            │ replay/backfill
           ▼                                           │
 ┌───────────────────────────┐              ┌──────────┴─────────┐
 │ Flink normalization job   │              │ Spark batch jobs   │
 │ · schema validation       │              │ · reprocess N days │
 │ · dedup (menu content hash│              │ · vendor backfills │
 │   keyed state)            │              │ · schema migrations│
 │ · currency/locale rules   │              └──────────┬─────────┘
 │ · route: structured vs    │                         │
 │   unstructured            │                         │
 └─────┬───────────────┬─────┘                         │
       │ structured    │ unstructured (PDF/image)      │
       ▼               ▼                               ▼
 catalog upsert   ┌────────────────────┐        catalog store
 (Eats menu API)  │ Agentic AI extract │        (validated menus)
                  │ RAG + Gemini 2.5   │
                  │ Pro + SFT schema   │
                  │ enforcement        │
                  └────────────────────┘
       │ ingestion-health events (success/fail/parse-error, per stage)
       ▼
 ┌─────────────────────┐     real-time dashboards + alerts
 │  Apache Pinot       │───► success-rate by source/stage,
 │  (real-time OLAP)   │     failure-spike alerting (minutes, not hours)
 └─────────────────────┘
```

## 3. Why each component (the "why this, not that" defense)

- **Kafka as the ingest bus** — scrapers are bursty and flaky; downstream consumers (Flink, AI extraction, audit) must be decoupled from scrape timing. Kafka gives replayable, partitioned, ordered-per-key (vendor id) buffering. **Numbers (ESTIMATED):** 30K menus/mo ≈ 1K menus/day; item-level scrape + retry + health events peak at **~200–500 events/sec** during fleet runs (steady-state much lower). Consumer lag is the health metric. *Alternative rejected:* direct HTTP to the catalog service — no replay, backpressure pushed into scrapers, one slow consumer stalls ingestion.
- **Flink for the real-time path** — per-event normalization with **keyed state** (dedup by menu content hash per vendor), event-time semantics for out-of-order scrape retries, exactly-once sink semantics via checkpointing. **Numbers (ESTIMATED):** job sized to keep pace with the Kafka peak (~200–500 events/sec) with near-zero lag in steady state; keyed state TTL prevents unbounded growth. *Alternative rejected:* Kafka consumer + cron — no state management, no exactly-once, hand-rolled windowing. Spark Structured Streaming — micro-batch latency and heavier ops for a per-event workload; at Uber, Flink is the standard stream engine.
- **Spark for batch** — backfills ("re-ingest vendor X's last 90 days"), reprocessing after schema/parser upgrades, and large joins against catalog snapshots. Batch is throughput-shaped: Spark's shuffle + columnar reads win; running backfills through the Flink job would starve the real-time path. **Numbers (ESTIMATED):** a typical 90-day / parser-upgrade backfill is on the order of **~1–2M item rows** — deliberately off the real-time path.
- **Pinot for ingestion health** — ops needed *sub-minute* visibility ("is parse-failure rate spiking on source Y?"). Pinot ingests straight from Kafka and serves low-latency OLAP (filter+groupBy on high-cardinality dims: source, vendor, stage, error class). **Numbers:** sub-second dashboard queries (ops target); time-to-detect hours → minutes (documented intent). *Alternative rejected:* batch warehouse dashboards — hours of lag.
- **RAG + Gemini 2.5 Pro + SFT for unstructured menus** — PDFs/images defeat rule-based parsers. Retrieval grounds extraction in similar previously-labeled menus; SFT enforces the output schema (100% schema consistency, 98% extraction fidelity — offline/eval). Validation gate before catalog write: schema check, price sanity, currency/locale checks; sub-threshold confidence → human review queue.
- **Anti-bot layer** — IP rotation, user-agent spoofing, dynamic proxy pools; retry budget per source; raised successful ingestions by **95% (~60–65% → 95%+)** (baseline ESTIMATED — see `09_metrics_derivations.md`).

## 4. Numbers to keep straight

30,000+ menus/month · onboarding 24 h → 2 h (90%) · $2/menu third-party cost eliminated → $600K+/yr · Kafka peak **~200–500 events/sec** (ESTIMATED) · Flink at that rate with keyed dedup · Spark backfills **~1–2M item rows** (ESTIMATED) · Pinot sub-second health queries · +95% successful ingestions (**~60–65% → 95%+**, baseline ESTIMATED) · 98% extraction fidelity, 100% schema consistency (SFT, offline/eval) · failure time-to-detect hours → minutes (Pinot) · ANZ compliance automation: 99.9% document compliance, 20 h/week manual work removed (separate workstream, same platform umbrella).

Full ESTIMATED vs DOCUMENTED tags: `../09_metrics_derivations.md`.

## 5. Deep-dive Q&A

- **"How does the Flink job stay correct on retries?"** Checkpointed keyed state; dedup key = hash(vendor_id, menu content); sink is idempotent upsert into the catalog keyed by vendor+item, so replays converge.
- **"Event-time or processing-time?"** Event-time with bounded lateness — scrape retries arrive out of order; we want the *latest* menu version to win deterministically, so events carry scrape timestamps and the job keeps last-write-wins state per key.
- **"Why not run the LLM extraction inside Flink?"** Latency/cost isolation. LLM calls are seconds and can fail; the streaming job must stay hot. Unstructured menus are routed to a separate async consumer group with its own retry/DLQ semantics.
- **"Pinot vs Druid vs ClickHouse for the health analytics?"** Pinot is Uber's in-house standard for real-time OLAP from Kafka (it powers Eats ops dashboards broadly); zero new infra to justify, native Kafka ingestion, sub-second groupBys.
- **"What breaks first at 10× volume?"** The scraper fleet (proxy pool exhaustion, per-source rate limits) — the streaming path scales by partitions. Mitigations: per-source token buckets, priority tiers for new-vendor onboarding vs refresh.
- **"Schema evolution?"** Versioned event schema on the bus; Flink job tolerates additive fields; breaking parser changes ship with a Spark reprocess of the affected window.

## 6. STAR-ready fragments

- **Cost/impact:** killed a $2/menu external dependency at 30K menus/month → $600K+/yr, plus 90% onboarding-time cut.
- **Reliability:** anti-bot arms race — measured, iterated proxy/fingerprint strategies to +95% success.
- **AI with guardrails:** LLM extraction never writes to catalog directly — schema validation + confidence gate + human review queue for low-confidence menus.
