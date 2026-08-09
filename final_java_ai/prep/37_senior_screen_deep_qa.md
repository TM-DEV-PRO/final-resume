# Senior screen deep Q&A — millions / prod / perf / product / deploy

**Purpose:** One place for the classic senior-screen questions interviewers ask early. Full answers + follow-ups. Honesty tags = MEASURED / TARGET / HISTORICAL / DESIGN / ESTIMATED per `GROUND_TRUTH.md`.

**Stack note (this file = Java final):** FRM + AssortSmart write APIs = **Spring Boot**. Menu/Masters/GFG stories stay Python-path truthful (Selenium/Kafka/Flink/RAG). Agent plane remains Python LangGraph/MCP.

**Related (deeper):** `23a`/`23b`/`23c` packs · `10`/`11`/`12`/`14` deep dives · `campaign_extras/.../deployment_and_scale.md` · `07_behavioral_star_stories.md` · `32_common_interview_qa.md`

---

## 0. Thirty-second cheat sheet

| Question | Lead with | Number to say | Honesty |
|---|---|---|---|
| Millions of requests? | Masters GST IRP on Kafka | **1M+ submissions/day**, **700→4,000 req/min** | HISTORICAL; ~12 TPS avg / 100+ peak **ESTIMATED** |
| Production issue? | Masters IRP timeout canary **or** Menu anti-bot drop **or** double-filing near-miss | triage **−70%**; ingest **95%+**; zero duplicate filings after fix | HISTORICAL |
| Perf in distributed systems? | Masters p95 **or** Menu 24h→2h **or** CH pivot POC | p95 **1.2s→300ms**; onboarding **24h→2h**; pivot **189s→12.3s** on **250M** | HISTORICAL / MEASURED POC |
| Core product? | Pick company they care about | AssortSmart / FRM / Eats menus / GST e-invoice / GFG | product truth |
| Complex system? | Menu E2E **or** Masters strangler **or** AssortSmart agent+CH | E2E ownership + tradeoffs | building for IA |
| How deploy? | Masters canary strangler **or** Menu jobs+Kafka rewind **or** IA dual deployables | canary %; offset rewind; agent≠Go ship | HISTORICAL / DESIGN |

---

## 1. Core product of each company you worked at

### Q1.1 What is the core product at Impact Analytics / AssortSmart?

**Answer:** AssortSmart is a **merchandise planning SaaS**. Retail planners decide **what to buy, how much, and which stores** for a season ahead. Store clustering and assortment plans are the foundation every buying strategy binds to. I own end-to-end architecture for the **Cluster Recommendation Copilot** (agent plane: Python LangGraph + MCP; write/doing plane: Spring Boot) and I am building **Hindsight** as the prior-season decision layer. I also drove **ClickHouse** adoption as the planning analytics engine after a row-identical **Postgres → ClickHouse** POC (**250M** rows, **189s → 12.3s**, ~**15.5×** MEASURED).

**Honesty:** Copilot is **building**, not fully shipped to every tenant. Load test pending. Do not invent IA TPS/RPM.

**Follow-ups**
- *Who is the user?* Merch planners / assortment teams at enterprise retailers.
- *What does success look like?* Faster plan turnaround (TARGET: days → under 1h), more configs explored (TARGET: ≥20), fewer failed clustering runs (MEASURED baseline **8.5%** → TARGET under **2%**).
- *Why agents?* Batch explore + explain; humans still approve writes (3 confirm gates).

### Q1.2 What did you work on at Uber (via EPAM)?

**Answer — two products, do not mix:**

1. **FRM Risk Scoping (Uber Finance):** Replaces quarterly Google Sheets risk scoping with a **Spring Boot + MySQL** system of record — **30+ REST APIs** powering **8 screens**, materiality sample **$340M** / residual **$170M**, ~**55×14** line/entity logic, Sheets→MySQL recon v2, led **3** engineers. Output feeds **PwC** audit work papers. Targeting **~70%** cut in manual recon cycle (~2 weeks → ~3–4 days) — **TARGET**, not measured.

2. **Uber Eats Menu Ingestion:** Owned menu ingestion **end to end on GCP**: Selenium → Kafka → Flink keyed normalize/dedupe; LangChain RAG + Gemini + Milvus with hard schema gate; scrape fleet to **95%+**. Outcomes: onboarding **24h→2h**, **$600K+/yr**, **30K+ menus/month** (HISTORICAL).

3. **ANZ Driver Document Compliance (Uber Mobility — separate):** Automated driver/vehicle doc checks vs **local authority requirements** to **99.9%**, removing ~**20 h/week** (HISTORICAL; not re-measured here). **Not Eats.**

