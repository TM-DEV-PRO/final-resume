# FAANG batch — resume rebuild decisions (Sept 2026)

Two variants built in this directory. **Nothing in `final_pygo_ai/`, `final_java_ai/`, or `final_java_pygo_ia/` was modified.**

- `pygo_ai/` — Python + Go + AI. Primary.
- `java_pygo_ia/` — Java + Python + Go + AI. Keeps the existing track's Spring Boot framing for FRM and Masters.

Both compile to **2 comfortable pages**. Verify locally: `cd pygo_ai && pdflatex resume.tex` twice.

**Layout (revised):** body **10/12.3pt** (was 9.4/10.15), margins **0.6in** left/right (was 0.2in), bullet itemsep 2.2pt (was 0.55pt), section spacing loosened, and a continuation footer carrying name + page number on page 2. The Java variant runs at 9.9/12.0 with marginally tighter spacing because the Spring Boot tech lines are wordier — content is identical, the difference is imperceptible.

Because two pages freed up room, the bullets that had been **merged purely to save space are restored**: ANZ Driver Compliance is its own project block again, "Led 3 engineers" is its own bullet, Masters and GeeksforGeeks are back to 4 bullets each, the Summary is back to 3 bullets, and Achievements to 3.

See `SCORECARD.md` for the audit against the original rejection reasons and per-JD ATS coverage.

---

## 1. Claims REMOVED, and why

Verified against the actual source in `~/Desktop/Agentic-Assort` (both repos) plus `KNOWLEDGE-MATERIAL/`.

| Removed | Verdict | Where it was |
|---|---|---|
| **MCP** (Model Context Protocol) | **Zero references** in either repo — no `mcp`, `fastmcp`, `modelcontextprotocol`, no imports. Tools are LangChain `StructuredTool`. | Was in the Tech line and Skills of the live resume |
| "**≥80% offline accuracy**" phrased as an achievement | It is a *configured gate*, and the agent **fails it**: `docs/TELEMETRY_GOLD200.md` records 4 models at **57.0–63.2%** vs a **$0 deterministic baseline at 74%**, with your own doc saying the free signal beats every model. | Old bullet implied it was met |
| "2.4B weekly rows / 106M rollup / 1.6M article-season / 335K articles / 16B combinations / 5 seasons" | **None of these figures exist anywhere.** Real numbers are in `assort_kd_flow/docs/TELEMETRY.md:145-165`. | The AI-generated bullets you pasted |
| "1,144 test functions" | Actual count is **1,227** (`grep -rn "^func Test" --include=*.go`). Resume says "1,200+" so it cannot rot. | pasted bullets |
| "64-article batches in ~24 seconds" | 64 is real (`max_articles_per_llm_batch`). The 24s is not: real per-batch durations are **94.8–268.7s**, and the only nearby number is a **572s timeout budget**. | pasted bullets |
| "10 modules / 30 routes" | **36 routes** in the 8 shipping modules (the 4 in `internal/server/router.go` are commented-out examples; framework meta routes add 3). Only **8 of 10 modules ship** — `lineplanning` and `strategy` are `// TODO: register this module's routes` scaffolds. | pasted bullets |
| Terraform, deep Kubernetes | Not in your evidence base; your own `GROUND_TRUTH.md` says omit them. | (not added despite 2–3 JDs asking) |
| C, C++ | Listed in Skills, used in zero bullets. Reads as keyword padding. Google Ads accepts "Python **or** C++" — Python satisfies it. | old Skills line |

### Claims KEPT because they verified

