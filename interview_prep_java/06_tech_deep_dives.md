# Tech deep-dives — Java / Spring resume track

Every technology on `resume_java`. Fundamentals → internals → why we used it → interview gotchas. Streaming (Kafka/Flink/Spark/Pinot) and ClickHouse/cloud overlap with the main track — abbreviated here with Java integration notes.

---

## 1. Java (language + concurrency)

- **Fundamentals.** Statically typed, JVM bytecode, GC'd. Memory: heap + metaspace; escape analysis; generations (young/old) — know G1 vs ZGC at a high level for latency talk.
- **Concurrency.** Threads → `ExecutorService` / `ThreadPoolExecutor` (core/max/queue/rejection). `CompletableFuture` for fan-out. **Virtual threads (Java 21+)** = cheap blocking concurrency without reactive complexity. `synchronized` / `ReentrantLock` / concurrent collections; happens-before via `volatile` / atomics.
- **Gotchas.** Thread-pool leaks (unbounded queues); `HashMap` in concurrent use → `ConcurrentHashMap`; equals/hashCode contracts; checked exceptions at API boundaries; autoboxing + identity (`==` on Integer); string concat in hot loops → `StringBuilder`.

## 2. Spring Boot + Spring MVC

- **Boot.** Auto-config + starters + embedded server + Actuator. Externalized config (`application.yml`, profiles, `@ConfigurationProperties`). Fat JAR deploy.
- **MVC.** DispatcherServlet → HandlerMapping → Controller → View/HttpMessageConverter. `@RestController` + Jackson. Filter / `HandlerInterceptor` / `ControllerAdvice` chain.
- **Why.** Fast production path for REST microservices; ecosystem for Security, Data, Batch, Kafka.
- **Gotchas.** Component-scan boundaries; circular deps; `@Transactional` self-invocation (proxy); blocking calls on Tomcat threads under load (scale threads or go WebFlux/virtual threads).

## 3. Hibernate / Spring Data JPA

- **JPA.** ORM standard; Hibernate = implementation. Entity = persistent identity; `EntityManager` / persistence context; flush vs commit.
- **Spring Data.** `JpaRepository`, derived queries, `@Query`, Specifications/Criteria for dynamic filters, `@EntityGraph`.
- **Gotchas.** N+1 lazy loads; Open Session In View (often disable in APIs); dirty checking surprises; `@OneToMany` default fetch; equals/hashCode on entities (prefer business key or don't put entities in Sets across sessions); 2nd-level cache only with clear invalidation story.
- **Do not claim:** Hibernate against ClickHouse — planning facts use the ClickHouse Java/JDBC client; JPA is for MySQL/Postgres OLTP metadata only.

## 4. Spring Security (JWT)

- **Resource server.** Validate JWT signature/issuer; map claims → `Authentication`; method security (`@PreAuthorize`) for roles/tenants.
- **Filter chain.** Stateless session; CORS; CSRF off for pure bearer APIs.
- **Gotchas.** Wrong order of filters; mixing session + JWT; leaking stack traces; not validating `aud`/`iss`.

## 5. Spring Batch + async workers

- **Batch.** Job → Step → chunk-oriented reader/processor/writer; JobRepository for restartability; skip/retry policies.
- **vs Celery (main track).** Same product need (bulk imports, retries); Spring Batch = first-class job semantics on JVM.
- **Idempotency.** Business keys in writers; restart from failed chunk without double side effects.
- **Gotchas.** Wrong chunk size; stateful processors; not making readers restartable.

## 6. Bean Validation + Jackson

- Boundary validation (`@NotNull`, custom constraints) on DTOs — never trust clients.
- Jackson: `ObjectMapper` config, `@JsonIgnore`, unknown properties policy; record/DTO preference over exposing entities.

## 7. Python agent tier (FastAPI + LangGraph + MCP)

- **Role on this resume.** All agentic / RAG / LLM orchestration stays Python — FastAPI service, LangGraph workflows, LangChain tools, MCP integrations. Spring Boot does not run the agents.
- **Why Python here.** Mature agent graphs, tool-calling, RAG, and eval loops; pairs cleanly with a Java API tier over versioned HTTP contracts.
- **Gotchas.** Prompt injection; schema validation of tool args; timeout/budget per turn; never let the model write raw SQL without a guarded text-to-SQL layer.
- Defenses for LangGraph/RAG/MCP: same depth as main `interview_prep/agentic_assort_playbook/05_tech_deep_dives.md`.

## 8. Apache Kafka (Java client / Spring Kafka)

- Same fundamentals as main track (partitions, consumer groups, exactly-once story).
- **Java:** `KafkaProducer`/`KafkaConsumer`; `spring-kafka` `@KafkaListener`; error handlers + DLT; idempotent producer config.
- **Gotchas.** Listener concurrency vs partition count; blocking work in listeners; committing offsets too early.

## 9. Flink / Spark / Pinot

Same depth as main `interview_prep/06_tech_deep_dives.md` §§3–6 (now includes ESTIMATED rates). Flink/Spark jobs are often Java/Scala at Uber; this resume's Menu **Tech Used** line stays Python + streaming (matches live stack) — do not invent a Spring control-plane bullet you cannot defend.

**Numbers to memorize (ESTIMATED):** Kafka peak ~200–500 events/sec · Flink keeps pace · Spark backfills ~1–2M item rows · Pinot sub-second health queries · +95% ingest success (~60–65% → 95%+). Full derivation: `09_metrics_derivations.md`.

## 10. Redis / MySQL / PostgreSQL / ClickHouse

- **Redis:** cache, rate limits, Batch/broker adjacent state; eviction + stampede.
- **MySQL (FRM):** normalized 8-table schema; ETL aggregation.
- **PostgreSQL:** IA metadata ACID plane; Masters India primary store.
- **ClickHouse:** append-only planning facts — **not** via Hibernate.

## 11. Cloud, build, observability

- **GCP/AWS, Docker, K8s** — same stories as main track.
- **Maven/Gradle** — reproducible builds; dependency BOM (Spring Boot parent).
- **ELK / New Relic / Grafana / Sentry / Actuator** — RED metrics, correlation IDs, alerts on user symptoms.
- **JUnit 5 / Mockito / Testcontainers** — unit vs slice (`@WebMvcTest`, `@DataJpaTest`) vs full integration.

## 12. One-line "why" for the rest

- **WebSockets/SSE:** agent progress streaming (Python agent tier / UI).
- **Bazel:** Uber monorepo build — prefer this over inventing Maven on FRM.
- **Maven:** fine for Spring Boot services outside Uber.
