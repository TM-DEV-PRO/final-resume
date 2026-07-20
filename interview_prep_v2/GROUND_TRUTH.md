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

| Claim | Tag | Source |
|---|---|---|
| **Agentic AssortSmart store (resume headline):** ClickHouse/GCS end-to-end planning store via **insert-only versioned writes** (`ReplacingMergeTree` + `argMax` / version watermark); HLD doing layer → ClickHouse/GCS only. Thin Postgres metadata (auth/tenant/workflow) may remain — not the planning SoR on this resume | MEASURED design (Jul 2026 stack direction + HLD) | `10_stack_direction_jul2026.md`, `final_agenticassort.png` |
| **POC evidence (numbers on resume):** CH cut **250M-row** pivot grids from **189.4s to 12.3s** (~15.5× COUNT DISTINCT; typical aggs ~**2–3×**); line-plan flat→aggregate avoided **~12B** store-week (**100–450×** / ~140–457×). Hardware: PG 48 GB host advantaged; CH 10 CPU / 3.3 GB Docker | MEASURED | Pivot + LinePlanning + consolidated POC |
| **POC hybrid verdict (prep / decision history):** PG wins interactive keyed UPDATE (~0.35–0.94 ms); CH wins large reads; **no wholesale CH** for legacy mtp-assort (fix BQ first). Unlocked agentic CH writes by changing write model to insert-only versions — not by claiming CH beats PG at OLTP mutations | MEASURED | consolidated POC; stack direction evolution story |
| Agentic clustering POC 5 (2026-07-06): dedicated CH for runtime **read** plane (slot-determinism vs BQ); early note said writes still PG for strategy-flow join — **superseded for agentic-assort** by Jul 2026 CH end-to-end planning-store directive | MEASURED decision → superseded for greenfield | POC §6 vs stack direction §10 |
| Existing mtp-assort: **NO** wholesale CH move now; fix BigQuery SELECT*/clustering/rollups first | MEASURED decision | consolidated POC §5 |
| **HLD Agentic System (`final_agenticassort.png`):** Path A FE→FastAPI Agent (`POST /chat` DIRECT)→LLM→tools→Go Doing Layer; Path M FE→Go REST manual; Go domains Hindsight/Clustering/Strategy; stores **ClickHouse + GCS**; obs LangSmith (L1) + Datadog (L2) + PostHog linked by OTEL `trace_id` | MEASURED design | diagram |
| Order Batching metric, 23.7M join rows: CH **3.86s** vs PG **3m40s - 7m48s** (~60x) | MEASURED (**prep depth**) | POC dump 2707030040 |
| CH insert ~**5.9M rows/s** vs PG 250K raw (~14-24x) | MEASURED (prep) | 2612625411 |
| Order Batching CQRS / CDC design (PG writes / CH reads, Redis RYW TTL ~30s) | MEASURED design (legacy/Order Batching path) | 2764046370 |
| CDC platform SLOs (p95 ≤ 10s visible; tool by Ashvin Sharma) | MEASURED | 2727084070 |
| Cluster Recommendation Copilot: LLM orchestrates, deterministic plane, 14 tools, human gates | MEASURED design (Phase 1 PASS, load test pending) | 2817589251 |
| Copilot baselines: failures 8.5% (37/437), reproducibility 0%; targets under 2%, 100% reproducible, under 1h, ≥20 configs | MEASURED / TARGET | 2817589251 |
| Agent probes: BigQuery 1–20s+ baseline vs CH p95 <500ms target | MEASURED / TARGET | 2817589251 |

Do NOT claim: identical benchmark hardware, full production CH cutover of **legacy mtp-assort**, authorship of pg2ch_cdc, shipped copilot to all tenants, PostHog/Datadog/LangSmith as sole personal ownership, or that ClickHouse beats Postgres at classic OLTP keyed UPDATE without the insert-only versioned model.

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

**RESUME DECISION (Jul 2026, restored):** Menu bullet is **Selenium scrapers on GCP → Kafka (~200–500 peak events/sec ESTIMATED) → Flink online normalize/dedupe → Spark backfills**, plus RAG/Gemini and ANZ. Best fit for Flink/Spark on this resume is Uber Menu (not Masters, not IA). Peak event rate and Spark ~1–2M backfill rows are ESTIMATED. Pinot stays off the one-pager. Kafka on Masters India remains a separate claim (e-invoicing).

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
