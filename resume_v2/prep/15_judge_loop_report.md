# Judge loop report (19 Jul 2026)

## Loop 1. Fact vs resume

| Check | Result |
|---|---|
| No 19M GL claim | PASS (dropped) |
| No "36 endpoints" | PASS (says 30+) |
| FRM 70% worded as targeting | PASS |
| IA start May 2026 (14 May in prep) | PASS |
| Mentored 2 / led 3 | PASS |
| CH measured numbers (5.9M, 3.86s, 60x, 43x, 39s to 7s) | PASS |
| CQRS + CDC + Redis RYW | PASS |
| GFG 10K+ (user choice) | PASS |
| Masters 1500+ clients, 700 to 4000 RPM | PASS |
| CDC authorship not claimed as own tool | PASS (prep honesty) |
| Copilot targets not claimed as measured | PASS ("Targets are...") |

## Loop 2. AI markers on resume tex

Scanned experience/objective/skills/activities/education for em dash, whose, enabling, leverage, robust, seamless, cutting-edge, delve. **Zero hits.**

## Loop 3. ATS keyword coverage

- v2 Python/Go track: 19/19 must-haves present (Python, Distributed systems, Microservices, Kafka, PostgreSQL, MySQL, Redis, Kubernetes, Docker, AWS, GCP, CI/CD, Observability, Caching, Mentorship, System Design, ClickHouse, Flink, Spark).
- Java track: 16/16 must-haves present (Java, Spring Boot, Hibernate, Distributed Systems, Microservices, Kafka, MySQL, Redis, Kubernetes, Docker, AWS, GCP, CI/CD, Mentorship, gRPC, JUnit).

## Loop 4. Prep completeness per resume bullet

| Resume project | Defense file |
|---|---|
| IA | 10_impact_analytics_deep_dive.md |
| FRM | 11_uber_frm_deep_dive.md |
| Menu | 14_uber_menu_deep_dive.md |
| Masters + GFG | 12_masters_gfg_deep_dive.md |
| Behavioral / why switch | 13_behavioral_why_switch.md |
| Metrics arithmetic | 09_metrics_derivations.md + GROUND_TRUTH.md |

## Loop 5. Open risks (do not hide)

1. Java track FRM/Masters/GFG Spring framing is a **positioning variant**. Real code for FRM is FastAPI. Interview line: "architecture and outcomes are what I owned; Spring is how I would express the same layering for a Java shop."
2. Menu Kafka peak events/sec and Spark row counts remain ESTIMATED.
3. FRM cycle from-to days remain ESTIMATED if spoken; resume correctly says "targeting a 70% cut" without inventing days.
4. Two page resumes are intentional per user; many FAANG ATS prefer one page for ~5 YoE — keep a one page condensed variant ready if a recruiter asks.

## Loop 6. Layout and credentials

- PASS: name/contact header appears on page 1 only.
- PASS: every project heading has its first bullet on the same page.
- PASS: resume bullets render in one line, except the copilot bullet which uses one full line plus a short continuation.
- PASS: HackerRank Problem Solving and LangChain Academy links match `KNOWLEDGE-MATERIAL/certificates.txt`.

## Loop 5 final judge (TPS/RPS hardening round)

Source: PyMuPDF text extract of `Tarun_Mittal_SSE_5yr_v2.pdf` and `Tarun_Mittal_SSE_Java_5yr.pdf` vs `GROUND_TRUTH.md` (19 Jul 2026).

