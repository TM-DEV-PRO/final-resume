# PostgreSQL + MySQL + Redis + SQLAlchemy

## What
Relational stores + cache. SQLAlchemy 2.0 on FRM MySQL. PostgreSQL quarter sharding on Masters. Redis cache-aside.

## How used here
- FRM: 11-table MySQL schema recon migration Sheets→MySQL.
- Masters: PG sharding + Redis cutting redundant reads 30%.
- IA: thin PG metadata (auth/tenant/workflow) beside ClickHouse.

## Tradeoffs
OLTP correctness vs OLAP speed (CH). Cache freshness vs load. Repository layer vs raw SQL.

## Failure modes
- Column aliasing bugs on joins (FRM fix story)
- Cache stampede
- Shard key mistakes

## Likely questions
Walk SQLAlchemy 2.0 Mapped models. Explain recon v2. How does quarter sharding work? Cache invalidation strategy?