**Follow-ups**
- *EPAM or Uber employee?* Via **EPAM**, client Uber — say that once, clearly.
- *Did you own React?* No frontend ownership claim on PDF.

### Q1.3 Masters India — what is the product?

**Answer:** **GST compliance / e-invoicing SaaS** for **1,500+** enterprise clients. Clients submit invoices; we validate, register with the government **IRP**, return IRN/QR. Bulk imports and reconciliation under filing deadlines. Correctness and idempotency beat raw speed — but filing days spike hard.

### Q1.4 GeeksforGeeks — what is the product?

**Answer:** Learning / content platform. I worked backend on **doubt-support** and monetization surfaces used by **10K+** daily queries with **10×** contest spikes: PHP→Django migration, voting/pinning/locking APIs, influencer earnings dashboard, cron pipelines for video/reminders/cleanup.

---

## 2. “Describe a complex system you designed / built”

### Q2.1 Pick your strongest complex system (recommended order)

**A. Uber Eats Menu Ingestion (best “complex distributed” story)**

**Answer:** Partner menus arrive as JS sites, PDFs, and images. I owned the path **end to end on GCP**:

```
Selenium fleet (IP rotate, dynamic proxies, adaptive retries)
  → Kafka ingest bus (replay, fan-out)
  → Flink keyed normalize/dedupe/route
       ├─ structured HTML → catalog upsert
       └─ PDF/image → LangChain RAG + Milvus retrieve → Gemini 2.5 Pro
            → hard schema validation gate → low-confidence human review → upsert
```

Complexity is not “many boxes” — it is **bursty adversarial acquisition**, **exactly-once-ish catalog writes under retries**, and **LLM output that must not poison the catalog** without a deterministic gate. Outcomes: **24h→2h**, **$600K+/yr**, **30K+/mo**, **95%+** success, offline **98%/100%** schema eval (**no SFT on PDF**).

**B. Masters India strangler + Kafka IRP (best “migration + scale” story)**

**Answer:** Migrated Laravel monolith → FastAPI microservices behind a gateway with **per-endpoint canaries**, shared DB during cutover (no dual-write SoR), then Kafka bulk path for IRP with idempotency keys, retries, DLQ, and PostgreSQL quarter sharding. Mentored **2**. Outcomes: p95 **1.2s→300ms**, **700→4,000 req/min**, **1M+/day**, **100K+/import**.

**C. AssortSmart Copilot + ClickHouse (best “agentic + analytics” story)**

**Answer:** Two planes — LangGraph/MCP agent (read-only tools, human gates) and Spring Boot doing APIs on append-only per-tenant ClickHouse. Complexity = **tool allow-lists + audit + OLAP pivots** without letting the LLM invent SQL. Status: **building**.

**Follow-ups**
- *What did you personally own?* Contracts, critical path, canaries/cutovers, anti-bot loop, schema gate — not “the whole company.”
- *What would you change?* Menu: stronger online fidelity SLIs. Masters: earlier async for all IRP. IA: finish load test before “shipped.”

### Q2.2 Application-form wording (“complex system you designed”)

Paste-ready short form lives in `ApplicationKit.md` / `22_application_questions.md`. Lead with AssortSmart architecture **or** FRM backend ownership + Menu E2E depending on JD (AI vs backend).

---

## 3. “Have you built a system that handles millions of requests?”

### Q3.1 Direct answer

**Yes — Masters India GST e-invoicing bulk/IRP path.**

**Answer:** We processed **1M+ IRP submissions per day** (HISTORICAL) for **1,500+** clients, with bulk imports at **100K+ transactions per import**. Sustained API throughput moved **700 → 4,000 requests/min** after the async/Kafka rewrite.

**How the math hangs together (say estimated if pressed):**
- 1M/day ≈ **~12 TPS** average (1e6/86400) — ESTIMATED arithmetic.
- Filing peaks are the design driver: roughly **8–10×** average → **~100+ TPS** bursts — ESTIMATED.
- Kafka + workers absorb spikes; government IRP latency variance is why we went async (202 + progress) instead of blocking request threads.

**Also cite (not “millions of HTTP RPS,” but real volume):**
- Menu: **30K+ menus/month** event-driven ingest (not millions of QPS — don’t inflate).
- GFG: **10K+ daily** queries with **10×** spikes.
- IA: **250M-row** pivot POC — analytics volume, not request RPS.

**Do not say:** “We handled millions of RPS.” Say **1M+ transactions/submissions per day** and explain TPS.

