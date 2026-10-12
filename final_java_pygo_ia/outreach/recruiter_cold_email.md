# Cold Mail Recruiter / Sourcer

This page matches the **Final Java + AI (IA = Py/Go)** resume (`Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf`). Everything inside a quote box is paste-ready. The templates were adapted from the AssortSmart-tab packet, but every claim matches the **current PDF** rather than the older packet overclaims (no Kubernetes operations, no Flink or CDC at Impact Analytics).

<div class="callout note">

**How to use this page**

- **What it covers:** subject lines, one long cold email, a short and a long LinkedIn DM, and an honest "data platform" hook for infrastructure roles.
- **When to use it:** when you write first to a recruiter or sourcer you have never spoken to. For people who already work at the company, use [Referral asks](referrals_short_long.md) instead.
- **What to memorise:** the "How to defend it" notes. A recruiter will often read one line of your email back to you on the call.
- **Full playbook:** [LinkedIn and outreach explained](../handbook/12_linkedin_and_outreach.md) covers when to send which template and how to follow up.

</div>

Before you send, replace every `[bracket]`, attach the PDF, and delete any bullet that is irrelevant to the role. Three strong bullets beat five crowded ones.

---

## Email subject lines (pick one)

> Senior Software Engineer (Java · Python · Go) | Uber FRM + AssortSmart platform/AI

> 5y backend · Go/Gin 10k RPS · ClickHouse 4B-row rollups · Kafka 1M+/day · LangGraph

> Referral-ready Senior SWE (Java · Python · Go) [Company] [Req ID]

**When to use which.** The first suits generalist recruiters, because brand names (Uber) get opened. The second suits data platform or infrastructure sourcers who scan for scale. The third is for when you already have a referral or a specific requisition ID.

**How to defend it.** "4B-row rollups" means one rollup table (attr weekly), which holds 4.09B rows across two seasons. Kafka 1M+/day is Masters India, not Impact Analytics.

---

## Email body (long)

> Hi [Name],
>
> I am Tarun Mittal, a Senior Software Engineer (Java, Python and Go) with 5 years owning production backends and applied-AI systems. Quick proof points from my resume:
>
> - **Impact Analytics, AssortSmart:** Multi-tenant Go/Gin platform at 10k peak RPS (Wire, h2c, Datadog). ClickHouse pivots from 189s to 12s on 250M-row operations across six rollup tables. Weekly rollups built one fiscal week at a time after a roughly 170 GB OOM. A Go native-TLS pump at about 344k rows/s combined, measured on a 4.09B-row attr weekly set. Keep/Drop on 348k article-seasons, plus the shipped Ask Iris copilot. Releases gated by a 300-case eval and an 80% CI promotion gate.
> - **Uber via EPAM, FRM:** 36 Spring Boot endpoints, 19M GL rows, L1–L4 FSLI hierarchy, 8-table SOADB schema, SHA-256 keys. Reconciliation cut 70%, from 14 days to 3, against $340M materiality. Led 3 engineers, 100% coverage, SOX 50% delta-variance checks.
> - **Uber Eats menu ingestion:** 24 hours to 2 hours, $600K/yr, 30K+ menus/month, 98% offline field fidelity with RAG over Milvus, Kafka + Flink exactly-once.
> - **Masters India:** Spring Boot strangler migration, p95 from 1.2s to 300ms, Kafka e-invoicing at 1M+/day. Mentored 2 engineers.
>
> I am targeting [Senior SWE / SDE2 / MTS] roles on [Team]. My resume is attached. Happy to do a 15-minute screen this week.
>
> Thanks,<br>
> Tarun Mittal<br>
> (+91) 9079727197 · tmittaliet@gmail.com<br>
> linkedin.com/in/t-mittal · github.com/TM-DEV-PRO

**What each line means and how to defend it.**

- **10k peak RPS** is peak requests per second on the Go/Gin platform. Do not attach an SLA or uptime number to it, because none is claimed.
- **189s to 12s** was measured on a 250M-row benchmark harness. It is query time. The **170 GB OOM** was a separate load-time problem when building the weekly tables, so the two are not cause and effect.
- **344k rows/s** is a copy rate in rows per second, not requests per second. The 4.09B-row copy was measured while still running, so do not say "I migrated 4 billion rows".
- **80% CI promotion gate** means a new model or prompt cannot ship unless it scores at least 80% on the 300-case harness. It is not live accuracy for all tenants.
- **70% from 14 days to 3** is the reconciliation outcome on the PDF. State it plainly. If pressed: "the technical design doc framed that cut, and that's what the platform delivered for the close."
- **98%** is offline evaluation, not live production accuracy.
- **"Led 3"** is Uber FRM (tech lead of an EPAM pod). **"Mentored 2"** is Masters India. Keep them separate.

---

## LinkedIn DM short

> Hi [Name], I'm a Senior SWE (Java, Python and Go, 5y). I owned Uber FRM scoping (36 endpoints, led 3), built a Kafka pipeline at 1M+/day at Masters India, and now work on AssortSmart: Go/Gin at 10k RPS plus LangGraph Keep/Drop. Open to [Role]? Happy to send my resume.

**When to use it.** Use it as a LinkedIn connection note or the first message to a sourcer. Connection notes have a tight character limit (a few hundred characters), and this fits.

**How to defend it.** "LangGraph Keep/Drop" is the AssortSmart decision engine. Its steps run in a fixed order (peer, decider, lenses, blend, explain), and no LLM decides what runs next. The LangGraph supervisor pattern is Ask Iris.

---

## LinkedIn DM long

> Hi [Name], here is my fit in one glance. At Uber (via EPAM) I owned FRM (36 Spring Boot endpoints, reconciliation from 14 days to 3, a 70% cut, led 3) and built Menu ingestion end to end ($600K/yr, 24 hours to 2 hours, Kafka/Flink). At Masters India I ran Kafka at 1M+/day. Today at AssortSmart I work on a Go/Gin platform at 10k RPS, six ClickHouse rollup tables, a Go pump at about 344k rows/s combined on a 4.09B-row attr weekly set, and the shipped Ask Iris copilot. I'm looking at [Company] senior backend / data platform / applied-AI roles. If you are sourcing for [Team], I would love a quick screen. Resume here: [link].

**When to use it.** Use it after the person accepts your connection, or as an InMail when you have no connection-note limit.

**How to defend it.** "Menu ingestion end to end" covers the Selenium scraping fleet, the Kafka and Flink pipeline, and the Gemini RAG extraction. It does not cover ANZ, which is a separate Uber Mobility project.

---

## Data platform hook (honest)

Use this for Data Infrastructure, Core Platform and Data Engineering roles.

**Do not send:** "I stream 4.09 billion rows at 344,000 rows/second."

**Send:**

> I built six ClickHouse rollup tables for planner reads and a Go pump that copies season partitions at about 344k rows/s combined, measured on a 4.09B-row attr weekly set. Weekly grain is one fiscal week per INSERT after a roughly 170 GB OOM.

**Why the first version is wrong.** "I stream 4.09 billion rows" claims a finished, continuous stream. The truth is a partition copy measured while it was still running, at a combined rate across two parallel season streams.

**Fit and rules.**

- Best fit is Senior SWE plus Data Infrastructure, Core Platform or Data Engineering.
- For Java-heavy roles, send the Java track PDF and Java track templates instead of this page.
- Never offer to open-source or share the copier code. It contains hosts, DDL and passwords. Whiteboard it instead.
- Deep pack: [ClickHouse rollup migration](../prep/42_clickhouse_rollup_migration.md).
