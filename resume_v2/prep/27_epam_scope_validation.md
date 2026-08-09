# EPAM / Uber scope validation

**Date:** 2026-07-27  
**Sources:** `GROUND_TRUTH.md`, FRM code dump + TDD, `11_uber_frm_deep_dive.md`, `23b_uber_interview_packs.md`, Menu HISTORICAL ops  
**Purpose:** Answer CTO/EM red flag — “via EPAM = fake Uber ownership?”

## Verdict

| Claim | Validated? | Confidence | How to say it |
|---|---|---|---|
| Employed by **EPAM**, embedded on **Uber Finance / Menu** products | **YES** | High | “SDE2 at Uber via EPAM (staff aug)” |
| **Uber FTE / people manager** | **NO** | High | Never claim Uber employee or perf reviews |
| **Tech lead of 3-engineer EPAM pod** | **YES** (user-confirmed + code conventions) | High | Design reviews, API contracts, Bazel CI gates |
| **Owned FRM scoping service design + recon v2 migration** | **YES** (code + branch + migration doc) | High | Personal branch `tmitta1/recon-income-api-migration` |
| Owned **HFM ETL** end-to-end | **NO** | High | “Service consumes HFM-loaded MySQL; ETL was shared” |
| Owned **frm-collaboration-service** (Slack/collab) | **NO** | High | Separate service — don’t claim |
| **70% recon cut measured** | **NO** — TARGET only | High | “Targeting 70%…” |
| Menu **$600K / 24h→2h / 98% fidelity** | **HISTORICAL** (past resume + ops) | Medium | Defend as Menu work on same employment; offline eval honesty |
| Menu Kafka/Flink **peak TPS measured** | **NO** | High | Burst/replay/keyed dedupe defense; ESTIMATED peaks |

**Panel answer:** Scope is **real IC ownership inside Uber product + monorepo**, with **employer = EPAM**. Not inflated “Uber Staff.” Not ticket-only if you can walk FRM code (layers, recon migration, 1,100+ tests).

---

## Employment facts (canonical)

| Field | Truth |
|---|---|
| Employer | **EPAM Systems** |
| Client / product | **Uber** (Finance FRM + Uber Eats Menu) |
| Title | Software Engineer **A2 / SDE2** |
| Dates | **Jul 2024 – May 2026** (~1.9y) |
| Location | Bangalore |
| Resume line | `UBER (via EPAM Systems)` — keep this; do not hide EPAM |

---

## What was actually owned (FRM) — evidence-backed

| Area | Evidence | Ownership level |
|---|---|---|
| Platform: FastAPI + MySQL + React (Fusion.js), 8 screens, **30+ REST APIs** | Code: ~32 routes incl. health; TDD | **Primary backend owner** of scoping service |
| **11-table** SQLAlchemy 2.0 schema | `database/models/` | Design + implementation |
| Layered handler → service → repository | Uniform across codebase | Set/enforced conventions for pod |
| Recon v1 Sheets → v2 MySQL | `RECON_API_MIGRATION.md`; **18 files, +1,268 LOC**; branch under your id | **Personally owned migration** |
| Auth via gateway `x-auth-params-email` | Middleware pattern in code | Implemented in service |
| Tests **1,100+** (grep ~1,288 `def test_`) | Bazel `uber_py_test` | Grew suite + CI gate |
| Materiality **$340M** / residual **$170M** | Q4 2025 sample CSVs | MEASURED sample, not eternal constants |
| Feeds **PwC** work papers | Product purpose / TDD | Platform output; you didn’t “work at PwC” |
| Led **3 engineers** | User-confirmed EPAM pod | **Tech lead**, not manager |

### Explicit non-ownership (say out loud if probed)

1. **HFM ETL pipeline** — shared; you consume loaded tables.  
2. **Collaboration / Slack service** — separate repo.  
3. **Uber org design review board as FTE** — you worked in EPAM+Uber stakeholder cadence (PM/Finance); don’t invent ARB membership.  
4. **People management** — no Uber/EPAM perf reviews of the 3 as “my reports” in HR sense.  
5. **Measured 70% time save** — TDD target only.

---

## What “led 3” means (validated framing)

**Safe one-liner:**  
“I was tech lead of a **3-engineer EPAM pod** on Uber Finance FRM — not a people manager. I sliced work by layer, enforced API/ORM conventions from backend syncs, and gated merges on Bazel tests.”

**Concrete actions (prep-backed):**

- Task split along handler / service / repository / model so two people could ship one feature without merge wars (recon migration is the example).  
- Conventions: thin handlers; services own trees; repos own sessions; `updated_by` from auth header; `asyncio.to_thread` for blocking DB.  
- Review gate: tests + `uber_py_test` before merge → suite to 1,100+.

**Fail answer:** “I managed three Uber engineers and owned the Finance org roadmap.”

---

## Menu (same employment) — scope honesty

| Claim | Tag | Interview rule |
|---|---|---|
| Same EPAM→Uber engagement | HISTORICAL role | OK to discuss as second Uber product |
| 30K+ menus/mo, 24h→2h, $600K+/yr, 95%+ ingest | HISTORICAL ops | Keep; don’t invent new TPS |
| RAG + Gemini + SFT 98% / 100% schema | Offline eval | Say offline, not online A/B |
| Kafka + Flink on PDF (post-Flink update) | HISTORICAL / ESTIMATED rates | Defend **burst, replay, keyed dedupe** — not vanity TPS |

---

## How recruiters / CTO should hear it

| Bad packaging | Good packaging |
|---|---|
| “I worked at Uber” (implies FTE) | “SDE2 on Uber FRM **via EPAM**” |
| “Led Uber’s Finance eng team” | “Tech-led **EPAM pod of 3** on FRM” |
| “Built Uber’s entire audit stack” | “Owned **FRM scoping service** + recon migration; feeds PwC work papers” |
| Hide EPAM | Lead with **product problem + ownership**, EPAM as employment vehicle |

Amazon recruiter guidance already matches this: EPAM secondary; product + owned design primary.

---

## Reference-check questions (what would validate)

Ask an EPAM lead / Uber PM peer:

1. Who owned the recon Sheets→MySQL migration and the SQLAlchemy schema?  
2. Did Tarun set review/CI standards for the pod?  
3. Was he presenting progress to Uber Finance stakeholders or only EPAM internal?

If answers align with migration doc + backend sync notes → **scope validated**. If “he only took tickets under Uber Staff design” → **downgrade “owned design” language**.

---

## Score: EPAM risk after validation

| Dimension | Score | Note |
|---|---|---|
| Honesty of employment framing | **9/10** | “via EPAM” on resume is correct |
| Hands-on FRM depth | **8/10** | Code + migration doc strong |
| Leadership claim accuracy | **7/10** | Solid if “pod TL”; fails if “manager” |
| Outcome metrics honesty | **8/10** | 70% TARGET correctly worded on good resumes |
| Inflated Uber brand risk | **Mitigated** | If verbal matches this doc |

**CTO condition still stands:** advance to rounds; **offer only after** EPAM-scope story holds in interview (and IA exit narrative is clean). Scope itself is **defensible**, not fabricated — if you stay inside the guardrails above.
