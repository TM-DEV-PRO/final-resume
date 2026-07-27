# Uber Menu Ingestion Deep Dive (v2 + Java tracks)

> **Start here for interviews:** [`23b_uber_interview_packs.md`](23b_uber_interview_packs.md) § Menu.

Numbers match `GROUND_TRUTH.md` and `09_metrics_derivations.md`. Rates tagged ESTIMATED where derived.

> **RESUME ALIGNMENT (Jul 2026):** Menu PDF is **Selenium + Kafka + Flink + RAG/Gemini** (Uber Eats). **ANZ is a separate Uber Mobility project** — main-app drivers/earners, driver+vehicle docs vs local authorities — **not** Eats catalog. Masters also owns Kafka for GST IRP (different product). Use [`23b_uber_interview_packs.md`](../../interview_prep_v2/23b_uber_interview_packs.md) § Menu / ANZ as the canonical pack.

---

## Why this project is the best fit for Flink and Spark

| Option | Verdict | Why |
|---|---|---|
| **Uber Menu** | **Selected** | Burst scrapers need a durable bus (Kafka), online normalize/dedupe (Flink), and large reprocess/backfill jobs (Spark). Matches original resume claim and production pattern used at Uber-scale ingestion teams. |
| Masters India | Rejected for Flink/Spark | Already has Kafka + Celery/Spring Batch for IRP bulk. Adding Flink/Spark there duplicates without stronger evidence. |
| Impact Analytics | Rejected | Analytics path is ClickHouse POC / CQRS, not a Spark/Flink job you owned. |
| Skills-only | Too weak | Big-tech data/backend screens (Databricks, Airbnb data, Netflix data platform) want experience bullets, not only a skills chip. |

### Role split (defend this whiteboard)

```
Partner sites / PDF+image menus
        |
        v
Selenium scrapers (GCP) + proxy pools     ← acquire HTML / files
        |
        v
Kafka (keyed by vendor_id)                ← buffer, replay, fan-out
        |
        +--> Flink (event-time)           ← normalize, validate, dedupe, route
        |         |
        |         +--> catalog upsert (idempotent)
        |         +--> low-confidence → RAG/Gemini path
        |
        +--> Spark (batch / micro-batch)  ← backfills, reprocess windows, joins
        |
        +--> ANZ compliance jobs (separate Python track)
```

**Flink why not Spark for the hot path:** scrapes are bursty; you need keyed state for per-vendor dedupe, event-time ordering when late pages arrive, and lower latency than Spark micro-batches so catalog freshness stays minutes not hours.  
**Spark why not Flink for backfills:** reprocessing 90 days of item rows is batch-shaped (large shuffle, SQL joins, replay from object storage). Spark’s DataFrame API and existing batch ops fit; spinning Flink state for a one-shot backfill is the wrong cost curve.  
**Kafka why not direct HTTP to catalog:** scrapers must not block on slow catalog writes; replay after a bad parser deploy; multiple consumers (Flink online, Spark backfill, audit) share one log.

