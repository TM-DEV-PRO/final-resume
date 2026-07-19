# Python/Go resume v2 — Interview Prep Hub (grounded rewrite)

**Tarun Mittal · Senior Software Engineer · July 2026**

This hub backs `resume_v2/` (PDF: `Tarun_Mittal_SSE_5yr_v2.pdf`). Original `resume/` + `interview_prep/` stay untouched.

## Study order (do this)

1. [`GROUND_TRUTH.md`](GROUND_TRUTH.md) — every shippable number and honesty tag
2. [`10_impact_analytics_deep_dive.md`](10_impact_analytics_deep_dive.md) — Agentic AssortSmart, PG to CH POC, read path design, copilot, mock interview Q&A
0. [`16_ats_recruiter_report.md`](16_ats_recruiter_report.md) — big tech ATS/recruiter scorecards per company (which resume to send where)
3. [`11_uber_frm_deep_dive.md`](11_uber_frm_deep_dive.md) — real schema, routes, recon migration
4. [`14_uber_menu_deep_dive.md`](14_uber_menu_deep_dive.md) — Kafka/Flink/Spark/Pinot
5. [`12_masters_gfg_deep_dive.md`](12_masters_gfg_deep_dive.md) — strangler migration, caching, GFG
6. [`13_behavioral_why_switch.md`](13_behavioral_why_switch.md) — intro, every switch, IA 14 May 2026 exit
7. [`17_senior_systems_study_only.md`](17_senior_systems_study_only.md) — ownership, on-call/SLOs, fault tolerance; STUDY ONLY for multi-region, K8s ops, Spark, Flink, Terraform
8. [`09_metrics_derivations.md`](09_metrics_derivations.md) — ESTIMATED vs DOCUMENTED arithmetic

Supporting: [`01_skills_trim_rationale.md`](01_skills_trim_rationale.md), [`02_mongodb_elasticsearch.md`](02_mongodb_elasticsearch.md), [`03_uber_menu_streaming_numbers.md`](03_uber_menu_streaming_numbers.md), [`08_role_targeting_and_rapid_fire.md`](08_role_targeting_and_rapid_fire.md), [`15_judge_loop_report.md`](15_judge_loop_report.md).

Original playbook still useful for agentic Assort depth: `../interview_prep/agentic_assort_playbook/`.

<div class="callout warn">
<b>Honesty guardrail.</b> MEASURED vs TARGET vs HISTORICAL vs ESTIMATED are defined in GROUND_TRUTH. FRM 70% is a TDD target. CDC tool authorship is not yours. Copilot is Phase 1 design approved, load test pending. Benchmark hardware was not identical (PG 32 vCPU / 256 GB vs CH 16 vCPU / 64 GB).
</div>

## Resume at a glance (v2 grounded)

| Company | Lead claims |
|---|---|
| Impact Analytics (14 May 2026–) | CH Order Batching 3.86s vs PG 3m40s+ (60x); 5.9M rows/s insert; CQRS + CDC + Redis RYW; update 39s to 7s; copilot targets days to under 1h |
| Uber FRM | Owned platform; designed layered architecture; owned recon v2 (18 files); led 3; 8 screens, 30+ APIs, $340M, targeting 70% |
| Uber Menu | 30K menus/mo, 24h to 2h, $600K+/yr, +95% ingest, RAG/Gemini 98% fidelity (Python + Selenium + GCP) |
| Masters India | Owned strangler + mentored 2; Kafka/sharding TPS/RPS; idempotency/DLQ fault tolerance; on-call alerting; 1M+ txn/day |
| GeeksforGeeks | 10K+ daily queries; +15–20% premium; +30% courses; +70% ops efficiency |
