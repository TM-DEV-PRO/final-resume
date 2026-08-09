# Python-focused JD pull + ATS match (13 companies)

**Date:** 2026-07-27  
**Resumes:** **v2 / PyGo primary** (Python+FastAPI real). Java only if JD is polyglot and Java helps secondary keywords.  
**Method:** Prefer postings that list **Python as required/preferred** (or AI/agent FastAPI-adjacent). Score YoE + language + keyword fit. Not an interview prediction.

## Verdict legend

| Verdict | Meaning |
|---|---|
| PASS | Clears YoE + Python gate + most keywords |
| BORDERLINE | YoE stretch, ML/platform specialty, or L5 bar |
| FAIL | Hard YoE / wrong specialty (GPU kernels, Apex-only, C/Postgres internals) |

## Executive rollup (best of v2/pygo)

| Company | # Python JDs scored | PASS | BORDERLINE | FAIL | Default PDF |
|---|---:|---:|---:|---:|---|
| Google | 3 | 2 | 1 | 0 | v2/pygo |
| Amazon | 3 | 1 | 1 | 1 | v2/pygo |
| Microsoft | 3 | 2 | 1 | 0 | v2/pygo |
| Airbnb | 2 | 1 | 0 | 1 | pygo |
| PlanetScale | 2 | 0 | 1 | 1 | v2 (Go primary; Python secondary) |
| Databricks | 3 | 1 | 1 | 1 | v2/pygo |
| Roku | 2 | 0 | 1 | 1 | v2 |
| Rubrik | 2 | 1 | 0 | 1 | v2 |
| Netflix | 2 | 0 | 1 | 1 | pygo |
| LinkedIn | 2 | 1 | 1 | 0 | v2 |
| Apple | 2 | 1 | 1 | 0 | v2 |
| Atlassian | 3 | 2 | 1 | 0 | v2/pygo |
| Salesforce | 3 | 2 | 0 | 1 | v2/pygo |
| **TOTAL** | **32** | **14** | **10** | **8** | |

**Vs general 65-JD bank:** Python lane is **stronger for Microsoft AI / Copilot, Atlassian FDE-AI, Salesforce agentic/RAG, Airbnb CSE GenAI** — and **weaker where Python means ML compilers (Neuron), Netflix Python Platform (GPU), or PlanetScale Go-first**.

**Keyword ATS (unchanged):** local pygo/v2 ~**94**/100 · agent bank v2 **89** · pygo **87**.

---

## Apply-now (Python PASS)

