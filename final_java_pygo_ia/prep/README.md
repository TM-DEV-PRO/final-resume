# Final Java + AI (IA = Py/Go) — README

Uber FRM / Masters framing: **Spring Boot / Spring Data JPA / Hibernate** / **Spring Boot**.
AssortSmart platform on every track PDF: **Go / Gin**. Agent plane: **Python / LangGraph**.
Contact block: (+91) 9079727197 · tmittaliet@gmail.com

## Layout

```
  resume.tex                 compile this
  sections/*.tex             objective · skills · experience · education
  artifacts/
    Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf
  prep/                      grounded interview prep (this folder)
    00_index.md              hub + stack mapping
    GROUND_TRUTH.md          every PDF number, honesty tag, omit list
    38_why_hire_tarun_qa.md  screening & behavioral Q&A
  campaign_extras/           behavioral bank · architecture · tech depth
  ats/ · linkedin/ · outreach/
```

## Rebuild PDF

```bash
# from this track directory
mkdir -p /tmp/rb
tectonic resume.tex --outdir /tmp/rb
cp /tmp/rb/resume.pdf artifacts/Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf
```

Or upload the Overleaf zip (main file `resume.tex`).

## Rebuild the published HTML

```bash
python3 build_pages_html.py       # mirrors every .md → .html + site map
python3 build_interview_prep.py   # rebuilds each track's InterviewPrep.html
```

## Stack on this resume

- **Languages / Backend:** Java, Python and Go · Spring Boot / Spring Data JPA / Hibernate · FastAPI · Gin · Django
- **AI & Applied ML:** LangGraph, LangChain, RAG, Milvus, LLM agents, LangSmith, offline evaluation
- **Data & Streaming:** Kafka, Flink, ClickHouse, BigQuery, ETL
- **Cloud & DevOps:** GCP, AWS, Docker, Datadog, ELK, New Relic, CI/CD
- **Architecture & Core:** distributed systems, microservices, HLD/LLD, sharding, concurrency, idempotency
- **Streaming on the PDF:** Kafka and Flink on **Menu**. **No Spark, no Pinot.** No K8s-ops / Terraform ownership.
- MCP is **not** a PDF skill.

## Summary block on the PDF

1. Senior Software Engineer with **5 years** architecting high-throughput, cloud-native **distributed systems** and leading zero-downtime monolithic migrations.
2. Expert in **Java, Python and Go microservices** — event-driven pipelines, multi-billion-row databases, extreme latency reductions.
3. LangGraph multi-agent systems, Milvus RAG architectures, and deterministic evaluation harnesses.\n