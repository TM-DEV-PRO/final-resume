# Observability + Cloud (Docker GCP AWS)

## What
Datadog LangSmith PostHog at IA. ELK + New Relic on-call at Masters. Docker everywhere. GCP (IA Menu) AWS (Masters). Kubernetes listed as skill (no claim of cluster ops ownership).

## How used here
- IA: LangSmith for agent quality Datadog platform PostHog product stitched by trace ids.
- Masters: on-call alerting cut triage 70% coverage 35→82% 98% deploy success.
- Honesty: do not claim sole ownership of Datadog/LangSmith org-wide. No Terraform production ownership.

## Tradeoffs
Three obs tools vs one. Prefer domain-right tool with shared trace_id over forcing one vendor.

## Likely questions
How do you debug a bad agent answer end to end? What is your on-call loop? What does 98% deployment success mean?
