# Skills on the resume: fundamentals, where I used each, and how strongly to claim it

<div class="callout note">

**How to use this page**

- **What it covers:** every item on the Skills section of `Tarun_Mittal_SSE_5yr_Java_AI.pdf` (summary line: "Expertise in Java and Python microservices"), plus the extra technologies that appear on project Tech lines. For each item: what it is in one line, the fundamentals an interviewer will probe, where it appears on my resume, and how strongly I can claim it.
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

- **Java and Spring Boot:** Uber FRM (36 Spring Boot endpoints, Spring Data JPA / Hibernate migration, JUnit) and Masters India (PHP monolith to Spring Boot microservices, Hibernate). **Never Spring Boot at Impact Analytics.**
- **Go/Gin:** Impact Analytics platform. **Python with FastAPI and LangGraph:** the IA agent plane (Ask Iris, Keep/Drop batch). **Python:** Uber Menu. **Django:** GeeksforGeeks.
- **Kafka:** Uber Menu and Masters India (two different products). **Flink:** Uber Menu only. **Neither at Impact Analytics.**
- **ClickHouse, LangGraph, LangSmith, Datadog:** Impact Analytics. LangSmith is Ask Iris only.
- **RAG, Milvus, LangChain, Selenium, Gemini 2.5 Pro:** Uber Menu.
- **ELK, New Relic:** Masters India.
- **Spring MVC, Spring Security, Spring Batch, Maven, Amazon S3, Celery, asyncio:** skills-line items with no bullet naming them. Explain where they fit, don't attach outcomes.
- **MCP, tool calling:** skills-level. IA tool design (Cluster Recommendation Copilot, 14 tools) is verbal only.
- **C, C++, pgvector, DynamoDB, Kubernetes, gRPC:** literacy. No production ownership claims.

</div>

---

## 1. Languages

| Skill | What it is | Fundamentals to know | Where on the resume | Strength |
|---|---|---|---|---|
| **Java** | Statically typed, compiled-to-bytecode language running on the JVM (Java Virtual Machine) | Classes and interfaces, generics, collections, exceptions (checked versus unchecked), threads and executors, garbage collection, records, streams | Uber FRM (Spring Boot, Spring Data JPA, Hibernate, JUnit). Masters India (Spring Boot, Hibernate, Kafka consumers) | Production |
| **Python** | General-purpose language, strongest for AI and data work | GIL and I/O versus CPU work, asyncio event loop, typing with Pydantic, packaging | IA agent plane (Keep/Drop batch, Ask Iris). Uber Menu (Selenium, RAG). GeeksforGeeks (Django) | Production |
| **Go** | Compiled language with cheap concurrency | Goroutines, channels, `context` deadlines, interfaces, error values, GC | IA: Gin platform (10k peak RPS), KPI parser, auth waterfall, native-TLS ClickHouse copier | Production |
| **SQL** | Query language for relational and analytical databases | Joins, indexes, `EXPLAIN`, transactions and isolation, window functions, GROUP BY | Everywhere: MySQL (FRM, GFG), PostgreSQL (Masters, IA), ClickHouse (IA) | Production |
| **C, C++** | Systems languages | Memory and pointers, stack versus heap, compilation, STL basics | On the skills line for fundamentals | Literacy. No production ownership claim |

Deep pages: [python_fastapi.md](python_fastapi.md), [go_gin.md](go_gin.md). Java and Spring entries: [../../../handbook/09_tech_glossary.md](../../../handbook/09_tech_glossary.md).

---

## 2. Backend and APIs

**Spring in one paragraph.** Spring is the standard Java framework for backend services. Its container creates your objects (**beans**) and hands each one its dependencies, which is **dependency injection**. **Spring Boot** adds defaults and an embedded web server so a service starts from one `main` method. The other Spring items below are modules that plug into a Spring Boot service.

