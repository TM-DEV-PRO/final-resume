# 11. Uber FRM Risk Scoping Platform: Deep Dive

> **Start here for interviews:** [`23b_uber_interview_packs.md`](23b_uber_interview_packs.md) § Uber FRM.

Defense material for the four Uber FRM resume bullets. Every number here traces to `GROUND_TRUTH.md` or to the code in `KNOWLEDGE-MATERIAL/UBER-WORK/FRM PROJECT/frm_scoping_service/`. Tags: **MEASURED** (documented artifact or code), **TARGET** (design goal, say "targeting"), **ESTIMATED** (derived, say so). No number here is invented.

Role framing: Software Development Engineer 2 at Uber Finance via EPAM Systems, Jul 2024 to May 2026. This was Uber's internal monorepo (Bazel, Fusion.js, SOADB MySQL, langfx FastAPI framework).

---

## 0. The four bullets I am defending (Jul 2026 hardened wording)

1. **Owned** Uber's **FRM Risk Scoping backend (Spring Boot, MySQL)** across **30+ REST APIs** powering **8** scoping screens, automating quarterly close at **$340M group materiality**, targeting a **70% cut** in manual reconciliation (**~2 weeks → ~3–4 days**, ESTIMATED baseline; 70% is TDD TARGET).
2. **Owned** the Sheets → **MySQL** recon v2 migration (**18 files**), shipping parallel **/v2** APIs that build **L1→L2→L3** FSLI trees, tie **HFM** amounts to public **10-Q** filings, and give each line a durable ID for audit.
3. **Automated** in-scope decisions across **~55 line items × 14 entities** by encoding materiality, qualitative override, residual-risk, and **5%** component-threshold logic in the scoping services against **$340M / $170M** thresholds.
4. **Led 3 engineers** on the FRM backend by owning API contracts and layered design reviews for Finance's quarterly scoping.

Java track maps FastAPI layers to Spring Boot controller / service / repository / JPA. Same ownership and numbers. Do not say 36 endpoints or 19M GL rows.

---

## 1. What FRM Risk Scoping actually IS (plain language)

FRM is Uber's Financial Risk Management team inside Finance. Once a quarter, during the financial close, they run the **Scoping Process**: deciding which financial line items (FSLIs, Financial Statement Line Items) and which legal entities are "in scope" for risk assessment and audit testing. The output is the evidence PwC (external auditor) uses to build their **audit work papers**. Getting scoping right is a SOX-style compliance activity: too narrow and you miss risk, too broad and you waste audit hours.

Before this tool it was a manual Google Sheets workbook (the legacy "DSW version") with formulas, manual parent-child mapping, and no collaboration, no history, no audit trail. The TDD (`FRM _ Scoping Tool - Technical Design Doc .docx`, authored by Priyadharshini Govindan, reviewed by Ramesh Raju, started 02-02-2026) frames the problem as "flat-file storage prevents the system from handling complex recursive financial hierarchies, leading to manual mapping errors and lack of real-time data visibility."

The concepts you must be able to explain:

- **Materiality**: the dollar threshold above which a misstatement would matter to a reader of the financials. Group materiality on the Q4 2025 sample was **$340M** (MEASURED, from the CSVs / metrics table); residual threshold **$170M**. Materiality is stored as a metric in `frm_metrics_table` (`metric_key = "materiality"`).
- **Group scoping vs component scoping**: *Group scoping* looks at the consolidated Uber balance sheet and income statement, line by line, and asks "is this FSLI significant to the group?" *Component scoping* drills down to the individual entity or component level under each FSLI and decides which components get tested. Group is the top of the tree, component is the leaves.
- **Thresholds (5% rule)**: from `Scoping Features.docx`, a component is a **Financially Significant Component** if `Total Revenue % > 5%` OR `|Total Assets %| > 5%`. Those 5% benchmarks are configurable (`assets_benchmark`, `revenue_benchmark` metrics) and recomputed via the `PUT /update_benchmark_thresholds` endpoint.
- **Quantitative vs qualitative material**: Quantitative Material = "YES if HFM Amount > Materiality". Qualitative Material is a manual yes/no answer to a scoping question. **Overall Significance = Significant if quantitative OR qualitative is YES** (this exact rule is in the code: `conclusion_overall_significance_from_balance_sheet_materials`).
- **Residual risk**: after removing what is already covered by in-scope components, what balance and multiple of materiality is left uncovered. Computed per leaf: Residual Balances = HFM Amount - Total in Scope, Residual Multiples = Residual Balances / Materiality (from `Scoping Features.docx` calculation matrix). Flags: `> 50% Materiality`, `> % threshold change`.
- **EMI entities (Equity Method Investments)**: minority investments Uber accounts for under the equity method (for example stakes where Uber owns a percentage but does not consolidate). These are scoped separately in the EMI screen, one grid column per investee, with fields like ownership %, asset balance, preliminary income/loss, auditor, framework.
- **10-Q reconciliation**: Uber's source-of-truth financial numbers come from **Oracle HFM** (Hyperion Financial Management). The recon screen checks HFM amounts against the **publicly filed 10-Q** amounts, line by line, so scoping is built on numbers that tie to what was filed with the SEC. `difference = hfm_amount_in_millions - financial_statement_amount_in_millions`.
- **HFM (Oracle HFM)**: the consolidation system. An ETL job (owned by the data pipeline, not entirely by me: see honesty guardrails) extracts raw GL balances and entity data from HFM and loads them into the MySQL tables.

The 8 screens (MEASURED, TDD + `Scoping Features.docx`): **Reconciliation, Materiality, EMI Scoping, Group Scoping, Threshold Setup, Component Scoping, Residual Risk, Summary**.

---

## 2. The real database schema (11 SQLAlchemy 2.0 models)

All models use SQLAlchemy 2.0 `Mapped[...]` / `mapped_column(...)` typing on a shared `DeclarativeBase` (`database/models/base.py`). Every table carries `fiscal_quarter` (String(4)) + `fiscal_year` (String(8)) as the period key and audit columns (`created_at/by`, `updated_at/by`). There are no DB-level foreign keys in the ORM: relationships are logical, joined on `level_id` and the fiscal period (this matters, see the bug story).

