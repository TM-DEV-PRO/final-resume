# Interview Prep Index (Final Java + AI (IA = Py/Go))

<div class="callout note">
<b>How to use this page</b>
<ul>
<li>It's the map of the interview_prep folder. Every page is listed with a plain description of what's inside and when to read it.</li>
<li>Read it first when you start a prep session, then follow the suggested order below.</li>
<li>Nothing to memorise here. Memorise from the pages it points to.</li>
</ul>
</div>

**Track:** Final Java + AI (IA = Py/Go), resume `Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf`. Expertise in Java, Python and Go microservices. Uber FRM is Java with Spring Boot, Spring Data JPA and Hibernate. Masters India is Spring Boot microservices. Impact Analytics platform APIs are Go with Gin, and the AI agent code is Python.

**What's on the resume for Impact Analytics.** AssortSmart has two resume sections. *Core Infrastructure and Pipeline* covers the Go platform, the KPI parser, auth and tenant isolation, ClickHouse rollups and the cluster data pump. *Agentic Flows and Orchestration* covers the Keep/Drop decision engine, the orchestration registry, Ask Iris and the evaluation gate. The Cluster Recommendation Copilot and Hindsight are real work but **verbal only, not on the PDF**.

## Suggested study order

1. **Start with the Impact Analytics pack.** It's the job interviewers ask about most.
2. **Read Numbers defense.** Every number, how it was derived, and how to say it.
3. **Read Design decisions.** The "why" behind each system, with alternatives.
4. **Read the Uber pack, then Masters and GFG.**
5. **Before system-design rounds,** read Deployment and scale plus the architecture page for the project you'll lead with.
6. **Use the deep dives** when you have a full evening, or when you expect to be grilled on one project.

---

## Core pages (read these for every loop)

| Page | What's inside | When to read |
|---|---|---|
| [Numbers defense](numbers_defense.md) | Every resume number explained: what it measures, how it was derived, why it mattered, how to say it out loud, and what not to say. Includes the off-PDF numbers you may mention with a caveat | Before any resume walk-through. Re-read the "Don't say" lines on interview morning |
| [Design decisions and trade-offs](design_decisions_tradeoffs.md) | 24 design decisions across all projects. Each has What, Why, How with a small example, Alternatives, Trade-off, and What I'd do differently | Before system-design rounds and "tell me about a technical decision" questions |
| [Deployment and scale](deployment_and_scale.md) | Deployment and scaling concepts explained from zero (canary, rollback, blue-green, autoscaling, rate limiting, circuit breakers, backpressure, caching, sharding, Kubernetes basics), then how each project actually shipped and scaled | Before "how did you deploy this" or "what happens at 10x" questions |

## Project packs (fast, speakable)

| Page | What's inside | When to read |
|---|---|---|
| [Impact Analytics pack](projects/01_impact_analytics.md) | **Start here.** The current role in 30-second, 2-minute and long form. All ten AssortSmart resume bullets decoded, the numbers table, design choices, likely questions, and a "do not say" list | Before every interview |
| [Uber FRM and Menu pack](projects/02_03_uber_frm_menu.md) | Both Uber via EPAM projects in compact form. Part A is the FRM Finance scoping backend. Part B is Uber Eats menu ingestion plus the separate ANZ document compliance project | Day-of refresher, after reading the deep dives once |
| [Masters India and GFG pack](projects/04_05_masters_gfg.md) | Speakable 30-second and 2-minute versions, architecture, each bullet with interviewer probes, mock Q&A, and an honesty box for both earlier jobs | Morning of an interview that will cover earlier roles |

## Project deep dives (full depth, one evening each)

| Page | What's inside | When to read |
|---|---|---|
| [Impact Analytics deep dive](projects/01_ia_deep_dive.md) | Every IA bullet (five Agentic, five Core) from plain English down to code, plus older POC and design material that is verbal depth only. Long | The week before an IA-heavy loop. Sections 1 to 4 the night before |
| [Uber FRM deep dive](projects/02_frm_deep_dive.md) | The finance ideas from zero (materiality, general ledger, line-item hierarchy, SOX), then architecture, each bullet decoded, hard problems, and a large Q&A bank | The week before any loop where Uber via EPAM will come up |
| [Uber Menu deep dive](projects/03_menu_deep_dive.md) | Uber Eats menu ingestion end to end: business problem, Kafka, Flink, RAG with Milvus and Gemini, one menu traced step by step, numbers with arithmetic, and failure scenarios. Also covers ANZ | Before streaming, data-pipeline or GenAI rounds |
| [Masters and GFG deep dive](projects/04_masters_gfg_deep_dive.md) | Full depth behind the Masters bullets (strangler migration, Kafka bulk pipeline, idempotency, caching, observability) and the GFG bullets (Django migration, doubt-support APIs, dashboard, scheduled workflows) | Before backend or system-design loops that go deep on migrations or pipelines |

