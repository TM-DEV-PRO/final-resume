# Senior screen deep Q&A — millions / prod / perf / product / deploy

**PDF:** `Tarun_Mittal_SSE_PyGo_AI_Final.pdf`. Tags per `GROUND_TRUTH.md`.
**Stack:** FRM/Masters = **FastAPI / SQLAlchemy 2.0** / **FastAPI**. AssortSmart platform = **Go Gin**. Agent = **Python, FastAPI, LangGraph**. MCP not on PDF.

---

## 0. Thirty-second cheat sheet

| Question | Lead with | Number | Honesty |
|---|---|---|---|
| Millions of requests / rows? | IA 10k RPS + 2.11B fact **or** Masters IRP | 10k peak RPS; 2.11B; 2.4B rollups; 1M+/day | PDF / HISTORICAL |
| Production issue? | Packet OOM leak (tag not-PDF) **or** Menu anti-bot **or** IRP near-miss | 95%+; zero dup filings | HISTORICAL / packet |
| Perf? | CH pivot **or** Masters p95 **or** Menu 24h→2h | 189s→12s; 1.2s→300ms | MEASURED / HISTORICAL |
| Core product? | AssortSmart Platform+AI / FRM / Eats / GST / GFG | — | |
| Complex system? | AssortSmart air-gap+Ask Iris **or** Menu E2E **or** FRM SOADB | 2.11B; exactly-once | PDF / HISTORICAL |
| Deploy? | Go 100% coverage gate **or** Masters canary **or** Menu Kafka rewind | 100%; 98% deploy | PDF / HISTORICAL |

---

## 1. Core products

### Q1.1 Impact Analytics / AssortSmart

**Answer:** Merchandise-planning SaaS. On this PDF I own **two** chapters. Platform: Go/Gin **10k peak RPS**, Wire, h2c, Datadog; ClickHouse **189s to 12s** on **250M**, **1.6M** article-seasons, **2.4B** weekly rollups; ifNotFinite KPI parser; Firebase/JWT/OIDC; **100%** / **1,200+** Go tests. Agentic: Keep/Drop + Missed Opportunities + Top Style on **335K+** products, **88k**/pass under **$100**, **7** lenses; **2.11B-row** fact air-gapped from batch LLM; **shipped Ask Iris** (Supervisor+Evaluator, frozen scopes); **300-case** / **≥80%** CI promotion gate vs **74%** baseline. **Verbal only:** Cluster Copilot · Hindsight.

**Honesty:** Gate ≠ all tenants live. Do not invent extra TPS. Do not claim K8s-ops or Flink on IA.

### Q1.2 Uber via EPAM

1. **FRM:** 36 FastAPI endpoints, 19M GL, L1–L4, 8-table SOADB, SHA-256, 70% from 14 days to 3, $340M, led 3, 100% coverage, SOX 50% delta-variance.
2. **Menu:** 24h→2h, $600K, 30K+, 98% offline RAG/Milvus, 95%+, Kafka+Flink exactly-once.
3. **ANZ Mobility:** 99.9%, 20h/week HISTORICAL. Not Eats.

Employment **via EPAM**. No React ownership.

### Q1.3–1.4 Masters / GFG
GST e-invoicing, 1,500+ clients, Kafka IRP 1M+/day, FastAPI strangler.
GFG doubt-support Django, 10K+, 10x spikes, 20%/30%/70%.

---

## 2. Complex system

**A. AssortSmart (best “platform + AI” story)** — 23a architecture; air-gap; Ask Iris frozen scopes; eval gate.

**B. Menu** — adversarial + streaming + LLM schema gate.

**C. FRM** — SOX-grade scoping, optimistic locking, SHA-256 keys, 19M GL.

**D. Masters strangler + Kafka IRP** — deadline windows, idempotency.

---

## 3. Production issue

Prefer Menu anti-bot or Masters near-miss (on-resume adjacent).
**Packet OOM leak:** Impact Analytics Python/FastAPI worker; connection/cursor leak in a long-lived async loop; context managers + pool limits + backpressure. **Not a PDF bullet.** Do not claim you operated the Kubernetes cluster.

---

## 4. Performance

CH 189s→12s MEASURED POC. Masters p95 1.2s→300ms HISTORICAL. Menu 24h→2h. IA 10k peak RPS is PDF — do not add p99 you cannot defend.

---

## 5. Deploy / CI

IA: 100% Go coverage (race/atomic), golangci-lint, SAST/SBOM, Bitbucket. Ask Iris configs promote only if ≥80% offline gate passes vs 74% baseline.
Masters: 98% deploy, 35%→82% coverage, canary strangler.
Menu: Kafka rewind after bad parser.

---

## 6. L5 fit (packet)

“I fit senior because I own RFCs and gates — ClickHouse migration, FRM SOX 50% delta-variance, agent promotion vs a free deterministic baseline — and I mentor. I do not claim K8s cluster operations.”

**Debug agentic:** Datadog traces/timeouts/pools first, then LangGraph checkpoint / Evaluator loop / frozen scope / Pydantic-or-schema guards. Same as packet Q2, minus overclaimed infra.
