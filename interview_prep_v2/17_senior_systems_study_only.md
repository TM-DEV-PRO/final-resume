# Senior Systems Deep Dive (Ownership, Reliability, Data Infra)

**Purpose:** Interview fluency for big-tech senior screens.  
**Honesty rule:** Items marked `STUDY ONLY - NOT RESUME EXPERIENCE` are study material. Do **not** claim them as production ownership on the resume unless a later evidence matrix row reaches 95%+.

Resume-safe claims live in `GROUND_TRUTH.md` evidence matrix: FRM ownership/architecture, Masters strangler + Kafka scale + idempotency/DLQ + ELK/New Relic on-call alerting, Design Patterns / Fault Tolerance skills. Kubernetes stays skills-listed only. Multi-region, K8s ops, Spark, Flink, and Terraform are **off the resume**.

---

## 1. Ownership and software design / architecture (RESUME-SAFE)

### What recruiters mean
End-to-end ownership = you can answer: who owned the design doc, who set API contracts, who owned the cutover, who owned the rollback, who owned the post-incident fix.

### Map to your work
| Pattern | Your evidence | Defense line |
|---|---|---|
| Owned a platform | Uber FRM Risk Scoping (8 screens, 30+ APIs) | "I owned the recon v2 migration branch and enforced layer boundaries across the pod." |
| Software design and architecture | FRM handler / service / repository / ORM | "Controllers stay thin; services own rules; repositories own SQL." |
| Led design reviews | Led 3 engineers (EPAM) | "I sliced work by layer, reviewed PRs for contract and test gates." |
| Strangler migration ownership | Masters India monolith cutover | "Per-endpoint canary, shared DB first, no dual-write source of truth." |

### Cross-questions
**Interviewer:** What does "owned design and architecture" mean day to day?  
**Candidate:** Design review agenda, API contract freeze before UI, migration plan with rollback, CI quality gates, and being the person who can explain every non-obvious trade-off in the critical path.

**Interviewer:** Amazon asks for years leading design. How do you answer without lying?  
**Candidate:** Do not say 5 years leading design. Say roughly 3 years of leading design reviews and architecture decisions across Masters India (~1.5y) and Uber FRM (~1.9y), with IC ownership at IA.

