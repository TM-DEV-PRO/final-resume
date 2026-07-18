# Role targeting + rapid-fire — Python/Go resume v2

Use with `resume_v2/` / `Tarun_Mittal_SSE_5yr_v2.pdf`.

## New wording you must say correctly

**“Under 1 hour” (IA clustering)**  
“That’s the committed design target from the clustering FRD — we’re building and load-testing against it. Baseline we measured: days of manual config, ~8.5% run failures, one config tried per plan. I don’t claim a year of production p50 on that number yet.”

**“Without lock contention” (ClickHouse)**  
“Append-only inserts + latest-state reads — we don’t take row locks or run ClickHouse mutations for planner overrides. Every decision is an insert; versions resolve via views. That’s concurrency without lock contention, not a claim that the engine is wait-free in the CS sense.”

**“BigQuery on your skills?”**  
“Upstream historical source of truth. I own the ingest lane into ClickHouse (staging → `REPLACE PARTITION`, reconciliation). I don’t claim BigQuery warehouse optimization as my work.”

**“Why drop Mongo/Cassandra/ES/DuckDB/gRPC/Rust from skills?”**  
“Kept what’s evidenced on this resume’s Tech Used lines or the live IA/Uber stack. DuckDB was an earlier serving idea; July 2026 direction is ClickHouse end-to-end. Rust is an in-house escape hatch (CortexEye) — not something I claim as delivered on this PDF.”

**Menu 98% / $600K**  
Same as original prep: offline-eval fidelity; finance-owned savings model — know the arithmetic before quoting.

## Role families

Same lead stories as `../interview_prep/08_role_targeting_and_rapid_fire.md` — IA Go+ClickHouse, Uber Menu streaming, Masters quality/observability, FRM audit correctness.
