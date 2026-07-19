# Masters India and GeeksforGeeks Deep Dive (v2 resume defense)

Every number here traces to `GROUND_TRUTH.md`. Tags: HISTORICAL (from past resume claims, own experience), ESTIMATED (derived, say "estimated").

---

## Masters India (Dec 2022 to Jun 2024), SDE 2

### What the product is

GST compliance and e-invoicing SaaS for Indian enterprises. Clients push invoices through our APIs, we validate, register them with the government Invoice Registration Portal (IRP), and return signed e-invoices with IRN and QR codes. Bulk imports, reconciliation against GST returns, and audit trails on top. Compliance means correctness and traceability matter more than raw speed, but filing deadline days bring heavy spikes.

### Bullet 1. PHP monolith to FastAPI microservices, mentored 2 engineers, p95 1.2s to 300ms, 1,500+ clients

**Why migrate.** The Laravel monolith was synchronous, one slow IRP callout blocked a worker per request, deployments were all-or-nothing, and scaling meant scaling everything. Filing deadline spikes caused queue pileups and timeouts.

**How we did it (this is the migration playbook to narrate).**

1. Strangler pattern, not big bang. New FastAPI services were put behind the existing gateway one domain at a time (auth, e-invoice submit, bulk import, reconciliation). The monolith kept serving whatever was not yet migrated.
2. Route-level cutover with fallback. Nginx routed a small percentage of traffic per endpoint to the new service first (canary), watching error rate and latency dashboards, then ramped to 100. Rollback was a config change, not a deploy.
3. Shared database first, then split. Services initially read the same MySQL/PostgreSQL data to avoid a risky data migration during the traffic cutover. Only after traffic was fully moved did we carve out service-owned tables.
4. Contract tests pinned the old PHP responses. We recorded monolith responses for the top endpoints and asserted the FastAPI replacements matched field for field, so clients never saw a payload change.
5. Async by default. IRP calls, PDF generation, webhooks and email went through Celery workers with retries and idempotency keys so request threads never blocked on third parties.

**Where the latency win came from (1.2s to 300ms p95, HISTORICAL).**
- Async IO for IRP and internal fan-out calls instead of blocking PHP workers.
- Redis caching of hot reads (client config, tax rates, auth context), which also cut redundant DB reads about 30 percent (HISTORICAL).
- Query fixes surfaced during the rewrite: missing composite indexes on (client_id, invoice_date), N+1 removal, pagination on list endpoints.
- Connection pooling per service instead of PHP-FPM per-request connections.

**Mentoring 2 engineers.** Two juniors owned individual service extractions. I set the conventions (router, service, repository layering, Pydantic schemas at the boundary, retry and idempotency helpers), reviewed every PR for the first months, and paired on the first canary cutover. Both were independently shipping services by the end.

### Bullet 2. 100K per import, 1M+ daily transactions, 700 to 4,000 RPM

- Bulk import path: file lands in S3, a Celery chain validates in chunks (schema, GSTIN checks, duplicates via idempotency keys), then batch-registers with the IRP with bounded concurrency and exponential backoff, streaming progress back to the client dashboard.
- 1M+ daily transactions averages about 12 TPS (ESTIMATED arithmetic, 1M / 86,400). Filing deadline peaks are the real sizing problem, 100+ TPS bursts (ESTIMATED, roughly 8 to 10x average). Queue-based load leveling is what absorbed them.
- Sustained throughput went from 700 to 4,000 requests per minute (HISTORICAL) after the async rewrite plus worker autoscaling on queue depth.
- Idempotency: every invoice carries a client-supplied reference; a unique constraint plus an idempotency key check makes retries safe, since double-registering an invoice with the government is not recoverable.

### Bullet 3. Redis caching (30 percent fewer redundant reads) and audit logs (15 percent churn cut)

