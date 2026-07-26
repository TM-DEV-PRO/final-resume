# Application / screening questions (paste-ready)

Canonical copy-paste bank. HTML twin: `../ApplicationKit.html`. Keep honesty tags aligned with `GROUND_TRUTH.md`.

---

## Autonomous AI system (LangGraph / LlamaIndex / ADK)

**Question:** Can you describe an autonomous AI system you built and deployed in production using frameworks like LangGraph, LlamaIndex, or ADK? Please explain the architecture, orchestration logic, monitoring strategy, and how you ensured scalability and reliability.

**Honesty before paste:** Phase 1 of the Cluster Recommendation Copilot is **design-complete with external review PASS to bring-up**; **bring-up load test pending**. Prefer “building for production / production-bound” over “fully deployed to every tenant.” Framework used: **LangGraph + MCP** (not LlamaIndex or ADK).

### Full answer (screening form / ~250–350 words)

```
At Impact Analytics I am building the Cluster Recommendation Copilot inside AssortSmart, a merchandise-planning SaaS where retailers decide what to buy, how much, and for which stores. The autonomous path uses LangGraph (not LlamaIndex/ADK) for orchestration and MCP for a fixed tool registry. Phase 1 is design-complete with external review PASS to bring-up; the remaining gate is a bring-up load test, so I describe this as a production-bound agent system I am building and hardening, not as a claim that every tenant already runs the shipped copilot.

Architecture
Two planes. (1) An agent plane: FastAPI + LangGraph + MCP. The LLM plans, explains, and selects tools; it never invents SQL. (2) A doing plane: Go (Gin) APIs for Hindsight / Clustering / Strategy, plus a per-tenant ClickHouse planning store (63 tables / 8 layers, append-only, agent profile read-only). Manual UI and agent tools converge on the same Go APIs so auth, validation, and audit are not duplicated in the LLM path. Object artifacts land in GCS; BigQuery remains historical truth for some feeds, with a dedicated ClickHouse read plane targeting deterministic agent probes (design: p95 under 500ms vs measured BigQuery variance of 1–20s+).

Orchestration logic
LangGraph models the workflow as a stateful graph with human-in-the-loop interrupts: ground the planner’s intent → confirm a search plan → fan out batch evaluation of many cluster configs (design target ≥20, batch window 20–100) via 14 audited read-only tools → present scored options with evidence → require human approval before any write-back. Three product confirm gates keep autonomy banded: the agent can explore and recommend, but write-back only happens after human signature. Content-addressed config snapshots make approved runs reproducible. MCP is the tool contract so the agent discovers schemas at runtime and cannot invent free-form warehouse queries.

Monitoring strategy
Three layers stitched by a shared OpenTelemetry trace_id: LangSmith for agent run trees, prompt/tool replay, tokens, and evals; Datadog for FastAPI/Go HTTP, DB, and infra SLOs; PostHog for product behavior (e.g. chat abandonment vs manual wizard). That split exists because Datadog alone does not give prompt replay, and LangSmith alone does not page on Go p99 or ClickHouse health.

Scalability and reliability
Scale the agent tier with LLM latency (Python), and the doing tier with request volume (Go goroutine pools, bounded bulk saves, idempotent batch ids). Reliability is engineered as constraints, not hope: DB-enforced read-only agent profile, fixed 14-tool registry, human gates before writes, append-only / versioned planning data, and measured baselines we engineer against — e.g. clustering-run failures were 8.5% (37/437 on kik, mostly input-boundary errors) with a target under 2%. A separate row-identical pivot POC (250M rows, 189s → 12.3s on ClickHouse) informed the analytics store choice before we committed the agentic read plane.
```

### Short answer (~120 words)

```
I am building AssortSmart’s Cluster Recommendation Copilot with LangGraph + MCP on FastAPI, backed by a Go doing layer and a per-tenant ClickHouse planning store. LangGraph owns the stateful flow (ground → search plan → batch tool calls → human approval → write-back). MCP exposes 14 audited read-only tools so the agent never invents SQL. Reliability comes from a DB read-only profile, three human confirm gates, and content-addressed configs. Monitoring splits LangSmith (agent quality), Datadog (platform SLOs), and PostHog (product), joined by one OTEL trace_id. Phase 1 is design-approved for bring-up; load test is the remaining production gate.
```

### Bullet checklist

```
• Framework: LangGraph orchestration + MCP tool registry (not LlamaIndex/ADK)
• Product: AssortSmart Cluster Recommendation Copilot for retail merchandise planning
• Architecture: FastAPI agent plane ↔ Go doing layer ↔ ClickHouse (append-only, agent read-only) + GCS
• Orchestration: stateful graph with human-in-the-loop gates; 14 audited read-only tools; agent cannot write
• Monitoring: LangSmith + Datadog + PostHog on shared OTEL trace_id
• Reliability: read-only DB profile, approval gates, content-addressed configs; baseline failures 8.5% (37/437) → target <2%
• Status honesty: Phase 1 design PASS / bring-up load test pending
```

---

## Production-grade RAG for enterprise document processing

**Question:** How would you design a production-grade RAG pipeline for enterprise document processing? Please cover vector database selection, context management, retrieval optimization, feedback loops, and methods for improving response accuracy and compliance.

