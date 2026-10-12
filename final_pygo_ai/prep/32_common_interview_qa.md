# Common interview questions: filled answers (your experience)

<div class="callout note">
<b>How to use this page</b>
<ul>
<li>These are the classic HR and hiring-manager questions ("Tell me about yourself", "Greatest weakness", "Tell me about a conflict") with answers built from your real projects.</li>
<li>Read it before any behavioural or manager round. Practise each answer out loud. Each one should take 30 to 60 seconds.</li>
<li>Every answer follows the same shape: the direct answer first, then the reason, then a project example. Memorise the first sentence of each and the example you attach to it.</li>
<li>Start with "Technical terms in plain English" so you can explain any term an interviewer picks up on.</li>
</ul>
</div>

The format follows the "90 toughest interview questions" style: a numbered question, an answer, and sometimes a follow-up. Question 20 must be customised per employer.

**Tags used here.** MEASURED means there is a log, document or code behind the number. TARGET means a design goal, so say "targeting". ESTIMATED means arithmetic I can show. HISTORICAL means from my past work records. Full rules live in [`GROUND_TRUTH.md`](GROUND_TRUTH.md).

HTML: [`32_common_interview_qa.html`](32_common_interview_qa.html) · Hub: [`ApplicationKit.html`](../ApplicationKit.html)

---

## Technical terms in plain English

Behavioural answers still contain technical words, and a good interviewer will pick one and ask "what does that mean?" Each term below has a plain definition, a tiny example, and where it appears in my answers.

**p95 latency.** The response time that 95% of requests are faster than. If 100 requests take between 100ms and 2s, and the 95th-fastest took 300ms, the p95 is 300ms. It matters more than the average because it shows what slow users feel. *In my work:* Masters India p95 went from 1.2 seconds to 300 milliseconds.

**Strangler pattern.** A way to replace an old system piece by piece. New services take over one route at a time while the old system keeps serving the rest, until the old one can be switched off. *Example:* move `/invoice/validate` to the new service first and leave everything else on PHP. *In my work:* the Masters India PHP to FastAPI migration.

**Canary release.** Sending a small slice of real traffic, say 5%, to the new version first and watching errors before sending everyone. *In my work:* each migrated route at Masters India went out as a canary.

**Idempotency key.** A unique ID attached to an operation so that doing it twice has the same effect as doing it once. *Example:* if a client retries "register invoice 42" with the same key, the server returns the first result instead of registering it again. *In my work:* Masters India used client + file hash + batch index as the key.

**Dead-letter queue (DLQ).** A side queue for messages that keep failing, so they are parked for inspection instead of blocking everything behind them. *In my work:* Masters India IRP submissions that failed after bounded retries went to a DLQ.

**Optimistic locking.** Each row carries a version number. You read version 3, and your update only succeeds if the row is still version 3. If someone else saved first, your update fails and you retry with fresh data. *In my work:* Uber FRM review-status updates.

**ORM (Object-Relational Mapper).** A library that maps database tables to code objects, so you write `session.get(Account, id)` instead of raw SQL. *In my work:* the Uber FRM migration to SQLAlchemy 2.0.

**ReplacingMergeTree.** A ClickHouse table type where you never update a row in place. You insert a new version, and a background merge later keeps only the newest one. It is like a notebook where you write corrections below the old line and a cleaner crosses out old lines later. *In my work:* Impact Analytics AI decision writes.

**RAG (Retrieval-Augmented Generation).** Look up relevant reference material first, then hand it to the LLM with the question, so it answers from evidence. It is an open-book exam for the model. *In my work:* Uber Eats menu extraction with Gemini, LangChain and Milvus.

**CI gate.** An automatic check in the build pipeline that blocks a change if a score is below a bar. *In my work:* the 80% accuracy gate on the 300-case harness for AssortSmart AI changes.

**SOX and materiality.** SOX (Sarbanes-Oxley) is the US law that requires companies to prove their financial reporting controls work. Materiality is the size threshold above which an error would matter to investors. *In my work:* Uber FRM scoped accounts against a $340M materiality threshold.

---

**1. Tell me about yourself.**

**Answer:**
I'm a Senior Software Engineer with about five years building backend and data platforms in Python and Go. Right now at Impact Analytics I own the AssortSmart platform: a Go/Gin service that peaks at 10k requests per second, ClickHouse rollups that cut planner pivots from 189 seconds to 12 seconds, and an AI decision engine that scores 348k article-seasons, plus a shipped copilot called Ask Iris. Before that, at Uber via EPAM, I owned the Finance risk scoping backend (FastAPI and MySQL, 36 endpoints) that cut quarterly reconciliation from 14 days to 3 days, and I worked on Uber Eats menu automation that cut restaurant onboarding from 24 hours to 2 hours and saves about $600K a year. At Masters India I led a PHP-to-FastAPI migration for 1,500+ clients that took p95 latency from 1.2 seconds to 300 milliseconds, and worked on a Kafka pipeline handling over a million government submissions a day. I started at GeeksforGeeks, moving their doubt-support backend to Django. The common thread is that I own systems end to end and I can defend every number I quote.

