# Architecture — Impact Analytics AssortSmart (Platform & AI)

**PDF (Sep 2026):** two subsections — Core Infrastructure & Pipeline, Agentic Flows & Orchestration.
**Verbal only / not on PDF:** Cluster Recommendation Copilot · Hindsight (keep FRD notes below labeled as such).
Canonical: `docs/ASSORTSMART_TAB_RESUME.md`.

## 1. Where each tech is used (PDF)

| Tech | Where | Why |
|---|---|---|
| **Go / Gin + Wire** | Multi-tenant HTTP edge, 10k peak RPS | Compile-time DI, h2c, nested timeouts |
| **Datadog** | Distributed tracing on the edge | Debug 10k RPS without a reverse proxy |
| **ClickHouse** | 250M pivots, 1.6M article-seasons, 2.4B rollups, 2.11B fact | Columnar planner analytics |
| **ifNotFinite parser** | KPI configurator | Safe operator SQL without deploys |
| **Firebase / JWT / OIDC + Redis + Postgres** | Auth waterfall + roles | Tenant + UAM boundaries |
| **golangci-lint / SAST/SBOM / 1200+ tests** | Bitbucket CI | Zero-regression gate |
| **Python, FastAPI, LangGraph / LangGraph** | Keep/Drop lenses + Ask Iris Supervisor+Evaluator | Stateful agent graphs, not chatbots |
| **LangSmith + JSON telemetry** | Token cost, step duration, fallbacks | Eval + cost control |
| **ReplacingMergeTree** | Two-phase inserts after air-gapped LLM | Idempotent fact writes |

Kafka / Flink / Spark / K8s-ops are **not** IA PDF claims (Menu owns Kafka+Flink).

## 2. ASCII (PDF-honest)

```
[ Planner UI / Ask Iris WebSocket ]
              │
[ Go/Gin edge — Wire, h2c, 10k peak RPS, Datadog ]
              │
     ┌────────┼─────────────┬──────────────────┐
     ▼        ▼             ▼                  ▼
  Redis    Postgres     ClickHouse        Python agents
  auth     roles/UAM    2.11B fact        Keep/Drop + Missed Opp + Top Style
  cache                 2.4B rollups      7 lenses, 88k/pass <$100
                        RMT two-phase     air-gap LLM (JSON) vs DB
                        ifNotFinite KPI   breakers / checkpoints
                                          Ask Iris Supervisor+Evaluator
                                          frozen socket scopes
                                          300-case / 80% gate vs 74% baseline
```

Packet diagrams that show Kafka→Flink→CH on IA, or K8s as “owned ops,” are **overclaim**. Use them only as generic study sketches, never as “what I shipped on AssortSmart.”

## 3. Stores

### ClickHouse
- Fact **2.11B** (PDF). Rollups **2.4B** weekly (PDF). Pivot POC **250M / 189s→12s** (MEASURED).
- Engine: **ReplacingMergeTree** two-phase; agent path air-gapped from SQL writes.
- Verbal depth: 63/8 insert-only DDL (`29_ia_ch_ddl_phase1_source.md`) — **not** a PDF bullet.

### PostgreSQL
- Roles / tenant / workflow — not the heavy grid.

### Milvus
- **Menu RAG**, not IA PDF.

## 4. Hindsight / Cluster Copilot

**Verbal only / not on PDF.** Tenant catalogs without code deploy, carry-forward Keep/Shop/Drop, 14 tools / 3 gates — interview depth only. See `../projects/01b_hindsight_defense.md`.

## 5. Observability (Datadog JSON — packet, IA-honest)

Every Go/Python service should emit structured JSON Datadog can facet:

```json
{
  "timestamp": "2026-09-03T03:40:39.123Z",
  "level": "ERROR",
  "service": "assortsmart-edge",
  "env": "production",
  "trace_id": "4a6f8c9b2e1d3f5a",
  "span_id": "8b2d1c4f5a6e3",
  "tenant_id": "tenant_xyz_99",
  "message": "LLM batch fallback to deterministic score",
  "metadata": { "pipeline": "keep_drop", "batch_id": "b_981273" }
}
```

Honesty: do not claim `dd.trace_id` log injection if the repo does not inject it — correlate via your explicit `trace_id` field + Datadog traces.\n