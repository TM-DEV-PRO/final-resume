# Senior Software Engineer (~5 YoE) — Persona Expectations

**Profile in scope:** Python/Go backend · distributed systems · agentic AI / LLM production systems  
**Level calibration:** Big-tech Senior IC (Google L5 / Meta E5 / Amazon SDE II–III edge / Stripe/OpenAI “Senior”) — scope over years; ~5 YoE is common floor, not the bar.  
**Sources synthesized:** Big-tech interview bars (Amazon Bar Raiser / SDE3, OpenAI L5, FAANG system-design weight), senior JD templates used across hundreds of hires, backend ATS keyword practice (2025–2026), agentic AI production JDs (runtime, orchestration, MCP, evals).

**How to use this doc:** Each persona reads your resume at three depths. Optimize so the **6-second scan** clears the gate, the **30-second read** earns a phone screen, and the **deep-read** survives hiring-committee scrutiny.

---

## Shared senior bar (all personas)

At big tech and strong product companies, “Senior” means:

| Dimension | Mid-level | Senior (~5 YoE bar) |
| --- | --- | --- |
| Ambiguity | Executes a scoped ticket | Frames the problem; owns scoping |
| Ownership | Feature / PR | Multi-quarter outcome: design → ship → operate |
| Blast radius | Own service / squad | Cross-team contracts, platform, or domain |
| Judgment | Implements the chosen design | Names tradeoffs, rejects bad options, documents ADRs/RFCs |
| Multiplication | Improves own craft | Raises review bar; mentors; unblocks peers |
| Ops | Fixes bugs when assigned | Owns SLOs, incidents, postmortems, on-call |

**Three resume inferences every senior page must support:** (1) decision weight under ambiguity, (2) measurable consequence, (3) “I” ownership that would still read senior if the title were removed.

---

## 1. CTO

### 6-second scan
- Title + YoE + stack match (Senior · Python/Go · backend/distributed/AI infra).
- One line of **judgment + leverage**: architecture owned, team multiplied, or business risk reduced — not a tech laundry list.
- Credible company/scale context (users, QPS, $ impact, or hard domain) near the top.

### 30-second read
- Evidence you can **decide what to build and how**, not only how to implement.
- At least one story of **saying no / choosing a cheaper simpler path / reversing a bad bet**.
- Communication signal: design docs, RFCs, partnering with product — readable by a non-coding founder or board-aware CTO.

### Deep-read criteria
- Technical strategy taste: build-vs-buy, when to introduce complexity (queues, multi-agent, new datastore), when not to.
- Ability to connect engineering to **product velocity, cost, reliability risk, and hiring/bar culture**.
- For agentic AI: treats LLMs as unreliable components inside a system (evals, guardrails, cost/latency budgets) — not demo theater.
- Intellectual honesty: what failed, what you’d redo, what you still don’t know.

### Must-have signals
- Owned a non-trivial system or initiative end-to-end with explicit tradeoffs.
- Cross-functional influence without authority (product, infra, security, another eng team).
- Quantified outcomes (latency, reliability, cost, time-to-ship, incident MTTR).
- Mentorship or bar-raising (reviews, hiring loop, standards) — even informally.
- Production AI/agents framed as **reliability + observability + cost**, not “prompted GPT.”

### Reject signals
- Feature factory bullets (“built REST APIs,” “worked on microservices”) with no decisions.
- Buzzword soup (Kubernetes + Kafka + RAG + agents) with zero operational consequence.
- Overclaiming staff/principal scope (org-wide strategy) without artifacts or blast radius.
- Pure LeetCode / academic framing with no production ownership.
- “We” everywhere; no personal decision weight.

---

## 2. Director of Engineering

### 6-second scan
- Clear **domain ownership** (payments, platform, data plane, agent runtime, etc.).
- Delivery + reliability language: multi-quarter project, rollout, SLO, migration — not only “built.”
- Team-fit keywords: mentorship, design review, cross-team, on-call.

