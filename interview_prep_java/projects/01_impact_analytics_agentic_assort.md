# Impact Analytics — Agentic AssortSmart (Java / Spring track)

**Role:** Senior Software Engineer · 14 May 2026 – Present · Bangalore  
**Resume tech:** Java · Spring Boot · Python (FastAPI, LangGraph, MCP) · ClickHouse · BigQuery · GCS · Datadog · LangSmith · PostHog · Docker  

> Same facts as `interview_prep_v2/10_impact_analytics_deep_dive.md` and `GROUND_TRUTH.md`. This file is the **Java/Spring telling**. Agentic / AI tier stays **Python**.

---

## 1. Elevator pitch (30 seconds)

"I work on AssortSmart's agentic rebuild. FastAPI owns chat (LangGraph/MCP); Spring Boot is the doing layer for Hindsight, Clustering, and Strategy — manual REST and agent tools hit the same APIs against **ClickHouse/GCS**. We instrumented Datadog, LangSmith, and PostHog under a shared OTEL trace id. Planning data is **ClickHouse end-to-end** via insert-only versioned writes — unlocked after POCs showed classic OLTP mutations are the wrong CH model. Evidence: on a **250M-row** pivot harness CH cut heavy grids from **189s to 12.3s** (~**15×** on DISTINCT grids; typical aggregates ~**2–3×**), and line-planning avoided materializing **~12B** store-week rows via a **~25M** aggregate (**100–450×**). Copilot targets under **1 hour** and under **2%** failures from measured **8.5%**; Phase 1 design PASS, load test pending."

## 2. Service split (say it exactly)

"Path A: FE → FastAPI `POST /chat` → LLM → tools → **Spring Boot doing layer** → CH/GCS. Path M: FE → Spring REST → **same** doing modules — no LLM. FastAPI owns chat because agent loops are LLM-latency-shaped. Spring owns doing because Path M is throughput I/O. Agent never bypasses Spring for mutations; probe DB profiles stay read-only."

## 3. Spring Boot doing layer — defend the resume bullet

Resume: *Designing Java (Spring Boot) microservices for manual REST and agent tool paths (Hindsight, Clustering, Strategy) with JWT auth, plus Datadog, LangSmith, and PostHog under a shared OTEL trace id.*

- **Hindsight / Clustering / Strategy** — `@RestController` + `@Service` modules shared by Path M and Path A tool calls.
- **JWT** — Spring Security resource server; tenant + role claims.
- **Bulk / tool I/O** — bounded `ExecutorService` / virtual threads for fan-out; request deadlines on CH clients; idempotency via batch id + content hash; versioned batch INSERT into ClickHouse.
- **Obs** — OTEL `trace_id` into Datadog (L2 platform). Claim **instrumentation design**, not sole SaaS ownership. LangSmith stays on the Python agent tier (L1); PostHog on product/FE.

## 4. Agentic microservice (Python — unchanged ownership)

Same FRD targets: 20–100 configs vs 1; under 1h (TARGET); 8.5% → under 2% (MEASURED/TARGET); 100% reproducible (TARGET); p95 probes under 500ms vs BQ 1–20s (MEASURED/TARGET).

## 5. ClickHouse end-to-end + POC numbers

| Claim | Tag | Defense |
|---|---|---|
| ClickHouse/GCS planning store (insert-only versions) | MEASURED design | HLD + Jul 2026 stack direction |
| 250M pivot **189s → 12.3s** (~15×) | MEASURED | DISTINCT/option-count cliff; typical ~2–3× if stripped |
| Avoided **12B** flat (**100–450×**) | MEASURED / projected 12B | Aggregate ~25M; explode ~25 ms |
| Hardware | MEASURED | PG 48 GB host vs CH 10 CPU / 3.3 GB VM |
| POC hybrid / PG cell &lt;1ms | MEASURED prep | Decision history — why insert-only unlock, not resume headline |
| Legacy mtp-assort no wholesale CH | MEASURED | Fix BigQuery first |
| Order Batching 60× | MEASURED prep | Offer if asked |

**Interview close:** "POCs said hybrid for legacy keyed UPDATE. Agentic AssortSmart changed the write model — planning facts are ClickHouse end-to-end."

## 6. Stack evolution (correct order)

1. Live audit: no wholesale CH for legacy in-place UPDATEs — correct for that write model.
2. Pivot + line-plan POCs → CH wins large reads; schema flat→agg is the bigger lever; hybrid for classic OLTP.
3. Insert-only / versioned write PoC → `mutations_used = 0`.
4. Jul 2026: agentic-assort commits ClickHouse end-to-end for planning data; HLD shows doing layer → ClickHouse/GCS.

## 7. Q&A (Java-flavored)

- **"Hibernate on ClickHouse?"** No — clickhouse-java / JDBC. JPA only if a thin metadata plane stays on Postgres.
- **"Why not Spring AI for agents?"** LangGraph/MCP stay Python on this resume; Java owns Spring doing-layer APIs.
- **"Virtual threads?"** Prefer for blocking I/O fan-out on Java 21+; bound pools by CH connection budget.
- **"What shipped vs POC?"** CH planning-store direction = MEASURED design (HLD/stack). Pivot/line-plan numbers = MEASURED harness. Copilot = Phase 1 design PASS, load test pending.
