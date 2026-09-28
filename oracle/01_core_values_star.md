# 01. OCI core values: STAR answers for every value

Source: *OCI Interview Prep Pack* (11 core values + STAR method). Resume: PyGo track. Every story uses real work from the PDF or from your verified prep. Where a detail is verbal (not on the PDF), it says so.

<div class="callout note">
<b>How OCI scores this.</b> The pack says: choose real examples, give details (they are "a technical organization"), every answer needs a beginning, middle, and end, and be ready for follow-ups. Interviewers probe each STAR letter with the questions below. Aim for 2 minutes per answer: 15s Situation, 15s Task, 60s Action (with "I", not "we"), 20s Result with a number, 10s lesson.
</div>

---

## 0. The probes they will use (from the PDF)

| STAR part | What they will ask | Have this ready |
|---|---|---|
| **Situation** | What happened? How did this come about? Who was involved? What was the main issue? | Team size, your role, the system, the stakes (customer, money, deadline) |
| **Task** | What responsibility did you take on? Did your manager assign it? Did you take it on your own? Did others have tasks? | Say clearly what *you* owned vs others |
| **Action** | What did you do first? How did the person/situation respond? What did you do next? What were the alternatives? | Ordered steps, 1 rejected alternative and why |
| **Result** | What was the end result? Was your manager satisfied? Did you keep handling it over time? Were you given new responsibilities because of it? | Number, follow-up process change, what you owned next |

**Always prepare the "what next / new responsibilities" tail.** OCI asks it a lot. Real ones you have:
- After the ClickHouse POC, you owned the rollup tables, the Go pump, and the KPI configurator.
- After the FRM v2 recon migration, you led 3 engineers on the SQLAlchemy 2.0 migration.
- After the Masters strangler, you owned the bulk pipeline and mentored 2 engineers.

---

## 1. Story bank (learn these 14 names, map any question to one)

| # | Story name | Company | One line | Values it fits |
|---|---|---|---|---|
| S1 | **Timeout canary** | Masters India | My 10s timeout broke legit long IRP calls in canary; rolled back by config, moved to async 202 + polling | Own without ego, Take risks remain calm, Customers first |
| S2 | **Double-filing near-miss** | Masters India | Retry almost double-filed e-invoices; I flagged it, wrote the review, retrofitted idempotency + DLQ everywhere | Earn trust, Choose safety, Own without ego |
| S3 | **Strangler under deadlines** | Masters India | PHP monolith to FastAPI per endpoint with canaries and deadline freezes; p95 1.2s to 300ms, 1,500+ clients | Act now iterate, Expect change, Champion execution |
| S4 | **SSH-and-grep to ELK** | Masters India | Structured logs + request IDs + New Relic alerts; triage 70% faster, coverage 35 to 82%, 98% deploy success | Nail the basics, Take pride, Continuous improvement |
| S5 | **Sheets to SOX-grade MySQL** | Uber FRM (EPAM) | 14 days to 3 days recon at $340M materiality; 8-table SOADB, optimistic locking, SHA-256 keys | Customers first, Nail the basics, Choose safety |
| S6 | **Pure refactor that wasn't** | Uber FRM | My stacked PR smuggled a behavior change; caught, fixed, added "pure refactor = zero test diff" to checklist | Own without ego, Take pride, Earn trust |
| S7 | **Coverage that lied** | Uber FRM | 34.6% coverage despite tests; mocks hid the model layer; 12 direct tests to 100% | Nail the basics, Challenge ideas |
| S8 | **Rulebook disagreement** | Uber FRM | Argued classmethods on ORM models vs repository rule; documented exception, committed | Challenge ideas, Innovate together, Earn trust |
| S9 | **ClickHouse verdict** | Impact Analytics | Org split on ClickHouse; I separated facts from conclusions, ran row-identical POC: 189s to 12s on 250M | Challenge ideas champion execution, Innovate together |
| S10 | **170 GB weekly OOM** | Impact Analytics | Season weekly rollup OOM'd at 80 and 200 GB; sliced unit of work to one fiscal week with caps + spill | Take risks remain calm, Nail the basics |
| S11 | **64.1M half-loaded partition** | Impact Analytics | Failed HTTP INSERT committed blocks; "skip if rows exist" passed a partial partition; built TSV ledger + DROP PARTITION rebuild | Choose safety, Own without ego, Take pride |
| S12 | **Allowlist pump** | Impact Analytics | Cloud cluster-to-cluster pull blocked; wrote a Go native-TLS pump, ~344k rows/s combined, double buffer fixed EOF | Act now iterate, Take risks |
| S13 | **LLM lost to the rule** | Impact Analytics | Blended LLM ~63% < det 74% on gold-200; froze weights, gated promotion at 80% on 300 cases, picked model 73% cheaper at 100% coverage | Challenge ideas, Customers first, Choose safety |
| S14 | **No SQL tool, frozen scope** | Impact Analytics | LLMs get JSON payloads, never a SQL tool; Ask Iris freezes plan scope at JWT handshake, 3-attempt cap | Choose safety, Earn trust |
| S15 | **Anti-bot arms race** | Uber Eats (EPAM) | Scraper success ~60% to 95%+ via per-source block signatures, proxy pools, retry budgets | Act now iterate, Expect change |
| S16 | **Mentoring two engineers** | Masters India | Set layering conventions, reviewed every PR, paired on first canary; both shipped services independently | Innovate together, Give trust |
| S17 | **KPI configurator** | Impact Analytics | Operators author formulas; tokenizer compiles to parameterized CH SQL with ifNotFinite; no deploy per formula | Customers first, Innovate together |

