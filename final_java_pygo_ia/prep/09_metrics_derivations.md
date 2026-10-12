# Metrics Derivations (current Java + AI PDF, IA = Py/Go)

<div class="callout highlight">
<b>How to use this page</b>
<ul>
<li>It covers every number printed on <code>Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf</code>, one entry per number, grouped by company.</li>
<li>Each entry tells you what the number measures, where it comes from (with the arithmetic), why the business cared, how to say it out loud, and what not to say.</li>
<li>Read it the night before any screen where numbers will be probed. Memorise the "Say it" lines and the "Do not say" lines.</li>
<li>Numbers that are true but not printed on the PDF live in the "Off-PDF but true" section near the end. Numbers from older resumes live in the last section.</li>
</ul>
</div>

The quick one-line version of each number is in the [number catalog](18_resume_number_catalog.md). The per-bullet defence for Impact Analytics is in [IA bullet defense](43_ia_bullet_defense.md). The facts this page must match are in [GROUND_TRUTH](GROUND_TRUTH.md) and the canonical claims file [ASSORTSMART_TAB_RESUME](../../docs/ASSORTSMART_TAB_RESUME.md).

## The tags, explained once

Every entry carries one tag. The tag tells you how to phrase the number when an interviewer pushes.

| Tag | What it means | How to phrase it |
|---|---|---|
| **MEASURED** | There is a log, benchmark output, code constant, config file or design doc that shows this number. | "We measured..." or "The benchmark showed..." |
| **STATED** | The number is printed on the PDF from the project's own source (the AssortSmart tab or the design doc), but this prep folder holds no separate arithmetic for it. | State it plainly. If asked how it was measured, keep the answer qualitative and do not invent extra precision. |
| **TARGET** | A design goal, not a result. | "We were targeting..." |
| **ESTIMATED** | Arithmetic I can show on a whiteboard. | "Roughly, derived from..." |
| **HISTORICAL** | From my past work records and earlier resumes. No artifact I can open today. | State it plainly as the outcome of that project. |

Two habits that apply to every number. First, say from-to numbers in full words: "from 189 seconds to 12 seconds", "from 14 days to 3 days", "from 24 hours to 2 hours". Second, never add precision the source does not have. If the source says "about", you say "about".

---

## Summary line

### "5 years"

- **What it measures:** My full-time software engineering tenure, from GeeksforGeeks in August 2021 to Impact Analytics today.
- **Tag:** HISTORICAL.
- **Derivation:** August 2021 to the present is about five years. The roles are GeeksforGeeks (Aug 2021 to Nov 2022), Masters India (Dec 2022 to Jun 2024), Uber via EPAM (Jul 2024 to May 2026) and Impact Analytics (May 2026 to present).
- **Why it mattered:** It sets the level. Five years with ownership of production systems is a senior backend profile.
- **Say it:** "I have about five years of backend experience across four companies."
- **Do not say:** "Five years at Uber." Uber was via EPAM and ran from July 2024 to May 2026.

---

## 1. Impact Analytics, AssortSmart (May 2026 to present)

AssortSmart is a retail merchandise planning product. Retailers use it to decide which products (articles) to keep, drop or add for each selling season. An **article-season** is one product in one selling season. For example, "Blue linen shirt, Spring-Summer 2026" is one article-season. The PDF has two sub-sections, Agentic Flows and Core Infrastructure, and the numbers below follow the PDF order.

### 1.1 "348k article-seasons"

- **What it measures:** How many article-seasons the Keep/Drop, Missed Opportunities and Top Style pipelines evaluated.
- **Tag:** MEASURED.
- **Derivation:** It is the scored volume across the three pipelines on the AssortSmart tab. It is not the size of the catalog. The catalog is about 1.6M article-seasons (see the off-PDF section). Only articles that are in scope for a decision get scored.
- **Why it mattered:** It proves the engine works at real retailer scale, not on a demo set of a few hundred products.
- **Say it:** "The decision engine evaluated about 348 thousand article-seasons across Keep/Drop, Missed Opportunities and Top Style."
- **Do not say:** "1.6 million article-seasons scored." Do not divide 348k by 88k and claim a number of passes. They are separate counts.

### 1.2 "88k items per pass" (also "88k-article batch runs")

- **What it measures:** How many articles one batch run (one "pass") processes end to end.
- **Tag:** MEASURED.
- **Derivation:** It is the per-pass batch size from the pipeline runs. It sets the memory footprint and how many LLM calls hit the provider's rate limits in one run.
- **Why it mattered:** A pass this size is where provider failures actually happen, which is why the orchestration registry (timeouts, circuit breakers, checkpoints) exists.
- **Say it:** "Each pass processes about 88 thousand items."
- **Do not say:** "$100 per pass" as if it were on the PDF. It is true but off the PDF.

### 1.3 "7 AI lenses"

- **What it measures:** The number of separate analytical viewpoints the LLM scores each article from. A **lens** is one focused question asked to the model, for example "how is the in-season sales trend?" Each lens returns a structured score.
- **Tag:** MEASURED (it is the lens list in the pipeline config).
- **Derivation:** Count of lenses configured in `config/decision.json` and described in the [Keep/Drop pipeline doc](../docs/assort_kd_flow/PIPELINE.md). A cheap prefilter (the lens gate) decides which lenses apply to a given article, and a "decider" step picks the mix.
- **Why it mattered:** Splitting judgement into small lenses keeps each prompt narrow, makes outputs easy to validate, and lets us see which lens drove a decision.
- **Say it:** "The LLM side scores each article through up to seven lenses, and a decider combines them."
- **Do not say:** "Seven agents talking to each other." Keep/Drop has no LLM orchestrator. The batch order is fixed in code: peer, then decider, then lenses, then blend, then explain.

### 1.4 "2.11B-row ClickHouse master"

