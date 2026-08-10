# Fresh SMTS / GenAI / Python / Go scorecard + full-bank rollup

**Date:** 2026-07-27 (evening refresh)  
**Resumes:** v2 · Java · PyGo (post Go/sharding/Flink packaging lift; summary unchanged)  
**Scope:** Fresh **Salesforce SMTS** pull + **Python / Go / GenAI** lanes across the 13 companies + rollup vs prior banks ([`24`](24_job_listings_5x_ats_scorecard.md), [`26`](26_python_job_listings_ats.md)).

## Verdict legend

| Verdict | Meaning |
|---|---|
| PASS | Clears YoE + primary lang + most keywords |
| BORDERLINE | YoE stretch, specialty gap, or Staff/SMTS bar |
| FAIL | Hard YoE, wrong specialty, or language miss |

---

## Executive rollup (all banks combined)

| Bank | # JDs | PASS | BORDERLINE | FAIL | Notes |
|---|---:|---:|---:|---:|---|
| Prior general (13 cos × ~5) | 65 | **34** | **21** | **10** | Post-Flink ([`25`](25_panel_ats_rescore_post_flink.md)) |
| Prior Python-lane | 32 | **14** | **10** | **8** | [`26`](26_python_job_listings_ats.md) |
| **This pull: SF SMTS + GenAI/Py/Go fresh** | **28** | **12** | **8** | **8** | Below |
| **Unique apply-now (deduped priority)** | — | **~40+** | — | — | See shortlist |

**Best overall PDFs:** **pygo/v2** for GenAI + Go shops · **java** for Salesforce Agentforce (Java-first) + Airbnb JVM · skip hard YoE.

---

## A. Fresh Salesforce SMTS / Agentforce (priority)

