# Skills on the resume: fundamentals, where I used each, and how strongly to claim it

<div class="callout note">

**How to use this page**

- **What it covers:** every item on the Skills section of `Tarun_Mittal_SSE_5yr.pdf` (the PyGo track), plus the extra technologies that appear on project Tech lines. For each item: what it is in one line, the fundamentals an interviewer will probe, where it appears on my resume, and how strongly I can claim it.
- **When to read it:** when a job description names a technology and you want to know in 30 seconds what to say, or when an interviewer points at your skills list and says "tell me about X".
- **What to memorise:** the **claim strength** column. "Production" means I can tell a project story. "Skills-level" means I can explain it well but there is no resume bullet. "Literacy" means I know the concepts and must say so plainly. If you cannot place a skill, do not emphasise it.

</div>

**Labels used on this page.** MEASURED means we have a log, doc or code for it. STATED means printed on the resume from the project source. ESTIMATED means arithmetic I can show. HISTORICAL means from my past work records. TARGET means a design goal.

**Claim strength key**

| Strength | Meaning | How to talk about it |
|---|---|---|
| **Production** | I used it in shipped work that is on the resume | Tell the project story with numbers |
| **Production (historical)** | Used in past roles, from work records | State the outcome plainly. Some baselines are estimates |
| **Skills-level** | I can explain and design with it. It is not a resume bullet | "I know it well and have designed with it, but it's not one of my shipped bullets" |
| **Literacy** | I know the concepts | "I understand how it works. I haven't owned it in production" |

<div class="callout warn">

**Placement rules that interviewers check**

- **Kafka:** Uber Menu and Masters India (two different products). **Flink:** Uber Menu only. **Neither at Impact Analytics.**
- **ClickHouse, Go/Gin, LangGraph, LangSmith, Datadog:** Impact Analytics. LangSmith is Ask Iris only.
- **RAG, Milvus, LangChain, Selenium, Gemini 2.5 Pro:** Uber Menu.
- **ELK, New Relic, Celery:** Masters India.
- **MCP, tool calling:** skills-level. IA tool design (Cluster Recommendation Copilot, 14 tools) is verbal only.
- **C, C++, pgvector, DynamoDB, Kubernetes, gRPC:** literacy. No production ownership claims.

</div>

---

## 1. Languages

| Skill | What it is | Fundamentals to know | Where on the resume | Strength |
|---|---|---|---|---|
| **Python** | General-purpose language, the main one in my career | GIL and I/O versus CPU work, asyncio event loop, typing with Pydantic, packaging | IA agent plane (Keep/Drop, Ask Iris). Uber FRM (FastAPI). Uber Menu (Selenium, RAG). Masters India (FastAPI, Celery). GeeksforGeeks (Django) | Production |
| **Go** | Compiled language with cheap concurrency | Goroutines, channels, `context` deadlines, interfaces, error values, GC | IA: Gin platform (10k peak RPS), KPI parser, auth waterfall, native-TLS ClickHouse copier | Production |
| **SQL** | Query language for relational and analytical databases | Joins, indexes, `EXPLAIN`, transactions and isolation, window functions, GROUP BY | Everywhere: MySQL (FRM, GFG), PostgreSQL (Masters, IA), ClickHouse (IA) | Production |
| **C, C++** | Systems languages | Memory and pointers, stack versus heap, compilation, STL basics | On the skills line for fundamentals | Literacy. No production ownership claim |

Deep pages: [python_fastapi.md](python_fastapi.md), [go_gin.md](go_gin.md).

---

## 2. Backend and APIs

| Skill | What it is | Fundamentals to know | Where | Strength |
|---|---|---|---|---|
| **FastAPI** | Async Python web framework on Starlette and Pydantic | ASGI, `Depends` injection, `async def` versus `def`, OpenAPI, WebSockets | Uber FRM (36 endpoints). Masters India (strangler migration, p95 from 1.2s to 300ms). IA Ask Iris WebSocket | Production |
| **Gin** | Lightweight Go HTTP framework | Router, middleware chain, binding and validation, recovery | IA platform (C1) | Production |
| **Django** | Batteries-included Python web framework | ORM, migrations, admin, auth, DRF | GeeksforGeeks doubt platform (10K+ daily queries, 10x contest spikes) | Production (historical) |
| **REST** | Resource-oriented HTTP APIs | Verbs and status codes, idempotent methods, pagination, versioning, 202 with polling | Every project | Production |
| **gRPC** | RPC framework over HTTP/2 with Protocol Buffers | Protobuf schemas and codegen, unary versus streaming calls, deadlines | Not used in a resume bullet. REST was primary | Literacy |
| **Pydantic** | Data validation from Python type hints | Models, validators, JSON schema, strict types | FRM and Masters request and response models. IA structured LLM outputs | Production |
| **Celery** | Python distributed task queue | Broker, workers, retries with backoff, rate limits, chains | Masters India: validation chains, PDFs, webhooks | Production (historical) |
| **asyncio** | Python's cooperative concurrency | Event loop, `await`, `gather`, never block the loop, `to_thread` | Masters (async IRP calls). FRM (`asyncio.to_thread` around sync ORM). IA agent plane | Production |