- **What it measures:** The row count of the main ClickHouse fact table that holds planning data. **ClickHouse** is a column-oriented analytics database: it stores each column separately, so summing one column over billions of rows is fast. A **fact table** holds the raw measurements (sales, inventory) at the finest grain.
- **Tag:** MEASURED (table row count).
- **Derivation:** The row count of the master table as recorded on the AssortSmart tab.
- **Why it mattered:** At this size, letting an LLM run its own queries is dangerous. One bad query could scan billions of rows or exhaust the connection pool. That risk is why we serve context as JSON payloads instead.
- **Say it:** "The master table is about 2.1 billion rows, so the model never queries it. We hand it JSON."
- **Do not say:** "The LLM queries ClickHouse asynchronously." "Async" describes how batches run. The model never gets a SQL tool.

### 1.5 "3-attempt evaluator loop" (Ask Iris)

- **What it measures:** The maximum number of times the Ask Iris evaluator will ask the supervisor to retry an answer before giving up gracefully.
- **Tag:** MEASURED (code constant `MAX_ATTEMPTS = 3`).
- **Derivation:** It is a constant in the Ask Iris graph code. There is also a recursion limit on the supervisor graph.
- **Why it mattered:** Without a cap, an LLM that keeps judging its own answer as "not good enough" can loop forever and burn tokens. The cap bounds cost and latency per question.
- **Say it:** "The evaluator gets three attempts. After that we return a graceful answer instead of looping."
- **Do not say:** Any SLA, questions per week or user count for Ask Iris. It is a shipped capability with no published usage numbers.

### 1.6 "300-case proxy evaluation harness"

- **What it measures:** The size of the offline test set used to decide whether a new model or prompt version may be promoted. A **proxy** set means the labels stand in for real planner decisions, because true "right answers" for Keep/Drop are only known after the season ends.
- **Tag:** MEASURED (`cases.json` in the eval suite).
- **Derivation:** 300 labelled cases in the gold file.
- **Why it mattered:** It turns "the new prompt feels better" into a pass or fail check that runs before anything ships.
- **Say it:** "We built a 300-case proxy evaluation set that every model or prompt change has to pass."
- **Do not say:** "The 300 cases showed 73% lower cost." The 73% came from a different benchmark (see 1.8).

### 1.7 "80% accuracy CI gate"

- **What it measures:** The minimum accuracy a candidate must hit on the 300-case set to be promoted. **CI** (continuous integration) is the automated pipeline that runs checks on every change.
- **Tag:** MEASURED (it is a config value: `eval.json` has `gold_min_accuracy: 0.8`).
- **Derivation:** The gate is a threshold, not a result. It is set to 0.8 in the eval config.
- **Why it mattered:** It is a hard guardrail. A model that scores below 80% on the proxy set cannot be deployed, no matter how good it looks in a demo.
- **Say it:** "Promotion requires at least 80% on the proxy set. It is a CI gate."
- **Do not say:** "All tenants run at 80% accuracy live." The 80% is a promotion gate, not a live accuracy number.

### 1.8 "73% lower live execution cost"

- **What it measures:** How much cheaper the chosen model was to run than the previous model, for the same scoring work.
- **Tag:** MEASURED (gold-200 benchmark run).
- **Derivation:** A separate 200-case "gold-200" benchmark compared two OpenAI models (gpt-5.6-luna against gpt-5.4-mini). Both completed 200 out of 200 cases. The cost summary from that run showed the chosen model about 73% cheaper. A third, even cheaper model left rows pending, so completion reliability decided the pick. Model names are not on the PDF.
- **Why it mattered:** LLM token spend is the biggest variable cost of a batch run. Cutting it by about three quarters, without losing coverage, makes the pipeline affordable to run on every season.
- **Say it:** "On a 200-case benchmark, the model we picked cost about 73% less and still completed every case."
- **Do not say:** That the 300-case file measured the 73%. Do not print the model names as if they were on the PDF.

### 1.9 "100% coverage"

- **What it measures:** In this bullet, coverage means every article in the benchmark got a complete answer from the model. It is not test coverage.
- **Tag:** MEASURED (gold-200 benchmark, 200/200 complete).
- **Derivation:** 200 completed out of 200 cases = 100%.
- **Why it mattered:** A cheaper model that silently skips items is worse than useless, because the planner sees gaps. Full coverage is what made the cheaper model acceptable.
- **Say it:** "Cheaper, and it still answered all 200 out of 200."
- **Do not say:** "100% test coverage" for this bullet. The 100% Go statement coverage is a different, off-PDF number.

### 1.10 "74% deterministic baseline"

- **What it measures:** How accurate the plain rule-based score (no LLM) was on the same 200-case benchmark. **Deterministic** means the same input always gives the same output. Here it is KPI math on sell-through and rate of sale.
- **Tag:** MEASURED (gold-200 benchmark).
- **Derivation:** The production deterministic threshold (0.65) applied to the 200 gold cases scored 74%. On the same set, the blended LLM score came in at about 63%, which is below 74%. So we froze the blend weights instead of retuning them on a small set.
- **Why it mattered:** It is the free bar. If an LLM cannot beat a rule that costs nothing, it should not be allowed to change decisions. That is a senior judgement call, and interviewers like it.
- **Say it:** "The rule-only baseline scored 74%. When the blended model came in lower, we froze the blend weights rather than tune them on a small set."
- **Do not say:** That the 74% and the 80% gate come from the same run. They do not.

### 1.11 "10k peak RPS"

- **What it measures:** Peak HTTP requests per second handled by the multi-tenant Go/Gin platform. **RPS** means requests per second. **Gin** is a lightweight Go web framework.
- **Tag:** STATED (on the PDF from the AssortSmart tab).
- **Derivation:** No separate arithmetic in prep. It is the platform's stated peak.
- **Why it mattered:** It is the load the HTTP edge has to absorb without a reverse proxy in front of it, which is why nested timeouts, h2c and tracing live inside the process.
- **Say it:** "The Go platform scales to about 10 thousand requests per second at peak."
- **Do not say:** A latency SLA, a p99, or any other Impact Analytics throughput number. Do not claim Kubernetes cluster operations.

