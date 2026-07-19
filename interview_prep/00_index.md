# Final Resume — Interview Prep Hub

**Tarun Mittal · Senior Software Engineer · July 2026**

This hub backs every line of `resume/resume.tex` (PDF in `output/`). Study order:

1. **Project deep dives** — one chapter per resume project, in resume order: Impact Analytics (Agentic Assort Planner + Clustering Copilot), Uber FRM Scoping, Uber Menu Ingestion, Masters India GST, GeeksforGeeks.
2. **Tech deep dives** — every technology named on the resume: fundamentals, internals, why-this-not-that, gotchas. (ClickHouse/BigQuery/Postgres/DuckDB/LangGraph/RAG live in the playbook chapters at the end.)
3. **Behavioral bank** — 10 STAR stories mapped to Amazon Leadership Principles and Googliness signals, plus rapid-fire answers.
4. **Agentic Assort playbook (§0–§10)** — the full Impact Analytics reference: XYZ bullets with backing blocks, HLD/LLD, DB architecture, per-tech deep dives, Q&A bank, honesty tiers, the Cluster Copilot FRD digest, and the **July 2026 stack direction** (Go/Gin + Rust + ClickHouse end-to-end).

<div class="callout warn">
<b>Honesty guardrail (read before every interview).</b> Know which numbers are <b>REAL</b> (live-audit measured: 8.5% run failures = 37/437, 1 config per plan, 0% reproducibility, 75% Masters India latency), which are <b>offline-eval</b> (0.54→0.99 decomposition), and which are <b>design targets</b> (p95 &lt;500 ms, &lt;1 h to plan, &lt;2% failures). Say "measured," "in an offline evaluation," or "our design target" accordingly — the full tier table is in the playbook §7.4. BigQuery framing: it is the <b>upstream source of truth we ingest from</b> — never claim BigQuery optimization work as yours.
</div>

## The resume at a glance

| Company | Project | Lead metric |
|---|---|---|
| Impact Analytics (Jun 2026–) | Agentic AssortSmart (one project block) | Agentic microservice: conversational agent grounds scope, batch-evaluates ~100 silhouette-scored candidate clusterings, presents top 3 with evidence, days → <1 h · Go (Gin) core backend: worker pools, bounded channels, context timeouts · ClickHouse per-tenant, append-only never-erase store: partition swaps, latest-state views, lock-free writes (planning-grid p95 bullet currently commented out of resume) |
| Uber via EPAM (Jul 2024–May 2026) | FRM Scoping Platform (listed first) | 70% cycle (~2 weeks → ~3–4 days) · 36 endpoints p95 <300ms · 19M→300K rows |
| Uber via EPAM | Menu Ingestion Platform | 30K+ menus/mo · Kafka ~200–500 peak events/sec · +95% (~60–65% → 95%+) · Pinot sub-second |
| Masters India (Dec 2022–Jun 2024) | GST e-invoicing SaaS | p95 1.2s→300ms · 1M+ txn/day (~12 TPS avg, 100+ peak) · triage 70% (~30→<10 min) |
| GeeksforGeeks (Aug 2021–Nov 2022) | Backend (no project header on resume) | 100K+ daily queries (~1–2 RPS avg, ~10× spikes) · +15–20% relative |

## Metrics honesty

Every TPS/RPS/from→to on the PDF is catalogued in [`09_metrics_derivations.md`](09_metrics_derivations.md) as **DOCUMENTED** vs **ESTIMATED**. Read that before quoting numbers.
