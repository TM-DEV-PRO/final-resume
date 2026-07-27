# Table schemas · database design · API contracts (all resume projects)

Column-level schemas and API surfaces you can whiteboard. Complements [`34_er_tables_tech_why.md`](34_er_tables_tech_why.md) (ER / why-tech) and deep dives.

| Project | Schema truth | API truth |
|---|---|---|
| **IA AssortSmart** | MEASURED design — CH DDL Phase-1 (`DDL.sql` / Confluence) | DESIGN — MCP tools + Go write path (load test pending) |
| **Uber FRM** | MEASURED code — 11 SQLAlchemy models | MEASURED code — 32 routes under `/frm-scoping` |
| **Uber Menu** | LOGICAL / HISTORICAL shapes (no public DDL in repo) | LOGICAL event + upsert contracts |
| **Masters India** | LOGICAL / HISTORICAL (compliance SaaS narrative) | LOGICAL REST + async IRP |
| **GFG** | LOGICAL / HISTORICAL | LOGICAL REST |

**Honesty:** omit IA **624 columns**. No invented IA TPS. FRM = say **11 models in scoping service**, **30+** APIs. Menu = **Milvus** (not Pinecone). Copilot = **building**.

---

## How to answer

1. Name the **store** (MySQL / CH / Kafka+catalog / PG+Mongo).  
2. Draw **2–3 tables** with PK + natural key + 5–8 critical columns.  
3. Sketch **3–5 endpoints** with method, path, query/body, response shape.  
4. Tag MEASURED / DESIGN / HISTORICAL / LOGICAL.

---

# 1. Impact Analytics — ClickHouse schemas + API surface

**Tenant DB example:** `cluster_briscoes` (one CH database per retailer).  
**Inventory:** 63 tables (incl. 7 stage twins) · 8 layers · 5 dictionaries · 19 views.  
**Writers:** SYNC (facts/cubes/mirrors) · API/JR/NIGHT (decision plane) · agent = `readonly=1` only.

### 1.1 Facts (P1 — MergeTree + stage twin + `REPLACE PARTITION`)

```sql
-- fact_sales  ENGINE = MergeTree
-- PARTITION BY toYYYYMM(date)
-- ORDER BY (l1_name, l2_name, l3_name, store_code, date)
date Date
fy_fw UInt32
channel / sub_channel LowCardinality(String)
store_code LowCardinality(String)
product_code / article / style String
color / size / season LowCardinality(String)
l0_name … l6_name LowCardinality(String)   -- hierarchy denormalized on fact
product_bucket_code, brand, product_type, …
is_clearance UInt8
revenue / qty / qty_returns / cost / margin / discount_amount / msrp / price / lost_units Float64
-- bloom indexes: style, article, product_code
-- twin: fact_sales_stage AS fact_sales
```

```sql
-- fact_inventory_wk  PARTITION BY toYYYYMM(week_start)
-- ORDER BY (l1_name, l2_name, l3_name, store_code, week_start)
week_start Date
fy_fw UInt32
channel, store_code, l1_name, l2_name, l3_name
product_code String
oh_units / oh_cost / receipts_qty / receipts_cost / receipts_msrp / lost_units Float64
stockout_flag UInt8
```

```sql
-- fact_forecast_wk  (future windows use forecast KPIs like actuals)
week_start, fy_fw, channel, store_code, l1/l2/l3
forecast_ver LowCardinality(String)
fc_revenue / fc_qty / fc_margin Float64
```

```sql
-- ingest_watermark  (append-only sync ledger — reproducibility anchor)
source_table LowCardinality(String)
partition_id String
last_modified DateTime64(3)
row_count UInt64
bytes_landed UInt64
load_id UUID
status Enum8('landed','verified','failed')
detail String
synced_at DateTime64(3)
-- views: v_watermark_latest (argMax), v_data_as_of
```

**Interview line:** “Facts restate by building a stage twin and `REPLACE PARTITION` — no row UPDATE on the hot path.”

### 1.2 Dims (P2 — ReplacingMergeTree)

```sql
-- dim_store  RMT(synced_at, is_deleted)  ORDER BY store_code
store_code, store_name, channel, sub_channel, region, store_type
active UInt8, open_date Date, close_date Nullable(Date)
is_deleted UInt8, synced_at DateTime

-- dim_hierarchy  RMT(synced_at, is_deleted)
hierarchy_code, level UInt8
l0_name … l6_name, path, is_leaf, is_custom, active
attribute_list String, search_text (+ ngram / aliases)

-- dim_fiscal, dim_sister_store, dim_channel  (same RMT pattern)
```

