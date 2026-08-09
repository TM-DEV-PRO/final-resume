# Common interview questions — filled answers (your experience)

Format matches the “90 toughest interview questions” style: **numbered question**, **Answer:**, horizontal rule.  
Honesty: MEASURED / TARGET / HISTORICAL per `GROUND_TRUTH.md`. Company-specific Q20 — customize per employer.

HTML: [`32_common_interview_qa.html`](32_common_interview_qa.html) · Hub: [`ApplicationKit.html`](../ApplicationKit.html)

---

**1. Tell me about yourself.**

**Answer:**  
I am a Senior Software Engineer with about 5 years building backend and data platforms in Python and Go. I have worked across Impact Analytics, Uber via EPAM, Masters India, and GeeksforGeeks. At Uber I owned the FRM Risk Scoping backend (Spring Boot, MySQL — 30+ APIs powering 8 screens) at $340M group materiality, and I worked on Uber Eats menu automation that cut onboarding from 24 hours to 2 hours and saved $600K+ a year on 30K+ menus a month. At Masters India I migrated a PHP Laravel GST platform to FastAPI microservices for 1,500+ clients, cutting p95 from 1.2s to 300ms, and scaled bulk e-invoicing on Kafka to 1M+ government submissions a day. Now at Impact Analytics I am building AssortSmart’s planner copilot with LangGraph, MCP, and ClickHouse — say building, not fully shipped. I care about honest metrics, clear design tradeoffs, and owning systems end to end.

---

**2. Why should we hire you?**

**Answer:**  
I bring architecture ownership, production discipline, and mentorship — not only ticket delivery. With my background in distributed backends and event-driven systems, I have successfully owned Uber Finance FRM design while leading 3 engineers, cut Uber Eats menu ops cost by $600K+ a year, and scaled Masters India IRP traffic from 700 to 4,000 requests/min with Kafka while mentoring 2 engineers. I am skilled in Python, FastAPI, Go, Kafka, and agentic systems (LangGraph/MCP), and adaptable across product domains from GST compliance to retail planning. My ability to defend every resume number with MEASURED vs TARGET honesty lets me drive results without overclaiming. I am committed to adding value to your team and aligning with how you ship reliable systems at scale.

---

**3. What is your greatest strength?**

**Answer:**  
My greatest strength is turning messy production constraints into clear system designs and shipping them safely. I thrive when correctness, latency, and ownership collide. For example, at Uber Finance we still ran quarterly FRM scoping on Google Sheets with no durable line IDs or audit trail. I designed a layered Spring Boot + MySQL backend, owned the Sheets→MySQL recon v2 migration across 18 files with L1→L2→L3 APIs and HFM vs 10-Q checks, and encoded materiality/residual/5% threshold logic across ~55×14 for PwC-facing work. That helped Finance move from a fragile workbook close toward a system of record targeting a large cut in manual reconciliation. It shows I can handle pressure and think in both product and engineering terms.

---

**4. What is your greatest weakness?**

**Answer:**  
One area I continuously improve is delegating earlier when I own the critical path. Earlier in my career I took too many recon and cutover tasks myself to “guarantee quality,” which slowed mentoring. At Masters India and later at EPAM/Uber I changed that: I set API contracts, paired juniors on the first canary or recon slice, then stepped back so others owned services. Leading 3 engineers on FRM and mentoring 2 on the FastAPI migration forced that habit. Clear expectations and review cadence now beat doing everything myself.

---

**5. Tell me about a time you failed.**

**Answer:**  
At Masters India, early in the PHP→FastAPI cutover, I set API timeouts too aggressively compared with the old PHP path. Some legitimate IRP government calls needed longer round trips, so the first canary showed timeouts and risked filing-day pain. I owned the miscalculation, moved those calls fully async (202 + progress), aligned timeouts with real IRP behavior, and added idempotency keys, retries, and a dead-letter queue so safe replay was possible. The lesson stuck: for third-party compliance APIs, design for latency variance and idempotent retry up front, not after the first canary scare.