### 30-second read
- Can this person **absorb a workstream** and reduce director attention tax?
- Predictable shipping: migrations, phased rollouts, feature flags, backwards-compatible APIs.
- Collaboration: unblocking other teams, clear interfaces, written plans.

### Deep-read criteria
- Capacity and planning literacy: estimates with uncertainty, dependency management, risk callouts.
- Operational maturity: SLOs/error budgets, incident roles, postmortem quality.
- Org hygiene: raises code/design review quality; grows mid-levels toward senior.
- For distributed + AI systems: understands **operational cost of complexity** (more services, more agent tools = more failure modes).

### Must-have signals
- Led delivery of a multi-person or multi-quarter effort (tech lead of the work, even without title).
- Measurable reliability or efficiency wins (p99, error rate, cost/QPS, deploy frequency).
- Mentored or coached engineers; improved team throughput or quality.
- Written design/RFC that other teams consumed.
- Comfortable with production ownership (on-call, incident response).

### Reject signals
- Heroics-only narrative (weekend fire drills) with no prevention or systemic fix.
- No evidence of working through others — only individual coding velocity.
- Unscoped “led team of N” without outcomes (looks like inflated title).
- Job hopping framed as growth without cumulative ownership depth.
- Ignores operational reality (never mentions rollout, monitoring, rollback).

---

## 3. Engineering Manager (EM)

### 6-second scan
- Will this person **raise the team bar** and need low supervision?
- Stack fit for the squad (Python and/or Go backend + distributed systems keywords).
- Soft-hard combo: ownership + mentorship + collaboration in the first screenful.

### 30-second read
- Independence: proposes work, scopes it, ships without a tech lead translating product → eng.
- Team citizen: code review quality, pairing, onboarding, knowledge sharing.
- Conflict and communication: can disagree professionally; can explain tradeoffs to PM/design.

### Deep-read criteria
- Behavioral depth (Amazon LP-style / Google “Googleyness” adjacent): ownership, bias for action, disagree-and-commit, learn from failure — with **specific numbers and counterfactuals**.
- Technical depth sufficient that the EM trusts them as the team’s senior IC on design and incidents.
- Coaching instinct: how they made someone else better (not only how they got better).
- Scope honesty: clear “I owned X; team owned Y.”

### Must-have signals
- End-to-end project ownership with design + implementation + production health.
- Mentorship of 1–3+ engineers (reviews, design guidance, career/skill growth).
- Incident or production debugging story with root cause and prevention.
- System design fluency visible on the page (consistency, idempotency, failure modes — via bullets, not a buzzword list).
- Partnering with PM on scoping and cutting scope under deadline.

### Reject signals
- “Responsible for…” duty lists; no impact.
- Blame-heavy or lone-wolf framing (“fixed everyone else’s mess”) without collaboration.
- Claims of management (“managed 5 engineers”) on an IC resume without clarifying tech lead vs people manager — confuses leveling.
- No mentorship or review signal at ~5 YoE senior.
- Cannot separate personal contribution from team (“we shipped the platform”).

---

## 4. Hiring Manager (HM)

*Often the EM or a senior EM/Director who owns the req. Distinct lens: “Will I stake my headcount on this person?”*

### 6-second scan
- Exact role match: Senior Backend / Distributed Systems / AI Platform — title alignment.
- Strongest 1–2 bullets of **recent** role scream the job’s pain (latency, migrations, agents, scale).
- Clean, scannable layout; quantified impact in the first role block.

### 30-second read
- Risk check: can they ramp in weeks on our stack? (language depth + adjacent systems beat perfect framework match.)
- Evidence of **the hard problem this team has** (e.g., stateful agent runtime, Kafka backpressure, Postgres at limit, multi-tenant isolation).
- Trajectory: increasing scope across roles, not lateral ticket closing.

