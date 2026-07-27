# Java Track — Interview Prep Hub (grounded rewrite)

**Tarun Mittal · Senior Software Engineer (Java / Spring) · July 2026**

Backs `resume_java/` (PDF: `Tarun_Mittal_SSE_Java_5yr.pdf`). Same facts as v2. Non-agentic APIs framed in Spring Boot / Hibernate where defensible. AI/RAG, Menu, and ClickHouse work stay Python.

## Study order

1. [`GROUND_TRUTH.md`](GROUND_TRUTH.md) then [`../interview_prep_v2/GROUND_TRUTH.md`](../interview_prep_v2/GROUND_TRUTH.md)
2. **[`../interview_prep_v2/31_resume_deep_explain_map.md`](../interview_prep_v2/31_resume_deep_explain_map.md)** — every PDF tech / flow / number
3. **[`../interview_prep_v2/23_project_interview_packs.md`](../interview_prep_v2/23_project_interview_packs.md)** — all project interviewer packs (map Spring verbally)
4. [`../interview_prep_v2/10_impact_analytics_deep_dive.md`](../interview_prep_v2/10_impact_analytics_deep_dive.md)
5. [`../interview_prep_v2/11_uber_frm_deep_dive.md`](../interview_prep_v2/11_uber_frm_deep_dive.md) — map FastAPI layers to Spring controller / service / repository
6. [`../interview_prep_v2/14_uber_menu_deep_dive.md`](../interview_prep_v2/14_uber_menu_deep_dive.md) — no Spring claim; Menu stays Python
7. [`../interview_prep_v2/12_masters_gfg_deep_dive.md`](../interview_prep_v2/12_masters_gfg_deep_dive.md) — Celery → Spring Batch
8. [`../interview_prep_v2/13_behavioral_why_switch.md`](../interview_prep_v2/13_behavioral_why_switch.md) · [`07_behavioral_star_stories.md`](07_behavioral_star_stories.md)
9. [`../interview_prep_v2/22_application_questions.md`](../interview_prep_v2/22_application_questions.md)
10. Local: [`06_tech_deep_dives.md`](06_tech_deep_dives.md), [`08_role_targeting_and_rapid_fire.md`](08_role_targeting_and_rapid_fire.md)

## Stack mapping

| Real / v2 | Java track claim |
|---|---|
| FastAPI (FRM, Masters) | Spring Boot (MVC) |
| SQLAlchemy 2.0 | Spring Data JPA / Hibernate |
| Django (GFG) | Spring Boot + Spring MVC |
| Celery | Spring Batch / `@Async` |
| pytest | JUnit 5 + Mockito |
| LangGraph / Menu / ClickHouse | Unchanged Python |

<div class="callout warn">
<b>Honesty.</b> Same as v2 GROUND_TRUTH. Do not invent Spring for Menu or Hibernate for ClickHouse. FRM 70% is a TDD target. Endpoint count is 30+, not 36. Menu PDF has no Kafka/Flink/Spark.
</div>

## Resume at a glance (Java grounded)

| Company | Lead claims |
|---|---|
| Impact Analytics | Product-first AssortSmart; Spring write APIs; ONE CH bullet; see `23a` + `31` |
| Uber FRM | Spring Boot + JPA; 30+ APIs; targeting 70%; led 3; see `23b` |
| Uber Menu | Python Selenium→Kafka→Flink + RAG/Gemini/Milvus + ANZ Mobility; see `23b` |
| Masters India | Step-by-step Laravel→Spring Boot; Kafka + PG by tax quarter; see `23c` |
| Masters India | Spring Boot strangler; Kafka event platform; 700→4,000 req/min; see `23c` |
| GeeksforGeeks | Spring Boot telling; 10K+ daily; see `23c` |
