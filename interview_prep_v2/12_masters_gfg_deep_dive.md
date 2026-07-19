# Masters India and GeeksforGeeks Deep Dive (v2 resume defense)

Every number here traces to `GROUND_TRUTH.md`. Tags: HISTORICAL (from past resume claims, own experience), ESTIMATED (derived, say "estimated").

---

## Masters India (Dec 2022 to Jun 2024), SDE 2

### What the product is

GST compliance and e-invoicing SaaS for Indian enterprises. Clients push invoices through our APIs, we validate, register them with the government Invoice Registration Portal (IRP), and return signed e-invoices with IRN and QR codes. Bulk imports, reconciliation against GST returns, and audit trails on top. Compliance means correctness and traceability matter more than raw speed, but filing deadline days bring heavy spikes.

### Bullet 1. Owned PHP monolith to FastAPI microservices strangler, mentored 2 engineers, p95 1.2s to 300ms, 1,500+ clients

**Resume XYZ:** Owned the strangler migration (X) by cutting over services behind a gateway with canaries and mentoring 2 engineers (Y), cutting p95 from 1.2s to 300ms for 1,500+ clients (Z).

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

### Bullet 2. 100K per import, 1M+ daily transactions, 700 to 4,000 RPM (~12 TPS / ~67 RPS)

**Resume XYZ:** Scaled bulk e-invoicing with async Kafka and PostgreSQL quarter sharding (X/Y) to 100K+ per import and 1M+ daily (~12 TPS avg, 100+ peak) and 700 to 4,000 requests/min (~67 RPS) (Z).

- Bulk import path: file lands in S3, a Celery chain validates in chunks (schema, GSTIN checks, duplicates via idempotency keys), then batch-registers with the IRP with bounded concurrency and exponential backoff, streaming progress back to the client dashboard.
- 1M+ daily transactions averages about 12 TPS (ESTIMATED arithmetic, 1M / 86,400). Filing deadline peaks are the real sizing problem, 100+ TPS bursts (ESTIMATED, roughly 8 to 10x average). Queue-based load leveling is what absorbed them.
- Sustained throughput went from 700 to 4,000 requests per minute (HISTORICAL) after the async rewrite plus worker autoscaling on queue depth.

### Bullet 3. Fault tolerant bulk paths (idempotency, retries, DLQ) + Redis -30% reads

**Resume XYZ:** Built fault tolerant bulk paths with idempotency keys, retries, and DLQ replay (X/Y), and Redis caching that cut redundant DB reads 30% (Z). Audit-log churn -15% remains HISTORICAL prep depth, not required on the hardened one-pager.

- Idempotency: `client + fileHash + batchIndex` (and client-supplied invoice references) so retries never double-register with IRP.
- Retries: exponential backoff with jitter and bounded concurrency against the flaky government portal.
- DLQ / dead-letter state: poison batches park for operator replay instead of blocking the whole import.
- Circuit breaker (verbal): open when IRP error rate spikes; serve degraded status to clients.
- Cache-aside: miss to read DB to SET with TTL jitter; SETNX singleflight against stampedes. Hot keys: client config, rate/tax masters, session and auth lookups, GSTIN masters.
- Invalidation on write for config data; TTL-only for slowly changing masters.
- Caching mostly helped p50 and read-heavy endpoints; async IO and query fixes drove the p95 tail.

### Bullet 4. ELK + New Relic on-call alerting, triage 70 percent faster, coverage 35 to 82, 98 percent deploy success

**Resume XYZ:** Established ELK and New Relic on-call alerting (X/Y), cutting incident triage 70% and raising coverage 35% to 82% with 98% deployment success (Z).

- Before: SSH into boxes and grep. After: structured JSON logs with request IDs shipped to ELK, New Relic APM traces, alert rules on error rate and latency SLOs.
- Triage went from about 30 minutes to under 10 (baseline ESTIMATED, the 70 percent cut is HISTORICAL). The win is correlation: one request ID follows a transaction across services and workers.
- Honesty: claim on-call **alerting** and faster triage. Do not invent a formal pager rotation or SEV commander title without proof.
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
- SMTP 50% faster? Keep the SMTP connection open and reuse it across sends (1yr/2.5yr resume). TCP+TLS handshake is often 100-400ms per new connection; amortizing that across a batch cuts wall-clock send time roughly in half for reminder and promo traffic.

## Mock interview: hardest questions with answers

### Masters India

**Interviewer:** You were on AWS. Why Kafka instead of RabbitMQ or SQS for e-invoicing?