### Deep-read criteria
- Interviewability: bullets that map to probeable STAR stories (ambiguity, conflict, failure, scale, tradeoff).
- Level calibration: senior IC scope, not staff-inflated claims that will fail the bar-raiser / hiring committee.
- Reference-ready specificity: names of systems, metrics before/after, your decision, blast radius.
- For agentic AI reqs: production path (tool calling, durable execution, evals, sandboxing, MCP) vs courseware.

### Must-have signals
- Domain-relevant wins with metrics (latency/throughput, reliability, migration success, cost).
- Architecture ownership in at least one bullet (you chose the shape; others built on it).
- On-call / production ownership signal.
- Mentorship or interview-loop participation (optional but strong).
- Clear stack: Python and/or Go with supporting distributed systems vocabulary used in context.

### Reject signals
- Keyword stuffing that doesn’t match narrative depth (ATS bait the HM will smell in screen).
- Gaps between claimed level and evidence (Senior title, junior bullets).
- Only CRUD/API work when the req is distributed systems / agent infra.
- Inflated metrics without mechanism (“improved performance 10x” with no how).
- Resume that could belong to any mid-level at any company after removing the title.

---

## 5. Technical Lead (Tech Lead / Staff-adjacent interviewer)

### 6-second scan
- Depth markers: consistency models, idempotency, backpressure, schema evolution, p99, SLO — used as **outcomes**, not glossary.
- Proof of design ownership: “designed,” “RFC,” “migrated,” “decomposed,” “hardened.”
- Language credibility: idiomatic Python (async, typing) and/or Go (concurrency, profiling) tied to real systems.

### 30-second read
- Would I trust their design review comments next week?
- Failure-mode thinking visible: retries, poison messages, partial failure, rollout/rollback.
- Data path literacy: Postgres/Redis/Kafka (or equivalent) with query/partition/consumer-group reality.

### Deep-read criteria
- System design seniority: clarifies requirements, estimates load, picks consistency intentionally, discusses operational complexity.
- Code taste implied by bullets: API contracts, observability, testing strategy for distributed and non-deterministic (LLM) components.
- Agentic AI: state/leases/checkpoints, tool sandboxing, streaming, eval harnesses, cost/latency controls — systems engineering, not prompt lists.
- Ability to simplify: removed a service, collapsed a queue, avoided premature multi-agent complexity.

### Must-have signals
- At least one **hard systems** bullet: sharding/partitioning, exactly-once/idempotent processing, multi-region, backfill/migration, hot-path latency work.
- Observability ownership: metrics/traces/logs → detected or diagnosed production issue.
- Performance work with numbers (p50/p99, QPS, CPU/mem, cost).
- Cross-service contract design (API/protobuf/event schema) with compatibility story.
- Mentorship via design/code review (peer technical multiplication).

### Reject signals
- Framework tourism without production constraints.
- Distributed systems buzzwords with monolith-CRUD evidence only.
- “Implemented Kafka” with no consumer failure/ordering/backpressure story.
- AI bullets that stop at LangChain wrappers / demos / hackathon.
- No mention of testing, rollout, or observability on backend work.

---

## 6. Technical Recruiter

### 6-second scan (ATS + human skim)
- Title match: “Senior Software Engineer” (or equivalent) in headline and recent role.
- Tier-1 keyword coverage for the req: `Python`, `Go`/`Golang`, `distributed systems`, `system design`, plus role-specific (`gRPC`, `Kafka`, `Kubernetes`, `PostgreSQL`, `LLM`/`agents`/`MCP` as applicable).
- Location/eligibility/YoE readable immediately; no puzzle formatting.

### 30-second read
- Checklist hire: years ≈ 5+, backend focus, relevant company type, no obvious red flags.
- Skills section + first bullets echo the JD’s must-haves (not a 50-item dump).
- Impact numbers present (recruiters use them to sell the HM).

