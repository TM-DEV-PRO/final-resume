# IA — Agentic Cluster ClickHouse DDL Model (Phase-1) source

**Fetched:** 27 Jul 2026 via Atlassian MCP (authenticated).  
**Page:** [Agentic Cluster Module — ClickHouse DDL Model (Phase-1)](https://impactanalytics.atlassian.net/wiki/spaces/AgenticAss/pages/2816606240/Agentic+Cluster+Module+ClickHouse+DDL+Model+Phase-1)  
**Status on page:** v1.5 · 2026-07-15 · `formatQuery`-validated on CH **25.12** · optimization review **PASS**  
**Machine SoT:** `Plans/agentic-clustering/ch-schema/` (`DDL.sql` · `DESIGN_NOTES.md` · `OPERATIONS.md`)

Use this note when defending the **ONE resume CH bullet** (63/8 + insert-only / partition-swapped + agent R/O + pivot 189s→12.3s). Pivot latency is **not** from this page — it is from `21_ia_pivot_benchmark_source.md`.

---

## Resume-safe inventory (recite these)

| Item | Count / claim | Tag |
|---|---|---|
| Tables | **63** (incl. **7** stage twins for partition swaps) | MEASURED design (DDL footer + §3) |
| Layers | **8** (one-directional) | MEASURED design |
| Dictionaries | **5** (store / hierarchy / fiscal / channel / sister-store; + `dict_user` at bring-up) | MEASURED design |
| Views | **19** (argMax latest-state, generation guards, eligibility) | MEASURED design |
| Roles / profiles / quotas | **4 / 3 / 2** | MEASURED design |
| Agent DB profile | `readonly=1` — exploring surface **physically cannot write** | MEASURED design |
| Service roles | **INSERT-only** on owned tables — no `ALTER` below sync role ⇒ no UPDATE path in privileges | MEASURED design |
| Operations mapped | **58** named SQL paths (`OPERATIONS.md`) | MEASURED design |
| Validation | Syntax-complete on live CH **25.12.8.9**; 4 adversarial review passes | MEASURED design |
| Runtime latency on this schema | **Zero runtime evidence yet** — load test at bring-up | Honesty: do **not** claim prod CH latency from DDL |

**60 vs 63:** Overview inventory table says **60** tables; §3 / table catalog / DDL footer say **63** including stage twins. **Resume + interview default = 63.** If challenged: “Overview abbreviated; DDL.sql creates 63 objects including the seven stage twins.”

**624 columns:** **OMIT.** That number does **not** appear on the Phase-1 Confluence page (earlier prep recycled it). Do not recite 624 unless you personally recount `DDL.sql`.

---

## The one idea: never erase

Incumbent product updates/deletes in place. This model bans that on the hot path:

- Facts/cubes arrive as **atomic partition swaps** (`REPLACE PARTITION` via stage twins)
- Decisions arrive as **append-only events**
- Approvals mint **immutable snapshots**
- “Current state” is always a **view** over history
- Writer races: both rows land; deterministic **argMax** / claim-token tiebreak picks the winner; loser stays as audit

---

## Eight layers (names to draw)

| Layer | ~Tables | Physical pattern |
|---|---|---|
| **L0 facts + ledger** | 7 | P1 swap · P4 ledger (`ingest_watermark`) |
| **Grounding dims** | 7 + 5 dicts | P2 RMT + FINAL-sourced dictionaries |
| **L1 cubes + caches** | 7 | P1 swap · P2 caches |
| **PG mirrors** (transitional) | 5 | full-swap `EXCHANGE TABLES` · plan lines P1 |
| **Decision plane** | 20 | P2 / P3 / P4 per table |
| **Outcome loop** | 9 | P4 immutable · P1 weekly swap |
| **Write-back** (transitional) | 3 | incumbent wire-shape + P3 status stream |
| **Telemetry** | 2 | P4 append-only, never expires |

End state (§9): **Postgres = identity / UAM only**. Write-back + PG mirrors retire on a defined timeline; neither gains new features.

---

## Four physical patterns (DDL doctrine)

1. **P1 — Immutable partition-swapped MergeTree** — facts, cubes, variance. Build `_stage` twin → `REPLACE PARTITION`. No mutations, no `FINAL`, no MVs on hot paths.
2. **P2 — ReplacingMergeTree(version) + FINAL** — **only tiny** dims/registries/caches where last-write-wins is the semantic.
3. **P3 — Append-only event streams** — status / intent / approval / writeback events; latest via **argMax views** (not wall-clock alone; `event_seq` is first tiebreak).
4. **P4 — Append-only ledgers / immutable snapshots / telemetry** — watermarks, approval snapshots, probe logs; never rewritten.

**Lock-free claim:** runner inserts `claimed` with a `claim_token`, reads `v_run_status*` back, proceeds **only if its token won** the argMax tiebreak.

---

## Platform / sizing honesty (verbal OK)

- One CH database **per tenant** (e.g. `cluster_briscoes`); kik identical shape.
- Fact feed = platform BQ→CH lane; module lands **nonzero slim extract** (~**10⁸** real rows / briscoes), **not** the raw **46.9B**-row / **43 TB** BQ spine (~99.8% zeros).
- At runtime **nothing reads BigQuery** for agent probes.
- PG cortex for decisions is **superseded** — decision plane lives in CH.

---

## How this maps to the resume bullet

| Resume phrase | Confluence backing |
|---|---|
| per-tenant ClickHouse | One DB per tenant |
| 63 tables / 8 layers | §3 + DDL footer |
| insert-only | Service roles INSERT-only; hot path bans UPDATE/DELETE |
| partition-swapped | P1 stage twin + `REPLACE PARTITION` |
| agent read-only | `readonly=1` / `agent_ro_*` SELECT-only |
| 189s → 12.3s (~15.5×) | **Pivot POC only** — separate source; not this page |

**Do not say:** “DDL load-tested,” “624 columns,” “CH mutations_used=0 in prod,” or invent TPS/RPM from this schema.
