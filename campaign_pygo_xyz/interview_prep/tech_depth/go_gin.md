# Go + Gin (doing layer)

## What
Go (Golang) with Gin HTTP framework for AssortSmart shared doing layer (Hindsight Clustering Strategy).

## How used here
Manual UI and Agent tool calls both hit Go engines so authorization and business rules stay one surface. Agent plans in Python then invokes Go tools.

## Tradeoffs
Two languages increase cognitive load but prevent duplicating merch engines. Go gives predictable latency for compute-ish paths.

## Failure modes
- Divergent auth between Python and Go
- Tool contract drift (MCP schema vs Go API)
- Overloading Gin with LLM logic (keep LLMs in Python)

## Likely questions
Why Go not Python for clustering? How do you version tool contracts? How do you observe cross-language traces?
