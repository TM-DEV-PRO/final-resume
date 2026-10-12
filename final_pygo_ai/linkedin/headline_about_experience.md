# LinkedIn Profile Pack (stand out)

This pack matches the **Final Python + Go + AI** resume (`Tarun_Mittal_SSE_5yr.pdf`). Everything inside a quote box is paste-ready LinkedIn copy. Everything outside the boxes is a note for you and should not be pasted.

<div class="callout note">

**How to use this page**

- **What it covers:** your LinkedIn headline, the short and long About section, one blurb per job, the Featured section and the skills order.
- **When to read it:** when you update the live profile, and the night before a recruiter call, because recruiters read LinkedIn before they read the PDF.
- **What to memorise:** the "How to defend it" note under each block. A recruiter can quote any LinkedIn line back to you, including the few true facts that are not on the PDF.
- **Deeper explanation:** the handbook chapter [LinkedIn and outreach explained](../handbook/12_linkedin_and_outreach.md) decodes every line in plain English.

</div>

**Tags used on this page.** HISTORICAL means the number comes from past work records (Uber Mobility ANZ). "Off-PDF" means a true fact that appears on LinkedIn or in conversation but not on the resume PDF. Off-PDF facts are fine to say, but you should know they are not printed on the PDF in case someone compares the two.

**Style rule for the About section.** Avoid a colon-heavy "AI voice". Write the way you would speak.

**One profile, three tracks.** LinkedIn is a single public profile, but you have three resume tracks. This page is the Python + Go version (Uber FRM in FastAPI and SQLAlchemy 2.0). Whichever version you paste live, keep it consistent with the PDF you send most often. The Java version lives in [the Java + PyGo track pack](../../final_java_pygo_ia/linkedin/headline_about_experience.md).

---

## Headline (pick one)

LinkedIn headlines are capped at roughly 220 characters. All three options fit.

> 1. Senior Software Engineer | Python · Go | High throughput backends and data platforms | Go · ClickHouse · Kafka · Agentic AI

> 2. Senior Software Engineer | Go · ClickHouse · Kafka · LangGraph | 4B-row weekly rollups · 10k RPS

> 3. Backend SSE (Python and Go) | Uber (via EPAM) FRM · Kafka 1M+/day · Go/Gin 10k RPS · LangGraph

**Recommended:** use #1 for Staff and data platform searches. Use #2 if the recruiter is hunting for scale numbers. Use #3 for backend-heavy roles where the Uber name opens doors.

**How to defend it.**

- **Kafka in the headline** is Uber Eats Menu (with Flink) and Masters India (e-invoicing). It is not AssortSmart. If someone asks "how do you use Kafka at Impact Analytics?", say "I don't. My Kafka work was at Uber Menu and Masters India."
- **"4B-row weekly rollups"** refers to one table: the attr weekly rollup, which holds 4.09B rows across two seasons. Do not write or say "scaled to 4B+ rows" as if every table is that size.
- **10k RPS** is the peak requests per second on the AssortSmart Go/Gin platform. It is on the PDF.
- **Kafka 1M+/day** is Masters India: more than 1 million government e-invoice submissions per day.

---

## About (short)

Use this when space is tight, or as your 30-second spoken intro. It is the PDF summary word for word.

> Senior Software Engineer with 5 years of experience designing and owning cloud-native, high-throughput distributed systems. Expertise in Python and Go microservices, with applied experience in AI-assisted and RAG systems. Proven track record shipping production systems, leading backend migrations, and improving reliability, performance, and scalability.

**How to defend it.** "AI-assisted and RAG systems" points to two places: the AssortSmart decision engine and Ask Iris copilot at Impact Analytics, and the Gemini plus LangChain RAG (retrieval-augmented generation) menu pipeline at Uber Eats. "Leading backend migrations" points to the PHP-to-FastAPI move at Masters India and the SQLAlchemy 2.0 migration at Uber FRM.

---

## About (long)

LinkedIn caps About at about 2,600 characters. This version fits.

