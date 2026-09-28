# 02. JD technical map: every responsibility, the concept, and my evidence

For each JD line: **what it means**, **what a strong answer covers**, **my real evidence**, and an **honest bridge** where my experience is thinner. OCI interviewers respect "I haven't operated X, here's how I'd do it and what I did that's closest." They don't respect bluffing.

---

## 0. OCI vocabulary you should use naturally

| Term | Meaning | Why it matters in answers |
|---|---|---|
| **Region** | Geographic area with one or more availability domains | Region-by-region deploys; data residency |
| **Availability Domain (AD)** | One or more isolated data centers in a region. Independent power/cooling/network | Replicate across ADs for HA; quorum across 3 ADs |
| **Fault Domain (FD)** | Grouping of hardware inside an AD (3 per AD). Anti-affinity for instances | Spread replicas across FDs so one rack/hardware failure doesn't take all |
| **Control plane** | APIs that create/modify resources (create bucket, launch VM) | Can be less available; must be correct and idempotent |
| **Data plane** | The path that serves the resource (read object, route packet) | Must be highly available; should keep working if control plane is down (**static stability**) |
| **Cell / shard architecture** | Split a service into independent cells, each serving a subset of tenants | Limits blast radius; deploy cell by cell |
| **Blast radius** | How many customers one failure or bad deploy can hurt | Every design and deploy answer should reduce it |
| **One-box / canary** | Deploy to one host, then one FD, then one AD, then region, then next region, with bake time | Change management answers |
| **Tenancy / compartment** | OCI's multi-tenant isolation units; IAM policies are written against compartments | Access control answers |
| **COE / RCA** | Post-incident review: timeline, root cause (5 whys), action items with owners | Incident answers |

---

## 1. System scalability

**JD:** components that support horizontal and vertical scaling, distributed state management, optimizing large-scale data processing, reviewing teammates for scalability, data plane platforms, performance and load testing.

### What a strong answer covers
- **Vertical** = bigger machine: simple, has a ceiling, a single point of failure. **Horizontal** = more machines: needs stateless services or partitioned state.
- Make compute **stateless**. Push state into a store built for it (DB, cache, log). Session affinity is a smell.
- **Partition** state by a key with good cardinality and even load (tenant, hash of id). Avoid hot keys: salting, splitting hot tenants into their own cell.
- Scale reads with caches and replicas. Scale writes with partitioning, batching, and append-only logs.
- Know the **bottleneck** before scaling: CPU, memory, IO, locks, connection pool, downstream dependency.
- Back-of-envelope: QPS, payload size, storage per day, fan-out.

### My evidence
- **Go/Gin platform, 10k peak RPS.** Stateless processes behind the load balancer. The process is a self-protecting edge (no reverse proxy) with native h2c, nested context timeouts, and Datadog tracing. It scales horizontally by adding instances. Auth identity is cached in Redis (Firebase to JWT/OIDC waterfall), so no instance holds session state.
- **ClickHouse rollups, 15.5x (189s to 12s on 250M rows).** Scaling reads by precomputing: pay once at load, read cheap with `PARTITION BY season_code` and bloom indexes on product/store/attr.
- **Vertical limits, handled:** weekly rollup needed ~170 GB of aggregator state and OOM'd on a ~236 GiB box. I shrank the unit of work to one fiscal week with memory caps and spill, instead of buying a bigger box. That is the classic "you can't scale up forever" story.
- **Masters India:** Kafka + Postgres **sharded by tax quarter**, 1M+ transactions/day, sustained **700 to 4,000 rpm**. Worker autoscaling on queue depth. Queue-based load leveling for 8 to 10x filing-deadline spikes.
- **Data processing:** Go pump at ~344k rows/s combined with 500k columnar double buffers and no per-row reflection. Keep/Drop engine processes 88k items per pass with bounded parallel batches.

### Performance and load testing: how I answer
1. Define the SLO first (p99 latency at target QPS, error budget).
2. Build a **realistic** workload: production-shaped payloads and key distributions (hot keys!), not uniform random.
3. Step load (ramp), soak (hours, looking for leaks), spike (sudden 10x), stress (to break point, to learn *how* it fails).
4. Measure p50/p95/p99, saturation (CPU, memory, pool usage, GC), and downstream latency.
5. Compare apples to apples. My **row-identical harness** for Postgres vs ClickHouse used the same 250M rows and the same query, and checked results matched, so the 15.5x wasn't a benchmark trick.
6. Put a performance regression check in CI for critical paths.

