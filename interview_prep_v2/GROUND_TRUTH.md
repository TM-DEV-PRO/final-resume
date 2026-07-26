# Ground Truth Fact Sheet (single source for v2 + Java tracks)

Built from KNOWLEDGE-MATERIAL (ClickHouse POC dump, Uber FRM code + KT docs, IA PRDs, all past resumes) on 19 Jul 2026. Every resume bullet on the v2 and Java PDFs must trace to a row here. Tags: **MEASURED** (documented artifact), **TARGET** (design goal, say "targeting"), **HISTORICAL** (from past resumes, defensible), **ESTIMATED** (derived, say so).

## Evidence matrix (95%+ resume-safe vs omit)

| Claim | Confidence | Placement | Source |
|---|---|---|---|
| Owned Uber FRM recon v1 Sheets to MySQL v2 (18 files, +1,268 LOC) | 95% MEASURED | Resume experience | `RECON_API_MIGRATION.md`, FRM code |
| Designed layered handler / service / repository / ORM architecture (11 models, 30+ APIs) | 95% MEASURED | Resume experience | `frm_scoping_service/` |
| Led 3 engineers (EPAM pod) via design reviews, API contracts, CI gates | 90% user-confirmed | Resume experience | User confirm + code conventions |
| Led Masters PHP monolith to microservices (strangler), mentored 2, p95 1.2s to 300ms | 85%+ HISTORICAL | Resume experience | Past resumes + prep |
| Kafka + PostgreSQL quarter sharding: 100K+/import, 1M+/day (~12 TPS, 100+ peak), 700 to 4,000 RPM (~67 RPS) | 85% HISTORICAL / ESTIMATED peaks | Resume experience | Past resumes + metrics derivations |
| Fault tolerance: idempotency keys, retries, DLQ replay on bulk IRP path | 75% HISTORICAL narrative | Resume experience (Masters) | Masters prep + past resumes |
| On-call alerting via ELK + New Relic, triage ~70% faster | 75% HISTORICAL | Resume experience (Masters) | 4yr resume; baseline ~30 to <10 min ESTIMATED |
| Design Patterns keyword (strangler, layered, repository, cache-aside, idempotency) | 90%+ pattern evidence | Skills | FRM code + Masters migration |
| Fault Tolerance keyword | 85% | Skills | Masters idempotency / DLQ / retries |
| Kafka + Flink + Spark on Uber Menu (Selenium→Kafka→Flink online→Spark backfills) | 70% HISTORICAL role / ESTIMATED rates | Resume experience (Menu) | Original event-driven resume + ops numbers; peak events/sec ESTIMATED |
| Multi-region / active-active / DR ownership | <5% | **OMIT resume** | CDC DR doc authored by Ashvin Sharma; no personal ownership |
| Kubernetes cluster operations (kubectl/helm/operators) | <5% | **OMIT resume experience**; STUDY ONLY prep | Zero manifests / ops narrative |
| Spark / Flink production ownership on Uber Menu | 70% HISTORICAL role / ESTIMATED rates | Resume experience (Menu) | Restored Jul 2026; see Menu decision above. Not at Masters/IA. |
| Terraform / IaC production ownership | <5% | **OMIT resume**; STUDY ONLY prep | Keyword blob only on old PDF |
| CGPA 7.7/10 | MEASURED | **Removed from resume PDFs** (kept here for reference) | Education record |

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
| **14** audited read-only tools; **3** human confirm gates; agent never writes SQL | DESIGN | Overview + Copilot FRD |
| Per-tenant **ClickHouse**: **63 tables / 8 layers**, append-only; agent **read-only** | MEASURED design | Overview + DDL Model |
| External review **PASS**; load test remaining — say **building**, not shipped | MEASURED design status | Overview |
| HLD stack: FastAPI + **LangGraph/MCP**; Go doing layer; CH + GCS; LangSmith/Datadog/PostHog | DESIGN + confirmed | `final_agenticassort.png` |
| **ONE resume CH bullet:** store adoption + **250M** pivot **189.4s → 12.3s** (~**15.5×**) | MEASURED | `pivot-poc/results/MASTER_RESULTS.md` |
| Line-plan: projected **~12B** → **~25M** aggregate; month rollup **sub-second**; cell edit **~0.4 ms** (PG measured) | PROJECTED 12B / MEASURED ops | `LinePlanning-Benchmark.docx` |
| HLR scenario cap **3–5** | DESIGN | `PRD'S/…HLR_v1.1.docx` |
| Agent probes: BQ **1–20s+** → CH **p95 <500ms** | MEASURED / TARGET | Copilot FRD |