### 1.12 "15.5×" faster pivots

- **What it measures:** How many times faster the heavy planner pivot grid query ran on ClickHouse than on PostgreSQL. A **pivot** is the spreadsheet-like grid planners use: rows by product hierarchy, columns by week or store, cells aggregated.
- **Tag:** MEASURED (pivot benchmark harness, [source](21_ia_pivot_benchmark_source.md)).
- **Derivation:** Postgres took 189,408 ms. ClickHouse took 12,256 ms on the same query and the same 250M rows. 189,408 ÷ 12,256 ≈ 15.45, which rounds to 15.5×.
- **Why it mattered:** At 189 seconds the grid is unusable. Planners wait three minutes per click. At about 12 seconds it becomes workable.
- **Say it:** "Planner pivots got about 15 and a half times faster, from 189 seconds to 12 seconds on 250 million rows."
- **Do not say:** "Sub-second pivots." Do not say the OOM fix (1.15) caused this speedup. Say this carefully: 15.5× is the heavy grid query. The benchmark's own adversarial review said typical aggregates are closer to 2 to 3 times faster. If an interviewer asks whether every query got 15× faster, say no.

### 1.13 "189s to 12s"

- **What it measures:** The wall-clock time of the heavy pivot grid, before and after.
- **Tag:** MEASURED.
- **Derivation:** 189.4 seconds on Postgres (it also spilled 42 GB of sort files to disk). 12.3 seconds on ClickHouse, rounded to 12 on the PDF. The harness was not tilted toward ClickHouse. Postgres ran natively on a 48 GB host with 8 parallel workers. ClickHouse ran in a 10-CPU, 3.3 GB Docker VM.
- **Why it mattered:** It is the number a planner feels. "Three minutes" versus "twelve seconds" is the whole story of why ClickHouse won.
- **Say it:** "From 189 seconds to 12 seconds."
- **Do not say:** "12.0 seconds exactly." It was 12.3 and the PDF rounds. If pressed on how the production rollups relate: the 189 to 12 is the engine comparison on the same query, and the pre-aggregation rollups are how production serves those grids.

### 1.14 "250M-row operations"

- **What it measures:** The size of the dataset the pivot benchmark ran on.
- **Tag:** MEASURED.
- **Derivation:** The harness was built at 5M, 50M and 250M rows. The current largest client was around 5M at the time, so 250M tested whether the choice would survive growth. The gap grew with scale: 13.8× at 5M, 13.0× at 50M, 15.5× at 250M.
- **Why it mattered:** It shows the decision was made for future data size, not just today's.
- **Say it:** "We benchmarked at 250 million rows so the choice would survive growth."
- **Do not say:** "Our production table is 250M rows." Production master is 2.11B. 250M is the benchmark.

### 1.15 "170GB OOM crashes"

- **What it measures:** The memory a single weekly rollup build tried to use before it crashed. **OOM** means out of memory: the database kills the query because it needs more RAM than allowed.
- **Tag:** MEASURED (failed builds).
- **Derivation:** A whole-season weekly `INSERT ... SELECT ... GROUP BY` built about 170 GB of aggregation state in RAM. It failed even with 80 GB and 200 GB memory caps. Profiling showed one product week needs about 11 GB and one attribute week needs over 40 GB. So the fix was to cut the unit of work to one fiscal week per insert and add memory and disk-spill caps.
- **Why it mattered:** The rollups that make pivots fast could not be built at all. No rollups, no fast grid.
- **Say it:** "A whole-season weekly build needed about 170 GB and crashed. We sliced it into one fiscal week per insert with memory and spill caps."
- **Do not say:** That this fix produced the 15.5×. 15.5× is query time. 170 GB is load time. They are not cause and effect.

### 1.16 "~344k rows/s"

- **What it measures:** How many rows per second the custom Go copier moved between two ClickHouse Cloud clusters. It is an ingest rate, not requests per second.
- **Tag:** MEASURED (live snapshot during the copy).
- **Derivation:** Two season streams ran in parallel, each at about 150k to 190k rows/s. Each stream sends 500k-row batches at about 0.3 to 0.4 sends per second, so 0.3 × 500,000 = 150k and 0.4 × 500,000 = 200k rows/s per stream. Two streams combined gave about 344k rows/s at the snapshot.
- **Why it mattered:** Cross-cluster IP allowlists blocked the built-in cluster-to-cluster copy path (`remoteSecure`). The custom pump was the workaround, and its throughput decided whether billion-row tables could be moved at all.
- **Say it:** "About 344 thousand rows per second, combined across two parallel season streams."
- **Do not say:** "344k RPS" or "344k TPS". It is rows per second over ClickHouse's native protocol, not HTTP requests or transactions.

### 1.17 "4.09B rows"

- **What it measures:** The largest object the copier handled: the attribute-weekly rollup table for two seasons.
- **Tag:** MEASURED (row counts), copy measured in flight.
- **Derivation:** Season 6 had 2,779,317,472 rows and season 7 had 1,311,108,195 rows. Together that is 4,090,425,667, or about 4.09B. For scale only: at 344k rows/s, 4.09B rows would take roughly 4,090,000,000 ÷ 344,000 ≈ 11,900 seconds, a bit over 3 hours. Do not quote that as a measured duration.
- **Why it mattered:** It proves the pump, batching and rollback design work on a real multi-billion-row table.
- **Say it:** "Partitions up to about 4.1 billion rows. That copy was measured while it was running."
- **Do not say:** "We finished a 4.09B cutover." The copy was in flight at the snapshot.

### 1.18 "500k-row double-buffered batches"

