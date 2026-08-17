# Behavioral / STAR stories — Java / Spring

**Self-contained** behavioral bank — the full 10 stories are below, so you never leave this track
to prep. Outcomes, Amazon Leadership Principle mapping, and Googliness signals are identical across
every resume track; only the **stack wording** differs. Pure Java/Spring framing: non-agentic APIs are **Spring Boot / Hibernate**; the agent plane stays **Python**.

Tell each in 60–90 seconds: one line of Situation, one of Task, 3–4 concrete Actions, a quantified
Result, and a one-line Lesson. Never tell the same story twice in one loop — this bank gives you
coverage. Company-by-company LP mapping (Amazon, Google, Microsoft, LinkedIn, Apple, Netflix,
Atlassian, Salesforce) lives in `../campaign_extras/behavioral/company_behavior_guides.md`.

**Coverage matrix**

| Story | Amazon LPs | Googliness |
|---|---|---|
| 1. Reconciled ClickHouse verdict | Are Right, A Lot · Have Backbone; Disagree & Commit · Dive Deep | Intellectual humility · ambiguity |
| 2. BQ→CH ingestion lane (freshness as a feature) | Ownership · Invent & Simplify · Insist on Highest Standards | Bias to action |
| 3. Malformed-plan validator | Customer Obsession · Insist on Highest Standards | Problem-first thinking |
| 4. Clustering copilot inversion | Think Big · Customer Obsession · Deliver Results | Ambiguity · user empathy |
| 5. Constants-refactor regression | Insist on Highest Standards · Earn Trust | Humility · owning mistakes |
| 6. Coverage-gap fix (test where code lives) | Dive Deep · Learn & Be Curious | Rigor |
| 7. ORM-vs-repository disagreement | Have Backbone; Disagree & Commit · Earn Trust | Healthy conflict |
| 8. Masters India migration under deadline | Deliver Results · Ownership · Bias for Action | Execution under pressure |
| 9. Anti-bot arms race | Learn & Be Curious · Invent & Simplify | Persistence |
| 10. Double-filing near-miss / idempotency | Earn Trust · Insist on Highest Standards | Doing the right thing |

---

## 1. The reconciled database verdict (disagreement between two expert camps)

> **resume_java wording:** Decision process and PoC gates stay identical. Implementation plane on this track: the agentic planner is a **Python** service; the AssortSmart write APIs it calls are **Spring Boot**; the ClickHouse client and staging jobs sit behind them.

**Use for:** "Tell me about a time you disagreed with your team / made a decision with incomplete data / influenced without authority."

- **S:** At Impact Analytics, the org was split on adopting ClickHouse for the new agentic planner. A live audit of the legacy backend concluded "no ClickHouse"; senior SMEs pushed "yes, unified OLAP." Both sides had evidence; a wrong call was expensive either way.
- **T:** Produce a recommendation the org could commit to, without discarding either side's evidence.
- **A:** Separated *facts* from *conclusions*: accepted every measured fact in the audit, then showed its "no" conclusion was a property of the legacy in-place-UPDATE write model, not of planning workloads. Designed an insert-only/versioned write model that sidesteps ClickHouse's mutation weakness, and proposed a 3-gate path: in-stack BigQuery fixes first, Postgres discipline second, a versioned-write PoC third — each gate measurable.
- **R:** Both camps agreed to the staged path. The PoC held the mutation queue at zero at 10× scale; in July 2026 the org committed to ClickHouse end-to-end. No premature infra spend, no camp "lost."
- **Lesson:** disagreements between competent people are usually about hidden assumptions, not facts — make the assumptions explicit and the decision often resolves itself.

## 2. The BigQuery→ClickHouse ingestion lane (freshness as a feature)

> **resume_java wording:** Freshness design (atomic `REPLACE PARTITION`, reconciliation, staleness sentinel) is language-agnostic. If asked *who runs the load*, it is a scheduled **Spring Boot** job on this track, not a Python cron.

**Use for:** "Design decision you're proud of / handling hidden failure modes / raising the bar."

