# Application Kit (paste-ready)

Aligned to **Final PyGo + AI** (`Tarun_Mittal_SSE_5yr.pdf`). Canonical: `docs/ASSORTSMART_TAB_RESUME.md`.

## One-liners
- **Headline fit:** Senior SWE Python · Go · Go/Gin 10k RPS · ClickHouse 2.11B · 36 FastAPI endpoints · Kafka 1M+/day · LangGraph Ask Iris
- **30s intro:** LinkedIn About short in `linkedin/headline_about_experience.md`
- **Why hire you:** FRM 70% 14d→3d + Kafka 1M+/day + AssortSmart platform/AI (10k RPS, air-gapped 2.11B, shipped Ask Iris, honest promotion gate)

## Common application questions

### Describe a complex system you designed
AssortSmart (Impact Analytics): two layers. (1) Platform — multi-tenant Go/Gin at 10k peak RPS (Wire, h2c, Datadog), ClickHouse 189s→12s on 250M with 1.6M article-seasons / 2.4B weekly rollups, KPI ifNotFinite parser, Firebase/JWT/OIDC + Redis + Postgres roles, 100% coverage / 1,200+ Go tests. (2) Agentic — Keep/Drop + Missed Opportunities + Top Style over 335K+ products (88k/pass under $100, 7 lenses); air-gap LLM vs 2.11B-row fact table with ReplacingMergeTree two-phase; orchestration registry with circuit breakers/checkpoints/LangSmith; shipped Ask Iris (WebSocket, LangGraph Supervisor+Evaluator, frozen scopes). 300-case offline eval; ≥80% is a CI promotion gate vs 74% deterministic baseline — not all-tenants-live.

Also owned Uber FRM via EPAM: 36 FastAPI endpoints, 19M GL rows, L1–L4 FSLI, 8-table SOADB, SHA-256 keys; 70% from 14 days to 3 against $340M; led 3; 100% coverage; SOX 50% delta-variance.

### Experience with AI / LLMs / agents
AssortSmart agentic flows: structured LLM invokes across 7 lenses blended with deterministic KPI math; air-gapped batch LLM from CH queries; fallback to deterministic scores. Shipped Ask Iris — LangGraph Supervisor + Evaluator, socket-level frozen scopes. Guardrails: 300-case offline harness, ≥80% CI promotion gate, 74% deterministic baseline. Uber Eats: Gemini 2.5 Pro + LangChain RAG + Milvus at 98% field fidelity (**offline eval**), hard schema gate, 95%+ scrape success, Kafka+Flink exactly-once. ANZ 99.9% is HISTORICAL Mobility.

**Verbal only / not on PDF:** Cluster Recommendation Copilot and Hindsight (building) — use only if the form asks for a broader agentic roadmap.

### Largest scale
AssortSmart: 10k peak RPS (PDF); 2.11B-row CH fact; 2.4B weekly rollups; 335K+ products; 88k items/pass. Masters: Kafka e-invoicing 1M+ IRP/day, 100K+/import, 700 to 4,000 rpm. ClickHouse pivot POC 189s to 12s on 250M rows (MEASURED).

### Leadership
Led 3 (Uber/EPAM FRM). Mentored 2 (Masters).

### Production bug you resolved (packet STAR — tag honestly)
**Company:** Impact Analytics / Python FastAPI worker (packet story). **Not a PDF bullet.** Do not claim Kubernetes cluster-ops ownership.

Crisis: 504s and memory growth on a high-concurrency async worker consuming a queue. Investigation: heap + APM showed DB/HTTP clients created inside a long-lived async loop without context managers — connection/cursor leak. Fix: `async with` + pool limits + consumer backpressure. Prevention: load test at 3x peak in CI and pool metrics. Tag: DESIGN/packet for K8s pod language; the leak+fix is the engineering story.

### Why this company
Pivot to technical alignment: their [distributed store / event bus / applied-AI eval] matches ClickHouse 2.11B + Menu Kafka/Flink + 300-case promotion gates — not generic praise.

## Links
Phone (+91) 9079727197 · tmittaliet@gmail.com · linkedin.com/in/t-mittal · github.com/TM-DEV-PRO

## Attach
`artifacts/Tarun_Mittal_SSE_5yr.pdf`

## Deeper answers
Track screening bank: `prep/22_application_questions.md`\n