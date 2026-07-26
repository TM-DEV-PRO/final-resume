# Amazon Technical Recruiter Screen

## Typical titles and levels

| Target title (posting) | Internal level | YoE pattern on public postings (2025–2026) | Fit for this candidate |
|---|---|---|---|
| Software Development Engineer II | SDE II | 3+ YoE SWE; 2+ design/architecture | **Primary target** — strong match |
| Software Development Engineer III | SDE III | 5+ YoE; 5+ leading design/architecture; mentor/TL | **Stretch / selective** — only if design ownership + leadership is front-and-center |
| Senior SDE / SDE III (specialist: storage, EKS, ads, etc.) | SDE III | Same bar + domain keywords | Stretch unless domain match is explicit |

**Practical targeting:** Apply and pitch **SDE II** as the honest default. Discuss SDE III only for teams where FRM-style design ownership + leading 3 reads as “led design of new/existing systems,” not just senior IC title at a vendor/client.

**Title translation recruiters use:** “Senior Software Engineer” at Impact Analytics ≈ SDE II–III depending on scope evidence. Uber (via EPAM) “Software Engineer / SDE2” maps cleanly to SDE II.

---

## Hard requirements recruiters check

### Years of experience
- SDE II: **3+** non-internship SWE (you clear at ~5y).
- SDE III: **5+** SWE **and** **5+ leading design/architecture** wording on many postings — recruiters parse this as multi-year architecture ownership, not “I designed one feature.”
- Degree: CS/related or equivalent experience (usually soft gate).

### Languages
- At least one of: **Java, Go, C++, Python** (stated repeatedly on amazon.jobs).
- Your **Python + Go** pair clears the language gate for most backend/distributed postings.
- Weakness: Java/C++ heavy teams may still screen-in if you show production systems depth; do not claim Java fluency you do not have.

### Systems / stack signals they keyword-scan
- Distributed systems, reliability, scaling, design patterns
- Event-driven / messaging (Kafka, SQS, Kinesis — team-dependent)
- Cloud (AWS strongly preferred on many teams; transferable cloud OK for some)
- Containers / K8s (bonus on platform teams; omit fake ops ownership)
- Observability, on-call, operational excellence
- Mentorship / tech lead / “leading an engineering team” (harder gate for SDE III)

### Leadership
- SDE II: evidence of owning features/systems, code review, mentoring juniors is enough.
- SDE III: explicit **mentor / tech lead / led engineers** + architecture ownership over time.

---

## Keyword bank (2025–2026 public posting patterns)

**Must-hit (ATS + recruiter skim):**
`software development`, `Python`, `Go` / `Golang`, `distributed systems`, `scalable`, `design patterns`, `architecture`, `reliability`, `high availability`, `REST APIs`, `microservices`, `code reviews`, `mentoring`

**Strong differentiators for backend / data-ish roles:**
`Kafka`, `event-driven`, `idempotency`, `retries`, `dead-letter` / `DLQ`, `PostgreSQL` / `MySQL`, `ClickHouse` (analytics/OLAP teams), `FastAPI`, `Gin`, `observability`, `Datadog` / `New Relic` / `ELK`, `CI/CD`, `production ownership`

**Amazon-flavored preferred (use only if true):**
`AWS`, `DynamoDB`, `SQS`, `SNS`, `Kinesis`, `Lambda`, `EKS` / `Kubernetes`, `Terraform` / `CloudFormation`, `operational excellence`, `incident management`

**Leadership / bar-raiser language:**
`tech lead`, `design reviews`, `API contracts`, `cross-team`, `ownership`, `delivered ambiguous projects`

**Avoid inventing:** multi-region active-active DR ownership, K8s cluster ops, Terraform production ownership — if not evidenced.

---

## Pass vs borderline vs fail (this candidate)

**Profile assumed (honest):** ~5y Python/Go; FastAPI/Gin; Kafka (Masters GST path); ClickHouse (IA); owned FRM design at Uber via EPAM; led 3 (EPAM pod); mentored 2 (Masters); agentic AI at Impact Analytics. No invented TPS/RPM beyond what you can defend.

