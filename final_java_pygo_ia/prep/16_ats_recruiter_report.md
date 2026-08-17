# ATS + Recruiter Screening Report

<div class="callout warn">
<b>Historical snapshot — do not read as current.</b> This audit was run against an earlier PDF revision. Since then <b>Design Patterns</b> was removed from Backend &amp; APIs and <b>JUnit</b> from Core Engineering, and the Summary was rewritten to three lines with a per-track language stack. Any keyword row below that credits Design Patterns or JUnit to <i>Skills</i> is stale. Current truth lives in <code>GROUND_TRUTH.md</code> and <code>01_skills_trim_rationale.md</code>.
</div>

**Candidate:** Tarun Mittal (~5 years, Bangalore)  
**Variants reviewed:**  
- **Py/Go:** `Tarun_Mittal_SSE_5yr_v2.pdf`  
- **Java:** `Tarun_Mittal_SSE_Java_5yr.pdf`  
**Target levels:** SSE / SDE2 / SDE3 / SMTS / MTS (backend, data platform)  
**Review date:** 19 Jul 2026  
**Lens:** FAANG-tier ATS parse + human recruiter screen (not interview bar)

---

## Recruiter gut-check (applies to both variants)

### 6-second scan test

**What stands out first**
1. Header title: **Senior Software Engineer** + Bangalore
2. Brand names: **Uber**, then Impact Analytics, Masters India, GeeksforGeeks
3. Dense metrics: 60x ClickHouse POC, $600K+, 1M+ daily invoices, 30K+ menus/month
4. Skills row: either Python/Go/Kafka/ClickHouse or Java/Spring Boot/Kafka

**What a recruiter notices next (seconds 3-6)**
- Uber is **via EPAM** (contractor / vendor staffing, not Uber FTE)
- Current SSE role started **May 2026** (~2 months as of this review)
- Prior titles were **SDE2 / SDE**, not Senior, until IA
- One page is packed; metrics read strong but some lines feel target-heavy (“targeting…”)

### Title alignment

“Senior Software Engineer” at Impact Analytics since May 2026 is **credibly stretch, not fraud**, for ~5 YoE India market titles. For FAANG L5 / Amazon Sr SDE / Airbnb Senior / Netflix L5 screens, it is **optimistic**:

- Scope at Uber (led 3, design reviews, CI gates) supports SDE2 / mid-senior.
- Two months in title does not yet prove senior ownership at the new company.
- Safer external framing in outreach: “SDE2 / Senior-track backend (~5 YoE)” while keeping resume title if IA HR letter matches.

### Inflation / AI-sounding risk

| Signal | Recruiter read |
|---|---|
| Precise CH numbers (3.86s, 5.9M rows/sec, 60x) | Strong if defendable; looks measured, not fluff |
| “targeting a 70% cut”, “designed to cut… to under 2%” | Honest hedging; good. Do not upgrade to past-tense in interviews |
| “Defeated anti bot defenses…” | Slightly marketing; prefer “handled anti-bot via IP rotation…” |
| Dense SaaS + Agentic + RAG + migrations in one page | Can read as keyword-maxed; keep one crisp ownership story per role |
| Java variant: Spring Boot on Uber FRM / Masters / GFG | ATS win for Java shops. Integrity risk if interviewer expects Java code ownership at Uber Finance (position as architecture + outcomes; clarify stack in interview) |

### Structural red flags (both variants)

| Flag | Severity | Recruiter note |
|---|---|---|
| Tenure: GFG ~1.2y, Masters ~1.5y, Uber ~1.9y, IA ~2mo | Medium | Not classic hopping (each prior >1y), but 4 employers in ~5y needs a clean narrative |
| Uber via EPAM | Medium-High | Many FAANG recruiters discount vendor tenure vs FTE; emphasize Uber product ownership, not EPAM branding |
| SSE title + 2 months | Medium | Ask why leave so soon; prepare “comp/level/stack fit” story |
| One-page density | Low-Medium | ATS OK; human skim may miss leadership bullets buried mid-role |
| ~5 YoE vs 8-9y hard gates | Hard fail | Roku 8+, Rubrik 9+ will auto-screen out unless recruiter overrides |

---

## 1. Google

