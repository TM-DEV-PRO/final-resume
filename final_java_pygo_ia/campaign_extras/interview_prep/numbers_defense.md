# Resume Number Catalog / Numbers Defense

<div class="callout note">
<b>How to use this page</b>
<ul>
<li>It explains every number on <code>Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf</code>: what it measures, where it came from, why it mattered to the business, how to say it out loud, and what not to say.</li>
<li>Read it before any round where they'll go through your resume line by line. Re-read the "Don't say" lines the morning of the interview.</li>
<li>Memorise the spoken form of each number and the one-sentence derivation. If you can say where a number came from in one breath, it sounds credible.</li>
<li>A short "off the PDF" list at the end covers numbers you may say out loud but that aren't on the resume.</li>
</ul>
</div>

Sources: canonical IA claims are in `docs/ASSORTSMART_TAB_RESUME.md`. Cross-links: [`GROUND_TRUTH.md`](../../prep/GROUND_TRUTH.md), [`18_resume_number_catalog.md`](../../prep/18_resume_number_catalog.md), [`09_metrics_derivations.md`](../../prep/09_metrics_derivations.md).

## What the tags mean

- **MEASURED** means there is a benchmark, log, document or code behind it.
- **TARGET** means it was a design goal. Say "targeting".
- **ESTIMATED** means it's arithmetic I can show on a whiteboard. Say "roughly, derived from...".
- **HISTORICAL** means it comes from my past work records and wasn't re-measured.
- **PDF** means it is on the resume as written and I defend it as written.
- **CI GATE** means it is a release check, not a live production result.

## Three rules for saying any number

1. **Say it as a change, slowly.** "From 189 seconds to 12 seconds" is easier to hear than "15.5x".
2. **Say what it measured.** "On a 250-million-row test" or "on a fixed test set".
3. **Stop after the number.** Let them ask the follow-up. You have the derivation ready.

---

## Impact Analytics: Agentic Flows and Orchestration

**Context in plain words.** AssortSmart helps retailers plan assortments: which products to keep, drop or add each season. An *article* is one product. An *article-season* is one product in one selling season, like "blue denim jacket, Spring 2026". The AI decision engine scores article-seasons and recommends what to do.

### 348k article-seasons evaluated (PDF)

- **What it measures.** The number of product-in-season combinations the decision engine scored across its pipelines: Keep/Drop, Missed Opportunities and Top Style.
- **How it was derived.** It's the count of rows the engine scored, from the AssortSmart run records.
- **Why it mattered.** Planners can't review that many items by hand each season. Scoring them all means every item gets a consistent recommendation.
- **Say it.** "The engine evaluates about 348 thousand article-seasons, where an article-season is one product in one selling season."
- **Don't say.** Don't mix it with **1.6 million**. That's the size of the whole catalog, it's off the PDF, and it's a different number. Scored is 348k.

### 88k items per pass (PDF)

- **What it measures.** How many items one batch run of the engine processes.
- **How it was derived.** It's the batch size of a single pass in the run records.
- **Why it mattered.** It shows the orchestration has to survive long batch runs. A provider failure halfway through 88 thousand items can't mean starting over.
- **Say it.** "One pass processes about 88 thousand items."
- **Don't say.** Don't claim a specific number of passes unless you know how they split. If someone divides 348k by 88k and gets about 4, say "roughly, depending on the pipeline".

### 7 AI lenses (PDF)

- **What it measures.** The number of separate LLM judgments made per item. A *lens* is one angle of analysis, like a specialist giving an opinion on one aspect. A *decider* step combines them.
- **How it was derived.** It's a count from the pipeline design.
- **Why it mattered.** Splitting the judgment into focused lenses makes each prompt simpler and each output easier to check.
- **Say it.** "Each item is looked at through seven AI lenses, and a decider combines them into one AI score."
- **Don't say.** Don't say there's an LLM orchestrator choosing which lens to run. Keep/Drop runs in a fixed order: peer comparison, decider, lenses, blend, explanation.

