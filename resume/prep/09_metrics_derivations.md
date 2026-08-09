# Metrics Derivations (estimated vs documented)

Every TPS / RPS / from→to number on the resume. Interview line: say **"estimated, derived from X"** for ESTIMATED rows and **"documented / measured"** for DOCUMENTED rows. Do not invent finer precision than this table.

| Tag | Meaning |
|---|---|
| **DOCUMENTED** | Already in prep / resume source material before this pass |
| **ESTIMATED** | Derived from a documented volume; mark as estimate in interviews |

---

## 1. Impact Analytics — AssortSmart

| Claim on resume | Tag | Derivation / source |
|---|---|---|
| Days → under 1 hour turnaround | DOCUMENTED (design target) | FRD / playbook design target — say "targeting", not measured live |
| ~100 candidate clusterings → top 3 | DOCUMENTED | Agentic design (silhouette-scored batch) |
| Bulk-save APIs **~10–20 peak RPS** | ESTIMATED | Internal planner SaaS: tens of concurrent planners, not consumer internet scale. Peak ≈ concurrent edit sessions × a few saves/min → ~10–20 RPS. Do **not** claim thousands of RPS. |
| ClickHouse **~5–10K row writes/sec** | ESTIMATED | Derived from 250M-row PoC load + bulk plan-edit batches (partition swaps / insert batches). Sustained *row write* throughput under load tests / PoC shape — not a live multi-tenant SLA yet. |
| p95 < 500 ms reads / < 80 ms cell edits | DOCUMENTED (design target) | Playbook grid targets (bullet may be commented on resume) |

**Rapid fire:** *"How did you get 10–20 RPS?"* — Internal planning tool, not public API. Concurrent planners × save frequency, not load-test peak of a public edge.

---

## 2. Uber FRM Scoping

| Claim on resume | Tag | Derivation / source |
|---|---|---|
| **70%** cycle-time cut (**~2 weeks → ~3–4 days**) | ESTIMATED baseline | 70% DOCUMENTED as outcome claim. From→to ESTIMATED from a ~10-business-day quarterly close workflow → ~3–4 days after platform. Say "about two weeks of analyst calendar time down to three-to-four days." |
| 36 REST endpoints / 8 screens | DOCUMENTED | Resume / FRM prep |
| Endpoint **p95 < 300 ms** | ESTIMATED | Internal quarterly tool, low concurrency. Latency framing for API quality — not a public RPS claim. Do **not** invent RPS for FRM (traffic is sparse). |
| 19M → 300K rows quarterly ETL | DOCUMENTED | Resume / FRM prep |
| 100% changed-module coverage | DOCUMENTED | Resume |

**Rapid fire:** *"Why no RPS on FRM?"* — Quarterly internal finance tool; claiming thousands of RPS would be dishonest. Defend schema, ETL compaction, and endpoint latency instead.

---

## 3. Uber Menu Ingestion (Kafka / Flink / Spark / Pinot)

| Claim on resume | Tag | Derivation / source |
|---|---|---|
| 30,000+ menus/month · 24h → 2h · $600K+/yr | DOCUMENTED | Menu prep |
| Kafka **~200–500 peak events/sec** | ESTIMATED | 30K menus/mo ≈ 1K menus/day. Item-level scrape/retry events (items + retries + health) amplify menu count; burst windows during fleet runs → hundreds of events/sec peak. Steady-state much lower. |
| Flink processes at that peak | ESTIMATED | Same event rate; keyed dedup / validate / route keeps up with Kafka lag target near zero in steady state |
| Spark nightly / backfill **~1–2M item rows** | ESTIMATED | ~1K menus/day × tens–hundreds of items + 90-day reprocess windows → order of 1–2M rows for a typical backfill batch |
| Pinot **sub-second** health queries | ESTIMATED (ops target) | Uber Pinot paved-road expectation for filter+groupBy dashboards; time-to-detect hours → minutes is DOCUMENTED intent |
| **+95%** successful ingestions (**~60–65% → 95%+**) | ESTIMATED baseline | +95% DOCUMENTED. From→to ESTIMATED: pre-anti-bot success in the low-to-mid 60s → mid-90s after IP rotation / proxy pools |
| 98% extraction fidelity | DOCUMENTED (offline/eval) | Say "offline evaluation / SFT eval", not live measured forever |

**Why each streaming piece (with numbers):** see § below and `projects/03_uber_menu_ingestion.md`.

**Rapid fire:** *"How did you get 200–500 events/sec?"* — Menus/day × items × scrape retries, peaked during fleet runs — order-of-magnitude estimate, not a Grafana screenshot.

---

## 4. Masters India GST

| Claim on resume | Tag | Derivation / source |
|---|---|---|
| p95 **1.2s → 300ms** | DOCUMENTED | Resume / GST prep |
| 100K+ txn/import · **1M+ daily** | DOCUMENTED | Resume |
| **~12 TPS avg, 100+ TPS peak** | ESTIMATED | 1M txn/day ÷ 86,400 ≈ **11.6 TPS** average. Filing-deadline peaks (GSTR windows) assumed ~8–10× average → **~100+ TPS** peak on the write path |
| Triage **70%** (**~30 min → <10 min**) | ESTIMATED baseline | 70% DOCUMENTED with ELK/New Relic. From→to ESTIMATED from ~half-hour mean triage to under 10 minutes with centralized logs + alerts |
| Coverage **35% → 82%** | DOCUMENTED | Resume |

**Rapid fire:** *"How 100 TPS?"* — 1M/day is ~12 TPS flat; peaks are filing deadlines when many clients push invoices — order-of-magnitude 8–10×, not a precise load-test number.

---

## 5. GeeksforGeeks

| Claim on resume | Tag | Derivation / source |
|---|---|---|
| **100,000+ daily queries** | DOCUMENTED | Resume |
| **~1–2 RPS avg, ~10× contest spikes** | ESTIMATED | 100K/day ÷ 86,400 ≈ **1.16 RPS** average. Contests / viral posts → short spikes ~10× → ~10–20 RPS |
| Premium **+15–20%** (relative lift) | DOCUMENTED as relative | No absolute baseline (before ARR or sub count) in prep — always say **relative lift**, not "from X% to Y%" |

**Rapid fire:** *"What's the RPS?"* — Convert daily queries to average RPS; call out contest spikes separately.

---

## 6. Uber Menu — streaming "why" with numbers (study card)

| Component | Why required | Number to say |
|---|---|---|
| **Kafka** | Scrapers are bursty/flaky; need replay, per-vendor key order, backpressure isolation | Peak **~200–500 events/sec** into topics; consumer lag = health |
| **Flink** | Per-event dedup + event-time LWW on out-of-order retries; exactly-once state via checkpoints | Same peak rate; keyed state by vendor+content hash |
| **Spark** | Backfills / parser upgrades must not starve the real-time path | Batch windows **~1–2M item rows**; nightly or on-demand |
| **Pinot** | Ops need minutes-not-hours detection of parse/scrape failures | Sub-second filter/groupBy; ingest from Kafka health topic |

Full prose defense: `projects/03_uber_menu_ingestion.md` §3–4 and `06_tech_deep_dives.md` §§3–6.
