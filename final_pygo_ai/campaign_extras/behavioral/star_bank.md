# Behavioral / managerial rounds: STAR stories (Final PyGo + AI)

<div class="callout note">
<b>How to use this page</b>
<ul>
<li>It holds every behavioral story you own, written as first-person answers you can say out loud in 60 to 90 seconds.</li>
<li>Read it before any behavioral, managerial or "bar raiser" round. Pick 2 or 3 stories per company using the <a href="company_behavior_guides.md">company guides</a>.</li>
<li>Memorise the first sentence and the lesson of each story. The middle can be in your own words.</li>
<li>Never tell the same story twice in one interview loop. This bank gives you enough coverage.</li>
</ul>
</div>

**Track:** Final PyGo + AI. Uber FRM is FastAPI and SQLAlchemy 2.0. Masters India is FastAPI. Impact Analytics platform APIs are Go with Gin. The AI agent code is Python.

## What STAR means and how to tell one

STAR stands for **Situation, Task, Action, Result**. It is the structure interviewers expect for "tell me about a time when..." questions.

- **Situation** (1 to 2 sentences): where you were and what was going wrong.
- **Task** (1 sentence): what you personally had to achieve.
- **Action** (3 to 4 sentences): what *you* did. Say "I", not "we", for your part.
- **Result** (1 to 2 sentences): what changed, with at most 2 or 3 numbers.
- **Lesson** (1 sentence): what you'd carry to the next job.

Most of the time goes to Action. If you notice you're spending a long time on Situation, cut it.

## Status tags used below

- **PDF**: the story backs a resume bullet. Safe to tell anywhere.
- **Verbal, not on PDF**: real work, but not a resume bullet. Tell it only when it fits the question, and say it isn't on the resume if they ask.
- **Design**: you designed it. Say "I designed", never "it runs in production".
- **Packet**: a prepared story that is not a resume bullet. Tell it as an example, without claiming infrastructure ownership.

## Coverage matrix

| # | Story | Status | Amazon Leadership Principles | Google "Googleyness" signals |
|---|---|---|---|---|
| 1 | The ClickHouse disagreement | Verbal context for PDF platform work | Are Right, A Lot · Have Backbone · Dive Deep | Intellectual humility · ambiguity |
| 2 | BigQuery to ClickHouse ingestion lane | Design, verbal | Ownership · Invent and Simplify | Bias to action |
| 3 | Malformed-plan validator | Verbal, not on PDF | Customer Obsession · Highest Standards | Problem-first thinking |
| 4 | Clustering copilot inversion | Verbal, not on PDF | Think Big · Customer Obsession | Ambiguity · user empathy |
| 5 | The "pure refactor" that wasn't | Uber FRM | Highest Standards · Earn Trust | Humility, owning mistakes |
| 6 | Coverage that lied | Uber FRM (PDF) | Dive Deep · Learn and Be Curious | Rigor |
| 7 | Disagreeing with the architecture rulebook | Uber FRM (PDF) | Have Backbone · Earn Trust | Healthy conflict |
| 8 | Masters migration under deadline | Masters (PDF) | Deliver Results · Ownership | Execution under pressure |
| 9 | Anti-bot arms race | Uber Menu (PDF) | Learn and Be Curious · Invent and Simplify | Persistence |
| 10 | Double-filing near-miss | Masters (PDF) | Earn Trust · Highest Standards | Doing the right thing |
| 11 | Connection-leak OOM | Packet, not on PDF | Ownership · Dive Deep | Ambiguity |
| 12 | ClickHouse RFC and migration | IA (PDF) | Bias for Action · technical leadership | Measurement |
| 12b | Weekly rollup out-of-memory | IA (PDF) | Dive Deep · Frugality | Problem solving |
| L1 | Leading 3 engineers | Uber FRM (PDF) | Hire and Develop the Best | Collaboration |
| L2 | Mentoring 2 engineers | Masters (PDF) | Hire and Develop the Best | Collaboration |

---

## 1. The ClickHouse disagreement (two expert camps)

**Use for:** "Tell me about a time you disagreed with your team", "made a decision with incomplete data", "influenced without authority".