> I am a Senior Software Engineer focused on backend, data, and production AI platforms in Python and Go.
>
> What I am known for:
>
> - Platform: At Impact Analytics I architected AssortSmart's multi-tenant Go/Gin edge (Wire, h2c, Datadog) to 10k peak RPS. I cut planner pivots from 189s to 12s on 250M rows with six ClickHouse rollup tables (product, store, and attr at season and weekly grains). I keep a 100% statement-coverage CI gate across 1,200+ Go tests.
> - Scale and infrastructure: Weekly grain is built one fiscal week at a time, after a full-season weekly aggregate hit about 170 GB and ran out of memory. I wrote a Go native-TLS pump that copies season partitions between ClickHouse Cloud clusters at about 150-190k rows/s per stream, 344k combined. It uses 500k-row columnar batches with double buffering, so the SELECT of the next batch overlaps the INSERT of the last. The largest object I timed is attr weekly at 4.09B rows across two seasons, measured in flight, not a finished cutover. The Kafka and Flink on my profile are Uber Menu, not AssortSmart.
> - Agentic: I built Keep/Drop, Missed Opportunities, and Top Style over 348k article-seasons (88k items per pass, 7 lenses), reading JSON payloads instead of querying the 2.11B-row ClickHouse master. I shipped Ask Iris, a JWT-secured WebSocket copilot with a LangGraph supervisor, a 3-attempt evaluator, and hierarchy access frozen at the handshake. Promotions are gated on a 300-case proxy harness and an 80% CI gate (a gate, not live accuracy for all tenants). On a separate benchmark we cut live scoring cost 73% at 100% coverage against a 74% deterministic baseline, and froze blend weights when the LLM lost.
> - Uber via EPAM: FRM scoping with 36 FastAPI endpoints, 19M GL rows, an L1–L4 FSLI hierarchy, an 8-table SOADB schema, and SHA-256 keys. I led 3 engineers to 100% coverage with SOX 50% delta-variance checks. Reconciliation dropped 70%, from 14 days to 3, against $340M materiality. Menu ingestion went from 24 hours to 2 hours, saving $600K/yr on 30K+ menus/month, with 98% offline field fidelity (RAG over Milvus) and Kafka + Flink exactly-once upserts.
> - Masters India: A FastAPI strangler migration cut p95 75%, from 1.2s to 300ms. A Kafka + PostgreSQL pipeline sharded by tax quarter handles 1M+ submissions/day. Coverage went from 35% to 82% at 98% deploy success. I mentored 2 engineers.
>
> I care about honest metrics (measured vs promotion gate vs historical) and mentoring people to ship safely.
>
> Open to Senior Software Engineer / SDE2+ roles in backend, platform, data infrastructure, and applied-AI systems.

**How to defend each paragraph** (the handbook chapter expands every line).

- **Platform.** "Wire" is Google Wire, which wires up Go dependencies at compile time. "h2c" is HTTP/2 without TLS, served directly by Go with no reverse proxy in front. The 189s to 12s pivot result was measured on a 250M-row benchmark harness (12.3s, rounded to 12). The **100% coverage across 1,200+ Go tests is off-PDF**. It is true, so say it plainly, but know it is a LinkedIn and verbal fact.
- **Scale and infrastructure.** Two separate stories live here. The 15.5× pivot speed-up is about query time. The 170 GB out-of-memory failure is about building the weekly tables (load time). One did not cause the other. 344k is **rows per second during a copy**, not requests per second. The 4.09B copy was measured while it was running. Never say the cutover finished.
- **Agentic.** An article-season is one product in one selling season. 348k is the number scored. The full catalog is larger (1.6M, off-PDF). The LLM never gets a SQL tool. It only sees JSON prepared for it. Keep/Drop runs its steps in a fixed order (peer, decider, lenses, blend, explain). No LLM decides what runs next, and the supervisor pattern belongs to Ask Iris. The 300-case harness and the 80% gate are one thing. The 73% cost cut and the 74% baseline come from a different 200-case gold benchmark. Do not fuse them.
- **Uber via EPAM.** Always say "Uber via EPAM". "Led 3" means tech lead of an EPAM pod, not people manager. 98% is an offline evaluation number, not live production accuracy. "Exactly-once" in practice means at-least-once delivery plus idempotent upserts, so a replayed message cannot create a duplicate.
- **Masters India.** "Mentored 2" belongs to Masters India. "Led 3" belongs to Uber FRM. Never merge them into "led a team of 5".

