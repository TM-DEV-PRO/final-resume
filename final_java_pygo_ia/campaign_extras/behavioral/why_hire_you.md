# Why Should We Hire You? / What Work Have You Done?

<div class="callout note">
<b>How to use this page</b>
<ul>
<li>It covers the pitch questions: "why should we hire you", "what work have you done", "why you over someone with more years", "what's your biggest risk", and the objections interviewers raise.</li>
<li>Read it before recruiter screens and hiring-manager rounds, and again before the final round.</li>
<li>Memorise the 30-second pitch. For everything else, memorise the first sentence and the honest caveat.</li>
<li>Each answer uses at most three numbers. The full number list lives in <a href="../interview_prep/numbers_defense.md">Numbers defense</a>.</li>
</ul>
</div>

**Track:** Final Java + AI (IA = Py/Go), resume `Tarun_Mittal_SSE_5yr_Java_PyGo_AI.pdf`. Uber FRM and Masters India are Java with Spring Boot. Impact Analytics is Go with Gin plus Python agents. Full pitch bank: [`38_why_hire_tarun_qa.md`](../../prep/38_why_hire_tarun_qa.md). Question bank: [`39_behavioral_question_bank.md`](../../prep/39_behavioral_question_bank.md).

**The three things you are selling.** Every answer on this page comes back to these:

1. **Ownership.** I take a system from design to production and keep it running.
2. **Measurement.** I decide with benchmarks, not opinions.
3. **Honesty about AI.** I put hard release gates in front of AI features and I don't inflate the results.

**Words used below:**

- **Release gate (CI gate)** is an automated check that blocks a change from shipping unless it passes. CI (continuous integration) runs these checks on every code change.
- **Deterministic baseline** is a plain rule-based scorer with no AI. It gives the same answer every time, and AI has to beat it to be worth using.
- **Materiality threshold** is the money amount above which an accounting error is big enough to matter to auditors.
- **ClickHouse** is a database built for fast analytics on very large tables.

---

## 1. Why should we hire you?

### Short (30 to 45 seconds)

> You should hire me because I own backend systems end to end and I can defend every number I give you. I have five years in Java, Python and Go. At Uber, through EPAM, I owned a Java Spring Boot Finance risk backend that cut quarterly reconciliation from 14 days to 3 days. On Uber Eats, the menu pipeline I architected cut restaurant onboarding from 24 hours to 2 hours. Now at Impact Analytics I own the Go platform and the AI decision engine for a retail planning product. I bring architecture ownership, production discipline, and honest quality gates on AI.

**Numbers used:** 14 to 3 days, 24 to 2 hours. Two is enough here.

### Long (90 to 120 seconds)

> You should hire me if you need a senior backend engineer who owns a system from design through production, and who can connect classic infrastructure with applied AI.
>
> At Uber, through EPAM, I owned the FRM scoping backend. FRM is the Finance team that decides which accounts need audit attention. I moved their process off Google Sheets into a proper MySQL database, designed the schema so many people could edit safely at once, and led 3 engineers through a database-layer migration. The quarterly reconciliation went from 14 days to 3 days.
>
> On Uber Eats I owned menu ingestion. That's turning restaurant menus, including messy multilingual PDFs, into Uber's catalog format, using Kafka and Flink for the streaming part and an LLM with retrieval for the PDFs.
>
> At Masters India I led a move from a PHP monolith to Spring Boot microservices, one endpoint at a time, and mentored 2 engineers.
>
> At Impact Analytics I own two things: a Go platform that serves retail planners at peak load, and an AI engine that recommends which products to keep or drop. The AI never queries the big database directly. It gets prepared data, and if it times out we fall back to the rule-based score. Every new model must pass an 80% accuracy gate before release. When the AI did worse than our rule-based baseline, we kept the baseline weights instead of shipping it.
>
> So you get ownership, measurement, and someone who won't oversell an AI result.

**Numbers used:** 14 to 3 days, led 3, 80% gate. The "mentored 2" is a headcount, not a result. Keep it separate from "led 3".

**Follow-up they may ask:** "Is the 80% live accuracy?" Answer: "No. It's the bar a model has to clear on a fixed 300-case test set before it can be promoted. It's a release gate, not a claim about every customer in production."

---

## 2. What work have you done?

### Short (one breath per job)

> At Impact Analytics I own the Go platform, the ClickHouse analytics layer and the AI decision engine for retail planning. At Uber through EPAM, I owned the Finance risk backend and the Uber Eats menu ingestion pipeline on Kafka and Flink. At Masters India I built the bulk GST e-invoicing pipeline on Kafka and led a PHP-to-Spring Boot migration. At GeeksforGeeks I moved the doubt-support platform from PHP to Django.

### Long (walk it chronologically)

Go oldest to newest. For each job give one sentence of context, one thing you owned, and one result. Then end with what you want next.

