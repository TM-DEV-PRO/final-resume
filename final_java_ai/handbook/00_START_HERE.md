# Study Handbook — start here (Java + Python track)

<div class="callout highlight">
<b>What this is.</b> A plain-English handbook for explaining every project, technology and number on the resume <code>Tarun_Mittal_SSE_5yr_Java_AI.pdf</code>, in depth and in your own words. Every chapter defines its terms, shows diagrams and worked examples, explains why each design was chosen, and ends with practice questions and a whiteboard script.
</div>

This is the **Java + Python** track. Stack wording here: Uber FRM is Spring Boot + Spring Data JPA / Hibernate. Masters India is Spring Boot. Impact Analytics is Go/Gin for the platform and Python for the AI agents.

---

## Chapters

| # | Chapter | Read it when |
|---|---|---|
| 01 | [Introductions and career story](01_introductions_and_career_story.md) | First. "Tell me about yourself", "walk me through your resume", "why are you looking". |
| 02 | [Every resume number, explained](02_numbers_explained.md) | Before any technical round. What each number means and how it was derived. |
| 03 | [Impact Analytics: Core platform](03_ia_core_platform.md) | Backend, infra and data rounds. Go/Gin, KPI compiler, tenancy, ClickHouse rollups, 170 GB OOM, Go copier. |
| 04 | [Impact Analytics: Agentic AI](04_ia_agentic_ai.md) | AI / LLM rounds. Keep/Drop, lenses, fallbacks, registry, Ask Iris, evaluation gates. |
| 05 | [Uber FRM Scoping Platform](05_uber_frm.md) | Backend, data modelling and correctness rounds. Finance concepts explained from zero. |
| 06 | [Uber Eats Menu + Uber Mobility ANZ](06_uber_menu_and_anz.md) | Streaming (Kafka, Flink), scraping and RAG rounds. |
| 07 | [Masters India](07_masters_india.md) | Microservices migration, latency, queues, idempotency, sharding. |
| 08 | [GeeksforGeeks](08_geeksforgeeks.md) | Early-career story, Django, caching, hot rows. |
| 09 | [Tech glossary](09_tech_glossary.md) | Every technology on the resume: what, how, where used, why, alternatives. |
| 10 | [Core concepts explained](10_core_concepts_explained.md) | Idempotency, caching, circuit breakers, sharding, exactly-once, p95, RAG and more, from zero. |
| 11 | [STAR stories](11_star_stories.md) | Behavioral rounds. |
| 12 | [LinkedIn and outreach](12_linkedin_and_outreach.md) | Recruiter calls, LinkedIn questions, cold emails, referrals. |

---

## Study plans

**If you have one evening.** Read 01 (intros), 02 (numbers), and the one-minute version plus the "Say this / don't say this" box of chapters 03–07.

**If you have three days.**
- Day 1: 01, 02, 03, 04. Practise the IA whiteboard scripts out loud.
- Day 2: 05, 06, 07, 08. Practise each one-minute version.
- Day 3: 11 (pick 6 stories and rehearse), skim 09 and 10 for anything unfamiliar, then do the practice drills at the end of each project chapter without looking.

**If you have a week.** Add one deep-dive doc per day from `prep/` (listed below) and do every practice drill twice, once out loud.

---

## How to answer any question (the shape that works)

1. **Direct answer first**, in one sentence.
2. **Context**: what the system was and why it mattered.
3. **What I did**: the design, with one concrete detail.
4. **Result**: one or two numbers, said the way chapter 2 shows.
5. **What I learned or would change.**

Keep it to about 60–90 seconds, then stop and let them pick the next thread.

---

## The honesty rules (they protect you)

<div class="callout warn">
• Uber work was <b>via EPAM</b>. ANZ is <b>historical</b> Uber Mobility work. Menu 98% is <b>offline</b> evaluation.<br>
• 80% is a <b>CI promotion gate</b>, not live accuracy for all tenants. 73% and 74% come from a <b>separate 200-case benchmark</b>.<br>
• 15.5× is <b>query time</b>. The 170 GB OOM is <b>load time</b>. They're not cause and effect.<br>
• 344k is <b>rows per second</b>, not requests per second. The 4.09B copy was <b>in flight</b>.<br>
• Partition rollback means <b>drop the partition and recopy</b>, not an atomic swap.<br>
• At Impact Analytics there's no Kafka, Flink, CDC, Kubernetes operations, Milvus or human review queue. Cluster Copilot and Hindsight are <b>verbal-only</b> depth. LangSmith is <b>Ask Iris</b> only.<br>
• "Led 3" is Uber FRM. "Mentored 2" is Masters India. Don't merge them.<br>
• Kubernetes, Terraform, Spark: study-only / literacy. Never "I operated clusters".<br>
• Never share cluster hosts, passwords or .env values. Don't offer to open-source the copier.
</div>

---

## Deeper material in this track

Once a chapter makes sense, these go further:

- Impact Analytics: [`prep/10_impact_analytics_deep_dive.md`](../prep/10_impact_analytics_deep_dive.md), [`prep/23a_ia_interview_pack.md`](../prep/23a_ia_interview_pack.md), [`prep/42_clickhouse_rollup_migration.md`](../prep/42_clickhouse_rollup_migration.md), [`prep/43_ia_bullet_defense.md`](../prep/43_ia_bullet_defense.md), [`docs/assort_kd_flow/PIPELINE.md`](../docs/assort_kd_flow/PIPELINE.md)
- Uber: [`prep/11_uber_frm_deep_dive.md`](../prep/11_uber_frm_deep_dive.md), [`prep/14_uber_menu_deep_dive.md`](../prep/14_uber_menu_deep_dive.md), [`prep/23b_uber_interview_packs.md`](../prep/23b_uber_interview_packs.md)
- Masters and GFG: [`prep/12_masters_gfg_deep_dive.md`](../prep/12_masters_gfg_deep_dive.md), [`prep/23c_masters_gfg_interview_packs.md`](../prep/23c_masters_gfg_interview_packs.md)
- All bullets with their tech: [`prep/41_pdf_bullet_tech_defense.md`](../prep/41_pdf_bullet_tech_defense.md). Number sources: [`prep/09_metrics_derivations.md`](../prep/09_metrics_derivations.md)
- Behavioral: [`prep/07_behavioral_star_stories.md`](../prep/07_behavioral_star_stories.md), [`prep/39_behavioral_question_bank.md`](../prep/39_behavioral_question_bank.md)
- Diagrams and schemas: [`prep/33_architecture_diagrams.md`](../prep/33_architecture_diagrams.md), [`prep/34_er_tables_tech_why.md`](../prep/34_er_tables_tech_why.md), [`prep/35_table_schemas_api_design.md`](../prep/35_table_schemas_api_design.md)
- Facts registry: [`prep/GROUND_TRUTH.md`](../prep/GROUND_TRUTH.md)
- Company-specific: [Oracle OCI guide](../../oracle/index.md)
