---

# 9. The Cluster Recommendation Copilot — the module you are building right now

<div class="stage-badge stage-c">Source: Agentic Cluster FRD v1.8 (PM edition, 2026-07-06) + companion HLD/LLD · live tenant audits (kik, briscoes)</div>

This is the **current, concrete build** — the strongest thing on the résumé because it is present-tense ownership: a full agentic module from measured problem → architecture → phased rollout. Everything below is what/why/how at interview depth. When asked *"what are you working on right now?"*, this chapter is the answer.

## 9.1 WHAT — in one breath

> "A conversational + structured copilot for store clustering. The planner states *what* to cluster and *for when* — a dedicated agent handles store scoping, attribute selection, exploration and scoring on a dedicated ClickHouse read plane; the planner reviews evidence, adjusts stores with consequences shown, and approves. The existing product consumes the result completely unchanged."

Two entry modes, one agent: the **manual wizard with inline recommendations** (Mode A) and **chat-native** (Mode B — "cluster Small Appliances for SS27"). The **convergence rule** is non-negotiable: whichever door you enter, the flow converges before execution — same config document, same search plan, same three gates, same write-back. A session started in one mode can continue in the other; the modes are two surfaces on one agent, never two implementations.

## 9.2 WHY — the measured problem (all live-audit numbers)

Store clustering is the foundation every strategy plan is built on — and the least assisted step in the product:

| Measured reality (today) | Number | Source |
|---|---|---|
| Configurations evaluated per plan | **exactly 1** (search space: 12 algorithms × k 3–10 × any attribute subset) | live audit |
| Run failure rate | **8.5%** (37/437 runs, kik) — **>80% are input mistakes** at the data boundary | live audit |
| Reproducibility of shipped clusterings | **0%** — algorithm/params/seed never persisted | live audit |
| Manual store swaps surviving a re-run | **0%** — silently erased | live audit |
| Significance scores (the hardest signal) | computed, then **ignored** — user picks from raw score lists | code + UX audit |
| Median clustering job | **≈20 s** (370 live runs; max 463 s) | live audit |
| Agent data-probe latency on shared BQ | **1–20 s+, variance uncontrolled** | live audit |
| Strategy-create help choosing a cluster plan | **zero** — and 1 in 5 finalized kik plans has **zero stores attached**; briscoes' finalized inventory is 100% **>17 months stale** | live audit |

The one-line diagnosis for interviews: **"the compute is fast (~20 s median); the bottleneck is everything around the machine"** — expert choices made blind up-front, one shot per try, knowledge thrown away after.

## 9.3 HOW — the workflow inversion

Today's flow asks the human for four expert choices up front, blind, then runs once. The agentic flow inverts it:

```
TODAY:   human picks hierarchy → period → store groups → attributes → submit(1 config) → eyeball → hand-fix → finalize
AGENTIC: human states INTENT (hierarchy + period — the only 2 non-derivable inputs)
           → agent proposes store scope        (active stores, sister-store subs, sample-size guards)   [Gate ~ confirm]
           → agent proposes attribute sets     (significance + coverage + redundancy gates, ranked)     [Gate 1: search plan]
           → agent explores 20–100 pruned configs on an isolated scratch plan (results stream)
           → top-3 with evidence packs (driving attributes, separation, stability, size balance,
             churn-vs-current-live-clusters)
           → human reviews, what-ifs (≤10 s warm), moves/pins stores with impact shown                  [Gate 2]
           → explicit approval → write-back into today's tables                                          [Gate 3]
```

Key definitions you must own in the room:

- **Intent** = hierarchy scope + reference period — the only two inputs that are business strategy rather than derivable from data. Everything else (store cohort, attributes, algorithm, k, tuning) the agent derives. Pins/moves are *not* intent — they're **business-knowledge injection** during review. The invariant: *intent is always human-owned; the agent may ground, expand, execute or queue it — never invent or auto-resolve one.*
- **Config document** = the unit of record: algorithm, k, hyperparameters, seed, features, windows, pins, data watermark, scorer version — persisted and **content-addressed**. "Re-run" reproduces membership on the same watermark or explains drift.
- **Pins** = durable constraints with reason codes; honored by every subsequent re-run and refresh. This kills the silent-loss-of-swaps failure (0% → 100% survival).
- **Three delegation levels:** **L1 copilot** (proposes every step, executes on confirmation — launch) → **L2 autopilot-with-approval** (one intent runs the whole flow unattended; one review, one approval) → **L3 standing monitor** (nightly drift detection — "12 stores no longer fit, stability dropped 0.18" — raises a proposal). Nothing at any level auto-finalizes; system-originated work surfaces as **pending intents** unless the tenant grants a recorded, one-time standing pre-approval.