1. **Google** — [Senior SWE, AI/ML Google Cloud AI](https://careers.google.com/jobs/results/88495581663503046-senior-software-engineer/) — 5y Python/C++; ML infra 3y stretch → **PASS thin** if you lead FastAPI agents + ClickHouse, not “I train models.”
2. **Google** — [Senior SWE Recommendations / Search pattern](https://bluewhaleai.ai/jobs/google-senior-software-engineer-recommendations-eeee2550) — Python+C++ preferred; general backend → **PASS** with v2.
3. **Amazon** — [SDE II, AWS Data Processing & Analytics](https://tryjeremy.com/jobs/amazon-software-development-engineer-ii-aws-data-processing-and-analytic-019ee1eadf29) — Python + Spark/distributed → **PASS** (Spark gap → defend Kafka/Flink + CH; don’t claim Spark ownership).
4. **Microsoft** — [SSE Data Platform / AI Infra (FastAPI preferred)](https://aplyr.ai/jobs/cf99f0180a7b/senior-software-engineer-data-platform-ai-infrastructure) — Python/FastAPI explicit → **PASS**.
5. **Microsoft** — [MTS Backend — Copilot orchestrator/APIs](https://microsoft.ai/job/member-of-technical-staff-backend-engineer/) — Python allowed + APIs → **PASS**.
6. **Airbnb** — [SSE Community Support / GenAI-adjacent](https://careers.airbnb.com/positions/8017556/) (pattern; verify live) — Python + RAG → **PASS** with **pygo**.
7. **Databricks** — [Senior Backend SWE — AI Platform](https://www.databricks.com/company/careers/engineering/senior-backend-software-engineer--ai-platform-8035969002) — Python/Go/Java; agents → **PASS**.
8. **Rubrik** — [Senior Backend Engineer (R&D)](https://builtin.com/job/senior-backend-engineer/9394403) — Kafka/async; Python OK → **PASS**.
9. **LinkedIn** — [SSE Systems Infrastructure](https://jobs.smartrecruiters.com/LinkedIn3/744000084132730-senior-software-engineer-systems-infrastructure) — Python/Java/Go → **PASS**.
10. **Apple** — [SWE iCloud Platform](https://jobs.apple.com/en-us/details/200636744-3337/software-engineer-apple-services-engineering-icloud-platform?team=SFTWR) — polyglot; Python services exist → **PASS** if JD lists Python/Go.
11. **Atlassian** — [Senior SWE (Java/Python/Go/Kotlin)](https://www.builtinsf.com/job/senior-software-engineer/10274395) — Python listed → **PASS**.
12. **Atlassian** — [Senior FDE AI (LangChain/Python)](https://www.builtinsf.com/job/senior-forward-deployed-engineer-ai-remote/7660197) — Python + agents → **PASS** (customer-facing stretch).
13. **Salesforce** — [Distributed Systems SWE Public Cloud](https://www.salesforce.com/company/careers/jobs/jr249834/distributed-systems-software-engineer-public-cloud-midseniorleadprincipal/) — Java/Go/**Python**/Ruby → **PASS**.
14. **Salesforce** — Backend mid/senior (Python allowed polyglot) — **PASS** with v2.

---

## Per-company detail

### Google (2 PASS / 1 BORDERLINE / 0 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| [SSE AI/ML, Google Cloud AI](https://careers.google.com/jobs/results/88495581663503046-senior-software-engineer/) | 5y Python or C++; 3y ML infra | **PASS** thin | Pitch agent platforms + evals, not PyTorch training. |
| [SSE Recommendations / Search](https://bluewhaleai.ai/jobs/google-senior-software-engineer-recommendations-eeee2550) | 5y; excellent Python+C++ | **PASS** | General backend + DSA. |
| Senior Staff Gemini Enterprise (Jeremy) | **8y** Python/C++/Java/Go | **BORDERLINE→FAIL YoE** | Skip unless referral; staff bar. |

### Amazon (1 PASS / 1 BORDERLINE / 1 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| [SDE II AWS Data Processing & Analytics](https://tryjeremy.com/jobs/amazon-software-development-engineer-ii-aws-data-processing-and-analytic-019ee1eadf29) | 3y; Python + Spark workloads | **PASS** | Spark keyword gap; Flink/Kafka/CH help. |
| [SDE II eCommerce Services](https://www.amazon.jobs/en/jobs/2556973/software-development-engineer-ii-ecommerce-services-ecs) | 3y; any modern lang | **PASS** (already in gen bank) | Use pygo; Python primary. |
| [Sr SDE AI/ML AWS Neuron Inference](https://www.amazon.jobs/en/jobs/3008864/senior-software-development-engineer-ai-ml-aws-neuron-model-inference) | 5y + **leading design** + PyTorch/CUDA | **FAIL** | Compiler/inference specialty + 5y design-lead gate. |
| ASBX GenAI Tools Sr SDE (Jeremy) | 5y + **5y leading design** | **FAIL / BORDERLINE** | Treat as SDE III bar; don’t apply as Sr. |

### Microsoft (2 PASS / 1 BORDERLINE / 0 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| [SSE Data Platform AI Infra](https://aplyr.ai/jobs/cf99f0180a7b/senior-software-engineer-data-platform-ai-infrastructure) | 4y; **Python/FastAPI preferred** | **PASS** | Best Microsoft Python fit this pull. |
| [MTS Backend Copilot](https://microsoft.ai/job/member-of-technical-staff-backend-engineer/) | 4y; Python allowed | **PASS** | Orchestrator/APIs map to LangGraph story carefully. |
| [SSE Microsoft AI Copilot](https://jobs.digitalhire.com/job-listing/opening/46uP9iBnYsNnNzMswHoGyt) | 4y; Python/C#/Go/Java | **BORDERLINE** | Personalization pipelines; Azure preferred. |

### Airbnb (1 PASS / 0 BORDERLINE / 1 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| CSE / GenAI backend (Python+RAG pattern) | ~6y; Python | **PASS** | pygo; LangGraph/RAG. |
| [Payments AI/ML Foundation SSE](https://hirejack.com/jobs/airbnb.com/greenhouse-airbnb-7581839/) | **7+ y**; Python + Kafka/Spark | **FAIL** YoE | Skip. |

### PlanetScale (0 PASS / 1 BORDERLINE / 1 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| Insights / observability | 5y; Go primary, Python OK ops | **BORDERLINE** | ClickHouse/Kafka help; Go depth probed. |
| Vitess / Postgres internals | Go/C | **FAIL** for Python lane | Not a Python role. |

### Databricks (1 PASS / 1 BORDERLINE / 1 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| Senior Backend / AI Platform | 5y; Python among langs | **PASS** | Agents + SaaS. |
| [SSE Data Platform Bengaluru](https://www.databricks.com/company/careers/engineering---pipeline/senior-software-engineer---data-platform-7601580002) | **7+ y** Python/Java/Scala | **BORDERLINE** | YoE stretch. |
| [SSE Foundation Model API](https://www.databricks.com/company/careers/engineering/senior-software-engineer-foundation-model-api-8635900002) | **8+ y**; Scala/Go/Python | **FAIL** YoE | Skip. |

### Roku (0 PASS / 1 BORDERLINE / 1 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| SSE Backend CMS 5y (Java/Scala/**Python**) | 5y | **BORDERLINE** | Prefer java PDF historically; pygo OK if Python emphasized. |
| SSE Backend & Data / SDET Python | **8+ y** or test-only | **FAIL** / skip SDET | YoE or wrong track. |

### Rubrik (1 PASS / 0 BORDERLINE / 1 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| Senior Backend R&D | 5y; Python/Go | **PASS** | Same as gen bank. |
| SSE Enterprise AI | **9+ y**; deep K8s | **FAIL** | Unchanged. |

### Netflix (0 PASS / 1 BORDERLINE / 1 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| [L5 Python Platform](https://explore.jobs.netflix.net/careers/job/790315922591-software-engineer-l5-python-platform-usa-remote?domain=netflix.com) | L5; **FastAPI/Flask** + **GPU/CUDA** stack | **BORDERLINE→FAIL** | FastAPI helps; CUDA/platform ownership missing. Hold. |
| Distributed Systems L5 (gen) | L5 bar | **BORDERLINE** | Same as prior bank. |

### LinkedIn (1 PASS / 1 BORDERLINE / 0 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| SSE Systems Infrastructure | 5y Java/Python/Go | **PASS** | Kafka + scale. |
| Staff Enterprise Infra | 6–8y | **BORDERLINE** | Prefer non-Staff. |

### Apple (1 PASS / 1 BORDERLINE / 0 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| iCloud / Services (Go/Java/Python variants) | 3–5y | **PASS** | Confirm Python on that JD before apply. |
| App Store / CloudKit Java-heavy | 5–7y Java | **BORDERLINE** for Python lane | Use **java** PDF instead. |

### Atlassian (2 PASS / 1 BORDERLINE / 0 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| [Senior SWE backend](https://www.builtinsf.com/job/senior-software-engineer/10274395) | 5y; Java/**Python**/Kotlin/Go | **PASS** | Best enterprise SaaS match. |
| [Senior FDE AI](https://www.builtinsf.com/job/senior-forward-deployed-engineer-ai-remote/7660197) | 5y backend + 3y AI; Python | **PASS** | LangChain listed; your LangGraph maps. |
| Streaming Seattle JVM/Flink | 5y | **PASS** (gen bank) | Flink helps; Java PDF stronger for JVM culture. |

### Salesforce (2 PASS / 0 BORDERLINE / 1 FAIL)

| Role | YoE / Python signal | Verdict | Note |
|---|---|---|---|
| [Distributed Systems Public Cloud](https://www.salesforce.com/company/careers/jobs/jr249834/distributed-systems-software-engineer-public-cloud-midseniorleadprincipal/) | 3y; Java/Go/**Python**/Ruby | **PASS** | |
| Backend SDE mid/senior polyglot | 3y+ | **PASS** | |
| [SMTS Agentic Services](https://careers.salesforce.com/en/jobs/jr327522/senior-member-technical-staff-agentic-services/) | 6y + **Apex/Data Cloud** | **FAIL** specialty | RAG helps; Apex gate fails ATS. |

---

## What changed vs non-Python bank

| Better on Python pull | Worse / still skip |
|---|---|
| Microsoft FastAPI data platform + Copilot backend | Amazon Neuron / 5y leading-design Sr |
| Atlassian FDE AI (LangChain) | Netflix Python Platform (CUDA) |
| Google Cloud AI SWE (Python 5y) | Airbnb Payments 7y; Databricks FMAPI 8y |
| Salesforce Public Cloud (Python listed) | Salesforce Agentic SMTS (Apex) |

**This week (Python lane):** Microsoft FastAPI AI infra → Atlassian backend/FDE-AI → Amazon SDE II analytics/eCom → Salesforce Public Cloud → Google Cloud AI (thin) → Rubrik Senior Backend.

---

## Resume packaging lift (2026-07-27) — PlanetScale / Rubrik / Databricks / Airbnb

Honest wording upgrades on **v2 + PyGo + Java** (no Spark, no Vitess, no YoE invention). PDFs rebuilt same day.

| Change | Where | Target company lift |
|---|---|---|
| Lead IA with **Go (Gin) write/doing path**; Tech leads with Go, Gin | v2 / pygo | PlanetScale Vitess/Neki Go signal |
| Masters: **quarter-sharded PostgreSQL** + **idempotent sinks** | all three | PlanetScale Neki/sharded-PG narrative; Rubrik fault tolerance |
| Menu: **Flink keyed normalize/dedupe and replay** | all three | Databricks Runtime / streaming ATS |
| PyGo Core: Multithreading / Concurrency (no FT/HA/On-call keywords) | pygo skills | Kept lean per prior skills trim |
| Java: sharding + Flink phrase + RAG/Spring unchanged | java | Airbnb App Foundation (Java PDF); CSE still **pygo** |

Summary/objective left unchanged.

### Expected ATS after lift (best-of-3)

| Company | Before | After (expected) | Still skip |
|---|---|---|---|
| PlanetScale | 3 PASS / 1 BORDER / 1 FAIL | Insights/Vitess/Neki stay **PASS**; Sharded-PG BORDERLINE **softens** (app sharding ≠ product engine) | Postgres Internals (C) |
| Rubrik | 1 PASS / 2 BORDER / 2 FAIL | Senior Backend stays **PASS**; Identity still BORDERLINE | Enterprise AI 9y; Staff SRE |
| Databricks | Backend/AI PASS; Runtime stronger via Flink | Runtime confidence **up**; no Spark claim | FMAPI 8y; Bengaluru 7y stretch |
| Airbnb | Java PASS App Foundation; pygo PASS CSE | **Unchanged routing** — submit Java vs pygo correctly | 8y GenAI; 7y Payments |

**Apply routing reminder:** Airbnb JVM → `Tarun_Mittal_SSE_Java_5yr.pdf` · Airbnb GenAI/CSE + PlanetScale → v2/pygo · Databricks Runtime JVM lean → java OK · Rubrik Senior Backend → v2/pygo.

## Related

- General 65-JD: [`24_job_listings_5x_ats_scorecard.md`](24_job_listings_5x_ats_scorecard.md)
- Panel rescore: [`25_panel_ats_rescore_post_flink.md`](25_panel_ats_rescore_post_flink.md)
- EPAM scope: [`27_epam_scope_validation.md`](27_epam_scope_validation.md)
