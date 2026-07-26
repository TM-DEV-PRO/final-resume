# LangGraph + MCP + RAG + Gemini

## What
LangGraph orchestrates multi-step agent graphs. MCP exposes tools. RAG retrieves context. Gemini 2.5 Pro used on Menu extraction (offline eval). LLM providers also OpenAI/Claude at IA.

## How used here
- IA: planner copilot graph with 14 audited tools that only read planning data and 3 human gates before write-back.
- Menu: RAG + Gemini + SFT for menu field extraction 98% fidelity 100% schema consistency offline.

## Tradeoffs
Autonomy vs safety. Gated human confirm beats fully autonomous writes for money decisions. RAG + SFT beats brittle regex for messy menus.

## Failure modes
- Hallucinated tool args → validators
- Stale RAG index
- Eval leakage (offline ≠ production)

## Likely questions
Why LangGraph vs plain LangChain chains? How do MCP tools stay read-only? How do you evaluate RAG? What is SFT vs prompt-only?
