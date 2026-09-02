> Canonical interviewer pack for `Tarun_Mittal_SSE_PyGo_AI_Final.pdf` IA bullets (Platform + Agentic). Project title: **AssortSmart — Senior Software Engineer (Platform & AI)**. Synced Sep 2026. Canonical: `docs/ASSORTSMART_TAB_RESUME.md`.

# Impact Analytics — Interview Pack

**Role:** Senior Software Engineer · Impact Analytics, Bangalore · May 2026 – Present (IC)
**Product:** AssortSmart — AI-powered retail merchandise planning
**Honesty:** 300-case / ≥80% = **CI promotion gate** (not all tenants live). Ask Iris = **shipped capability** (no invented SLAs). 10k RPS / 2.11B / 2.4B / $100 = **on PDF** (AssortSmart tab). Cluster Copilot / Hindsight = **verbal only**. No IA Kafka/Flink/K8s-ops.

Agent plane: **Python, FastAPI, LangGraph**. Platform APIs: **Go / Gin**.

---

## 1. 30s / 2min

### 30 seconds

AssortSmart has two PDF chapters. Platform: I architected the multi-tenant Go/Gin edge to **10k peak RPS** (Wire, h2c, Datadog), moved planning analytics to ClickHouse — **189s to 12s** on **250M** rows, **1.6M** article-seasons, **2.4B** weekly rollups — plus an ifNotFinite KPI parser, Firebase/JWT/OIDC tenancy, and a **100%** coverage gate over **1,200+** Go tests. Agentic: Keep/Drop + Missed Opportunities + Top Style on **335K+** products, **88k** items/pass under **$100**, **7** lenses; air-gapped LLM vs a **2.11B-row** fact table; **shipped Ask Iris** (LangGraph Supervisor+Evaluator, frozen scopes); **300-case** offline eval and **≥80%** CI promotion gate vs a **74%** deterministic baseline.

### 2 minutes

**Platform path:** tenant request → Go/Gin (Wire) → Redis-fronted OIDC waterfall → UAM/Postgres roles → ClickHouse (RMT, ifNotFinite KPI SQL) → Datadog traces.

**Agentic path:** registry starts a pipeline (Keep/Drop / Missed Opp / Top Style) → deterministic KPI math + 7 structured LLM lenses on JSON payloads **never** issued as CH writes → two-phase ReplacingMergeTree insert → checkpoints / circuit breakers → LangSmith + JSON telemetry. Ask Iris: WebSocket → Supervisor routes → Evaluator loop → frozen socket scope.

**Status:** promotion gate ≠ GA. Ask Iris is a shipped capability.

<details><summary>Verbal / not on PDF (Cluster Copilot · Hindsight)</summary>

Copilot: days → under 1h TARGET, 8.5% (37/437) MEASURED → under 2% TARGET, 14 tools, 3 gates, Phase 1 design PASS / load test pending. Hindsight: prior-season layer. 63/8 DDL and 12B→25M are interview depth, not PDF bullets.

</details>

---

## 2. Architecture (PDF-honest)

```
Planner UI / Ask Iris WS
        │
Go/Gin edge (Wire, h2c, 10k peak RPS, Datadog)
        │
 Redis   Postgres roles/UAM   ClickHouse 2.11B fact / 2.4B rollups / RMT
        │
Python agent plane — 7 lenses, 88k/pass <$100, air-gap LLM vs DB
Ask Iris — LangGraph Supervisor + Evaluator, frozen scopes
300-case harness / ≥80% CI gate vs 74% baseline
```

Packet sketches that put Kafka→Flink or K8s-ops on IA are **overclaim**. Menu owns Kafka+Flink.

---

## 3. Design decisions (PDF-first)

| Decision | Why | Tradeoff |
|---|---|---|
| Go edge, no reverse proxy | 10k RPS with h2c, nested timeouts, Wire | You own caps/SIGTERM |
| CH vs PG vs Snowflake | Columnar pivots; BQ 1–20s+ variance; Snowflake cost/latency for this UI | CH ≠ keyed UPDATE OLTP |
| Air-gap LLM vs 2.11B fact | Hallucinated SQL must not write | Extra hop; deterministic fallback |
| Supervisor+Evaluator | Stop infinite loops + tenant bleed | Framework surface |
| ≥80% gate vs 74% baseline | Models must beat a free rule | Gate can fail the agent — that is success |
| Kafka/Flink | **Menu only** | Do not move them onto IA |

---

## 4. Bullet-by-bullet (PDF Sep 2026)

### P1 — Go/Gin 10k peak RPS, Wire, h2c, Datadog

| | |
|---|---|
| **Claim** | Multi-tenant Go/Gin platform scaling to 10k peak RPS; Wire; self-protecting HTTP edge; h2c; nested timeouts; Datadog tracing |
| **Tag** | PDF / AssortSmart tab |
| **Attack** | “Is 10k measured in Datadog? Where is the reverse proxy?” |
| **Reply** | “It is a PDF claim from the AssortSmart tab — peak RPS of the Go edge we deployed without a reverse proxy, so the process owns h2c, timeouts, and traces. I will not invent a 99.9% SLA or tenant count that is not on the resume.” |

### P2 — 189s→12s / 1.6M / 2.4B

