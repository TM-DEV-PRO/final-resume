# Metrics Derivations (Java track)

**Same numbers and honesty tags as the main track.** Full tables: [`../interview_prep/09_metrics_derivations.md`](../interview_prep/09_metrics_derivations.md).

Stack framing only changes *how* you describe the service (Spring Boot / JPA / Spring Batch vs FastAPI / SQLAlchemy / Celery). **TPS, RPS, from→to baselines, and Kafka/Flink/Spark/Pinot rates do not change.**

## Resume-facing quick list (Java wording)

| Project | Numbers to defend |
|---|---|
| AssortSmart | Spring Boot bulk-save **~10–20 peak RPS** · ClickHouse **~5–10K row writes/sec** · agent days→<1h (design target) |
| FRM | **70%** cycle (**~2 weeks → ~3–4 days**) · 36 endpoints **p95 < 300 ms** · 19M→300K · no RPS claim |
| Menu | Kafka **~200–500 peak events/sec** · +**95%** success (**~60–65% → 95%+**) · Pinot sub-second · Spark **~1–2M** item-row batches · **Python** streaming/RAG (no Spring claim) |
| Masters GST | **~12 TPS avg / 100+ TPS peak** on 1M+ txn/day · triage **70%** (**~30 min → <10 min**) · p95 1.2s→300ms |
| GFG | **~1–2 RPS avg, ~10× contest spikes** · +15–20% premium **relative** lift |

## Interview line

> "Those RPS/TPS figures are **estimated from documented daily volumes** (1M txn/day, 100K queries/day, 30K menus/month). I can walk the arithmetic. I will not invent partition counts or Grafana screenshots I don't have."
