# Masters India — GST & E-Invoicing (Java / Spring track)

**Role:** Software Development Engineer 2 · December 2022 – June 2024 · Noida  
**Resume tech:** Java, Spring Boot, Hibernate, Kafka, PostgreSQL, MongoDB, Redis, Elasticsearch, Spring Batch, Docker, ELK, New Relic, AWS

> Same facts as `../interview_prep_v2/12_masters_gfg_deep_dive.md`. Live path was Python/FastAPI + Celery; Java track is a positioning variant.

---

## 1. Elevator pitch

"Masters India is a GST Suvidha Provider. I owned the strangler migration of core compliance APIs from a PHP (Laravel) monolith to Spring Boot microservices, mentored 2 engineers, and cut p95 latency from 1.2s to 300ms for 1,500+ enterprise clients. We scaled bulk e-invoicing to 100K+ transactions per import and 1M+ daily (~12 TPS avg, 100+ peak) via async Kafka and PostgreSQL quarter sharding, lifting throughput from 700 to 4,000 requests/min (~67 RPS). I built fault tolerant bulk paths with idempotency keys, retries, and DLQ replay, plus Redis caching that cut redundant reads 30%, and established ELK + New Relic on-call alerting that cut incident triage about 70%."

## 2. Migration story (strangler)

**Why:** Laravel/PHP-FPM blocked workers on government IRP round-trips. Peak GSTR deadline windows exhausted pools.

**Approach:**
1. Carve bounded contexts: e-invoice, e-way bill, returns, reconciliation, dashboard.
2. New Spring Boot services behind the same gateway; per-endpoint canary cutover.
3. Move IRP round-trips off the request thread — async workers / Spring Batch for bulk and flaky portal calls (same product need as FastAPI + Celery; do **not** claim WebFlux unless you can defend Reactor end-to-end).
4. Shared database first, then split hot tables.
5. Contract tests against recorded PHP responses.

**Results:** p95 1.2s → 300ms; 1M+ txn/day; triage ~70% faster with ELK + New Relic; coverage 35% → 82%; 98% deploy success.

## 3. Fault tolerance + scale (resume-hardened)

- Idempotency keys: `clientId + fileHash + batchIndex` — retries never double-file with IRP.
- Retries with exponential backoff + jitter; bounded concurrency.
- DLQ / dead-letter state for operator replay.
- Kafka for ordered replayable compliance events; PostgreSQL quarter sharding for filing-period locality.
- Redis cache-aside with TTL jitter; -30% redundant DB reads (HISTORICAL).

## 4. Observability & quality

- Structured JSON logs + correlation IDs through Batch/async jobs → ELK.
- New Relic APM: error rate, p95, DB time.
- On-call **alerting** (not an unproven formal pager-commander claim).
- JUnit + Mockito; CI gate on coverage 35% → 82%.

## 5. Q&A

- **"Why Spring Boot not WebFlux?"** MVC + async/Batch covers the IRP wait pattern without a full reactive rewrite.
- **"Spring Batch vs Kafka?"** Batch for chunked import job semantics; Kafka when multiple consumers need a replayable log.
- **"Biggest incident class?"** IRP flakiness at deadline peak → retry-with-jitter + DLQ + client-visible degraded mode.
- **"Client count?"** Use **1,500+**, never 2,500+.