| # | Python model | `__tablename__` | Purpose | Key columns |
|---|---|---|---|---|
| 1 | `BalanceSheet` | `balance_sheet` | Group + component BS scoping facts | `uuid` (PK), `level_id`, `level_1..level_4`, `hfm_amount`, `hfm_amount_previous_year`, `percentage_of_total`, `group_multiple`, `quantitative_material`, `qualitative_material`, `conclusion_overall_significance`, `conclusion_scope`, `total_inscope`, `residual_balances`, `residual_multiples`, `group_status`, `component_status`, `residual_status`, `is_level_active` |
| 2 | `IncomeStatement` | `income_statement` | Group + component IS scoping facts | same shape as `balance_sheet`; also has classmethods `fetch_for_period`, `uuid_exists`, `get_qualitative_and_conclusion`, `update_scope_and_status` (ORM-side query helpers) |
| 3 | `EmiData` | `emi_data` | EMI grid, one row per investee/column | `uuid` (PK), `investee`, `investee_entity`, `uber_investor_entity`, `uber_ownership_equity_interest_percentage`, `asset_balance`, `preliminary_income_loss_on_investments`, `auditor`, `financial_reporting_framework`, `significant_emi`, `is_active`; `@validates` strips whitespace on all string columns |
| 4 | `ScopingMetrics` | `frm_metrics_table` | key/value metrics (materiality, benchmarks) | `uuid` (PK), `metric_key`, `metric_value` (String(512)), `unit`, `is_active` |
| 5 | `ScopingQuestion` | `scoping_questions` | default qualitative questions per page | `uuid` (PK, SHA-256 of question_text + normalized page_name), `question_text` (Text), `page_name`, `is_active` |
| 6 | `ScopingAssessment` | `scoping_assessments` | per-line answers to questions | `uuid` (PK), `question_id`, `line_id`, `answer_text` (Text) |
| 7 | `ThresholdSetup` | `threshold_table_v2` | legal-entity threshold significance | `uuid` (PK), `legal_entity`, `total_assets`, `total_assets_percentage`, `total_revenue`, `total_revenue_percentage`, `financially_significant_component`, `significant_due_to_risk`, `inscope_due_to_coverage`, `conclusion`, `review_status` |
| 8 | `LevelMapping` | `level_mapping` | maps FSLI text hierarchy to a stable `level_id` | `uuid` (PK, used as the join target), `level1..level4`, `is_active` |
| 9 | `ComponentEntityRow` | `component_entity` | per-component HFM amounts by `level_id` | `uuid` (PK), `level_id`, `scoping_component`, `amount` |
| 10 | `ReconBalanceSheet` | `recon_balance_sheet` | recon v2 BS leaf rows | `uuid` (PK), `level_id`, `level_1..level_3`, `hfm_amount`, `hfm_amount_in_millions`, `financial_statement_amount_in_millions`, `difference`, `is_level_active` |
| 11 | `ReconIncomeStatement` | `recon_income_statement` | recon v2 IS leaf rows | same shape as `recon_balance_sheet` |

Note the table name traps to say out loud: the threshold table is physically `threshold_table_v2` (the model class is `ThresholdSetup`), and the metrics/materiality store is `frm_metrics_table` (class `ScopingMetrics`). GROUND_TRUTH notes the full physical `schema.uql` has 16+ tables (collaboration service, comments, notifications live elsewhere); the scoping service itself owns these 11 ORM models. Say "11 SQLAlchemy models in the scoping service", not "the whole database is 11 tables".

### ASCII ER sketch (logical joins, not FK constraints)

```
                         level_mapping (level_id = uuid)
                         level1 / level2 / level3 / level4
                                    ^        ^
             join on level_id +     |        |     join on level_id +
             fiscal_quarter/year    |        |     fiscal_quarter/year
                                    |        |
        +---------------------------+        +--------------------------+
        |                                                               |
   balance_sheet (uuid PK, level_id)                        component_entity (uuid PK, level_id,
   income_statement (uuid PK, level_id)                        scoping_component, amount)
        |   level_1..level_4, hfm_amount,
        |   quantitative/qualitative_material,
        |   conclusion_*, residual_*, *_status
        |
        | line_id = balance_sheet.uuid / income_statement.uuid
        v
   scoping_assessments (uuid PK, question_id, line_id, answer_text)
        |
        | question_id = scoping_questions.uuid
        v
   scoping_questions (uuid PK, question_text, page_name)

   frm_metrics_table        threshold_table_v2         emi_data
   (materiality,            (legal_entity,             (one row per
    assets/revenue           5% significance,           investee column)
    benchmarks)              conclusion)

   recon_balance_sheet / recon_income_statement  (v2 recon leaves,
      level_1..level_3, hfm vs financial_statement amount, difference)
```

The spine is `level_mapping`: the fact tables (`balance_sheet`, `income_statement`) and `component_entity` all carry a `level_id` that equals `level_mapping.uuid`, and joins are always ANDed with `fiscal_quarter`, `fiscal_year`, and the active flags (`lm.is_active = 'true'`, `is_level_active = 'true'`). `scoping_assessments.line_id` points at a fact row `uuid`; `scoping_assessments.question_id` points at `scoping_questions.uuid`.

---

## 3. API surface (from `handler/scoping_handler.py`)

One `APIRouter(prefix="/frm-scoping", tags=["FRM Scoping Tool"])`. I counted the `add_api_route(...)` registrations directly in `setup_routes()`: **32 route registrations, one of which is `/health`**, so 31 functional endpoints plus the health check. That is the honest basis for "**30+ REST endpoints**" on the resume. Do NOT say 36 (that number only appears if you also count the separate `frm-collaboration-service` comment/notification APIs listed in the TDD).

Route groups (all under `/frm-scoping`):

- **Health / smoke**: `GET /health`, `POST /scoping` (welcome echo).
- **Reconciliation (v1, Sheets-backed)**: `GET /recon_balance_sheet`, `GET /recon_income_statement` (served by `RiskScopingService`).
- **Reconciliation (v2, MySQL-backed)**: `GET /v2/recon_balance_sheet`, `GET /v2/recon_income_statement` (served by `NewReconBalanceSheetService` / `NewReconIncomeStatementService`). This is the migration I owned.
- **Group scoping**: `GET /group_balance_sheet`, `PATCH /group_balance_sheet/{balance_sheet_uuid}`, `GET /group_income_statement`, `PATCH /group_income_statement/{income_statement_uuid}` (update `conclusion_scope` and/or `group_status`; allowed statuses Draft, Review, ReOpen, Closed).
- **Component scoping**: `GET /bs_components`, `GET /is_components`, plus cascading filter option endpoints `GET /bs_component_filters`, `GET /is_component_filters` (return distinct `level_1..level_4` options).
- **Residual risk**: `GET /residual_risk?fsli_type=bs|is`.
- **EMI**: `GET /emi_scoping` (v1 comparison view), `GET /emi_data` (MySQL grid), `PATCH /emi_data/{uuid}`.
- **Metrics / materiality / thresholds**: `POST /add_scoping_metrics`, `GET /scoping_metrics`, `PUT /update_benchmark_thresholds`, `GET|PUT /materiality`, `GET|PUT /active-page-number`, `GET /threshold-setup`, `PATCH /threshold-setup/{uuid}`.
- **Scoping questions / assessments**: `POST /scoping_questions/bulk`, `GET /scoping_questions`, `POST /scoping_assessments`, `GET /scoping_assessments`, `PATCH /scoping_assessments/{assessment_uuid}`.

