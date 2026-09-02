# AssortSmart-tab resume source (Google Doc)

Canonical experience/summary/skills from the AssortSmart tab. Stack wording on FRM/Masters differs per track (Spring Boot vs FastAPI); IA bullets are identical (Go/Python).

## Summary

Senior Software Engineer with 5 years of experience architecting high-throughput, cloud-native distributed systems and leading zero-downtime monolithic migrations.

Expert in {Java and Python | Python and Go | Java, Python and Go} microservices, specializing in scaling event-driven pipelines, optimizing multi-billion row databases, and driving extreme latency reductions for enterprise platforms.

Proven track record of bridging enterprise data with fault-tolerant AI by deploying LangGraph multi-agent systems, Milvus RAG architectures, and deterministic evaluation harnesses to deliver measurable business impact.

## Skills (AssortSmart tab)

Languages · Backend & APIs · AI & Applied ML · Data & Streaming · Databases & Storage · Cloud & DevOps · Architecture & Core Concepts

Tab list (Python/Go). Java and hybrid tracks add Java + Spring Boot/MVC/Security/Data JPA/Hibernate/Spring Batch + Maven; keep every tab skill including Go, FastAPI, Gin, Pydantic, Celery, asyncio, DynamoDB.

- Languages: Python, Go (Golang), SQL, C, C++
- Backend & APIs: FastAPI, Gin, Django, REST, gRPC, Pydantic, Celery, asyncio
- AI & Applied ML: LangGraph, LangChain, RAG, Milvus, pgvector, LLM Agents (OpenAI/Gemini/Claude), LangSmith, Offline Evaluation
- Data & Streaming: Apache Kafka, Apache Flink, ClickHouse, BigQuery, ETL Pipelines
- Databases & Storage: PostgreSQL, MySQL, Redis, MongoDB, Elasticsearch, DynamoDB, S3
- Cloud & DevOps: GCP, AWS, Docker, Kubernetes, Bazel, CI/CD, Datadog, ELK, New Relic
- Architecture & Core Concepts: Distributed Systems, Microservices, System Design (HLD/LLD), Database Sharding, Concurrency, Idempotency

## Impact Analytics / AssortSmart — Platform Engineering & Infrastructure

- Architected a multi-tenant Go/Gin platform scaling to 10k peak RPS, utilizing Google Wire for compile-time DI. Deployed as a self-protecting HTTP edge without a reverse proxy, guaranteeing high availability through native h2c, nested timeouts, and Datadog distributed tracing.
- Accelerated retail analytics performance by 15.5x, slashing pivot query latency from 189s to 12s on 250M-row operations. Migrated the data layer to ClickHouse, scaling the catalog to process 1.6M article-season combinations and 2.4B weekly rollup rows.
- Eliminated deployment bottlenecks by architecting a dynamic KPI configurator and custom formula parser. Engineered a real-time compilation layer that tokenizes operator-authored math into safe, ifNotFinite-wrapped ClickHouse SQL fragments, decoupling business logic from code releases.
- Guaranteed strict multi-tenant data boundaries and UAM-scoped hierarchy access across the platform. Secured system entry by implementing a Redis-fronted Firebase Admin to JWT/Google OIDC verification waterfall, constant-time API keys, and Postgres-backed role resolution.
- Enforced zero-regression engineering practices by designing a 100.0% statement-coverage CI gate (race and atomic) across 1,200+ Go tests. Hardened the Bitbucket deployment pipeline with automated golangci-linting, pre-push hooks, and continuous SAST/SBOM security scanning.

## Impact Analytics / AssortSmart — Agentic Flows & Orchestration

- Architected a multi-pipeline AI merchandise decision engine (Keep/Drop, Missed Opportunities, Top Style) evaluating 335K+ products across multiple seasons. Optimized inference at scale—processing 88k items per pass for under $100 token spend—by blending deterministic KPI math with structured LLM invokes across 7 AI lenses.
- Guaranteed zero-data-corruption across a 2.11B-row ClickHouse fact table by physically air-gapping batch LLM execution from database queries. Ensured fault tolerance using ClickHouse ReplacingMergeTree for two-phase inserts, feeding models via JSON payloads and falling back to deterministic scores upon LLM failure.
- Engineered a resilient AI orchestration registry to safely manage high-throughput LLM workloads across millions of tokens. Guaranteed stable parallel batch processing via custom circuit breakers and durable checkpoints, embedding LangSmith and custom per-run JSON telemetry to track exact token costs, step durations, and batch fallbacks.
- Shipped “Ask Iris,” a WebSocket AI copilot enabling planners to interactively query multi-billion-row KPIs, generate dynamic charts, and drill down into AI decisions. Architected the underlying LangGraph orchestration—featuring a Supervisor router and Evaluator loop—enforcing socket-level frozen scopes to guarantee data isolation and prevent infinite LLM loops.
- Established rigorous AI deployment guardrails by building a 300-case offline evaluation harness and a ≥80% accuracy CI promotion gate. Prevented degraded rollouts by benching candidate agent configurations against a 74% deterministic baseline, ensuring provable business value before production release.

## Uber FRM

- 70% recon cut, 14 days to 3 days, $340M materiality, 19M raw GL rows, 36 endpoints, L1–L4 FSLI, quarter-annualization
- 8-table MySQL SOADB, polymorphic review-status, optimistic row-locking, SHA-256 natural keys
- Led 3 engineers; ORM migration 100% statement coverage; Bazel PRs; SQL allowlists; FSM 50% delta-variance; SOX
- PyGo: FastAPI + SQLAlchemy 2.0. Java/hybrid: Spring Boot + JPA/Hibernate

## Uber Eats Menu

- 24 hours to 2 hours, $600K/yr, 30K+ menus/month, 98% field fidelity, Gemini 2.5 Pro + LangChain RAG + Milvus
- 95%+ success, Selenium proxies, Kafka, Flink keyed dedupe, exactly-once upserts

## Uber Mobility ANZ

- 99.9% compliance, 20 hours/week saved

## Masters India

- p95 1.2s to 300ms (75%), 1,500+ clients, 700 to 4,000 rpm, mentored 2
- Kafka + PostgreSQL tax-quarter shard, 1M+/day, 100K+ imports, idempotency, DLQ
- ELK + New Relic, Redis −30% reads, coverage 35% to 82%, 98% deploy success
- PyGo: FastAPI. Java/hybrid: Spring Boot

## GeeksforGeeks

- Django, 10K+ daily queries, 10x contest spikes, 20% premium lift, 30% course sales, 70% ops efficiency
