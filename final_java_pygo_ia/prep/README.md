# Final Java + AI (IA = Py/Go) — README

The **primary public resume**. Uber and Masters India work is framed in Java / Spring; the Impact
Analytics AssortSmart work keeps its real stack — FastAPI and LangGraph for the agent plane, Go and
Gin for the shared write APIs. Contact block matches the Python/Go final track.

## Layout

```
final_java_pygo_ia/
  resume.tex                 compile this
  sections/*.tex             objective · skills · experience · education
  artifacts/
    Tarun_Mittal_SSE_Java_PyGoIA_Final.pdf        ← site download
    Tarun_Mittal_Java_PyGoIA_Overleaf.zip
  prep/                      grounded interview prep (this folder)
    00_index.md              hub + stack mapping table
    GROUND_TRUTH.md          every number, honesty tag, and omit list
    38_why_hire_tarun_qa.md  screening & behavioral Q&A bank
  campaign_extras/           behavioral bank · architecture · tech depth
  ats/ · linkedin/ · outreach/
  InterviewPrep.html         one-page hub (generated)
  ApplicationKit.html        paste-ready application answers
```

## Rebuild PDF

```bash
mkdir -p /tmp/rb && cd final_java_pygo_ia && tectonic resume.tex --outdir /tmp/rb
cp /tmp/rb/resume.pdf artifacts/Tarun_Mittal_SSE_Java_PyGoIA_Final.pdf
```

Or upload `artifacts/Tarun_Mittal_Java_PyGoIA_Overleaf.zip` to Overleaf (main file `resume.tex`).

## Rebuild the published HTML

```bash
python3 build_pages_html.py       # mirrors every .md → .html + site map
python3 build_interview_prep.py   # rebuilds each track's InterviewPrep.html
```

## Stack on this resume

- **Languages:** Java, Python, Go (Golang), SQL, C, C++
- **Backend & APIs:** Spring Boot, Spring MVC, Spring Security, Spring Data JPA, Hibernate, FastAPI,
  Gin, Django, REST, gRPC, Spring Batch — **Design Patterns removed** (Aug 2026), defend verbally
- **AI & Agents:** LLM agents, LangGraph, LangChain, MCP, tool calling, prompt engineering, RAG,
  embeddings, Milvus, pgvector, offline eval, LangSmith (agent plane is Python, not Spring AI)
- **Core Engineering:** Distributed Systems, System Design (HLD/LLD), Multithreading, Concurrency,
  Caching, Sharding, Reliability, Testing — **JUnit removed** from Skills (Aug 2026); JUnit still
  appears on the **Uber FRM experience Tech line**
- **Streaming on the PDF:** Kafka and Flink only. **No Spark, no Pinot, no SFT** — study-only depth.

## Summary block on the PDF

1. Senior Software Engineer with **5 years** of experience designing and owning cloud-native,
   high-throughput **distributed systems**.
2. Expertise in **Java, Python and Go microservices**, with applied experience in **AI-assisted and RAG systems**.
3. Proven track record shipping production systems, leading backend migrations, and improving
   reliability, performance, and scalability.