### The blend: 0.4, 0.6 and 0.55 (verbal design detail)

- **What it measures.** How the final score is built. The deterministic score (from sell-through and rate of sale) gets weight 0.4. The AI score gets weight 0.6. An item is kept if the final score is 0.55 or higher.
- **Worked example.** Deterministic score 0.70, AI score 0.45. Final = 0.4 × 0.70 + 0.6 × 0.45 = 0.28 + 0.27 = 0.55. That's exactly the threshold, so the item is kept.
- **Say it.** "The final score is 40% rule-based and 60% AI, and we keep the item at 0.55 or above."
- **Don't say.** Don't say these weights were retuned after the benchmark. They were frozen (see 74% below).

### 2.11B-row ClickHouse master (PDF)

- **What it measures.** The number of rows in the main ClickHouse fact table, which holds detailed sales and inventory facts.
- **How it was derived.** It's the table's row count.
- **Why it mattered.** It explains the design choice. A table that large is too risky to let an LLM query directly. A bad generated query could be very slow or expensive, and a bad write would be very hard to undo. So the engine gets prepared JSON context instead.
- **Say it.** "The main ClickHouse table has about 2.11 billion rows, so the AI never touches it directly. It gets prepared JSON."
- **Don't say.** Don't say "sub-second queries on 2.11 billion rows". That isn't claimed.

### 300-case evaluation harness and 80% CI gate (PDF, CI GATE)

- **What it measures.** The 300 is the number of test cases in a proxy evaluation set. *Proxy* means it stands in for real decisions with known answers. The 80% is the minimum accuracy a model or prompt change must reach on that set before it can be promoted. In config it's `gold_min_accuracy: 0.8`.
- **How it was derived.** 300 is the count of cases in the evaluation file. 80% is the threshold set in the gate config.
- **Why it mattered.** It stops a "looks good in a demo" change from reaching users. A change that makes the AI worse is blocked automatically.
- **Say it.** "We have a 300-case evaluation set, and CI blocks any change that scores below 80% on it."
- **Don't say.** Never say "the AI is 80% accurate in production" or "all tenants are live at 80%". It's a release gate.

### 73% lower cost at 100% coverage (PDF, MEASURED)

- **What it measures.** In a separate benchmark of 200 gold-labelled items, a newer, cheaper model cost 73% less to run than the previous model. It also completed all 200 items. That's what "100% coverage" means here: every item got a valid answer, none timed out or failed.
- **How it was derived.** Comparing the total cost of the two models on the same 200 items. The model names (gpt-5.6-luna versus gpt-5.4-mini) are off the PDF. Use them only if asked.
- **Why it mattered.** Lower cost per run, with no loss of completeness, makes it affordable to run the engine regularly.
- **Say it.** "On a 200-item benchmark, switching models cut execution cost by 73%, and it still answered all 200."
- **Don't say.** Don't say this came from the 300-case file. It's a different set. And "100% coverage" here is not test coverage. It means 200 out of 200 items completed.

### 74% deterministic baseline, and freezing the weights (PDF, MEASURED)

- **What it measures.** The accuracy of the rule-based scorer alone on that same 200-item set, using the production threshold of 0.65.
- **How it was derived.** Running the deterministic scorer on the gold-200 set and counting correct decisions.
- **Why it mattered.** The blended LLM score came out at about 63%, which is worse than 74%. So we did not retune the blend to make the AI look better. We froze the weights and kept the safer setup.
- **Say it.** "The rule-based baseline scored 74% on the benchmark. The AI blend scored lower, so we froze the weights instead of shipping a worse model."
- **Don't say.** Don't fuse 73%, 74% and 80% into one story. 80% is the gate on the 300-case file. 73% and 74% come from the 200-item benchmark.

### Ask Iris (PDF capability, no numbers)

