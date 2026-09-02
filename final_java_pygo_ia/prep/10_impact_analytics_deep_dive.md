# Impact Analytics — AssortSmart deep dive (Final Java + AI (IA = Py/Go))

**PDF (Sep 2026):** two subsections. Canonical: `docs/ASSORTSMART_TAB_RESUME.md`.
**Verbal only / not on PDF:** Cluster Recommendation Copilot · Hindsight · 8.5%/14 tools/63/8/12B.

<div class="callout warn">
<b>Never break these.</b> 300-case / ≥80% is a <b>CI promotion gate</b> — not “all tenants live.”
Ask Iris is <b>Shipped</b> on the PDF as a capability — do not invent tenant-wide SLAs.
10k peak RPS / 2.11B / 2.4B / $100 token / 1.6M article-seasons / 335K+ products are <b>on the PDF</b> (source: AssortSmart tab / PDF).
Cluster Recommendation Copilot / Hindsight are <b>verbal only / not on PDF</b>.
Menu <b>98% is offline eval</b>. Uber work was <b>via EPAM</b>. ANZ 99.9% is <b>HISTORICAL Mobility</b>.
Do not invent Spark / Pinot / Kubernetes-operations / CDC ownership. Packet Kafka/Flink belongs on <b>Menu</b>, not IA.
</div>


**Stack:** Python, FastAPI, LangGraph agent plane · **Go / Gin** platform APIs.

Keep/Drop pipeline: [`../docs/assort_kd_flow/PIPELINE.md`](../docs/assort_kd_flow/PIPELINE.md).

---

## 0. What to lead with (60s)

Platform: Go/Gin **10k peak RPS**, Wire, h2c, Datadog; CH **189s→12s** on **250M**, **1.6M** article-seasons, **2.4B** weekly rollups; ifNotFinite KPI parser; Firebase/JWT/OIDC + Redis + Postgres roles; **100%** / **1200+** Go tests / golangci-lint / SAST/SBOM.

Agentic: Keep/Drop + Missed Opportunities + Top Style, **335K+**, **88k**/pass under **$100**, **7** lenses; **2.11B** fact air-gap + RMT two-phase; registry/breakers/checkpoints/LangSmith; **shipped Ask Iris**; **300-case** / **≥80%** CI gate vs **74%** baseline.

---

## 1. Platform Engineering & Infrastructure

### 10k RPS / Wire / h2c / Datadog
Self-protecting edge (no reverse proxy). Nested timeouts, body cap, SIGTERM drain. **Tag:** PDF / AssortSmart tab. Do not invent uptime %.

### ClickHouse 189s→12s, 1.6M, 2.4B
MEASURED POC at 250M (PDF rounds 12.3s to 12s). Hardware was unfair to CH (Docker 3.3GB vs PG 48GB host) and CH still won the heavy grid. Verbal: DISTINCT caveat ~2–3× vs ~13–15×. Catalog numbers 1.6M / 2.4B are **on the PDF**.

### ifNotFinite parser
Operator-authored KPI math compiled to safe CH fragments so merch logic is not a release train.

### Auth waterfall
Redis-fronted Firebase Admin → JWT / Google OIDC; constant-time API keys; Postgres roles; UAM hierarchy. Cache miss ≠ fail-open.

### CI
100.0% statement coverage gate (race + atomic), 1,200+ Go tests, golangci-lint, SAST/SBOM. Own 99.93% profile if asked.

---

## 2. Agentic Flows & Orchestration

### Three pipelines, not one chatbot
Keep/Drop, Missed Opportunities, Top Style over 335K+ products. 88k items/pass under $100 token spend. 7 AI lenses + deterministic KPI math.

### Air-gap + ReplacingMergeTree
LLM sees JSON, never issues CH writes. Two-phase inserts on RMT. Fallback to deterministic scores. **2.11B-row fact is on the PDF.**

### Registry
Circuit breakers, durable checkpoints, LangSmith + per-run JSON (tokens, duration, fallbacks).

### Ask Iris
PDF says **Shipped**. WebSocket copilot; LangGraph Supervisor router + Evaluator loop; socket-level frozen scopes. Defend as shipped **capability**. No tenant-wide SLA, QPS, or “every planner uses it daily” unless you have that metric (you do not on the PDF).

### Eval
300-case offline harness. ≥80% is a **CI promotion gate**. 74% deterministic baseline is the free rule the LLM must beat. Do not imply production GA at 80%.

---

## 3. CH vs PG vs Snowflake (packet, PDF-honest)

| Store | Use | Why not the other |
|---|---|---|
| Postgres | Roles, tenant, OLTP cell edits | Row-store dies on multi-column planner pivots (189s at 250M) |
| ClickHouse | Pivots, rollups, 2.11B fact | Weak at keyed UPDATE; use insert-only / RMT |
| Snowflake / shared BQ | Warehouse truth | Slot variance 1–20s+; cost for interactive UI |

You did **not** author `pg2ch_cdc` (Ashvin Sharma). Dual-write/CDC talk = DESIGN / verbal.

---

## 4. Architecture ASCII

See `23a_ia_interview_pack.md` §2 and `campaign_extras/interview_prep/architecture/01_ia_assortsmart_hindsight.md`.

Kafka backpressure / Flink credit-based flow control: defend on **Uber Menu**, not IA.

Datadog JSON logging: tenant_id + trace_id + service; do not claim dd.trace_id injection unless true.

---

## 5. Verbal only — Cluster Recommendation Copilot (was prior PDF bullet)

> Building the Cluster Recommendation Copilot for AssortSmart — LangGraph agent, 14 audited tools, deterministic clustering engine, human gates. Targets: under 1 hour (from days), ≥20 configs (from 1), failures under 2% (from measured 8.5% = 37/437). **Not on the current PDF.** Phase 1 design PASS; load test pending. FastAPI/LangGraph chat; Go doing layer for Hindsight / Clustering / Strategy.

If they drill Copilot, use the old Q&A in `campaign_extras/interview_prep/projects/01_ia_deep_dive.md` (bannered verbal-only).

## 6. Verbal only — Hindsight

Prior-season decision layer (carry-forward, Keep/Shop/Drop narration, no-code catalogs). **Not on PDF.** `01b_hindsight_defense.md`.

---

## 7. Senior Q&A (PDF)

**Q: Walk AssortSmart.**
Two chapters: platform Go/Gin 10k RPS + CH 15.5x, then agentic Keep/Drop / Ask Iris / eval gate. Write plane Go; agent plane Python.

**Q: Millions of rows?**
2.11B fact, 2.4B weekly rollups, 250M pivot POC — all PDF. Masters 1M+/day is a different product.

**Q: Is the agent in production?**
Ask Iris is shipped as a capability. ≥80% is how we refuse a bad config. I will not say every tenant is on the promoted agent.

**Q: Spark on IA?**
No. Spark is not on any of these PDFs. Menu is Kafka+Flink.