**Candidate:** We needed three things together: per-client ordering, durable replay for compliance, and independent consumer groups. Partition key was client GSTIN (or GSTIN plus document type), so invoice submit, IRN callback, and webhook fan-out for one taxpayer stayed ordered on one partition. Kafka's log lets us reset offsets and reprocess a bad consumer window after a parser bug; SQS deletes on ack and does not give cheap multi-consumer replay, and SQS FIFO caps throughput per message group. RabbitMQ could have worked at our scale for task dispatch; I am honest about that. We still picked Kafka because (1) replay and audit reprocessing were first-class for GST disputes, (2) multiple groups could read the same topic (IRP workers, audit projector, metrics) without fanout-exchange plumbing, and (3) the team already had AsyncIOKafka in the FastAPI stack (2.5yr resume). Ops cost of Kafka was the trade-off; correctness and replay won.

**Interviewer:** Derive TPS and RPS from your resume numbers. Do they even hang together?

**Candidate:** 1M+ daily transactions is 1,000,000 / 86,400 ≈ 11.6 TPS average, call it ~12 TPS (ESTIMATED). Filing deadline spikes are the sizing problem; we sized for 100+ TPS peak, roughly 8 to 10x average (ESTIMATED). Sustained API throughput went from 700 to 4,000 requests per minute (HISTORICAL), which is 700/60 ≈ 12 RPS to 4,000/60 ≈ 67 RPS. Those are complementary: RPM is gateway and service capacity under load tests and peaks; daily transactions are IRP-registered documents. p95 latency moved from about 1.2s (resumes also say 1000-1200ms) to about 300ms (300-400ms band) for 1,500+ clients.

**Interviewer:** What actually drove p95 from 1.2s to 300ms? Caching alone cannot do that.

**Candidate:** Caching helped p50 and read-heavy endpoints; the p95 tail was async IO and removing PHP synchronous bottlenecks. IRP calls no longer blocked a PHP-FPM worker for the full round trip; FastAPI plus workers returned 202 or awaited without holding a process hostage. Connection pooling replaced per-request connect storms. We killed N+1 list queries and added composite indexes on (client_id, invoice_date). Redis cut redundant DB reads about 30% (HISTORICAL), which shortened the middle of the distribution. Net: async + pooling + query fixes moved the tail; cache moved the body.

**Interviewer:** Cache-aside specifics: keys, TTLs, invalidation, thundering herd. Make the 30% read cut plausible.

**Candidate:** Pattern was classic cache-aside: miss → read DB → SET with TTL. Hot keys: e-invoice IRP auth tokens (short TTL, under the IRP token lifetime, typically a few hours with safety margin), client config and feature flags, GSTIN master lookups, and tax-rate masters. Config and GSTIN keys invalidated on write (DELETE inside the update path) so admins never served stale credentials. Masters used TTL-only with jitter so expiries did not align. Thundering herd: TTL jitter plus a SETNX lock so one worker recomputes while others wait or serve slightly stale. 30% fewer redundant reads is plausible because the same client config and GSTIN validation ran on every invoice in a bulk import; caching those across 100K-row imports removes a huge duplicate read fan-out.

**Interviewer:** Quarter-based sharding: why shard GST data by financial quarter instead of plain partitioning?

**Candidate:** Indian GST reporting and returns are quarter-scoped and filing-deadline driven. Writes concentrate in the current quarter; older quarters are mostly read for reconciliation and audits. Separate quarter tables (or quarter schemas) let us prune or archive cold quarters without touching the hot write set, and keep indexes smaller where inserts land. Trade-off versus native RANGE partitioning: we owned routing in application code (AsyncMotorIO / SQL layer picked the quarter), which is more moving parts than DB-native partitions, but gave us explicit drop/archive of an entire quarter and clearer operational runbooks. Wrong-quarter writes are the footgun; we derived quarter from invoice date at the API boundary and rejected mismatches.

**Interviewer:** Sketch the IRP e-invoicing path and where Kafka sits.

**Candidate:** Client creates the invoice in their ERP, posts JSON to our API, we validate schema and GSTIN, then report to a government Invoice Registration Portal. IRP returns a signed e-invoice with IRN and QR; that is what makes a B2B GST invoice valid. Kafka carried async stages: accepted import chunks, IRP submit jobs, signed-response persistence to Mongo snapshots, and client webhooks. Idempotency keys plus unique client references stopped double registration, which is not recoverable with the government. Bulk path: file to object storage, chunk validate, bounded concurrency to IRP, progress on the dashboard. 100K+ transactions per import and 1M+ daily (HISTORICAL).

**Interviewer:** You mentored 2 engineers on a monolith-to-microservices migration. What did "led" mean day to day?

**Candidate:** Strangler pattern behind the gateway, not a big bang. I owned conventions: router / service / repository, Pydantic at the boundary, retry and idempotency helpers. Two juniors each extracted a service; I reviewed early PRs closely and paired on the first canary cutover (Nginx percentage route, watch errors and latency, ramp or roll back by config). Shared DB during traffic cutover avoided dual writes; table splits came after. Mentorship claim is user-confirmed: 2 engineers at Masters India.

