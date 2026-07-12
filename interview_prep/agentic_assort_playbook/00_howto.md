# Agentic Assort Planner — Resume & Interview Playbook

<div class="stage-badge stage-obs">Senior SWE · Python + AI/Agents + Data · grounded in your own repos, PoC & audit — July 2026</div>

This is a single place to (1) copy **resume-ready bullets** for the **Agentic Assort Planner** project, (2) understand the **detailed backing** for every claim — the *why*, the *tradeoffs*, the *decision path*, the *impact* — and (3) walk into an interview able to defend the **architecture, databases, AI/agent design, and every technology named**, down to fundamentals. Written for a **senior software engineer (Python + AI + data)**.

## How to use this doc
- **§1** — the project one-liner + summary blurb (paste at the top of the project).
- **§2** — the **XYZ resume bullets** (pick 5–8), each followed by a **backing block** (how/why/tradeoff/impact/evidence/honesty).
- **§3** — **product architecture (HLD)** — the agentic planning workspace + agent orchestration.
- **§4** — **database architecture (HLD + LLD)** — three-tier spine, the tenant-unified derived schema, and the ClickHouse insert-only/versioned design.
- **§5** — **per-technology deep dives** — fundamentals · architecture · how it solves the problem · gotchas, for every tech you'd list.
- **§6** — **interview Q&A** — the questions an engineering manager / architect will ask, with model answers.
- **§7** — **talking tracks + honesty guardrail** — 30-sec / 2-min / deep pitches, STAR stories, and exactly which numbers are real vs indicative.
- **§8** — **authoritative product specifics** from the requirements notebook (stack, autonomy bands, ClickHouse PoC numbers).
- **§9** — **the Cluster Recommendation Copilot** — the agentic clustering module now in build (FRD v1.8): what/why/how, measured baselines, targets, and its own Q&A. This is your *present-tense* flagship — the answer to "what are you working on right now?"
- **§10** — **the July 2026 stack direction (authoritative)** — Go/Gin for non-agentic flows, Rust for profile-proven hot paths, agentic tier unchanged, and **ClickHouse end-to-end (transactional + analytical)** via the insert-only/versioned write model. Where §4/§5 describe Postgres as the planning system-of-record, read them as decision history; §10 is the current stance.

## The format: Google's XYZ formula
Every strong bullet follows **"Accomplished [X], as measured by [Y], by doing [Z]"** — X = the outcome, Y = the metric, Z = the method/tech. Lead with impact, quantify it, then name the technique. For a *senior* role the narrative is **"I architected systems and multiplied team output,"** not "I wrote code" — so bullets emphasize design decisions, cross-system tradeoffs, cost/latency wins, and de-risking. Structure the résumé as a 2–3 line summary, then 5–8 quantified XYZ bullets per project. (Sources: Wonsulting, Teal, IGotAnOffer — linked at the end.)

<div class="callout warn">
<b>Honesty guardrail — read before you paste.</b> Keep only what <b>you personally</b> did; this doc is scoped to work evidenced in your repos/PoC/audit, but you must still own each line in the room. Two tiers of numbers appear here:
<ul>
<li><b>REAL (defend as measured):</b> the BigQuery cost figures (≈3× / 74× / 280× / 880×; the 38.8 TiB / $327 <code>SELECT *</code> leak), the Postgres audit facts (88% orphaned optimizer rows; 5,503 partitions for 298K rows), and the catalog verification (5,385 columns, 46 FKs) — these come from the <b>live mtp audit + read-only metadata</b>.</li>
<li><b>INDICATIVE (frame as "in an offline eval" / "design target"):</b> the decomposition score 0.54→0.99, and the PoC latency/seed/pivot milliseconds — these are <b>mock / pure-Python</b> harness results measuring <i>structure & correctness</i>, not production model accuracy or real-engine latency. The load-bearing PoC result that IS real is the <b>architecture property</b>: <code>mutations_used = 0</code> at every scale.</li>
<li><b>FRD (Cluster Copilot, §9):</b> two sub-tiers — <b>measured baselines</b> from live tenant audits (8.5% run failures = 37/437; 0% reproducibility; median job ≈20 s over 370 runs; 1-in-5 finalized plans with zero stores) which you defend as "measured on live tenants," and <b>committed targets</b> (<1 h to finalized plan, ≥20 configs, <2% failures, p95 <500 ms) which you frame as "the design targets we set and are building against."</li>
</ul>
Say "in an offline evaluation" or "modeled/projected" for the indicative ones and you'll never be caught out.
</div>

<div class="callout warn">
<b>Final-resume alignment (July 2026).</b> The shipped resume diverges from this playbook in three deliberate ways: (1) the <b>BigQuery cost program (§2 P1–P2) is NOT on the resume</b> — treat it as platform history/context only, never claim it as your delivery; the resume bullet is the <b>BigQuery→ClickHouse ingestion pipeline</b> (see the final-resume project file §3c). (2) <b>Rust appears on the resume only in the Skills line</b> (Languages: Python, Go, Java, C, C++, Rust, SQL) — there is no Rust project bullet; if asked, frame it as the team's designated escape hatch for perf-critical APIs that Go can't hit, per the July 2026 stack direction. (3) The resume shows <b>one project block</b> ("Agentic AssortSmart") with five bullets: agentic rebuild overview, Python agentic microservice (clustering agent, 3–5 ranked scenarios), Go (Gin) core backend, ClickHouse append-only versioned store, planning grid backend (p95 &lt;500ms, edits &lt;80ms). When a playbook talking track conflicts with these, the resume framing wins.
</div>