Not on the PyGo skills line but on a Tech line: **SQLAlchemy 2.0** (Uber FRM; typed `Mapped` models, `select()` with `aliased()` and `.label()`), **Google Wire** and **h2c** (IA C1 bullet). See [postgres_mysql_redis.md](postgres_mysql_redis.md) and [go_gin.md](go_gin.md).

---

## 3. Generative AI

| Skill | What it is | Fundamentals to know | Where | Strength |
|---|---|---|---|---|
| **LangGraph** | Library for LLM apps as stateful graphs | Nodes, edges, conditional edges, shared state, checkpointing, recursion limit | IA Ask Iris: supervisor plus 3-attempt evaluator (A4) | Production |
| **LangChain** | Building blocks for LLM apps | Loaders, splitters, embeddings, retrievers, prompt templates | Uber Menu RAG pipeline (M1) | Production (historical) |
| **RAG** | Retrieve relevant context, then generate | Chunking, embeddings, ANN retrieval, prompt assembly, schema validation, offline eval | Uber Menu: 98% field fidelity (offline) with Gemini 2.5 Pro over Milvus | Production (historical) |
| **Milvus** | Vector database | ANN indexes (HNSW, IVF), collections, similarity metrics | Uber Menu only | Production (historical) |
| **pgvector** | Postgres extension for vector search | Vector column, HNSW and IVFFlat indexes, joins with relational data | None | Literacy |
| **LLM agents (OpenAI, Gemini, Claude)** | Programs that use LLMs to decide steps | Structured outputs, loops and caps, cost and latency, non-determinism, provider selection | IA Keep/Drop lenses (OpenAI models, names off PDF) and Ask Iris. Uber Menu Gemini 2.5 Pro. Claude has no named project | Production (Claude: skills-level) |
| **Tool calling** | Model requests a function call, code runs it | JSON schemas for tools, argument validation, read-only defaults, scope from session | Skills line. IA scoring deliberately has no tools. Copilot design is verbal | Skills-level |
| **MCP** | Open protocol connecting LLM apps to tools and data | Host, client, server. Tools, resources, prompts. JSON-RPC over stdio or HTTP | Skills line only | Skills-level |
| **Prompt engineering** | Designing instructions, context and output format | Narrow prompts, schemas, data separated from instructions, versioning | IA lens prompts (inside `config_hash`). Menu extraction prompts | Production |
| **LangSmith** | Tracing and eval platform for LLM apps | Trace trees, token and latency per step, datasets | IA Ask Iris only | Production |
| **Offline evaluation** | Testing models on labelled sets before shipping | Proxy versus gold sets, promotion gates, baselines, leakage | IA: 300-case set with 80% CI gate. Gold-200: 73% cheaper at 100% coverage, 74% deterministic baseline. Menu: 98% offline | Production |

Deep page: [langgraph_mcp_rag.md](langgraph_mcp_rag.md). Generative AI defense table: [../../../prep/36_skills_ai_agents_defense.md](../../../prep/36_skills_ai_agents_defense.md).

**Watch out:** 80% is a promotion gate, not live accuracy. 73% and 74% come from gold-200, not the 300-case file. Keep/Drop has a fixed step order with no LLM orchestrator.

---

## 4. Data and Streaming

| Skill | What it is | Fundamentals to know | Where | Strength |
|---|---|---|---|---|
| **Apache Kafka** | Partitioned, replayable event log | Topics, partitions, keys and ordering, consumer groups, offsets, at-least-once, DLQ, lag | Uber Menu (keyed by vendor, feeds Flink). Masters India (keyed by GSTIN, idempotent workers, 1M+ a day) | Production (historical) |
| **Apache Flink** | Stateful stream processor | keyBy and keyed state, event time and watermarks, checkpoints, backpressure, exactly-once state | Uber Menu only: keyed dedupe, normalization, routing | Production (historical) |
| **ClickHouse** | Columnar OLAP database | MergeTree parts and merges, sparse index, partitions, ReplacingMergeTree, memory and spill settings | IA: six rollup tables (15.5x, from 189s to 12s), 170GB OOM fix, copier at about 344k rows per second, 2.11B master | Production |
| **BigQuery** | Google's serverless data warehouse | Columnar storage, pricing by bytes scanned, partitioned and clustered tables | IA tech line. Keep qualitative | Production (light). Keep claims qualitative |
| **ETL pipelines** | Extract, transform, load | Idempotent loads, checkpoints, backfills, validation, chunking | FRM Sheets-to-MySQL (19M raw GL rows). IA rollup builds. Menu ingestion. Masters bulk imports | Production |

