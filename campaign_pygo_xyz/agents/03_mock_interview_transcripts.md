# Mock Interview Transcripts (interviewee vs panel)

Interviewee answers in first person. Interviewer pushback in italics. Numbers match GROUND_TRUTH.

## Round A — Technical Lead (IA deep dive)

**TL:** Walk AssortSmart and what you own.

**You:** AssortSmart helps retailers decide what to buy, how much, and which stores. I am building the cluster recommendation copilot on FastAPI LangGraph MCP over a shared Go Gin doing layer on per-tenant ClickHouse. Measured clustering failures on kik were 8.5% (37/437). We target under 2% with 14 audited tools that only read planning data and 3 human confirm gates before write-back. I am also building Hindsight scorecards with overnight narration grounded in computed metrics and tenant catalogs that onboard without a code deploy. Copilot targets days to under 1 hour and at least 20 configs per plan. Phase 1 design passed external review. Load test is still pending so I say building not shipped.

*TL: Why not let the agent run arbitrary SQL?*
**You:** The model does not get a SQL shell. Tools are allow-listed read functions. Writes go through human gates and the product write path. That is the accurate claim, not a slogan about never writing SQL.

*TL: Defend the ClickHouse number.*
**You:** Row-identical pivot POC at 250M rows cut a heavy grid from 189s to 12.3s about 15.5× measured. If you strip COUNT(DISTINCT) typical aggs can fall to roughly 2–3×. I will say that unprompted if pushed.

## Round B — Engineering Manager (Masters on-call)

**EM:** Tell me about production ownership.

**You:** At Masters India I owned the FastAPI strangler and Kafka e-invoice platform. We cut p95 from 1.2s to 300ms for 1500+ clients and lifted throughput from 700 to 4000 requests/min. I put ELK and New Relic on-call alerting in place which cut incident triage about 70% and raised coverage from 35% to 82% at 98% deployment success.

*EM: Walk a bad night.*
**You:** Bulk IRP spike consumer lag rising. First check lag and error class. Idempotency keys plus DLQ meant we could pause replay and drain without double-filing invoices. Postmortem added better saturation alerts.

## Round C — Amazon-style Hiring Manager (LP)

**HM:** Tell me about Ownership.

**You:** At Uber via EPAM I owned design and architecture for FRM Risk Scoping FastAPI MySQL React across 8 screens and 30+ APIs at $340M group materiality targeting a 70% cut in manual reconciliation. I personally owned Sheets to MySQL recon v2 across 18 files and led 3 engineers through design reviews API contracts and CI gates for PwC-facing releases.

*HM: Is 70% measured?*
**You:** No. It is a TDD target. Baseline calendar time is estimated about 2 weeks to 3–4 days. I always say targeting.

## Round D — CTO (business impact)

**CTO:** Where did you save real money?

**You:** Uber Eats menu ingestion. Selenium scrapers on GCP cut onboarding from 24h to 2h and saved $600K+ annually on 30K+ menus/month. RAG plus Gemini offline eval hit 98% fidelity and 100% schema consistency. Successful ingestions rose to 95%+ with anti-bot controls.

## Round E — Technical Recruiter (Google)

**Recruiter:** What languages and systems?
**You:** Python and Go. FastAPI Gin Kafka ClickHouse PostgreSQL MySQL Redis Docker on GCP and AWS. About 5 years. Currently Senior Software Engineer at Impact Analytics building agentic planning. Before that SDE2 at Uber via EPAM and Masters India.

## Round F — Director of Engineering (mentorship)

**DoE:** How have you multiplied others?
**You:** Mentored 2 engineers through the Masters strangler and led 3 at EPAM/Uber via design reviews and CI quality gates. I measure success as others shipping safely behind contracts not just my LOC.
