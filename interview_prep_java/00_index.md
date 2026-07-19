# Java Track — Interview Prep Hub (grounded rewrite)

**Tarun Mittal · Senior Software Engineer (Java / Spring) · July 2026**

Backs `resume_java/` (PDF: `Tarun_Mittal_SSE_Java_5yr.pdf`). Same facts as v2. Non-agentic APIs framed in Spring Boot / Hibernate where defensible. AI/RAG, Menu streaming, and ClickHouse work stay Python.

## Study order

1. [`GROUND_TRUTH.md`](GROUND_TRUTH.md) then [`../interview_prep_v2/GROUND_TRUTH.md`](../interview_prep_v2/GROUND_TRUTH.md)
2. [`../interview_prep_v2/10_impact_analytics_deep_dive.md`](../interview_prep_v2/10_impact_analytics_deep_dive.md)
3. [`../interview_prep_v2/11_uber_frm_deep_dive.md`](../interview_prep_v2/11_uber_frm_deep_dive.md) — map FastAPI layers to Spring controller / service / repository
4. [`../interview_prep_v2/14_uber_menu_deep_dive.md`](../interview_prep_v2/14_uber_menu_deep_dive.md) — no Spring claim
5. [`../interview_prep_v2/12_masters_gfg_deep_dive.md`](../interview_prep_v2/12_masters_gfg_deep_dive.md) — Celery → Spring Batch
6. [`../interview_prep_v2/13_behavioral_why_switch.md`](../interview_prep_v2/13_behavioral_why_switch.md)
7. Local: [`06_tech_deep_dives.md`](06_tech_deep_dives.md), [`08_role_targeting_and_rapid_fire.md`](08_role_targeting_and_rapid_fire.md), [`09_metrics_derivations.md`](09_metrics_derivations.md)

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
<b>Honesty.</b> Same as v2 GROUND_TRUTH. Do not invent Spring for Menu or Hibernate for ClickHouse. FRM 70% is a TDD target. Endpoint count is 30+, not 36.
</div>

## Resume at a glance (Java grounded)

| Company | Lead claims |
|---|---|
| Impact Analytics (14 May 2026–) | Same CH/CQRS/copilot numbers as v2 (Python) |
| Uber FRM | Spring Boot + JPA framing; 8 screens, 30+ endpoints, 11 tables, led 3, 1,100+ tests, targeting 70% |
| Uber Menu | Python streaming (no Spring) |
| Masters India | Spring Boot + Spring Batch framing; mentored 2; 1.2s to 300ms; 700 to 4,000 RPM |
| GeeksforGeeks | Spring Boot framing; 10K+ daily queries |