---

## Experience blurbs

### Impact Analytics — Senior Software Engineer (May 2026 – Present)

The PDF has two chapters for this role and puts Agentic first. Paste them in the same order.

> **AssortSmart — Platform & AI.**
>
> **Agentic Flows & Orchestration.** I built the Keep/Drop, Missed Opportunities, and Top Style pipelines over 348k article-seasons, 88k items per pass, across 7 lenses. The models get JSON payloads instead of querying the 2.11B-row ClickHouse master. Writes use ReplacingMergeTree, with fallback to deterministic scores on LLM timeouts. A shared orchestration registry adds circuit breakers, checkpoints that skip redundant deterministic scoring, a config_hash on every output row, and JSON telemetry. I shipped Ask Iris, a JWT-secured WebSocket copilot with a LangGraph supervisor, a 3-attempt evaluator, hierarchy access frozen at the handshake, and LangSmith tracing. Releases pass a 300-case proxy eval and an 80% CI gate. On a separate benchmark, the model choice made scoring 73% cheaper at 100% coverage against a 74% deterministic baseline, and the blend weights were frozen.
>
> **Core Infrastructure & Pipeline.** I architected a multi-tenant Go/Gin platform at 10k peak RPS (Wire, h2c, Datadog). I built a KPI formula tokenizer with native division-by-zero protection. Auth runs Firebase, then JWT / Google OIDC, fronted by Redis, with Postgres-backed roles.
>
> Reduced planner pivot latency by 15.5× (189s to 12s on 250M-row operations) by building a ClickHouse pre-aggregation layer for season and weekly rollups. Prevented 170GB OOM crashes by slicing batch inserts into temporal chunks and enforcing strict distributed memory and disk-spill caps.
>
> Migrated ClickHouse rollups across Cloud clusters at ~344k rows/s by writing a custom Go native-TLS data pump to bypass strict cross-cluster IP allowlist restrictions. Processed partitions up to 4.09B rows using 500k-row double-buffered batches, and eliminated partial-commit ghost rows using TSV ledgers and atomic partition rollbacks.
>
> The full catalog holds 1.6M article-seasons. A full scoring pass costs about $100 in LLM tokens. The Go codebase holds a 100% statement-coverage gate across 1,200+ tests, with golangci-lint and SAST/SBOM checks.
>
> Stack: Go, Gin, Python, FastAPI, LangGraph, ClickHouse, BigQuery, Redis, PostgreSQL, Datadog, LangSmith, GCP, Docker.

**What this means and how to defend it.**

- **The last paragraph is all off-PDF.** 1.6M article-seasons (the catalog), $100 per pass (token spend), 100% Go statement coverage and 1,200+ tests are true and allowed on LinkedIn. 1.6M is the whole catalog, and 348k is what the engine actually scores. They are different numbers, so never swap them. golangci-lint and SAST/SBOM are not in the locked resume facts. Keep them only if you can explain what you configured. Otherwise delete that clause before pasting.
- **"Atomic partition rollbacks"** means: if a partition copy fails halfway, drop that partition on the target and copy the whole season again. It is not an atomic swap while live readers are using the table.
- **"TSV ledgers"** are plain tab-separated files that record which weeks and partitions already finished, so a restart skips them and never double-writes.
- **Not on LinkedIn or the PDF:** Cluster Recommendation Copilot and Hindsight (still being built). Use them only as deep-dive context if an interviewer asks what you are working on next. They are not headline bullets.

### Uber via EPAM — SDE2 (Jul 2024 – May 2026)