---

## 2. Put customers first

> "We put doing the right thing for customers ahead of doing what they specifically say or ask for. When faced with a choice between what is easy for us and what is good for customers, customers win every time."

**Likely questions**
- Tell me about a time you did what was right for the customer even though it was not what they asked for.
- Tell me about a time you pushed back on a customer or stakeholder request.
- How do you find out what customers really need?

### Primary: S13 LLM lost to the rule (what they asked for vs what was right)

- **S:** At Impact Analytics, AssortSmart planners at retail clients decide which articles to keep or drop each season. Product wanted the Keep/Drop engine to "use AI" for the final call. We score 348k article-seasons, 88k per pass, across 7 AI lenses.
- **T:** I owned the evaluation and promotion path: which model scores live, and how LLM lenses blend with the deterministic KPI score.
- **A:**
  1. Built a 300-case proxy eval harness and made 80% accuracy a CI gate, so no model or prompt change ships without passing it.
  2. Benchmarked models on a gold-200 set against the deterministic baseline, which scored 74%.
  3. The blended LLM scored around 63%, *below* the free rule. The easy move was to retune blend weights on 200 cases until it looked good. I argued that was overfitting a small proxy and would hand planners worse decisions labeled "AI".
  4. Froze the blend weights, kept the LLM lenses for qualitative reasoning the planner sees, and picked the model that completed 200/200 at 73% lower cost than the incumbent.
- **R:** Planners got decisions no worse than the baseline, with AI explanations on top, at 73% lower live cost and 100% coverage. Promotion stays behind the 80% gate. Lesson: the customer asked for "AI", but what they need is correct decisions.
- **Follow-ups**
  - *Did product agree?* I showed the numbers side by side (74 vs ~63) and framed it as protecting planners' trust in the tool. We agreed to revisit weights when the eval set is larger.
  - *Is 80% the live accuracy?* No. 80% is the CI promotion gate on the 300-case file. 73% cost cut and 74% baseline are gold-200. I keep those separate.

### Backup: S1 Timeout canary (async 202 instead of the sync call clients asked for)

