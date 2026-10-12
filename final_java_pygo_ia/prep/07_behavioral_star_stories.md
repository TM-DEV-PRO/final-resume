# Behavioral and managerial rounds: my STAR stories

<div class="callout note">
<b>How to use this page</b>
<ul>
<li>This is my bank of 13 behavioral stories (numbered 1 to 12, plus 12b), written the way I would actually say them out loud.</li>
<li>Read it the night before any behavioral, hiring-manager or "culture" round. Pick 2 or 3 stories per loop and never tell the same story twice to the same company.</li>
<li>Memorise the numbers in bold and the "Say this carefully" notes. Everything else I can say in my own words.</li>
<li>To find the right story for a question fast, use the <a href="40_behavioral_prep_grid.md">prep grid</a>.</li>
</ul>
</div>

## Before you start

**What a STAR story is.** STAR stands for Situation, Task, Action, Result. Interviewers use it to check that I did something real, that I know why I did it, and that I can measure what happened. I add a fifth part, **What I learned**, because senior interviewers almost always ask for it.

**How long.** Aim for 60 to 90 seconds. That is one or two sentences of Situation, one sentence of Task, three or four concrete Actions, a Result with a number, and one sentence of learning. Then stop and let them ask follow-ups. The follow-ups are where the real interview happens.

**Amazon Leadership Principles (LPs)** are the 16 values Amazon interviewers score against, such as Ownership, Dive Deep and Earn Trust. **Googliness** is Google's word for how I work with people: intellectual humility, bias to action, collaboration, comfort with ambiguity, and doing the right thing. Most other companies ask the same kinds of questions with different labels, so this mapping works everywhere.

**What the tags mean.** MEASURED means there is a log, document or code behind the number. TARGET means a design goal, so I say "targeting". ESTIMATED means arithmetic I can show. HISTORICAL means it comes from my past work records. "On the PDF" means it is a bullet on my current resume (`Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf`). "Verbal only" means I can talk about it if asked, but it is not a resume bullet.

**Stack wording on this track.** On this resume, Uber FRM uses Java with Spring Boot, Spring Data JPA and Hibernate, and Masters India uses Spring Boot microservices. At Impact Analytics, the platform APIs are written in Go with the Gin web framework, and the AI agent side is Python (FastAPI and LangGraph). Never say Spring Boot for Impact Analytics.

**What is on the Impact Analytics PDF.** Two groups of bullets: Core Infrastructure and Pipeline, and Agentic Flows and Orchestration (Keep/Drop, Missed Opportunities, Top Style, Ask Iris, the 300-case harness and the 80% gate). The Cluster Recommendation Copilot and Hindsight are verbal only. The source of truth for the Impact Analytics wording is `docs/ASSORTSMART_TAB_RESUME.md`.

**Company names.** I always say "Uber via EPAM" once per story, because I was employed by EPAM Systems and worked on Uber's teams.

## Which story covers what

| # | Story | Company | On the PDF? | Amazon LPs | Googliness |
|---|---|---|---|---|---|
| 1 | The ClickHouse decision between two expert camps | Impact Analytics | Background to the ClickHouse bullets | Are Right, A Lot. Have Backbone, Disagree and Commit. Dive Deep | Intellectual humility, ambiguity |
| 2 | BigQuery to ClickHouse ingestion lane (freshness as a feature) | Impact Analytics | Verbal only, design written but not executed | Ownership. Invent and Simplify. Insist on the Highest Standards | Bias to action |
| 3 | The validator for malformed LLM plans | Not tied to a named product, see note | Verbal only | Customer Obsession. Insist on the Highest Standards | Problem-first thinking |
| 4 | Inverting the clustering workflow | Impact Analytics | Verbal only (Cluster Copilot) | Think Big. Customer Obsession. Deliver Results | Ambiguity, user empathy |
| 5 | The "pure refactor" that wasn't | Uber via EPAM (FRM) | Supports the Spring Data JPA / Hibernate migration bullet | Insist on the Highest Standards. Earn Trust | Humility, owning mistakes |
| 6 | Coverage that lied | Uber via EPAM (FRM) | Supports the 100% coverage bullet | Dive Deep. Learn and Be Curious | Rigor |
| 7 | Disagreeing with the architecture rulebook | Uber via EPAM (FRM) | Supports the Spring Data JPA / Hibernate migration bullet | Have Backbone, Disagree and Commit. Earn Trust | Healthy conflict |
| 8 | The migration nobody could pause the business for | Masters India | Yes | Deliver Results. Ownership. Bias for Action | Execution under pressure |
| 9 | The anti-bot arms race | Uber via EPAM (Menu) | Yes | Learn and Be Curious. Invent and Simplify | Persistence |
| 10 | The double-filing near-miss | Masters India | Supports the idempotency bullet | Earn Trust. Insist on the Highest Standards | Doing the right thing |
| 11 | Connection leak causing out-of-memory | Impact Analytics | No, prep story only | Ownership. Dive Deep | Ambiguity |
| 12 | Leading the ClickHouse RFC and migration | Impact Analytics | Yes | Bias for Action. Technical leadership | Measurement |
| 12b | The weekly rollup out-of-memory problem | Impact Analytics | Yes | Dive Deep. Deliver Results | Rigor |

