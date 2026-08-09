# Ground Truth Fact Sheet (campaign_pygo_xyz snapshot)

Canonical facts for the Python/Go XYZ MNC campaign resume. Mirrors `resume_v2/prep/GROUND_TRUTH.md` with campaign notes. Every resume bullet in `campaign_pygo_xyz/resume/` must trace to a row here. Tags: **MEASURED** (documented artifact), **TARGET** (design goal, say "targeting"), **HISTORICAL** (from past resumes, defensible), **ESTIMATED** (derived, say so).

**Campaign AI-marker rule:** resume bullet text must not contain `:`, `;`, or em dashes.

## Evidence matrix (95%+ resume-safe vs omit)

| Claim | Confidence | Placement | Source |
|---|---|---|---|
| Owned Uber FRM recon v1 Sheets to MySQL v2 (18 files, +1,268 LOC) | 95% MEASURED | Resume experience | `RECON_API_MIGRATION.md`, FRM code |
| Designed layered handler / service / repository / ORM architecture (11 models, 30+ APIs) | 95% MEASURED | Resume experience | `frm_scoping_service/` |
| Led 3 engineers (EPAM pod) via design reviews, API contracts, CI gates | 90% user-confirmed | Resume experience | User confirm + code conventions |
| Led Masters PHP monolith to microservices (strangler verbally), mentored 2, p95 1.2s to 300ms | 85%+ HISTORICAL | Resume experience | Past resumes + prep |
| Kafka + PostgreSQL quarter sharding: 100K+/import, 1M+/day (~12 TPS, 100+ peak), 700 to 4,000 RPM (~67 RPS) | 85% HISTORICAL / ESTIMATED peaks | Resume experience | Past resumes + metrics derivations |
| Fault tolerance: idempotency keys, retries, DLQ replay on bulk IRP path | 75% HISTORICAL narrative | Resume experience (Masters) | Masters prep + past resumes |
| On-call alerting via ELK + New Relic, triage ~70% faster | 75% HISTORICAL | Resume experience (Masters) | 4yr resume; baseline ~30 to <10 min ESTIMATED |
| Design Patterns keyword (strangler, layered, repository, cache-aside, idempotency) | 90%+ pattern evidence | Skills | FRM code + Masters migration |
| Fault Tolerance / HA / Operational Excellence / On-call skill keywords | n/a | **OMIT from Skills** (Jul 2026) — experience-only via Masters idempotency/DLQ + ELK | User skills trim; Core = Multithreading + Concurrency |
| Kafka + Flink on Uber Menu (Selenium→Kafka→Flink keyed normalize/dedupe/replay) | 70% HISTORICAL role / ESTIMATED rates | Resume experience (Menu) | Restored Jul 2026; Spark verbal/study only |
| Multi-region / active-active / DR ownership | <5% | **OMIT resume** | CDC DR doc authored by Ashvin Sharma; no personal ownership |
| Kubernetes cluster operations (kubectl/helm/operators) | <5% | **OMIT resume experience**; STUDY ONLY prep | Zero manifests / ops narrative |
| Spark production ownership on Uber Menu | <50% verbal/study | **OMIT resume** | Not on PDF |
| Terraform / IaC production ownership | <5% | **OMIT resume**; STUDY ONLY prep | Keyword blob only on old PDF |
| CGPA 7.7/10 | MEASURED | **Removed from resume PDFs** (kept here for reference) | Education record |
| Go (Gin) write APIs at IA; PostgreSQL by tax quarter + idempotency/retries/DLQ at Masters | MEASURED design / HISTORICAL | Resume experience | Simple-language PDF pass Jul 2026 |

## Career timeline (canonical)

| Company | Title | Dates |
|---|---|---|
| Impact Analytics, Bangalore | Senior Software Engineer | **14 May 2026 - Present** |
| Uber (via EPAM Systems), Bangalore | Software Engineer (A2) / SDE2 | Jul 2024 - May 2026 |
| Masters India, Noida | SDE 2 | Dec 2022 - Jun 2024 |
| GeeksforGeeks, Noida | SDE | Aug 2021 - Nov 2022 |
| IET Lucknow, B.Tech IT | CGPA **7.7/10** | Jul 2017 - Jun 2021 |

Leadership headcounts (user confirmed): **Masters India led/mentored 2 engineers; EPAM/Uber led 3 engineers.** IA is IC so far.

## Impact Analytics (May 2026 - Present)

**Source scope:** Only files **directly** under `KNOWLEDGE-MATERIAL/Impact-Analytics-work/` (incl. `pivot-poc/`) plus `PRD'S/`. **Ignore** nested `ASSORTSMART-OLD-KNOWLEDGE/` and `ClickHouse-POC-Dump/`.