- **S:** Masters India, GST e-invoicing SaaS, 1,500+ enterprise clients. Clients wanted "faster synchronous submit." During the FastAPI migration I set a 10s timeout on the new submit path. The PHP path had 60s.
- **T:** I owned the submit endpoint cutover.
- **A:** In canary, error rate rose on a small slice. I rolled back by gateway config (no deploy). The logs showed some government IRP calls legitimately take longer than 10s. Raising the timeout would just hold workers hostage again. Instead I moved IRP registration fully async: return **202 Accepted** with a status URL, process in workers with retries and idempotency keys, and push status to the dashboard.
- **R:** Clients never saw failed submits from slow IRP calls, and p95 on the API went from 1.2s to 300ms. It was not what clients literally asked for, but it was what they needed on filing deadline days.

---

## 3. Act now, iterate

> "A grungy solution now is superior to no solution at all. We keep it simple. We don't discuss endlessly, and we are scientific in our approach. We offer solutions, not problem statements."

**Likely questions**
- Tell me about a time you saw a gap and filled it without being asked.
- Tell me about a time you shipped something imperfect and then improved it.
- Tell me about a time you moved fast with incomplete information.

### Primary: S12 Allowlist pump

- **S:** At Impact Analytics we needed season partitions of the new ClickHouse rollup tables copied between two ClickHouse Cloud clusters. Cluster-to-cluster pull was blocked by Cloud IP allowlists. Waiting on network changes meant blocking planner reads on the new tables.
- **T:** Nobody owned "move billions of rows between clusters." I took it on.
- **A:**
  1. Grungy first: a Go process on an allowlisted operator machine that SELECTs from source and INSERTs to target over native TLS. Unit of work is one `season_code` partition. A per-table checkpoint file marks finished seasons, and a file lock stops two terminals copying the same table.
  2. First version used HTTP and hit `unexpected EOF`: the SELECT stream sat idle while the INSERT ran. I iterated to **double buffering**: two 500k-row columnar buffers, so reading the next batch overlaps sending the previous one. No per-row reflection.
  3. Made failure boring: on an incomplete season, DROP PARTITION and recopy. SIGINT finishes the in-flight batch and does *not* checkpoint that season.
- **R:** About **344k rows/s combined** at a live snapshot with two season workers, measured on a 4.09B-row attr weekly table. I say "measured on," not "migrated." The copy was still in flight at that snapshot. Lesson: ship the simple safe version, then let measurements tell you what to fix.
- **Follow-ups**
  - *Why not wait for the proper path?* The proper path is allowlist and `INSERT SELECT` server-side, or object storage. I said so in the doc. The pump was a workaround with a clear retirement plan.
  - *What is the biggest risk?* No atomic swap. A crash leaves a truncated season until DROP + retry. Readers can see a partial season.

### Backup: S4 SSH-and-grep to ELK (see Nail the basics), or S15 Anti-bot (experiment loop)

S15 short form: Uber menu scrapers were getting blocked as sites rotated bot defenses. I treated it as an experiment loop: instrumented per-source block signatures, iterated IP rotation, fingerprints, and proxy pools, set per-source retry budgets, and put block rate on the same dashboard as parse failures. Success went from about 60% to **95%+**, and new defenses got countered in days.

---

## 4. Nail the basics

> "We focus on fundamentals over flash... the path to advanced solutions always runs through the basics."

**Likely questions**
- Tell me about a time you found a fundamental gap and fixed it.
- Tell me about a time you chose a simple solution over a fancy one.
- How do you make sure your code is production ready?

### Primary: S4 SSH-and-grep to ELK + test coverage (Masters India)

- **S:** Masters India. On-call debugging meant SSHing into boxes and grepping logs. Test coverage was 35%. We were about to split a monolith into services, which makes both problems worse.
- **T:** I took ownership of observability and test discipline for the services I was migrating.
- **A:**
  1. Structured JSON logs with a **request ID** propagated across services and Celery workers, shipped to ELK. One ID follows an invoice from API to IRP call to webhook.
  2. New Relic APM traces plus alert rules on error rate and latency.
  3. pytest with coverage as a CI gate, prioritizing money paths first: registration, reconciliation, imports.
  4. During the rewrite, fixed boring things: composite index on `(client_id, invoice_date)`, removed N+1 queries, added pagination and connection pooling.
