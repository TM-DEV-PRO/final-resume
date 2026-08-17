# Why hire Tarun — screening & behavioral Q&A bank

**Track:** Java/Spring (source) · **PDF:** `Tarun_Mittal_SSE_Java_5yr.pdf` · **Contact:** tm.eng2021@gmail.com · (+91) 9001542418

**Purpose:** the questions that decide recruiter screens and hiring-manager rounds, with full
answers you can say out loud. Technical depth lives in the project packs (`23a`/`23b`/`23c`,
`10`–`14`, `31`–`37`); this file is the *persuasion and honesty* layer.

**Honesty tags:** MEASURED (instrumented) · TARGET (goal, not yet proven) · HISTORICAL (earlier
role, not re-measured) · DESIGN (approved design, build in progress) · ESTIMATED (derived).

<div class="callout warn">
<b>Never break these.</b> Agentic AssortSmart is <b>building, not shipped</b>. FRM <b>70% is a TARGET</b>.
Menu <b>98% / 100% is offline eval</b>, not a live SLA. <b>No Spark</b> and no IA TPS/RPM claims.
Uber work was <b>via EPAM</b>. ANZ is Uber <b>Mobility</b>, and its 99.9% is HISTORICAL.
</div>

---

## 0. The pitch — third-person summary (recruiter blurb / referral)

Paste-ready prose for a recruiter, a referral note, or a LinkedIn "About". Third person on purpose,
so a referrer can send it as-is. Every claim here is on the resume and defensible.

> Tarun Mittal is a Senior Software Engineer with **5 years** of experience designing and owning
> cloud-native, high-throughput distributed systems using **Java, Python, Spring Boot, FastAPI, Kafka, Flink, Redis, PostgreSQL, ClickHouse, and cloud platforms (AWS, GCP)**. He has a proven track record
> of improving system performance, designing high-throughput services, and building reliable,
> event-driven architectures — cutting API p95 from **1.2s to 300ms**, scaling a government
> e-invoicing pipeline to **1M+ submissions a day**, automating a menu-ingestion flow that saved
> **$600K+ a year**, and driving a storage migration proven on a **250M-row** benchmark (189s → 12.3s).
>
> He brings strong expertise in **distributed systems, microservices, concurrency, event-driven
> design, and system design (HLD/LLD)**, plus **Agentic AI and RAG** systems, where he owns the
> architecture of a cluster-recommendation copilot. His problem-solving is evidenced by a
> **Google Code Jam** qualifier rank of **2260 / 37,000+**, a **top-3 national finish at the Smart
> India Hackathon 2020**, and **HackerRank Problem Solving** and **LangChain Academy** certifications.
> His ability to own complex projects end to end, decide with measured evidence rather than opinion,
> and lead and mentor engineers makes him a strong addition to any engineering team.

**First-person, 20-second spoken version:** "I'm a senior backend engineer, 5 years, building
cloud-native distributed systems in Java and Python. I've owned finance-grade services at Uber, scaled a
1M-a-day pipeline at Masters India, and I now own the architecture for an agentic planning copilot.
I decide with benchmarks, I own things end to end, and I can defend every number on my resume."

<div class="callout note">
<b>Honesty note on the "problem-solving" line.</b> Use the real credentials above — Google Code Jam
rank, Smart India Hackathon finalist, HackerRank / LangChain certs. Do <b>not</b> claim a LeetCode
rating or a specific "N problems solved" count; that is not on the resume and cannot be verified.
</div>

---

## 1. Why should we hire Tarun?

### 1.1 Thirty-second answer (recruiter screen)

I am a Senior Software Engineer with 5 years designing and owning cloud-native, high-throughput
distributed systems in Java and Python. At Uber, via EPAM, I owned the FRM Risk Scoping backend —
30+ REST APIs behind 8 finance screens at $340M group materiality — and I owned Uber Eats menu
ingestion end to end, which cut partner onboarding from 24 hours to 2 and saved $600K+ a year at
30K+ menus a month. At Masters India I took a Laravel monolith to microservices, moved p95 from
1.2 seconds to 300 milliseconds, and ran a Kafka e-invoicing path at 1M+ government submissions a
day. Right now I own the architecture for AssortSmart's Cluster Recommendation Copilot and I drove
ClickHouse adoption with a measured 250M-row POC that took a planning pivot from 189 seconds to
12.3 seconds. You get architecture ownership, production discipline, and numbers I can defend.