- **What it is.** A copilot that planners chat with over a secure WebSocket (a connection that stays open for live back-and-forth) to ask about KPIs and inspect AI decisions.
- **The one number.** It uses a 3-attempt evaluator loop. After 3 failed attempts it stops and answers with what it has, so it can't loop forever.
- **Say it.** "Ask Iris is shipped. It has an evaluator that retries at most three times."
- **Don't say.** Don't invent usage, latency or uptime numbers.

---

## Impact Analytics: Core Infrastructure and Pipeline

### 10k peak RPS (PDF)

- **What it measures.** RPS is requests per second. 10k peak means the Go/Gin platform is built for and handles bursts of about 10,000 requests per second.
- **How it was derived.** It's the peak figure stated for the platform on the AssortSmart record.
- **Why it mattered.** The edge serves many retailers at once and has no reverse proxy in front of it, so it has to protect itself under load. That's why it has nested timeouts and native HTTP/2.
- **Say it.** "The Go platform handles peaks of about ten thousand requests per second."
- **Don't say.** Don't invent average load, latency SLAs or TPS. Don't say you operated Kubernetes for it.

### 15.5x faster, from 189 seconds to 12 seconds, on 250M rows (PDF, MEASURED)

- **What it measures.** How long one planner pivot query took. A *pivot* is the grid view that groups numbers by product, store and time. It went from 189 seconds on Postgres to about 12 seconds on ClickHouse with pre-aggregated rollups.
- **How it was derived.** A benchmark harness with 250 million rows, where both databases held identical data. The ClickHouse time was 12.3 seconds, rounded to 12 on the PDF. 189 ÷ 12.3 is about 15.4, and the benchmark doc reports about 15.5x. Either way, say "about fifteen times".
- **Why it mattered.** At over three minutes, planners would give up on the screen. At 12 seconds the workflow becomes usable.
- **Say it.** "Planner pivots went from 189 seconds to 12 seconds on a 250-million-row test, about fifteen times faster."
- **Don't say.** Don't say "sub-second". Don't say the 170 GB fix caused this speed-up.

### Six rollup tables (PDF)

- **What it measures.** The number of pre-aggregated tables. A *rollup* stores totals in advance, like keeping a running monthly total instead of adding up receipts every time. The six are product, store and attribute, each at season level and at weekly level.
- **Say it.** "Six rollup tables: product, store and attribute, each by season and by week."

### 170 GB out-of-memory prevented (PDF)

- **What it measures.** The memory one query would have needed to build a whole season's weekly rollup in one go. OOM means out of memory, where the database kills the query.
- **How it was derived.** From the failed runs. The whole-season build needed about 170 GB of working memory and failed even when the cap was raised to 80 GB and then 200 GB.
- **Why it mattered.** Without a fix, there was no weekly level of detail at all.
- **The fix in one line.** Build one fiscal week per insert, with memory and disk-spill caps. A product week needed about 11 GB. An attribute week went above 40 GB.
- **Say it.** "Building a whole season at once needed about 170 GB and crashed. I sliced it into one week per insert, and it fit."
- **Don't say.** This is load time, not query time. It is not why pivots got faster. The exact caps (55 GB memory, 16 GB spill, 8 threads, 4 weeks in flight) are verbal detail, not on the PDF.

### About 344k rows per second (PDF, MEASURED)

- **What it measures.** The combined copy speed of the custom Go data pump while migrating rollups between ClickHouse Cloud clusters.
- **How it was derived.** Two season streams ran at the same time, each around 150k to 190k rows per second. Added together that's about 344k rows per second.
- **Why it mattered.** Cross-cluster IP allowlists blocked ClickHouse's own cluster-to-cluster copy. The pump made multi-billion-row moves practical anyway.
- **Say it.** "The pump copied about 344 thousand rows per second, combined across two streams."
- **Don't say.** This is rows per second, an ingest rate. It is **not** requests per second or transactions per second.

### Partitions up to 4.09B rows (PDF, MEASURED)

