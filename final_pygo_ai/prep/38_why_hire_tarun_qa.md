# Why hire Tarun — screening and pitch Q&A

**Track:** Final Python + Go + AI · **PDF:** `Tarun_Mittal_SSE_5yr.pdf` · **Contact:** tmittaliet@gmail.com · (+91) 9079727197

<div class="callout note">
<b>How to use this page</b>
<ul>
<li><b>What it covers:</b> the "sell yourself" questions. Why hire me, why leave, why this company, biggest risk, and the objections recruiters and hiring managers raise.</li>
<li><b>When to read it:</b> the night before a recruiter screen or hiring-manager round, and again 15 minutes before the call.</li>
<li><b>What to memorise:</b> the 30-second "why hire me" (section 1.1), the biggest-risk answer (1.4), and the objection answers (section 5). Read the 90-second versions out loud twice. Do not memorise them word for word.</li>
<li><b>Technical depth lives elsewhere</b> (links below). This page is persuasion plus honesty.</li>
</ul>
</div>

Technical depth: [IA pack](23a_ia_interview_pack.md) · [Uber packs](23b_uber_interview_packs.md) · [Masters and GfG packs](23c_masters_gfg_interview_packs.md) · [IA bullet defense](43_ia_bullet_defense.md) · [STAR stories](07_behavioral_star_stories.md)

**What the tags mean.** Some numbers carry a tag so you know how strongly you can state them.

- **PDF** means the number is printed on the resume. Say it plainly.
- **MEASURED** means there is a log, benchmark, doc, or code behind it.
- **ESTIMATED** means it is arithmetic I can show. Say "roughly, derived from...".
- **TARGET** means it is a design goal. Say "targeting".
- **HISTORICAL** means it comes from my past work records, not something I can re-run today.
- **Verbal only** means it is real interview depth but not on the resume. Use it only if they ask.

<div class="callout warn">
<b>Say these carefully. They are the lines interviewers check.</b>
<ul>
<li>The <b>80%</b> number is a CI promotion gate. It means a change cannot be promoted unless it scores at least 80% on a 300-case test set. It does not mean "every tenant runs at 80% accuracy in production".</li>
<li>The <b>73%</b> cost cut and the <b>74%</b> baseline both come from a separate 200-case gold benchmark. They do not come from the 300-case file. Never fuse the two.</li>
<li><b>Ask Iris</b> is a shipped capability. I do not have SLA or usage numbers for it, so I do not quote any.</li>
<li>On the PDF for Impact Analytics: 10k peak RPS, 2.11B-row master, 348k article-seasons, 88k items per pass, six rollup tables, 170GB OOM, about 344k rows per second, partitions up to 4.09B rows.</li>
<li>Off the PDF (verbal only): $100 per pass token spend, the 1.6M-row catalog, the 55 GB and 16 GB memory knobs, 100% Go test coverage.</li>
<li>Cluster Recommendation Copilot and Hindsight are verbal only. They are not resume bullets.</li>
<li>Menu <b>98%</b> is from offline evaluation. Uber work was <b>via EPAM</b>. ANZ <b>99.9%</b> is HISTORICAL and belongs to Uber Mobility, not Uber Eats.</li>
<li>No Spark, Pinot, Kubernetes operations, or CDC ownership anywhere. Kafka and Flink belong to Uber Menu, not to Impact Analytics.</li>
</ul>
</div>

---

## How to structure any answer on this page

Every answer here follows the same four-step shape. If you lose your place mid-answer, come back to it.

1. **Direct answer first.** One sentence that answers the question as asked. "You should hire me because I own systems end to end and I can prove the numbers."
2. **Two or three proof points.** Each one is a project, what I did, and at most two or three numbers. More numbers than that and the listener stops hearing them.
3. **Explain any technical word in one clause.** "ClickHouse, which is a database built for fast analytical reads, ..." The listener may not be an engineer.
4. **Short close.** One sentence that ties it back to their role. Then stop talking.