| Claim | Tag | Source |
|---|---|---|
| Product: AssortSmart helps retailers decide **what to buy / how much / which stores** | MEASURED product framing | Overview §1 + Copilot FRD |
| Copilot targets: days → under **1 hour**; **1 → ≥20** (design batch **20–100**) configs/plan | TARGET | Copilot FRD §0 / §2 |
| Failures **8.5%** = **37/437** (kik); **>80%** input-boundary | MEASURED | Copilot FRD §1 |
| Failures toward **under 2%**; reproducibility **0→100%** | TARGET | Copilot FRD §0 / §6 |
| **14** audited read-only tools; **3** human confirm gates; agent tools only read planning data (writes gated) | DESIGN | Overview + Copilot FRD |
| Hindsight scorecard + grounded narration + tenant catalogs without code deploy | DESIGN / building | Hindsight FRD v1.2 |
| Per-tenant **ClickHouse**: **63 tables / 8 layers** (incl. 7 stage twins), insert-only / partition-swapped; agent **`readonly=1`**; service roles **INSERT-only** | MEASURED design | Confluence DDL Phase-1 v1.5 (`../resume_v2/prep/29_ia_ch_ddl_phase1_source.md`) |
| **5** dictionaries · **19** argMax views · **4/3/2** roles/profiles/quotas; syntax PASS on CH **25.12**; **zero runtime evidence** yet | MEASURED design | same |
| Do **not** recite **624 columns** (not on Phase-1 page); prefer **63** over overview “60” | Honesty | same |
| External review **PASS**; load test remaining — say **building**, not shipped | MEASURED design status | Overview + DDL Phase-1 |
| HLD stack: FastAPI + **LangGraph/MCP**; Go doing layer; CH + GCS; Kafka async embeddings; LangSmith/Datadog/PostHog | DESIGN + confirmed | `final_agenticassort.png` + playbook |
| **ONE resume CH bullet (Aug 2026):** Drove store decision with evidence. Row-identical **Postgres→ClickHouse** POC on **250M** heavy planning pivots **189s → 12.3s** (~**15.5×**) | MEASURED POC | `../resume_v2/prep/21_ia_pivot_benchmark_source.md` |
| Line-plan aggregates **~25M**; month rollup **sub-second**; cell edit **~0.4 ms** (PG measured). Flat **12B** projection | MEASURED ops / PROJECTED | **OMIT from PDF** (Jul 2026) — verbal/study only |
| HLR scenario cap **3–5** | DESIGN | `PRD'S/…HLR_v1.1.docx` |
| Agent probes: BQ **1–20s+** → CH **p95 <500ms** | MEASURED / TARGET | Copilot FRD |

**Resume PDF IA bullets (Aug 2026):** product · Cluster Recommendation Copilot ownership · Hindsight · Postgres→ClickHouse 250M POC. Building not shipping. 8.5%/14 tools/63-8 are interview depth. No IA TPS/RPM. Hybrid PG write-back is prep-only history.

## Uber FRM (Jul 2024 - May 2026)

| Claim | Tag | Source |
|---|---|---|
| FRM Risk Scoping platform: FastAPI + MySQL + React (Fusion.js), replaces Google Sheets / legacy Flask workbook, feeds PwC audit work papers | MEASURED | TDD, code dump |
| 8 screens (Recon, Materiality, EMI, Group Scoping, Threshold Setup, Component Scoping, Residual Risk, Summary) | MEASURED | TDD, Scoping Features |
| **30+ REST endpoints** (code truth: 32 routes + health; do NOT say 36 unless counting collab service) | MEASURED | scoping_handler.py |
| **11-table** SQLAlchemy 2.0 schema (balance_sheet, income_statement, emi_data, frm_metrics_table, scoping_questions, scoping_assessments, threshold_table_v2, level_mapping, component_entity, recon_balance_sheet, recon_income_statement); full schema.uql 16+ | MEASURED | database/models/ |
| Layered handler / service / repository / ORM architecture, MySQLManager cached engine, auth via x-auth-params-email header middleware | MEASURED | code |
| Recon v1 (Sheets-backed) to v2 (MySQL) API migration, branch tmitta1/recon-income-api-migration, 18 files, +1268 lines | MEASURED, personally owned | RECON_API_MIGRATION.md |
| ~1125 unit tests (pytest + mocks) across ~65 files, Bazel uber_py_test | MEASURED | code |
| SQLAlchemy 2.0 Mapped models, aliased() joins, hybrid raw SQL; column-aliasing bug fix plausible pattern | MEASURED style; bug fix HISTORICAL (own prep) | code |
| Materiality $340M, residual threshold $170M, ~26 BS / ~29 IS FSLIs (resume says "55 financial line items"), 14 entities, 10-Q recon | MEASURED (Q4 2025 sample) | CSVs |
| **70% reduction in manual ingestion + reconciliation time = PROJECT TARGET (TDD goal)**, not measured. Resume wording: targeting a **70% cut (~2 weeks to ~3–4 days)** — from-to is ESTIMATED analyst calendar baseline | TARGET + ESTIMATED baseline | TDD 3.1; v1 resume brackets |
| 19M GL rows to 300K: **UNSUPPORTED** (raw dumps 76K / 38K / 95K rows). DROPPED from resumes. Real scale: raw GL extracts up to ~95K rows/quarter, ~1.7-1.8K accounts, ~400 entities | MEASURED | CSVs |
| Led 3 engineers (EPAM pod) | User confirmed | - |