Stories 1 and 12 cover the same ClickHouse decision from two angles. Story 1 is about the disagreement. Story 12 is about leading the work. Use only one of them per loop.

---

## 1. The ClickHouse decision between two expert camps

**Status:** Impact Analytics. This is the background to my ClickHouse bullets. The details of the two camps come from my own notes, not the PDF.

**Questions this answers:** "Tell me about a time you disagreed with your team." "Tell me about a decision you made with incomplete data." "How do you influence people when you have no authority over them?" "What are you most proud of?"

**Words to know.** ClickHouse is a database built for analytics. It stores data by column, so it can scan and sum billions of rows quickly, a bit like reading one column of a huge spreadsheet instead of every row. Its weak spot is editing existing rows in place, because each edit (called a "mutation") rewrites whole chunks of data in the background. OLAP means analytical processing: big read queries that summarise lots of rows.

**Situation.** When I joined Impact Analytics in May 2026, our planners' pivot screens were slow on PostgreSQL. A pivot is the grid where a planner slices sales by product, store and week. The organisation was split on whether to adopt ClickHouse for the new AI planning product. One group had run a live audit of the legacy backend and concluded "no ClickHouse". Senior subject-matter experts were pushing "yes, one unified analytics store". Both sides had real evidence, and a wrong call would be expensive either way.

**Task.** My job was to produce a recommendation the whole organisation could commit to, without throwing away either side's evidence.

**Action.**
- I separated facts from conclusions. I accepted every measured fact in the audit.
- Then I showed that the audit's "no" came from the legacy system's write pattern, which edited rows in place. That is exactly what ClickHouse is bad at. It was not a property of planning workloads themselves.
- I designed an insert-only, versioned write model. Instead of editing a row, you write a new version, and the database keeps only the newest one. That sidesteps ClickHouse's weak spot.
- I proposed a path with three gates, each one measurable. First, fix what we could inside the existing BigQuery stack. Second, tighten how we used Postgres. Third, run a proof of concept (PoC) of the versioned write model in ClickHouse.

**Result.** Both camps agreed to the staged path. In the PoC, the mutation queue (the backlog of pending background rewrites) stayed at zero at 10 times our scale. In July 2026 the organisation committed to ClickHouse end to end. We spent no money on infrastructure before we had evidence, and neither camp "lost".

**What I learned.** When two competent groups disagree, they usually disagree about a hidden assumption, not about the facts. If you make the assumption explicit, the decision often resolves itself.

**Follow-ups they may ask.**
- *"What was in the audit?"* "It measured how the legacy backend behaved, and I accepted all of it. Where I differed was the conclusion. Its pain came from editing rows in place, and the new design didn't do that." If they push for specifics, keep it qualitative.
- *"What would you have done if the PoC failed?"* "That was the point of the gates. If the third gate failed, we would have kept the improvements from gates one and two and stayed on BigQuery and Postgres. Nobody would have spent money on a migration that didn't work."
- *"What stayed in Postgres?"* "Thin metadata, user access management (who can see which part of the product hierarchy) and roles. ClickHouse took the large analytical reads."
- *"You'd only been there two months. How did you get people to listen?"* "I didn't ask anyone to trust me. I wrote it down, accepted their facts, and proposed gates that anyone could check. The evidence carried the decision."

**Say this carefully.** The "10 times scale" and the July 2026 commitment come from my notes, not the PDF. The PDF numbers that came later (from 189 seconds to 12 seconds) are a separate measurement. That story is in Story 12.

---

## 2. The BigQuery to ClickHouse ingestion lane (freshness as a feature)

**Status:** Impact Analytics, verbal only. This is a **design I wrote, not something that was executed**. It was meant for the Cluster Recommendation Copilot, which is also verbal only. The p95 under 500 ms and the 0.1% tolerance are TARGETS in the design, not measured results.

**Questions this answers:** "Tell me about a design decision you're proud of." "How do you handle failure modes nobody else is thinking about?" "Tell me about a time you raised the bar."