Tools to name: k6, Locust (Python), vegeta / ghz (Go, gRPC), wrk. In Go, `pprof` for CPU/heap and `go test -bench`.

### Reviewing peers for scalability (they ask "what do you look for in code review?")
- Unbounded things: loops over user input, unbounded queues, `SELECT` without `LIMIT`, unbounded goroutines, retries without caps.
- N+1 queries, missing indexes, full scans.
- Anything holding a lock or connection across a network call.
- Missing timeouts on outbound calls.
- Per-request allocations in hot paths (reflection, JSON in a loop).
- Is the new state partitionable? What happens at 10x?

---

## 2. Reliability design: redundancy, replication, automatic failover, in-service updates

**JD:** fault-tolerant components that withstand in-service updates, redundancy, replication, automatic failover.

### What a strong answer covers
- **Redundancy:** N+1 or N+2 capacity so losing one instance/FD/AD doesn't breach the SLO. Spread across fault domains and ADs.
- **Replication:** leader-follower (simple, failover needed), multi-leader (conflicts), leaderless quorum (R + W > N). Sync vs async: sync costs latency, async risks losing recent writes on failover (RPO > 0).
- **Automatic failover:** health checks, then leader election (Raft/etcd/ZooKeeper leases), then fencing tokens so an old leader can't write (split brain), then clients re-resolve. Failover must be **tested regularly**, or it won't work when needed.
- **In-service updates:** rolling deploys with connection draining, backwards-compatible schemas (expand, migrate, contract), feature flags, versioned APIs, readiness probes gating traffic.
- **Static stability:** the data plane keeps serving with last known config if the control plane dies.

### My evidence
- **Idempotent, replay-safe writes:** `ReplacingMergeTree` keeps the latest version per key, so a retried batch or overlapping wave never duplicates. Reads use `argMax` / `LIMIT 1 BY`.
- **SHA-256 natural keys** (Uber FRM): reloading the same source data produces the same keys, so reloads are upserts.
- **Optimistic row locking** (FRM): version column; a concurrent update fails instead of silently overwriting.
- **Zero-downtime migration** (Masters): a strangler behind the gateway, per-endpoint canaries, and config-based rollback. The shared DB during cutover avoided dual writes.
- **Stacked Bazel PRs** (FRM): changes land in small, reversible steps.

### Honest bridge
> "I haven't personally run a leader election or operated a multi-AD failover. Managed services (Cloud SQL, ClickHouse Cloud replicas) handled that for my systems. What I own is the application side of failover: idempotent writes so retries after failover don't duplicate, timeouts so clients don't hang on a dead leader, and replay from checkpoints or a log. For a design at OCI I'd use Raft-based replication across 3 ADs, fencing tokens, and regular game days."

---

## 3. Recovery-oriented computing (ROC), retries, circuit breakers, timeouts

### ROC in one paragraph
Failures are inevitable, so optimize **MTTR** (time to recover), not only MTBF. Principles:
1. **Fast, safe restart** (crash-only software: the only way to stop is crash, and the only way to start is recovery).
2. **Isolation / partitioning** so failures stay small (bulkheads, cells).
3. **Undo / rollback** of operator actions and data.
4. **Checkpoints** so work resumes instead of restarting.
5. **Fault injection** to test recovery paths.
6. **Diagnosis aids:** tracing and correlation IDs.

### My evidence, mapped to ROC
| ROC principle | What I built |
|---|---|
| Checkpoint and resume | Orchestration registry: det results land first (`det.json`), LLM progress appended per article. `--resume` skips finished work and never recomputes the deterministic phase. |
| Crash-safe unit of work | Go copier: unit = one `season_code` partition. Incomplete season means DROP PARTITION + recopy. SIGINT finishes the batch and doesn't checkpoint. |
| Truth from the system, not the client | Loader success = `QueryFinish` in `system.query_log`, not curl exit (an HTTP client can time out after the server commits). |
| Isolation | Per-table flock. Circuit breaker per provider. Tenant scope frozen per socket. |
| Undo | Config-based rollback at Masters. Frozen `config_hash` per output row so any bad run is identifiable and re-runnable. |
| Dead-letter | Masters DLQ: poison batches park for operator replay. |