Two lengths are written for the main questions. The **30-second version** is for recruiter screens and the opening of a hiring-manager call. The **90-second version** is for when they say "tell me more" or for a dedicated "why you" question.

---

## 0. Recruiter blurb (third person)

Paste this into emails or give it to a recruiter who needs to pitch you internally.

> Tarun Mittal is a Senior Software Engineer with **5 years** of experience building high-throughput, cloud-native distributed systems in **Python and Go**.
>
> At Impact Analytics he owns the Go/Gin platform behind AssortSmart, a retail merchandise-planning product, serving **10k peak requests per second**. He made planner pivot screens **15.5× faster (from 189 seconds to 12 seconds)** with a ClickHouse pre-aggregation layer, and he shipped **Ask Iris**, a LangGraph-based copilot that lets planners ask questions about their KPIs and AI decisions.
>
> At Uber via EPAM he owned the Financial Risk Management scoping backend (**36 FastAPI endpoints**), which cut quarterly reconciliation **from 14 days to 3 days**. He also owned Uber Eats menu ingestion, which cut restaurant onboarding **from 24 hours to 2 hours** and saved about **$600K a year**.
>
> At Masters India he led a PHP-to-FastAPI migration that cut p95 API latency **from 1.2 seconds to 300 milliseconds**, and scaled government e-invoicing to **1M+ submissions a day**.
>
> He is a Google Code Jam 2021 qualifier (rank 2260 of 37,000+), a Smart India Hackathon 2020 national finalist (top 3), and holds HackerRank Problem Solving and LangChain Academy certificates.

**20-second spoken version (first person):**

"I'm a senior backend engineer with five years in Python and Go. At Uber via EPAM I owned a finance-grade reconciliation platform and the Uber Eats menu ingestion pipeline. At Masters India I scaled an e-invoicing path to over a million submissions a day. Now at Impact Analytics I own the Go platform and the AI decision engine for a retail planning product. I make decisions with benchmarks, and I can defend every number on my resume."

---

## 1. Why should we hire Tarun?

### 1.1 Why hire you — 30-second version

"Because I own systems end to end, and I measure before I claim. Three examples. At Uber via EPAM I owned the finance risk scoping backend, and quarterly reconciliation went from 14 days to 3 days. At Masters India I led the migration off a PHP monolith, and p95 latency went from 1.2 seconds to 300 milliseconds. At Impact Analytics I own the Go platform and the AI decision engine, and I put an 80% accuracy gate in CI so no AI change ships without passing a test set. You get someone who builds it, measures it, and is honest about what the numbers mean."

### 1.2 Why hire you — 90-second version

"The short answer is ownership, evidence, and honesty. Let me give you one example of each.

**Ownership.** At Uber via EPAM I owned the FRM scoping backend. FRM is Financial Risk Management, the tool Finance uses each quarter to decide which accounts are in scope for audit. I designed the API contracts, built 36 FastAPI endpoints, and led a pod of 3 engineers. Reconciliation went from 14 days to 3 days. On Uber Eats I owned menu ingestion end to end, from the Selenium scrapers through a Kafka and Flink pipeline to the catalog. Kafka is a durable message queue and Flink is a stream processor that cleans and deduplicates events as they arrive.

**Evidence.** At Impact Analytics, planner pivot screens were slow on PostgreSQL. Instead of arguing about databases, I ran a proof of concept on a 250-million-row test harness. With ClickHouse rollup tables the pivot went from 189 seconds to 12 seconds. The same benchmarks also showed where ClickHouse is the wrong answer, which is small keyed updates to single cells. So we kept those in Postgres.

**Honesty.** When our AI model scored below a simple rule-based baseline, I froze the blend weights instead of shipping it anyway. I'm also careful with my own numbers. The 80% figure is a CI gate, not live accuracy for every customer. Ask Iris is a shipped capability, and I don't quote usage numbers I don't have.

So you get an engineer who can own a system, prove it works, and tell you plainly where the edges are."

