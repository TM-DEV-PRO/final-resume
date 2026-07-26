# AuthN / AuthZ, rate limits, API vs AI controls, per-tenant quotas

How authentication, authorization, throttling, and multi-tenant limits work across resume projects. Say DESIGN vs HISTORICAL. Do not invent org-wide IAM ownership.

---

## 1. Map by project (quick)

| Project | AuthN | AuthZ | Rate / quota | Tenant isolation |
|---|---|---|---|---|
| **IA AssortSmart** | JWT on Go doing layer + session/SSO at edge (product) | Role + tenant claims; agent tools allow-listed | Per-tenant concurrency + tool budgets; agent quotas | Per-tenant CH + PG config catalogs |
| **IA agent (AI level)** | Same user JWT / service identity calling tools | **14 read tools only**; writes via **3 human gates** | Token/cost budgets; tool call caps; concurrency budget | Tools scoped to tenant planning data |
| **Uber FRM** | Gateway injects `x-auth-params-email` | AuthZ **upstream** of service | Platform gateway limits (not owned in-service) | Single Uber Finance tenant / period-scoped data |
| **Uber Menu** | Internal service auth / job identity on GCP | Catalog write ACLs via service accounts | Scraper backoff + proxy pools (anti-bot), consumer lag backpressure | Vendor/menu keys; not retail multi-tenant SaaS |
| **Masters GST** | JWT (access + refresh); enterprise IP allowlists | RBAC on mutating APIs; audit who/what/when | Gateway + service capacity; Celery rate limits; Kafka lag | Client/GSTIN partition keys; per-client config |
| **GFG** | Django session/auth | Permissions on threads/content | Classic web limits | User/content ACLs |

---

## 2. Impact Analytics — multi-tenant SaaS (deep)

### Authentication (AuthN)
- Planner hits product UI → edge issues identity (SSO/session → **JWT** with `tenant_id`, `user_id`, roles).
- **Go (Gin) middleware** validates JWT on plan lifecycle / tenant config / bulk save APIs (resume-era doing layer).
- **FastAPI agent service** accepts the same tenant-bound identity (or mints a short-lived service token for tool calls) so every tool invocation is attributable.
- Correlation: `trace_id` + user/tenant on Datadog and LangSmith.

**Defend:** “AuthN is JWT at the API edge of the doing layer. I do not claim I own corporate IdP/Okta.”

### Authorization (AuthZ)
| Layer | Rule |
|---|---|
| **API (Go)** | Role claims (planner / admin / read-only) gate mutating routes; tenant claim must match resource `tenant_id` |
| **Data** | Queries always filter `tenant_id` (PG config + CH tables partitioned/keyed by tenant) |
| **AI tools** | Allow-list of **14** audited tools — **read planning data only** |
| **Writes** | No free-form SQL from the LLM; write-back only after **3 human confirm gates** through product APIs |
| **Hindsight catalogs** | Tenant metric catalogs are config — live without code deploy — still behind admin AuthZ |

**Cross-tenant attack defense:** never take `tenant_id` only from the request body; bind from JWT. Reject tool calls whose scope ≠ token tenant.

### Rate limiting — API level
- Per-route limits on Gin/FastAPI (requests / burst) for interactive plan APIs.
- Bulk save / clustering kickoff: stricter quotas than read APIs.
- Backpressure: Go worker pools + context timeouts so one tenant cannot exhaust goroutines.

### Rate limiting / budgets — AI level
| Control | Purpose |
|---|---|
| **Tool-call budget** per session / plan | Stop runaway LangGraph loops |
| **Concurrency budget** per tenant | Cap parallel clustering pipelines from one chat (“N parallel” bounded) |
| **Token / cost budget** (LangSmith attribution) | Cap LLM spend per tenant/day |
| **Timeout budgets** per tool | CH/Go p95; kill hung tools |
| **Scenario / batch caps** | UI **3–5** scenarios; batch explore **20–100** under the hood (design) — still bounded |
| **k / child-cluster caps** | Client min/max k; ~10 child clusters default | Business guardrail + cost control |

**Say:** “AI limits are product budgets, not only nginx `limit_req`. The dangerous amplifier is tool fan-out × LLM retries.”

### Per-tenant limits (how we manage noisy neighbors)
1. **Physical / logical isolation:** per-tenant ClickHouse (or tenant-keyed tables) + PG tenant config — blast radius.
2. **Onboarding = config**, not fork-the-codebase (Hindsight catalogs without code deploy).
3. **Quotas:** concurrent clustering jobs, agent sessions, embed/Kafka async job rate, CH read concurrency.
4. **Fairness:** one tenant’s batch explore cannot starve another’s interactive edits (`~0.4 ms` path stays protected).
5. **Observability:** per-tenant metrics in Datadog; LangSmith datasets tagged by tenant for eval regressions.

**Honesty:** Exact numeric quota table (e.g. “50 RPM per tenant”) is **DESIGN / product config** — do not invent a number not in FRD. Describe the **mechanism**.