### Timeouts
- Every outbound call has a timeout. Set it from the dependency's p99.9, not a guess.
- **Deadline propagation:** in Go, `context.WithTimeout` from the edge down, so inner calls get the *remaining* budget. That's what "nested timeouts" means on my resume.
- Timeouts at each layer must be **decreasing** inward (edge 10s > service 8s > DB 5s). Otherwise the outer layer gives up while the inner one still burns resources.

### Retries
- Only retry **idempotent** operations, or make them idempotent with idempotency keys.
- **Exponential backoff with jitter** (full jitter: `sleep = random(0, min(cap, base * 2^attempt))`).
- **Cap** attempts, and use a **retry budget** (e.g. retries ≤ 10% of requests) to avoid retry storms.
- Retry at **one** layer only. Retries at 3 layers × 3 attempts = 27x amplification.
- Don't retry 4xx (except 429 with Retry-After).

### Circuit breaker
- States: **closed** (normal, count failures), **open** (fail fast for a cool-off period), **half-open** (let a few trial requests through; success closes, failure reopens).
- Trip on consecutive failures or failure rate over a window with a minimum request count.
- **Fallback** when open: cached value, default, degraded response, or fail fast with a clear error.
- My registry trips after about 5 consecutive failures or a fail fraction. When open, articles get the **deterministic baseline** score (graceful degradation), and the run finishes.

### Bulkheads and load shedding
- Separate pools per dependency so one slow dependency can't eat all threads or connections.
- Shed load early (at admission) with 429/503 when queues are too deep. Serving everyone slowly is worse than rejecting some fast.

Go sketch for "timeout + retry + breaker" (they may ask you to write it):

```go
type Breaker struct {
    mu        sync.Mutex
    failures  int
    threshold int
    openUntil time.Time
    cooldown  time.Duration
}

var ErrOpen = errors.New("circuit open")

func (b *Breaker) Do(ctx context.Context, fn func(context.Context) error) error {
    b.mu.Lock()
    if time.Now().Before(b.openUntil) {
        b.mu.Unlock()
        return ErrOpen
    }
    b.mu.Unlock()

    err := fn(ctx)

    b.mu.Lock()
    defer b.mu.Unlock()
    if err != nil {
        b.failures++
        if b.failures >= b.threshold {
            b.openUntil = time.Now().Add(b.cooldown) // half-open after cooldown
            b.failures = 0
        }
        return err
    }
    b.failures = 0
    return nil
}

func CallWithRetry(ctx context.Context, b *Breaker, attempts int, fn func(context.Context) error) error {
    base, maxBackoff := 100*time.Millisecond, 2*time.Second
    var err error
    for i := 0; i < attempts; i++ {
        cctx, cancel := context.WithTimeout(ctx, 2*time.Second)
        err = b.Do(cctx, fn)
        cancel()
        if err == nil || errors.Is(err, ErrOpen) {
            return err
        }
        backoff := time.Duration(rand.Int63n(int64(min(maxBackoff, base<<i))))
        select {
        case <-time.After(backoff):
        case <-ctx.Done():
            return ctx.Err()
        }
    }
    return err
}
```

---

## 4. Tests, alarms, dashboards, telemetry

### What a strong answer covers
- **SLIs** (availability, latency p99, error rate, freshness), **SLOs** (targets), **error budgets** (what you can burn before freezing launches).
- **Four golden signals:** latency, traffic, errors, saturation. **RED** for services (rate, errors, duration). **USE** for resources (utilization, saturation, errors).
- **Alarms on symptoms** (customer impact), not causes. Page only on things that need a human now. Everything else is a ticket.
- **Multi-window burn-rate alerts:** for example, page if the 1h burn rate is > 14.4x *and* the 5m burn rate is > 14.4x.
- **Canaries / synthetic probes:** a script that continuously calls your API like a customer, from outside.
- Dashboards: one top-level "is it healthy?" page, then drill-downs per dependency. Deploy markers on graphs.
- Telemetry: structured logs with correlation IDs, metrics (counters, histograms), and distributed traces.
- Tests: unit, integration, contract, end-to-end, load, chaos. Alarms themselves should be tested.

