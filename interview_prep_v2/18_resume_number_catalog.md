# Resume Number Catalog (every PDF metric, money, and rationale)

Single interview sheet for **v2 and Java** PDFs. Cross-links: `GROUND_TRUTH.md`, `09_metrics_derivations.md`, project deep dives.

## Impact Analytics

| Resume number | Why / how | Tag | Defense file |
|---|---|---|---|
| what-to-buy / how-much / which-stores | AssortSmart product job for retail planners | MEASURED framing | Overview / Copilot FRD |
| ≥20 configs vs 1 (batch design 20–100) | Copilot batch explore vs one manual attempt | TARGET / DESIGN | `10_impact_analytics_deep_dive.md` |
| Under 1 hour (from days) | Hierarchy-to-approved-plan design goal | TARGET | same |
| **8.5% (37/437 kik)** → under 2% (target) | Measured baseline; under 2% TARGET | MEASURED / TARGET | same |
| 14 read-only tools + 3 confirm gates | Agent never writes SQL | DESIGN | Overview / FRD |
| **~0.4 ms** cell edit + **sub-second** month rollup | Line-plan aggregate on PG (measured) | MEASURED | LinePlanning / `20_…` |
| Projected **12B** → **~25M** aggregate | Schema win; 12B PROJECTED | PROJECTED / MEASURED | same |
| **ONE CH bullet:** 63/8 insert-only / partition-swapped + agent R/O + **250M 189s→12.3s (~15.5×)** | Store design + pivot POC | MEASURED design + MEASURED | DDL Phase-1 (`29_…`) + `pivot-poc/` |
| Typical CH aggs ~2–3× if DISTINCT stripped | Adversarial correction — verbal only | MEASURED | `21_…` |
| p95 probes <500ms vs 1–20s BQ | Shared BQ variance vs dedicated CH | MEASURED / TARGET | Copilot FRD |
| building not shipping | Phase 1 design PASS; load test pending | DESIGN status | Overview |

**Do NOT invent IA TPS/RPM** — none measured in IA docs.

## Uber FRM

| Resume number | Why / how | Tag | Defense file |
|---|---|---|---|
| 8 screens / 30+ APIs | Product surface; code ~32 routes | MEASURED | `11_uber_frm_deep_dive.md` |
| $340M materiality | Q4 2025 sample metric | MEASURED | same |
| 70% (~2 weeks → ~3–4 days) | TDD target; baseline ESTIMATED | TARGET + EST. | same |
| 11 tables / 55 lines / 14 entities | ORM models + sample | MEASURED | same |
| 18 files recon v2 | `RECON_API_MIGRATION.md` | MEASURED | same |
| Led 3 engineers | User-confirmed EPAM pod | Confirmed | same |

## Uber Menu

| Resume number | Why / how | Tag | Defense file |
|---|---|---|---|
| 30K+ menus/mo · 24h→2h · $600K+/yr | Historical ops | HISTORICAL | `14_uber_menu_deep_dive.md` |
| 98% fidelity / 100% schema | Offline eval | HISTORICAL | same |
| 95%+ ingest / ANZ 99.9% / 20h/week | Anti-bot + compliance | HISTORICAL | same |
| No Kafka/Flink/Spark on Menu PDF | Mayank-style streaming → Masters | Decision | `GROUND_TRUTH.md` |

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