- **R:** Incident triage **70% faster**. Coverage **35% to 82%**. **98% deploy success**. The p95 win (1.2s to 300ms) came mostly from these basics plus async IO, not from anything exotic.

### Backup: S7 Coverage that lied (Uber FRM)

- **S:** My SQLAlchemy 2.0 ORM migration failed CI at **34.6%** new-line coverage even though I had tests for the paths.
- **T:** Find out why tested code showed as uncovered.
- **A:** Repository tests stubbed the new ORM classmethods with mock chains, so the model package never executed. I wrote 12 direct model-layer unit tests, including rejection paths (empty updates, unknown columns).
- **R:** **100%** on the changed module. "Test where the code lives, not where it is called" went into the team's testing notes. Lesson: a metric you don't understand will lie to you.

Third option for AI-heavy panels: **deterministic KPI math, never the LLM.** At 88k items the LLM gets pre-computed KPIs as JSON, and the formula compiler wraps every division in `ifNotFinite(..., 0)`. Correctness does not depend on the model.

---

## 5. Expect and embrace change

> "We value people who align quickly with current priorities, who have situational awareness, and who are willing to adapt... We do not hang on to outdated processes and goals."

**Likely questions**
- Tell me about a time priorities changed suddenly. What did you do?
- Tell me about a time you had to learn a new technology quickly.
- Tell me about a process you changed because it was outdated.

### Primary: Python to Go, Postgres to ClickHouse at Impact Analytics (S9 short + learning)

- **S:** I joined Impact Analytics as a Python engineer. The platform direction shifted to a **Go/Gin** API layer for throughput. Planner analytics also moved from Postgres to ClickHouse after pivots hit **189s at 250M rows**.
- **T:** Become productive in Go and in ClickHouse's very different write model fast enough to own production parts, not just follow.
- **A:**
  1. Learned Go by owning real parts: the Gin edge with nested context timeouts, **Google Wire** compile-time DI, h2c, and Datadog tracing.
  2. For ClickHouse, I learned the engine semantics before building: MergeTree parts, `ReplacingMergeTree` versioning, why `FINAL` is expensive, and partition pruning.
  3. Dropped the Postgres habits that don't fit (in-place UPDATEs) and designed insert-only versioned writes.
- **R:** The platform scales to **10k peak RPS**. I built the six rollup tables (15.5x, 189s to 12s), the KPI formula compiler, and a Go pump running ~344k rows/s. Lesson: learn the new system's model, don't port the old one.

### Backup: S3 Strangler under deadlines (priorities shift around GST deadlines)

At Masters we froze cutovers during GST deadline weeks and reordered the migration: bulk async paths first, interactive filing later, because deadline spikes were the pain. The plan changed every month based on the filing calendar. No deadline-window outage during the migration.

Or: **Uber FRM recon v1 (Google Sheets) to v2 (MySQL).** The team's tool had lived on Sheets. The finance close needed audit history and collaboration, so the old process had to go. I owned the v2 recon endpoints on MySQL while v1 kept serving, and the SQLAlchemy 2.0 migration followed.

---

## 6. Innovate together

> "We practice empathy and respect... We seek and celebrate the diverse perspectives... collaboration drives innovation. We provide the tools, processes, and resources to enable everyone."

**Likely questions**
- Tell me about a time you worked with people who thought very differently from you.
- Tell me about a time you helped someone else succeed.
- How have you made your team more effective?

### Primary: S16 Mentoring two engineers + S17 tooling for non-engineers

- **S:** Masters India strangler migration. Two junior engineers joined the migration. They had never extracted a service from a monolith.
- **T:** I owned the migration and was asked to grow them into independent owners, not just give them tickets.
- **A:**
  1. Wrote down the conventions once: router, service, and repository layers, Pydantic schemas at the boundary, shared retry and idempotency helpers. That way they didn't need to guess.
  2. Gave each an entire service extraction to own, not subtasks.
  3. Reviewed every PR in the first months with the "why", and paired on their first canary cutover.
