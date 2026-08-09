# Masters India & GeeksforGeeks — MongoDB / Elasticsearch (v2)

Added to `resume_v2` Tech Used because you owned them on these roles. Defend like this:

## Masters India
- **Elasticsearch (ELK):** centralized logging — structured JSON logs, correlation IDs, Kibana queries; pairs with the New Relic story (triage ~70% faster). Same stack as the resume “ELK” bullet.
- **MongoDB:** document store for flexible / semi-structured payloads (e.g. client config blobs, import job metadata, or non-relational side collections) alongside PostgreSQL as the system of record for invoices/returns. Say which collections you touched if asked — don’t invent schemas you can’t draw.

## GeeksforGeeks
- **MongoDB:** flexible documents for community/content shapes that didn’t fit cleanly in MySQL alone (or dual-write/read paths during migration). MySQL remained the primary relational store for votes/pins counts.
- **Elasticsearch:** search / feed retrieval over posts and content (full-text), not just logging — distinguish from Masters ELK if asked.

## Interview one-liners
- “Postgres/MySQL for transactional correctness; Mongo where the document shape varied; Elasticsearch for search and (at Masters) the log plane.”
- If probed on indexing: ES inverted index + analyzers; Mongo indexes on query fields; know when you’d pick one over the other.
