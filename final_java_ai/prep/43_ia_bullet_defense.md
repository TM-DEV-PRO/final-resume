# IA bullet defense — Agentic + Core (PDF Sep 2026)

**PDF:** `Tarun_Mittal_SSE_5yr_Java_AI.pdf` · Canonical: [`docs/ASSORTSMART_TAB_RESUME.md`](../../docs/ASSORTSMART_TAB_RESUME.md)

This is the interview sheet for **every current IA PDF line**. Answers use your AssortSmart work. They do **not** import Kafka, Flink, CDC, Kubernetes ops, Milvus, sub-second ClickHouse, or a 70% document-RAG pipeline onto IA.

<div class="callout warn">
<b>Split these numbers.</b> 348k article-seasons = scored Keep/Drop volume on the PDF. 1.6M = catalog (verbal). $100/pass is off PDF. 300-case / 80% = CI gate. 73% cheaper at 100% coverage = gold-200 Luna vs mini, n=200. 74% = production det threshold on that bench. 55 GB / 16 GB / one fiscal week = verbal OOM knobs; PDF says temporal chunks + memory/spill caps. Partition rollback = DROP PARTITION then recopy; not a live reader swap. 4.09B copy was in flight. Gate ≠ all tenants live. Ask Iris = shipped capability, no SLA.
</div>

---

# SECTION 1 — Agentic Flows & Orchestration

## A1 — Multi-pipeline engine · 348k · 88k/pass · 7 lenses

**PDF:** Architected a multi-pipeline AI merchandise decision engine (Keep/Drop, Missed Opportunities, Top Style) evaluating **348k article-seasons**. Optimized inference at scale—processing **88k items per pass**—by blending deterministic KPI math with structured LLM invokes across **7 AI lenses**.

**What:** Distributed batch scoring across three named pipelines. Deterministic Python owns KPI math. The LLM sees packed JSON and returns structured lens scores.

**Why:** LLMs are bad at arithmetic. Hardcoded KPI math stays financially correct; lenses do qualitative pattern work.

**Decisions:** Separate det layer from prompt payloads; strict JSON schemas; 88k batch cap for memory and provider rate limits.

**Q: Why not let the LLM calculate KPIs via Python tools?**
A: Security, speed, determinism. A scoring agent with a code or SQL tool at 88k items is a latency and injection surface. We pre-compute KPIs and pass JSON. Math accuracy does not depend on the model.

**Q: How did you handle rate limits at 88k?**
A: Parallel article batches, hard per-batch timeouts, backoff, and a circuit breaker in the orchestration registry. A throttle does not wipe the run; checkpoints resume the LLM phase without recomputing det.

**Do not say:** 348k = 1.6M catalog. $100 is on this PDF (it is off). One giant chatbot.

---

## A2 — JSON payloads · ReplacingMergeTree · timeout fallback

**PDF:** Decoupled AI inference from a **2.11B-row** ClickHouse master by asynchronously serving context via JSON payloads rather than direct database querying. Engineered an eventually consistent write pattern via `ReplacingMergeTree` that guaranteed system availability by gracefully falling back to deterministic baselines during LLM timeouts.

**What:** Scoring LLMs do not query the 2.11B master. Context is packed JSON. Writes go through engine `insert` onto ReplacingMergeTree. Timeout → det score, run continues.

**Why:** Direct SQL from an LLM against a production analytical table is runaway queries, pool exhaustion, and prompt-injection risk.

**Decisions:** No DB tool on the scoring path (`db_safety.md`). Async batch mapper. RMT version column so retries do not duplicate articles. Keep/Drop default still CSV-first; CH publish is a separate ops step.

**Q: Why ReplacingMergeTree instead of MergeTree?**
A: Retries and overlapping waves can land twice. RMT keeps the latest version per key in the background. We read with `argMax` / `LIMIT 1 BY`, not `OPTIMIZE FINAL` as a runtime requirement.

**Q: What happens on LLM timeout?**
A: Hard timeout on the in-flight batch. Exception → mark fallback → write the precomputed deterministic score. The pipeline does not block the rest of the 88k on one vendor 504.

**Do not say:** “Physical air-gap” as the PDF phrase (old wording). “Zero corruption” as a 2PC guarantee. LLM issues CH writes. You authored CDC.

**If they say “so the LLM still queries CH, just async?”** Correct them: async is the batch executor. The model never gets a SQL tool. JSON in, engine writes out.

---

## A3 — Registry · timeouts · breakers · checkpoints · config_hash

**PDF:** Engineered a **shared orchestration registry** to guarantee **88k-article** batch runs survive provider failures by implementing hard timeouts, circuit breakers, and durable checkpoints that bypass redundant deterministic scoring. Ensured full observability by stamping every output row with a frozen config hash and custom JSON telemetry tracking tokens, USD cost, step duration, and batch fallbacks.

