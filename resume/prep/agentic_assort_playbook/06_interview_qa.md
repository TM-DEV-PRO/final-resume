---

# 6. Interview Q&A (what an EM / architect will ask)

## 6.1 Architecture & databases
**Q: Why three databases? Isn't that over-engineered?**
A: The product is two workloads in one — an editable, pivoted **planning grid** (OLTP: ACID, per-cell read-after-write, locks) and **hindsight analytics** (OLAP: scan-and-aggregate). No single engine is best at both. BigQuery is the cheap, scalable source of truth; Postgres owns editable state with ACID; ClickHouse/DuckDB serve fast pivots. Forcing one engine means either broken transactional writes (OLAP DBs) or DML quota/latency walls (BigQuery). The complexity is a deliberate trade for correctness + cost + latency, and the invariant is simple: **BigQuery = truth, Postgres = editable SoR, always.**

**Q: Why ClickHouse if it's bad at updates — and a planning grid is all updates?**
A: That objection is about *in-place* updates. ClickHouse mutations are async and stop accepting past ~1,000, so `ALTER UPDATE` per cell is a non-starter. But our grid is built around **versions/variance/undo** — so an edit is an **INSERT of a new version**, reads take `argMax(version)`, deletes are tombstones, bulk re-seeds are atomic `REPLACE PARTITION`. That keeps the mutation queue at **zero** and turns "what ClickHouse is worst at" into "what it's fine at," while giving undo/version-diff for free. We proved `mutations_used = 0` at 1× and 10× in the PoC.

**Q: How does undo / version-diff actually work on an append-only store?**
A: Every edit writes a row with a monotonic `version` (epoch-ms). The latest state is `argMax(value, version)`. Because older versions are retained until background merges collapse them, **undo** = read the prior version; **version-diff** = compare two `version` snapshots. `ReplacingMergeTree(version)` dedups newest-wins on merge; `FINAL`/`argMax` gives correct reads before merge.

**Q: What does "unify the schema at the derived level" mean?**
A: One common schema keyed by `tenant` at the **cube grain** (`cluster×class×fiscal_week`), not per-tenant tables. The cube-build SQL is tenant-parameterized and identical, so one codebase/query set/procedures serve all clients; onboarding a tenant = add a partition. Physical isolation (separate Postgres DB + BigQuery project per tenant) is kept for blast-radius; "unified" is a **schema/codebase standard**, not one shared instance.

**Q: How did you get ~280× cheaper on BigQuery?**
A: BigQuery bills by bytes scanned. Three levers: route the hot hierarchy read to the **clustered** `_assort` copy (~3×), materialize a narrow **store×category×week rollup** (reads ~3.3 GiB vs ~2.9 TiB → ~280×; ~$8 to build, ~$0.008/day), and enforce **partition pruning + no `SELECT *`**. We also caught a `SELECT * LIMIT 2` billing 38.8 TiB / $327 — fixed by a cost-guard that rejects `SELECT *` and un-dated scans.

**Q: How do you keep the three stores in sync?**
A: BigQuery → batch ELT builds the cube → upsert/COPY to Postgres (SoR). Planner edits commit to Postgres; DuckDB pivots a hydrated slice and commits deltas back. ClickHouse is fed read-only from BigQuery cube/rollup builds via HTTP insert / partition-swap. It's **batch, not streaming** — planning has a cadence, not a millisecond SLA.

## 6.2 AI / agents
**Q: Why multiple agents instead of one big prompt?**
A: Separation of concerns + reliability. Each agent owns a domain (hindsight, clustering, line plan, recommendations, assortment data), its own tools, prompt, and validation. A router decides single-agent vs orchestrate; a decomposer builds a DAG. This gives parallelism, targeted prompts (better accuracy), independent failure handling, and an auditable trace — impossible in one monolith prompt.

**Q: LLM plans are unreliable — how do you stop bad plans from executing?**
A: A hard **structural validator** runs before execution: it rejects unknown domains/tools, duplicate ids, over-wide stages, and forward references in `<A_n>` placeholders. On failure it re-prompts the LLM once with the exact errors and re-validates (`repaired=True`). In an offline eval this lifted decomposition quality from 0.54→0.99. The validator — not the model — is what makes it production-safe.

