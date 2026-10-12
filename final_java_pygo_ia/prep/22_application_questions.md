# Application / screening questions (paste-ready)

<div class="callout note">
<b>How to use this page</b>
<ul>
<li>This is the copy-paste bank for written application forms ("Describe an AI system you built", "Tell us about a RAG system", "What is the largest system you have worked on").</li>
<li>Each question has a <b>full answer</b> (for long text boxes), a <b>short answer</b> (for 500-character boxes) and a <b>checklist</b> (for bullet fields). Paste the code-block text as it is.</li>
<li>Read the "Check before you paste" note under each question first. Those notes stop you from over-claiming.</li>
<li>Memorise the numbers in the checklists. They are the same numbers that are on the PDF, so a recruiter can cross-check them.</li>
</ul>
</div>

This page is the canonical bank for this track (`Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf`, Java, Python and Go). The HTML twin is [`../ApplicationKit.html`](../ApplicationKit.html) and the longer kit is [`../ApplicationKit.md`](../ApplicationKit.md). If anything here disagrees with [`GROUND_TRUTH.md`](GROUND_TRUTH.md), the ground truth wins. The Keep/Drop pipeline reference is [`../docs/assort_kd_flow/PIPELINE.md`](../docs/assort_kd_flow/PIPELINE.md).

**Tags used on this page.** MEASURED means there is a log, document or code to back the number. ESTIMATED means it is arithmetic I can show. HISTORICAL means it comes from my past work records. A gate (like the 80% CI gate) is a promotion rule, not a live result.

**Verbal only.** The Cluster Recommendation Copilot (14 tools, the 8.5% run-failure baseline) and Hindsight are interview depth. They are not PDF bullets, so never paste them into a form unless the form asks specifically about clustering, and even then say they are design work.

---

## 1. Describe an autonomous AI system you built and deployed (LangGraph / LlamaIndex / ADK)

**What the question is really asking.** They want proof that you built an AI system that takes several steps on its own, that it runs in production, and that you kept it safe and measurable. Your best answer is Impact Analytics (AssortSmart), because it has both a batch AI engine and a shipped chat copilot.

**Words you may need to explain in an interview after this form.**

- **LangGraph** is a Python library for building AI agents as a graph of steps. Each node is a step (call the model, check the answer), and edges decide what runs next. Think of it as a flowchart that an LLM can walk through.
- **Supervisor** is the node that reads the user's question and decides which specialist step should handle it, like a receptionist routing calls.
- **Evaluator loop** is a check step that grades an answer and sends it back for another try if it is not good enough. Ours stops after 3 attempts so it can never loop forever.
- **ClickHouse** is a column-oriented analytics database built for fast reads over billions of rows.
- **ReplacingMergeTree** is a ClickHouse table type that keeps only the newest version of a row with the same key. You never update in place. You insert a new version, and a background merge later drops the old one.
- **CI gate** is an automatic test in the build pipeline that blocks a change from being promoted if a score is below a bar.

<div class="callout warn">
<b>Check before you paste.</b>
The framework is <b>LangGraph</b>, not LlamaIndex or ADK. Say so plainly.
MCP is skills-level for me, not an Impact Analytics bullet, so do not name it here.
Ask Iris is a <b>shipped capability</b>. Do not add usage numbers or an SLA.
The 80% is a <b>CI promotion gate</b>. It is not "every tenant runs at 80% accuracy".
The 73% cost cut and the 74% baseline come from a separate 200-case benchmark, not the 300-case harness.
No Kafka, Flink or Kubernetes operations on this product. Kafka and Flink are Uber Eats Menu.
</div>

### Full answer

