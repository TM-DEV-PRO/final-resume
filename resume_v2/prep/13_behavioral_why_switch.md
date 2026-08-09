# Behavioral, Intros, and Why Switch (v2 + Java tracks)

Use with STAR stories in the main prep. Numbers and ownership match `GROUND_TRUTH.md`.

---

## 60 second introduction

I am a Senior Software Engineer with five years building backend and data platforms. Most recently at Impact Analytics I am owning the PostgreSQL to ClickHouse analytics path for our retail planning product and the agentic store clustering copilot. Before that, at Uber via EPAM, I built the Financial Risk Management scoping platform that replaced a Google Sheets close process for Finance and PwC, and I worked on the Uber Eats menu ingestion pipeline that processes about 30,000 menus a month. Earlier I led the Masters India GST platform migration from a PHP monolith to FastAPI microservices, mentoring two engineers, and I started at GeeksforGeeks migrating PHP services to Django. I am looking for a senior backend or data platform role where I can own systems end to end for the next several years.

---

## Why each switch (keep each under 45 seconds)

### GeeksforGeeks to Masters India (after about 1.2 years)

At GFG I was shipping feature work on a consumer content platform. Masters India offered ownership of a regulated financial product and a real platform migration. I wanted to grow from feature delivery into owning a service cutover and mentoring juniors. That is where I led the PHP to FastAPI migration and mentored two engineers.

### Masters India to Uber via EPAM (after about 1.5 years)

I had taken the GST platform through migration and scale. Uber via EPAM was a jump in engineering bar, global product surface, and systems complexity. I wanted Bazel's monorepo discipline, Uber scale practices, and work that sat next to Finance and audit. That is where I owned the FRM scoping backend and the recon v2 migration.

### Uber via EPAM to Impact Analytics (after about 1.9 years)

I wanted deeper ownership of data platform and agentic AI systems, not just service APIs. Impact Analytics offered a senior charter around ClickHouse, CQRS analytics offload, and an agentic clustering product. That matched where I want to go deep for the next stretch of my career.

### Why exploring after joining Impact Analytics on 14 May 2026 (about 2 months)

Use framing A plus D from production research. Do not badmouth.

> I joined Impact Analytics for a senior charter around ClickHouse analytics offload and the agentic clustering product. After onboarding I learned the day to day mix of scope and team structure was not the multi year ownership I had signed up for. I closed my open work professionally and I am being careful about fit this time. I am interviewing fewer companies more carefully, including yours, because I want the next role to be a multi year build.

If asked about four companies in five years:

> Each move added a layer: product features at GFG, SaaS migration and mentorship at Masters India, Uber scale platform work via EPAM, and data plus agentic systems at Impact. The last nearly two year stretch shows I stay when scope compounds. I am optimizing for that again.

Avoid: calling anyone toxic, leading with compensation, saying the current role does not count, apologizing as if you failed.

---

## Leadership STAR fragments (use real headcounts)

### Led 3 engineers at EPAM / Uber (FRM)

- Situation: FRM scoping backend needed a layered architecture and a Sheets to MySQL recon migration while the frontend and Finance stakeholders kept iterating.
- Task: Own the service, keep the pod shipping, and raise test coverage under Bazel.
- Action: Broke work into handler, service, repository ownership; set PR conventions from the backend team sync; paired on the recon v2 cutover; reviewed every PR early, then stepped back as ownership stuck.
- Result: Platform at 8 screens and 30 plus endpoints, 1,100 plus unit tests, recon on MySQL, Finance using the tool for quarterly close.

### Mentored 2 engineers at Masters India

- Situation: Junior engineers were new to FastAPI and async patterns during the monolith to microservices migration.
- Task: Get them shipping independently without breaking filing day traffic.
- Action: Pair programmed the first canary cutover, wrote the shared retry and idempotency helpers, reviewed PRs for boundary validation and observability, then let them own full services.
- Result: Both shipped services on their own; platform reached 1.2s to 300ms p95 and 700 to 4,000 RPM.

---

## Amazon LP mapping (short)

| LP | Story |
|---|---|
| Ownership | FRM recon v2 migration and schema ownership |
| Dive Deep | ClickHouse update strategy bake off (39s to 7s) and column aliasing bug |
| Deliver Results | Menu pipeline $600K annual savings, Masters 700 to 4,000 RPM |
| Hire and Develop the Best / Mentorship | Pod of 3 at EPAM, mentored 2 at Masters India |
| Insist on Highest Standards | Coverage 35 to 82 percent, 1,100 plus FRM tests |
| Bias for Action | Early exit from a short tenure rather than coasting |

---

## Netflix / culture style one liners

- Judgment: Chose CQRS plus CDC over dual write because dual write creates silent drift across engines.
- Candor: Tell interviewers the 70 percent FRM cut is a TDD target, not a measured KPI.
- Ownership: Recon v2 branch under my username, end to end from design to cutover.
