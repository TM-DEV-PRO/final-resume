# Application Kit (paste-ready)

Aligned to **Final Python + Go + AI** (`Tarun_Mittal_SSE_5yr.pdf`). Canonical: `docs/ASSORTSMART_TAB_RESUME.md`.

## One-liners
- **Headline fit:** Senior SWE Python · Go · Go/Gin 10k RPS · ClickHouse 2.11B · 36 FastAPI endpoints · Kafka 1M+/day · LangGraph Ask Iris
- **30s intro:** LinkedIn About short in `linkedin/headline_about_experience.md`
- **Why hire you:** FRM 70% 14d→3d + Kafka 1M+/day + AssortSmart (10k RPS, 348k article-seasons, JSON payloads vs 2.11B master, shipped Ask Iris, 80% gate)

## Common application questions

### Describe a complex system you designed
AssortSmart (Impact Analytics): two layers. (1) Agentic — Keep/Drop + Missed Opportunities + Top Style over 348k article-seasons (88k/pass, 7 lenses); JSON payloads vs a 2.11B-row ClickHouse master with ReplacingMergeTree timeout fallback; shared registry with circuit breakers/checkpoints/config_hash; shipped Ask Iris (JWT WebSocket, LangGraph supervisor, 3-attempt evaluator, handshake-frozen hierarchy). 300-case proxy eval; 80% is a CI promotion gate vs 74% det; 73% cheaper at 100% coverage is gold-200, not the 300-case file. (2) Core — multi-tenant Go/Gin at 10k peak RPS (Wire, h2c, Datadog), ClickHouse 189s→12s on 250M-row operations with six rollup tables / 170 GB weekly OOM, KPI tokenizer with division-by-zero protection, Firebase/JWT/OIDC + Redis + Postgres roles. 100% coverage / 1,200+ Go tests is LinkedIn / verbal.

Also owned Uber FRM via EPAM: 36 FastAPI endpoints, 19M GL rows, L1–L4 FSLI, 8-table SOADB, SHA-256 keys; 70% from 14 days to 3 against $340M; led 3; 100% coverage; SOX 50% delta-variance.

### Experience with AI / LLMs / agents
AssortSmart agentic flows: structured LLM invokes across 7 lenses blended with deterministic KPI math; JSON payloads rather than LLM SQL against the 2.11B master; fallback to deterministic scores on timeout. Shipped Ask Iris — JWT WebSocket, LangGraph supervisor, 3-attempt evaluator, handshake-frozen hierarchy, LangSmith. Guardrails: 300-case proxy harness, 80% CI promotion gate, 74% deterministic baseline, freeze blend weights if the LLM loses; 73% cheaper at 100% coverage is the gold-200 model pick. Uber Eats: Gemini 2.5 Pro + LangChain RAG + Milvus at 98% field fidelity (**offline eval**), hard schema gate, 95%+ scrape success, Kafka+Flink exactly-once. ANZ 99.9% is HISTORICAL Mobility.

**Verbal only / not on PDF:** Cluster Recommendation Copilot and Hindsight (building) — use only if the form asks for a broader agentic roadmap.

### Largest scale
AssortSmart: 10k peak RPS (PDF); 2.11B-row CH master; six ClickHouse rollup tables; 348k article-seasons; 88k items/pass. Masters: high-concurrency Kafka e-invoicing, 1M+ IRP/day, 100K+ idempotent imports, 700 to 4,000 rpm. ClickHouse pivot POC 189s to 12s on 250M rows (MEASURED).

### Leadership
Led 3 (Uber/EPAM FRM). Mentored 2 (Masters).

### Production bug you resolved
**Lead with the 170GB weekly OOM (on the PDF).** Whole-season weekly INSERT SELECT sat ~170 GB and OOM'd. Fix: temporal chunks (one fiscal week), memory and disk-spill caps (verbal: 55 GB / 16 GB). Do not use a FastAPI/Kafka heap-leak packet story as the IA headline.

**Masters alternate:** IRP timeout canary — too-aggressive timeouts; moved async + idempotency.

### Why this company
Pivot to technical alignment: their [distributed store / event bus / applied-AI eval] matches ClickHouse 2.11B + Menu Kafka/Flink + 300-case promotion gates — not generic praise.

## Links
Phone (+91) 9079727197 · tmittaliet@gmail.com · linkedin.com/in/t-mittal · github.com/TM-DEV-PRO

## Attach
`artifacts/Tarun_Mittal_SSE_5yr.pdf`

## Deeper answers
Track screening bank: `prep/22_application_questions.md`\n