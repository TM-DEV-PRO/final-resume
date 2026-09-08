# Cold Mail Recruiter / Sourcer

Aligned to **Final Java + AI** (`Tarun_Mittal_SSE_5yr_Java_AI.pdf`). Paste-ready. Adapted from the AssortSmart-tab packet templates; claims match the **current PDF**, not packet overclaims (no K8s-ops, no IA Flink/CDC).

## Email subject lines (pick one)
- Senior Software Engineer Java Spring Uber FRM + AssortSmart platform/AI
- 5y backend · Go/Gin 10k RPS · ClickHouse 4B-row rollups · Kafka 1M+/day · LangGraph
- Referral-ready Senior SWE (Java · Python · Go) [Company] [Req ID]

## Email body (long)
Hi [Name]

I am Tarun Mittal, a Senior Software Engineer (Java, Python and Go) with 5 years owning production backends and applied-AI systems. Quick proof points from the resume:

- Impact Analytics AssortSmart: multi-tenant Go/Gin platform at 10k peak RPS (Wire, h2c, Datadog). ClickHouse pivots 189s to 12s on 250M-row operations across six rollup tables. Weekly grain after a roughly 170 GB OOM. Go native TLS pump at about 344k rows/s combined, measured on a 4.09B-row attr weekly set. Keep/Drop on 348k article-seasons + shipped Ask Iris. 300-case / 80% CI promotion gate.
- Uber via EPAM FRM: 36 Spring Boot endpoints, 19M GL rows, L1–L4 FSLI, 8-table SOADB, SHA-256 keys; 70% recon cut from 14 days to 3 against $340M; led 3; 100% coverage; SOX 50% delta-variance.
- Uber Eats menu: 24 hours to 2 hours, $600K/yr, 30K+ menus/month, 98% offline RAG/Milvus, Kafka+Flink exactly-once.
- Masters India: Spring Boot strangler, p95 1.2s to 300ms, Kafka e-invoicing 1M+/day; mentored 2.

I am targeting [Senior SWE / SDE2 / MTS] roles on [Team]. Resume attached. Happy to do a 15-minute screen this week.

Thanks
Tarun Mittal
(+91) 9079727197 · tmittaliet@gmail.com
linkedin.com/in/t-mittal · github.com/TM-DEV-PRO

## LinkedIn DM short
Hi [Name] Senior SWE Java/Spring + Go 5y. Owned Uber FRM (36 endpoints, led 3) Kafka 1M+/day and now AssortSmart Go/Gin 10k RPS + LangGraph Keep/Drop. Open to [Role]? Can send resume.

## LinkedIn DM long
Hi [Name] — hire-for-fit in one glance: Uber (via EPAM) FRM owner (36 Spring Boot endpoints, 70% 14d to 3d, led 3) + Menu E2E ($600K/yr, 24h to 2h, Kafka/Flink) + Masters Kafka 1M+/day + current AssortSmart Go/Gin 10k RPS, ClickHouse six rollup tables, Go pump at about 344k rows/s combined on a 4.09B-row attr weekly set, and shipped Ask Iris. Looking at [Company] senior backend / data platform / applied-AI roles. If you are sourcing for [Team] I would love a quick screen. Resume here: [link].

## Data platform hook (honest)

Do not send: "I stream 4.09 billion rows at 344,000 rows/second."

Send: "I built six ClickHouse rollup tables for planner reads and a Go pump that copies season partitions at about 344k rows/s combined, measured on a 4.09B-row attr weekly set. Weekly grain is one fiscal week per INSERT after a roughly 170 GB OOM."

Fit: Senior SWE plus Data Infrastructure / Core Platform / Data Engineering. Keep Java SSE tracks. Do not open-source the copier (hosts, DDL, passwords). Whiteboard it. Pack: `prep/42_clickhouse_rollup_migration.md`.
