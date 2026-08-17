# Final Resume — Tarun Mittal (Senior Software Engineer)

Each resume flavour is **self-contained**: LaTeX · PDF · Overleaf zip · prep · hub.

| Track | Folder | PDF | Notes |
|---|---|---|---|
| **Primary (site download)** | [`final_java_pygo_ia/`](final_java_pygo_ia/) | `Tarun_Mittal_SSE_Java_PyGoIA_Final.pdf` | Java/Spring history + PyGo IA (FastAPI/Go Gin) |
| Final Java + AI | [`final_java_ai/`](final_java_ai/) | `Tarun_Mittal_SSE_Java_AI_Final.pdf` | IA write APIs = Spring Boot |
| Final PyGo + AI | [`final_pygo_ai/`](final_pygo_ai/) | `Tarun_Mittal_SSE_PyGo_AI_Final.pdf` | Python/Go full stack |
| Source Python / Go v2 | [`resume_v2/`](resume_v2/) | `Tarun_Mittal_SSE_5yr_v2.pdf` | source track |
| Source Java / Spring | [`resume_java/`](resume_java/) | `Tarun_Mittal_SSE_Java_5yr.pdf` | source track |
| Campaign PyGo XYZ | [`campaign_pygo_xyz/`](campaign_pygo_xyz/) | `Tarun_Mittal_SSE_PyGo_XYZ.pdf` | campaign |
| Legacy | [`resume/`](resume/) | older PDF | prefer finals |

Repo hub (GitHub Pages): [`index.html`](index.html) → https://tm-dev-pro.github.io/final-resume/

Personal site download uses the **hybrid** PDF only: https://tm-dev-pro.github.io/

## Published HTML

Every markdown file in this repo is mirrored to HTML beside it, so nothing on GitHub Pages is
reachable only as raw `.md`. Two entry points:

- [`all_pages.html`](all_pages.html) — site map of every published page, grouped by track
- `<track>/InterviewPrep.html` — one-page hub containing that track's **entire** prep set

Each track also carries a screening Q&A bank at `<track>/prep/38_why_hire_tarun_qa.md`
("why should we hire you", why leaving, biggest failure, leadership, objection handling, questions
to ask them) with stack-correct wording for that track.

## Current PDF facts (Aug 2026)

- Summary is three lines; only the language stack differs per track — Java+Python, Python+Go, or
  Java+Python+Go.
- **Design Patterns** is no longer in Backend & APIs; **JUnit** is no longer in Core Engineering.
  JUnit still appears on the Uber FRM *experience* Tech line on the Java tracks.
- `final_java_pygo_ia` and `final_pygo_ai` share the same email and phone.
- Not on any PDF: Spark, Pinot, SFT, Vitess, multi-region or Kubernetes operations ownership.

## Rebuild

```bash
mkdir -p /tmp/rb && cd final_java_pygo_ia && tectonic resume.tex --outdir /tmp/rb
cp /tmp/rb/resume.pdf artifacts/Tarun_Mittal_SSE_Java_PyGoIA_Final.pdf
cd ..

python3 build_pages_html.py       # every .md → .html, folder indexes, all_pages.html
python3 build_interview_prep.py   # per-track InterviewPrep.html hubs
```