**Follow-up they may ask:** "What does 'froze the blend weights' mean?" Answer: "Our final score is a weighted mix of a rule-based score and an LLM score. On a 200-case benchmark the rule-based baseline scored 74% and the blended LLM scored lower. So we kept the weights fixed instead of tuning them to favour the LLM."

### 1.3 Why you over someone with more years?

**Direct answer:** "Scope, not years. I've already owned systems where mistakes are expensive."

"At Uber via EPAM my platform was the system of record for a $340M materiality threshold. Materiality is the dollar line above which an account must be audited, so a wrong number becomes audit evidence. At Masters India the pipeline I worked on handles over 1 million government submissions a day. At Impact Analytics the platform peaks at 10k requests per second over a 2.11-billion-row ClickHouse table. I've also led 3 engineers at Uber and mentored 2 at Masters.

Here's the boundary, so you hear it from me. I haven't run a 50-person org, and I haven't operated Kubernetes clusters. If the role needs those, I'd ramp on them. If it needs someone who owns hard systems and can defend the design, that's what I already do."

### 1.4 Why *not* hire you? What is your biggest risk?

**Short version:** "The honest risk is that my newest AI work is recent. Ask Iris is shipped, but I don't have long-term usage numbers yet. My longer production record is at Uber and Masters India."

**Full version:** "Let me separate what's proven from what's new. Ask Iris, the copilot at Impact Analytics, is a shipped capability. I won't invent an SLA or usage stats for it. The 80% figure is a CI gate that blocks bad changes. It isn't a claim that every tenant runs at 80% accuracy. Some AI designs I can talk about, like the Cluster Recommendation Copilot, are design depth and aren't on my resume.

What has run in production for a long time is the Uber menu pipeline, the FRM platform, and the Masters India e-invoicing system. Those are where my track record is strongest, and I'm happy to go as deep as you want on any of them."

### 1.5 What makes you different?

**Direct answer:** "Five things: finance-grade correctness, real money saved, scale, benchmark-driven decisions, and AI with guardrails."

| Claim | Evidence (pick one or two when speaking) | Tag |
|---|---|---|
| Finance-grade backend | Uber FRM: 36 FastAPI endpoints, 19M raw GL rows migrated off Sheets, $340M materiality, led 3 engineers, 100% module coverage, 50% delta-variance SOX checks | PDF |
| Real money | Uber Eats menus: from 24 hours to 2 hours, $600K a year saved, 30K+ menus a month | PDF |
| Scale | Masters India: 1M+ submissions a day. Impact Analytics: 10k peak RPS, 2.11B-row master table | PDF |
| Benchmarks before opinions | ClickHouse pivots from 189 seconds to 12 seconds on a 250M-row harness | PDF, MEASURED |
| Safe AI agents | LLM gets JSON context, never SQL access to the 2.11B table. Tenant scope frozen at login. 80% CI gate on 300 cases. Weights frozen when the LLM lost to the 74% baseline | PDF |
| People | Led 3 at Uber FRM. Mentored 2 at Masters India. Never merge these | PDF |

How to say it: pick the two rows that match their job description and give one sentence each. For example, for a fintech role: "I've built finance-grade systems where correctness is audited, and I've worked at real scale." For an AI role: "I build AI features with hard guardrails, and I'll freeze a model that loses to a simple baseline."

GL means general ledger, the company's master record of every financial transaction. SOX is the US Sarbanes-Oxley law that requires controls over financial reporting.

---

## 2. Motivation and fit

### 2.1 Why are you leaving Impact Analytics?

"I'm not running from the work. I'm proud of what I built there. I'm looking for a larger production surface and a harder design-review bar, where my decisions are challenged by more senior peers and the systems are bigger."

**Follow-up they may ask:** "You only joined in May 2026." Answer: "Right. I joined for platform and AI ownership, and I got it. I'm not someone who shops for a new job every year. This move is about the scale and review bar your team offers."

### 2.2 Why this company?

Never improvise this cold. Prepare it per company with this two-sentence shape:

1. One sentence about their product and why it interests you.
2. One sentence linking one of their systems to something you've already built. For example, high-traffic APIs map to the 10k RPS Go platform, big analytical data maps to the 2.11B-row ClickHouse table, streaming maps to the Uber Menu Kafka and Flink pipeline, and AI quality maps to the evaluation gates.

Example: "You process millions of payments a day, and correctness is the product. I spent my time at Uber via EPAM building a finance platform where every number became audit evidence, so I know what that bar feels like."

### 2.3 Where do you see yourself in 3 to 5 years?

"As a Staff-level engineer or tech lead owning a whole domain. I care more about mentoring and technical direction than a manager title, unless the work genuinely needs a manager."

### 2.4 What is your best working environment?

"A team that writes design docs and reviews them before code, and where measuring is the default. I do my best work when a decision has to survive a benchmark, not a debate."

### 2.5 What is your notice period?

State your actual notice period. Do not round it down to sound attractive.

### 2.6 What are your compensation expectations?

"I'd like to understand the band for this level first, so we're working from the same frame." If pushed, give a range you have prepared in advance.

---

## 3. Achievement, failure, judgment

Full stories are in [07_behavioral_star_stories.md](07_behavioral_star_stories.md). These are the openers.

### 3.1 What is your biggest technical achievement?

Pick based on the room.

**For a general backend or data room, use Uber Eats menu ingestion.** "My biggest achievement is the Uber Eats menu ingestion pipeline. Restaurant menus arrive as websites, PDFs, and images, and the sites actively block scrapers. I hardened the scraper fleet so extraction success reached 95%+, and built a Kafka and Flink pipeline that deduplicates and writes each menu into the catalog exactly once. Onboarding went from 24 hours to 2 hours and saved about $600K a year."

Say "exactly once" carefully. In practice it is at-least-once delivery plus idempotent writes, meaning a repeated write has no extra effect. Do not claim zero message loss.

**For an AI room, use the AssortSmart safety design.** "At Impact Analytics I designed the AI decision engine so the LLM never touches the database. It receives only a JSON payload of the context it needs, not access to the 2.11-billion-row master table. If the LLM times out, we fall back to deterministic scores. I also shipped Ask Iris, a copilot for planners, and put AI changes behind an 80% CI gate on a 300-case test set."

### 3.2 What is your biggest failure?

"A refactor at Uber that wasn't really a refactor. I had a stacked PR that was supposed to only consolidate constants across 31 files. A downstream test failed. When I diffed my own code, I found I'd slipped in a small helper that changed behaviour. I removed it and added a rule to our checklist: a pure refactor must produce zero test changes. It was caught in CI, so nothing broken shipped. A few weeks later that checklist caught a similar issue for a teammate."

This is story 5 in [07_behavioral_star_stories.md](07_behavioral_star_stories.md). The point is the process fix.

### 3.3 What is your hardest technical decision?

"Choosing which database does which job at Impact Analytics, instead of picking one database for everything. ClickHouse, a columnar database built for big analytical scans, handles planner reads. PostgreSQL handles small keyed edits to single cells, plus users and roles. For AI-generated facts we write insert-only rows, which suits ClickHouse because it is slow at updating rows in place. The decision came from benchmarks, not preference."

### 3.4 Tell me about a time you were wrong

Verbal only, not on the PDF.

"On the line-planning module I went in thinking the big question was the engine, Postgres versus ClickHouse. The benchmark showed it was the schema. Storing every store and every week flat would be about 12 billion rows per plan. Storing the editable truth at choice-by-cluster-by-week is about 25 million rows, and you derive the store-week view on demand. The lesson I took is to check the shape of the data before arguing about the engine."

### 3.5 Tell me about quiet work nobody asked for

"Observability. On the AssortSmart decision engine I added custom JSON telemetry for tokens, dollar cost, step duration, and fallbacks. I wired Datadog distributed tracing on the Go platform, and LangSmith tracing on Ask Iris so we can see every step the agent took. At Masters India, ELK and New Relic tracing helped cut incident triage time by 70%. If they ask for minutes, say roughly from 30 minutes to under 10, which is an estimate."

---

## 4. Leadership