**Words to know.** BigQuery is Google's cloud data warehouse. Its compute is shared across users, so the same query can take 1 second one minute and 20 seconds the next. p95 latency means 95 out of 100 requests finish faster than that time. A partition is a slice of a table, for example one season of data. `REPLACE PARTITION` is a ClickHouse command that swaps a whole slice in from a staging table in one step, so readers see either the old slice or the new one, never half of each. Reconciliation means comparing row counts and totals between the source and the copy.

**Situation.** The copilot's design had agents asking many small data questions ("probes") while a planner waited, so they needed fast, predictable answers. The design target was p95 under 500 milliseconds. But our historical data lives in BigQuery, where the same query can take anywhere from 1 to 20 seconds. The obvious fix is to copy the data into ClickHouse. That has a known trap: copies go stale silently. A planner making buying decisions on stale data is worse off than one waiting for a slow query.

**Task.** Design the ingestion lane from BigQuery into ClickHouse so the agents' read path is both fast and provably fresh.

**Action.** I designed it in three parts.
- **Atomic loads.** Scheduled exports land in ClickHouse staging tables first. They get promoted to the live table with `REPLACE PARTITION`, so nobody ever reads a half-loaded night.
- **Reconciliation that blocks.** Before promotion, each partition's row count and sums are compared with the BigQuery source. If they differ by more than 0.1%, promotion is blocked.
- **Freshness on the answer.** A "freshness sentinel" stamps the data-as-of date onto every agent recommendation. If data is stale, the planner sees it in the product instead of us discovering it in an incident.

I also added a nightly precompute of attribute significance (which store attributes actually explain sales differences) for product hierarchies with active plans. That way most copilot sessions would start with that work already done.

**Result.** The design was written but not executed. What I can honestly claim is the design's property: silent staleness is structurally hard. Loads are atomic, mismatches block promotion, and the as-of date is printed on every answer. The latency number is a target, not a measurement.

**What I learned.** When you copy data for speed, freshness and reconciliation are product features, not operations chores. Design them in on day one.

**Follow-ups they may ask.**
- *"Why not just query BigQuery directly?"* "Because shared compute makes its latency unpredictable, from 1 to 20 seconds for the same query. An agent making many small probes would feel that every time."
- *"Did this ship?"* "No. I wrote the design and it wasn't executed. What we actually ran for ClickHouse migrations was simpler. If a season's copy went wrong, we dropped that partition and recopied it."
- *"Why 0.1%?"* "It was the tolerance in the design, tight enough to catch a broken load but loose enough to ignore rounding. I'd tune it with real data."

**Say this carefully.** Never say "the read plane serves p95 under 500 ms". Say "the design targeted p95 under 500 ms". Never say `REPLACE PARTITION` ran in production. The rollback we actually used was DROP PARTITION, then recopy that season. That is not an atomic swap with live readers.

---

## 3. Fixing the top failure in an LLM planner (malformed plans)

**Status:** Verbal only, not on the PDF. Older prep does not name which system this was. Confirm the project in my own records before using this story. Never attach it to Keep/Drop, because Keep/Drop has no LLM orchestrator. Its batch order is fixed. The 0.54 and 0.99 numbers come from an offline evaluation in my prep notes.

**Questions this answers:** "What's the hardest technical problem you've solved?" "How do you keep quality high with non-deterministic systems like LLMs?"

**Words to know.** An LLM (large language model) planner is a setup where the model breaks a user's question into a list of steps, called an execution plan, that other agents then run. A validator is ordinary code that checks the plan before anything runs. A forward reference is when step 2 tries to use the result of step 4, which hasn't happened yet.

**Situation.** We had a multi-agent planner where an LLM broke questions into execution plans. Malformed plans were our top failure class. They called agents that didn't exist, they had forward references, or a stage tried to run too many things at once. On our evaluation set, only 0.54 of plans were structurally correct.

**Task.** Make plans safe to execute without giving up the flexibility of the LLM.

**Action.**
- I wrote a strict structural validator over the plan's schema. It checked for unknown agent names, duplicate step ids, stages that were too wide, and forward references. It runs before anything executes.
- If validation fails, the system does one self-repair pass. It sends the LLM the specific errors and asks for a fixed plan.
- I made every agent's `answer()` function non-throwing. If one agent fails, the user gets a clearly labelled partial answer instead of a crash.

**Result.** Structural correctness went from 0.54 to 0.99 on the offline evaluation. Failures became explicit and recoverable instead of mysterious.

**What I learned.** With LLMs, don't chase a perfect prompt. Put a deterministic contract around a probabilistic component.

