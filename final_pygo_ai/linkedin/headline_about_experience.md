# LinkedIn Profile Pack (stand out)

Aligned to **Final Python + Go + AI** resume (`Tarun_Mittal_SSE_5yr.pdf`). Paste-ready. Avoid colon-heavy AI voice in About.

## Headline (pick one)
1. Senior Software Engineer | Python · Go | High throughput backends and data platforms | Go · ClickHouse · Kafka · Agentic AI
2. Senior Software Engineer | Go · ClickHouse · Kafka · LangGraph | 4B-row weekly rollups · 10k RPS
3. Backend SSE (Python and Go) | Uber (via EPAM) FRM · Kafka 1M+/day · Go/Gin 10k RPS · LangGraph

**Recommended:** #1 for Staff / data platform search. Use #2 if the recruiter is hunting scale numbers. Do not write “scaled to 4B+ rows” as if every table is 4B. The 4.09B figure is attr weekly, two seasons.

## About — short
Senior Software Engineer with 5 years of experience designing and owning cloud-native, high-throughput distributed systems. Expertise in Python and Go microservices, with applied experience in AI-assisted and RAG systems. Proven track record shipping production systems, leading backend migrations, and improving reliability, performance, and scalability.

## About — long
I am a Senior Software Engineer focused on backend, data, and production AI platforms in Python and Go.

What I am known for:
- Platform: at Impact Analytics I architected AssortSmart's multi-tenant Go/Gin edge (Wire, h2c, Datadog) to 10k peak RPS, cut planner pivots from 189s to 12s on 250M rows, and serve six ClickHouse rollup tables (product, store, and attr at season and weekly grains). I keep a 100% statement-coverage CI gate across 1,200+ Go tests.
- Scale and infrastructure: weekly grain is built one fiscal week at a time after a full-season weekly aggregate sat around 170 GB and OOM'd. I wrote a Go native TLS pump to copy season partitions between ClickHouse Cloud clusters, about 150 to 190k rows/s per stream and about 344k combined, using 500k row columnar batches and double buffering so SELECT of the next batch overlaps INSERT of the last. Largest object I timed is attr weekly at 4.09B rows across two seasons. That copy was measured in flight, not a finished 4.09B cutover. Kafka and Flink on my profile are Uber Menu, not AssortSmart.
- Agentic: Keep/Drop + Missed Opportunities + Top Style over 348k article-seasons (88k items/pass, 7 lenses), JSON payloads vs a 2.11B-row ClickHouse master, and shipped Ask Iris, a JWT-secured WebSocket LangGraph supervisor with a 3-attempt evaluator and handshake-frozen hierarchy. Promotions gated on a 300-case proxy harness and an 80% CI gate; we cut live scoring cost 73% at 100% coverage vs a 74% deterministic baseline and froze blend weights when the LLM lost (gate, not all-tenants-live).
- Uber via EPAM: FRM scoping (36 FastAPI endpoints, 19M GL rows, L1–L4 FSLI, 8-table SOADB, SHA-256 keys, led 3, 100% coverage, SOX 50% delta-variance) cutting recon 70% from 14 days to 3 against $340M materiality. Menu ingestion 24 hours to 2 hours, $600K/yr, 30K+ menus/month, 98% offline RAG/Milvus, Kafka+Flink exactly-once.
- Masters India: FastAPI strangler, p95 1.2s to 300ms (75%), Kafka + PostgreSQL tax-quarter shard at 1M+/day, coverage 35% to 82% at 98% deploy. Mentored 2.

I care about honest metrics (measured vs promotion-gate vs historical) and mentoring people to ship safely.

Open to Senior Software Engineer / SDE2+ backend, platform, data infrastructure, and applied-AI systems roles.

## Experience blurbs

### Impact Analytics — Senior Software Engineer (May 2026 – Present)
**AssortSmart — Platform & AI.** Two PDF chapters (Agentic first):

