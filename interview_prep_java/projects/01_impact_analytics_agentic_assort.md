# Impact Analytics — Agentic AssortSmart (Java / Spring track)

**Role:** Senior Software Engineer · June 2026 – Present · Bangalore  
**Resume header tech:** Java · Spring Boot · Spring AI / LangChain4j · MCP · Hibernate · ClickHouse · PostgreSQL · Redis · Kafka · GCP · Docker

> Same product, metrics, and architecture as `interview_prep/projects/01_impact_analytics_agentic_assort.md` and the agentic playbook. This file is the **Java/Spring telling** for interviews targeting Java backend roles.

---

## 1. Elevator pitch (30 seconds)

"I work on the agentic rebuild of AssortSmart — a merchandise planning SaaS where enterprise retailers decide what products to buy, in what quantities, for which stores, a season ahead. AI agents draft store clusters and plans; planners review, override, and approve. Architecturally it's one Spring Boot agentic microservice (Spring AI / LangChain4j, MCP) that runs agentic workflows, and a Spring Boot core backend exposing REST APIs for plan lifecycle, reference data, and bulk saves. I own the store-clustering agent: it grounds a plain-language request into hierarchy, season, and store scopes, batch-evaluates ~100 silhouette-scored candidate clusterings, and presents the top 3 with evidence for planner approval — turnaround from days to under an hour. Under both sits ClickHouse with an append-only versioned write model — every planner override is an insert — giving version diff, undo/redo, and an immutable audit trail."

## 2. Service split (say it exactly)

"One Spring Boot microservice runs all agentic workflows — agents, tools, LLM orchestration via Spring AI / LangChain4j and MCP. The core backend is also Spring Boot: REST controllers for plan lifecycle, tenant config, and bulk saves, secured with Spring Security JWT. The two talk over versioned API contracts. The split is a natural deployment boundary — the agent tier scales with LLM latency; the API tier scales with request volume."

## 3. Spring Boot core backend — defend the bullet

Resume: *"Spring Boot microservices covering plan lifecycle, tenant configuration, and bulk save REST APIs, with ExecutorService worker pools and bounded queues for concurrent writes, request-scoped timeouts, and JWT auth via Spring Security."*

- **Plan lifecycle** — `@RestController` endpoints: create/copy/finalize/soft-delete; state machine in a `@Service` (draft → in-review → finalized); finalize enforces role + confirmation token.
- **Reference data** — hierarchy trees, fiscal calendars, store masters, tenant config. Concurrent reads via `CompletableFuture` / virtual threads with a shared timeout; partial-safe composites.
- **Bulk save** — grid save arrives as a batch of cell edits; service assigns one `version = epoch-ms`, validates with Bean Validation (`@Valid` + custom validators), fans batched ClickHouse inserts through a **bounded `ExecutorService`** (fixed pool + `ArrayBlockingQueue` / `ThreadPoolExecutor` rejection policy). Idempotency: batch id + content hash.
- **Spring Security** — JWT resource server; tenant + role claims; filter chain for correlation IDs, validation, rate limits.
- **Timeouts** — `@Transactional` boundaries for Postgres metadata; ClickHouse clients with request deadlines; graceful shutdown drains the pool (`DisposableBean` / `@PreDestroy`).
- **Why Spring here:** "This tier is bind → validate → authorize → fan-out I/O → return. Spring Boot gives me production defaults (Actuator, metrics, config), Hibernate for the thin Postgres metadata plane, and a boring enough codebase that the team can own it."

## 4. Agentic microservice — defend the clustering bullet

Same product behavior as the main playbook (HLR-AG-001…006): autonomous feature selection, k optimization via silhouette, top 3 scenarios with evidence, approval gating, <1 h turnaround.

**Java framing:**
- Orchestration graph in LangChain4j / Spring AI (nodes = tool calls + LLM steps; state held in a typed conversation/session object).
- Tools call ClickHouse / Postgres / Redis via Spring beans (repositories), not ad-hoc HTTP from prompts.
- MCP tools as first-class integrations where the platform exposes them.
- Streaming progress to the UI via SSE (`SseEmitter` / WebFlux `Flux`).

## 5. ClickHouse append-only store

Unchanged from main track: `ReplacingMergeTree(version)`, `argMax` / latest-state views, `REPLACE PARTITION` seeds, never-erase inserts, Postgres for true ACID metadata (auth, tenant config, workflow state).

**Precision:** planning-grid transactionality ≠ bank-ledger OLTP. Say this unprompted.

## 6. Stack evolution story (senior narrative)

1. Live audit said "no ClickHouse" for legacy in-place UPDATEs — correct for that write model.
2. Verdict: objection is write-model, not engine → gated PoC on insert-only semantics.
3. PoC passed → org committed ClickHouse end-to-end; Spring Boot for API + agent tiers; ClickHouse for planning facts.

## 7. Q&A (Java-flavored)

- **"Why Spring Boot over Quarkus/Micronaut?"** Team familiarity, Actuator/observability ecosystem, Spring Data + Security maturity; Quarkus wins on cold start for serverless — not our deployment model.
- **"Hibernate on ClickHouse?"** No — ClickHouse via native JDBC / clickhouse-java client. Hibernate/JPA only on PostgreSQL metadata.
- **"Virtual threads?"** Prefer virtual threads for blocking I/O fan-out on Java 21+; keep a bounded platform-thread pool for CPU-bound scoring if needed.
- **"How do you test?"** JUnit 5 + Mockito for services; `@SpringBootTest` + Testcontainers for Postgres/Redis integration; contract tests on REST with MockMvc / WebTestClient.