Cross-cutting details worth mentioning in an interview:
- **Auth**: every write path calls `_get_auth_email(request)` which reads the `x-auth-params-email` header and raises 401 if missing. That email is stored as `updated_by` / `created_by`. Uber's gateway injects this header after authenticating the user, so the service trusts the edge and just records identity for the audit trail.
- **Async offload**: the DB calls are synchronous SQLAlchemy, so blocking work is pushed off the event loop with `await asyncio.to_thread(...)`. The FastAPI handler stays async; the repository runs on a thread.
- **Lazy service init**: `ScopingHandler` defers constructing the heavy SQLAlchemy-backed services (`GroupBalanceSheetService`, etc.) so app startup and `/openapi.json` stay fast unless those endpoints are actually hit.
- **Error contract**: `ValueError` with "not found"-style messages maps to 404, other validation to 400/422, `RuntimeError` (Sheets unavailable) to 503, everything else to 500. Pydantic `ValidationError` on query params is re-raised as 422 via `jsonable_encoder(e.errors())`.

---

## 4. The recon v1 to v2 migration (the story I own)

Source: `RECON_API_MIGRATION.md` (branch `tmitta1/recon-income-api-migration`, dated 2026-05-06, 2 commits, **18 files changed, 1,268 insertions, 4 deletions**) plus `service/recon_service.py` and the repository.

### Why
The v1 reconciliation endpoints were **Google Sheets backed**: the L3 line data lived only in a sheet, "lacks direct storage in the database" (`Scoping Features.docx`). That meant you could not attach comments to a specific recon line (no stable line-item ID), could not track it by quarter/year, and the numbers were not part of the relational source of truth. The fix, per the TDD's SSOT goal, was to persist recon L3 data in MySQL (`recon_balance_sheet`, `recon_income_statement`) keyed by quarter and year, so recon becomes queryable, comment-mappable, and consistent with the rest of scoping.

### How (the safe migration pattern)
1. **Add v2 alongside v1, do not replace.** New endpoints `GET /v2/recon_balance_sheet` and `GET /v2/recon_income_statement` were added; the v1 `GET /recon_balance_sheet` / `GET /recon_income_statement` stayed untouched. This is a parallel-run: both endpoints live at the same time.
2. **New layers top to bottom**: ORM models (2), Pydantic response schema (`ReconLevel3Item`, `ReconLevel2Node`, `ReconLevel1Node`, `ReconFetchResponse`), repository readers (`fetch_recon_balance_sheet_rows`, `fetch_recon_income_statement_rows`), and a service (`recon_service.py`) that builds the L1 -> L2 -> L3 nested tree and aggregates child sums up to parents.
3. **Comparison / validation**: v2 returns HFM amount, the filed financial statement amount, and the difference per line (`difference = hfm_amount_in_millions - financial_statement_amount_in_millions`, with a null fallback that recomputes it). QA compared v1 (Sheets) and v2 (MySQL) responses for the same period side by side, plus the `RECON_API_MIGRATION.md` test plan: happy paths, empty period returns `level_1_fslis: []`, missing params return 422, and a v1 regression check that the old shape (`headers`, `data`, `analytics`) is unchanged.
4. **FSLI display ordering**: the financial-statement order is hardcoded in `_BS_FSLI_ORDER` and `_IS_FSLI_ORDER` dicts keyed by parent-path tuples. Unknown FSLIs (not in the dict) are appended at the end rather than dropped, so new source data cannot break the API. Negative amounts render with parentheses, for example `($8)`.
5. **Cutover**: the UI (`/risk-scoping/reconciliation`) was pointed at v2 once verified on staging (`frm-staging.uberinternal.com`); v1 stayed as a fallback and for regression safety.

### The column-aliasing bug (tell this precisely)

The legacy read path built row dicts from a raw SQL result like this (still visible in `_fetch_fiscal_period_rows` and the component readers):

```python
result = session.execute(text(sql), bind)
keys = list(result.keys())
rows = [dict(zip(keys, tuple(r))) for r in result.fetchall()]
```

`dict(zip(result.keys(), row))` is only safe if `result.keys()` is unique. The moment you **join two tables that share column names**, it stops being safe. The component/scoping aggregate joins the fact table (`balance_sheet` or `income_statement`, aliased `i`) to `level_mapping` (aliased `lm`), and both sides carry `uuid`, `level_id`, `fiscal_quarter`, `fiscal_year`, and level columns. When such a join projects `i.uuid` and `lm.uuid` (or `i.fiscal_quarter` and `lm.fiscal_quarter`) without distinct labels, the driver returns two columns literally named `uuid`. `zip` pairs positionally and `dict` keeps the **last** write, so the row dict silently took the `level_mapping` uuid instead of the fact uuid (and similar collisions on the period columns). Symptom: recon/component rows that looked correct but keyed off the wrong identifier, so PATCH-by-uuid and comment mapping pointed at the wrong line.

The fix is in `_component_scoping_rows_select` (and the pattern I carried into recon): move from raw SQL to a SQLAlchemy `select()` on `aliased()` models and give **every projected column an explicit `.label()`** so `result.keys()` is unambiguous:

```python
i = aliased(fact_model, name="i")
lm = aliased(LevelMapping, name="lm")
select(
    func.min(i.uuid).label("fsli_id"),          # fact identity, uniquely named
    func.min(i.level_id).label("level_id"),
    func.max(lm.uuid).label("level_mapping_uuid"),   # mapping identity, separately named
    lm.level1.label("level_1"),
    func.max(lm.fiscal_quarter).label("level_mapping_fiscal_quarter"),
    ...
)
```

