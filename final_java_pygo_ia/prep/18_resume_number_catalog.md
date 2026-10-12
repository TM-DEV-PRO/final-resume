# Resume Number Catalog (every PDF metric)

<div class="callout highlight">
<b>How to use this page</b>
<ul>
<li>This is the one-screen list of every number on <code>Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf</code>, with one plain sentence saying what each number means.</li>
<li>Read it five minutes before a call. If a number needs a longer explanation, follow the link to <a href="09_metrics_derivations.md">Metrics Derivations</a>, which has the arithmetic and the "say it / do not say it" lines.</li>
<li>Memorise the warning box and the off-PDF table. Those are where candidates usually slip.</li>
</ul>
</div>

**Tags in one line each.** MEASURED means there is a log, benchmark, config or doc. STATED means it is printed on the PDF from the project source, with no extra arithmetic in prep. ESTIMATED means arithmetic I can show. HISTORICAL means from my past work records. TARGET means a design goal.

Other sources: [GROUND_TRUTH](GROUND_TRUTH.md), [IA bullet defense](43_ia_bullet_defense.md), [IA interview pack](23a_ia_interview_pack.md), [FRM deep dive](11_uber_frm_deep_dive.md), [Menu deep dive](14_uber_menu_deep_dive.md), [Masters and GFG deep dive](12_masters_gfg_deep_dive.md).

<div class="callout warn">
<b>Numbers people mix up.</b> 348k article-seasons were scored. 1.6M is the catalog (off PDF). The 80% gate and the 300 cases are one benchmark. The 73% cost cut, 100% coverage and 74% baseline are a different 200-case benchmark. 15.5× is query time. 170 GB is load time. 344k is rows per second, not requests per second. The 4.09B copy was measured while running, not finished. "Led 3" is Uber FRM. "Mentored 2" is Masters India.
</div>

---

## Impact Analytics, AssortSmart (on the PDF)

AssortSmart helps retailers decide which products to keep, drop or add each season. An article-season is one product in one season.

### Agentic Flows and Orchestration

| PDF number | What it means in plain English | Tag | Defend in |
|---|---|---|---|
| **348k article-seasons** | The total number of product-season combinations the three decision pipelines (Keep/Drop, Missed Opportunities, Top Style) scored. | MEASURED | [43](43_ia_bullet_defense.md) A1 |
| **88k items per pass** | How many articles one batch run processes end to end. The same 88k appears as "88k-article batch runs" in the registry bullet. | MEASURED | 43 A1, A3 |
| **7 AI lenses** | Seven focused questions the LLM answers about each article. A decider picks which apply, and their scores are blended with rule-based KPI math. | MEASURED | 43 A1 |
| **2.11B-row ClickHouse master** | The main planning fact table has about 2.1 billion rows, so the LLM never queries it. It gets JSON payloads instead. | MEASURED | 43 A2 |
| **3-attempt evaluator loop** | In Ask Iris, the evaluator can send an answer back for a retry at most three times. This stops infinite loops. | MEASURED (code constant) | 43 A4 |
| **300-case proxy harness** | An offline test set of 300 labelled cases that every model or prompt change must pass before promotion. | MEASURED | 43 A5 |
| **80% accuracy CI gate** | The minimum score on the 300 cases to promote a change. It is a gate, not live accuracy. | MEASURED (config) | 43 A5 |
| **73% lower live execution cost** | On a separate 200-case benchmark, the chosen model cost about 73% less than the previous one for the same work. | MEASURED | 43 A5 |
| **100% coverage** | On that same 200-case benchmark, the cheaper model answered all 200 cases. This is answer completeness, not test coverage. | MEASURED | 43 A5 |
| **74% deterministic baseline** | The rule-only score (no LLM) got 74% on the 200 cases. The blended model scored lower, so we froze the blend weights. | MEASURED | 43 A5 |

### Core Infrastructure and Pipeline

