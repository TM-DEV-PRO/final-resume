# Final Resume — Tarun Mittal (Senior Software Engineer)

One repo for the resume, its Overleaf sources, and every piece of interview-prep material that backs it.

**Two tracks (same projects/metrics, different primary stack):**

| Track | Resume PDF | Sources | Interview prep |
|---|---|---|---|
| Python / Go (default) | `Tarun_Mittal_SSE_5yr.pdf` | `resume/` | `interview_prep/` |
| Java / Spring | `output/Tarun_Mittal_SSE_Java_5yr.pdf` | `resume_java/` | `interview_prep_java/` |

## Layout

```
resume/                      LaTeX sources — Python/Go track (Overleaf-ready)
  resume.tex                 main file — compile this
  _header.tex, TLCresume.sty, sections/*.tex
resume_java/                 LaTeX sources — Java/Spring/Hibernate/J2EE track
interview_prep_java/         Interview prep for the Java resume (see its README)
output/
  resume.pdf                 compiled Python/Go resume (1 page)
  Tarun_Mittal_SSE_Java_5yr.pdf
  Tarun_Mittal_Resume_Overleaf.zip
  Tarun_Mittal_Resume_Java_Overleaf.zip
InterviewPrep.html           single-file study hub (Python/Go track)
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

# Java/Spring track
cd resume_java && tectonic resume.tex --outdir ../output
mv ../output/resume.pdf ../output/Tarun_Mittal_SSE_Java_5yr.pdf

# Study hub (Python/Go markdown → HTML)
python3 build_interview_prep.py
```

## Overleaf

Upload `output/Tarun_Mittal_Resume_Overleaf.zip` → New Project → Upload Project. Compiles with pdfLaTeX or XeLaTeX; main file `resume.tex`.

## Resume rules encoded here

- Google XYZ format: "Accomplished [X], as measured by [Y], by doing [Z]" on every bullet.
- Structure: company → project → bullets, with a **Tech Used** line per project.
- One page, ATS-safe (single column, standard headings, no images/tables in content).
- **Python/Go track:** stack reflects the July 2026 direction: Python (agents) · Go/Gin (non-agentic) · ClickHouse end-to-end. (Rust stays in prep, not on the resume.)
- **Java track (`resume_java/`):** same projects/metrics; primary stack Java · Spring Boot · Hibernate/JPA · Spring Security/Batch/WebFlux for non-agentic APIs; **AI/agentic tier stays Python** (FastAPI, LangGraph, LangChain, MCP); cloud + Kafka/Flink/Spark/Pinot/ClickHouse unchanged.
- `ats_scan.py` audits the compiled PDF against an ATS rubric; rerun after any edit.