Now `dict(zip(result.keys(), row))` cannot collide, and `_finalize_component_scoping_row` deterministically maps `fsli_id` back onto `uuid`. The general lesson to state: with `result.keys()` row mapping, ambiguous/duplicate column names across joined tables cause silent last-write-wins overwrites; labeling every column (or using ORM entity rows / `RowMapping`) removes the ambiguity.

### What could still go wrong (say this proactively)
- **Aggregation vs identity**: because L1/L2 amounts are `SUM`s of children, a duplicated or mis-mapped leaf double-counts. Hence the test-plan checks that a parent equals the sum of its children.
- **Active-flag drift**: joins require `is_active = 'true'` and `is_level_active = 'true'`; if the ETL loads rows with the wrong flag the line vanishes from the tree with no error.
- **Currency parsing**: amounts arrive as display strings in places (`parse_currency_display_to_float`); a malformed string silently becomes 0.0.
- **Hardcoded FSLI order** is brittle if Finance renames a line; unknowns fall to the bottom rather than erroring, which is safe but can look "out of order".

---

## 5. Leadership: leading a pod of 3 engineers

Headcount is confirmed in GROUND_TRUTH: **led 3 engineers (EPAM pod)** at Uber. Frame it as a tech-lead-of-a-pod, not a people manager (EPAM contractor structure inside Uber).

What "led" concretely meant, tied to artifacts:
- **Task breakdown by layer**: work was sliced along the handler / service / repository / model boundary so two engineers could work the same feature without colliding (one on the Pydantic schema + handler, one on the repository + ORM). The recon migration is a clean example: 18 files but cleanly split across the five layers.
- **Layered architecture conventions**: I set and enforced the conventions that show up consistently across the codebase: handlers stay thin and only do HTTP + auth + error mapping; services own orchestration and tree building; repositories own all SQLAlchemy and session lifecycle (`get_read_write()` / `commit` / `rollback` / `close` in `finally`); models hold column definitions plus period-scoped query classmethods. These came out of the **backend team syncs** (see `Notes - FRM CT Backend Team Sync.docx` in KT&DOCS).
- **Code review gates**: every PR had to add or update tests in the matching `tests/` folder and pass the Bazel `uber_py_test` targets before merge. That is why the suite grew to 1,100+ tests (see below).
- **Consistency reviews**: I pushed patterns like "every write path reads `x-auth-params-email` and records `updated_by`", "no bare `except` that swallows, always log with `exc_info` and re-map to an HTTPException", and "offload blocking DB work with `asyncio.to_thread`". You can see these applied uniformly, which is the tell of an enforced convention rather than one person's style.

Behavioral answer shape: situation (manual Sheets close, PwC deadline pressure), task (stand up the platform and keep 3 engineers unblocked), action (layered decomposition + review discipline + test gates), result (8 screens shipped, recon migrated, targeting the 70% effort cut).

---

## 6. Honesty guardrails (do not oversell)

- **70% is a TARGET, not a measured KPI.** It is TDD section 3.1's goal: "Achieve a 70% reduction in time spent on manual data ingestion and reconciliation through automated ETL pipelines." Always say "**targeting** a 70% cut" or give the baseline as ESTIMATED (~2 weeks manual close down to ~3-4 days). Never claim it was measured post-launch.
- **Endpoint count is 30+.** Code truth is 32 `add_api_route` registrations including `/health` (31 functional + health). Say "30+"; do not say 36 (that only holds if you fold in the separate collaboration service).
- **Do NOT claim 19M rows.** Real scale (MEASURED from the Q4 2025 CSVs): raw GL extracts up to ~95K rows per quarter (individual dumps of ~76K / ~38K / ~95K), roughly **1.7K-1.8K accounts** and **~400 entities**. The "19M rows to 300K" line was unsupported and is dropped. If asked about volume, this is a **tens-of-thousands-of-rows** system, not big data; the value is correctness, hierarchy, and auditability, not throughput.
- **Materiality $340M / residual $170M** are from the Q4 2025 sample (MEASURED), and ~26 balance-sheet FSLIs / ~29 income-statement FSLIs, 14 entities in that sample. Present them as "on the Q4 2025 close", not as fixed constants.
- **Test count**: a grep of `def test_` across the 65 test files returns roughly **1,288** test functions. The resume says **1,100+**, which is deliberately conservative and safe. GROUND_TRUTH's "~1125" is in the same ballpark. **Coverage percentage is unverified**: do not quote a coverage number for FRM (the 82% coverage figure belongs to Masters India, not this project).
- **ETL ownership**: the HFM extract/transform/load pipeline is described in the TDD but was a shared/pipeline responsibility. Say "the service consumes HFM-loaded MySQL tables" and "I owned the scoping APIs and the recon migration", not "I built the entire ETL".
- **Real-time collaboration / Slack notifications** live in the separate `frm-collaboration-service`. Do not claim I built that; I built the scoping service.

---

## 7. Rapid-fire Q&A (12+)

**Q1. Why FastAPI?**
It is the Uber-internal standard for Python HTTP services (via the `langfx`/`uber.ai.langfx.fastapi` framework), and the workload is I/O-bound API serving with heavy request/response validation. Pydantic models give me typed request validation, automatic 422s, and a free OpenAPI/Swagger surface that Finance users and QA used directly. Async handlers let me offload blocking SQLAlchemy calls with `asyncio.to_thread` while keeping the event loop responsive.

**Q2. Why MySQL (and not Postgres or a warehouse)?**
It was mandated by Uber's **SOADB** standard (MySQL + InnoDB) for service-owned relational data, which gives ACID guarantees for multi-user concurrent edits during close. The data is small (tens of thousands of rows/quarter) and highly relational (recursive FSLI hierarchies), so a row store with composite indexes on `(fiscal_quarter, fiscal_year)` is exactly right; a columnar warehouse would be overkill and would not give the transactional edit semantics the scoping workflow needs.

**Q3. Why the layered handler / service / repository pattern?**
Separation of concerns and testability. Handlers do only HTTP (auth header, param validation, error-to-status mapping). Services own business logic and tree building. Repositories own every session and all SQL. Because dependencies point one direction, I can unit test a handler with a mocked service and a service with a mocked repository, with zero database. It also let 3 engineers work the same feature across layers without merge collisions.

**Q4. How does auth work?**
There is no password logic in the service. Uber's gateway authenticates the user and injects an `x-auth-params-email` header. `_get_auth_email(request)` pulls it, returns 401 if missing, and the email is persisted as `created_by` / `updated_by` on every mutation. So the service trusts the authenticated edge and its own job is identity capture for the audit trail. Authorization (who may edit) was enforced upstream, which is a fair thing to call out as a limitation.

