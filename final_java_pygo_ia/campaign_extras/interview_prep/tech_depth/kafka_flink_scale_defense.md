# Kafka + Flink — where, why at high numbers, how to defend

Interview sheet. Numbers are HISTORICAL / ESTIMATED peaks where noted. Do not invent TPS you never measured.

---

## 1. Where each tech is used (map)

| Place | Kafka? | Flink? | Job |
|---|---|---|---|
| **Uber Menu** | Yes — ingest bus after Selenium | Yes — hot-path validate / keyed dedupe / route | 30K+ menus/mo, 24h→2h, 95%+ success |
| **Masters India GST** | Yes — bulk IRP / e-invoice pipeline | **No** | 1M+/day, 100K+/import, 700→4,000 req/min |
| **Impact Analytics** | Yes — async jobs (embeddings etc.) on Tech | **No** | Not the CH OLAP path |
| **FRM / GFG** | No | No | — |

**One-liner:** Kafka absorbs bursts and enables replay. Flink adds **stateful** stream logic on Menu only. Masters stays Kafka + idempotent workers + PG shards.

---

## 2. Why these tech at “high numbers” (the defense)

### Uber Menu — why not “just call the catalog API from the scraper”

| Pressure | Number / shape | Why sync HTTP dies | Why Kafka | Why Flink |
|---|---|---|---|---|
| Volume | **30K+ menus/month** (~1K+/day average; spikes when vendors refresh) | Scrapers block on slow catalog writes | Buffer + multiple consumers | Continuous process without waiting for batch windows |
| Latency goal | Onboarding **24h → 2h** | Retry storms amplify latency | Decouple scrape success from catalog success | Stateful dedupe avoids redoing work |
| Burstiness | Scrape waves, anti-bot backoff, retries | Thread pool meltdown | Partitioned log absorbs spikes | Backpressure into Kafka lag, not scraper crashes |
| Failure / bad deploy | Parser bug ships | Cannot replay HTTP | **Rewind offsets**, reprocess | Keyed state + watermark rewind |
| Fan-out | Structured path + RAG path + health | One HTTP call cannot fan out cleanly | Many consumer groups | Route in-stream after validate |
| Ordering | Per-vendor menu updates | Race overwrites | Key by vendor/menu id | Keyed state matches that key |

**Rough rate talk (ESTIMATED, say so):**  
30K menus/mo ≈ **~0.4–1 event/s average** if one event per menu, but scrape retries, page chunks, and re-scrapes make the **bus** busier than “30K messages.” Peaks are bursty (vendor batches), not a flat TPS. Defend **burst + replay + fan-out**, not “we ran Flink because we had a million TPS.”

**If interviewer says “30K/month is tiny for Kafka”:**  
Agree averages are modest. Kafka is there for **operational properties** (replay, decoupling, multi-consumer, ordered keys under scrape failure), not because we needed LinkedIn-scale throughput. Flink is there for **keyed dedupe + event-time**, not vanity TPS.

### Masters India — why Kafka at 1M+/day and 4k req/min

| Pressure | Number | Why sync PHP/Laravel workers die | Why Kafka |
|---|---|---|---|
| Daily IRP | **1M+ submissions/day** (~12 TPS avg; **100+ TPS peak ESTIMATED** at filing deadlines) | One slow IRP blocks a worker | Queue absorbs deadline spikes |
| Bulk import | **100K+/import** | Memory + request timeout | Chunk → topics → consumers |
| API throughput | **700 → 4,000 req/min** (~12 → ~67 RPS) | Monolith scaled as one unit | Microservices + async bulk path |
| Safety | Double-file risk | Retries without idempotency | Idempotency keys + DLQ + replay |
| Ordering | Per taxpayer | Race on same GSTIN | Partition key = client GSTIN |

**Why no Flink at Masters:**  
Consumers + Celery/workers + **idempotent DB writes** were enough. Adding Flink would duplicate the pipeline without a stateful windowing/dedupe requirement like Menu’s late scrape pages.

### IA — why Kafka on Tech (light claim)

Async embedding / background jobs off the request path. **Do not** claim Menu- or Masters-scale Kafka ownership at IA. ClickHouse is the OLAP story.

---

## 3. Attack → answer (memorize)