**Direct answer:** "I lead through clear contracts and design reviews, not authority."

"At Uber via EPAM I was tech lead of a 3-engineer pod on FRM. I wasn't their people manager. I agreed API contracts up front so we could work in parallel, ran design reviews, and led the ORM migration. ORM means object-relational mapping, a library that maps database rows to code objects. At Masters India I mentored 2 engineers. One thing I always do is encode fuzzy business rules as code. On FRM, whether an account is 'in scope' became a reproducible rule against the materiality threshold, not a judgment call in a spreadsheet."

Do not merge "led 3" (Uber FRM) with "mentored 2" (Masters India). They are different jobs.

---

## 5. Objection handling

Each answer starts by agreeing with the true part of the objection, then gives the evidence.

**"Your agentic AI work isn't really in production, is it?"**
"Ask Iris is a shipped capability. Changes are gated by an 80% accuracy check in CI on a 300-case test set. That's a promotion gate, not a claim about every tenant. The clustering copilot I sometimes describe is design work, and I say so."

**"You don't have Spark."**
"Correct, Spark isn't on my resume. My streaming work on Uber Eats menus was Kafka and Flink. I can talk about when I'd pick Spark, for example a large batch backfill, but I won't claim I ran it."

**"Have you operated Kubernetes?"**
"I've deployed containerised services with Docker, but I haven't operated Kubernetes clusters or written Terraform. I'm a consumer of that platform, not its operator."

**"Uber was through a vendor, EPAM."**
"Yes, I was at Uber via EPAM. I started as a vendor engineer and ended up owning the FRM scoping backend and leading a pod of 3."

**"Is the 70% reconciliation cut real?"**
"Yes. It's from 14 days to 3 days for the quarterly reconciliation. The technical design doc framed that cut, and that's what the platform delivered for the close. Under it are 36 endpoints, 19 million raw GL rows migrated off Google Sheets, and SOX checks that flag any 50% swing between quarters."

**"98% accuracy on menus sounds too high."**
"It's 98% field fidelity from offline evaluation, meaning we scored extracted fields against a labelled test set. It's not a live production metric."

**"10k RPS at Impact Analytics, can you prove it?"**
"That's the platform's peak requests per second, and it's on the resume. I don't quote any other throughput numbers for that platform beyond it."

**"You've only been at Impact Analytics a few months."**
"I joined in May 2026 for platform and AI ownership and I got it. I'm not someone who changes jobs every year. This move is about scale and review bar."

**"99.9% compliance on ANZ, was that Uber Eats?"**
"No, that was Uber Mobility in Australia and New Zealand, automating driver and vehicle document checks. It's from my past work records, and it's a separate project from menus."

---

## 6. Questions to ask them

Pick three. Prefer engineering and culture questions over flattery.

1. What does the design review process look like before code gets written?
2. Where does the team's on-call pain actually come from right now?
3. Which decision in the last six months would you reverse?
4. What separates a senior engineer from a staff engineer here?
5. If I join, what should be measurably better in six months because I was here?
6. What technical debt are you deliberately living with, and why?

---

## 7. Delivery rules

- **Lead with the outcome, then the mechanism.** "From 189 seconds to 12 seconds, using ClickHouse rollup tables."
- **Know each number's tag** (PDF, MEASURED, ESTIMATED, TARGET, HISTORICAL, or CI gate) and say it the right way.
- **Say "Uber via EPAM" once** early. You don't need to repeat it.
- **Menu Kafka is not Masters Kafka.** They are two different products at two different companies.
- **Stop after the number.** Silence is fine. Let them ask the follow-up.

**Cross-references:** [GROUND_TRUTH.md](GROUND_TRUTH.md) · [18_resume_number_catalog.md](18_resume_number_catalog.md) · [37_senior_screen_deep_qa.md](37_senior_screen_deep_qa.md) · [07_behavioral_star_stories.md](07_behavioral_star_stories.md) · [39_behavioral_question_bank.md](39_behavioral_question_bank.md) · [ApplicationKit.md](../ApplicationKit.md)