*Follow-up they may ask:* "Which of those are you proudest of?" Pick the one that matches the role (see [`08_role_targeting_and_rapid_fire.md`](08_role_targeting_and_rapid_fire.md)).

---

**2. Why should we hire you?**

**Answer:**
Because I bring design ownership, production discipline and mentoring, not just ticket delivery. At Uber via EPAM I owned the FRM backend design while leading 3 engineers, and the Eats menu work saves about $600K a year. At Masters India I led the FastAPI migration that raised throughput from 700 to 4,000 requests per minute, and I mentored 2 engineers through it. At Impact Analytics I own a Go/Gin edge at 10k peak RPS, a 15.5x faster pivot path in ClickHouse, and an AI engine that only promotes changes through an 80% CI gate. I'm also careful with claims: I'll tell you which numbers are measured, which are gates, and which are historical. One example of that care: Kafka and Flink on my profile belong to Uber Menu, not Impact Analytics, and I keep those stories separate.

---

**3. What is your greatest strength?**

**Answer:**
My greatest strength is turning messy production constraints into a clear system design and shipping it safely. I do my best work where correctness, latency and ownership collide. At Uber Finance, quarterly risk scoping still ran on Google Sheets, with no durable line IDs and no audit trail. I designed a layered FastAPI and MySQL backend, migrated 19M raw general ledger rows off Sheets, and owned the reconciliation v2 rewrite, an 18-file change that ran in parallel with the old Sheets version until Finance trusted it. I encoded the materiality logic ($340M materiality and $170M residual on the Q4 2025 close, with 5% significance thresholds) and the checks of HFM (Oracle Hyperion) data against the filed 10-Q. The result was reconciliation going from 14 days to 3 days. It shows I can work under audit pressure and think in both product and engineering terms.

*Follow-up they may ask:* "What was the hardest bug?" The column-aliasing bug: duplicate column names in a joined raw SQL query silently mapped rows to the wrong ID. I fixed it with aliased selects and explicit labels, and the later SQLAlchemy 2.0 migration removed that class of bug.

---

**4. What is your greatest weakness?**

**Answer:**
I used to hold on to critical-path work too long instead of delegating early. Earlier in my career I took too many reconciliation and cutover tasks myself to "guarantee quality", and that slowed down mentoring. I changed the habit at Masters India and later at Uber via EPAM. Now I set the API contract, pair with a teammate on the first slice (the first canary or the first reconciliation screen), then step back and let them own it. Leading 3 engineers on the FRM ORM migration and mentoring 2 on the FastAPI migration forced me to practise that. Clear expectations and a steady review rhythm work better than doing everything myself.

---

**5. Tell me about a time you failed.**

**Answer:**
At Masters India, early in the PHP-to-FastAPI cutover, I set API timeouts too tight compared with the old PHP path. Some legitimate calls to the government Invoice Registration Portal took longer, so the first canary showed timeouts and put filing-day traffic at risk. I owned the mistake. I moved those calls to a fully asynchronous flow, where the API accepts the job, returns a "202 Accepted" response, and the client polls for progress. I aligned timeouts with how the portal really behaved and added idempotency keys, bounded retries and a dead-letter queue so failed calls could be replayed safely. The lesson stuck: for third-party compliance APIs, design for slow responses and safe retries from day one, not after the first scare.

*Follow-up they may ask:* "How did you know the timeouts were the problem?" The canary errors were timeouts on the government portal calls, which the old PHP path had tolerated with longer waits. Beyond that, keep the detail qualitative.

---

**6. Describe a time when you had to deal with a difficult team member.**

**Answer:**
I dealt with it by finding the cause before escalating. At Uber via EPAM on FRM, a teammate kept missing API contract and test gates, which blocked Finance-facing releases. I set up a one-on-one and learned they were overloaded across UI and backend spikes. We re-split ownership: I kept the schema and the reconciliation v2 critical path, and they owned a bounded set of screens and APIs with a clearer definition of done. I paired with them on the first pull request using our handler, service and repository layering. Delivery stabilised, CI stayed green, and we hit the quarterly release without damaging the relationship.

---

**7. Where do you see yourself in five years?**

**Answer:**
I see myself as a senior-to-staff backend or platform engineer who owns a multi-service domain end to end: design, reliability and mentoring. I want to keep deepening distributed systems, data platforms and production AI systems. That direction comes straight from my last few projects, where the hard part was always making something correct and safe at scale, not just making it work. I also want to help others ship safely behind clear contracts and quality gates, like the CI gate on our AI changes. I'm looking for a multi-year build where scope compounds, not a short hop.

