# Metrics Derivations (resume v2)

**Same numbers and honesty tags as the main track.** Full tables: [`../interview_prep/09_metrics_derivations.md`](../interview_prep/09_metrics_derivations.md).

v2 only hardens IA *phrasing* (targeting / concurrent writes without row locks) and skills trim. **All TPS / RPS / from→to / streaming rates match the main resume.**

## Resume-facing quick list (v2 wording)

| Project | Numbers to defend |
|---|---|
| AssortSmart | Go Gin bulk-save **~10–20 peak RPS** · ClickHouse **~5–10K row writes/sec** · turnaround **targeting** days→<1h |
| FRM | **70%** cycle (**~2 weeks → ~3–4 days**) · 36 endpoints **p95 < 300 ms** · 19M→300K · no RPS claim |
| Menu | Kafka **~200–500 peak events/sec** · +**95%** (**~60–65% → 95%+**) · Pinot sub-second · Spark **~1–2M** item rows |
| Masters GST | **~12 TPS avg / 100+ TPS peak** · triage **70%** (**~30 min → <10 min**) · p95 1.2s→300ms · MongoDB/ES as documented |
| GFG | **~1–2 RPS avg, ~10× contest spikes** · +15–20% premium **relative** · MongoDB/ES as documented |

## Streaming study pointer

Use main `../interview_prep/projects/03_uber_menu_ingestion.md` and `../interview_prep/06_tech_deep_dives.md` §§3–6 (updated with rates). Do not invent Kafka partition counts.