| Check | Result |
|---|---|
| 1. Number consistency vs GROUND_TRUTH | PASS with notes. All listed money/scale/latency/throughput figures match GT (23.7M, 3.86s, 3m 40s, 60x, 24x, 250K to 5.9M, 8.5% to under 2%, 100% reproducible, p95 under 500ms vs 1 to 20s, 20 to 100 configs, 8 screens, 30+ APIs, $340M, targeting 70%, 11 tables, 55 line items, 14 entities, 10-Q, 30K+/24h to 2h/$600K+, 98%/100% schema, 95% ingestions, 99.9%/20h, 1.2s to 300ms, 1,500+, 100K+/1M+, ~12 TPS/100+ peak, 700 to 4,000 RPM/~67 RPS, 30%/15%/70% triage, 35% to 82%, 98% deploy, 10K+/10x, 15 to 20%, 30%/70% GFG, 2260/37,000+, CGPA 7.7). No 1,100+ tests claim on either PDF (correct: GT has ~1125 unit tests but resume omits). Soft note: "3 approval gates" is not enumerated in GROUND_TRUTH (only "human approval gates"); number is defended in `10_impact_analytics_deep_dive.md` Q6. |
| 2. Grammar / wording / tense | FAIL (minor). Current-role IA mixes present progressive (Building/Developing/Designing) with past "Enforced". Several "from X to Y" ranges omit "from" (latency, throughput, coverage). Hyphen gaps: evidence backed, read only, rule based, anti bot, on call, AI Powered, Sheets backed. Copilot turnaround clause "under 1 hour from days" is stumble-prone. |
| 3. AI markers | PASS. No em dashes, no semicolons in bullet text, no leveraging/spearheaded/utilize/delve/robust/seamlessly. Date en dashes only. |
| 4. v2 vs Java consistency | PASS. Same dates (May 2026 Present, July 2024 May 2026, December 2022 June 2024, August 2021 November 2022). Same numeric claims for shared bullets. Contact/email/phone and stack wording differences intentional. |
| 5. Recruiter 6s first-bullet scan | FAIL (IA only). IA opener is product description with no scale/money/leadership. FRM ($340M/70%), Menu ($600K+/30K+), Masters (led 2 / 1,500+ / p95), GFG (10K+/10x) all lead with strength. |
| 6. Duplicate opening verbs within a project | PASS. |
| 7. Past-role tense | PASS. |

### Flagged items (actionable)

1. Both PDFs, IA bullet 1: weak 6s scan opener. Prefer leading with 60x / 23.7M / ClickHouse POC or Copilot batch 20 to 100 + under 1 hour target.
2. Both PDFs, IA gates bullet: "Enforced ..." among present-tense bullets. Prefer "Enforcing read-only agent tools and 3 approval gates, ..."
3. Both PDFs, Masters: "cutting p95 latency 1.2s to 300ms" -> "from 1.2s to 300ms"; "lifting throughput 700 to 4,000" -> "from 700 to 4,000"; "raised coverage 35% to 82%" -> "from 35% to 82%".
4. Both PDFs, IA copilot: "targeting turnaround under 1 hour from days" -> "targeting turnaround under 1 hour (from days)".
5. Optional hyphen polish (both): evidence-backed, read-only, rule-based, anti-bot, on-call, AI-Powered, Sheets-backed.
6. Optional GT hygiene: add "3 approval gates" to GROUND_TRUTH so the PDF number is not GT-orphan.

## Loop 6 evidence-backed skill hardening (Jul 2026)

| Check | Result |
|---|---|
| Evidence matrix in GROUND_TRUTH | PASS. Resume-safe vs omit rows documented for ownership, architecture, on-call alerting, fault tolerance, Design Patterns, and STUDY-ONLY items. |
| CGPA removed from both PDFs | PASS. Still recorded in GROUND_TRUTH only. |
| Ownership / architecture wording | PASS. FRM uses Owned + Designed the software architecture + Owned recon v2 (18 files). Masters uses Owned strangler. |
| Fault tolerance + on-call alerting | PASS. Masters idempotency/retries/DLQ + ELK/New Relic on-call alerting. Skills add Fault Tolerance; v2 adds Design Patterns. |
| Forbidden on resume | PASS. No Terraform, Spark, Flink, multi-region, Vitess on either PDF. |
| One-page layout | PASS. v2 bottom ~778, Java ~773 (letter page ~792). No semicolons / em dashes. |
| Prep coverage | PASS. `17_senior_systems_study_only.md` added with STUDY ONLY labels and official SRE/K8s/Terraform/Spark/Flink links. Java FRM/Masters project pages corrected (dropped 36 endpoints / 19M rows / 2500 clients). |
| Cross-track numeric parity | PASS on shared money/scale figures. |

## Loop 7 number / money / Spark-Flink verification

| Check | Result |
|---|---|
| IA CH POC vs BENCHMARK-NUMBERS.md | PASS. 60× / 23.7M / 3m40s→3.86s / 24× 250K→5.9M all MEASURED. |
| FRM 70% with (~2 weeks to ~3–4 days) | PASS on both PDFs. Tagged TARGET + ESTIMATED baseline in GT. |
| Spark/Flink absent from PDFs | PASS. Decision log + study-only prep present. |
| Every resume number catalogued | PASS via `18_resume_number_catalog.md` + rewritten `09_metrics_derivations.md`. |
| AI markers / CGPA / one page | PASS. |

## Loop 8 Spark + Flink restore

| Check | Result |
|---|---|
| Placement | Uber Menu (best fit) |
| Both PDFs one page with Flink+Spark | PASS |
| Prep depth | `14_uber_menu_deep_dive.md` rewritten |
| Contradictions cleared in GT evidence matrix | PASS |