1. **GeeksforGeeks (SDE).** Moved the doubt-support platform to Django so it survived 10x traffic spikes during live coding contests.
2. **Masters India (SDE 2).** Led the PHP to Spring Boot migration and built the Kafka pipeline for over a million government submissions a day.
3. **Uber via EPAM (SDE 2).** Owned the FRM scoping backend and architected the Uber Eats menu ingestion pipeline.
4. **Impact Analytics (Senior SWE).** Owns AssortSmart's Go platform, ClickHouse layer and AI decision engine.
5. **Close:** "Next I want a senior backend or platform role, ideally with applied AI at scale, where I own a domain for several years."

---

## 3. Why you over someone with more years?

> Scope, not years. I've owned a Finance system that auditors relied on against a $340 million materiality threshold. I've run a pipeline doing over a million government submissions a day. And I own a platform with a 2.11-billion-row analytics table behind it. I've also led a small team and mentored juniors. To be clear about my limits: I haven't run a 50-person org and I haven't operated Kubernetes clusters myself. But for owning a system end to end, I've done it at real stakes.

**Numbers used:** $340M, a million a day, 2.11 billion rows.

---

## 4. What's the biggest risk in hiring you?

The honest answer turns a risk into a credibility point.

> Probably that some of my AI work is new. "Ask Iris", the planner copilot, is shipped as a capability, but I don't have long-term usage numbers to show you. And the 80% on my resume is a release gate, not proof that every customer sees 80%. Some of my other AI work, like a store-clustering copilot, is design and build work that isn't on the resume. Where I'm strongest is the systems that have run in production for a long time: the Uber Finance backend, the Uber Eats menu pipeline, and the Masters India e-invoicing pipeline.

---

## 5. Your differentiators (pick one per answer)

| What I can claim | Proof | Status |
|---|---|---|
| Finance-grade backend | Uber FRM: 36 Spring Boot endpoints, $340M materiality, led 3, module coverage 100% | PDF |
| Real money saved | Uber Eats menu: 24 hours to 2 hours, $600K a year | HISTORICAL |
| Scale | Masters India: 1M+ submissions a day. Impact Analytics: 10k peak requests per second, 2.11B-row table | PDF / HISTORICAL |
| Decisions backed by benchmarks | Planner pivots from 189 seconds to 12 seconds on a 250M-row test | MEASURED |
| Safe AI | LLM fed prepared JSON, not database access. 300-case test set, 80% release gate. Weights frozen when AI lost to the 74% baseline | PDF |
| People | Led 3 at Uber via EPAM. Mentored 2 at Masters | PDF |

**Tags in this table:** MEASURED means there's a benchmark, log or doc behind it. HISTORICAL means it comes from past work records and wasn't re-measured. PDF means it's a resume bullet you can defend as written.

---

## 6. Objection handling

Each answer is short on purpose. Say it, then stop.

**"Your AI isn't really in production."**
> Ask Iris is shipped as a capability for planners. The 80% line is a release gate for promoting models. The clustering copilot is separate design and build work, and I don't claim it on the resume.

**"No Spark?"**
> Correct. My streaming work was Kafka and Flink on Uber Eats. Spark isn't on my resume.

**"Have you run Kubernetes?"**
> I've deployed and consumed containerised services. I haven't operated Kubernetes clusters or written the infrastructure code for them.

**"Uber through a vendor?"**
> Yes, I was an EPAM employee embedded full time in an Uber team. I worked in Uber's codebase and owned the FRM scoping backend design.

**"Is 70% on reconciliation real?"**
> Yes. Reconciliation went from 14 days to 3 days. The technical design doc framed that cut, and that's what the platform delivered for the close. The value came from automating the financial math and the account hierarchy, which used to be done by hand in Sheets.

**"98% on menus, really?"**
> That's 98% field accuracy on an offline evaluation set, meaning a fixed set of menus with known correct answers.

**"10k RPS, what's the latency?"**
> 10k requests per second is the peak load the platform is built for. I don't quote a latency SLA for it.

**"You've only been at Impact Analytics a few months."**
> I joined for the platform and AI ownership, and I shipped real things there. I'm not job-hopping every year. The longest stretch on my resume shows I stay when the scope keeps growing.

**"Is 99.9% compliance from Uber Eats?"**
> No, that was a separate Uber Mobility project in Australia and New Zealand. It automated driver and vehicle document checks. It's historical work.

---

## 7. Questions to ask them at the end

- "How does design review work here before code gets written?"
- "What's the biggest on-call pain right now?"
- "What's a technical decision the team would reverse if it could?"
- "What separates senior from staff here?"
- "What would a great first six months look like, in measurable terms?"
- "Where is the team carrying deliberate technical debt?"

---

## 8. Delivery rules

- Lead with the outcome, then explain how.
- Say "Uber via EPAM" once, early.
- Uber Eats Kafka and Masters India Kafka are different products. Never blend them.
- Stop after the number. Let them ask the follow-up.
- If a number isn't on the PDF (100% Go coverage, 1,200+ Go tests, $100 per run token cost, the 1.6M catalog size), say "that's not on the resume, but" before giving it.

**Verbal only, not on PDF:** the Cluster Recommendation Copilot and Hindsight. Offer them only if they ask about a broader AI roadmap.

Related: [Intros](intros_short_long.md) · [STAR bank](star_bank.md) · [Company guides](company_behavior_guides.md)
