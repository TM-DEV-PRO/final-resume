# ATS cross-track benchmark — Aug 2026

Measured keyword hits on both final PDFs (pdfminer, space-tolerant) + recruiter lane adjust. Full cards: `final_pygo_ai/ats/00_ats_11_company_scorecard.md` · `final_java_ai/ats/00_ats_11_company_scorecard.md`.

| Company | PyGo fit | PyGo | Java fit | Java | Submit |
|---|---|---:|---|---:|---|
| Amazon SDE II | Strong | 92–96 | **BEST** | 96–100 | **Java** |
| Google SWE L4/L5 | **BEST** | 96–100 | Strong | 90–94 | **PyGo** |
| Microsoft Senior | **BEST** | 96–100 | Strong | 94–98 | **PyGo** |
| LinkedIn Systems | Strong | 90–94 | **BEST** | 98–100 | **Java** |
| Apple Backend | Strong | 88–94 | **BEST** | 96–100 | **Java** |
| Netflix L5 | **BEST** | 94–98 | Borderline | 88–92 | **PyGo** |
| Atlassian Senior | Strong | 90–94 | **BEST** | 98–100 | **Java** |
| Salesforce SMTS | Strong | 94–98 | **BEST** | 96–100 | **Java** (JVM) / either |
| Rubrik | Strong | 90–94 | Strong | 92–96 | **Java** slight edge |
| Databricks | Strong | 88–94 | Borderline | 82–88 | **PyGo** (still no Spark) |
| PlanetScale | Strong | 90–94 | Borderline | 84–90 | **PyGo** |

**Panel avg (est.):** PyGo ~**94** · Java ~**93**

### Shared evidence (both PDFs)
- Keyword bank coverage **37/37** (track-specific banks)
- Menu: owned E2E Selenium→Kafka→Flink · RAG/Gemini/Milvus schema gate · 95%+ scrape
- ANZ Mobility local-authority compliance line present
- Spark **not** on PDF (Databricks miss is intentional/honest)

### Only material keyword miss
| Token | PyGo | Java | Impact |
|---|---|---|---|
| Spark | miss | miss | Databricks −6 to −10 recruiter points |
| Java (token) | miss | hit | Salesforce JVM-preferring posts favor Java PDF |
