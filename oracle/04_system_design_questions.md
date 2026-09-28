# 04. System design: interview framework and top questions with answers

Background concepts: [fundamentals](04_system_design_fundamentals.md). Reliability depth: [JD map](02_jd_technical_map.md).

---

## A. The 45 to 60 minute framework

| Step | Time | What you do | What you say |
|---|---|---|---|
| 1. Requirements | 5–8 min | Functional (3–5 core features), non-functional (scale, latency, availability, consistency, durability, security), out of scope | "Let me confirm scope before designing." |
| 2. Estimates | 3–5 min | QPS (avg/peak), storage, bandwidth, read:write | "About 12k QPS peak writes, mostly reads, so read path optimization matters most." |
| 3. API | 3–5 min | 3–6 endpoints with key parameters, idempotency tokens, pagination | |
| 4. Data model | 5 min | Entities, keys, partition key, which store and why | "Partition by tenant_id plus hash, to avoid hot shards." |
| 5. High-level design | 10 min | Boxes: client, LB, services, stores, queues, caches | Draw the **write path** and the **read path** separately |
| 6. Deep dives | 15 min | 2–3 hardest parts: consistency, hot keys, failure handling, scaling the bottleneck | Offer options and choose with a trade-off |
| 7. Reliability and ops | 5 min | Failure modes, multi-AD, monitoring, deployment, security | OCI weighs this heavily |
| 8. Wrap up | 2 min | Summarize, bottlenecks, what you'd do next | |

### Senior signals interviewers look for
- You drive. You don't wait for prompts.
- Trade-offs named explicitly: "I choose X over Y because of Z. If Z changes, Y is better."
- Numbers used to justify decisions.
- Failure handling designed in, not added at the end.
- Operability: how would I know it's broken? How do I deploy safely? How do I roll back?
- Simplicity: don't add Kafka and 5 databases without a reason.

### Non-functional checklist (read it out)
Availability target (99.9 = 8.7h/year, 99.99 = 52 min/year) · latency p99 · consistency per operation · durability · throughput · multi-tenancy · security/compliance · cost · operability.

---

## B. Top questions with answers

### Q1. Design a distributed rate limiter (OCI API throttling)

**Requirements:** limit per tenant/API key/operation (e.g. 100 req/s with bursts to 200). Low overhead (< 1 ms). Highly available: **fail open** or closed? Usually fail open for availability, except security-sensitive limits. Return 429 with `Retry-After`.

**Estimate:** 1M QPS across the fleet, 10M keys.

**Algorithm:** token bucket per key: `(tokens, last_refill_ts)`. On request: `tokens = min(cap, tokens + (now - last) * rate)`; if tokens ≥ 1, decrement and allow.

**Design options:**
1. **Central store (Redis cluster):** a Lua script does refill + decrement atomically. Keys are sharded by hash. Accurate. Adds a network hop (~0.5 ms). Redis failure needs a fallback (local limits).
2. **Local buckets + async sync:** each API node holds buckets with `rate / N_nodes` or a leased share of the global budget, periodically reconciled. No hop, slightly inaccurate. Good at huge scale.
3. **Hybrid:** local first, and consult central only for tenants near their limit.

```
client → LB → API gateway [local token bucket] ──(async)── limiter service / Redis
                         │
                         └→ backend
```

**Deep dives:**
- **Hot tenant:** its key lives on one Redis shard. Use local pre-aggregation or split the key.
- **Clock:** use the Redis server time inside the script, not client clocks.
- **Config:** limits come from the control plane, cached in the data plane (static stability).
- **Multi-region:** limits are per region (simple), or global with an approximate sync.
- **Observability:** metrics for throttled requests per tenant, so throttling is visible.

**My tie-in:** the Masters IRP pipeline used bounded concurrency + backoff against a rate-limited government API. That's the client side of the same problem.

---

### Q2. Design a distributed key-value store (Dynamo / etcd style)

**Requirements:** `put(k, v)`, `get(k)`, `delete(k)`. Billions of keys, 100k+ QPS, p99 < 10 ms, highly available, durable, tunable consistency.

**Partitioning:** consistent hashing with virtual nodes. Each key has a **preference list** of N = 3 replicas on distinct ADs.

