# Tech depth index

<div class="callout note">

**How to use this page**

- **What it covers:** the map of the tech-depth folder. There is one study page per technology group on my resume. Each page teaches the technology from scratch, shows exactly where I used it, explains the design choices, ties the numbers, and ends with interview questions and speakable answers.
- **When to read it:** at the start of a study session, to pick the pages that match the job description. Read the "Where each technology lives" table before any round.
- **What to memorise:** the placement table below. Most interview slip-ups are putting a technology on the wrong project.
- **Which resume:** these pages match `Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf`, whose summary says "Expertise in Java, Python and Go microservices". Uber FRM and Masters India are Java and Spring Boot. Impact Analytics is Go/Gin plus a Python agent plane.

</div>

**Labels used across these pages.** MEASURED means we have a log, doc, config or code for it. STATED means printed on the resume from the project's own source with no extra arithmetic in prep. ESTIMATED means arithmetic I can show ("roughly, derived from..."). HISTORICAL means from my past work records. TARGET means a design goal ("targeting"). Verbal means true but not printed on the resume.

---

## Where each technology lives

| Technology | Project | Notes |
|---|---|---|
| Go, Gin, Google Wire, h2c, Datadog | Impact Analytics (Core) | 10k peak RPS. No SLA. No Kubernetes operations |
| ClickHouse, BigQuery | Impact Analytics | 15.5x pivots, 170GB OOM fix, about 344k rows per second, 4.09B in flight, 2.11B master |
| LangGraph, LangSmith | Impact Analytics, Ask Iris | Supervisor plus 3-attempt evaluator. Keep/Drop has a fixed step order and no LLM orchestrator |
| Python, FastAPI (agent plane) | Impact Analytics | Keep/Drop batch, Ask Iris WebSocket. Never Spring Boot at IA |
| PostgreSQL, Redis | IA (thin metadata, auth cache), Masters (sharded, cache-aside) | |
| Java, Spring Boot, Spring Data JPA, Hibernate, MySQL, JUnit, Bazel, Docker | Uber FRM (Uber via EPAM) | 36 Spring Boot endpoints, 8-table schema, 100% module statement coverage |
| Python, Selenium, Kafka, Flink, LangChain RAG, Gemini 2.5 Pro, Milvus | Uber Menu (Uber via EPAM) | 30K+ menus a month, from 24 hours to 2 hours, 98% offline field fidelity |
| Java, Spring Boot, Hibernate, Kafka, PostgreSQL, MongoDB, Redis, Elasticsearch, ELK, New Relic, AWS | Masters India | PHP monolith to Spring Boot microservices. 1M+ submissions a day. No Flink |
| Django, MySQL, MongoDB, Redis, Elasticsearch | GeeksforGeeks | 10K+ daily queries |
| Spring MVC, Spring Security, Spring Batch, Maven, Amazon S3, Celery, asyncio | Skills-level | On the skills line. No bullet names them |
| MCP, tool calling | Skills-level | IA tool design (Cluster Copilot, 14 tools) is verbal only |
| C, C++, pgvector, DynamoDB, Kubernetes, gRPC | Literacy | No production ownership claims |

<div class="callout warn">

**The lines interviewers check most**

- No Kafka, Flink, CDC, Milvus or Kubernetes operations at Impact Analytics.
- 80% is a CI promotion gate on 300 cases. 73% and 74% come from a separate gold-200 benchmark.
- 15.5x is query time. 170GB OOM is load time. Not cause and effect.
- 344k is rows per second, not requests. 4.09B was measured in flight.
- "Exactly-once" means at-least-once delivery plus idempotent writes.
- Led 3 (Uber FRM) and mentored 2 (Masters India) are different teams.
- IA platform APIs are Go/Gin. Spring Boot belongs to Uber FRM and Masters India only.

</div>

---

## The pages