**Interviewer:** ELK + New Relic cut triage 70%. Prove that is not vanity metrics.

**Candidate:** Before: SSH and grep across boxes with no request correlation. After: structured JSON logs with request IDs into Elasticsearch/Kibana, New Relic APM traces, alerts on error rate and latency. Triage from roughly 30 minutes to under 10 is ESTIMATED baseline math behind a HISTORICAL 70% cut. The real win is one request ID across API, Kafka consumer, and IRP worker. Coverage 35% to 82% with pytest as a CI gate on money paths; deployment success 98% (HISTORICAL).

### GeeksforGeeks

**Interviewer:** Doubt support at 10K+ daily queries. Design unread counts without melting MySQL.

**Candidate:** Scale is user-standardized at 10K+ daily interactions (older resumes said 1000+ doubts/day; 4yr said 100K; we standardize 10K+). Average is well under 1 RPS with contest-day spikes maybe 10x (ESTIMATED). Unread counts lived behind a REST API: per-user counters in Redis for the badge path, durable rows in MySQL for threads and messages. Increment on new reply, decrement or clear on read receipts. Periodic reconcile from MySQL fixed drift. PHP to Django migration bought transactions, validation, and cleaner read/write separation for reliability.

**Interviewer:** Voting API idempotency and hot rows. How did MySQL, Redis, MongoDB, and Elasticsearch split?

**Candidate:** Vote table had a unique (user_id, content_id) constraint so double-submit is idempotent at the DB. Display counters sat in Redis and reconciled asynchronously to MySQL to avoid hot-row contention on popular doubts. MySQL remained source of truth for relational threads and permissions. Mongo held flexible payloads where the doubt body or attachments varied. Elasticsearch powered search across doubts and content. Pinning was per-context ordering columns, not a free-for-all sort. Premium lift 15 to 20% is HISTORICAL relative attribution by growth.

**Interviewer:** Cron pipelines for video processing claimed +70% ops efficiency. How do you keep crons reliable?

**Candidate:** Jobs covered video processing handoffs, automated reminders, payment processing, and cloud recording deletion. Reliability pattern: lock or DB advisory lease so two cron hosts do not double-run, idempotent job keys, structured success/fail logs, and dead-letter or retry for partial batches. The 70% efficiency figure is HISTORICAL time saved on those manual ops workflows. Course sales +30% is business attribution on the influencer dashboard; I own the engineering, attribute causality carefully.

**Interviewer:** You also cut email send time 50% with SMTP changes. Is that real?

**Candidate:** Yes, on the 1yr and 2.5yr resumes: keep the SMTP connection open and reuse it across sends instead of TCP+TLS handshaking every message. Handshake overhead is often 100-400ms per new connection; pooling amortizes it across reminder and promo batches. That matches what large mail senders document with SMTP connection reuse. It is a GFG optimization detail, not a Masters India claim.

## Confidence audit

| Resume bullet | Rating | Fallback wording if pressed |
|---|---|---|
| Owned FastAPI strangler, mentored 2, p95 1.2s to 300ms, 1,500+ clients | SOLID | Use 1000-1200ms to 300-400ms band if they cite older resumes; never say 2,500+ clients (dropped). |
| 100K+/import, 1M+ daily, async Kafka, quarter sharding, 700 to 4,000 req/min | SOLID on throughput; NEEDS CARE on peak TPS | Say ~12 TPS avg and 100+ TPS peak as ESTIMATED. Kafka justification: ordering, replay, consumer groups; admit RabbitMQ could work at that scale. |
| Fault tolerant bulk paths (idempotency, retries, DLQ) + Redis -30% reads | SOLID on pattern; NEEDS CARE on circuit-breaker wording | Defend idempotency key shape and DLQ replay. Circuit breaker is verbal prep, not a measured resume metric. Audit churn -15% is prep-only now. |
| ELK + New Relic on-call alerting, triage -70%; coverage 35 to 82; 98% deploy success | SOLID on coverage/deploy; NEEDS CARE on triage baseline | Claim alerting, not unproven pager ownership. Triage baseline ~30 min to <10 min is ESTIMATED behind HISTORICAL 70%. |
| GFG PHP to Django, 10K+ daily queries | SOLID (standardized) | Say "order of ten thousand daily interactions"; do not say 100K. |
| Voting/pinning, premium +15-20% | NEEDS CARE | "Relative lift attributed by growth; engineering owned APIs and reliability." |
| Influencer dashboard + cron, course sales +30%, ops +70% | NEEDS CARE | Own engineering; attribute sales/efficiency as HISTORICAL business metrics. |