- **R:** Both shipped services independently by the end. The conventions doc became how new services started.

### Backup: S17 KPI configurator (innovation with operators, not for them)

- **S:** At Impact Analytics, every new KPI formula a client wanted meant an engineering change and a release.
- **A:** Sat with the people defining formulas to see what they actually write. Then built a configurator with a Go tokenizer and parser. It has allowlisted functions, maps logical names to physical columns, and compiles to parameterized ClickHouse SQL with native division-by-zero protection.
- **R:** Operators author formulas without a code release. Business logic is decoupled from deploys.

Also: **S9 ClickHouse verdict.** Two expert camps disagreed. I accepted every measured fact from both and found the hidden assumption. Everyone agreed to a staged path.

---

## 7. Challenge ideas, champion execution

> "We ask why. We test the validity of ideas through rigor, research, and critical thinking... We own decisions. We drive effective implementation."

**Likely questions**
- Tell me about a time you disagreed with a technical decision.
- Tell me about a time you used data to change someone's mind.
- Tell me about a decision you owned end to end.

### Primary: S9 ClickHouse verdict, then execution

- **S:** Impact Analytics. Planner pivots on Postgres took **189s** at **250M rows**. The org was split. One audit of the legacy backend said "no ClickHouse" because updates are painful. Senior SMEs said "yes, unified OLAP."
- **T:** I owned the RFC and a recommendation the org could commit to.
- **A:**
  1. Asked why each side believed what they did. The audit's facts were right, but the "no" was a property of the legacy in-place-UPDATE write model, not of planning workloads.
  2. Proposed insert-only, versioned writes (`ReplacingMergeTree`), which sidesteps the mutation problem.
  3. Built a **row-identical** POC harness: same 250M rows, same query, both engines, same answers checked. No benchmarketing.
  4. Kept Postgres for OLTP (roles, config). Didn't dual-write "a religion."
- **Execution (the champion part):** Designed and built six ClickHouse rollup tables. Weekly grain hit a 170 GB OOM and I fixed it (see S10). Built the Go pump to move partitions.
- **R:** **15.5x** faster (189s to 12s on 250M). The org committed to ClickHouse for planning analytics. I went on to own the rollups, the KPI compiler, and the copier.
- **Follow-up trap:** *So the OOM fix made it 15.5x faster?* No. 15.5x is query time on the harness. OOM was load time. Different problems.

### Backup: S8 Rulebook disagreement (Uber FRM)

- **S:** Team rules at Uber said all data access goes in `repository/`. For the SQLAlchemy 2.0 migration I wanted query classmethods on the ORM models.
- **A:** Wrote the case: SQL next to column definitions means renames fail the type checker immediately. The motivating bug was raw SQL reading income-statement rows with balance-sheet column lists. Listened to the consistency argument, documented the exception, and committed to repository functions for dynamic multi-model queries.
- **R:** Exception accepted and documented. That class of column-aliasing bug could not recur.

---

## 8. Take risks, remain calm

> "We are logical and data-driven in assessing our risks. We react to unexpected situations by remaining calm, and then making and executing mitigation plans... learning from our failures is part of our path to success."

**Likely questions**
- Tell me about a production incident you handled.
- Tell me about a calculated risk you took.
- Tell me about a failure and what you learned.

### Primary: S10 170 GB weekly OOM

- **S:** Weekly-grain ClickHouse rollups for planners. A whole-season weekly `INSERT SELECT` needed ~110 `any()` states plus `argMax`/`argMin` over wide strings. Estimated aggregator state was around **170 GB**. It failed `MEMORY_LIMIT_EXCEEDED` at an 80 GB cap and again at 200 GB on a ~59 core / ~236 GiB replica.
- **T:** Keep weekly grain (planners need `fiscal_year_week`) without taking down the shared box.
- **A:**
  1. Stopped the reflex to raise memory. Profiled by grain: product week peaks were ~11 GB, attr weeks over 40 GB.
  2. Changed the **unit of work** from one season to **one fiscal week**.
  3. Generated per-build settings: 8 threads, 55 GB memory cap, 16 GB external spill, 4 weeks in flight. Rule: never raise season parallelism and week parallelism together on the same box.