**Q: What happens when an agent fails?**
A: `BaseAgent.answer()` never raises; a failure returns `status="error"`, transient I/O is retried with exponential backoff, and the orchestrator still **synthesizes a partial answer** from the agents that succeeded (clearly labeled). Degrade, don't crash.

**Q: How do agents pass data to each other?**
A: The DAG has stages; agents within a stage run in parallel (thread pool). When a later sub-query depends on an earlier answer, a rephraser substitutes the `<A1>` placeholder with the prior result before dispatch — explicit, inspectable dependency passing rather than hidden shared state.

**Q: How do you keep autonomous agents safe?**
A: Confidence/impact **thresholds**: below threshold agents act and log; above it they raise a human-in-the-loop **Signal** with a reason code for Accept/Edit/Dismiss. Every action + decision hits an immutable **audit log**. That's what makes overnight autonomy acceptable to merchants.

**Q: Is text-to-SQL safe?**
A: Only with guardrails: SELECT-only, `LIMIT` caps, `NULLIF` denominators, no `SELECT *`, validate before execute, and route through the BigQuery cost-guard. The LLM proposes; the guardrails dispose.

**Q: How do you measure agent/answer quality?**
A: An offline eval harness scores routing, decomposition structure, dependency capture, and coverage against gold queries (structured 0.99 vs flat baseline 0.54). For confidence at serve time: rules + LLM logprobs + intent-match. (I'm explicit that the harness measures structure/correctness on mock outputs, not live model accuracy — production would add human-rated eval sets + online metrics.)

**Q: You keep saying "agentic" — what's actually shipping?**
A: The clustering module — a cluster-recommendation copilot spec'd against live-audit baselines (1 config tried per plan, 8.5% run failures >80% of which are input errors, 0% reproducibility). The planner states intent — hierarchy + period — and a dedicated agent does scoping, attribute selection and a 20–100-config batch exploration on a dedicated ClickHouse read plane; three human gates; approved results write back into the existing tables unchanged. Targets: <1 h to a finalized plan, ≥20 configs, <2% failures, p95 <500 ms probes. Full module Q&A in §9.7 — including "why isn't this just AutoML," "how do you stop hallucinated recommendations," and "what did you deliberately not build."

## 6.3 Tradeoffs, scale, "what would you do differently"
**Q: Biggest tradeoff you made?**
A: Accepting **more infra + a sync path** (three tiers) to get correctness + cost + pivot latency, instead of one-DB simplicity. And on ClickHouse: trading **storage + merge overhead** (versioned history) for zero mutations + free undo/diff.

**Q: How does this scale to 20k stores?**
A: Cube pre-aggregation keeps pivots proportional to the *slice*, not the fact; ClickHouse partition/cluster + `argMax` reads are sub-second on ~900M rows (cited target); Postgres stays the editable SoR with proper partitioning. The gate is a **10× PoC** on the insert-only model before committing ClickHouse.

**Q: What would you do differently / next?**
A: Add circuit-breakers + per-agent timeouts; a human-rated eval set for model accuracy (not just structure); wire the `AggregatingMergeTree` materialized views end-to-end; and evaluate a CDC/Kafka path if we need near-real-time facts. I'd also fix the legacy BigQuery leaks first (cheapest, certain win) before any ClickHouse spend — which is exactly the staged gate I recommended.

**Q: How did you decide ClickHouse vs not, given the team disagreed?**
A: I separated **facts** (accepted from the live audit) from **conclusions**, showed the anti-ClickHouse argument was about *legacy in-place-update code* not the new product, and converted the disagreement into a **3-gate decision** (in-stack BQ fixes → Postgres discipline → versioned-write PoC). Nobody had to "win" — we agreed on measurements.

## 6.4 Behavioral (use these as STAR seeds)
- **Decision under ambiguity / conflict:** the reconciled DB verdict (three conflicting sources → one staged gate). *(§2 L1)*
- **Ownership / de-risking:** the BigQuery cost program + cost-guard (found a $327-for-2-rows leak; codified the fix). *(§2 P1/P2)*
- **Depth / correctness:** catalog-verified 5,385 columns / 46 FKs via $0 metadata, overturning "inferred" assumptions. *(§2 L2/P4)*
- **Invention:** the insert-only/versioned ClickHouse model that made an OLAP engine viable for an edit-heavy grid. *(§2 D2)*
