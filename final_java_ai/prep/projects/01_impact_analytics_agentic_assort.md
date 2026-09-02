# Impact Analytics — AssortSmart (Platform & AI)

**Role:** Senior Software Engineer · May 2026 – Present · Bangalore
**Resume tech:** Go, Gin, Wire, Python, FastAPI, LangGraph, ClickHouse, BigQuery, Redis, PostgreSQL, Datadog, LangSmith, GCP, Docker
**PDF title:** AssortSmart — Senior Software Engineer (Platform & AI)

> Ground truth: [`GROUND_TRUTH.md`](../GROUND_TRUTH.md). Canonical: [`../../../docs/ASSORTSMART_TAB_RESUME.md`](../../../docs/ASSORTSMART_TAB_RESUME.md). Pipeline: [`../../docs/assort_kd_flow/PIPELINE.md`](../../docs/assort_kd_flow/PIPELINE.md).

---

## PDF bullets (say these)

### Platform Engineering & Infrastructure
1. Multi-tenant **Go/Gin** to **10k peak RPS**, **Google Wire**, self-protecting HTTP edge (h2c, nested timeouts, **Datadog**).
2. **15.5x** analytics: **189s → 12s** on **250M** rows; ClickHouse **1.6M** article-seasons and **2.4B** weekly rollups.
3. KPI configurator + **ifNotFinite** formula parser → safe ClickHouse SQL fragments.
4. UAM-scoped tenancy; Redis-fronted Firebase → JWT/OIDC; constant-time API keys; Postgres roles.
5. **100.0%** statement-coverage CI (race/atomic) · **1,200+** Go tests · golangci-lint · SAST/SBOM.

### Agentic Flows & Orchestration
1. Keep/Drop + Missed Opportunities + Top Style · **335K+** products · **88k**/pass under **$100** · **7** AI lenses.
2. **2.11B-row** fact table · physical **air-gap** LLM vs DB · **ReplacingMergeTree** two-phase · deterministic fallback.
3. Orchestration registry · circuit breakers · checkpoints · **LangSmith** + per-run JSON telemetry.
4. **Shipped Ask Iris** — WebSocket copilot · LangGraph **Supervisor + Evaluator** · frozen scopes. Capability, not tenant-wide SLA.
5. **300-case** offline eval · **≥80%** CI **promotion gate** · **74%** deterministic baseline. Gate ≠ all tenants live.

## Elevator pitch (30 seconds)

"AssortSmart has two PDF chapters. Platform: I architected the multi-tenant Go/Gin edge to 10k peak RPS with Wire, h2c, and Datadog, moved planning analytics to ClickHouse — 189 seconds to 12 on 250 million rows, 1.6 million article-seasons, 2.4 billion weekly rollups — plus a KPI formula parser and Firebase/OIDC tenancy, held by a 100% coverage gate over 1,200+ Go tests. Agentic: Keep/Drop, Missed Opportunities, and Top Style over 335 thousand products, 88k items a pass under $100 across 7 lenses, air-gapped from a 2.11 billion-row fact table. I shipped Ask Iris, a WebSocket LangGraph Supervisor+Evaluator copilot with frozen scopes. Promotions require a 300-case offline harness and an 80% CI gate against a 74% deterministic baseline — that is a promotion gate, not a claim every tenant is live."

## Honesty

- 10k RPS / 2.11B / 2.4B / $100 / 1.6M / 335K+ = **on PDF** (AssortSmart tab).
- 300 / ≥80% = **promotion gate**. Ask Iris = **shipped capability**.
- **Verbal only / not on PDF:** Cluster Recommendation Copilot · Hindsight (`01b_hindsight_defense.md` if asked).

## ClickHouse POC

| Claim | Tag | Defense |
|---|---|---|
| **189s → 12s** (~15.5×) on **250M** row-identical PG vs CH | MEASURED | `pivot-poc/` · `21_ia_pivot_benchmark_source.md`. PDF rounds 12.3s→12s. |
| 1.6M article-seasons · 2.4B weekly rollups · 2.11B fact | PDF / AssortSmart tab | Catalog + fact-table scale on the resume. |

## Q&A

- **"Shipped to all tenants?"** No — gold/≥80% is the promotion bar. Ask Iris is a shipped capability without invented SLAs.
- **"What about Cluster Copilot / Hindsight?"** Verbal only / not on PDF.
- **"Did you run Kafka/Flink/K8s on IA?"** Not PDF claims. Kafka+Flink are **Menu**. K8s ops / CDC authorship are packet overclaims — do not take them.\n