**Honesty:** Uber Menu RAG + Gemini numbers (**98% fidelity / 100% schema**) are **offline/eval**. Lead with design; ground with that production path.

### Full answer

```
I design enterprise RAG as an extraction + grounding pipeline with a hard schema contract, not as “chat over a vector DB.” At Uber Eats I shipped a production path that turns PDF/image menus into catalog rows with RAG + Gemini 2.5 Pro, supervised fine-tuning for schema adherence, and offline eval at 98% fidelity / 100% schema consistency — low-confidence outputs went to human review, not silent upsert.

1) Vector database selection
Default for enterprise docs when Postgres is already SoR: pgvector (or a managed equivalent) colocated with tenancy, ACLs, and transactional metadata — one backup/IAM story, row-level security, and joins between vectors and document ACL tables. Choose a dedicated vector service (e.g. Vertex AI Vector Search / Pinecone / OpenSearch k-NN) when you need multi-million embeddings, aggressive QPS, or hybrid lexical+dense at search-engine scale. Reject “vector DB of the week” if it cannot express tenant isolation, soft-delete, and document versioning. Store: embedding + chunk text + document_id + version + tenant_id + ACL tags + content_hash + source URI + as_of timestamp.

2) Context management
Ingest: OCR/layout-aware parse → semantic chunking (section/heading aware, not fixed 500 tokens) with overlap only at section boundaries → embed with a pinned model version → upsert by (tenant, document_id, chunk_id, content_hash) for idempotent re-ingest. At query time: retrieve top-k, then pack a budgeted context window (token budget + citation slots), prefer fewer high-quality chunks over stuffing, and always pass structured fields (item name, price, allergens) separately from free text so the LLM cannot invent required columns. Session memory stays short; durable state is the validated catalog row, not the chat transcript.

3) Retrieval optimization
Hybrid retrieval: dense (embeddings) + sparse (BM25/keyword) for SKUs, prices, and rare tokens LLMs miss; optional cross-encoder / Cohere-style rerank on the top 50→10. Metadata filters first (tenant, locale, menu version, effective date) so you never retrieve another customer’s docs. Query rewrite for typos/synonyms; multi-query only when recall is measured low. Cache embeddings and frequent query vectors; invalidate on document version bump. Measure recall@k and citation precision on a golden set — not vibes.

4) Feedback loops
Offline: labeled gold menus / docs, regression suite on every prompt or embed-model change (LangSmith-style run trees + dataset evals). Online: thumbs / correct-edit capture when humans fix extracted fields; route corrections into a hard-negative and SFT set. Confidence gates: if model confidence or schema validation fails, escalate to human queue; never auto-write. Track drift: weekly sample of production outputs vs human corrections; alert when fidelity or schema-pass rate drops.

5) Accuracy and compliance
Accuracy: schema validation as a deterministic gate (100% schema consistency was our offline bar); constrained decoding / structured output where the API supports it; cite chunk IDs in the answer; refuse when evidence is missing. Compliance: tenant-isolated indexes; PII redaction before embed when required; encryption in transit/at rest; audit log of document version used for each extraction; retention and right-to-delete by content_hash; no training on customer docs without contract; prompt/tool allowlists; DLP on egress. For regulated surfaces, human approval before publish is part of the pipeline, not a bolt-on.

Principle I ship with: the LLM proposes; validators and humans dispose. RAG improves recall of evidence; the schema and ACL layer decide what is allowed to become system of record.
```

### Short answer

```
I’d build enterprise RAG as ingest → hybrid retrieve → budgeted context → structured generate → schema validate → human escalate on fail. Vector store: pgvector when Postgres/tenancy/ACLs matter; dedicated vector search at multi-million scale. Chunk by document structure, version every upsert by content hash, filter by tenant before ANN. Optimize with dense+BM25, rerank, and golden-set recall@k. Close the loop with offline evals, human edit capture into SFT/hard-negatives, and confidence gates. Accuracy and compliance come from deterministic schema validation, citations, tenant isolation, audit of document versions, and never writing low-confidence output to SoR. That is the pattern I used on Uber Eats menu PDFs/images with RAG + Gemini (offline eval: 98% fidelity, 100% schema consistency).
```

### Bullet checklist

```
• Vector DB: pgvector (Postgres/ACL-first) or managed vector search at high QPS/scale; always tenant_id + version + content_hash
• Context: structure-aware chunks, token-budget packing, structured fields outside free text
• Retrieval: hybrid dense+BM25 → rerank; metadata filters before ANN; measure recall@k
• Feedback: offline golden evals; human corrections → SFT/hard-negatives; confidence → human queue
• Accuracy/compliance: schema gate, citations, tenant isolation, audit, PII/retention, no silent SoR writes
• Grounding example: Uber Eats menu RAG + Gemini (98% fidelity / 100% schema, offline eval)
```

---

## Related deep dive

- Architecture / Q&A: `10_impact_analytics_deep_dive.md` (Why LangGraph, Why MCP, observability split)
- Menu RAG: `14_uber_menu_deep_dive.md`
- Numbers: `18_resume_number_catalog.md`, `GROUND_TRUTH.md`
