# Ground Truth (Final PyGo + AI)

Self-contained for this track. Do **not** treat `resume/`, `resume_v2/`, `resume_java/`, or `campaign_pygo_xyz/` as sources of truth (those tracks are being removed).

**PDF:** `Tarun_Mittal_SSE_PyGo_AI_Final.pdf` · Canonical claims: [`docs/ASSORTSMART_TAB_RESUME.md`](../../docs/ASSORTSMART_TAB_RESUME.md)

**Keep/Drop pipeline reference:** track copy [`docs/assort_kd_flow/PIPELINE.md`](../docs/assort_kd_flow/PIPELINE.md) · shared [`docs/assort_kd_flow/PIPELINE.md`](../../docs/assort_kd_flow/PIPELINE.md).

## Summary (PDF — 3 lines)

1. Senior Software Engineer with **5 years** of experience architecting high-throughput, cloud-native **distributed systems** and leading zero-downtime monolithic migrations.
2. Expert in **Python and Go microservices**, specializing in scaling event-driven pipelines, optimizing multi-billion row databases, and driving extreme latency reductions for enterprise platforms.
3. Proven track record of bridging enterprise data with fault-tolerant AI by deploying **LangGraph** multi-agent systems, **Milvus RAG** architectures, and deterministic evaluation harnesses to deliver measurable business impact.

## Skills categories (PDF)

Languages · Backend & APIs · **AI & Applied ML** · **Data & Streaming** · Databases & Storage · **Cloud & DevOps** · **Architecture & Core**

## Resume PDF — Impact Analytics / AssortSmart (TWO subsections)

Project title on PDF: **AssortSmart — Senior Software Engineer (Platform & AI)**. IA bullets are identical across tracks (Go/Python). Source: AssortSmart tab / PDF.

### 1) Platform Engineering & Infrastructure

1. Multi-tenant **Go/Gin** platform scaling to **10k peak RPS**, **Google Wire** compile-time DI, self-protecting HTTP edge (no reverse proxy), native **h2c**, nested timeouts, **Datadog** distributed tracing.
2. Retail analytics **15.5x**: pivot **189s → 12s** on **250M-row** operations. ClickHouse catalog **1.6M** article-season combinations and **2.4B** weekly rollup rows.
3. Dynamic KPI configurator + formula parser: operator-authored math tokenized into safe **ifNotFinite**-wrapped ClickHouse SQL fragments (business logic decoupled from code releases).
4. Multi-tenant + UAM-scoped hierarchy access. Redis-fronted **Firebase Admin → JWT / Google OIDC** waterfall, constant-time API keys, **Postgres**-backed role resolution.
5. **100.0%** statement-coverage CI gate (race and atomic) across **1,200+** Go tests. Bitbucket pipeline: golangci-lint, pre-push hooks, continuous **SAST/SBOM**.

### 2) Agentic Flows & Orchestration

1. Multi-pipeline AI merchandise engine (**Keep/Drop**, Missed Opportunities, Top Style) evaluating **335K+** products. **88k** items/pass under **$100** token spend; deterministic KPI math + structured LLM invokes across **7 AI lenses**.
2. Zero-data-corruption on a **2.11B-row** ClickHouse fact table by **air-gapping** batch LLM execution from database queries. **ReplacingMergeTree** two-phase inserts; JSON payloads; fallback to deterministic scores on LLM failure.
3. AI orchestration registry: circuit breakers, durable checkpoints, **LangSmith** + per-run JSON telemetry (token costs, step durations, batch fallbacks).
4. **Shipped “Ask Iris”** — WebSocket AI copilot (multi-billion-row KPIs, dynamic charts, drill-down). **LangGraph** Supervisor router + Evaluator loop; socket-level **frozen scopes**. Shipped **capability** — do not invent tenant-wide SLAs.
5. **300-case** offline evaluation harness and **≥80%** accuracy **CI promotion gate**. Candidate agents benched against a **74%** deterministic baseline. Gate ≠ “all tenants live.”

