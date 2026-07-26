# Agentic AssortSmart — flow, guardrails, evals, benchmarking honesty

**PDF sync:** failures **8.5% (37/437)** MEASURED · under **2%** TARGET · **14** read tools + **3** gates · LangSmith on Tech · load test **pending** (say **building**).

---

## 1. End-to-end flow (say this out loud)

```text
Planner chat (UI)
  → FastAPI Agent Service (LangGraph graph)
      → MCP / audited tools (14) — READ planning data only
      → optional LLM plan / tool selection (OpenAI / Gemini / Claude)
  → Go (Gin) doing layer — Clustering / Hindsight / Strategy APIs
      → ClickHouse (append-only planning store) + product write APIs
  → 3 human confirm gates before any plan/cluster write-back
  → Telemetry: LangSmith (agent) + Datadog (platform) + PostHog (product)
      joined by shared OTEL trace_id
```

**One sentence:** The LLM proposes and reads; the deterministic engine computes; humans approve; writes go through product APIs — never free-form model SQL.

---

## 2. Guardrails (what stops bad writes)

| Layer | Mechanism | Why |
|---|---|---|
| Tool allow-list | **14** audited tools only | No raw SQL shell / arbitrary code |
| Read scope | Tools **only read** planning/clustering data | Separates explore from mutate |
| Input grounding | Catalog backtrack, fiscal calendar, sample-size guards | Cuts input-boundary failures (majority of the **8.5%**) |
| k / scenario caps | Client min/max k, child-cluster cap (~10), UI **3–5** scenarios | Business guardrails over pure silhouette optimum |
| Human gates | **3** confirm steps before write-back | Money decisions stay human-owned |
| Content-addressed config | Persist recipe + data watermark / seed | Moves reproducibility **0% → 100%** (TARGET) |
| Quotas / timeouts | Per-tenant concurrency and tool budgets | Protect CH and Go from agent storms |

**Auth / rate-limit deep dive:** [../tech_depth/auth_tenancy_rate_limits.md](../tech_depth/auth_tenancy_rate_limits.md)

**Do not say:** "the agent never fails" or "we never write SQL." Say: tools are read-scoped; humans gate writes; engineers still write SQL in services.

---

## 3. Evaluations (what exists today)

### Offline / design evals (use these)

| Eval | What it measures | Status |
|---|---|---|
| Failure taxonomy on kik | **37/437 = 8.5%** run failures; &gt;80% input-boundary | MEASURED baseline |
| Clustering job latency | Median **~20s** over **370** live runs | MEASURED (engine, not full agent chat) |
| Reproducibility audit | Winning config/seed not persisted → **0%** | MEASURED baseline |
| Tool-contract tests | Allow-list, schema validators, no write paths on tools | DESIGN / CI |
| LangSmith run replay | Prompt version, tool args, tokens/cost on agent trees | DESIGN instrumentation |
| Scenario quality rubric | Distinct lens / horizon / scope / k; evidence attached | DESIGN (HLR) |
| Batch breadth | **20–100** configs explored under the hood; UI still **3–5** | TARGET / design |

### Production agentic-flow benchmark (honesty)

**We have not finished a production load test that proves** "days → under 1 hour" or "8.5% → under 2%" on the **full chat → tools → Go → CH → gate → write** path.

Correct interview lines:
- "Baselines are measured on live clustering runs (kik)."
- "Targets are design goals we engineer against."
- "Phase 1 design passed external review; **load test pending** — I say **building**, not shipped."
- "LangSmith is for agent-quality evals and regression; Datadog pages platform SLOs."

**Wrong line:** "We benchmarked the agentic flow in production and hit under 2% / under 1 hour."

---

## 4. How we will / do benchmark (method, not fake results)

When asked "how do you benchmark?":

1. **Baseline freeze** — failure rate, median job time, repro rate on a named tenant extract (already have kik numbers).
2. **Offline agent suites** — fixed planner prompts → expected tool sequences → golden evidence bundles in LangSmith datasets.
3. **Tool latency SLOs** — p95 per tool against CH; reject tools that scan unbounded.
4. **Gate funnel metrics** — % sessions that reach each of the 3 confirms; abandon rate (PostHog).
5. **Load test (pending)** — concurrent planners × tool fan-out × Go/CH; declare pass only when TARGET metrics hold under load.
6. **Canary** — one tenant first; compare failure class mix before expanding.

---

## 5. Whole safety story in 30 seconds

"Measured **8.5%** clustering failures on kik, mostly bad inputs. We cut that class with grounded tools and validators, explore many configs in batch, and require **three human confirms** before write-back through the Go APIs. Agent quality is traced in LangSmith; platform health in Datadog. Under **2%** and under **1 hour** are targets until load test lands."

## Related
- [01c_agent_read_tools_defense.md](01c_agent_read_tools_defense.md)
- [01_ia_deep_dive.md](01_ia_deep_dive.md) § observability
- [../architecture/01_ia_assortsmart_hindsight.md](../architecture/01_ia_assortsmart_hindsight.md)
