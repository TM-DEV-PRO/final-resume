# Impact Analytics — Agentic AssortSmart (AI-Powered Retail Merchandise Planning)

**Role:** Senior Software Engineer · 14 May 2026 – Present · Bangalore  
**Resume tech:** FastAPI, LangGraph, MCP · write plane **Go / Gin** · ClickHouse · BigQuery · GCS · Datadog · LangSmith · PostHog · Docker  

> Ground truth: [`GROUND_TRUTH.md`](../GROUND_TRUTH.md). Keep/Drop pipeline: [`../../docs/assort_kd_flow/PIPELINE.md`](../../docs/assort_kd_flow/PIPELINE.md) · shared [`../../../docs/assort_kd_flow/PIPELINE.md`](../../../docs/assort_kd_flow/PIPELINE.md).

---

## PDF bullets (say these)

1. Building **AssortSmart**, a retail merchandise planning platform for seasonal buying, store clustering, and assortment decisions.
2. Architected AssortSmart's **Keep/Drop engine** at article × plan-season grain, combining deterministic **ST%/ROS** scoring with **LangGraph** lenses, kept agents **SELECT-only** on ClickHouse through CSV-first bake-and-promote, with promotions gated on **300 gold cases** and **≥80% offline accuracy**.
3. Built a **read-only dig-deeper QnA agent** over locked Keep/Drop decisions, enabling planners to understand why styles were kept or dropped while schema constraints preserved frozen decisions and blocked writes to ClickHouse, CSVs, and outcomes.
4. Drove adoption of **ClickHouse** as AssortSmart's planning analytics engine, reducing pivot latency from **189s to 12.3s** (~**15.5x**) on **250M rows** through a row-identical Postgres-versus-ClickHouse POC.

## Elevator pitch (30 seconds)

"Four PDF stories on AssortSmart. Keep/Drop scores article × plan-season with ST%/ROS plus LangGraph lenses; agents stay SELECT-only on ClickHouse via CSV bake-and-promote; promotions gate on 300 gold cases and ≥80% offline accuracy. Dig-deeper QnA explains locked Keep/Drop without writing outcomes. ClickHouse POC took a planning pivot from 189s to 12.3s on 250M rows. Write plane on this track is Go / Gin; agent plane stays Python/LangGraph."

## Honesty

- Keep/Drop + QnA = real `assort_kd_flow` work.
- 300-gold / ≥80% = **promotion gate / design** — not “shipped to all tenants.”
- **Verbal only / not on PDF:** Cluster Recommendation Copilot · Hindsight (building / deep-dive via `01b_hindsight_defense.md` if asked).

## ClickHouse POC

| Claim | Tag | Defense |
|---|---|---|
| from **189s to 12.3s** (~15.5×) on **250M** row-identical PG vs CH | MEASURED | `pivot-poc/` · `21_ia_pivot_benchmark_source.md` |

## Q&A

- **"Shipped to all tenants?"** No — gold gate is the promotion bar; say continuous present / gated rollout.
- **"What about Cluster Copilot / Hindsight?"** Verbal only / not on PDF — building context if they ask.
- **"Hibernate on ClickHouse?"** No.
