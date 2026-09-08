> Canonical interviewer pack for `Tarun_Mittal_SSE_5yr_Java_AI.pdf` IA bullets (Agentic first, then Core). Project title: **AssortSmart — Senior Software Engineer (Platform & AI)**. Synced Sep 2026. Canonical: `docs/ASSORTSMART_TAB_RESUME.md`. Full Q&A: [`43_ia_bullet_defense.md`](43_ia_bullet_defense.md).

# Impact Analytics — Interview Pack

**Role:** Senior Software Engineer · Impact Analytics, Bangalore · May 2026 – Present (IC)
**Product:** AssortSmart — AI-powered retail merchandise planning
**Honesty:** 300-case / **80%** = **CI promotion gate** (not all tenants live). **73% / 100% coverage** = gold-200 Luna vs mini, **not** the 300-case file. Ask Iris = **shipped capability** (JWT WS, 3-attempt evaluator — no invented SLAs). On PDF: 10k RPS / 2.11B master / **348k article-seasons** / 88k/pass / six rollups / 170 GB OOM / ~344k rows/s / 4.09B. Off PDF: **$100/pass**, **1.6M** catalog, **55GB/16GB**, 100% Go coverage. Cluster Copilot / Hindsight = **verbal only**. No IA Kafka/Flink/K8s-ops.

Agent plane: **Python, FastAPI, LangGraph**. Platform APIs: **Go / Gin**.

---

## 1. 30s / 2min

### 30 seconds

AssortSmart has two PDF chapters. Agentic: Keep/Drop + Missed Opportunities + Top Style on **348k article-seasons**, **88k**/pass, **7** lenses; JSON payloads off a **2.11B-row** ClickHouse master with RMT timeout fallback; a shared registry with checkpoints; **shipped Ask Iris** (JWT WebSocket, LangGraph supervisor, **3-attempt** evaluator, handshake-frozen hierarchy); **300-case** proxy / **80%** CI gate, **73%** cheaper at **100%** coverage vs a **74%** det baseline with frozen weights. Core: Go/Gin **10k peak RPS** (Wire, h2c, Datadog), KPI tokenizer with division-by-zero protection, PG+CH isolation (Firebase/JWT/OIDC), ClickHouse **189s to 12s** on **250M**, **170 GB** OOM fixed with temporal chunks and spill caps, Go native TLS pump about **344k rows/s** on partitions up to **4.09B**.

### 2 minutes

**Agentic path:** registry starts Keep/Drop / Missed Opp / Top Style → det KPI math + 7 structured LLM lenses on JSON (**no SQL tool**) → RMT insert / timeout → det fallback → checkpoints / circuit / config_hash + JSON telemetry. Ask Iris: JWT handshake freezes hierarchy → Supervisor → 3-attempt Evaluator → LangSmith.

**Core path:** tenant request → Go/Gin (Wire) → Redis-fronted OIDC waterfall → UAM/Postgres roles → ClickHouse rollups (`ifNotFinite` KPI SQL) → Datadog traces. Weekly grain = temporal INSERT chunks after 170GB OOM. Cluster copy = native-TLS pump, partition rollback = DROP then recopy.

**Status:** 80% gate ≠ GA. Ask Iris is a shipped capability. 73% is the gold-200 model pick.

<details><summary>Verbal / not on PDF (Cluster Copilot · Hindsight)</summary>

Copilot: days → under 1h TARGET, 8.5% (37/437) MEASURED → under 2% TARGET, 14 tools, 3 gates, Phase 1 design PASS / load test pending. Hindsight: prior-season layer. 63/8 DDL and 12B→25M are interview depth, not PDF bullets.

</details>

---

## 2. Architecture (PDF-honest)

```
Planner UI / Ask Iris WS
        │
Go/Gin edge (Wire, h2c, 10k peak RPS, Datadog)
        │
 Redis   Postgres roles/UAM   ClickHouse 2.11B fact / six rollup tables / RMT
        │
Python agent plane — 7 lenses, 88k/pass, JSON payloads vs 2.11B master
Ask Iris — JWT WS, LangGraph supervisor, 3-attempt evaluator, handshake freeze
300-case / 80% CI gate · 73% cost (gold-200) · 74% det · frozen weights
```

