# Application Kit (paste-ready)

This kit matches the **Final Java + AI (IA = Py/Go)** resume (`Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf`). Canonical source of truth: [AssortSmart tab resume](../docs/ASSORTSMART_TAB_RESUME.md). Everything inside a quote box is paste-ready for application forms. Everything outside the boxes is a note for you.

<div class="callout note">

**How to use this page**

- **What it covers:** ready answers to the free-text questions on most application forms. They lead with the Agentic chapter, in the same order as the PDF.
- **When to use it:** while filling an AI-leaning or applied-AI application. For a platform-first version, see the [Application Kit](ApplicationKit.md).
- **What to memorise:** which numbers come from which test set. The 300-case harness and the 80% gate are one set. The 73% cost cut and the 74% baseline come from a separate 200-case gold benchmark.
- **Deeper answers:** the screening bank in [prep 22](prep/22_application_questions.md), and the handbook chapter [LinkedIn and outreach explained](handbook/12_linkedin_and_outreach.md).

</div>

**Tags.** MEASURED means there is a log, doc or benchmark behind the number. HISTORICAL means it comes from past work records. "Off-PDF" means true and said on LinkedIn or verbally, but not printed on the resume.

---

## One-liners

**Headline fit** (for "summarise yourself in one line" fields):

> Senior SWE Java · Python · Go · Go/Gin 10k RPS · ClickHouse 2.11B · 36 Spring Boot endpoints · Kafka 1M+/day · LangGraph Ask Iris

**30-second intro:** paste the short About from the [LinkedIn profile pack](linkedin/headline_about_experience.md).

**Why hire you:**

> FRM reconciliation cut 70%, from 14 days to 3, plus Kafka at 1M+/day, plus AssortSmart: 10k RPS, 348k article-seasons, JSON payloads instead of LLM queries against a 2.11B-row master, the shipped Ask Iris copilot, and an 80% promotion gate.

**How to defend it.** 36 endpoints is Uber FRM. Kafka 1M+/day is Masters India, not Impact Analytics. The 80% is a CI gate a release must pass, not live accuracy for every tenant.

---

## Common application questions

### Describe a complex system you designed

> At Impact Analytics I work on AssortSmart, a retail merchandise planning product, which has two layers.
>
> The agentic layer runs Keep/Drop, Missed Opportunities and Top Style over 348k article-seasons, 88k items per pass, across 7 AI lenses. The models receive JSON payloads instead of querying the 2.11B-row ClickHouse master. Writes go through ReplacingMergeTree, with fallback to deterministic scores on LLM timeouts. A shared registry provides circuit breakers, checkpoints and a config_hash on every output row. I also shipped Ask Iris, a JWT-secured WebSocket copilot with a LangGraph supervisor, a 3-attempt evaluator, and hierarchy access frozen at the handshake. Releases pass a 300-case proxy eval, and 80% is a CI promotion gate. Separately, a 200-case gold benchmark compared us against a 74% deterministic baseline, and the model chosen there made scoring 73% cheaper at 100% coverage.
>
> The core layer is a multi-tenant Go/Gin platform at 10k peak RPS, using Google Wire, h2c and Datadog. I cut ClickHouse planner pivots from 189s to 12s on 250M-row operations with six rollup tables, and fixed a 170 GB out-of-memory failure in the weekly build. The core also includes a KPI tokenizer with division-by-zero protection, and Firebase, JWT and OIDC auth fronted by Redis, with Postgres roles.
>
> I also owned Uber FRM via EPAM: 36 Spring Boot endpoints, 19M GL rows, an L1–L4 FSLI hierarchy, an 8-table SOADB schema and SHA-256 keys. Reconciliation dropped 70%, from 14 days to 3, against $340M materiality. I led 3 engineers to 100% coverage, with SOX 50% delta-variance checks.

**Optional add-on sentence (true, off-PDF):**

> The Go codebase holds 100% statement coverage across 1,200+ tests.

**What this means and how to defend it.**

