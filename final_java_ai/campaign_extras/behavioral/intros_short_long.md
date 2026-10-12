# Interview Intros (short and long)

<div class="callout note">
<b>How to use this page</b>
<ul>
<li>It covers every way you introduce yourself: recruiter screen, hiring manager, technical screen opener, the 3-minute career story, why each job switch, and "why this company".</li>
<li>Read it the night before any first-round call. Say each intro out loud twice with a timer.</li>
<li>Memorise the 30-second recruiter intro word for word. For the longer ones, memorise the order of the beats, not the exact words.</li>
<li>Rule of thumb: never say more than three numbers in one answer. Stop after the number and let them ask.</li>
</ul>
</div>

**Track:** Final Java + AI (`Tarun_Mittal_SSE_5yr_Java_AI.pdf`). The resume summary says "Expertise in Java and Python microservices". On this track Uber FRM is Java with Spring Boot, Spring Data JPA and Hibernate, Masters India is Spring Boot microservices, and the Impact Analytics platform APIs are Go with Gin. The AI agent code at Impact Analytics is Python.

**Words used below, in one line each:**

- **AssortSmart** is Impact Analytics' retail planning software. Retailers use it to decide which products to keep, drop or add each season.
- **ClickHouse** is a database built for fast analytics. It reads only the columns a report needs, so big summaries come back quickly.
- **Go / Gin** is Google's programming language for fast network services. Gin is a small web framework on top of it.
- **Spring Boot** is the most common Java framework for building web services. It wires up the web server, database access and configuration for you.
- **FRM (Financial Risk Management)** is the Uber Finance team that decides which accounts need audit attention each quarter.
- **Kafka** is a durable message queue. Producers drop events in, consumers read them later at their own pace.
- **LangGraph** is a Python library for building LLM agents as a graph of steps with explicit loops and exits.

---

## 1. Recruiter / HR screen

The recruiter is checking three things: are you senior, does your stack match, and are you a calm communicator. Keep it simple. No jargon unless they use it first.

### Short (about 30 seconds)

> Hi, I'm Tarun Mittal. I'm a Senior Software Engineer with five years of experience building backend systems in Java, Python and Go. Recently a lot of my work has been production AI, which means LLM features that are measured and tested before they ship. Right now I'm at Impact Analytics, working on a retail planning product. I'm exploring senior backend roles, and [Company] stood out to me because [one specific reason].

### Long (60 to 90 seconds)

> I'm Tarun, based in Bangalore, with about five years of building production backends.
>
> Right now I'm a Senior Software Engineer at Impact Analytics on AssortSmart. It's software that helps retailers decide which products to keep, drop or add each season. I own two areas. The first is the Go platform that planners use every day. The second is the AI decision engine that scores products. One result I'm proud of: planner reports used to take 189 seconds, and I brought them down to 12 seconds by building a summary layer in ClickHouse, which is a database built for fast analytics.
>
> Before that I was an SDE 2 at Uber, through EPAM. I owned the backend for a Finance risk tool and cut the quarterly reconciliation from 14 days to 3 days. I also owned the Uber Eats menu automation pipeline. Before Uber I was at Masters India on GST e-invoicing, and I started my career at GeeksforGeeks.
>
> I'm looking for a senior role where I own a system end to end, from design to production.

**Numbers used:** 189 to 12 seconds, 14 to 3 days. That is enough. Do not add more here.

**Follow-up they may ask:** "What does 'through EPAM' mean?" Answer: "EPAM is a services company. I was an EPAM employee working full time inside an Uber team, on Uber's codebase and tools."

---

## 2. Hiring manager

The hiring manager wants to know how you work: do you own things, do you measure, can you lead without being told. Lead with ownership, then one proof point per job.

### Short (about 30 seconds)

> I own backend systems end to end: the APIs, the data model, production support, and the quality gates before release. I'm happy to go deep on any of four systems. The Go platform and AI engine at Impact Analytics, the Finance risk backend at Uber, the Uber Eats menu pipeline, or the GST e-invoicing pipeline at Masters India. Which would be most useful for you?

