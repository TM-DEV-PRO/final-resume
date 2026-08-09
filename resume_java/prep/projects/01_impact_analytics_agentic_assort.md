# Impact Analytics — Agentic AssortSmart (Java / Spring track)

**Role:** Senior Software Engineer · 14 May 2026 – Present · Bangalore  
**Resume tech:** Java · Spring Boot · Python (FastAPI, LangGraph, MCP) · ClickHouse · BigQuery · GCS · Datadog · LangSmith · PostHog · Docker  

> Same facts as `../../resume_v2/prep/10_impact_analytics_deep_dive.md` and `GROUND_TRUTH.md`. This file is the **Java/Spring telling**. Agentic / AI tier stays **Python**.

---

## 1. Elevator pitch (30 seconds)

"Four stories on AssortSmart. Copilot cuts clustering from days toward under one hour and from one to 20–100 configs — Python LangGraph owns chat, Spring Boot is the doing layer. Safety moves failures from a measured 8.5% toward under 2% with read-only tools and three human gates. The same Spring Hindsight/Clustering/Strategy APIs serve agents and manual screens, with Datadog, LangSmith, and PostHog on one OTEL trace. Pivot hybrid cuts 250M Hindsight grids from 189s to 12.3s on ClickHouse reads while Postgres keeps cell edits; line-plan avoided 12B store-week rows via a ~25M aggregate; agentic planning store is ClickHouse insert-only. Phase 1 design PASS, load test pending."

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
| 250M Hindsight pivot **189s → 12.3s** (~15×) via CH reads + PG cell edits | MEASURED | `pivot-poc/`; ~15.5× with option-count; typical ~2–3×; PG write ~14× tuned |
| Avoided **12B** flat (**100–450×**) | MEASURED / projected 12B | Aggregate ~25M; explode ~25 ms |
| Hardware | MEASURED | PG 48 GB host vs CH 10 CPU / 3.3 GB VM |
| Hybrid decision rule (aggregate→CH, cell edit→PG) | MEASURED | Same rule as line-plan POC; agentic store still insert-only CH |
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