**Replication:**
- *AP design (Dynamo):* leaderless with quorums W = 2, R = 2, N = 3. Sloppy quorum + hinted handoff when a node is down. Read repair. Anti-entropy with Merkle trees. Vector clocks or LWW for conflicts.
- *CP design (etcd/Spanner-like):* each partition is a **Raft group** of 3 across ADs. The leader serves linearizable reads (with a lease or read index).

**Storage engine per node:** LSM tree (WAL → memtable → SSTables + compaction + Bloom filters). Write-optimized.

**Request path:**
```
client → router (knows ring/partition map, cached) → coordinator node
   put: write to N replicas, ack after W
   get: read R replicas, return newest (by version), repair stale
```

**Membership:** gossip + failure detector (phi accrual). Or a small Raft-based metadata service holding the partition map.

**Deep dives:**
- **Rebalancing on node add:** move only the affected vnode ranges, throttled.
- **Hot keys:** a cache in front, key splitting.
- **Durability:** fsync WAL per batch (group commit), replication across ADs.
- **Deletes:** tombstones, removed after the grace period during compaction.
- **Consistency trade-off:** say when you'd pick each design (bucket names: CP; session data: AP).

---

### Q3. Design object storage (like OCI Object Storage / S3)

**Requirements:** buckets and objects (KB to TB), PUT/GET/DELETE/LIST, multipart upload, 11 nines durability, high availability, strong read-after-write consistency (OCI Object Storage offers this), versioning, lifecycle policies, encryption at rest, IAM.

**Architecture (split metadata from data):**
```
client → LB → API front end (auth, throttling)
                 ├→ metadata service (bucket/object → chunk locations, versions)  [sharded, Raft-replicated DB]
                 └→ storage nodes (chunks, erasure coded across ADs)
```

**PUT flow:**
1. Authenticate, authorize (IAM policy on the compartment), check quotas.
2. Split into chunks (e.g. 8–64 MB). Stream to storage nodes. **Erasure code** (e.g. 8 data + 4 parity) placed across ADs and fault domains. Much cheaper than 3x replication at the same durability.
3. Checksums per chunk, verified end to end.
4. **Commit metadata last** (atomic write of the object version → chunk list). The object becomes visible only after the metadata commit, which gives read-after-write consistency.
5. Orphaned chunks from failed uploads get cleaned up by a garbage collector.

**GET:** metadata lookup (cached), then fetch chunks in parallel, reconstruct from any k of n chunks if some nodes are slow (**hedged reads**).

**LIST:** the metadata store is ordered by `(bucket, key)`, so a range scan with pagination tokens. Partition big buckets by key range, and split hot ranges automatically.

**Multipart upload:** upload parts in parallel with part numbers and ETags, then a commit that stitches the metadata. Resumable.

**Durability operations:** background **scrubbing** verifies checksums; repair re-encodes lost chunks on node failure; prioritize repair by the number of missing chunks.

**Security:** TLS, envelope encryption per object (DEK wrapped by a KEK in Vault), customer-managed keys, pre-authenticated requests with expiry.

**Deep dives:** hot objects (CDN, cache), small-object overhead (pack small objects together), metadata scaling (shard by bucket + key hash, with range partitioning inside), consistency of overwrite (version IDs; last committed wins).

**My tie-in:** "metadata commit last" is the same principle as my partition ledger. The data being present isn't success; the commit record is.

---

### Q4. Design a URL shortener (warm-up, often first)

- **Requirements:** create a short URL, redirect, optional custom alias and expiry. 100M new URLs/month, 10:1 read:write.
- **Estimate:** ~40 writes/s, ~400 reads/s avg; 5 years ≈ 6B URLs × 500 B ≈ 3 TB.
- **Key generation:** base62 of a unique ID. 7 chars = 62^7 ≈ 3.5 trillion. IDs come from a distributed ID generator (Snowflake: time + machine + sequence) or pre-allocated ranges per server (a ticket server hands out blocks of 1M). Avoid hash + collision checks at scale.
- **Store:** KV (short → long, created, expiry). Partition by the short key.
- **Read path:** cache (Redis/CDN) in front, since hot links dominate. Use 301 (cacheable by browsers) vs 302 (so you count analytics).
- **Analytics:** emit click events to a log, aggregate asynchronously.
- **Abuse:** rate limit creation, malware URL scanning.

---

### Q5. Design a distributed cache (like Memcached/Redis cluster)