Dictionaries (5 + `dict_user` at bring-up): store / hierarchy / fiscal / channel / sister-store — `dictGet` for agent grounding.

### 1.3 Cubes / caches (planner rollups)

```sql
-- cube_store_attr_week / cube_store_kpi_week  (+ stage twins, P1 swap)
-- significance_cache / precomputed_candidates  RMT(computed_at)
-- feature_matrix_cache  MergeTree
```

Say purpose in interview; full column lists live in DDL § cubes — do not recite every column.

### 1.4 PG mirrors (transitional read models)

```sql
-- mirror_plan  ORDER BY plan_code
plan_code UInt32
plan_name, description String
step_x10 UInt8          -- NEVER Float32 (1.3 not binary-safe); 13 = step 1.3
is_deleted UInt8
selling_sdate / selling_edate Date
selling_periods JSON
channels Array(String)
hierarchy_level LowCardinality(String)
scope_filters JSON
scope_l1s / scope_l2s / scope_l3s Array(String)
scope_fingerprint FixedString(64)
scope_recoverable UInt8
member_cnt UInt32, cluster_cnt UInt16, adoption_cnt UInt32
created_via, created_at, updated_at, synced_at

-- mirror_plan_membership  ORDER BY (plan_code, channel, store_code)
plan_code, channel, store_code, cluster_code, display_name, synced_at

-- mirror_strategy_consumer  ORDER BY (cluster_plan_code, strategy_plan_id)
-- mirror_plan_line  (+ stage) planned_* / bought_* by week — outcome loop
```

View `v_doorway_eligible`: `step_x10 >= 13 AND is_deleted = 0 AND member_cnt > 0 AND scope_recoverable = 1`.

### 1.5 Decision plane (content-addressed config + event status)

```sql
-- cluster_config  RMT(created_at)  ORDER BY config_hash
config_hash FixedString(64)     -- content address; insert dedup token
doc JSON
scope_fingerprint FixedString(64)
entry_mode, created_by, created_at

-- cluster_run  (immutable HEADER — status NEVER here)
config_hash, data_watermark, run_id UUID, batch_id UUID, session_id UUID
plan_code UInt32 DEFAULT 0
scope_fingerprint, entry_mode, scorer_version, weights_version, seed
created_by, created_at, created_date
ORDER BY (config_hash, data_watermark, run_id)

-- cluster_run_event  (P3 append-only status)
run_id, event_seq UInt16, event_time DateTime64(6)
status Enum8('queued','claimed','running','scored','failed','timeout','superseded')
claim_token, error, actor, event_date
-- latest: v_run_status / v_run_status_recent via argMax(event_seq, event_time, claim_token)

-- cluster_run_membership  (typed store→label; shortlist policy)
run_id, config_hash, batch_id
axis Enum8('product','performance','store')
k UInt8, channel, store_code, label, label_ord, margin_to_next
pinned UInt8, shortlisted UInt8
```

**Lock-free claim:** runner INSERTs `claimed` + `claim_token`, reads `v_run_status*`, proceeds only if its token won argMax. Crash reclaim: append `superseded`, mint **new** `run_id`.

### 1.6 Approval + immutable snapshot + write-back

```sql
-- approval_event
run_id, event_seq, event_time
status Enum8('pending','approved','rejected')
approver, comment
snapshot_id FixedString(64)
writeback_plan_code UInt32
-- view: v_approval_state

-- Ordering contract: write plan_snapshot + snapshot_* FIRST, 'approved' event LAST

-- plan_snapshot  ORDER BY (plan_code, approved_at)  FOREVER
plan_code, approved_at, snapshot_id, run_id, config_hash
config_doc JSON, metric_vector JSON, pins_applied JSON
data_watermark, scorer_version, weights_version, approved_by

-- snapshot_cluster  ORDER BY (snapshot_id, channel, cluster_code)
-- cluster_code = trim(concat(channel, ' ', product_label, performance_label, ' ', store_label))

-- snapshot_membership  frozen store→cluster (+ per-axis labels)

-- writeback_staging / writeback_plan_shell / writeback_event  (transitional PG wire)
-- pending_intent + intent_event  (strategy_create, recluster_proposal, …)
```