---

**8. Why do you want to leave your current job?**

**Answer:**
I'm looking for a role whose day-to-day ownership matches a multi-year backend and platform charter. At Impact Analytics I have learned a lot, especially about ClickHouse at billions of rows, LangGraph agents, and how to evaluate AI safely before promoting it. What I want next is deeper production ownership of distributed systems and data platforms at scale, which this role offers. I'm closing my open work professionally and interviewing carefully for fit, not running away from anything.

*Follow-up they may ask:* "You joined in May 2026. Isn't that short?" Say it honestly: the work has been intense and productive, and I'm being selective. Do not criticise the employer. See [`13_behavioral_why_switch.md`](13_behavioral_why_switch.md).

---

**9. How do you handle pressure and stress?**

**Answer:**
I treat pressure as a signal to prioritise and communicate, not to panic. I break the work into milestones, protect the critical path, and keep stakeholders updated on risk. During Uber FRM quarterly close windows and Masters India GST filing spikes, I sequenced the reconciliation and portal work so the most important piece shipped first. I relied on observability (ELK logs, New Relic traces and CI gates) so we were not guessing under load. Time-boxing, a clear owner list, and honest status updates keep me calm.

---

**10. What motivates you?**

**Answer:**
Hard systems problems with real business or compliance impact motivate me. Examples: fixing a broken financial close, making filing-day government traffic safe, or building an AI engine that cannot silently write bad decisions. On that last one, every AssortSmart output row carries a config_hash, a fingerprint of the exact prompts and settings that produced it, so any decision can be traced. I like designing the trade-off, shipping it, and being able to defend the numbers afterwards. Teamwork matters too: mentoring engineers through a migration is as satisfying as the metric itself.

---

**11. How do you handle constructive criticism?**

**Answer:**
I treat it as a free design review. I listen, find the real failure mode, and change the system, not just the slide. At Impact Analytics, reviewers pushed on two things. First, whether the LLM should ever query ClickHouse directly. I agreed it should not, so the model only receives a prepared JSON payload and has no SQL tool. Second, whether our 80% number could be misread as live accuracy. I changed how we describe it: it is a CI promotion gate, not a claim that every tenant runs at 80%. That feedback made both the architecture and our reporting more honest.

---

**12. Tell me about a time you led a team.**

**Answer:**
I led a pod of 3 engineers at Uber via EPAM on the FRM scoping backend, as tech lead rather than people manager. I set the layered architecture (handler, service, repository), the API contracts and the design reviews, and I personally owned the reconciliation v2 migration. We delivered 36 endpoints behind 8 Finance screens, and I led the ORM migration to SQLAlchemy 2.0, which removed latent column-aliasing bugs and raised module statement coverage to 100%. We shipped with zero downtime using stacked Bazel pull requests, which are small dependent changes reviewed and merged in order. Separately, at Masters India, I mentored 2 engineers through the FastAPI migration with the same approach: pair first, then hand off.

*Follow-up they may ask:* "How many tests?" About 1,100+, but that is verbal, not on the PDF.

---

**13. Tell me about a time you disagreed with a technical decision.**

**Answer:**
I disagreed with using row-level updates in ClickHouse for planning data at Impact Analytics. ClickHouse mutations (in-place UPDATE or DELETE) rewrite whole data parts in the background and queue up, which makes them slow and unpredictable for interactive work. I pushed for insert-only writes with ReplacingMergeTree, where each change is a new row version and reads resolve the newest one. Planner pivots had been slow on PostgreSQL, and proof-of-concept comparisons showed ClickHouse winning on large analytical reads, while Postgres kept the thin metadata, user access and roles. I backed the design with measurement: a pre-aggregation layer took pivots from 189 seconds to 12 seconds on a 250-million-row benchmark harness. Presenting evidence rather than opinion is what made the decision stick.

---

**14. Tell me about a time you had to decide with incomplete information.**

**Answer:**
On Uber Eats menu ingestion, partner sites and anti-bot defences changed without notice, so we could never have a complete list of failure modes. Instead of waiting, I hardened the Selenium scraping fleet with dynamic proxy pools and adaptive retries, which raised extraction success to 95%+ from an estimated 60-65%. For unstructured PDF menus we kept a LangChain RAG path with Gemini 2.5 Pro over Milvus, with a strict schema check before anything reached the catalog. We decided with partial information by measuring the success rate and offline field fidelity (98% on the evaluation set) rather than freezing delivery. Measurement replaced certainty.

*Say this carefully:* older prep also cites 100% schema consistency offline. It is not on the PDF, so lead with 98% and always say "offline".

---

**15. What are you most proud of?**