**Q5. How would you scale it?**
It barely needs scaling given the data size, but: the SQLAlchemy engine already uses `pool_pre_ping=True` and a cached engine per config (`MySQLManager` memoizes the `nemo` instance). To scale reads I would add read-replica routing (the internal `MySQLDatabase` already exposes read/write split), cache per-period GET responses (the tree is expensive to build and immutable within a closed period), and add composite indexes on `(fiscal_quarter, fiscal_year, level_id)`. Writes are low volume (managers editing cells), so the bottleneck is read fan-out of the nested trees, which caching solves.

**Q6. How does ETL from HFM work?**
Scheduled Python jobs extract raw balances and entity data from Oracle HFM, transform them (cleansing, recursive parent-child hierarchy resolution into `level_mapping`, aggregations), and load normalized rows into `balance_sheet` / `income_statement` / `component_entity` / recon tables keyed by period. My service consumes those loaded tables; I owned the scoping and recon APIs on top, and the pipeline was a shared responsibility (honesty guardrail).

**Q7. Why not just keep the Google Sheets workflow?**
Sheets cannot model recursive financial hierarchies safely, has no stable per-line IDs (so you cannot attach comments or audit history), no concurrency control (managers overwrite each other), and no single source of truth (versions drift). For a SOX-adjacent, PwC-audited process that is a real risk. The relational schema gives referential integrity, period keys, an audit trail, and comment mapping, which is the whole point of the tool.

**Q8. How do you handle transactions?**
Every repository function opens a session via `db.get_read_write()`, does its work, `commit()`s on success, `rollback()`s on any exception, and `close()`s in a `finally`. Multi-step writes are done in one session so they are atomic: for example updating benchmark metrics updates both `assets_benchmark` and `revenue_benchmark` and commits once (raising `ValueError` if either row is missing), and the EMI "Total" column patch mirrors the amount into `balance_sheet` / `income_statement` in the **same** transaction before commit. The `scoping_assessments` write with `sync_required` updates the mapped line table and the assessment together, and rolls back the whole thing if the line sync affects zero rows.

**Q9. Idempotency?**
GETs are naturally idempotent. PATCH/PUT are idempotent by design: they set explicit column values by primary key (`uuid`), so replaying the same PATCH yields the same state. `scoping_questions` bulk uses a **deterministic uuid** (SHA-256 of `question_text` + normalized `page_name`) and upserts, so re-injecting the same payload updates in place instead of duplicating. `scoping_assessments` are "create once, then update" per line (from `Scoping Features.docx`). What is not strictly idempotent is `POST /add_scoping_metrics` (append), which is acceptable because those are versioned by `is_active` and timestamp.

**Q10. How did you test handlers with mocks?**
`handler/tests/test_scoping_handler.py` (112 test functions in that file alone) uses FastAPI's `TestClient` plus `unittest.mock` (`AsyncMock`, `MagicMock`, `patch`). I inject fake services into `ScopingHandler(...)` (its constructor takes optional service instances precisely for this) and `patch` the repository-level functions (for example `...recon_service.fetch_recon_balance_sheet_rows`) so no database is touched. Tests assert status codes, response shapes, the 401-on-missing-header path (`test_scoping_handler_auth.py`), and error-to-status mapping.

**Q11. Bazel test setup?**
Each package has a `tests/BUILD.bazel` declaring an `uber_py_test` target named `py_default_test`, `python_version = "3.11"`, listing the test srcs and deps (the package library plus `@third_party_python_base//pytest`, `//fastapi`, etc.). CI runs the five layer targets (database, schema, repository, service, handler) as shown in `RECON_API_MIGRATION.md`; all must PASS to merge. The app itself is a `py_binary` (`frm_scoping_service`) with a `py_library`.

**Q12. What is `level_id` and why join on it plus period?**
`level_id` on a fact row equals `level_mapping.uuid`, and `level_mapping` holds the `level1..level4` text hierarchy. Facts store the id, not the text, so hierarchy renames do not rewrite every fact. Joins always AND `level_id` with `fiscal_quarter` + `fiscal_year` + active flags because the same logical FSLI exists once per period; joining on id alone would fan out across quarters.

**Q13. Why store amounts as DECIMAL(18,2) and percentages as DECIMAL(5,2)?**
Money must be exact (no float rounding), so `DECIMAL`/`Numeric` in the DB and `Decimal` in Python; `_to_float` only converts at the display/aggregation edge. Percentages fit in `(5,2)` (up to 999.99%).

**Q14. What was the hardest part?**
Getting the recursive tree correct and consistent between v1 and v2 while the underlying identity was ambiguous (the column-aliasing bug), under a hard quarterly-close deadline, without breaking the live v1 path. The parallel-run plus explicit column labeling plus the parent-equals-sum-of-children invariant checks are what made the cutover safe.

---

## 8. One-paragraph verbal summary (for "walk me through FRM")

"At Uber Finance I built the FRM Risk Scoping platform, a FastAPI + MySQL tool that replaced a manual Google Sheets close for the quarterly scoping process, the activity that decides which financial line items and entities are in scope for PwC's audit. It is 8 screens and 30-plus REST endpoints over an 11-table SQLAlchemy 2.0 schema, in a strict handler / service / repository layering with header-based auth. On the Q4 2025 close, group materiality was $340M. The project's goal was targeting a 70% cut in manual ingestion and reconciliation time. I personally owned migrating reconciliation from Sheets-backed v1 APIs to MySQL-backed v2 APIs, running both in parallel and validating HFM against the filed 10-Q, and I fixed a latent column-aliasing bug where joined tables produced duplicate result-key names and silently mapped rows to the wrong identity, by moving to SQLAlchemy aliased selects with explicit labels. I led a pod of 3 engineers and we grew the service to 1,100-plus pytest tests gated by Bazel CI."

---

## Mock interview: hardest questions with answers

Adversarial round with a skeptical senior engineering manager from a fintech background. Questions are the ones designed to expose exaggeration; answers are grounded only in the code and KT docs. Anything not in the shipped scoping-service code is labeled design intent, not implemented fact.

