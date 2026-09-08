# Final Java + AI — every PDF point → deep defense

Use this map in interviews. Honesty tags: MEASURED / TARGET / DESIGN / HISTORICAL / PDF (AssortSmart tab).

**Keep/Drop pipeline:** [`../docs/assort_kd_flow/PIPELINE.md`](../docs/assort_kd_flow/PIPELINE.md) · shared [`../../docs/assort_kd_flow/PIPELINE.md`](../../docs/assort_kd_flow/PIPELINE.md)

Canonical claims: [`../../docs/ASSORTSMART_TAB_RESUME.md`](../../docs/ASSORTSMART_TAB_RESUME.md)

## Summary
| # | PDF claim | Defense pack | Tag |
|---|---|---|---|
| S1 | 5y designing and owning cloud-native high-throughput distributed systems | this track objective · `31` · `41` | HISTORICAL tenure |
| S2 | Expertise in Java, Python and Go microservices; AI-assisted and RAG | `36` · `41` | framing |
| S3 | Shipping production systems; backend migrations; reliability / performance / scalability | `41` | framing |
| IA0 | Project title: **AssortSmart — Senior Software Engineer (Platform & AI)** | `23a` · PIPELINE.md | product |

## IA — Agentic Flows & Orchestration (PDF first)
| # | PDF claim | Defense pack | Tag |
|---|---|---|---|
| A1 | Keep/Drop + Missed Opportunities + Top Style · 348k article-seasons · 88k/pass · 7 lenses | `43` A1 · `23a` A1 · PIPELINE.md | PDF. $100/pass off PDF |
| A2 | 2.11B-row CH master · JSON payloads not direct DB querying · RMT · timeout → det baseline | `43` A2 · `23a` A2 | PDF |
| A3 | Shared registry · 88k survive provider failure · timeouts / breakers / checkpoints · config_hash · JSON telemetry | `43` A3 · `23a` A3 | PDF |
| A4 | Shipped Ask Iris JWT WebSocket · LangGraph supervisor · 3-attempt evaluator · LangSmith · freeze hierarchy on handshake | `43` A4 · `23a` A4 | PDF shipped capability |
| A5 | 300-case proxy · 80% CI gate · 73% cost / 100% coverage · 74% det · freeze blend weights | `43` A5 · `23a` A5 | 73% = gold-200. Gate ≠ all tenants live |

## IA — Core Infrastructure & Pipeline
| # | PDF claim | Defense pack | Tag |
|---|---|---|---|
| C1 | Go/Gin 10k peak RPS · Wire · h2c · Datadog · no reverse proxy | `43` C1 · `23a` · `10` | PDF / AssortSmart tab |
| C2 | KPI configurator / tokenizer · parameterized CH SQL · native division-by-zero (`ifNotFinite` verbal) | `43` C2 · `23a` | PDF |
| C3 | Multi-tenant data isolation + UAM access control on PG + ClickHouse · OIDC · API keys | `43` C3 · `41` | PDF |
| C4 | 15.5× · 189s to 12s on 250M-row ops · season/weekly rollups · 170GB OOM · temporal chunks · memory/spill caps | `21_ia_pivot_benchmark_source.md` · `43` C4 · `42_clickhouse_rollup_migration.md` | MEASURED POC + PDF. 55GB/16GB verbal |
| C5 | ~344k rows/s Go native-TLS pump · allowlist bypass · 4.09B · 500k double-buffer · TSV + atomic partition rollbacks | `43` C5 · `42` | PDF. Copy in flight. TSV is loader. Rollback = DROP then recopy |

## Rest of PDF
| # | PDF claim | Defense pack | Tag |
|---|---|---|---|
| FRM | 70% · 14d→3d · $340M · 19M GL · 36 Spring Boot endpoints · L1–L4 · 8-table SOADB · SHA-256 · led 3 · 100% coverage · SOX 50% delta-variance | `11_uber_frm_deep_dive.md` · `23b` | PDF |
| Menu | 24h→2h · $600K · 30K+/mo · 98% Gemini+LangChain RAG+Milvus (offline) · 95%+ · Kafka+Flink **ingestion/processing** exactly-once | `14_uber_menu_deep_dive.md` · `23b` · `41` | MEASURED / offline / HISTORICAL |
| ANZ | 99.9% · 20h/week | `23b` | HISTORICAL Mobility |
| Masters | 1.2s→300ms (75%) · 1500+ · 700→4000 rpm · Kafka+PG **high-concurrency idempotent** 1M+/day · 35%→82% · 98% deploy | `12_masters_gfg_deep_dive.md` · `23c` · `41` | HISTORICAL |
| GFG | Django · 10K+ · 10x · 20% premium · 30% sales · 70% ops | `12` · `23c` | HISTORICAL |

## Schemas · ER · APIs · design decisions
| Topic | File |
|---|---|
| IA bullet defense (current PDF Q&A) | `43_ia_bullet_defense.md` |
| Architecture diagrams | `33_architecture_diagrams.md` · `campaign_extras/interview_prep/architecture/` |
| ER + tables + why tech | `34_er_tables_tech_why.md` |
| Column schemas + API design | `35_table_schemas_api_design.md` |
| CH DDL Phase-1 (63/8 interview depth, **not** a PDF bullet) | `29_ia_ch_ddl_phase1_source.md` |
| Numbers catalog | `18_resume_number_catalog.md` · `09_metrics_derivations.md` |
| Design decisions / tradeoffs | `campaign_extras/interview_prep/design_decisions_tradeoffs.md` · `23a` |
| AI skills (LangGraph, RAG, offline eval, LangSmith) | `36_skills_ai_agents_defense.md` |
| Common Q&A | `32_common_interview_qa.md` |
| Application forms | `22_application_questions.md` · `../ApplicationKit.md` |
| Keep/Drop pipeline | `../docs/assort_kd_flow/PIPELINE.md` |

## Verbal only (not on PDF)
Cluster Recommendation Copilot · Hindsight (building / deep-dive) · 8.5% (37/437) → under 2% TARGET · 14 tools · 3 gates · 63/8 DDL · line-plan 12B → ~25M · under 1h / ≥20 configs TARGET.

| Senior screen Q&A | `37_senior_screen_deep_qa.md` |\n