**Words:** *ClickHouse* is a database built for fast analytics. It is great at reading huge tables but weak at changing individual rows in place. *PoC (proof of concept)* is a small experiment that proves or disproves an idea before you commit.

> **Situation.** At Impact Analytics the org was split on whether to adopt ClickHouse for the new AI planning product. An audit of the old backend said "no ClickHouse". Senior experts said "yes, move everything to it". Both sides had real evidence, and a wrong call was expensive either way.
>
> **Task.** I had to produce a recommendation that both camps could commit to, without throwing away either side's evidence.
>
> **Action.** First I separated facts from conclusions. I accepted every measured fact in the audit. Then I showed that its "no" came from the old system's habit of updating rows in place, which ClickHouse is bad at. It wasn't a property of planning workloads in general. So I designed an insert-only write model, where every change is a new versioned row, which avoids ClickHouse's weakness. Then I proposed a three-gate path: fix what we could inside the current stack first, tighten Postgres second, and run a versioned-write PoC third. Each gate had a measurable pass or fail.
>
> **Result.** Both camps agreed to the staged path. The PoC held ClickHouse's background mutation queue at zero even at 10 times our expected scale. In July 2026 the org committed to ClickHouse end to end. Nobody "lost", and we didn't spend on infrastructure before the evidence was in.
>
> **Lesson.** When competent people disagree, it's usually about hidden assumptions, not facts. Make the assumptions explicit and the decision often resolves itself.

**Follow-up they may ask:** "What did Postgres keep?" Answer: "Postgres kept the thin metadata: users, roles and access rules. ClickHouse took the large analytical reads."

---

## 2. The BigQuery to ClickHouse ingestion lane (freshness as a feature)

**Status: Design, verbal.** This was the read layer designed for the Cluster Recommendation Copilot, which is not a resume bullet. Tell it as a design you're proud of. Do not claim it runs in production. The 500 ms number is a design target.

**Words:** *BigQuery* is Google's cloud data warehouse. It's cheap for big batch queries but the same query can take very different times because compute is shared. *p95* means the time within which 95% of requests finish. *REPLACE PARTITION* is a ClickHouse command that swaps a whole slice of a table in one step, so readers see either the old slice or the new one, never half.

> **Situation.** The copilot's AI agent needed fast, predictable reads. But our historical data lives in BigQuery, where the same query can take anywhere from 1 to 20 seconds. The obvious fix was to copy the data into ClickHouse. The trap is that copies go stale silently, and a planner making buying decisions on stale data is worse off than one waiting on a slow query.
>
> **Task.** Design the lane from BigQuery into ClickHouse so the agent's reads would be fast and provably fresh.
>
> **Action.** I designed it in three parts. First, nightly exports land in staging tables and get promoted with an atomic partition swap, so nobody reads a half-loaded night. Second, row counts and sums are reconciled per partition against BigQuery, and a mismatch blocks promotion. Third, a freshness stamp, "data as of this date", goes into every agent answer, so staleness is visible in the product instead of found in an incident.
>
> **Result.** The design targets p95 under 500 milliseconds for agent reads. More importantly, it makes silent staleness structurally impossible: loads are all-or-nothing, mismatches block promotion, and the data date is printed on the answer.
>
> **Lesson.** When you copy data for speed, freshness and reconciliation are product features, not ops chores. Design them in on day one.

---

## 3. Fixing the top LLM-planner failure (malformed plans)

**Status: Verbal, not on PDF.** Older prep places this in agent-planner work at Impact Analytics. It is **not** Keep/Drop. Keep/Drop has no LLM planner and runs its steps in a fixed order. The 0.54 and 0.99 scores are offline-evaluation numbers. Confirm which product surface you name before using this story.

**Words:** an *LLM planner* is a model that breaks a user's question into a list of steps for other agents to run. A *schema* is the agreed shape of the data, like a form with required fields.