- **API:** get, set with TTL, delete.
- **Partitioning:** consistent hashing (the client library or a proxy knows the ring).
- **Eviction:** LRU per node (hashmap + doubly linked list, see [LLD](05_lld_problems.md)), with memory limits.
- **Replication:** optional primary-replica per shard for availability. Cache data is usually rebuildable.
- **Failure:** a node dies and its keys miss, so the DB load spikes. Protect with request coalescing, gradual warm-up, and a replica promotion.
- **Hot keys:** replicate hot keys to multiple nodes, plus a local in-process L1 cache with a short TTL.
- **Consistency:** cache-aside with delete-on-write; TTL as a safety net. Stampede protection (singleflight, SETNX lock, TTL jitter), which is exactly what I did at Masters.

---

### Q6. Design a distributed job scheduler (cron at scale)

**Requirements:** schedule one-off and recurring jobs (millions), run at the right time (±seconds), **at-least-once** with idempotent jobs, retries, timeouts, priorities, visibility (status, logs), and no job lost if a node dies.

```
API → jobs DB (job definitions, next_run_at, indexed)       [partitioned by job_id hash]
scheduler shards (each owns partitions; leader per partition via lease)
   poll: SELECT due jobs WHERE next_run_at <= now LIMIT n  → enqueue
queue (per priority) → worker pool → execution records (attempt, status, heartbeat)
```

**Key decisions:**
- **Ownership:** partitions assigned to scheduler instances via leases (etcd/ZooKeeper) with fencing tokens, so two schedulers don't fire the same job.
- **Exactly-once firing is hard:** use at-least-once + idempotency. The job run ID = `(job_id, scheduled_time)`, and a unique constraint dedups.
- **Time wheel / timing wheel** for near-term timers in memory; the DB for long-term.
- **Worker heartbeats:** if the heartbeat stops, the attempt is presumed dead and re-enqueued after a visibility timeout.
- **Retries** with backoff, max attempts, then DLQ.
- **Checkpoints** for long jobs so a retry resumes. That's my Keep/Drop registry pattern.
- **Backpressure:** don't enqueue faster than workers drain. Priority lanes.
- **Missed schedules** after an outage: a policy per job (catch up all, run once, skip).
- **Observability:** schedule lag (actual start − scheduled), failure rate, queue depth.

**My tie-in:** I built the application-level version of this. The orchestration registry runs 88k-article batches with hard timeouts, circuit breakers, durable checkpoints, a claim ledger, and per-run telemetry. I chose not to add Airflow/Temporal for that workload, and I'd explain when I *would* (many teams, many DAGs, cross-service workflows).

---

### Q7. Design a metrics and alerting system (like OCI Monitoring)

**Requirements:** ingest metrics from millions of resources (e.g. 10M series, 1 point per 10–60 s), query with aggregations over time windows, alarms with thresholds, retention with downsampling, and multi-tenant.

**Estimate:** 10M series / 10 s = 1M points/s, ~16 bytes compressed per point → ~16 MB/s raw.

```
agents → ingestion front end (auth, throttle) → Kafka/Streaming (partitioned by series id)
       → aggregators (pre-aggregate 1-minute rollups) → time-series store (sharded by tenant+metric+time)
       → query service (fan-out, merge)          → dashboards
       → alarm evaluator (streaming, per alarm window) → notification service (dedupe, escalation)
```

**Deep dives:**
- **Storage:** time-series DB with columnar chunks per series (Gorilla compression: delta-of-delta timestamps, XOR floats), time-partitioned. Hot recent data in memory/SSD, older data downsampled (1 min → 1 h) in object storage.
- **Cardinality explosion** (someone puts a request ID in a label): per-tenant series limits and rejection.
- **Alarm evaluation:** streaming evaluation on ingest vs periodic queries. Handle late data with a grace window. **Missing data** policy (treat as breaching or not).
- **Alerting on the monitoring system itself:** a separate "meta-monitoring" stack; synthetic heartbeats ("dead man's switch").
- **Multi-AD:** replicate ingestion. Alarm evaluators are active-passive per partition with leases.
- **Notification:** dedupe, grouping, suppression during maintenance, and escalation policies.

**My tie-in:** I built telemetry on the application side: Datadog traces on the Go edge, per-run JSON telemetry (tokens, USD, step duration, fallbacks), and ELK + New Relic alerting at Masters.

---

### Q8. Design a notification service (email/SMS/push/webhooks)