| PDF number | What it means in plain English | Tag | Defend in |
|---|---|---|---|
| **10k peak RPS** | The multi-tenant Go/Gin platform handles about 10 thousand HTTP requests per second at peak, with no reverse proxy in front. | STATED | 43 C1 |
| **15.5×** | The heavy planner pivot query ran about 15.5 times faster on ClickHouse than on Postgres. 189,408 ms ÷ 12,256 ms ≈ 15.45. | MEASURED | [21](21_ia_pivot_benchmark_source.md), 43 C4 |
| **189s to 12s** | The same pivot took 189 seconds before and about 12 seconds after (12.3, rounded on the PDF). | MEASURED | 21, 43 C4 |
| **250M-row operations** | The benchmark dataset size. It was chosen to test future growth, not to describe today's largest client. | MEASURED | 21 |
| **170GB OOM** | A whole-season weekly rollup build needed about 170 GB of RAM and crashed. Slicing it into one fiscal week per insert with memory and spill caps fixed it. | MEASURED | [42](42_clickhouse_rollup_migration.md), 43 C4 |
| **~344k rows/s** | The custom Go copier moved about 344 thousand rows per second between ClickHouse Cloud clusters, across two parallel streams. | MEASURED | 42, 43 C5 |
| **4.09B rows** | The largest partition set copied: attribute-weekly rollups for two seasons (2,779,317,472 + 1,311,108,195). Measured in flight. | MEASURED | 42, 43 C5 |
| **500k-row batches** | The copier reads and sends half-million-row batches, reading the next while sending the previous (double-buffering). | MEASURED | 42 |

Mechanisms on the PDF with no number, still worth knowing: Google Wire (compile-time dependency injection), h2c (HTTP/2 without TLS), Datadog tracing, the KPI formula parser with `ifNotFinite` division-by-zero protection, the Firebase Admin then JWT / Google OIDC auth waterfall, constant-time API key comparison, ReplacingMergeTree writes, frozen config hash on every output row, TSV ledgers and partition rollback (drop the season partition, then recopy).

---

## Impact Analytics, verbal only (not on the PDF)

| Number | What it means in plain English | Tag |
|---|---|---|
| **1.6M article-seasons** | The full catalog. Not the same as the 348k scored. | MEASURED, off PDF |
| **About $100 per pass** | LLM token spend for one 88k-item pass, about a tenth of a cent per item. | MEASURED, off PDF |
| **0.4 / 0.6 blend, keep at 0.55** | Final score = 0.4 × rule score + 0.6 × LLM score. Keep if 0.55 or higher. | MEASURED (config) |
| **55 GB cap, 16 GB spill, one fiscal week** | The settings that stopped the 170 GB crash. Also 8 threads and 4 weeks in flight. | MEASURED |
| **Six rollup tables** | Product, store and attribute, each at season and weekly grain. | MEASURED (design) |
| **839M product weekly** | Product-weekly rollup rows for two seasons. | MEASURED |
| **~150k to 190k rows/s per stream** | Each copier stream. Two together make ~344k. | MEASURED |
| **100% Go statement coverage, 1,200+ Go tests** | On LinkedIn, not the PDF. | MEASURED, off PDF |
| **8.5% (37 / 437) to under 2%, 14 tools, 3 gates, under 1 hour, 20+ configs** | Cluster Recommendation Copilot. Measured baseline, design targets. Not a resume bullet. Say "building". | MEASURED baseline, TARGET, DESIGN |
| **63/8 DDL, ~12B to ~25M** | ClickHouse schema and line-planning lesson. Interview depth only. | DESIGN |

Do not invent any Impact Analytics throughput number beyond 10k peak RPS.

---

## Uber via EPAM, FRM Scoping Platform

FRM scoping decides each quarter which financial line items and entities are material enough to need audit testing. It replaced Google Sheets.

