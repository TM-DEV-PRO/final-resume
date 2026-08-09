# Final Resume — Tarun Mittal (Senior Software Engineer)

Each resume flavour is **self-contained**: LaTeX · PDF · Overleaf zip · prep · hub.

| Track | Folder | PDF | Prep hub |
|---|---|---|---|
| **Python / Go v2** (primary) | [`resume_v2/`](resume_v2/) | `artifacts/Tarun_Mittal_SSE_5yr_v2.pdf` | `InterviewPrep.html` |
| **Java / Spring** | [`resume_java/`](resume_java/) | `artifacts/Tarun_Mittal_SSE_Java_5yr.pdf` | `InterviewPrep.html` |
| **Campaign PyGo XYZ** | [`campaign_pygo_xyz/`](campaign_pygo_xyz/) | `output/Tarun_Mittal_SSE_PyGo_XYZ.pdf` | `InterviewPrep.html` |
| Legacy Python / Go | [`resume/`](resume/) | `artifacts/Tarun_Mittal_SSE_5yr.pdf` | `InterviewPrep.html` |

Repo hub (GitHub Pages): [`index.html`](index.html) → https://tm-dev-pro.github.io/final-resume/

## Layout (per track)

```
resume_v2/
  resume.tex, sections/, TLCresume.sty   # LaTeX sources
  artifacts/*.pdf, *_Overleaf.zip        # ship artifacts
  prep/                                  # markdown + HTML mirrors
  InterviewPrep.html                     # one-page study hub
  ApplicationKit.html                    # LinkedIn / intros / answers
  index.html                             # track landing
```

Java hub **reads** shared grounded packs from `resume_v2/prep/` at build time (no duplicated markdown).

## Rebuild

```bash
# PDF (needs tectonic) — example for v2
cd resume_v2 && tectonic resume.tex
# then copy resume.pdf → artifacts/Tarun_Mittal_SSE_5yr_v2.pdf

# All HTML hubs + mirrors
python3 build_interview_prep.py
```