- Cache-aside pattern. On miss, read DB, set with TTL. TTLs carried jitter to avoid synchronized expiry stampedes. Hot keys: client config, rate/tax masters, session and auth lookups.
- Invalidation on write for config data (delete key inside the update transaction boundary), TTL-only for slowly changing masters.
- What p95 gains came from caching vs async: caching mostly helped p50 and read-heavy endpoints; async IO and query fixes drove the p95 tail.
- Audit logging (HISTORICAL): immutable event trail per invoice and per user action, exposed to enterprise clients. Compliance teams could self-serve answers during disputes and audits, which was cited in renewals; churn dropped about 15 percent.

### Bullet 4. ELK + New Relic, triage 70 percent faster, coverage 35 to 82, 98 percent deploy success

- Before: SSH into boxes and grep. After: structured JSON logs with request IDs shipped to ELK, New Relic APM traces, alert rules on error rate and latency SLOs.
- Triage went from about 30 minutes to under 10 (baseline ESTIMATED, the 70 percent cut is HISTORICAL). The win is correlation: one request ID follows a transaction across services and workers.
- Coverage 35 to 82 percent with pytest, enforced as a CI gate. Focus was on money paths first (registration, reconciliation, imports). Deployment success rate reached 98 percent (HISTORICAL).

### Rapid fire

- Why FastAPI over Django or Flask? Async-native for IRP fan-out, Pydantic validation at the boundary, OpenAPI for enterprise client docs, small per-service footprint.
- Why strangler over rewrite? Compliance product, zero tolerance for a broken filing day. Strangler let us cut over per endpoint with instant rollback.
- Dual writes during migration? Avoided. We kept a shared database during traffic cutover precisely so we never had two sources of truth; the data split came after.
- What broke? Early canary showed timeout mismatches (PHP had 60s, we set 10s); some IRP calls legitimately took longer, so we moved them fully async and returned 202 with polling.
- How do you protect against cache stampede? TTL jitter plus a simple lock (setnx) so one worker recomputes and the rest wait or serve stale.
- Why both MongoDB and Elasticsearch on the tech line? Mongo held flexible invoice payload snapshots and vendor responses; Elasticsearch powered invoice search and the ELK stack.

---

## GeeksforGeeks (Aug 2021 to Nov 2022), SDE

### Bullet 1. PHP to Django migration, 10,000+ daily queries

- The doubt/query platform (users post questions on articles and courses) ran on legacy PHP. We rebuilt it in Django with DRF, migrating incrementally page by page behind the same URLs.
- 10,000+ daily queries (user-standardized scale; say "order of ten thousand daily interactions" if pressed, it averages well under 1 RPS with contest-day spikes roughly 10x, ESTIMATED).
- Reliability wins came from ORM-managed transactions, request validation, and separating read views from write endpoints, plus staging and code review discipline the PHP stack lacked.

### Bullet 2. Voting and pinning APIs, premium subscriptions up 15 to 20 percent

- Designed data models for votes (unique user-content constraint, denormalized counters updated atomically) and pinned content (per-context ordering).
- Vote counts were cached in Redis and reconciled to MySQL asynchronously, avoiding hot-row contention on popular posts.
- The features gated some interactions behind premium, lifting premium subscription sales 15 to 20 percent relative (HISTORICAL; say "relative lift attributed by the growth team").

### Bullet 3. Influencer dashboard and cron pipelines, course sales up 30 percent, ops efficiency up 70 percent

- Dashboard aggregated video and course analytics for influencer partners with near-real-time counters (Redis) and daily rollups (cron).
- Cron pipelines handled video processing handoffs, automated reminders, and cloud recording cleanup, removing manual steps the ops team did by hand (the 70 percent efficiency figure is HISTORICAL, framed as time saved on those workflows).
- Course sales rose 30 percent (HISTORICAL, attribution by the business team; own the engineering, attribute the causality).

### Rapid fire

- Why Django here but FastAPI at Masters India? 2021 CMS-style product with admin, auth, ORM batteries included; Masters India needed async IO for third-party government APIs.
- Hot-row problem on votes? Unique constraint for correctness, Redis counter for display, periodic reconciliation for truth.
- What would you change today? Move vote events onto a queue and make counters event-sourced; add idempotency on the reminder cron.