> **Situation.** We had a multi-agent planner where an LLM turned questions into execution plans. The top failure was malformed plans: plans that named agents that didn't exist, referred to steps that hadn't run yet, or tried to run too many things at once. Structural correctness on our test set was only 0.54.
>
> **Task.** Make plans safe to run without losing the LLM's flexibility.
>
> **Action.** I wrote a strict validator that checks every plan before anything executes. It checks agent names, duplicate step ids, how wide each stage is, and references to future steps. If a plan fails, the system gives the LLM one repair attempt, passing back the exact validation errors. I also made every agent's answer function never throw, so one failing agent produces a labelled partial answer instead of crashing the whole response.
>
> **Result.** Structural correctness went from 0.54 to 0.99 on the offline test set. Failures became visible and recoverable instead of mysterious.
>
> **Lesson.** With LLMs, don't chase the perfect prompt. Put a deterministic contract around the probabilistic part.

---

## 4. Inverting the clustering workflow

**Status: Verbal, not on PDF.** The Cluster Recommendation Copilot is not a resume bullet. Use it only if they ask about product thinking or an AI roadmap. The baseline numbers (1 configuration tried, 8.5% failed runs, 37 of 437) were measured from audits. The "after" numbers are targets. Say "targeting".

**Words:** *store clustering* means grouping a retailer's stores into similar groups, so each group gets a suitable product mix. *Silhouette score* is a standard measure of how well-separated clusters are.

> **Situation.** Store clustering is the base of every assortment plan, but it was the least-assisted step. The system computed which store attributes mattered and then made people choose from raw score lists. Audits showed users tried exactly one configuration per plan, and 8.5% of runs failed, mostly because of input mistakes.
>
> **Task.** Define the AI rebuild of this module, with user adoption as the main risk.
>
> **Action.** I flipped the workflow. The user states only what the system can't work out: which part of the product hierarchy and which reference period. The agent does the rest. It selects features by statistical significance, evaluates a large batch of candidate clusterings and scores them, and presents the top 3 with evidence and plain-English reasons. One of the three is always a baseline that mimics the client's old setup. The human approves at explicit checkpoints. I also kept the old manual wizard available per client, so adoption was a choice, not forced.
>
> **Result.** The committed target was under an hour to a finished plan instead of days, with far fewer failed runs. Everything the agent chose stays visible to the planner, and results write back into the existing product tables unchanged.
>
> **Lesson.** The highest-leverage AI feature is often turning the workflow around, not a better model.

---

## 5. The "pure refactor" that wasn't (owning a mistake)

**Use for:** "Tell me about a mistake", "a bug you caused", "your quality standards".

**Words:** a *stacked PR* is one of a chain of small pull requests where each builds on the previous one, so reviewers see small, focused changes. A *refactor* changes how code is organised without changing what it does.

> **Situation.** At Uber, I was shipping a refactor as a stack of 3 PRs. The second PR was supposed to only consolidate constants across 31 files. But a downstream test started failing.
>
> **Task.** Find out why a test that expected the "component" strategy to be kept was now seeing "aggregate".
>
> **Action.** I diffed my own PR line by line. I found I'd slipped in a small helper that quietly downgraded the strategy in one case. That was a behaviour change hidden inside a refactor, which is exactly what a refactor must not do. I removed it and restored the pass-through. Then I added a rule to the team's stacked-PR checklist: a pure refactor must cause zero test changes.
>
> **Result.** It shipped as a true refactor. A few weeks later that checklist rule caught a similar issue in a teammate's PR.
>
> **Lesson.** Call your own fouls fast and turn them into process. Credibility compounds.

---

## 6. Coverage that lied (dive deep)

**Use for:** "Debugging something non-obvious", "your testing philosophy".

**Words:** *statement coverage* is the share of code lines that actually run during tests. A *mock* is a fake object used in tests so you don't call the real thing. An *ORM (object-relational mapper)* lets you work with database rows as code objects instead of raw SQL.

> **Situation.** My Uber ORM migration failed the CI coverage check at 34.6% on new lines, even though I knew those code paths were being tested.
>
> **Task.** Understand how tested code could show up as "not covered".
>
> **Action.** I dug into how coverage was measured. The tests for the data-access layer were mocking the new ORM methods. So the model code itself never actually ran, and coverage was credited to the wrong layer. I wrote 12 direct tests at the model layer, including the rejection paths like empty updates and unknown columns.
>
> **Result.** The changed module reached 100% coverage. The rule "test where the code lives, not where it's called" went into the team's testing notes.
>
> **Lesson.** A metric you don't understand will eventually lie to you.