| PDF number | What it means in plain English | Tag |
|---|---|---|
| **70%** | Quarterly reconciliation time went down by about 70%. | STATED (framed in the design doc) |
| **14 days to 3 days** | The same cut in calendar time. The arithmetic gives about 79%, so 70% is the conservative figure. | STATED |
| **$340M materiality** | The dollar threshold every significance decision is compared against on the Q4 2025 close. | MEASURED |
| **19M raw GL rows** | General ledger rows migrated from Sheets into MySQL. The value was correctness and auditability, not big-data speed. | STATED |
| **36 Spring Boot endpoints** | About 31 scoping routes plus the collaboration-service APIs from the design doc. | MEASURED |
| **4-level FSLI (L1 to L4)** | Financial statement line items are a four-level tree, and the math rolls up and down it with quarter annualization. | MEASURED |
| **8-table schema** | The normalized MySQL schema on SOADB (Uber's service-owned MySQL). The code has 11 ORM models, which is verbal depth. | MEASURED |
| **3 engineers** | I was tech lead of an EPAM pod of three on the Spring Data JPA / Hibernate migration. Not a people manager. | HISTORICAL |
| **100% statement coverage** | Every statement in the migrated module was executed by tests. | STATED |
| **50% delta-variance** | The review state machine flags a 50% change between periods at an automated gate, for SOX controls. | STATED |

Older prep said "30+ endpoints, do not say 36", "do not say 19M" and "70% is a target". All three are obsolete. Defend the PDF.

---

## Uber via EPAM, Menu Ingestion (Uber Eats) and Document Compliance (Mobility ANZ)

| PDF number | What it means in plain English | Tag |
|---|---|---|
| **24 hours to 2 hours** | Time to get a restaurant's menu live dropped from a day to two hours. | HISTORICAL |
| **$600K annually** | About $2 per menu × 30K per month × 12 = $720K, floored to $600K. | ESTIMATED on HISTORICAL inputs |
| **30K+ menus monthly** | About 1,000 menus a day on average. | HISTORICAL |
| **98% field fidelity** | 98% of extracted fields matched labelled truth in offline evaluation. Gemini 2.5 Pro, LangChain RAG, Milvus. | HISTORICAL, offline evaluation |
| **95%+ extraction success** | Scrapes that produced a usable menu, up from an estimated 60% to 65%. | HISTORICAL, ESTIMATED baseline |
| **99.9% compliance (ANZ)** | Driver and vehicle documents meeting local authority rules after automation. Mobility, not Eats. | HISTORICAL |
| **20 hours per week (ANZ)** | Manual review time removed each week. | HISTORICAL |

Kafka plus Flink with keyed deduplication and exactly-once catalog upserts is on the PDF. In practice that is at-least-once delivery plus idempotent upserts. Spark is not on the PDF.

---

## Masters India, GST E-Invoicing

| PDF number | What it means in plain English | Tag |
|---|---|---|
| **75%** | p95 latency (the slow tail) fell by three quarters. | HISTORICAL |
| **1.2s to 300ms** | The p95 before and after the PHP to Spring Boot migration. | HISTORICAL |
| **1,500+ enterprise clients** | Customers on the platform. | HISTORICAL |
| **Two engineers** | I mentored two engineers through the migration. | HISTORICAL |
| **700 to 4,000 requests per minute** | About 12 to 67 requests per second. | HISTORICAL |
| **1M+ daily submissions** | E-invoices sent to the government portal per day, about 12 per second on average. | HISTORICAL, rate ESTIMATED |
| **100K+ concurrent imports** | Bulk imports processed idempotently, so retries never duplicate an invoice. | HISTORICAL |
| **70% triage** | Time to locate the cause of an incident, roughly from 30 minutes to under 10. | HISTORICAL, ESTIMATED baseline |
| **30% lower DB read load** | Redis cache-aside took repeat reads off PostgreSQL. | HISTORICAL |
| **35% to 82% coverage** | Automated test coverage before and after. | HISTORICAL |
| **98% deployment success** | Deployments that went out without rollback. | HISTORICAL |

---

## GeeksforGeeks

| PDF number | What it means in plain English | Tag |
|---|---|---|
| **10K+ daily queries** | Student doubts handled per day on the doubt-support platform. | HISTORICAL |
| **10x spikes** | Contest traffic reached about ten times normal. | HISTORICAL |
| **20% premium lift** | Relative lift in premium subscriptions, attributed by the growth team. | HISTORICAL |
| **30% course sales** | Growth after the influencer analytics dashboard, attributed by the business team. | HISTORICAL |
| **70% ops efficiency** | Less manual operations work after scheduled background workflows. | HISTORICAL |

---

## Achievements

| PDF number | What it means in plain English | Tag |
|---|---|---|
| **2260 / 37,000+** | Google Code Jam Qualifier 2021 rank, roughly the top 6%. | HISTORICAL |
| **Top 3 nationally** | Smart India Hackathon 2020 (MHRD) finalist. | HISTORICAL |
