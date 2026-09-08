# Final resume — Generative AI skills defense

**PDF categories (Sep 2026):** Languages · Backend & APIs · **Generative AI** · Data & Streaming · Databases & Storage · Cloud & DevOps · Architecture & Core.

Canonical: `docs/ASSORTSMART_TAB_RESUME.md`. MCP is **not** on this PDF.

| Skill on PDF | What it means here | Where to defend | Tag |
|---|---|---|---|
| **LLM agents** | Multi-step graphs, not chatbots | AssortSmart Keep/Drop + Ask Iris (Supervisor+Evaluator) | PDF |
| **OpenAI / Gemini / Claude** | Provider APIs | IA lenses; Menu Gemini 2.5 Pro | PDF / HISTORICAL |
| **LangGraph** | Stateful orchestration | 7 lenses + Ask Iris Supervisor/Evaluator | PDF |
| **LangChain** | RAG glue | Menu RAG | HISTORICAL |
| **tool calling / structured invokes** | Typed LLM calls; never raw SQL writes | Air-gapped Keep/Drop; Ask Iris frozen scopes | PDF |
| **prompt engineering** | Structured outputs, schema-shaped extraction | IA lenses; Menu extraction | PDF / HISTORICAL |
| **RAG / embeddings / Milvus** | Retrieve → generate → schema gate | **Menu** (98% offline) | HISTORICAL offline |
| **offline evaluation** | Harness, not live SLA | IA **300-case / 80% CI promotion gate** vs **74%** baseline; Menu 98% | PDF gate / HISTORICAL |
| **LangSmith** | Token/step/fallback telemetry | IA orchestration registry | PDF |

**Verbal only / not on PDF:** Cluster Recommendation Copilot, MCP, 14 tools.

## One-liners
**Agents:** Keep/Drop blends deterministic KPI math with 7 structured LLM lenses; Ask Iris is a shipped Supervisor+Evaluator copilot with frozen scopes.
**Offline eval:** ≥80% is a CI promotion gate, not all-tenants-live. Menu 98% is offline.
**LangSmith:** Per-run JSON + LangSmith for tokens/duration/fallbacks; Datadog for the Go edge.

## Do not say
- MCP as a PDF skill
- Fine-tuning / SFT on the PDF
- Copilot/Hindsight as resume bullets
- pgvector as production (literacy only)