Packet sketches that put Kafka→Flink or K8s-ops on IA are **overclaim**. Menu owns Kafka+Flink.

---

## 3. Design decisions (PDF-first)

| Decision | Why | Tradeoff |
|---|---|---|
| Go edge, no reverse proxy | 10k RPS with h2c, nested timeouts, Wire | You own caps/SIGTERM |
| CH vs PG vs Snowflake | Columnar pivots; BQ 1–20s+ variance; Snowflake cost/latency for this UI | CH ≠ keyed UPDATE OLTP |
| JSON payloads vs 2.11B master | Hallucinated SQL must not write | Extra hop; timeout → det fallback |
| Supervisor + 3-attempt evaluator | Stop infinite loops + tenant bleed | Framework surface |
| 80% gate vs 74% baseline; freeze weights | Models must beat a free rule | Gate can fail the agent — that is success |
| Kafka/Flink | **Menu only** | Do not move them onto IA |

---

## 4. Bullet-by-bullet (PDF Sep 2026)

### C1 — Go/Gin 10k peak RPS, Wire, h2c, Datadog

| | |
|---|---|
| **Claim** | Multi-tenant Go/Gin platform scaling to 10k peak RPS; Wire; self-protecting HTTP edge; h2c; nested timeouts; Datadog tracing |
| **Tag** | PDF / AssortSmart tab |
| **Attack** | “Is 10k measured in Datadog? Where is the reverse proxy?” |
| **Reply** | “It is a PDF claim from the AssortSmart tab — peak RPS of the Go edge we deployed without a reverse proxy, so the process owns h2c, timeouts, and traces. I will not invent a 99.9% SLA or tenant count that is not on the resume.” |

### C2 — KPI tokenizer · division-by-zero

| | |
|---|---|
| **Claim** | Dynamic KPI configurator; tokenize operator math into parameterized CH SQL with native division-by-zero protection |
| **Tag** | PDF. Mechanism = allowlisted parser + `ifNotFinite` wrap |
| **Reply** | “KPI changes must not require a deploy. We tokenize, allowlist functions, map identifiers, and wrap with ifNotFinite so Inf/NaN never poison planner JSON.” |

### C3 — Firebase / JWT / OIDC + Redis + Postgres roles

| | |
|---|---|
| **Claim** | Multi-tenant **data isolation** + UAM **access control** across **PostgreSQL** and **ClickHouse**; Redis-fronted Firebase Admin → JWT/Google OIDC waterfall; constant-time API keys; Postgres roles |
| **Tag** | PDF |
| **Reply** | “Same tenant id on PG (identity/UAM) and CH (facts). Cache-miss falls through to Postgres — it does not degrade open. Constant-time compare on API keys. This is access control, not encryption and not a privacy program. Milvus is Menu RAG, not this bullet.” |

### C4 — 15.5× / 170GB OOM / temporal chunks

| | |
|---|---|
| **Claim** | Reduced planner pivot latency by 15.5× (189s to 12s on 250M-row operations) via season/weekly rollups. Prevented 170GB OOM by slicing inserts into temporal chunks and enforcing memory and disk-spill caps. |
| **Tag** | PDF. 189s to 12s MEASURED POC. 170GB write-time. **55GB / 16GB / one fiscal week** are verbal knobs. |
| **Attack** | “The OOM fix caused the 15.5×.” |
| **Reply** | “Pivot is request-time. OOM is write-time weekly GROUP BY. I sliced to one fiscal week so weekly grain could exist. Full Q&A: `42` and `43` C4.” |

### C5 — Go native-TLS pump / ~344k rows/s / 4.09B / partition rollbacks

| | |
|---|---|
| **Claim** | ~344k rows/s Go native-TLS pump; allowlist bypass; up to 4.09B; 500k double-buffer; TSV ledgers; atomic partition rollbacks |
| **Tag** | PDF. 344k = two season streams combined. Copy in flight. Rollback = DROP PARTITION then recopy. |
| **Attack** | “You finished 4.09B.” / “344k TPS.” / “TSV was the copier.” |
| **Reply** | “PDF says up to 4.09B. Attr weekly was in flight. TSV is the weekly loader. Copier uses `.done` files. Partition rollback is how we restart a season, not a live reader swap. `42`.” |

