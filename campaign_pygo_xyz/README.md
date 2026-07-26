# Campaign PyGo XYZ — Senior MNC Pack

Self-contained Python/Go XYZ resume + interview/outreach pack for Amazon, Google, Microsoft, LinkedIn, Apple, Netflix, Atlassian, Salesforce.

**Does not modify** `resume_v2/` or the Java track.

## Quick start
1. Resume PDF: [`output/Tarun_Mittal_SSE_PyGo_XYZ.pdf`](output/Tarun_Mittal_SSE_PyGo_XYZ.pdf)
2. Index of all docs: [`00_index.md`](00_index.md)
3. Facts: [`GROUND_TRUTH.md`](GROUND_TRUTH.md)
4. ATS scorecard: [`ats/00_ats_master_scorecard.md`](ats/00_ats_master_scorecard.md)

## Rules
- XYZ bullets (outcome + metric + method)
- No `:`, `;`, or em dashes in resume bullet text
- Every number tagged MEASURED / TARGET / HISTORICAL / ESTIMATED
- No invented IA TPS/RPM
- FRM 70% = targeting
- Menu PDF = Selenium + RAG/Gemini + ANZ only (Kafka on Masters)

## Compile
```bash
cd campaign_pygo_xyz/resume && tectonic resume.tex --outdir ../output
mv ../output/resume.pdf ../output/Tarun_Mittal_SSE_PyGo_XYZ.pdf
```