- **S:** The copilot's agent probes needed deterministic low latency (design target p95 <500 ms), but our historical data lives in BigQuery, where shared-slot variance means the same query can take 1 to 20 seconds. The obvious fix — copy the data into ClickHouse — has a known trap: derived copies rot silently, and a planner making buy decisions on stale data is worse than a slow query.
- **T:** Build the ingestion lane from BigQuery into ClickHouse so the agent read plane is both fast *and* provably fresh.
- **A:** Designed the lane in three parts: scheduled exports land in ClickHouse staging tables and get promoted with atomic `REPLACE PARTITION`, so readers never see a half-loaded night; per-partition row-count and sum reconciliation against the BigQuery source with 0.1% tolerance blocks promotion on mismatch; and a freshness sentinel stamps *data-as-of* into every agent recommendation, so staleness is visible in the product instead of discovered in an incident. Added nightly precompute of attribute significance for hierarchies with active plans so most copilot sessions start warm.
- **R:** The read plane serves agent probes against its p95 <500 ms design target, and the failure mode everyone fears with derived data — silent rot — is structurally impossible: loads are atomic, mismatches block promotion, and staleness is printed on the answer.
- **Lesson:** when you copy data for speed, freshness and reconciliation are product features, not ops chores — design them in on day one.

## 3. Fixing the #1 LLM-planner failure (malformed plans)

> **resume_java wording:** The planner is a **Python / LangGraph** service, so keep the story as-is. The transferable principle — a deterministic contract around a probabilistic component — is exactly how you use **Bean Validation / schema checks** before a commit in a Spring service.

**Use for:** "Hardest technical problem / quality bar / working with non-deterministic systems."

- **S:** Our multi-agent planner let an LLM decompose questions into execution plans; malformed plans (unknown agents, forward references, over-wide stages) were the top failure class — structural correctness was 0.54 on our eval set.
- **T:** Make plans safe to execute without giving up LLM flexibility.
- **A:** Wrote a hard structural validator over the plan schema (domains, duplicate ids, stage widths, forward references in dependency placeholders) that runs before anything executes; on failure, one self-repair pass re-prompts the LLM with the specific validation errors; made every agent's `answer()` non-throwing so a single agent failure produces a labeled partial answer instead of a crash.
- **R:** Structural correctness 0.54 → 0.99 on the offline eval; failures became explicit and recoverable.
- **Lesson:** with LLMs, don't chase a perfect prompt — put a deterministic contract around a probabilistic component.

## 4. Inverting the clustering workflow (customer obsession + think big)

> **resume_java wording:** Product/workflow content is unchanged; the copilot is a **Python FastAPI + LangGraph** microservice. The write-back into existing product tables goes through the **Spring Boot** APIs.

**Use for:** "A time you challenged the status quo / product thinking / ambiguity."