**Follow-ups they may ask.**
- *"Why only one repair pass?"* "To keep cost and latency bounded. If the model can't fix a plan when it's told exactly what's wrong, a second or third try rarely helps, and an endless loop is worse than a clear failure."
- *"What does 0.99 mean exactly?"* "99 out of 100 plans in the evaluation set passed the structural validator. It's structure, not whether the final answer was right."

---

## 4. Inverting the clustering workflow

**Status:** Impact Analytics, **verbal only, not on the PDF.** This is the Cluster Recommendation Copilot. Use it only if they ask about product thinking or a clustering roadmap. The "before" numbers came from live audits in my notes. The "after" numbers are TARGETS, not results.

**Questions this answers:** "Tell me about a time you challenged the status quo." "Show me some product thinking." "How do you handle ambiguity?"

**Words to know.** Store clustering means grouping stores that behave alike, so each group gets an assortment that fits it. For example, small urban stores in one group and large suburban stores in another. "k" is the number of groups. A silhouette score measures how cleanly separated the groups are. Higher is better.

**Situation.** Store clustering is the foundation of every assortment plan, but it was the least-assisted step. The system computed which store attributes mattered and then made people choose from raw score lists. Our live audits showed users tried exactly 1 configuration per plan, out of a huge search space (12 algorithms, k from 3 to 10, and any subset of attributes). 8.5% of runs failed (37 out of 437), and more than 80% of those failures were input mistakes. Nothing was reproducible.

**Task.** Define how to rebuild the module with an AI agent, with adoption risk as the main constraint.

**Action.**
- I inverted the workflow. The user states only what the system can't work out alone: the product hierarchy and the reference time period.
- The agent turns that into concrete scopes and picks features by statistical significance. It evaluates about 100 candidate clusterings in a batch and scores them on silhouette.
- It shows the **top 3 with evidence** and a plain-English rationale. One of the three is always a baseline that mimics the client's old configuration, so the planner can compare against what they know.
- The planner confirms the choice at clear checkpoints before anything is written back.
- I kept the old manual wizard alive per client, so adoption is opt-in, not forced.

**Result.** The design committed to these targets: under 1 hour to a finalised plan, down from days. Top 3 of about 100 evaluated candidates, up from 1 configuration ever tried. Failures under 2%. Features and k fully visible to the planner. Results write back into the existing product tables unchanged.

**What I learned.** The highest-leverage AI feature is often turning the workflow around, not a better model.

**Follow-ups they may ask.**
- *"Did this ship?"* "No, it's a design with committed targets, and it isn't a resume bullet. I can walk you through the design and the audit numbers that motivated it."
- *"Why keep the old wizard?"* "Because adoption was the biggest risk. Planners trust what they know. Letting each client opt in costs a bit of maintenance, but it means nobody gets forced onto a tool they don't trust yet."

**Say this carefully.** These are targets, so say "targeting under 1 hour", not "cut it to under 1 hour". Don't describe the checkpoints as a human review queue or a "human-in-the-loop system". My resume makes no human-in-the-loop claim. One more thing: another prep doc phrases the candidate target as "at least 20 configurations". This story says "about 100". Check my design notes and use one number consistently.

---

## 5. The "pure refactor" that wasn't (owning a mistake)

**Status:** Uber via EPAM, FRM (Financial Risk Management) scoping platform. Supports the Spring Data JPA / Hibernate migration bullet.

**Questions this answers:** "Tell me about a mistake you made." "Tell me about a bug you caused." "How do you hold your own quality bar?" "Tell me about a time you failed."

**Words to know.** A refactor is a change that tidies code without changing what it does. Stacked PRs are a chain of small pull requests, each one built on the one before, so reviewers see one small step at a time. In this codebase, a scoping "strategy" decides whether scoping is done at the component level (COMPONENT) or rolled up (AGGREGATE).

**Situation.** At Uber via EPAM, I was running a 3-PR stacked refactor. PR 2 was supposed to be constants only: moving repeated fixed values into one place across 31 files. A downstream test started failing.

**Task.** Find out why a test that asserts "keep the COMPONENT strategy when the selection is empty" was now getting AGGREGATE.

**Action.**
- I diffed my own PR line by line, assuming the bug was mine until proven otherwise.
- I found it. I had slipped in a small `resolveStrategy` helper that silently downgraded the strategy. That was a behaviour change hidden inside a refactor.
- I removed it and restored the simple pass-through.
- I added a rule to the team's stacked-PR checklist: "a pure refactor means zero test changes". That way this kind of mistake gets caught by process, not by someone happening to notice.

**Result.** The PR shipped as a true refactor. A few weeks later the checklist caught a similar issue in a teammate's PR.

**What I learned.** Call your own fouls fast and turn them into process. Credibility compounds.

