# Ground Truth (Final Java + PyGo IA hybrid)

Same facts as [`../../resume_v2/prep/GROUND_TRUTH.md`](../../resume_v2/prep/GROUND_TRUTH.md).

**PDF IA bullets (Aug 2026):** same four as PyGo final. Cluster Recommendation ownership line uses **FastAPI, LangGraph, MCP** chat plane and **Go Gin** write APIs (not Spring Boot on IA). Uber FRM / Masters stay Spring Boot.

Stack framing:
- FRM and Masters APIs: Spring Boot / Hibernate / Spring Batch. **GFG stays PHP → Django (Python)** on this PDF.
- Menu scraping and AI extraction: **Python unchanged**
- IA agentic and ClickHouse work: **Python + Go** (FastAPI/LangGraph/MCP + Gin); ClickHouse is not accessed via Hibernate
- Never claim shipped IA services in production; say building / design ownership.
- Never say Spring Boot write APIs for AssortSmart on this track — that is `final_java_ai` only.

Evidence boundary (same as v2 `GROUND_TRUTH.md` evidence matrix):
- Resume-safe: FRM ownership + layered architecture, Masters strangler + Kafka scale + idempotency/DLQ + ELK/New Relic on-call alerting (experience). **Skills omit** Design Patterns / JUnit (use Testing + Multithreading + Concurrency). **Core omits** Fault Tolerance / HA / On-call skill keywords.
- Menu has Kafka + Flink (keyed normalize/dedupe/replay) on PDF. Omit Spark, multi-region, K8s ops, Terraform from resume; study in `../../resume_v2/prep/17_senior_systems_study_only.md`.
- Contact on this track: `tm.eng2021@gmail.com` / `(+91) 9001542418` (same as PyGo final).

Deep dives:
- `10_impact_analytics_deep_dive.md` · `23a_ia_interview_pack.md` (IA = Go Gin like PyGo)
- `11_uber_frm_deep_dive.md` (Spring controller/service/repository)
- `12_masters_gfg_deep_dive.md` · `14_uber_menu_deep_dive.md`
- `37_senior_screen_deep_qa.md`

Verified certificates: **HackerRank Problem Solving** and **LangChain Academy** (source: `KNOWLEDGE-MATERIAL/certificates.txt`).
