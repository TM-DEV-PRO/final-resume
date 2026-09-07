# Final PyGo + AI — README

Uber FRM / Masters framing: **FastAPI / SQLAlchemy 2.0** / **FastAPI**.
AssortSmart platform on every track PDF: **Go / Gin**. Agent plane: **Python / LangGraph**.
Contact block: (+91) 9079727197 · tmittaliet@gmail.com

## Layout

```
  resume.tex                 compile this
  sections/*.tex             objective · skills · experience · education
  artifacts/
    Tarun_Mittal_SSE_5yr.pdf
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
cp /tmp/rb/resume.pdf artifacts/Tarun_Mittal_SSE_5yr.pdf
```

Or upload the Overleaf zip (main file `resume.tex`).

## Rebuild the published HTML

```bash
python3 build_pages_html.py       # mirrors every .md → .html + site map
python3 build_interview_prep.py   # rebuilds each track's InterviewPrep.html
```

## Stack on this resume

- **Languages / Backend:** Python and Go · FastAPI / SQLAlchemy 2.0 · FastAPI · Gin · Django
- **Generative AI:** LangGraph, LangChain, RAG, Milvus, LLM agents, LangSmith, offline evaluation
- **Data & Streaming:** Kafka, Flink, ClickHouse, BigQuery, ETL
- **Cloud & DevOps:** GCP, AWS, Docker, Datadog, ELK, New Relic, CI/CD
- **Architecture & Core:** distributed systems, microservices, HLD/LLD, sharding, concurrency, idempotency
- **Streaming on the PDF:** Kafka and Flink on **Menu**. **No Spark, no Pinot.** No K8s-ops / Terraform ownership.
- MCP is **not** a PDF skill.

## Summary block on the PDF

1. Senior Software Engineer with **5 years** of experience designing and owning cloud-native, high-throughput **distributed systems**.
2. Expertise in **Python and Go** microservices, with applied experience in **AI-assisted** and **RAG** systems.
3. Proven track record shipping production systems, leading backend migrations, and improving reliability, performance, and scalability.