### Official references
- [AWS Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)
- [Martin Fowler: Patterns of Distributed Systems](https://martinfowler.com/articles/patterns-of-distributed-systems/)
- [microservices.io patterns](https://microservices.io/patterns/index.html)

---

## 2. On-call, incident response, SLOs (PARTIAL RESUME-SAFE)

### Resume-safe wording
Masters India: established ELK + New Relic on-call alerting, cut incident triage ~70% (HISTORICAL; baseline ~30 min to under 10 min is ESTIMATED), coverage 35% to 82%, 98% deploy success.

### Do not claim
Pager rotation ownership, SEV commander title, Netflix-scale error budgets, or Uber Menu Pinot dashboards as on-call proof.

### Concepts to study (Google SRE)
- SLO = service level objective (for example p95 latency, availability).
- Error budget = 100% minus SLO; burn rate drives release freezes.
- Alert on symptoms users feel, not every CPU blip.
- Postmortem: timeline, root cause, blast radius, action items with owners.

### Cross-questions
**Interviewer:** Walk an incident from alert to close.  
**Candidate:** Alert on error rate or p95 spike with request IDs in ELK. Trace one ID across API, worker, and third party. Mitigate first (rollback, open circuit, shed load). Write the incident note with cause and follow-ups. At Masters, correlation IDs were the triage win; I do not invent a formal pager rotation I cannot prove.

### Official references
- [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
- [Google SRE Workbook: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/)

---

## 3. Fault tolerance (RESUME-SAFE at Masters)

### Resume-safe wording
Built fault tolerant bulk paths with idempotency keys, retries, and DLQ replay, plus Redis caching that cut redundant DB reads 30%.

### Patterns you can defend
| Pattern | Why | Your example |
|---|---|---|
| Idempotency key | Retries must not double-register invoices with IRP | `client + fileHash + batchIndex` |
| Exponential backoff + jitter | Flaky government portal | Bounded concurrency on IRP submit |
| Dead-letter queue / state | Park poison batches for operator replay | Bulk import DLQ |
| Circuit breaker | Stop hammering a dead dependency | IRP breaker (prep narrative) |
| Cache-aside + TTL jitter + SETNX | Stampede protection | Redis masters/config cache |

### Cross-questions
**Interviewer:** Why not exactly-once end to end?  
**Candidate:** Across a government portal you get at-least-once plus idempotency. Exactly-once needs a shared transactional sink; IRP is outside your transaction boundary.

### Official references
- [AWS Reliability: Fault isolation](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_fault_isolation_multiaz_region.html)
- [Google SRE: Handling overload](https://sre.google/sre-book/handling-overload/)

---

## 4. Multi-region / HA / DR (`STUDY ONLY - NOT RESUME EXPERIENCE`)

### Why it is off the resume
No personal multi-region ownership in source material. IA CDC docs mention active-active / disaster recovery goals for a tool authored by Ashvin Sharma. Do not claim you built multi-region HA.

### Study map (whiteboard fluency)
```
Client
  │
  ├─ Region A (active) ── DB primary + replicas
  │
  └─ Region B (passive or active) ── replica / second primary
         │
         └─ DNS / GSLB failover + data replication lag budget
```

Trade-offs to recite:
- Active-passive: simpler consistency, longer failover.
- Active-active: lower RTO, harder conflict resolution.
- RPO = data you can lose. RTO = time to recover.
- Multi-AZ is not multi-region. AZ failure != region failure.

### Cross-questions
**Interviewer:** Have you operated multi-region production?  
**Candidate:** No. I can design for it: define RPO/RTO, choose async vs sync replication, and test failover. My production reliability work was single-region SaaS with fault-tolerant bulk paths and observability.

### Official references
- [Kubernetes multiple zones](https://kubernetes.io/docs/setup/best-practices/multiple-zones/)
- [AKS multi-region models](https://learn.microsoft.com/en-us/azure/aks/reliability-multi-region-deployment-models)
- [GCP Architecture Framework: Reliability](https://cloud.google.com/architecture/framework/reliability)

---

## 5. Kubernetes operational depth (`STUDY ONLY` beyond skills keyword)

### Resume boundary
Kubernetes appears on the skills line historically. There is no kubectl/helm/operator production narrative in your material. Do **not** say "operated production clusters."

### Study topics for infra interviews
- Pod, Deployment, Service, Ingress, ConfigMap, Secret.
- Requests/limits, HPA, PDB, readiness vs liveness.
- Control plane HA, etcd, multi-AZ worker pools.
- Rollout strategies: rolling, blue/green, canary.
- Failure modes: CrashLoopBackOff, OOMKilled, image pull backoff, network policy blocks.

### Cross-questions
**Interviewer:** How deep is your Kubernetes experience?  
**Candidate:** Containerized services with Docker and listed Kubernetes familiarity. I have not owned cluster upgrades or operators. For Masters and Uber work I can defend service design, health checks, and deploy gates; cluster control-plane ownership is not my claim.

### Official references
- [kubeadm HA](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)
- [Kubernetes production best practices](https://kubernetes.io/docs/setup/best-practices/multiple-zones/)

---

## 6. Terraform / IaC (`STUDY ONLY - NOT RESUME EXPERIENCE`)

### Why off the resume
No Terraform modules, state files, or IaC ownership in your material.

### Study topics
- Providers, resources, modules, remote state, workspaces.
- Plan/apply, drift, import, destroy safety.
- Secrets: do not store them in state plaintext; use secret managers.
- Idempotent infra changes vs snowflake servers.

### Cross-questions
**Interviewer:** Did you manage infra with Terraform?  
**Candidate:** No production Terraform ownership. I can explain plan/apply and remote state, and I owned application deploy quality (CI gates, 98% deploy success) rather than cloud account IaC.

### Official references
- [Terraform language](https://developer.hashicorp.com/terraform/language)
- [AWS EKS Terraform resource](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eks_cluster)
- [GKE Terraform resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_cluster)

---

## 7. Spark (RESUME on Uber Menu; study extras below)

### Resume claim
Uber Menu: Spark for **batch backfills / reprocess** after Selenium→Kafka→Flink online path. Volume ~1–2M item rows ESTIMATED per typical reprocess window. See `14_uber_menu_deep_dive.md`.

### Extra study (beyond resume bullet)
- Driver vs executors, partitions, shuffle, skew, AQE.
- Structured Streaming micro-batches vs continuous (on this resume Flink owns online).
- When Spark beats a warehouse OLAP engine and when ClickHouse wins for interactive analytics (IA story).

### Bridge
"Menu Spark is ETL/backfill. IA ClickHouse is interactive OLAP POC. Databricks pure runtime roles: lead Menu Spark + CH judgment; do not invent Delta Lake ownership."

### Official references
- https://spark.apache.org/docs/latest/cluster-overview.html
- https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html

---

## 8. Flink (RESUME on Uber Menu; study extras below)

### Resume claim
Uber Menu: Flink for **online normalize / dedupe / route** on Kafka (~200–500 peak events/sec ESTIMATED). Event-time, keyed state, checkpoints. See `14_uber_menu_deep_dive.md`.

### Extra study
- Event time vs processing time, watermarks, keyed state.
- Checkpoints, savepoints, exactly-once sinks.
- Backpressure and operator chaining.
- Flink vs Kafka Streams vs Spark Structured Streaming trade-offs.

### Bridge
"Masters India Kafka is e-invoice async without a Flink claim. Menu is where Flink sits."

### Official references
- https://nightlies.apache.org/flink/flink-docs-stable/
- https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/ha/overview/
- https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/

---

## 9. Design patterns (RESUME SKILL + verbal depth)

### Patterns you can name from your projects
| Pattern | Where |
|---|---|
| Strangler Fig | Masters monolith migration |
| Layered / Repository | FRM handler-service-repository |
| CQRS (verbal, not resume bullet) | IA Order Batching PG writes / CH reads |
| Cache-aside | Masters Redis |
| Idempotent consumer | Masters bulk IRP |
| Parallel run / expand-contract | FRM recon v1 + v2 endpoints side by side |

### Cross-questions
**Interviewer:** Give one design pattern and the trade-off.  
**Candidate:** Strangler vs rewrite. Strangler keeps filing day safe with per-endpoint rollback, at the cost of temporary dual stacks and gateway complexity. Rewrite is cleaner long-term but unacceptable for compliance deadlines.

---

## 10. Mock interviewer loop (hardest combined questions)

**Q1:** Sell me on your ownership in 60 seconds without buzzwords.  
**A:** At Uber FRM I owned recon v2 end to end: schema, repository, service, handlers, tests, and the cutover from Sheets. At Masters I owned the strangler migration plan, mentored two engineers through canaries, and owned the bulk path that hit 1M+ daily transactions.

**Q2:** Where is fault tolerance in your stack, with numbers?  
**A:** Masters bulk e-invoicing: 100K+ per import, ~12 TPS average and 100+ peak estimated, 700 to 4,000 RPM. Idempotency keys stop double IRP registration. Retries with backoff absorb portal flakes. DLQ holds poison batches. Redis cut redundant reads 30%.

**Q3:** Why should PlanetScale / Netflix care if you lack multi-region and Terraform?  
**A:** Because I can prove production ownership of data correctness, sharding, throughput, latency, and alerting. Multi-region and Terraform are study-ready; I will not invent cluster or IaC ownership. My closest HA story is fault-tolerant bulk processing and observability, not geo failover.

**Q4:** Spark vs ClickHouse for AssortSmart analytics?  
**A:** Interactive planner metrics with sub-second probes and high insert rates fit ClickHouse (measured 3.86s vs multi-minute PG, 5.9M rows/s inserts). Spark fits large offline ETL and ML feature generation across object storage. I own the CH POC path; Spark remains study-only for me.

**Q5:** How do you answer Kubernetes depth without failing the screen?  
**A:** Honest scope: Dockerized services, Kubernetes listed as familiarity, no claim of operating control planes. Pivot to deploy quality, health checks, and rollback stories from CI and canary cutovers.

---

## 11. Company targeting cheat sheet

| Company | Lean on | Do not invent |
|---|---|---|
| Google / Amazon | Ownership, design reviews, latency, on-call alerting | 5y leading design, multi-region |
| Microsoft | Backend + agentic + cloud | Azure-only depth |
| Airbnb | Java track for App Foundation; Kafka + scale | Kotlin unless true |
| PlanetScale | Go track, MySQL/PG, sharding, TPS/RPS, Linux | Vitess internals, DB engine work |
| Databricks | ClickHouse/analytics + distributed design | Production Spark ownership |
| Netflix | HA language, on-call alerting, p95 | Netflix-scale blast radius |
| Roku / Rubrik | Skip hard YoE gates; study K8s/Terraform only | Fake infra ownership |