| Skill | What it is | Fundamentals to know | Where | Strength |
|---|---|---|---|---|
| **Spring Boot** | Opinionated Spring setup with auto-configuration and an embedded server | Beans and constructor injection, auto-configuration, profiles and properties, Actuator health checks, `@RestControllerAdvice` error mapping | Uber FRM: 36 Spring Boot endpoints. Masters India: PHP monolith to Spring Boot microservices (p95 from 1.2s to 300ms, 700 to 4,000 requests per minute) | Production |
| **Spring MVC** | Spring's web layer: controllers, request mapping, message conversion | `@RestController`, `@GetMapping` / `@PatchMapping`, `@RequestBody` with `@Valid`, `@RequestHeader`, the servlet thread-per-request model, filters versus interceptors | The REST controllers in the FRM and Masters Spring Boot services are Spring MVC under the hood. No bullet names it | Skills-level (in practice under the Spring Boot bullets) |
| **Spring Security** | Spring's authentication and authorization framework, built as a chain of servlet filters | Filter chain, `SecurityContext`, JWT resource server, method security (`@PreAuthorize`), CSRF and CORS basics | Where it fits: the JWT and role checks in front of Masters' mutating APIs (JWT access plus refresh tokens, RBAC). FRM trusted Uber's gateway header instead. No bullet names it | Skills-level |
| **Spring Data JPA** | Repository abstraction over JPA: declare an interface, Spring writes the queries | Derived query methods, `@Query` JPQL, projections mapped by alias, paging, `@Modifying` bulk updates | Uber FRM: core Spring Data JPA / Hibernate migration, led 3 engineers, removed column-aliasing bugs, 100% module statement coverage | Production |
| **Hibernate** | The most used JPA implementation (ORM) | Entities and the persistence context, dirty checking, lazy versus eager loading and N+1, `@Version` optimistic locking, `@Transactional` boundaries | Uber FRM (8-table schema on SOADB, `@Version`, atomic cross-table syncs). Masters India tech line (PostgreSQL entities) | Production |
| **Spring Batch** | Framework for chunked, restartable batch jobs | Job, step, chunk (reader, processor, writer), job repository for restart, skip and retry policies | Where it fits: chunked bulk invoice imports at Masters, where progress must survive a restart. The bullet names Kafka and idempotency, not Spring Batch, so keep it at the pattern level | Skills-level |
| **FastAPI** | Async Python web framework on Starlette and Pydantic | ASGI, `Depends` injection, `async def` versus `def`, OpenAPI, WebSockets | IA agent plane: Ask Iris WebSocket (A4) | Production |
| **Gin** | Lightweight Go HTTP framework | Router, middleware chain, binding and validation, recovery | IA platform (C1) | Production |
| **Django** | Batteries-included Python web framework | ORM, migrations, admin, auth, DRF | GeeksforGeeks doubt platform (10K+ daily queries, 10x contest spikes) | Production (historical) |
| **REST** | Resource-oriented HTTP APIs | Verbs and status codes, idempotent methods, pagination, versioning, 202 with polling | Every project | Production |
| **gRPC** | RPC framework over HTTP/2 with Protocol Buffers | Protobuf schemas and codegen, unary versus streaming calls, deadlines | Not used in a resume bullet. REST was primary | Literacy |
| **Pydantic** | Data validation from Python type hints | Models, validators, JSON schema, strict types | IA structured LLM outputs and the Ask Iris service | Production |
| **Celery** | Python distributed task queue | Broker, workers, retries with backoff, rate limits, chains | Skills line only. My production queue story is Kafka | Skills-level |
| **asyncio** | Python's cooperative concurrency | Event loop, `await`, `gather`, never block the loop, `to_thread` | Skills line. The async Ask Iris WebSocket handler is where the idea shows up, but no bullet names asyncio | Skills-level |

Not on the skills line but on a Tech line or in a bullet: **JUnit** (Uber FRM tech line; JUnit 5 with Mockito and MockMvc, 100% module statement coverage), **Google Wire** and **h2c** (IA C1 bullet). Bean Validation (`@Valid`, `@NotNull` on request DTOs) and Spring Kafka (`@KafkaListener`) are how the FRM and Masters services used Spring, explained on [postgres_mysql_redis.md](postgres_mysql_redis.md) and [kafka_streaming.md](kafka_streaming.md). Go details: [go_gin.md](go_gin.md).

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
| **Apache Kafka** | Partitioned, replayable event log | Topics, partitions, keys and ordering, consumer groups, offsets, at-least-once, DLQ, lag | Uber Menu (Python producers, keyed by vendor, feeds Flink). Masters India (Spring Kafka consumers, keyed by GSTIN, idempotent processing, 1M+ a day) | Production (historical) |
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
| **PostgreSQL** | Open-source relational database | MVCC, indexes, isolation levels, partitioning, pooling (HikariCP in Java) | Masters India (sharded by tax quarter, via Hibernate and JdbcTemplate). IA (thin metadata, UAM, roles) | Production |
| **MySQL** | Open-source relational database | InnoDB row locks, transactions, optimistic locking, indexes | Uber FRM (8-table schema on SOADB, through Spring Data JPA / Hibernate). GeeksforGeeks | Production |
| **Redis** | In-memory key-value store | Data types, TTL, cache-aside, invalidation, stampede guards, `SET NX` locks | Masters (Spring Data Redis, read load down 30%). IA (auth waterfall front cache). GFG (counters) | Production |
| **MongoDB** | Document database | Flexible schemas, indexes, document modelling | Masters (invoice payload snapshots). GFG (doubt bodies) | Production (historical) |
| **Elasticsearch** | Search engine on inverted indexes | Analyzers, inverted index, relevance, as ELK log storage | Masters (invoice search, ELK). GFG (doubt search) | Production (historical) |
| **DynamoDB** | AWS managed key-value and document database | Partition and sort keys, capacity modes, single-table design | None | Literacy |
| **Amazon S3** | AWS object storage | Buckets, keys, durability, lifecycle rules, presigned URLs | Skills line. Under Masters' AWS stack, bulk import files landed in object storage. No bullet names it | Skills-level. Do not claim deep ownership |