**What:** One harness across Keep/Drop, Missed Opp, Top Style: freeze config, claim ledger, timed LLM batches, circuit, resume files, telemetry JSON.

**Why:** Provider 502/504 midway through 88k must not force a full det recompute.

**Decisions:** `--resume` checkpoints (`det.json`, `agent_progress.json`). Circuit trips after consecutive / fail-fraction thresholds (default ~5). `config_hash` is SHA-256 of frozen guardrails + params + prompts + catalog.

**Q: How do checkpoints work?**
A: Det results land first. As LLM chunks complete we append per-article progress. Restart reloads det, skips finished articles, continues the LLM map. That is “bypass redundant deterministic scoring.”

**Q: Why not Airflow / Temporal?**
A: This workload needed application-native resume tightly coupled to CH inserts, config hashing, and per-run token/USD JSON. A heavy external orchestrator was extra infra for a batch CLI + HTTP start path we already owned.

**Do not say:** HITL validation queues (not in this repo). LangSmith on this bullet (LangSmith is Ask Iris on this PDF). Netflix Hystrix as the product.

---

## A4 — Ask Iris · JWT WebSocket · 3-attempt evaluator · frozen handshake

**PDF:** Shipped “Ask Iris,” a JWT-secured WebSocket copilot enabling planners to interactively query KPIs and inspect AI decisions on a multi-billion-row database. Prevented infinite LLM loops and multi-tenant data leaks by orchestrating a **LangGraph** supervisor with a **3-attempt** evaluator loop, utilizing **LangSmith** for observability, and strictly freezing hierarchy access on the initial socket handshake.

**What:** FastAPI WebSocket chat. JWT on handshake (`Authorization: Bearer` or `?token=`). `plan_scope` frozen once. Supervisor routes workers; evaluator retries up to `MAX_ATTEMPTS = 3`; LangSmith traces.

**Why:** Chat is a tenant-bleed and token-loop surface if scope can change mid-session.

**Q: How do you prevent multi-tenant leaks?**
A: Tenant / hierarchy / plan scope bind at JWT handshake. Tool calls inherit that frozen `plan_scope`. A later chat message cannot pivot into another tenant’s hierarchy.

**Q: How do you stop infinite LangGraph loops?**
A: Evaluator loop is capped at 3 attempts. Recursion limit on the supervisor graph. Fail closed with a graceful response rather than another tool hop.

**Do not say:** Tenant-wide SLA, questions/week, “generate dynamic charts” as a PDF claim (dropped). HITL review queue.

---

## A5 — 300-case proxy · 80% CI · 73% cost · 74% det · frozen weights

**PDF:** Built a **300-case** proxy evaluation harness and an **80%** accuracy CI gate to enforce strict deployment guardrails. Reduced live execution costs by **73%** at **100% coverage** by benchmarking models against a **74%** deterministic baseline, strategically freezing final decision weights when the LLM underperformed the baseline.

**Split (say this unprompted if they fuse the numbers):**

| Number | Source | Meaning |
|---|---|---|
| 300-case / 80% | `eval.json` `gold_min_accuracy: 0.8`, `cases.json` | CI **promotion gate** |
| 73% cheaper, 100% coverage | gold-200 bench, Luna vs `gpt-5.4-mini`, 200/200 complete | Model pick for live scoring |
| 74% | production det threshold 0.65 on that 200-set | Free rule the LLM must beat |
| Frozen blend weights | same bench: blended LLM ~63% < det 74% | Do not retune 0.4/0.6 from a small proxy |

**Q: What did you do when the LLM scored below det?**
A: Held blend weights frozen. We do not ship a “smarter” model that loses to a free rule on the proxy set. Promotion still requires the 80% CI gate on the 300-case file.

**Q: How did you choose Luna?**
A: Gold-200: Luna 200/200 complete, 73% cheaper than mini, 100% lens coverage. Nano was slightly cheaper but returned pending rows. Completion reliability won. **Do not** say the 300-case suite measured 73%.

**Do not say:** All tenants live at 80%. gpt-5.6-luna is printed on the PDF (it is not). 73% came from the 300-case file.

---

# SECTION 2 — Core Infrastructure & Pipeline

## C1 — Go/Gin 10k peak RPS · Wire · h2c · Datadog

**PDF:** Architected a multi-tenant **Go/Gin** platform scaling to **10k peak RPS**, utilizing **Google Wire** for compile-time DI. Deployed as a self-protecting HTTP edge without a reverse proxy, guaranteeing high availability through native **h2c**, nested timeouts, and **Datadog** distributed tracing.

**Q: Why Wire over Fx / Dig?**
A: Compile-time. Wire generates Go. Wiring errors fail the build, not a request path. Zero reflection at runtime.

