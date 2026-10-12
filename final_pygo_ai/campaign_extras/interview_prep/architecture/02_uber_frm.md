# Architecture: Uber FRM Scoping Platform (Uber via EPAM)

<div class="callout note">
<b>How to use this page</b>
<ul>
<li><b>What it covers:</b> the FRM (Financial Risk Management) scoping backend I owned at Uber Finance via EPAM. That means the FastAPI service, the MySQL schema, how one edit flows through it, and how the quarterly close runs.</li>
<li><b>When to read it:</b> before system design rounds that touch data modelling, concurrency or correctness, and before any "tell me about Uber" question.</li>
<li><b>What to memorise:</b> the six-box diagram, the PATCH request with the version check, and the three numbers: 70% (from 14 days to 3 days), $340M materiality, 36 endpoints.</li>
</ul>
</div>

**Tags on this page.** MEASURED means there is a log, a doc or code. ESTIMATED means arithmetic I can show. TARGET means a design goal (say "targeting"). HISTORICAL means from past work records.

**Stack on this track (PyGo):** Python, FastAPI, SQLAlchemy 2.0, Pydantic, MySQL, Bazel, Docker.

---

## 1. The one-paragraph version

Every quarter, Uber's finance team must decide which accounts and which legal entities the auditors (PwC) need to test. That decision is called **scoping**. Before this project it lived in a large Google Sheets workbook with manual formulas, no stable row IDs, no audit trail, and people overwriting each other during the close. I owned the backend that replaced it: a FastAPI service with **36 endpoints** on a normalized MySQL schema, migrating **19M raw GL rows** off Sheets. It automates the financial math, models a 4-level account hierarchy, and keeps an auditable history. The close-related reconciliation work went **from 14 days to 3 days, a 70% cut**, against a **$340M materiality threshold**.

---

## 2. Words you need

- **FRM (Financial Risk Management).** The finance function that decides where the risk of a misstatement in the financial statements is, and therefore what auditors should test.
- **Scoping.** Choosing which accounts and entities are "in scope" for audit testing. Like a teacher deciding which chapters will be on the exam.
- **Materiality.** The size of error that would matter to someone reading the financial statements. Here it was **$340M** for the Q4 2025 close. Anything bigger than that cannot be ignored.
- **Residual risk.** The part of the balance that is not covered by the in-scope items. On the Q4 2025 close the residual threshold was **$170M**.
- **GL (general ledger).** The master list of every accounting entry, by account and entity. Think of the company's full bank statement for every account.
- **FSLI (Financial Statement Line Item).** A line on the balance sheet or income statement, such as "Cash" or "Accounts receivable". FSLIs nest in a hierarchy, here **4 levels, L1 to L4** (for example L1 "Current assets", L2 "Cash and equivalents", down to more detailed lines).
- **HFM (Oracle Hyperion Financial Management).** The consolidation system where entity trial balances are loaded, converted to one currency and combined into group numbers.
- **10-Q.** The quarterly report a US public company files with the SEC (Securities and Exchange Commission). Its numbers are the publicly attested truth.
- **Reconciliation.** Checking that two sources agree, here HFM numbers against the filed 10-Q, line by line. `difference = HFM amount − filed amount`. Like matching your own budget spreadsheet to your bank statement.
- **SOX (Sarbanes-Oxley).** US law that requires companies to have controls over financial reporting. Practically: every change must be traceable and controlled.
- **EMI (Equity Method Investment).** A company Uber partly owns and accounts for by its share of profit or loss. It has its own scoping screen.
- **Quarter-annualization.** Converting a figure for part of a year into an annual figure so it can be compared with annual thresholds. The general idea: a year-to-date number after two quarters is scaled up to a full-year equivalent. "Dynamic" means the scaling depends on which quarter you are in.
- **SOADB.** Uber's standard for service-owned relational databases: MySQL on InnoDB. InnoDB gives ACID transactions (all-or-nothing writes that stay consistent).
- **Normalized schema.** Each fact stored once, in its own table, linked by keys, instead of copying the same data into many places. Like keeping one contacts list instead of writing a friend's number in every notebook.
- **ORM (object-relational mapper).** A library that maps database rows to Python objects. **SQLAlchemy 2.0** is the ORM here. 2.0 brought a more explicit, typed query style.
- **Pydantic.** A Python library that validates request and response data against typed models. If a field is the wrong type, the request is rejected at the door.
- **Natural key.** An ID derived from the data itself rather than a random number. Here, a **SHA-256** hash of meaningful fields, so the same question on the same page always gets the same ID.
- **Optimistic row-locking.** Each row has a version number. An update only succeeds if the version is still what you read. If someone else saved first, your update affects zero rows and you get a conflict instead of silently overwriting. Like a shared document that warns "this was changed since you opened it".
- **Polymorphic review-status model.** One status model reused across many screens. Every screen's rows move through the same states: **Draft, Review, ReOpen, Closed**.
- **FSM (finite state machine).** A fixed set of states and allowed transitions. "Draft can go to Review, Review can go to Closed or ReOpen", and nothing else.
- **Bazel.** Uber's monorepo build and test system. **Stacked PRs** are a chain of small pull requests, each building on the previous, so each can be reviewed and shipped safely.
- **Statement coverage.** The percentage of code lines executed by tests.