## Verbal-only and older pages (not resume bullets)

These pages describe real work that isn't on the PDF. Use them only when an interviewer asks about your broader AI roadmap. Some still use older wording. Where they disagree with the resume, the resume wins.

| Page | What's inside | Caution |
|---|---|---|
| [Hindsight defense](projects/01b_hindsight_defense.md) | The Hindsight prior-season decision layer, from its requirements doc | Verbal only. Not a resume bullet |
| [Agent read-tools defense](projects/01c_agent_read_tools_defense.md) | How the clustering copilot's 14 audited tools only read planning data, and why the LLM never gets a raw SQL shell | Verbal only. The 14 tools belong to the Cluster Recommendation Copilot design |
| [Agentic evals and guardrails flow](projects/01d_agentic_evals_guardrails_flow.md) | Older end-to-end flow for the clustering copilot: tools, gates, the 8.5% failure baseline and targets, plus benchmarking honesty | Mostly Copilot-shaped, so verbal only. For the resume's evaluation story (300-case set, 80% gate, 74% baseline) use the IA pack and Numbers defense |

## Architecture pages

[Architecture index](architecture/00_index.md) gives one page per project, all built the same way: a diagram of five to eight boxes, one request traced end to end, the database design, and a 3-minute whiteboard script.

| Page | Covers |
|---|---|
| [Impact Analytics AssortSmart](architecture/01_ia_assortsmart_hindsight.md) | Go/Gin platform, ClickHouse and rollups, the Python agent plane (Keep/Drop and Ask Iris), the cluster copier. Hindsight is a verbal-only section at the end |
| [Uber FRM](architecture/02_uber_frm.md) | Spring Boot service, MySQL schema, one edit traced through optimistic locking, the quarterly close |
| [Uber Menu](architecture/03_uber_menu.md) | Scraping, Kafka, Flink and the RAG extraction path, plus a short ANZ section |
| [Masters India GST](architecture/04_masters_gst.md) | Strangler migration, Kafka bulk pipeline, quarter sharding, idempotency and dead-letter queues |
| [GeeksforGeeks](architecture/05_geeksforgeeks.md) | Doubt-support platform after the Django migration, voting and locking APIs, dashboard, scheduled workflows |

## Technology pages

[Tech depth index](tech_depth/00_index.md) gives one page per technology. Each covers what the technology is, how I used it, trade-offs, failure modes and likely questions. The fullest pages are:

- [ClickHouse](tech_depth/clickhouse.md): MergeTree tables, partitions, ReplacingMergeTree, the rollup layer, the 170 GB out-of-memory fix, the copier and the 2.11B-row master.
- [Go and Gin](tech_depth/go_gin.md): goroutines, context, middleware, timeouts, HTTP/2, Wire, and how the IA platform used them.
- [Kafka](tech_depth/kafka_streaming.md) and [Flink](tech_depth/flink.md): the core ideas, and how each was used on Uber Menu and (Kafka only) Masters India.
- [Kafka and Flink scale defense](tech_depth/kafka_flink_scale_defense.md): answers to pushback like "30K a month is tiny" or "prove you needed Flink".
- [Auth, tenancy and rate limits](tech_depth/auth_tenancy_rate_limits.md): JWT, OIDC, role-based access, constant-time comparison, token buckets, and AI-level budgets, per project.

Some smaller tech pages still use older shorthand. Where any page disagrees with the resume or with Numbers defense, trust Numbers defense.

---

## Five rules that apply on every page

1. **Uber was via EPAM.** Say it once, early.
2. **The 80% is a CI release gate,** not live accuracy for every tenant. 73% and 74% come from a separate 200-item benchmark.
3. **No Kafka, Flink, CDC, Kubernetes operations, Milvus or human review queues at Impact Analytics.** Kafka and Flink are Uber Menu. Kafka is also Masters India, but a different product.
4. **"Led 3" is Uber FRM. "Mentored 2" is Masters India.** Never merge them.
5. **Ask Iris is a shipped capability,** with no invented usage or uptime numbers.

**Handbook note.** The plain-English [Study Handbook](../../handbook/00_START_HERE.md) is the main entry point for this track. This folder is the reference shelf.

Related behavioral prep: [STAR bank](../behavioral/star_bank.md) · [Intros](../behavioral/intros_short_long.md) · [Why hire you](../behavioral/why_hire_you.md) · [Company guides](../behavioral/company_behavior_guides.md)