Deep pages: [kafka_streaming.md](kafka_streaming.md), [flink.md](flink.md), [kafka_flink_scale_defense.md](kafka_flink_scale_defense.md), [clickhouse.md](clickhouse.md).

The HFM (Oracle Hyperion) ETL at FRM was a shared pipeline responsibility. I owned the scoping backend and the Sheets-to-MySQL migration.

---

## 5. Databases and Storage

| Skill | What it is | Fundamentals to know | Where | Strength |
|---|---|---|---|---|
| **PostgreSQL** | Open-source relational database | MVCC, indexes, isolation levels, partitioning, pooling | Masters India (sharded by tax quarter). IA (thin metadata, UAM, roles) | Production |
| **MySQL** | Open-source relational database | InnoDB row locks, transactions, optimistic locking, indexes | Uber FRM (8-table schema on SOADB). GeeksforGeeks | Production |
| **Redis** | In-memory key-value store | Data types, TTL, cache-aside, invalidation, stampede guards, `SET NX` locks | Masters (read load down 30%). IA (auth waterfall front cache). GFG (counters) | Production |
| **MongoDB** | Document database | Flexible schemas, indexes, document modelling | Masters (invoice payload snapshots). GFG (doubt bodies) | Production (historical) |
| **Elasticsearch** | Search engine on inverted indexes | Analyzers, inverted index, relevance, as ELK log storage | Masters (invoice search, ELK). GFG (doubt search) | Production (historical) |
| **DynamoDB** | AWS managed key-value and document database | Partition and sort keys, capacity modes, single-table design | None | Literacy |
| **S3** | AWS object storage | Buckets, keys, durability, lifecycle rules | Masters: bulk import files landed in object storage | Light production use. Do not claim deep ownership |

Deep page: [postgres_mysql_redis.md](postgres_mysql_redis.md). MongoDB and Elasticsearch depth: [../../../prep/02_mongodb_elasticsearch.md](../../../prep/02_mongodb_elasticsearch.md).

---

## 6. Cloud and DevOps

| Skill | What it is | Fundamentals to know | Where | Strength |
|---|---|---|---|---|
| **GCP** | Google Cloud | Compute, storage, BigQuery, IAM basics | IA, Uber Menu | Production (keep product names qualitative unless sure) |
| **AWS** | Amazon Web Services | S3, KMS, compute, IAM basics | Masters India | Production (historical) |
| **Docker** | Container images and runtime | Layers and caching, small pinned images, one process per container | IA, FRM, Menu, Masters tech lines | Production |
| **Kubernetes** | Container orchestration | Pods, deployments, services, HPA, probes, graceful SIGTERM | None | Literacy. No cluster operations claim |
| **Bazel** | Hermetic, incremental monorepo build system | BUILD files, test targets, caching, stacked PRs | Uber FRM | Production |
| **CI/CD** | Automated checks and releases | Test gates, coverage gates, canaries, rollbacks | Masters (coverage from 35% to 82%, 98% deploy success). FRM (Bazel gates, 100% module coverage). IA (80% eval promotion gate) | Production |
| **Datadog** | Hosted metrics, logs and APM | Traces and spans, service maps, monitors | IA Go edge distributed tracing (C1) | Production |
| **ELK** | Elasticsearch, Logstash, Kibana | Structured logs, correlation ids, dashboards | Masters India (triage down 70%) | Production (historical) |
| **New Relic** | Hosted APM | Distributed tracing, error rates, alerting | Masters India | Production (historical) |

Deep page: [observability_cloud.md](observability_cloud.md).

---

## 7. Architecture and Core Concepts