---

**6. Describe a time when you had to deal with a difficult team member.**

**Answer:**  
At Uber via EPAM on FRM, a teammate kept slipping on API contract and test gates, which blocked Finance-facing releases. Instead of escalating first, I scheduled a one-on-one. They were overloaded across UI and backend spikes. We re-sliced ownership — I kept schema and recon v2 critical path, they owned a bounded screen/API set with clearer Definition of Done — and I paired on the first PR using our handler/service/repository pattern. Delivery stabilized, CI stayed green, and we hit the release bar for PwC work papers without burning the relationship.

---

**7. Where do you see yourself in five years?**

**Answer:**  
In five years I see myself as a senior/staff-leaning backend or platform engineer who owns a multi-service domain end to end — design, reliability, and mentoring. My goal is to keep deepening distributed systems, data platforms, and production agentic systems, while helping others ship safely behind clear contracts. I want the next role to be a multi-year build where scope compounds, not a short hop.

---

**8. Why do you want to leave your current job?**

**Answer:**  
I have learned and grown at Impact Analytics — especially around ClickHouse, LangGraph/MCP, and agentic planning safety — but I am seeking a role whose day-to-day ownership matches a multi-year backend/platform charter. I am particularly interested in deeper production ownership of distributed systems and data platforms at scale, which this role offers. I closed open work professionally and I am interviewing carefully for fit. I believe my skills will add value here while I keep developing.

---

**9. How do you handle pressure and stress?**

**Answer:**  
I treat pressure as a signal to prioritize and communicate, not to panic. I break work into milestones, protect the critical path, and keep stakeholders aligned on risk. For instance, during Uber FRM quarterly close windows and Masters India GST filing spikes, I stayed calm, sequenced recon/IRP work, and used observability (ELK/New Relic, CI gates) so we did not guess under load. Time-boxing, clear owner lists, and honest status updates keep me composed.

---

**10. What motivates you?**

**Answer:**  
I am motivated by hard systems problems with real business or compliance impact — fixing a broken close process, making filing-day IRP traffic safe, or making an agent that cannot silently write bad plans. I like designing the tradeoff, shipping it, and defending the numbers. Teamwork matters too: mentoring engineers through a strangler cutover or FRM pod delivery is as satisfying as the metric itself.

---

**11. How do you handle constructive criticism?**

**Answer:**  
I treat constructive criticism as free design review. I listen, clarify the failure mode, and change the system — not just the slide. At Impact Analytics, design reviews pushed harder on agent write safety and ClickHouse mutation risk; I tightened the story to read-only tools, human confirm steps, and insert-only / partition-swap refreshes, and I keep saying “building / load test pending” instead of “shipped.” That feedback made the architecture more interview- and production-honest.

---

**12. Tell me about a time you led a team.**

**Answer:**  
I led a pod of 3 engineers at Uber via EPAM on the FRM Risk Scoping backend. I set the layered architecture (handler/service/repository), API contracts, and design reviews, and I personally owned the Sheets→MySQL recon v2 migration. Through design reviews and clear ownership slices we delivered 30+ APIs powering 8 screens for Finance's quarterly scoping releases, with a large unit-test suite for release confidence. At Masters India I also mentored 2 engineers through the FastAPI migration with the same pattern: pair first, then hand off.

---

**13. Tell me about a time you disagreed with a technical decision.**

**Answer:**  
On AssortSmart analytics, a natural instinct is “just put the planner grid on Postgres forever” or “use ClickHouse with row UPDATEs.” I disagreed with row-level CH mutations for interactive planning because ClickHouse mutation queues are a known footgun. I backed an insert-only model with partition swaps for refresh, agent read-only privileges, and a measured pivot POC (250M rows, 189s → 12.3s). I presented the evidence, accepted that load test is still pending, and kept the claim honest: adopting the store design after POC proof, not “fully shipped to every tenant.”

---

**14. Tell me about a time you had to decide with incomplete information.**