### A1 — 348k article-seasons · 88k/pass · 7 lenses

| | |
|---|---|
| **Claim** | Multi-pipeline engine; 348k article-seasons; 88k items/pass; 7 AI lenses + deterministic KPI math |
| **Tag** | PDF. $100/pass off PDF. 1.6M catalog is verbal. |
| **Reply** | “Three named pipelines, not a chatbot. 348k is scored article-seasons. Seven lenses typically fire per article.” |

### A2 — JSON payloads vs 2.11B master · RMT · timeout fallback

| | |
|---|---|
| **Claim** | Decoupled inference from 2.11B-row CH master via JSON payloads; RMT eventually consistent writes; det fallback on LLM timeouts |
| **Tag** | PDF |
| **Reply** | “The model has no SQL tool. JSON in, engine insert out. Timeout substitutes the det score so the 88k run does not stall. I did not author pg2ch_cdc.” |

### A3 — Registry · checkpoints skip det · config_hash

| | |
|---|---|
| **Claim** | Shared registry; 88k survive provider failure; hard timeouts, breakers, durable checkpoints that bypass redundant det; config_hash; JSON telemetry (tokens, USD, duration, fallbacks) |
| **Tag** | PDF |
| **Reply** | “Resume reloads det.json and continues LLM progress. Breakers are run-level. config_hash is the frozen SHA of prompts/params/catalog.” |

### A4 — Ask Iris JWT · 3-attempt evaluator · handshake freeze

| | |
|---|---|
| **Claim** | Shipped Ask Iris; JWT WebSocket; LangGraph supervisor; 3-attempt evaluator; LangSmith; freeze hierarchy on handshake |
| **Tag** | PDF **shipped capability** |
| **Reply** | “Scope binds at JWT handshake. Evaluator caps at 3. I will not invent questions/week or a tenant-wide SLA.” |

### A5 — 300-case / 80% / 73% / 74% / frozen weights

| | |
|---|---|
| **Claim** | 300-case proxy harness; 80% CI gate; 73% live cost cut at 100% coverage; 74% det baseline; freeze final decision weights if LLM underperforms |
| **Tag** | 80% = promotion gate. 73%/100% = gold-200 Luna vs mini |
| **Reply** | “I split the files. 300-case is CI. 73% cheaper at 200/200 complete is the model pick. Det was 74% on that bench so we froze blend weights.” |

### Verbal — Cluster Copilot / Hindsight (**not on PDF**)

Use only if asked. Do not volunteer as resume bullets. Deep dive: `01b_hindsight_defense.md`, `10` verbal section.

---

## 5. Mock Q&A (new PDF)

**Shipped vs gated?** Ask Iris is a shipped capability. 80% is a promotion gate. AssortSmart SaaS is live; I do not claim every tenant runs every agent config.

**Why not Snowflake?** Interactive planner UI + cost; CH columnar vs PG row-store; BQ slot variance 1–20s+.

**Why JSON payloads instead of LLM SQL?** A 2.11B-row master cannot take hallucinated queries. Async batching is throughput; no-SQL-tool is the isolation invariant.

**Debug agent vs Go?** LangSmith for graph/tokens; Datadog for HTTP/CH; JSON logs with tenant_id + trace_id. Packet 4-step: isolate → traces → saturation → mitigate.

**K8s/CDC/Flink on IA?** Not PDF. Flink is Menu. CDC author is Ashvin Sharma. K8s = skills literacy, not cluster ops.

## 6. Do NOT say

- All tenants live at 80%
- 73% measured on the 300-case file
- HITL queues / Kafka-Flink-CDC on IA
- Extra IA TPS beyond PDF 10k peak RPS
- Spark / Pinot / K8s-ops / Terraform / Flink-on-IA / MCP-on-PDF
- Cluster Copilot / Hindsight as PDF bullets
- Tenant-wide Ask Iris SLA
- “I built pg2ch_cdc”