Industry grounding (interview citations, not personal claims): Flink for true stream / stateful Kafka consumers; Spark for unified batch + near-real-time and lakehouse ETL ([Confluent Flink vs Spark](https://www.confluent.io/compare/spark-streaming-vs-flink/), [Estuary comparison](https://estuary.dev/blog/apache-spark-vs-flink/)).

---

## Bullet defenses

### 1. Selenium → Kafka → Flink + Spark, 30K menus/mo, 24h→2h, $600K+

**Resume wording (Jul 2026):** no peak events/sec on the PDF. Kafka is the ingest bus; Flink online normalize/dedupe; Spark backfills. Outcomes stay **24h→2h**, **30K+ menus/month**, **$600K+/yr**.

**Acquire (HISTORICAL).** Python Selenium on GCP hits JS-heavy vendor sites through proxy pools; emits menu/item/scrape-health events.

**Bus.** Kafka topic(s) keyed by `vendor_id` for per-vendor ordering, replay, and fan-out. **Verbal only if asked:** peak **~200–500 events/sec** during fleet runs (ESTIMATED) — 30K menus/mo ≈ 1K menus/day; item-level events + retries + health amplify bursts. Steady-state much lower. Consumer lag is the primary SLO.

**Flink online (HISTORICAL role / ESTIMATED load).** Consume Kafka; keyed process by vendor; schema validate; dedupe by content hash / menu version; route structured items to catalog upsert; route unstructured payloads to RAG/Gemini.

**Spark batch (HISTORICAL role / ESTIMATED volume).** Nightly or on-demand backfills (~**1–2M item rows** ESTIMATED for a typical 90-day reprocess).

**Impact.** Onboarding **24h → 2h** (90%). Money: kill ~**$2/menu** third-party tool → 30K × $2 × 12 = **$720K** list → resume **$600K+** conservative floor.

### 2. RAG + Gemini, 98% fidelity, 100% schema consistency

Unstructured PDFs/images. Chunk → retrieve similar labeled menus → Gemini generate → schema validate → low confidence to human review. SFT for schema. **Offline/eval** numbers. Say that.

### 3. +95% success (about 60% → 95%+), anti-bot

IP rotation, UA spoofing, dynamic proxies, per-source retry budgets. Baseline ESTIMATED ~60–65% → mid-90s.

### 4. ANZ driver/vehicle compliance 99.9%, 20h/week saved (Uber Mobility)

**Not Uber Eats.** Separate PDF project under **Uber Mobility**: automate **driver and vehicle documents** for **main-app drivers / earners in ANZ** against local authorities. HISTORICAL from 4yr resume. Do not invent Selenium/RAG for this path.

---

## Flink deep dive (must-know for interviews)

| Topic | What you say |
|---|---|
| API | DataStream or Table API; keyed by `vendor_id` |
| Time | Event time from scrape timestamp; watermarks with bounded out-of-orderness (late pages) |
| State | Keyed dedupe state (last content hash / menu version) in RocksDB state backend |
| Fault tolerance | Checkpoint barriers; restore from last successful checkpoint on TaskManager loss |
| Delivery | Kafka source at-least-once or exactly-once with transactional sink if required; catalog sink idempotent either way |
| Backpressure | Slow catalog → Flink network buffers → Kafka consumer lag rises (that is the alert) |
| Failure mode | Bad deploy of normalizer → rewind Kafka offsets to before bad watermark, reprocess, Spark backfill for gaps |

**Q: Why not Kafka Streams?**  
Kafka Streams is an option for lighter transforms. Flink chosen for richer event-time + larger keyed state and clearer ops story for a dedicated processing cluster at Uber-shaped platforms. Admit Kafka Streams could work at this event rate if the team standard was Streams-only.

**Q: Exactly-once end to end?**  
Across Selenium + Kafka + Flink + external catalog you usually get **at-least-once + idempotent upsert**. Exactly-once needs transactional sinks and a store that participates; do not claim two-phase commit across Gemini or third-party sites.

### Official Flink refs
- https://nightlies.apache.org/flink/flink-docs-stable/
- https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/
- https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/ha/overview/

---

## Spark deep dive (must-know for interviews)

| Topic | What you say |
|---|---|
| Role | Backfill / reprocess / large joins — not the hot online path |
| API | Spark SQL / DataFrames on object storage dumps or Kafka batch read |
| Why Spark | Unified batch, shuffle-friendly joins, team familiarity for large historical rewrites |
| Skew | Hot vendors (huge menus) → salt keys or isolate whale vendors |
| AQE | Adaptive query execution for skew and partition coalescing on backfills |
| Structured Streaming | Optional near-real-time path; on this resume Flink owns online, Spark owns batch — do not claim both for the same hot path without a clear reason |

**Q: Why not only Spark Structured Streaming?**  
Micro-batch latency (seconds) is weaker for live catalog freshness under scrape bursts; Flink fits online. Spark still wins for multi-million-row historical reprocess.

**Q: Spark vs ClickHouse (if they mix IA and Menu)?**  
Different problems. Menu backfill = ETL over scrape history. IA Order Batching = interactive OLAP metric (measured CH 3.86s vs PG minutes). Do not merge the stories.

### Official Spark refs
- https://spark.apache.org/docs/latest/cluster-overview.html
- https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html

---

## Money and rate math (rapid fire)

| Claim | Arithmetic | Tag |
|---|---|---|
| $600K+/yr | $2/menu × 30K × 12 = $720K list → floor $600K+ | HISTORICAL |
| ~200–500 peak events/sec | Menus/day × items × retries in fleet windows | ESTIMATED |
| ~1–2M Spark backfill rows | ~1K menus/day × items × multi-day reprocess window | ESTIMATED |
| 24h → 2h | Onboarding cycle | HISTORICAL |
| +95% ingestions | ~60–65% → 95%+ after proxies | HISTORICAL / EST. baseline |

---

## Mock interview: hardest questions

**Interviewer:** You previously said Menu was only Selenium. Which is it?  
**Candidate:** Both layers. Selenium acquires pages. Kafka/Flink/Spark process and land catalog data. An earlier one-pager dropped streaming to save space and reduce risk; the fuller claim matches the original event-driven resume bullet and is what I defend now. Kafka at Masters India is a separate product (e-invoice).

**Interviewer:** Derive 200–500 events/sec.  
**Candidate:** 30K menus/month ≈ 1K/day. Each menu emits many item and retry/health events during a fleet run. Bursts concentrate into short windows → hundreds of events/sec peak. Steady-state is much lower. Order-of-magnitude estimate, not a Grafana screenshot.

**Interviewer:** Flink checkpoint fails mid-fleet. What happens?  
**Candidate:** Job restores from last checkpoint; Kafka offsets rewind to the checkpointed positions; idempotent catalog upserts prevent duplicate items; lag alert fires until catch-up. If a whole window is corrupt, Spark backfill repairs from raw object storage.

**Interviewer:** Why both Flink and Spark — is that overkill at 30K menus/month?  
**Candidate:** Volume is moderate; the architecture is about **shape**, not only QPS. Online path needs event-time dedupe under scrape jitter. Offline path needs large historical rewrites after schema changes. At this scale a single consumer could work, but splitting online vs batch matches Uber-style paved roads and keeps blast radius small when reprocessing.

**Interviewer:** Databricks asks about Spark depth. How far do you go?  
**Candidate:** Production role on Menu was batch/backfill oriented: DataFrames, reprocess jobs, skew handling. I do not claim Spark kernel or Delta Lake ownership. For Databricks pure runtime roles I still lead with Menu Spark plus IA ClickHouse analytics judgment.

---

## Confidence audit

| Resume bullet | Rating | Fallback |
|---|---|---|
| Selenium + Kafka + Flink + Spark, 30K+, 24h→2h, $600K+ | SOLID on outcomes; peak events/sec **off PDF** | Money uses $720K list / $600K+ floor; defend Kafka rate verbally only if asked |
| RAG/Gemini 98%/100% | SOLID if offline eval stated | Always say offline/eval |
| +95% ingestions | NEEDS CARE on baseline | Give ~60–65% → 95%+ as estimated baseline |
| ANZ 99.9% / 20h | SOLID HISTORICAL | Separate track from streaming |

**Honesty:** Do not claim Pinot on the current PDF. Do not claim Spark at IA. Do not claim Flink at Masters India.