| Claim | Evidence |
|---|---|
| 189s → 12.3s (~15.5x) on 250M rows | `KNOWLEDGE-MATERIAL/Impact-Analytics-work/ClickHouse-vs-Postgres-POCs.docx`: `250M PG 189,408 / 250M CH 12,256` ms. **Not** in the repos — the artifact is the docx. Carry the caveat: the doc itself says ~13–15x, hosts were unequal (PG 48GB vs CH 3.3GB Docker), and ~90% of the gap is `COUNT(DISTINCT)`; strip it and typical aggregates are ~2–3x. |
| 100% statement-coverage CI gate, 1,200+ tests | `scripts/coverage.sh:12` THRESHOLD=100.0, `Makefile cover-check`, `lefthook.yml` pre-push, `bitbucket-pipelines.yml`. Committed `coverage.out` shows **99.93%** (5 uncovered blocks) — pre-empt this if asked. |
| Google Wire DI, h2c, 10MiB cap, 10/30/130/120s budgets, 2s-per-hook SIGTERM drain | All verified exactly: `go.mod` wire v0.7.0, `cmd/server/main.go:21` StartH2CServer, `httpserver/constant.go:9,31,33,37,43,49`, `app/shutdown.go:26,45`. |
| SELECT-only enforcement, six layers | Prompt ban (`assort_kd_flow/prompts/md/db_safety.md`), no-raw-SQL tool contract, regex statement guard (`assort_kd_flow/tools/ch_read.py:16-39`), table allowlist, per-run budgets, and `pipeline_registry/freeze.py:48-52` which **refuses to boot** if writes are enabled. Genuinely strong. |
| 88,863 articles / 20,265 LLM calls / 8.25h / $821 | `docs/TELEMETRY.md:60-90`, real season-76 production run. **205/min is the peak** (session 4 of 4: 122/149/188/205); sustained over the pass is ~177/min. Resume says "peak 205". |
| 2.11B-row ClickHouse fact table | `TELEMETRY.md:157` (16.9B at `:162`, second tenant). |
| 300 gold cases | `evals/gold/cases.json` is exactly 300. |

### Late corrections from the adversarial pass (applied to both variants)

| Was | Now | Why |
|---|---|---|
| "LangGraph supervisor graph over 7 weighted evidence lenses" | Lens scoring described as a **bounded parallel fan-out over 8 gated, weighted lenses**; **LangGraph StateGraph/ToolNode** moved onto the dig-deeper QnA bullet where it actually lives | Two different subsystems. Lens scoring is a hand-written fan-out/fan-in orchestrator (`engines/agentic.py:4-5`, gate at `lenses/gate.py:8-42`) with no StateGraph. The LangGraph supervisor is `orchestration/graph.py:137-153`, and its nodes are worker agents serving the QnA plane. Anyone opening the repo sees this in a minute. |
| "7 lenses" | "**8** gated, weighted lenses" | `config/decision.json` defines 8 summing to 1.0. Typically 7 fire per article — say that verbally. |
| "38 REST routes" | "**36** REST routes" | 38 had no clean derivation. |
| "4 LLMs at 57--63%" | "**4 models at 57--62%**" | 63.2% is `gpt-4o-mini` at **n=19 of 200**, marked in your own `TELEMETRY_GOLD200.md:3` as "not a quality estimate". Never quote it. |
| "it benchmarked 4 LLMs" (implying the 300 set) | "a **200-case balanced proxy run** benchmarked..." | The gold file holds 300 cases; the model benchmark ran on 200 (100 keep / 100 drop). |
| "RBAC" in the bullet | "**UAM-backed store/product access checks**" | No role model in the Go repo; authorization is code/dimension-scope intersection delegated to UAM (`platform/uam/access_check.go:21-30`). RBAC stays in Skills only. |
| "Redis ... degrades open" | "over a Redis-fronted user store" | "Degrades open" is security vocabulary for *bypassing* a check. The real behavior is cache-miss fallthrough to Postgres (`platform/usermaster/resolver.go:100-145`). A security interviewer would have caught it. |
| "provider circuit breakers" / "adaptive per-call timeouts" | folded into "bounded parallel fan-out"; details kept in Skills | The breaker is **run-level** (fail-fraction + consecutive-fail abort, `engines/agentic.py:1386-1396`), not per-provider; timeouts are **batch-size-derived**, not feedback-adaptive. |
| "hash-frozen CSV" | "**config-hash-stamped** CSV bake-and-promote" | The *config* is SHA-256 hashed (`freeze.py:95`), not the CSV. |
| Skills: Liquibase, DynamoDB, pgvector | **removed** | Liquibase: zero hits anywhere. DynamoDB: appears only in your own old skills line — same argument that cut C/C++. pgvector: `36_skills_ai_agents_defense.md:22` tags it "literacy"; Milvus is the real one and is listed. |

