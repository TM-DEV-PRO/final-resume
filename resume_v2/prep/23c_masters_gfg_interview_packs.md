> Canonical interviewer packs for current resume_v2 Masters + GFG bullets. 1500+ clients; no ~TPS on PDF. Synced Jul 2026.

# Masters India — Interview Pack

**Role:** SDE 2 · Dec 2022 – Jun 2024 · GST Compliance & E-Invoicing Platform  
**Consensus numbers:** 1,500+ clients · p95 1.2s → 300ms · 700 → 4,000 req/min · 1M+ IRP submissions/day · 100K+/import · Redis −30% reads · triage −70% · coverage 35% → 82% · 98% deploy success  
**Framing:** Event-driven Kafka platform for bulk IRP registration — not a CRUD monolith rewrite story.

---

## 1. 30s / 2min explain

**30 seconds**  
At Masters India I owned the GST e-invoicing path for 1,500+ enterprise clients. We migrated a PHP Laravel monolith to FastAPI microservices and built a bulk IRP pipeline on Kafka and PostgreSQL tables split by tax quarter. That cut p95 from 1.2s to 300ms, lifted sustained throughput from 700 to 4,000 requests/min, and reliably processed 1M+ IRP submissions/day with 100K+ per import — with idempotency keys, retries, and a dead-letter queue so we never double-register with the government.

**2 minutes**  
GST e-invoicing is a compliance product: clients push invoices, we validate, register with the government Invoice Registration Portal, and return signed IRN + QR. Filing-deadline days spike load; correctness beats raw speed, but timeouts still lose clients.

The Laravel monolith was synchronous — one slow IRP call blocked a PHP-FPM worker, deploys were all-or-nothing, and scaling meant scaling everything. We cut over FastAPI services behind the gateway endpoint-by-endpoint with canaries (interviewers may call this a strangler migration), shared DB during traffic move (no dual writes), contract tests against old PHP payloads, then table ownership split later. Mentored 2 engineers on the extraction conventions.

The bulk path is where Kafka earns its keep. Import file → object storage → chunk validate → Kafka topics for IRP submit / signed-response persistence / webhook fan-out → PostgreSQL quarter tables for hot-quarter writes. Partition key by client GSTIN for per-taxpayer ordering. Idempotency keys (`client + fileHash + batchIndex`), exponential backoff, and DLQ replay for poison batches. Redis caching cut redundant DB reads ~30%. Ops: ELK + New Relic request-ID correlation cut triage ~70%; pytest coverage 35% → 82%; 98% deployment success.

If they ask “why Kafka?” — ordering, durable replay for GST disputes, and independent consumer groups on the same log. Admit RabbitMQ could dispatch work at our scale; replay and multi-consumer audit won.

---

## 2. Architecture

```
Client ERP / Dashboard
        │
   API Gateway (Nginx canary % → FastAPI | fallback PHP)
        │
   FastAPI services (auth, e-invoice submit, bulk import, recon)
        │
   ┌────┴────┬──────────────┬─────────────┐
   │         │              │             │
PostgreSQL  Redis      Kafka topics    MongoDB
(quarter    (config,   (import chunks, (invoice payload
 shards)     GSTIN,     IRP jobs,       + IRP response
             tokens)    webhooks,       snapshots)
                        audit projector)
        │
   Celery / consumers ──bounded concurrency──► IRP (gov)
        │
   ELK (JSON logs + request ID) · New Relic APM
```

**Hot path (single invoice):** validate → optional Redis lookups → 202/async or sync submit → IRP → persist IRN/QR → webhook.  
**Bulk path:** S3 file → chunk validate → Kafka → IRP workers → progress on dashboard.  
**Migration rule:** shared DB until traffic 100% on FastAPI; then carve service-owned tables.

---

## 3. Design decisions

