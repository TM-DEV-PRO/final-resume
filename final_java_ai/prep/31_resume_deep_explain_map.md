# Resume deep-explain map (study this before loops)

**Purpose:** Anything on the PDF you can defend in depth — each tech (where / why / problem solved), numbers, user flows, architecture, ER-ish schema notes. Prep keeps jargon; **PDF uses simple English**.

**PDF IA bullets (Aug 2026):** product · Keep/Drop engine (LangGraph + SELECT-only CH + 300-gold/≥80%) · dig-deeper QnA · ClickHouse POC from 189s to 12.3s. Project title: **Agentic AssortSmart (AI-Powered Retail Merchandise Planning)**. Pipeline: `../docs/assort_kd_flow/PIPELINE.md`. **Verbal only / not on PDF:** Cluster Recommendation Copilot · Hindsight · 14 tools / 8.5% / 63/8. Full defense: [`23a_ia_interview_pack.md`](23a_ia_interview_pack.md).

**Honesty:** MEASURED / TARGET / HISTORICAL / ESTIMATED — see [`GROUND_TRUTH.md`](GROUND_TRUTH.md).

**Packs:** [`23a`](23a_ia_interview_pack.md) · [`23b`](23b_uber_interview_packs.md) · [`23c`](23c_masters_gfg_interview_packs.md)  
**Diagrams:** `campaign_extras/interview_prep/architecture/` · deep dives `10`/`11`/`12`/`14`/`29`  
**Schemas + APIs:** [`34`](34_er_tables_tech_why.md) (ER/why) · [`35`](35_table_schemas_api_design.md) (columns + contracts)

---

## How to answer any tech (template)

1. **Where** — which product + which path (user click → API → store).  
2. **Why** — the failure mode it fixed (not “industry standard”).  
3. **Rejected** — one alternative you didn’t pick and why.  
4. **Number** — MEASURED vs TARGET vs HISTORICAL; never invent TPS for IA.  
5. **Failure** — what still breaks if this piece dies.

---

## Impact Analytics — AssortSmart (building, not shipped)

### User flow
Planner opens AssortSmart → Keep/Drop scores article × plan-season (ST%/ROS + LangGraph lenses) → CSV bake-and-promote behind gold gate → dig-deeper QnA explains locked decisions read-only → ClickHouse planning analytics (POC from 189s to 12.3s). **Verbal only:** Cluster Copilot / Hindsight if asked.

### Architecture flow
```
Planner UI (chat + grid)
    │
FastAPI + LangGraph + MCP (agent plane: sequence tools, explain)
    │  read-only tools (14) + 3 confirm steps
Go Gin / Spring Boot write APIs (doing layer: Manual UI + agent share same auth)
    │
ClickHouse planning store (per tenant) ← ingest ← BigQuery / GCS
Obs: LangSmith (agent) · Datadog (platform) · PostHog (product) · shared trace_id
```

### Tech on PDF

| Tech | Where used | Why / problem solved | Rejected / trade-off | Number defense |
|---|---|---|---|---|
| **FastAPI + LangGraph + MCP** | Planner chat / copilot | Orchestrate tool calls + prompts; MCP = typed tool surface | Raw LLM SQL → agent invents queries | Turnaround **days → under 1h**, configs **1 → ≥20** = **TARGET** |
| **Go Gin** (v2/PyGo) / **Spring Boot** (Java) | Write/doing APIs | Same write path as Manual UI; auth once; not “LLM writes DB” | Agent-only writes | Design; load test pending |
| **14 read-only tools + 3 confirm steps** | Agent safety | Stop bad clustering inputs before engine | Silent auto-finalize | Failures **8.5% (37/437 kik) → under 2%** MEASURED→TARGET |
| **ClickHouse 63/8** | Planning store | Fast pivots + versioned inserts; agent SELECT only | Postgres-only OLAP; CH `ALTER UPDATE` | **189s→12.3s** on **250M** MEASURED POC; **63/8** from DDL Phase-1 (`29`) |
| **Insert-only + swap partitions** | Facts/cubes refresh | Avoid mutation queue; atomic refresh | Row UPDATEs | Say “refresh by swapping partitions” on PDF; `argMax`/`FINAL` verbally |
| **~25M aggregate vs 12B store-week** | Line-plan grain (**not on PDF**) | Avoid table explosion | Flat store-week | **~0.4 ms** edits MEASURED; month rollups sub-second — verbal only |
| **BigQuery / GCS** | Upstream truth / files | Warehouse + object store for feeds | CH as sole system of record for all company data | Design |
| **Datadog / LangSmith / PostHog** | Ops / agent quality / product | Different questions each answers | One tool for everything | Design |

