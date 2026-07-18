# Java Track — Interview Prep Hub

**Tarun Mittal · Senior Software Engineer (Java / Spring) · July 2026**

This hub backs every line of `resume_java/resume.tex` (PDF: `output/Tarun_Mittal_SSE_Java_5yr.pdf`). It is a **separate track** from the Python/Go prep in `interview_prep/` — same projects, metrics, and companies; **tech stack reframed to Java / Spring / Hibernate / J2EE**.

Study order:

1. **Project deep dives** — one chapter per resume project (Impact → Uber FRM → Uber Menu → Masters India → GFG).
2. **Tech deep dives** — Java, Spring Boot, Hibernate/JPA, Spring Security, Spring Batch/WebFlux, Kafka/Flink/Spark/Pinot, cloud.
3. **Behavioral bank** — same STAR stories as the main track (outcomes don't change); stack references swapped to Java where needed.
4. **Role targeting** — Java/Spring senior SWE listings and rapid-fire defense.

<div class="callout warn">
<b>Honesty guardrail.</b> Same as the main track: know which numbers are <b>REAL</b> (measured), <b>offline-eval</b>, or <b>design targets</b>. Say "measured," "in an offline evaluation," or "our design target" accordingly. BigQuery is the <b>upstream source of truth we ingest from</b> — never claim BigQuery optimization work as yours. This Java resume is a <b>positioning variant</b> for Java/Spring roles; defend the architecture and outcomes, and be ready to map Spring/JPA patterns to the same systems you built.
</div>

## Stack mapping (Python/Go resume → this Java resume)

| Original | Java track |
|---|---|
| Gin / non-agentic FastAPI | Spring Boot (MVC) |
| SQLAlchemy / Pydantic | Hibernate / Spring Data JPA + Bean Validation / Jackson |
| Django | Spring Boot + Spring MVC |
| Celery | Spring Batch + `@Async` / Redis-backed workers |
| pytest | JUnit 5 + Mockito + Testcontainers |
| **LangGraph / FastAPI agents** | **Unchanged — Python (FastAPI, LangGraph, LangChain, MCP)** |
| Menu ingestion (Kafka/Flink/Spark/Pinot + RAG) | **Unchanged — Python + streaming stack** (no Spring claim) |
| Goroutine pools / channels | `ExecutorService` + bounded queues / virtual threads |
| JWT middleware | Spring Security (JWT resource server) |

## The resume at a glance

| Company | Project | Lead metric |
|---|---|---|
| Impact Analytics (Jun 2026–) | Agentic AssortSmart | Python agentic microservice (FastAPI, LangGraph): ~100 silhouette-scored clusterings → top 3, days → <1 h · Spring Boot (Java) core: worker pools, timeouts, Spring Security JWT · ClickHouse append-only never-erase store |
| Uber via EPAM (Jul 2024–May 2026) | FRM Scoping Platform | 70% cycle-time cut · 36 endpoints/8 screens · 19M rows/quarter · JPA/Hibernate |
| Uber via EPAM | Menu Ingestion Platform | 30K+ menus/mo · 24 h→2 h · $600K+/yr · Kafka/Flink/Spark/Pinot |
| Masters India (Dec 2022–Jun 2024) | GST e-invoicing SaaS | p95 1.2s→300ms · 1M+ txn/day · Spring Boot + Spring Batch |
| GeeksforGeeks (Aug 2021–Nov 2022) | Backend | 100K+ daily queries · +15–20% subscriptions · Spring Boot |
