# Skills defense — what was trimmed in v2

| Removed / demoted | Why | If interviewer asks anyway |
|---|---|---|
| Rust, C, C++ | Not on Tech Used; Rust is escape-hatch only per playbook | “Familiar / adjacent; Go is the shipped non-agentic tier” |
| gRPC | Not evidenced on project lines | “Would use for service-to-service binary contracts; REST is what we shipped” |
| DuckDB | Superseded by ClickHouse end-to-end (Jul 2026) | “Earlier pivot-accelerator idea; current store is ClickHouse” |
| MongoDB, Cassandra, Elasticsearch | Never on Tech Used | “General familiarity, not ownership claims on this resume” |
| ChromaDB, semantic caching | Soft vs pgvector on the live path | “pgvector / Postgres path is the one I defend; Chroma was exploratory” |

## Kept on purpose

- **BigQuery** — ingest source of truth (defend carefully)
- **WebSockets / SSE** — agent progress streaming (IA)
- **Kafka** — IA async jobs + Uber Menu bus
- **Kubernetes, Grafana, Sentry** — ops literacy next to ELK/New Relic ownership story