| Decision | Chose | Rejected | Why |
|---|---|---|---|
| Migration shape | Step-by-step cutover + gateway canaries (strangler) | Big-bang rewrite | Filing-day zero-tolerance; rollback = config flip |
| Async runtime | FastAPI + workers | Django sync / keep PHP | IRP fan-out must not pin workers |
| Event bus | Kafka | SQS / RabbitMQ alone | Per-GSTIN ordering, durable replay, multi consumer groups |
| Partition key | Client GSTIN (± doc type) | Random / invoice id | Per-taxpayer order for submit → callback → webhook |
| Data during cutover | Shared DB then split | Dual writes | One source of truth; avoid recon nightmares |
| Shard strategy | PostgreSQL quarter shards | Single fat table / hash-only | GST returns are quarter-scoped; cold quarters archive cleanly |
| Fault model | Idempotency + backoff + DLQ | Fire-and-forget retries | Double IRP registration is not recoverable |
| Cache | Cache-aside Redis + SETNX | Write-through everywhere | Hot config/GSTIN on every bulk row; stampede control |

---

## 4. Bullet-by-bullet defense

### Bullet 1 — PHP → FastAPI microservices · 1,500+ clients · p95 1.2s → 300ms · mentored 2

| Probe | Defense |
|---|---|
| What did you own? | Design + cutover playbook + conventions; two juniors extracted services under review |
| Why not rewrite? | Compliance; per-endpoint canary with instant rollback |
| “Strangler”? | Endpoint canaries behind gateway — gradual cutover, not big-bang |
| Latency sources? | Async IRP (no blocked PHP-FPM), pooling, composite indexes `(client_id, invoice_date)`, N+1 kill; Redis moved p50, async/query fixes moved p95 |
| Client count? | **1,500+** always — never 2,500+ |
| Mentoring day-to-day? | Router/service/repository + Pydantic + idempotency helpers; paired first canary |
| Resume XYZ | Cut p95 **1.2s→300ms** for **1,500+** by Laravel→FastAPI microservices + mentoring **2** |

### Bullet 2 — Kafka + PG quarter sharding · 1M+/day · 100K+/import · 700 → 4,000 req/min

| Probe | Defense |
|---|---|
| Where is Kafka? | Import chunks, IRP jobs, signed-response persistence, webhooks, audit projector |
| Throughput claim? | HISTORICAL sustained gateway/service capacity under load + peaks |
| TPS/RPS on PDF? | **Do not put on resume.** Verbal only if asked: ~12 TPS avg from 1M/86400; 4,000/min ≈ 67 RPS |
| Quarter sharding? | Hot writes in current quarter; archive cold quarters; app routes by invoice date |
| 100K import? | Chunk validate → bounded IRP concurrency → progress stream |
| Resume XYZ | Lifted **700→4,000 req/min** and **1M+/day** by Kafka + PostgreSQL split by tax quarter |

### Bullet 3 — Idempotency, retries, DLQ · Redis −30%

| Probe | Defense |
|---|---|
| Idempotency key? | `client + fileHash + batchIndex` (+ client invoice refs) |
| Why DLQ? | Poison batch parks; rest of import continues; operator replay |
| 30% reads? | Same config/GSTIN hit on every row of a 100K import — cache removes fan-out |
| Stampede? | TTL jitter + SETNX singleflight |
| Circuit breaker? | Verbal prep only — not a resume metric |
| Resume XYZ | Cut repeat DB reads **30%** and made IRP retries safe via idempotency keys, retries, DLQ + Redis |

### Bullet 4 — ELK + New Relic · triage −70% · support tickets −35% · coverage 35→82 · 98% deploy