**Resume wording (Jul 2026):** building not shipping; under 2% marked (target); ONE CH speed claim; no IA TPS/RPM (none measured); hybrid PG write-back is prep-only history.

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

All HISTORICAL from original resume + 4yr ops numbers: 30K+ menus/month, onboarding 24h to 2h (90%), $2/menu cost killed = $600K+/yr, +95% ingestion success (anti-bot), RAG + Gemini 2.5 Pro + SFT (100% schema consistency, 98% fidelity, offline eval), ANZ compliance 99.9% / 20h week saved.

**RESUME DECISION (Jul 2026, updated):** Menu is **Selenium scrapers + RAG/Gemini + ANZ** (no Kafka/Flink/Spark on PDF — Mayank-style streaming belongs on event platforms). **Kafka ownership lives on Masters India GST e-invoice** (1M+/day, 700→4,000 req/min, idempotency/DLQ). Flink/Spark stay off skills until a real owned bullet exists. Do not put ~200–500 events/sec or ~12 TPS / ~67 RPS parentheticals on the PDF.

## Masters India (Dec 2022 - Jun 2024)

| Claim | Tag |
|---|---|
| Led PHP (Laravel) monolith to Python FastAPI microservices migration; mentored **2 engineers** | HISTORICAL + user |
| p95 latency 1.2s to 300ms (75%) for enterprise clients | HISTORICAL (all resumes agree at 1000-1200 to 300-400ms) |
| Throughput **700 to 4,000 RPM** under peak load | HISTORICAL (2.5yr resume) |
| Redis caching cut redundant DB queries ~30% | HISTORICAL (2.5yr) |
| Audit Logs feature reduced client churn ~15% | HISTORICAL (2.5yr) |
| Bulk e-invoicing 100K+ txns/import, **1M+ daily txns** (~12 TPS avg, 100+ TPS peak ESTIMATED), **1,500+ clients** (use 1500+, drop 2500+ which appears only once) | HISTORICAL |
| Coverage 35% to 82%, 98% deployment success | HISTORICAL |
| ELK + New Relic on-call alerting, triage -70% (~30 min to <10 min ESTIMATED baseline) | HISTORICAL |
| Fault tolerance on bulk IRP path: idempotency keys (client + file hash + batch index), exponential backoff retries, dead-letter replay | HISTORICAL (prep + past narratives) |
| KMS encryption, RBAC, JWT, audit logging for compliance | HISTORICAL |
| Client usage dashboard, support tickets -35% | HISTORICAL |

## GeeksforGeeks (Aug 2021 - Nov 2022)

| Claim | Tag |
|---|---|
| PHP to Django migration, **10,000+ daily queries** (user-chosen scale; old resumes said 1000+ doubts/day, 4yr said 100K, we standardize 10K+) | User decision |
| Voting/pinning REST APIs, +15-20% premium subscriptions (relative) | HISTORICAL |
| Influencer dashboard with real-time analytics, +30% course sales | HISTORICAL |
| Cron orchestration (video processing, reminders, recording cleanup), +70% ops efficiency | HISTORICAL |
| Email/SMTP optimization 50% faster sends, rate limiting | HISTORICAL (1yr/2.5yr) |

## Achievements / education

- Code Jam 2260 / 37,000+ (2021). SIH 2020 finalist, top 3 nationally. **Global AI Hackathon, EPAM Systems**. CGPA 7.7/10 kept in ground truth only; **removed from v2 and Java resume PDFs** per Jul 2026 hardening.
- Certificates verified in `KNOWLEDGE-MATERIAL/certificates.txt`: **HackerRank Problem Solving** (`7e492a2e11be`) and **LangChain Academy** (`vkkkoij3ke`).

## Why-switch narratives (see behavioral prep)

- GFG to Masters India (1.2yr): scope jump from feature work to owning a platform migration.
- Masters to EPAM/Uber (1.5yr): scale jump, global product, Uber-grade engineering practices.
- Uber to IA (1.9yr): agentic AI + data platform ownership at senior level.
- IA (joined 14 May 2026) exploring after ~2 months: role fit / charter honesty (see prep for exact framing; never badmouth).