---

## 3. The architecture diagram

```mermaid
flowchart LR
  UI["React finance screens, 8 pages"]
  GW["Uber gateway, injects user identity header"]
  H["FastAPI handlers, 36 endpoints"]
  S["Service layer: scoping math, FSM gates"]
  R["Repository layer: SQLAlchemy 2.0"]
  DB["MySQL on SOADB: 8-table normalized schema"]
  ETL["Shared ETL from Oracle HFM"]
  TENQ["Filed 10-Q figures"]
  COL["Separate collaboration service, not mine"]
  PWC["PwC audit work papers"]

  UI --> GW
  GW --> H
  H --> S
  S --> R
  R --> DB
  ETL --> DB
  TENQ --> S
  UI -.-> COL
  DB --> PWC
```

*What to notice: a classic three-layer service (handler, service, repository) on one transactional database. The ETL from HFM and the collaboration service are shared or separate pieces. I owned the scoping service in the middle.*

---

## 4. Box-by-box walkthrough

### React finance screens (8 pages)
The UI finance managers use. The 8 screens are Reconciliation, Materiality, EMI Scoping, Group Scoping, Threshold Setup, Component Scoping, Residual Risk and Summary. Each screen reads and edits rows through the API. I describe the UI as context; my ownership is the backend.

### Uber gateway
Authenticates the user and injects their identity as a header (for example `x-auth-params-email`). The service writes that email into `created_by` and `updated_by` columns, so every change is attributable. That matters for SOX.

### FastAPI handlers (36 endpoints)
The HTTP layer. Each handler validates input with Pydantic, calls the service layer, and returns typed responses, including nested trees for the L1 to L4 hierarchy. If asked for the breakdown: about 31 functional routes live in the scoping service handler, and the comment and notification APIs specified in the technical design doc (TDD) for the collaboration service make up the rest of the 36.

Why FastAPI: it was the Python service norm in this part of the monorepo, it validates with Pydantic at the boundary, and it generates API docs automatically. The ORM calls were synchronous, so handlers ran them off the event loop with `asyncio.to_thread`.

### Service layer
Where the finance logic lives:
- Group scoping: a line is significant if it passes the quantitative test (compared with materiality) or a qualitative test.
- Component scoping: drills into entities under each FSLI, using a 5% significance threshold.
- Residual risk: computes the balance not covered by in-scope items and compares it with the residual threshold.
- Quarter-annualization for comparisons against annual thresholds.
- **FSM gates**: allowed status transitions only, plus a **50% delta-variance check**. If a line moves by more than half compared with the prior period, the automatic transition is blocked and the line is flagged. This is a SOX control.

### Repository layer (SQLAlchemy 2.0)
All database access goes through repositories. The **ORM migration** I led (with 3 engineers) moved this layer to SQLAlchemy 2.0 style with explicit aliased joins and labelled columns. That removed a class of column-aliasing bugs (explained below) and brought module statement coverage to **100%**.

**Reporting SQL allowlists:** reporting queries can only run from an approved list, so nobody ships an ad hoc query against financial tables.

### MySQL on SOADB (8-table normalized schema)
The system of record. The schema stores the hierarchy, the per-quarter balances, the reconciliation leaves, thresholds, questionnaires and assessments. Key properties:
- **Fiscal period keys** on every fact row (`fiscal_quarter`, `fiscal_year`) with composite indexes.
- The ETL flattens the recursive FSLI tree into a stable `level_id` in a mapping table, so the API joins facts to a level ID instead of walking a tree in SQL.
- **Optimistic row-locking** through a version check on update.
- **Atomic cross-table syncs:** when one edit must change rows in several tables, it happens in one transaction. Either all change or none.
- **SHA-256 natural keys** so re-imported data updates in place instead of duplicating.

