# Referral Asks (short and long)

This page matches the **Final Java + AI (IA = Py/Go)** resume (`Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf`). It adapts Packet Template 1 so every metric is on the current PDF. Everything inside a quote box is paste-ready.

<div class="callout note">

**How to use this page**

- **What it covers:** a short referral ask (DM or Slack), a long referral ask (email or LinkedIn), and a cover letter.
- **When to use it:** when you are writing to someone who already works at the company, such as an ex-colleague, an alumnus or a friend of a friend. For recruiters you have never met, use [Cold mail recruiter / sourcer](recruiter_cold_email.md).
- **What to memorise:** the "How to defend it" notes. A referrer forwards your message as-is, so the hiring manager may quote it back to you.
- **Full playbook:** [LinkedIn and outreach explained](../handbook/12_linkedin_and_outreach.md) covers follow-up timing.

</div>

A referral works best when you make it effortless. Send the exact job link, offer a short fit summary, and give the person an easy way to say no.

---

## Short (LinkedIn DM / Slack)

> Hi [Name], I am Tarun, a Senior Software Engineer (Java, Python and Go, 5y). I owned Uber FRM scoping (36 Spring Boot endpoints, led 3) and now scale AssortSmart: Go/Gin at 10k RPS, ClickHouse pivots from 189s to 12s on 250M rows, six rollup tables, a Go pump at about 344k rows/s combined on a 4.09B-row attr weekly set, LangGraph Keep/Drop, and the shipped Ask Iris copilot. Could you refer me for [Role link]? Happy to send a 5-bullet fit summary.

**When to use it.** Use it with someone you know a little, on LinkedIn or a shared Slack. Keep the role link in the message so they can act in one click.

**How to defend it.** "Now scale AssortSmart" means the platform and data work at Impact Analytics (current role). The 189s to 12s is a benchmark on a 250M-row harness. The 4.09B-row copy was measured while still running, not a finished migration. Keep/Drop runs its steps in a fixed order. The LangGraph supervisor pattern is Ask Iris.

---

## Long (email / LinkedIn)

> Hi [Name],
>
> Hope you are having a good week. I have been following [Company]'s work on [specific team problem: high-throughput services / real-time data / applied AI].
>
> I am Tarun Mittal, a Senior Software Engineer in Bangalore with about 5 years in Java, Python and Go backends. At Impact Analytics I architected AssortSmart's Go/Gin platform (10k peak RPS) and its ClickHouse rollups. Pivots went from 189s to 12s on 250M rows across six tables. Weekly grain is built one fiscal week at a time after a 170 GB OOM. A Go pump runs at about 344k rows/s combined, measured on a 4.09B-row attr weekly set. I also built Keep/Drop and Ask Iris behind a 300-case eval and an 80% promotion gate. Before that, at Uber via EPAM, I owned FRM (36 Spring Boot endpoints, 19M GL rows, reconciliation from 14 days to 3, a 70% cut, led 3) and Uber Eats menu ingestion (24 hours to 2 hours, $600K/yr, Kafka + Flink exactly-once). At Masters India I led a Spring Boot strangler migration and a Kafka e-invoice path at 1M+ submissions/day.
>
> I am applying to [Role title link]. If you are open to a referral, I can send a short fit note and my resume today. No worries if you are swamped. Either way, thank you for reading.
>
> Best,<br>
> Tarun<br>
> (+91) 9079727197 · tmittaliet@gmail.com · linkedin.com/in/t-mittal

**When to use it.** Use it for a cold referral ask to someone you do not know well, such as an alumnus or a second-degree connection. The first line must name something real about their team. Fill `[specific team problem]` with one concrete thing from their engineering blog, talk or job post.

**How to defend it.**

- **"Architected"** is the PDF verb for the Go/Gin platform. Be ready to draw it: Gin HTTP edge, Google Wire for dependency injection, h2c, Datadog tracing, ClickHouse and PostgreSQL behind it.
- **"300-case eval and an 80% promotion gate"** is a release check, not live accuracy across tenants.
- **"Kafka + Flink exactly-once"** in practice means at-least-once delivery plus idempotent upserts. Do not claim zero message loss.
- **"Led a Spring Boot strangler migration"**: the strangler pattern replaces a legacy system one route at a time, with a canary per route, until the old system can be switched off.

---

## Cover letter (packet, PDF-honest)

Use this only when a form explicitly asks for a cover letter. Most engineering recruiters skip them.

> Subject: Application for Senior Software Engineer – Distributed Systems & Backend
>
> Dear Hiring Team,
>
> I am writing to apply for the Senior Software Engineer role at [Target Company]. I architect high-throughput distributed systems and production AI orchestration in Java, Python and Go.
>
> Recent impact from my resume:
>
> - **Latency at scale:** ClickHouse pivots from 189s to 12s (about 15.5×) on 250M-row operations, served from six rollup tables. Weekly grain is built one fiscal week per INSERT SELECT after a roughly 170 GB OOM.
> - **Data movement:** A Go native-TLS pump at about 344k rows/s combined, using 500k-row columnar batches and double buffering, measured on a 4.09B-row attr weekly set covering two seasons (in flight at the snapshot, not a finished cutover).
> - **Platform:** A multi-tenant Go/Gin HTTP edge at 10k peak RPS (Wire, h2c, Datadog), held to a 100% Go statement-coverage gate across 1,200+ tests.
> - **Event streaming (Uber Eats):** Kafka + Flink keyed dedupe and exactly-once catalog upserts. Onboarding went from 24 hours to 2 hours, saving $600K/yr across 30K+ menus/month. (This Kafka and Flink work was at Uber Eats, not AssortSmart.)
> - **Production AI:** LangGraph Keep/Drop and the shipped Ask Iris copilot. Milvus RAG on Uber Eats menus at 98% offline field fidelity. A 300-case eval harness with an 80% CI promotion gate, and a separate benchmark against a 74% deterministic baseline.
>
> [Company]'s work on [specific infrastructure / product] matches how I own systems: design, measurement, and honest gates. My resume is attached.
>
> Best regards,<br>
> Tarun Mittal<br>
> (+91) 9079727197 · tmittaliet@gmail.com · linkedin.com/in/t-mittal · github.com/TM-DEV-PRO

**How to defend it.**

- **100% Go coverage and 1,200+ tests** are true and listed on LinkedIn, but not printed on the PDF. Say them confidently, and know where they live.
- **Kubernetes and Flink at AssortSmart:** the letter makes no such claim. Do not add one. Kubernetes is skills-level for you, not cluster operations.
- **74% deterministic baseline** comes from a 200-case gold benchmark, not the 300-case harness. The 80% gate and the 74% baseline are measured on different sets, so do not say "80% vs 74%" as if they were one comparison.