| # | Role | YoE / langs | v2 | Java | PyGo | Best | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | [SMTS Backend — Agentforce](https://www.builtinsf.com/job/software-engineering-smts/9696645) (may be closed; pattern live on careers) | **5+ y**; **Java-heavy** start + **Python** ML; Kafka/Docker; LLM guardrails | BORDERLINE | **PASS** | BORDERLINE | **java** | Strongest SF SMTS fit. Pitch FRM Java framing + IA agents/guardrails; say building not shipped. |
| 2 | [Senior AI/ML Engineer — SMTS](https://careers.salesforce.com/en/jobs/jr340228/senior-aiml-engineer-smts/) | Senior; Java or **Python**; Agents, RAG, copilots | PASS | PASS | **PASS** | **pygo** | Agentic + RAG + multi-tenant maps. |
| 3 | [Senior/Lead — Agentforce Voice Agents](https://careers.salesforce.com/en/jobs/jr329851/seniorlead-software-engineer-agentforce-voice-agents/) | **5+ y** SaaS distributed; **Python**; GenAI | PASS | BORDERLINE | **PASS** | **pygo** | Voice/ASR gap → backend GenAI path OK. |
| 4 | [Senior/Lead/Principal — Agentforce Ops / Supply Chain](https://careers.salesforce.com/en/jobs/jr340462/seniorleadprincipal-software-engineer-agentforce-operations/) | Senior+; Java/**Python**/**Go**; queues | BORDERLINE | BORDERLINE | BORDERLINE | **pygo** | Lead/Principal stretch; Go/GraphQL preferred. Apply Senior track only. |
| 5 | [Senior/Lead AI SWE — Agentforce Supply Chain](https://careers.salesforce.com/en/jobs/jr323328/seniorlead-ai-software-engineer-agentforce-for-supply-chain/) | Senior+; Python/Go/Java | BORDERLINE | BORDERLINE | BORDERLINE | **pygo** | Agent planning maps; Lead title stretch. |
| 6 | [Data Engineer SMTS/LMTS — Knowledge Graph & AI](https://www.salesforce.com/company/careers/jobs/jr347480/data-engineer-smtslmts-knowledge-graph-ai/) | **8+ y**; Python | FAIL | FAIL | FAIL | — | YoE hard fail. |
| 7 | [SMTS — Cloud Reliability](https://www.salesforce.com/company/careers/jobs/jr328096/software-engineering-smts-cloud-reliability/) | **7+ y**; Terraform/AWS deep; Python/Go tooling | FAIL | FAIL | FAIL | — | Platform/SRE specialty + YoE. |
| 8 | [SMTS/MTS — Platform Eng Bangalore (K8s)](https://careers.salesforce.com/en/jobs/jr347341/software-engineering-smts-mts-platform-engineering-backend-kubernetes-cloud/) | **7+ y**; Java/Python/Go; **K8s** | FAIL | BORDERLINE | FAIL | **java** thin | SMTS YoE+K8s ops; MTS only if recruiter opens mid level. |
| 9 | Distributed Systems SWE Public Cloud (prior) | 3+ y; Java/Go/**Python**/Ruby | PASS | PASS | PASS | **v2** | Still open pattern — apply. |
| 10 | Backend SDE Mid/Senior (prior) | 3+ y OO | PASS | PASS | PASS | **v2** | Still apply. |

**Salesforce SMTS subtotal (rows 1–8):** PASS **2** · BORDERLINE **3** · FAIL **3** (best-of-3)

**Apply SF this week:** (1) AI/ML SMTS agentic · (2) Agentforce SMTS backend **java** · (3) Agentforce Voice **pygo** · (4) Public Cloud / Backend mid-senior from prior bank.

---

## B. Fresh GenAI lane (all companies)

| Company | Role | YoE / stack | Best PDF | Verdict | Note |
|---|---|---|---|---|---|
| **Databricks** | [Senior Backend SWE — AI Platform](https://www.databricks.com/company/careers/engineering/senior-backend-software-engineer--ai-platform-8035969002) | 5y; Scala/Go/**Python** | pygo | **PASS** | Agents + APIs. |
| **Databricks** | [Staff Backend — AI Platform](https://www.databricks.com/company/careers/engineering/staff-backend-software-engineer--ai-platform-8367019002) | Staff bar; Scala/Go/Python | v2 | **BORDERLINE** | Staff ≠ SSE; skip unless referral. |
| **Databricks** | [Sr MLE — GenAI Platform](https://www.databricks.com/company/careers/engineering---pipeline/senior-machine-learning-engineer---genai-platform--6954585002) | 4y+; Python/Scala/Go; ML platform | pygo | **BORDERLINE** | Platform/ML lifecycle > app agents. |
| **Databricks** | [SSE AI Runtime](https://www.databricks.com/company/careers/engineering/senior-software-engineer-ai-runtime-8582276002) | GPU training runtime | — | **FAIL** | GPU/scheduler specialty. |
| **Databricks** | Staff Fullstack Agentic (LangGraph) | **8+ y** + 2y prod agents | — | **FAIL** | YoE. |
| **Google** | [SSE AI/ML Google Cloud AI](https://careers.google.com/jobs/results/88495581663503046-senior-software-engineer/) | 5y Python/C++; ML infra | pygo | **PASS** thin | Agents not model training. |
| **Amazon** | ASBX GenAI / Neuron Sr | 5y **leading design** | — | **FAIL** | Design-lead gate / CUDA. |
| **Amazon** | SDE II eCom / analytics (prior) | 3y; Python OK | v2 | **PASS** | Keep applying. |
| **Microsoft** | [MTS Backend Copilot](https://microsoft.ai/job/member-of-technical-staff-backend-engineer/) | 4y; Python OK | pygo | **PASS** | Orchestrator/APIs. |
| **Microsoft** | SSE Data Platform AI Infra (FastAPI) | 4y; **Python/FastAPI** | pygo | **PASS** | Best MSFT Python fit. |
| **Airbnb** | CSE GenAI / RAG pattern | ~6y; Python | pygo | **PASS** thin | YoE stretch. |
| **Airbnb** | Payments AI 7y / Bangalore 8y | 7–8y | — | **FAIL** | Skip. |
| **Atlassian** | [Senior FDE AI](https://www.builtinsf.com/job/senior-forward-deployed-engineer-ai-remote/7660197) | 5y + LangChain/Python | pygo | **PASS** | Customer-facing stretch. |
| **Atlassian** | Senior Backend (Python listed) | 5y | v2 | **PASS** | |
| **Rubrik** | [SSE Enterprise AI](https://www.rubrik.com/company/careers/departments/job.7849713) | **9+ y**; Python/Go; **K8s ops** | — | **FAIL** | Unchanged. |
| **Rubrik** | Senior Backend R&D (prior) | 5y | v2 | **PASS** | Prefer this over Enterprise AI. |
| **Netflix** | L5 Python Platform | L5; FastAPI + **CUDA** | pygo | **BORDERLINE→FAIL** | Hold. |
| **Salesforce** | SMTS Agentforce / AI-ML (above) | 5y | java/pygo | **PASS** | See §A. |
| **LinkedIn** | SSE Systems Infra | 5y Java/Python/Go | v2 | **PASS** | Not GenAI-primary. |
| **Apple** | iCloud / Services | 3–5y polyglot | v2 | **PASS** | Confirm Python on JD. |

**GenAI lane subtotal (unique fresh rows):** ~PASS **10** · BORDERLINE **5** · FAIL **6**

---

## C. Fresh Python / Go backend lane (non-GenAI emphasis)

| Company | Role pattern | Lang gate | Best PDF | Verdict |
|---|---|---|---|---|
| **PlanetScale** | Vitess / Neki Orchestration / Insights | **Go** strong | v2/pygo | **PASS** (Insights strongest) |
| **PlanetScale** | Postgres Internals | **C** | — | **FAIL** |
| **PlanetScale** | Sharded Postgres product | Go + DB engine | v2 | **BORDERLINE** (app sharding ≠ product) |
| **Google** | Workspace Infra / general SSE | Python/Go/Java | v2 | **PASS** |
| **Amazon** | SDE II (Python OK lists) | any modern | v2 | **PASS** |
| **Databricks** | Senior Backend | Go/Java/Scala | v2 | **PASS** |
| **Databricks** | Runtime / Spark engine | Java/Scala + Spark | java | **BORDERLINE→PASS** thin (Flink helps; no Spark claim) |
| **Roku** | Backend CMS 5y | Java/Python | java | **BORDERLINE→PASS** |
| **Roku** | 8y Backend/Data | 8y | — | **FAIL** |
| **Apple** | iCloud Account Services Java/Go | Java/Go | v2 | **PASS** |
| **LinkedIn** | Systems Infrastructure | Python/Go/Java | v2 | **PASS** |

---

## D. Full apply-now shortlist (deduped, this week)

Submit in this order:

1. **Salesforce** — AI/ML SMTS (Agentic/RAG) → **pygo**  
2. **Salesforce** — SMTS Agentforce backend → **java**  
3. **Salesforce** — Public Cloud / Backend mid-senior → **v2**  
4. **Microsoft** — FastAPI AI infra / Copilot backend → **pygo**  
5. **Databricks** — Senior Backend AI Platform → **pygo**  
6. **Atlassian** — Senior Backend + FDE AI → **java** / **pygo**  
7. **PlanetScale** — Insights → Vitess/Neki → **v2**  
8. **Amazon** — SDE II eCom / analytics → **v2**  
9. **Airbnb** — App Foundation → **java**; CSE GenAI → **pygo**  
10. **Rubrik** — Senior Backend R&D only → **v2**  
11. **Google** — Cloud AI / general SSE → **v2**  
12. **LinkedIn** — Systems Infra → **v2**

### Still skip (structural)

- Salesforce Knowledge Graph **8y**, Cloud Reliability **7y** Terraform, Platform SMTS **7y** K8s  
- Rubrik Enterprise AI **9y**  
- Airbnb **7–8y**, Databricks Staff/8y agentic, AI Runtime GPU  
- PlanetScale Postgres C internals  
- Amazon Neuron / 5y leading-design Sr  

---

## E. Keyword ATS (post-lift, unchanged banks)

| Resume | Local 34-kw bank | Agent bank (prior) |
|---|---:|---:|
| v2 | ~94 | 89 |
| Java | ~91 | 91 |
| PyGo | ~94 | 87 |

**New keyword hits vs SF SMTS / GenAI:** LangGraph, MCP, RAG, guardrails/human gates, multi-tenant, Kafka, Flink, Go/Gin, FastAPI — all present on pygo/v2; Java clears Agentforce Java-first gate.

---

## F. Honest interview guardrails (same as panel)

- IA: **building**, under 2% / under 1h **targets**, load test pending  
- FRM 70%: **targeting**  
- EPAM: tech lead of pod, not Uber FTE  
- No Spark / K8s operator / Vitess internals claims  

## Related

- [`24_job_listings_5x_ats_scorecard.md`](24_job_listings_5x_ats_scorecard.md) · [`25_panel_ats_rescore_post_flink.md`](25_panel_ats_rescore_post_flink.md) · [`26_python_job_listings_ats.md`](26_python_job_listings_ats.md) · [`27_epam_scope_validation.md`](27_epam_scope_validation.md)
