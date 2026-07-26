# Skills on the campaign PDF → fundamentals + where used

Every skill line on `campaign_pygo_xyz/resume/sections/skills.tex`. If you cannot place it, do not emphasize it in interviews.

---

## Languages
| Skill | Fundamentals | Where on resume |
|---|---|---|
| **Python** | GIL vs I/O, asyncio, typing, packaging | IA agent, Menu, Masters, FRM |
| **Go** | goroutines, channels, static binary, Gin | IA doing layer |
| **SQL** | joins, indexes, EXPLAIN, transactions | All data stores |
| **C / C++** | memory, systems literacy | Listed as literacy — no production ownership claim |

## Backend and APIs
| Skill | Fundamentals | Where |
|---|---|---|
| **FastAPI** | ASGI, Pydantic validation, dependency injection | IA agent, FRM, Masters |
| **Gin** | middleware, binding, handlers | IA Go APIs |
| **Django** | MVT, ORM — GFG-era web | GFG |
| **SQLAlchemy / Pydantic** | ORM vs Core, models/validation | FRM |
| **REST / gRPC** | idempotency, versioning; protobuf/contracts | REST primary; gRPC as protocol literacy |
| **Celery** | brokers, retries, acks | Masters async jobs (alongside Kafka) |
| **asyncio** | event loop, fan-out I/O | FastAPI agent / workers |
| **Design Patterns / SOA** | strangler, gateway, bounded contexts | Masters strangler; FRM services |

## AI and Agents
| Skill | Fundamentals | Where |
|---|---|---|
| **LLM agents** | tool calling, non-determinism, cost/latency | IA copilot |
| **LangGraph** | stateful graphs, checkpoints | IA |
| **LangChain** | chains/retrievers glue | IA / Menu RAG |
| **MCP** | tool protocol / host | IA tools |
| **RAG** | chunk, embed, retrieve, generate, validate | Menu extraction |
| **pgvector** | ANN indexes, embedding storage | vector literacy / RAG stacks |

See also: [langgraph_mcp_rag.md](langgraph_mcp_rag.md), [projects/01d_agentic_evals_guardrails_flow.md](../projects/01d_agentic_evals_guardrails_flow.md).

## Data and Streaming
| Skill | Fundamentals | Where |
|---|---|---|
| **Kafka** | partitions, keys, consumer groups, lag, DLQ | Menu ingest, Masters IRP, IA async jobs |
| **Flink** | keyed state, watermarks, parallelism | Menu hot path |
| **ClickHouse** | MergeTree, parts, PK/order by, append-only | IA |
| **BigQuery** | warehouse scans, slots | IA historical / POC baselines |
| **PostgreSQL** | MVCC, indexes, sharding | Masters quarter shards; IA config |
| **MySQL** | InnoDB, transactions | FRM SSOT |
| **Redis** | cache-aside, TTL, stampede | Masters −30% reads |
| **MongoDB** | document model | Masters adjacent storage |
| **Elasticsearch** | inverted index, scoring | Masters ELK logs |
| **DynamoDB** | partition keys, RCU/WCU | cloud NoSQL literacy / AWS paths |
| **S3** | object storage, prefixes | Menu payloads, cloud artifacts |

See: [kafka_streaming.md](kafka_streaming.md), [flink.md](flink.md), [clickhouse.md](clickhouse.md), [postgres_mysql_redis.md](postgres_mysql_redis.md).

## Cloud and Infra
| Skill | Fundamentals | Where |
|---|---|---|
| **GCP** | GCE/GKE literacy, GCS | IA, Menu |
| **AWS** | compute/DB/network basics | Masters |
| **Docker** | images, layers, healthchecks | All |
| **Kubernetes** | pods/services — **familiarity**, not cluster-admin ownership | Skills only |
| **Linux / CI/CD** | processes, pipelines | All |
| **Bazel** | hermetic builds, test targets | FRM **1,100+** tests |
| **ELK / New Relic** | correlating request IDs | Masters triage −70% |
| **Datadog / PostHog / LangSmith** | platform / product / agent | IA |

See: [observability_cloud.md](observability_cloud.md).

## Core
| Skill | Fundamentals | Where |
|---|---|---|
| **Distributed Systems** | consistency, retries, backpressure | All post-GFG |
| **Microservices** | independent deploy, contracts | Masters, IA, FRM |
| **HLD/LLD** | API + schema + sequence | FRM ownership; IA HLD |
| **Multithreading / Concurrency** | threads vs async vs goroutines | Go pools; Python asyncio; Java track separate |
| **Caching / Sharding** | cache-aside; PG quarter shards; CH partitions | Masters, IA |
| **Mentorship** | led **3** (FRM), mentored **2** (Masters) | Explicit bullets |
| **JWT / AuthZ / quotas** | Tenant claims, API vs AI limits | All — see [auth_tenancy_rate_limits.md](auth_tenancy_rate_limits.md) |

---

## Selenium
Covered in [selenium_scraping.md](selenium_scraping.md) (Menu Tech, not skills row — still defend).

## Anti-patterns
- Do not claim **Terraform** / **K8s operator** ownership.
- Do not claim **Spark** on PDF unless you add it; Spark stays verbal backfill next to Flink.
- Do not claim **production agentic load-test PASS** — see 01d.
