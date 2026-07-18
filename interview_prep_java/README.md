# Java / Spring track — README

Separate **Senior Software Engineer** resume and interview prep for **Java / Spring / Hibernate / J2EE** roles. Same companies, projects, and metrics as the main Python/Go track; tech stack swapped.

## Layout

```
resume_java/                 LaTeX sources (Overleaf-ready)
  resume.tex                 compile this
  sections/*.tex
output/
  Tarun_Mittal_SSE_Java_5yr.pdf
  Tarun_Mittal_Resume_Java_Overleaf.zip
interview_prep_java/
  00_index.md                hub + stack mapping table
  projects/01..05_*.md       per-project deep dives (Java telling)
  06_tech_deep_dives.md      Java, Spring, JPA, Security, Batch, Kafka, …
  07_behavioral_star_stories.md  pointers + Java wording swaps
  08_role_targeting_and_rapid_fire.md
```

Main (Python/Go) materials stay in `resume/` and `interview_prep/` — do not mix stacks in one interview loop.

## Rebuild PDF

```bash
cd resume_java && tectonic resume.tex --outdir ../output
mv ../output/resume.pdf ../output/Tarun_Mittal_SSE_Java_5yr.pdf
```

Or upload `output/Tarun_Mittal_Resume_Java_Overleaf.zip` to Overleaf (main file `resume.tex`).

## Stack on this resume

- **Languages lead:** Java  
- **Backend:** Spring Boot, Spring MVC/WebFlux, Spring Security, Spring Data JPA, Hibernate, Jakarta EE (J2EE), Spring Batch  
- **AI:** Spring AI, LangChain4j, MCP, RAG  
- **Unchanged:** Kafka, Flink, Spark, Pinot, ClickHouse, Postgres/MySQL/Redis, GCP/AWS, Docker/K8s, observability
