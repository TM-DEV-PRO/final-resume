# Uber (via EPAM Systems) — Financial Risk Management (FRM) Scoping Platform

**Role:** Software Engineer · July 2024 – May 2026 · Bangalore
**Resume tech line:** Python, FastAPI, SQLAlchemy, Pydantic, MySQL, Bazel, pytest, ruff, Redis, React (integration)

---

## 1. Elevator pitch

"I built the backend for Uber's Financial Risk Management quarterly scoping tool — the system that decides which financial statement line items get audited each quarter. It replaced a Google-Sheets workflow with a FastAPI + MySQL service used by FRM managers; the output is the audit work paper PwC reviews. Get scoping wrong and you either over-pay PwC (~$500K per audited product line) or under-audit and risk an audit finding."

## 2. What it does — the 8 screens

Quarterly SOC compliance walks the reviewer through 8 screens in order:

1. **Reconciliation** — confirm raw Oracle HFM amounts match the public 10-Q (read-only)
2. **Materiality** — set the dollar threshold (Q4 2025: $340M)
3. **EMI Scoping** — Equity Method Investments, special-cased user-input data
4. **Group Scoping** — line-by-line significance decision for ~29 income-statement + ~26 balance-sheet FSLIs
5. **Threshold Setup** — entity-level (UTI, Careem, Freight, …) significance by % of group revenue/assets
6. **Component Scoping** — which entities to audit per FSLI (most complex screen)
7. **Residual Risk** — the un-scoped remainder, QoQ comparison
8. **Summary + Coverage** — final dashboard, in-scope % at L1/L2

## 3. Architecture

```
React / Fusion.js SPA (BaseWeb virtual-scroll grid, TanStack Query)
        │ REST/HTTPS
        ├──────────────────────┬─────────────────────────┐
        ▼                      ▼                          │
frm-scoping-service      frm-collaboration-service        │
(FastAPI, 20 endpoints)  (FastAPI, 16 endpoints:          │
        │                 comments, threads, Slack DM)    │
        ▼                      ▼                          │
frm-scoping-db           frm-collaboration-db             │
(MySQL/SOADB, 8 tables)  (MySQL/SOADB)                    │
        ▲                                                 │
        │ quarterly ETL (manual HFM extract + 4 mapping CSVs,
        │ pandas transform, LAG() QoQ, 10-Q reconciliation)
   Oracle HFM  ~19M raw GL rows/quarter → ~300K aggregated rows
```

**Layering (strict, code-review enforced):** `handler/` (routes, DI, Pydantic models) → `service/` (business rules only) → `repository/` (SQLAlchemy sessions) → `database/` (ORM models). Handlers never call repositories; services never open sessions or import `HTTPException`; repositories never compute derived values. All DI via FastAPI `Depends()` factories.

**Why two services, not one?** Different write patterns (scoping is bursty-quarterly; collaboration is steady), lock isolation (comments must not contend with ETL writes), and reuse (collaboration serves other FRM apps). Tradeoff: cross-service joins happen in the React layer (BFF-style aggregation).

## 4. Database design (memorize — you will draw this)

8 core tables: `oracle_raw_data` → `income_statement` / `balance_sheet` → `component_entity`, `scoping_assessments` → `scoping_questions`; standalone `scoping_metrics`, `threshold_table`, `ui_review_status`.

Key decisions and their defenses:

- **Polymorphic `ui_review_status` (parent_uuid, table_source, screen_name)** — chosen over (a) wide columns on IS/BS (lock contention with ETL, bloats the PwC-exported table, doesn't scale to screen N+1) and (b) a JSON column (race conditions on partial updates, unindexable). Later added a 5th screen with zero schema change.
- **Deterministic UUIDs: `MD5(level_id + year + quarter)`** — idempotent ETL: re-running a quarter regenerates identical keys → clean UPSERTs, no duplicates. We need determinism, not cryptography.
- **`(fiscal_quarter, fiscal_year)` on every row** — all quarters in the same tables, never copied per quarter.
- **Prior-quarter amounts via SQL `LAG()`** window function partitioned by (entity, account, dept, icp, lob, location, currency, scenario, component) — single pass, no self-join.
- **`component_selection` as a space-separated string** — ~12 entities, never queried by containment, always rendered whole; a junction table would add a join per read for zero query benefit. Service-level validation enforces the allowed set.
- **Soft delete via `is_level_active='No'`** — PwC needs the audit trail; rows are never hard-deleted.

## 5. Tech choices — the "why this, not that" table

| Choice | Rejected | Why |
|---|---|---|
| FastAPI | Flask (previous version), Django REST | Pydantic-first validation, `Depends()` DI, free OpenAPI; Flask's stringly-typed dicts were the pain point; Django too heavy (no admin/ORM needed) |
| SQLAlchemy 2.x | raw SQL `text()` | Type-safe, refactor-safe column refs — raw SQL hid a real bug (`IS_SELECT` aliased to balance-sheet columns); team banned new raw SQL |
| MySQL (SOADB) | Postgres, Spanner, Dynamo | SOADB = Uber's managed MySQL: HA/backups/secrets free; Spanner overkill at ~10 RPS; Dynamo wrong shape (hard FK invariants) |
| Optimistic locking | Pessimistic row locks | Reviewers think in minutes; held locks would block readers. Compare-and-set on `updated_at`; conflict → "stale row, refresh" |
| Redis 24h TTL (heavy reads) | app memoization | Financial data changes once a quarter; UI status reads through directly |
| Bazel + gazelle, `arh` stacked PRs, ruff, pytest+MagicMock | pip/setuptools, mega-PRs | Monorepo standard; stacked PRs made the 3-step refactor reviewable |

## 6. The work I lead with

1. **ORM migration + coverage story.** Moved 4 raw-SQL functions for group-income-statement APIs into classmethods on the `IncomeStatement` ORM model. Coverage check first failed at 34.6% because repository tests stubbed the new classmethods — coverage wasn't credited where the code lived. Fixed with 12 direct model-layer unit tests → 100% on the changed module. Lesson: mocking shifts coverage; test where the code lives.
2. **The constants refactor regression.** Consolidating 31 files of duplicated constants into one screen-prefixed `constants.py`, a "pure refactor" PR accidentally introduced a `_resolve_strategy` helper that downgraded COMPONENT→AGGREGATE when selection was empty. A downstream regression test caught it. Lesson: a pure-refactor PR must produce zero test diff.
3. **Stacked PRs.** 3 logical changes touching the same files: imports → constants → ORM. One mega-PR is unreviewable; three independent PRs conflict. `arh feature` / `arh rebase --sync` / `arh publish` landed them independently.

## 7. Q&A bank (fast answers)

- **Scale to 100 teams?** Shard by team/fiscal-quarter range, SOADB read replica for heavy reads, Redis read-through 24h TTL, queue the Slack fan-out.
- **Bad ETL data?** Two nets: manual 10-Q reconciliation sign-off before scoping opens; Flipr feature flag to flip UI read-only. Silent corruption is the real risk — the reconciliation step exists for it.
- **Quarterly tool — why does latency matter?** Scoping runs in 1–2 day bursts post-earnings; the grid must stay conversational on 300K-row aggregated reads (BaseWeb virtual scroll, no pagination).
- **Why not GraphQL?** One internal client; schema-management cost without the flexibility benefit.
- **Why not Spark for ETL?** 19M rows/month is pandas territory; Spark adds infra for a problem we don't have.
- **Audit trail depth?** Every write logs `updated_by` (LDAP) + `updated_at`; status history in `ui_review_status`; comments immutable in the collaboration DB.

## 8. Numbers to keep straight

~19M raw GL rows/quarter → ~300K aggregated → 29 IS + 26 BS FSLIs · 36 endpoints (20 scoping + 16 collaboration) · 8 screens · ~12 entity components · $340M materiality (Q4 2025) · 10-Q reconciliation tolerance $2–3M · ETL script 10–15 min/quarter · coverage 34.6% → 100% · 31 files → 1 constants module · 3-PR stack.
