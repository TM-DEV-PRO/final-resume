# Kafka + event-driven paths (Menu + Masters + IA)

## What
Kafka as the **replayable, partitioned, multi-consumer log** — three contracts, three scales.

## Where used
| Project | Role | Scale to defend | Flink after it? |
|---|---|---|---|
| **Menu** | Ingest bus after Selenium; feeds Flink + RAG | 30K+ menus/mo; 24h→2h; 95%+ | **Yes** |
| **Masters** | Bulk IRP / e-invoice | 1M+/day; 100K+/import; 700→4k req/min | **No** |
| **IA** | Async embedding / background jobs | Light Tech claim | **No** |

## Why Kafka when numbers are “high” (or bursty)

### Menu
- Scrapers must not block on catalog/RAG latency.
- Need **replay** after bad parsers (rewind offsets).
- Need **ordered keys** per vendor and fan-out to Flink + health consumers.
- Average rate from 30K/mo is modest; **bursts + failure modes** justify the bus. See [kafka_flink_scale_defense.md](kafka_flink_scale_defense.md).

### Masters
- Filing deadlines → **100+ TPS peak ESTIMATED** on top of ~12 TPS avg from 1M+/day.
- **100K+/import** cannot be one sync request.
- Idempotency + DLQ so at-least-once Kafka does not double-file.
- Partition key ≈ GSTIN for per-taxpayer ordering.

### IA
- Keep agent request path free of heavy embed work. Do not inflate to Menu/Masters scale.

## Tradeoffs
Async complexity vs sync spikes melting the DB. Menu: Kafka + **Flink** state. Masters: Kafka + PG quarter shards + idempotent workers.

## Failure modes
- Dual writes without idempotency
- Poison messages without DLQ
- Consumer lag / backpressure
- Bad parser → rewind before bad watermark (Menu)

## Likely questions
Exactly-once? Idempotency key contents? DLQ replay? Why not only Celery? Why Menu has Flink but Masters does not? “Isn’t 30K/mo too small for Kafka?”

## Related
- [kafka_flink_scale_defense.md](kafka_flink_scale_defense.md) — full attack/defense
- [flink.md](flink.md)
