# 11. Uber FRM Risk Scoping Platform: Deep Dive

Defense material for the four Uber FRM resume bullets. Every number here traces to `GROUND_TRUTH.md` or to the code in `KNOWLEDGE-MATERIAL/UBER-WORK/FRM PROJECT/frm_scoping_service/`. Tags: **MEASURED** (documented artifact or code), **TARGET** (design goal, say "targeting"), **ESTIMATED** (derived, say so). No number here is invented.

Role framing: Software Development Engineer 2 at Uber Finance via EPAM Systems, Jul 2024 to May 2026. This was Uber's internal monorepo (Bazel, Fusion.js, SOADB MySQL, langfx FastAPI framework).

---

## 0. The four bullets I am defending

1. Built Uber's quarterly FRM Risk Scoping platform (FastAPI, MySQL, React) replacing a manual Google Sheets workflow across **8 screens and 30+ REST endpoints**, scoping output feeding **PwC audit work papers at $340M group materiality**, targeting a **70% cut** in manual ingestion and reconciliation effort per close.
2. Designed the **11 table SQLAlchemy 2.0 MySQL schema** behind a layered **handler / service / repository** architecture with header based auth middleware.
3. Owned the migration of reconciliation from Sheets backed v1 APIs to **MySQL backed v2 APIs**, validating HFM vs public **10-Q** amounts, and fixed a latent **column aliasing bug** surfaced during the ORM move.
4. **Led a pod of 3 engineers**; grew the service to **1,100+ pytest unit tests** under Bazel with mocked handler and repository suites gating CI.

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

"At Uber Finance I built the FRM Risk Scoping platform, a FastAPI + MySQL + React tool that replaced a manual Google Sheets close for the quarterly scoping process, the activity that decides which financial line items and entities are in scope for PwC's audit. It is 8 screens and 30-plus REST endpoints over an 11-table SQLAlchemy 2.0 schema, in a strict handler / service / repository layering with header-based auth. On the Q4 2025 close, group materiality was $340M. The project's goal was targeting a 70% cut in manual ingestion and reconciliation time. I personally owned migrating reconciliation from Sheets-backed v1 APIs to MySQL-backed v2 APIs, running both in parallel and validating HFM against the filed 10-Q, and I fixed a latent column-aliasing bug where joined tables produced duplicate result-key names and silently mapped rows to the wrong identity, by moving to SQLAlchemy aliased selects with explicit labels. I led a pod of 3 engineers and we grew the service to 1,100-plus pytest tests gated by Bazel CI."
