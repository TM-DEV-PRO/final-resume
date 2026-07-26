# Multi-persona panel + 65-JD ATS rescore (post-Flink)

**Date:** 2026-07-27  
**Resumes:** PyGo XYZ · v2 · Java (Flink on Menu for all three)  
**Agents:** CTO · EM · Technical interviewer · Recruiter (8 MNCs) · ATS rescore

---

## Executive verdict

| Lens | Verdict |
|---|---|
| **CTO / VP Eng** | **BORDERLINE** — advance to technical rounds; no offer without EPAM scope validation + honesty on TARGETS |
| **Engineering Manager** | **Borderline SSE / strong SDE2** — hire as senior IC contributor; FAANG often levels SDE2-high |
| **Hard interviewer** | **BORDERLINE → PASS if honest** to GROUND_TRUTH | Scores: systems **7/10**, agentic honesty **6/10**, streaming **5/10**, leadership **7/10** |
| **Recruiter (8 MNCs)** | **Advance:** Amazon, Microsoft, LinkedIn, Atlassian, Salesforce · **Hold:** Google, Apple, Netflix |
| **ATS vs 65 JDs** | **34 PASS · 21 BORDERLINE · 10 FAIL** (was 31/23/11; **+3 PASS** from Flink on Menu) |

**Keyword ATS (agent bank):** v2 **89** · Java **91** · PyGo **87** · **Local bank:** pygo/v2 **94** · java **91**

---

## Persona summaries

### CTO
**Hire?** Borderline — screen, don't skip-offer.  
**Strengths:** Masters strangler + Kafka/idempotency; Menu Kafka→Flink with measured outcomes; FRM audit/SSOT depth; measured IA baselines (8.5%).  
**Risks:** EPAM ≠ Uber FTE; IA 2 months + “building/targeting”; skills breadth (K8s/gRPC padding); hop pattern.  
**Must prep:** EPAM scope story; why leave IA; TARGET vs MEASURED; strip or defend K8s/gRPC.

### Engineering Manager
**Level:** Strong SDE2; SSE only if bar ≈5y + light mentoring.  
**Submit Java** only to true Java shops (Airbnb App Foundation, Atlassian, Salesforce) — integrity risk if interviewed as Spring owner at Uber.  
**STAR needed:** Masters strangler, Menu ingest, FRM led-3 (honest pod lead), IA building-not-shipped, on-call triage Masters.

### Technical interviewer
**Fail traps:** invent Menu peak TPS; say agentic “shipped under 2%”; claim FRM 70% measured; claim K8s ops.  
**Pass path:** burst/replay Flink defense; building + load test pending; FRM TARGET; Masters 1M+/day with estimated peak TPS tagged.

### Recruiter — 8 companies
| Company | Gut | PDF | Title |
|---|---|---|---|
| Amazon | Advance | pygo | SDE II |
| Google | Hold | pygo | SSE |
| Microsoft | Advance | java | SSE / SWE II backend |
| LinkedIn | Advance | java/pygo | SSE Systems Infra |
| Apple | Hold | java/pygo | SWE Services |
| Netflix | Hold | pygo | L5 stretch |
| Atlassian | Advance | java | Senior Backend |
| Salesforce | Advance | java | Senior Backend |

**Prioritize this month:** 1) Atlassian 2) Salesforce 3) Amazon SDE II

---

## 65-JD ATS rollup (best-of-3, post-Flink)

| Company | PASS | BORDERLINE | FAIL |
|---|---:|---:|---:|
| Google | 3 | 2 | 0 |
| Amazon | 2 | 2 | 1 |
| Microsoft | 2 | 2 | 1 |
| Airbnb | 3 | 1 | 1 |
| PlanetScale | 3 | 1 | 1 |
| Databricks | 4 | 1 | 0 |
| Roku | 1 | 2 | 2 |
| Rubrik | 1 | 2 | 2 |
| Netflix | 0 | 4 | 1 |
| LinkedIn | 2 | 1 | 2 |
| Apple | 4 | 1 | 0 |
| Atlassian | 5 | 0 | 0 |
| Salesforce | 4 | 1 | 0 |
| **TOTAL** | **34** | **21** | **10** |

**Flink upgrades:** Atlassian streaming/SF community · Databricks Runtime (java PASS stretch) · Menu Kafka+Flink now on all PDFs.

**2026-07-27 packaging lift:** Go write-path + quarter-sharded PG + Flink keyed dedupe/replay — see [`26_python_job_listings_ats.md`](26_python_job_listings_ats.md) § Resume packaging lift. Expected: PlanetScale Go signal stronger; Databricks Runtime confidence up; Rubrik/Airbnb routing unchanged (still skip hard YoE).

Full apply/skip lists: prior file [`24_job_listings_5x_ats_scorecard.md`](24_job_listings_5x_ats_scorecard.md) + agent deltas above.

---

## Action list (from panel)

1. Apply **Atlassian / Salesforce / Amazon SDE II** this week with correct PDF.  
2. In every screen: “IA building; under 2% / under 1h are targets; load test pending.”  
3. Defend Menu Flink as **burst + keyed dedupe + replay**, not vanity TPS.  
4. Do not lead with K8s/gRPC; drop from verbal if probed cold.  
5. Prep EPAM “via Uber product ownership” story without title inflation.

---

## Agent artifacts
- CTO: panel notes in session  
- EM / Interviewer / Recruiter / ATS: consolidated here  
- Live hub: https://tm-dev-pro.github.io/final-resume/