**Kept with a known caveat:** `gRPC` in Skills (only real evidence is `UBER_PORT_GRPC` opened by Uber's internal scaffold — say "exposed via the framework; I didn't author gRPC services"), and `BigQuery`/`GCS` on the IA Tech line (design-plane, not code you shipped).

---

## 2. What the rewrite adds that wasn't there

Your old IA section was 4 bullets of mostly *design* language. The repos contain far stronger material that was going unused:

1. **Go platform ownership with hard numbers** — 36 routes, 8 modules, Wire DI, h2c, request budgets, SIGTERM drain.
2. **CI/CD and engineering rigor** — 100% coverage gate, 1,200+ tests, golangci-lint, race detection, SAST/SBOM. Hits `CI/CD` (3 JDs) and `testing` (4 JDs), both previously skills-only.
3. **Security/authn/authz** — Firebase → JWT/Google OIDC chain, tenant resolution, UAM access checks, constant-time API keys. `security` appears in **5 of 8** JDs and your resume had nothing on it.
4. **Production scale, measured** — 88,863 articles, 20,265 calls, $821, peak 205/min. Replaces vague design claims with a real run.
5. **ML/eval infrastructure** — the gold harness reframed honestly. This is the exact vocabulary Google Ads gates on ("model evaluation, optimization, debugging"), and it is now a *senior* bullet: you built the harness that killed your own rollout.

That last one is the single strongest line on the resume. Interviewers see engineers oversell AI constantly; an engineer who built the measurement that said "not yet" is rare.

---

## 3. ATS coverage vs the 8 JDs

Must-have set (appears in 4+ JDs): Python, Go, distributed systems, system design, scalability, APIs/REST, AWS, GCP, cloud-native, agents/agentic AI, LLMs, security, end-to-end ownership, code/design reviews, testing, collaboration.

| Keyword | JDs | Before | After |
|---|---|---|---|
| Python | 7 | ✅ | ✅ |
| Go / goroutines | 5 | skills only | ✅ headline + 3 bullets |
| Distributed systems | 6 | summary only | ✅ own skills group |
| System design / architecture | 6 | ✅ | ✅ |
| APIs / REST | 4 | ✅ | ✅ |
| AWS | 5 | ✅ | ✅ |
| GCP / cloud-native | 4 | ✅ | ✅ |
| Agents / agentic AI | 5 | partial | ✅ |
| LLMs | 4 | ✅ | ✅ |
| **Security / authn / authz** | 5 | ❌ | ✅ new bullet |
| **Testing / TDD** | 4 | skills only | ✅ 1,200+ tests + gate |
| **CI/CD** | 3 | skills only | ✅ pipeline bullet |
| Code / design reviews | 4 | 1 mention | ✅ |
| End-to-end ownership | 5 | ✅ | ✅ |
| Kubernetes | 3 | skills only | skills only ⚠️ |
| Terraform / IaC | 2 | ❌ | ❌ ⚠️ |
| gRPC | 1 | skills only | skills only |

**Still-open gaps:** Kubernetes depth and Terraform. Rubrik Enterprise AI gates hard on *"building and operating clusters, not just deploying to them"* — you can't honestly claim that, and it's one reason that req is out of reach regardless of YoE.

---

## 4. Where to send which — and honest fit

| Role | YoE gate | You | Send | Real odds |
|---|---|---|---|---|
| **Google Cloud SSE** (Bengaluru) | 5 yrs **Go or Python** + distributed systems + LLM/GenAI/Agentic AI | 5 | `pygo_ai` | **Best fit in the batch.** The req reads like your resume. Level tag is internally "Mid", which matches your actual seniority. |
| **Google Ads AI/ML GenAI** (Bangalore) | 5 yrs Python/C++, **3 yrs ML infrastructure**, 1 yr GenAI | 5 / ~1.5 ML-infra | `pygo_ai` | Plausible. The gold-harness + model-benchmarking + cost-telemetry bullets are your ML-infra evidence. The 3-year ML depth is the stretch. |
| **Salesforce MTS** (Trailhead) | Not stated; AWS + **Terraform** + CI/CD + web fundamentals + AI-*tool* usage | Terraform ❌ | `pygo_ai` | Mismatch of kind, not level. Wants a full-stack generalist who uses Claude/Cursor, not an AI engineer. Low priority. |
| **Rubrik Sr SWE Enterprise AI** | **9+ yrs** + deep K8s cluster operation | 5, no K8s depth | — | Out of reach on two independent gates. |
| **Rubrik Sr Backend** (Israel) | 5+ yrs, Kafka/RabbitMQ/SQS/Celery, gRPC, asyncio | 5 ✅ | `pygo_ai` | Skills fit is genuinely good (Kafka, Celery, asyncio, SQL all real). **Tel Aviv hybrid** is the blocker. |
| **Rubrik Sr SWE Identity Infra** (Palo Alto) | **6+ yrs** + Active Directory / Entra-ID / Okta | 5, no AD | `java_pygo_ia` | Weak. Domain knowledge is the real gate, not the language. |
| **Rubrik SWE Cloud Native Protection** (Bangalore) | **2+ yrs** | 5 | `java_pygo_ia` | You're over-level. Would likely be a downlevel offer. |
| **Microsoft Sr SWE (MSEC)** | **8+ yrs** + Java/Python/.Net + **agents/MCP** | 5 | `java_pygo_ia` | Out of reach on YoE. Note it explicitly wants MCP — and you don't have it. Don't add it to get past the filter. |

**Blunt summary: this batch has one strong shot (Google Cloud), one credible one (Google Ads), and six that are gated on years, geography, or domain.** The resume is now genuinely competitive — the constraint is the target list, not the document. Worth building a wider list of 5-YoE-appropriate reqs: Databricks, Snowflake, Atlassian, Confluent, Stripe, Uber (as FTE this time), plus Indian product companies where 5 years reads as senior.

---

## 5. Interview landmines to pre-empt

Ranked by damage if an interviewer opens the repo.

1. **Gold accuracy is 57–63% and the LLM loses to the deterministic rule (74%).** Your own `TELEMETRY_GOLD200.md` says so in bold. The resume now states this deliberately. Have the story ready: *"I built the harness, it said the agent wasn't ready, so I blocked promotion."* Never imply you hit 80%.
2. **`lineplanning` and `strategy` are empty scaffolds.** Resume says "8 modules", not 10. Keep it that way.
3. **`gold_min_accuracy: 1.0` in three `hindsight_*` pipelines** — an unreachable 100% gate. If asked, call it a placeholder, not a design.
4. **Python repo has no CI and no coverage measurement at all**, while the Go repo advertises a 100% gate. Own the asymmetry: hardened service plane, research-grade pipeline plane.
5. **`coverage.out` shows 99.93%, not 100%** — 5 uncovered blocks in `secrets/gcp.go` and `hindsight/service/`. Say "gate is 100%, last committed profile 99.93%."
6. **The batch-size sweep used synthetic `A000xx` articles**, and `bench_decision_architecture` is `"mock_only": true`. Label them as offline sweeps, never production evidence.
7. **Datadog "correlation-ID-joined logs and traces"** overstates it — there's no `dd.trace_id` log injection. The resume avoids the phrase; keep avoiding it.
8. **Client data at repo root** — `briscoes_by_item_table_top200.csv` (202KB), `keep_drop_season7.csv`. If anyone ever sees the repo, that's a data-hygiene question. Worth cleaning regardless.

---

## 6. Structural issues I did NOT fix (they need your call)

1. **"Senior Software Engineer" on 4 months of the title.** Restructured to lead with scope rather than level, but the date column still shows May 2026. Both Google reqs are internally "Mid" — you may do better not fighting this.
2. **"UBER (via EPAM Systems)."** Kept, honestly. It costs you brand credit; removing it would be misrepresentation.
3. **Four tenures averaging under 2 years, with the newest at 4 months.** Nothing on a resume fixes this. It gets asked. Have the answer.
4. **Java framing.** Per your instruction, `java_pygo_ia` keeps FRM and Masters as Spring Boot. Be aware: `KNOWLEDGE-MATERIAL/UBER-WORK/FRM PROJECT/frm_scoping_service/` is Python/FastAPI/Bazel with `mysql_manager.py` and Pydantic schemas. If a Microsoft or Rubrik interviewer asks you to walk through the FRM code, the story and the artifact diverge. That's your risk to carry, and I'd reconsider it for any role where a code-level FRM discussion is likely.
5. **Achievements are 2020–2021** (Code Jam, SIH) plus a HackerRank cert — junior signals. Compressed to 2 lines. Consider replacing with a talk, OSS contribution, or writeup within 6 months.

---

## 7. Second adversarial pass (post-XYZ rewrite) — corrections applied

After rewriting every bullet into XYZ format I re-verified against source. Fifteen claims failed. All corrected in both variants.

**My own error, first:** I proposed "~770 in-scope audit decisions per quarter (55 × 14)" in `METRIC-GAPS.md` and then used it. **The multiplication is invalid.** Per `11_uber_frm_deep_dive.md:195` the ~55 is a *sum* (~26 balance-sheet + ~29 income-statement line items) evaluated at **group** level; the 14 entities are a separate screen and a separate table (`threshold_table_v2.legal_entity`). They're two dimensions of the tool, not a grid — nothing shows 55 decisions per entity. Real entity scale is ~400 (`:194`); 14 was the Q4-2025 sample. "Audit decisions" was also the wrong noun: `11_...:24,:313` are emphatic that the tool produces PwC's evidence inputs and does not decide or block. **Reverted to a non-multiplied claim. Do not reintroduce 770.**

| Claim | Problem | Now reads |
|---|---|---|
| "Scored 88,863 in a **single production run**… **\$821 measured cost**" | Four sessions (1 run + 3 resumes), three ending `status:error`; `TELEMETRY.md:141`. Single-run estimate is 7.2h, not 8.25h. And `TELEMETRY.md:14`: token meters recorded **0** — every `cost_summary.json` is `total_cost_usd: 0.0`. \$821 is call-volume × a bench token shape, i.e. **inferred, not metered**. | "across a full production season — 20,265 LLM calls over one run plus three resumes, 8.25 hours, ~\$821 **inferred from measured call volume**" |
| "**Secured every request path**" | 2 of 36 routes mount outside `server.Protect`: `/v1/health` and `GET /v1/kpi-configurator/ui`, plus framework `/meta/*`. | "Secured **every tenant-facing route** (health and meta endpoints excepted)" |
| "**SAST/SBOM on every run**" | `bitbucket-pipelines.yml` runs AccuKnox only under `branches: {main,dev}` — the file says explicitly "not on PRs". | "golangci-lint and `-race` on every run and SAST/SBOM **on every merge to integration branches**" |
| "Firebase Admin **falling back to** local JWT and Google OIDC" | Local JWT is an **alternative chosen at startup** (`firebase/auth.go:280-286`, when `AUTH_TOKEN_ISS` is set), not a fallback. Only request-time fallback is → Google OIDC. | "Firebase Admin — **or** local JWT validation when a token issuer is configured — falling back to Google OIDC JWKS" |
| "**per-user store and product** scope checks" | `BACKEND_UAM` defaults **false**; exactly **one** call site across 36 routes (`hierarchyconfig` `POST /v1/filters/values`), dimension `store` only. No product-dimension call site. | "a **store-scope check on hierarchy filter reads** via the internal access service" |
| "**Guaranteed** … **six** independent controls … 8-table **allowlist** … 250 queries/batch … **aborts startup**" | Three of six don't hold: `allowed_tables` is never used as a membership check (and is bypassed on the `feature_cache` branch); `max_db_calls_per_batch: 250` has **zero Python references** (real budget is 4 calls/query); the assertion runs at freeze/run time in a package `assort_kd_flow` doesn't import. The other three verify cleanly. | "**Held** the LLM agents SELECT-only … **five** independent controls … an **8-table read set** … per-query budgets (**4 tool calls**, 15s timeout) … **fails the run** if writes are enabled" |
| "LangGraph **supervisor graph** … (4 steps, 10 tool calls per article)" | Wrong graph. QnA runs `agents/tool_agent.py:40-54` — a plain two-node agent↔ToolNode loop. The real supervisor (`orchestration/graph.py`) serves a chat-only `/ws` surface that doesn't answer keep/drop. Both config bounds are **dead** — read by no Python file. Enforced: 4 tool calls/query (`qna/service.py:120`), 15s timeout. | "a LangGraph **tool-calling agent loop** bounded to 4 read-only tool calls and a 15s timeout **per question**" |
| "**immutable** decision snapshots" | Bake tables are `SharedReplacingMergeTree` on `(season_code, article)` — a re-score silently replaces the prior snapshot; in-place `ALTER … DELETE/UPDATE` are routine. | "hash-stamped, **replace-on-rerun** decision snapshots" |
| "2.11B-row ClickHouse **warehouse**" | 2.11B is one **fact table** in one staging DB for one tenant. `kik_dev` is ~4.1B; Briscoes master is 16.9B. | "2.11B-row ClickHouse **fact table**" (also fixed in Summary) |
| "tables **partitioned** by tax quarter" | `12_masters_gfg_deep_dive.md:127` says the opposite — quarter *sharding* with routing owned in application code, explicitly traded off against native RANGE partitioning. | "tables **sharded** by tax quarter" |
| "**cut operational load 70%**" | Direction inverted. Every source says "**raised** operational **efficiency** 70%", narrowed at `12_...:95` to "time saved on those workflows". | "**saved ~70% of the manual effort** on those ops workflows" |
| "~15x" ClickHouse | Source and all six prep docs say **15.5×** (189.4/12.26 = 15.45). Understating created a mismatch with your own interview pack. | "~**15.5x**" |
| "across **18 source files**" | `11_...:127` — "18 **files changed**, 1,268 insertions" in the migration PR. "Source files" reads as 18 input spreadsheets. | "in an **18-file change across five layers**" |
| "staged timeouts (10/30/130/120s)" | Five values exist, four named, and idle/request (both 120) were conflated. | "**nested** timeout budgets (10s headers / 30s read / **120s request** / 130s write / 120s idle)" |
| Summary "88,863 **products** per production **run**" | Noun switched mid-document; "per run" implies a repeatable single-run rate. | "88,863 **articles** scored per production **season**" |

### Skills hygiene, same pass

Removed as orphaned or contradicted: **gRPC** (no service authored in either repo; only incidental driver deps), **circuit breakers** (`12_masters_gfg_deep_dive.md:52,:165` marks it verbal-only prep, explicitly not a resume claim), **cost telemetry** (its only support was the \$821 figure, which was never metered). Replaced with "bounded parallelism", which the config demonstrably supports.

Fixed inconsistency: the Java variant claimed **Django** in its GfG bullet and **Google Wire** in its IA bullet and Tech line while omitting both from Skills. Both added back.

**Still knowingly carried:** `Kubernetes` in Skills. `GROUND_TRUTH.md:44` says omit K8s *ops*; `01_skills_trim_rationale.md:23` permits it as *ops literacy*. It appears in 3 of 8 JDs so it stays as a skills-line item — **never let it become a bullet**, and `16_ats_recruiter_report.md:346` already grades it "WEAK (listed, no cluster-ops proof)".

### Two things to know for interviews

- **8 lenses are configured but one is `is_active: false`, and TELEMETRY says "7 lenses" throughout.** The resume says 8 (config truth). If asked, say "8 defined, 7 active." Also: config weights are passed as `weight_hint` — the operative mix is chosen per-article by the model, not fixed by config.
- **The ClickHouse 15.5× caveat still applies:** ~90% of the gap is PostgreSQL's non-parallelizable grouped `COUNT(DISTINCT)`. Strip it and ClickHouse leads ~2–3×. Volunteer this before you're asked; it reads as rigor.

### Layout note

Both variants now share **identical** `resume.tex` — 9.9/12.0pt, 0.6in margins, itemsep 1.5pt — landing on 2 pages each (54/46 and 52/50 lines). The only differences between variants are the four intended experience lines plus Summary and Skills; `activities.tex` and `education.tex` are byte-identical.
