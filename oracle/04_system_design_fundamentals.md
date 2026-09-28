# 04. System design fundamentals: basics to distributed systems

Everything you need to *reason* in a design round. Questions with full answers are in [04 System design questions](04_system_design_questions.md).

---

## 1. Numbers and estimation

### Latency numbers (order of magnitude)
| Operation | Time |
|---|---|
| L1 cache | 1 ns |
| Main memory | 100 ns |
| Compress 1 KB (fast codec) | ~2 µs |
| SSD random read | ~16–100 µs |
| Read 1 MB sequential from memory | ~3 µs–10 µs |
| Round trip within a data center (same AD) | ~0.5 ms |
| Read 1 MB sequential from SSD | ~50 µs–1 ms |
| Disk seek (HDD) | ~10 ms |
| Cross-AD round trip (same region) | ~1–2 ms |
| Cross-region round trip | 50–150 ms |

### Useful conversions
- 1 day ≈ 86,400 s ≈ **10^5 s**. 1M requests/day ≈ **12 QPS** (I used that exact math for Masters: 1M/86,400 ≈ 11.6 TPS).
- 1 month ≈ 2.5 × 10^6 s.
- QPS peak ≈ 2 to 10× average (filing deadlines were ~8 to 10× at Masters).
- Storage/year = writes/s × size × 3 × 10^7 s.
- 1 server can do roughly 1k–50k simple HTTP QPS depending on work per request. Go/Gin at 10k peak RPS was our platform.

### Estimation procedure (2 to 3 minutes, out loud)
1. Users → DAU → requests per user per day → average QPS → peak QPS.
2. Read:write ratio.
3. Object size → storage per day → retention → total (× replication factor).
4. Bandwidth = QPS × size.
5. Memory for cache = 20% of hot data (80/20 rule).

---

## 2. Scaling

- **Vertical (scale up):** bigger CPU/RAM. Simple, no code change. Hard ceiling, expensive at the top, still one failure domain.
- **Horizontal (scale out):** more nodes. Needs stateless services + a load balancer, or partitioned state. Near-linear if there's no shared bottleneck.
- **Stateless service:** any instance can serve any request. State lives in a DB, cache, or client token (JWT). My Go/Gin platform is stateless; identity is resolved from the token and a Redis-fronted lookup.
- **Autoscaling:** on CPU, QPS, or **queue depth** (better for workers; I scaled Masters workers on queue depth).
- **Bottlenecks move:** scale the web tier and the DB connection pool breaks; scale the DB and a hot partition breaks. Always ask "what's the next bottleneck?"
- **Amdahl's law:** the serial part limits speedup. Locks, single leaders, and global counters are serial parts.

---

## 3. Networking and the request path

- **DNS:** name → IP, TTL-based caching, geo-DNS / latency routing for multi-region, and health-checked failover records.
- **CDN / edge cache:** static content and cacheable GETs near users.
- **Load balancers:**
  - **L4** (TCP/UDP): fast, connection-level, no content awareness.
  - **L7** (HTTP): routing by path/header, TLS termination, retries, and rate limiting.
  - Algorithms: round robin, least connections, least latency (EWMA), consistent hashing (sticky by key), **power of two choices** (pick 2 random, choose the less loaded; near-optimal and cheap).
  - Health checks: active (probe) + passive (outlier detection). Drain connections on deploy.
- **Protocols:**
  - HTTP/1.1: one request at a time per connection (head-of-line blocking).
  - **HTTP/2:** multiplexed streams over one connection, header compression. **h2c** = HTTP/2 cleartext (no TLS), used internally. My Go edge serves native h2c without a reverse proxy.
  - HTTP/3 / QUIC: over UDP, no TCP head-of-line blocking.
  - **gRPC:** HTTP/2 + protobuf, streaming, deadlines built in. Good for service to service.
  - **WebSocket:** full duplex over one TCP connection (Ask Iris chat). Needs sticky routing or a pub/sub backplane to scale.
  - Long polling / SSE: simpler server push.
- **TLS:** handshake cost (1-RTT with TLS 1.3), session resumption, mTLS for service identity.
- **Connection pooling:** reuse TCP/TLS connections. At GFG, reusing the SMTP connection cut send time roughly in half.

---

## 4. Storage

### SQL vs NoSQL
| | Relational (Oracle DB, MySQL, Postgres) | Key-value / wide-column (Cassandra, DynamoDB-like, Redis) | Document (Mongo) | Columnar OLAP (ClickHouse, BigQuery) |
|---|---|---|---|---|
| Model | Tables, joins, schema | Key → value / row | JSON documents | Columns stored separately |
| Transactions | Full ACID | Per key (usually) | Per document (multi-doc exists) | Weak; append-oriented |
| Scale | Vertical + read replicas + sharding (manual) | Horizontal by design | Horizontal | Horizontal, scan-optimized |
| Use | Metadata, money, control plane | High QPS lookups, sessions, counters | Flexible payloads | Aggregations over billions of rows |

