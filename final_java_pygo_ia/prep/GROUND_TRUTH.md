# Ground Truth (Final Java + AI (IA = Py/Go))

Self-contained for this track. Do **not** treat `resume/`, `resume_v2/`, `resume_java/`, or `campaign_pygo_xyz/` as sources of truth (those tracks are being removed).

**PDF:** `Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf` · Canonical claims: [`docs/ASSORTSMART_TAB_RESUME.md`](../../docs/ASSORTSMART_TAB_RESUME.md)

**Keep/Drop pipeline reference:** track copy [`docs/assort_kd_flow/PIPELINE.md`](../docs/assort_kd_flow/PIPELINE.md) · shared [`docs/assort_kd_flow/PIPELINE.md`](../../docs/assort_kd_flow/PIPELINE.md).

## Summary (PDF — 3 lines)

1. Senior Software Engineer with **5 years** of experience designing and owning cloud-native, high-throughput **distributed systems**.
2. Expertise in **Java, Python and Go** microservices, with applied experience in **AI-assisted** and **RAG** systems.
3. Proven track record shipping production systems, leading backend migrations, and improving reliability, performance, and scalability.

## Skills categories (PDF)

Languages · Backend & APIs · **Generative AI** · **Data & Streaming** · Databases & Storage · **Cloud & DevOps** · **Architecture & Core**

## Resume PDF — Impact Analytics / AssortSmart (TWO subsections)

Project title on PDF: **AssortSmart — Senior Software Engineer (Platform & AI)**. Order on PDF: **Agentic Flows** then **Core Infrastructure**. IA bullets are identical across tracks (Go/Python). Source: AssortSmart tab / PDF. Defense: [`43_ia_bullet_defense.md`](43_ia_bullet_defense.md).

### 1) Agentic Flows & Orchestration

1. Multi-pipeline AI merchandise engine (**Keep/Drop**, Missed Opportunities, Top Style) evaluating **348k article-seasons**. **88k** items/pass; deterministic KPI math + structured LLM invokes across **7 AI lenses**. **$100/pass** still true, **off PDF**.
2. Decoupled inference from a **2.11B-row** ClickHouse master via JSON payloads (no direct DB querying from the LLM). **ReplacingMergeTree** eventually-consistent writes; fallback to deterministic baselines on **LLM timeouts**.
3. Shared orchestration registry: hard timeouts, circuit breakers, durable checkpoints that skip redundant det scoring; frozen **config_hash** on output rows; JSON telemetry (tokens, USD, step duration, batch fallbacks).
4. **Shipped “Ask Iris”** — JWT-secured WebSocket copilot. **LangGraph** supervisor + **3-attempt** evaluator; **LangSmith**; hierarchy frozen on socket handshake. Shipped **capability** — do not invent tenant-wide SLAs.
5. **300-case** proxy harness and **80%** accuracy **CI gate**. **73%** live cost cut at **100% coverage** (gold-200 Luna vs mini — **not** the 300-case file). **74%** deterministic baseline; freeze blend weights when the LLM loses. Gate ≠ “all tenants live.”

### 2) Core Infrastructure & Pipeline

1. Multi-tenant **Go/Gin** platform scaling to **10k peak RPS**, **Google Wire** compile-time DI, self-protecting HTTP edge (no reverse proxy), native **h2c**, nested timeouts, **Datadog** distributed tracing.
2. Dynamic KPI configurator + formula parser: operator math tokenized into parameterized ClickHouse SQL fragments with native division-by-zero protection (`ifNotFinite` wrap — verbal mechanism).
3. **Multi-tenant data isolation** + UAM-scoped hierarchy **access control** across **PostgreSQL** and **ClickHouse**. Redis-fronted **Firebase Admin → JWT / Google OIDC** waterfall, constant-time API keys, **Postgres**-backed role resolution. Isolation ≠ encryption.
4. Reduced planner pivot latency by **15.5×** (**189s to 12s** on **250M-row** operations) via ClickHouse season/weekly rollups. Prevented **170GB** OOM by slicing inserts into temporal chunks and enforcing distributed memory + disk-spill caps. Verbal knobs: one fiscal week, **55GB** / **16GB**. Six tables stay the interview drawing. **1.6M** catalog article-seasons still true, off PDF.
5. Migrated ClickHouse rollups across Cloud clusters at **~344k rows/s** with a custom Go native-TLS data pump (allowlist bypass). Partitions up to **4.09B**, **500k-row** double-buffered batches, TSV ledgers, atomic **partition rollbacks** (`DROP PARTITION` then recopy — not a live reader swap). Copy of 4.09B was in flight. **100% / 1,200+ tests** off PDF (LinkedIn / verbal).

**Stack:** agent plane = Python, FastAPI, LangGraph; platform / write APIs = **Go / Gin**. MCP is **not** on this PDF.

## Uber FRM (via EPAM)

- **70%** recon cut, **14 days to 3 days**, **$340M** materiality, **19M** raw GL rows, **36 Spring Boot endpoints**, nested **L1–L4 FSLI**, quarter-annualization.
- **8-table** MySQL SOADB, polymorphic review-status, optimistic row-locking, **SHA-256** natural keys.
- Led **3** engineers; Spring Data JPA / Hibernate migration **100%** statement coverage; stacked Bazel PRs; SQL allowlists; FSM **50%** delta-variance; SOX.
- Tech: Java, Spring Boot, Spring Data JPA, Hibernate, MySQL, JUnit, Bazel, Docker

Older prep tagged 70% as TDD TARGET. **The PDF now states 70% / 14→3 days as the outcome.** Defend the PDF. If pressed: the TDD framed that cut; do not walk it back unprompted.

## Uber Eats Menu

- **24 hours → 2 hours**, **$600K**/yr, **30K+** menus/month, **98%** field fidelity (**offline eval**), Gemini 2.5 Pro + LangChain RAG + Milvus.
- **95%+** success, Selenium proxies, **Kafka** + **Flink** large-scale data ingestion and processing pipeline, keyed dedupe, **exactly-once** catalog upserts. Not ClickHouse. Not zero message loss.
- **Spark is not on the PDF.** Verbal/study backfill only.

## Uber Mobility ANZ

- **99.9%** compliance, **20 hours/week** saved. **HISTORICAL Mobility** (not Eats). Uber via EPAM.

## Masters India

- p95 **1.2s → 300ms** (**75%**), **1,500+** clients, **700 → 4,000** rpm, mentored **2**.
- Kafka + PostgreSQL tax-quarter shard, **high-concurrency** **1M+/day**, **100K+** **idempotent** imports, DLQ / fault-tolerant state.
- ELK + New Relic, Redis **−30%** reads, coverage **35% → 82%**, **98%** deploy success.
- Stack on this PDF: **Spring Boot**. Tech: Java, Spring Boot, Hibernate, Kafka, PostgreSQL, MongoDB, Redis, Elasticsearch, Docker, ELK, New Relic, AWS

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

- `10_impact_analytics_deep_dive.md` · `23a_ia_interview_pack.md` · `42_clickhouse_rollup_migration.md`
- `11_uber_frm_deep_dive.md` · `14_uber_menu_deep_dive.md`
- `12_masters_gfg_deep_dive.md` · `13_behavioral_why_switch.md`
- `17_senior_systems_study_only.md` · `36_skills_ai_agents_defense.md`
- Keep/Drop pipeline: `../docs/assort_kd_flow/PIPELINE.md`

Verified certificates: **HackerRank Problem Solving** and **LangChain Academy**.\n