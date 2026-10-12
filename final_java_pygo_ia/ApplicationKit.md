# Application Kit (paste-ready)

This kit matches the **Final Java + AI (IA = Py/Go)** resume (`Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf`). Canonical source of truth: [AssortSmart tab resume](../docs/ASSORTSMART_TAB_RESUME.md). Everything inside a quote box is paste-ready for application forms. Everything outside the boxes is a note for you.

<div class="callout note">

**How to use this page**

- **What it covers:** one-liners plus ready answers to the free-text questions most application forms ask: complex system, AI experience, largest scale, leadership, a production bug, and why this company.
- **When to use it:** while filling an application form. For a version that leads with the Agentic chapter (as the PDF does), see [Application questions](application_questions.md).
- **What to memorise:** the notes under each answer. A screener may ask you to expand on any line you pasted.
- **Deeper answers:** the screening bank in [prep 22](prep/22_application_questions.md), and the handbook chapter [LinkedIn and outreach explained](handbook/12_linkedin_and_outreach.md).

</div>

**Tags.** MEASURED means there is a log, doc or benchmark behind the number. HISTORICAL means it comes from past work records. A "packet story" is a real engineering story from older prep that is not a PDF bullet, so label it honestly if you use it.

---

## One-liners

**Headline fit** (for "summarise yourself in one line" fields):

> Senior SWE Java · Python · Go · Go/Gin 10k RPS · ClickHouse 2.11B · 36 Spring Boot endpoints · Kafka 1M+/day · LangGraph Ask Iris

**30-second intro:** paste the short About from the [LinkedIn profile pack](linkedin/headline_about_experience.md).

**Why hire you:**

> FRM reconciliation cut 70%, from 14 days to 3, plus Kafka at 1M+/day, plus AssortSmart platform and AI: 10k RPS, the LLM decoupled from a 2.11B-row master, the shipped Ask Iris copilot, and an honest promotion gate.

**How to defend it.** 2.11B is the row count of the ClickHouse master table at AssortSmart. "Decoupled" means the LLM never queries that table. It only receives JSON prepared for it. 36 endpoints is Uber FRM. Kafka 1M+/day is Masters India.

---

## Common application questions

### Describe a complex system you designed

> At Impact Analytics I work on AssortSmart, a retail merchandise planning product, which has two layers.
>
> The platform layer is a multi-tenant Go/Gin service at 10k peak RPS, using Google Wire, h2c and Datadog tracing. I cut planner pivots in ClickHouse from 189s to 12s on 250M rows with six rollup tables, and fixed a roughly 170 GB out-of-memory failure in the weekly build. The platform also has a KPI formula parser with ifNotFinite division-by-zero protection, and an auth chain of Firebase, JWT and Google OIDC fronted by Redis, with Postgres-backed roles. The Go code holds 100% statement coverage across 1,200+ tests.
>
> The agentic layer runs Keep/Drop, Missed Opportunities and Top Style over 348k article-seasons, 88k items per pass, across 7 AI lenses. The models receive JSON payloads instead of querying the 2.11B-row ClickHouse master. Writes are eventually consistent through ReplacingMergeTree, with fallback to deterministic scores on LLM timeouts. An orchestration registry adds circuit breakers, checkpoints, a config_hash and JSON telemetry. I also shipped Ask Iris, a WebSocket copilot with a LangGraph supervisor and evaluator and hierarchy scopes frozen at the socket handshake. Promotions require a 300-case offline eval and an 80% CI gate, which is a promotion gate, not live accuracy for all tenants. A separate 200-case benchmark compares us against a 74% deterministic baseline.
>
> I also owned Uber FRM via EPAM: 36 Spring Boot endpoints, 19M GL rows, an L1–L4 FSLI hierarchy, an 8-table SOADB schema and SHA-256 keys. Reconciliation dropped 70%, from 14 days to 3, against $340M materiality. I led 3 engineers to 100% coverage, with SOX 50% delta-variance checks.

**What this means and how to defend it.**

- **The 15.5× pivot win and the 170 GB OOM are separate.** The first is query time on the rollups. The second is load time when building the weekly rollup. Fixing one did not cause the other.
- **ifNotFinite** is a ClickHouse function. The parser wraps every formula as `ifNotFinite(toFloat64(expr), 0)`, so a divide-by-zero returns 0 instead of infinity or NaN.
- **ReplacingMergeTree** is a ClickHouse table type that keeps only the newest version of rows sharing the same key. Think of a notebook where you never erase. You write the new value below, and a cleaner later crosses out the old line.
- **100% coverage across 1,200+ Go tests** is true but off-PDF (LinkedIn and verbal). Delete that sentence if a form says "resume facts only".
- **LangSmith** belongs to Ask Iris only. It is not on the Keep/Drop batch registry.
- **Older prep said** "ReplacingMergeTree two-phase" and "registry with LangSmith". The current resume says eventually consistent writes with deterministic fallback, and LangSmith on Ask Iris only.