If someone has seen the code and asks why there are 11 ORM models: the resume number is the 8-table normalized schema in the bullet. Keep the answer at that level and do not invent a table-by-table mapping.

### Shared ETL from Oracle HFM
HFM extracts land in MySQL for each fiscal period. The ETL was a shared pipeline responsibility. Do not claim you built it alone.

### Filed 10-Q figures
The reconciliation screen compares HFM amounts with the public 10-Q line amounts, so scoping is built on numbers that match what went to the SEC.

### Separate collaboration service
Comments, notifications and Slack alerts live in a separate service. I did not build it. Scope your ownership to the scoping service.

### PwC audit work papers
The Summary screen and the stored history feed the auditors. Stable row IDs mean an auditor's comment points at the same line every quarter.

---

## 5. One request, step by step: a manager moves a line to Review

**Example.** A finance manager on the Group Scoping screen marks the "Cash and equivalents" line for Q4 2025 as in scope and moves it from Draft to Review.

```mermaid
sequenceDiagram
  participant UI as Group Scoping screen
  participant H as FastAPI handler
  participant S as Service layer
  participant DB as MySQL
  UI->>H: PATCH group balance sheet line, status Review, version 3
  H->>H: Pydantic validates body and reads user email header
  H->>S: update request
  S->>S: FSM check, Draft to Review is allowed
  S->>S: delta check against prior quarter, under 50 percent
  S->>DB: BEGIN, UPDATE where uuid and version 3, write audit columns, COMMIT
  DB-->>S: 1 row updated, version now 4
  S-->>H: updated line
  H-->>UI: 200 with new state
```

1. The browser sends a PATCH with the new status, the scoping conclusion and the version it last read (3).
2. Pydantic rejects the request if the status is not one of Draft, Review, ReOpen, Closed.
3. The service checks the FSM: Draft to Review is allowed. Closed straight back to Draft would not be.
4. The service runs the delta-variance check. Illustrative numbers: last quarter $1,000M, this quarter $1,200M, a 20% move. That is under 50%, so the gate passes.
5. The repository runs one transaction:

```sql
UPDATE group_balance_sheet
SET group_status = 'Review', conclusion_scope = 'In scope',
    version = version + 1, updated_by = :email, updated_at = NOW()
WHERE uuid = :uuid AND version = :expected_version;   -- expected 3
```

6. One row changed, so it commits. If another manager had saved first, the version would already be 4, zero rows would change, and the API would return a conflict instead of silently overwriting.
7. The UI shows the new state, and the audit columns record who did it.

### The quarterly close, as one job

1. HFM extracts land in MySQL for the fiscal period (shared ETL).
2. Reconciliation ties HFM to the 10-Q line by line and shows every non-zero difference.
3. Materiality and thresholds are set: **$340M** materiality, **$170M** residual for Q4 2025.
4. Group scoping marks significant FSLIs. Component scoping drills into entities under each.
5. Residual risk computes what is still uncovered. EMI scoping handles part-owned investees.
6. Summary rolls up coverage for PwC.

---

## 6. Design decisions

### Decision 1: move the close off Google Sheets into a normalized MySQL schema
- **What:** an 8-table normalized schema on SOADB replaces the workbook.
- **Why:** Sheets has no stable row IDs (so no comments or audit history per line), no concurrency control, and no way to model a recursive hierarchy safely. Versions drift between copies. Finance had ETL lock contention during the close.
- **Alternatives:** keep Sheets with Apps Script (no real concurrency control), or use a columnar warehouse (built for scans, not transactional edits).
- **Trade-off:** more upfront schema design, and a migration with a parallel run.
- **What I'd do differently:** build the parallel-run comparison report as a first-class feature from day one, not as a side script.

### Decision 2: optimistic row-locking instead of pessimistic locks
- **What:** a version check on every update.
- **Why:** many managers read and few collide on the same line. Holding row locks while someone thinks in the UI would block others.
- **Alternatives:** `SELECT ... FOR UPDATE` (pessimistic). Safe, but locks pile up during the close.
- **Trade-off:** the UI must handle a conflict response and ask the user to reload.
- **What I'd do differently:** return the current row with the conflict so the UI can show a diff.