### Long (90 seconds)

> I'd describe myself as a strong senior individual contributor who also leads small groups.
>
> At Uber, through EPAM, I owned the design of the FRM scoping backend, which Finance uses to decide which accounts need audit attention. I was tech lead for 3 engineers on a database-layer migration, and the platform cut quarterly reconciliation from 14 days to 3 days.
>
> At Masters India I mentored 2 engineers while we moved a PHP monolith to Spring Boot services piece by piece, and I was on call for the system.
>
> At Impact Analytics I own the platform engineering and the AI decision flows for AssortSmart. On the AI side I care a lot about honest quality gates. For example, we have an automated test that blocks a new model from release unless it clears 80% accuracy on a fixed test set. When the AI scored worse than a simple rule-based baseline, we kept the rule-based weights instead of shipping it anyway.
>
> So the short version is: I own the system, I measure it, and I don't inflate the results.

**Say this carefully:** "led 3" is Uber FRM. "Mentored 2" is Masters India. Never merge them into "led 5". The 80% is a release gate in CI (continuous integration, the automated checks that run on every code change). It is not "80% accuracy live for every customer".

**Off the PDF, only if asked:** the Go code at Impact Analytics has 100% statement coverage over 1,200+ tests. That is on LinkedIn, not the PDF. Say "it's on my LinkedIn" if you mention it.

---

## 3. Technical screen opener

Use this when the interviewer says "tell me about yourself" at the start of a technical round. Offer a menu so they pick the system you know best.

> I can give you a 60-second walk-through of any system you like and then take questions. The options I know deepest are: the AssortSmart Go platform and ClickHouse layer, the AI decision engine and the "Ask Iris" planner copilot, the Uber FRM finance backend, the Uber Eats menu ingestion pipeline with Kafka and Flink, or the Masters India e-invoicing pipeline with Kafka. Which one is closest to what your team does?

**Why this works:** it shows range, it puts you on home ground, and it hands control back to them. If they say "you choose", pick the one closest to the job description.

---

## 4. The 3-minute career story

Use when they say "walk me through your resume". Go oldest to newest. Each job gets one sentence of context, one thing you owned, and one reason you moved.

> I graduated in IT from IET Lucknow in 2021.
>
> I started at **GeeksforGeeks** as an SDE. I moved their doubt-support platform, where students ask coding questions, from PHP to Django so it could survive traffic spikes during live coding contests. I also built an influencer earnings dashboard. That job taught me to ship product features fast.
>
> Then I joined **Masters India** as an SDE 2. They build GST compliance software. Big Indian companies send us invoices, we validate them and register them with the government's invoice portal. I led the move from a PHP monolith to Spring Boot microservices in Java, mentored 2 engineers, and built the bulk pipeline on Kafka that handled over a million government submissions a day. That was my first time owning a migration end to end.
>
> Next I joined **Uber through EPAM** as an SDE 2. I owned the Java Spring Boot backend of a Finance risk tool that replaced Google Sheets with a proper MySQL database, and I was tech lead for 3 engineers. I also owned the Uber Eats menu automation pipeline, turning restaurant menus, including messy PDFs, into Uber's catalog format.
>
> Now I'm a **Senior Software Engineer at Impact Analytics**. I own the Go platform for AssortSmart, the ClickHouse analytics layer, and the AI decision engine that tells retailers which products to keep or drop.
>
> Each move added a layer: product features, then owning a migration, then Uber-scale engineering standards, then data platforms plus production AI. Next I want a role where I own a system for several years.

**Numbers used:** mentored 2, a million a day, led 3. Keep it at that. Let them ask for the rest.

---

## 5. Why each switch (keep each under 45 seconds)

**GeeksforGeeks to Masters India (about 1.3 years).**
> At GFG I was shipping features on a consumer learning platform. Masters India offered ownership of a regulated product and a real platform migration. I wanted to grow from feature delivery into owning a service cutover and mentoring juniors, and that's what I got.

