# AssortSmart-tab resume source (Google Doc)

Canonical experience/summary/skills from the AssortSmart tab. Stack wording on FRM/Masters differs per track (Spring Boot vs FastAPI); IA bullets are identical (Go/Python).

## Summary

Current PDF (Sep 2026):

Senior Software Engineer with 5 years of experience designing and owning cloud-native, high-throughput distributed systems.

Expertise in {Java and Python | Python and Go | Java, Python and Go} microservices, with applied experience in AI-assisted and RAG systems.

Proven track record shipping production systems, leading backend migrations, and improving reliability, performance, and scalability.

## Skills (AssortSmart tab)

Languages · Backend & APIs · Generative AI · Data & Streaming · Databases & Storage · Cloud & DevOps · Architecture & Core Concepts

Tab list (Python/Go). Java and hybrid tracks add Java + Spring Boot/MVC/Security/Data JPA/Hibernate/Spring Batch + Maven; keep every tab skill including Go, FastAPI, Gin, Pydantic, Celery, asyncio, DynamoDB.

- Languages: Python, Go (Golang), SQL, C, C++
- Backend & APIs: FastAPI, Gin, Django, REST, gRPC, Pydantic, Celery, asyncio
- Generative AI: LangGraph, LangChain, RAG, Milvus, pgvector, LLM Agents (OpenAI/Gemini/Claude), LangSmith, Offline Evaluation
- Data & Streaming: Apache Kafka, Apache Flink, ClickHouse, BigQuery, ETL Pipelines
- Databases & Storage: PostgreSQL, MySQL, Redis, MongoDB, Elasticsearch, DynamoDB, S3
- Cloud & DevOps: GCP, AWS, Docker, Kubernetes, Bazel, CI/CD, Datadog, ELK, New Relic
- Architecture & Core Concepts: Distributed Systems, Microservices, System Design (HLD/LLD), Database Sharding, Concurrency, Idempotency

## Impact Analytics / AssortSmart — Agentic Flows & Orchestration

PDF order: **Agentic first**, then Core Infrastructure. Exact PDF lines:

- Architected a multi-pipeline AI merchandise decision engine (Keep/Drop, Missed Opportunities, Top Style) evaluating 348k article-seasons. Optimized inference at scale—processing 88k items per pass—by blending deterministic KPI math with structured LLM invokes across 7 AI lenses.
- Decoupled AI inference from a 2.11B-row ClickHouse master by asynchronously serving context via JSON payloads rather than direct database querying. Engineered an eventually consistent write pattern via ReplacingMergeTree that guaranteed system availability by gracefully falling back to deterministic baselines during LLM timeouts.
- Engineered a shared orchestration registry to guarantee 88k-article batch runs survive provider failures by implementing hard timeouts, circuit breakers, and durable checkpoints that bypass redundant deterministic scoring. Ensured full observability by stamping every output row with a frozen config hash and custom JSON telemetry tracking tokens, USD cost, step duration, and batch fallbacks.
- Shipped “Ask Iris,” a JWT-secured WebSocket copilot enabling planners to interactively query KPIs and inspect AI decisions on a multi-billion-row database. Prevented infinite LLM loops and multi-tenant data leaks by orchestrating a LangGraph supervisor with a 3-attempt evaluator loop, utilizing LangSmith for observability, and strictly freezing hierarchy access on the initial socket handshake.
- Built a 300-case proxy evaluation harness and an 80% accuracy CI gate to enforce strict deployment guardrails. Reduced live execution costs by 73% at 100% coverage by benchmarking models against a 74% deterministic baseline, strategically freezing final decision weights when the LLM underperformed the baseline.

## Impact Analytics / AssortSmart — Core Infrastructure & Pipeline