- **R:** Weekly grain builds reliably, and the request path stays partition-pruned reads. Lesson: shrink the unit of work before buying RAM.

### Backup: S1 Timeout canary (calm rollback)

Error rate rose in canary. I didn't debug live on customer traffic. I rolled back by gateway config in minutes, then diagnosed from logs, then fixed the design (async 202). The risk was sized small because the canary percentage was small and rollback was config, not deploy.

**Calculated risk version:** S12 pump. Going through an operator machine was a risk. I sized it (no atomic swap, partial seasons visible), mitigated it (checkpoint ledger, DROP + recopy, flock, finish-batch-on-SIGINT), and wrote down the proper path.

---

## 9. Own without ego

> "We take responsibility for the state of our team, our products, and ourselves... We are the first to admit when we are wrong... We never say, 'That's not my job.'"

**Likely questions**
- Tell me about a mistake you made.
- Tell me about a time you took ownership of something outside your role.
- Tell me about feedback that changed how you work.

### Primary: S6 The pure refactor that wasn't

- **S:** Uber FRM (via EPAM). I split a refactor into 3 stacked Bazel PRs. PR 2 was supposed to be a constants-only consolidation across 31 files. A downstream test failed: it expected the COMPONENT strategy to be kept on empty selection and got AGGREGATE.
- **T:** It was my PR. I owned finding and fixing it.
- **A:** Diffed my own PR line by line. I had slipped in a `_resolve_strategy` helper that silently downgraded the strategy, a behavior change smuggled into a "refactor." I told the reviewers plainly, removed it, and restored pass-through. Then I added "pure refactor means zero test diff" to the team's stacked-PR checklist.
- **R:** Shipped as a true refactor. Weeks later the checklist caught a similar issue for a teammate. Lesson: call your own fouls fast and turn them into process.

### Backup: S11 64.1M half-loaded partition (owning a bug in my loader)

- **S:** My weekly rollup loader resumed with "skip a season if its partition already has rows."
- **A:** A failed HTTP INSERT in ClickHouse still commits the blocks it wrote. A **64.1M-row** half-loaded partition passed my "has rows" check and would have been served as complete. I owned it: replaced the check with a TSV ledger of finished `(kind, season_code)` pairs. Success now comes from `system.query_log` `QueryFinish`, not curl exit. A missing ledger entry means DROP PARTITION and rebuild.
- **R:** Resume became correct by construction. "Never use `count() > 0` as success" went into the failure catalog.

Also good: **not my job, did it anyway**: S12 (nobody owned the cluster copy).

---

## 10. Earn trust, give trust

> "We build trust by communicating openly and transparently... We learn from failures rather than seeking to place blame, and we don't invoke rank to convince others we are right."

**Likely questions**
- Tell me about a time you had to deliver bad news.
- Tell me about a time you trusted a teammate with something important.
- Tell me about a time you raised a problem you could have hidden.

### Primary: S2 Double-filing near-miss

- **S:** Masters India. A retried bulk import almost filed duplicate e-invoices with the government portal. For a GST compliance product, that is a serious error for the client. No customer was hurt yet, and nobody outside the team would have known.
- **T:** Decide between quietly patching one endpoint and treating it as a systemic risk.
- **A:**
  1. Flagged it to leadership as a near-miss the same day.
  2. Wrote the incident review myself, blameless, focused on the mechanism: retries without idempotency.
  3. Retrofitted idempotency keys (`client + file hash + batch index`, plus client invoice refs) across the **entire** bulk pipeline, not only the endpoint that almost failed.
  4. Added a dead-letter state so poison batches park for operator replay instead of retrying forever.
- **R:** Zero duplicate filings after rollout. The review became the team's template for later incidents. Lesson: trust is built in the moments where you could have stayed quiet.