**Gotcha to say:** `is_optimal` (engine on run metrics) ≠ `is_final` (human via approval/snapshot). Agent never writes these tables.

### 1.7 Thin PostgreSQL (identity / UAM)

Logical only in interview:

```
users(id, email, …)
tenant_membership(user_id, tenant_id, role)
workflow_state / feature_flags
-- CH dict_user syncs identity for audit labels; PG remains auth SoR
```

### 1.8 API / tool design (DESIGN — building)

**Plane split**

| Layer | Role | Mutates? |
|---|---|---|
| FastAPI + LangGraph + MCP | Chat, tool sequencing, evidence packs | No planning facts |
| **14 audited tools** (MCP) | Templated reads: grounding, significance, candidates, score, compare, pins/impact, … | SELECT / `dictGet` only |
| Go Gin doing layer | Clustering / Hindsight / Strategy product writes after gates | INSERT-only on owned CH + PG write-back SPs |
| Sync / NIGHT jobs | BQ→CH facts, cube rebuild, mirror refresh | Stage + partition swap / RMT inserts |

**Human gates:** grounding → search plan → approval → write-back.

**Tool categories (say these — do not invent 14 product names unless from FRD):**

1. Scope / hierarchy grounding  
2. Eligibility / doorway FitScore inputs  
3. Significance / candidate generation  
4. Feature matrix / k-search support reads  
5. Score / rank / compare configs  
6. Pin & edit-impact preview (read)  
7. Run/batch progress (`v_batch_progress`)  
8. Watermark / data-as-of disclosure  

**Go write API sketch (DESIGN shape):**

```
POST /v1/runs                    {config_hash|config_doc, plan_code?, session_id}
                                 → {run_id, batch_id, status: queued}
GET  /v1/runs/{run_id}           → header + v_run_status
POST /v1/batches/{id}/claim      → claim_token dance (worker)
POST /v1/approvals               {run_id, decision, comment}
                                 → snapshot_id (snapshot rows then approved event)
POST /v1/writeback               {snapshot_id, plan_code}  // after human gate
GET  /v1/plans/{plan_code}       → mirror + doorway eligibility
```

**Auth / tenancy:** tenant → CH database; agent DB user `readonly=1`; service roles INSERT-only; OTEL `trace_id` across LangSmith / Datadog / PostHog.

---

# 2. Uber FRM — MySQL schemas (MEASURED ORM) + REST

**Source:** `frm_scoping_service/database/models/*.py` + `handler/scoping_handler.py`.  
**Prefix:** `/frm-scoping`. **Auth:** `x-auth-params-email` → `updated_by`.  
**Period key on almost every row:** `fiscal_quarter` String(4) · `fiscal_year` String(8).  
**No DB foreign keys** — logical joins on `level_id` + period + active flags.

### 2.1 Shared audit columns

```
created_at TIMESTAMP
created_by String(36)   -- default "Scoping APP" on some tables
updated_at TIMESTAMP
updated_by String(36)
```

### 2.2 `level_mapping` — hierarchy spine

```
uuid PK String(36)          -- THIS is level_id on facts
level1…level4 String(256)
fiscal_quarter, fiscal_year
is_active String(16)
+ audit
```

### 2.3 `balance_sheet` / `income_statement` — FSLI facts

```
uuid PK String(36)
level_id String(36)         -- = level_mapping.uuid
hfm_amount DECIMAL(18,2)
percentage_of_total DECIMAL(5,2)
group_multiple DECIMAL(18,2)
hfm_amount_in_millions DECIMAL(18,2)
hfm_amount_previous_year DECIMAL(18,2)
quantitative_material / qualitative_material String(16)
conclusion_overall_significance / conclusion_scope String(64)
testing_strategy Text
component_selection String(256)
total_inscope DECIMAL(18,2)
total_inscope_percentage DECIMAL(5,2)
residual_balances / residual_multiples DECIMAL(18,2)
residual_percentage DECIMAL(5,2)
residual_balance_prev_year, residual_dollar_change, residual_percentage_change
group_dollar_change, group_percentage_change
greater_than_materiality / greater_than_threshold_change / investigate String(16)
level_1…level_4 String(256)   -- denormalized labels for UI tree
is_level_active String(16)
group_status / component_status / residual_status String(36)
  -- group_status allowlist: Draft | Review | ReOpen | Closed
fiscal_quarter, fiscal_year + audit
```

