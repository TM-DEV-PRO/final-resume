# Resume deep-explain map (study this before loops)

**Purpose:** Anything on `Tarun_Mittal_SSE_Java_AI_Final.pdf` you can defend in depth.
Canonical: `docs/ASSORTSMART_TAB_RESUME.md`.

**PDF IA (Sep 2026):** Platform (10k RPS, CH 189s→12s / 1.6M / 2.4B, KPI parser, OIDC, 100%/1200+ tests) + Agentic (335K+, 88k/<$100, 7 lenses, 2.11B air-gap, Ask Iris shipped, 300-case / ≥80% vs 74%).
**Verbal only:** Cluster Copilot · Hindsight · 14 tools / 8.5% / 63/8.

<div class="callout warn">
<b>Never break these.</b> 300-case / ≥80% is a <b>CI promotion gate</b> — not “all tenants live.”
Ask Iris is <b>Shipped</b> on the PDF as a capability — do not invent tenant-wide SLAs.
10k peak RPS / 2.11B / 2.4B / $100 token / 1.6M article-seasons / 335K+ products are <b>on the PDF</b> (source: AssortSmart tab / PDF).
Cluster Recommendation Copilot / Hindsight are <b>verbal only / not on PDF</b>.
Menu <b>98% is offline eval</b>. Uber work was <b>via EPAM</b>. ANZ 99.9% is <b>HISTORICAL Mobility</b>.
Do not invent Spark / Pinot / Kubernetes-operations / CDC ownership. Packet Kafka/Flink belongs on <b>Menu</b>, not IA.
</div>


**Packs:** [`23a`](23a_ia_interview_pack.md) · [`23b`](23b_uber_interview_packs.md) · [`23c`](23c_masters_gfg_interview_packs.md)

---

## How to answer any tech

1. **Where** — product + path.
2. **Why** — failure mode, not “industry standard.”
3. **Rejected** — one alternative.
4. **Number** — PDF vs MEASURED vs TARGET vs HISTORICAL. IA extra TPS beyond **10k peak RPS** = fail.
5. **Failure** — what breaks if this dies.

---

## Impact Analytics — AssortSmart (Platform + AI)

### User flow
Planner opens AssortSmart → platform APIs (Go/Gin, OIDC, UAM) → CH grids (ifNotFinite KPIs) → Keep/Drop / Missed Opp / Top Style run (7 lenses, air-gapped) → Ask Iris explains / charts over frozen scope.

### Architecture
```
Planner UI / Ask Iris WS
    → Go/Gin (Wire, h2c, 10k RPS, Datadog)
    → Redis + Postgres roles + ClickHouse (2.11B / 2.4B / RMT)
    → Python LangGraph (lenses + Supervisor/Evaluator)
    → LangSmith + JSON telemetry
```

### Tech on PDF

| Tech | Where | Why | Rejected | Number |
|---|---|---|---|---|
| Go/Gin + Wire | HTTP edge | 10k RPS, compile-time DI | Python public edge | 10k peak RPS PDF |
| ClickHouse | Analytics + fact | Columnar pivots | PG OLAP; Snowflake for this UI | 189s→12s; 1.6M; 2.4B; 2.11B |
| ifNotFinite parser | KPI config | No-deploy math | Hard-coded SQL | PDF |
| Firebase/OIDC/Redis/PG | Authz | Tenant bleed | Gateway-header-only | PDF |
| LangGraph | Lenses + Ask Iris | Supervisor+Evaluator, frozen scopes | Single-shot chat | Shipped capability |
| 300-case / ≥80% / 74% | CI | Beat free baseline | Vibe-ship | promotion gate |
| Datadog / LangSmith | Edge vs agent | Different questions | One tool for everything | PDF |

**Verbal:** 14 tools, 3 gates, 63/8, Copilot, Hindsight — `23a` verbal section.

---

## Uber FRM

### User flow
Finance Recon → HFM vs 10-Q → materiality / EMI / group / component / residual → PwC work papers.

### Architecture
```
Finance UI → Spring Boot / Spring Data JPA / Hibernate (36 Spring Boot endpoints)
  → 8-table MySQL SOADB, SHA-256 natural keys, optimistic locking
  → L1–L4 FSLI, 19M GL rows, $340M materiality
```

| Tech | Number |
|---|---|
| Spring Boot / Spring Data JPA / Hibernate | 36 Spring Boot endpoints |
| 70% 14d→3d | PDF outcome |
| Led 3 · 100% coverage · SOX 50% delta-variance | PDF |

8 screens / ~55×14 / 11 ORM models / 18-file recon = **verbal depth** if asked.

---

## Uber Menu + ANZ

Selenium → Kafka → Flink keyed dedupe → catalog **or** RAG/Milvus/Gemini → schema gate.
**24h→2h · $600K · 30K+ · 95%+ · 98% offline · exactly-once.** Spark not on PDF.
ANZ 99.9% / 20h HISTORICAL Mobility.

---

## Masters / GFG

Spring Boot strangler: p95 1.2s→300ms (75%), 700→4000 rpm, Kafka+PG tax-quarter shard, 1M+/day, 35%→82%, 98% deploy.
GFG Django 10K+ / 10x / 20% / 30% / 70%.
