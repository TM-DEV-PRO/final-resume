# Ground Truth Fact Sheet (single source for v2 + Java tracks)

Built from KNOWLEDGE-MATERIAL (ClickHouse POC dump, Uber FRM code + KT docs, IA PRDs, all past resumes) on 19 Jul 2026. Every resume bullet on the v2 and Java PDFs must trace to a row here. Tags: **MEASURED** (documented artifact), **TARGET** (design goal, say "targeting"), **HISTORICAL** (from past resumes, defensible), **ESTIMATED** (derived, say so).

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
| PG vs CH POC on retail workloads (promo loaders, aggregation MVs, Order Batching metric SP) | MEASURED | POC dump 2612625411, 2707030040 |
| Order Batching metric, 23.7M join rows: CH **3.86s** vs PG **3m40s - 7m48s** (~60x) | MEASURED | 2707030040 |
| CH insert ~**5.9M rows/s** (3.9B rows, 30 parallel promos) vs PG 250K raw / 417K detach-attach (~14-24x) at ~30 vs 280 connections | MEASURED | 2612625411 |
| Export path 541s / 607 rows/s (PG) to 38s / 26.4K rows/s (CH), ~43x | MEASURED | 2612625411 |
| Incremental CH MV 0.65s per 100K insert vs PG full refresh ~4s over 1.69M rows (~85% faster) | MEASURED | 2701262897, 2702934024 |
| 10K updates on ~29M-row CARFG: full rewrite 36-39s, partition-scoped ~7s, delta join 6.7s/partition, full-table delta OOM at 14.4 GiB | MEASURED | 2780954663 |
| Fact table 17.15M rows, 432.81 MiB compressed vs 3.31 GiB raw (~7.8x compression) | MEASURED | 2642608187 |
| Order Batching migration architecture: **CQRS** (PG writes / CH reads), CDC mirrors for CARFG + plan_master + dc_pack_reserve, daily full refresh for low-churn dims, Redis read-your-writes flag TTL ~30s falling back to PG post-save | MEASURED design doc | 2764046370 |
| CDC platform SLOs (PG commit to CH visible p95 <= 10s, snapshot >= 25K rows/s) | MEASURED (tool by Ashvin Sharma; say "designed against / integrated with", NOT "built") | 2727084070 |
| Cluster Recommendation Copilot: LLM orchestrates, deterministic plane computes, 14 audited tools, agent cannot write, human approval gates | MEASURED design (Phase 1, external review PASS, load test pending) | 2817589251, 2816999437 |
| Copilot baselines: run failures 8.5% (37/437), median clustering job ~20s, reproducibility 0% | MEASURED | 2817589251 |
| Copilot targets: hierarchy-to-finalized-plan days to <1h, configs 1 to >=20, failures <2%, reproducibility 100%, CH read plane sub-second | TARGET | 2817589251 |
| Agentic cluster DDL: 63 tables / 8 layers / 624 columns, partition-swapped facts, append-only events, zero row-level mutations | MEASURED design | 2816606240 |
| Grid p95 <500ms, cell edit <80ms, History Opt <30s, 3 scenarios <60s | TARGET (platform NFRs) | Planning_Platform_Architecture_v5-2 |
| Clustering agent flow: auto feature select + k via elbow+silhouette, 3-5 scenarios per session, planner approve before master write | MEASURED PRD | Agentic_Store_Clustering_HLR_v1.1 |

Do NOT claim: identical benchmark hardware (PG 32vCPU/256GB vs CH 16vCPU/64GB), full production cutover, authorship of pg2ch_cdc tool, shipped copilot (design approved, load test pending).

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
| Materiality $340M, residual threshold $170M, ~26 BS / ~29 IS FSLIs, 14 entities, 10-Q recon | MEASURED (Q4 2025 sample) | CSVs |
| **70% reduction in manual ingestion + reconciliation time = PROJECT TARGET (TDD goal)**, not measured. Resume wording: "targeting a 70% cut" or with baseline as ESTIMATED (~2 weeks to ~3-4 days) | TARGET | TDD 3.1 |
| 19M GL rows to 300K: **UNSUPPORTED** (raw dumps 76K / 38K / 95K rows). DROPPED from resumes. Real scale: raw GL extracts up to ~95K rows/quarter, ~1.7-1.8K accounts, ~400 entities | MEASURED | CSVs |
| Led 3 engineers (EPAM pod) | User confirmed | - |

## Uber Menu Ingestion (same employment)

All HISTORICAL from 4yr resume + prep: 30K+ menus/month, onboarding 24h to 2h (90%), $2/menu cost killed = $600K+/yr, +95% ingestion success (anti-bot), RAG + Gemini 2.5 Pro + SFT (100% schema consistency, 98% fidelity, offline eval), ANZ compliance 99.9% / 20h week saved, Kafka ~200-500 peak events/s ESTIMATED, Spark backfills ~1-2M rows ESTIMATED, Pinot sub-second ops dashboards.

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
| ELK + New Relic, triage -70% (~30 min to <10 min ESTIMATED baseline) | HISTORICAL |
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

- Code Jam 2260 / 37,000+ (2021). SIH 2020 finalist, top 3 nationally. **Global AI Hackathon, EPAM Systems** (add). CGPA 7.7/10 (add).

## Why-switch narratives (see behavioral prep)

- GFG to Masters India (1.2yr): scope jump from feature work to owning a platform migration.
- Masters to EPAM/Uber (1.5yr): scale jump, global product, Uber-grade engineering practices.
- Uber to IA (1.9yr): agentic AI + data platform ownership at senior level.
- IA (joined 14 May 2026) exploring after ~2 months: role fit / charter honesty (see prep for exact framing; never badmouth).
