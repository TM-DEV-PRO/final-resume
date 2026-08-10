# ATS cross-track benchmark — Aug 2026

Measured keyword hits on final PDFs + recruiter lane adjust. Cards: `final_pygo_ai/ats/` · `final_java_ai/ats/` · `final_java_pygo_ia/ats/`.

| Company | PyGo | Java (Spring IA) | Hybrid (Go IA) | Prefer |
|---|---:|---:|---:|---|
| Amazon SDE II | 92–96 | **96–100** | **96–100** | Java or Hybrid |
| Google SWE L4/L5 | **96–100** | 90–94 | 92–96 | **PyGo** |
| Microsoft Senior | **96–100** | 94–98 | 94–98 | **PyGo** / Hybrid ok |
| LinkedIn Systems | 90–94 | **98–100** | **98–100** | Java or Hybrid |
| Apple Backend | 88–94 | **96–100** | **96–100** | Java or Hybrid |
| Netflix L5 | **94–98** | 88–92 | 90–94 | **PyGo** |
| Atlassian Senior | 90–94 | **98–100** | **98–100** | Java or Hybrid |
| Salesforce SMTS | 94–98 | **96–100** | **96–100** | Java or Hybrid |
| Rubrik | 90–94 | 92–96 | 92–96 | Java / Hybrid |
| Databricks | 88–94 | 82–88 | 88–94 | **PyGo** / Hybrid |
| PlanetScale | 90–94 | 84–90 | 88–92 | **PyGo** (Go on IA helps Hybrid) |

**Panel avg (est.):** PyGo ~**94** · Java ~**93** · Hybrid ~**94**

**Hybrid =** `final_java_pygo_ia`: Java/Spring Uber·Masters + AssortSmart IA = FastAPI/LangGraph/MCP + **Go Gin** (same IA as PyGo).

### Shared evidence (all finals)
- Menu: owned E2E Selenium→Kafka→Flink · RAG/Gemini/Milvus schema gate · 95%+ scrape
- ANZ Mobility local-authority compliance line present
- Spark **not** on PDF (Databricks miss is intentional/honest)

### Only material keyword miss
| Token | PyGo | Java | Hybrid | Impact |
|---|---|---|---|---|
| Spark | miss | miss | miss | Databricks −6 to −10 |
| Java (token) | miss | hit | hit | Salesforce JVM posts favor Java/Hybrid |
| Go / Gin on IA | hit | miss | hit | PlanetScale / Netflix lean PyGo or Hybrid |