- **What it measures:** The copier's batch size. **Double-buffered** means the program reads the next batch from the source while it is still sending the previous batch to the target, so neither side sits idle.
- **Tag:** MEASURED (copier constant).
- **Derivation:** A code constant. At 4.09B rows that is 4,090,000,000 ÷ 500,000 ≈ 8,180 batches.
- **Why it mattered:** Large columnar batches are how ClickHouse likes to receive data. Small batches create too many parts and slow merges.
- **Say it:** "Half-million-row batches, double-buffered, so reading and writing overlap."
- **Do not say:** That each batch is an atomic transaction across clusters. Ghost rows are handled by ledgers and partition rollback (drop the season partition, then recopy), not by distributed transactions.

---

## 2. Uber via EPAM, FRM Scoping Platform (Jul 2024 to May 2026)

FRM (Financial Risk Management) scoping is how Uber Finance decides, each quarter, which balance-sheet and income-statement lines and which entities are material enough to need audit testing. Before this platform, analysts did it in Google Sheets. Always say "Uber via EPAM".

### 2.1 "70%" reconciliation time cut

- **What it measures:** The reduction in time to complete quarterly reconciliation and scoping.
- **Tag:** STATED (the outcome on the PDF, framed in the technical design doc).
- **Derivation:** The technical design doc framed the cut, and the platform delivered it for the close. If someone does the math on "14 days to 3 days", they get (14 − 3) ÷ 14 ≈ 79%. So 70% is the conservative figure, and 14 to 3 is consistent with "at least 70%".
- **Why it mattered:** Quarterly close has a hard deadline. Every analyst-day spent copying Sheets is a day not spent reviewing risk.
- **Say it:** "We cut quarterly reconciliation by about 70%, from 14 days to 3 days."
- **Do not say:** "It was only a target." Older prep tagged it TARGET. That guidance is obsolete. If pressed, say: "The technical design doc framed that cut, and that is what the platform delivered for the close." Do not walk it back unprompted.

### 2.2 "14 days to 3 days"

- **What it measures:** Calendar time for the reconciliation and scoping cycle, before and after.
- **Tag:** STATED.
- **Derivation:** Same source as 2.1.
- **Why it mattered:** Same as 2.1. It is the human version of the 70%.
- **Say it:** "From 14 days to 3 days."
- **Do not say:** "Two weeks to three or four days." That was older estimated wording. Use the PDF numbers.

### 2.3 "$340M materiality threshold"

- **What it measures:** Group materiality for the Q4 2025 close. **Materiality** is the dollar size above which a misstatement would change the decision of someone reading the financials. Lines above it get scoped in for testing.
- **Tag:** MEASURED (stored as a metric row in the scoping database for Q4 2025).
- **Derivation:** It is a configured value, not hard-coded. The residual threshold on the same close was $170M (off PDF).
- **Why it mattered:** Every significance decision compares against this number, so getting the math right against it is the platform's core job.
- **Say it:** "Scoping ran against a 340 million dollar materiality threshold."
- **Do not say:** "We processed $340M." It is a threshold, not a volume.

### 2.4 "19M raw GL rows"

- **What it measures:** Raw general ledger rows migrated off Google Sheets into MySQL. A **GL** (general ledger) is the master record of every accounting entry.
- **Tag:** STATED.
- **Derivation:** No further breakdown in prep beyond "raw GL rows migrated off Sheets". Individual quarterly extracts were about 38K to 95K rows, about 1.7K to 1.8K accounts and about 400 entities.
- **Why it mattered:** The value was correctness, hierarchy and auditability, not big-data throughput. Sheets could not enforce any of those.
- **Say it:** "We migrated about 19 million raw GL rows from Sheets into MySQL."
- **Do not say:** Where the 19M came from beyond "raw GL rows migrated off Sheets". Do not call it a big-data pipeline. Older prep said "do not say 19M". That is obsolete.

### 2.5 "36 Spring Boot endpoints"

- **What it measures:** The number of API endpoints shipped for the scoping platform. **Spring Boot** is a Java framework for building web services. Each endpoint is a method on a `@RestController` class, and request bodies are checked with Bean Validation annotations such as `@Valid` and `@NotNull`.
- **Tag:** MEASURED.
- **Derivation:** About 31 functional routes in the scoping service handler, plus the collaboration-service APIs (comments and notifications) from the technical design doc, make 36.
- **Why it mattered:** Each endpoint replaced a manual Sheets step: a calculation, a status change, a threshold edit.
- **Say it:** "About 36 Spring Boot endpoints covering the scoping math, the four-level line-item hierarchy and the review workflow."
- **Do not say:** Do not claim you built the collaboration or Slack notification service. Older prep said "30+ APIs, do not say 36". That is obsolete.

### 2.6 "4-level FSLI (L1 to L4) hierarchy"