### Experience with AI / LLMs / agents

> At AssortSmart the agentic flows blend structured LLM calls across 7 lenses with deterministic KPI math. The LLM gets JSON payloads rather than writing SQL against ClickHouse, and the system falls back to deterministic scores when the LLM fails. I shipped Ask Iris, a copilot built on a LangGraph supervisor and evaluator, with scopes frozen at the socket level. Guardrails include a 300-case offline harness, an 80% CI promotion gate, and a 74% deterministic baseline on a separate benchmark. At Uber Eats I used Gemini 2.5 Pro with LangChain RAG over Milvus to reach 98% field fidelity in offline evaluation, behind a hard schema gate, with 95%+ scrape success and Kafka + Flink exactly-once processing.

**What this means and how to defend it.**

- **"Structured LLM calls"** means the model must return a fixed JSON schema (for example a score and a reason), not free text.
- **98% is offline evaluation**, not live production accuracy.
- **ANZ 99.9% is HISTORICAL** and is Uber Mobility. It is a deterministic rules backend, not AI, so leave it out of this answer unless asked.
- **Verbal only, not on the PDF:** Cluster Recommendation Copilot and Hindsight (still being built). Mention them only if the form asks about a broader agentic roadmap.

### Largest scale

> At AssortSmart: 10k peak RPS, a 2.11B-row ClickHouse fact table, six ClickHouse rollup tables, 348k article-seasons, and 88k items per pass. A ClickHouse pivot benchmark went from 189s to 12s on 250M rows. At Masters India: a high-concurrency Kafka e-invoicing pipeline at 1M+ IRP submissions per day, 100K+ idempotent concurrent imports, and throughput from 700 to 4,000 requests per minute.

**What this means and how to defend it.** The 189s to 12s result is MEASURED on a 250M-row benchmark harness. 1M+ per day averages about 12 per second (1,000,000 ÷ 86,400). 700 to 4,000 requests per minute is roughly 12 to 67 requests per second. IRP is India's government Invoice Registration Portal.

### Leadership

> I led 3 engineers at Uber (via EPAM) on the FRM platform. I mentored 2 engineers at Masters India.

**How to defend it.** "Led 3" means tech lead of an EPAM pod, not people manager. Never merge the two into "led 5".

### Production bug you resolved

**Lead with the 170 GB weekly OOM (it is on the PDF).**

> On AssortSmart, building the weekly rollup for a whole season in one INSERT SELECT needed about 170 GB of memory and crashed with out-of-memory errors. I sliced the build into temporal chunks, one fiscal week per insert, and enforced memory and disk-spill caps (a 55 GB memory cap and 16 GB of spill). That stopped the OOM crashes.

**How to defend it.** The 55 GB and 16 GB caps are verbal detail, not on the PDF. Other verbal detail you can add: the whole-season build failed even with 80 GB and 200 GB caps, a product week needs about 11 GB, and an attr week needs more than 40 GB.

**Alternate: packet story (not a PDF bullet).** Company: Impact Analytics, a Python FastAPI worker. Do not claim Kubernetes cluster-operations ownership.

> A high-concurrency async Python worker consuming a queue started returning 504s while its memory kept growing. Heap profiles and APM traces showed database and HTTP clients being created inside a long-lived async loop without context managers, which leaked connections and cursors. I fixed it with `async with` blocks, connection-pool limits and consumer backpressure. To prevent a repeat, I added a load test at 3x peak in CI and pool metrics.

**How to defend it.** The leak and the fix are the real engineering story. Any Kubernetes "pod" wording from the original packet is design-level language, not something you operated. Do not name the queue as Kafka, because there is no Kafka on Impact Analytics. Do not use this as your Impact Analytics headline story. The 170 GB OOM is stronger and is on the PDF.

### Why this company

Pivot to technical alignment, not generic praise. Name one real system of theirs and map it to one of yours.

> Your [distributed store / event bus / applied-AI eval] work lines up closely with what I have built: a 2.11B-row ClickHouse master at AssortSmart, Kafka and Flink menu ingestion at Uber Eats, and 300-case promotion gates for LLM releases.

---

## Links

> Phone (+91) 9079727197 · tmittaliet@gmail.com · linkedin.com/in/t-mittal · github.com/TM-DEV-PRO

## Attach

[`artifacts/Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf`](artifacts/Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf)

## Deeper answers

Track screening bank: [prep/22_application_questions.md](prep/22_application_questions.md)