```text
At Impact Analytics I build the AI layer of AssortSmart, a retail merchandise planning product. I own two pieces: a batch AI decision engine and a planner-facing copilot called Ask Iris. The agent framework is LangGraph (not LlamaIndex or ADK), and it drives Ask Iris. The batch engine deliberately has no LLM orchestrator: it runs a fixed step order (peer step, decider, lenses, blend, explanation) controlled by our own registry, which keeps it predictable at scale.

The decision engine runs three pipelines (Keep/Drop, Missed Opportunities and Top Style) and evaluates 348k article-seasons, which means one product in one selling season. It processes 88k items per pass. For each item it blends deterministic KPI math, such as sell-through and rate of sale, with structured LLM calls across 7 AI lenses. The model never queries the database. Instead we read from a 2.11B-row ClickHouse master table and hand the model a JSON payload of exactly the context it needs. Results are written back with ReplacingMergeTree, so writes are insert-only and eventually consistent. If the LLM times out, the item falls back to its deterministic baseline score, so a pass always completes.

All pipelines share one orchestration registry. It provides hard timeouts, circuit breakers that stop calling a failing model, durable checkpoints so a restarted run skips work already done, and a frozen config_hash. The config_hash is a SHA-256 fingerprint of the guardrails, parameters, prompts and catalog, stamped on every output row so any decision can be traced to the exact configuration that produced it. Custom JSON telemetry records tokens, USD cost, step duration and batch fallbacks.

Ask Iris is a shipped, JWT-secured WebSocket copilot. Planners use it to query KPIs and inspect why the AI made a decision. A LangGraph supervisor routes each question, and an evaluator loop retries a weak answer at most 3 times, which stops infinite loops. The user's hierarchy access is frozen at the socket handshake, so a conversation can never drift into another tenant's data. We trace it with LangSmith.

Reliability is enforced by a gate. A 300-case proxy evaluation harness feeds an 80% accuracy CI gate, and a model or prompt change is not promoted unless it passes. That gate is how we refuse a bad agent. It is not a claim that every tenant is live at 80%. On a separate 200-case benchmark, the newer model cut live execution cost by 73% at 100% coverage. The deterministic baseline scored 74% on that benchmark, and the blended LLM score came in lower, so we froze the blend weights instead of retuning them to look better.

The HTTP edge in front of all this is a Go/Gin platform that handles 10k peak RPS with Datadog distributed tracing.
```

### Short answer

```text
At Impact Analytics I built AssortSmart's AI layer. A batch engine (Keep/Drop, Missed Opportunities, Top Style) runs a fixed, registry-controlled step order and scores 348k article-seasons, 88k per pass, by blending deterministic KPI math with 7 structured LLM lenses. The LLM gets JSON context, never SQL access, to a 2.11B-row ClickHouse table, and falls back to deterministic scores on timeout. I also shipped Ask Iris, a JWT-secured WebSocket copilot with a LangGraph supervisor, a 3-attempt evaluator and hierarchy access frozen at the handshake. Changes are promoted only through a 300-case harness and an 80% CI gate. Platform APIs are Go/Gin.
```

### Bullet checklist

```text
• Framework: LangGraph for Ask Iris (supervisor + 3-attempt evaluator). Not LlamaIndex or ADK.
• Batch engine: fixed step order run by our registry, no LLM orchestrator
• Product: AssortSmart Keep/Drop, Missed Opportunities, Top Style + Ask Iris copilot
• Scale: 348k article-seasons, 88k items per pass, 7 AI lenses
• Data safety: LLM gets JSON payloads, no SQL tool, over a 2.11B-row ClickHouse master
• Writes: ReplacingMergeTree (insert-only, eventually consistent); deterministic fallback on LLM timeout
• Orchestration: shared registry with hard timeouts, circuit breakers, durable checkpoints, config_hash
• Monitoring: LangSmith on Ask Iris, JSON run telemetry (tokens, USD, duration, fallbacks), Datadog on the Go edge
• Quality: 300-case harness + 80% CI promotion gate; 74% deterministic baseline on a separate 200-case bench
• Status: Ask Iris is a shipped capability; the 80% gate is a promotion rule, not "all tenants live"
```

**Follow-up they may ask:** "Why not let the agent write SQL?" Say: "Because a model with a SQL tool on a 2-billion-row table can run an expensive or wrong query, and it can read data outside the user's scope. Giving it a prepared JSON payload keeps cost predictable and access controlled by our code, not by the model."

---

## 2. Describe a production-grade RAG system for enterprise document processing

**What the question is really asking.** They want to see that you turned messy documents into reliable structured data with retrieval plus an LLM, and that you measured quality. Lead with **Uber Eats Menu** (Uber via EPAM). Do not move this architecture onto AssortSmart.

