# Python/Go resume v2 — Interview Prep Hub (hardened)

**Tarun Mittal · Senior Software Engineer · July 2026**

This hub backs `resume_v2/` (PDF: `Tarun_Mittal_SSE_5yr_v2.pdf`). The original `resume/` + `interview_prep/` are **unchanged** — use this track when you want the credibility-hardened Python/Go resume.

## What changed vs the original resume

| Area | Original | v2 (this track) |
|---|---|---|
| IA turnaround claim | “cutting … under 1 hour” | “**targeting** … under 1 hour” (FRD design target) |
| ClickHouse writes | “lock free writes” | “concurrent writes **without lock contention**” |
| Languages | + Rust, C, C++ | Python, Go, Java, SQL only |
| Backend skills | + gRPC | Dropped gRPC (not on any Tech Used line) |
| AI skills | + ChromaDB, semantic caching | Kept LangGraph/LangChain/MCP/RAG/text-to-SQL/pgvector |
| Streaming/data | + DuckDB | Dropped DuckDB (ClickHouse end-to-end direction) |
| Databases | + MongoDB, Cassandra, Elasticsearch | Postgres, MySQL, Redis, S3 only |
| BigQuery | In skills | **Kept** — defend as upstream SoT you ingest from, not “I optimize BigQuery” |

## Study path

Deep project defense is still in the original materials (do not duplicate):

1. `../interview_prep/projects/01..05_*.md`
2. `../interview_prep/06_tech_deep_dives.md`
3. `../interview_prep/07_behavioral_star_stories.md`
4. `../interview_prep/agentic_assort_playbook/` (§0–§10)

Plus this folder’s rapid-fire for v2 wording.

<div class="callout warn">
<b>Honesty guardrail (same as original).</b> Know REAL vs offline-eval vs design targets. BigQuery = upstream source of truth you ingest from — never claim BigQuery optimization work as yours. Rust stays off the resume; if asked, “Go by default, Rust by measurement / escape hatch — not a shipped claim on this PDF.”
</div>

## Resume at a glance (v2)

Same companies, projects, and metrics as the original — only skills trim + two IA phrasing hardenings above.
