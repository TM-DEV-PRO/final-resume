# Ground Truth (Final Java + AI)

Self-contained for this track. Do **not** treat `resume/`, `resume_v2/`, `resume_java/`, or `campaign_pygo_xyz/` as sources of truth (those tracks are being removed).

**PDF:** `Tarun_Mittal_SSE_Java_AI_Final.pdf` · Project title: **Agentic AssortSmart (AI-Powered Retail Merchandise Planning)**

**Keep/Drop pipeline reference:** track copy [`docs/assort_kd_flow/PIPELINE.md`](../docs/assort_kd_flow/PIPELINE.md) · shared [`docs/assort_kd_flow/PIPELINE.md`](../../docs/assort_kd_flow/PIPELINE.md).

## Summary (PDF)

1. Senior Software Engineer with **5 years** of experience designing and owning cloud-native, high-throughput **distributed systems**.
2. Expertise in **Java and Python microservices**, with applied experience in **AI-assisted and RAG systems**.
3. Proven track record shipping production systems, leading backend migrations, and improving reliability, performance, and scalability.

Skills line still uses **AI & Agents** (full list), not “Applied AI”.

## Resume PDF IA bullets (approved)

1. Building **AssortSmart**, a retail merchandise planning platform for seasonal buying, store clustering, and assortment decisions.
2. Architected AssortSmart's **Keep/Drop engine** at article × plan-season grain, combining deterministic **ST%/ROS** scoring with **LangGraph** lenses, kept agents **SELECT-only** on ClickHouse through CSV-first bake-and-promote, with promotions gated on **300 gold cases** and **≥80% offline accuracy**.
3. Built a **read-only dig-deeper QnA agent** over locked Keep/Drop decisions, enabling planners to understand why styles were kept or dropped while schema constraints preserved frozen decisions and blocked writes to ClickHouse, CSVs, and outcomes.
4. Drove adoption of **ClickHouse** as AssortSmart's planning analytics engine, reducing pivot latency from **189s to 12.3s** (~**15.5x**) on **250M rows** through a row-identical Postgres-versus-ClickHouse POC.

**Stack on this track:** agent plane = Python, LangGraph, MCP; write plane = Spring Boot. IA agent plane Python; write APIs framed as Spring Boot on this track; ClickHouse is not accessed via Hibernate. Never claim shipped Java services in production at IA; say building / design ownership for Copilot/Hindsight verbal topics.

**Honesty:** Keep/Drop and QnA are real work from `assort_kd_flow`. The 300-gold / ≥80% offline accuracy line is a **promotion gate / design** — do **not** invent “shipped to all tenants.”

## Verbal only / not on PDF (building)

- **Cluster Recommendation Copilot** — architecture / FRD / deep-dive; not a PDF headline bullet.
- **Hindsight** — prior-season decision layer; not a PDF headline bullet.
- Off-PDF interview depth: 8.5% (37/437) → under 2% TARGET · 14 tools · 3 gates · 63/8 DDL · line-plan ~12B → ~25M · under 1h / ≥20 configs TARGET.

## Stack framing (this PDF)

- FRM / Masters APIs: Spring Boot framing where this track claims it.
- Menu scraping and AI extraction: **Python unchanged**.
- IA: IA agent plane Python; write APIs framed as Spring Boot on this track; ClickHouse is not accessed via Hibernate. Never claim shipped Java services in production at IA; say building / design ownership for Copilot/Hindsight verbal topics.
- GFG on PDF: **PHP → Django (Python)**.

## Evidence boundary

- Resume-safe: FRM ownership + layered architecture; Masters strangler + Kafka scale + idempotency/DLQ + ELK/New Relic on-call (experience). Skills use **AI & Agents** full list.
- Menu has Kafka + Flink (keyed normalize/dedupe/replay) on PDF. Omit Spark, multi-region, K8s ops, Terraform from resume.
- Metric prose everywhere: **from about 2 weeks to 3–4 days**; **from 24 hours to 2 hours**; **from 189s to 12.3s** (not arrow form in spoken/written prose).
- CGPA removed from resume PDFs.

## Deep dives (this track)

- `10_impact_analytics_deep_dive.md` · `23a_ia_interview_pack.md`
- `11_uber_frm_deep_dive.md` · `14_uber_menu_deep_dive.md`
- `12_masters_gfg_deep_dive.md` · `13_behavioral_why_switch.md`
- `17_senior_systems_study_only.md` · `36_skills_ai_agents_defense.md`
- Keep/Drop pipeline: `../docs/assort_kd_flow/PIPELINE.md`

Verified certificates: **HackerRank Problem Solving** and **LangChain Academy**.
