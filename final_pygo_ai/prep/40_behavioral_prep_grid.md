# Behavioral prep grid — project × question

**Track:** Final PyGo + AI · **PDF:** `Tarun_Mittal_SSE_5yr.pdf`

Stack: FRM = **FastAPI / SQLAlchemy 2.0** · IA platform = **Go / Gin** · agent = **Python, FastAPI, LangGraph** · Masters = **FastAPI**.

Full answers: [`07_behavioral_star_stories.md`](07_behavioral_star_stories.md) · [`39_behavioral_question_bank.md`](39_behavioral_question_bank.md).

---

## Grid

| Question theme | IA Platform + Agentic (Copilot·Hindsight verbal) | Uber FRM | Uber Menu | Masters | GFG |
|---|---|---|---|---|---|
| Ownership | 10k RPS, 100% Go tests, Ask Iris shipped, 300-case gate | 36 FastAPI endpoints, $340M, led 3 | Selenium→Kafka→Flink; 24h→2h; $600K | FastAPI; 1M+/day; mentored 2 | Django |
| Disagreement | Story 1 CH camps | Story 7 ORM | — | Sequencing | — |
| Failure | Packet OOM leak (not PDF) | Story 5 refactor | Early anti-bot | Story 10 near-miss | — |
| Dive deep | Air-gap 2.11B / ifNotFinite | Story 6 coverage | Block-rate | Idempotency | — |
| Deadline | Eval gate vs ship pressure | PwC trains | Partner SLA | GST freeze | — |
| Customer | Frozen Ask Iris scopes | PwC materiality | Multilingual menus | 1,500+ filers | — |
| Mentorship | — | Led 3 | — | Mentored 2 | — |
| Initiative | CH POC + KPI parser | Recon SOADB | Schema gate | Idempotency + DLQ | — |
| Ambiguity | Story 1; 74% vs ≥80% gate | Materiality encoding | Adversarial sources | Peak vs migration | — |
| Ethics | Promotion gate over vibe-ship | Audit reproducibility | Low-confidence review | Story 10 | — |
| Why it matters | 2.11B corruption risk | Finance SoR | $600K/yr | Compliance filings | Learning |

---

## Per-project one-liners

**IA — Platform + Agentic (PDF)**
Go/Gin 10k RPS, Wire, h2c, Datadog; CH 189s→12s / 1.6M / 2.4B; ifNotFinite; OIDC waterfall; 100%/1200+ tests. Keep/Drop + Missed Opp + Top Style, 335K+, 88k/<$100, 7 lenses; 2.11B air-gap; Ask Iris shipped; 300-case / ≥80% vs 74% (gate, not GA). **Verbal:** Copilot · Hindsight.

**Uber FRM (via EPAM)**
FastAPI / SQLAlchemy 2.0; 36 FastAPI endpoints; 19M GL; L1–L4; 8-table SOADB; SHA-256; 70% 14d→3d; $340M; led 3; 100% coverage; SOX 50%.

**Uber Menu**
24h→2h; $600K; 30K+; 95%+; 98% **offline** RAG/Milvus; Kafka+Flink exactly-once. No Spark on PDF. No SFT.

**Masters**
FastAPI; 1.2s→300ms (75%); 1M+/day; 700→4,000 rpm; 35%→82%; 98% deploy; mentored 2.

**GFG**
Django 10K+ / 10x / 20% / 30% / 70% — keep short.

---

## Loop checklist

- [ ] 2–3 stories pre-chosen
- [ ] Numbers tagged PDF / MEASURED / TARGET / HISTORICAL / gate
- [ ] Uber = via EPAM once
- [ ] Ask Iris = shipped capability; ≥80% = promotion gate
- [ ] Copilot/Hindsight not claimed as PDF bullets
- [ ] Masters Kafka ≠ Menu Kafka
- [ ] No Spark / SFT / K8s-ops / extra IA TPS
