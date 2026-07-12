---

# 7. Talking tracks, tailoring & honesty

## 7.1 Three pitch lengths
**30 seconds:** "I build the AI and data backbone of an agentic retail assortment planner — right now the store-clustering copilot: the planner states what to cluster and for when, a dedicated agent handles scoping, attribute selection and a 20-to-100-configuration exploration on a dedicated ClickHouse read plane, with evidence packs and three human approval gates. It's spec'd against measured baselines — 8.5% run failures, one config tried per plan, zero reproducibility — with targets of under an hour to a finalized plan and sub-500 ms agent probes. Under it sits a three-tier data architecture (BigQuery, Postgres, ClickHouse/DuckDB) I designed, and a BigQuery cost program that cut recurring scan cost up to ~280×."

**2 minutes:** add the *why* — clustering is the foundation of every strategy plan yet the least assisted step (the system computed attribute significance and then ignored it); the workflow inversion (human states intent, agent derives everything derivable, human confirms at gates and injects pins); the governance ladder (copilot → autopilot-with-approval → drift monitor; nothing auto-finalizes; content-addressed config documents make every shipped clustering reproducible); two workloads in one product (OLTP-with-pivot + OLAP) → three tiers; the ClickHouse insight (edit = insert-a-version → mutation queue stays at zero → undo/diff for free); the agent orchestration (router → decomposer → validated DAG → parallel specialists → synthesize, with a structural validator that fixed the #1 LLM failure); and the staged decision gate that de-risked the migration.

**Deep dive:** walk §9 (the copilot — measured problem → inversion → architecture positions → doorway), then §4 (DB LLD) and §3 (agent DAG), then the numbers in §2 (real vs indicative), then the tradeoffs in §6.3.

## 7.2 STAR stories (ready to tell)
- **S/T:** Team split on whether the new planner should adopt ClickHouse; a live audit said "no," a SME push said "yes." **A:** Separated facts from conclusions, showed the objection was about legacy in-place-update code, designed an insert-only/versioned model + a 3-gate decision. **R:** Agreed, measurable path; PoC proved zero mutations at 10×; no premature infra spend.
- **S/T:** Hindsight/pivot reads were slow and BigQuery spend was high. **A:** Audited scan patterns; routed to clustered copy, built a rollup, added a cost-guard. **R:** up to ~280× fewer bytes; caught a 38.8 TiB / $327 leak; codified as a guardrail.
- **S/T:** LLM planners produced malformed multi-step plans. **A:** Added a structural DAG validator + one self-repair pass + `<A_n>` dependency passing. **R:** decomposition 0.54→0.99 in an offline eval; graceful partial answers on agent failure.
- **S/T:** Clustering — the foundation of every strategy plan — was the least assisted step: 1 config tried per plan, 8.5% of runs failing on avoidable input errors, nothing reproducible, planner swaps silently erased. **A:** Spec'd and started building the cluster-recommendation copilot: intent-only input, deterministic grounding, batch exploration on a dedicated ClickHouse read plane, evidence packs, three gates, pins as durable constraints, content-addressed config documents. **R:** committed targets — <1 h to a finalized plan, ≥20 configs, <2% failures, 100% reproducibility, p95 <500 ms probes — with write-back into the existing product unchanged.

## 7.3 Tailoring to the JD
- **AI/ML-platform role** → lead with C1 + C3 + A1–A4 + §5.5/5.6 (the shipping copilot, deterministic grounding, orchestration, decomposition, text-to-SQL, RAG, confidence).
- **Data/infra/DB role** → lead with C2 + D1–D4 + P1–P3 + §4 (dedicated ClickHouse read plane, three-tier spine, insert-only ClickHouse, cost program).
- **Backend/platform role** → lead with D1, A2, P3 + §5.7/5.8 (Rust API boundary, async, Redis, streaming, Cloud Tasks).
- **Staff/architect signal** → lead with C1 + C4 + L1 (a governed agentic system you own end-to-end, the reconciled verdict / decision gates) + the tradeoff answers in §6.3.
- **Agentic/AI-product role** → lead with C1–C5 wholesale + §9 (intent taxonomy, delegation levels, terminal-states contract, learning loops).
Keep the résumé to the 5–8 strongest for that JD; the rest live here for the interview.

## 7.4 Honesty guardrail (repeat — this protects you)
| Claim | Tier | Say it as |
|---|---|---|
| BigQuery ~3× / 74× / 280× / 880×; 38.8 TiB / $327 leak | **REAL** (live audit) | "measured" / "cut" |
| Postgres 88% orphaned rows; 5,503 partitions / 298K rows | **REAL** (audit) | "found / fixed" |
| Catalog verified: 5,385 columns, 46 FKs | **REAL** (metadata) | "verified" |
| `mutations_used = 0` at 1×/10× (insert-only works) | **REAL property** (PoC) | "proved the architecture property" |
| Decomposition 0.54 → 0.99 (+0.45) | **EVAL** (offline, mock model) | "in an offline evaluation harness" |
| Pivot/seed/edit milliseconds (1×→100×) | **INDICATIVE** (mock, pure-Python) | "modeled / kept interactive as it scaled" |
| ClickHouse PoC: **8–130 ms pivots / ~160 ms writes / ~140–200× vs Postgres / 250M rows** | **PoC benchmark** (requirements notebook) | "the ClickHouse PoC achieved …" (a PoC result, not a prod SLA) |
| ClickHouse sub-second on 900M rows; 4.5M rows/s | **CITED target** (team benchmark) | "the design target / cited benchmark" |
| Cluster baselines: 8.5% failures (37/437); 0% reproducible; 1 config/plan; median job ≈20 s (370 runs); 1-in-5 finalized plans zero stores | **REAL** (FRD live-tenant audit) | "measured on live tenants" |
| Cluster targets: <1 h to plan; ≥20 configs; <2% failures; p95 <500 ms; ≥60% top-3 acceptance | **FRD TARGET** (committed, in build) | "the design targets we set / are building against" |

Never present a mock latency as production throughput. When in doubt, name the harness. Also be ready to say clearly **what you personally built** vs. what you reverse-engineered/designed vs. what's team/prototype — interviewers respect the precision.

## 7.5 One-page résumé skeleton (fill with §2 bullets)
```
TARUN MITTAL — Senior Software Engineer (Python · AI/Agents · Data)
Summary: 2–3 lines — agentic systems + multi-engine data architecture; impact-first.

IMPACT ANALYTICS — Senior Software Engineer
Agentic Assort Planner — AI-assisted multi-agent retail planning platform
  • C1  agentic cluster copilot: intent → agent explores ≥20 configs, 3 gates [AI · flagship]
  • C2  dedicated ClickHouse read plane: probes 1–20s → p95 <500ms target     [Data/AI-infra]
  • A1  multi-agent decomposition + validated DAG (0.54→0.99 offline)         [AI]
  • D2  insert-only/versioned ClickHouse planning store (0 mutations)         [Data]
  • D1  three-tier data spine (BigQuery / Postgres / ClickHouse+DuckDB)       [Data/Arch]
  • P1  BigQuery cost ↓ up to ~280× (2.9 TiB→3.3 GiB); caught $327/2-row leak [Perf]
  • C4  reproducible clusterings (0%→100%) + pins + delegation-level autonomy [AI-governance]
  • L1  reconciled DB verdict → 3-gate decision that de-risked migration      [Leadership]
Tech: Python, FastAPI, asyncio · OpenAI/Gemini, LangGraph-style orchestration, RAG (pgvector,
  BM25+dense, Cohere rerank), text-to-SQL · BigQuery, PostgreSQL, ClickHouse, DuckDB, Redis ·
  Rust/Axum (adjacent) · GCP (Cloud Tasks/Scheduler, GCS, Secret Manager)
(8 shown — trim to 5–8 per JD; C-bullets are the present-tense flagship, A/D the platform, P/L the seniority.)
```

## Sources (résumé best-practice research)
- [The XYZ Formula — Wonsulting](https://www.wonsulting.com/job-search-hub/the-power-of-quantifiable-results-how-to-use-the-xyz-formula-to-supercharge-your-resume)
- [XYZ Method Resume — Teal](https://www.tealhq.com/post/xyz-resume)
- [Senior Software Engineer Resume Examples — IGotAnOffer](https://igotanoffer.com/en/advice/senior-software-engineer-resume-examples)
- [Software Engineer Resume in 2025 — NestCV](https://nestcv.com/blog/software-engineer-resume)

*Product/architecture facts are grounded in your own repos and study artifacts: `agentic_assort_multiagent/`, `db_architecture_poc/` (+ `results/*.json`), `docs/01–07`, `product_artifacts/`, the AssortSmart data deep-dive / performance-findings deliverables, and the **Agentic Cluster FRD v1.8** (+ companion HLD/LLD) for the clustering copilot (§9).*
