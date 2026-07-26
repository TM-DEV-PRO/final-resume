# Google Technical Recruiter Screen

## Typical titles and levels

| Target title | Level | Typical external hire YoE (community + posting patterns) | Fit |
|---|---|---|---|
| Software Engineer | L3 | New grad / early career | Too junior |
| Software Engineer | **L4** | ~2–5y industry; feature ownership | **Primary / realistic** |
| Senior Software Engineer | **L5** | ~5–8y+; system ownership, ambiguity, multi-team | **Stretch** — possible if packet emphasizes design ownership + leadership |
| Staff Software Engineer | L6 | Org-level technical leadership | Not a fit yet |

**Practical targeting:** Ask recruiter for **L4 with L5 consideration** only if they open that door. Self-pitch **L4** as the honest bar; use FRM design ownership + led 3 as **uplevel signals**, not as a demand for L5.

**Title map:** Impact Analytics “Senior SWE” ≠ automatic L5. Google levels by **scope**, not title.

---

## Hard requirements recruiters check

### Years of experience
- L4: industry experience owning features end-to-end (~2–5y common).
- L5: sustained ownership of larger systems, mentoring, driving design under ambiguity.
- Degree: CS or equivalent; non-CS possible with strong coding signal (hiring committee cares more than recruiter).

### Languages
- Postings often list **C++, Java, Python, Go**, sometimes JavaScript/TypeScript.
- Your **Python + Go** clears language gates for many backend roles.
- Recruiter note: Google still weights **coding interview readiness** higher than stack match — “Do you code daily in a mainstream language?” is the real gate.

### Systems
- Distributed systems fundamentals, APIs, data stores, caching, async processing.
- Domain teams may want: streaming, storage, ML infra, ads, etc.
- **ClickHouse / Kafka** help domain match (data/analytics/platform) but do not replace algo readiness.

### Leadership
- L4: feature ownership, collaboration, mentoring juniors (nice).
- L5: tech leadership, mentoring, cross-team influence expected in stories.

---

## Keyword bank (2025–2026 patterns)

**Core ATS / recruiter skim:**
`Python`, `Go`, `distributed systems`, `scalable`, `APIs`, `microservices`, `data structures`, `algorithms` (implied by SWE role), `production`, `reliability`, `latency`, `throughput`

**Systems design vocabulary (resume + screen talk track):**
`sharding`, `caching`, `consistency`, `idempotency`, `pub/sub`, `message queues`, `Kafka`, `PostgreSQL` / `MySQL`, `observability`, `SLO` / `SLA` (only if you can discuss honestly)

**Data / AI adjacent (IA story):**
`ClickHouse`, `analytical store`, `agentic`, `LLM tools`, `LangGraph` / `MCP` (team-dependent — great for AI/infra-adjacent; neutral for classic SWE)

**Leadership:**
`tech lead`, `mentored`, `design reviews`, `API contracts`, `cross-functional`

**Prefer not to overclaim:**
`Kubernetes operator`, `multi-region active-active`, `planet-scale` — Google interviewers punish vague scale claims.

---

## Pass vs borderline vs fail (this candidate)

### Pass — L4 screen-in
- Clear ~5y progression with increasing ownership (GFG → Masters → Uber FRM → IA).
- Production Python/Go + concrete systems (APIs, MySQL, Kafka, CH).
- One crisp ownership story (FRM design) + one scale/reliability story (Masters GST).
- Recruiter hears: “I own end-to-end features/systems and can pass coding + light/medium design.”

### Borderline — L5 ask / packet
- ~5y with strong design ownership can be **L5-eligible** on some teams, but many recruiters will **anchor L4**.
- Vendor/client employment (EPAM@Uber) without product framing → “contractor” bias.
- Agentic AI focus without CS fundamentals signal → “ML tinkerer” misread for general SWE.
- Thin algorithm practice signal (resume can’t prove LC; recruiter may ask about interview prep readiness).

### Fail
- Demanding L5/L6 based on title alone.
- Invented Google-scale metrics.
- Cannot commit to coding interview timeline / poor self-assessment on DSA.
- Resume full of tools, empty of ownership verbs (“participated,” “exposed to”).

---

## Highest-impact honest resume flips (no fake years)

1. **Scope language for L4→L5 signal:** “Owned architecture and delivery of FRM Risk Scoping…” not “worked on Uber project.”
2. **Quantify only defended numbers:** FRM APIs/schema/tests; Masters latency/RPM/txn; IA one CH measured speedup — drop unsupported GL row myths.
3. **Put Go next to Python in skills + IA doing-layer** — Google likes multi-language production.
4. **Kafka + fault tolerance on Masters** as distributed-systems proof.
5. **Mentorship as Googleyness fuel:** mentored 2 / led 3 with *how* (design reviews, contracts, CI).
6. **Agentic AI: engineering constraints** (read-only tools, human confirm gates, observability) — shows judgment.
7. **Remove or demote** anything you cannot whiteboard (K8s ops, Terraform, multi-region DR).
8. **Education line clean** — degree + years; no CGPA inflation games.

---

## Culture / behavior screen notes (Googleyness & Leadership)

Google G&L (and related attributes) typically probe roughly:
- **Doing the right thing / ethics**
- **Helpfulness / collaboration**
- **Comfort with ambiguity**
- **Conscientiousness / follow-through**
- **Growth mindset / learning**
- **Humility + confidence balance**

**Map your stories:**
| Signal | Honest story hooks |
|---|---|
| Ambiguity | Sheets→structured FRM platform; IA Copilot from PRD ambiguity |
| Collaboration | EPAM pod + Uber stakeholders; API contracts |
| Mentorship | Masters mentored 2; Uber led 3 |
| Judgment | Agent never writes SQL; human gates; CH append-only vs OLTP |
| Learning | Go adoption; agentic stack; CH for planner analytics |
| Impact without ego | Prefer “we shipped X; I owned Y” |

**2025–2026 process notes (public candidate reports):** coding remains decisive; system design common at L4+ (lighter than L5); some process steps (assessments) appear before onsite — treat recruiter instructions as source of truth.

**Phone tip:** Google recruiters care that you **want Google for the problem space**, can relocate/hybrid per role, and will prepare for coding. Do not oversell L5.