- **S:** Store clustering is the foundation of every assortment plan, yet it was the least-assisted step: the system computed attribute significance and then made humans choose from raw score lists. Live audits: users tried exactly 1 configuration per plan (search space: 12 algorithms × k=3–10 × any attribute subset), 8.5% of runs failed (37/437, >80% on input mistakes), and nothing was reproducible.
- **T:** Define the module's agentic rebuild — with adoption risk as the main constraint.
- **A:** Inverted the workflow: the user states intent (hierarchy + reference period — the only non-derivable inputs); the agent grounds the request into concrete scopes, selects features by statistical significance, batch-evaluates **~100 candidate clusterings** scored on silhouette, and presents the **top 3 with evidence** (a baseline scenario mimicking the client's legacy configuration always included) with plain-English rationale — the human approves at explicit gates. Kept the manual wizard alive as a legacy path per client so adoption is opt-in, not forced.
- **R:** Committed targets: <1 h to a finalized plan (from days), top 3 of ~100 batch-evaluated candidates presented (from 1 config ever tried), <2% failures, agent-selected features and k fully visible to the planner — with write-back into existing product tables unchanged.
- **Lesson:** the highest-leverage AI feature is often workflow inversion, not model quality.

## 5. The "pure refactor" that wasn't (owning a mistake)

> **resume_java wording:** Owning-the-mistake content is unchanged (it happened on the Uber Python codebase). On this track, describe the guardrail as a **JUnit** gate — "the test that would have caught it".

**Use for:** "Tell me about a mistake / a bug you caused / quality standards."

- **S:** At Uber, PR 2 of my 3-PR stacked refactor — supposedly a constants-only consolidation across 31 files — had a downstream test failing.
- **T:** Find why a test asserting "preserve COMPONENT strategy when selection is empty" now saw AGGREGATE.
- **A:** Diffed my own PR ruthlessly: I had slipped in a `_resolve_strategy` helper that silently downgraded the strategy — a behavioral change smuggled into a refactor. Removed it, restored the pass-through, and added "pure refactor ⇒ zero test diff" to the team's stacked-PR checklist so the class of error is caught by process, not vigilance.
- **R:** Shipped as a true refactor; the checklist caught a similar issue for a teammate weeks later.
- **Lesson:** call your own fouls fast and convert them into process — credibility compounds.

## 6. Coverage that lied (dive deep)

> **resume_java wording:** Test-where-the-code-lives principle is unchanged. Java wording: **JUnit + Mockito**, changed-module coverage in CI, **Testcontainers** for DB-backed tests.

**Use for:** "Tell me about debugging something non-obvious / testing philosophy."

- **S:** My Uber ORM migration failed CI at 34.6% new-line coverage despite the code paths being exercised.
- **T:** Understand how tested code could be "uncovered."
- **A:** Dug into the coverage mechanics: repository-layer tests stubbed the new ORM classmethods via mock chains, so the model package's lines never executed — mocking had shifted the coverage to the wrong layer. Wrote 12 direct model-layer unit tests including rejection paths (empty updates, unknown columns).
- **R:** 100% on the changed module; the pattern ("test where the code lives, not where it's called") went into the team's testing notes.
- **Lesson:** a metric you don't understand is a metric that will lie to you.

## 7. Disagreeing with the architecture rulebook (backbone + commit)

> **resume_java wording:** Disagree-and-commit content is unchanged. Java framing: the boundary is **Hibernate / JPA** repositories vs. raw SQL — keep query mapping next to the entity so a rename fails the compiler, keep the repository a thin session wrapper.

**Use for:** "A time you disagreed with a standard / with a senior engineer."

- **S:** Uber's team architecture rules said all data access lives in `repository/`. For the ORM migration, I put query classmethods on the ORM model instead.
- **T:** Either follow the rule mechanically or argue the exception.
- **A:** Made the engineering case: classmethods keep SQL adjacent to column definitions so renames fail the type checker immediately; the repository stays a thin session wrapper; no business logic leaks. Heard the counter-argument (consistency of the rulebook), documented the deviation explicitly, and committed to free repository functions for dynamic queries that don't naturally belong to one model.
- **R:** Exception accepted and documented; the latent column-aliasing bug that motivated the migration (raw SQL reading income-statement rows with balance-sheet column lists) could not recur.
- **Lesson:** disagree with a written rationale, commit visibly, and leave the decision auditable.

## 8. The migration nobody could pause the business for (deliver results)

> **resume_java wording:** Deadline, sequencing, and every number stay identical. Java wording: **Spring Boot** strangler per endpoint, **Spring Batch** for the bulk IRP path, **Kafka + PostgreSQL** quarter sharding.

**Use for:** "Delivering under pressure / leading a project end-to-end."

- **S:** Masters India's PHP monolith was collapsing during monthly GST deadline peaks — worker pools exhausted by blocking government-portal calls — while **1,500+** enterprise clients kept filing.
- **T:** Lead the migration to async FastAPI microservices with zero downtime tolerance during deadline windows.
- **A:** Strangler pattern per endpoint behind the gateway; shadow traffic on read paths first; moved bulk/async Kafka paths before interactive filing; kept data in place (PostgreSQL quarter sharding) to avoid a risky data migration during cutover; froze cutovers during deadline weeks; hardened bulk IRP with idempotency keys, retries, and DLQ.
- **R:** p95 **1.2 s → 300 ms**, **1M+ IRP submissions/day**, **100K+/import**, throughput **700 → 4,000 requests/min**, no deadline-window outage during the migration.
- **Lesson:** sequencing is the risk-management tool — the migration plan mattered more than the target architecture.

## 9. The anti-bot arms race (learn and be curious)

> **resume_java wording:** Unchanged — this is **Selenium** acquisition with proxy pools and a measurement loop, regardless of the service language.

**Use for:** "Working against a moving target / persistence."

- **S:** Uber menu scrapers were being blocked — success rates dropped as source platforms rotated their bot defenses.
- **T:** Get ingestion reliability up without an unbounded proxy budget.
- **A:** Treated it as an experiment loop, not a one-off fix: instrumented per-source block signatures, iterated countermeasures (IP rotation, user-agent/fingerprint management, dynamic proxy pools), set retry budgets per source, and fed block-rate metrics into the same ops dashboards as parse failures so regressions surfaced in minutes.
- **R:** Successful ingestions up to **95%+**; the measurement loop meant new defenses were detected and countered in days, not weeks.
- **Lesson:** against an adversarial moving target, the asset is the feedback loop, not any single countermeasure.

## 10. The double-filing near-miss (earn trust / do the right thing)

> **resume_java wording:** Integrity content is unchanged. Java wording: idempotency key (`clientId + fileHash + batchIndex`) enforced in the **Spring Batch** writers and a DB unique constraint, plus a dead-letter replay path.

**Use for:** "Integrity / a time you raised a problem you could have hidden."

- **S:** At Masters India, a retried bulk import came close to filing duplicate e-invoices with the government portal — a compliance-grade error for the client. It hadn't caused customer damage yet, and nobody outside the team would have known.
- **T:** Decide between quietly patching the retry and treating it as the systemic risk it was.
- **A:** Flagged it to leadership as a near-miss, wrote the incident review myself, and retrofitted idempotency keys (client + file hash + batch index) across the entire bulk pipeline plus a dead-letter replay path — not just the endpoint that almost failed.
- **R:** Zero duplicate filings after rollout; the near-miss review became the template the team used for later incidents.
- **Lesson:** trust is built in the moments where you could have stayed quiet.

---

## Rapid-fire answers (30 seconds each)

- **"Why are you leaving / why big tech?"** "I've now built and owned systems end-to-end — an agentic platform, streaming pipelines, a finance-grade audit tool. I want the scale ceiling removed: harder distributed-systems problems, deeper peer bench, and infrastructure where a 1% improvement matters."
- **"Biggest weakness?"** "I over-invest in written artifacts — decision docs, playbooks. I've learned to time-box them and lead with a one-page summary, because a 20-page analysis nobody reads is a failure mode too." (Real, specific, shows self-correction.)
- **"Conflict with a manager?"** Use story 7 (rulebook disagreement), framed upward.
- **"A time you failed?"** Story 5 (refactor regression) or story 10 (near-miss) — both end in process fixes.
- **"What are you most proud of?"** Story 1 — turning an org-level disagreement into a gated, evidence-based decision that later became the committed direction.

---

## Stack-wording quick answers (say these on this track)

- **CI gating:** the pipeline blocks a merge if **JUnit** fails or changed-module coverage drops;
  **Testcontainers** for DB-backed tests. (JUnit is on the FRM experience Tech line, not in Skills.)
- **Testability:** constructor-injected ports (repositories, clients), pure domain functions for
  tax/dedup rules, DTO validation at the boundary.
- **Idempotent retries:** `clientId + fileHash + batchIndex` recognized on replay — same guarantee
  as the main track, enforced in the **Spring Batch** writers plus a DB unique constraint.
- **Observability:** **Actuator + Micrometer** metrics, ELK correlation IDs, New Relic APM — the
  Masters India "triage 70% faster" story is unchanged.

---

**Also study:** [`39_behavioral_question_bank.md`](39_behavioral_question_bank.md) (all ~43 common questions → which story) · [`40_behavioral_prep_grid.md`](40_behavioral_prep_grid.md) (project × question drill sheet).