Deep page: [postgres_mysql_redis.md](postgres_mysql_redis.md). MongoDB and Elasticsearch depth: [../../../prep/02_mongodb_elasticsearch.md](../../../prep/02_mongodb_elasticsearch.md).

---

## 6. Cloud and DevOps

| Skill | What it is | Fundamentals to know | Where | Strength |
|---|---|---|---|---|
| **GCP** | Google Cloud | Compute, storage, BigQuery, IAM basics | IA, Uber Menu | Production (keep product names qualitative unless sure) |
| **AWS** | Amazon Web Services | Amazon S3, KMS, compute, IAM basics | Masters India | Production (historical) |
| **Docker** | Container images and runtime | Layers and caching, small pinned images, one process per container | IA, FRM, Menu, Masters tech lines | Production |
| **Kubernetes** | Container orchestration | Pods, deployments, services, HPA, probes, graceful SIGTERM | None | Literacy. No cluster operations claim |
| **Maven** | The standard Java build and dependency tool | `pom.xml`, dependency scopes, lifecycle phases (compile, test, package), plugins, the Spring Boot parent and fat JAR | Skills line. FRM built with Bazel inside Uber's monorepo, and no bullet names Maven | Skills-level |
| **Bazel** | Hermetic, incremental monorepo build system | BUILD files, test targets, caching, stacked PRs | Uber FRM (Java test targets per layer) | Production |
| **CI/CD** | Automated checks and releases | Test gates, coverage gates, canaries, rollbacks | Masters (coverage from 35% to 82%, 98% deploy success). FRM (Bazel gates, 100% module coverage). IA (80% eval promotion gate) | Production |
| **Datadog** | Hosted metrics, logs and APM | Traces and spans, service maps, monitors | IA Go edge distributed tracing (C1) | Production |
| **ELK** | Elasticsearch, Logstash, Kibana | Structured logs, correlation ids, dashboards | Masters India (triage down 70%) | Production (historical) |
| **New Relic** | Hosted APM | Distributed tracing, error rates, alerting | Masters India (Java agent on the Spring Boot services) | Production (historical) |

Deep page: [observability_cloud.md](observability_cloud.md).

---

## 7. Architecture and Core Concepts

