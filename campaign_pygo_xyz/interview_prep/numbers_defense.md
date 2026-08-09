# Resume Number Catalog / Numbers Defense (campaign_pygo_xyz)

Single interview sheet for the **PyGo XYZ campaign** PDF (same metrics as v2 honesty set). Cross-links: `../GROUND_TRUTH.md`, project packs under `projects/`, and `design_decisions_tradeoffs.md`.

## Impact Analytics

| Resume number | Why / how | Tag | Defense file |
|---|---|---|---|
| what-to-buy / how-much / which-stores | AssortSmart product job for retail planners | MEASURED framing | Overview / Copilot FRD |
| ≥20 configs vs 1 (batch design 20–100) | Copilot batch explore vs one manual attempt | TARGET / DESIGN | `10_impact_analytics_deep_dive.md` / projects packs |
| Under 1 hour (from days) | Hierarchy-to-approved-plan design goal | TARGET | same |
| **8.5% (37/437 kik)** → under 2% (target) | Measured baseline; under 2% TARGET | MEASURED / TARGET | same |
| 14 audited **read** tools + 3 confirm gates | Tools only read planning data; writes gated | DESIGN | `projects/01c_agent_read_tools_defense.md` |
| Hindsight prior-season decision layer (carry-forward, Keep/Shop/Drop, grounded narration, no-code-deploy catalogs) | Hindsight FRD FR-6.1, FR-16.5, FR-8.1, FR-1.3 | DESIGN / building | `projects/01b_hindsight_defense.md` |
| **~0.4 ms** cell edit + **sub-second** month rollup on **~25M** aggregates | Line-plan aggregate path (measured) | MEASURED | LinePlanning / `20_…` — **OMIT from PDF** (verbal/study) |
| **ONE CH bullet (PDF):** Drove Postgres→ClickHouse with row-identical **250M** heavy planning pivots **189s→12.3s (~15.5×)** | Store decision + pivot POC | MEASURED | `pivot-poc` / `21_…` |
| **63/8 insert-only / agent R/O** | Interview depth (off PDF Aug 2026) | MEASURED design | DDL Phase-1 |
| Kafka on IA Tech line | Async embedding jobs in product stack | DESIGN / product | playbook §5 / §8 |
| building not shipping | Phase 1 design PASS; load test pending | DESIGN status | Overview |

**Do NOT invent IA TPS/RPM** — none measured in IA docs.
**Do NOT put projected 12B on the PDF** — internal benchmark projection only; defend verbally if asked.

## Uber FRM

| Resume number | Why / how | Tag | Defense file |
|---|---|---|---|
| 8 screens / 30+ APIs | Product surface; code ~32 routes | MEASURED | architecture/02_uber_frm.md |
| $340M materiality / $170M residual | Q4 2025 sample | MEASURED | same |
| 70% (~2 weeks → ~3–4 days) | TDD target; baseline ESTIMATED | TARGET + EST. | same |
| MySQL SSOT + HFM vs 10-Q for PwC | Replaced Sheets close; durable line IDs | MEASURED | same |
| 55 FSLIs / 14 entities auto-flag | Group/component/residual/EMI workflows | MEASURED sample | same |
| Led 3 + 1,100+ Bazel tests | Pod leadership; pytest suite size | Confirmed / MEASURED | same |
| 11-table schema / 18-file recon migration | **Verbal only** (removed from PDF) | MEASURED | deep dive 11 |

## Uber Menu

| Resume number | Why / how | Tag | Defense file |
|---|---|---|---|
| 30K+ menus/mo · 24h→2h · $600K+/yr | Historical ops | HISTORICAL | Menu deep dive |
| Kafka ingest bus | Replayable ordered scrape events; burst + fan-out | HISTORICAL | `tech_depth/kafka_flink_scale_defense.md` |
| Flink normalize/dedupe | Keyed state + event-time after Kafka | HISTORICAL architecture | same |
| Menu peak events/sec | Do not invent; defend burst/replay not vanity TPS | ESTIMATED if asked | same |

## Masters India (consensus across past resumes)

| Resume number | Why / how | Tag |
|---|---|---|
| p95 **1.2s → 300ms** | All past resumes | HISTORICAL |
| **1,500+ clients** (not 2,500+) | Consensus | HISTORICAL |
| **1M+/day** · **100K+/import** | 4yr+ resumes | HISTORICAL |
| **700 → 4,000 requests/min** | 2.5yr + current | HISTORICAL |
| Redis −30% · triage −70% · coverage 35→82% · 98% deploy | HISTORICAL |
| No ~12 TPS / ~67 RPS on PDF | ESTIMATED derivations — verbal only | ESTIMATED |

## GeeksforGeeks

| Resume number | Why / how | Tag |
|---|---|---|
| **10K+ daily queries · 10× contest spikes** | Standardized (not 1K / not 100K) | HISTORICAL / user |
| Premium +15–20% · course sales +30% · ops +70% | HISTORICAL |