`income_statement` same shape (+ ORM helpers `fetch_for_period`, `update_scope_and_status`, …).

### 2.4 Recon v2 leaves

```
-- recon_balance_sheet / recon_income_statement
uuid PK, level_id
hfm_amount, hfm_amount_in_millions
financial_statement_amount_in_millions
difference                    -- HFM − filed (10-Q)
level_1…level_3
is_level_active
fiscal_quarter, fiscal_year + audit
```

### 2.5 Component, EMI, metrics, thresholds, Q&A

```
-- component_entity
uuid PK, level_id, scoping_component, amount DECIMAL(18,2)
is_active, fiscal_quarter, fiscal_year + audit

-- emi_data  (one row ≈ one UI column / investee)
uuid PK
investee, investee_entity, uber_investor_entity
period_acquired, security
uber_ownership_equity_interest_percentage
uber_ownership_interest_as_of_date
asset_balance, preliminary_income_loss_on_investments
asset_as_a_perc_of_total, income_loss_as_a_perc_of_total_emi_components
financial_reporting_framework, fiscal_year_end
audited_financial_statements_available, report_issuance_date
auditor, additional_considerations Text
significant_emi, auditboard_link_to_risk_assessment
is_active, fiscal_quarter, fiscal_year + audit
-- @validates strips whitespace on string columns

-- frm_metrics_table  (class ScopingMetrics)
uuid PK, metric_key String(128), metric_value String(512)
unit String(32), is_active
-- materiality key → e.g. $340M (MEASURED product number)

-- threshold_table_v2  (class ThresholdSetup)
uuid PK, legal_entity
total_assets / total_revenue DECIMAL(18,2)
total_assets_percentage / total_revenue_percentage DECIMAL(5,2)
financially_significant_component / significant_due_to_risk / inscope_due_to_coverage
conclusion / updated_conclusion / review_status
is_active, fiscal_quarter, fiscal_year + audit

-- scoping_questions
uuid PK   -- SHA-256(question_text + normalized page_name) → 32 hex
question_text Text, page_name String(36), is_active

-- scoping_assessments
uuid PK, question_id, line_id   -- line_id = fact uuid
answer_text Text
fiscal_quarter, fiscal_year + audit
```

### 2.6 API catalog (32 registrations; say **30+**)

Query period (most GETs): `fiscal_quarter=Q1|…|Q4` & `fiscal_year=YYYY`.

| Method | Path | Body / notes | Response idea |
|---|---|---|---|
| GET | `/health` | — | `{status, service}` |
| POST | `/scoping` | welcome echo | `DataResponse` |
| GET | `/recon_balance_sheet` | v1 Sheets | recon response |
| GET | `/v2/recon_balance_sheet` | **MySQL nested tree** (migration owned) | `ReconFetchResponse` |
| GET | `/v2/recon_income_statement` | same for IS | `ReconFetchResponse` |
| GET | `/recon_income_statement` | v1 | — |
| GET | `/group_balance_sheet` | nested from `balance_sheet` | tree |
| PATCH | `/group_balance_sheet/{uuid}` | `{conclusion_scope?, group_status?}` | dict |
| GET | `/group_income_statement` | — | tree |
| PATCH | `/group_income_statement/{uuid}` | same patch shape | dict |
| GET | `/bs_components` | optional `level_1…4` filters | `ComponentScopingResponse` |
| GET | `/is_components` | YTD annualization rules | same |
| GET | `/bs_component_filters` | cascading distinct labels | filter options |
| GET | `/is_component_filters` | same | — |
| GET | `/residual_risk` | `fsli_type=bs\|is`, optional `threshold_percentage` | residual analytics |
| GET | `/emi_scoping` | comparison view | — |
| GET | `/emi_data` | grid; active flag | `header_row` + `columns_data` |
| PATCH | `/emi_data/{uuid}` | partial column; not `investee` | patch response |
| POST | `/add_scoping_metrics` | metrics payload | — |
| GET | `/scoping_metrics` | optional period | list |
| PUT | `/update_benchmark_thresholds` | assets/revenue benchmarks → recompute significance | dict |
| GET/PUT | `/materiality` | `metric_key=materiality` | value + doc link |
| GET/PUT | `/active-page-number` | UI page state | dict |
| GET | `/threshold-setup` | active rows for period | list |
| PATCH | `/threshold-setup/{uuid}` | partial | dict |
| POST | `/scoping_questions/bulk` | `[{question_text, page_name, is_active}]` upsert | uuids in order |
| GET | `/scoping_questions` | `page_name` allowlisted | list |
| POST | `/scoping_assessments` | create | — |
| GET | `/scoping_assessments` | by `line_id` | joined questions |
| PATCH | `/scoping_assessments/{uuid}` | `{answer_text}`; may sync BS qualitative fields in same txn | dict |

