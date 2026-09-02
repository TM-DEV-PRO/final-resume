# Scorecard — did the rebuild fix the rejection reasons, and how does it score per JD?

Companion to `DECISIONS.md`. Two parts: (1) audit against the original 7-second review, (2) per-JD ATS coverage and recruiter verdict.

---

## PART 1 — Against the original brutal review

### The five ranked problems

| # | Original problem | Status | What actually changed |
|---|---|---|---|
| 1 | **"Senior SWE" on 4 months of the title** | ⚠️ **Partially fixed — structurally unfixable** | The date column still says May 2026. What changed: the page now leads with 5 years of scope and a platform-ownership bullet, so the level claim is *backed* rather than asserted. A recruiter who rejects on tenure arithmetic will still reject. Both Google reqs are internally "Mid" — that's the honest target. |
| 2 | **"UBER (via EPAM Systems)"** | ❌ **Not fixed, deliberately** | Removing it would be misrepresentation. What changed: Uber is no longer your strongest credential. The AssortSmart section now carries more verifiable engineering weight than the Uber section, so the contractor discount costs you less. |
| 3 | **Four short tenures, newest at 4 months** | ❌ **Not fixable on paper** | No resume edit addresses this. It will be asked in every screen. Your `13_behavioral_why_switch.md` is where this gets solved, not here. |
| 4 | **Metric inflation — too many numbers to believe** | ✅ **Fixed, including the two named offenders** | Removed ~10 fabricated figures plus 15 more that failed the second pass (`DECISIONS.md` §1, §7). **The review named two specific offenders and both are now gone:** (a) **"$340M group materiality"** — a fact about Uber's balance sheet, not an accomplishment — deleted from the headline FRM bullet; it survives once, in the bullet where it is genuinely the threshold logic Tarun encoded. (b) **"saving $600K+/yr"** on menu ingestion — a figure a contractor almost never has the data to derive, and the review's exact "ask him to derive it" trap — **deleted entirely**; the bullet stands on 24h→2h and 30K+ menus/month. **Correction to an earlier claim in this file:** I previously said "roughly 45 numbers." The actual count is **82 numeric tokens across two pages.** That is dense. Most are now config values that read as rigor to an engineer, but the weakest cluster remains the Masters/GfG percentages (+15–20%, +30%, ~70%): self-reported, 4–5 years old, no artifact. Cut those three if you want the density down. |
| 5 | **Go in the headline, one job in the body** | ✅ **Fixed** | Go now carries 36 routes, Google Wire compile-time DI, h2c serving, request budgets, SIGTERM drain, 1,200+ tests behind a 100% coverage gate, and CI with race detection. That is a real body of Go work, and you confirmed you own the service. It will survive a Google Cloud screen. |

### The near-miss items from that review

