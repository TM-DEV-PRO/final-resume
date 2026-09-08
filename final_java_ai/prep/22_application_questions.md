# Application / screening questions (paste-ready)

Canonical copy-paste bank. HTML twin: `../ApplicationKit.html`. Align with `GROUND_TRUTH.md`.
**PDF IA (Sep 2026):** Platform + Agentic (Ask Iris, 300-case gate). Pipeline: `../docs/assort_kd_flow/PIPELINE.md`.
Cluster Copilot / 14 tools / 8.5% = **verbal / interview depth**, not PDF bullets.

---

## Autonomous AI system (LangGraph / LlamaIndex / ADK)

**Question:** Describe an autonomous AI system you built and deployed using LangGraph, LlamaIndex, or ADK.

**Honesty before paste:** Framework = **LangGraph** (not LlamaIndex/ADK). MCP is **not** on this PDF. Ask Iris is **shipped capability**. ≥80% is a **CI promotion gate**, not all-tenants-live. Cluster Copilot is verbal-only if they insist on clustering.

### Full answer

```
At Impact Analytics I own AssortSmart's agentic merchandise engine and the Ask Iris copilot. Orchestration is LangGraph (not LlamaIndex or ADK). Keep/Drop, Missed Opportunities, and Top Style evaluate 348k article-seasons — 88k items per pass — by blending deterministic KPI math with structured LLM invokes across 7 lenses. Models see JSON, not SQL, against a 2.11B-row ClickHouse master; writes go through ReplacingMergeTree with timeout fallback to det scores. An orchestration registry provides circuit breakers, durable checkpoints, config_hash, and JSON telemetry for tokens, USD, step duration, and fallbacks.

Ask Iris is a shipped WebSocket copilot. A LangGraph Supervisor routes planner questions; an Evaluator loop plus socket-level frozen scopes stop infinite LLM loops and cross-tenant reads. Planners query multi-billion-row KPIs, generate charts, and drill into AI decisions without unfreezing the warehouse.

Reliability is a gate, not a slogan: a 300-case offline harness and an 80% accuracy CI promotion bar versus a 74% deterministic baseline. I describe that as how we refuse a bad agent, not as “every tenant already runs the promoted graph.” The HTTP edge in front of this is Go/Gin at 10k peak RPS with Datadog traces; I do not claim Kubernetes cluster operations or Flink on this product (Kafka+Flink are Uber Eats menu).
```

### Short answer

```
AssortSmart uses LangGraph for Keep/Drop (7 lenses, 88k/pass, air-gapped from a 2.11B-row fact table) and for Ask Iris (Supervisor + Evaluator, frozen WebSocket scopes). Promotions require a 300-case offline eval and a 80% CI gate against a 74% deterministic baseline. That gate is not all-tenant GA. Platform APIs are Go/Gin.
```

### Bullet checklist

```
• Framework: LangGraph Supervisor+Evaluator (not LlamaIndex/ADK; MCP not on PDF)
• Product: AssortSmart Keep/Drop + Ask Iris
• Data: air-gapped LLM vs 2.11B CH fact; RMT two-phase
• Monitoring: LangSmith + per-run JSON + Datadog on the Go edge
• Reliability: 300-case / 80% CI promotion gate vs 74% baseline
• Status: Ask Iris shipped capability; gate ≠ all tenants live
```

---

## Production-grade RAG for enterprise document processing

Lead with **Uber Eats Menu** (on PDF): Gemini 2.5 Pro + LangChain RAG + Milvus, **98% field fidelity offline**, hard schema gate, 95%+ scrape, Kafka+Flink exactly-once. Do not relocate this architecture onto AssortSmart.

(Full RAG design answer from the previous bank still applies — Milvus vs pgvector, hybrid retrieval, schema gate, human review. **98% remains offline eval.**)

---

## Complex system / why hire / scale

Use `../ApplicationKit.md` and `38_why_hire_tarun_qa.md`. Largest scale: 10k RPS + 2.11B/2.4B on IA (PDF) and Masters 1M+/day (HISTORICAL).