> **FRM (Financial Risk Management):** Owned the FRM scoping backend (Python, FastAPI, SQLAlchemy 2.0): 36 FastAPI endpoints, 19M raw GL rows, an L1–L4 FSLI hierarchy, an 8-table MySQL schema on SOADB, SHA-256 natural keys, and optimistic locking. Cut reconciliation 70%, from 14 days to 3, against a $340M materiality threshold. Led 3 engineers on the SQLAlchemy 2.0 ORM migration to 100% statement coverage, with stacked Bazel PRs, SQL allowlists, and FSM gates with 50% delta-variance checks for SOX.
>
> **Menu (Uber Eats):** Cut restaurant onboarding from 24 hours to 2 hours, saving $600K/yr across 30K+ menus/month. Gemini 2.5 Pro + LangChain RAG + Milvus at 98% field fidelity (offline eval). 95%+ scrape success. Kafka + Flink keyed dedupe with exactly-once catalog upserts.
>
> **ANZ (Uber Mobility):** 99.9% document compliance and about 20 hours/week of manual review saved by automating driver and vehicle document verification.

**What this means and how to defend it.**

- **FRM** is the tool Uber Finance uses each quarter to decide which accounts and entities need audit attention. GL is the general ledger, the company's master list of accounting entries. FSLI is a Financial Statement Line Item, grouped four levels deep (L1 to L4). SOADB is Uber's standard service-owned MySQL. If asked how the 36 endpoints break down, say about 31 functional routes in the scoping service plus the collaboration-service APIs (comments and notifications) from the design doc. The 70% is the outcome the platform delivered for the close. If pressed, say "the technical design doc framed that cut, and that's what the platform delivered". Do not walk it back unprompted.
- **Menu.** 98% is offline evaluation. $600K is a conservative floor: about $2 per menu × 30K menus × 12 months is $720K, rounded down. Milvus is Uber Menu only.
- **ANZ** is HISTORICAL and is Uber Mobility, not Uber Eats. It was a deterministic rules backend. Do not add Selenium or RAG to this story.

### Masters India — SDE2 (Dec 2022 – Jun 2024)

> Cut p95 latency from 1.2s to 300ms (75%) for 1,500+ clients by migrating a PHP monolith to FastAPI microservices, and mentored 2 engineers. Took throughput from 700 to 4,000 requests per minute and ran 1M+ IRP submissions/day on a high-concurrency Kafka + PostgreSQL pipeline sharded by tax quarter. Idempotent processing, dead-letter queues and fault-tolerant state, and a Redis cache that cut database reads 30%. Raised test coverage from 35% to 82% at a 98% deployment success rate.

**What this means and how to defend it.** Masters India sells GST (Goods and Services Tax) compliance and e-invoicing software. IRP is the government's Invoice Registration Portal, which returns an IRN (invoice reference number) and a signed QR code. 1M+ per day averages about 12 per second (1,000,000 ÷ 86,400), with ESTIMATED peaks of 8 to 10 times that around filing deadlines. 700 to 4,000 requests per minute is roughly 12 to 67 requests per second.

### GeeksforGeeks — SDE (Aug 2021 – Nov 2022)

> Migrated the doubt-support platform to Django to handle 10K+ daily queries and 10× contest spikes. Voting, pinning, and locking APIs lifted premium subscriptions 20%. An influencer dashboard raised course sales 30%. Scheduled jobs raised ops efficiency 70%.

**What this means and how to defend it.** The 20% and 30% are business lifts attributed by the growth and business teams. Say "I owned the engineering, and the business team attributed the lift." The 20% is a relative lift.

---

## Featured section

- Resume PDF (Python + Go + AI track, `Tarun_Mittal_SSE_5yr.pdf`)
- LangChain Academy cert
- HackerRank Problem Solving cert
- Optional: GitHub TM-DEV-PRO

Never feature or link the ClickHouse copier code. It contains hosts, DDL and credentials, so whiteboard it instead.

---

## Skills order (LinkedIn)

> Python · Go · Gin · FastAPI · Distributed Systems · Microservices · Kafka · ClickHouse · System Design · Docker · AWS · GCP · PostgreSQL · MySQL · Redis · LangGraph · RAG · Mentorship

**Why this order.** LinkedIn shows the top few skills first, and recruiters filter on them. Python and Go lead because this track sells Python and Go microservices. If you switch the live profile to a Java track, add Java, Spring Boot and Hibernate at the front, and switch the FRM blurb to the Java wording at the same time.