My stack across all four: MySQL (Uber FRM), Postgres (IA roles/OLTP, Masters), Redis, Mongo (invoice payload snapshots), ClickHouse and BigQuery (analytics).

### Indexes
- **B+ tree:** balanced, sorted, range scans, in-place updates. Read-optimized. Used by Oracle, MySQL InnoDB, and Postgres.
- **LSM tree** (RocksDB, Cassandra): writes go to a memtable + WAL, flush to sorted SSTables, and compact in the background. Write-optimized. Reads may check several levels (Bloom filters help).
- **Composite index** order matters (leftmost prefix). At Masters, `(client_id, invoice_date)` fixed slow lists.
- **Covering index:** the query is served from the index alone.
- The cost of indexes: slower writes and more storage.

### ACID and isolation
- **Atomicity** (all or nothing, via WAL/undo), **Consistency** (constraints), **Isolation**, **Durability** (fsync, replication).
- Isolation levels and anomalies:

| Level | Dirty read | Non-repeatable read | Phantom | Notes |
|---|---|---|---|---|
| Read uncommitted | yes | yes | yes | |
| Read committed | no | yes | yes | Oracle and Postgres default |
| Repeatable read | no | no | maybe | MySQL InnoDB default (gap locks prevent most phantoms) |
| Snapshot isolation | no | no | no* | *write skew possible |
| Serializable | no | no | no | Costly |

- **Optimistic concurrency:** a version column; `UPDATE ... WHERE id = ? AND version = ?`; 0 rows updated means a conflict, so retry or report it. I used **optimistic row locking** at Uber FRM so two reviewers can't overwrite each other.
- **Pessimistic:** `SELECT ... FOR UPDATE`. Holds locks, risks deadlocks, fine for short hot sections.
- **MVCC:** readers don't block writers. Each transaction sees a snapshot.

### OLTP vs OLAP
- OLTP: many small transactions, row-oriented, indexes.
- OLAP: few big scans, **columnar**, compression, vectorized execution, partition pruning, skip indexes. My ClickHouse move: 189s to 12s on 250M rows.
- ClickHouse specifics I can explain: MergeTree parts and background merges, `ORDER BY` as the sparse primary index, `PARTITION BY` for pruning and partition-level ops, **ReplacingMergeTree** for versioned upserts (dedup at merge time, so read with `argMax`/`FINAL`), and materialized views and rollup tables.

### Object and block storage
- **Block** (OCI Block Volume): a raw disk for one VM, low latency.
- **File** (OCI File Storage, NFS): shared POSIX.
- **Object** (OCI Object Storage): immutable blobs by key, massive scale, HTTP API, 11 nines durability via erasure coding/replication across ADs, and a metadata service + storage nodes split.

---

## 5. Partitioning (sharding) and distributed state

- **Why:** data or write load bigger than one node.
- **Range partitioning:** by key range (time, alphabetical). Good for range scans. Risks hot spots (all writes on "today"). ClickHouse `PARTITION BY season_code` and Postgres sharded **by tax quarter** at Masters are range-style partitions.
- **Hash partitioning:** `hash(key) % N`. Even spread, but no range scans and resharding moves almost everything.
- **Consistent hashing:** nodes and keys on a ring. Adding a node moves only ~1/N of the keys. **Virtual nodes** smooth the load and handle heterogeneous machines. Used by Dynamo, Cassandra, and cache clusters.
- **Rendezvous (HRW) hashing:** for each key pick the node with the highest `hash(key, node)`. Simple, minimal movement.
- **Directory-based:** a lookup service maps key → shard. Flexible (move a hot tenant) at the cost of an extra dependency (cache it).
- **Hot keys / celebrities:** split the key (`key#1..#k`) and aggregate on read, cache aggressively, isolate hot tenants in their own cell, and use request coalescing.
- **Rebalancing:** move partitions, not keys (fixed number of partitions > nodes), throttle it, and never rebalance during an incident.
- **Secondary indexes on sharded data:** local (scatter-gather reads) vs global (partitioned by the index term, with async updates).
- **Distributed state tools:** see [02 JD map §13](02_jd_technical_map.md).

---

## 6. Replication and consistency