---

## 3. Uber FRM — gateway trust + audit AuthN

```text
User → Uber gateway (AuthN + AuthZ)
     → FRM FastAPI
          reads x-auth-params-email
          401 if missing
          persists created_by / updated_by
```

- **In-service:** identity capture for SOX-adjacent audit trail.
- **Not in-service:** fine-grained “who may edit Materiality” — upstream.
- **Interview upgrade if asked:** signed JWT + roles inside service for standalone harden.

No multi-tenant retail model here — period-scoped finance data for Uber entities.

---

## 4. Masters India — JWT + RBAC + compliance data

| Control | How |
|---|---|
| AuthN | Short-lived **JWT access** + refresh; TLS |
| AuthZ | **RBAC** on mutating e-invoice / recon APIs |
| Audit | Who/what/when/before-after on mutations |
| Enterprise | IP allowlisting for some clients |
| Secrets | AWS KMS (HISTORICAL framing) |
| Cache | Redis for IRP auth tokens (TTL &lt; token life), client config |
| Rate | Gateway/service capacity (**700→4,000 req/min**); Celery task rate limits; Kafka absorbs bulk (**100K+/import**) so HTTP tier is not the bulk meter |

**Per-client:** config/feature flags; GSTIN-keyed Kafka partitions for ordering — not full CH-style tenant DBs.

---

## 5. Menu — service identity + scrape throttle (different problem)

- Jobs use **service accounts**, not end-user JWT.
- “Rate limit” = **anti-bot**: IP rotation, proxy pools, adaptive backoff (drives **95%+** success) — protecting against *external* blocks, not multi-tenant SaaS fairness.
- Downstream: Kafka lag = backpressure; Flink parallelism bounded by partitions.

Do not conflate Menu proxy backoff with IA per-tenant agent quotas.

---

## 6. API level vs AI level (comparison cheat sheet)

| Concern | API level (REST/Gin/FastAPI) | AI level (LangGraph/MCP) |
|---|---|---|
| Identity | JWT / gateway header | Same user/tenant propagated into tool context |
| AuthZ | Route + role + tenant match | Tool allow-list + read-only tools |
| Abuse | RPM / burst / IP | Tool loops, prompt injection, cost bombs |
| Limit unit | HTTP requests | Tool calls, tokens, parallel graphs |
| Failure mode | 429 / 401 / 403 | Refuse tool, ask clarify, gate write |
| Audit | Access + mutation logs | LangSmith run tree + tool args |
| Write path | Authenticated handlers | **Human gates** then product write API |

**One sentence:** “APIs authenticate who you are and throttle requests; the agent stack authorizes *what tools you may call* and budgets *how much non-determinism you may burn*.”

---

## 7. Attack → answer

**Q. How do you stop cross-tenant data leaks?**  
**A.** Tenant id from JWT, not body; CH/PG always filtered; agent tools inherit tenant scope; integration tests attempt cross-tenant IDs and expect 403.

**Q. How do you rate-limit the agent differently from the API?**  
**A.** API: per-route RPM. Agent: max tool calls/session, max parallel clustering jobs/tenant, token budget, timeouts. A 429 on HTTP does not stop an already-running graph — need graph-level budgets.

**Q. What if the LLM ignores the read-only instruction?**  
**A.** Instruction is not the control. Tools are allow-listed functions without write SQL. Write APIs require human confirm tokens / gates.

**Q. Per-tenant limits — numbers?**  
**A.** Mechanism is concurrency + tool + token budgets in config catalogs (no code deploy to change). I will not invent a specific RPM without a measured/doc’d value. kik baselines (8.5% failures) are measured; quotas are product DESIGN.

**Q. FRM — is header auth insecure?**  
**A.** Trusted mesh: only gateway can inject the header on the internal network. Internet-facing would need signed JWT. Tradeoff for audit email capture inside Uber.

**Q. Masters — JWT vs session?**  
**A.** Stateless access tokens for microservices behind gateway; refresh rotation; RBAC on money paths; audit trail for GST compliance data.

---

## 8. 30-second story (IA)

“Multi-tenant AssortSmart: JWT carries tenant and role into Go APIs; every query is tenant-scoped. The copilot only gets 14 read tools and three human gates before write-back. We rate-limit HTTP at the API and budget tool calls, tokens, and parallel jobs per tenant so one retailer’s batch explore cannot starve another’s interactive plan edits.”

---

## Related
- [projects/01d_agentic_evals_guardrails_flow.md](../projects/01d_agentic_evals_guardrails_flow.md)
- [projects/01c_agent_read_tools_defense.md](../projects/01c_agent_read_tools_defense.md)
- [tech_depth/go_gin.md](go_gin.md)
- [architecture/01_ia_assortsmart_hindsight.md](../architecture/01_ia_assortsmart_hindsight.md)
- [architecture/02_uber_frm.md](../architecture/02_uber_frm.md)
