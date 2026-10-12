# Behavioral question bank — mapped to Tarun's stories

**Track:** Final Java + AI · **PDF:** `Tarun_Mittal_SSE_5yr_Java_AI.pdf`

**Stack on this track:** Uber FRM is Java with Spring Boot, Spring Data JPA and Hibernate on MySQL. Masters India is Spring Boot microservices. AssortSmart platform APIs at Impact Analytics are Go with Gin, and the AI agent plane there is Python (FastAPI and LangGraph). Never say Spring Boot for Impact Analytics.

<div class="callout note">
<b>How to use this page</b>
<ul>
<li><b>What it covers:</b> about 43 common behavioral questions, which of your stories answers each one, and ready-to-speak answers for the questions your 10 core stories don't cover.</li>
<li><b>When to read it:</b> before any behavioral, managerial, or "culture fit" round. Use the coverage table the night before. Use the cheat sheet (section 3) 10 minutes before.</li>
<li><b>What to memorise:</b> the story key (which number is which story), the 30-second version of G1 "Tell me about yourself", and the rule "never tell the same story twice in one loop".</li>
<li><b>Full STAR stories</b> live in the story bank, linked below. This page tells you which one to pull.</li>
</ul>
</div>

**Companion files:**
- Full STAR stories: [07_behavioral_star_stories.md](07_behavioral_star_stories.md)
- Why hire me, pitch, objections: [38_why_hire_tarun_qa.md](38_why_hire_tarun_qa.md)
- Project-by-question drill sheet: [40_behavioral_prep_grid.md](40_behavioral_prep_grid.md)
- Company leadership-principle guides: [company_behavior_guides.md](../campaign_extras/behavioral/company_behavior_guides.md)