### Replication topologies
- **Single leader:** all writes to the leader, followers replicate the log. Simple and consistent on the leader. Failover is needed. Read replicas can be stale (**replication lag**).
- **Multi-leader:** writes in each region. Conflicts need resolution (LWW, CRDTs, app merge). Used for multi-region active-active.
- **Leaderless (Dynamo-style):** write to W of N replicas, read from R. **R + W > N** gives overlap (the read sees the latest write). Sloppy quorum + **hinted handoff** when nodes are down, **read repair** and **anti-entropy with Merkle trees** to converge.

### Sync vs async
- **Synchronous:** the write is acknowledged after the replica confirms. RPO = 0, higher latency, availability depends on the replica.
- **Asynchronous:** fast, but a leader failover can lose the last writes (RPO > 0).
- **Semi-sync / quorum:** ack after a majority. Raft does this.

### Consistency models (strong to weak)
1. **Linearizable:** acts like a single copy. Every read sees the latest completed write. Needed for locks, leader election, and unique constraints.
2. **Sequential:** all see the same order, not necessarily real time.
3. **Causal:** cause before effect for everyone (a reply after its question).
4. **Read-your-writes, monotonic reads:** session guarantees. Route a user's reads to the leader for a few seconds after a write, or use version tokens.
5. **Eventual:** replicas converge if writes stop. My `ReplacingMergeTree` writes are eventually consistent: duplicates collapse at merge, and reads use `argMax` to be correct before the merge.

### CAP and PACELC
- **CAP:** during a network **P**artition you choose **C**onsistency (reject some requests) or **A**vailability (serve possibly stale data). You can't avoid partitions, so it's really C vs A under partition.
- **PACELC:** if Partition, choose A or C; **E**lse, choose **L**atency or **C**onsistency. Example: DynamoDB-style is PA/EL; Spanner-style is PC/EC.
- Say which one your design picks **per operation**: "creating a bucket name must be unique, so it's CP; reading an object listing can be slightly stale, so it's AP."

### RPO and RTO
- **RPO:** how much data you can lose (time since the last replicated point).
- **RTO:** how long until you're serving again.
- Backups (RPO hours), async replication (seconds), sync replication (zero).

---

## 7. Consensus, coordination, time

### Raft (know it well enough to explain in 2 minutes)
- Roles: leader, follower, candidate. **Terms** are monotonically increasing epochs.
- **Leader election:** a follower times out (randomized 150–300ms), becomes a candidate, increments its term, and requests votes. A majority wins. It votes only for candidates whose log is at least as up to date.
- **Log replication:** the leader appends an entry and sends AppendEntries. The entry is **committed** once a majority stores it. Then it's applied to the state machine.
- **Safety:** a committed entry is present in all future leaders' logs.
- 3 nodes tolerate 1 failure; 5 tolerate 2. Spread them across **3 ADs**.
- Used in: etcd, Consul, CockroachDB, TiKV. **Paxos** is the older equivalent (Multi-Paxos in Chubby/Spanner). **ZAB** is ZooKeeper's.

### Leases, locks, and fencing
- **Lease:** a lock with a timeout. The holder must renew. If it pauses (GC, network) past the lease, someone else takes over.
- **Fencing token:** the lock service hands out an increasing number with each lease. The storage rejects writes with an older token. This prevents a paused old leader from corrupting data (**split brain**).
- **Redis lock (SET NX PX):** fine for efficiency (avoid duplicate work), not for correctness without fencing. Redlock is debated. Use etcd/ZooKeeper for correctness locks.

### Clocks
- Physical clocks drift, and NTP can jump backwards. **Never** use wall-clock timestamps to order events across machines for correctness (LWW with skew loses writes).
- **Lamport clock:** a counter, `max(local, received) + 1`. Gives a total order consistent with causality.
- **Vector clock:** a counter per node. It can detect **concurrent** writes (conflicts).
- **Hybrid logical clock (HLC):** physical time + a logical counter. Used by CockroachDB.
- **TrueTime** (Spanner): bounded uncertainty. Commit waits out the uncertainty for external consistency.

### Distributed transactions
- **2PC:** the coordinator runs prepare (all vote) then commit. **Blocking** if the coordinator dies after prepare. Use it within one database system, and avoid it across services.
- **Saga:** a sequence of local transactions, each with a **compensating action** (refund, release). Orchestrated (central coordinator) or choreographed (events).
- **Transactional outbox:** write the business row and an outbox row in one local transaction. A relay publishes the outbox to the queue. That solves "DB updated but message not sent."
- **Idempotent consumers** + at-least-once delivery ≈ effectively once.

### Gossip and membership
- Nodes periodically exchange state with random peers. Converges in O(log N) rounds. Used for membership and failure detection (SWIM, phi-accrual detectors).