---

## 7. Disagreeing with the architecture rulebook (backbone, then commit)

**Use for:** "A time you disagreed with a standard", "disagreed with a senior engineer", "conflict with your manager" (frame it upward).

**Words:** a *repository layer* is a folder of functions whose only job is talking to the database. A *classmethod* here is a query function attached directly to the model class that describes a table.

> **Situation.** Uber's team rules said all database access must live in the repository folder. For the ORM migration, I wanted to put query methods on the ORM model classes instead.
>
> **Task.** Either follow the rule mechanically, or make the case for an exception.
>
> **Action.** I wrote down the engineering argument. With queries next to the column definitions, a renamed column breaks the type checker immediately, instead of failing quietly at runtime. The repository stays a thin wrapper, and no business logic leaks into models. I listened to the counter-argument, which was consistency across the codebase. Then I documented the exception explicitly, and I agreed to keep dynamic queries that don't belong to one model as repository functions.
>
> **Result.** The exception was accepted and written down. The bug that started the migration couldn't come back. In the old raw SQL, joined tables had duplicate column names, so some rows were silently mapped to the wrong id. In one case income-statement rows were read with balance-sheet column lists. Typed models with explicit column labels removed that whole class of bug.
>
> **Lesson.** Disagree with a written rationale, commit visibly, and leave the decision auditable.

---

## 8. The migration nobody could pause the business for (deliver results)

**Use for:** "Delivering under pressure", "leading a project end to end".

**Words:** a *monolith* is one big application where everything is deployed together. The *strangler pattern* means replacing a monolith one endpoint at a time, routing each endpoint to the new service once it's ready, until the old app has nothing left. *IRP (Invoice Registration Portal)* is the government system that registers each e-invoice.

> **Situation.** At Masters India, our PHP monolith was falling over during monthly GST filing deadlines. Each slow call to the government portal blocked a worker, and the worker pool ran out. Meanwhile more than 1,500 enterprise clients kept filing.
>
> **Task.** Lead the move to async FastAPI microservices, with no downtime allowed during deadline windows.
>
> **Action.** I used the strangler pattern, endpoint by endpoint behind the gateway. We sent shadow traffic to read endpoints first, to compare old and new answers safely. We moved the bulk background paths onto Kafka before touching interactive filing. We kept the data where it was, in PostgreSQL split by tax quarter, so we didn't add a risky data migration on top. We froze cutovers during deadline weeks. And we protected bulk submissions with idempotency keys, retries and a dead-letter queue.
>
> **Result.** p95 latency went from 1.2 seconds to 300 milliseconds, and we had no outage in a deadline window during the whole migration.
>
> **Lesson.** Sequencing is the real risk-management tool. The migration plan mattered more than the target architecture.

**Follow-up they may ask:** "What was throughput?" Answer: "It went from 700 to 4,000 requests per minute."

---

## 9. The anti-bot arms race (learn and be curious)

**Use for:** "Working against a moving target", "persistence".

**Words:** *Selenium* drives a real web browser from code, so you can load pages that need JavaScript. A *proxy pool* is a set of different IP addresses you rotate through, so a website doesn't block you for too many requests from one address.

> **Situation.** Our Uber Eats menu scrapers were getting blocked. Success rates dropped as source websites kept changing their bot defences.
>
> **Task.** Get extraction reliability back up without an unlimited proxy budget.
>
> **Action.** I treated it as an experiment loop, not a one-off fix. I logged the block signature for each source. I iterated countermeasures: IP rotation, browser fingerprint management and dynamic proxy pools. I set a retry budget per source so retries couldn't run away. And I put block rates on the same dashboards as parse failures, so a new block showed up in minutes.
>
> **Result.** Successful extraction rose to 95% plus. New defences were spotted and countered in days instead of weeks.
>
> **Lesson.** Against a moving adversary, the asset is the feedback loop, not any single trick.