### Give trust: S16 mentees owned whole services (see Innovate together)

I gave each junior an entire extraction, including the canary, instead of keeping the risky parts for myself. I kept a safety net (reviews, config rollback) and let them own it.

**Transparency on numbers (quick add):** I correct inflated numbers about my own work. "344k" is rows per second, not TPS. "80%" is a CI gate, not live accuracy across all tenants. Interviewers remember that.

---

## 11. Take pride in your work

> "We strive for excellence in all that we do... We identify work that needs to be done... and we communicate those goals well to the broader organization."

**Likely questions**
- What are you most proud of?
- Tell me about a time you went beyond "done."
- Tell me about a time you raised the quality bar for your team.

### Primary: S5 Sheets to SOX-grade MySQL (Uber FRM)

- **S:** Uber Finance's FRM team scopes which financial line items are in audit scope each quarter. The external auditor relies on the output. It ran on a Google Sheets workbook: manual parent-child mapping, no history, no audit trail. Reconciliation took **14 days**. Group materiality was **$340M**.
- **T:** I owned the scoping backend.
- **A:**
  1. Moved from Sheets to MySQL across **19M** raw GL rows. Built **36 FastAPI endpoints** over a nested **L1 to L4 FSLI** hierarchy with quarter annualization.
  2. Designed an **8-table** normalized MySQL SOADB schema: polymorphic review status (Draft, Review, ReOpen, Closed), **optimistic row locking** so two reviewers can't silently overwrite each other, atomic cross-table syncs, and **SHA-256 natural keys** so reloads are idempotent.
  3. Led **3 engineers** on the SQLAlchemy 2.0 migration to **100%** statement coverage. We used stacked Bazel PRs, SQL allowlists, and FSM **50% delta-variance gates** for SOX.
- **R:** Reconciliation went from **14 days to 3** (70%). Auditors got history and traceability. I'm proud of the correctness, not just the speed: nobody can overwrite a reviewer's decision silently.

### Backup: IA CI bar

On AssortSmart the Go platform CI enforces **100% statement coverage** with 1,200+ Go tests and SAST/SBOM checks (verbal; fine on LinkedIn, not on the PDF bullet). Every scoring output row is stamped with a frozen `config_hash`, so any decision can be traced to its exact prompts, params, and catalog.

---

## 12. Choose safety

> "We build systems knowing people make mistakes, software has bugs and bad things can happen... We implement guardrails... We speak up and push back when we see unsafe practices."

This is the value most aligned with the JD. Expect 1 to 2 questions on it.

**Likely questions**
- Tell me about a guardrail you built.
- Tell me about a time you pushed back on something unsafe.
- How do you make deployments safe?

### Primary: S14 No SQL tool, frozen scope (AI on a multi-tenant production database)

- **S:** AssortSmart has a **2.11B-row** ClickHouse master and multiple retail tenants. There was pressure to give the scoring LLM a SQL tool ("let the agent query what it needs") and to let the Ask Iris copilot answer any question.
- **T:** I owned the scoring pipeline and Ask Iris guardrails.
- **A:**
  1. Pushed back on the SQL tool. At 88k items per pass it creates runaway queries, pool exhaustion, and prompt-injection risk. Instead, context is pre-computed and served as **JSON payloads**. The LLM never touches the database.
  2. Writes go through the engine onto `ReplacingMergeTree` with a version column, so retries can't duplicate. On LLM timeout, the run falls back to the deterministic score and continues.
  3. Ask Iris: **JWT** checked on the WebSocket handshake, and the tenant/hierarchy/plan scope is **frozen at the handshake**. Tools inherit that scope, so a later message can't pivot to another tenant.
  4. A LangGraph supervisor with a **3-attempt** evaluator cap and a recursion limit. It fails closed with a graceful message instead of looping. LangSmith traces every run.
