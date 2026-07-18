# Uber (via EPAM) — Menu Ingestion Platform (Java / Spring track)

**Role:** Software Development Engineer 2 · July 2024 – May 2026 · Bangalore  
**Resume tech:** Python, Apache Kafka, Apache Flink, Apache Spark, Apache Pinot, Selenium, Gemini, GCP, Docker

> Same pipeline and metrics as `interview_prep/projects/03_uber_menu_ingestion.md`. **No Spring claim on this project** — streaming + Python RAG matches the live stack and stays defensible.

---

## 1. Elevator pitch

"Uber Eats onboards restaurant menus from third-party platforms. Manual or third-party tooling was ~24 hours per vendor and expensive. I built the ingestion platform: scrapers publish raw menu events to Kafka; a Flink job normalizes and validates in real time; unstructured menus (PDFs, images) go through a RAG + Gemini extraction path; Spark handles backfills; Pinot powers ingestion-health dashboards. Onboarding went from 24 hours to ~2 hours at 30,000+ menus/month, saving $600K+/year."

## 2. Architecture

```
 3rd-party menus (HTML, PDF, images)
        │  Selenium + anti-bot (IP rotation, proxy pools)
        ▼
   Kafka (ingest bus)
        │
        ├─ Flink job: validate, dedup (keyed state), route structured vs unstructured
        │     ├─ structured → catalog upsert API
        │     └─ unstructured → Python RAG + Gemini extract → schema-validated catalog
        │
        └─ Spark: backfills / reprocessing
        │
   Pinot ← ingestion-health events → real-time ops dashboards + alerts
```

## 3. What you own in the story

- **Streaming path** — Kafka bus, Flink normalize/dedup/route, Spark backfills, Pinot health dashboards (defend these deeply).
- **RAG extraction** — Python service calling Gemini; chunk → retrieve → generate → validate against menu schema; 98% fidelity is offline/eval-backed — say so.
- **Anti-bot layer** — IP rotation, proxy pools → +95% successful ingestions.
- **Do not invent:** a Spring Boot catalog service on this resume line unless you add a real bullet for it.

## 4. Streaming defense (must be deep)

Interviewers will probe Kafka/Flink/Spark/Pinot more than Spring here. Use the same depth as the main `06_tech_deep_dives.md` streaming sections. One-liners:

- **Kafka:** partitioned log, per-vendor key ordering, consumer lag as health.
- **Flink:** event time, watermarks, keyed state dedup, checkpoints.
- **Spark:** batch backfills, shuffle-aware joins.
- **Pinot:** real-time OLAP for high-QPS ops slices from Kafka.

## 5. Q&A

- **"Why Flink not a Spring consumer alone?"** Need true streaming state (dedup, event-time LWW). Flink is the stream engine; don't claim Spring Cloud Stream as a substitute on this project.
- **"$600K — how?"** Onboarding-hours saved × ops cost at 30K menus/mo — finance-owned model; know the arithmetic before quoting.
