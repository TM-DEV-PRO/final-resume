# Behavioral question bank — mapped to Tarun's stories

**Track:** Final Java + AI (IA = Py/Go) · **PDF:** `Tarun_Mittal_SSE_Java_PyGoIA_Final.pdf` · **Stack on this track:** Java/Spring · Python · Go/Gin

**Source of the question list:** adapted from
[ashishps1/awesome-behavioral-interviews](https://github.com/ashishps1/awesome-behavioral-interviews)
(tips, question taxonomy, reverse questions, CTCI-style prep-grid idea). Their sample
answers are generic fiction and are **not** copied. Every answer below uses Tarun's
real experience and the honesty tags in `GROUND_TRUTH.md`.

**Companion files:**
- Full 10 STAR stories: [`07_behavioral_star_stories.md`](07_behavioral_star_stories.md)
- Why-hire / pitch / objections: [`38_why_hire_tarun_qa.md`](38_why_hire_tarun_qa.md)
- Project × question prep grid: [`40_behavioral_prep_grid.md`](40_behavioral_prep_grid.md)
- Company LP guides: [`company_behavior_guides.md`](../campaign_extras/behavioral/company_behavior_guides.md)

<div class="callout warn">
<b>Never break these.</b> Keep/Drop gold gate is a <b>promotion gate</b> (not multi-tenant GA). Cluster Copilot / Hindsight are <b>verbal only / not on PDF</b>. FRM <b>70% is a TARGET</b>.
Menu <b>98%/100% is offline eval</b>. <b>No Spark / SFT</b>. Uber work was <b>via EPAM</b>.
ANZ 99.9% is HISTORICAL Mobility work. Do not invent a LeetCode rating.
</div>

---

## 0. General tips (say these to yourself before the loop)

Adapted from the awesome-behavioral-interviews tip list; keep them short.

1. **STAR every behavioral.** Situation → Task → Action (you, not "we") → Result (number + tag) → one-line Lesson.
2. **Listen, then answer the question asked.** If unclear: "Do you want a technical deep dive or a leadership story?"
3. **Be concise.** 60–90 seconds. Stop after the number.
4. **It is OK to take 5 seconds.** Say "Let me pick the strongest example."
5. **No trash talk.** Past employers, managers, teammates — frame friction as disagreement between competent people.
6. **Failures end in process.** Story 5 and story 10 already do this — reuse that shape.
7. **If you do not have the experience:** "I have not lived that exact case. Here is how I would handle it, grounded in a related story." Do not invent.
8. **Balance "I" and the team.** Lead with your ownership, credit the people you led/mentored.
9. **Ask clarifying questions** on ambiguous prompts (especially system-design-flavored behavioral).
10. **Prepare reverse questions.** Section 4 below — pick three per company.

---

## 1. Coverage matrix — ~43 common questions → your stories

Story numbers = the bank in `07_behavioral_star_stories.md`.
**G** = short gap answer written in §2 (not one of the original 10).
**H** = honesty / "how I would" — no fabricated STAR.

| # | Question | Use | Notes |
|---|---|---|---|
| 1 | Tell me about yourself | **G1** | 60–90s walkthrough |
| 2 | Disagreement with manager / senior | **1** or **7** | CH verdict or ORM rulebook |
| 3 | Conflict with a teammate | **7** (or **1**) | Technical disagreement, not personal |
| 4 | Tell me about a time you failed | **5** or **10** | Prefer 5 (refactor) or 10 (near-miss) |
| 5 | Led a team — outcome | **8** + FRM led-3 | Masters + FRM design reviews |
| 6 | Worked well under pressure | **8** | GST deadline windows |
| 7 | Difficult decision | **1** or **3** | CH split decision / validator |
| 8 | Above and beyond | **2** or **9** | Freshness as a feature / anti-bot loop |
| 9 | Don't know the answer | **G2** | Honest + research loop |
| 10 | Received tough / critical feedback | **G3** | Coverage CI failure → learning |
| 11 | Gave someone difficult feedback | **G4** | Mentorship at Masters |
| 12 | Prioritize tasks quickly | **G5** | Menu bug vs feature / Masters peak |
| 13 | Anticipated problems / prevention | **2** or **3** or **10** | Freshness / validator / idempotency |
| 14 | Difficult customer / stakeholder | **G6** | PwC-facing FRM releases |
| 15 | Missed a deadline | **G7** | Honest near-miss + communication |
| 16 | Heavy workload | **8** + **G5** | Short-staffed Masters peak framing |
| 17 | Significant change at work | **G8** | Monolith→microservices / agentic rebuild |
| 18 | Took initiative without being asked | **1** or **2** | CH PoC / BQ→CH lane |
| 19 | Conflict within the team (mediator) | **1** | Two expert camps |
| 20 | Out of your comfort zone | **G8** / **4** | Agentic ownership / workflow inversion |
| 21 | Delivered under a tight deadline | **8** | Same as pressure |
| 22 | Big risk that failed | **5** (small) or **H** | Do not invent a catastrophic failure |
| 23 | Design/test for diversity & inclusion | **H** | No product-DEI ownership — approach only |
| 24 | Explain technical to non-technical | **G9** | Materiality / clustering to planners |
| 25 | Disagreed with a colleague | **7** or **1** | Same pool |
| 26 | Collaborate with another department | **G6** / FRM | Finance + PwC + eng |
| 27 | Complex technical project | Menu or **4** / **8** | Pick one; do not merge Kafka stories |
| 28 | Stay up-to-date with tech | **G10** | Real habits only |
| 29 | Why this company? | `38` §2.2 + intros templates | Never improvise cold |
| 30 | Biggest technical challenge | Menu or **3** | Adversarial + LLM gate, or validator |
| 31 | Why leave / change company? | `38` §2.1 | Positive framing |
| 32 | Many possible solutions — how choose? | **1** | Evidence gates |
| 33 | Motivate / encourage collaboration | FRM led-3 + Masters mentored-2 | With story **8** |
| 34 | Enhance technical knowledge | **G10** | Same as 28 |
| 35 | Assigned a task you don't know | **G2** | Same shape |
| 36 | Urgent + long-term at once | **G5** | Explicit priority rule |
| 37 | Hard time working with someone | **7** | Keep it technical |
| 38 | Project that didn't go to plan | **5** or Menu anti-bot early misses | Process fix |
| 39 | Something new you learned recently | **G10** + ClickHouse / LangGraph | Concrete |
| 40 | Decision without all information | **1** or **G11** | Explicit assumptions |
| 41 | Linked two problems → underlying issue | **6** or **10** | Coverage lie / idempotency class |
| 42 | Sacrifice short-term for long-term | **G12** | Strangler sequencing / CH gates |
| 43 | Friday prod deploy ask (ethics) | **G13** | Never hero-deploy |

**Amazon LP quick map:** Ownership→2,8 · Dive Deep→1,6 · Deliver Results→8 · Bias for Action→8,9 · Earn Trust→5,10 · Have Backbone→1,7 · Invent & Simplify→2,4 · Insist on Highest Standards→3,5 · Customer Obsession→3,4 · Think Big→4 · Learn & Be Curious→6,9 · Hire & Develop→mentorship narrative.

**Googliness:** humility→1,5 · ambiguity→1,4 · collaboration→7, mentorship · bias to action→2,8 · doing the right thing→10.

---

## 2. Gap answers (Tarun-specific — memorize these)

Stack on this track: FRM = **Spring Boot / MySQL** · AssortSmart writes = **Go / Gin** · agent plane = **Python FastAPI + LangGraph** · Masters migration = **Spring Boot strangler**.

### G1. Tell me about yourself (60–90s)

"I'm Tarun Mittal, a Senior Software Engineer with 5 years designing and owning cloud-native distributed systems in **Java, Python and Go**. Chronologically: GeeksforGeeks backend reliability → Masters India, where I led a **Spring Boot strangler** and a Kafka e-invoicing path to 1M+ submissions a day → Uber via EPAM, where I owned the FRM Risk Scoping backend (30+ APIs, 8 screens, $340M materiality, led 3) and Uber Eats menu ingestion end to end (from 24 hours to 2 hours, $600K+/yr) → Impact Analytics, where I build AssortSmart Keep/Drop and dig-deeper QnA (**FastAPI, LangGraph, MCP**, write APIs in **Go / Gin**) and drove ClickHouse adoption with a measured 250M-row POC. I want a senior role where I keep owning systems end to end, with a stronger design-review bar."

Stop. Do not append hobbies unless asked.

### G2. Don't know the answer / task you've never done

"I say I don't know, then I show the loop. Example shape: in a client or design review, if I'm asked about a technology I haven't used in production, I acknowledge it, outline how I'll get the answer — docs, a spike, a teammate who has done it — and commit to a follow-up time. I do not bluff. Related: when ClickHouse was new to parts of the org, I didn't argue taste — I ran a row-identical POC and let 189s→12.3s decide."

### G3. Received tough / critical feedback

"Use the coverage story (story 6) framed as feedback: CI failed me at 34.6% on an ORM migration even though I thought the paths were tested. The tough part was realizing my mental model of coverage was wrong — mocks had shifted execution away from the model layer. I asked for the specific concern, wrote 12 direct model-layer tests including rejection paths, and wrote the pattern into the team's testing notes. Result: 100% on the changed module. Lesson: a metric you don't understand will lie to you."

### G4. Gave someone difficult feedback

"At Masters India I mentored 2 engineers. One shipped working endpoints with almost no tests around the tax/dedup rules. In a 1:1 I led with what was strong, then showed a concrete failure mode a missing test would miss, paired on the first test, and set a CI coverage gate on changed modules so it wasn't personal taste. They presented the next slice themselves in review. Tone: growth, not gotcha."

### G5. Prioritize quickly / urgent + long-term

"Rule I use: customer-visible correctness and deadline-window risk beat feature work. At Masters during GST peaks I froze cutovers in deadline weeks and kept long-term strangler work on non-peak days. On Menu, a production ingest block outranks a parser tidy-up. I say the priority out loud to the lead, time-box the urgent fix, then return to the long-term thread with mini-deadlines."

### G6. Difficult customer / stakeholder (PwC-facing)

"FRM releases were PwC-facing. Ambiguity in 'in scope' was expensive. I encoded materiality, qualitative override, residual risk, and the 5% component threshold as explicit rules against $340M / $170M thresholds so the system could reproduce and audit a decision. Weekly clarity with finance stakeholders beat arguing in a spreadsheet. Result: platform of 30+ APIs / 8 screens; the 70% reconciliation cut remains a TARGET."

### G7. Missed a deadline

"I do not have a dramatic missed-deadline story with customer damage. Closest honest shape: when anti-bot defenses rotated on Menu sources, ingest success dipped and a planned parser improvement slipped. I flagged the slip early, explained the adversarial cause, proposed a contingency (protect the critical path first, defer nice-to-haves), and instrumented block-rate into the same dashboards as parse failures. We recovered to 95%+ successful ingestions. Lesson: surface the miss early with a revised plan — silence is the real failure."

If pressed for a harder miss: use story 5 (refactor regression caught in CI before release) and be explicit it did **not** ship broken.

### G8. Significant change / comfort zone

"Two real ones. (1) Masters: PHP monolith → **Spring Boot strangler** + Kafka under live filing traffic — I had to learn the strangler sequencing, not just the target architecture. (2) Impact Analytics: owning an agentic rebuild (LangGraph / MCP / RAG) when my prior strength was classical backends — I stayed in the comfort of APIs for the write plane (**Go / Gin**) and stretched on the agent plane with explicit human gates and offline eval. Lesson: change the workflow and the measurement first; the model second."

### G9. Explain technical to non-technical

"Pick the audience. To a finance stakeholder on FRM: 'materiality' as a dollar threshold that decides whether a line item is in scope for the audit, with an override path that is logged. To a retail planner on clustering: 'we evaluate ~100 ways to group stores and show you the top 3 with why, including one that mimics how you used to do it — you still approve before anything writes back.' No jargon without a one-line translation."

### G10. Stay up-to-date / something new learned

"Concrete, not vague: ClickHouse mutation limits and why insert-only planning stores win; LangGraph / MCP tool-calling patterns with schema gates; Flink keyed dedupe vs micro-batching for Menu. Habits: read the primary docs and one postmortem/blog for a new system before proposing it; spike with a measurable PoC before arguing in a design review. Recently: the line-planning schema lesson — choice×cluster×week (~25M) beat a flat store-week projection (~12B). The lever was the schema, not the engine."

### G11. Decision without all information

"Story 1 shape: both CH camps had partial evidence. I wrote the assumptions down, accepted every measured fact, and proposed gated experiments instead of a one-shot decision. If a gate failed, we would stop. That is how you decide under incomplete information without gambling the company."

### G12. Sacrifice short-term for long-term

"Strangler sequencing at Masters: shadow reads and bulk Kafka paths before interactive filing, freeze cutovers in deadline weeks — slower short-term delivery, zero deadline-window outage. Same idea on CH: BigQuery fixes and Postgres discipline before a full cutover, so we did not burn a quarter on the wrong store."

### G13. Friday afternoon prod deploy ask

"I would not develop and deploy a change to production alone on a Friday afternoon without review. Course of action: clarify severity (is it a Sev-1 customer outage?). If yes — incident process, pair if possible, minimal fix, feature flag / quick rollback, postmortem. If no — schedule for Monday with a design note and a reviewer. Hero deploys without a rollback plan are how you create weekend incidents. Earn Trust > looking helpful."

### H. Diversity & inclusion product design (no fabricated STAR)

"I have not owned a formal product-DEI workstream, so I will not invent one. How I would approach a design/test question: define who is excluded by the current flow (language, device, accessibility, data bias in rankings), add explicit test cases and eval slices for those groups, keep a human review path for low-confidence model output (we already do this on Menu schema gates), and measure quality per cohort — not only global averages. Related muscle: Menu multilingual menus + human review for low-confidence extractions; clustering always includes a baseline scenario so we do not silently drop a client's legacy configuration."

---

## 3. Rapid reuse cheat sheet

| Signal they want | Open with |
|---|---|
| Ownership | FRM led-3 / Menu end-to-end / Copilot architecture |
| Dive Deep | Story 6 coverage / Story 1 assumptions |
| Bias for Action | Story 8 sequencing / Story 9 experiment loop |
| Earn Trust | Story 10 near-miss / G13 Friday deploy |
| Customer Obsession | Story 4 workflow inversion / G6 PwC |
| Humility | Story 5 / Story 1 |
| Ambiguity | Story 1 / Story 4 / G11 |

Never tell the same story twice in one loop. Never merge Masters Kafka with Menu Kafka.

---

## 4. Questions to ask them (pick 3)

Expanded from the awesome-behavioral-interviews reverse-question list; prefer culture/engineering over flattery.

1. What does the design review process look like before code gets written?
2. Where does this team's on-call pain actually come from right now?
3. Which decision in the last six months would you make differently?
4. How do you tell a senior engineer from a staff engineer here — what changes?
5. If I join, what should be measurably better in six months because I was here?
6. What is the biggest piece of technical debt you are deliberately living with, and why?
7. What is the ratio of developers to testers / PMs, and how does planning actually happen?
8. What is the onboarding process for this role in the first 30/60/90 days?
9. What has changed in the org since you joined?
10. What are the most exciting projects on this team in the next two quarters?
11. How does project planning and prioritization work when urgent work lands mid-sprint?
12. What opportunities are there here to go deep on scalability / data platforms?
13. Can you describe a typical day for someone in this role?
14. What type of person usually does well here — and who struggles?
15. What challenges is the company facing that this team is expected to help with?
16. What do you personally like most about working here?

---

## 5. Delivery rules (again)

- Lead with the outcome, then the mechanism.
- Tag every number: MEASURED / TARGET / HISTORICAL / DESIGN / ESTIMATED.
- One story, one owner. Building stays building.
- Stop talking after the number.