- **R:** No path exists for the model to issue SQL or cross tenants. Provider outages degrade to baseline instead of failing runs. Lesson: complicated instructions ("please don't query other tenants") are impossible to follow every time. Structure beats instructions (this echoes the value text).

### Backup: S5/S2 guardrails in finance and compliance

- **Uber FRM:** SQL allowlists, optimistic locking, and **FSM 50% delta-variance gates**. A quarter-over-quarter swing above 50% blocks the state transition until someone reviews it.
- **Masters India:** idempotency keys and DLQ (S2).
- **AssortSmart edge:** constant-time API key comparison (no timing leaks), Postgres roles per service, and a Redis-fronted Firebase to JWT/OIDC auth waterfall.

---

## 13. JD core responsibilities as behavioral questions

The JD lists five "core responsibilities." Expect questions shaped like these.

| JD line | Question you'll hear | Story |
|---|---|---|
| **Planning and execution:** track timelines with minimal supervision; reprioritize as resources change | "Tell me about a project where the timeline or resources changed." | S3: deadline freezes reordered the migration. Or S12: pump when the allowlist blocked the plan. |
| **Collaboration and partnership:** align across teams, understand stakeholder needs, listen | "Tell me about working with a team with different goals." | S9: two camps. S5: finance/auditor needs. S17: operators. |
| **Problem solving:** standard and non-standard issues, escalate appropriately, analyze multiple sources, share knowledge | "Tell me about a hard bug." "When did you escalate?" | S10, S11, S7. Escalation: S2 (took the near-miss to leadership instead of silently patching). |
| **Continuous learning:** new skills and tools, feedback, share knowledge | "What did you learn recently? How?" | Python to Go and ClickHouse internals (section 5). LangGraph/LangSmith eval discipline. Wrote the failure catalog for the team. |
| **Continuous improvement:** recommend process updates, seek alternative approaches | "Tell me about a process you improved." | S6 checklist. S7 testing notes. S2 incident template. S4 ELK. |

### Escalation answer (they like this for Senior)

> I escalate when the blast radius is beyond my team or when the fix needs a decision I don't own. The double-filing near-miss touched compliance with a government system, so I took it to leadership the same day with a proposed fix instead of patching quietly. For the cluster allowlist, I built the workaround myself but raised the proper network fix with the owner in writing, with the risks of the workaround listed.

---

## 14. Generic questions mapped fast

| Question | Story |
|---|---|
| Tell me about yourself | Hub intro (index) |
| Most challenging project | S9 + S10 (ClickHouse + OOM) |
| Conflict with a teammate | S8 |
| Conflict with a manager | S8 framed upward, or S13 with product |
| Failure | S6, S1 |
| Tight deadline | S3 |
| Ambiguity | S12 |
| Customer impact | S5, S13 |
| Mentoring | S16 |
| Went above and beyond | S2 (whole pipeline, not one endpoint) |
| Disagreed and committed | S8 (committed to repository functions for dynamic queries) |
| Biggest technical decision | S9 |
| Incident / on-call | S11, S1, S10 |
| Security | S14 |
| Why OCI | "The JD is literally resiliency, operability, and correctness in distributed systems. I've done it at startup and Uber-team scale and want it at cloud-provider scale, where fundamentals and safety are the culture. Choose safety and Nail the basics read like my own failure catalog." |
| Why leaving | "I want harder distributed-systems problems and a deeper engineering bench. Infrastructure where a 1% improvement matters." |
| Weakness | "I over-invest in written artifacts: decision docs and failure catalogs. Now I time-box them and lead with a one-page summary." |

---

## 15. Delivery rules

1. Say **"I"** for your actions. OCI wants what *you* did ("what did you do first?").
2. Put a **number** in every Result.
3. Name **one alternative you rejected** in Action. They ask "what were the alternatives?"
4. End with **what happened next** (process change, new ownership).
5. Don't reuse the same story twice in one loop. You have 17.
6. If you don't know a detail, say "I don't remember the exact figure; it was on the order of X." Don't invent.
7. Respect confidentiality: "a retail client," not internal names or data.
