# Ground Truth (Java track)

Same facts as [`../../resume_v2/prep/GROUND_TRUTH.md`](../../resume_v2/prep/GROUND_TRUTH.md).

**PDF IA bullets (Aug 2026):** same four as v2. Cluster Recommendation ownership line uses **Python, LangGraph, MCP** chat plane and **Spring Boot** write APIs (v2/xyz use Go, Gin).

Stack framing only:
- FRM and Masters and GFG APIs: Spring Boot / Hibernate / Spring Batch (positioning variant)
- Menu scraping and AI extraction: **Python unchanged**
- IA agentic and ClickHouse work: **Python agent plane unchanged**; write APIs framed as Spring Boot on this track; ClickHouse is not accessed via Hibernate
- Never claim shipped Java services in production at IA; say building / design ownership.

Evidence boundary (same as v2 `GROUND_TRUTH.md` evidence matrix):
- Resume-safe: FRM ownership + layered architecture, Masters strangler + Kafka scale + idempotency/DLQ + ELK/New Relic on-call alerting (experience), Design Patterns in Skills. **Core omits** Fault Tolerance / HA / On-call skill keywords (use Multithreading + Concurrency).
- Menu has Kafka + Flink (keyed normalize/dedupe/replay) on PDF. Omit Spark, multi-region, K8s ops, Terraform from resume; study in `../../resume_v2/prep/17_senior_systems_study_only.md`.
- CGPA removed from Java resume PDF (kept in shared ground truth for reference).

Deep dives to study (shared with v2):
- `../../resume_v2/prep/10_impact_analytics_deep_dive.md`
- `../../resume_v2/prep/11_uber_frm_deep_dive.md` (map FastAPI layers to Spring controller/service/repository)
- `../../resume_v2/prep/12_masters_gfg_deep_dive.md` (map FastAPI to Spring Boot, Celery to Spring Batch)
- `../../resume_v2/prep/13_behavioral_why_switch.md`
- `../../resume_v2/prep/14_uber_menu_deep_dive.md`
- `../../resume_v2/prep/17_senior_systems_study_only.md`
- `../../resume_v2/prep/23a_ia_interview_pack.md` (PDF bullet defense Aug 2026)

Verified certificates: **HackerRank Problem Solving** and **LangChain Academy** (source: `KNOWLEDGE-MATERIAL/certificates.txt`).