**Follow-ups they may ask.**
- *"Why did you add the helper in the first place?"* "It felt like a harmless clean-up while I was in the file. That's exactly the trap. Any behaviour change, however small, belongs in its own PR with its own tests."
- *"How did you tell the team?"* "I raised it myself, with the fix and the checklist item ready at the same time, so the conversation was about prevention, not blame."

---

## 6. Coverage that lied (dive deep)

**Status:** Uber via EPAM, FRM. Supports the bullet on raising module statement coverage to 100%.

**Questions this answers:** "Tell me about debugging something non-obvious." "What's your testing philosophy?"

**Words to know.** Statement coverage is the percentage of code lines that actually run during tests. Mocking means replacing a real piece of code with a fake one in a test, so you can test the caller in isolation. In Java the usual mocking library is Mockito, and the tests themselves run on JUnit 5.

**Situation.** My Spring Data JPA / Hibernate migration at Uber via EPAM failed the CI (continuous integration) coverage check at 34.6% on new lines, even though I knew those code paths were being exercised by tests.

**Task.** Understand how tested code could show up as "uncovered".

**Action.**
- I dug into how coverage was being measured.
- The repository-layer tests were replacing the new entity methods with Mockito mocks. So the entity code never actually ran during tests. The mocks had moved coverage to the wrong layer.
- I wrote 12 direct JUnit tests at the entity layer, including the rejection paths: empty updates and unknown column names.

**Result.** The changed module reached 100% statement coverage. The pattern "test where the code lives, not where it's called" went into the team's testing notes.

**What I learned.** A metric you don't understand is a metric that will lie to you.

**Follow-ups they may ask.**
- *"Is 100% coverage worth it?"* "On a small, critical module that handles financial data, yes. Here the point wasn't the number. The number was hiding the fact that the real code never ran."
- *"How many tests overall?"* "The platform had over 1,100 tests." (This is verbal, not on the PDF.)

---

## 7. Disagreeing with the architecture rulebook (backbone, then commit)

**Status:** Uber via EPAM, FRM. Supports the Spring Data JPA / Hibernate migration bullet.

**Questions this answers:** "Tell me about a time you disagreed with a standard." "Tell me about a disagreement with a senior engineer or manager." "Tell me about a conflict with your manager." For the manager version, frame it upward: I made the case to the people who owned the rules.

**Words to know.** An ORM (object-relational mapper, here Hibernate used through Spring Data JPA) lets code work with database rows as Java objects called entities. A repository layer is a folder of code whose only job is talking to the database. A `@NamedQuery` is a JPQL query declared on the entity class itself, right next to the fields that define the table's columns.

**Situation.** The team's architecture rules said all data access lives in the `repository/` folder. For the Spring Data JPA / Hibernate migration, I put the query definitions on the entity classes instead.

**Task.** Either follow the rule mechanically or make an honest case for the exception.

**Action.**
- I made the engineering case in writing. With the queries next to the field definitions, renaming a field breaks immediately, because Hibernate validates named queries when the application starts, instead of failing at runtime on a real request. The repository stays a thin Spring Data interface. No business logic leaks into the entity.
- I listened to the counter-argument, which was consistency of the rulebook, and took it seriously.
- I documented the deviation explicitly. I also committed to using plain repository methods for dynamic queries that don't belong to one entity.

**Result.** The exception was accepted and documented. The latent column-aliasing bug that had motivated the migration could no longer recur. That bug was raw SQL that joined tables with duplicate column names, so rows got silently mapped to the wrong id. In one case, income-statement rows were read with the balance-sheet column list.

**What I learned.** Disagree with a written rationale, commit visibly, and leave the decision auditable.

**Follow-ups they may ask.**
- *"What if they had said no?"* "I would have followed the rule and kept the queries in the repository. I'd still have used explicit, aliased column names to kill the bug. The disagreement was about where code lives, not about whether to fix the bug."
- *"How did you fix the aliasing bug itself?"* "Aliased selects with explicit labels, so every column has one unambiguous name, and then the JPA entity mappings, so column lists come from the entity, not hand-typed SQL."

---

## 8. The migration nobody could pause the business for (deliver results)

**Status:** Masters India. On the PDF.

**Questions this answers:** "Tell me about delivering under pressure." "Tell me about leading a project end to end." "Tell me about a disagreement over sequencing or priorities."