**Q1. You put "30+ REST APIs" on a resume. That reads like padding. Show me the real number and prove you are not double counting trivial routes.**
The honest basis is code, not marketing. In `handler/scoping_handler.py`, `setup_routes()` makes exactly 32 `add_api_route(...)` registrations, one of which is `/health`, so it is 31 functional endpoints plus a health check. I say "30+" precisely so I am under-claiming against the real count. I do not say 36, because that number only appears if you fold in the separate `frm-collaboration-service` comment and notification APIs, which I did not build. The 31 span reconciliation v1 and v2, group balance sheet and income statement, component scoping and filters, residual risk, EMI, metrics and materiality and benchmarks, threshold setup, and scoping questions and assessments. None of them are duplicate verbs on the same resource for padding; the PATCH and PUT routes carry distinct business logic like status transitions and benchmark recomputation.

**Q2. Why MySQL and not PostgreSQL? Postgres has recursive CTEs and better JSON. Defend the choice or admit it was handed to you.**
Both are true at once: it was the right tool and it was the platform standard, and I will not pretend I picked it in a vacuum. Uber's SOADB standard for service-owned relational data is MySQL on InnoDB, so choosing anything else would have meant fighting the platform for no product gain. On the merits it still fits: the working set is tiny, up to about 95K raw GL rows per quarter and roughly 1.7K to 1.8K accounts and about 400 entities, so this is a tens-of-thousands-of-rows correctness problem, not a scale problem. I did not need Postgres recursive CTEs because I do not resolve the hierarchy in SQL at query time; the ETL flattens the recursive FSLI tree into a stable `level_id` in `level_mapping`, and the API joins facts to that id plus the fiscal period. InnoDB gives me the ACID multi-user edit semantics the close needs, and that is what actually matters here.

**Q3. "SQLAlchemy 2.0" is a buzzword unless you can tell me what 2.0 actually changed for you. What did the 2.0 style buy you on this project?**
Concretely, every model is a `Mapped[...]` / `mapped_column(...)` declaration on a shared `DeclarativeBase`, which gives me typed attributes the type checker can see instead of the old implicit `Column` attributes. The read paths use the 2.0 `select()` construct with `aliased()` models rather than legacy `Query`, which is exactly what let me kill the column-aliasing bug by labeling every projected column. It also standardized session handling: repositories open a session with `get_read_write()`, commit on success, roll back on any exception, and close in a `finally`. So 2.0 is not decoration here; the typed models plus `select()` with explicit `.label()` are the mechanism behind the correctness fix I am proudest of.

**Q4. In the Java variant of your resume this is Spring Boot and Hibernate. Which is the lie?**
Neither is a lie, and I would tell an interviewer the truth up front: the actual implementation is Python, FastAPI, and SQLAlchemy 2.0. When I present the Java framing I am mapping the same architecture onto the Spring vocabulary because the patterns are one to one: the FastAPI handler layer is the Spring `@RestController`, the service layer is `@Service`, the repository layer is the Spring Data JPA repository, and the SQLAlchemy declarative models map to JPA entities under Hibernate. The `x-auth-params-email` middleware is a servlet filter or `HandlerInterceptor`, and the Bazel `uber_py_test` gate is the equivalent of a Maven or Gradle Surefire gate. I position it as "transferable architecture, implemented in Python," and I never claim I wrote Hibernate code that I did not write.

**Q5. Explain materiality and FSLI to me like I do not have a finance degree, then tell me exactly where they live in your system.**
An FSLI is a Financial Statement Line Item, one line on the balance sheet or income statement, for example Cash, Accounts Receivable, or Revenue. Materiality is the dollar threshold above which a misstatement would change the decision of someone reading the financials; auditors set it top-down, commonly as a percentage of a key figure like pre-tax income, total assets, or revenue. In my system materiality is not hard coded; it is a row in `frm_metrics_table` with `metric_key = "materiality"`, and on the Q4 2025 close it was $340M with a residual threshold of $170M. The FSLIs live as rows in `balance_sheet` and `income_statement`, about 26 balance-sheet and 29 income-statement line items on that close, each carrying its HFM amount and its computed significance conclusion.

**Q6. Walk me through the rule engine. What is the actual boolean logic that flags an item as material, and where is it in code?**
There are two independent tests per line and then an OR. Quantitative Material is "YES if HFM Amount > Materiality," a straight value against the $340M threshold. Qualitative Material is a manual yes or no answer captured against a scoping question. The overall verdict is Overall Significance = Significant if quantitative OR qualitative is YES, and that exact rule is in the code as `conclusion_overall_significance_from_balance_sheet_materials`. At the component level there is a second rule set from `Scoping Features.docx`: a component is a Financially Significant Component if Total Revenue % > 5% OR absolute Total Assets % > 5%, where the 5% benchmarks are configurable metrics (`assets_benchmark`, `revenue_benchmark`) recomputed via `PUT /update_benchmark_thresholds`. So it is threshold comparisons and a benchmark rule, deterministic and auditable, not a black box.

**Q7. Residual risk sounds like a made-up screen. What does it actually compute?**
It answers "after everything we already put in scope, how much uncovered balance is left and does it still matter." Per leaf line the computation is Residual Balances = HFM Amount minus Total in Scope, and Residual Multiples = Residual Balances divided by Materiality, both from the `Scoping Features.docx` calculation matrix and stored on the fact rows as `residual_balances` and `residual_multiples`. The screen then flags lines where residual exceeds 50% of materiality or crosses a percentage-change threshold, which is what tells a manager an uncovered remainder is still audit-relevant. It is served by `GET /residual_risk?fsli_type=bs|is`. The point is that scoping is not just "flag the big lines," it also proves the leftover is small enough to ignore.

**Q8. How do you model a recursive financial hierarchy in a database that you just told me has no recursive queries? That smells contradictory.**
The trick is I resolve recursion once, in the ETL, not on every read. `level_mapping` holds the flattened path columns `level1` through `level4` and a stable `uuid` that I use as `level_id`. Every fact row in `balance_sheet`, `income_statement`, and `component_entity` stores that `level_id` instead of the hierarchy text, so a rename of a parent node does not rewrite thousands of fact rows. At read time the service builds the L1 to L2 to L3 nested tree in application code and aggregates child sums up to parents, and joins always AND `level_id` with `fiscal_quarter`, `fiscal_year`, and the active flags. So the hierarchy is real and recursive in shape, but it is materialized into stable ids, which is both faster and safer than recursive SQL for a dataset this size.