**ER / schema talk track:** 8 layers (stage twins, facts, dims, cubes, decisions/events…); agent `readonly=1`; services INSERT-only. Detail: [`29_ia_ch_ddl_phase1_source.md`](29_ia_ch_ddl_phase1_source.md), pack `23a`, deep dive `10`.

---

## Uber FRM (Finance)

### User flow
Finance opens Recon → loads HFM lines → Materiality / EMI / Group & Component Scoping / Residual Risk / Summary → flags material lines → exports feed PwC work papers.

### Architecture flow
```
Finance UI (8 screens, not owned) → FastAPI or Spring Boot backend (30+ REST)
    → handler/controller → service → repository
    → MySQL (11 tables, SQLAlchemy 2.0 or JPA)
Auth: gateway email header · Bazel/JUnit CI · PwC-facing releases
```

### Tech on PDF

| Tech | Where | Why | Rejected | Numbers |
|---|---|---|---|---|
| **FastAPI / Spring Boot backend** | FRM scoping APIs | Replace Sheets close; API ownership | Keep Sheets | **30+ APIs powering 8 screens** |
| **MySQL + 11-table schema** | System of record | Durable line IDs + audit trail | Sheets forever | **55 lines / 14 entities**; **$340M** materiality sample |
| **SQLAlchemy 2.0 / JPA** | ORM + joins | Typed models; explicit column labels | Raw SQL everywhere | Join bug: two columns same name → wrong identity (**HISTORICAL** fix story) |
| **HFM + 10-Q** | Recon truth | Internal extract vs public filing | Trust one source | Recon v2 **18 files** |
| **Led 3** | Delivery | Design reviews, contracts, CI | IC-only | Leadership claim |

Diagrams: `architecture/02_uber_frm.md` · pack `23b` · deep dive `11`.

---

## Uber Menu (Eats) + ANZ (Mobility — separate)

### User flow (Menu)
Partner menu URL/PDF/image → Selenium fetch → Kafka → Flink normalize → structured catalog **or** RAG/Milvus + Gemini extract → schema gate → low confidence human review → live menu.

### Architecture flow
```
Selenium fleet (IP rotate, proxies, retries)
    → Kafka → Flink
         ├─ structured HTML → catalog
         └─ PDF/image → chunk → Milvus retrieve → Gemini → validate → review
```

### Tech on PDF

| Tech | Where | Why | Rejected | Numbers |
|---|---|---|---|---|
| **Selenium** | Acquisition | JS-heavy partner sites | Static curl only | Part of **24h→2h**, **30K+/mo**, **$600K+**/yr |
| **Kafka + Flink** | Ingest pipeline | Buffer spikes; stream transform | Sync batch only | Same economics; don’t mix with Masters Kafka story |
| **LangChain RAG + Gemini + Milvus** | Unstructured menus | Multilingual PDF/image → schema | Pure regex OCR | **98% fidelity / 100% schema** = **offline HISTORICAL eval**; 100% = validation gate |
| **IP rotation / dynamic proxies / adaptive retries** | Anti-bot scrape fleet | Partner sites block bots | Fixed IP | **95%+** menu ingestions |
| **ANZ docs** | **Mobility** drivers/vehicles vs **local authorities** | Compliance automation | Manual checks | **99.9%**; **~20h/week** HISTORICAL — **not Eats** |

Diagrams: `architecture/03_uber_menu.md` · pack `23b` · deep dive `14` · panel `30`.

---

## Masters India GST