**Words to know.** Masters India sells GST (India's Goods and Services Tax) compliance software. Businesses send us invoices, and we register them with the government's IRP (Invoice Registration Portal). A monolith is one big application. The strangler pattern means replacing it one route at a time behind the same front door, until the old system can be switched off. Shadow traffic means copying real requests to the new service and comparing answers, without showing users the new answer yet. A DLQ (dead-letter queue) is a holding area for messages that keep failing, so they can be inspected and replayed later.

**Situation.** Masters India's PHP monolith was struggling during the monthly GST filing peaks. Its worker pools ran out because they sat blocked, waiting on slow government portal calls. Meanwhile, **1,500+ enterprise clients** kept filing.

**Task.** Lead the migration to Spring Boot microservices, with non-blocking calls to the government portal, with zero tolerance for downtime during filing deadlines. I was also mentoring two engineers through it.

**Action.**
- I used the strangler pattern, moving one endpoint at a time behind the gateway.
- I sent shadow traffic to read paths first, so we could compare answers safely.
- I moved the bulk, Kafka-driven background paths before the interactive filing paths. Kafka is a message queue that lets work be processed in the background.
- I kept the data where it was, in PostgreSQL sharded by tax quarter, to avoid a risky data migration during cutover.
- I froze cutovers during deadline weeks.
- I hardened bulk submissions to the IRP with idempotency keys, bounded retries and a DLQ. An idempotency key is a unique id per job, so a retry can never file the same invoice twice.

**Result.**
- p95 latency went from **1.2 seconds to 300 milliseconds**, a 75% cut.
- The system handles **1M+ government submissions a day** and **100K+ concurrent imports**.
- Throughput went from **700 to 4,000 requests per minute**, roughly 12 to 67 per second.
- We had no outage in a deadline window during the migration.

**What I learned.** Sequencing is the risk-management tool. The migration plan mattered more than the target architecture.

**Follow-ups they may ask.**
- *"Where did the latency win actually come from?"* "Mostly non-blocking calls to the government portal, using Spring WebClient and bounded thread pools, so request threads weren't blocked waiting. Then HikariCP connection pooling, query and index fixes, and Redis for frequent reads."
- *"What was your role versus the two engineers?"* "I led the migration and mentored them. I paired on the first cutover, wrote the shared retry and idempotency helpers, and then let them own full services."
- *"Why not migrate the data too?"* "It would have added a second risky change at the same time. Keeping data in place meant each cutover was only a code change, which we could roll back by routing traffic back."

**Say this carefully.** 1M+ a day averages about 12 per second (1,000,000 divided by 86,400 seconds). Peaks around filing deadlines were roughly 8 to 10 times that, which is ESTIMATED. I "mentored 2" here. Don't mix that with "led 3" at Uber.

---

## 9. The anti-bot arms race (learn and be curious)

**Status:** Uber via EPAM, Uber Eats menu ingestion. On the PDF (95%+ extraction success).

**Questions this answers:** "Tell me about working against a moving target." "Tell me about a time you had to persist." "Tell me about an early failure you turned around."

**Words to know.** The pipeline used Selenium, a tool that drives a real web browser automatically, to collect restaurant menus from source platforms. Those platforms run bot defences that block automated traffic. A proxy pool is a set of different network addresses to send requests from. A retry budget is a cap on how many times you retry a source before you stop.

**Situation.** At Uber via EPAM, our menu scrapers were getting blocked. Success rates kept dropping as the source platforms rotated their bot defences. Before my work, success was an estimated 60 to 65%.

**Task.** Get ingestion reliability up without an unbounded proxy budget.

**Action.**
- I treated it as an experiment loop, not a one-off fix.
- I instrumented each source's block signatures, meaning what a block looks like for that site.
- I iterated on countermeasures: IP rotation, browser fingerprint and user-agent management, and dynamic proxy pools.
- I set adaptive retry budgets per source, so a hostile source couldn't burn the whole budget.
- I put block-rate metrics on the same dashboards as parse failures, so regressions showed up in minutes.

**Result.** Successful extractions rose to **95%+**, from an estimated 60 to 65%. Because of the measurement loop, we detected and countered new defences in days instead of weeks.

**What I learned.** Against an adversarial, moving target, the asset is the feedback loop, not any single countermeasure.

**Follow-ups they may ask.**
- *"What happened after a menu was scraped?"* "It went into a Kafka and Apache Flink pipeline. Flink is a stream-processing engine. It removed duplicates per vendor and menu using a content hash, normalised the schema, and did idempotent upserts into the catalog."
- *"How did this connect to the business result?"* "It fed the bigger outcome. Restaurant onboarding went from 24 hours to 2 hours, saving about $600K a year across 30K+ menus a month."

**Say this carefully.** 60 to 65% is an estimate. The "exactly-once" catalog upserts are really at-least-once delivery plus idempotent writes. Don't claim zero message loss.

---

## 10. The double-filing near-miss (earn trust, do the right thing)

**Status:** Masters India. Supports the idempotency and dead-letter-queue bullet.

**Questions this answers:** "Tell me about your integrity." "Tell me about a problem you raised that you could have hidden." "Tell me about a time you failed."

**Words to know.** An e-invoice registered with the government gets a unique IRN (Invoice Reference Number). Filing the same invoice twice is a compliance error for the client. A retry is an automatic second attempt after a failure.

**Situation.** At Masters India, a retried bulk import came close to filing duplicate e-invoices with the government portal. It hadn't hurt any customer yet, and nobody outside the team would have known.

**Task.** Decide between quietly patching that one retry and treating it as the systemic risk it really was.

**Action.**
- I flagged it to leadership as a near-miss.
- I wrote the incident review myself.
- I retrofitted idempotency keys across the whole bulk pipeline, not just the endpoint that almost failed. Each key was built from client, file hash and batch index, so a retried batch is recognised as the same batch.
- I added a dead-letter replay path, so failed batches could be fixed and replayed safely.

**Result.** We had zero duplicate filings after the rollout. The near-miss review became the template the team used for later incidents.

**What I learned.** Trust is built in the moments where you could have stayed quiet.

**Follow-ups they may ask.**
- *"Why build the key from client, file hash and batch index?"* "That combination uniquely identifies a piece of work. The same client re-uploading the same file gets the same keys, so the system knows it already processed those batches."
- *"Wasn't it embarrassing to raise it?"* "A little, but a duplicate filing would have been far worse for the client. Raising it early was cheap compared to that."

---

## 11. The connection leak that caused out-of-memory errors

**Status:** Impact Analytics, Python/FastAPI worker. **Not a resume bullet. It is a prep ("packet") story.** If it comes up in a Kubernetes context, say the service ran in containers. Do not claim I operated clusters.

**Questions this answers:** "Tell me about a production bug." "Tell me about a cascading failure." "Tell me about diving deep into a problem you couldn't reproduce."

**Words to know.** A 504 is the error a gateway returns when the service behind it takes too long. APM (application performance monitoring) is tooling that shows where time and memory go in a live service. The heap is the memory a program allocates as it runs. In Python, `async with` is a context manager: it guarantees a connection gets closed when the block ends, even after an error. Backpressure means slowing down intake when the downstream system can't keep up.

**Situation.** During peak traffic, an async ingestion and agent worker started returning 504s, and its memory kept climbing.

**Task.** Diagnose it without being able to reproduce it locally.

**Action.**
- I lined up the APM traces against heap snapshots.
- The cause was database and HTTP clients and cursors being created inside a long-lived async loop without context managers. They were never released.
- I fixed it with `async with` blocks, pool limits and timeouts. I added consumer backpressure so the worker could not outrun the systems downstream of it.

**Result.** Memory stabilised and the 504s cleared. As follow-ups, I added a load test at 3 times peak to CI and added connection-pool metrics.

**What I learned.** In async Python, how long a resource lives is a correctness bug, not an infrastructure ticket.

**Follow-ups they may ask.**
- *"Why didn't it show up in testing?"* "Tests ran short loops, so leaked connections never piled up. Only a long-running worker under peak load accumulated enough to matter. That's why I added the 3-times-peak load test."

---

## 12. Leading the ClickHouse RFC and migration (bias for action, technical leadership)

**Status:** Impact Analytics. On the PDF: 15.5 times faster pivots (from 189 seconds to 12 seconds on a 250M-row harness), the KPI formula parser, versioned writes with ReplacingMergeTree, keeping the LLM away from the 2.11B-row table, and the 170GB out-of-memory story (Story 12b).

**Questions this answers:** "Tell me about driving a migration." "Tell me about acting on incomplete information." "Tell me about a time you were right when others doubted." "Tell me about technical leadership."

**Words to know.** An RFC (request for comments) is a written design proposal that others review before work starts. A row-identical PoC means loading exactly the same rows into both databases, so the comparison is fair. A rollup table is a pre-summarised table, like a monthly total kept ready so you don't add up every daily row each time. ReplacingMergeTree is a ClickHouse table type that keeps only the newest version of a row with the same key. Think of a notebook where you never erase: you write the new value below, and a cleaner later crosses out the old lines.

**Situation.** Planner pivots on Postgres were blowing past 30 seconds. On our 250M-row test harness, one heavy pivot took **189 seconds**.

**Task.** Write the RFC, run a proof of concept, and drive adoption, without pretending ClickHouse is a general replacement for Postgres.

**Action.**
- I wrote the RFC. It compared a hybrid store with an insert-only store for the agent workloads.
- I ran a row-identical PoC comparing Postgres and ClickHouse.
- I chose ClickHouse for analytical reads and built a pre-aggregation layer of **six rollup tables** (product, store and attribute, each at season and weekly level).
- I kept Postgres for roles and transactional edits.
- I kept the LLM away from the **2.11B-row** fact table entirely. It gets context as JSON payloads and never a database query tool.

**Result.** The organisation committed to ClickHouse for planning analytics. Pivots went from **189 seconds to 12 seconds** (12.3, rounded), which is **15.5 times faster**, on the 250M-row harness. Several related pieces are now on my resume: the KPI formula parser, the versioned writes with ReplacingMergeTree, the six rollup tables, and the Go data pump that copied rollups between ClickHouse clusters.

**What I learned.** Measure first. Separate how you write data from how you read it. Don't choose a database out of loyalty.

**Follow-ups they may ask.**
- *"Why not just tune Postgres?"* "Postgres stores data by row. A pivot across many columns and hundreds of millions of rows makes it read far more than it needs. Tightening Postgres was one of the gates, but the row-identical benchmark showed the gap was structural."
- *"Why keep the LLM away from the database?"* "Safety and predictability. A model writing its own SQL against 2.11 billion rows can run something huge or wrong. Giving it a prepared JSON context means it reasons over exactly what we chose to show it."

**Say this carefully.** 15.5 times is query time on a benchmark harness. The 170GB out-of-memory fix was about load time for weekly builds. They are separate. One did not cause the other.

---

## 12b. The weekly rollup out-of-memory problem (hardest technical hurdle)

**Status:** Impact Analytics. On the PDF (prevented a 170GB out-of-memory failure on weekly rollup builds). Full technical pack: [`42_clickhouse_rollup_migration.md`](42_clickhouse_rollup_migration.md).

**Questions this answers:** "What's the hardest technical hurdle you've faced?" "Tell me about a failure." "How do you debug memory problems at scale?"

**Words to know.** `INSERT SELECT` builds a table by running a query and inserting its results. While aggregating, ClickHouse keeps running totals per group in memory. That is the "aggregator state". Spilling means writing overflow to disk when memory runs out. OOM means out of memory.

**Situation.** Building the weekly rollup for a whole season in one `INSERT SELECT` needed about **170GB** of aggregator state. It failed with a memory-limit error even when we set the cap to 80GB, and again at 200GB.

**Task.** Keep the weekly level of detail, without overwhelming a replica with about 59 cores and 236 GiB of memory.

**Action.**
- I sliced the work into one fiscal week per insert instead of a whole season.
- I set explicit caps: 55GB of memory, 16GB of spill to disk, 8 threads, and at most 4 weeks in flight at once.
- I measured the slices. An attribute-level week peaked above 40GB. A product-level week was around 11GB. Both fit under the cap.

**Result.** The weekly rollups build reliably at full weekly detail.

**What I learned.** Shrink the unit of work before you buy more RAM.

**Follow-ups they may ask.**
- *"Why not just get a bigger machine?"* "It failed even at a 200GB cap, and season sizes grow. Slicing by week makes memory use bounded and predictable no matter how big the season gets."
- *"Did this make the pivots faster?"* "No, that's a separate result. This fixed how we load the rollups. The 15.5 times speed-up was about query time on the benchmark."

---

## Rapid-fire answers (about 30 seconds each)

**"Why are you leaving? Why big tech?"** "I've built and owned systems end to end: an AI decision platform, a streaming ingestion pipeline and a finance-grade audit tool. Now I want bigger problems. I'm after harder distributed-systems work, a deeper bench of peers to learn from, and infrastructure where a 1% improvement really matters." For the full answer on why I'm moving after joining Impact Analytics in May 2026, see [why switch](13_behavioral_why_switch.md).

**"What's your biggest weakness?"** "I over-invest in written artifacts like decision docs and playbooks. I've learned to time-box them and lead with a one-page summary, because a 20-page analysis nobody reads is a failure too." This works because it's real, specific and shows I've corrected it.

**"Tell me about a conflict with a manager."** Use Story 7 (the rulebook disagreement), framed upward.

**"Tell me about a time you failed."** Use Story 5 (the refactor regression) or Story 10 (the near-miss). Both end in a process fix.

**"What are you most proud of?"** Use Story 1. I turned an organisation-level disagreement into a gated, evidence-based decision that became the committed direction.

---

**Also study:** [`39_behavioral_question_bank.md`](39_behavioral_question_bank.md) maps about 43 common questions to stories. [`40_behavioral_prep_grid.md`](40_behavioral_prep_grid.md) is the one-page drill sheet of question types by project. [`13_behavioral_why_switch.md`](13_behavioral_why_switch.md) has intros and why-switch answers.
