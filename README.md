# Final Resume — Tarun Mittal (Senior Software Engineer)

Three maintained, self-contained final tracks: LaTeX · PDF · Overleaf zip · prep · hub.

| Track | Folder | PDF | Notes |
|---|---|---|---|
| **Primary (site download)** | [`final_java_pygo_ia/`](final_java_pygo_ia/) | `Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf` | Java/Spring history + PyGo IA (FastAPI/Go Gin) |
| Final Java + Python | [`final_java_ai/`](final_java_ai/) | `Tarun_Mittal_SSE_5yr_Java_AI.pdf` | IA write APIs = Spring Boot |
| Final Python + Go | [`final_pygo_ai/`](final_pygo_ai/) | `Tarun_Mittal_SSE_5yr.pdf` | Python/Go full stack |

Repo hub (GitHub Pages): [`index.html`](index.html) → https://tm-dev-pro.github.io/final-resume/

Personal site download uses the **hybrid** PDF only: https://tm-dev-pro.github.io/

## Published HTML

Every markdown file is mirrored to HTML beside it. Entry points:

- [`all_pages.html`](all_pages.html) — site map
- `<track>/InterviewPrep.html` — full prep hub
- [`docs/assort_kd_flow/PIPELINE.md`](docs/assort_kd_flow/PIPELINE.md) — Keep/Drop bake→promote pipeline source

## Current PDF facts (Sep 2026)

- Two-page layout; contact identity is on page 1 only (no repeating header on page 2).
- IA is structured as **Agentic Flows & Orchestration** then **Core Infrastructure & Pipeline**.
- Headline IA numbers: 348k article-seasons, 88k/pass, JSON payloads vs 2.11B master, Ask Iris JWT + 3-attempt evaluator, 300-case / 80% gate, 73% cost / 100% coverage vs 74% det; Go/Gin 10k RPS, KPI tokenizer, isolation, 15.5× (189s to 12s on 250M-row ops) with 170GB OOM / temporal chunks, Go pump ~344k rows/s up to 4.09B with partition rollbacks.
- Off PDF / verbal: $100/pass, 1.6M catalog, 55GB/16GB knobs, 100% Go coverage / 1,200+ tests.
- FRM: 70% (14 days → 3 days), 19M GL rows, 36 endpoints, L1–L4. Menu: 24 hours → 2 hours, $600K.
- Cluster Recommendation Copilot and Hindsight remain **verbal / deep-dive only**.
- `final_java_pygo_ia` and `final_pygo_ai` share email/phone.

## Rebuild

```bash
mkdir -p /tmp/rb && cd final_java_pygo_ia && tectonic resume.tex --outdir /tmp/rb
cp /tmp/rb/resume.pdf artifacts/Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf
cd ..

python3 build_pages_html.py       # every .md → .html, folder indexes, all_pages.html
python3 build_interview_prep.py   # per-track InterviewPrep.html hubs
```