**Masters India to Uber via EPAM (about 1.5 years).**
> I had taken the GST platform through migration and scale. Uber was a jump in engineering bar and systems complexity. I wanted the discipline of a large monorepo with Bazel, which is Google-style build tooling, and work that sat next to Finance and audit.

**Uber via EPAM to Impact Analytics (about 1.9 years).**
> I wanted deeper ownership of data platforms and production AI, not only service APIs. Impact Analytics offered a senior role around ClickHouse analytics and agentic AI for retail planning. That's where I want to go deep.

**Why are you exploring after a few months at Impact Analytics?**
> I joined for a senior charter around analytics and AI. The work itself has been great, and I've shipped real things there. What I'm looking for now is a larger production surface and a stronger design-review culture, where I can own a domain for several years. So I'm talking to fewer companies, more carefully.

**If they say "four companies in five years":**
> Each move added a layer. The longest stretch, at Uber, shows I stay when the scope keeps growing. That's what I'm optimising for again.

**Do not:** call anyone toxic, lead with compensation, say the current job doesn't count, or apologise as if you failed.

---

## 6. "Why this company?" templates

The formula is one sentence about their product plus one sentence linking it to something you have actually built. Replace the brackets.

| Company | What to say |
|---|---|
| Amazon | "Ownership and Dive Deep match how I work. I've run migrations end to end, built a Finance tool where every number had to be auditable, and put hard quality gates in front of AI releases." |
| Google | "I want large-scale reliable systems with strong design review. My recent work is a Go service edge, a ClickHouse analytics layer, and LangGraph agents with offline evaluations, so the problems feel familiar but bigger." |
| Microsoft | "I'm drawn to cloud and applied-AI platform problems. I like shipping AI behind honest release gates rather than shipping on vibes." |
| LinkedIn | "LinkedIn's data scale interests me. I've worked with multi-billion-row analytics tables and with streaming ingestion on Kafka and Flink." |
| Apple | "I care about quality bars. At Uber I raised a module's test coverage to 100% during a migration, and at Impact Analytics I lock each copilot session to the user's data scope when it connects." |
| Netflix | "I like high ownership with real operational responsibility. I build my own observability, like structured JSON telemetry for every AI batch and LangSmith traces for the copilot." |
| Atlassian | "I like collaboration products and practical distributed systems. A lot of my Uber Finance work was about many people editing the same data safely." |
| Salesforce | "Trusted multi-tenant platforms are what I build now. Tenant isolation, access control and an auth chain that checks several identity providers are all in my current work." |

**Words in those lines:** *multi-tenant* means one system serves many customer companies, and each must see only its own data. *Offline evaluation* means testing a model against a fixed set of known-correct answers before release. *LangSmith* is a tracing tool for LLM apps that records each step an agent took.

---

## 7. Things that are verbal only (not on the PDF)

Two Impact Analytics projects are real work but are not resume bullets: the **Cluster Recommendation Copilot** (an assistant for grouping stores) and **Hindsight**. Mention them only if the interviewer asks about your broader AI roadmap.

If asked, say:
> Those are design and build work I've done beyond what's on the resume. The resume focuses on the shipped pieces: the Go platform, the ClickHouse layer, the Keep/Drop decision engine, and Ask Iris.

---

## 8. Honesty checklist for any intro

- Say "Uber via EPAM" or "Uber through EPAM" once. Never just "I worked at Uber".
- Ask Iris is a **shipped capability**. Do not invent user counts or uptime numbers.
- The 80% is a release gate in CI, not live accuracy for all tenants.
- No Kafka, Flink or Kubernetes operations at Impact Analytics. Kafka and Flink are Uber Menu. Kafka is also Masters India, but that is a different product.
- ANZ document compliance is historical Uber Mobility work, not Uber Eats.

Related: [Why hire you](why_hire_you.md) · [STAR bank](star_bank.md) · [Company guides](company_behavior_guides.md) · [Full why-hire Q&A](../../prep/38_why_hire_tarun_qa.md)