| Skill | What it means | Fundamentals to know | My best example | Strength |
|---|---|---|---|---|
| **Distributed systems** | Many services and machines cooperating over a network | Partial failure, retries, timeouts, consistency models, idempotency | Masters bulk pipeline. Menu Kafka and Flink. IA copier | Production |
| **Microservices** | Small services owning one domain each | Service boundaries, strangler migration, shared database during cutover | Masters PHP monolith to FastAPI microservices | Production (historical) |
| **System design (HLD and LLD)** | High-level architecture and low-level class and schema design | Requirements, capacity math, data model, failure modes, trade-offs | Any project whiteboard. FRM schema (LLD). Menu pipeline (HLD) | Production |
| **Data structures and algorithms** | Problem solving fundamentals | Complexity, hashing, trees, graphs, DP | Google Code Jam Qualifier 2021, rank 2260 out of 37,000+. HackerRank Problem Solving certificate | HISTORICAL achievements |
| **Caching** | Keeping hot data close and cheap to read | Cache-aside, TTL, invalidation, stampede, precomputation | Masters Redis (read load down 30%). IA ClickHouse rollups as precomputation. IA auth cache | Production |
| **Reliability** | Keeping systems working under failure | Timeouts, circuit breakers, checkpoints, DLQs, bounded retries, canaries, graceful fallback | IA registry (timeouts, breakers, checkpoints, deterministic fallback). Masters DLQ and retries. Go edge nested timeouts | Production |
| **Multithreading** | Running work in parallel threads | Races, locks, thread pools, the GIL | Go copier double buffering. FastAPI thread pool for sync handlers | Production |
| **Database sharding** | Splitting data across tables or servers by a key | Shard key choice, routing, hot shards, archiving | Masters PostgreSQL sharded by tax quarter. (ClickHouse partitions by season are partitioning, not sharding) | Production (historical) |
| **Concurrency** | Many tasks in progress at once | async versus threads versus goroutines, backpressure, bounded concurrency | Go goroutines, asyncio IRP calls, Celery workers, Flink parallelism | Production |
| **Idempotency** | Doing it twice has the same effect as once | Idempotency keys, upserts, unique constraints, version columns | Masters `client + fileHash + batchIndex`. Menu catalog upserts. FRM SHA-256 natural keys. IA ReplacingMergeTree versions. GFG unique (user, content) votes | Production |

---

## 8. Java tracks (for reference only)

This page is the PyGo track. The Java tracks (`final_java_pygo_ia`, `final_java_ai`) add Java, Spring Boot, Spring MVC, Spring Security, Spring Data JPA, Hibernate, Spring Batch and Maven, and say "Amazon S3". On those tracks, the Uber FRM and Masters India stacks are described in Spring terms. Impact Analytics platform APIs are **Go/Gin on every track**, never Spring Boot. JUnit is not on this track's PDF.

---

## 9. Anti-patterns: what not to claim

- No **Terraform** or **Kubernetes operator or cluster operations** ownership.
- No **Spark**, **Pinot**, **Vitess** or **Pinecone** on the resume. Spark is a verbal backfill option for Menu only.
- No **Kafka, Flink, CDC or Milvus at Impact Analytics.** The CDC pipeline there was written by a colleague, Ashvin Sharma.
- No **fine-tuning or SFT** claims.
- No **human review queues (HITL)** at Impact Analytics.
- **Ask Iris is shipped** (capability, no SLA). The **Cluster Recommendation Copilot is still being built** (say "building"). Its load test is pending, and its 14 tools and 3 confirm gates are verbal design depth. Older prep said "do not claim production agentic load-test PASS, AssortSmart is building". The accurate version is that Ask Iris shipped and the Copilot load test is pending.
- **Mentorship and SOA** are not skills-line items. Defend them from the bullets (mentored 2 at Masters, led 3 at FRM, and SOADB at FRM). **Design Patterns** was removed from Skills in August 2026 and is verbal only.
- Older versions of this map listed **Linux**, **PostHog** and "embeddings for IA async jobs". None of those are on the current resume. Older versions also said **Microservices, ELK and SQLAlchemy** were removed from Skills. Microservices and ELK are back on the skills line, and SQLAlchemy 2.0 is on the FRM tech line.

---

## 10. Rapid-fire drill

1. **Where is Flink?** Uber Menu only.
2. **Where is Kafka?** Uber Menu and Masters India. Two different products.
3. **Where is LangSmith?** Ask Iris at Impact Analytics.
4. **Where is Milvus?** Uber Menu only.
5. **Is MCP a production claim?** No. Skills-level.
6. **Where is Go?** Impact Analytics: the Gin platform, KPI parser, auth middleware and copier.
7. **What is your strongest database story?** FRM's 8-table MySQL schema and the column-aliasing bug, or IA's ClickHouse rollups and 170GB OOM fix.
8. **Have you run Kubernetes clusters?** No. Literacy only.
9. **gRPC?** Literacy. REST was primary.
10. **Where did you shard a database?** Masters India: PostgreSQL by tax quarter.

---

## Related

- [00_index.md](00_index.md)
- [../../../handbook/09_tech_glossary.md](../../../handbook/09_tech_glossary.md)
- [../../../prep/36_skills_ai_agents_defense.md](../../../prep/36_skills_ai_agents_defense.md)