### Deep-read criteria
*Usually shallow — but strong recruiters and sourcers do a second pass:*
- Boolean/search hits: seniority + stack + domain (e.g., `(Python OR Go) AND (distributed OR microservices OR Kafka) AND (Senior OR "tech lead")`).
- Narrative coherence: AI/agent experience is backend/production, not “ChatGPT user.”
- Comp/level story: senior IC trajectory; no conflicting titles that force downgrade.
- Easy to pitch: one-sentence value prop the recruiter can paste to the HM.

### Must-have signals
- Explicit senior title + ~5 YoE.
- Python and/or Go listed and evidenced in bullets.
- Distributed systems / backend / cloud keywords with at least one quantified achievement.
- Clean contact + LinkedIn; consistent dates.
- For agentic roles: `agents`, `LLM`, `tool calling`, `RAG`, `MCP`, `evals`, or `orchestration` appearing near production verbs (`shipped`, `scaled`, `on-call`, `latency`).

### Reject signals
- Missing must-have keywords from the JD (silent ATS rank drop).
- Full-stack/frontend-heavy resume for a backend distributed req.
- Creative formatting that breaks ATS (tables, icons, multi-column text as images).
- Vague summaries (“passionate engineer”) with no stack or scope.
- Title mismatch (“Software Engineer” only when filtering Senior) without senior scope language to compensate.
- Job descriptions copied as duties; no metrics → hard for recruiter to advocate.

---

## Shared senior bar checklist — Python/Go backend

Use as a resume self-audit. Aim to **show evidence**, not claim the checkbox.

### Scope & ownership
- [ ] Multi-quarter or multi-person initiative owned end-to-end (problem → design → ship → operate)
- [ ] Explicit tradeoff or decision you owned (not just implementation of someone else’s design)
- [ ] Blast radius beyond a single ticket (team, multi-service, platform, or customer-facing reliability)

### Python / Go depth
- [ ] **Python:** production services (e.g. FastAPI/async), typing, performance/GIL awareness where relevant, packaging/testing
- [ ] **Go:** concurrency (goroutines/channels/context), API/gRPC services, profiling (`pprof`) or performance tuning evidence
- [ ] Comfort stated honestly: strong in one, productive in the other — or deep in one with clear ramp signal

### Distributed systems
- [ ] Data stores used under load (Postgres and/or Redis/Kafka/etc.) with a real constraint named
- [ ] Failure modes: retries, idempotency, timeouts, partial failure, poison messages, backpressure
- [ ] Consistency choice stated or implied (strong vs eventual) with why
- [ ] API/event contract evolution (versioning, compatibility, schema discipline)

### Performance & reliability
- [ ] Latency and/or throughput metrics (p99, QPS/RPS, SLA/SLO)
- [ ] Observability: metrics, logs, traces → action taken
- [ ] On-call or incident leadership with root cause + prevention
- [ ] Rollout strategy: flags, canaries, migrations, rollback

### Agentic AI / LLM systems (when targeting those roles)
- [ ] Production path: tool/function calling, durable/long-running execution, session state, streaming
- [ ] Reliability for non-determinism: evals, guardrails, sandboxing, human-in-the-loop where needed
- [ ] Cost/latency budgets for model calls; caching/compaction/context management
- [ ] Platform seams: MCP/tool APIs, orchestration (queues/workflows), OpenTelemetry on agent runs
- [ ] Avoid: demo-only, prompt-only, or “used ChatGPT” as experience

### Multiplication
- [ ] Mentorship, design/code review bar, or interview loop participation
- [ ] Written design doc / RFC / ADR consumed by others
- [ ] Unblocked peers or other teams via interfaces, tooling, or clarity

### Resume craft (senior inference)
- [ ] Every strong bullet: scope + ambiguity/decision + consequence (metric when real)
- [ ] “I” clarity without erasing collaboration
- [ ] First screenful sells senior backend; skills section supports ATS without stuffing
- [ ] Would still read senior if job titles were removed