- Architected a multi-tenant Go/Gin platform scaling to 10k peak RPS, utilizing Google Wire for compile-time DI. Deployed as a self-protecting HTTP edge without a reverse proxy, guaranteeing high availability through native h2c, nested timeouts, and Datadog distributed tracing.
- Eliminated deployment bottlenecks by architecting a dynamic KPI configurator and custom formula parser. Engineered a real-time compilation layer that tokenizes operator-authored math into parameterized ClickHouse SQL fragments with native division-by-zero protection, decoupling business logic from code releases.
- Guaranteed strict multi-tenant data isolation and UAM-scoped hierarchy access control across PostgreSQL and ClickHouse. Redis-fronted Firebase Admin to JWT/Google OIDC waterfall, constant-time API keys, Postgres-backed role resolution.
- Reduced planner pivot latency by 15.5× (189s to 12s on 250M-row operations) by building a ClickHouse pre-aggregation layer for season and weekly rollups. Prevented 170GB OOM crashes by slicing batch inserts into temporal chunks and enforcing strict distributed memory and disk-spill caps.
- Migrated ClickHouse rollups across Cloud clusters at ~344k rows/s by writing a custom Go native-TLS data pump to bypass strict cross-cluster IP allowlist restrictions. Processed partitions up to 4.09B rows using 500k-row double-buffered batches, and eliminated partial-commit ghost rows using TSV ledgers and atomic partition rollbacks.

**Tech (PDF):** Go, Gin, Python, FastAPI, LangGraph, ClickHouse, BigQuery, Redis, PostgreSQL, Datadog, LangSmith, GCP, Docker.

## Interview honesty (off PDF, still true)

- **1.6M article-seasons** = product × season catalog. PDF now uses **348k article-seasons** for scored Keep/Drop volume. Do not mix them.
- **$100 / pass** token spend is still true, **off PDF**.
- Weekly INSERT settings **55 GB cap / 16 GB spill / one fiscal week** remain the verbal OOM story. PDF says “temporal chunks” and “memory and disk-spill caps.”
- **100.0%** statement-coverage CI (race and atomic) across **1,200+** Go tests, golangci-lint, SAST/SBOM = LinkedIn / verbal.
- Six tables remain product/store/attr × season and weekly.
- TSV ledger on the PDF is the weekly *loader* skip file. Copier ledger is `migrate-checkpoints/<table>.done`.
- **Atomic partition rollbacks** = `DROP PARTITION` then recopy that season. Not an atomic swap with live readers.
- **4.09B** is attr weekly two seasons; copy in flight at snapshot. Do not say the cutover finished.
- **73% cost / 100% coverage** = gold-200 model bench (`gpt-5.6-luna` vs `gpt-5.4-mini`, 200/200 complete). **300-case / 80%** = proxy gold CI gate (`eval.json`). Do not fuse them into one measured run.
- **80%** is a **CI promotion gate**, not all tenants live.
- JSON payloads + no DB tool on the scoring path is the isolation invariant. “Async” is how batches run; the LLM does not issue ClickHouse SQL.
- Ask Iris = **shipped capability**. No invented tenant-wide SLAs.
- Cluster Recommendation Copilot / Hindsight = **verbal only**.
- Do **not** put Kafka, Flink, CDC, K8s-ops, Milvus, or sub-second ClickHouse on IA.

## Uber FRM

- 70% recon cut, 14 days to 3 days, $340M materiality, 19M raw GL rows, 36 endpoints, L1–L4 FSLI, quarter-annualization
- 8-table MySQL SOADB, polymorphic review-status, optimistic row-locking, SHA-256 natural keys
- Led 3 engineers; ORM migration 100% statement coverage; Bazel PRs; SQL allowlists; FSM 50% delta-variance; SOX
- PyGo: FastAPI + SQLAlchemy 2.0. Java/hybrid: Spring Boot + JPA/Hibernate

## Uber Eats Menu

- 24 hours to 2 hours, $600K/yr, 30K+ menus/month, 98% field fidelity, Gemini 2.5 Pro + LangChain RAG + Milvus
- 95%+ success, Selenium proxies, Kafka + Flink **large-scale data ingestion and processing pipeline**, keyed dedupe, exactly-once catalog upserts

## Uber Mobility ANZ

- 99.9% compliance, 20 hours/week saved

## Masters India

- p95 1.2s to 300ms (75%), 1,500+ clients, 700 to 4,000 rpm, mentored 2
- Kafka + PostgreSQL tax-quarter shard, **high-concurrency** 1M+/day, 100K+ **idempotent** imports, DLQ / fault-tolerant state, bounded retries
- ELK + New Relic, Redis −30% reads, coverage 35% to 82%, 98% deploy success
- PyGo: FastAPI. Java/hybrid: Spring Boot

## GeeksforGeeks

- Django, 10K+ daily queries, 10x contest spikes, 20% premium lift, 30% course sales, 70% ops efficiency