| Probe | Defense |
|---|---|
| What changed? | SSH/grep → structured JSON + request ID across API/consumer/worker |
| 70% math? | ~30 min → <10 min ESTIMATED baseline behind HISTORICAL cut |
| Support −35%? | Client usage dashboard + log downloads (4yr resume) — HISTORICAL ops attribution |
| Own on-call title? | Claim **alerting + triage**, not invented SEV commander |
| Coverage focus? | Money paths first: register, recon, import |
| 98%? | HISTORICAL deploy success under CI gates |
| Resume XYZ | Cut triage **70%** and tickets **35%** via ELK/New Relic + usage dashboard; coverage **35→82** at **98%** deploy |

### Tech line — defend if pressed

Python, FastAPI, Kafka, PostgreSQL, MongoDB (payload snapshots), Redis, Elasticsearch (search + ELK), Celery, Docker, New Relic, AWS.

---

## 5. Mock interview — 10 Q&A

**Q1. Why Kafka over SQS or RabbitMQ for e-invoicing?**  
**A.** Needed per-client ordering, durable replay for GST disputes, and independent consumer groups on one log. Partition by GSTIN. SQS drops cheap multi-consumer replay after ack; FIFO group throughput caps hurt. RabbitMQ could dispatch at our scale — honest trade-off. Replay + multi-reader audit + existing AsyncIOKafka stack won.

**Q2. Derive TPS/RPS — do the numbers hang together?**  
**A.** 1M+/day ≈ 11.6 ≈ ~12 TPS average (ESTIMATED). Peaks sized ~100+ TPS (ESTIMATED, ~8–10×). 700 → 4,000 req/min ≈ 12 → ~67 RPS. RPM is gateway/service capacity; daily count is IRP-registered docs. Complementary, not the same meter. Keep TPS/RPS off the PDF.

**Q3. Caching alone cannot move p95 1.2s → 300ms. What did?**  
**A.** Tail: async IRP (no hostage PHP worker), connection pooling, N+1 removal, composite indexes. Body: Redis −30% redundant reads. Cache ≠ p95 story; async + queries = p95.

**Q4. Cache-aside: keys, TTL, invalidation, herd.**  
**A.** Miss → DB → SET + TTL. Hot: IRP auth tokens (TTL under token life), client config/flags, GSTIN masters, tax rates. Config/GSTIN: DELETE on write. Masters: TTL + jitter. Herd: SETNX lock; others wait or serve slightly stale. 30% plausible under 100K-row imports repeating the same lookups.

**Q5. Why shard by financial quarter?**  
**A.** GST returns and filing spikes are quarter-scoped. Writes land in current quarter; older quarters are recon/audit reads. Quarter tables/schemas → smaller hot indexes, clean archive/drop. Cost: app-level routing; footgun = wrong-quarter write — derive quarter from invoice date at API boundary and reject mismatches.

**Q6. Sketch the IRP path and where Kafka sits.**  
**A.** Client posts JSON → validate schema/GSTIN → report to IRP → signed IRN+QR. Kafka: accepted chunks, IRP submit jobs, Mongo snapshots of responses, client webhooks. Idempotency prevents double registration. Bulk: object storage → chunk → bounded IRP concurrency → dashboard progress. 100K+/import, 1M+/day.

**Q7. What did “mentored 2” mean day to day?**  
**A.** Conventions: router/service/repository, Pydantic boundary, retry/idempotency helpers. Each junior owned a service extraction. Heavy early PR review; paired first Nginx % canary (watch errors/latency; ramp or config rollback). Shared DB during cutover. Headcount user-confirmed.

**Q8. ELK + New Relic triage −70% — vanity or real?**  
**A.** Before: SSH + grep, no correlation. After: request ID through API → Kafka consumer → IRP worker; NR APM; alerts on error/latency. ~30→<10 min ESTIMATED under HISTORICAL 70%. Claim alerting, not unproven pager ownership. Coverage 35→82 on money paths; 98% deploy HISTORICAL.

**Q9. Dual writes during migration?**  
**A.** Avoided. Shared DB through traffic cutover so one truth; table ownership split only after 100% FastAPI. Contract tests pinned PHP response shapes field-for-field.

