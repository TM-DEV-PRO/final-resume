---

# 1. Project summary (paste-ready)

**One-liner (résumé project header):**
> **Agentic Assort Planner** — AI-assisted, multi-agent retail merchandise-planning platform (Impact Analytics). *Python (FastAPI, LangGraph, FastMCP) · Go (Gin) · Rust (Axum) · ClickHouse (insert-only versioned, end-to-end) · BigQuery · pgvector · GCP.* *(Stack per the July 2026 direction — see §10.)*

**2–3 line summary (top of the project block):**
> Designed and built the AI and data backbone of a next-generation assortment-planning product: a **router→orchestrator→specialist multi-agent system** that turns natural-language planning questions into a validated execution DAG, and a **three-tier data architecture** (BigQuery source-of-truth → Postgres editable system-of-record → ClickHouse/DuckDB OLAP serving) with a **tenant-unified schema at the derived grain**. Currently building its first shipping module — an **agentic store-clustering copilot** (deterministic tools on a dedicated ClickHouse read plane, LLM orchestration, three human confirm-gates) targeting <1 h to a finalized plan (from days), ≥20 configurations explored (from 1) and <2% run failures (from a measured 8.5%). Drove the ClickHouse decision via a runnable PoC and a cost/perf audit that cut recurring BigQuery scan cost by up to ~280×.

**Current-work one-liner (for "what are you doing right now?"):**
> "I'm building the clustering module of the agentic planner — a copilot where the planner states *what to cluster and for when*, and a dedicated agent handles store scoping, attribute selection and batch exploration on a dedicated ClickHouse read plane, with evidence packs and three human approval gates; approved clusters write back into the existing product unchanged. We spec'd it against live-audit baselines — 8.5% run failures, zero reproducibility, one configuration tried per plan — and the targets are <1 hour to a finalized plan, ≥20 configs explored, and p95 sub-500 ms agent data probes." *(Full depth: §9.)*

**How to describe the product in one breath (for interviews):**
> "It's the agentic rebuild of our assortment planner. A merchant works a plan through a staged pipeline — hindsight → strategy → clustering → line plan → buy plan — and a fleet of specialist AI agents runs alongside: surfacing issues as *Signals*, proposing scenarios, and acting autonomously overnight within approval thresholds. Under the hood it's a multi-agent orchestrator plus a three-tier data spine designed so a pivot-heavy, editable planning grid and scan-heavy hindsight analytics each run on the engine that's best at them."

**Where to place it on the résumé:** flagship project under Impact Analytics. Lead the project with 2 AI/agentic bullets and 2 data-architecture bullets (the most senior, best-evidenced work), then 1–2 cost/perf or leadership bullets depending on the JD (§7 has tailoring guidance).