- **What it measures.** The biggest partition group copied: the attribute weekly table across two seasons. A *partition* is a slice of a table, here one season.
- **How it was derived.** 2,779,317,472 rows plus 1,311,108,195 rows equals 4,090,425,667, which is about 4.09 billion.
- **Say it.** "The largest table we moved had about 4.09 billion rows across two seasons."
- **Don't say.** The 4.09B copy was measured in flight. Don't say the cutover finished.

### 500k-row double-buffered batches (PDF)

- **What it measures.** The batch size the pump reads and writes. *Double-buffered* means while one batch is being sent, the next one is already being read, so neither side waits.
- **Say it.** "It moved 500 thousand rows per batch, reading the next batch while sending the previous one."

---

## Uber via EPAM: FRM Scoping Platform

**Context in plain words.** FRM (Financial Risk Management) is the Uber Finance team that decides each quarter which accounts and entities need audit attention. Before this platform, much of that work was done in Google Sheets.

### 70%, from 14 days to 3 days (PDF)

- **What it measures.** The calendar time for the quarterly reconciliation, which is checking that numbers in the finance system match the filed reports.
- **How it was derived.** The technical design doc framed the cut, and that's what the platform delivered for the close. If someone does the math, 14 to 3 is about a 79% cut, so 70% is the conservative figure.
- **Why it mattered.** Two weeks of analyst time each quarter became about three days. That leaves more time before filing deadlines and less manual error.
- **Say it.** "Quarterly reconciliation went from 14 days to 3 days."
- **Don't say.** Don't walk it back unprompted. Older prep called this a "TARGET". The current resume states it as the outcome, and that's what you defend.

### $340M materiality threshold (PDF)

- **What it measures.** *Materiality* is the money amount above which a misstatement matters to auditors. Accounts or entities above it get scoped in for review.
- **How it was derived.** From the Q4 2025 close data the platform worked with. Residual materiality on that close was $170M, and the significance thresholds were 5%.
- **Say it.** "The platform scoped against a 340-million-dollar materiality threshold."
- **Don't say.** Don't say you set the threshold. Finance sets it. The platform computes against it.

### 19M raw GL rows (PDF)

- **What it measures.** The number of raw general ledger rows migrated off Sheets into MySQL. A *general ledger* is a company's master list of accounting entries.
- **Say it.** "We migrated about 19 million raw general-ledger rows off Sheets."
- **If they push on volume.** Individual quarterly extracts were roughly 38K to 95K rows, around 1.7K to 1.8K accounts and about 400 entities. Say: "The value was correctness, hierarchy and auditability, not big-data throughput."
- **Don't say.** Don't invent where the 19M comes from beyond "raw GL rows migrated off Sheets".

### 36 Spring Boot endpoints (PDF)

- **What it measures.** The number of API routes, meaning the handler methods on the Spring Boot REST controllers (`@GetMapping`, `@PatchMapping` and so on).
- **How it was derived.** About 31 functional routes in the scoping service handler, plus the collaboration-service APIs for comments and notifications from the design doc, make 36.
- **Say it.** "Thirty-six Spring Boot endpoints."
- **Don't say.** Older prep said "30+, don't say 36". That guidance is obsolete. Don't claim you built the collaboration or Slack notification service itself.

### L1 to L4 FSLI hierarchy (PDF)

- **What it measures.** FSLI means Financial Statement Line Item, like "Cash" or "Revenue". L1 to L4 are four nested levels, like a folder tree from broad category down to detail.
- **Say it.** "A four-level line-item hierarchy, with annualisation for partial quarters."

### 8-table schema (PDF)

- **What it measures.** The number of tables in the normalised MySQL schema on SOADB, Uber's standard service-owned MySQL.
- **Verbal depth.** The code has 11 ORM models (JPA entity classes). The product has 8 screens. Don't confuse 8 tables with 8 screens.

### Led 3 engineers, 100% coverage, 50% delta-variance (PDF)

