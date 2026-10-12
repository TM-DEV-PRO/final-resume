# Chapter 2 — Every resume number, explained

<div class="callout note">
<b>How to use this chapter</b><br>
• Each number has five parts: <b>what it measures</b>, <b>where it comes from</b> (arithmetic or source), <b>why it mattered</b>, <b>how to say it</b>, and <b>what not to say</b>.<br>
• Interviewers love to ask "how did you measure that?". If you can explain the source in one sentence, the number becomes believable.<br>
• Read the "trap pairs" in section 7 last. Those are the numbers people mix up.
</div>

**Tags used below.**
- **MEASURED**: there is a log, benchmark, document or code that shows it.
- **ESTIMATED**: arithmetic you can show on a whiteboard. Say "roughly" and show the math.
- **HISTORICAL**: from your past work records at an earlier company. Say it plainly, and attribute business outcomes to the team that measured them.
- **OFF-PDF**: true, but not printed on the resume. Use it only when it helps an answer.

---

## 1. Summary line

| Number | Meaning | How to say it |
|---|---|---|
| **5 years** | Aug 2021 (GeeksforGeeks) to now: GFG ~1.3 yrs, Masters India ~1.5 yrs, Uber via EPAM ~1.9 yrs, Impact Analytics since May 2026 | "Five years building backend and data systems, the last two-plus on AI-assisted systems." |

---

## 2. Impact Analytics — AssortSmart (May 2026 to Present)

### Agentic

**348k article-seasons** · MEASURED
- *What:* How many product-in-a-season items the Keep/Drop engine scores.
- *Source:* The scored volume from the Keep/Drop runs.
- *Why it mattered:* It's far more than planners can review by hand, which is why automation plus explanations is valuable.
- *Say:* "It evaluates about 348 thousand article-seasons."
- *Don't:* Confuse it with the **1.6M** catalog (all product × season combinations, OFF-PDF).

**88k items per pass** · MEASURED
- *What:* The batch size of one scoring run.
- *Why:* Sized to fit memory and LLM provider rate limits. Also the unit that checkpoints and circuit breakers protect.
- *Say:* "About 88 thousand items per pass."
- *OFF-PDF:* about **$100 per pass** in token spend.

**7 AI lenses** · MEASURED
- *What:* Seven active LLM "questions" (colour cannibalisation, size curve, channel divergence, multi-season consistency, trend velocity, discount dependency, margin resilience).
- *Say:* "Seven structured lenses, each only run when the article has data for it."

**2.11B-row ClickHouse master** · MEASURED
- *What:* The size of the main fact table the agents' context comes from.
- *Why:* At that size, letting an LLM query it is dangerous and expensive. That's why it gets JSON.
- *Don't:* Mix it with **4.09B** (a rollup table in the copier story).

**3 attempts** (Ask Iris evaluator) · MEASURED (code constant `MAX_ATTEMPTS = 3`)
- *Why:* Enough to recover from a bad first answer, low enough to cap cost and stop loops.

**300 cases / 80% gate** · MEASURED (config `gold_min_accuracy: 0.8`, cases file)
- *What:* A 300-case proxy evaluation set. CI blocks promotion of a config that scores below 80%.
- *Say:* "Promotion is gated at 80% on a 300-case proxy set in CI."
- *Don't:* "80% accuracy in production for all tenants."

**73% lower cost at 100% coverage** · MEASURED (gold-200 benchmark)
- *What:* On a separate 200-case benchmark, the chosen model cost 73% less than the previous mini model and completed all 200 cases (100% coverage = no pending rows).
- *Why:* Running across all clients every season, cost is what decides whether it's viable.
- *Don't:* Say the 300-case set measured 73%.

**74% deterministic baseline** · MEASURED (same 200-case benchmark)
- *What:* Accuracy of the free rule-based score (threshold 0.65) on that 200-case set.
- *Why:* It's the bar the AI must beat. The blended LLM scored about 63%, below it, so blend weights were frozen.
- *Say:* "When the blend lost to the 74% rule, we froze the weights instead of tuning to the test."

### Core

**10k peak RPS** · on the PDF
- *What:* Peak requests per second the Go/Gin platform serves.
- *How to explain the source:* name the actual source you saw (for example a Datadog request-rate graph or a load test). Only say the one that's true for you.
- *Don't:* Turn it into an average or an uptime SLA.