**Q9. Tell me the column-aliasing bug precisely. What broke, how did it surface, and how did you find it? No hand waving.**
The legacy read path built row dicts with `dict(zip(result.keys(), row))` off a raw SQL result. That is only safe when `result.keys()` is unique. The component aggregate joins the fact table (aliased `i`) to `level_mapping` (aliased `lm`), and both sides carry `uuid`, `level_id`, `fiscal_quarter`, and `fiscal_year`. When the projection returned two columns literally named `uuid`, `zip` paired positionally and `dict` kept the last write, so the row silently took the `level_mapping` uuid instead of the fact uuid. The symptom was rows that looked correct on screen but keyed off the wrong identifier, so PATCH-by-uuid and comment mapping pointed at the wrong line; it surfaced when an edit to one recon line appeared to affect a different line. The fix was to move to a SQLAlchemy `select()` on `aliased()` models and give every projected column an explicit `.label()`, for example `func.min(i.uuid).label("fsli_id")` versus `func.max(lm.uuid).label("level_mapping_uuid")`, so `result.keys()` can no longer collide.

**Q10. The 10-Q validation is the part I trust least. Walk me through exactly how HFM numbers get checked against a public filing.**
HFM is Oracle Hyperion Financial Management, the consolidation system where entity trial balances are loaded, currency-translated, and run through intercompany eliminations and minority-interest and equity adjustments to produce the consolidated group numbers. The 10-Q is the quarterly report filed with the SEC, so its line items are the post-consolidation, publicly attested truth. The recon screen puts the two side by side per line: `difference = hfm_amount_in_millions - financial_statement_amount_in_millions`, and a nonzero difference means HFM and the filed statement do not tie and someone has to explain it before scoping proceeds. This is a standard finance tie-out: you reconcile the consolidated HFM output against the filed statements so that scoping is built on numbers that match what went to the SEC. In my system the v2 recon endpoints persist those leaf rows in `recon_balance_sheet` and `recon_income_statement` keyed by quarter and year so the tie-out is queryable and comment-mappable, which the old Sheets version could not do.

**Q11. What are the 8 screens, and which ones carry real logic versus being glorified tables?**
The 8 are Reconciliation, Materiality, EMI Scoping, Group Scoping, Threshold Setup, Component Scoping, Residual Risk, and Summary. Reconciliation runs the HFM-versus-10-Q tie-out. Materiality stores and edits the $340M threshold and benchmarks. EMI Scoping handles Equity Method Investments, one grid column per investee with ownership percentage, asset balance, and preliminary income or loss. Group Scoping applies the quantitative-OR-qualitative significance rule at the consolidated level with status transitions Draft, Review, ReOpen, and Closed; Component Scoping drills into entities under each FSLI and applies the 5% Financially Significant Component rule; Threshold Setup manages legal-entity significance; Residual Risk computes the residual balance and multiple; and Summary rolls up coverage. So Group, Component, Residual, Threshold, and EMI carry real rule logic; Reconciliation carries the tie-out; Materiality and Summary are lighter but still write-through.

**Q12. Multiple managers edit the same close at once. How do you stop them from clobbering each other? Be specific about what you actually built versus what was designed.**
I will separate the two cleanly. What I built in the scoping service: writes are keyed by `uuid` primary key with explicit column sets, each write runs in a single committed transaction with rollback on failure, and every mutation records `updated_by` from the auth header, so the system of record is consistent and attributable. What is design intent in the TDD, not something I hand-wrote in the scoping service: true real-time multi-user sync uses a WebSocket-lite or polling model on the frontend via TanStack Query, and Optimistic Concurrency Control with version numbers lives in the separate `frm-collaboration-service` and its own MySQL, which checks that no other manager modified a record since it was fetched. So if you ask "did you personally ship WebSocket conflict resolution," the honest answer is no; the scoping service relies on transactional per-uuid writes, and the real-time and version-check layers are the collaboration service and the client.

**Q13. Your auth is one header. That is either elegant or a gaping hole. Convince me it is not the latter.**
The service reads `x-auth-params-email` via `_get_auth_email(request)`, returns 401 if it is missing, and stores that email as `created_by` and `updated_by`. It works because Uber's gateway authenticates the user at the edge and injects that header only after authentication, so the service trusts the edge and its job is identity capture for the audit trail, which is exactly what a SOX-adjacent tool needs. The honest limitation, and I say it before the interviewer does, is that this is authentication trust plus audit, not fine-grained authorization; the service does not itself decide who is allowed to edit which entity, that was enforced upstream. If I were hardening it standalone I would add role checks in a dependency and verify a signed token rather than a plain header, so the service does not blindly trust an internal-only assumption.

**Q14. You claim "1,100+ tests." Sounds inflated. What is the real count, what do they actually cover, and could they all be trivial?**
The real count is higher than the resume: a grep of `def test_` across the roughly 65 test files returns about 1,288 test functions, and I wrote 1,100+ deliberately to under-claim. They are not trivial: `handler/tests/test_scoping_handler.py` alone has about 112 functions using FastAPI's `TestClient` with `AsyncMock` and `patch` to inject fake services, so handlers are tested for status codes, response shapes, the 401-on-missing-header path, and error-to-status mapping with zero database. The layered design is what makes this possible; I can unit test a handler against a mocked service and a service against a mocked repository. What I do not claim is a coverage percentage, because I never verified one for this project, so I quote the test count, not a coverage number.

**Q15. Bazel for a Python service? Explain the test setup and why CI actually gates anything.**
Bazel is the Uber monorepo build system, so it is not a choice, it is the environment. Each package has a `tests/BUILD.bazel` declaring an `uber_py_test` target, `python_version = "3.11"`, listing its srcs and deps including the package library and third-party pytest and FastAPI. The app itself is a `py_binary` over a `py_library`. CI runs the five layer targets, database, schema, repository, service, and handler, and all must pass before merge, which is documented in `RECON_API_MIGRATION.md`. The gate is real because the review convention I enforced was that every PR must add or update tests in the matching `tests/` folder, which is the direct reason the suite grew past 1,100.

**Q16. "Led 3 engineers" is the easiest thing on a resume to inflate. What did leading actually look like, with evidence?**
I was the tech lead of a 3-engineer EPAM pod inside Uber Finance, not a people manager, and I say that framing plainly. Leading meant three concrete things backed by the codebase. First, I sliced work along the handler, service, repository, model boundary so two engineers could build the same feature without merge collisions; the recon migration is the clean example, 18 files and 1,268 insertions split across five layers. Second, I set and enforced the conventions that appear uniformly across the code: thin handlers doing only HTTP, auth, and error mapping; services owning tree building; repositories owning every session; and the `x-auth-params-email` plus `updated_by` pattern on every write. Third, I ran the review gate that required tests with every PR and passing Bazel targets before merge, which came out of the backend team syncs documented in `Notes - FRM CT Backend Team Sync.docx`. The uniformity of those patterns across many files is the evidence it was an enforced standard, not one person's style.