**Q10. What broke in early canary?**  
**A.** Timeout mismatch: PHP 60s vs we set 10s. Legitimate long IRP calls failed. Fix: move IRP fully async, return 202 + poll. Canary caught it before full ramp.

---

# GeeksforGeeks — Interview Pack

**Role:** SDE · Aug 2021 – Nov 2022  
**Consensus numbers:** 10K+ daily queries (not 1K, not 100K) · ~10× contest spikes · premium +15–20% · course sales +30% · ops efficiency +70%  
**Framing:** Early-career reliability + product APIs on a high-traffic education platform — foundation for Masters ownership story.

---

## 1. 30s / 2min explain

**30 seconds**  
At GeeksforGeeks I migrated the doubt-support backend from PHP to Django to harden reliability for 10K+ daily queries and ~10× contest-day spikes. I designed voting and pinning APIs across MySQL, MongoDB, Redis, and Elasticsearch that the growth team tied to a 15–20% relative lift in premium subscriptions, and shipped an influencer analytics dashboard plus cron pipelines that correlated with +30% course sales and ~70% ops efficiency on video workflows.

**2 minutes**  
Doubt support is the Q&A layer on articles and courses — high read volume, contest spikes, messy legacy PHP. We migrated page-by-page behind the same URLs to Django + DRF: transactions, validation, cleaner read/write split, staging discipline.

Voting/pinning: unique `(user_id, content_id)` for idempotent votes; Redis display counters reconciled async to MySQL to avoid hot rows on viral posts; pinning as per-context order columns. Premium gating on some interactions — own the APIs; attribute +15–20% to growth.

Influencer dashboard: near-real-time Redis counters + daily cron rollups for partners. Crons: video processing handoffs, reminders, recording cleanup — leased so hosts don’t double-run. Own engineering; sales/efficiency are HISTORICAL business metrics.

Why Django then FastAPI at Masters? CMS/admin/ORM batteries in 2021 vs async IRP fan-out later.

---

## 2. Architecture

```
Learners / influencers
        │
   Django + DRF (doubt APIs, votes, pins, dashboard)
        │
   ┌────┴─────┬──────────┬────────────┐
   │          │          │            │
 MySQL     Redis      MongoDB    Elasticsearch
 (threads,  (badges,   (flexible   (doubt/content
  perms,     counters,  bodies /    search)
  votes SoT) unread)    attachments)
        │
   Cron host(s) ── lease/lock ──► video handoff, reminders, cleanup
        │
   SMTP connection reuse for reminder/promo batches
```

**Scale honesty:** 10K+ daily ≈ well under 1 RPS average; contest days ~10× (ESTIMATED). Reliability and spike survival matter more than “we ran at Uber scale.”

---

## 3. Design decisions

| Decision | Chose | Rejected | Why |
|---|---|---|---|
| Stack migration | PHP → Django/DRF incremental | Big-bang / stay PHP | Same URLs; transactions + validation without outage |
| Vote correctness | Unique `(user, content)` + MySQL SoT | Counter-only Redis | Double-submit idempotent; counters can drift safely |
| Hot counters | Redis display + async reconcile | Update MySQL on every vote | Viral posts melt hot rows |
| Search vs docs | Elasticsearch + Mongo flexibility | Stuff everything in MySQL JSON | Search path ≠ document shape |
| Cron safety | Advisory lease + idempotent job keys | Naive multi-host cron | No double video/reminder runs |
| Mail send | Persistent SMTP connection | Connect-per-message | Handshake 100–400ms; reuse ≈ ~50% wall-clock (prep depth) |

---

## 4. Bullet-by-bullet defense

### Bullet 1 — PHP → Django · 10K+ daily · 10× contest spikes