**15.5× (189 s to 12 s on 250M rows)** · MEASURED (benchmark harness)
- *What:* The same planner pivot on a 250-million-row test: 189 seconds on the old PostgreSQL path, 12.3 seconds on ClickHouse rollups (rounded to 12 on the PDF).
- *Arithmetic:* 189 ÷ 12.3 ≈ 15.4. The harness reported about 15.5×. If someone checks, "about 15 times faster" is safe.
- *Why:* A 3-minute screen is unusable. 12 seconds is workable for a heavy grid.
- *Say:* "From 189 seconds to 12 seconds on a 250-million-row test."
- *Don't:* "Sub-second", or "because we fixed the OOM".

**170 GB OOM** · MEASURED
- *What:* Estimated memory a whole-season weekly `GROUP BY` needed. It failed even with 80 GB and 200 GB caps.
- *Fix knobs (OFF-PDF, true):* one fiscal week per insert, **55 GB** memory cap, **16 GB** spill, 8 threads, 4 weeks in flight. Product week ≈ **11 GB**, attribute week **> 40 GB**.
- *Don't:* Link it to the 15.5×. OOM = building tables. 15.5× = reading them.

**~344k rows/s** · MEASURED (live snapshot)
- *What:* Combined copy speed of the Go pump, two season streams of about 150k–190k rows/s each.
- *Don't:* Call it TPS or RPS. It's rows per second of bulk data.

**4.09B rows** · MEASURED
- *What:* Largest table copied: attribute weekly, two seasons (2,779,317,472 + 1,311,108,195).
- *Arithmetic (ESTIMATED):* 4.09B ÷ 344k ≈ 11,900 s ≈ 3.3 hours at that rate.
- *Don't:* Say the cutover finished. It was measured in flight.

**500k-row batches** · MEASURED
- *What:* Rows per insert batch in the pump, with double buffering (read the next 500k while sending the current one).

**OFF-PDF but true:** 100% Go statement coverage with race detection across **1,200+** tests (on LinkedIn). **839M** rows in product weekly for the same two seasons. Six rollup tables.

---

## 3. Uber via EPAM (Jul 2024 to May 2026)

### FRM Scoping Platform

**70% (from 14 days to 3 days)**
- *What:* Quarterly reconciliation time. The calendar went from about 14 days to about 3.
- *Source:* The technical design doc set a 70% reduction in manual ingestion and reconciliation time as the goal. The PDF states it as the outcome. Defend the PDF. If pressed: "the design doc framed that cut and that's what the platform delivered for the close."
- *If someone does the math:* 14 → 3 is about a 79% calendar cut. Say "I quote the conservative 70% figure, which is the reduction in manual reconciliation effort that the project measured itself against."
- *Why:* The close is time-boxed and audit-facing. Days saved is analyst time and risk saved.

**$340M materiality threshold**
- *What:* The dollar amount above which a misstatement would matter to someone reading Uber's financials. On the Q4 2025 close, group materiality was $340M (residual threshold $170M, verbal).
- *Why:* Every scoping decision ("is this line item in scope for audit?") compares against it.
- *Say:* "Against a $340 million materiality threshold." Present it as that close's value, not a fixed constant.

**19M raw GL rows**
- *What:* General-ledger rows covered by the Sheets-to-MySQL migration.
- *If asked about volume per quarter:* individual quarterly GL extracts were much smaller (tens of thousands of rows). The value of the system is correctness, hierarchy and auditability, not big-data throughput. Don't invent a breakdown of the 19M beyond "raw GL rows migrated off Sheets".

**36 endpoints (Spring Boot)**
- *What:* API endpoints shipped for the scoping workflow.
- *If they drill in:* about 31 functional routes in the scoping service handler, plus the collaboration-service APIs (comments, notifications) from the design doc.

**L1–L4 FSLI hierarchy**
- *What:* Four levels of Financial Statement Line Items, for example Assets → Current assets → Receivables → Trade receivables.

**8-table normalized schema**
- *What:* The core scoping schema on Uber's SOADB (MySQL). If they've seen code-level detail: the scoping service has 11 ORM models including recon and helper tables.

**Led 3 engineers**
- *What:* Tech lead of a 3-person EPAM pod on the ORM migration. Not a people manager.
- *Don't:* Merge with "mentored 2" (that's Masters India).

**100% statement coverage**
- *What:* Every line in the migrated module executed by tests. Statement coverage doesn't prove every behaviour is correct, so pair it with "plus tests for the aliasing bug class".

**50% delta-variance check**
- *What:* A state-machine gate. A line item can't move forward (for example to Closed) if its period-over-period change exceeds 50% without review.