**Idempotency talking points**

- GET/PATCH/PUT by uuid = set semantics.  
- Questions bulk: deterministic uuid → upsert.  
- `POST /add_scoping_metrics` is append/versioned by `is_active` (not strictly idempotent).

**Bug story (schema-linked):** join `balance_sheet` ⨝ `level_mapping` without `.label()` → duplicate `uuid` keys in `dict(zip(...))` → wrong PATCH target. Fix: SQLAlchemy 2.0 `select` + explicit labels (`fsli_id` vs `level_mapping_uuid`).

---

# 3. Uber Eats Menu — event / catalog / RAG schemas (LOGICAL)

No production DDL in this repo. Defend **shapes**, not invent Uber table names as fact.

### 3.1 Kafka scrape event (producer: Selenium)

```json
{
  "event_id": "uuid",
  "event_time": "2024-…Z",
  "vendor_id": "string",          // partition key
  "menu_id": "string|null",
  "source_url": "https://…",
  "content_type": "html|pdf|image",
  "content_hash": "sha256",
  "object_uri": "gs://…/raw/…",
  "locale": "en|…",
  "scrape_attempt": 1,
  "proxy_pool": "string",
  "status": "ok|blocked|timeout",
  "http_status": 200
}
```

### 3.2 Flink → catalog upsert contract

```json
{
  "vendor_id": "…",
  "menu_version": "content_hash or version",
  "items": [
    {
      "item_key": "vendor_id+normalized_name+size",
      "name": "…",
      "description": "…",
      "price_amount": 12.99,
      "currency": "USD",
      "modifiers": [{"name": "…", "price_delta": 1.5}],
      "availability": true,
      "raw_refs": ["object_uri#chunk"]
    }
  ],
  "idempotency_key": "vendor_id+menu_version"
}
```

**Dedupe state (Flink keyed):** `(vendor_id, content_hash)` → drop duplicates; late events by event-time.

### 3.3 RAG / Milvus metadata + schema gate

```
milvus collection fields (logical):
  embedding vector
  menu_id / vendor_id
  locale
  chunk_text
  label_tags
  source_uri

Gemini output → JSON Schema validate → catalog upsert
low confidence → human review queue
```

**Offline HISTORICAL:** **98%** fidelity · **100%** schema consistency. Say offline/eval, not live SLA.

### 3.4 Processing APIs (LOGICAL ops surface)

```
POST /internal/scrape/jobs          {vendor_ids[], priority}
GET  /internal/scrape/jobs/{id}     lag / success
POST /internal/catalog/upsert       (from Flink sink; idempotent)
POST /internal/rag/extract          {object_uri} → validated menu JSON
GET  /internal/menus/{vendor_id}    freshness SLO (24h→2h HISTORICAL)
```

**ANZ Mobility (separate):** `driver`, `vehicle`, `document`, `compliance_check` — not Eats Kafka topics.

---

# 4. Masters India — GST e-invoice schemas + APIs (LOGICAL / HISTORICAL)

### 4.1 PostgreSQL (quarter-routed)

```sql
-- clients
client_id PK, gstin UNIQUE, name, config JSONB, created_at

-- invoice_header_YYYY_QN   (or schema per quarter)
invoice_id PK
client_id, gstin
invoice_number, invoice_date
supply_type, place_of_supply
taxable_value, cgst, sgst, igst, total_value
status Enum('accepted','irp_pending','registered','failed','cancelled')
idempotency_key UNIQUE   -- client + doc ref
period_quarter  -- derived at API; reject mismatch
INDEX (client_id, invoice_date)

-- invoice_line
line_id PK, invoice_id, hsn, qty, rate, tax_breakup…

-- irp_registration
invoice_id PK/FK
irn, signed_qr, ack_no, ack_date
irp_status, raw_response_ref  -- points to Mongo
```