## Uber Menu Ingestion (same employment)

All HISTORICAL from original resume + 4yr ops numbers: 30K+ menus/month, onboarding 24h to 2h (90%), $2/menu cost killed = $600K+/yr, +95% ingestion success (anti-bot).

**Unstructured → structured:** multilingual PDFs/images → Uber Eats schema via **LangChain RAG + Gemini 2.5 Pro** over **Milvus** → schema gate → **98%/100%** offline eval. **No SFT** on PDF.

**Resume PDF:** Menu = **Selenium → Kafka → Flink** + **LangChain RAG / Gemini / Milvus** (no SFT). Masters also owns Kafka for GST e-invoice (different product).

## ANZ Driver Document Compliance (Uber Mobility — same employment, NOT Eats)

| Claim | Tag | Source |
|---|---|---|
| Python automation for **driver and vehicle documents** vs local authorities for **Uber drivers / earners in ANZ** | HISTORICAL | 4yr resume (“Uber earners in the ANZ region”) |
| **99.9%** compliance | HISTORICAL | same |
| **20 hours/week** manual verification removed | HISTORICAL only | Past resume — **not** re-measured from logs here |
| Separate Uber Mobility project; say **Uber drivers in ANZ** (no “main-app”) | Resume decision | User + past wording |

## Masters India (Dec 2022 - Jun 2024)

| Claim | Tag |
|---|---|
| Led PHP (**Laravel**) monolith to Python FastAPI microservices migration; mentored **2 engineers** | HISTORICAL + user |
| p95 latency 1.2s to 300ms (75%) for enterprise clients | HISTORICAL (all resumes agree at 1000-1200 to 300-400ms) |
| Throughput **700 to 4,000 RPM** under peak load | HISTORICAL (2.5yr resume) |
| Redis caching cut redundant DB queries ~30% | HISTORICAL (2.5yr) |
| Audit Logs feature reduced client churn ~15% | HISTORICAL (2.5yr) — prep depth |
| Bulk e-invoicing 100K+ txns/import, **1M+ daily** IRP submissions (~12 TPS avg, 100+ TPS peak ESTIMATED), **1,500+ clients** (use 1500+, drop 2500+) | HISTORICAL |
| Coverage 35% to 82%, 98% deployment success | HISTORICAL |
| ELK + New Relic on-call alerting, triage -70% (~30 min to <10 min ESTIMATED baseline) | HISTORICAL |
| Client usage dashboard / log downloads cut support tickets **~35%** | HISTORICAL (4yr) — on PDF with triage |
| Fault tolerance on bulk IRP path: idempotency keys, retries, DLQ | HISTORICAL |
| KMS encryption, RBAC, JWT, audit logging for compliance | HISTORICAL — prep depth |

## GeeksforGeeks (Aug 2021 - Nov 2022)

| Claim | Tag |
|---|---|
| PHP to Django migration, **10,000+ daily queries** (standardize 10K+; not 1K / not 100K) | User decision |
| Voting / pinning / **locking** REST APIs, +15-20% premium subscriptions (relative) | HISTORICAL |
| Influencer dashboard (earnings, transactions, coupons, filters), +30% course sales | HISTORICAL — own bullet |
| Cron orchestration (video processing, reminders, recording cleanup), +70% ops efficiency | HISTORICAL — separate bullet from course sales |
| Email/SMTP optimization 50% faster sends | HISTORICAL — prep depth |

## Achievements / education

- Code Jam 2260 / 37,000+ (2021). SIH 2020 finalist, top 3 nationally. **Global AI Hackathon, EPAM Systems**. CGPA 7.7/10 kept in ground truth only; **removed from v2 and Java resume PDFs** per Jul 2026 hardening.
- Certificates verified in `KNOWLEDGE-MATERIAL/certificates.txt`: **HackerRank Problem Solving** (`7e492a2e11be`) and **LangChain Academy** (`vkkkoij3ke`).

## Why-switch narratives (see behavioral prep)

- GFG to Masters India (1.2yr): scope jump from feature work to owning a platform migration.
- Masters to EPAM/Uber (1.5yr): scale jump, global product, Uber-grade engineering practices.
- Uber to IA (1.9yr): agentic AI + data platform ownership at senior level.
- IA (joined 14 May 2026) exploring after ~2 months: role fit / charter honesty (see prep for exact framing; never badmouth).
