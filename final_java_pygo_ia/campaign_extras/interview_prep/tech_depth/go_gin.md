# Go + Gin (doing layer)

## What
Go (Golang) with Gin HTTP framework for AssortSmart shared doing layer (Hindsight Clustering Strategy).

## How used here
Manual UI and Agent tool calls both hit Go engines so authorization and business rules stay one surface. Agent plans in Python then invokes Go tools. **JWT middleware** carries tenant + role claims; per-route validation and timeouts on handlers.

## Tradeoffs
Two languages increase cognitive load but prevent duplicating merch engines. Go gives predictable latency for compute-ish paths.

## Failure modes
- Divergent auth between Python and Go
- Missing tenant claim checks on new routes
- Agent calling Go without propagating identity / `trace_id`
- Tool contract drift (MCP schema vs Go API)
- Overloading Gin with LLM logic (keep LLMs in Python)

## Auth + quotas
JWT middleware, role/tenant claims, and per-tenant concurrency: [auth_tenancy_rate_limits.md](auth_tenancy_rate_limits.md).

## Likely questions
Why Go not Python for clustering? How do you version tool contracts? How do you observe cross-language traces? How is tenant AuthZ enforced on bulk save?