| Page | What it covers | Read it before |
|---|---|---|
| [python_fastapi.md](python_fastapi.md) | Python, GIL, asyncio, FastAPI, Pydantic, Celery, Django. The IA agent plane (Ask Iris), Menu's Python services, GFG on Django, plus a pointer to the Java services and a Python-to-Spring comparison table | Python backend and AI rounds, IA Agentic deep dive |
| [go_gin.md](go_gin.md) | Go, Gin, goroutines, context, Wire, h2c, nested timeouts, Datadog, the KPI formula compiler, the copier | Go rounds, platform design, IA Core |
| [langgraph_mcp_rag.md](langgraph_mcp_rag.md) | LLM agents, structured outputs, LangGraph and Ask Iris, Keep/Drop lenses, tool calling, MCP, prompt engineering, offline eval, RAG, Milvus, LangChain, LangSmith | AI engineer rounds, IA Agentic, Menu RAG |
| [clickhouse.md](clickhouse.md) | Columnar storage, MergeTree, partitions, ReplacingMergeTree, the six rollups, the 170GB OOM, the Go copier, the 2.11B master | Data platform rounds, IA Core, "hardest problem" |
| [kafka_streaming.md](kafka_streaming.md) | Kafka fundamentals (partitions, keys, consumer groups, offsets, DLQ, lag) at Uber Menu and Masters India, and the Spring Kafka client view (`@KafkaListener`, `DefaultErrorHandler`, `DeadLetterPublishingRecoverer`) | Streaming and event-driven design |
| [flink.md](flink.md) | Flink fundamentals (keyed state, event time, watermarks, checkpoints) on the Menu hot path. Spark as a verbal backfill option | Menu deep dive, "why Flink" |
| [kafka_flink_scale_defense.md](kafka_flink_scale_defense.md) | Attack-and-defense sheet: "30K a month is tiny", peak rates, exactly-once, recovery | The night before a streaming or system design round |
| [auth_tenancy_rate_limits.md](auth_tenancy_rate_limits.md) | AuthN versus AuthZ, JWT, OIDC, constant-time keys, multi-tenancy, token buckets. The IA waterfall, Ask Iris scope freeze, AI-level budgets, FRM, Masters, Menu | Security and multi-tenant SaaS questions |
| [postgres_mysql_redis.md](postgres_mysql_redis.md) | Transactions, indexes, locking, sharding, cache-aside. Spring Data JPA and Hibernate at FRM (`@Version`, `@Transactional`, the column-aliasing bug), Masters quarter shards through Hibernate, JdbcTemplate and HikariCP, Spring Data Redis, MongoDB and Elasticsearch briefly | Database and schema design rounds, FRM and Masters deep dives |
| [observability_cloud.md](observability_cloud.md) | Logs, metrics and traces. Datadog, LangSmith, JSON telemetry, ELK, New Relic, Docker, GCP, AWS, Kubernetes literacy, Bazel, CI/CD | Debugging, on-call and DevOps questions |
| [selenium_scraping.md](selenium_scraping.md) | WebDriver, waits, bot detection, proxy pools, adaptive retries, the Menu fleet | Menu deep dive, "design a crawler" |
| [skills_fundamentals_map.md](skills_fundamentals_map.md) | Every skills-line item: what it is, fundamentals, where used, claim strength | Any "tell me about X on your resume" moment |

---

## Suggested study order

1. [skills_fundamentals_map.md](skills_fundamentals_map.md), to know what you can claim and how strongly.
2. The pages for your two strongest stories: [clickhouse.md](clickhouse.md) and [langgraph_mcp_rag.md](langgraph_mcp_rag.md) (Impact Analytics).
3. [go_gin.md](go_gin.md) and [auth_tenancy_rate_limits.md](auth_tenancy_rate_limits.md) (IA Core).
4. [postgres_mysql_redis.md](postgres_mysql_redis.md) and [kafka_streaming.md](kafka_streaming.md) for the Java services (Uber FRM and Masters India), then [python_fastapi.md](python_fastapi.md) for the Python side and the Spring comparison table.
5. [flink.md](flink.md), [selenium_scraping.md](selenium_scraping.md), then [kafka_flink_scale_defense.md](kafka_flink_scale_defense.md) (Uber Menu and Masters streaming).
6. [observability_cloud.md](observability_cloud.md) last, as glue for "how do you debug it".

---

## Elsewhere in the repo

- Handbook tech glossary (one entry per technology, shorter, including Java, Spring Boot, Spring MVC, Spring Security, Spring Data JPA, Hibernate, Spring Batch, Maven and JUnit): [../../../handbook/09_tech_glossary.md](../../../handbook/09_tech_glossary.md)
- Generative AI skills defense table: [../../../prep/36_skills_ai_agents_defense.md](../../../prep/36_skills_ai_agents_defense.md)
- Every resume number, derived: [../../../prep/09_metrics_derivations.md](../../../prep/09_metrics_derivations.md)
- IA bullet-by-bullet defense: [../../../prep/43_ia_bullet_defense.md](../../../prep/43_ia_bullet_defense.md)
- ClickHouse rollups and copier: [../../../prep/42_clickhouse_rollup_migration.md](../../../prep/42_clickhouse_rollup_migration.md)
- Architecture pages: [../architecture/00_index.md](../architecture/00_index.md)
- Numbers defense: [../numbers_defense.md](../numbers_defense.md)
- Design decisions and trade-offs: [../design_decisions_tradeoffs.md](../design_decisions_tradeoffs.md)