---

## 8. Resilience patterns

(Deep version with Go code: [02 JD map §3](02_jd_technical_map.md).)

| Pattern | What | My use |
|---|---|---|
| **Timeout** | Bound every remote call. Propagate deadlines. | Nested Go context timeouts at the edge; hard per-batch LLM timeouts |
| **Retry + backoff + jitter** | Only idempotent ops. Cap attempts, use a retry budget. | Bounded retries against the IRP (Masters) |
| **Circuit breaker** | Fail fast when a dependency is unhealthy. Half-open probe. | Orchestration registry, per provider |
| **Fallback / graceful degradation** | A degraded but useful answer | Deterministic baseline score on LLM timeout |
| **Bulkhead** | Separate pools per dependency or tenant | Per-worker connection budgets in the copier |
| **Backpressure** | Slow the producer when the consumer lags | Kafka consumer lag as the SLO (Menu); bounded queues |
| **Load shedding** | Reject early with 429/503 when overloaded | Admission control at the edge |
| **Rate limiting** | Per tenant/key quotas | See the rate limiter design |
| **Idempotency keys** | Safe retries of non-idempotent operations | `client + fileHash + batchIndex` (Masters) |
| **Checkpointing** | Resume long work | det.json + agent_progress.json; partition ledger |
| **Dead-letter queue** | Park poison messages | Masters DLQ replay |
| **Health checks** | Liveness vs readiness | Readiness gates traffic during deploys |

### Rate limiting algorithms
| Algorithm | How | Pros / cons |
|---|---|---|
| **Token bucket** | Tokens refill at rate r up to capacity b. Each request takes one. | Allows bursts up to b. Most common (OCI API throttling behaves like this) |
| **Leaky bucket** | A queue drains at a fixed rate | Smooths output, adds latency |
| **Fixed window counter** | Count per minute | Simple. Double burst at the window edge |
| **Sliding window log** | Store the timestamps | Exact, memory heavy |
| **Sliding window counter** | Weighted current + previous window | Good approximation, cheap |

Distributed: Redis `INCR` + `EXPIRE`, or a Lua script for an atomic token bucket. Or local buckets with a periodically synced global budget (fast, slightly inaccurate).

---

## 9. Caching

- **Where:** client, CDN, load balancer, application (in-process), distributed (Redis/Memcached), and DB buffer cache.
- **Patterns:**
  - **Cache-aside** (lazy): read cache; on a miss, read the DB and set the cache with a TTL. Most common. I used it at Masters (Redis cut redundant DB reads 30%).
  - **Read-through:** the cache loads from the DB itself.
  - **Write-through:** write the cache and DB together (consistent, slower writes).
  - **Write-behind:** write the cache, flush to the DB async (fast, risk of loss).
  - **Refresh-ahead:** refresh hot keys before expiry.