---

## Signal → resume theme mapping

Map persona must-haves onto six resume themes. Each theme should appear as **concrete bullets**, not section headers alone.

| Resume theme | What to prove | Highest-value personas | Example signal language (pattern) |
| --- | --- | --- | --- |
| **Architecture ownership** | You shaped the system under uncertainty; others depend on your interfaces | CTO, Tech Lead, HM, Director | Designed X for Y constraint; chose A over B because…; RFC adopted by N teams; defined service boundaries / event schema |
| **Mentorship** | You multiply engineers; raise review/design bar | EM, Director, CTO, Recruiter (keyword) | Mentored N engineers on…; set review bar for…; paired through design of…; onboarded…; interviewed for… |
| **Latency / throughput** | You reason in numbers about hot paths and capacity | Tech Lead, HM, Recruiter, CTO | Cut p99 from A→B; sustained N QPS; reduced tail latency via…; profiled Go/Python path; cache/pool/query plan fix |
| **Migrations** | You ship change safely under compatibility and risk | Director, EM, Tech Lead, HM | Zero-downtime migration; dual-write/backfill; versioned API; strangled monolith; traffic shift with rollback |
| **On-call** | You own production consequences | EM, Director, Tech Lead, HM | On-call for…; incident commander/responder; MTTR; postmortem actions; SLO/error budget; toil reduction |
| **System design** | You can clarify, estimate, trade off, and operate a design | Tech Lead, HM, CTO, Recruiter (keyword) | Idempotent consumers; consistency model; sharding/partitioning; backpressure; multi-tenant isolation; agent session leases/checkpoints |

### Theme coverage matrix (target)

| Theme | CTO | Director | EM | HM | Tech Lead | Tech Recruiter |
| --- | --- | --- | --- | --- | --- | --- |
| Architecture ownership | Critical | High | High | Critical | Critical | Keyword + one bullet |
| Mentorship | High | Critical | Critical | High | High | Keyword |
| Latency / throughput | High | High | Medium | Critical | Critical | Metrics sell |
| Migrations | Medium | Critical | High | High | High | Nice-to-have keyword |
| On-call | Medium | Critical | Critical | High | High | Plus if JD mentions |
| System design | Critical | High | High | Critical | Critical | Tier-1 keyword |

### Placement guidance
1. **Header / summary (6-second):** stack + senior + 1 theme spike (usually architecture + latency or agents-in-production).
2. **Top 2–3 bullets of latest role (30-second):** architecture ownership + latency/throughput or migrations + one multiplication or on-call signal.
3. **Deeper bullets / earlier roles (deep-read):** second systems story, mentorship detail, incident/postmortem, agentic reliability (evals, durable execution).
4. **Skills line (recruiter/ATS):** Python, Go, distributed systems, system design, Postgres/Redis/Kafka (as true), observability, and agent/LLM terms only if evidenced above.

---

## Quick anti-patterns (all personas)

| Anti-pattern | Why it fails senior bar |
| --- | --- |
| Duty list without decisions | Reads mid-level execution |
| Metrics without mechanism | HM/Tech Lead distrust; un-probeable |
| Buzzword inventory | CTO/Tech Lead reject; ATS may pass then human fails |
| Staff-scope claims at ~5 YoE without blast radius | Fails bar-raiser / committee calibration |
| AI demo bullets for production agent reqs | Instant Tech Lead/HM no |
| No ops signal on backend distributed resume | EM/Director assume you create pages |

---

## One-line resume north star

> A Senior (~5 YoE) Python/Go backend engineer **owns ambiguous, multi-quarter systems work** — architecture, measurable performance/reliability, safe change (migrations), production accountability (on-call), and team lift (mentorship) — and, for agentic AI roles, makes **non-deterministic model calls behave like dependable distributed components**.
