# Final Python + Go + AI — README

AI / data-leaning submit track for Google · Microsoft · Netflix · Databricks · PlanetScale. Every
project keeps its real stack: FastAPI and LangGraph for the AssortSmart agent plane, Go and Gin for
the shared write APIs, FastAPI and MySQL for Uber FRM.

## Layout

```
final_pygo_ai/
  resume.tex                 compile this
  sections/*.tex             objective · skills · experience · education
  artifacts/
    Tarun_Mittal_SSE_PyGo_AI_Final.pdf
    Tarun_Mittal_PyGo_AI_Overleaf.zip
  prep/                      grounded interview prep (this folder)
    00_index.md              hub + stack mapping table
    GROUND_TRUTH.md          every number, honesty tag, and omit list
    38_why_hire_tarun_qa.md  screening & behavioral Q&A bank
  campaign_extras/           behavioral bank · architecture · tech depth · ATS loops
  ats/ · linkedin/ · outreach/
  InterviewPrep.html         one-page hub (generated)
  ApplicationKit.html        paste-ready application answers (hand-maintained)
```

Do not mix tracks inside one interview loop — if you sent this PDF, Uber FRM is FastAPI, not Spring.

## Rebuild PDF

```bash
mkdir -p /tmp/rb && cd final_pygo_ai && tectonic resume.tex --outdir /tmp/rb
cp /tmp/rb/resume.pdf artifacts/Tarun_Mittal_SSE_PyGo_AI_Final.pdf
```

Or upload `artifacts/Tarun_Mittal_PyGo_AI_Overleaf.zip` to Overleaf (main file `resume.tex`).

## Rebuild the published HTML

```bash
python3 build_pages_html.py       # mirrors every .md → .html + site map
python3 build_interview_prep.py   # rebuilds each track's InterviewPrep.html
```

## Credibility rules carried over from the source track

1. Skills list only technologies evidenced on a Tech line or the live stack.
2. AssortSmart "under 1 hour" and "under 2%" are **TARGET**, not measured.
3. No "lock-free writes" — say concurrent writes **without lock contention**.
4. BigQuery stays, with the ingest source-of-truth talking track in prep.
5. **Design Patterns and JUnit are not in Skills** (trimmed Aug 2026).
6. **No Spark, no Pinot, no SFT** on the PDF — study-only depth.

## Summary block on the PDF

1. Senior Software Engineer with **5 years** of experience designing and owning cloud-native,
   high-throughput **distributed systems**.
2. Expertise in **Python and Go microservices**, with applied experience in **AI-assisted and RAG systems**.
3. Proven track record shipping production systems, leading backend migrations, and improving
   reliability, performance, and scalability.