### 1.2 Ninety-second answer (hiring manager)

Open with the sentence above, then add the three things that actually make me senior:

1. **I own systems end to end, not tickets.** On FRM I owned API contracts, the layered service
   design, and the design reviews for a PwC-facing quarterly close — and I led 3 engineers doing it.
   On Menu I owned acquisition, the Kafka ingest bus, Flink keyed normalize/dedupe, and the LLM
   extraction path with a hard schema gate before anything touched the catalog.
2. **I make storage and platform decisions with evidence, not taste.** I did not argue for
   ClickHouse; I ran a row-identical Postgres → ClickHouse POC on 250M rows and let 189s → 12.3s
   (~15.5x, MEASURED) make the case. I also told the team where ClickHouse was *wrong* — legacy
   in-place keyed updates stay on Postgres.
3. **I am honest about what is proven.** The FRM 70% reconciliation cut is a TARGET. The Copilot is
   design-approved and building, with the bring-up load test still pending. The Menu 98% fidelity /
   100% schema consistency numbers are offline eval. I would rather lose a point in the interview
   than have you discover the gap in month two.

Close on fit: "I want to keep doing this on a bigger system with a stronger engineering bar."

### 1.3 "Why you over someone with more years?"

Years are a proxy for scope, so answer with scope: financial system of record at $340M materiality,
a 1M+/day event pipeline, a cost line I moved by $600K+/yr, a storage migration I justified with a
measured benchmark, and 3 engineers I led plus 2 I mentored. Then be candid about the boundary:
I have not run a 50-engineer platform org, and I am not claiming multi-region or Kubernetes
operations ownership. What I bring is the ability to take an ambiguous business problem, produce a
design others can review, and ship it with instrumentation.

### 1.4 "Why should we *not* hire you?" / biggest risk

Say the real one: my most recent agentic work is **building, not shipped**, so if the role needs
somebody who has already operated an LLM agent product at scale under live traffic, I am not the
strongest candidate on that axis. What I do have is the design, the safety model — read-only tools,
14 audited tools, three human gates — and the measured baseline it has to beat (8.5% clustering-run
failures, 37 of 437, MEASURED). Then pivot to shipped evidence: Menu, FRM, and the Masters Kafka
platform all ran in production.

### 1.5 Differentiators (memorize the shape, not the words)

| Claim | Evidence | Tag |
|---|---|---|
| Owns finance-grade backends | FRM: 30+ APIs, 8 screens, $340M materiality, ~55 line items x 14 entities, led 3 | MEASURED scope |
| Moves real money | Menu: 24h → 2h onboarding, $600K+/yr, 30K+ menus/month | MEASURED |
| Handles genuine scale | Masters: 1M+ submissions/day, 700 → 4,000 req/min, p95 1.2s → 300ms, 1,500+ clients | HISTORICAL |
| Decides with benchmarks | Postgres → ClickHouse, 250M rows, 189s → 12.3s (~15.5x) | MEASURED POC |
| Builds agents safely | Read-only tools, schema gates, human approval before writes; 8.5% failure baseline | MEASURED baseline + DESIGN |
| Grows people | Led 3 (Uber via EPAM), mentored 2 (Masters India) | HISTORICAL |

---

## 2. Motivation and fit

### 2.1 Why are you open to leaving Impact Analytics?

Positive framing, no employer criticism: I have the architecture ownership I wanted and I am
enjoying the agentic work. What I want next is a larger production surface — more traffic, more
tenants, a stronger review culture, and peers who will push my designs harder. I am not running
from anything; I am optimizing for the next five years of technical growth.

### 2.2 Why this company / role?

Do not improvise this. Before the call, write one sentence on each: (a) the product problem you
find genuinely interesting, (b) the specific system in the job description that maps to something
you have owned, (c) what you would want to learn there. Then deliver it as: "Your <system> is the
same shape as <my system> — bursty ingest, strict correctness, human-in-the-loop — and I want to
work on it at your scale."

