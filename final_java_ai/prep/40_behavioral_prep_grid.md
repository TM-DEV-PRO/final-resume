# Behavioral prep grid — project × question

**Track:** Final Java + AI · **PDF:** `Tarun_Mittal_SSE_Java_AI_Final.pdf`

Inspired by the Cracking-the-Coding-Interview-style grid recommended in
[awesome-behavioral-interviews](https://github.com/ashishps1/awesome-behavioral-interviews).
Fill one cell before each loop. Keep answers to 4 bullets: **S / T / A / R** (plus tag).

Stack on this track: FRM = **Spring Boot / MySQL** · writes = **Spring Boot** · agent = **Python FastAPI + LangGraph** · Masters = **Spring Boot strangler**.

Full answers live in [`07_behavioral_star_stories.md`](07_behavioral_star_stories.md) and
[`39_behavioral_question_bank.md`](39_behavioral_question_bank.md). This sheet is for recall drill.

---

## How to use

1. Pick the company → open `company_behavior_guides` (or Amazon/Google rows in §1 of `39`).
2. Pick 2–3 stories you will allow yourself in that loop — mark them below.
3. For each project column, jot a 1-line S and the number you will say.
4. After the interview, mark cells you actually used so you never repeat in a follow-up.

---

## Grid

| Question theme | IA Copilot / CH / Hindsight | Uber FRM | Uber Menu | Masters India | GFG |
|---|---|---|---|---|---|
| Ownership / end-to-end | Arch owner; writes=Spring Boot; agent=Python FastAPI + LangGraph; CH POC 189s→12.3s MEASURED | 30+ APIs, 8 screens, $340M, led 3 | Selenium→Kafka→Flink→RAG gate; 24h→2h; $600K+/yr | Spring Boot strangler; 1M+/day; mentored 2 | Django reliability |
| Disagreement / backbone | Story 1 CH camps | Story 7 ORM vs repository | — | Sequencing debates | — |
| Failure / mistake | — | Story 5 constants refactor | Early anti-bot misses | Story 10 near-miss | — |
| Dive deep / debug | Schema choice×cluster×week | Story 6 coverage lie | Block-rate instrumentation | Idempotency class bug | — |
| Deadline / pressure | Design targets (TARGET) | PwC-facing release trains | Partner onboarding SLA | GST deadline freeze cutovers | — |
| Customer / stakeholder | Planner UX inversion (story 4) | G6 PwC materiality rules | Partner menus multilingual | Enterprise filers 1,500+ | — |
| Mentorship / feedback | — | Led 3 via contracts | — | Mentored 2; G4 feedback | — |
| Initiative / prevention | CH PoC; freshness lane (story 2) | Recon v2 design | Schema gate before catalog | Idempotency + DLQ | — |
| Ambiguity / incomplete info | Story 1 gates; story 4 intent-only inputs | Materiality encoding | Adversarial sources | Peak vs migration sequencing | — |
| Ethics / trust | Human gates before writes | Audit reproducibility | Low-confidence → human review | Story 10 raised near-miss | — |
| Why this work matters | MEASURED 8.5% failure baseline | Finance system of record | $600K+/yr ops | Compliance filings | Learning foundation |

---

## Per-project one-liners (memorize)

**IA — AssortSmart Cluster Recommendation Copilot**  
Building (not shipped). Agent plane Python FastAPI + LangGraph; write APIs Spring Boot; Hindsight; ClickHouse insert-only planning store; 250M-row POC 189s→12.3s (~15.5×) MEASURED; clustering failure baseline 8.5% (37/437) MEASURED; <1h / <2% are TARGET.

**Uber FRM (via EPAM)**  
Spring Boot / MySQL; 30+ REST APIs; 8 screens; $340M materiality; ~55×14; led 3; 70% recon cut = TARGET.

**Uber Menu (via EPAM)**  
Python · Selenium · Kafka · Flink · LangChain · Gemini · RAG · Milvus · GCP. 24h→2h; $600K+/yr; 30K+ menus/mo; 95%+ ingest; 98%/100% offline eval. No Spark. No SFT.

**Masters India**  
Spring Boot strangler; Kafka IRP 1M+/day; p95 1.2s→300ms; 700→4,000 req/min; 1,500+ clients; mentored 2; ELK/New Relic triage ~70% faster HISTORICAL.

**GeeksforGeeks**  
Django reliability / early career — use only if asked for first job; keep short.

---

## Loop checklist (print this)

- [ ] 2–3 stories pre-chosen for this company
- [ ] Numbers tagged MEASURED / TARGET / HISTORICAL
- [ ] Uber = via EPAM said once
- [ ] Copilot = building said once
- [ ] Masters Kafka ≠ Menu Kafka
- [ ] 3 reverse questions picked from `39` §4
- [ ] No LeetCode / Spark / SFT / Design-Patterns-as-Skills claims