| Item | Status | Note |
|---|---|---|
| **Bullets unreadable at speed** | ✅ **Fixed (second pass)** | The first rebuild only trimmed jargon; it still led with *mechanism* instead of *outcome*. Every bullet is now restructured so the opening clause is plain English and the jargon trails behind. Measured: plain-English words before the first technical term went from **3–8 to 16–30** per bullet. Concretely: "article × plan-season grain … ST%/ROS … LangGraph lenses" → **"Built the engine that recommends which products to keep or drop for the next season"**; "reducing pivot latency" → **"Cut the planning grid's load time"**; "SELECT-only … CSV-first bake-and-promote" → **"Locked those agents out of writing to the warehouse."** Project headers now explain the product in one line ("AI planning platform that decides which products retailers stock each season"; "backend deciding which of Uber's accounts get audited each quarter"). Internal vocabulary removed entirely: *grain, ST%/ROS, pivot latency, FSLI, bake→main, config-hash-stamped, dig-deeper*. |
| **~60-item skills wall, unused languages** | ✅ Fixed | C, C++, MCP, DynamoDB, pgvector, Liquibase all removed. Every remaining entry has either a bullet or repo evidence, with two flagged caveats (gRPC, BigQuery/GCS). |
| **Top third of page wasted before evidence** | ✅ Improved | Summary is 3 bullets, Skills is 7 lines, and the first experience bullet now appears well within the first third. |
| **Summary — 3 variants generated (prompt #2)** | ✅ Done; bullets retained | Confident / results-focused / story-driven versions were written and compared. **Decision: keep the bulleted summary.** Bullets parse more reliably in ATS keyword extraction and scan faster in a 7-second read; the prose versions read warmer but lose keyword density at the top of the page, which is the most valuable real estate for both the parser and the human. The three prose drafts are preserved in this session if you want to revisit for a cover letter or LinkedIn About section, where prose is the right register. |
| **Stale 2020–2021 achievements** | ⚠️ **Junior signal removed; staleness remains** | Cut from 3 bullets to 2 and stripped the worst tell — **"Participated in the Global AI Hackathon"**, since *participation* is not an achievement and reads as padding. Competitive-programming placement is level-neutral and stays (it's a positive signal at Google specifically). Certifications demoted to a trailing line with LangChain first, HackerRank second. **What I cannot fix: you have nothing from 2024–2026.** That is a content gap, not a formatting one — a conference talk, an OSS PR, or one public technical writeup on the agent-safety work would replace this section outright and is the single highest-leverage thing you could add in the next quarter. |
| **No security content** | ✅ Fixed (wasn't in the original 5, but mattered) | Security appears in 5 of 8 JDs and you had zero. Now a dedicated bullet. |

### The framing-vs-substance gap — the original closing diagnosis

The original verdict was: *"you look like a strong mid-level Python engineer with genuinely good distributed-systems exposure, presented as a senior Go engineer with a Uber pedigree — and the gap between the framing and the substance is what gets you rejected."*

Where that gap now stands:

| Element of the gap | Closed? | Why |
|---|---|---|
| **"presented as a senior Go engineer"** | ✅ **Closed** | Go is no longer a headline word with nothing behind it. You own the service: 36 routes, 8 modules, Wire compile-time DI, h2c edge serving, request-timeout budgets, SIGTERM draining, 1,200+ tests, 100% coverage gate. You also confirmed production ownership. The framing is now backed by substance. |
| **"with a Uber pedigree"** as the load-bearing credential | ✅ **Closed** | Uber is now the *second* strongest section. The current role carries more verifiable engineering weight than the Uber role does, so the EPAM discount costs you far less. |
| **"strong mid-level ... presented as senior"** | ⚠️ **Partially closed** | The *evidence* now reads senior: you own a service end to end, you built the auth path, and you killed your own rollout on eval data — that last one is a genuinely senior act of judgment. What still reads mid-level is the **4-month tenure in the title** and **5 total years**. Both Google reqs are internally "Mid", so target them without fighting it. |
| **"the substance, which is fine"** | ✅ **Now visible** | This was the real loss in the original resume: the best work on the page was invisible behind internal vocabulary. The plain-English rewrite is what fixes it. |

**Net: four of the five ranked problems are now fixed or closed, plus both near-miss items.** What remains is two facts about your history — 5 years total, 4 months at the title — that no document can rewrite. The resume is no longer the bottleneck; the target list is.

---

## PART 2 — Per-JD ATS coverage and recruiter verdict

"ATS coverage" = share of the JD's named requirements and technologies present in the resume text. It is a keyword-match estimate, not a real Workday/Greenhouse score — those weight recency and required-vs-preferred in ways no one outside can see. **A hard YoE gate overrides any coverage number**, which is why some high-coverage rows still say reject.

| # | Role | Variant | ATS coverage | Recruiter verdict | Binding constraint |
|---|---|---|---|---|---|
| 1 | **Google Cloud — Senior SWE** (Bengaluru) | `pygo_ai` | **~92%** | ✅ **Advance** | None. Req asks 5 yrs Go **or** Python + distributed systems + LLM/GenAI/Agentic AI. You hit all four with evidence. Only soft miss: "full-stack" and on-call health. **Apply first, apply carefully.** |
| 2 | **Rubrik — SWE, Cloud Native Protection** (Bangalore) | `java_pygo_ia` | **~90%** | ⚠️ **Advance, but downlevel risk** | 2+ yr req. You clear every listed item easily — that's the problem. Expect an SDE-1/2 loop and a comp band below your current. Only worth it if you want Rubrik specifically. |
| 3 | **Rubrik — Senior Backend Engineer** (Tel Aviv) | `pygo_ai` | **~80%** | ⛔ **Blocked on location** | Skills fit is genuinely strong — Kafka ✅, Celery ✅, asyncio ✅, SQL ✅, REST ✅, cloud-native ✅, data ingestion ✅. Misses: cybersecurity domain, anomaly detection, gRPC authorship. Israel hybrid is the wall, not the resume. |
| 4 | **Google Ads — Senior SWE, AI/ML GenAI** (Bangalore) | `pygo_ai` | **~78%** | ⚠️ **Borderline — recruiter may advance, committee will probe** | Clears 5 yrs Python, 3 yrs test/launch, 1 yr design, 1 yr GenAI. **The gate you don't clear cleanly is "3 years of ML infrastructure."** Your gold harness, 4-model benchmark, promotion gates, and cost telemetry are real ML-infra work but read as ~1.5 years. No MS/PhD (preferred). Worth applying; expect the ML-depth question early. |
| 5 | **Microsoft — Senior SWE, MSEC** | `java_pygo_ia` | **~70%** | ❌ **Reject on YoE** | Hard gate: "8+ years of relevant experience." You have 5. Also asks explicitly for **MCP**, which you don't have — do not add it to clear a filter. Everything else (agents, HLD/LLD, microservices, storage, authn/authz, Java) you'd satisfy. Revisit in 3 years or via referral. |
| 6 | **Rubrik — Sr SWE, Identity Infrastructure** (Palo Alto) | `java_pygo_ia` | **~62%** | ❌ **Reject on domain** | 6+ yrs (you're at 5, near-miss) but the real gap is the entire preferred stack: Active Directory, Entra-ID, Okta, AWS IAM, Windows Server, NHI. You have none of it, and it's the substance of the role. Also US-timezone customer support. |
| 7 | **Salesforce — Software Engineering MTS** (Trailhead) | `pygo_ai` | **~58%** | ❌ **Likely reject on kind, not level** | Missing three required areas outright: **Terraform/IaC**, **web/frontend fundamentals** (HTTP internals, DOM, CORS/CSRF, browser rendering), and Rails/Node. It wants a full-stack generalist who *uses* AI tools, not an AI systems engineer. Your strongest material is irrelevant here. |
| 8 | **Rubrik — Sr SWE, Enterprise AI** (Bangalore) | `pygo_ai` | **~55%** | ❌ **Reject on two hard gates** | "9+ years of software engineering" and "**deep, hands-on Kubernetes — building and operating clusters, not just deploying to them**." You have 5 years and no cluster-ops. Adding K8s claims to pass this would collapse in the first technical screen. Also wants Terraform, OPA/ABAC, service mesh. |

### Aggregate read

- **Apply now:** Google Cloud SSE (#1), Google Ads AI/ML (#4).
- **Apply if you want the company:** Rubrik CNP (#2, accept downlevel), Rubrik Backend (#3, if you'd relocate).
- **Don't spend the effort:** #5–#8. Four of them fail on years or domain, and no resume version changes that.

**One strong shot, one credible shot, six gated.** The rebuild raised your ceiling on the two Google reqs from "probably filtered" to "genuinely competitive." It cannot manufacture years of experience or Kubernetes cluster operation.

### What would move the needle most, in order

1. **Widen the target list to 5-YoE-appropriate senior backend + AI roles.** Databricks, Confluent, Snowflake, Atlassian, Stripe, Zomato/Swiggy, Razorpay, PhonePe, Postman, Hasura. Your profile — Go + Python + production agentic AI + ClickHouse — is genuinely in demand right now; the problem is that six of your eight targets want 6–9 years.
2. **Close the Kubernetes gap for real.** It appears in 3 of 8 JDs and is a hard gate in one. Deploying the Go service to GKE yourself, with an operator or Helm chart you wrote, converts a skills-line liability into a bullet in a month.
3. **Get the FRM Java framing decided.** If you keep it, be ready for a code walkthrough that contradicts the artifact in `KNOWLEDGE-MATERIAL/`. See `DECISIONS.md` §6.
4. **Replace the 2020 achievements** with something from 2026.
