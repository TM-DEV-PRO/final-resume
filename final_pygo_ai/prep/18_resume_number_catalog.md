# Resume Number Catalog (every PDF metric)

Single interview sheet for `Tarun_Mittal_SSE_5yr.pdf`. Cross-links: `GROUND_TRUTH.md`, `09_metrics_derivations.md`, `23a`/`11`/`14`.
Source for new IA scale numbers: **AssortSmart tab / PDF**.

## Impact Analytics — on PDF

| Resume number | Why / how | Tag | Defense |
|---|---|---|---|
| **10k peak RPS** | Go/Gin HTTP edge | PDF | `43` C1 · `23a` |
| Wire · h2c · Datadog · no reverse proxy | Self-protecting edge | PDF | `43` C1 |
| **189s → 12s** (~15.5×) on **250M-row** ops | Row-identical PG vs CH POC (PDF rounds 12.3→12) | MEASURED POC | `21` · `43` C4 |
| **170GB** OOM · temporal chunks · memory/spill caps | Write-time weekly GROUP BY | PDF. 55GB/16GB verbal | `42` · `43` C4 |
| **348k article-seasons** · Keep/Drop + Missed Opp + Top Style | Scored volume | PDF | `43` A1 |
| **88k** items/pass · **7** AI lenses | Batch inference | PDF. $100/pass off PDF | `43` A1 |
| **2.11B-row** CH master · JSON payloads · RMT · timeout fallback | Isolation | PDF | `43` A2 |
| Registry · breakers · checkpoints skip det · config_hash | Orchestration | PDF | `43` A3 |
| Ask Iris JWT WS · 3-attempt evaluator · handshake freeze · LangSmith | Copilot | PDF shipped capability | `43` A4 |
| **300-case** · **80%** CI gate | Proxy gold `eval.json` | promotion gate ≠ all tenants live | `43` A5 |
| **73%** cost · **100%** coverage | gold-200 Luna vs mini | **not** the 300-case file | `43` A5 |
| **74%** det baseline · freeze weights | Production det threshold 0.65 on gold-200 | PDF | `43` A5 |
| ~**344k rows/s** · **4.09B** · 500k double-buffer · partition rollbacks | Go native-TLS pump | PDF. Copy in flight | `43` C5 · `42` |
| KPI tokenizer · division-by-zero | `ifNotFinite` wrap | PDF | `43` C2 |
| Firebase → JWT/OIDC · Redis · Postgres roles | Auth waterfall + UAM | PDF | `43` C3 |

## Impact Analytics — verbal only (not on PDF)

| Number | Tag | Notes |
|---|---|---|
| **$100**/pass token spend | MEASURED, off PDF | Dropped from this PDF for space |
| **1.6M** article-seasons (catalog) | verbal | Do not mix with 348k scored |
| **55GB** cap / **16GB** spill / one fiscal week | verbal OOM knobs | PDF says temporal chunks |
| **100.0%** coverage · **1,200+** Go tests | LinkedIn / verbal | Off PDF |
| ≥20 configs / under 1h / 8.5% (37/437) → under 2% / 14 tools / 3 gates | TARGET / DESIGN / MEASURED baseline | Cluster Copilot — not a PDF bullet |
| 63/8 DDL · ~12B → ~25M · ~0.4 ms cell | DESIGN / PROJECTED / MEASURED agg | Interview depth |
| p95 probes <500ms vs 1–20s BQ | TARGET / MEASURED BQ variance | Verbal |

Do **not** invent extra IA TPS beyond PDF **10k peak RPS**.

## Uber FRM (PDF)

| Resume number | Tag | Notes |
|---|---|---|
| **70%** · **14 days → 3 days** | PDF outcome | Older prep said TARGET; defend PDF |
| **$340M** materiality · **19M** raw GL rows | PDF | |
| **36 Spring Boot endpoints** · L1–L4 FSLI · quarter-annualization | PDF | 8 screens remain verbal product depth |
| **8-table** MySQL SOADB · SHA-256 keys · optimistic locking | PDF | 11 ORM models = verbal schema depth |
| Led **3** · **100%** statement coverage · SOX **50%** delta-variance | PDF | |

## Uber Menu / ANZ

| Resume number | Tag |
|---|---|
| 24h→2h · $600K/yr · 30K+/mo · 95%+ | HISTORICAL |
| 98% field fidelity Gemini+LangChain+Milvus | **offline eval** |
| Kafka + Flink keyed dedupe · exactly-once upserts | PDF |
| Spark | **not on PDF** — verbal backfill only |
| ANZ 99.9% · 20h/week | HISTORICAL Mobility |

## Masters / GFG

| Resume number | Tag |
|---|---|
| p95 1.2s→300ms (75%) · 1,500+ · 700→4,000 rpm · 1M+/day · 100K+ · Redis −30% · coverage 35→82% · 98% deploy | HISTORICAL · Spring Boot |
| GFG 10K+ · 10x · 20% premium · 30% sales · 70% ops | HISTORICAL Django |\n