### Q3.2 Follow-ups

**Q: Why Kafka?**  
Bursty imports + flaky IRP; need durable buffer, replay, and fan-out to submit / persist / webhook consumers. Partition by client GSTIN for per-taxpayer ordering.

**Q: How avoid double-filing?**  
Idempotency key `client + fileHash + batchIndex` (+ invoice refs); DLQ for poison batches; near-miss incident drove this across the bulk path (STAR #10).

**Q: DB strategy?**  
PostgreSQL tables split by **tax quarter** so hot-quarter writes don’t thrash cold history.

---

## 4. “Tell me about a production issue you resolved”

Pick **one** primary; keep two backups.

### Q4.1 Masters — IRP timeout canary (best “I broke / I fixed”)

**Answer (STAR):**  
**S:** Early PHP→FastAPI canary: I set API timeouts too aggressively vs old PHP (e.g. ~10s vs ~60s). Legitimate IRP calls timed out — filing-day risk.  
**T:** Stop customer pain without rolling back the whole migration.  
**A:** Owned the miss; moved slow IRP calls fully **async** (202 + poll/progress); aligned timeouts with real IRP behavior; added **idempotency, retries, DLQ**.  
**R:** Canary stabilized; pattern became default for third-party compliance calls.

### Q4.2 Masters — double-filing near-miss (best “integrity”)

**Answer:** Retried bulk import nearly double-registered with IRP. Flagged to leadership, wrote the review, retrofitted idempotency + DLQ across the bulk pipeline — not one endpoint. **Zero duplicate filings** after rollout.

### Q4.3 Menu — anti-bot success collapse (best “moving target”)

**Answer:** Partner sites rotated defenses; scrape success dropped. Instrumented per-source block signatures; IP rotation, dynamic proxy pools, adaptive retries; fed block-rate into ops dashboards. Successful ingestions to **95%+**. Lesson: feedback loop > one trick.

### Q4.4 Masters — triage / observability (best “production discipline”)

**Answer:** Before: SSH + grep. After: ELK + New Relic with **request IDs** across API → Kafka → worker. Incident triage **~70%** faster (HISTORICAL; baseline ~30→&lt;10 min ESTIMATED). Claim **alerting + faster triage**, not SEV commander / formal pager title without proof.

### Q4.5 Follow-ups interviewers love
- *Root cause vs symptom?* Timeouts were config/assumption mismatch with third-party latency, not “FastAPI is slow.”
- *How did you prevent recurrence?* Async IRP standard + idempotency template + canary checklist.
- *Customer impact?* Near-miss: no customer damage yet — still treated as P0 process failure.

---

## 5. “Did you resolve a performance issue in a distributed system?”

### Q5.1 Masters p95 1.2s → 300ms (classic API perf)

**Answer:** Distributed after the strangler (many services + Redis + Kafka workers). Win was **not one cache magic**:
1. Async I/O for IRP/fan-out (stop blocking workers).
2. Redis cache-aside on hot reads (**−30%** redundant DB reads HISTORICAL) — helps p50 more than tail.
3. Query fixes: composite indexes `(client_id, invoice_date)`, kill N+1, pagination.
4. Connection pooling per service vs PHP-FPM per-request connect.

**Say:** Caching alone does **not** explain the full p95 move — async + queries drove the tail.

### Q5.2 Menu onboarding 24h → 2h (pipeline perf / freshness)

**Answer:** Replaced slow third-party/manual menu onboarding with in-house Selenium + **Kafka** + **Flink** keyed normalize/dedupe so catalog freshness stays hours not a day; anti-bot hardening kept the fleet at **95%+**. Money: kill ~$2/menu tool → **$600K+/yr** floor (HISTORICAL).

### Q5.3 ClickHouse pivot 189s → 12.3s on 250M rows (analytics perf)

**Answer:** MEASURED row-identical **Postgres → ClickHouse** POC for AssortSmart planning pivots. Drove CH adoption as planning analytics engine. Not “I rewrote production overnight” — **evidence-gated store decision**.

### Q5.4 FRM — careful honesty

**Answer:** FRM hardness is **correctness/audit**, not big-data throughput (GL extracts tens of thousands of rows/quarter — not millions of RPS). Do **not** invent FRM p95&lt;300ms as measured. Value = hierarchy + recon + PwC-ready trail.

---

## 6. Deployment — how do you deploy? CI/CD? Rollback?

### Q6.1 Masters (best deploy story)

**Answer:** **Strangler + canary:**
- New FastAPI services behind gateway.
- **Nginx** routes **% traffic per endpoint** to new service; watch error/latency; ramp to 100%.
- **Rollback = traffic flip**, not a rebuild.
- Shared DB during cutover → split tables after traffic moved.
- Contract tests vs recorded PHP payloads.
- pytest coverage gate (**35%→82%**); deploy success **98%** HISTORICAL.
- Kafka consumers for bulk; Docker on **AWS**.

### Q6.2 Uber Menu

**Answer:** Separate deployables: scraper jobs, Kafka, Flink jobs, RAG workers — Docker on **GCP**. Bad parser: **rewind Kafka offsets** / reprocess instead of re-scraping the internet. Proxy pools = config.

### Q6.3 Uber FRM

**Answer:** Spring Boot + MySQL; **Bazel** monorepo tests; Docker via Uber/EPAM release process. Staged rollout for finance tooling. Schema migrations expand/contract minded for audit. Rollback = previous revision + migration discipline.

### Q6.4 Impact Analytics

**Answer:** Dual deployables — **Python agent** and **Spring Boot** services + per-tenant ClickHouse. Ship independently. Hindsight metric catalogs can go live **without a code deploy**. Observability: Datadog + LangSmith + PostHog on one `trace_id`. **Honesty:** load test pending → say building.

### Q6.5 Follow-ups
- *Blue/green vs canary?* Canary per route for Masters (compliance risk).
- *Migrations?* Expand/contract; never break old readers mid-canary.
- *Secrets/config?* Don’t invent Vault ownership — say env/secret store via platform norms.
- *K8s?* Skills list has Kubernetes; do **not** claim cluster-admin/operator ownership unless asked as study (`17_senior_systems_study_only.md`).

---

## 7. Extra high-frequency screens (short answers)

### Q7.1 How do you monitor production?
Masters: ELK + New Relic + request-ID correlation + alerts on error/latency. IA: Datadog (platform) + LangSmith (agent) + PostHog (product). Menu: ingest success / block-rate / parse failure dashboards.

### Q7.2 How do you ensure reliability?
Idempotency, retries with jitter, DLQ, canaries, schema gates (Menu), human approval gates (IA agents), contract tests (strangler).

### Q7.3 Biggest technical challenge?
Pick one: Menu adversarial scrapers + schema-safe LLM writes **or** Masters filing-day IRP spikes **or** FRM Sheets→MySQL recon correctness.

### Q7.4 Scale a system 10×?
Masters: already lived filing spikes — queue load-level, autoscale workers on depth, shard hot quarter, cache hot reads, keep IRP async. Don’t scale the monolith.

### Q7.5 Disagreement / leadership?
FRM: led 3 via API contracts + design reviews. Masters: mentored 2 on extraction conventions. STAR bank has conflict/near-miss stories.

### Q7.6 Why Python vs Go (or Java)?
Java/Spring for FRM and AssortSmart write APIs; Python for agents/RAG/Menu scrapers — same products/metrics.

---

## 8. “All possible questions” drill index (where to go deeper)

| Topic | Open this |
|---|---|
| IA product / agents / CH | `23a_ia_interview_pack.md`, `10_impact_analytics_deep_dive.md` |
| FRM finance correctness | `23b` § FRM, `11_uber_frm_deep_dive.md` |
| Menu streaming / RAG / ANZ | `23b` § Menu, `14_uber_menu_deep_dive.md`, `30_panel_menu_anz_milvus.md` |
| Masters / GFG scale | `23c`, `12_masters_gfg_deep_dive.md` |
| Deploy shapes | `campaign_extras/interview_prep/deployment_and_scale.md` |
| Kafka/Flink defense | `campaign_extras/.../kafka_flink_scale_defense.md` |
| Behavioral STAR | `07_behavioral_star_stories.md` |
| HR / classic 21 | `32_common_interview_qa.md` |
| Screening forms | `22_application_questions.md`, `ApplicationKit.html` |
| Every PDF number | `18_resume_number_catalog.md`, `GROUND_TRUTH.md` |
| Study-only (don’t claim) | `17_senior_systems_study_only.md` |

---

## 9. Red lines (fail the screen if you say these)

- IA **shipped** to all tenants / invent **TPS/RPM**
- FRM **70%** as measured (it is TARGET)
- Menu **98%/100%** as live SLA (offline eval) or **SFT on PDF**
- ANZ as **Uber Eats** or “main-app”
- **Spark/Pinot/Vitess** ownership on PDF claims
- **SEV commander** / multi-region sole owner without proof
- “Millions of **RPS**” (say **1M+/day submissions** instead)