**Agentic Flows & Orchestration.** Keep/Drop + Missed Opportunities + Top Style, 348k article-seasons, 88k items/pass, 7 lenses. JSON payloads vs a 2.11B-row ClickHouse master; ReplacingMergeTree timeout fallback. Shared orchestration registry, circuit breakers, checkpoints that skip redundant det, config_hash, JSON telemetry. Shipped Ask Iris (JWT WebSocket, LangGraph supervisor, 3-attempt evaluator, handshake-frozen hierarchy, LangSmith). 300-case proxy eval, 80% CI gate, 73% cheaper at 100% coverage vs 74% det, frozen blend weights.

**Core Infrastructure & Pipeline.** Multi-tenant Go/Gin at 10k peak RPS (Wire, h2c, Datadog). KPI formula tokenizer with native division-by-zero protection. Firebase/JWT/OIDC + Redis + Postgres roles.

Reduced planner pivot latency by 15.5× (189s to 12s on 250M-row operations) by building a ClickHouse pre-aggregation layer for season and weekly rollups. Prevented 170GB OOM crashes by slicing batch inserts into temporal chunks and enforcing strict distributed memory and disk-spill caps.

Migrated ClickHouse rollups across Cloud clusters at ~344k rows/s by writing a custom Go native-TLS data pump to bypass strict cross-cluster IP allowlist restrictions. Processed partitions up to 4.09B rows using 500k-row double-buffered batches, and eliminated partial-commit ghost rows using TSV ledgers and atomic partition rollbacks.

Catalog still includes 1.6M article-seasons. $100/pass and 100% coverage / 1,200+ Go tests / golangci-lint / SAST/SBOM stay LinkedIn / verbal.

Stack on this PDF: Go, Gin, Python, FastAPI, LangGraph, ClickHouse, BigQuery, Redis, PostgreSQL, Datadog, LangSmith, GCP, Docker.

**Verbal only / not on PDF (building):** Cluster Recommendation Copilot and Hindsight remain deep-dive context if asked — not resume headline bullets.

### Uber via EPAM — SDE2 (Jul 2024 – May 2026)
**FRM:** Owned FRM scoping backend (Spring Boot / Spring Data JPA / Hibernate) — 36 FastAPI endpoints, 19M raw GL rows, L1–L4 FSLI, 8-table MySQL SOADB, SHA-256 natural keys, optimistic locking. 70% recon cut from 14 days to 3 against $340M. Led 3 on the Spring Data JPA / Hibernate migration to 100% statement coverage; Bazel PRs; SQL allowlists; FSM 50% delta-variance for SOX.

**Menu (Uber Eats):** 24 hours to 2 hours, $600K/yr, 30K+ menus/month. Gemini 2.5 Pro + LangChain RAG + Milvus at 98% field fidelity (offline eval). 95%+ scrape success. Kafka + Flink keyed dedupe, exactly-once catalog upserts.

**ANZ (Uber Mobility):** 99.9% document compliance, ~20h/week saved (HISTORICAL Mobility — not Eats).

### Masters India — SDE2 (Dec 2022 – Jun 2024)
Cut p95 from 1.2s to 300ms (75%) for 1,500+ clients by migrating a PHP monolith to FastAPI microservices; mentored 2. 700 to 4,000 rpm and 1M+ IRP/day on a high-concurrency Kafka + PostgreSQL quarter-shard pipeline. Idempotent processing, DLQ/fault-tolerant state, Redis −30% reads. Coverage 35% to 82% at 98% deploy.

### GeeksforGeeks — SDE (Aug 2021 – Nov 2022)
Django doubt-support for 10K+ daily queries and 10× contest spikes. Voting/pinning/locking APIs lifted premium 20%. Influencer dashboard raised course sales 30%. Scheduled jobs raised ops efficiency 70%.

## Featured section
- Resume PDF (Java FRM + Py/Go IA)
- LangChain Academy cert
- HackerRank Problem Solving cert
- Optional: GitHub TM-DEV-PRO

## Skills order (LinkedIn)
Java · Spring Boot · Hibernate · Python · Go · Gin · FastAPI · Distributed Systems · Microservices · Kafka · ClickHouse · System Design · Docker · AWS · GCP · PostgreSQL · MySQL · Redis · LangGraph · RAG · Mentorship\n