### Pass (likely screen-in) — SDE II
- Resume header + summary: **Python, Go, distributed systems, ownership** in first 5 lines.
- Uber FRM: **owned design / layered architecture / 30+ APIs / MySQL** — reads as design + delivery.
- Masters: **Kafka + FastAPI + scale language** (1M+/day, idempotency/DLQ) — systems keywords.
- Leadership line present: **led 3**, **mentored 2** (separate employers, clear).
- Recruiter phone: can map one story to **Customer Obsession / Ownership / Dive Deep** without fluff.

### Borderline
- Applying as **SDE III** with only ~5y and vendor/client framing (“via EPAM”) — recruiters may push to SDE II or reject for “5+ years leading design.”
- Agentic AI / LangGraph emphasized **instead of** systems reliability — AI teams may love it; classic SDE teams may shrug.
- ClickHouse without explaining **why** (append-only analytics, latency) — looks niche/tool-chasing.
- No AWS keywords on cloud-heavy reqs — still passable for many SDE II roles if systems story is strong; weaker for AWS org roles.

### Fail (common recruiter kills)
- Inflating to **SDE III Principal-like** scope or claiming Amazon-scale numbers you cannot defend.
- “Led a team” without headcount or sounding like people-manager when you were pod lead.
- Resume that reads as **services company / body shop** only — fix by leading with **Uber product problem** and ownership, EPAM as employment vehicle.
- Missing any production language match and no systems design signal.
- Keyword stuffing Terraform/K8s/multi-region without ownership.

---

## Highest-impact honest resume flips (no fake years)

1. **Lead with product + ownership, not employer brand alone:** “Owned design & delivery of Uber FRM Risk Scoping (FastAPI, MySQL, 30+ APIs…) via EPAM” — EPAM secondary.
2. **Make SDE II / senior IC scope explicit:** one line: design reviews, API contracts, CI gates for pod of 3.
3. **Kafka on Masters, not vague “streaming everywhere”:** put Kafka + idempotency/DLQ next to GST e-invoice throughput you can defend.
4. **ClickHouse as systems decision:** “append-only planning store; measured pivot speedup on 250M grids” — one measured claim, not a CH résumé.
5. **Agentic AI as production engineering:** tools, human gates, observability (LangSmith/Datadog) — not “built a chatbot.”
6. **Operational excellence crumbs:** Masters ELK/New Relic on-call; IA Datadog — Amazon loves ops mindset.
7. **Do not add years** or backdate titles; map titles: SDE2 / Senior SWE → Amazon SDE II.
8. **Optional AWS bridge (honest):** if you used any AWS/GCS-adjacent cloud concepts, say cloud object storage / managed services carefully — never invent AWS certs or deep AWS ownership.

---

## Culture / behavior screen notes (Leadership Principles)

Recruiters and bar-raisers listen for **LP-tagged stories**, not buzzwords.

| LP | How this profile can answer (honest) |
|---|---|
| **Customer Obsession** | FRM: auditors/PwC work papers; IA: retail planners’ time-to-config |
| **Ownership** | Recon Sheets→MySQL migration personally owned; pod design reviews |
| **Dive Deep** | ClickHouse POC numbers; FRM schema/API correctness; GST fault-tolerance path |
| **Deliver Results** | Masters p95 / throughput / coverage improvements you can defend |
| **Hire and Develop the Best / Earn Trust** | Mentored 2; led 3 via contracts and CI — growth of others |
| **Insist on the Highest Standards** | ~1125 tests on FRM; CI gates; audit correctness bar |
| **Bias for Action** | Shipping migrations under constraints (Sheets→MySQL; PHP→FastAPI) |
| **Are Right, A Lot / Think Big** | Use carefully — trade-off stories (OLTP vs OLAP, agent read-only) beat slogans |
| **Frugality** | Menu cost narratives only if you can defend finance model; else skip |
| **Learn and Be Curious** | Python→Go; agentic stack; CH for planning analytics |

**Phone-screen tips:** Name the LP once after the story, not as a preface. Prefer **STAR with a metric you own**. Avoid blaming Uber/EPAM/IA. For “why Amazon”: ownership at scale + operational bar — not compensation.

**Level risk on behavior:** SDE III expects **broader org impact** stories. Stick to SDE II behavioral scope unless you have cross-org influence evidence.