**Stack:** agent plane = Python, FastAPI, LangGraph; platform / write APIs = **Go / Gin**. MCP is **not** on this PDF.

## Uber FRM (via EPAM)

- **70%** recon cut, **14 days to 3 days**, **$340M** materiality, **19M** raw GL rows, **36 FastAPI endpoints**, nested **L1–L4 FSLI**, quarter-annualization.
- **8-table** MySQL SOADB, polymorphic review-status, optimistic row-locking, **SHA-256** natural keys.
- Led **3** engineers; SQLAlchemy 2.0 migration **100%** statement coverage; stacked Bazel PRs; SQL allowlists; FSM **50%** delta-variance; SOX.
- Tech: Python, FastAPI, SQLAlchemy 2.0, Pydantic, MySQL, Bazel, Docker

Older prep tagged 70% as TDD TARGET. **The PDF now states 70% / 14→3 days as the outcome.** Defend the PDF. If pressed: the TDD framed that cut; do not walk it back unprompted.

## Uber Eats Menu

- **24 hours → 2 hours**, **$600K**/yr, **30K+** menus/month, **98%** field fidelity (**offline eval**), Gemini 2.5 Pro + LangChain RAG + Milvus.
- **95%+** success, Selenium proxies, **Kafka**, **Flink** keyed dedupe, **exactly-once** upserts.
- **Spark is not on the PDF.** Verbal/study backfill only.

## Uber Mobility ANZ

- **99.9%** compliance, **20 hours/week** saved. **HISTORICAL Mobility** (not Eats). Uber via EPAM.

## Masters India

- p95 **1.2s → 300ms** (**75%**), **1,500+** clients, **700 → 4,000** rpm, mentored **2**.
- Kafka + PostgreSQL tax-quarter shard, **1M+/day**, **100K+** imports, idempotency, DLQ.
- ELK + New Relic, Redis **−30%** reads, coverage **35% → 82%**, **98%** deploy success.
- Stack on this PDF: **FastAPI**. Tech: Python, FastAPI, Kafka, PostgreSQL, MongoDB, Redis, Elasticsearch, Celery, Docker, ELK, New Relic, AWS

## GeeksforGeeks

- **Django**, **10K+** daily queries, **10x** contest spikes, **20%** premium, **30%** course sales, **70%** ops.

## Verbal only / not on PDF

- **Cluster Recommendation Copilot** — architecture / FRD / deep-dive; not a PDF headline bullet.
- **Hindsight** — prior-season decision layer; not a PDF headline bullet.
- Off-PDF interview depth: 8.5% (37/437) → under 2% TARGET · 14 tools · 3 gates · 63/8 DDL · line-plan ~12B → ~25M · under 1h / ≥20 configs TARGET.
- Packet stories **OOM leak** (Python/FastAPI connection leak) and **CDC dual-write** are **not PDF bullets**. Tag company + MEASURED vs DESIGN. Do **not** claim Kubernetes cluster operations or that you authored `pg2ch_cdc` (Ashvin Sharma).

## Evidence boundary

- Omit Spark, multi-region, K8s **ops**, Terraform from resume claims. Kubernetes may appear on Skills as literacy, not “I operated clusters.”
- Menu Kafka+Flink are on the PDF. IA does **not** claim Kafka/Flink/CDC as PDF bullets.
- Spoken prose: **from 189 seconds to 12 seconds**; **from 14 days to 3 days**; **from 24 hours to 2 hours**.
- CGPA removed from resume PDFs.

## Deep dives (this track)

- `10_impact_analytics_deep_dive.md` · `23a_ia_interview_pack.md`
- `11_uber_frm_deep_dive.md` · `14_uber_menu_deep_dive.md`
- `12_masters_gfg_deep_dive.md` · `13_behavioral_why_switch.md`
- `17_senior_systems_study_only.md` · `36_skills_ai_agents_defense.md`
- Keep/Drop pipeline: `../docs/assort_kd_flow/PIPELINE.md`

Verified certificates: **HackerRank Problem Solving** and **LangChain Academy**.\n