### Decision 3: SHA-256 natural keys
- **What:** for example `uuid = SHA-256(question_text + normalized page_name)` for scoping questions.
- **Why:** quarterly re-imports of the same data must update rows, not create duplicates across audit trails.
- **Alternatives:** random UUIDs plus a uniqueness constraint on several columns. That works, but the ID is not reproducible from the data.
- **Trade-off:** if the source text changes (even a typo fix), the key changes. Normalising the inputs first reduces that.

Tiny example (teaching sketch):

```python
import hashlib

def question_uuid(question_text: str, page_name: str) -> str:
    key = f"{question_text.strip()}|{page_name.strip().lower()}"
    return hashlib.sha256(key.encode()).hexdigest()

question_uuid("Is the balance subject to significant estimates?", "Group Scoping")
# same input next quarter gives the same id, so the upsert updates in place
```

### Decision 4: one polymorphic review-status model across screens
- **What:** Draft, Review, ReOpen, Closed, shared by every screen.
- **Why:** one set of FSM rules, one set of tests, one audit format.
- **Alternatives:** a separate status column and rules per screen. Faster to start, but rules drift.
- **Trade-off:** a screen with special needs has to fit the shared model.

### Decision 5: lead an ORM migration to SQLAlchemy 2.0
- **What:** move the repository layer to explicit SQLAlchemy 2.0 queries with aliased joins and labelled columns.
- **Why:** a real bug. A raw SQL join returned two columns with the same name. The code built a dictionary from column names, so the second value silently overwrote the first, and some rows were mapped to the wrong uuid.
- **Alternatives:** patch each raw query by hand. Fixes today's bug, not the class of bugs.
- **Trade-off:** a migration across many modules, which needed tests first. That is why coverage reached 100% for the module.
- **What I'd do differently:** add a lint rule that rejects raw SQL with unlabelled duplicate column names.

### Decision 6: zero-downtime releases through stacked Bazel PRs
- **What:** each change is a small PR in a stack. Schema changes ship before code that depends on them.
- **Why:** finance cannot have the tool down during the close.
- **Trade-off:** more PRs to coordinate and review.

---

## 7. The numbers on this diagram

| Number | What it measures | Tag |
|---|---|---|
| 70%, from 14 days to 3 days | Quarterly reconciliation time | On PDF |
| $340M | Group materiality threshold, Q4 2025 close | On PDF |
| 19M | Raw GL rows migrated off Sheets | On PDF |
| 36 | API endpoints | On PDF |
| 4 levels, L1 to L4 | FSLI hierarchy depth | On PDF |
| 8 | Tables in the normalized schema | On PDF |
| 3 engineers | People I led on the ORM migration | On PDF |
| 100% | Module statement coverage after the migration | On PDF |
| 50% | Delta-variance threshold in the FSM gates | On PDF |
| $170M, 5% | Residual threshold and component significance threshold | Verbal |
| 1,100+ | Tests in the suite | Verbal |

**70% (from 14 days to 3 days).** It measures how long the quarterly reconciliation took before and after. It mattered because the close is time-boxed, and every day spent on manual tie-outs is a day not spent on analysis. Say it as "we cut quarterly reconciliation from 14 days to 3 days, about 70%". If someone does the arithmetic: 14 to 3 is actually about a 79% cut, because (14 − 3) / 14 ≈ 0.79. The 70% headline is the figure the technical design doc framed, so the resume understates rather than overstates. If pressed on source, say "the technical design doc framed that cut and that is what the platform delivered for the close". Do not walk it back unprompted.

**$340M materiality.** It is not a volume metric. It is the threshold that drives the scoping rules. Say "against a $340 million materiality threshold".

**19M raw GL rows.** It is the total migrated off Sheets. Individual quarterly GL extracts were about 38K to 95K rows, about 1.7K to 1.8K accounts and about 400 entities. If asked, say "the value was correctness, hierarchy and auditability, not big-data throughput". Do not invent a breakdown of where 19M comes from beyond "raw GL rows migrated off Sheets".

**36 endpoints.** About 31 functional routes in the scoping service plus the comment and notification APIs from the TDD. Older prep said "30+ endpoints, do not say 36". That guidance is obsolete. The current resume says 36.

**3 engineers.** I was tech lead of an EPAM pod, not a people manager. Never add this to "mentored 2" from Masters India.

---

## 8. Failure modes and what the system does