**Answer:**  
On Uber Eats menu ingestion, partner sites and anti-bot behavior change without notice. We could not wait for perfect catalogs of every failure mode. I pushed IP rotation, proxy pools, and retries, raised successful ingestions toward 95%+, and kept unstructured PDF/image menus on a LangChain RAG + Gemini + Milvus path with schema validation and human review for low confidence. We decided with partial information by measuring success rate and offline fidelity (98%/100% schema offline eval) instead of freezing delivery.

---

**15. What are you most proud of?**

**Answer:**  
Two threads: (1) Replacing a fragile Finance Sheets close with a real FRM platform and owning recon correctness under audit pressure. (2) Making bulk GST IRP traffic durable with Kafka, quarter-split PostgreSQL, and idempotent retries so 1M+ submissions/day did not mean double-registration with the government. Both combined systems design with accountability.

---

**16. Tell me about a time you went above and beyond.**

**Answer:**  
At Uber Finance, recon v2 was not “just another API.” I went beyond ticket scope: validated HFM extracts against public 10-Q filings line by line, hunted a silent identity bug from duplicate join column names, and kept v1 running in parallel until trust was earned. That protected PwC-facing work papers and Finance’s quarterly close — more than shipping an endpoint.

---

**17. How do you handle conflict in the workplace?**

**Answer:**  
I handle conflict by separating people from the design argument and forcing a shared success metric. For example, at Masters India, opinions split between big-bang rewrite vs gradual FastAPI cutover. I facilitated around filing-day risk: canary per endpoint behind the gateway, shared DB during traffic move, instant rollback. We picked gradual migration, mentored two engineers on the pattern, and still hit p95 1.2s → 300ms without a dark launch.

---

**18. What is your leadership style?**

**Answer:**  
Collaborative and standards-driven. I set architecture and quality bars (contracts, CI, observability), then empower others to own slices. On FRM I reviewed early, then stepped back as ownership stuck. On Masters I paired on the first canary and let juniors take full services. I adapt: tighter hands-on on compliance/audit paths, more autonomy on well-bounded features.

---

**19. Tell me about a time you had to learn something new quickly.**

**Answer:**  
At Impact Analytics I had to ramp quickly on ClickHouse planning-store design and LangGraph/MCP agent orchestration for AssortSmart. I used internal Confluence DDL/HLD, ran and read the pivot POC results, and paired design with safety constraints (14 read-only tools, human confirm steps). Within the onboarding window I could defend 63 tables / 8 layers, insert-only refresh, and the 189s → 12.3s pivot evidence — while being clear the product is still building toward load test.

---

**20. What do you know about our company?**

**Answer:**  
*(Customize per employer — keep this skeleton.)*  
Your company is known for [product/platform + engineering bar]. I respect your focus on [reliability / developer platform / AI / scale], and roles like this match where I have shipped: backend platforms, event-driven systems, and careful production AI. I am excited to contribute to [team mission] with the same ownership I brought to Uber FRM, Masters IRP, and AssortSmart.

---

**21. How do you handle tight deadlines?**

**Answer:**  
I handle tight deadlines with ruthless prioritization and visible risk. I scope the must-have path, cut nice-to-haves, and communicate tradeoffs early. For instance, on Uber FRM recon v2 under quarterly close pressure, I sequenced identity-correct joins and HFM vs 10-Q checks before polish, kept parallel v1 as safety, and used CI gates so speed did not mean silent breakage. At Masters India on filing spikes, async IRP + DLQ mattered more than perfect sync latency. Deliver the critical path first; never surprise stakeholders on the last day.

---

## Quick tips

- Prefer **stories** (company + constraint + action + number) over generic soft skills.  
- Never claim IA copilot “fully shipped” or FRM “70% achieved” — those are TARGET / building.  
- Menu **98%/100%** = offline eval; ANZ **20h/week** = HISTORICAL.  
- For Q20, research the company’s latest product/eng blog the night before.
