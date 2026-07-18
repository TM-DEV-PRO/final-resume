# Behavioral / STAR stories — Java track

Outcomes, leadership signals, and story structure are **identical** to `interview_prep/07_behavioral_star_stories.md`. Use that file as the canonical bank (10 stories). Below are **stack wording swaps** so you don't say FastAPI/Gin/pytest when interviewing on the Java resume.

| Story | Keep as-is | Swap in conversation |
|---|---|---|
| 1. ClickHouse verdict | Decision process, PoC gates | Implementation plane: Spring Boot services + ClickHouse client |
| 2. BQ→CH ingestion | Freshness, REPLACE PARTITION | Scheduler/job in Java (Batch/cron service) if asked "who runs the job" |
| 3. Malformed-plan validator | Product failure mode | Bean Validation / schema checks before agent commit |
| 4. Clustering copilot | HLR behavior, <1 h | Python FastAPI/LangGraph agent microservice |
| 5. Constants-refactor regression | Owning mistakes | JUnit gate; "tests that would have caught it" |
| 6. Coverage-gap fix | Test where code lives | JUnit/Mockito; CI coverage on changed modules |
| 7. ORM-vs-repository | Disagree & commit | Hibernate/JPA repository boundaries vs raw SQL |
| 8. Masters India migration | Deadline pressure, p95 | Spring Boot strangler; Spring Batch bulk path |
| 9. Anti-bot arms race | Persistence | Same; Selenium + proxy pools |
| 10. Double-filing / idempotency | Earn trust | Idempotency keys in Batch writers / DB constraints |

**Rapid-fire quality answers (Java wording):**

- **CI gating:** pipeline blocks merge if JUnit fails or changed-module coverage drops; Testcontainers for DB-backed tests.
- **Testability:** constructor-injected ports (repositories, clients); pure domain functions for tax/dedup rules; DTO validation at the boundary.
- **Idempotent retries:** `importId + chunkIndex + contentHash` recognized on replay — same as main track.
- **Observability:** Actuator + Micrometer metrics, ELK correlation IDs, New Relic APM — Masters India triage 70% story unchanged.