### My evidence
- **Masters India:** built ELK + New Relic on-call alerting on error rate and latency, with structured JSON logs and request IDs across services and workers. **Triage 70% faster** (about 30 min to under 10), support tickets down 35%.
- **AssortSmart:** Datadog distributed tracing on the Go edge. **Per-run JSON telemetry** in the orchestration registry: tokens, USD cost, step duration, and batch fallbacks. Every output row is stamped with a frozen `config_hash`. LangSmith traces on Ask Iris.
- **Tests as guardrails:** 300-case eval + 80% CI gate. Coverage 35 to 82% (Masters), 100% statement coverage (FRM migration; IA Go CI).
- **Alarm example I'd define for the Keep/Drop engine:** fallback rate > X% in a run (provider degraded), cost per 1k items above budget, and run duration p95.

Honest line: "I built alerting and dashboards and was on the escalation path at Masters. I don't claim a formal pager rotation title."

---

## 5. Runbooks, incident response, RCA

### Incident response flow (say this as a sequence)
1. **Detect:** alarm or customer report. Acknowledge.
2. **Triage:** severity by customer impact and blast radius. Open an incident channel. Assign roles for big incidents (incident commander, comms, ops).
3. **Mitigate first, root-cause later:** roll back the last change, shift traffic away from a bad AD/cell, scale up, flip a feature flag, shed load. "What changed?" is the first question.
4. **Communicate:** status updates on a cadence, and customer-facing status if external.
5. **Resolve and verify:** metrics back to baseline.
6. **RCA / COE:** timeline, impact, 5 whys, what went well and badly, **action items with owners and dates**. Blameless: focus on mechanisms, not people.
7. **Follow through:** action items tracked to done. Add alarms/tests that would have caught it.

### Runbook structure
- **Symptom / alarm name**, what it means, customer impact.
- **Dashboards and queries** to check (links).
- **Diagnosis tree:** if X, go to step N.
- **Mitigation steps** as copy-pasteable, idempotent commands. Prefer scripts over manual steps (people make mistakes, per "Choose safety").
- **Rollback steps.**
- **Escalation:** who, when.
- **Verification:** how to know it's fixed.

### My real incident story (use for "walk me through an incident")
**64.1M half-loaded partition.**
- Detect: counts didn't reconcile between product and store rollups at the same filters.
- Diagnose: a failed HTTP INSERT still commits the blocks it wrote. My resume check "skip if partition has rows" treated a partial partition as done.
- Mitigate: DROP PARTITION for that season and rebuild.
- Root cause: success signal came from the wrong place (row existence or client exit code).
- Fix: TSV ledger of finished `(kind, season_code)`; success = `QueryFinish` in `system.query_log`; no ledger entry = drop and rebuild.
- Prevent: failure catalog entry "never `count() > 0` for success"; parity check `sum(product) = sum(store) = sum(attr)` at the same filters.

I also wrote a failure catalog for the copier (9 entries: OOM, half-written partition, client timeout after commit, EOF, retrying a spent batch, TLS reset, allowlists, oversubscription, secrets). That is effectively a runbook.