**Q17. Where is your caching and what are your latency numbers? Fintech grids get slow.**
I will be exact about what exists versus what was planned. In the shipped scoping service, the only server-side caching is that `MySQLManager` memoizes the SQLAlchemy engine per config with `pool_pre_ping=True`; there is no Redis and no response cache in my code, so I will not claim one. The frontend, per the TDD, uses TanStack Query for client-side caching and Base Web virtual scrolling to render thousands of FSLIs, and the TDD states a sub-second grid target. Those are design intent and NFR targets, not latency numbers I measured and can defend, so I present them as targets. If asked how I would add caching, the honest design is a per-period response cache, because a closed period's tree is immutable and expensive to rebuild, plus composite indexes on `(fiscal_quarter, fiscal_year, level_id)`; I mark that as what I would do, not what shipped.

**Q18. This whole thing is tens of thousands of rows. Is this even a hard engineering problem, or a spreadsheet with extra steps?**
It is deliberately not a big-data problem, and pretending otherwise is how people get caught. The raw GL extracts are up to about 95K rows per quarter across roughly 1.7K to 1.8K accounts and about 400 entities, so throughput is trivial. The hardness is correctness, hierarchy, and auditability under a hard quarterly-close deadline for a PwC-audited process. Getting the recursive tree right, keeping parent equal to the sum of children, migrating recon from Sheets to MySQL with both paths running in parallel, and fixing an identity bug that silently mapped rows to the wrong line, those are the real risks, because a wrong number here flows into an SEC filing's audit evidence. So the value is not scale, it is that the output is trustworthy and traceable, which a spreadsheet cannot guarantee.

**Q19. If HFM does not tie to the 10-Q, what does your system do? Does it block or just display?**
The v2 recon endpoint computes and returns the per-line `difference` between the HFM amount and the filed financial-statement amount, so a nonzero difference is surfaced explicitly rather than hidden. The system displays and persists the mismatch keyed by quarter and year, and because recon lines now have stable ids, a manager can attach a comment explaining or resolving each break, which the old Sheets version could not do. It does not hard-block scoping in code; the control is procedural, a manager must review and clear differences before finalizing, and the tool makes every break visible and commentable rather than silently proceeding. That is the honest boundary: the tool enforces visibility and auditability of breaks, humans enforce the sign-off.

**Q20. What is the single thing most likely to silently produce a wrong scoping result, and how do you defend against it?**
Aggregation identity errors, because L1 and L2 amounts are sums of children, so a single duplicated or mis-mapped leaf double-counts and quietly inflates a parent. That is exactly the failure mode the column-aliasing bug could have caused, which is why the fix and the test plan both matter. My defenses are the parent-equals-sum-of-children invariant checked in the recon test plan, explicit `.label()` on every joined column so identity can never collide, and the active-flag discipline where joins require `is_active = 'true'` and `is_level_active = 'true'` so stale rows drop out. The residual honest risk is silent data issues from the ETL, like a malformed currency string parsing to 0.0 in `parse_currency_display_to_float` or an active-flag drift making a line vanish with no error, which I would harden with validation and reconciliation alerts rather than trusting the upstream load.

---

## Confidence audit

Each resume bullet with a SOLID or NEEDS CARE verdict and the exact safer wording to fall back to if pressed. SOLID means it traces directly to code or a KT artifact. NEEDS CARE means it is a target, a framing, or partly outside my direct authorship and must be qualified.

**Bullet 1: Owned Uber's FRM Risk Scoping backend (Spring Boot, MySQL), 30+ REST APIs powering 8 screens, automating quarterly close at $340M group materiality, targeting a 70% cut in manual reconciliation (~2 weeks → ~3–4 days).**
- Backend ownership: SOLID. Screens are product surface powered by APIs — do not claim React/UI ownership.
- 30+ APIs: SOLID (~32 route registrations including health).
- $340M / 70% / timeline: MEASURED materiality sample; TARGET + ESTIMATED for 70% and days.

**Bullet 2: Owned Sheets → MySQL recon v2 (18 files), parallel /v2 APIs, L1→L2→L3 FSLI trees, HFM vs public 10-Q, durable line IDs for audit.**
- 18 files / dual-run / trees / 10-Q: SOLID (RECON_API_MIGRATION.md + code).
- Join/identity bug: verbal depth only; not required on PDF.

**Bullet 3: Automated in-scope decisions across ~55 line items × 14 entities via materiality, qualitative override, residual-risk, and 5% component-threshold logic against $340M / $170M.**
- 55×14 and thresholds: SOLID as Q4 2025 sample + encoded rules.
- Schema (11 models): supporting depth for interviews, not a separate PDF bullet.

**Bullet 4: Led 3 engineers on the FRM backend by owning API contracts and layered design reviews for Finance's quarterly scoping.**
- Led 3: SOLID headcount (EPAM pod tech lead). Do not center CI gates on the resume line.



**Cross-cutting NEEDS CARE items that span bullets:**
- Real-time collaboration, WebSockets, Optimistic Concurrency Control, and Slack notifications: NEEDS CARE. These are TDD design intent and largely live in the separate `frm-collaboration-service` and the frontend, not in my scoping-service code. Fallback: "the scoping service uses transactional per-uuid writes; real-time sync and version-check concurrency are the collaboration service and the client, which I did not author."
- Caching, Redis, and p95 latency: NEEDS CARE. No Redis or response cache in the shipped scoping service; only the memoized engine with `pool_pre_ping`. Fallback: "server-side, only the SQLAlchemy engine is cached; TanStack Query caching and the sub-second grid target are frontend design intent, and any p95 figure is a target, not a measurement."
- ETL from HFM: NEEDS CARE on ownership. Fallback: "the service consumes HFM-loaded MySQL tables; I owned the scoping APIs and the recon migration, the ETL pipeline was a shared responsibility."
- 19M GL rows: DROPPED, do not claim. Real scale is up to about 95K rows per quarter. If asked about volume, "this is a tens-of-thousands-of-rows correctness system, not big data."
- Coverage percentage: do not quote one for FRM; quote the 1,288 test-function count instead.
