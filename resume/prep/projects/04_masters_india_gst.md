# Masters India — GST Compliance & E-Invoicing SaaS Platform

**Role:** Software Development Engineer 2 · December 2022 – June 2024 · Noida
**Resume tech line:** Python, FastAPI, PostgreSQL, Redis, Celery, Docker, ELK, New Relic, AWS

---

## 1. Elevator pitch

"Masters India is a GST Suvidha Provider — enterprises file GST returns and generate e-invoices/e-way bills through our APIs. I led the migration of the core compliance APIs from a legacy PHP (Laravel) monolith to async Python (FastAPI) microservices: p95 latency went from 1.2 s to 300 ms, and the platform scaled to 1M+ daily transactions for 2,500+ enterprise clients. The bulk e-invoicing path — 100K+ transactions per import — was the company's chief revenue driver."

## 2. The migration story (your strongest system-design narrative here)

**Why migrate at all:** the Laravel monolith was synchronous per-request PHP-FPM — every government-portal call (NIC/IRP e-invoice registration) blocked a worker for its full round-trip (500ms–3s). Peak filing windows (monthly GSTR deadlines) exhausted worker pools; latency and error rates spiked exactly when clients needed the system most.

**Approach — strangler pattern, not big-bang:**
1. Carved bounded contexts out of the monolith: e-invoice generation, e-way bill, returns filing, reconciliation, client dashboard.
2. New FastAPI services fronted by the same gateway; routes cut over per-endpoint with shadow traffic first.
3. Async I/O (httpx + asyncio) for government-portal calls — a worker no longer blocks during the IRP round-trip; concurrency comes from the event loop, not from more PHP-FPM processes.
4. Celery + Redis for the heavy async work: bulk imports, scheduled retries against flaky government endpoints, report generation.
5. Data stayed in place (PostgreSQL) — services shared the DB initially, then split hot tables; avoided a risky data migration during cutover.

**Results:** p95 1.2 s → 300 ms (75%); additional 40% backend-routine latency cut from query optimization + Redis caching; 1M+ transactions/day; 30% infra-load reduction.

## 3. Bulk processing at 100K+ transactions/import

- Chunked ingestion: file upload → validate + split into batches → Celery fan-out → per-batch idempotency keys (client_id + file hash + batch index) so retries never double-file an invoice.
- Set-based SQL writes (multi-row INSERT ... ON CONFLICT) instead of per-row ORM saves — the single biggest throughput lever.
- Rate-limit-aware outbound queue to the government IRP (token bucket per GSTIN) with circuit breaker; failed batches park in a dead-letter state with operator replay.
- Progress tracking per batch surfaced to the client dashboard (reduced "where is my import" support tickets 35%).

## 4. Security & compliance (financial data)

Encryption at rest + TLS in transit; RBAC with JWT (short-lived access + refresh); audit logs on every mutating call (who/what/when/before-after); IP allowlisting for enterprise clients; secrets in AWS KMS. Framing: "compliance data (GSTINs, invoices, turnover) — we treated auditability as a feature, not an afterthought."

## 5. Observability

Centralized ELK (structured JSON logs, correlation IDs propagated through Celery) + New Relic APM (transaction traces, DB time breakdown). Incident triage accelerated ~70%: before, engineers grepped per-box logs; after, one Kibana query by correlation ID. Test coverage 35% → 82% (pytest, factory fixtures, contract tests on government-API adapters) → 98% deployment success.

## 6. Q&A bank

- **"Why FastAPI over Django/Flask?"** Async-native (the workload is outbound-I/O-bound), Pydantic validation at the boundary (malformed invoice payloads are the #1 client error class), OpenAPI docs for enterprise client integration teams for free.
- **"How did you cut over without downtime?"** Per-endpoint strangler cutover behind the gateway; shadow traffic comparison on read paths; bulk/async paths moved first (lowest user-facing risk), interactive filing last.
- **"Biggest incident?"** Government IRP flakiness during deadline peaks — fixed with retry-with-jitter + circuit breaker + client-visible degraded-mode status instead of silent failures.
- **"Why Celery not Kafka?"** Task semantics (retries, rate limits, scheduled jobs), not stream semantics; team already ran Redis; volumes fit comfortably. I'd reach for Kafka when multiple independent consumers need replayable history.
- **"What would you do differently?"** Split the shared database earlier — schema coupling slowed independent deploys near the end; and introduce idempotency keys from day one instead of retrofitting them after a double-filing near-miss.