## 9.4 The architecture positions (and why)

1. **Deterministic tools compute; the LLM orchestrates and explains.** Every number in an evidence pack traces to a tool call; same inputs + same scorer version ⇒ identical ranking. The LLM never invents a metric. This is the anti-hallucination stance *and* what makes recommendations auditable.
2. **Deterministic grounding for chat.** Department mentions are backtracked to full hierarchy paths via catalog search (ambiguity → clarifying question, never a guess); season labels resolve via the tenant's fiscal calendar (seasons differ per tenant and hemisphere); the **grounding card** (scope, cohort, attributes, each with a reason) must be confirmed before any compute.
3. **A dedicated ClickHouse read plane.** Agent probes need p95 < 500 ms deterministic (vs 1–20 s+ on shared BigQuery slots). Fed by the org's existing BQ→CH ingestion pipeline (proven on ItemSmart); **agent access is read-only enforced by database profile, not convention**; exploration writes only to isolated scratch plans; nightly precompute makes active hierarchies feel instant (≥80% cold→warm target). This is the gated ClickHouse adoption from the reconciled DB verdict actually happening — read plane only; BigQuery stays truth; Postgres stays the editable SoR (explicit FRD non-goal).
4. **Write-back compatibility.** Approved results land in the existing `plan_cluster_final` / `plan_cluster_store_final` tables — strategy, budget, wedge, line consume them with **zero product changes**. The legacy wizard keeps working untouched in parallel (adoption de-risk).
5. **Safe editing of consumed plans.** Editing a plan referenced by strategies defaults to **clone-and-version with lineage** (in-place edits would silently invalidate downstream budgets/wedges); rebinding is explicit per-strategy; an edit-impact card shows consumers *before* any change.
6. **Every flow closes.** A 19-workflow audit produced a **terminal-states contract**: every flow defines success / rejection / failure / abandonment-expiry. Degraded batches (<3 viable candidates) surface partials + a failure taxonomy + retry; capacity is a queue with a position banner, not an error; rejection returns to comparison and is captured as a learning event.
7. **Honest learning loops.** Deviations (attribute removed, store moved, non-top pick, dismissal) are captured with reason chips: (a) deterministic memory — never blindly re-recommend what this scope rejected; (b) human-approved calibration of tenant metric weights (versioned, never silently self-tuned); (c) a labeled recommended-vs-chosen corpus for any future learned ranker, shipped only as an explicit scorer-version release to preserve determinism.

## 9.5 The strategy doorway (§2.2 of the FRD — best cross-module story)

Every strategy plan binds to exactly one cluster plan at creation; today there's zero help and the audit found strategies pointing at cluster plans that **no longer exist**. The fix, three tiers:

- **Hard eligibility gate before scoring:** finalized ∧ not deleted ∧ non-empty membership ∧ recoverable scope. (1 in 5 finalized kik plans has zero stores — binding one silently breaks every downstream step. Unusable plans are listed, never scored.)
- **FitScore ≤2 s, deterministic:** cheap terms rank all candidates; the expensive variance-explained term ("these clusters explain X% of store-revenue variance in your scope") runs top-5-only, computed on the **last comparable season** (a future window has no sales yet), **penalized for cluster count** (so many-tiny-clusters can't game it) and **weighted by store coverage**. Bands Green/Yellow/Red **calibrated by backtesting against 467 historical bindings** (363 kik + 104 briscoes).
- **Always a top-3 shortlist** with explain cards + pairwise deltas ("#2 covers your scope but is 9 months staler"); padded with a **spawn card** when fewer exist — never an empty dropdown. Spawn runs the full recommendation pipeline inline, writes at the pre-finalize step, promotes only on human confirmation (or parks as a **pending intent** where tenant governance requires a cluster-owner sign-off), records `created_via` + full scope keys for future dedup, and the create API now validates bindings are live + finalized — eliminating the dangling-reference class.

## 9.6 Targets & rollout (know these cold)

| Metric | Baseline (measured) | Target (6 mo) |
|---|---|---|
| Hierarchy → finalized plan | hours–days | **< 1 h** (<10 min precomputed) |
| Configs evaluated per plan | 1 | **≥ 20** |
| Run failure rate | 8.5% | **< 2%** |
| Top-3 contains shipped config | n/a | **≥ 60%** |
| Store corrections surviving re-run | 0% | **100%** |
| Agent probe latency | 1–20 s+ | **p95 < 500 ms** |
| Reproducible shipped clusterings | 0% | **100%** |
| Strategy plans using a suggested cluster | 0% | **≥ 40%** |

**Phases:** P0 read-only copilot (CH instance + cubes + significance/explain tools; exit: p95 <500 ms, cube reconciles to BQ within 0.1%) → P1 recommendation engine (batch exploration + what-if + config documents; exit: top-3 ≤60 s cold, deterministic re-rank) → P2 approve & write-back (gates, pins with impact preview, doorway point-at-existing; exit: end-to-end consumption in staging) → P3 scale-out (nightly precompute, L2/L3, spawn, kik at 6,040 stores — gated on kik's BQ env cutover).

**Top risks + mitigations (one-liners):** derived-data rot → owned ingestion + freshness sentinel + data-as-of quoted in every rec; metric gaming → hard gates before scoring, stability as pass/fail, full metric vector always shown; trust gap → evidence packs + churn-vs-current + P0 ships read-only value first; compute tail (463 s max) → async batches with streamed partials + nightly precompute for heavy hierarchies.

## 9.7 Interview Q&A for this module

**Q: Why an agent at all — isn't this just AutoML for clustering?**
A: AutoML optimizes a loss; this optimizes a *decision* a human must own. The agent's job is search + evidence + explanation; the human's job is intent, business-knowledge injection (pins), and accountability (`is_final` is a human signature). The measured problem wasn't model quality — it was 1 config tried per plan, 8.5% avoidable failures, zero reproducibility. Those are workflow failures, so the fix is a workflow agent with hard governance, not a better optimizer.

**Q: How do you stop the LLM from hallucinating a recommendation?**
A: It structurally can't — deterministic tools compute every number, the LLM only orchestrates and narrates, and every figure in an evidence pack traces to a tool call. Scope grounding is catalog search, season resolution is the fiscal calendar, and ranking is a versioned deterministic scorer: same inputs ⇒ identical order.

**Q: Why ClickHouse here when the earlier audit said no?**
A: The audit's "no" was about the *legacy editable* workload (in-place OLTP mutations). This is the opposite shape: a **read-only** analytical plane for agent probes, insert-only ingestion from BigQuery, isolated from the product's write path. It's exactly the gated forward option my reconciled verdict defined — and the FRD non-goals pin it: no transactional data moves, BigQuery stays truth.

**Q: What happens when the agent is wrong or the batch degrades?**
A: Defined outcomes everywhere (the terminal-states contract): <3 viable candidates → partial results + failure taxonomy + one-tap retry; autopilot ambiguity → parked as a pending intent, never auto-resolved; capacity → queue with a position banner; rejection → back to comparison, reason captured as a learning event. Nothing accumulates silently; sessions expire at the tenant retention boundary.

**Q: How does it learn without becoming non-deterministic?**
A: Three honest loops — deterministic memory (never re-recommend what this scope rejected, acknowledged in-session), human-approved calibration (aggregated deviations inform the next *versioned* weight set), and a labeled corpus for a future ranker shipped only as an explicit scorer-version release. No silent self-tuning, ever.

**Q: Multi-tenancy?**
A: Per-tenant everything: ingestion lanes, quotas/concurrency budgets, k-ranges and algorithm allow-lists, metric weights (versioned, actually consumed — fixing a known ignored-weightage defect), default-hierarchy registries with draft vs standing-pre-approval governance, and ClickHouse placement per tenant (briscoes = AU, kik = EU) as a config decision, not a redesign. kik launch gates on its BigQuery environment cutover — its prod dataset is an empty shell today.

**Q: What did you deliberately not build?**
A: Four explicit non-goals: no auto-finalize without human approval; no replacement of the existing wizard (parallel, untouched); no transactional/plan data on ClickHouse and no replacing BigQuery as truth; no attempt to make the ML itself faster (~9 s/config median is accepted physics — we parallelize and precompute around it).