| Probe | Defense |
|---|---|
| Scale number? | **10K+ daily** standardized — never 100K; older “1K+ doubts/day” is narrower metric |
| What improved? | ORM transactions, request validation, read/write separation, review/staging |
| Spike story? | Contest days ~10×; design for burst without melting write path |
| Avg RPS? | Order of ten thousand/day ≪ 1 RPS average (ESTIMATED) |
| Resume XYZ | Stabilized doubt-support for **10K+/10×** by PHP→Django |

### Bullet 2 — Voting / pinning / locking · premium +15–20%

| Probe | Defense |
|---|---|
| Idempotency? | Unique constraint; second vote is no-op/update, not double count |
| Locking? | Moderation lock on a doubt thread (past resumes: voting, pinning, **locking**) |
| Hot row? | Redis counter for badge/UI; reconcile to MySQL |
| Data split? | MySQL relational SoT; Mongo flexible bodies; ES search; Redis hot reads |
| +15–20%? | Relative lift attributed by growth — own APIs/reliability, not causal monopoly |
| Resume XYZ | Lifted premium **15–20%** by shipping voting/pinning/locking REST APIs |

### Bullet 3 — Influencer dashboard · sales +30%

| Probe | Defense |
|---|---|
| Dashboard? | Earnings, transactions, coupons, filters/CSV (past resumes); Redis near-real-time + cron rollups |
| Metrics? | HISTORICAL business attribution; engineer the system, attribute carefully |
| Resume XYZ | Raised course sales **30%** via influencer earnings/analytics dashboard |
| Do not mix | Video processing / ops crons are a **separate** bullet |

### Bullet 4 — Cron pipelines · ops +70%

| Probe | Defense |
|---|---|
| Cron jobs? | Video handoff, reminders, recording cleanup |
| Reliability? | Host lease, idempotent keys, success/fail logs, retry/partial-batch handling |
| Metrics? | HISTORICAL time saved on manual video/reminder/cleanup workflows |
| Resume XYZ | Raised ops efficiency **70%** via cron pipelines (video / reminders / cleanup) |

---

## 5. Mock interview — 6 Q&A

**Q1. Design unread counts for 10K+ daily queries without melting MySQL.**  
**A.** Scale: 10K+ daily interactions (not 100K). Badge path: Redis per-user counters. Durability: MySQL threads/messages. Increment on reply; clear on read receipt. Periodic reconcile fixes drift. Django migration bought transactional write paths the PHP stack lacked.

**Q2. Voting API — idempotency and hot rows. How did MySQL / Redis / Mongo / ES split?**  
**A.** Unique `(user_id, content_id)` for idempotency. Redis display counters, async reconcile to MySQL. MySQL = threads/permissions/truth. Mongo = variable bodies/attachments. Elasticsearch = search. Pinning = ordered columns per context. Premium +15–20% = growth attribution.

**Q3. Cron pipelines claimed +70% ops efficiency — how do you keep crons honest?**  
**A.** Lease/advisory lock so two hosts don’t double-run; idempotent job keys; structured logs; retry or dead-letter partial batches. 70% = HISTORICAL time saved on manual video/reminder/cleanup workflows. Course +30% = business attribution on influencer analytics; own engineering.

**Q4. Why Django at GFG but FastAPI at Masters?**  
**A.** 2021 CMS-style product: admin, auth, ORM batteries. Masters needed async IO against flaky government IRP APIs and an event-driven bulk pipeline — FastAPI + Kafka fit that job.

**Q5. SMTP 50% faster — is that real?**  
**A.** Prep depth from older resumes: reuse one SMTP connection across a batch instead of TCP+TLS per message (often 100–400ms handshake). Amortizing that halves wall-clock for reminder/promo traffic. GFG detail, not a Masters claim.

**Q6. What would you change today?**  
**A.** Vote events on a queue with event-sourced counters; idempotency keys on reminder crons by default; clearer SLOs on contest-day latency. The Django migration and vote/pin models were the right 2021 move; the event patterns I later owned at Masters are what I’d backport.