- **Led 3.** Tech lead of an EPAM pod of 3, not a people manager. Not to be merged with "mentored 2" at Masters.
- **100%.** Statement coverage of the migrated module, meaning every line ran during tests. 1,100+ tests is verbal, off the PDF.
- **50% delta-variance.** An automated gate in the review workflow. If a line's value moved more than 50% against its comparison period (for example the prior year), it is flagged and cannot pass the gate automatically. This supports SOX (Sarbanes-Oxley, the US law on financial controls) compliance. Keep the exact transition rules qualitative.
- **Say it.** "I led three engineers, took the module to 100% coverage, and added review gates that flag any line that moved more than 50% against its comparison period."

---

## Uber via EPAM: Menu Ingestion (Uber Eats)

### From 24 hours to 2 hours (PDF, HISTORICAL)

- **What it measures.** How long it took to onboard a restaurant's menu onto Uber Eats.
- **Why it mattered.** Faster onboarding means restaurants start selling sooner, and fewer menus wait in a manual queue.
- **Say it.** "Restaurant onboarding went from 24 hours to 2 hours."

### $600K a year saved (PDF, HISTORICAL, ESTIMATED arithmetic)

- **What it measures.** Annual cost avoided by replacing a third-party and manual menu-processing cost.
- **How it was derived.** About $2 per menu × 30,000 menus per month × 12 months = $720K list. Floored to $600K to be conservative.
- **Say it.** "About 600 thousand dollars a year. That's roughly two dollars a menu across 30 thousand menus a month, rounded down."
- **Don't say.** Don't say $720K. The resume uses the conservative floor.

### 30K+ menus a month (PDF, HISTORICAL)

- **Say it.** "Over 30 thousand menus a month."
- **Don't say.** The Kafka peak of roughly 200 to 500 events per second is a prep-only estimate. Don't put it next to this number.

### 98% field fidelity (PDF, offline evaluation)

- **What it measures.** The share of extracted menu fields (item name, price, description and so on) that matched the known correct answer on an offline test set.
- **How it was derived.** An offline evaluation: a fixed set of menus with labelled correct answers, compared field by field.
- **Say it.** "98% field accuracy on an offline evaluation."
- **Don't say.** Always say "offline". Older prep also mentions "100% schema consistency". That means a schema check rejected malformed output, and it isn't on the PDF.

### 95%+ extraction success (PDF, HISTORICAL, baseline ESTIMATED)

- **What it measures.** The share of scraping attempts that successfully pulled a menu.
- **How it was derived.** The baseline was an estimated 60% to 65% before hardening the Selenium fleet with proxy pools and adaptive retries.
- **Say it.** "Extraction success rose to over 95%, from roughly 60 to 65%."

### Exactly-once catalog upserts (PDF wording)

- **What it means.** Each menu change lands in the catalog once, even if a message is delivered twice. In practice this is at-least-once delivery plus idempotent upserts. *Idempotent* means doing it twice has the same effect as doing it once.
- **Don't say.** Don't claim zero message loss or two-phase commit across third parties.

---

## Uber Mobility: ANZ Document Compliance (HISTORICAL)

- **99.9% regulatory compliance.** The share of driver and vehicle documents that met local authority rules after automating the checks with a deterministic validation backend.
- **20 hours a week.** The manual review time removed.
- **Say it.** "99.9% compliance and about 20 hours a week of manual work removed."
- **Don't say.** It's Uber Mobility in Australia and New Zealand, not Uber Eats. Don't add Selenium or RAG to this story.

---

## Masters India: GST and e-invoicing

**Context in plain words.** Masters India sells GST compliance software. Enterprise clients send invoices, and the platform validates them and registers them with the government's IRP (Invoice Registration Portal), which returns an invoice reference number and a signed QR code.

### 75%, from 1.2 seconds to 300 milliseconds (PDF, HISTORICAL)

- **What it measures.** p95 API latency, meaning 95% of requests finished within this time.
- **How it was derived.** (1,200 − 300) ÷ 1,200 = 0.75, so 75%.
- **Why it happened.** Non-blocking calls to the government portal (so a slow portal no longer tied up a request thread), HikariCP connection pooling, query and index fixes, and Redis for reads.
- **Say it.** "p95 latency went from 1.2 seconds to 300 milliseconds."

