# Role targeting + rapid-fire defense (checked against live listings, Jul 13 2026)

The resume was scored at 100% keyword coverage against these five live listings. This file tells you **which parts of your story to lead with per role family**, and gives rapid-fire answers for every operational claim on the resume.

## 1. The five target listings and what each actually screens for

| Listing | What they screen for | Lead with |
|---|---|---|
| Google mid-level SWE (SWE III / Senior, search page quals) | Languages + DSA, testing/launching products, 1–3 yrs design & architecture, large-scale distributed systems | IA architecture story (agentic service + Go backend + ClickHouse write model), then Uber scale numbers. Expect heavy DSA + system design rounds — the resume only gets you in the door. |
| Airbnb Senior SWE (Quality), Payments — 7668022, Bangalore | Test automation, CI/CD integration, debugging, DSA, testability advocacy, payments/financial domain | Masters India (financial compliance, coverage 35→82%, pytest gating CI/CD releases) + Uber FRM (audit-grade correctness, changed-module coverage 100%, PwC work papers). You have a genuinely strong quality narrative — financial data where correctness is audited. |
| Airbnb Senior SWE, Global Markets (Backend) — 7768472 | Large-scale backend architecture, APIs, scalable data models, high-throughput pipelines, metrics-driven iteration | Uber Menu (Kafka/Flink/Spark pipeline, 30K+ menus/mo) + IA planning grid backend (p95 targets) + GST (1M+ txn/day). Note: posting is China-based, no visa support — treat as a template for the role family. |
| Airbnb Senior SWE, Reliability Engineering — 8026696 | SRE tooling, incident response, monitoring/alerting, Docker/K8s, AWS/GCP, Go/Python | Masters India observability story (ELK + New Relic with alerting, triage 70% faster) + Menu ingestion health dashboards on Pinot + Go services (context timeouts, graceful shutdown = reliability thinking). |
| Airbnb Senior SWE, Reliability Experience — 8026735 | Internal tooling, observability UX, dashboards, Grafana, async programming, developer productivity | Pinot ingestion health dashboards (built FOR operators — that's an internal tool), ELK/New Relic rollout as a productivity story (what did triage look like before/after), Grafana in skills. |

## 2. Rapid-fire: defending every operational/quality claim on the resume

**"You claim incident triage got 70% faster. How did you measure that?"**
Before: a support escalation meant SSH-ing into boxes and grepping app logs across services — median time to find the failing request was over an hour. After centralized ELK (structured JSON logs, correlation IDs, per-service indexes) plus New Relic APM with alert policies on error rate and latency, the same lookup is a filtered query — minutes. The 70% is the change in median time-to-root-cause on escalated tickets across a quarter.

**"What does 'pytest automated tests gating CI/CD releases' mean concretely?"**
The pipeline blocks merge/deploy if the test suite fails or coverage drops below threshold on changed modules. Tests are the unit + integration suite (httpx test client against FastAPI apps, DB fixtures on a throwaway schema). Coverage went 35% → 82% because we wrote tests module-by-module as we extracted services from the monolith — each extraction PR had to land with its tests.

**"How do you design for testability?"** (Payments Quality will ask this)
Three habits: (1) dependency boundaries as interfaces — repositories and external clients injected, so handlers test against fakes; (2) deterministic cores — pure functions for business rules (tax computation, dedup rules) that test without I/O; (3) contract-first APIs — Pydantic/validator schemas mean malformed input is rejected at the boundary and tests enumerate the contract, not the implementation. At Uber, Bazel + the changed-module coverage rule enforced this: you can't merge untested logic.

**"Tell me about an incident you handled."**
Use the Masters India peak-window story: GSTR filing deadline, worker pool exhaustion from blocking government-portal calls. Walk detection (New Relic latency alert), mitigation (shed bulk imports to the async queue, scale workers), root cause (sync I/O in request path), permanent fix (async workers + idempotent retries so replays are safe), and the lesson (capacity planning around deadline-shaped traffic, alerts on saturation not just errors).

**"What's 'idempotent retries' protecting against?"**
Duplicate side effects on replay. Bulk e-invoice imports chunk into jobs; each job carries a deterministic key (import id + chunk index + content hash). On retry after a crash or timeout, already-committed chunks are recognized and skipped — so a retry storm can't double-register invoices with the government portal. Same pattern in the IA bulk-save path (batch id + content hash prevents double-inserting versions).

**"How would you monitor a service you own?"** (Reliability roles)
Four layers: RED metrics per endpoint (rate, errors, duration — p50/p95/p99, not averages); saturation metrics (worker pool depth, queue lag, DB connections); structured logs with correlation IDs so a trace ties the layers together; and alerts on symptoms users feel (error rate, p95 breach, queue age) rather than causes, with runbooks per alert. That's the shape I set up with ELK + New Relic and what the Pinot ingestion-health dashboards did for the menu pipeline — per-source success rate, failure taxonomy, detection in minutes instead of the next morning.

**"What made the Pinot dashboards an internal product?"** (Reliability Experience)
The users were ops and vendor-onboarding teams, not customers. Before: failures discovered when a partner complained. After: real-time ingestion health by source, drill-down to failure class (auth, layout change, blocking), and time-to-detection in minutes. The design decisions were UX decisions — what the operator needs to see first, what's actionable vs noise — which is exactly the Reliability Experience pitch: observability tooling is a product with engineers as customers.

## 3. The two claims interviewers will poke hardest, and the honest lines

- **IA latency numbers (p95 <500 ms, <80 ms edits):** "Those are the committed design targets from our platform architecture NFRs — the numbers the serving layer is engineered and load-tested against, not yet year-in-production measurements. The architecture that delivers them: pre-aggregated ClickHouse serving reads so the grid never hits the transactional path, and optimistic write-back so the UI acknowledges before the async commit."
- **Menu $600K+/yr saving:** cost model from onboarding-hours saved × ops hourly cost at 30K menus/month — the finance team's number, adopted by the team. Know the arithmetic before you quote it.

## 4. If the interviewer is Google (mid-level loops)

- The resume gets you the screen; the loop is DSA (2 rounds), system design (1), Googliness (1). Design round: pick the **planning grid backend** or the **menu ingestion pipeline** as your prepared "tell me about a system you built" — both have clean load numbers, storage choices, and failure-mode stories.
- Googliness maps: use STAR story 1 (reconciled ClickHouse verdict — intellectual humility), story 4 (clustering copilot — ambiguity), story 5 (constants-refactor regression — owning mistakes).
- Mid level at Google = "drives progress, solves problems, mentors juniors." Sprinkle the mentoring evidence: PR reviews at Uber (stacked PRs culture), onboarding EPAM teammates, GFG interns.
