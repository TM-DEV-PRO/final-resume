# Role targeting + rapid-fire — Java / Spring senior SWE

Use this when applying with `resume_java` / `Tarun_Mittal_SSE_Java_5yr.pdf`. Lead with Java/Spring keywords; keep cloud, Kafka, and systems stories.

## 1. Role families and what to lead with

| Role family | Screen for | Lead with |
|---|---|---|
| Senior Java / Spring Boot backend | Spring Boot, JPA, microservices, REST, SQL | Masters India migration (Spring Boot + Batch, p95, 1M+ txn/day) + Uber FRM (JPA, 36 APIs, audit correctness) |
| Platform / distributed systems (Java shops) | Kafka, scale, design | Menu ingestion (Kafka/Flink/Spark/Pinot — Python + streaming) + IA ClickHouse write model |
| FinTech / payments / compliance Java | Correctness, audits, observability | FRM (PwC work papers, 100% module coverage) + GST (RBAC, audit logs, idempotency) |
| AI platform with Java services | Agents + solid backend | IA: Python agent service + Spring Boot core + ClickHouse |
| SRE-leaning Java | Observability, K8s, incidents | ELK + New Relic 70% triage; Actuator/metrics; Pinot ops dashboards |

## 2. Rapid-fire (Java resume claims)

**"Spring Boot microservices with worker pools — how?"**  
Bulk-save handler validates the batch, assigns a version, submits chunk insert tasks to a fixed `ThreadPoolExecutor` with a bounded queue and `CallerRunsPolicy` (or abort + 429). Each task uses the ClickHouse batch API; futures collected with a per-request deadline. Pool sized from DB/ClickHouse connection budget, not "CPU cores × 200."

**"Why Hibernate then also ClickHouse?"**  
Different workloads. Hibernate/JPA on PostgreSQL/MySQL for OLTP metadata and FRM CRUD. ClickHouse for insert-only / partition-swapped analytical/planning facts — mutations are the wrong model there; we insert versions (or swap partitions) and read latest state via views. Never claim Hibernate→ClickHouse.

**"100% changed-module coverage — how enforced?"**  
CI computes coverage for files touched in the PR; merge blocked under threshold. Encourages tests with the code, not a heroic end-of-quarter push.

**"Did you really build Uber FRM / Masters / GFG in Spring?"**  
This Java resume is a **positioning track** for Spring roles — same products, schemas, endpoints, and metrics as the live systems. Defend architecture and outcomes first; map service/ORM boundaries to Spring idioms. Do not invent org-specific Spring internals you cannot walk through line-by-line.

## 3. Claims interviewers poke hardest

- **IA p95 &lt;500 ms / &lt;80 ms edits:** design targets from NFRs — say "design target," not "we measured in prod for a year."
- **Menu $600K+/yr:** finance-owned cost model; know the arithmetic.
- **Java vs your Python/Go track:** "Same systems and ownership; this resume leads with Spring for Java roles. Agentic/RAG stays Python because that is the real agent stack." Interviewers respect a bilingual story more than a brittle all-Java claim.

## 4. System design prep picks (Java interview)

1. **Planning grid backend** — versioned writes, ClickHouse, Spring API tier + Python agents.  
2. **Menu ingestion** — Kafka → Flink → sinks; Python RAG path (no Spring claim on resume).  
3. **GST bulk e-invoice** — Spring Batch + idempotency + rate limits to external IRP.