### Menu Ingestion (Uber Eats)

**From 24 hours to 2 hours** · HISTORICAL
- *What:* Restaurant onboarding time for the menu. (24 − 2) ÷ 24 ≈ 92% faster.

**$600K per year** · HISTORICAL, arithmetic
- *Derivation:* about $2 per menu in manual or third-party cost × 30,000 menus × 12 months = $720K. Floored to $600K to be conservative.
- *Say:* "Roughly $2 a menu, 30 thousand a month, that's about $720K a year. I quote $600K to be conservative."

**30K+ menus per month** · HISTORICAL
- *Arithmetic:* about 1,000 a day.

**98% field fidelity** · HISTORICAL, offline evaluation
- *What:* Share of extracted fields (name, price, description, category...) that matched the labelled answer in an offline evaluation set.
- *Always say:* "offline", or "on our evaluation set".

**95%+ extraction success** · HISTORICAL
- *What:* Share of scrape-and-extract jobs that completed. The baseline before hardening was roughly 60–65% (ESTIMATED).

**OFF-PDF, prep only:** Kafka peak of about 200–500 events per second (ESTIMATED from fleet-run bursts). Don't put it on the resume.

### Document Compliance (Uber Mobility ANZ)

**99.9% compliance, 20 hours per week saved** · HISTORICAL
- *What:* Share of driver and vehicle documents meeting local authority rules after automation, and manual review time removed each week.
- *Don't:* Call it Uber Eats.

---

## 4. Masters India (Dec 2022 to Jun 2024)

**75% (from 1.2 s to 300 ms p95)** · HISTORICAL
- *Arithmetic:* (1.2 − 0.3) ÷ 1.2 = 75%.
- *p95 meaning:* 95 out of 100 requests finish within that time.
- *Why it improved:* async calls to the government portal, connection pooling, query and index fixes, Redis for reads.

**1,500+ enterprise clients** · HISTORICAL

**700 to 4,000 requests per minute** · HISTORICAL
- *Arithmetic:* 700 ÷ 60 ≈ 12 RPS. 4,000 ÷ 60 ≈ 67 RPS.

**1M+ daily government submissions** · HISTORICAL
- *Arithmetic (ESTIMATED):* 1,000,000 ÷ 86,400 ≈ 11.6, so about 12 per second on average. Filing-deadline peaks roughly 8–10× that.

**100K+ concurrent imports** · HISTORICAL
- *What:* Rows in bulk imports processed concurrently with idempotency keys.

**Mentored 2 engineers** · HISTORICAL

**Triage −70%** · HISTORICAL (baseline ESTIMATED: about 30 minutes to under 10)

**DB read load −30%** · HISTORICAL (Redis cache-aside)

**Coverage 35% to 82%, 98% deploy success** · HISTORICAL

---

## 5. GeeksforGeeks (Aug 2021 to Nov 2022)

**10K+ daily queries** · HISTORICAL. Well under 1 request per second on average. The hard part was **10× spikes** during live contests.
**20% premium lift** · HISTORICAL, relative, attributed by the growth team.
**30% course sales** · HISTORICAL, business attribution for the influencer dashboard.
**70% ops efficiency** · HISTORICAL, time saved on manual ops workflows by scheduled jobs.

*How to say business numbers:* "I owned the engineering; the business team measured and attributed the lift."

---

## 6. Education and achievements

| Number | Meaning |
|---|---|
| **2260 / 37,000+** | Rank in Google Code Jam Qualifier 2021 |
| **Top 3 nationally** | Finalist, Smart India Hackathon 2020 (MHRD) |
| B.Tech IT, IET Lucknow, 2017–2021 | CGPA isn't on the resume. Give it only if asked. |

---

## 7. Trap pairs (people mix these up)

| Pair | The difference |
|---|---|
| 348k vs 1.6M | Scored article-seasons vs whole catalog |
| 2.11B vs 4.09B | Agentic fact table vs largest rollup table copied |
| 15.5× vs 170 GB | Read speed-up vs build-time memory crash |
| 344k rows/s vs 10k RPS | Bulk copy speed vs API request rate |
| 300-case / 80% vs 200-case / 73% / 74% | CI gate vs model benchmark |
| Led 3 vs mentored 2 | Uber FRM vs Masters India |
| Menu Kafka vs Masters Kafka | Different products, different companies |
| 98% (Menu) | Offline evaluation, not live accuracy |