| What breaks | How you notice | What happens |
|---|---|---|
| Two managers edit the same line | Update affects 0 rows | Version check fails, API returns a conflict, nobody's change is silently lost. |
| An edit must touch several tables and one write fails | Exception inside the transaction | Whole transaction rolls back. No half-applied edit. |
| Same data re-imported next quarter | Same SHA-256 key | Upsert updates in place, no duplicates. |
| Large unexpected swing in a line | Delta over 50% | FSM gate blocks the automatic transition and flags the line. |
| Joined raw SQL with duplicate column names | Wrong uuid on rows (the real bug) | Fixed by the ORM migration: aliased joins and explicit labels. |
| HFM and 10-Q do not tie | Non-zero difference on Reconciliation | Shown and commentable on every line. Managers clear breaks before sign-off. The tool makes breaks visible. Humans do the sign-off. |
| Ad hoc reporting query | Not in allowlist | Rejected. |
| Bad release during close | Tests and staged PRs | Small stacked PRs, 100% module coverage, rollback is one small PR. |

---

## 9. Verbal depth (not on the PDF, true)

- **Sheets to MySQL reconciliation, v1 to v2.** Version 2 endpoints ran in parallel beside version 1. The change touched 18 files, +1,268 lines of code. Stable IDs unlocked per-line comments. Cutover happened after staging parity.
- **The column-aliasing bug.** A join of the fact table and the level mapping table returned columns with the same name. The code zipped column names to values, so the last one won, and rows got the wrong uuid. Fix: SQLAlchemy `aliased()` and an explicit `.label()` on every projected column.
- **Q4 2025 sample:** about 55 line items and 14 entities in scope (MEASURED in older prep).
- **Tests:** the suite grew past 1,100 tests because every PR had to add or update tests in the matching folder. CI ran five layer targets (database, schema, repository, service, handler).

---

## 10. Say this, not that

| Say this | Not this |
|---|---|
| "Uber via EPAM." | "I worked at Uber" without EPAM. |
| "I owned the scoping backend." | "I built the collaboration and Slack service." |
| "The HFM ETL was a shared pipeline." | "I built the whole data pipeline." |
| "Led 3 engineers as tech lead of an EPAM pod." | "I managed a team" or "led 5". |
| "36 endpoints." | "30+ endpoints" (obsolete prep). |
| "Value was correctness and auditability." | "Big data at 19M rows per quarter." |

Say this carefully about optimistic locking. Older prep notes said version-check concurrency lived in the collaboration service. The current resume claims optimistic row-locking in the schema. If pressed, explain the mechanism (version column, conditional UPDATE, conflict on zero rows) and keep the scope to the scoping tables.

---

## 11. How to draw it in 3 minutes

**Minute 1: the problem and the spine.** Write "Google Sheets close, 14 days" on the left and cross it out. Draw UI, gateway, FastAPI, MySQL left to right. Say: "Uber's quarterly scoping lived in Sheets: no stable IDs, no audit trail, people overwriting each other. I owned the FastAPI backend that replaced it, 36 endpoints on MySQL on Uber's SOADB standard, and we migrated 19 million raw GL rows off Sheets."

**Minute 2: inside the service.** Split the FastAPI box into handler, service, repository. Say: "Handlers validate with Pydantic. The service holds the finance math: materiality at $340 million, the L1 to L4 FSLI hierarchy, quarter-annualization, and a state machine with a 50% delta-variance gate for SOX. The repository is SQLAlchemy 2.0. I led 3 engineers on that migration, which killed a column-aliasing bug and took module coverage to 100%."

**Minute 3: the data guarantees.** Draw the 8 tables as a stack under MySQL and write three words next to them: "version", "transaction", "SHA-256". Say: "Every update checks a version, so two managers cannot overwrite each other. Cross-table edits are one transaction. Natural keys are SHA-256 of the meaningful fields, so re-imports never duplicate. The result was reconciliation from 14 days to 3 days." Add HFM and 10-Q arrows into reconciliation and a PwC arrow out of Summary to finish.

---

## Related

- Full FRM deep dive: [../projects/02_frm_deep_dive.md](../projects/02_frm_deep_dive.md)
- Uber FRM and Menu interview pack: [../projects/02_03_uber_frm_menu.md](../projects/02_03_uber_frm_menu.md)
- Python and FastAPI depth: [../tech_depth/python_fastapi.md](../tech_depth/python_fastapi.md)
- Postgres, MySQL and Redis depth: [../tech_depth/postgres_mysql_redis.md](../tech_depth/postgres_mysql_redis.md)