Other options: the Masters **double-filing near-miss** review (it became the team's incident template) and the **timeout canary rollback**.

---

## 6. Fault injection and brown-out testing

### Concepts
- **Fault injection:** deliberately inject failures (kill instance, add latency, drop packets, return 500s, fill disk, expire certs, clock skew) to verify detection, failover, and recovery work. Start in test, then staging, then small production experiments with an abort switch.
- **Brown-out:** partial degradation, not full outage. The dependency is *slow* or fails 20% of requests. That is harder than a clean failure, because timeouts, retries, and breakers must all behave. Brown-outs cause most real cascades (retry storms, thread pool exhaustion).
- **Game days:** scheduled exercises where a team practices an incident with runbooks.
- Tools: Chaos Monkey style instance kill, `tc netem` for latency and loss, Toxiproxy between service and dependency, fault flags in code.

### What I'd test for my systems (strong because it's specific)
| Fault | Expected behavior | Where my design handles it |
|---|---|---|
| LLM provider returns 504 for 20% of calls (brown-out) | Timed batches fall back to det score; breaker opens after threshold; run finishes; telemetry shows fallback rate | Registry |
| Process killed mid-run | `--resume` reloads det, skips finished articles | Checkpoints |
| ClickHouse INSERT fails midway | Partition not in ledger; DROP + rebuild | Loader ledger |
| Copier TLS reset | Crash; season not checkpointed; rerun recopies | Copier |
| IRP slow (Masters) | Async 202; bounded concurrency; backoff with jitter; DLQ after max attempts | Bulk pipeline |
| Redis down | Auth falls through the waterfall to source of truth; latency up, not errors | Auth cache-aside |

---

## 7. Replication, synchronization, data integrity

### Concepts
- Replication modes and consistency levels (see [fundamentals](04_system_design_fundamentals.md) §6).
- **Synchronization** techniques: change data capture, log shipping, anti-entropy with **Merkle trees**, read repair, hinted handoff, version vectors, last-writer-wins (with the clock caveat), CRDTs.
- **Integrity checks:** checksums per block/object (end to end), row counts and sums per partition, parity checks between derived and source data, periodic scrubbing.

### My evidence
- Parity validation: `sum(product)` vs `sum(store)` vs `sum(attr)` at the same filters. Store totals are re-weighted to match SKU sums. Earlier season-grain parity was 0% difference across seasons 1 to 7.
- Row-identical harness to verify ClickHouse answers equal Postgres answers.
- SHA-256 natural keys for idempotent reload (FRM).
- Keyed dedup with exactly-once upserts (Uber Menu: Kafka + Flink). I say honestly that end to end it's at-least-once plus idempotent upsert.

---

## 8. Zero maintenance windows

**JD:** "ensuring no maintenance windows are required for customers and users when resolving issues."

### Techniques
- Rolling deploys with draining. Blue/green. Canary.
- **Expand/contract schema migrations:** add the new column (nullable), dual-write or backfill, switch reads, then drop the old column in a later release. Never rename in place.
- Online index builds. Chunked backfills with throttling.
- Feature flags to turn off a broken path without a deploy.
- Backwards and forwards compatible API and message formats (add fields, never repurpose).
- Config-driven behavior (hot reload) so fixes don't need restarts.

### My evidence
- **Masters strangler:** per-endpoint canary, rollback via gateway config, shared DB during cutover (no dual writes), contract tests pinning old PHP responses field by field so clients saw no payload change.
- **KPI configurator:** new formulas without a code release.
- **ClickHouse partition rebuilds:** per season, while other seasons keep serving. Honest caveat: DROP PARTITION then recopy is *not* an atomic swap. The proper design is building into a scratch table and `REPLACE PARTITION`. That was written but not executed.

---

## 9. Automation, troubleshooting tooling, Infrastructure as Code

### Concepts
- IaC (Terraform, which OCI supports through the OCI Terraform provider and **Resource Manager**): declarative, reviewed in PRs, `plan` before `apply`, remote state with locking, modules, drift detection.
- Immutable infrastructure: replace, don't patch in place.
- Operational tooling: scripts that are **idempotent**, have `--dry-run`, log what they do, and require confirmation for destructive steps.

### My evidence
- **Go copier** as operational tooling: per-table flock, checkpoint ledger, `-reset` required for full truncate, env-only secrets (never `.env` auto-read, never committed).
- **Generated settings:** weekly rollup memory caps, thread counts, and spill are generated per build, not hand-typed.
- **CI/CD:** Bazel at Uber, Docker, CI gates (coverage, eval, SAST/SBOM on IA).
- **Resume flags** (`--resume`) on the batch engine.

### Honest bridge
> "I've written Dockerfiles and CI pipelines and built operational tooling. I haven't been the Terraform owner for a production estate. I know the workflow (modules, remote state with locking, plan in PR, apply from CI), and I'd be comfortable picking up OCI Resource Manager."

---

## 10. Security in multi-tenant environments

### Concepts to cover
- **Encryption in transit:** TLS everywhere, mTLS between services, cert rotation.
- **Encryption at rest:** **envelope encryption.** A data encryption key (DEK) encrypts the data, and a key encryption key (KEK) in a KMS/HSM (OCI Vault) wraps the DEK. Rotation re-wraps DEKs without re-encrypting all the data. Customer-managed keys.
- **Access control:** authentication (who) vs authorization (what). Least privilege, RBAC/ABAC, OCI IAM policies on compartments. Short-lived credentials (instance principals rather than static keys).
- **Tenant isolation:** tenant ID derived from the *authenticated token*, never from request parameters. Enforced at the data layer (row-level security, per-tenant schemas/keys). Noisy-neighbor limits (quotas, rate limits per tenant).
- **Secrets:** never in code or logs. A vault. Rotation.
- **Input safety:** parameterized queries, allowlists, and constant-time comparison for secrets.
- **Remediation:** vulnerability scanning (SAST, dependency/SBOM), patch SLAs by severity, and pen-test findings tracked to closure.

### My evidence
- **Auth:** Redis-fronted Firebase to JWT/OIDC waterfall on the Go platform. **Constant-time API key** comparison. **Postgres roles** per service.
- **Multi-tenant scope frozen at handshake** (Ask Iris): tenant, hierarchy, and plan scope are bound when the JWT is verified on WebSocket connect. Tools can't widen it.
- **No LLM SQL tool;** JSON payloads only (injection surface removed).
- **KPI compiler:** allowlisted functions and logical-to-physical column mapping, compiled to **parameterized** SQL.
- **Uber FRM:** SQL allowlists, SOX controls.
- **Secrets hygiene:** env-only for Cloud passwords, never committed.
- **CI:** SAST/SBOM on the IA Go platform (verbal).

### Honest bridge on encryption
> "I've used TLS everywhere and managed KMS-backed encryption on cloud databases. I haven't implemented envelope encryption myself. I can explain it and would design with it: per-tenant DEKs wrapped by a KEK in Vault, so revoking a tenant's key crypto-shreds their data."

---

## 11. Compliance and documentation

- **SOX** at Uber FRM: audit trail (review status history), FSM gates (50% delta-variance blocks transitions until reviewed), change control through code review and CI. Output feeds the external auditor's work papers.
- **GST compliance** at Masters: e-invoices registered with the government IRP. Idempotency prevents double filing, and records are traceable.
- **Documentation habits:** RFCs (the ClickHouse RFC), failure catalogs, a conventions doc for new services, and the incident review template.
- For OCI: know the names SOC 1/2, ISO 27001, PCI DSS, HIPAA, and FedRAMP. Compliance means evidence, meaning logs, access reviews, and change records.

---

## 12. Change management: patching, updating, rolling back

### Safe deployment pipeline (say this for OCI)
1. Code review, then CI (unit, integration, security scans), then build an immutable artifact.
2. Deploy to **pre-prod / integration**, run automated tests.
3. **One-box** in the first production region, then bake (watch alarms automatically).
4. **One fault domain**, then the rest of the AD, then the other ADs, then **the next region**. Start with the smallest, least-used region. Bake at each step. Never deploy to multiple regions at once.
5. **Automated rollback** when alarms fire during bake.
6. Rollback must be tested. The previous artifact stays deployable. Data migrations must be backwards compatible, so rollback doesn't need a data rollback.
7. Change freezes around peak periods (I did this around GST deadlines).

### My evidence
- Masters canary ramps with config rollback, cutover freezes during GST deadline weeks, 98% deploy success.
- Uber stacked Bazel PRs: small reversible changes, and "pure refactor means zero test diff."
- The frozen `config_hash` on every output row makes prompt/config changes auditable and revertible.
- The 80% eval gate as a promotion gate for AI changes (the change management for models).

---

## 13. Distributed state tools (they may name them)

| Tool | What it is | When |
|---|---|---|
| etcd / ZooKeeper / Consul | Consensus-backed small KV for config, leader election, locks | Coordination, not data |
| Redis / Memcached | In-memory cache, rate limit counters, short-lived locks | Hot reads, counters |
| Kafka | Durable partitioned log | Event streams, replay, decoupling |
| Cassandra / DynamoDB-like | Leaderless or partitioned wide-column, tunable consistency | High write volume KV |
| Oracle DB / MySQL / Postgres | Relational, transactions | Control plane metadata |
| ClickHouse | Columnar OLAP | Analytics |
| Object storage | Immutable blobs, cheap, durable | Data lakes, backups, large payloads |

I've used Redis, Kafka, Postgres, MySQL, ClickHouse, BigQuery, and S3 in production. I know etcd/ZooKeeper conceptually (Raft/ZAB, leases, watches).
