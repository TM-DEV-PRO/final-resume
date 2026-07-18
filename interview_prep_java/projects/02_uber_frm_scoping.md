# Uber (via EPAM) — FRM Scoping Platform (Java / Spring track)

**Role:** Software Development Engineer 2 · July 2024 – May 2026 · Bangalore  
**Resume tech:** Java, Spring Boot, Spring Data JPA, Hibernate, Bean Validation, MySQL, Redis, Maven, JUnit

> Same domain and metrics as `interview_prep/projects/02_uber_frm_scoping.md`. Stack reframed to Spring Boot + JPA/Hibernate.

---

## 1. Elevator pitch

"I built the backend for Uber's Financial Risk Management quarterly scoping tool — the system that decides which financial statement line items get audited each quarter. It replaced a Google Sheets workflow with a Spring Boot + MySQL service used by FRM managers; the output is the audit work paper PwC reviews. Get scoping wrong and you either over-pay PwC or under-audit and risk an audit finding. We cut quarterly cycle time by ~70%, served 36 REST endpoints across 8 screens, and ETL'd 19M+ GL rows/quarter down to ~300K aggregated rows."

## 2. Architecture (Java telling)

```
React SPA
    │ REST
    ▼
frm-scoping-service          frm-collaboration-service
(Spring Boot, ~20 APIs)      (Spring Boot, ~16 APIs:
 controllers → services →      comments, threads, Slack)
 Spring Data JPA repos)
    │                            │
    ▼                            ▼
MySQL (8-table schema)       MySQL
    ▲
    │ quarterly ETL (HFM extract → transform → LAG QoQ → 10-Q reconcile)
Oracle HFM  ~19M raw → ~300K aggregated
```

**Layering (strict):** `controller` → `service` → `repository` (Spring Data JPA) → entities. Controllers never touch repositories; services never throw raw HTTP exceptions without an `@ControllerAdvice`; repositories never compute business rules.

**DI:** constructor injection (preferred over field `@Autowired`). Config via `@ConfigurationProperties`.

## 3. Hibernate / JPA migration bullet

Resume: *"Refactored brittle raw SQL data access to Spring Data JPA / Hibernate, fixing a latent column-aliasing bug and raising changed-module test coverage to 100%."*

- **Before:** hand-written SQL with brittle column aliases; rename/refactor bugs invisible until runtime (same failure mode as the live SQLAlchemy migration — do not invent a JDBC-only history).
- **After:** typed entities + `JpaRepository` / custom `@Query`; JPQL/Criteria for dynamic filters; the aliasing bug surfaced during mapping and was fixed with explicit `@Column` names.
- **Coverage:** JUnit + Mockito on services; `@DataJpaTest` for repositories; changed-module gate in CI to 100%.

## 4. Redis

24h-TTL cache for expensive financial read paths (materiality / summary screens). Stampede protection: jittered TTLs + single-flight style lock key.

## 5. Q&A

- **"Why JPA over jOOQ/MyBatis?"** Refactor safety and team velocity on a CRUD-heavy domain; complex ETL stayed as set-based SQL / batch scripts where ORM would hurt.
- **"N+1?"** `JOIN FETCH` / `@EntityGraph` / batch size; never leave lazy loads in hot request paths.
- **"Transactions?"** `@Transactional` on service methods; read-only for reporting screens; watch for self-invocation bypassing proxies.
- **"Bean Validation?"** `@Valid` on request DTOs at the controller boundary — cheapest correctness for malformed scoping payloads.
