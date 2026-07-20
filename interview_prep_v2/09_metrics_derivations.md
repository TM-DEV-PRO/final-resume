# Metrics Derivations (resume v2 + Java tracks)

Every TPS / RPS / from-to / money number on the **current** v2 and Java PDFs. Interview line: say **"estimated, derived from X"** for ESTIMATED and **"measured / documented"** for MEASURED or HISTORICAL. Do not invent finer precision than this table.

| Tag | Meaning |
|---|---|
| **MEASURED** | Documented in POC / code / Confluence |
| **TARGET** | Design goal; say "targeting" |
| **HISTORICAL** | From past resumes / own experience |
| **ESTIMATED** | Derived arithmetic; say so |

---

## Decision log: Spark, Flink, Pinot, Terraform, multi-region, K8s ops

| Tech | Resume decision | Why |
|---|---|---|
| **Spark + Flink on Uber Menu** | **ON resume (restored Jul 2026)** | Best fit: scrapers → Kafka → Flink online → Spark backfills. Matches original event-driven Menu bullet. Peak events/sec and Spark row counts ESTIMATED. |
| **Pinot** | Off one-pager | Space + weaker need vs Flink/Spark for ATS; keep verbal if asked about health dashboards. |
| **Kafka** | Skills + Menu + Masters | Menu bus + Masters e-invoice async. |
| **Terraform / multi-region / K8s cluster ops** | **OMIT** experience; STUDY ONLY in `17_senior_systems_study_only.md` | No 95%+ personal ownership evidence. Kubernetes stays skills-listed only. |
| **ClickHouse** | Keep as **POC** bullet | MEASURED benchmarks; not a full production cutover claim. |

---

## 1. Impact Analytics — AssortSmart + PG→CH POC

| Claim on resume | Tag | Derivation / source |
|---|---|---|
| 20 to 100 configs per plan vs 1 manual | TARGET / design | Copilot Phase 1 FRD (`2817589251`); batch eval goal |
| Turnaround under 1 hour (from days) | TARGET | Same FRD; say targeting |
| Failures under 2% from 8.5% | MEASURED baseline / TARGET | 8.5% = 37/437 runs MEASURED; under 2% TARGET |
| 100% reproducible clusters | TARGET | Config/seed persistence design |
| p95 probes under 500ms vs 1 to 20s BigQuery | MEASURED baseline / TARGET | Shared BigQuery slots 1–20s+; CH target p95 <500ms |
| **60x** Order Batching; **23.7M** rows; **3m 40s → 3.86s** | MEASURED | `2707030040` / `BENCHMARK-NUMBERS.md`: 23,749,263 join rows; CH 3.857s; PG 3m40s UTC / 7m48s Melbourne TZ |
| **24x (250K → 5.9M rows/sec)** | MEASURED | CH 5,907,446 rows/s on 3.9B rows vs PG raw 250K (~23.6× → resume 24×). Also own ~14× vs PG detach/attach ~417K |
| Hardware caveat | MEASURED | PG 32 vCPU / 256 GB tuned; CH 16 vCPU / 64 GB untuned. POC, not identical A/B, not full cutover |

**Rapid fire:** Lead with hardware caveat. Cite both PG times. Defend 24× vs raw 250K; if challenged, also cite ~14× vs detach/attach.

---

## 2. Uber FRM Scoping

| Claim on resume | Tag | Derivation / source |
|---|---|---|
| 8 screens, **30+ REST APIs** | MEASURED | Code: ~32 routes including health. Do **not** say 36. |
| **$340M** group materiality | MEASURED | Q4 2025 sample metrics / CSVs |
| **70% cut (~2 weeks → ~3–4 days)** | TARGET + ESTIMATED baseline | 70% is TDD project target (not measured). From-to ESTIMATED analyst calendar time for manual Sheets recon/scoping. Say "targeting". |
| 11 table schema, 55 line items, 14 entities | MEASURED | 11 SQLAlchemy models; ~26 BS + ~29 IS ≈ 55; 14 entities in sample |
| Recon v2 **18 files**, +1,268 LOC | MEASURED | `RECON_API_MIGRATION.md` |
| 10-Q validation | MEASURED | Recon HFM vs financial statement amounts |

