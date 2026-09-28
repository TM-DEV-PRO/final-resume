# Oracle OCI Senior Software Engineer: interview hub

Resume used everywhere here: **PyGo track** (`final_pygo_ai`, `Tarun_Mittal_SSE_5yr.pdf`). Python + Go. Uber roles are **via EPAM**.

<div class="callout warn">
<b>Confidentiality (Oracle's own rule).</b> "We only know what you tell us, so don't tell us anything that is confidential." No client names beyond what is on the PDF, no cluster hosts, passwords, internal repo paths, or customer data. Numbers on the PDF are fine. Say "a retail client" if you are unsure.
</div>

---

## What the loop looks like

OCI loops are usually 4 to 5 rounds, 45 to 60 minutes each. Each interviewer owns a **focus area** and also scores **core values** (the PDF says every loop is "rooted in behavioral-based questions"). Expect behavioral questions in *every* round, not only the hiring manager round.

| Round | Typical content | Study file |
|---|---|---|
| Coding 1 / 2 | 1 to 2 LeetCode medium (sometimes hard). Trees, graphs, heaps, DP, intervals, design-a-class. Talk out loud. | [DSA hub](03_dsa_index.md) |
| System design | Distributed service at OCI scale: object store, metadata service, rate limiter, job scheduler, metrics pipeline, control plane | [SD fundamentals](04_system_design_fundamentals.md), [SD questions](04_system_design_questions.md) |
| LLD / OOD | Class design with extensibility, sometimes with concurrency (LRU, rate limiter, parking lot, logger, KV store with TTL) | [LLD foundations](05_lld_foundations.md), [LLD problems](05_lld_problems.md) |
| Concurrency (often mixed into coding or LLD) | Thread-safe cache, bounded blocking queue, producer/consumer, worker pool, deadlock | [Concurrency](06_concurrency.md) |
| Hiring manager / bar raiser | Core values, projects deep dive, ops/on-call, incident, RCA, conflict | [Core values STAR](01_core_values_star.md), [Projects](07_projects_deep_dive.md) |
| Any round | Reliability, operability, security, change management (the JD is heavy on this) | [JD technical map](02_jd_technical_map.md) |

---

## Files

1. [01 Core values: STAR answers for all 11 OCI values](01_core_values_star.md)
2. [02 JD technical map: every JD responsibility, concept answer, and my evidence](02_jd_technical_map.md)
3. [03 DSA hub: pattern cheat sheet, study plan, top-question list](03_dsa_index.md)
    - [03.1 Arrays, strings, hashing, two pointers, sliding window, prefix sums, binary search](03_dsa_1_arrays_hashing_search.md)
    - [03.2 Linked list, stack, monotonic stack, queue, deque, heap](03_dsa_2_linkedlist_stack_queue_heap.md)
    - [03.3 Trees, BST, trie](03_dsa_3_trees_bst_trie.md)
    - [03.4 Graphs, BFS/DFS, topological sort, shortest paths, MST, DSU](03_dsa_4_graphs_dsu.md)
    - [03.5 Dynamic programming, all families](03_dsa_5_dynamic_programming.md)
    - [03.6 Backtracking, greedy, intervals, matrix, bit manipulation, math](03_dsa_6_backtracking_greedy_intervals_matrix_bits.md)
4. [04 System design fundamentals (basics to distributed systems)](04_system_design_fundamentals.md)
5. [04 System design: interview framework and top questions with answers](04_system_design_questions.md)
6. [05 LLD foundations: OOP, SOLID, patterns, zero to hero](05_lld_foundations.md)
7. [05 LLD problems with full designs and code](05_lld_problems.md)
8. [06 Multithreading and concurrency in depth (Python + Go)](06_concurrency.md)
9. [07 My projects deep dive, OCI framing](07_projects_deep_dive.md)

---

## 14 day plan (compress to 7 by halving DSA sets)

| Day | Morning (2h) | Evening (2h) |
|---|---|---|
| 1 | Read 01 fully, write your own 2 line hook per value | DSA 03.1 arrays/hashing/window |
| 2 | 07 projects: say each pitch out loud, 2 min each | DSA 03.1 binary search + prefix |
| 3 | 04 fundamentals sections 1 to 6 | DSA 03.2 stack/heap |
| 4 | 04 fundamentals sections 7 to 12 | DSA 03.3 trees/trie |
| 5 | 04 questions: rate limiter, KV store, object storage | DSA 03.4 graphs |
| 6 | 02 JD map (reliability, ops, security) | DSA 03.4 DSU + topo |
| 7 | 05 LLD foundations | DSA 03.5 DP 1D/2D |
| 8 | 05 LLD problems: LRU, parking lot, rate limiter | DSA 03.5 DP knapsack/interval |
| 9 | 06 concurrency: primitives + Go | DSA 03.6 backtracking/intervals |
| 10 | 06 classic problems, code bounded queue from memory | Mock coding 2 problems timed |
| 11 | 04 questions: scheduler, metrics, notification | Mock system design out loud |
| 12 | 01 again: tell 11 stories to a timer, 2 min each | Mock LLD 45 min |
| 13 | Weak areas | Mixed mock |
| 14 | Light review, questions to ask, sleep | |

---

## The 60 second intro (Oracle version)

> I'm a senior backend engineer with about five years in Python and Go, focused on high-throughput services and data platforms. Most recently at Impact Analytics I built the Go/Gin platform for AssortSmart that handles 10k peak RPS as a self-protecting edge with nested timeouts and Datadog tracing, moved planner analytics onto ClickHouse rollups (189 seconds to 12 seconds on a 250M-row pivot), and built a batch AI decision engine with timeouts, circuit breakers, and durable checkpoints so 88k-item runs survive provider failures. Before that I was at Uber via EPAM, where I owned a SOX-grade FastAPI and MySQL backend for Finance risk scoping that cut reconciliation from 14 days to 3, and at Masters India, where I migrated a PHP monolith to FastAPI with canaries, idempotent Kafka pipelines, and a dead-letter queue, taking p95 from 1.2s to 300ms. What draws me to OCI is that the job is literally what I've been doing at smaller scale: resiliency, operability, and correctness in distributed systems, where the basics matter.

---

## JD to topic map (one screen)

| JD phrase | Where it's covered | My strongest real evidence |
|---|---|---|
| Horizontal and vertical scaling, distributed state | 04 fundamentals §2, §5; 02 §1 | Go/Gin 10k peak RPS stateless edge; Redis-fronted auth waterfall; Kafka + PG sharded by tax quarter |
| Large-scale data processing, data plane | 02 §1; 07 AssortSmart core | ClickHouse rollups, 15.5x; Go pump ~344k rows/s; 170 GB OOM sliced by week |
| Performance and load testing | 02 §2 | 250M row-identical harness PG vs CH; Masters 700 to 4,000 rpm; gold-200 bench |
| Redundancy, replication, automatic failover | 04 fundamentals §6; 02 §3 | ReplacingMergeTree idempotent writes; PG/CH replicas; honest bridge on failover |
| Recovery-oriented computing | 02 §3 | Checkpoints skip det recompute; partition ledger + DROP PARTITION recopy; DLQ replay |
| Retries, circuit breakers, timeouts | 04 fundamentals §8; 02 §3 | Registry breakers and hard timeouts; nested context timeouts in Go; bounded retries with jitter against IRP |
| Tests, alarms, dashboards, telemetry | 02 §4 | Datadog tracing; ELK + New Relic triage down 70%; per-run JSON telemetry (tokens, USD, fallbacks) |
| Runbooks, incident response, RCA | 02 §5 | 64.1M half-loaded partition; Masters near-miss review; timeout canary rollback |
| Fault injection, brown-out | 02 §6 | Timeout fallback to det baseline (graceful degradation); how I'd inject faults |
| Replication and synchronization | 04 fundamentals §6; 02 §7 | Store totals re-weighted to match SKU sums; row-identical parity checks |
| No maintenance windows | 02 §8 | Strangler + canary at Masters; stacked Bazel PRs; config-driven KPIs without deploys |
| Automation and troubleshooting tooling, IaC | 02 §9 | Go copier with flock + ledger; generated weekly settings; honest bridge on Terraform |
| Encryption, access control, multi-tenant | 02 §10 | JWT/OIDC waterfall, constant-time API keys, Postgres roles, frozen handshake scope, SQL allowlists |
| Compliance and documentation | 02 §11 | SOX gates at Uber FRM (FSM 50% delta-variance); GST compliance at Masters |
| Change management: patch, update, roll back | 02 §12 | Canary ramps, config rollback, 98% deploy success, frozen config_hash per output row |
| Planning, collaboration, problem solving, learning, improvement | 01 bottom section | Led 3 at FRM; mentored 2 at Masters; ClickHouse RFC |

---

## Questions to ask them (pick 3)

1. How is the team split between control plane and data plane work, and which does this role touch?
2. What does on-call look like: rotation size, ticket volume, what counts as a Sev 2?
3. How do you do deployments here: one-box, then fault domain by fault domain, then region by region? What is the bake time?
4. What's the most recent COE / RCA that changed how the team builds things?
5. What would make someone in this role clearly successful at six months?
6. How much of the team's roadmap is new features versus operational excellence work?

---

## Day-before checklist

- Laptop charged, camera, good light (the PDF asks for this).
- Know your 11 value stories by name (one line each, see top of 01).
- Rehearse the 3 numbers people fuse: **15.5x is query time**, **170 GB OOM is load time**, **344k is rows/s, not RPS**.
- Rehearse the honesty lines: 80% is a CI gate, 73% is gold-200, Uber is via EPAM, no K8s cluster ops, no Kafka on AssortSmart.
- If a question is unclear, ask (the PDF explicitly asks you to).