| | |
|---|---|
| **Claim** | 15.5x; 189s to 12s on 250M; 1.6M article-seasons; 2.4B weekly rollups |
| **Tag** | 189s→12s MEASURED POC (PDF rounds 12.3→12); 1.6M / 2.4B PDF catalog |
| **Attack** | “15.5× is COUNT(DISTINCT).” / “2.4B isn’t in the repo.” |
| **Reply** | “Pivot harness is row-identical 250M: ~189s to ~12s. Adversarial: strip DISTINCT and typical aggs are ~2–3×; keep option-count and cite ~13–15×. 1.6M and 2.4B are **on the PDF** (AssortSmart tab) as catalog scale after the CH migration — I defend them as resume claims, not as a number I re-derived live in this interview.” |

### P3 — ifNotFinite KPI parser

| | |
|---|---|
| **Claim** | Dynamic KPI configurator; operator math → ifNotFinite-wrapped CH SQL |
| **Tag** | PDF |
| **Reply** | “KPI changes must not require a deploy, and NaN/Inf must not poison rollups. Parser tokenizes operator formulas into safe fragments.” |

### P4 — Firebase / JWT / OIDC + Redis + Postgres roles

| | |
|---|---|
| **Claim** | UAM-scoped hierarchy; Redis-fronted Firebase Admin → JWT/Google OIDC waterfall; constant-time API keys; Postgres roles |
| **Tag** | PDF |
| **Reply** | “Cache-miss falls through to Postgres — it does not ‘degrade open.’ Constant-time compare on API keys. UAM intersects store/product scope. I do not claim I built a generic RBAC product.” |

### P5 — 100% coverage / 1200+ tests / SAST/SBOM

| | |
|---|---|
| **Claim** | 100.0% statement-coverage CI (race and atomic) across 1,200+ Go tests; golangci-lint; pre-push; SAST/SBOM |
| **Tag** | PDF |
| **Reply** | “Gate is 100% with race and atomic. If asked about coverage.out: last committed profile can be 99.93% — I say the gate, then the profile. Python pipeline plane does not claim the same gate.” |

### A1 — Keep/Drop + Missed Opp + Top Style · 335K+ · 88k/<$100 · 7 lenses

| | |
|---|---|
| **Claim** | Multi-pipeline engine; 335K+ products; 88k items/pass under $100; 7 AI lenses + deterministic KPI math |
| **Tag** | PDF / AssortSmart tab |
| **Reply** | “Three named pipelines, not a chatbot. Token budget is a PDF claim. Seven lenses on the resume; if a reviewer opens config and sees eight weights, I say typically seven fire per article.” |

### A2 — 2.11B air-gap · RMT two-phase

| | |
|---|---|
| **Claim** | Zero-corruption on 2.11B-row fact; air-gap batch LLM from DB queries; RMT two-phase; JSON payloads; deterministic fallback |
| **Tag** | PDF / AssortSmart tab |
| **Reply** | “LLM never issues ClickHouse writes. We feed JSON, insert in two phases on ReplacingMergeTree, fall back to deterministic scores if the model fails. I did not author pg2ch_cdc.” |

### A3 — Registry · breakers · checkpoints · LangSmith

| | |
|---|---|
| **Claim** | Orchestration registry; circuit breakers; durable checkpoints; LangSmith + per-run JSON telemetry |
| **Tag** | PDF |
| **Reply** | “Breakers are run-level (fail-fraction / consecutive-fail), not a per-provider Netflix Hystrix story unless asked to go deeper. Telemetry tracks tokens, step duration, fallbacks.” |

### A4 — Ask Iris shipped

| | |
|---|---|
| **Claim** | Shipped Ask Iris; WebSocket; Supervisor + Evaluator; frozen scopes |
| **Tag** | PDF **shipped capability** |
| **Reply** | “Shipped means the copilot exists with socket-level frozen scopes so a planner cannot wander into another tenant or loop forever. I will not invent questions/week or a tenant-wide SLA.” |

### A5 — 300-case / ≥80% gate / 74% baseline

| | |
|---|---|
| **Claim** | 300-case offline harness; ≥80% CI promotion gate; 74% deterministic baseline |
| **Tag** | promotion gate — **not** all tenants live |
| **Reply** | “The harness is how we refuse a bad agent. The free deterministic baseline is 74%; candidates must clear the configured ≥80% gate in CI before promotion. I do not claim production accuracy is 80% for every tenant. If asked about gold200 proxy runs vs 300-case file, I separate the files honestly.” |

### Verbal — Cluster Copilot / Hindsight (**not on PDF**)

Use only if asked. Do not volunteer as resume bullets. Deep dive: `01b_hindsight_defense.md`, `10` verbal section.

---

## 5. Mock Q&A (new PDF)

**Shipped vs gated?** Ask Iris is a shipped capability. ≥80% is a promotion gate. AssortSmart SaaS is live; I do not claim every tenant runs every agent config.

**Why not Snowflake?** Interactive planner UI + cost; CH columnar vs PG row-store; BQ slot variance 1–20s+.

**Why air-gap?** A 2.11B-row fact table cannot take hallucinated writes.

**Debug agent vs Go?** LangSmith for graph/tokens; Datadog for HTTP/CH; JSON logs with tenant_id + trace_id. Packet 4-step: isolate → traces → saturation → mitigate.

**K8s/CDC/Flink on IA?** Not PDF. Flink is Menu. CDC author is Ashvin Sharma. K8s = skills literacy, not cluster ops.

## 6. Do NOT say

- All tenants live at ≥80%
- Extra IA TPS beyond PDF 10k peak RPS
- Spark / Pinot / K8s-ops / Terraform / Flink-on-IA / MCP-on-PDF
- Cluster Copilot / Hindsight as PDF bullets
- Tenant-wide Ask Iris SLA
- “I built pg2ch_cdc”
