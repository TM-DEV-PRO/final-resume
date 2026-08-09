# Java / Spring track — README

Separate **Senior Software Engineer** resume and interview prep for **Java / Spring / Hibernate** roles. Same companies, projects, and metrics as the main Python/Go track; non-agentic APIs framed in Spring where defensible; AI/RAG and Menu streaming stay Python.

## Layout

```
resume_java/                 LaTeX sources (Overleaf-ready)
  resume.tex                 compile this
  sections/*.tex
output/
  Tarun_Mittal_SSE_Java_5yr.pdf
  Tarun_Mittal_Resume_Java_Overleaf.zip
resume_java/prep/
  00_index.md                hub + stack mapping table
  projects/01..05_*.md       per-project deep dives (Java telling)
  06_tech_deep_dives.md      Java, Spring, JPA, Security, Batch, Kafka, …
  07_behavioral_star_stories.md  pointers + Java wording swaps
  08_role_targeting_and_rapid_fire.md
```

Main (Python/Go) materials stay in `resume/` (legacy) and `resume_v2/` — do not mix stacks in one interview loop.

## Rebuild PDF

```bash
cd resume_java && tectonic resume.tex --outdir ../output
mv ../output/resume.pdf ../output/Tarun_Mittal_SSE_Java_5yr.pdf
```

Or upload `output/Tarun_Mittal_Resume_Java_Overleaf.zip` to Overleaf (main file `resume.tex`).

## Stack on this resume

- **Languages lead:** Java  
- **Backend:** Spring Boot, Spring MVC, Spring Security, Spring Data JPA, Hibernate, Spring Batch  
- **AI:** LangGraph, LangChain, MCP, tool calling, prompt engineering, RAG, embeddings, Milvus, pgvector, offline eval, LangSmith (agent plane Python; not Spring AI) — see `prep/36_skills_ai_agents_defense.md`  
- **Unchanged streaming:** Kafka, Flink, Spark, Pinot (Menu tech line stays Python + streaming — no Spring claim)  
- **Data/cloud:** ClickHouse, Postgres/MySQL/Redis, GCP/AWS, Docker/K8s, observability
