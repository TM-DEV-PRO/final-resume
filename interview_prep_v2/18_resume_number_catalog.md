# Resume Number Catalog (every PDF metric, money, and rationale)

Single interview sheet for **v2 and Java** PDFs. Cross-links: `GROUND_TRUTH.md`, `09_metrics_derivations.md`, project deep dives.

## Impact Analytics

| Resume number | Why / how | Tag | Defense file |
|---|---|---|---|
| 20–100 configs vs 1 | Copilot batch eval vs one manual clustering attempt | TARGET | `10_impact_analytics_deep_dive.md` |
| Under 1 hour (from days) | Hierarchy-to-finalized-plan design goal | TARGET | same |
| 8.5% → under 2% failures | 37/437 measured baseline; under 2% target | MEASURED / TARGET | same |
| 100% reproducible | Persist winning config + seed | TARGET | same |
| p95 probes <500ms vs 1–20s BQ | Shared BigQuery variance vs dedicated CH | MEASURED / TARGET | same |
| Datadog / LangSmith / PostHog + OTEL | L2 platform / L1 agent / product analytics; shared `trace_id` | MEASURED design | HLD + `10_…` §6 |
| **ClickHouse/GCS end-to-end planning store** | Insert-only versioned writes; HLD doing layer → CH/GCS | MEASURED design | stack direction + HLD |
| **250M pivot 189s → 12.3s (~15×)** | Heavy grid + option-count; ~15.5× DISTINCT; typical ~2–3× | MEASURED | Pivot + consolidated POC / `10_…` |
| **Avoided 12B store-week (100–450×)** | Aggregate ~25M; explode ~25 ms; schema &gt; engine | MEASURED | LinePlanning / `10_…` |
| Hardware caveat (Jul 2026 POC) | PG 48 GB host vs CH 10 CPU / 3.3 GB VM | MEASURED | same |
| PG cell &lt;1ms / hybrid verdict | POC decision history (legacy OLTP / why insert-only unlock) | MEASURED prep | consolidated POC |
| 60×; 23.7M; 3m40s → 3.86s | Order Batching (**prep depth**) | MEASURED | older POC dump / `10_…` §5 |
| 24×; 250K → 5.9M rows/s | Insert POC (**prep**) | MEASURED | same |

## Uber FRM

| Resume number | Why / how | Tag | Defense file |
|---|---|---|---|
| 8 screens / 30+ APIs | Product surface; code ~32 routes | MEASURED | `11_uber_frm_deep_dive.md` |
| $340M materiality | Q4 2025 sample metric | MEASURED | same |
| 70% (~2 weeks → ~3–4 days) | TDD target; baseline ESTIMATED analyst calendar | TARGET + EST. | same + `09_metrics_derivations.md` |
| 11 tables / 55 lines / 14 entities | ORM models + sample FSLIs/entities | MEASURED | same |
| 18 files recon v2 | `RECON_API_MIGRATION.md` | MEASURED | same |
| Led 3 engineers | User-confirmed EPAM pod | Confirmed | same |

## Uber Menu (money + streaming)

| Resume number | Why / how | Tag | Defense file |
|---|---|---|---|
| 30K+ menus/mo | Historical volume | HISTORICAL | `14_uber_menu_deep_dive.md` |
| 24h → 2h | Onboarding cycle | HISTORICAL | same |
| **$600K+/yr** | Kill ~$2/menu tool: 30K×$2×12=$720K list → floor $600K+ | HISTORICAL | same + `09_…` |
| Kafka ~200–500 peak events/sec | Fleet-run item/retry amplification | ESTIMATED | same |
| Flink online normalize/dedupe | Event-time keyed state; best-fit project for Flink | HISTORICAL role | same |
| Spark backfills (~1–2M rows) | Historical reprocess / joins | HISTORICAL / EST. | same |
| +95% ingestions | Proxy/IP rotation; baseline ~60–65% EST. | HISTORICAL | same |
| 98% / 100% schema | Offline SFT eval | HISTORICAL | same |
| 99.9% / 20h week | ANZ compliance automation | HISTORICAL | same |

## Masters India

| Resume number | Why / how | Tag | Defense file |
|---|---|---|---|
| 1.2s → 300ms p95 | Async rewrite + pooling + indexes | HISTORICAL | `12_masters_gfg_deep_dive.md` |
| 1,500+ clients | Prefer 1500+ | HISTORICAL | same |
| 100K+/import; 1M+/day | Bulk IRP path | HISTORICAL | same |
| ~12 TPS; 100+ peak | 1M/86400≈11.6; peaks EST. | ESTIMATED | `09_…` |
| 700 → 4,000 RPM (~67 RPS) | Gateway throughput | HISTORICAL | same |
| Redis −30% | Cache-aside hot keys | HISTORICAL | same |
| Idempotency / DLQ | Fault tolerance vs IRP flakes | HISTORICAL | same |
| Triage −70% (~30→<10 min) | ELK + New Relic correlation | HIST. / EST. | same |
| 35% → 82% coverage; 98% deploys | CI gates | HISTORICAL | same |

## GeeksforGeeks + Achievements

| Resume number | Why / how | Tag | Defense file |
|---|---|---|---|
| 10K+ daily queries; 10× spikes | Standardized scale | User / EST. | `12_…` |
| Premium +15–20%; courses +30%; ops +70% | Relative / business attribution | HISTORICAL | same |
| Code Jam 2260/37k+; SIH top 3 | Public contests | HISTORICAL | activities |
| Certificates | Verified URLs | MEASURED | `certificates.txt` |

## Explicit non-claims (do not invent)

Pinot on current PDF · Terraform · multi-region ownership · K8s cluster ops · FRM 19M→300K · FRM measured 70% · identical CH hardware · full PG→CH production cutover · IA people leadership · Spark/Flink at Masters India or IA (Menu only)
