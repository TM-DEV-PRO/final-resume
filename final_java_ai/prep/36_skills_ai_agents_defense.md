# Final resume — AI & Agents skills defense

**Track:** Final Java + AI (agent plane is still Python — Spring is product write APIs).

**PDF line (both finals):**  
`LLM agents (OpenAI/Gemini/Claude), LangGraph, LangChain, MCP, tool calling, prompt engineering, RAG, embeddings, Milvus, pgvector, offline eval, LangSmith`

Every item below must map to a project. Do not invent training/fine-tuning ownership.

| Skill on PDF | What it means here | Where to defend | Tag |
|---|---|---|---|
| **LLM agents** | Multi-step planner/agent loops, not chatbots | IA Cluster Recommendation Copilot | DESIGN / building |
| **OpenAI / Gemini / Claude** | Provider APIs used in agent + extraction paths | IA agents; Menu Gemini 2.5 Pro | DESIGN / HISTORICAL |
| **LangGraph** | Stateful agent graph / orchestration | IA chat plane | DESIGN / building |
| **LangChain** | Chains / retrievers glue | IA + Menu RAG | DESIGN / HISTORICAL |
| **MCP** | Tool protocol hosting audited tools | IA (14 read-only tools — verbal count) | DESIGN / building |
| **tool calling** | Models invoke typed tools; args validated; agent never raw-SQL writes | IA tools + confirm gates | DESIGN / building |
| **prompt engineering** | System/tool prompts, structured outputs, schema-shaped extraction | IA agent prompts; Menu extraction prompts | DESIGN / HISTORICAL |
| **RAG** | Retrieve → ground → generate → validate | Menu PDF/image → Uber Eats schema | HISTORICAL |
| **embeddings** | Vectorize labeled menus / retrieval corpus | Menu **Milvus**; IA async embedding jobs (Kafka on Tech) | HISTORICAL / DESIGN |
| **Milvus** | Vector store for menu RAG | Menu | HISTORICAL |
| **pgvector** | Postgres-side vector literacy / RAG option | Skills literacy; prefer Milvus for Menu story | literacy |
| **offline eval** | Measured offline, not live SLA | Menu **98% fidelity / 100% schema**; IA LangSmith eval/regression | HISTORICAL / DESIGN |
| **LangSmith** | Agent/LLM traces, offline eval & regression | IA observability split (with Datadog/PostHog) | DESIGN / building |

## One-liner answers

**Tool calling:** “The model never writes the DB. It calls audited tools; we validate args; writes need human confirm gates.”  

**Prompt engineering:** “Prompts + schemas constrain outputs — Menu schema gate is what makes 100% schema consistency offline; IA tools use structured contracts.”  

**Embeddings:** “Menu: labeled-menu embeddings in Milvus for RAG. IA: embedding jobs on the async/Kafka path for planning content — not a separate product claim.”  

**Offline eval:** “Menu 98%/100% is offline eval HISTORICAL — not a production SLA. Say that unprompted.”  

**LangSmith:** “Agent traces and eval/regression; Datadog for service SLOs; PostHog for product — three different jobs.”

## Do not say
- Prompt engineering as a full-time specialty title  
- Fine-tuning / SFT on the PDF (removed)  
- Pinecone / Weaviate ownership  
- “Production agentic load-test PASS” / shipped AssortSmart  
- 14 tools / 3 gates / 8.5% on the PDF (verbal)

## Cross-links
- `campaign_extras/interview_prep/tech_depth/langgraph_mcp_rag.md`  
- `campaign_extras/interview_prep/tech_depth/skills_fundamentals_map.md`  
- `23a_ia_interview_pack.md` · `23b_uber_interview_packs.md` (Menu RAG)  
- `10_impact_analytics_deep_dive.md` (LangSmith / tools)
