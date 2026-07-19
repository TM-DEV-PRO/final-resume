# Ground Truth (Java track)

Same facts as [`../interview_prep_v2/GROUND_TRUTH.md`](../interview_prep_v2/GROUND_TRUTH.md).

Stack framing only:
- FRM and Masters and GFG APIs: Spring Boot / Hibernate / Spring Batch (positioning variant)
- Menu scraping and AI extraction: **Python unchanged**
- IA agentic and ClickHouse work: **Python unchanged**; ClickHouse is not accessed via Hibernate
- IA services tier bullet ("Designing Java (Spring Boot) microservices for plan lifecycle and bulk save REST APIs"): positioning variant of the same services tier the v2 resume frames as Go (Gin). The platform services tier is being designed now; on the Java track you present the design in Spring Boot terms (async executors, HikariCP connection pooling, JWT auth filter). If pressed on implementation detail, discuss the design honestly: service boundaries, worker pool sizing, timeout budgets, and idempotent bulk save semantics are language independent. Never claim shipped Java services in production at IA.

Evidence boundary (same as v2 `GROUND_TRUTH.md` evidence matrix):
- Resume-safe: FRM ownership + layered architecture, Masters strangler + Kafka scale + idempotency/DLQ fault tolerance + ELK/New Relic on-call alerting, Design Patterns / Fault Tolerance skills.
- Omit from resume experience: multi-region, Kubernetes cluster ops, Spark, Flink, Terraform. Study those in `../interview_prep_v2/17_senior_systems_study_only.md`.
- CGPA removed from Java resume PDF (kept in shared ground truth for reference).

Deep dives to study (shared with v2):
- `../interview_prep_v2/10_impact_analytics_deep_dive.md`
- `../interview_prep_v2/11_uber_frm_deep_dive.md` (map FastAPI layers to Spring controller/service/repository)
- `../interview_prep_v2/12_masters_gfg_deep_dive.md` (map FastAPI to Spring Boot, Celery to Spring Batch)
- `../interview_prep_v2/13_behavioral_why_switch.md`
- `../interview_prep_v2/14_uber_menu_deep_dive.md`
- `../interview_prep_v2/17_senior_systems_study_only.md`

Verified certificates: **HackerRank Problem Solving** and **LangChain Academy** (source: `KNOWLEDGE-MATERIAL/certificates.txt`).
