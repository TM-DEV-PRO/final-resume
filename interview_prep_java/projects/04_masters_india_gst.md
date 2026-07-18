# Masters India — GST & E-Invoicing (Java / Spring track)

**Role:** Software Development Engineer 2 · December 2022 – June 2024 · Noida  
**Resume tech:** Java, Spring Boot, Hibernate, PostgreSQL, Redis, Spring Batch, Docker, ELK, New Relic, AWS

---

## 1. Elevator pitch

"Masters India is a GST Suvidha Provider — enterprises file GST returns and generate e-invoices through our APIs. I led the migration of core compliance APIs from a PHP (Laravel) monolith to Java Spring Boot microservices: p95 latency 1.2s → 300ms, scaled to 1M+ daily transactions for 2,500+ enterprise clients. Bulk e-invoicing — 100K+ transactions per import — was a chief revenue path."

## 2. Migration story (strangler)

**Why:** Laravel/PHP-FPM blocked workers on government IRP round-trips (500ms–3s). Peak GSTR deadline windows exhausted pools.

**Approach:**
1. Carve bounded contexts: e-invoice, e-way bill, returns, reconciliation, dashboard.
2. New Spring Boot services behind the same gateway; per-endpoint cutover with shadow traffic.
3. Move IRP round-trips off the request thread — async workers / Spring Batch for bulk and flaky portal calls (same product need as the live FastAPI + Celery path; do **not** claim WebFlux unless you can defend Reactor end-to-end).
4. **Spring Batch** (+ Redis) for bulk imports, retries, report generation.
5. Data stayed on PostgreSQL initially (shared DB → split hot tables later).

**Results:** p95 1.2s → 300ms; 1M+ txn/day; triage ~70% faster with ELK + New Relic; coverage 35% → 82%.

## 3. Bulk processing (100K+/import)

- Upload → validate → chunk → Spring Batch steps / async workers.
- Idempotency keys: `clientId + fileHash + batchIndex` — retries never double-file.
- Set-based SQL (`INSERT ... ON CONFLICT`) over per-row saves.
- Token-bucket rate limit per GSTIN + circuit breaker to IRP; DLQ for operator replay.

## 4. Observability & quality

- Structured JSON logs + correlation IDs through Batch/async jobs → ELK.
- New Relic APM: error rate, p95, DB time.
- JUnit + Mockito + Testcontainers; CI gate on coverage.

## 5. Q&A

- **"Why Spring Boot not WebFlux?"** MVC + async/Batch covers the IRP wait pattern without a full reactive rewrite; WebFlux only pays off if the whole stack (DB drivers included) is non-blocking.
- **"Spring Batch vs Kafka?"** Task semantics (retries, chunking, job repository) fit imports; Kafka when multiple consumers need a replayable log.
- **"Biggest incident?"** IRP flakiness at deadline peak → retry-with-jitter + circuit breaker + client-visible degraded mode.
- **"What differently?"** Split shared DB earlier; idempotency keys from day one.