- **An article-season** is one product in one selling season. 348k is what the engine scores, and 88k is one batch pass.
- **config_hash** is a SHA-256 fingerprint of the guardrails, parameters, prompts and catalog used for a run. Every output row carries it, so you can always tell which configuration produced a decision.
- **The 80% gate and the 74% baseline come from different test sets.** The 300-case harness is the gate. The 200-case gold benchmark gave the 73% cost cut (model choice) and the 74% deterministic baseline. On that benchmark the blended LLM scored lower than the baseline, so the blend weights were frozen rather than retuned.
- **The 15.5× pivot win and the 170 GB OOM are separate.** One is query time, the other is load time.

### Experience with AI / LLMs / agents

> At AssortSmart the agentic flows blend structured LLM calls across 7 lenses with deterministic KPI math. The LLM gets JSON payloads rather than writing SQL against the 2.11B-row master, and the system falls back to deterministic scores on timeout. I shipped Ask Iris, a JWT-secured WebSocket copilot with a LangGraph supervisor, a 3-attempt evaluator, hierarchy access frozen at the handshake, and LangSmith tracing. Guardrails include a 300-case proxy harness and an 80% CI promotion gate. We also benchmarked against a 74% deterministic baseline and froze the blend weights when the LLM lost. The 73% cost cut at 100% coverage came from that benchmark's model pick. At Uber Eats I used Gemini 2.5 Pro with LangChain RAG over Milvus to reach 98% field fidelity in offline evaluation, behind a hard schema gate, with 95%+ scrape success and Kafka + Flink exactly-once processing.

**What this means and how to defend it.**

- **The 3-attempt evaluator** is a loop with MAX_ATTEMPTS = 3. If the answer still fails the evaluator after three tries, the loop stops instead of running forever.
- **Hierarchy frozen at the handshake** means the planner's allowed scope is read once when the WebSocket opens and cannot change mid-session, which prevents cross-tenant leaks.
- **Ask Iris is a shipped capability.** No SLA or usage numbers are claimed, so do not invent any.
- **98% is offline evaluation.** Milvus is Uber Menu only.
- **ANZ 99.9% is HISTORICAL** and Uber Mobility. It is not an AI project.
- **Verbal only, not on the PDF:** Cluster Recommendation Copilot and Hindsight (still being built). Mention them only if the form asks about a broader agentic roadmap.

### Largest scale

> At AssortSmart: 10k peak RPS, a 2.11B-row ClickHouse master, six ClickHouse rollup tables, 348k article-seasons, and 88k items per pass. A ClickHouse pivot benchmark went from 189s to 12s on 250M rows. At Masters India: a high-concurrency Kafka e-invoicing pipeline at 1M+ IRP submissions per day, 100K+ idempotent concurrent imports, and throughput from 700 to 4,000 requests per minute.

**What this means and how to defend it.** The 189s to 12s result is MEASURED on a 250M-row benchmark harness. 1M+ per day averages about 12 per second. 700 to 4,000 requests per minute is roughly 12 to 67 requests per second.

### Leadership

> I led 3 engineers at Uber (via EPAM) on the FRM platform. I mentored 2 engineers at Masters India.

**How to defend it.** "Led 3" means tech lead of an EPAM pod, not people manager. Keep the two numbers separate.

### Production bug you resolved

**Lead with the 170 GB weekly OOM (it is on the PDF).**

> On AssortSmart, a whole-season weekly INSERT SELECT used about 170 GB of memory and crashed with out-of-memory errors. I sliced it into temporal chunks, one fiscal week per insert, and enforced memory and disk-spill caps (a 55 GB memory cap and 16 GB of spill). That stopped the OOM crashes.

**How to defend it.** The 55 GB and 16 GB caps are verbal detail, not on the PDF. Do not use a FastAPI or Kafka heap-leak packet story as your Impact Analytics headline.

**Masters India alternate:**

> At Masters India, a canary release of the IRP integration showed that our timeouts were too aggressive for the volatile government portal. We moved those calls to async processing with idempotency, so retries were safe.

**How to defend it.** A canary release sends a small share of live traffic to the new version first. Idempotency means sending the same request twice has the same effect as sending it once, so a retry cannot register an invoice twice.

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
