> **PDF sync (Sep 2026):** AssortSmart has TWO PDF subsections — Platform Engineering & Infrastructure, and Agentic Flows & Orchestration. Canonical: `docs/ASSORTSMART_TAB_RESUME.md`. **Verbal only / not on PDF:** Cluster Recommendation Copilot · Hindsight · 8.5%/14 tools/3 gates · 63/8 DDL · line-plan 12B. Hindsight defense: `01b_hindsight_defense.md`.

# Impact Analytics — Interview Pack

**Role:** Senior Software Engineer · Impact Analytics, Bangalore · May 2026 – Present (IC)
**Product:** AssortSmart — retail merchandise planning (Platform & AI)
**Honesty:** 300-case / ≥80% = promotion gate. Ask Iris = shipped capability. 10k RPS / 2.11B / 2.4B / $100 = on PDF. No IA Kafka/Flink/K8s-ops ownership.

---

## 1. 30s / 2min project explain

### 30 seconds (PDF first)

AssortSmart helps retailers decide what to buy, how much, and for which stores. I own two PDF surfaces. Platform: Go/Gin at 10k peak RPS (Wire, h2c, Datadog), ClickHouse 189s to 12s on 250M with 1.6M article-seasons and 2.4B weekly rollups, KPI ifNotFinite parser, Firebase/JWT/OIDC tenancy, 100% coverage over 1,200+ Go tests. Agentic: Keep/Drop + Missed Opportunities + Top Style on 335K+ products, 88k items/pass under $100, 7 lenses; air-gapped LLM vs a 2.11B-row fact table; shipped Ask Iris (LangGraph Supervisor+Evaluator, frozen scopes); 300-case / ≥80% CI promotion gate vs 74% deterministic baseline.

### 2 minutes (architecture + evidence)

```
Planner UI / Ask Iris WebSocket
        │
Go/Gin HTTP edge (Wire DI, h2c, 10k peak RPS, Datadog tracing)
        │
   ┌────┼──────────────┬─────────────────────────┐
Redis  Postgres      ClickHouse                 Python agent plane
auth   roles/UAM     2.11B fact, 2.4B rollups   Keep/Drop + Missed Opp + Top Style
cache                ReplacingMergeTree         7 lenses, 88k/pass <$100
                     ifNotFinite KPI SQL        air-gap LLM vs DB
                                                registry / breakers / checkpoints
                                                LangSmith + JSON telemetry
                                                Ask Iris Supervisor+Evaluator
                                                300-case / ≥80% gate vs 74% baseline
```

**Evidence:** pivot POC 250M **189s → 12s** (~15.5×, MEASURED). Catalog/fact numbers are **PDF / AssortSmart tab**.

**Verbal only / not on PDF:** Cluster Recommendation Copilot (days → under 1h TARGET, 8.5% baseline, 14 tools, 3 gates) and Hindsight.

**Status:** Keep/Drop + Ask Iris are real assort_kd_flow / shipped-capability work. Gold / ≥80% is a **promotion gate** — not “all tenants live.”

---

## 2. Design decisions (PDF-first)

| Decision | Why | Tradeoff | Do not say |
|---|---|---|---|
| Go/Gin as HTTP edge, no reverse proxy | Compile-time Wire DI, h2c, nested timeouts, Datadog at the process that serves 10k peak RPS | You own timeouts/body caps/SIGTERM drain instead of inheriting nginx | Invented SLA / multi-region |
| ClickHouse vs Postgres vs Snowflake | Columnar + SIMD for planner pivots; self-hosted latency vs Snowflake/BQ slot variance and cost | CH is weak at keyed UPDATEs — insert-only / RMT, not OLTP cells | “I chose Snowflake” / “CH replaces PG for edits” |
| Air-gap LLM vs 2.11B fact | Hallucinated SQL must never write the warehouse; JSON payloads in, two-phase RMT out | Extra hop; fallback to deterministic scores when LLM fails | Agents have a SQL shell |
| LangGraph Supervisor+Evaluator on Ask Iris | Frozen socket scopes + eval loop stop infinite LLM loops and tenant bleed | Framework surface | Tenant-wide Ask Iris SLA |
| 300-case / ≥80% CI gate vs 74% baseline | Promotion requires beating a free deterministic rule, not vibes | Gate can fail models (that is the point) | “We hit 80% in production for all tenants” |
| Kafka/Flink | **Menu**, not IA | — | Flink/CDC/K8s-ops on AssortSmart |

Packet CH vs PG vs Snowflake one-liner: Postgres is row-store OLTP — multi-column planner pivots scan whole rows and lock. ClickHouse reads only needed columns and vectorizes. Snowflake/BQ lose when the UI needs interactive, self-hosted, sub-20s pivots you already pay to operate.

---

## 3. Bullet-by-bullet defense

See `../../prep/23a_ia_interview_pack.md` for the full P1–P5 / A1–A5 tables.

## 4. Mock notes

- **Ask Iris shipped?** Yes, as a capability with frozen scopes. No invented QPS/SLA.
- **pg2ch_cdc?** Ashvin Sharma. DESIGN against patterns; you did not author CDC.
- **OOM leak?** Packet STAR, Python/FastAPI — not a PDF bullet; do not claim K8s cluster operations.
- **Cluster Copilot?** Verbal only.

## 5. Do NOT say

- All tenants live on the ≥80% gate
- IA TPS beyond the PDF **10k peak RPS**
- Spark / Pinot / K8s ops / Terraform / Flink-on-IA
- MCP as a PDF skill
- Cluster Copilot / Hindsight as resume bullets\n