**Q: Why no reverse proxy?**
A: The process owns h2c, nested context timeouts, and traces. One less hop and one less ops surface. I do not invent a 99.9% SLA.

**Do not say:** Nginx/Envoy as the timeout story. K8s cluster operations.

---

## C2 — KPI configurator · tokenizer · division-by-zero

**PDF:** Eliminated deployment bottlenecks by architecting a dynamic KPI configurator and custom formula parser. Engineered a real-time compilation layer that tokenizes operator-authored math into parameterized ClickHouse SQL fragments with native division-by-zero protection, decoupling business logic from code releases.

**What actually ships:** Go tokenizer + parser, allowlisted functions, logical names mapped to physical columns, SELECT wrapped with `ifNotFinite(toFloat64(<expr>), 0)`.

**Q: SQL injection?**
A: We do not concatenate raw operator SQL. Tokens must parse; functions are allowlisted; identifiers resolve through the catalog. Unknown tokens fail closed.

**Q: Division by zero?**
A: Compilation wraps the expression in `ifNotFinite(..., 0)` so Inf/NaN never poison planner JSON. That is the “native division-by-zero protection” on the PDF.

**Do not say:** Operators can paste arbitrary SQL. Prepared-statement bind of free-form SQL if they press implementation — the guard is parse + allowlist + `ifNotFinite`, not a generic JDBC prepared statement.

---

## C3 — Isolation · OIDC waterfall · constant-time keys

**PDF:** Guaranteed strict multi-tenant data isolation and UAM-scoped hierarchy access control across PostgreSQL and ClickHouse. Redis-fronted Firebase Admin to JWT/Google OIDC waterfall, constant-time API keys, Postgres-backed role resolution.

**Q: Constant-time API keys?**
A: Normal `==` short-circuits. Timing leaks let an attacker probe the key. Constant-time compare keeps cost identical on mismatch.

**Q: Auth latency?**
A: Redis fronts verified tokens so we are not hitting Firebase/OIDC on every API. Miss falls through to Postgres — it does not degrade open.

**Do not say:** Encryption product. Privacy program. Milvus. Sub-millisecond as a published SLA unless they only want the cache-hit anecdote — keep it qualitative (“Redis-fronted”).

---

## C4 — 15.5× · 170GB OOM · temporal chunks · spill caps

**PDF:** Reduced planner pivot latency by **15.5×** (**189s to 12s** on **250M-row** operations) by building a ClickHouse pre-aggregation layer for season and weekly rollups. Prevented **170GB** OOM crashes by slicing batch inserts into temporal chunks and enforcing strict distributed memory and disk-spill caps.

**Split:** 15.5× is **request-time** pivot on 250M. 170GB is **write-time** whole-season weekly `GROUP BY`. They are not cause and effect.

**Verbal knobs (off PDF, true):** unit of work = one fiscal week; **55 GB** memory cap; **16 GB** spill; attr week >40 GB; product week ~11 GB.

**Q: Why did it OOM?**
A: ClickHouse holds aggregation state in RAM. A whole-season weekly GROUP BY pushed ~170 GB. We sliced to one fiscal week and enabled external GROUP BY spill.

**Q: Rollup shape?**
A: Six MergeTree tables, `PARTITION BY season_code`: product/store/attr × season and weekly. Planners read rollups, not raw daily facts.

**Do not say:** Sub-second pivots. OOM fix caused 15.5×. 4.09B is this bullet.

---

## C5 — Go native-TLS pump · ~344k rows/s · 4.09B · TSV · partition rollbacks

**PDF:** Migrated ClickHouse rollups across Cloud clusters at **~344k rows/s** by writing a custom Go native-TLS data pump to bypass strict cross-cluster IP allowlist restrictions. Processed partitions up to **4.09B** rows using **500k-row** double-buffered batches, and eliminated partial-commit ghost rows using TSV ledgers and atomic partition rollbacks.

**Q: Why not `remoteSecure` / distributed tables?**
A: Cross-cluster IP allowlists blocked it. A laptop Go pump on native TLS (9440) was the workaround. PDF says allowlist, not the protocol name.

**Q: Ghost rows / TSV / rollback?**
A: A failed INSERT can still commit blocks. `count() > 0` is a lie. Loader TSV stamps successful chunks. Copier uses `.done` files per table. Restart issues `DROP PARTITION` for that season and recopies. That is the PDF “atomic partition rollback.” It is **not** an atomic swap with live readers.

**Q: 344k — is that HTTP RPS?**
A: No. Combined native-protocol ingest of two season streams (~150–190k each), 500k columnar batches, double-buffer (read next while `Send()` previous). Not REST.

**Do not say:** Finished 4.09B cutover. 344k TPS. Open-sourced the copier. TSV is the copier ledger.

Full whiteboard: [`42_clickhouse_rollup_migration.md`](42_clickhouse_rollup_migration.md).

---