- **Invalidation:** TTL, explicit delete on write (delete, don't update, to avoid race ordering), versioned keys, or CDC-driven invalidation.
- **Stampede / thundering herd:** a hot key expires and 1,000 requests hit the DB. Fixes: **singleflight / request coalescing** (one fetch, others wait), a lock with `SETNX`, **TTL jitter**, serving stale while revalidating, and probabilistic early refresh.
- **Eviction:** LRU, LFU, TTL, and size-aware.
- **Consistency:** the cache is always potentially stale. Say how stale is acceptable per data type.
- **Negative caching:** cache "not found" briefly to protect against scans for missing keys.

---

## 10. Messaging and streams

| | Queue (SQS, RabbitMQ, OCI Queue) | Log (Kafka, OCI Streaming) |
|---|---|---|
| Consumption | A message is deleted after ack | Messages are retained; consumers track offsets |
| Replay | No | Yes (reset offset) |
| Multiple consumers | Competing consumers | Many independent consumer groups |
| Ordering | FIFO variants, limited | Per partition |
| Use | Task dispatch | Event streaming, audit, replay, fan-out |

- **Delivery semantics:** at-most-once (ack before processing), **at-least-once** (ack after processing; duplicates possible), and exactly-once (transactions inside Kafka + idempotent or transactional sinks). **In practice: at-least-once + idempotent consumer.** I say that honestly about Uber Menu's Kafka + Flink "exactly-once upserts."
- **Ordering:** partition by key (vendor_id at Uber Menu, client GSTIN at Masters) for per-entity order.
- **Consumer lag** is the key SLO. Alert on lag growth, not just the lag value.
- **Poison messages:** bounded retries, then DLQ with a replay tool.
- **Backpressure:** bounded buffers. Stream processors (Flink) propagate backpressure upstream.
- **Stream processing concepts:** event time vs processing time, watermarks (how late data can be), windows (tumbling, sliding, session), keyed state + checkpoints (Flink uses RocksDB state + checkpoint barriers).

---

## 11. Observability and operations

- **Logs** (structured JSON, correlation IDs), **metrics** (counters, gauges, histograms; percentiles from histograms), **traces** (spans across services; W3C trace context).
- SLI / SLO / error budget. Burn-rate alerts. Page on symptoms.
- Dashboards: golden signals per service and per dependency, with deploy markers.
- Synthetic canaries from outside.
- Full detail: [02 JD map §4 to §6](02_jd_technical_map.md).

---

## 12. Security basics

- AuthN (who: passwords, OAuth2/OIDC, mTLS, API keys, instance principals) vs AuthZ (what: RBAC, ABAC, policies).
- **JWT:** signed claims (verify the signature, `exp`, `aud`, `iss`); short-lived; revocation is hard, so keep TTLs short and use refresh tokens.
- TLS in transit, envelope encryption at rest with KMS/Vault, key rotation.
- Least privilege, secret management, audit logs.
- Multi-tenant: tenant ID from the token, enforced at the data layer; per-tenant quotas; noisy-neighbor isolation.
- OWASP basics: injection (parameterize), SSRF (egress allowlists, block the metadata IP), and timing attacks (constant-time compare, as I did for API keys).

---

## 13. Cloud-provider architecture patterns (what OCI interviewers love)

1. **Control plane vs data plane:** keep the data plane simple and highly available. The data plane caches config and keeps working if the control plane is down (**static stability**).
2. **Cells:** N independent copies of the full stack, each serving a subset of tenants. A cell router (thin, simple) maps tenant → cell. A bad deploy or poison request hurts one cell.
3. **Shuffle sharding:** each tenant gets a random subset of k workers out of N. Two tenants rarely share all workers, so one noisy tenant can't take down the others.
4. **Multi-AD by default:** replicas in 3 ADs with quorum writes. Spread instances across fault domains.
5. **Region independence:** no cross-region synchronous dependency in the request path. Regions fail independently.
6. **Constant work:** systems that do the same amount of work regardless of load (e.g. push full config every N seconds instead of deltas) have no surprise modes.
7. **Avoid bimodal behavior:** fallback paths that are rarely exercised break when needed. Exercise them (fault injection).
8. **Safe deployment:** one-box, FD, AD, region waves with bake times and automatic rollback.
9. **Idempotent APIs** with client tokens (OCI APIs take an `opc-retry-token` header for this).
10. **Quotas and limits** per tenancy, with throttling (429) instead of falling over.
11. **Backpressure and admission control** at every tier.
12. **Everything is metered:** usage events flow to billing through a durable log.

---

## 14. Data-structure building blocks for big systems

| Structure | What it answers | Where |
|---|---|---|
| **Bloom filter** | "Definitely not present" / "maybe present" | LSM reads, ClickHouse skip indexes, cache guard |
| **Count-Min Sketch** | Approximate frequency | Heavy hitters, top-k at scale |
| **HyperLogLog** | Approximate distinct count (~1.6% error, KBs) | Unique visitors |
| **Merkle tree** | Which ranges differ between replicas | Anti-entropy (Dynamo, Cassandra), Git |
| **Consistent hash ring** | Key → node with minimal movement | Caches, KV stores |
| **Skip list** | Sorted set with O(log n) ops | Redis ZSET, memtables |
| **LSM tree** | Write-heavy storage | RocksDB, Cassandra |
| **B+ tree** | Read-heavy indexed storage | Oracle DB, InnoDB |
| **Write-ahead log** | Durability and replication | Every DB; Raft log |
| **Geohash / quadtree** | Spatial lookup | Nearby search |
| **Inverted index** | Term → documents | Search (Elasticsearch) |
| **t-digest / HDR histogram** | Latency percentiles | Monitoring |

---

## 15. Batch vs stream processing

- **Batch** (MapReduce, Spark, SQL over a lake): high throughput, minutes to hours of latency, easy reprocessing.
- **Stream** (Flink, Kafka Streams): seconds, stateful, harder to operate.
- **Lambda architecture:** batch + speed layer (complex). **Kappa:** stream only, reprocess by replaying the log.
- My examples:
  - **Batch:** the Keep/Drop engine (88k per pass, checkpoints) and the ClickHouse rollups (week-sliced).
  - **Stream:** Uber Menu's Kafka + Flink keyed dedup.
- Memory-bounded aggregation: shrink the unit of work (my one-fiscal-week slicing), external spill, and cap parallelism.