---

## 10. The double-filing near-miss (earn trust, do the right thing)

**Use for:** "Integrity", "a time you raised a problem you could have hidden", "a failure".

**Words:** an *idempotency key* is a unique id for a request, so if the same request arrives twice the system does the work only once. A *dead-letter queue* is a holding area for messages that keep failing, so they can be inspected and replayed instead of retried forever.

> **Situation.** At Masters India, a retried bulk import came close to filing duplicate e-invoices with the government portal. For a client, that's a compliance-grade error. It hadn't caused damage yet, and nobody outside the team would have known.
>
> **Task.** Decide between quietly patching that one retry and treating it as the systemic risk it was.
>
> **Action.** I flagged it to leadership as a near-miss and wrote the incident review myself. Then I added idempotency keys across the entire bulk pipeline, not just the endpoint that almost failed. The key was built from client, file hash and batch index. I also added a dead-letter replay path.
>
> **Result.** Zero duplicate filings after rollout. The near-miss review became the template the team used for later incidents.
>
> **Lesson.** Trust is built in the moments when you could have stayed quiet.

---

## 11. Connection-leak out-of-memory (packet story)

**Status: Packet, not on the PDF.** It's a Python/FastAPI worker story at Impact Analytics. Don't describe it as Kubernetes cluster work, and don't claim cluster operations.

**Words:** *OOM (out of memory)* is when a process uses more memory than allowed and gets killed. A *504* is a "gateway timeout" error. *Backpressure* means slowing down the producer when the consumer can't keep up.

