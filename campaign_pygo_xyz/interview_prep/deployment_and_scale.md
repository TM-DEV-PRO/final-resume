# Deployment + scale for every resume project

How each project shipped, why that deploy shape, and the scale numbers you can defend. Tags: MEASURED / TARGET / HISTORICAL / DESIGN.

---

## Impact Analytics — Agentic AssortSmart + Hindsight

| | |
|---|---|
| **Scale** | Multi-tenant retail SaaS; kik audit **437** clustering runs; CH **63 tables / 8 layers**; pivot POC **250M** rows **189s→12.3s**; aggregates **~25M** choice-cluster-week; edits **~0.4 ms** |
| **Deploy shape** | Separate deployables: **Python FastAPI** agent service + **Go Gin** doing-layer services + per-tenant **ClickHouse** + UI. Config/catalog changes for Hindsight metrics **without code deploy**. |
| **Why** | Agent tier scales with LLM latency/cost; Go tier scales with request volume; boundary matches API contracts. Tenant CH isolates noisy neighbors. |
| **CI / gates** | Design review PASS; tool allow-list tests; **load test pending** before calling copilot shipped |
| **Honesty** | Say **building**. Do not invent prod TPS/RPM. |

**Deploy story (interview):** "Dockerized services on GCP. Agent and Go ship independently. Tenant onboarding is config sync into PG/CH catalogs, not a binary per retailer. Observability: Datadog + LangSmith + PostHog on one `trace_id`."

---

## Uber — FRM Risk Scoping

| | |
|---|---|
| **Scale** | **8** screens, **30+** REST APIs, **$340M** group / **$170M** residual sample, **55** FSLIs × **14** entities, **1,100+** Bazel tests, led **3** |
| **Deploy shape** | FastAPI services + **MySQL** SSOT + React UI; **Bazel** monorepo CI; Docker images behind Uber/EPAM release process |
| **Why** | Sheets could not be PwC audit SSOT. MySQL gives line-level audit trail tying **HFM** extracts to **10-Q**. |
| **CI / gates** | Design reviews, API contracts, pytest via Bazel — quality gate for audit-facing releases |
| **Honesty** | **70%** time cut is TARGET (~2 weeks → ~3–4 days). Do not claim multi-region FRM ownership. |

**Deploy story:** "Feature flags / staged rollout inside the finance tooling path. Schema migrations reviewed with audit trail in mind. Rollback = previous service revision + MySQL migration discipline (expand/contract)."

---

## Uber — Menu Ingestion

| | |
|---|---|
| **Scale** | **30K+** menus/month; onboarding **24h→2h**; **$600K+/yr**; ingest success **95%+**; offline RAG **98%** fidelity / **100%** schema; ANZ **99.9%**, **20 h/week** |
| **Deploy shape** | **Selenium** scraper fleet on **GCP** + **Kafka** ingest bus + **Flink** normalize/dedupe (hot path) + Python **RAG/Gemini** workers + Docker |
| **Why Kafka** | Scrapers are bursty/flaky; need replay and multiple consumers |
| **Why Flink** | Stateful keyed dedupe / event-time ordering for late pages; lower latency than Spark micro-batches for catalog freshness |
| **Why not Spark on hot path** | Spark for backfill/reprocess (verbal); Flink for streaming state |
| **Honesty** | RAG metrics are **offline eval**. $600K+ HISTORICAL vs third-party ~$2/menu. |

**Deploy story:** "Scrapers and consumers scale as separate jobs. Bad parser → rewind Kafka offsets before the bad watermark and reprocess. Proxies/IP pools are config, not code, for anti-bot."

---

## Masters India — GST / e-invoice

| | |
|---|---|
| **Scale** | **1,500+** clients; p95 **1.2s→300ms**; **700→4,000** req/min; **1M+** IRP/day; **100K+/import**; Redis **−30%** reads; triage **−70%**; coverage **35%→82%**; deploy success **98%** |
| **Deploy shape** | **Strangler:** FastAPI services cut over behind gateway **endpoint-by-endpoint** with **canary** % traffic; shared DB during move; Kafka consumers for bulk; Docker on **AWS** |
| **Why** | Laravel monolith: one slow IRP blocked a worker; all-or-nothing deploys; could not scale filing spikes |
| **CI / gates** | pytest coverage gate; contract tests vs old PHP payloads; ELK + New Relic alerts |
| **Honesty** | Triage baseline ~30→&lt;10 min ESTIMATED behind HISTORICAL 70%. |

**Deploy story:** "Nginx canary per route. Rollback = traffic flip, not a rebuild. Idempotency keys + DLQ so Kafka replay does not double-file."

---

## GeeksforGeeks — platform

| | |
|---|---|
| **Scale** | **10K+** daily users; **10×** traffic spikes; premium **+15–20%**; course sales **+30%**; ops efficiency **+70%** (HISTORICAL portfolio metrics) |
| **Deploy shape** | Django/app services + MySQL/Redis patterns of the era; CI deploys; feature work behind normal web release cadence |
| **Why** | Monetization + reliability under spike load on a content/learning platform |
| **Honesty** | Keep claims at product/ops outcomes; do not invent modern K8s/operator ownership for GFG. |

---

## Quick comparison table

| Project | Primary deploy unit | Bus / data plane | Hard scale number |
|---|---|---|---|
| IA Assort | FastAPI agent + Go services + CH | Kafka jobs (embed); CH OLAP | 250M pivot 15.5×; 8.5% baseline |
| FRM | FastAPI + MySQL + React | Sync REST; Bazel CI | $340M; 30+ APIs; 1100+ tests |
| Menu | Scraper jobs + Kafka + Flink + RAG workers | Kafka → Flink → catalog | 30K menus/mo; 24h→2h |
| Masters | FastAPI strangler + Kafka consumers | Kafka + PG shards | 1M+/day; 4k req/min |
| GFG | Web app releases | Classic LAMP-ish stack | 10K+ daily; 10× spikes |

## Related
- Architecture folder: [architecture/00_index.md](architecture/00_index.md)
- Numbers: [numbers_defense.md](numbers_defense.md)