### 2.3 Where do you see yourself in 3–5 years?

Staff-level individual contributor or tech lead: owning a domain rather than a service, setting
design standards, and mentoring. I care more about scope and technical judgment than about a
management title, though I have led teams and will do it when the work needs it.

### 2.4 What environment brings out your best work?

Clear ownership, written design review before code, and a team that treats measurement as normal.
I do my best work when I can instrument something, argue from data, and have someone senior
disagree with me in a document.

### 2.5 Notice period and availability

State your actual notice period and the earliest realistic start date. Offer flexibility on the
interview schedule rather than promising an unrealistic joining date.

### 2.6 Compensation expectations

Ask for the band first: "What range is budgeted for this level?" If pushed, give a researched range
for senior backend in Bangalore with a note that you are optimizing for scope and team, and that
you will evaluate the whole package. Never anchor below your current total compensation.

---

## 3. Achievement, failure, judgment

### 3.1 Biggest technical achievement

Menu ingestion, because it combined adversarial acquisition, streaming correctness, and LLM output
you cannot trust. Partner menus arrive as JavaScript-heavy sites, PDFs, and images in several
languages. I owned the whole path on GCP: Selenium acquisition hardened with IP rotation, dynamic
proxy pools, and adaptive retries to 95%+ successful ingestions; a Kafka ingest bus so acquisition
survives slow downstream and can be replayed after a bad parser; Flink keyed normalize and dedupe
so a late duplicate page cannot double-apply. Unstructured menus go through LangChain RAG over
Milvus embeddings into Gemini 2.5 Pro, then a hard schema validation gate before upsert, with
low-confidence output sent to human review instead of the catalog. Result: 24h → 2h onboarding,
$600K+/yr saved, 30K+ menus a month, and 98% fidelity / 100% schema consistency in offline eval.

### 3.2 Biggest failure or mistake

Use the constants-refactor regression: I changed shared constants during a refactor and broke
behavior that had no test covering it. The fix was not just the patch — I added the test that would
have caught it, then pushed a CI gate that blocks merges when changed-module coverage drops. That
work is part of how coverage moved from 35% to 82% at Masters India. Lesson stated plainly: if a
change is "obviously safe," that is precisely the change with no test.

### 3.3 Hardest technical decision

Telling the team that ClickHouse was the wrong answer for the legacy path. The benchmarks favored
ClickHouse for large analytical reads, but the legacy module did keyed in-place updates, and a
column store is a bad fit for that write model. So the recommendation was split: aggregate reads to
ClickHouse, cell edits stay on Postgres, and the new agentic planning store is insert-only
ClickHouse end to end. It would have been easier to declare one winner; the honest answer was a rule.

### 3.4 A time you were wrong

The line-planning schema. My first instinct was a flat store-week table, which projected to roughly
12 billion rows. Wrong shape. Modelling the editable truth at choice x cluster x week landed around
25M rows with sub-second month rollups. The lever was the schema, not the engine — I say that out
loud because it is the opposite of the "we switched databases and got faster" story people expect.

### 3.5 Quiet work you are proud of

Observability that nobody asks for until an incident: one OTEL `trace_id` stitched across the agent
tier, the write APIs, and the product analytics, so an agent action can be followed end to end.
At Masters India, the ELK and New Relic alerting plus a client usage dashboard cut incident triage
by 70% and support tickets by 35% (HISTORICAL).

---

## 4. Leadership and collaboration

### 4.1 Leading without the title

On FRM I led 3 engineers as an IC: I owned the API contracts, ran layered design reviews, and split
work so juniors got reviewable slices instead of vague features. Authority came from writing the
design first and being the person who could answer "why this way" for a PwC-facing release.

### 4.2 Disagreement with a senior stakeholder

Use the storage decision or a scope decision, and follow the same shape: state their position
fairly, state what evidence you produced, describe the decision rule you proposed, then the outcome
and what it cost. Never frame the other person as foolish — frame it as two reasonable positions
that a measurement resolved.

### 4.3 How do you mentor?

I mentored 2 engineers at Masters India. Pattern: pair on the first slice, hand over the second with
a written contract, review with reasons rather than rewrites, and let them present their own work in
review. The goal is that they can defend the design without me in the room.