**Words you may need.**

- **RAG (Retrieval-Augmented Generation)** means you first look up relevant reference material, then give it to the LLM with the question, so the model answers from evidence instead of memory. It is like an open-book exam.
- **Embeddings** are lists of numbers that represent the meaning of text, so similar text has similar numbers.
- **Milvus** is a vector database. It stores embeddings and finds the most similar ones quickly.
- **Field fidelity** is the share of extracted fields (item name, price, section and so on) that match the correct answer.
- **Offline evaluation** means measured on a labelled test set, not on live production traffic.

<div class="callout warn">
<b>Check before you paste.</b>
98% is <b>offline evaluation</b> field fidelity. Always say "offline".
$600K/yr is a conservative floor of a $720K arithmetic (about $2 per menu × 30K menus × 12 months).
"Exactly-once" catalog upserts means at-least-once delivery plus idempotent writes. Do not claim zero message loss.
Older prep also cites 100% schema consistency offline. It is not on the PDF, so lead with 98%.
Spark is not on the PDF. Milvus is Uber Menu only, never Impact Analytics.
</div>

### Full answer

```text
At Uber via EPAM I worked on Uber Eats menu ingestion, which turns restaurant menus into Uber's catalog format so restaurants can go live. Many menus arrive as unstructured, multilingual PDFs, and the catalog needs a strict schema: sections, items, prices and options.

We built the extraction on Gemini 2.5 Pro with LangChain RAG over Milvus embeddings. For each incoming menu, retrieval pulls similar, already-labelled menus from Milvus and gives them to Gemini as grounded examples, and the output must pass a strict catalog schema before it is accepted. On our offline evaluation set this reached 98% field fidelity.

Around the model sits a large-scale ingestion pipeline on Kafka and Apache Flink. Flink does stateful, keyed deduplication by vendor and content hash, normalises the schema and performs exactly-once catalog upserts, which in practice means at-least-once delivery with idempotent writes so a replay never creates duplicates. Upstream, I hardened a Selenium scraping fleet with dynamic proxy pools and adaptive retries, which raised extraction success to 95%+ from an estimated 60-65%.

The business result: restaurant onboarding went from 24 hours to 2 hours, the pipeline handles 30K+ menus a month, and it saves about $600K a year by replacing roughly $2 per menu of manual and third-party cost.
```

### Short answer

```text
At Uber via EPAM I built Uber Eats menu ingestion that turns unstructured multilingual PDF menus into a strict catalog schema using Gemini 2.5 Pro with LangChain RAG over Milvus embeddings, reaching 98% field fidelity in offline evaluation. A Kafka + Flink pipeline does keyed deduplication and idempotent, exactly-once catalog upserts, and a hardened Selenium fleet lifted extraction success to 95%+. Onboarding went from 24 hours to 2 hours for 30K+ menus a month, saving about $600K a year.
```

### Bullet checklist

```text
• Company: Uber via EPAM, Uber Eats Menu Ingestion & Automation
• Model + retrieval: Gemini 2.5 Pro, LangChain RAG, Milvus embeddings
• Quality: 98% field fidelity (offline evaluation), strict catalog schema gate
• Pipeline: Kafka + Apache Flink, keyed dedupe (vendor + content hash), exactly-once upserts (at-least-once + idempotent)
• Acquisition: Selenium fleet with dynamic proxy pools and adaptive retries, 95%+ success (from est. ~60-65%)
• Impact: onboarding from 24 hours to 2 hours, 30K+ menus/month, ~$600K/yr saved
```

**Follow-up they may ask:** "Why Milvus and not pgvector?" Milvus was the vector store on that project. The general trade-off is that pgvector keeps vectors inside PostgreSQL, which is simpler when the vector set is small and you already run Postgres. A dedicated vector database like Milvus is built for large vector sets and fast similarity search. pgvector is skills-level for me, so keep that answer general.

---

## 3. Describe the most complex or largest-scale system you have worked on

**What the question is really asking.** They want one system, its scale in numbers, and the hard design choices. Pick based on the job: AssortSmart for platform or AI roles, Masters India for high-throughput API and event roles.