### 4.2 Mongo + Redis + Kafka

```
mongo.invoice_payload_snapshot:
  { invoice_id, request_doc, irp_response, irn, qr, ts }

redis keys:
  irp:token:{env} TTL < IRP lifetime
  client:config:{client_id}
  gstin:master:{gstin}

kafka topics (logical):
  invoice.accepted      key=gstin
  irp.submit            key=gstin
  irp.completed         key=gstin
  client.webhook        key=client_id
  *.dlq
```

### 4.3 REST + async API sketch

```
POST /v1/einvoice/submit
  Headers: Authorization, Idempotency-Key
  Body: { gstin, invoice_number, invoice_date, lines[], … }
  → 200 { invoice_id, status, irn? }  or  202 { invoice_id, status: irp_pending }

GET  /v1/einvoice/{invoice_id}
POST /v1/bulk/imports          multipart → S3; returns import_id
GET  /v1/bulk/imports/{id}     progress {chunks_done, failed, irp_ok}
POST /v1/webhooks/irp/callback (if used) / internal consumer from Kafka
GET  /v1/invoices?client_id&from&to   // ES-backed search optional
```

**Idempotency:** `client + fileHash + batchIndex` (bulk) and client invoice refs — never double-register IRP.

**Numbers (HISTORICAL):** p95 ~1.2s→~300ms · 700→4,000 req/min · 1M+/day · Redis −30% redundant reads.

---

# 5. GeeksforGeeks — content / votes / subs (LOGICAL / HISTORICAL)

### 5.1 MySQL core

```sql
users(id, email, …)
content(id, type, author_id, title, status, created_at)
votes(
  id PK,
  user_id, content_id,
  value TINYINT,              -- +1 / -1
  UNIQUE(user_id, content_id) -- idempotent cast
)
pins(user_id, content_id, created_at) UNIQUE(user_id, content_id)
locks(content_id, locked_by, reason, expires_at)
subscriptions(user_id, plan, status, started_at, renewed_at)
unread_counters(user_id, thread_id, count)  -- durable; Redis for badge hot path
```

### 5.2 Mongo / ES / Redis

```
mongo: flexible article / doubt payloads
elasticsearch: content_id, title, body, tags — search
redis: vote_buffer:{content_id}, unread:{user_id}, contest hot keys
```

### 5.3 REST sketch

```
POST /api/v1/votes          {content_id, value}  → idempotent upsert
DELETE /api/v1/votes/{content_id}
POST /api/v1/pins           {content_id}
POST /api/v1/content/{id}/lock
GET  /api/v1/unread/count
POST /api/v1/subscriptions  …
GET  /api/v1/search?q=
```

**Numbers (HISTORICAL):** 10K+ daily interactions · premium +15–20% · course sales +30% (influencer dashboard) · ops +70% (crons — separate bullet).

---

# 6. One-page whiteboard cheat sheet

| Project | Draw first | API first |
|---|---|---|
| IA | `fact_*` + `cluster_run`/`_event` + `plan_snapshot` | MCP read tools → Go approve/writeback |
| FRM | `level_mapping` ← `balance_sheet` ← `scoping_assessments` | `GET/PATCH /group_balance_sheet` + `/v2/recon_*` |
| Menu | scrape_event → Flink state → catalog + Milvus | upsert + schema-gated extract |
| Masters | invoice_header → irp_registration + Kafka | submit + bulk import + idempotency |
| GFG | content ← votes (unique user+content) | vote/pin APIs + Redis counters |

---

# Sources

- IA: `KNOWLEDGE-MATERIAL/.../ClickHouse DDL Model (Phase-1).md` · [`29_ia_ch_ddl_phase1_source.md`](29_ia_ch_ddl_phase1_source.md)  
- FRM: `frm_scoping_service/database/models/*` · [`11_uber_frm_deep_dive.md`](11_uber_frm_deep_dive.md)  
- Menu / Masters / GFG: deep dives + packs — **logical** unless code present  

Full ER/why-tech: [`34_er_tables_tech_why.md`](34_er_tables_tech_why.md). Diagrams: [`33_architecture_diagrams.md`](33_architecture_diagrams.md).
