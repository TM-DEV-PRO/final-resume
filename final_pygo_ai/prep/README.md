# Python/Go resume v2 (hardened)

Credibility-hardened copy of the main Python/Go resume. **Does not modify** `resume/` or `interview_prep/`.

## Layout

```
resume_v2/                 LaTeX sources
resume_v2/prep/         Delta prep (index + skills rationale + rapid-fire)
output/
  Tarun_Mittal_SSE_5yr_v2.pdf
  Tarun_Mittal_Resume_v2_Overleaf.zip
Tarun_Mittal_SSE_5yr_v2.pdf
InterviewPrepV2.html
```

## Fixes applied

1. Skills trimmed to technologies evidenced on Tech Used lines / live stack
2. IA “under 1 hour” → **targeting** (design target)
3. “lock free writes” → concurrent writes **without lock contention**
4. BigQuery kept with explicit ingest-SoT talking track in prep

## Rebuild

```bash
cd resume_v2 && tectonic resume.tex --outdir ../output
mv ../output/resume.pdf ../output/Tarun_Mittal_SSE_5yr_v2.pdf
cp ../output/Tarun_Mittal_SSE_5yr_v2.pdf ../
```

Deep project chapters remain in `interview_prep/` — this folder only documents v2 deltas.
