# LangGraph + MCP + RAG + production agent skills

Defense for the **AI & Agents** skills line on both final resumes. Canonical table: [`../../../prep/36_skills_ai_agents_defense.md`](../../../prep/36_skills_ai_agents_defense.md) (from `campaign_extras/.../tech_depth/` use `../../../../prep/36_skills_ai_agents_defense.md` — prefer opening `prep/36_skills_ai_agents_defense.md` from the final folder root).

## What (PDF skills)
LLM agents (OpenAI/Gemini/Claude), **LangGraph**, **LangChain**, **MCP**, **tool calling**, **prompt engineering**, **RAG**, **embeddings**, **Milvus**, **pgvector**, **offline eval**, **LangSmith**.

## How used here
- **IA:** LangGraph copilot graph; MCP-hosted **tool calling** to audited **read-only** planning tools; **prompt engineering** + structured tool contracts; human confirm before writes; **LangSmith** for traces/eval; embeddings jobs on async/Kafka path; ClickHouse reads — say **building**, not shipped.
- **Menu:** **LangChain RAG** + **Gemini 2.5 Pro** + **Milvus** (**embeddings** of labeled menus); **prompt engineering** + schema validation gate; **98%/100% offline eval** (HISTORICAL). No SFT on PDF.

## Tradeoffs
Autonomy vs safety — gated confirms beat fully autonomous money/planning writes. RAG + schema gate beats brittle regex for messy menus. Offline eval ≠ live SLA without monitoring.

## Failure modes
- Hallucinated tool args → validators / typed schemas  
- Stale embeddings / RAG index  
- Eval leakage (offline ≠ production)  
- Prompt drift without golden-set regression (LangSmith)

## Likely questions
Why LangGraph vs plain chains? How do MCP tools stay read-only? What is tool calling vs free-form SQL? How do you evaluate RAG? Prompt engineering vs fine-tuning? Embeddings where?

## Full agentic flow / evals / guardrails
See [../projects/01d_agentic_evals_guardrails_flow.md](../projects/01d_agentic_evals_guardrails_flow.md) if present — production load-test honesty, LangSmith vs Datadog, 14 tools + 3 gates (verbal).
