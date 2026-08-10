# Flink (Menu hot path) + Spark (backfill — verbal)

## What
**Apache Flink** — stateful stream processor over Kafka. Used on **Uber Menu** after the ingest bus for validate / keyed dedupe / route structured vs unstructured.

**Apache Spark** — batch / micro-batch. Prefer for **backfills and reprocessing**, not the hot catalog freshness path (verbal unless JD demands Spark on PDF).

## Where (only Menu)
- **In:** Kafka topics of scrape events (keyed by vendor/menu).
- **Out:** structured → catalog upsert; unstructured → RAG/Gemini path.
- **Not used at:** Masters (Kafka workers), IA (CH + agent), FRM.

## Why we needed it at Menu scale
30K+ menus/month is not “Flink because huge TPS.” Drivers:

1. **Burst + retries** from Selenium/anti-bot — need continuous processing, not nightly batch.
2. **Keyed dedupe** — same vendor can emit late/duplicate pages; Flink keyed state drops duplicates.
3. **Event-time** — scrape timestamps out of order; watermarks bound lateness.
4. **SLA** — 24h→2h onboarding needs minutes-level freshness vs Spark micro-batches.
5. **Fan-out routing** — one job validates then routes structured vs unstructured.

Full scale attack answers: [kafka_flink_scale_defense.md](kafka_flink_scale_defense.md).

## Why Flink here (not Spark on the hot path)
| Need | Flink | Spark |
|---|---|---|
| Keyed state per vendor/menu | Native | Awkward |
| Event-time + late pages | Watermarks | Micro-batch delay |
| Catalog freshness (minutes) | Better | Heavier |
| Huge historical reprocess | Possible | **Better fit** |

## How it fits the Menu pipeline
```text
Selenium scrape → Kafka (replayable bus)
  → Flink: validate, dedupe (keyed state), route
       → structured → catalog upsert
       → unstructured → RAG/Gemini extract → schema validate → catalog
  → Spark (verbal): backfill / repair gaps after bad deploy
```

## Fundamentals to recite
- **Parallelism** ≈ Kafka partition count (rough alignment).
- **Keyed state** — vendor/menu id for dedupe.
- **Watermarks** — bounded out-of-orderness for late scrapes.
- **Exactly-once** — Flink + Kafka transactions help; **catalog upserts still idempotent**.
- **Failure** — bad Flink build → rewind Kafka before bad watermark; Spark backfill for holes.

## Failure modes
- State blowup if key cardinality explodes.
- Idle watermarks stalling windows.
- Brittle HTML in Flink UDFs — version parse modules.

## Likely questions
Why Flink not Spark? How do you handle late events? How do you rewind after a bad parser? What is in your dedupe key? Is 30K/month enough to justify Flink? (Answer: burst/replay/state, not vanity TPS.)

## Resume placement
- **Skills:** Flink under Data and Streaming.
- **Menu Tech + bullet:** Kafka + Flink.
- **Masters:** Kafka only.