### Role found
**Senior Software Engineer** (backend-capable L5 pattern; e.g. Full Stack / Infrastructure postings on Google Careers)  
**Source:** [Google Careers - Senior Software Engineer](https://www.google.com/about/careers/applications/jobs/results/112706085885747910-senior-software-engineer/) (min quals pattern also mirrored on active SSE infra/full-stack listings, 2026)

### Stated key requirements
- Bachelor’s or equivalent
- **5 years** software development (Python / Java / Go / C++)
- **3 years** testing, maintaining, or launching products
- **1 year** software design and architecture
- (Infra variants) **3 years** large-scale infrastructure / distributed systems
- Preferred: technical leadership, Master’s/PhD, algorithms depth

### Keyword hit / miss

| Requirement keyword | Py/Go | Java |
|---|---|---|
| Python | HIT | HIT (secondary) |
| Go / Golang | HIT | MISS |
| Java | MISS | HIT |
| Distributed systems | HIT | HIT |
| Design / architecture | HIT (HLD/LLD, led design reviews) | HIT |
| Testing / launching products | HIT (coverage, CI, production ship) | HIT |
| Mentorship / tech lead | HIT | HIT |
| Large-scale infrastructure | PARTIAL (Kafka, K8s listed; less “infra from scratch”) | PARTIAL |
| C++ | MISS | HIT (skills list) |

### Verdict
| Variant | Screen | Why |
|---|---|---|
| **Py/Go** | **BORDERLINE** | Hits 5y language bar and product launch depth. EPAM + short SSE + no FAANG-scale “billions of users” signal keeps it from clean PASS. Go+Python is a strong Google language match. |
| **Java** | **BORDERLINE** | Same YoE/contractor flags. Java helps many Google teams; missing Go is fine if Java depth is real. |

**Highest-impact flip (BORDERLINE → PASS):** Add one verbatim phrase under Uber or Masters: **“software design and architecture”** ownership span (**“Owned design and architecture for X for 2+ years”**) plus a concrete **on-call / production incident** line. Google ATS and recruiters both scan for design+launch years, not only tech names.

---

## 2. Amazon

### Role found
**Senior Software Development Engineer, AWS DynamoDB** (Sr SDE template used broadly across Amazon/AWS)  
**Source:** [Amazon.jobs - Senior SDE, AWS DynamoDB (Job ID 3182977)](https://www.amazon.jobs/en/jobs/3182977/senior-software-development-engineer-aws-dynamodb)  
Same basic quals appear on Bengaluru Sr SDE postings (e.g. FBA / Transactional Services).

### Stated key requirements
- **5+ years** non-internship professional software development
- **5+ years** programming in at least one language
- **5+ years** leading design or architecture (design patterns, reliability, scaling)
- Experience as mentor, tech lead, or leading an engineering team
- Preferred: full SDLC, code reviews, testing, operations; distributed systems at scale

### Keyword hit / miss

| Requirement keyword | Py/Go | Java |
|---|---|---|
| 5+ years experience | HIT (stated) | HIT |
| Leading design / architecture | PARTIAL (led reviews; hard to claim **5 years** of leading design) | PARTIAL |
| Mentor / tech lead | HIT (led 3; mentored 2) | HIT |
| Reliability / scaling | HIT | HIT |
| Design patterns | MISS as phrase | HIT (skills: Design Patterns) |
| Distributed systems | HIT | HIT |
| DynamoDB | HIT (skills) | MISS |
| AWS | HIT | HIT |
| Operations / on-call | WEAK | WEAK |

### Verdict
| Variant | Screen | Why |
|---|---|---|
| **Py/Go** | **BORDERLINE** (lean FAIL on strict parse) | Amazon’s “5+ years leading design or architecture” is the killer. Total career is ~5y; leading design for 5y is not believable on a cold screen. Mentorship hits. EPAM discount applies. |
| **Java** | **BORDERLINE** (lean FAIL) | “Design Patterns” helps ATS. Same architecture-years gap. Prefer Java for many Amazon teams, but bar is ownership years, not Spring keywords. |

**Highest-impact flip:** Reframe summary to **“5 years building production systems; 3+ years leading design and architecture of services (reliability, scaling, design reviews)”** and keep mentor/tech-lead bullets above the fold. Do not claim 5 years of *leading* architecture if the timeline cannot support it in interview.

---

## 3. Microsoft

### Role found
**Senior Backend Engineer** (Microsoft AI) / **Senior Software Engineer - Backend** pattern  
**Source:** [Microsoft AI - Senior Backend Engineer](https://microsoft.ai/job/senior-backend-engineer/) (posted pattern Jan 2026); similar mins on Microsoft SSE Backend listings (Apr 2026 crawls)

### Stated key requirements
- Bachelor’s in CS or related **AND 4+ years** coding (C/C++/C#/Java/Rust/Python)
- Preferred often **6-8 years** (Master’s+6 or Bachelor’s+8)
- Scalable distributed / cloud backend, APIs, live-site readiness
- Increasingly: agent frameworks, Azure/AWS/GCP, Kubernetes, REST

### Keyword hit / miss

| Requirement keyword | Py/Go | Java |
|---|---|---|
| 4+ years | HIT | HIT |
| Python | HIT | HIT |
| Java | MISS | HIT |
| Distributed systems | HIT | HIT |
| Cloud (GCP/AWS) | HIT | HIT |
| Kubernetes | HIT (skills) | HIT (skills) |
| REST APIs | HIT | HIT |
| Agent / orchestration frameworks | HIT (LangGraph, MCP) | HIT |
| Azure | MISS | MISS |
| C# | MISS | MISS |

### Verdict
| Variant | Screen | Why |
|---|---|---|
| **Py/Go** | **PASS** | Clears 4+ year hard gate. Strong agentic + backend + cloud story matches current MAI/Copilot-adjacent backend posts. Azure gap is preferred, not required. |
| **Java** | **PASS** | Same YoE pass; Java is a first-class Microsoft language. Agentic skills still present via Python side. |

**Highest-impact flip (if any recruiter hesitates):** Add **“production backend services”** + **“live-site / operational excellence”** (on-call, SLOs, incident triage already implied by ELK/New Relic; make it explicit). Optional: **Azure** only if truthful.

---

## 4. Airbnb

### Role found
**Senior Software Engineer, App Foundation (Backend)**  
**Source:** [Airbnb Careers - SSE, App Foundation (Backend)](https://careers.airbnb.com/positions/7717198/) (also see Global Markets / Community Support backend seniors with 5-6+ YoE)

### Stated key requirements
- **5+ years** software development (many sibling roles **6+**)
- Strong backend language: **Java / Kotlin / C++** (Python appears on some market teams)
- High-traffic distributed products
- Databases, cloud, **asynchronous messaging**
- Mentoring often expected on Listing/backend seniors

### Keyword hit / miss

| Requirement keyword | Py/Go | Java |
|---|---|---|
| 5+ years | HIT | HIT |
| Java / Kotlin | MISS | HIT (Java; Kotlin MISS) |
| Distributed / high-traffic | PARTIAL (strong throughput; not consumer billions) | PARTIAL |
| Databases | HIT | HIT |
| Cloud | HIT | HIT |
| Async messaging / Kafka | HIT | HIT |
| Mentorship | HIT | HIT |
| Kotlin | MISS | MISS |

### Verdict
| Variant | Screen | Why |
|---|---|---|
| **Py/Go** | **BORDERLINE** | YoE OK for 5+ posts; language mismatch vs Java/Kotlin App Foundation bar. Kafka + scale help. Contractor + short senior title still questioned. |
| **Java** | **PASS** (thin) | Language match unlocks ATS. Scope still mid-market vs Airbnb traffic, but enough for a screen-in if referral/recruiter likes Uber brand. Prefer 6+ roles only with strong narrative. |

**Highest-impact flip (Py/Go BORDERLINE → PASS):** For Airbnb apps, submit **Java variant**, or add truthful **Java** exposure. Wording: **“high-traffic distributed backend services”** + **“asynchronous messaging (Kafka)”** in summary (verbatim JD language).

---

## 5. PlanetScale

### Role found
**Software Engineer - PlanetScale Vitess**  
**Source:** [Greenhouse - PlanetScale Vitess](https://job-boards.greenhouse.io/planetscale/jobs/4009746009) (careers also list Neki / Postgres Go roles)

### Stated key requirements
- **5+ years** backend-focused engineering
- **Strong proficiency in Go** (Python/Java/C++ secondary)
- MySQL or other relational DBs
- Kubernetes + containers
- Building and operating distributed systems at scale
- Nice: DB internals, query optimization, consensus, OSS, observability

### Keyword hit / miss

| Requirement keyword | Py/Go | Java |
|---|---|---|
| Go proficiency | HIT (Gin microservices, goroutine pools) | MISS |
| MySQL / relational | HIT | HIT |
| Kubernetes | HIT (skills; depth unclear) | HIT (skills; depth unclear) |
| Distributed systems at scale | PARTIAL | PARTIAL |
| Database internals / Vitess | MISS | MISS |
| Observability | HIT | HIT |
| OSS contributions | MISS | MISS |

### Verdict
| Variant | Screen | Why |
|---|---|---|
| **Py/Go** | **BORDERLINE** | Go is present and current (IA), which is rare and valuable. Depth looks app-level Go, not Vitess/MySQL internals. K8s looks resume-listed, not operated-clusters. |
| **Java** | **FAIL** | Missing **strong Go** is a hard miss for Vitess/Neki/Postgres control-plane roles. |

**Highest-impact flip (Py/Go):** Elevate Go from side bullet to **primary language signal**: e.g. **“Go (Gin) production microservices: plan lifecycle APIs, goroutine worker pools, JWT middleware”** in summary, and add one line on **MySQL/Postgres operational depth** (schema, indexing, query plans). Do not claim Vitess/internals without proof.

---

## 6. Databricks

### Role found
**Senior Software Engineer - Backend**  
**Source:** [Databricks Careers - SSE Backend (Bellevue/Seattle)](https://www.databricks.com/company/careers/engineering---pipeline/senior-software-engineer---backend-6779084002)  
India siblings often ask **6-7+ years** (e.g. Data Platform Bengaluru).

### Stated key requirements
- BS+ in CS or related
- **5+ years** production in **Java, Scala, Golang, C++, or similar** (some posts list Python; many prefer JVM/Go)
- Large-scale distributed systems
- SaaS or service-oriented architectures
- Cloud: AWS, Azure, GCP, or Kubernetes
- Security / sensitive data (preferred on several posts)

### Keyword hit / miss

| Requirement keyword | Py/Go | Java |
|---|---|---|
| Java / Scala / Go / C++ | HIT (Go) | HIT (Java) |
| Python | HIT | HIT |
| Distributed systems | HIT | HIT |
| SaaS | HIT (AssortSmart SaaS; Masters platform) | HIT |
| GCP / AWS / K8s | HIT | HIT |
| Sensitive data / security | PARTIAL (finance FRM, GST compliance) | PARTIAL |
| Spark / data plane | MISS on this PDF text | MISS |
| Scala | MISS | MISS |

### Verdict
| Variant | Screen | Why |
|---|---|---|
| **Py/Go** | **BORDERLINE** | SaaS + distributed + Go/Python fit US 5+ posts. Bengaluru 6-7y posts fail YoE. ClickHouse/BigQuery help data-platform story; Spark/Delta absence hurts pure data-platform lanes. |
| **Java** | **BORDERLINE → thin PASS** for Java-leaning backend pods | Java + SaaS + Kafka is a cleaner Databricks backend ATS match than Python-primary. Same YoE limit on 7y India posts. |

**Highest-impact flip:** Add verbatim **“SaaS platform”** and **“service-oriented architecture / microservices at scale”** in summary. If targeting data platform: one honest **batch/stream pipeline** line with **Kafka** (already present) and avoid inventing Spark.

---

## 7. Roku

### Role found
**Senior Software Engineer - Backend and Data** (Bengaluru)  
**Source:** [Roku Jobs - SSE Backend and Data, Bengaluru](https://www.weareroku.com/jobs/senior-software-engineer-backend-and-data-bengaluru-karnataka-india)

### Stated key requirements
- **8+ years** professional software engineering
- Java / Scala / Python
- Microservices, REST, message queues, caching, databases
- Event-driven architectures
- Apache Spark, Flink; Hive/Presto/HDFS; Kafka
- Airflow or similar ETL orchestration
- AWS preferred, GCP OK
- AI literacy (GenAI exposure)

### Keyword hit / miss

| Requirement keyword | Py/Go | Java |
|---|---|---|
| **8+ years** | **MISS** | **MISS** |
| Java/Scala/Python | PARTIAL (Py; no Scala) | HIT (Java+Py) |
| Microservices / event-driven | HIT | HIT |
| Kafka | HIT | HIT |
| Spark / Flink | MISS | MISS |
| Airflow / ETL orchestration | MISS | MISS |
| GenAI | HIT | HIT |

### Verdict
| Variant | Screen | Why |
|---|---|---|
| **Py/Go** | **FAIL** | Hard **8+ years** gate. Strong event-driven/Kafka/GenAI still will not clear ATS YoE filter on this posting. |
| **Java** | **FAIL** | Same YoE hard fail. Better language mix does not matter. |

**Highest-impact flip:** None for this JD. Target Roku postings with **5+ years** (some Backend CMS/content roles) instead of Backend-and-Data 8+ , or wait on YoE. Do not inflate years.

---

## 8. Rubrik

### Role found
**Senior Software Engineer - Enterprise AI**  
**Source:** [Rubrik Careers - SSE Enterprise AI](https://www.rubrik.com/company/careers/departments/job.7849713) (also Built In / India mirrors; **9+ years**)

### Stated key requirements
- **9+ years** backend/infrastructure focus
- Strong **Python and/or Go** production code
- **Deep hands-on Kubernetes** (build/operate clusters, not only deploy)
- Distributed systems in production
- AWS and/or GCP (compute, storage, IAM, networking)
- Terraform / IaC + CI/CD
- Agentic AI tools, AI gateways, agent frameworks
- Observability (Prometheus, Grafana, etc.)

### Keyword hit / miss

| Requirement keyword | Py/Go | Java |
|---|---|---|
| **9+ years** | **MISS** | **MISS** |
| Python / Go | HIT | PARTIAL (Py; Go MISS) |
| Deep Kubernetes | WEAK (listed, no cluster-ops proof) | WEAK |
| Terraform / IaC | MISS | MISS |
| Agentic AI / LangGraph / MCP | HIT | HIT |
| Prometheus / Grafana | HIT | HIT (Grafana) |
| Distributed systems | HIT | HIT |

### Verdict
| Variant | Screen | Why |
|---|---|---|
| **Py/Go** | **FAIL** | YoE hard fail (9+). Agentic stack is ironically a strong skill match for Enterprise AI, but screen dies on years + deep K8s/Terraform. |
| **Java** | **FAIL** | Same YoE fail; weaker Go signal. |

**Highest-impact flip:** None for Enterprise AI 9+. For Rubrik **Identity Infrastructure** style roles (often **6+**), still YoE-short; prioritize companies with 4-5y bars. Building real **Kubernetes operations + Terraform** depth helps future infra screens, not this one today.

---

## 9. Netflix

### Role found
**Software Engineer 5 - Content & Business Products** (L5 senior IC pattern)  
**Source:** Active L5-style listings (e.g. [Content & Business Products SE5](https://hiretik.com/jobs/eed9c2da-9f31-46ad-8b50-2a95392192f2); Open Connect / Experimentation L5 variants on Netflix careers mirrors, 2026)

### Stated key requirements (L5 pattern)
- **5+ years** resilient, high-scale, low-latency distributed microservices
- **Java / C# / OO** proficiency common; concurrency, performance, observability
- gRPC / GraphQL / REST
- Architecting HA, fault-tolerant systems; set technical direction
- On-call / incident leadership
- Some roles: Kafka, Cassandra, data lakes, Spark SQL

### Keyword hit / miss

| Requirement keyword | Py/Go | Java |
|---|---|---|
| 5+ years microservices | PARTIAL (5y total; scale mid) | PARTIAL |
| Java / OO | WEAK | HIT |
| gRPC | HIT (skills) | HIT |
| REST | HIT | HIT |
| High availability / fault tolerance | PARTIAL (HA in skills; less incident story) | PARTIAL |
| Observability | HIT | HIT |
| Kafka | HIT | HIT |
| On-call / incidents | WEAK | WEAK |
| GraphQL | MISS | MISS |

### Verdict
| Variant | Screen | Why |
|---|---|---|
| **Py/Go** | **BORDERLINE** (lean FAIL for Java-heavy L5 pods) | YoE nominally OK. Netflix L5 expects JVM depth and “business-critical at Netflix scale.” EPAM + Python-primary + limited on-call story are typical screen-outs without a strong referral. |
| **Java** | **BORDERLINE** | Better language fit. Still short on proven HA ownership and FAANG-scale blast radius. |

**Highest-impact flip:** Add one bullet with Netflix JD vocabulary: **“owned on-call for production microservices; led incident review; improved availability/latency”** (only if true). Pair Java variant with **concurrency / performance tuning** wording.

---

## Cross-company scorecard summary

| Company | Role used | Py/Go | Java |
|---|---|---|---|
| Google | Senior Software Engineer | BORDERLINE | BORDERLINE |
| Amazon | Senior SDE (DynamoDB / Sr SDE template) | BORDERLINE | BORDERLINE |
| Microsoft | Senior Backend Engineer | **PASS** | **PASS** |
| Airbnb | SSE App Foundation (Backend) | BORDERLINE | **PASS** (thin) |
| PlanetScale | Software Engineer - Vitess | BORDERLINE | **FAIL** |
| Databricks | SSE Backend | BORDERLINE | BORDERLINE / thin PASS |
| Roku | SSE Backend and Data (BLR) | **FAIL** | **FAIL** |
| Rubrik | SSE Enterprise AI | **FAIL** | **FAIL** |
| Netflix | Software Engineer 5 (L5) | BORDERLINE | BORDERLINE |

**Strict PASS count (cold ATS + recruiter, no referral):**  
- **Py/Go:** **1 / 9** clear PASS (Microsoft); **5** BORDERLINE; **3** FAIL  
- **Java:** **2 / 9** clear PASS (Microsoft, Airbnb thin); **4** BORDERLINE; **3** FAIL  

If “BORDERLINE with referral / India hiring manager override” counts as workable: Py/Go ~6/9 chaseable; Java ~6/9 chaseable. Roku 8+ and Rubrik 9+ remain non-starters on YoE.

---

## Keyword gaps appearing across 3+ companies

These miss or weak signals show up repeatedly:

1. **Hard YoE gates above 5** (Roku 8+, Rubrik 9+, some Databricks India 6-7+, many Airbnb 6+) - structural, not a keyword tweak  
2. **Kubernetes depth** (listed, not “operated clusters / production troubleshooting”) - Google infra, PlanetScale, Databricks, Rubrik, Roku  
3. **On-call / incident leadership / live-site** - Amazon preferred SDLC, Microsoft live-site, Netflix L5, Google triage  
4. **“Leading design and architecture” with multi-year span** - Amazon explicit; Google 1y design min; Airbnb/Netflix senior ownership  
5. **JVM or Java as primary** for Airbnb App Foundation, Netflix L5, many Amazon/Databricks pods - Py/Go variant loses ATS ties  
6. **Spark / Flink / Airflow** - Roku data, some Databricks/Netflix data-adjacent - absent on both PDFs  
7. **Terraform / IaC** - Rubrik and infra-leaning screens  
8. **Azure** - Microsoft preferred ecosystem (GCP/AWS present)  

---

## Top 10 changes ranked by impact

*(Wording/keyword only. Do not invent experience. No .tex/.pdf edits made in this task.)*

1. **Split targeting:** Use **Java variant** for Airbnb / Amazon / Netflix / Databricks Java pods; **Py/Go** for PlanetScale / Microsoft AI-agent / Google Go teams. Biggest screen lift with zero new skills.  
2. **Fix Amazon architecture years claim:** Summary line that states **years leading design/architecture honestly (e.g. 2-3+)** plus reliability/scaling, instead of implying 5 years of leading design.  
3. **Promote Go on Py/Go resume** into summary (PlanetScale / Google / Rubrik-adjacent): production Gin, worker pools, not only skills row.  
4. **Add explicit on-call / incident / live-site bullet** (Microsoft, Netflix, Amazon, Google).  
5. **Verbatim SaaS + SOA/microservices at scale** in summary (Databricks, Airbnb, Microsoft).  
6. **Strengthen Kubernetes beyond skills list** only if true: “deployed/operated services on Kubernetes” with one production proof point (PlanetScale, Databricks, Rubrik future).  
7. **EPAM framing:** Keep “Uber (via EPAM)” for honesty, but lead with **Uber product org / Finance / Eats** ownership so ATS brand match survives human discount.  
8. **Tone down AI-marketing verbs** (“Defeated anti bot…”) to neutral eng voice; reduces inflated/AI-written skim risk.  
9. **Add “design patterns, reliability, and scaling”** phrase near FRM/Masters leadership bullets (Amazon ATS).  
10. **Do not chase Roku 8+ / Rubrik 9+** with keyword stuffing; retarget 5y-bar postings at those companies if any exist, or revisit later.

---

## Final recruiter note

Both one-pagers are **above average** for a ~5 YoE Bangalore backend candidate: real metrics, migration ownership, mentorship, and a modern agentic stack. They are **not yet default FAANG Senior / L5 auto-passes**. The limiting factors are **years at senior ownership**, **vendor tenure at Uber**, **brand-new SSE title**, and **company-specific language stacks** (Go vs Java), not a missing laundry list of buzzwords.

**Best near-term screen strategy:** Microsoft + Databricks backend + Airbnb (Java) + Google (language-matched) + PlanetScale (Py/Go only). Treat Amazon Sr SDE and Netflix L5 as **referral / borderline** campaigns. Park Rubrik Enterprise AI and Roku Backend-and-Data until YoE and infra depth catch up.

---

## Re-screen after TPS/RPS and PlanetScale hardening (Loop 4)

**Re-screen date:** 19 Jul 2026  
**PDFs re-extracted:** `Tarun_Mittal_SSE_5yr_v2.pdf`, `Tarun_Mittal_SSE_Java_5yr.pdf`  
**Delta since prior scorecard:** Masters TPS/RPS (~12 TPS avg / 100+ peak, ~67 RPS), p95 latency 1.2s to 300ms, IA p95 probes under 500ms vs 1 to 20s BigQuery, Py/Go skills now include Linux + Sharding + Performance Tuning, Masters on-call alerting bullet, Java IA Spring Boot microservices bullet, separate certification bullets.

### PlanetScale deep evaluation (priority)

**Active listings checked (planetscale.com/careers + Greenhouse, Jul 2026):**
- [Software Engineer - PlanetScale Vitess](https://job-boards.greenhouse.io/planetscale/jobs/4009746009) (EMEA Remote)
- [Software Engineer - Neki Orchestration](https://job-boards.greenhouse.io/planetscale/jobs/4280570009) (SF Bay / Remote)
- [Software Engineer - Sharded Postgres (Neki)](https://job-boards.greenhouse.io/planetscale/jobs/4009936009) (SF Bay / Remote)
- Also open: PlanetScale Postgres, Insights, Platform; **Postgres Internals** (C / PG core) is a different hiring lane and is out of scope for this candidate.

**What PlanetScale screens for (shared across Vitess / Neki Orchestration):**
- 5+ years backend / large-scale production systems
- **Strong Go** (Python/Java/C++ secondary)
- MySQL or other relational DBs
- Kubernetes + containers (working knowledge)
- Building and operating distributed systems at scale
- Performance, Linux/OS fundamentals (stronger on Neki Orchestration)
- On-call participation (explicit on Neki Orchestration)
- Nice: DB internals, query optimization, consensus, OSS, cloud, observability
- Culture signal: small-team ownership, high autonomy, customer-facing systems work

**Sharded Postgres (Neki) is a harder bar:** "focus on backend systems, database engines, query planners" and "not just operating, but **developing** PostgreSQL, MySQL or other databases." That is engine/product work, not app sharding alone.

#### Keyword hit / miss (updated Py/Go resume)

| Requirement | Vitess / Neki Orchestration | Evidence on updated Py/Go PDF |
|---|---|---|
| 5+ years backend | HIT | Stated 5y; multi-company production ownership |
| Strong Go | HIT | IA: Go (Gin) microservices, goroutine worker pools, JWT middleware |
| MySQL / relational | HIT | Uber FRM MySQL schema + APIs; GFG MySQL; Masters PostgreSQL; IA PostgreSQL/ClickHouse |
| Sharding | HIT (new) | Masters quarter sharding + Core skill "Sharding" |
| Throughput / scale numbers | HIT (new) | ~12 TPS avg / 100+ peak; ~67 RPS; 1M+ daily invoices |
| Performance tuning | HIT (new) | Skills keyword; p95 1.2s to 300ms; CH POC 60x; probe p95 under 500ms |
| Linux | HIT (new) | Skills: Linux |
| On-call / ops | HIT (new) | ELK + New Relic on-call alerting; incident triage 70% |
| K8s + containers | HIT (thin depth) | Docker + Kubernetes in skills; no cluster-ops narrative |
| Observability | HIT | ELK, New Relic, Prometheus, Grafana |
| Cloud (AWS/GCP) | HIT | Both present |
| DB internals / Vitess / consensus | MISS | Do not invent; preferred only on Vitess/Neki Orchestration |
| Developing PG/MySQL engines | MISS | Blocks clean PASS on Sharded Postgres (Neki) engine role |
| OSS DB contributions | MISS | Preferred only |

#### Verdict by PlanetScale lane

| Listing | Py/Go | Java | Margin / note |
|---|---|---|---|
| **Vitess** | **PASS** | **FAIL** | Py/Go clears all hard quals with **comfortable margin**. Go + MySQL + sharding + TPS/RPS + Linux + performance + on-call is a coherent PlanetScale story. Internals/Vitess still preferred-only gaps. |
| **Neki Orchestration** | **PASS** | **FAIL** | Same hard-qual clear. On-call + PostgreSQL + sharding + Linux/performance align well with control-plane / ops flavor. Margin **comfortable**, not "Vitess committer" margin. |
| **Sharded Postgres (Neki)** | **BORDERLINE** | **FAIL** | Go + sharding help ATS, but JD asks for **developing** DB engines / query planners. App-level quarter sharding and CH/PG POC benchmarking are adjacent, not engine work. |
| **Postgres Internals** | **FAIL** | **FAIL** | Needs C + PostgreSQL core/extensions. Out of lane. |

**Headline PlanetScale call (primary apply targets = Vitess + Neki Orchestration):**  
- **Py/Go: PASS with margin** (up from Loop 1 BORDERLINE). Loop 4 closed the thematic gaps (sharding, Linux, performance, quantified throughput, on-call) that previously made Go look like a side skill on a Python resume.  
- **Java: FAIL** (unchanged). Missing strong Go is a hard miss for these listings.

**Honest-only wording still worth making (optional; thickens margin, does not invent Vitess/kernel):**
1. Summary (Py/Go): add one clause elevating Go + data-plane ownership, e.g. "Go (Gin) production microservices; MySQL/PostgreSQL schema and quarter-based sharding for high-throughput billing APIs."
2. Masters sharding bullet: keep honesty as **quarter-based sharding** (time/partition strategy), optionally add "PostgreSQL" inline so ATS ties sharding to a relational store, not only Kafka.
3. Uber FRM: if true, one short phrase on **indexing / query performance** for the 11-table MySQL schema (schema design is already there; query/index language helps PlanetScale preferred "query optimization" without claiming internals).

Do **not** add Vitess, replication protocol work, consensus, or database kernel experience.

### Updated 9-company scorecard (both variants)

| Company | Py/Go | Java | What Loop 4 closed / still open |
|---|---|---|---|
| Google | BORDERLINE | BORDERLINE | On-call + latency numbers help design/launch skim. Still EPAM discount + short SSE tenure. |
| Amazon | BORDERLINE | BORDERLINE | On-call helps preferred ops. Still blocked by "5+ years leading design/architecture" cold parse. |
| Microsoft | **PASS** | **PASS** | Already PASS; on-call and p95 numbers strengthen live-site signal. |
| Airbnb | BORDERLINE | **PASS** | TPS/RPS help high-traffic skim. Py/Go still weak vs Java/Kotlin App Foundation language bar. |
| PlanetScale | **PASS** | **FAIL** | Py/Go flipped BORDERLINE to PASS with margin (sharding, Linux, performance, TPS/RPS, on-call). Java still no Go. |
| Databricks | BORDERLINE | BORDERLINE | Throughput + SaaS/CH POC help. YoE still soft on 6-7y India posts; no Spark. |
| Roku | **FAIL** | **FAIL** | Hard 8+ YoE gate unchanged. |
| Rubrik | **FAIL** | **FAIL** | Hard 9+ YoE gate unchanged; Linux/on-call do not move years. |
| Netflix | BORDERLINE | BORDERLINE | On-call + p95 latency close a prior gap. Still short of Netflix-scale HA ownership for clean L5 PASS. |

**Strict PASS count after Loop 4:**  
- **Py/Go: 2 / 9** (Microsoft, PlanetScale). Was 1 / 9.  
- **Java: 2 / 9** (Microsoft, Airbnb). Unchanged. PlanetScale remains FAIL on Java.

Chaseable with referral (BORDERLINE): Google, Amazon, Airbnb (Py/Go), Databricks, Netflix. Non-starters on YoE: Roku, Rubrik.

### Remaining honest-only suggestions (post Loop 4)

1. **PlanetScale / Google Go teams:** Elevate Go into the Py/Go summary (see PlanetScale wording above). Biggest remaining ATS skim gap vs skills-row-only Go.  
2. **Amazon:** Keep architecture-years honest (2-3+ leading design), do not imply 5 years of leading architecture.  
3. **Submit the right PDF:** Py/Go for PlanetScale and Go-heavy Google pods; Java for Airbnb / many Amazon / Netflix L5 pods.  
4. Still do not invent Vitess, Spark, Terraform depth, or YoE inflation for Roku/Rubrik.

## Re-screen after evidence-backed skill hardening (Loop 6)

**Delta:** ownership verbs + software architecture language on FRM; Masters strangler ownership + fault-tolerant bulk (idempotency/retries/DLQ) + on-call alerting; Design Patterns / Fault Tolerance skills; CGPA removed; STUDY ONLY deep dive for multi-region / K8s ops / Spark / Flink / Terraform (not on PDFs).

| Theme | Py/Go | Java | Notes |
|---|---|---|---|
| Ownership / design and architecture | HIT | HIT | "Owned backend", "18 files recon v2", "materiality engine", "Led 3 engineers" |
| On-call / live-site | HIT (alerting) | HIT (alerting) | Honest scope: alerting + triage, not invented pager commander |
| Fault tolerance | HIT | HIT | Idempotency, retries, DLQ + Core skill |
| Design Patterns | HIT (skills) | HIT (skills) | Backed by strangler / layered / cache-aside verbally |
| Multi-region | MISS (correct) | MISS (correct) | Study-only; would fail honesty audit if added |
| K8s ops depth | WEAK (skills only) | WEAK (skills only) | Correct; do not promote |
| Spark / Flink / Terraform | MISS (correct) | MISS (correct) | Study-only; Databricks Spark lane still needs real Spark later |

**Strict PASS count unchanged structurally (YoE gates):** Py/Go 2/9 (Microsoft, PlanetScale); Java 2/9 (Microsoft, Airbnb). Ownership/architecture language improves Amazon/Google skim quality inside BORDERLINE, without inventing 5 years of leading design.

**Honesty still required in interviews:** claim ~3 years leading design reviews (Masters + FRM), not Amazon's literal 5+ years leading architecture.

## Number / money / Spark-Flink verification pass (Jul 2026)

| Check | Result |
|---|---|
| IA PG→CH POC | **VERIFIED** against `ClickHouse-POC-Dump/_SYNTHESIS/BENCHMARK-NUMBERS.md`: 23.7M join rows, CH 3.86s vs PG 3m40s–7m48s (~60×), insert 5.91M vs 250K (~24×). Hardware caveat required in interview. |
| FRM 70% brackets | Resume now shows **targeting 70% (~2 weeks to ~3–4 days)**. 70% = TDD TARGET; from-to ESTIMATED. |
| Spark / Flink / Pinot | **Superseded by Loop 8** — Spark+Flink restored on Uber Menu; Pinot still off PDF. |
| Money deep dive | Menu $600K+ = $2/menu × 30K × 12 = $720K list → conservative floor. Catalogued in `18_resume_number_catalog.md`. |
| Big-tech company skim (Google, Amazon, Microsoft, Airbnb, PlanetScale, Databricks, Roku, Rubrik, Netflix) | Microsoft + PlanetScale (Py/Go); Microsoft + Airbnb (Java). Databricks skim improves with Spark on Menu. YoE hard fails (Roku 8+, Rubrik 9+) unchanged. |

## Loop 8: Spark + Flink restored on Uber Menu

| Check | Result |
|---|---|
| Placement judgment | **Uber Menu** best fit (not Masters, not IA). |
| Resume wording | Selenium→Kafka (~200–500 peak events/sec)→Flink→Spark; skills updated both tracks. |
| Prep depth | `14_uber_menu_deep_dive.md` rewritten with architecture, why Flink vs Spark, Q&A, money/rate math. |
| Databricks skim | Improves from Spark MISS to HIT on experience; still not a Delta/runtime specialist claim. |
| Honesty | Peak events/sec and Spark row counts ESTIMATED; Pinot still off PDF; no Spark/Flink at Masters or IA. |

## Loop 9: Evidence rewrite + fresh 5y Py/Go listings (Jul 2026)

### What changed on the PDF
- IA: product-first AssortSmart; **building** not shipping; **8.5% (37/437)** explicit; line-plan **~0.4 ms / sub-second** measured ops; **ONE** CH bullet (63/8 + 189s→12.3s)
- Summary: ATS phrases — `5 years professional software development`, `software design and architecture`, `building and operating`, `on-call`, `throughput (req/min)`
- Skills: `SOA`, `Operational Excellence`, `On-call / Incident Response`
- Masters: `Designed, built, and operated`; clean **700→4,000 requests/min** (no ~TPS/~RPS)
- Menu: no Kafka/Flink/Spark; Kafka ownership on Masters (Mayank-aligned)

### Fresh listing gates (~5y Python / Golang senior)
| Apply aggressively (JD ~4–5y) | Structural skip unless waived |
|---|---|
| Google SSE (**5y** + 1y design) | Amazon Senior posts with **8+** non-internship |
| Databricks Backend (**5+**) | Airbnb GenAI / Staff (**8+**) |
| PlanetScale Vitess/Neki (**5+** Go) | Meta Staff Systems (**8+**) |
| Microsoft SSE (required **4+**) | Rubrik **9+**, Roku **8+** |
| Stripe Core Technology (wide band) | Cloudflare mirrors **7–10y** |

### Updated cold-screen scorecard (after Loop 9)

| Company | Py/Go | Java | Margin note |
|---|---|---|---|
| Microsoft | **PASS (good)** | **PASS (good)** | On-call + design/architecture + latency/RPM explicit |
| Google SSE (5y JD) | **PASS (thin→good)** | BORDERLINE | Hits 5y + design phrase; EPAM still a human discount |
| Databricks Backend | **PASS (thin)** | BORDERLINE | Distributed + SaaS + Kafka/CH; Spark off PDF (honest) |
| PlanetScale (Go) | **PASS (thin→good)** | FAIL language | Go elevated in summary; sharding + on-call present |
| Airbnb (5y backend/infra) | BORDERLINE | **PASS (thin→good)** | Prefer Java PDF |
| Stripe Core Tech | **PASS (thin)** | BORDERLINE | Operate + alerting language |
| Amazon Sr (5y design JD only) | BORDERLINE | BORDERLINE | Claim ~3y design ownership, not 5y leading architecture |
| Amazon Sr (8y JD) | **FAIL** | **FAIL** | Structural YoE |
| Netflix L5 | BORDERLINE | BORDERLINE | Referral recommended |
| Roku / Rubrik | **FAIL** | **FAIL** | YoE hard gates |

**Chase with margin:** Microsoft, Google SSE (5y), PlanetScale, Databricks, Stripe Core, Airbnb (Java).  
**Not auto-pass:** Amazon 8y, Netflix L5, Staff/8y+ — referral or skip.
