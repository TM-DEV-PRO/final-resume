# Formula audit — action verb + what I did + measurable result

Every bullet checked against the Achievement Rewriter formula. **16 of 23 comply fully. 7 carry a *scope* number where a *result* belongs** — those are flagged `[ADD METRIC]` below with the specific number that would fix each and where to source it.

Note: `[ADD METRIC]` markers are **not** in the PDFs. Putting placeholder text on a resume you might send is a worse failure than a missing metric, and I will not invent numbers to fill them — that's exactly the fabrication problem we spent this session removing. Get the real figures and I'll wire them in.

---

## Verb audit — passed

Opening verbs across the whole document, no repeats within a section:

- **Impact Analytics:** Own · Hold · Gated · Built · Locked · Shipped · Blocked · Cut
- **Uber FRM:** Owned · Moved · Encoded · Led
- **Uber Eats:** Cut · Turned · Raised
- **ANZ:** Reached
- **Masters India:** Brought · Lifted · Made · Cut
- **GeeksforGeeks:** Stabilized · Lifted · Raised

Fixed in this pass: three Impact Analytics bullets all opened with "Built" (→ Gated, Built, Blocked). No weak constructions remain — no "Responsible for", "Worked on", "Helped with", "Participated in", "Involved in".

---

## The 7 bullets missing a measurable result

| Bullet | What it has now | What's missing | `[ADD METRIC]` — get this number | Where to source it |
|---|---|---|---|---|
| **IA-1** Own the Go service | 36 routes, 8 modules — that's **scope**, not outcome | No result at all. A recruiter learns the service is *big*, not that it's *good*. | **Requests/day or peak RPS**, **number of live tenants**, and ideally **uptime %** or **p99 latency**. "36 routes serving N requests/day across N tenants at 99.9% uptime" is a different bullet entirely. | Datadog APM — you already run it with the profiler. Tenant count from `user_master` / the kik+briscoes configs. |
| **IA-3** Gated every request behind auth | Zero numbers | Entirely descriptive. Strongest security bullet on the page and it has no result. | **Requests/day through the auth middleware**, **users/tenants covered**, or **auth overhead in ms at p99** (a low number here is a genuine engineering result). | Datadog trace on the auth middleware; row count in `user_master`. |
| **IA-5** Locked agents out of writing | 2.11B rows (scale), six layers (mechanism count) | No outcome. Six layers is impressive engineering with no stated consequence. | **"Zero write incidents across N production runs"** — this is the killer version. Also viable: **N agent queries served with 0 policy violations**. | Count run dirs in `assort_kd_flow/logs/`; `tool_calls.csv` per run gives query counts. |
| **IA-6** Shipped a read-only assistant | Zero numbers | Purely descriptive — reads like a feature announcement, not an achievement. | **Planners actively using it**, **questions answered/week**, or **median time-to-answer vs. manually digging through the data**. | PostHog (you have it instrumented) or LangSmith traces. |
| **FRM-2** Moved recon off Sheets into MySQL | 18 source files — **scope** | No outcome. Migrating 18 files isn't a win; what the migration *bought* is. | **Reconciliation error rate before/after**, **audit-prep time saved per close**, or **line items reconciled per quarter**. | `RECON_API_MIGRATION.md`; the Q4 recon CSVs in `KNOWLEDGE-MATERIAL/UBER-WORK/FRM PROJECT/KT&DOCS/`. |
| **FRM-3** Encoded the materiality rules | ~55 line items × 14 entities — **scope** | No outcome. | **The multiplication is your metric: ~55 × 14 ≈ 770 in-scope decisions automated per quarter.** That's derivable from what you already have and far stronger than the current phrasing. Better still: **analyst hours saved per close**. | Arithmetic on figures already in `18_resume_number_catalog.md`. |
| **FRM-4** Led 3 engineers | 3 (team size) — **scope** | Leadership with no result attached. | **On-time delivery of N quarterly closes**, **design-review turnaround**, or **N API contracts owned**. Even "shipped N consecutive quarterly closes on schedule" works. | Your own recollection; `Notes - FRM CT Backend Team Sync.docx`. |

---

## One existing metric worth upgrading

**FRM-1** says *"**targeting** a 70% cut in manual reconciliation, from about 2 weeks to 3–4 days."*

That word is honest — your `18_resume_number_catalog.md` tags the 70% as `TARGET + ESTIMATED` — but a recruiter reads "targeting" as "didn't happen." If the platform has now run a real quarterly close, **the achieved number replaces the target and becomes one of the strongest lines on the resume.** If it hasn't, leave "targeting" exactly as it is.

---

## Priority order

If you only chase three numbers, chase these:

1. **IA-5 — "zero write incidents across N runs."** Converts your most sophisticated engineering work from a mechanism list into a reliability claim. Cheapest to source.
2. **IA-1 — requests/day + tenants.** Your current role's headline bullet currently proves size, not quality. This is the bullet a Google Cloud interviewer reads first.
3. **FRM-3 — ~770 decisions/quarter.** Pure arithmetic on numbers you already own. No lookup required.

Everything else is upside.

---

## Aside on the prompt list

Prompts **#3 "The Weak Verb Killer"** and **#4 "The Achievement Rewriter"** in your source list contain *identical* prompt text — looks like a copy-paste slip in whatever you copied them from. The intended #3 was presumably about replacing weak verbs specifically (Responsible for / Worked on / Helped with), which is audited above and passes. #5 "The ATS Optimizer" is covered in `SCORECARD.md` Part 2, and #1 "The Brutal Audit" in Part 1.
