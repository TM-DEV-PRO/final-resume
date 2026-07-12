# Final Resume — Tarun Mittal (Senior Software Engineer)

One repo for the resume, its Overleaf sources, and every piece of interview-prep material that backs it.

## Layout

```
resume/                      LaTeX sources (Overleaf-ready)
  resume.tex                 main file — compile this
  _header.tex, TLCresume.sty, sections/*.tex
output/
  resume.pdf                 compiled resume (1 page)
  Tarun_Mittal_Resume_Overleaf.zip   upload this zip to Overleaf as a new project
InterviewPrep.html           single-file study hub (open in a browser) — everything below, navigable
interview_prep/
  00_index.md                orientation + honesty guardrail
  projects/01..05_*.md       per-company project deep dives (architecture, DB design, tradeoffs, Q&A)
  06_tech_deep_dives.md      Go/Gin, Rust/Axum, Kafka, Flink, Spark, Pinot, FastAPI, Redis, …
  07_behavioral_star_stories.md  10 STAR stories (Amazon LPs × Googliness) + rapid-fire answers
  agentic_assort_playbook/   the full Impact Analytics playbook (§0–§10), incl. the
                             July 2026 stack direction (Go + Rust + ClickHouse end-to-end)
build_interview_prep.py      regenerates InterviewPrep.html from the markdown
```

## Rebuild

```bash
# PDF (needs tectonic: brew install tectonic) — or just upload the zip to Overleaf
cd resume && tectonic resume.tex --outdir ../output

# Study hub
python3 build_interview_prep.py
```

## Overleaf

Upload `output/Tarun_Mittal_Resume_Overleaf.zip` → New Project → Upload Project. Compiles with pdfLaTeX or XeLaTeX; main file `resume.tex`.

## Resume rules encoded here

- Google XYZ format: "Accomplished [X], as measured by [Y], by doing [Z]" on every bullet.
- Structure: company → project → bullets, with a **Tech Used** line per project.
- One page, ATS-safe (single column, standard headings, no images/tables in content).
- No Java. Stack reflects the July 2026 direction: Python (agents) · Go/Gin (non-agentic) · Rust (hot paths) · ClickHouse end-to-end.
