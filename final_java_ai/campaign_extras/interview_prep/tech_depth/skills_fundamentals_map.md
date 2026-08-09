# Skills on the final PDF → fundamentals + where used

Maps every skill on `final_*/sections/skills.tex` (synced skeleton). If you cannot place it, do not emphasize it in interviews.

**AI line deep defense:** open `prep/36_skills_ai_agents_defense.md` in this final folder.

---

## Languages
| Skill | Fundamentals | Where on resume |
|---|---|---|
| **Python** | GIL vs I/O, asyncio, typing, packaging | IA agent, Menu, Masters (PyGo) / IA agents + Menu (Java track) |
| **Go** | goroutines, channels, static binary, Gin | IA doing layer (PyGo) |
| **Java** | JVM, concurrency, Spring ecosystem | FRM / Masters / GFG (Java track) |
| **SQL** | joins, indexes, EXPLAIN, transactions | All data stores |
| **C / C++** | memory, systems literacy | Listed as literacy — no production ownership claim |

## Backend and APIs
| Skill | Fundamentals | Where |
|---|---|---|
| **FastAPI / Gin / Django / Pydantic** (PyGo) | ASGI, validation, handlers | IA, FRM, Masters, GFG |
| **Spring Boot / MVC / Security / Data JPA / Hibernate / Batch** (Java) | controllers, security, ORM, batch | FRM, Masters, GFG, IA write APIs |
| **REST / gRPC** | idempotency, versioning; protobuf literacy | REST primary |
| **Celery / asyncio** (PyGo) | workers, event loop | Masters / agent I/O |
| **Design Patterns** | strangler, layered services | Masters, FRM |

## AI and Agents
| Skill | Fundamentals | Where |
|---|---|---|
| **LLM agents** | multi-step loops, cost/latency, non-determinism | IA copilot |
| **LangGraph** | stateful graphs, checkpoints | IA |
| **LangChain** | chains/retrievers glue | IA / Menu RAG |
| **MCP** | tool protocol / host | IA tools |
| **tool calling** | typed tools, arg validation, no free-form SQL writes | IA (14 tools / 3 gates verbal) |
| **prompt engineering** | system/tool prompts, structured outputs | IA + Menu extraction |
| **RAG** | chunk, embed, retrieve, generate, validate | Menu extraction |
| **embeddings** | vectorize corpus; index freshness | Menu Milvus; IA async embed jobs |
| **Milvus** | vector DB for menu RAG | Menu |
| **pgvector** | Postgres ANN literacy | Skills literacy |
| **offline eval** | golden sets; not live SLA | Menu 98%/100%; LangSmith regression |
| **LangSmith** | agent traces, eval/regression | IA (with Datadog/PostHog) |

See also: [langgraph_mcp_rag.md](langgraph_mcp_rag.md).

## Streaming and Data
| Skill | Fundamentals | Where |
|---|---|---|
| **Kafka / Flink** | partitions, keyed state, lag | Menu, Masters IRP |
| **ClickHouse / BigQuery** | OLAP pivots; warehouse | IA |
| **Batch Processing / ETL** | bulk paths | Masters, Menu, IA jobs |

## Databases and Storage
| Skill | Fundamentals | Where |
|---|---|---|
| **PostgreSQL / MySQL / Redis / MongoDB / Elasticsearch** | OLTP, cache, docs, search/logs | Masters, FRM, GFG |
| **DynamoDB / S3** (PyGo DynamoDB) | NoSQL / object storage literacy | AWS/cloud paths; Menu/IA artifacts |
| **Caching / Sharding** | cache-aside; quarter shards; CH partitions | Masters, IA |

## Cloud and Infrastructure
| Skill | Fundamentals | Where |
|---|---|---|
| **GCP / AWS / Docker / Kubernetes / Linux / CI/CD** | deploy literacy | All |
| **Maven** (Java) / **Bazel** | builds; FRM test targets | Java / FRM |
| **New Relic / Datadog / PostHog / LangSmith** | APM / platform / product / agent | Masters + IA |

See: [observability_cloud.md](observability_cloud.md).

## Core Engineering
| Skill | Fundamentals | Where |
|---|---|---|
| **Distributed Systems / HLD/LLD** | consistency, retries, design ownership | FRM, IA, Masters |
| **Multithreading / Concurrency** | threads vs async vs goroutines | All |
| **Caching / Sharding / Reliability / Testing** | ops + quality | Masters, FRM |
| **JUnit** (Java) | unit tests | FRM / Masters Java |

---

## Anti-patterns
- Do not claim **Terraform** / **K8s operator** ownership.
- Do not claim **Spark** / **Vitess** / **Pinecone** on PDF.
- Do not claim **production agentic load-test PASS** — AssortSmart is **building**.
- Do not claim **SFT** on Menu PDF.
- Mentorship / SOA / Microservices / ELK / SQLAlchemy removed from skills — defend from experience bullets if asked.