**Answer:**
Two things, both about correctness under pressure. First, replacing a fragile Finance close on Google Sheets with a real FRM platform at Uber via EPAM, and owning reconciliation correctness under audit, which cut the cycle from 14 days to 3 days. Second, making bulk GST e-invoicing durable at Masters India with Kafka, PostgreSQL sharded by tax quarter, and idempotent retries, so a million-plus submissions a day never meant double-registering an invoice with the government. Both combined systems design with real accountability.

---

**16. Tell me about a time you went above and beyond.**

**Answer:**
At Uber Finance, reconciliation v2 was not "just another API" to me. I went beyond the ticket and validated HFM extracts against the public 10-Q filings, line by line. I tracked down a silent identity bug where duplicate column names in a joined query mapped rows to the wrong ID, and fixed it with explicit aliases. I also kept v1 running in parallel until Finance trusted v2. That protected the audit work papers and the quarterly close, which mattered more than shipping an endpoint.

---

**17. How do you handle conflict in the workplace?**

**Answer:**
I separate the people from the design argument and get everyone to agree on one success metric. At Masters India, the team split between a big-bang rewrite and a gradual cutover to FastAPI. I framed the debate around filing-day risk: what happens if the new system fails on the busiest day? That led us to a canary per endpoint behind the gateway, a shared database during the traffic move, and instant rollback. We chose the gradual migration, I mentored two engineers on the pattern, and we still took p95 latency from 1.2 seconds to 300 milliseconds.

---

**18. What is your leadership style?**

**Answer:**
Collaborative and standards-driven. I set the architecture and the quality bar (contracts, CI, observability) and then let people own their slices. On FRM I reviewed closely early on and stepped back once ownership stuck. At Masters India I paired on the first canary and then let the engineers I mentored take whole services. I adapt to risk: I stay more hands-on for compliance and audit paths and give more autonomy on well-bounded features.

---

**19. Tell me about a time you had to learn something new quickly.**

**Answer:**
When I joined Impact Analytics in May 2026 I had to ramp up fast on ClickHouse at billion-row scale and on LangGraph agents. I read the existing design docs and the Postgres-versus-ClickHouse proof-of-concept results, then learned by building: the six rollup tables that cut pivots from 189 seconds to 12 seconds, and the fix for weekly builds that ran out of memory at 170GB. On the AI side I learned LangGraph by shipping Ask Iris, with a supervisor that routes questions and an evaluator capped at 3 attempts. My method is always the same: read the source of truth, build something small and measurable, then go deep where the measurements point.

*Follow-up they may ask:* "How did you fix the out-of-memory problem?" I sliced each big INSERT SELECT into one fiscal week at a time and set memory and disk-spill caps. That was a load-time fix, separate from the pivot speedup.

---

**20. What do you know about our company?**

**Answer:**
*(Customise per employer, keep this skeleton.)*
Your company is known for [product or platform, and engineering bar]. I respect your focus on [reliability, developer platform, AI or scale], and this role matches where I have shipped: backend platforms, event-driven systems and careful production AI. I'm excited to contribute to [team mission] with the same ownership I brought to Uber FRM, the Masters India e-invoicing pipeline and AssortSmart.

---

**21. How do you handle tight deadlines?**

**Answer:**
With ruthless prioritisation and visible risk. I scope the must-have path, cut nice-to-haves, and tell stakeholders about trade-offs early. On Uber FRM reconciliation v2 under quarterly close pressure, I did the identity-correct joins and the HFM-versus-10-Q checks before any polish, kept v1 running in parallel as a safety net, and leaned on CI gates so speed never meant silent breakage. At Masters India during filing spikes, making portal calls asynchronous with a dead-letter queue mattered more than perfect synchronous latency. Deliver the critical path first, and never surprise anyone on the last day.

---

## Quick tips

- Prefer stories (company, constraint, action, number) over generic soft-skill claims.
- Uber FRM's 70% (from 14 days to 3 days) **is on the PDF as the outcome**. Defend it. If pressed, say the technical design doc framed that cut and that is what the platform delivered for the close. (Older prep tagged it TARGET. That guidance is obsolete.)
- Ask Iris is a **shipped capability**. Do not invent usage numbers or an SLA. The 80% is a CI gate, not live accuracy.
- Cluster Recommendation Copilot, its 14 tools, and "63 tables / 8 layers" are verbal design depth, not PDF bullets. Older versions of answers 11, 13 and 19 used them. Do not bring them up unless asked about clustering.
- No human review queues and no MCP claims on Impact Analytics.
- Menu 98% is offline evaluation. ANZ 20 hours/week is HISTORICAL.
- Keep "led 3" (Uber FRM) and "mentored 2" (Masters India) separate.
- For Q20, read the company's latest product or engineering blog the night before.
