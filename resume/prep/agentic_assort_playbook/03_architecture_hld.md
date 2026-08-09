---

# 3. Product architecture (HLD) — how the agentic planner is built

## 3.1 The planning workspace (front door)
Four surfaces sit over the staged pipeline:

- **Signals** — the agent worklist: issues/opportunities/proposals, each Accept / Skip / Edit / Dismiss with a **reason code**.
- **Pipeline** — the staged plan workflow with **cascade warnings** when an upstream edit invalidates downstream work.
- **Log** — the immutable **audit trail** (who/what/when) for every agent action + human decision.
- **Ask** — the natural-language assistant; the UX front door to the multi-agent decomposition backend.

Plus a **Today** triage bucket (Attention / Resolved / Dismissed) and **overnight** autonomous-action summaries.

## 3.2 Cascade-aware staged planning
```
Hindsight ─▶ Strategy ─▶ Clustering ─▶ Line plan / Architecture ─▶ Buy plan ─▶ Review & approve
(last season)  (targets)   (store groups)   (option counts/depth)      (qty/receipts/flow)
        │ editing an upstream stage raises a cascade warning: downstream stages recompute/invalidate
```
Each stage is agent-assisted; `getDownstreamStages()` + `showCascadeWarning()` enforce that changing, say, clustering flags that the buy plan must be recomputed.

## 3.3 Agent orchestration (the backend shape)
Concrete pattern: **Router → Orchestrator (supervisor) → specialist agents**, executing a **planner-executor DAG**. In the product this runs on **LangGraph** (Planner → Executor → Solver nodes) with a **FastMCP (Model Context Protocol)** tool layer so agents discover/execute tools safely; the offline `agentic_assort_multiagent` PoC re-implements the same shape deterministically for testability (see §8.1).

```
NL query
  │
  ▼
[Semantic cache]──hit──▶ cached answer
  │ miss
  ▼
ROUTER (LLM intent classify)  ── single ──▶ one specialist agent ─▶ answer
  │ orchestrate
  ▼
DECOMPOSER ─▶ Plan{sub_queries[], path[][]}  ─▶  plan_schema.validate()
  │                                                   │ invalid
  │                                                   ▼
  │                                          self-repair (re-prompt once)
  ▼
ORCHESTRATOR executes path stage-by-stage:
   stage 0:  [agentA ‖ agentB]      ← parallel within a stage (ThreadPoolExecutor)
   stage 1:  [agentC(<A0>)]         ← <A_n> placeholder rephrased with prior answers
   ...
  ▼
_synthesize()  ─▶  final answer (+ status: ok | partial | rejected | generic)
```

**Specialist fleet (5 agents), each `validate→fetch→analyze→narrate`:**

| Agent | Store | Job |
|---|---|---|
| AssortmentData | BigQuery `fact_sales` | KPI snapshots, top/bottom-N |
| Clustering | Postgres `store_cluster` | cluster membership / tier / profile |
| Hindsight | BigQuery `causal_drivers` | rank KPI drivers by contribution (causal DAG "why") |
| LinePlan | Postgres `line_plan` | option counts / depth / phasing, Δ vs LY |
| Recommendation | BigQuery `ros_recommendations` | ROS-based option-count uplift + gap flags |

**Resilience:** `BaseAgent.answer()` never raises → `AgentResult(status="error")` → orchestrator still synthesizes a **partial** answer; transient `fetch()` wrapped in exponential-backoff retries.

## 3.4 The pivot planning grid (edit surface)
A React grid (`planning-grid-3.jsx`) with: drag **dimension tiles** into Row/Column/Filter axes (`PivotPanel`/`AxisZone`/`DimTile`); **Override / Variance / Diff** cells (`OvCell`/`VarCell`/`DiffCell`); **BulkEdit** (apply %, set, spread); **reason capture**; **downstream impact** panel; **version drawer** (compare/restore); and a custom **`useUndoRedo`** history. This grid is *why* the persistence layer must support versions/variance/diff — which is exactly what the insert-only ClickHouse model (below) provides natively.

## 3.5 The first shipping module — the Cluster Recommendation Copilot
The agentic pattern above is now being instantiated for real in the **clustering module** (FRD v1.8): one dedicated agent, two entry surfaces (manual wizard with inline recommendations + chat-native), **deterministic tools on a dedicated ClickHouse read plane** (p95 <500 ms target vs 1–20 s on shared BigQuery slots), an LLM that orchestrates and explains but never computes, **three confirm gates**, and write-back into the existing product tables unchanged. Delegation ladder: **L1 copilot → L2 autopilot-with-approval → L3 standing drift monitor** — nothing auto-finalizes. Full what/why/how, measured baselines, targets, rollout phases and module-specific Q&A: **§9**.

## 3.6 The wider CortexEye agentic platform (context you can speak to)
The agentic backend descends from CortexEye — a **4-service** system:
- **Frontend** — React + Redux, **Socket.IO** streaming, AG Grid, Highcharts.
- **Data API** — **Rust (Axum / Tokio / SQLx)**, `gcp-bigquery-client` — the deterministic data layer (no LLM).
- **`genai`** — Python + **LangGraph** + FastAPI: intent classification (`causal > data > insights`), entity extraction (parallel via `asyncio.gather`), **text-to-SQL** (LlamaIndex RAG + GPT-4o) on BigQuery, **confidence scoring** (rules + LLM logprobs).
- **`cortexeye-ai`** (Deep Research) — Python + LangGraph: the strong **sub-query decomposer** (`{question[], path[][]}` + `<A_n>` dependency rephrasing + reflection loop), hybrid **BM25 + dense (pgvector) retrieval + Cohere rerank**, semantic cache.
Cross-cutting: **Redis** (chat history, semantic cache, abort flags across Cloud Run replicas), **Postgres via PgBouncer** (`aiopg`), **GCS** (audio/images), progress streamed over **WSS**.