> **Situation.** At peak traffic we saw 504 errors and memory climbing on an async worker.
>
> **Task.** Find the cause without a local reproduction.
>
> **Action.** I lined up the APM traces with heap data. APM (application performance monitoring) shows where time and memory go. Database and HTTP clients were being created inside a long-running async loop without being closed. I fixed it with proper context managers (Python's `async with`, which always closes the resource), added pool limits and timeouts, and added backpressure so the worker couldn't outrun what was downstream.
>
> **Result.** Memory stabilised and the 504s cleared. As follow-up we added a load test at 3 times peak in CI, plus connection-pool metrics.
>
> **Lesson.** In async Python, resource lifetime is a correctness bug, not an infrastructure ticket.

---

## 12. The ClickHouse RFC and migration (bias for action, technical leadership)

**Use for:** "Driving a migration", "deciding with incomplete information", "Are Right, A Lot".

**Words:** an *RFC (request for comments)* is a written design proposal circulated for review. A *pivot* here is a planner's grid view that groups sales numbers by product, store and time. A *rollup table* stores pre-computed totals, so reports read the totals instead of adding up raw rows each time.

> **Situation.** Planner pivots on Postgres were getting slower and slower. On a 250-million-row test, one pivot took 189 seconds.
>
> **Task.** Write the RFC, prove it with a PoC, and get adoption, without pretending ClickHouse replaces Postgres for everything.
>
> **Action.** I wrote the RFC comparing a hybrid design with an insert-only store. I ran a PoC where both databases had exactly the same rows. ClickHouse won the large analytical reads, so I built a pre-aggregation layer of six rollup tables for product, store and attribute, each at season and weekly level. Postgres kept users, roles and other small records that change often. And I kept the LLM away from the big master table, serving it prepared JSON instead.
>
> **Result.** On that 250-million-row test, the pivot went from 189 seconds to 12 seconds. The org committed to ClickHouse for planning analytics.
>
> **Lesson.** Measure first, choose the write model on purpose, and don't treat a database choice as a religion.

---

## 12b. The weekly rollup out-of-memory (hardest technical hurdle)

**Use for:** "Hardest technical problem", "a failure and how you debugged it", "memory at scale". Full technical pack: [`42_clickhouse_rollup_migration.md`](../../prep/42_clickhouse_rollup_migration.md).

**Words:** an *INSERT SELECT* reads from one table, computes, and writes into another in one statement. *Disk spill* means letting a query write temporary data to disk when memory runs out, instead of crashing.

> **Situation.** Building the weekly rollup for a whole season in one INSERT SELECT needed about 170 GB of memory. It failed with "memory limit exceeded" even when we raised the cap to 200 GB.
>
> **Task.** Keep the weekly level of detail without crashing the server.
>
> **Action.** Instead of buying more memory, I shrank the unit of work. I sliced each build into one fiscal week per insert. I set a memory cap and a disk-spill cap, and limited how many weeks ran at once. Then I measured each slice. Even the heaviest weeks fit inside the caps.
>
> **Result.** The weekly rollups built successfully with predictable memory.
>
> **Lesson.** Shrink the unit of work before you buy RAM.

**Say this carefully:** the 170 GB fix is about *loading* data. The 189 to 12 seconds speed-up is about *querying* it. One did not cause the other. The exact caps (55 GB memory, 16 GB spill, 8 threads, 4 weeks in flight) are verbal detail, not on the PDF. If they ask for slice sizes: a product week needed about 11 GB and an attribute week went above 40 GB. An 80 GB cap also failed before the 200 GB attempt.

---

## L1. Leading 3 engineers at Uber via EPAM (FRM)

**Words:** *tech lead of an EPAM pod* means I set the technical direction and reviewed the work of a small EPAM team inside Uber. I was not their people manager.

> **Situation.** The FRM scoping backend needed a clean layered design and a database migration, while the frontend and Finance kept changing requirements.
>
> **Task.** Own the service, keep the pod of 3 shipping, and raise test coverage under Bazel, Uber's build system.
>
> **Action.** I split ownership by layer: request handlers, business logic, and data access. I set PR conventions and reviewed every PR early. I paired on the hardest cutover, the reconciliation move from Sheets to MySQL. Then I stepped back as each person owned their area.
>
> **Result.** The platform shipped 36 endpoints, the module reached 100% statement coverage, and Finance used it for the quarterly close.

**Follow-up they may ask:** "How many tests?" Answer: "Over 1,100." That number is verbal, not on the PDF.

## L2. Mentoring 2 engineers at Masters India

> **Situation.** Two junior engineers were new to FastAPI and async patterns during the monolith migration.
>
> **Task.** Get them shipping on their own without breaking filing-day traffic.
>
> **Action.** I pair-programmed the first canary cutover with them. A canary sends a small slice of traffic to the new version first. I wrote the shared retry and idempotency helpers so they didn't have to reinvent them. I reviewed their PRs for input validation and logging. Then I let them own full services.
>
> **Result.** Both shipped services independently, and the platform reached its latency and throughput goals.

---

## Rapid-fire answers (about 30 seconds each)

**"Why are you leaving?"**
> I've built and owned systems end to end: an AI decision platform, streaming pipelines, and a finance-grade audit tool. Now I want a bigger production surface, a stronger design-review culture, and problems where a 1% improvement really matters.

**"Biggest weakness?"**
> I over-invest in written documents, like decision docs and playbooks. I've learned to time-box them and lead with a one-page summary, because a 20-page analysis nobody reads is its own failure.

**"Conflict with a manager?"** Use story 7, framed as disagreeing upward with a written standard.

**"A time you failed?"** Story 5 (the refactor regression) or story 10 (the near-miss). Both end in a process fix.

**"What are you most proud of?"** Story 1. I turned an org-level disagreement into a staged, evidence-based decision that became the committed direction.

---

## Honesty checklist

- Stories 2, 3 and 4 are not resume bullets. Story 11 is a packet story. Say so if asked.
- Ask Iris is a shipped capability with no invented usage or uptime numbers.
- "Led 3" is Uber FRM. "Mentored 2" is Masters India. Never merge them.
- No Kafka, Flink or Kubernetes operations at Impact Analytics.
- The 170 GB load fix and the 189-to-12-second query speed-up are separate results.

**Also study:** [`07_behavioral_star_stories.md`](../../prep/07_behavioral_star_stories.md) (original story text) · [`39_behavioral_question_bank.md`](../../prep/39_behavioral_question_bank.md) (about 43 common questions mapped to stories) · [`40_behavioral_prep_grid.md`](../../prep/40_behavioral_prep_grid.md) (project-by-question drill sheet).
