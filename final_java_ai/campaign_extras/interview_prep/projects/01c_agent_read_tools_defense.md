# Agent tools that only read planning data (not "never writes SQL")

## What the resume means
The clustering copilot exposes **14 audited tools**. Those tools **only read** planning / clustering data. The LLM does **not** get a raw SQL shell. Any change to plans or clusters goes through **3 human confirm gates** and then a controlled write-back path (Go doing layer / existing product APIs), not free-form model-generated SQL.

## Why we do not say "never writes SQL" on the PDF
That phrase sounds absolute and confusing (engineers write SQL all the time). The accurate claim is **tool permissioning**: agent tools are read-scoped; writes are gated and go through the product write path.

## How to defend in interview
1. LLM plans which tool to call (LangGraph / MCP).
2. Tool implementations are audited allow-listed functions (filters, metrics, cluster evals) that query via controlled interfaces.
3. Human confirms scenarios before write-back.
4. Failure baseline on kik: **8.5% (37/437)**, mostly input-boundary mistakes; target **under 2%**.

## Tags
14 tools + 3 gates: DESIGN (Overview + Copilot FRD). Failure 8.5%: MEASURED. Under 2%: TARGET.