# SECTION 3 — Screening answers that match this PDF

Use these instead of generic L5 drafts that put Kafka/Flink/CDC/K8s/Milvus on AssortSmart.

## Why should we hire you? (L5)

You should hire me because I own systems through design, failure, and measurement — classical backends and production AI.

At Uber via EPAM I owned FRM scoping (36 Spring Boot endpoints, 19M GL rows, L1–L4, SHA-256 keys) and cut recon 70% from 14 days to 3 against $340M, leading 3 engineers. On Uber Eats I owned menu ingestion — Selenium, Kafka, Flink, exactly-once catalog upserts — 24 hours to 2, $600K/yr, plus Gemini/Milvus RAG at 98% offline fidelity.

At Impact Analytics I own AssortSmart in two PDF chapters. Agentic: Keep/Drop + Missed Opp + Top Style on 348k article-seasons, 88k/pass, 7 lenses, JSON payloads off a 2.11B ClickHouse master, Ask Iris as a JWT WebSocket with a 3-attempt LangGraph evaluator, 300-case / 80% CI gate, 73% cheaper model at 100% coverage vs a 74% det baseline with frozen weights. Core: Go/Gin 10k peak RPS, KPI tokenizer with `ifNotFinite`, 15.5× pivots (189s to 12s on 250M), 170GB OOM fixed by temporal chunks and spill caps, Go native-TLS pump ~344k rows/s on partitions up to 4.09B.

If you need someone who can independently design, debug, and refuse a bad agent with a gate, that is the work I already do.

**Do not** say Kubernetes as IA production, Kafka on IA, or “sub-second ClickHouse.”

## Production bug you resolved (use the 170GB OOM)

**Context:** Weekly ClickHouse rollups for planner pivots.

**Crisis:** Whole-season weekly `INSERT SELECT` built ~170 GB aggregator state and hit `MEMORY_LIMIT_EXCEEDED` (failed even at 80 GB and 200 GB caps).

**Investigation:** Profiled grain. Product week ~11 GB. Attr week >40 GB. The atomic unit was too big.

**Fix:** One fiscal week per INSERT, 55 GB cap, 16 GB spill, bounded in-flight weeks.

**Prevention:** Spill settings in generated SQL; do not GROUP BY a whole season for weekly grain.

**Alternate (Masters, people/process):** IRP timeout canary — too-aggressive timeouts on government calls; moved async + idempotency. Do **not** lead with a FastAPI/Kafka heap-leak packet story as if it were an IA PDF bullet.

## Complex system you developed (AssortSmart, not CDC)

**Problem:** Planner pivots on PostgreSQL were too slow (250M harness ~189s). Agents could not be allowed to SQL a 2.11B fact table.

**Architecture:** Go/Gin edge (Wire, h2c, Datadog) → Postgres UAM + Redis-fronted OIDC → ClickHouse six rollup tables for reads → Python batch agents on JSON payloads → Ask Iris WebSocket with frozen plan scope.

**Hard part:** Weekly grain OOM + cluster copy blocked by allowlists. Temporal INSERT chunks + Go native-TLS pump, not Kafka CDC.

**Result:** 15.5× on 250M; Keep/Drop 348k article-seasons; Ask Iris shipped; 80% CI gate.

**Do not** draw Kafka → Flink → ClickHouse for IA. That picture is **Uber Menu**.

## Agentic pipeline you owned (Keep/Drop + Ask Iris, not document RAG)

**Business:** Merchandise Keep/Drop / Missed Opp / Top Style.

**Stack:** Python batch + LangGraph Ask Iris. Not Milvus. Milvus is Menu.

**Loop:** Det KPI JSON → 7 structured lenses → blend → RMT insert or CSV bake. Failures: timeout → det fallback; circuit; checkpoint resume.

**Interactive path:** JWT WS → frozen hierarchy → supervisor → 3-attempt evaluator → LangSmith.

**Guardrails:** 300-case proxy, 80% CI, freeze weights if LLM loses to 74% det.

**Do not** tell a 70% invoice-extraction RAG story as this IA bullet. Menu RAG is a **different** PDF chapter.

---

# SECTION 4 — Do not import

| Draft idea | Verdict |
|---|---|
| IA architecture = Kafka + Flink + CDC + K8s | **No.** Menu owns Kafka/Flink. CDC author is Ashvin. K8s = skills literacy |
| Sub-second CH dashboards | **No.** PDF is 189s → 12s |
| HITL queues / human review of low-confidence scores | **No.** Offline evals replaced critic/evaluator agents |
| Open-source the copier | **No.** Whiteboard it |
| “I stream 4.09B at 344k” as a finished job | **No.** Measured in flight |
| 70% document extraction as AssortSmart | **No.** |
| FastAPI Kafka memory leak as the IA outage STAR | **No.** Use 170GB OOM or Masters IRP |