| Skill | What it means | Fundamentals to know | My best example | Strength |
|---|---|---|---|---|
| **Distributed systems** | Many services and machines cooperating over a network | Partial failure, retries, timeouts, consistency models, idempotency | Masters bulk pipeline. Menu Kafka and Flink. IA copier | Production |
| **Microservices** | Small services owning one domain each | Service boundaries, strangler migration, shared database during cutover | Masters PHP monolith to Spring Boot microservices | Production (historical) |
| **System design (HLD and LLD)** | High-level architecture and low-level class and schema design | Requirements, capacity math, data model, failure modes, trade-offs | Any project whiteboard. FRM schema and entities (LLD). Menu pipeline (HLD) | Production |
| **Data structures and algorithms** | Problem solving fundamentals | Complexity, hashing, trees, graphs, DP | Google Code Jam Qualifier 2021, rank 2260 out of 37,000+. HackerRank Problem Solving certificate | HISTORICAL achievements |
| **Caching** | Keeping hot data close and cheap to read | Cache-aside, TTL, invalidation, stampede, precomputation | Masters Redis (read load down 30%). IA ClickHouse rollups as precomputation. IA auth cache | Production |
| **Reliability** | Keeping systems working under failure | Timeouts, circuit breakers, checkpoints, DLQs, bounded retries, canaries, graceful fallback | IA registry (timeouts, breakers, checkpoints, deterministic fallback). Masters DLQ and retries. Go edge nested timeouts | Production |
| **Multithreading** | Running work in parallel threads | Races, locks, thread pools, the GIL, Java executors | Go copier double buffering. Spring Boot's thread-per-request model. Fixed Spring Kafka consumer threads at Masters capping concurrent IRP calls | Production |
| **Database sharding** | Splitting data across tables or servers by a key | Shard key choice, routing, hot shards, archiving | Masters PostgreSQL sharded by tax quarter. (ClickHouse partitions by season are partitioning, not sharding) | Production (historical) |
| **Concurrency** | Many tasks in progress at once | async versus threads versus goroutines, backpressure, bounded concurrency | Go goroutines. Masters consumer concurrency with WebClient timeouts on IRP calls. Async Ask Iris WebSocket handler. Flink parallelism | Production |
| **Idempotency** | Doing it twice has the same effect as once | Idempotency keys, upserts, unique constraints, version columns | Masters `client + fileHash + batchIndex`. Menu catalog upserts. FRM SHA-256 natural keys. IA ReplacingMergeTree versions. GFG unique (user, content) votes | Production |

---

## 8. Anti-patterns: what not to claim

- No **Spring Boot at Impact Analytics.** IA platform APIs are Go/Gin and the agent plane is Python.
- No **Terraform** or **Kubernetes operator or cluster operations** ownership.
- No **Spark**, **Pinot**, **Vitess** or **Pinecone** on the resume. Spark is a verbal backfill option for Menu only.
- No **Kafka, Flink, CDC or Milvus at Impact Analytics.** The CDC pipeline there was written by a colleague, Ashvin Sharma.
- No **Celery at Masters India** on this resume. Background work there is Spring Kafka consumers, with `@Async`, scheduled jobs and Spring Batch as the patterns for side work and chunked imports.
- No **fine-tuning or SFT** claims.
- No **human review queues (HITL)** at Impact Analytics.
- **Ask Iris is shipped** (capability, no SLA). The **Cluster Recommendation Copilot is still being built** (say "building"). Its load test is pending, and its 14 tools and 3 confirm gates are verbal design depth. Older prep said "do not claim production agentic load-test PASS, AssortSmart is building". The accurate version is that Ask Iris shipped and the Copilot load test is pending.
- **Mentorship and SOA** are not skills-line items. Defend them from the bullets (mentored 2 at Masters, led 3 at FRM, and SOADB at FRM). **Design Patterns** was removed from Skills in August 2026 and is verbal only.
- Older versions of this map listed **Linux**, **PostHog** and "embeddings for IA async jobs". None of those are on the current resume. Older versions also said **Microservices and ELK** were removed from Skills. Both are back on the skills line.

---

## 9. Rapid-fire drill

1. **Where is Java?** Uber FRM and Masters India, both Spring Boot.
2. **Where is Spring Boot not?** Impact Analytics. The platform there is Go/Gin.
3. **Where is Flink?** Uber Menu only.
4. **Where is Kafka?** Uber Menu and Masters India. Two different products. Masters consumers are Spring Kafka.
5. **Where is FastAPI?** The IA agent plane, for the Ask Iris WebSocket.
6. **Where is LangSmith?** Ask Iris at Impact Analytics.
7. **Where is Milvus?** Uber Menu only.
8. **Is MCP a production claim?** No. Skills-level.
9. **Are Spring Security, Spring Batch, Maven or Celery production claims?** No. Skills-level. Explain where they fit.
10. **Where is Go?** Impact Analytics: the Gin platform, KPI parser, auth middleware and copier.
11. **What is your strongest database story?** FRM's 8-table MySQL schema, `@Version` optimistic locking and the column-aliasing bug, or IA's ClickHouse rollups and 170GB OOM fix.
12. **Have you run Kubernetes clusters?** No. Literacy only.
13. **gRPC?** Literacy. REST was primary.
14. **Where did you shard a database?** Masters India: PostgreSQL by tax quarter.

---

## Related

- [00_index.md](00_index.md)
- [../../../handbook/09_tech_glossary.md](../../../handbook/09_tech_glossary.md)
- [../../../prep/36_skills_ai_agents_defense.md](../../../prep/36_skills_ai_agents_defense.md)