- **What it measures:** The depth of the line-item tree. An **FSLI** (Financial Statement Line Item) is one line on the balance sheet or income statement, such as Cash or Revenue. L1 is the broadest grouping and L4 the most detailed.
- **Tag:** MEASURED (schema columns `level_1` to `level_4`).
- **Derivation:** Every fact row carries its L1 to L4 path.
- **Why it mattered:** Auditors scope at different levels. The math has to roll up and down the tree correctly, including quarter-annualization (scaling a quarter's figure to a yearly view).
- **Say it:** "A nested four-level line-item hierarchy with quarter annualization."
- **Do not say:** That the hierarchy depth is configurable to any level. It is four.

### 2.7 "8-table normalized MySQL schema"

- **What it measures:** The number of tables in the scoping schema on SOADB. **SOADB** is Uber's service-owned MySQL standard.
- **Tag:** MEASURED.
- **Derivation:** Eight tables on the PDF. The code also has 11 ORM model classes, which is verbal schema depth. Natural keys are SHA-256 hashes, for example uuid = SHA-256 of question_text plus normalized page_name.
- **Why it mattered:** Normalizing fixed the ETL lock contention during close, and hashed natural keys stopped duplicate rows across quarters.
- **Say it:** "An eight-table normalized MySQL schema with deterministic SHA-256 natural keys."
- **Do not say:** "11 tables" as the PDF number. 11 is the ORM model count.

### 2.8 "3 engineers"

- **What it measures:** The size of the EPAM pod I led on the ORM migration.
- **Tag:** HISTORICAL.
- **Derivation:** Head count.
- **Why it mattered:** It shows technical leadership.
- **Say it:** "I led three engineers on the ORM migration as tech lead of the EPAM pod."
- **Do not say:** "I managed three people." I was tech lead, not people manager. Do not merge this with "mentored two" at Masters India.

### 2.9 "100% module statement coverage"

- **What it measures:** The share of code statements in the migrated module that tests executed. **Statement coverage** counts lines of code that ran at least once during tests.
- **Tag:** STATED.
- **Derivation:** The coverage report on the migrated module. The test count was 1,100+ (verbal).
- **Why it mattered:** The Spring Data JPA / Hibernate migration touched every query. Full coverage, from JUnit 5 and Mockito tests, is how we proved no hidden column-aliasing bug survived.
- **Say it:** "We raised the module's statement coverage to 100% during the Spring Data JPA and Hibernate migration."
- **Do not say:** "100% coverage on all of Uber Finance." It is the module.

### 2.10 "50% delta-variance checks"

- **What it measures:** The threshold for an automated check inside the review state machine. **Delta variance** is how much a value changed between periods. An **FSM** (finite state machine) is the fixed set of review statuses (Draft, Review, ReOpen, Closed) and the allowed moves between them.
- **Tag:** STATED.
- **Derivation:** A 50% change between periods is flagged by an automated gate in the state machine, supporting SOX controls. **SOX** (Sarbanes-Oxley) is the US law that requires auditable internal controls over financial reporting.
- **Why it mattered:** Big swings are where misstatements hide. A gate makes the check consistent and auditable, not dependent on an analyst noticing.
- **Say it:** "The review state machine has automated gates that flag 50% delta variance, for SOX."
- **Do not say:** Exact formula details beyond that if you are not sure. Keep it at "a 50% period-over-period variance is flagged at a gate".

---

## 3. Uber via EPAM, Menu Ingestion (Uber Eats)

Restaurants send menus as PDFs or images in many languages. Uber Eats needs them in a strict catalog schema (items, prices, modifiers). This pipeline scraped and parsed them automatically.

### 3.1 "24 hours to 2 hours"

- **What it measures:** Time from a restaurant's menu arriving to the menu being live in the catalog.
- **Tag:** HISTORICAL.
- **Derivation:** From my work records. 24 ÷ 2 = 12 times faster, about a 92% cut.
- **Why it mattered:** A restaurant that is not live is not earning. Same-day onboarding matters for sales teams.
- **Say it:** "Restaurant onboarding went from 24 hours to 2 hours."
- **Do not say:** "Instant" or "real time".

### 3.2 "$600K annually"

- **What it measures:** Yearly cost avoided by replacing a third-party or manual menu-processing step.
- **Tag:** ESTIMATED (arithmetic on HISTORICAL inputs).
- **Derivation:** About $2 per menu × 30,000 menus per month × 12 months = $720,000 list. The resume floors it to $600K to be conservative.
- **Why it mattered:** It turns an engineering project into a business case.
- **Say it:** "Roughly 600 thousand dollars a year. It comes from about two dollars per menu at 30 thousand menus a month, and I round down."
- **Do not say:** "$720K saved." $720K is the list arithmetic, and the resume deliberately floors it.

### 3.3 "30K+ menus monthly"

- **What it measures:** Menus processed per month.
- **Tag:** HISTORICAL.
- **Derivation:** From work records. 30,000 ÷ 30 ≈ 1,000 menus per day on average.
- **Why it mattered:** It is the volume behind the money number.
- **Say it:** "More than 30 thousand menus a month."
- **Do not say:** "30K events per second". Event rate is a separate, off-PDF estimate.

### 3.4 "98% field fidelity"

- **What it measures:** The share of extracted fields (item name, price, description, modifier) that matched a labelled ground truth. **Field fidelity** means "did each field come out right".
- **Tag:** HISTORICAL, offline evaluation.
- **Derivation:** Offline evaluation of the Gemini 2.5 Pro plus LangChain RAG over Milvus pipeline against labelled menus.
- **Why it mattered:** Wrong prices or missing modifiers cause refunds and support tickets. High fidelity is what let the pipeline skip most manual review.
- **Say it:** "98% field fidelity on our offline evaluation set."
- **Do not say:** "98% accuracy in production." Always say offline evaluation.

### 3.5 "95%+ extraction success"

- **What it measures:** The share of scrape attempts that produced a usable menu.
- **Tag:** HISTORICAL, with an ESTIMATED baseline.
- **Derivation:** From an estimated baseline of about 60% to 65%, raised to 95%+ by dynamic proxy pools and adaptive retries on the Selenium fleet.
- **Why it mattered:** Every failed scrape is a manual fallback.
- **Say it:** "Extraction success went to over 95%, from roughly 60 to 65% before."
- **Do not say:** The baseline as a measured number. It is an estimate.

### 3.6 "Exactly-once catalog upserts" (not a number, but often probed)

- **What it means:** The catalog ends up with each menu written once, even if events are retried. In practice that is at-least-once delivery from Kafka plus idempotent upserts keyed by vendor, menu and content hash. An **upsert** inserts a row or updates it if the key already exists. **Idempotent** means doing it twice has the same effect as doing it once.
- **Say it:** "Exactly-once at the catalog level, which in practice is at-least-once delivery with idempotent upserts."
- **Do not say:** "Zero message loss" or "two-phase commit across third parties". Do not mention ClickHouse or Spark here.

---

## 4. Uber via EPAM, Document Compliance (Uber Mobility ANZ)

Drivers and vehicles in Australia and New Zealand (ANZ) need valid documents (licences, registrations, inspections) per local authority rules. This backend checked them automatically.

### 4.1 "99.9% regulatory compliance"

- **What it measures:** The share of driver and vehicle documents that met local authority requirements after automation.
- **Tag:** HISTORICAL.
- **Derivation:** From work records on the Mobility ANZ project.
- **Why it mattered:** Non-compliance can mean fines or losing the right to operate in a market.
- **Say it:** "99.9% regulatory compliance for Uber Mobility in ANZ."
- **Do not say:** "Uber Eats." This is Mobility. Do not add Selenium or RAG to this story.

### 4.2 "20 hours per week"

- **What it measures:** Manual review time eliminated per week.
- **Tag:** HISTORICAL.
- **Derivation:** From work records. For scale, 20 hours is half of a 40-hour work week, and 20 × 52 = 1,040 hours a year.
- **Why it mattered:** It freed operations staff from repetitive queue work.
- **Say it:** "It removed about 20 hours a week of manual review."
- **Do not say:** "Replaced a team." It replaced queue work.

---

## 5. Masters India, GST E-Invoicing (Dec 2022 to Jun 2024)

Masters India sells GST (Goods and Services Tax) compliance software to Indian companies. Clients send invoices. The platform validates them and registers them with the government's IRP (Invoice Registration Portal), which returns an IRN (Invoice Reference Number) and a signed QR code.

### 5.1 "75%" p95 latency cut

- **What it measures:** The drop in p95 API latency. **p95** means 95% of requests finish faster than this value. It describes the slow tail, not the average.
- **Tag:** HISTORICAL.
- **Derivation:** (1.2 s − 0.3 s) ÷ 1.2 s = 0.9 ÷ 1.2 = 75%.
- **Why it mattered:** Enterprise clients send large batches near filing deadlines. A slow tail means timeouts on their side.
- **Say it:** "p95 latency dropped 75%, from 1.2 seconds to 300 milliseconds."
- **Do not say:** "Average latency." It is p95.

### 5.2 "1.2s to 300ms"

- **What it measures:** p95 latency before and after the move from the PHP monolith to Spring Boot microservices.
- **Tag:** HISTORICAL.
- **Derivation:** From work records. The win came from non-blocking IRP calls (Spring WebClient and bounded thread pools), HikariCP connection pooling, query and index fixes, and Redis for reads.
- **Why it mattered:** Same as 5.1.
- **Say it:** "From 1.2 seconds to 300 milliseconds at p95."
- **Do not say:** That Spring Boot alone made it faster. The causes were non-blocking IO, pooling, query fixes and caching.

### 5.3 "1,500+ enterprise clients"

- **What it measures:** Number of enterprise customers on the platform.
- **Tag:** HISTORICAL.
- **Derivation:** From work records. Older resumes had 2,500+. Use 1,500+.
- **Why it mattered:** It is the blast radius. A regression hits every one of them.
- **Say it:** "More than 1,500 enterprise clients."
- **Do not say:** 2,500+.

### 5.4 "Mentored two engineers"

- **What it measures:** People I mentored through the migration.
- **Tag:** HISTORICAL.
- **Say it:** "I mentored two engineers through the migration."
- **Do not say:** "Led three." That is Uber FRM.

### 5.5 "700 to 4,000 requests per minute"

- **What it measures:** Overall system throughput before and after.
- **Tag:** HISTORICAL. The per-second conversion is ESTIMATED.
- **Derivation:** 700 ÷ 60 ≈ 12 requests per second. 4,000 ÷ 60 ≈ 67 requests per second. 4,000 ÷ 700 ≈ 5.7 times more.
- **Why it mattered:** Filing deadlines create bursts. More headroom means fewer rejected uploads.
- **Say it:** "Throughput went from 700 to 4,000 requests per minute, about 12 to 67 per second."
- **Do not say:** "4,000 RPS". It is per minute.

### 5.6 "1M+ daily government submissions"

- **What it measures:** E-invoice submissions to the IRP per day.
- **Tag:** HISTORICAL. Average and peak rates are ESTIMATED.
- **Derivation:** 1,000,000 ÷ 86,400 seconds ≈ 11.6, so about 12 per second on average. Peaks around filing deadlines are estimated at 8 to 10 times the average, so roughly 90 to 120 per second.
- **Why it mattered:** Each submission is a legal obligation for the client. Missing one has real penalties.
- **Say it:** "More than a million submissions a day, about 12 per second on average, with much higher peaks around deadlines."
- **Do not say:** A measured peak TPS. The peak is an estimate.

### 5.7 "100K+ concurrent imports"

- **What it measures:** The size of bulk invoice imports the pipeline handled at once with idempotent processing.
- **Tag:** HISTORICAL.
- **Derivation:** From work records. Idempotency key looked like client + fileHash + batchIndex, so re-sending the same chunk does not create a second invoice.
- **Why it mattered:** Duplicate invoice registration with the government is a compliance problem, not just a data bug.
- **Say it:** "More than 100 thousand concurrent imports, each processed idempotently."
- **Do not say:** "Exactly-once delivery from Kafka." It is idempotent processing on top of retries.

### 5.8 "70%" triage time cut

- **What it measures:** Time from an alert to knowing which service and request caused it.
- **Tag:** HISTORICAL, with an ESTIMATED baseline.
- **Derivation:** Roughly 30 minutes to under 10 minutes. 30 → 9 minutes is a 70% cut.
- **Why it mattered:** Faster triage means shorter incidents near filing deadlines.
- **Say it:** "Incident triage time fell about 70%, roughly from half an hour to under ten minutes, thanks to ELK and New Relic tracing."
- **Do not say:** The 30-minute baseline as measured.

### 5.9 "30%" lower database read load

- **What it measures:** Reduction in read queries hitting PostgreSQL.
- **Tag:** HISTORICAL.
- **Derivation:** From work records. A Redis cache-aside layer served repeated reads. **Cache-aside** means the app checks the cache first, and on a miss reads the database and fills the cache.
- **Say it:** "A Redis cache-aside layer cut database read load by about 30%."
- **Do not say:** "30% faster." It is load, not latency.

### 5.10 "35% to 82%" test coverage

- **What it measures:** Automated test coverage of the services, before and after.
- **Tag:** HISTORICAL.
- **Say it:** "Test coverage went from 35% to 82%."
- **Do not say:** 100%. That is the Uber FRM module.

### 5.11 "98% deployment success rate"

- **What it measures:** Share of deployments that went out without a rollback.
- **Tag:** HISTORICAL.
- **Say it:** "98% of deployments succeeded without rollback."
- **Do not say:** "Zero downtime." That phrase belongs to Uber FRM stacked Bazel PRs.

---

## 6. GeeksforGeeks (Aug 2021 to Nov 2022)

### 6.1 "10K+ daily queries"

- **What it measures:** Doubts (student questions) handled by the doubt-support platform per day.
- **Tag:** HISTORICAL.
- **Derivation:** From work records. Older resumes conflicted (1K and 100K). Use 10K+. On average that is 10,000 ÷ 86,400 ≈ 0.1 per second, so the engineering challenge was the spikes, not the average.
- **Say it:** "More than 10 thousand doubt queries a day."
- **Do not say:** A per-second rate as if it were the hard part.

### 6.2 "10x traffic spikes"

- **What it measures:** Peak traffic during live coding contests compared with normal.
- **Tag:** HISTORICAL.
- **Say it:** "Contest traffic spiked about ten times normal, which is why we moved the backend to Django."
- **Do not say:** A measured RPS.

### 6.3 "20% lift in premium subscriptions"

- **What it measures:** Relative growth in premium subscriptions after the platform was stabilised.
- **Tag:** HISTORICAL. Attributed by the growth team.
- **Say it:** "The growth team attributed about a 20% lift in premium subscriptions. I owned the engineering."
- **Do not say:** An absolute subscriber count.

### 6.4 "30%" course sales

- **What it measures:** Growth in course sales after the influencer analytics and earnings dashboard launched.
- **Tag:** HISTORICAL. Business attribution.
- **Say it:** "Course sales grew about 30%. I owned the engineering. The business team attributed the lift."

### 6.5 "70%" operational efficiency

- **What it measures:** Reduction in manual operations work after asynchronous scheduled workflows for video processing, reminders and data cleanup.
- **Tag:** HISTORICAL.
- **Say it:** "Scheduled background workflows made engineering operations about 70% more efficient."
- **Do not say:** It is the same 70% as Masters triage or Uber FRM. They are three unrelated numbers.

---

## 7. Education and achievements

| Number | Tag | Plain meaning |
|---|---|---|
| Google Code Jam Qualifier 2021, rank 2260 out of 37,000+ | HISTORICAL | 2,260 ÷ 37,000 ≈ 6%, so roughly the top 6% of participants. |
| Smart India Hackathon 2020 (MHRD), finalist, top 3 nationally | HISTORICAL | A national government-run hackathon. Our team placed in the top three. |
| B.Tech IT, IET Lucknow, 2017 to 2021 | HISTORICAL | Degree years. |

CGPA is not on the PDF. Do not volunteer it.

---

## 8. Off-PDF but true (verbal only)

These numbers are real and you can use them when an interviewer goes deep. They are not printed on the current PDF, so introduce them as detail, not as headline claims.

### Impact Analytics

| Number | Tag | What it is, in plain words |
|---|---|---|
| **1.6M article-seasons** | MEASURED | The catalog size: every product × season combination. It is a different number from the 348k that were scored. |
| **About $100 per pass** | MEASURED | Token spend for one 88k-item pass. $100 ÷ 88,000 ≈ $0.0011, about a tenth of a cent per item. |
| **Blend 0.4 / 0.6, keep at 0.55** | MEASURED (config) | s_final = 0.4 × s_det + 0.6 × s_agent. An article is kept if s_final ≥ 0.55. |
| **Det threshold 0.65, blended ~63%** | MEASURED | The production rule threshold used for the 74% baseline, and the blended score that lost to it on gold-200. |
| **Circuit breaker trips after about 5 consecutive failures** | MEASURED (config default) | Also trips on a failure fraction. Stops hammering a failing provider. |
| **55 GB memory cap, 16 GB spill, 8 threads, 4 weeks in flight** | MEASURED | The weekly rollup insert settings after the 170 GB fix. **Spill** means ClickHouse writes partial aggregation to disk instead of crashing. |
| **Product week ~11 GB, attr week >40 GB** | MEASURED | Peak memory per one-week insert, used to size the caps. |
| **Failed at 80 GB and 200 GB caps** | MEASURED | Whole-season builds failed even with very large caps, which proved the unit of work was wrong. |
| **Six rollup tables** | MEASURED (design) | Product, store and attribute, each at season and weekly grain, partitioned by season_code. |
| **839M product weekly** | MEASURED | Product-weekly rollup for seasons 6 and 7: about 569.4M + 269.8M rows. |
| **~150k to 190k rows/s per stream** | MEASURED | Each of the two copier streams. Two combined gave ~344k. |
| **Port 9440** | MEASURED | ClickHouse native protocol over TLS, used by the Go pump. |
| **100% Go statement coverage, 1,200+ Go tests** | MEASURED | On LinkedIn and verbal. Not on the PDF. |

### Uber FRM

| Number | Tag | What it is |
|---|---|---|
| **About 31 functional routes** | MEASURED | Scoping service routes. Plus collaboration-service APIs from the design doc gives 36. |
| **11 ORM models** | MEASURED | Model classes in code. The PDF says 8 tables. |
| **8 screens** | MEASURED | Reconciliation, Materiality, EMI Scoping, Group Scoping, Threshold Setup, Component Scoping, Residual Risk, Summary. |
| **$170M residual threshold** | MEASURED | Q4 2025 close, alongside $340M materiality. |
| **5% significance thresholds** | MEASURED | A component is financially significant if revenue share or absolute asset share is above 5%. |
| **18 files, +1,268 lines** | MEASURED | Reconciliation v1 (Sheets) to v2 (MySQL) migration change set, run in parallel. |
| **38K to 95K rows per quarterly extract, ~1.7K to 1.8K accounts, ~400 entities** | MEASURED | Size of one quarter's GL dump. |
| **1,100+ tests** | HISTORICAL | Test count on the FRM module. |

### Uber Menu

| Number | Tag | What it is |
|---|---|---|
| **$720K list** | ESTIMATED | $2 × 30K × 12. The resume floors it to $600K. |
| **~60% to 65% baseline** | ESTIMATED | Extraction success before proxy hardening. |
| **~200 to 500 peak events per second on Kafka** | ESTIMATED, prep only | Fleet-run amplification of menu, item and retry events. Confusing next to "30K menus a month", so keep it off the page unless asked. |

### Masters India

| Number | Tag | What it is |
|---|---|---|
| **~12 TPS average** | ESTIMATED | 1,000,000 ÷ 86,400 ≈ 11.6. |
| **Peaks 8 to 10 times average** | ESTIMATED | Around filing deadlines. |
| **~12 to ~67 RPS** | ESTIMATED | 700 ÷ 60 and 4,000 ÷ 60. |
| **~30 min to under 10 min triage** | ESTIMATED | Baseline behind the 70%. |

### Not resume bullets at all (Impact Analytics, verbal only)

The Cluster Recommendation Copilot and Hindsight are verbal-only projects. Their numbers: a measured clustering failure rate of 8.5% (37 out of 437), a TARGET of under 2%, a design with 14 audited read-only tools and 3 gates, a TARGET of turnaround under 1 hour and at least 20 configs per plan. Say "building", not "shipped". Do not present any of these as PDF bullets.

---

## 9. Decision log: technologies on and off this PDF

| Technology | Where it stands | Why |
|---|---|---|
| **Kafka** | On the PDF for Uber Menu and Masters India | Two different products. Menu Kafka is not Masters Kafka. |
| **Apache Flink** | On the PDF for Uber Menu only | Keyed deduplication and schema normalization before catalog upserts. Never at Masters, never at Impact Analytics. |
| **ClickHouse** | On the PDF for Impact Analytics as production work | Pre-aggregation rollups, the 2.11B master, the Go copier. Older prep called it a "POC bullet". That is obsolete. |
| **Spark** | Not on the PDF | Verbal backfill option for Menu only. Do not claim ownership. |
| **Pinot** | Not on the PDF | Space, and weaker need than Flink. Verbal if asked about health dashboards. |
| **Kubernetes, Terraform, multi-region** | Kubernetes on skills line only as literacy. Others study only. | No "I operated clusters". See [senior systems study notes](17_senior_systems_study_only.md). |
| **Milvus** | On the PDF for Uber Menu only | Never at Impact Analytics. |

---

## 10. Older prep, not on the current PDF

Earlier versions of this page carried numbers from older resumes. They are listed here so you recognise them if they come up, and so you do not use them by mistake.

| Older prep said | Current status |
|---|---|
| FRM "8 screens, 30+ REST APIs, do not say 36" | Obsolete. PDF says 36 Spring Boot endpoints. |
| FRM "70% is a TARGET, say targeting" and "~2 weeks to ~3 to 4 days" | Obsolete. PDF states 70%, from 14 days to 3 days, as the outcome. |
| FRM "19M to 300K rows unsupported, do not say 19M" | Obsolete. PDF says 19M raw GL rows. |
| FRM "11-table schema, 55 line items, 14 entities" | 11 is the ORM model count. PDF says 8 tables. About 55 line items (26 balance sheet + 29 income statement) and 14 entities were a sample, verbal depth only. |
| IA "20 to 100 configs per plan", "under 1 hour", "failures under 2% from 8.5%", "100% reproducible clusters" | Cluster Copilot design targets. Verbal only, not on the PDF. |
| IA "p95 probes under 500 ms vs 1 to 20 s BigQuery" | Copilot design target. Not on the PDF. Do not make sub-second ClickHouse claims. |
| IA "ClickHouse POC bullet", "63/8 DDL", "insert-only planning store" | Old framing and interview depth. PDF now has production rollups (C4) and the copier (C5). |
| IA "avoided materializing 12B store-week (~25M aggregate)" | Line-planning schema lesson. Verbal depth only. |
| IA "2.4B weekly rollups" | Not on the current PDF. The current PDF uses 4.09B (attr weekly, two seasons). Do not quote 2.4B. |
| IA "$100 per pass is on the PDF" | It is not. It is true and off-PDF. |
| IA "335 thousand products" | Old wording. Use 348k article-seasons. |
| IA "Order Batching 60×, 23.7M, 3.86 s" and "Postgres single-cell edit ~82× faster" | POC history behind the hybrid verdict. Not resume claims. |
| Menu "Spark in the title", "Selenium to Kafka to Flink to Spark" | Spark is not on the PDF. |
| Menu "100% schema consistency" | Not on the current PDF. |
| Menu "24h to 2h (90%)" | The cut is about 92% (22 ÷ 24). Just say "from 24 hours to 2 hours". |
| GFG "premium +15 to 20%" and "~1 to 2 RPS average" | PDF says 20%. The per-second figure did not match the arithmetic (10K ÷ 86,400 ≈ 0.1). |
| Masters "~12 TPS average, 100+ peak" | Kept as ESTIMATED in section 8 (peaks 8 to 10× average). |
| CGPA 7.7 | Removed from PDFs. Do not volunteer. |
