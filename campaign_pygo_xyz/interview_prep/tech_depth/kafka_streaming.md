# Kafka + event-driven bulk paths

## What
Kafka as the event backbone for Masters India bulk e-invoicing (not on Menu PDF).

## How used here
1M+ IRP submissions/day 100K+/import throughput 700→4000 requests/min. Idempotency keys retries DLQ for safe replay.

## Tradeoffs
Async complexity vs sync IRP spikes melting the DB. Quarter sharding on PostgreSQL pairs with Kafka for retention and burst absorption.

## Failure modes
- Dual writes without idempotency
- Poison messages without DLQ
- Consumer lag and backpressure

## Likely questions
How do you guarantee exactly-once-ish effects? What is in your idempotency key? How do you replay DLQ safely? Why Kafka not only Celery?