- **Flow:** producers → API (validate, idempotency key) → queue per channel → workers → providers (SES, SMS gateway, APNs/FCM).
- **Preferences and templates:** a user preference service, templating, localization.
- **Reliability:** at-least-once with dedup by notification ID; retries with backoff per provider; circuit breaker per provider; failover to a secondary provider; DLQ.
- **Rate limits:** per user (don't spam), per provider quota.
- **Priority:** OTP/security first, marketing last (separate queues).
- **Tracking:** delivery status callbacks → event store.
- **Webhooks:** sign payloads (HMAC), retry with backoff for 24h, and let customers replay.

---

### Q9. Design a distributed message queue / log (like Kafka / OCI Streaming)

- **Model:** topics → partitions (ordered append-only logs) → segments on disk. Offset = position.
- **Producers:** partition by key hash (ordering per key); batch + compress; `acks=all` for durability; idempotent producer (producer ID + sequence) for dedup.
- **Replication:** each partition has a leader and followers in other ADs. The **ISR** (in-sync replicas) set; a commit needs all ISR (with `min.insync.replicas = 2`). Controller (Raft, KRaft) handles leader election.
- **Consumers:** consumer groups, one partition per consumer in a group; offsets committed to an internal topic; rebalancing.
- **Retention:** by time/size; log compaction keeps the latest per key.
- **Performance:** sequential IO, OS page cache, zero-copy `sendfile`, batching.
- **Exactly-once:** idempotent producer + transactions across partitions + read-committed consumers. External sinks must be idempotent.
- **Ops:** consumer lag alerts, partition skew, under-replicated partitions alarms.

**My tie-in:** I used Kafka at Masters (partition by client GSTIN for per-taxpayer ordering, offset reset for replay after a parser bug) and at Uber Menu (keyed by vendor_id, Flink keyed dedup).

---

### Q10. Design a log aggregation and search system (like ELK / OCI Logging)

- Agents tail logs → ingestion (throttle, parse, enrich with tenant/host) → a durable buffer (Kafka) → indexers → a search index (inverted index, time-based indices, sharded) + cold storage in object storage.
- Query: time-bounded first (prune indices), then full-text.
- Retention tiers: hot (7 days searchable), warm, cold (archive in object storage, rehydrate on demand).
- Protect from log storms: per-source rate limits and sampling for debug logs.
- Correlation: trace ID in every log line.

**My tie-in:** the ELK rollout at Masters with request IDs that follow an invoice across services and workers; triage 70% faster.

---

### Q11. Design a VM provisioning control plane (OCI Compute "LaunchInstance")

This is very OCI-specific. It tests control plane thinking.

**Requirements:** `LaunchInstance(shape, image, subnet, AD)` returns quickly with an OCID in PROVISIONING state; `GetInstance` shows the state; terminate. Must be idempotent, handle capacity, and survive component failures mid-workflow.

```
API (auth, validate, quota, idempotency via retry token) → instances DB (desired state)
  → workflow engine (durable state machine per request)
       1. reserve capacity (placement service: pick host in AD/FD with capacity, anti-affinity)
       2. allocate network (VNIC, IP) via network control plane
       3. attach boot volume (block storage control plane)
       4. tell host agent to start VM
       5. health check → RUNNING
  → each step idempotent, with compensation on failure (release IP, release capacity)
host agents: reconcile loop (desired vs actual), report status
```

**Key points:**
- **Desired state + reconciliation** (like Kubernetes controllers): agents converge the actual state to the desired state. This handles lost messages naturally.
- **Durable workflow** (saga) with a persisted step state. On a crash, resume from the last completed step. Same idea as my checkpoints.
- **Idempotency:** a retry token maps to the same instance OCID.
- **Placement:** bin packing with constraints (shape, FD, anti-affinity). Scoring function. Optimistic reservation with conflict retry.
- **Static stability:** running VMs don't depend on the control plane. If the control plane is down, launches fail but existing workloads are fine.
- **Cells:** per AD control planes to limit the blast radius.
- **Throttling:** per tenancy limits and service limits.
- **Observability:** per-step latency and failure metrics, stuck-workflow alarms.

---

### Q12. Design a distributed lock / configuration service (like ZooKeeper/etcd)

- A 3 or 5 node Raft cluster across ADs. Linearizable writes. Reads via the leader, or followers with read index for linearizability.
- API: create/get/set/delete with versions (CAS), **watches** (notify on change), **ephemeral keys tied to sessions/leases** (disappear when the client dies), and sequential keys (for fair locks and leader election).
- **Lock recipe:** create an ephemeral sequential key under `/locks/x`. The lowest sequence holds the lock; others watch their predecessor (avoids herd). Return a **fencing token** (the key's revision).
- **Leader election:** the same recipe; the holder of the lowest key is the leader.
- **Scale:** small data (MBs), not a database. Writes limited by consensus (~10k/s). Scale reads with followers/learners.
- **Config distribution:** clients cache config and watch for changes. Data planes keep the last known config if the service is down (static stability).

---

### Q13. Design a chat / real-time copilot service (WebSocket)

- Clients hold WebSocket connections to gateway nodes (stateful). A connection registry (user → gateway node) in Redis.
- Messages: persist first (DB partitioned by conversation ID, time-ordered), then fan out via pub/sub to the gateways holding recipients.
- Ordering per conversation: a sequence number from the conversation's partition.
- Delivery receipts, offline sync by last-seen sequence.
- Scale gateways horizontally; drain connections on deploy (clients reconnect with backoff + jitter to avoid a reconnect storm).
- **Auth at handshake:** verify the JWT on connect and bind identity and scope to the connection.

**My tie-in:** Ask Iris is exactly this pattern for an AI copilot. JWT on the WebSocket handshake, plan scope frozen at handshake (tenant isolation), a LangGraph supervisor with a 3-attempt evaluator cap (no infinite loops), and LangSmith traces.

---

### Q14. Design top-K / heavy hitters (trending, top API callers)

- Exact at small scale: hashmap counts + a min-heap of size k.
- At scale: stream → partition by key → per-partition counts in windows → merge the partial top-k (careful: the top-k of partitions isn't exact globally unless you partition by key).
- Approximate: **Count-Min Sketch** + heap, or the Space-Saving algorithm. Sliding windows via bucketed counts.
- Serve from a precomputed cache refreshed every N seconds.

---

### Q15. Design a large-scale batch AI scoring system (your own system; they may ask)

This is the Keep/Drop engine generalized. Draw it confidently.

```
trigger (CLI / HTTP start) → freeze config (prompts, params, catalog) → config_hash
   → deterministic phase: KPI math over the catalog (pure Python, no LLM) → det.json checkpoint
   → claim ledger → batch mapper (88k items per pass, bounded parallel batches)
        each batch: packed JSON context → LLM (hard timeout) → schema-validated lens scores
        breaker per provider; on timeout/open → deterministic fallback score
        progress appended per article (agent_progress.json)
   → blend (frozen weights) → write via engine insert → ReplacingMergeTree (versioned, idempotent)
   → telemetry JSON: tokens, USD, step duration, fallback count; config_hash on every row
eval: 300-case proxy harness, 80% CI gate for promotion; gold-200 bench for model choice
```

Talking points: why the LLM never gets SQL (safety, cost, determinism); why RMT (retries don't duplicate); why checkpoints (a provider outage at item 70k doesn't redo det math); why frozen weights (the LLM lost to the 74% baseline on gold-200); cost (the model picked was 73% cheaper at 100% coverage).

---

## C. Common follow-up questions and short answers

| Follow-up | Answer shape |
|---|---|
| "What if the DB goes down?" | Replicas across ADs, automatic failover (Raft/managed), clients retry with backoff; writes queue up or fail fast; reads served from cache/replica (stale OK?) |
| "What if traffic is 10x tomorrow?" | Which component saturates first (by the numbers), autoscale stateless tiers, add partitions, shed load, protect with rate limits |
| "How do you avoid a hot partition?" | Better key (add hash/salt), split hot tenants into their own cell, caching, and write sharding with read aggregation |
| "How do you deploy without downtime?" | Rolling deploy waves, backwards compatible schemas (expand/contract), feature flags, automatic rollback on alarms |
| "Exactly once?" | At-least-once + idempotent processing (dedup keys, upserts, versioned writes) |
| "Consistency vs availability here?" | Pick per operation and justify |
| "How do you know it's working?" | SLIs, burn-rate alarms, canaries, dashboards, traces |
| "How do you secure it?" | AuthN/AuthZ at the edge, tenant from the token, TLS, encryption at rest with KMS, least privilege, audit logs |
| "Cost?" | Erasure coding vs replication, tiered storage, caching, batch vs real time, and right-sizing |
