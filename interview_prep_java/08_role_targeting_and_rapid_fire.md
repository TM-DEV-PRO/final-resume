# Role targeting + rapid-fire — Java / Spring senior SWE

Use this when applying with `resume_java` / `Tarun_Mittal_SSE_Java_5yr.pdf`. Lead with Java/Spring keywords; keep cloud, Kafka, and systems stories.

## 1. Role families and what to lead with

| Role family | Screen for | Lead with |
|---|---|---|
| Senior Java / Spring Boot backend | Spring Boot, JPA, microservices, REST, SQL | Masters India migration (WebFlux/Batch, p95, 1M+ txn/day) + Uber FRM (JPA, 36 APIs, audit correctness) |
| Platform / distributed systems (Java shops) | Kafka, scale, design | Menu ingestion (Kafka/Flink/Spark/Pinot) + IA ClickHouse write model |
| FinTech / payments / compliance Java | Correctness, audits, observability | FRM (PwC work papers, 100% module coverage) + GST (RBAC, audit logs, idempotency) |
| AI platform with Java services | Agents + solid backend | IA: Spring AI agent service + Spring Boot core + ClickHouse |
| SRE-leaning Java | Observability, K8s, incidents | ELK + New Relic 70% triage; Actuator/metrics; Pinot ops dashboards |

## 2. Rapid-fire (Java resume claims)

**"Spring Boot microservices with ExecutorService worker pools — how?"**  
Bulk-save handler validates the batch, assigns a version, submits chunk insert tasks to a fixed `ThreadPoolExecutor` with a bounded queue and `CallerRunsPolicy` (or abort + 429). Each task uses the ClickHouse batch API; futures collected with a per-request deadline. Pool sized from DB/ClickHouse connection budget, not "CPU cores × 200."

**"Why Hibernate then also ClickHouse?"**  
Different workloads. Hibernate/JPA on PostgreSQL/MySQL for OLTP metadata and FRM CRUD. ClickHouse for append-only analytical/planning facts — mutations are the wrong model there; we insert versions and read latest state.

**"WebFlux in production — pitfalls?"**  
Don't call blocking JDBC on event-loop threads; propagate MDC/security context; prefer a small team fluent in Reactor — otherwise MVC + virtual threads is a valid alternative I'd defend.

**"J2EE on your skills — what do you mean?"**  
Jakarta EE concepts: Servlets/filters, DI, JPA, transaction boundaries, connection pools. Day-to-day delivery is Spring Boot on embedded Tomcat implementing those patterns — not claiming I ran a full EE app server for every project.

**"100% changed-module coverage — how enforced?"**  
CI computes coverage for files touched in the PR; merge blocked under threshold. Encourages tests with the code, not a heroic end-of-quarter push.

## 3. Claims interviewers poke hardest

- **IA p95 &lt;500 ms / &lt;80 ms edits:** design targets from NFRs — say "design target," not "we measured in prod for a year."
- **Menu $600K+/yr:** finance-owned cost model; know the arithmetic.
- **Java vs your public Python/Go work:** "This resume positions the same systems for Java/Spring roles — architecture and ownership are mine; idioms are Spring/JPA equivalents of the service boundaries I designed." Be ready to discuss either stack without freezing — interviewers respect bilingual backends more than a brittle claim.

## 4. System design prep picks (Java interview)

1. **Planning grid backend** — versioned writes, ClickHouse, Spring API tier.  
2. **Menu ingestion** — Kafka → Flink → sinks; Spring control plane.  
3. **GST bulk e-invoice** — Batch + idempotency + rate limits to external IRP.
