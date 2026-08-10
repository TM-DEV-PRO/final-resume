# Hindsight Module Defense (resume bullet)

**Source:** `KNOWLEDGE-MATERIAL/Impact-Analytics-work/PRD'S/Hindsight_Module_Functional_Requirements-2.docx` (v1.2)

## Resume claim (campaign PDF)
Building **Hindsight** as the prior-season decision layer with carry-forward and underperformance flags plus Keep/Shop/Drop recommendations, overnight narration checked against computed metrics, and tenant metric catalogs that go live without a code deploy.

## Why this is impactful (say this first)
Hindsight is the **first stage** of AssortSmart planning (hindsight → strategy → clustering → line plan → buy). Planners do not invent next season blind — they see **what worked / what failed last season**, which styles to **Keep / Shop / Drop**, and what to **carry forward**. That is buying-decision support, not a dashboard vanity project.

## Product surface (FRD v1.2)
Scorecard (TY vs LY / Optimised LY), contribution charts, store performance map, configurable bar charts, top performers, By Item grid, By Attribute heatmap, **Carry-Forward / What Didn't Work** panel, agent narration.

## FR mapping to resume words

| Resume phrase | FR | Why it matters |
|---|---|---|
| Prior-season decision layer | Overview + pipeline position | Hindsight exists so next-season buys are evidence-based |
| Carry-forward and underperformance flags | **FR-6.1** | Surfaces candidates and underperformers with **metric values beside narration** — never narration alone. Threshold user-personalizable within tenant bounds |
| Keep/Shop/Drop recommendations | **FR-16.5** | Item grid keeps existing Keep/Shop/Drop recommendation + per-item note; same grounding/fallback as other narration |
| Overnight narration checked against computed metrics | **FR-2.3, FR-4.3, FR-5.3, FR-8.1** | Batch overnight (not live). Shared **template library** driven by metric metadata. **Numbers checked before save**; fail → templated sentence. No invented KPIs |
| Deterministic visuals (verbal depth) | **FR-9.1** | Chart type/color/icons from config only — **narration agent never chooses layout** |
| Permission-scoped filters (verbal) | **FR-0.1–0.5** | One global product/location/season filter; "select all" never leaks outside permission scope |
| Shared metric catalog (verbal) | **§1.2, FR-1.1** | One catalog for scorecard, bars, item, attribute — no per-widget metric lists |
| Tenant catalogs without a code deploy | **FR-1.3** | Onboarding config (catalog + chart instances) applies to all tenant users **without a code deployment**; changes versioned with last-updated |
| Item grid at scale (verbal) | **FR-16.6** | Stay fast at **1,000+ items** via pagination / virtualized scrolling |

## Engineering judgment to defend
1. **LLM is not the visual designer** (FR-9.1) and **not the metric calculator** (grounding check).
2. **Batch overnight narration** avoids latency/cost spikes on every filter change (live narration is Phase 2 only for special cases).
3. **Config vs code** — new retailer metrics/charts = data/config, not a release train.
4. **Multi-tenant safety** — permission scope on every widget including map and item grid.

## Honesty
- Status: **building** against FRD (AssortSmart Phase-1 posture). Do not claim fully shipped to all tenants.
- Keep/Shop/Drop is **retained existing** recommendation behavior per FR-16.5 — you are hardening/shipping it inside the Hindsight module surface, not inventing a brand-new model claim without evidence.
- No $ or latency KPI in FRD for Hindsight alone — do not invent. Pivot/CH speed numbers stay on the ClickHouse bullet.

## 60-second talk track
"Hindsight is how planners learn from last season before they buy this season. I am building it as a decision layer — carry-forward and underperformance flags, Keep/Shop/Drop on the item grid, scorecard and contribution views — with permission-scoped filters and a shared tenant metric catalog that goes live without a code deploy. Agent narration runs overnight from a shared template library and is checked against computed numbers before save, and chart visuals stay deterministic so the model cannot invent layout or KPIs."

## Likely questions
**Q: Does the agent invent metrics?**  
A: No. Narration is checked against computed numbers before save (FR-2.3). Fail closed to a template sentence.

**Q: Why overnight not live?**  
A: v1 deliberately batches narration (Section 13). Live/on-demand is Phase 2 for narrow cases (FR-11.1) with the same grounding check.

**Q: What is Keep/Shop/Drop?**  
A: Per-item recommendation retained on the By Item grid (FR-16.5) with a note, grounded like other narration — guides assortment actions for the next plan.

**Q: How does this relate to ClickHouse?**  
A: Hindsight/pivot-style reads are scan-heavy; the CH planning store and pivot POC defend the read latency. Hindsight FRD is the product contract; CH is the serving engine.
