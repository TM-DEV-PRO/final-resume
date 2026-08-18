# LinkedIn Profile Pack (stand out)

Aligned to **Final Java + AI (IA = Py/Go)** resume. Paste-ready. Avoid colon-heavy AI voice in About where possible.

## Headline (pick one)
1. Senior Software Engineer | Java · Python · Go | Distributed Systems · Kafka · AI-assisted systems
2. Backend SSE (Java, Python and Go) | Owned Uber (via EPAM) FRM design · Kafka 1M+/day · LangGraph + ClickHouse
3. Senior Software Engineer building AI-assisted planning systems | LangGraph · ClickHouse · Kafka

**Recommended:** #2 (metric-led for recruiter search)

## About — short
Senior Software Engineer with 5 years of experience designing and owning cloud-native, high-throughput distributed systems. Expertise in Java, Python and Go microservices, with applied experience in AI-assisted and RAG systems. Proven track record shipping production systems, leading backend migrations, and improving reliability, performance, and scalability.

## About — long
I am a Senior Software Engineer focused on backend and data platforms in Java, Python, and Go.

What I am known for:
- Architecture ownership Uber (via EPAM) FRM Risk Scoping backend — 30+ APIs powering 8 screens at $340M materiality; recon v2 + materiality engine; led 3 engineers.
- Scale Masters India Kafka + PostgreSQL e-invoicing at 1M+ IRP/day lifting throughput from 700 to 4000 requests/min. Mentored 2 engineers. On-call with ELK and New Relic.
- Product impact owned Uber Eats menu ingestion end to end (Selenium/Kafka/Flink + RAG/Gemini/Milvus) — from 24 hours to 2 hours, $600K+/yr, 30K+ menus/month, 95%+ ingest success, 98%/100% offline eval.
- AI-assisted planning at Impact Analytics: AssortSmart Keep/Drop engine and dig-deeper QnA (FastAPI, LangGraph, MCP) with Go, Gin write plane and a measured ClickHouse 250M pivot POC (from 189s to 12.3s, about 15.5x).

I care about honest metrics (measured vs target) clear design tradeoffs and mentoring people to ship safely.

Open to Senior Software Engineer / SDE2+ backend platform and AI-assisted systems roles.

## Experience blurbs

### Impact Analytics — Senior Software Engineer (May 2026 – Present)
Building AssortSmart so retailers decide what to buy, how much, and which stores for a season ahead. PDF project title: **AssortSmart (Retail Merchandise Planning Platform)**. Architected AssortSmart's Keep/Drop engine at article × plan-season grain — deterministic ST%/ROS scoring plus LangGraph lenses, agents SELECT-only on ClickHouse via CSV-first bake-and-promote, promotions gated on 300 gold cases and ≥80% offline accuracy (promotion gate / design — do not claim shipped to all tenants). Built a read-only dig-deeper QnA agent over locked Keep/Drop decisions so planners can understand why styles were kept or dropped while schema constraints preserve frozen decisions and block writes to ClickHouse, CSVs, and outcomes. Drove adoption of ClickHouse as AssortSmart's planning analytics engine, reducing pivot latency from 189s to 12.3s (about 15.5x) on 250M rows through a row-identical Postgres-versus-ClickHouse POC. Stack on this PDF: Go, Gin, Python, FastAPI, LangGraph, MCP, ClickHouse, BigQuery, GCS, Datadog, LangSmith, PostHog, GCP, Docker.

**Verbal only / not on PDF (building):** Cluster Recommendation Copilot and Hindsight remain deep-dive context if asked — not resume headline bullets.

### Uber via EPAM — SDE2 (Jul 2024 – May 2026)
**FRM:** Owned FRM Risk Scoping backend (Spring Boot, MySQL) — 30+ REST APIs powering 8 screens at $340M materiality, targeting 70% recon cut from about 2 weeks to 3–4 days. Owned Sheets→MySQL recon v2 (18 files, L1→L2→L3 /v2 APIs, HFM vs 10-Q). Automated in-scope decisions ~55×14 with materiality/residual/5% logic. Led 3 engineers on the FRM backend by owning API contracts and layered design reviews for Finance's quarterly scoping.

**Menu (Uber Eats):** Owned end-to-end menu ingestion on GCP (Selenium → Kafka → Flink keyed normalize/dedupe) — onboarding from 24 hours to 2 hours, $600K+/yr at 30K+ menus/month. Owned LangChain RAG + Gemini 2.5 Pro over Milvus for multilingual PDF/image → Uber Eats catalog schema (98%/100% offline) with a hard schema gate before upsert. Raised successful ingestions to 95%+ via IP rotation, dynamic proxy pools, and adaptive retries.
**ANZ (Uber Mobility):** Automated Uber Mobility driver/vehicle document checks for ANZ against local authority requirements to 99.9%, removing ~20h/week manual verification (HISTORICAL).

### Masters India — SDE2 (Dec 2022 – Jun 2024)
Cut p95 from 1.2s to 300ms for 1500+ clients by migrating Laravel to Spring Boot microservices; mentored 2. Lifted from 700 to 4000 req/min and 1M+ IRP/day on Kafka + PostgreSQL split by tax quarter. Idempotency keys, retries, DLQ + Redis −30% reads. ELK/New Relic + usage dashboard cut triage 70% and support tickets 35%; coverage from 35 to 82% at 98% deploy.

### GeeksforGeeks — SDE (Aug 2021 – Nov 2022)
Stabilized doubt-support for 10K+ daily queries and 10× contest spikes via PHP to Django. Voting/pinning/locking APIs lifted premium 15–20%. Influencer earnings dashboard raised course sales 30%. Separate cron pipelines for video/reminders/cleanup raised ops efficiency 70%.

## Featured section
- Resume PDF (Java FRM + Py/Go IA)
- LangChain Academy cert
- HackerRank Problem Solving cert
- Optional: GitHub TM-DEV-PRO

## Skills order (LinkedIn)
Java · Spring Boot · Hibernate · Python · Go · Gin · FastAPI · Distributed Systems · Microservices · Kafka · ClickHouse · System Design · Docker · AWS · GCP · PostgreSQL · MySQL · Redis · LangGraph · RAG · Mentorship