### 1,500+ enterprise clients (PDF, HISTORICAL)

- **Say it.** "Over 1,500 enterprise clients."

### 700 to 4,000 requests per minute (PDF, HISTORICAL)

- **How to convert.** 700 ÷ 60 is about 12 requests per second. 4,000 ÷ 60 is about 67 requests per second. That's roughly 5.7 times more.
- **Say it.** "Throughput went from 700 to 4,000 requests per minute."

### 1M+ daily government submissions (PDF, ESTIMATED average)

- **How to convert.** 1,000,000 ÷ 86,400 seconds in a day is about 12 per second on average. Peaks around filing deadlines were roughly 8 to 10 times higher (ESTIMATED).
- **Say it.** "Over a million government submissions a day. That's about 12 a second on average, with big peaks around deadlines."

### 100K+ concurrent imports (PDF)

- **What it measures.** The scale of bulk imports processed with exactly-once, idempotent handling. The idempotency key was client plus file hash plus batch index.
- **Note.** Older prep said "100K+ per import". The resume says "100K+ concurrent imports". Use the resume wording.

### Mentored 2 (PDF)

- Two junior engineers during the migration. Never merge with "led 3" at Uber.

### Triage down 70%, database reads down 30% (PDF, HISTORICAL)

- **Triage 70%.** Time to find the cause of an incident. Baseline ESTIMATED at about 30 minutes, down to under 10, after adding ELK logs and New Relic tracing.
- **Reads 30%.** Database read load fell by 30% after a Redis cache-aside layer. *Cache-aside* means the app checks Redis first and only goes to the database on a miss.
- **Say it.** "Incident triage went from about half an hour to under ten minutes, and database reads dropped by 30%."

### Coverage 35% to 82%, 98% deployment success (PDF, HISTORICAL)

- **Coverage.** Test coverage went from 35% to 82%.
- **Deployment success.** 98% of deploys went out successfully, from release records. If asked for exact counts, keep it qualitative.

---

## GeeksforGeeks

- **10K+ daily queries.** Questions posted and handled on the doubt-support platform each day. Older resumes conflicted on this number, so use 10K+.
- **10x traffic spikes.** Traffic during live coding contests compared to normal.
- **20% lift in premium subscriptions.** A relative lift, attributed by the growth team.
- **30% course sales lift and 70% ops efficiency.** Business attribution, not your own measurement. Say: "I owned the engineering. The business team attributed the lift."

---

## Education and achievements

- **Google Code Jam 2021 qualifier, rank 2260 of 37,000+.**
- **Smart India Hackathon 2020 finalist, top 3 nationally.**
- CGPA is not on the PDF. Don't volunteer it.

---

## Off the PDF: numbers you may say, with a caveat

Always preface these with "that's not on my resume, but...".

| Number | What it is | Status |
|---|---|---|
| $100 per pass | Token spend for one engine pass | MEASURED, off PDF |
| 1.6M article-seasons | Size of the whole catalog. Not the 348k scored | Verbal |
| 100% Go coverage, 1,200+ tests | Impact Analytics Go code | LinkedIn, off PDF |
| 55 GB, 16 GB, 8 threads, 4 weeks | Out-of-memory fix caps | Verbal |
| 1,100+ tests | Uber FRM test count | Verbal |
| Copilot numbers (8.5%, 37 of 437, 14 tools) | Cluster Recommendation Copilot | Verbal, not a resume bullet |
| Line-plan 12B versus about 25M | A projected flat table versus an aggregate | Verbal. Never put 12B on the PDF |

**Removed from this page:** older prep listed "2.4B rollups" as a PDF number. It is not on the current resume. Don't quote it as a resume number.

**Never claim at Impact Analytics:** Kafka, Flink, CDC, Kubernetes operations, Milvus, or human review queues.