**Where the question list comes from.** The question list and tips are adapted from [ashishps1/awesome-behavioral-interviews](https://github.com/ashishps1/awesome-behavioral-interviews). Their sample answers are generic fiction and are not copied. Every answer here uses Tarun's real experience.

**What the tags mean.** **PDF** means printed on the resume. **MEASURED** means there is a log, benchmark, or doc behind it. **ESTIMATED** means arithmetic I can show ("roughly, derived from..."). **TARGET** means a design goal ("targeting"). **HISTORICAL** means from my past work records. **Verbal only** means real interview depth that is not on the resume.

<div class="callout warn">
<b>Say these carefully. They are the lines interviewers check.</b>
<ul>
<li>The <b>80%</b> number is a CI promotion gate on a 300-case test set. It is not "every tenant is live at 80%".</li>
<li><b>Ask Iris</b> is a shipped capability. There are no SLA or usage numbers, so quote none.</li>
<li>Cluster Recommendation Copilot and Hindsight are verbal only. They are not on the resume.</li>
<li>FRM's <b>70% cut, from 14 days to 3 days</b>, is on the PDF. State it plainly.</li>
<li>Menu <b>98%</b> is from offline evaluation. Uber work was <b>via EPAM</b>. ANZ <b>99.9%</b> is HISTORICAL and is Uber Mobility, not Uber Eats.</li>
<li>No Spark, no SFT (supervised fine-tuning), no Kubernetes operations.</li>
<li>On the PDF for Impact Analytics: 10k peak RPS and the 2.11B-row master table. The <b>$100 per pass</b> token spend is true but is <b>not</b> on the PDF.</li>
<li>There is no human review queue at Impact Analytics. Don't describe one.</li>
</ul>
</div>

---

## How to structure any behavioral answer

Use **STAR**, which stands for Situation, Task, Action, Result. Add a one-line Lesson at the end.

1. **Situation (one sentence).** Where you were and what was going wrong. "At Masters India, our PHP monolith was falling over during monthly tax-filing deadlines."
2. **Task (one sentence).** What you specifically had to do. "I had to lead the migration without any downtime during deadline weeks."
3. **Action (three or four sentences).** What *you* did, not "we". This is the longest part. Explain any technical term in one clause.
4. **Result (one or two sentences, two or three numbers at most).** "p95 latency went from 1.2 seconds to 300 milliseconds."
5. **Lesson (one sentence).** What you'd carry into the next job. Then stop.

Aim for 60 to 90 seconds. The **short version** of each answer below is about 30 seconds. Use it when the interviewer is moving fast, or as your opening before they ask for more. The **full version** is about 90 seconds.

---

## 0. General tips (read before the loop)

1. **STAR every behavioral answer.** Situation, Task, Action (you, not "we"), Result (number plus its tag), one-line Lesson.
2. **Answer the question they asked.** If it's unclear, ask: "Do you want a technical deep dive or a leadership story?"
3. **Be concise.** 60 to 90 seconds. Stop after the number.
4. **It's fine to pause for five seconds.** Say "Let me pick the strongest example."
5. **No trash talk.** Describe friction with past employers, managers, or teammates as a disagreement between competent people.
6. **Failures end in a process fix.** Stories 5 and 10 already have this shape. Reuse it.
7. **If you haven't had that experience, say so.** "I haven't lived that exact case. Here's how I'd handle it, based on a related story." Never invent one.
8. **Balance "I" and the team.** Lead with what you owned, then credit the people you led or mentored.
9. **Ask clarifying questions** on vague prompts, especially ones that drift into system design.
10. **Prepare questions to ask them.** Section 4 has a list. Pick three per company.

---

## 1. Story key (what each number means)

These are the stories in [07_behavioral_star_stories.md](07_behavioral_star_stories.md). Learn the one-line version so the numbers below mean something.

| # | Story | Where | One line | Say carefully |
|---|---|---|---|---|
| 1 | The reconciled ClickHouse verdict | Impact Analytics | Two expert camps disagreed on adopting ClickHouse. I separated facts from conclusions and proposed three measurable gates. Both camps agreed, and the org committed to ClickHouse in July 2026. | |
| 2 | BigQuery-to-ClickHouse ingestion lane | Impact Analytics | Designed a fast, provably fresh copy of BigQuery data in ClickHouse, with reconciliation checks and a "data as of" stamp on every answer. | This is design depth. The REPLACE PARTITION step was written, not executed. The p95 under 500 ms figure is a TARGET. |
| 3 | Malformed-plan validator | AI planner work | Wrapped an LLM planner in a strict validator plus one self-repair pass. Structural correctness went from 0.54 to 0.99 on an offline eval. | Verbal only. Do not attribute it to Keep/Drop, which has no LLM orchestrator. |
| 4 | Clustering workflow inversion | Impact Analytics | Redesigned store clustering so the agent evaluates about 100 groupings and shows the top 3 with reasons. | Verbal only. All outcome numbers are TARGETs. |
| 5 | The "pure refactor" that wasn't | Uber via EPAM | I slipped a behaviour change into a refactor. CI caught it. I added "pure refactor means zero test changes" to the checklist. | |
| 6 | Coverage that lied | Uber via EPAM | CI showed 34.6% coverage on my Spring Data JPA / Hibernate migration because Mockito mocks skipped the entity layer. I wrote 12 direct tests and reached 100% on the module. | |
| 7 | Disagreeing with the architecture rulebook | Uber via EPAM | Argued, in writing, for putting query methods on JPA entities instead of the repository layer. The exception was accepted and documented. | |
| 8 | Migration under deadline | Masters India | Led the PHP-to-Spring Boot strangler migration during GST filing peaks. p95 went from 1.2 seconds to 300 ms, with no deadline-window outage. | |
| 9 | The anti-bot arms race | Uber via EPAM, Menu | Treated scraper blocking as an experiment loop. Extraction success reached 95%+. | |
| 10 | Double-filing near-miss | Masters India | A retry nearly filed duplicate e-invoices. I flagged it, wrote the review, and added idempotency keys across the whole pipeline. | |

The story file also has extras: story 11 (a connection-leak OOM, packet story, not a PDF bullet), story 12 (the ClickHouse RFC migration), and story 12b (the weekly rollup OOM).

A few terms used above, in one line each:
- **ClickHouse** is a columnar database built for fast analytical reads over billions of rows.
- **Strangler pattern** means replacing an old system one route at a time, so the old and new run side by side until the old one can be switched off.
- **Idempotency key** is a unique tag on a request so that sending it twice has the same effect as sending it once.
- **ORM** (object-relational mapping) is a library that maps database rows to code objects. On FRM that is Hibernate, used through Spring Data JPA, and the mapped classes are called entities.

---

## 2. Coverage matrix — about 43 common questions mapped to your stories

**How to read it.** A number is a story from the key above. **G** means a gap answer written out in section 2b. **H** means an honest "here is how I would approach it" answer, with no invented STAR.

| # | Question | Use | Notes |
|---|---|---|---|
| 1 | Tell me about yourself | G1 | 60 to 90 second walkthrough |
| 2 | Disagreement with your manager or a senior | 1 or 7 | ClickHouse verdict, or the ORM rulebook |
| 3 | Conflict with a teammate | 7 (or 1) | Keep it a technical disagreement, not personal |
| 4 | Tell me about a time you failed | 5 or 10 | Prefer 5 (refactor) or 10 (near-miss) |
| 5 | Led a team, and the outcome | 8 plus FRM led-3 | Masters migration plus FRM design reviews |
| 6 | Worked well under pressure | 8 | GST deadline windows |
| 7 | A difficult decision | 1 or 3 | ClickHouse split decision, or the plan validator |
| 8 | Went above and beyond | 2 or 9 | Freshness as a feature, or the anti-bot loop |
| 9 | You didn't know the answer | G2 | Be honest, then show your research loop |
| 10 | Received tough or critical feedback | G3 | CI coverage failure, then what I learned |
| 11 | Gave someone difficult feedback | G4 | Mentoring at Masters |
| 12 | Prioritised tasks quickly | G5 | Menu bug versus feature, or Masters peak |
| 13 | Anticipated a problem and prevented it | 2, 3, or 10 | Freshness, validator, or idempotency |
| 14 | Difficult customer or stakeholder | G6 | PwC-facing FRM releases |
| 15 | Missed a deadline | G7 | Honest near-miss plus early communication |
| 16 | Heavy workload | 8 plus G5 | Masters peak framing |
| 17 | A significant change at work | G8 | Monolith to microservices, or the AI rebuild |
| 18 | Took initiative without being asked | 1 or 2 | ClickHouse proof of concept, or the BigQuery lane |
| 19 | Mediated a conflict within the team | 1 | Two expert camps |
| 20 | Out of your comfort zone | G8 or 4 | AI ownership, or workflow inversion |
| 21 | Delivered under a tight deadline | 8 | Same as pressure |
| 22 | Took a big risk that failed | 5 (small) or H | Do not invent a catastrophic failure |
| 23 | Designed or tested for diversity and inclusion | H | No product-DEI ownership, so describe the approach only |
| 24 | Explained something technical to a non-technical person | G9 | Materiality to Finance, scores to planners |
| 25 | Disagreed with a colleague | 7 or 1 | Same pool as 2 and 3 |
| 26 | Collaborated with another department | G6 or FRM | Finance, PwC, and engineering |
| 27 | A complex technical project | Menu, 4, or 8 | Pick one. Never merge the two Kafka stories |
| 28 | How you stay up to date with tech | G10 | Real habits only |
| 29 | Why this company? | [38](38_why_hire_tarun_qa.md) section 2.2 | Never improvise cold |
| 30 | Biggest technical challenge | Menu or 3 | Adversarial scraping plus LLM gate, or the validator |
| 31 | Why leave or change company? | [38](38_why_hire_tarun_qa.md) section 2.1 | Positive framing |
| 32 | Many possible solutions, how did you choose? | 1 | Evidence gates |
| 33 | Motivated others or encouraged collaboration | FRM led-3 plus Masters mentored-2 | Pair with story 8 |
| 34 | Improved your technical knowledge | G10 | Same as 28 |
| 35 | Assigned a task you didn't know how to do | G2 | Same shape |
| 36 | Urgent and long-term work at once | G5 | Explicit priority rule |
| 37 | Hard time working with someone | 7 | Keep it technical |
| 38 | A project that didn't go to plan | 5, or early Menu anti-bot misses | End on the process fix |
| 39 | Something new you learned recently | G10 plus ClickHouse or LangGraph | Be concrete |
| 40 | A decision without all the information | 1 or G11 | Write the assumptions down |
| 41 | Linked two problems to one underlying cause | 6 or 10 | Coverage that lied, or the idempotency gap |
| 42 | Sacrificed short-term for long-term | G12 | Strangler sequencing, or ClickHouse gates |
| 43 | Asked to deploy to prod on a Friday (ethics) | G13 | Never hero-deploy |

**Amazon Leadership Principles quick map.** Amazon rounds score you against named principles. Use this to pick a story.

| Principle | Stories |
|---|---|
| Ownership | 2, 8 |
| Dive Deep | 1, 6 |
| Deliver Results | 8 |
| Bias for Action | 8, 9 |
| Earn Trust | 5, 10 |
| Have Backbone; Disagree and Commit | 1, 7 |
| Invent and Simplify | 2, 4 |
| Insist on the Highest Standards | 3, 5 |
| Customer Obsession | 3, 4 |
| Think Big | 4 |
| Learn and Be Curious | 6, 9 |
| Hire and Develop the Best | Mentoring narrative (Masters mentored-2, FRM led-3) |

**Googliness quick map.** Google looks for these traits.

| Trait | Stories |
|---|---|
| Intellectual humility | 1, 5 |
| Comfort with ambiguity | 1, 4 |
| Collaboration | 7, mentoring |
| Bias to action | 2, 8 |
| Doing the right thing | 10 |

---

## 2b. Gap answers (memorise these)

These cover questions the 10 core stories don't answer well.

### G1. Tell me about yourself

**Short version (30 seconds):**

"I'm Tarun Mittal, a senior software engineer with five years building backend and distributed systems in Java, Python and Go. At Masters India I led a migration to Spring Boot microservices for a tax e-invoicing product. At Uber via EPAM I owned a finance reconciliation platform and the Uber Eats menu ingestion pipeline. Today at Impact Analytics I own the Go platform and the AI decision engine for a retail planning product. I'm looking for a senior role where I keep owning systems end to end, with a stronger design-review bar."

**Full version (90 seconds):**

"I'm Tarun Mittal, a senior software engineer with five years designing and owning cloud-native systems in Java, Python and Go.

I started at GeeksforGeeks, where I moved a struggling PHP backend to Django so it could handle traffic spikes during live coding contests.

At Masters India, a GST e-invoicing company, I led the migration off a PHP monolith using a strangler pattern, which means replacing it one route at a time. I used Java and Spring Boot for the new services. p95 latency went from 1.2 seconds to 300 milliseconds, and the Kafka-based submission path handles over 1 million government submissions a day.

At Uber via EPAM I owned two things. First, the FRM scoping backend, which Finance uses to decide which accounts need audit each quarter. I built 36 Spring Boot endpoints, led 3 engineers, and reconciliation went from 14 days to 3 days. Second, Uber Eats menu ingestion, which cut restaurant onboarding from 24 hours to 2 hours and saves about $600K a year.

Now at Impact Analytics I own the Go and Gin platform for AssortSmart, a retail planning product, at 10k peak requests per second. I also own the AI decision engine and shipped Ask Iris, a copilot built on LangGraph. Any AI change has to pass an 80% accuracy gate in CI before it ships.

I'm looking for a senior role where I keep owning systems end to end, with a stronger design-review bar."

Then stop. Don't add hobbies unless they ask.

### G2. You didn't know the answer, or got a task you'd never done

**Short version:** "I say I don't know, and then I show how I'll find out. I name the source I'll use, which might be the docs, a small spike, or a teammate who's done it, and I give a time for the follow-up. I don't bluff."

**Full version:** "First I say plainly that I don't know. Then I lay out how I'll get the answer. That might be the official docs, a small time-boxed spike, or a colleague who has done it before. And I commit to a follow-up time so it doesn't drift.

A related example: when ClickHouse was new to parts of the org at Impact Analytics, I didn't argue about it from taste. I ran a proof of concept on identical data, and the result decided it. Planner pivots went from 189 seconds to 12 seconds.

The lesson is that 'I don't know yet, here's my plan' builds more trust than a confident guess."

### G3. You received tough or critical feedback

This is story 6, framed as feedback.

**Short version:** "CI rejected my Spring Data JPA / Hibernate migration at Uber at 34.6% coverage, even though I was sure the code was tested. My mental model of coverage was wrong. I fixed it with direct tests, reached 100% on the module, and wrote the pattern up for the team."

**Full version:** "At Uber via EPAM, the CI system rejected my Spring Data JPA / Hibernate migration because new-line coverage was only 34.6%. I was sure the code paths were tested, so the tough part was admitting my understanding was wrong.

When I dug in, I found that the repository-layer tests used Mockito to mock out the new entity methods. Mocking means replacing real code with a fake during a test. So the entity code never actually ran, and coverage was counted in the wrong place. I wrote 12 direct JUnit tests on the entity layer, including the rejection cases like empty updates and unknown columns.

Coverage on the changed module went to 100%, and I added the pattern 'test where the code lives, not where it's called' to the team's testing notes. The lesson: a metric you don't understand will lie to you."

### G4. You gave someone difficult feedback

**Short version:** "At Masters India I mentored 2 engineers. One shipped working endpoints with almost no tests on the tax and dedup rules. I started with what was good, showed a real bug a test would have caught, paired on the first test, and added a CI coverage gate so it wasn't about my personal taste."

**Full version:** "At Masters India I mentored 2 engineers. One of them shipped endpoints that worked but had almost no tests around the tax and deduplication rules, which are exactly the rules that cause compliance problems.

I raised it in a one-to-one. I started with what was strong in the work. Then I showed a concrete failure that a missing test would let through. We paired on writing the first test together. And I set a CI coverage gate on changed modules, so the standard came from the pipeline and not from me personally.

On the next piece of work, they presented the design themselves in review. I aim for feedback that helps someone grow, not feedback that catches them out."

### G5. You had to prioritise quickly, or juggle urgent and long-term work

**Short version:** "My rule is that customer-visible correctness and deadline risk come before feature work. I say the priority out loud to my lead, time-box the urgent fix, and then go back to the long-term work with small deadlines."

**Full version:** "I use a simple rule. Anything that affects customer-visible correctness, or creates risk during a deadline window, beats feature work.

At Masters India, during GST filing peaks, I froze migration cutovers in deadline weeks and did the long-term strangler work on quieter days. On Uber Eats menus, a production ingest block always outranked a parser tidy-up.

The part people skip is communication. I tell my lead what I'm dropping and why, I time-box the urgent fix, and then I return to the long-term thread with small mini-deadlines so it doesn't stall."

### G6. A difficult customer or stakeholder

**Short version:** "On Uber's FRM platform, the output went to PwC, the external auditors, so a vague definition of 'in scope' was expensive. I turned the scoping rules into explicit code against the $340M materiality threshold, so every decision could be reproduced and audited."

**Full version:** "At Uber via EPAM, the FRM scoping platform's output went to PwC, the external auditors. The hard part was that 'in scope for audit' was a fuzzy idea. Different people in Finance meant slightly different things.

I encoded the rules explicitly. Materiality is the dollar threshold above which an account must be reviewed, and on the Q4 2025 close it was $340M. I also encoded the residual-risk threshold of $170M, the 5% component threshold, and a logged path for qualitative overrides. Once the rules were code, the system could reproduce and audit any decision. A weekly clarity session with Finance worked far better than arguing inside a spreadsheet.

The platform ended up with 36 Spring Boot endpoints and an 8-table MySQL schema, and quarterly reconciliation went from 14 days to 3 days."

Say carefully: the $340M is on the PDF. The $170M residual figure and the 5% threshold are verbal depth.

### G7. You missed a deadline

**Short version:** "I don't have a dramatic missed deadline that hurt a customer. The closest honest one is on Uber Eats menus: anti-bot defences changed, ingest success dropped, and a planned parser improvement slipped. I flagged it early, protected the critical path, and we recovered to 95%+ extraction success."

**Full version:** "I'll be honest that I don't have a missed deadline that caused customer damage. The closest real one is on Uber Eats menu ingestion.

The restaurant sites we scraped rotated their anti-bot defences, so ingest success dipped, and a parser improvement I'd planned slipped. I flagged the slip early to my lead. I explained the cause, which was an adversarial change outside our control, and proposed a plan. We'd protect the critical ingest path first and push the nice-to-haves. I also added block rate to the same dashboards as parse failures, so we'd see the next change faster.

We recovered to 95%+ extraction success. The lesson is to surface a miss early with a revised plan. Going quiet is the real failure."

**If they push for a harder miss:** use story 5, the refactor regression. Be clear that CI caught it before release and nothing broken shipped.

### G8. A significant change at work, or being out of your comfort zone

**Short version:** "Two real ones. At Masters India I had to move a PHP monolith to Spring Boot microservices while live tax filings kept flowing. At Impact Analytics I moved from classical backends into owning an AI decision engine. In both cases I changed the workflow and the measurement first."

**Full version:** "Two real examples.

First, at Masters India, I led the move from a PHP monolith to Spring Boot microservices, with Kafka for bulk work, while live tax filings kept running. The new part for me wasn't the target architecture. It was the sequencing, meaning which route to move first and when it's safe to cut over.

Second, at Impact Analytics, my background was classical backend work, and I took ownership of the AssortSmart Go and Gin platform plus the Python agent plane built on LangGraph. That includes the AI decision engine and Ask Iris. The first thing I did was set up measurement. Every AI change has to pass an 80% gate on a 300-case test set. And on a separate 200-case benchmark, the AI has to be compared against a 74% rule-based baseline.

The lesson from both: change the workflow and the measurement first, and the technology second."

### G9. You explained something technical to a non-technical person

**Short version:** "I translate the idea into the listener's world. For Finance on FRM, materiality became 'a dollar line, and any account above it must be audited'. For retail planners, the AI score became 'part sales math, part AI judgement, and above a cut-off we keep the item'."

**Full version:** "I start from the listener's job, not from the technology.

To a Finance stakeholder on FRM, I explained materiality as a dollar threshold. If an account is above it, it's in scope for the audit. If someone overrides that, the override is logged with a reason.

To a retail planner at Impact Analytics, I'd explain a Keep/Drop score like this. 'Each product gets a score. 40% of it comes from hard sales math, like how fast it sells. 60% comes from the AI's reading of the product from several angles. If the final score is 0.55 or higher, we recommend keeping it.' And in Ask Iris they can ask why a particular product got its decision.

My rule is no jargon without a one-line translation."

Say carefully: the clustering copilot ("we evaluate about 100 ways to group your stores and show you the top 3 with reasons") is a good analogy too, but it is verbal-only design work. Say so if you use it.

### G10. How you stay up to date, or something new you learned recently

**Short version:** "I read the primary docs and at least one real postmortem before I propose a new system, and I run a measurable spike before I argue for it in a design review. Recently that taught me that in line planning the schema mattered more than the database engine."

**Full version:** "Concrete habits, not vague ones. Before I propose a new system, I read the primary docs and at least one postmortem or engineering blog about it. Then I spike it with a small proof of concept that produces a number, so the design review argues about data.

Things I've learned recently this way: ClickHouse is slow at updating rows in place, which is why insert-only designs win there. LangGraph and tool-calling patterns, which let an LLM call functions safely when you validate its inputs against a schema. And on Uber Eats menus, Flink's keyed deduplication compared with micro-batching.

The most recent lesson is from line planning, which is verbal depth and not on the resume. Storing every store and week flat would be about 12 billion rows per plan. Storing the editable truth at choice-by-cluster-by-week is about 25 million rows. The lever was the schema, not the engine."

### G11. A decision without all the information

This uses the shape of story 1.

**Short version:** "I write the assumptions down, accept every measured fact from both sides, and turn the decision into gated experiments. If a gate fails, we stop. That way we decide without gambling."

**Full version:** "At Impact Analytics, two expert camps disagreed about adopting ClickHouse, and both had part of the evidence. I wrote down every assumption each side was making, and accepted every measured fact, even the ones against my view.

Instead of one big yes-or-no call, I proposed three gates, each with something we could measure. First, fixes inside our existing BigQuery stack. Second, tighter Postgres discipline. Third, a proof of concept with a versioned, insert-only write model. If any gate failed, we'd stop there.

Both camps agreed to the path, and the org later committed to ClickHouse. That's how I decide under incomplete information without betting the company on a guess."

### G12. You sacrificed short-term speed for long-term health

**Short version:** "At Masters India I sequenced the migration slowly on purpose. Read paths and bulk Kafka work moved first, interactive filing last, and no cutovers in deadline weeks. It was slower short-term, but we had no outage during a deadline window."

**Full version:** "At Masters India, the fast option was to cut over big chunks of the monolith at once. I chose slower sequencing on purpose. We sent shadow traffic to read paths first, which means copying real requests to the new service without using its answers. Then bulk Kafka paths moved, and interactive filing moved last. And we froze cutovers in GST deadline weeks.

Short-term delivery was slower. In return there was no outage during a deadline window, which is when an outage would hurt clients most.

I did the same thing with ClickHouse at Impact Analytics. We tried the BigQuery fixes and Postgres discipline first, so we wouldn't burn a quarter moving to the wrong database."

### G13. You're asked to deploy to production on a Friday afternoon

**Short version:** "I wouldn't write and deploy a change alone on a Friday afternoon without review. First I'd ask how severe it is. If it's a real customer outage, I follow the incident process with a minimal fix and a rollback plan. If not, it goes out Monday with a reviewer."

**Full version:** "I wouldn't develop and deploy a change to production alone on a Friday afternoon without review.

First I'd clarify severity. Is this a Sev-1 outage hurting customers right now? If yes, it goes through the incident process. I'd pair with someone if possible, make the smallest fix, put it behind a feature flag or have a quick rollback ready, and write a postmortem afterwards. If it isn't urgent, I'd schedule it for Monday with a short design note and a reviewer.

Hero deploys without a rollback plan are how weekend incidents start. Earning trust matters more than looking helpful in the moment."

### H. Designing or testing for diversity and inclusion (no invented story)

**Short version:** "I haven't owned a formal product-DEI workstream, so I won't make one up. My approach would be to find who the current flow excludes, add test cases for those groups, and measure quality per group, not just the overall average."

**Full version:** "I haven't owned a formal product diversity-and-inclusion workstream, so I won't invent one. Here's how I'd approach a design or testing question.

First, define who the current flow leaves out. That could be language, device, accessibility, or bias in the data behind a ranking. Second, add explicit test cases and evaluation slices for those groups. Third, measure quality per group, not only the global average, because a good average can hide a group that's failing.

The closest muscle I have is on Uber Eats menus, where we handled multilingual menus and sent low-confidence extractions to human review. On the clustering design at Impact Analytics, which is verbal only, a baseline scenario that copies the client's existing setup is always included, so we never silently drop how they used to work."

Say carefully: the human-review path is a Menu detail. Never describe a human review queue at Impact Analytics, because there isn't one.

---

## 3. Rapid reuse cheat sheet

| Signal they want | Open with |
|---|---|
| Ownership | FRM led-3, Menu end to end, or the AssortSmart platform at 10k RPS plus Ask Iris |
| Dive Deep | Story 6 (coverage) or story 1 (assumptions) |
| Bias for Action | Story 8 (sequencing) or story 9 (experiment loop) |
| Earn Trust | Story 10 (near-miss) or G13 (Friday deploy) |
| Customer Obsession | Story 4 (workflow inversion, verbal only) or G6 (PwC) |
| Humility | Story 5 or story 1 |
| Ambiguity | Story 1, story 4, or G11 |

Two hard rules. Never tell the same story twice in one loop. Never merge Masters India Kafka with Uber Menu Kafka, because they are different products at different companies.

---

## 4. Questions to ask them (pick 3)

Expanded from the awesome-behavioral-interviews list. Prefer engineering and culture questions over flattery.

1. What does the design review process look like before code gets written?
2. Where does this team's on-call pain actually come from right now?
3. Which decision in the last six months would you make differently?
4. How do you tell a senior engineer from a staff engineer here? What changes?
5. If I join, what should be measurably better in six months because I was here?
6. What's the biggest piece of technical debt you're deliberately living with, and why?
7. What's the ratio of developers to testers and PMs, and how does planning actually happen?
8. What does onboarding look like for this role in the first 30, 60, and 90 days?
9. What has changed in the org since you joined?
10. What are the most exciting projects on this team in the next two quarters?
11. How do planning and prioritisation work when urgent work lands mid-sprint?
12. What opportunities are there to go deep on scalability or data platforms?
13. Can you describe a typical day for someone in this role?
14. What kind of person usually does well here, and who struggles?
15. What challenges is the company facing that this team is expected to help with?
16. What do you personally like most about working here?

---

## 5. Delivery rules

- **Lead with the outcome, then the mechanism.**
- **Know each number's tag** (PDF, MEASURED, ESTIMATED, TARGET, HISTORICAL, or verbal only) and phrase it to match. Say "targeting" for a TARGET and "roughly" for an ESTIMATE.
- **One story, one owner.** If something is still a design, call it a design.
- **Stop talking after the number.** Let them ask the follow-up.
