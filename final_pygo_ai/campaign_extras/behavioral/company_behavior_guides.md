# Company Behavior Guides (beyond Amazon and Google)

<div class="callout note">
<b>How to use this page</b>
<ul>
<li>For each company it explains, in plain words, what their values mean and what interviewers are listening for. Then it says which of your stories fit and how to open them.</li>
<li>Read the section for a company the day before its behavioral round, together with the <a href="star_bank.md">STAR bank</a>.</li>
<li>Memorise your 2 or 3 chosen stories for that company and the one-line opener for each.</li>
<li>Never reuse the same story twice in one interview loop.</li>
</ul>
</div>

> **Full question bank and prep grid:** [`39_behavioral_question_bank.md`](../../prep/39_behavioral_question_bank.md) · [`40_behavioral_prep_grid.md`](../../prep/40_behavioral_prep_grid.md) (adapted from [awesome-behavioral-interviews](https://github.com/ashishps1/awesome-behavioral-interviews). The answers are Tarun-specific).

## Your story list (numbers match the STAR bank)

| # | Story in one line | Status |
|---|---|---|
| 1 | Resolved a ClickHouse yes-or-no split between two expert camps with a staged, measurable plan | Verbal context for PDF work |
| 2 | Designed a BigQuery to ClickHouse lane where freshness is checked and printed on every answer | Design, verbal |
| 3 | Put a strict validator around an LLM planner. Structural correctness went from 0.54 to 0.99 offline | Verbal, not on PDF |
| 4 | Flipped the store-clustering workflow so the agent proposes and the human approves | Verbal, not on PDF |
| 5 | Caught and owned a behaviour change I had hidden inside a "pure refactor" | Uber FRM |
| 6 | Found that mocks were hiding real coverage. Fixed it with model-layer tests | Uber FRM |
| 7 | Disagreed with a written architecture rule, got a documented exception, then committed | Uber FRM |
| 8 | Led the Masters India monolith migration with no outage during filing deadlines | Masters |
| 9 | Beat changing anti-bot defences with a measurement loop | Uber Menu |
| 10 | Reported a double-filing near-miss and fixed it across the whole pipeline | Masters |
| 11 | Debugged a connection-leak out-of-memory in an async worker | Packet, not on PDF |
| 12 | Wrote the ClickHouse RFC and PoC. Pivots went from 189 seconds to 12 seconds | IA |
| 12b | Fixed a 170 GB out-of-memory by slicing loads into one-week chunks | IA |
| L1 | Led 3 engineers at Uber via EPAM | Uber FRM |
| L2 | Mentored 2 engineers at Masters India | Masters |

**How to pick.** Choose stories from different employers. Mix at least one story about a mistake or disagreement with one story about delivering a result. Prefer PDF-backed stories. Use verbal-only stories (2, 3, 4) only when the question is clearly about AI product thinking.

---

## Amazon

**What they value, in plain words.** Amazon interviews are built around its Leadership Principles, usually called LPs. Every behavioral question maps to one or two LPs, and interviewers score you against them. They want specifics: your personal actions, real numbers, and what you'd do differently. Vague "we did it" answers score badly.

The LPs that matter most for you:

- **Ownership.** Act like an owner of the whole outcome, not just your ticket. Fix things beyond your job description.
- **Dive Deep.** Know the details. Be able to explain where a number came from and audit it yourself.
- **Deliver Results.** Ship the important thing on time, even when it's hard.
- **Bias for Action.** Move quickly when a decision can be reversed. Don't wait for perfect information.
- **Earn Trust.** Admit mistakes openly, listen, and treat others' views with respect.
- **Have Backbone; Disagree and Commit.** Push back with evidence when you disagree. Once a decision is made, commit fully.
- **Hire and Develop the Best.** Raise the people around you.
- **Insist on the Highest Standards.** Keep the quality bar high even when others would accept less.

**Stories that fit.**

| LP | Story | Why it fits |
|---|---|---|
| Ownership | L1 (led 3 on FRM) or 8 (Masters migration) | You owned the outcome end to end |
| Dive Deep | 6 (coverage that lied) or 12b (170 GB out-of-memory) | You found the real mechanism behind a misleading signal |
| Deliver Results | 8 (Masters migration) | No outage during deadline windows while 1,500+ clients kept filing |
| Bias for Action | 12 (ClickHouse RFC and PoC) | You measured quickly instead of debating |
| Earn Trust | 10 (near-miss) or 5 (refactor mistake) | You surfaced problems you could have hidden |
| Have Backbone | 7 (rulebook) or 1 (ClickHouse camps) | You disagreed with a rationale and then committed |
| Hire and Develop | L2 (mentored 2) | You got juniors shipping on their own |

**Opener you can use.** "The clearest example of ownership I have is the Masters India migration, where we couldn't pause the business for a single deadline."

**Watch out.** Amazon will push for your personal role. Say "I" for your actions. If they ask "what would you do differently", have one honest answer ready per story.

---

## Google

**What they value, in plain words.** Google looks for "Googleyness" alongside leadership. Googleyness is a mix of traits: intellectual humility (you can change your mind when shown better evidence), comfort with ambiguity (you make progress when the problem is fuzzy), collaboration (you work well across teams), bias to action, and doing the right thing for users. They also look for "emergent leadership", which means stepping up to lead when it's needed, even without a title.

**Stories that fit.**

| Signal | Story | Why it fits |
|---|---|---|
| Intellectual humility | 1 (ClickHouse camps) | You accepted the other side's facts and changed the question |
| Ambiguity | 4 (clustering inversion) or 1 | The right answer wasn't obvious and you made it concrete |
| Problem-first thinking | 3 (malformed-plan validator) | You wrapped an unreliable LLM in a deterministic contract |
| Doing the right thing | 10 (near-miss) | You reported something nobody would have noticed |

**Opener you can use.** "One time I learned the most was when two expert groups disagreed about ClickHouse, and both had real evidence."

**Watch out.** Stories 3 and 4 are not resume bullets. If you use them, say "this is design and build work beyond my resume" when asked. Google interviewers also like hearing what you'd do differently, so prepare one improvement per story.

---

## Microsoft

**What they value, in plain words.** Microsoft's culture centres on **growth mindset**: treating mistakes as learning and staying curious instead of acting like a know-it-all. They also emphasise **customer obsession** (understanding what the user actually needs), **inclusive collaboration** (working well with diverse people and teams), and **delivering results**.

**Stories that fit.**

| Value | Story | Why it fits |
|---|---|---|
| Growth mindset | 9 (anti-bot loop) or 6 (coverage) | You learned your way through a problem you didn't understand at first |
| Learning from mistakes | 5 (refactor mistake) | You owned it and turned it into a team checklist |
| Collaboration and mentoring | L2 (mentored 2) | You helped others grow instead of doing it all yourself |

**Opener you can use.** "A good example of learning my way through a problem is the Uber Eats scrapers, where the websites kept changing their bot defences."

**Watch out.** Don't present yourself as having all the answers. Microsoft responds well to "here's what I got wrong first".

---

## LinkedIn

**What they value, in plain words.** LinkedIn interviewers tend to probe three themes. The first is **transformation**: have you changed how a system or team works, not just added features? The second is **craft**: do you care about doing the work well, with quality and measurement? The third is **collaboration**: do you build good working relationships and give honest, constructive feedback?

**Stories that fit.**

| Theme | Story | Why it fits |
|---|---|---|
| Transformation | 8 (Masters migration) | You moved a monolith to services and changed how the team shipped |
| Scale and data craft | 12 (ClickHouse RFC) | You chose a database by benchmark and built a summary layer |
| Quality craft | Uber Eats menu pipeline (see story 9 and the menu numbers) | 98% field accuracy on an offline evaluation, behind a schema check |

**Opener you can use.** "The project that changed how my team worked the most was the Masters India migration from a PHP monolith to FastAPI."

**Watch out.** The 98% is an offline-evaluation number, measured on a fixed set of menus with known correct answers. Say "offline".

---

## Apple

**What they value, in plain words.** Apple doesn't publish an interview value list the way Amazon does. Interviewers consistently look for **quality and attention to detail** (sweating small things users would notice), **privacy and data protection**, and **deep ownership**. Apple uses the idea of a DRI (directly responsible individual), the one person accountable for a thing.

**Stories that fit.**

| Theme | Story | Why it fits |
|---|---|---|
| Attention to detail | 7 (column-aliasing bug) | A tiny SQL naming issue silently mapped rows to the wrong id, and you made it impossible |
| Quality bar | 6 (coverage) | You refused to accept a misleading metric |
| Data protection | Ask Iris scope lock (see design doc) | Each copilot session is locked to the user's allowed data when it connects |
| Correctness for auditors | FRM audit trail | Deterministic SHA-256 keys stop duplicate rows across quarters |

**Opener you can use.** "The bug I'm proudest of finding at Uber was invisible: rows silently mapped to the wrong id because two joined tables had the same column names."

**Watch out.** Older prep mentioned "100% schema" for the menu pipeline. That refers to a schema validation check that rejects malformed output. It is not on the PDF. Lead with the 98% offline field accuracy.

---

## Netflix

**What they value, in plain words.** Netflix's culture is "freedom and responsibility". You get a lot of autonomy, and in return you're expected to use good judgment without being supervised. "Context, not control" means leaders explain the why and trust you to decide. **Candor** means giving and receiving direct, honest feedback, including admitting your own mistakes plainly.

**Stories that fit.**

| Value | Story | Why it fits |
|---|---|---|
| High agency | 9 (anti-bot loop) | You ran your own experiment loop without waiting for instructions |
| Candor about mistakes | 5 (refactor mistake) | You called your own foul fast |
| Owning production | 10 (near-miss) or the Masters on-call experience | You treated a near-miss as your problem |

**Opener you can use.** "I'll give you one where I was the one who made the mistake, because I think how you handle that says a lot."

**Watch out.** Netflix values judgment over process. Don't over-explain checklists. Explain the decision and why it was right.

---

## Atlassian

**What they value, in plain words.** Atlassian's values include "Open company, no bullshit" (be transparent and direct), "Play, as a team" (help others succeed), "Build with heart and balance" (care about the work and the people), "Don't #@!% the customer" (protect the customer), and "Be the change you seek" (improve things yourself instead of complaining).

**Stories that fit.**

| Value | Story | Why it fits |
|---|---|---|
| Play, as a team | L1 (led 3) | You split ownership and stepped back as people grew |
| Open company, no bullshit | 7 (rulebook disagreement) | You disagreed openly in writing and documented the outcome |
| Be the change | 5 (refactor mistake) | You added a checklist rule so the team wouldn't repeat it |
| Don't hurt the customer | 10 (near-miss) | You protected clients from a compliance error |

**Opener you can use.** "When I led a pod of 3 at Uber via EPAM, the most important thing I did was give each person a clear area to own."

**Watch out.** "Led 3" was tech-lead work, not people management. Say "tech lead".

---

## Salesforce

**What they value, in plain words.** Salesforce's core values are **Trust** (customers trust you with their data, so security and reliability come first), **Customer Success**, **Innovation**, **Equality** and **Sustainability**. In engineering interviews, Trust and Customer Success come up most.

**Stories that fit.**

| Value | Story | Why it fits |
|---|---|---|
| Trust | 10 (idempotency near-miss) | You made duplicate government filings impossible |
| Trust in multi-tenant data | Impact Analytics tenant isolation | Each tenant sees only its own data across Postgres and ClickHouse |
| Customer success and audit | FRM for Finance and external auditors | Every scoping number became reproducible and traceable |
| Compliance | ANZ document checks | 99.9% compliance from a deterministic validation backend (historical Uber Mobility work) |

**Opener you can use.** "Trust for me is concrete. At Masters India I found a way our retries could have filed the same invoice twice with the government, and I closed it across the whole pipeline."

**Watch out.** ANZ is historical Uber Mobility work, not Uber Eats. Tenant isolation is access control, not encryption.

---

## Short mapping cheat sheet

| What they're testing | Best story | Backup |
|---|---|---|
| Disagreement | 1 | 7 |
| Ambiguity or product thinking | 4 (verbal) | 1 |
| Mistake or failure | 5 | 10 |
| Deadline or migration | 8 | 12 |
| Persistence | 9 | 12b |
| Compliance or trust | 10 | ANZ |
| Mentorship | L2 (mentored 2) | L1 (led 3) |
| Hardest technical problem | 12b | 3 (verbal) |
| Debugging | 6 | 11 (packet) |

## Honesty reminders for every company

- Say "Uber via EPAM" once.
- "Led 3" is Uber FRM. "Mentored 2" is Masters India. Never merge them.
- Ask Iris is a shipped capability. No invented usage or uptime numbers.
- The 80% is a release gate in CI, not live accuracy for every tenant.
- No Kafka, Flink or Kubernetes operations at Impact Analytics.
- The Cluster Recommendation Copilot and Hindsight are verbal only.

Related: [STAR bank](star_bank.md) · [Intros](intros_short_long.md) · [Why hire you](why_hire_you.md)