### User flow
Client ERP/dashboard → submit or bulk import invoices → validate → register with government IRP → IRN/QR back → webhook / dashboard progress.

### Architecture flow
```
Gateway canary (% FastAPI|Spring | fallback PHP)
    → microservices
    → Kafka (bulk chunks, IRP jobs, webhooks)
    → PostgreSQL (tables by tax quarter) + Redis + MongoDB payloads
    → IRP (gov) with idempotency keys, retries, DLQ
Obs: ELK + New Relic
```

**Plain English for “strangler”:** migrate endpoint-by-endpoint behind the gateway with canaries so filing day never goes dark; rollback = traffic flip. PDF just says migrated Laravel → microservices.

### Tech on PDF

| Tech | Where | Why | Rejected | Numbers |
|---|---|---|---|---|
| **Laravel → FastAPI / Spring** | Gradual cutover | Unblock PHP-FPM; ship services | Big-bang rewrite | **p95 1.2s→300ms**; **1,500+** clients; mentored **2** |
| **Kafka** | Bulk IRP path | Ordering, replay, fan-out | Sync-only / Rabbit alone | **1M+/day**, **100K+/import**, **700→4,000 req/min** HISTORICAL |
| **PostgreSQL by tax quarter** | Hot writes | GST is quarter-scoped; archive cold | One fat table | Same throughput story |
| **Idempotency + retries + DLQ** | Safe IRP retry | Double-register with gov is bad | Fire-and-forget | Narrative HISTORICAL |
| **Redis caching** | Hot GSTIN/config | Cut repeat reads on bulk | Hit DB every row | **−30%** reads |
| **ELK + New Relic + usage dashboard** | Ops | Faster triage; fewer tickets | SSH/grep only | Triage **−70%**, tickets **−35%**, coverage **35→82**, deploy **98%** |

Diagrams: `architecture/04_masters_gst.md` · pack `23c` · deep dive `12`.

---

## GeeksforGeeks

### User flow
Learner asks doubt / votes / pins → APIs → dashboards for influencers → crons process video/reminders offline.

### Tech on PDF

| Tech | Where | Why | Numbers |
|---|---|---|---|
| **Django / Spring Boot** | Backend rewrite | Survive **10K+** daily + **10×** contest spikes | HISTORICAL |
| **MySQL / MongoDB / Redis / ES** | Votes, pins, locks, search | Premium features | Premium **+15–20%** |
| **Influencer dashboard** | Sales | Earnings/coupons/filters | Course sales **+30%** (not video cron) |
| **Scheduled jobs** | Video / reminders / cleanup | Ops automation | Ops **+70%** — **separate** from sales bullet |

Diagrams: `architecture/05_geeksforgeeks.md` · pack `23c`.

---

## Quick “why this tech” cheat sheet

| If they point at… | One-line why |
|---|---|
| Go/Spring write APIs | Agent never owns writes; Manual UI and chat share one auth surface |
| LangGraph/MCP | Sequence audited tools; MCP keeps tools typed and reviewable |
| ClickHouse | Pivot/grid speed + insert-only planning; agent read-only |
| Kafka (Menu) | Decouple scrape from transform at menu volume |
| Kafka (Masters) | Ordered durable IRP work with replay for disputes |
| Milvus | Similar labeled menus for RAG before Gemini extract |
| Flink | Stream normalize after Kafka |
| Redis | Hot lookups on bulk paths |
| DLQ | Poison batch doesn’t poison the whole import |

---

## Study checklist (can you whiteboard this?)

- [ ] AssortSmart user flow + where agent stops (no SQL write)  
- [ ] CH 63/8 layers + why insert-only / partition swap (plain English)  
- [ ] Defend 8.5% and 189s→12.3s without saying “shipped under 2%”  
- [ ] FRM 8 screens + materiality rules + join-bug story  
- [ ] Menu Selenium→Kafka→Flink vs RAG path; ANZ ≠ Eats  
- [ ] Masters migration cutover + IRP idempotency key shape  
- [ ] GFG: sales dashboard vs video crons are **two** claims  

When PDF wording changes, update this file + packs’ “Resume XYZ” lines in the same PR.