**Do not claim:** 19M→300K rows (UNSUPPORTED), FRM p95 <300ms as measured, 100% coverage as resume fact.

**Rapid fire:** *"Is 70% measured?"* — No. TDD target. Baseline ~2 weeks of analyst work to ~3–4 days is the ESTIMATED from-to I use when asked for brackets.

---

## 3. Uber Menu Ingestion (Selenium → Kafka → Flink → Spark)

| Claim on resume | Tag | Derivation / source |
|---|---|---|
| **30K+** menus/month | HISTORICAL | Original / 4yr resume |
| Onboarding **24h → 2h** (90%) | HISTORICAL | Same |
| **$600K+** annually | HISTORICAL arithmetic | ~$2/menu × 30K × 12 = $720K list → floor $600K+ |
| Kafka **~200–500 peak events/sec** | ESTIMATED | Fleet-run amplification of menu/item/retry events |
| **Flink** normalize/dedupe online | HISTORICAL role | Event-time keyed processing; load ESTIMATED at Kafka peak |
| **Spark** backfills | HISTORICAL role / ESTIMATED volume | ~1–2M item rows for typical reprocess window |
| +**95%** successful ingestions | HISTORICAL; baseline ESTIMATED | ~60–65% → 95%+ |
| **98%** fidelity, **100%** schema consistency | HISTORICAL offline eval | Say offline/eval |
| ANZ **99.9%**, **20 h/week** saved | HISTORICAL | Separate track |

**Money deep dive:** Unit cost killed ≈ $2/menu. Monthly $60K. Annual list $720K. Resume floors at $600K+.

**Rapid fire:** Flink = online path; Spark = backfill. Masters India Kafka is a different product. Deep defense: `14_uber_menu_deep_dive.md`.

---

## 4. Masters India GST

| Claim on resume | Tag | Derivation / source |
|---|---|---|
| p95 **1.2s → 300ms** | HISTORICAL | All resumes agree ~1000–1200ms → 300–400ms |
| **1,500+** clients | HISTORICAL | Prefer 1500+; drop 2500+ |
| **100K+/import**, **1M+ daily** | HISTORICAL | Past resumes |
| **~12 TPS avg, 100+ peak** | ESTIMATED | 1M / 86,400 ≈ 11.6 TPS. Peaks ~8–10× on filing deadlines |
| **700 → 4,000 req/min (~67 RPS)** | HISTORICAL | 4000/60 ≈ 66.7 RPS |
| Redis **-30%** redundant reads | HISTORICAL | Cache-aside |
| Idempotency / retries / DLQ | HISTORICAL narrative | Fault-tolerance bullet |
| Triage **70%** (**~30 min → <10 min**) | HISTORICAL / ESTIMATED baseline | ELK + New Relic |
| Coverage **35% → 82%**, **98%** deploy success | HISTORICAL | CI gates |

---

## 5. GeeksforGeeks

| Claim on resume | Tag | Derivation / source |
|---|---|---|
| **10K+** daily queries | User-standardized | Older resumes conflicted (1K / 100K); use 10K+ |
| **~1–2 RPS avg, ~10× contest spikes** | ESTIMATED | 10K/86,400 ≈ 0.12 RPS if literal queries; treat as order-of-ten-thousand daily interactions with contest spikes ~10× |
| Premium **+15–20%** relative | HISTORICAL | Relative lift; no absolute baseline |
| Course sales **+30%**, ops **+70%** | HISTORICAL | Business attribution; own engineering |

---

## 6. Achievements

| Claim | Tag | Source |
|---|---|---|
| Code Jam **2260 / 37,000+** | HISTORICAL | Past resumes |
| SIH 2020 finalist top 3 nationally | HISTORICAL | Past resumes |
| Global AI Hackathon EPAM | HISTORICAL | User / EPAM |
| Certificates HackerRank + LangChain Academy | MEASURED | `certificates.txt` |
| CGPA 7.7 | MEASURED | Kept in GROUND_TRUTH only; **removed from PDFs** |