### “Kafka and Flink for only 30K menus a month — overkill?”

**A:** Average rate is not the design driver. Scrapers are **bursty and flaky** (anti-bot, retries). Catalog writes and RAG extraction have different latency profiles. Kafka lets scrape succeed even when downstream is slow, and lets us **replay** after a bad parser. Flink owns **keyed dedupe and routing** so we do not double-apply the same vendor menu when late pages arrive. If we only had Celery sync chains, a bad deploy meant re-scrape the internet instead of rewind the log.

### “Prove you needed Flink, not just Kafka consumers.”

**A:** Plain consumers are fine for fire-and-forget transforms. We needed **keyed state** (per vendor/menu), **event-time** for late HTML, and a single job that **validates → dedupes → routes** structured vs unstructured before catalog/RAG. That is Flink’s sweet spot. Spark is worse for the hot path (micro-batch delay); we keep Spark as **verbal backfill**.

### “What was the peak events/sec on Menu?”

**A:** I do not claim a measured Flink peak TPS on the resume. What is HISTORICAL is **30K+ menus/month**, **24h→2h**, **95%+** successful ingestions. Peak bus rate is **ESTIMATED** from scrape fan-out and retries — I will not invent a vanity number. I defend architecture under burst + failure, not a fake million-TPS slide.

### “Masters 1M+/day — was that Kafka or the API?”

**A:** Both. Interactive API path hit **4,000 req/min** after the FastAPI strangler. Bulk IRP submissions (**1M+/day**, **100K+/import**) ride **Kafka** so filing-deadline spikes do not melt Postgres. Idempotency keys stop double filing on replay.

### “How do you get exactly-once?”

**A:** End-to-end exactly-once is a slogan. Practical recipe: Kafka at-least-once + **idempotent sink** (Menu: catalog upsert keyed by vendor/menu version; Masters: `client + fileHash + batchIndex`). Flink can use transactional sinks into Kafka; the catalog still needs idempotent writes. DLQ for poison messages; never infinite retry on bad payload.

### “Bad Flink/parser deploy — recovery?”

**A:** Stop the job → fix → **rewind Kafka** to offsets before the bad watermark → reprocess. Gaps that need heavy history → Spark/batch backfill (verbal). Scrapers do not re-hit the open web for every repair if the raw payload is still in object storage / log.

### “Why Kafka not RabbitMQ / SQS / only Celery?”

**A:** We needed a **replayable, partitioned, multi-consumer log** with per-key ordering. Celery is a task queue (good for jobs); it is a weaker audit/replay bus for “reprocess last Tuesday’s scrapes.” SQS lacks the same ordered multi-subscriber log story we used. Kafka matched Menu fan-out and Masters IRP consumers.

---

## 4. Scale cheat sheet (say tags out loud)

| Claim | Tag | Notes |
|---|---|---|
| 30K+ menus/month, 24h→2h, $600K+, 95%+ | HISTORICAL | Menu outcomes |
| Kafka + Flink on Menu | HISTORICAL architecture | On campaign PDF |
| Menu peak events/sec | ESTIMATED if discussed | Do not put on PDF |
| 1M+ IRP/day, 100K+/import | HISTORICAL | Masters |
| ~12 TPS avg / 100+ TPS peak | ESTIMATED from 1M+/day | Say estimated |
| 700 → 4,000 req/min | HISTORICAL | Masters API |
| Spark / Pinot | STUDY / verbal | Not on PDF |

---

## 5. 20-second stories

**Menu:** “Scrapers are bursty. Kafka is the replayable bus. Flink does keyed dedupe and routes structured vs RAG paths so catalog freshness stays hours not a day. That is how 30K+ menus/month moved from 24h to 2h onboarding.”

**Masters:** “Filing deadlines spike IRP traffic. Kafka plus idempotent consumers and PG quarter shards took us to 1M+ submissions/day and 4,000 req/min without double-filing on replay. No Flink — workers were enough.”

---

## Related
- [flink.md](flink.md) · [kafka_streaming.md](kafka_streaming.md)
- [../architecture/03_uber_menu.md](../architecture/03_uber_menu.md)
- [../architecture/04_masters_gst.md](../architecture/04_masters_gst.md)
- [../deployment_and_scale.md](../deployment_and_scale.md)