### 4.4 Unclear requirements

Write the ambiguity down and make someone choose. On the scoping work that meant encoding
materiality, qualitative override, residual risk, and the 5% component threshold as explicit rules
against $340M / $170M thresholds, so "in scope" stopped being a judgment call in a spreadsheet and
became a decision the system could reproduce and audit.

### 4.5 Code review

Reviews should reference a contract, not taste: does it match the agreed API shape, is failure
handled, is it observable, is there a test at the level where the logic lives. On my own code I want
the design questioned before the syntax.

---

## 5. Objection handling (the honest answers)

| Objection you will hear | Answer |
|---|---|
| "Your agentic work is not in production." | Correct. Phase 1 design passed adversarial and external review; the bring-up load test is pending. I claim design and build ownership, plus a MEASURED 8.5% failure baseline it must beat. |
| "No Spark?" | No Spark on my resume and I will not claim it. Streaming is Kafka plus Flink for keyed dedupe and event-time ordering; batch and analytics are ClickHouse and BigQuery. I can explain why Flink beat micro-batching for that hot path. |
| "Do you own Kubernetes in production?" | I ship containerised services and know Kubernetes as a consumer. I do not claim cluster operations ownership, multi-region, or Terraform ownership. |
| "Uber via EPAM — was that real ownership?" | Employment was EPAM; the systems, stakeholders, and releases were Uber's. I owned the FRM backend contracts and design reviews, and menu ingestion end to end. Say the vendor relationship first so it never looks hidden. |
| "The 70% reconciliation cut?" | A TARGET for the quarterly close, roughly 2 weeks to 3–4 days. What is built and MEASURED is the platform: 30+ APIs, 8 screens, recon v2 with L1→L2→L3 FSLI trees tied from HFM to public 10-Q filings. |
| "98% / 100% on menus?" | Offline eval on a labelled set, not a live SLA. The 100% is a hard schema validation gate — anything failing the gate never reaches the catalog. |
| "Requests per second on the agent?" | I have no measured TPS or RPM for AssortSmart, so I will not invent one. For measured throughput, use Masters: 1M+ submissions/day and 700 → 4,000 req/min. |
| "Short tenure at Impact Analytics." | Fair. I joined for the agentic rebuild and I have delivered architecture ownership and the storage decision. I am not shopping every year; I am responding to a specific opportunity. |
| "ANZ 99.9%?" | HISTORICAL, from earlier documented work, not re-measured by me now. It was Uber **Mobility** driver and vehicle document compliance against local authority requirements — a different product from Eats menus. |
| "Did you build the frontend?" | No. I claim no React or UI ownership. I own APIs the manual screens and the agent tools both call. |

---

## 6. Questions to ask them

Pick three, and prefer the ones that reveal engineering culture:

- What does the design review process look like before code gets written?
- Where does this team's on-call pain actually come from right now?
- Which decision in the last six months would you make differently?
- How do you tell a senior engineer from a staff engineer here — what changes?
- If I join, what should be measurably better in six months because I was here?
- What is the biggest piece of technical debt you are deliberately living with, and why?

---

## 7. Delivery rules

- **Lead with the outcome, then the mechanism.** "Onboarding went 24 hours to 2" before "Kafka and Flink."
- **Tag every number in the same breath.** "Measured," "target," or "historical" — say it unprompted.
- **One story, one owner.** Menu Kafka is Eats ingest; Masters Kafka is GST e-invoicing. Never merge them.
- **Do not upgrade yourself mid-sentence.** Building stays building.
- **Stop talking after the number.** The strongest close is a metric plus silence.

**Cross-references:** `GROUND_TRUTH.md` (every number and tag) · `18_resume_number_catalog.md` ·
`37_senior_screen_deep_qa.md` (millions / production / performance / deploy) ·
`32_common_interview_qa.md` · `07_behavioral_star_stories.md` · `../ApplicationKit.md` (paste-ready).

**Also study:** [`39_behavioral_question_bank.md`](39_behavioral_question_bank.md) · [`40_behavioral_prep_grid.md`](40_behavioral_prep_grid.md) · [`07_behavioral_star_stories.md`](07_behavioral_star_stories.md).
