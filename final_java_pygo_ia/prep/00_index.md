# Final Java + AI (IA = Py/Go) — Interview Prep Hub

**Tarun Mittal · Senior Software Engineer · Sep 2026**

Backs this track (PDF: `Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf`). Canonical claims: [`docs/ASSORTSMART_TAB_RESUME.md`](../../docs/ASSORTSMART_TAB_RESUME.md).

**Summary on the PDF:** 5 years architecting high-throughput cloud-native distributed systems and leading zero-downtime migrations · Expert in **Java, Python and Go microservices** · LangGraph multi-agent systems, Milvus RAG, deterministic eval harnesses.

**Keep/Drop pipeline:** [`docs/assort_kd_flow/PIPELINE.md`](../docs/assort_kd_flow/PIPELINE.md).

## Study order

1. [`GROUND_TRUTH.md`](GROUND_TRUTH.md) · [`00_final_resume_map.md`](00_final_resume_map.md)
2. [`41_pdf_bullet_tech_defense.md`](41_pdf_bullet_tech_defense.md) · [`23a_ia_interview_pack.md`](23a_ia_interview_pack.md) · [`31_resume_deep_explain_map.md`](31_resume_deep_explain_map.md)
3. [`37_senior_screen_deep_qa.md`](37_senior_screen_deep_qa.md) · [`32_common_interview_qa.md`](32_common_interview_qa.md)
4. FRM/Menu/Masters: [`11_uber_frm_deep_dive.md`](11_uber_frm_deep_dive.md) · [`14_uber_menu_deep_dive.md`](14_uber_menu_deep_dive.md) · [`12_masters_gfg_deep_dive.md`](12_masters_gfg_deep_dive.md)
5. [`36_skills_ai_agents_defense.md`](36_skills_ai_agents_defense.md) · diagrams/schemas `33`/`34`/`35`
6. Keep/Drop pipeline: [`../docs/assort_kd_flow/PIPELINE.md`](../docs/assort_kd_flow/PIPELINE.md)

## Stack mapping (this PDF)

| Area | Claim on this PDF |
|---|---|
| AssortSmart platform / HTTP edge | **Go / Gin**, Wire, h2c, Datadog, 10k peak RPS |
| AssortSmart agentic flows | Python, FastAPI, LangGraph · Keep/Drop + Missed Opp + Top Style · Ask Iris LangGraph Supervisor+Evaluator |
| FRM / Masters | Spring Boot / Spring Data JPA / Hibernate / Spring Boot |
| Menu / GFG | Python (Selenium→Kafka→Flink exactly-once; PHP→Django) |

<div class="callout warn">
<b>Never break these.</b> 300-case / ≥80% is a <b>CI promotion gate</b> — not “all tenants live.”
Ask Iris is <b>Shipped</b> on the PDF as a capability — do not invent tenant-wide SLAs.
10k peak RPS / 2.11B / 2.4B / $100 token / 1.6M article-seasons / 335K+ products are <b>on the PDF</b> (source: AssortSmart tab / PDF).
Cluster Recommendation Copilot / Hindsight are <b>verbal only / not on PDF</b>.
Menu <b>98% is offline eval</b>. Uber work was <b>via EPAM</b>. ANZ 99.9% is <b>HISTORICAL Mobility</b>.
Do not invent Spark / Pinot / Kubernetes-operations / CDC ownership. Packet Kafka/Flink belongs on <b>Menu</b>, not IA.
</div>


## Resume at a glance

| Company | Lead claims |
|---|---|
| Impact Analytics | Two IA subsections: Platform (10k RPS, CH 189s→12s / 1.6M / 2.4B, KPI parser, Firebase/OIDC, 100% / 1200+ tests) and Agentic (335K+, 88k/<$100, 7 lenses, 2.11B air-gap, Ask Iris shipped, 300-case / ≥80% gate vs 74% baseline) |
| Uber FRM | 36 Spring Boot endpoints; 70% 14d→3d; $340M; 19M GL; L1–L4; 8-table SOADB; SHA-256; led 3; 100% coverage; SOX 50% |
| Uber Menu | 24h→2h; $600K; 30K+; 98% offline RAG/Milvus; 95%+; Kafka+Flink exactly-once |
| ANZ | 99.9% HISTORICAL Mobility; 20h/week |
| Masters India | Spring Boot; 1.2s→300ms; 1M+/day; 35%→82%; 98% deploy |
| GeeksforGeeks | Django; 10K+; 10x; 20% / 30% / 70% |\n