**Words you may need.**

- **RPS (requests per second)** is how many API calls the service handles each second. 10k peak RPS means the busiest moments reach 10,000 calls per second.
- **Rows per second** is a data copy rate, not API traffic. Never mix it with RPS.
- **Idempotency** means doing the same operation twice has the same effect as doing it once, so retries are safe.
- **Dead-letter queue (DLQ)** is a side queue where messages that keep failing are parked for inspection instead of blocking the main flow.

### Full answer (AssortSmart, platform and AI roles)

```text
The largest system I own is the AssortSmart platform at Impact Analytics, a multi-tenant retail planning SaaS. The API layer is Go/Gin and scales to 10k peak RPS. It uses Google Wire for compile-time dependency injection, a self-protecting HTTP edge with no reverse proxy, native h2c (HTTP/2 over a plain connection, without TLS), nested timeouts and Datadog distributed tracing.

The data layer is ClickHouse. The master fact table has 2.11B rows. Planner pivots used to take 189 seconds on a 250M-row benchmark harness. I built a pre-aggregation layer of six rollup tables and brought that down to 12 seconds, a 15.5x speedup. Separately, weekly rollup builds were running out of memory at 170GB, so I sliced the INSERT SELECT statements into one-fiscal-week chunks and enforced memory and disk-spill caps. I also wrote a Go native-TLS data pump that migrated rollups between ClickHouse Cloud clusters at about 344k rows per second, on partitions up to 4.09B rows, with 500k-row double-buffered batches and checkpoint ledgers so a restart never leaves duplicate rows.

On top of the platform sits the AI layer: a decision engine scoring 348k article-seasons with 7 LLM lenses and the shipped Ask Iris copilot, both gated by a 300-case harness and an 80% CI promotion gate.
```

### Full answer (Masters India, high-throughput API and event roles)

```text
At Masters India, a GST compliance and e-invoicing SaaS, I worked on the bulk e-invoicing pipeline that registers invoices with the government Invoice Registration Portal (IRP). It handled 1M+ government submissions a day for 1,500+ enterprise clients. We used Kafka as the event bus, PostgreSQL sharded by tax quarter, idempotency keys built from client, file hash and batch index so 100K+ concurrent imports could be retried safely, dead-letter queues, and bounded retries against an unreliable government portal.

I also led the migration from a legacy PHP monolith to Spring Boot microservices using the strangler pattern with a canary per route. p95 latency dropped by 75%, from 1.2 seconds to 300 milliseconds, and throughput rose from 700 to 4,000 requests per minute. I mentored 2 engineers through that migration.
```

### Bullet checklist

```text
• IA: Go/Gin 10k peak RPS; 2.11B-row ClickHouse master; pivots from 189s to 12s (15.5x, 250M-row harness)
• IA: 170GB weekly-build OOM fixed with one-week INSERT chunks + memory/spill caps (load time, not query time)
• IA: Go native-TLS pump ~344k rows/s (copy rate, not RPS) on partitions up to 4.09B rows (measured in flight)
• Masters: 1M+ IRP submissions/day, 1,500+ clients, Kafka, PostgreSQL sharded by tax quarter, idempotent 100K+ imports
• Masters: PHP to Spring Boot strangler migration, p95 from 1.2s to 300ms, 700 to 4,000 requests/min, mentored 2
```

<div class="callout warn">
<b>Say this carefully.</b>
The 15.5x pivot speedup (query time) and the 170GB OOM fix (load time) are two separate wins. One did not cause the other.
The 4.09B-row copy was measured while it was running. Do not say the cutover finished.
1M+ per day averages about 12 per second (1,000,000 ÷ 86,400). Peaks around filing deadlines were roughly 8-10x that, which is an ESTIMATE.
</div>

For "Why should we hire you?" use [`38_why_hire_tarun_qa.md`](38_why_hire_tarun_qa.md). For spoken versions of all of these, use [`32_common_interview_qa.md`](32_common_interview_qa.md) and [`37_senior_screen_deep_qa.md`](37_senior_screen_deep_qa.md).
