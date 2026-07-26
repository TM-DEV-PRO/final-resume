# LinkedIn Technical Recruiter Screen

## Typical titles and levels

| Title | Approx. level (community) | YoE pattern | Fit |
|---|---|---|---|
| Software Engineer | ICT / mid | ~2–4y | Possible but title undersells |
| Senior Software Engineer | Senior IC | Often **4–8+** | **Primary target** |
| Staff Software Engineer | Staff | Broader domain ownership | Stretch / not default |
| SWE (Infrastructure / Data / AI) | Varies | Domain keywords matter | Target by domain match |

LinkedIn (Microsoft company) uses engineering ladders similar in spirit to Microsoft but **product/culture is LinkedIn-specific**. Recruiters care about **member/customer impact**, **scalable backend**, and **craft**.

**Practical targeting:** **Senior Software Engineer** (backend, data, infra, AI platform). Avoid Staff unless you have multi-team platform ownership evidence.

---

## Hard requirements recruiters check

### Years of experience
- Senior postings commonly expect several years building production services (often **4+ / 5+**).
- Your ~5y clears typical senior YoE gates when ownership is visible.

### Languages
- **Java** is historically very common on LinkedIn backend (Play/Spring ecosystems in many teams).
- **Python**, **Scala**, **Go** appear on data/AI/infra postings.
- Recruiter reality: **Java-preferred teams** may still screen Python/Go seniors for adjacent teams; ask early “Is Java required?”

### Systems
- Large-scale distributed systems, service-oriented architecture
- Data pipelines, Kafka/streaming (strong cultural fit — LinkedIn originated Kafka)
- Caching, datastores, search (team-dependent)
- Cloud (Azure/AWS — team-dependent)

### Leadership
- Senior: mentoring, design influence, delivering multi-person projects
- Your led 3 / mentored 2 is relevant; frame as tech leadership not people management

---

## Keyword bank (2025–2026 patterns)

**High-signal for LinkedIn backend/data:**
`Java` (if learning — do not fake), `Python`, `Go`, `Kafka`, `stream processing`, `distributed systems`, `microservices`, `REST`, `gRPC` (only if true), `scalability`, `high throughput`, `data pipelines`, `PostgreSQL`, `Espresso`/`Venice`-style (do not name-drop internal systems you do not know)

**Reliability / member impact:**
`latency`, `availability`, `observability`, `feature ownership`, `A/B` (only if true), `API design`

**AI / modern:**
`LLM`, `agentic`, `recommendation` (careful — LinkedIn domain), `feature store` (only if true)

**Craft culture keywords:**
`code review`, `technical design`, `mentoring`, `operational excellence`

**Safe differentiators you actually have:**
`Kafka`, `FastAPI`, `Gin`, `ClickHouse`, `idempotency`, `DLQ`, `MySQL`, `design ownership`

---

## Pass vs borderline vs fail (this candidate)

### Pass
- Senior backend/data role where **Kafka + Python/Go + distributed systems** are listed.
- Resume shows **event-driven production** (Masters GST) + **service design ownership** (FRM).
- Mentorship/leadership present.
- Recruiter hears member/customer-oriented impact language.

### Borderline
- Core LinkedIn **Java service** teams with Java as hard filter — you may be routed elsewhere or asked about Java willingness.
- “Senior” with EPAM/vendor framing and weak product narrative.
- IA agentic story without systems backbone — LinkedIn may prefer platform/data engineers over app-AI generalists depending on team.

### Fail
- Faking Java years or LinkedIn-scale graph systems experience.
- Claiming Kafka “inventor-level” expertise from light usage.
- No evidence of production ownership or mentorship for senior reqs.
- Staff-level application with only feature scope.

---

## Highest-impact honest resume flips (no fake years)

1. **Kafka prominence:** Masters GST Kafka + idempotency/DLQ in skills **and** bullets — LinkedIn recruiters notice Kafka fluency.
2. **Distributed systems narrative:** throughput/latency improvements you can defend (Masters), not buzzwords.
3. **Design doc energy:** FRM layered architecture, 30+ APIs, schema ownership — reads as senior craft.
4. **Member/customer translation:** “enterprise clients / auditors / retail planners” → impact on users of systems.
5. **Go + Python** for polyglot services; mention willingness to ramp Java if targeting JVM teams (conversation, not fake resume skill).
6. **Leadership without manager title:** led 3 via design reviews/API contracts/CI.
7. **ClickHouse** for analytics/data platform postings; pair with “why append-only.”
8. **Trim consulting noise:** Uber problem first, EPAM employer second.

---

## Culture / behavior screen notes (LinkedIn / transformation)

LinkedIn culture themes (public engineering brand + interview reports):
- **Members first** — craft that serves professionals
- **Transformation** — continuous improvement, learning
- **Integrity** — honest claims, trustworthy systems
- **Collaboration** — “in it together,” cross-functional
- **Results / craftsmanship** — quality, operable services

**Also inherits Microsoft-adjacent professionalism** (growth mindset, inclusion) without being identical to Redmond Azure culture.

**Story mapping:**
| Theme | Hooks |
|---|---|
| Members/customers first | Who used FRM outputs; planner time; GST client reliability |
| Transformation | Monolith→microservices; Sheets→MySQL; agentic planning tools |
| Integrity | Read-only agent tools; audit correctness; no fake metrics |
| Collaboration | Pod leadership; stakeholder API contracts |
| Craft | Tests, CI gates, observability |

**Phone tip:** Ask which org (Flagship, Data, AI, Infra). Tailor: Kafka/data → Masters+CH; product backend → FRM; AI → IA with systems anchors. Be explicit about **Java gap** if asked — honesty beats discovery mid-loop.
