# 07. Masters India: GST Compliance & E-Invoicing Platform

<div class="callout note">
<b>How to use this chapter</b>
<ul>
<li><b>What it covers:</b> my SDE 2 role at Masters India (Noida, December 2022 to June 2024). The product is a GST e-invoicing platform. The chapter covers the PHP-to-Spring Boot migration, the Kafka bulk pipeline, PostgreSQL sharded by tax quarter, idempotency, retries and dead-letter queues, Redis caching, ELK and New Relic, and test coverage.</li>
<li><b>When to read it:</b> before any interview that may ask about "a migration you led", "a high-throughput pipeline", "idempotency", "Kafka vs a queue", "how you made an API faster" or "how you use Spring Boot in production".</li>
<li><b>What to memorise:</b> p95 from 1.2 seconds to 300 milliseconds (75% lower), 1,500+ enterprise clients, 700 to 4,000 requests per minute, 1M+ government submissions a day, 100K+ invoices processed concurrently in bulk imports, triage 70% faster, database reads 30% lower, coverage from 35% to 82%, 98% deploy success, mentored 2 engineers.</li>
<li><b>Tags used here:</b> HISTORICAL means it comes from my past work records and resume. ESTIMATED means it is arithmetic I can show on a whiteboard. If an illustration uses made-up sample numbers or sample code, I say "illustrative" next to it.</li>
</ul>
</div>

Related pages: [Start here](00_START_HERE.md) · [Every number explained](02_numbers_explained.md) · [Tech glossary](09_tech_glossary.md) · [Core concepts](10_core_concepts_explained.md) · [STAR stories](11_star_stories.md) · [Next chapter: GeeksforGeeks](08_geeksforgeeks.md). Older source packs: [Masters and GFG interview packs](../prep/23c_masters_gfg_interview_packs.md), [Masters and GFG deep dive](../prep/12_masters_gfg_deep_dive.md), [tables and why each tech](../prep/34_er_tables_tech_why.md), [schemas and APIs](../prep/35_table_schemas_api_design.md).

Resume stack for this role (Java + Python track, `Tarun_Mittal_SSE_5yr_Java_AI.pdf`): **Java, Spring Boot, Hibernate, Kafka, PostgreSQL, MongoDB, Redis, Elasticsearch, Docker, ELK, New Relic, AWS.**

---

## 2. The one-minute version

Say this out loud, roughly as written:

> "At Masters India I worked on a GST e-invoicing platform used by more than 1,500 enterprise clients. Indian businesses must register every B2B invoice with a government portal, which gives back an official invoice number and a signed QR code. Our job was to validate their invoices and register them safely, at volume.
>
> I led the migration of a legacy PHP monolith to Spring Boot microservices. We did it gradually, one route at a time behind the gateway, with a small canary percentage first and rollback by a config change. That cut p95 latency by 75%, from 1.2 seconds to 300 milliseconds, and throughput went from 700 to 4,000 requests per minute. I also mentored two engineers through it.
>
> I designed the bulk e-invoicing pipeline: a Kafka event bus, PostgreSQL sharded by tax quarter, and idempotency keys so a retry can never register the same invoice twice with the government. It handled 1M+ submissions a day. Failed batches went to dead-letter queues with bounded retries, because the government portal is often slow or down near filing deadlines.
>
> On the operations side, ELK logging and New Relic tracing with one request ID cut incident triage time by about 70%. A Redis cache cut database reads by 30%. I also pushed test coverage from 35% to 82%, which got us to a 98% deployment success rate."

---

## 3. The business in plain English

### What GST is

**GST (Goods and Services Tax)** is India's main indirect tax, introduced in July 2017. It replaced a long list of separate central and state taxes with one system. Every registered business gets a **GSTIN (GST Identification Number)**, a 15-character ID such as `29ABCDE1234F1Z5`. The first two digits are the state code. The middle ten are the business's PAN (tax ID). The last characters are an entity number and a checksum.

When a business sells to another business, the invoice shows the tax. Within one state the tax splits into **CGST** (central) and **SGST** (state). Across states it is **IGST** (integrated). The buyer later claims an **input tax credit**: "I already paid ₹18,000 of tax to my supplier, so subtract it from what I owe." That credit is why invoice accuracy matters to both sides. A wrong or missing invoice costs the buyer money, not only the seller.

Businesses file periodic **returns** (statements of their sales and tax) on fixed monthly or quarterly due dates. Reconciliation and audits look at a tax period, so the data naturally groups by period.

### What an e-invoice is

An **e-invoice** does not mean "a PDF sent by email". It means the invoice is **registered with the government** before it is legally valid for B2B use. Since 2020 India has required this for businesses above a turnover threshold, and the threshold has been lowered in phases, so more and more businesses fall under it.

The government runs the **IRP (Invoice Registration Portal)**. The flow is:

1. The seller's ERP (accounting software, like SAP or Tally) creates the invoice.
2. The invoice JSON is sent to the IRP.
3. The IRP validates it and returns an **IRN (Invoice Reference Number)**. This is a unique 64-character hash that identifies the invoice in the government's records.
4. The IRP also returns a **digitally signed QR code**. The QR carries the key invoice details plus the government's signature, so anyone can scan it and verify the invoice is genuine.
5. The seller prints the QR on the invoice and sends it to the buyer.

Think of the IRP like a notary office. You bring a document, the notary checks it, stamps it with a unique serial number and signs it. After that it is an official record.

### Where Masters India fits

Most enterprises do not want to talk to the government API directly. It has strict schemas, authentication tokens that expire, rate limits and bad days. Masters India sat in between. Clients sent invoices to us (one at a time from their ERP, or as bulk files with thousands of rows). We validated them, registered them with the IRP, stored the IRN and signed QR, and returned them to the client by API response or webhook. On top of that the product did bulk imports, reconciliation against GST returns, and audit trails. We served **1,500+ enterprise clients** (HISTORICAL).

### Why double registration is unrecoverable

This is the single most important constraint, and it is why idempotency appears everywhere in this chapter.

Once the IRP issues an IRN, that invoice is a legal record at the government. You cannot edit it. Under the GST rules as I worked with them, cancellation is allowed only in full and only within a short window (24 hours). After that, correcting a mistake needs credit notes and adjustments through returns, which is slow, manual and visible to auditors. If a retry bug registered the same sale twice (say, with a regenerated document number), the client would have two legal invoices for one sale. The buyer's tax credit and the seller's returns would no longer match. That shows up as a compliance problem for our client, and it is not something an engineer can "roll back".

So the design rule was: **retries must be safe**. Any step that talks to the IRP must be able to run twice and still produce exactly one registration.

<div class="callout warn">
<b>Say this carefully.</b> The 24-hour cancellation window and the "cannot edit" rule are general GST rules, not something I built. If an interviewer is a GST expert, keep it at "cancellation is narrow and time-limited, so a double registration becomes a compliance problem for the client". Don't argue tax law.
</div>

### Filing-deadline spikes

Businesses tend to do tax work close to due dates. On the days before a return deadline, many clients upload a whole month or quarter of invoices at once. Load on those days is many times the normal average, and the IRP itself is under load too, so it gets slower and returns more errors at exactly the same moment. Normal days are easy. The system has to be built for the deadline day.

### What hurt before, and why the company paid for this

Before the work in this chapter, the backend was a **PHP (Laravel) monolith**:

- It was **synchronous**. A request that called the IRP held a PHP worker for the whole round trip. When the IRP was slow, workers ran out and every other request queued behind them, even ones that had nothing to do with the IRP.
- **Deploys were all-or-nothing.** A change to reconciliation meant redeploying e-invoice submit too.
- **Scaling meant scaling everything.** You could not add capacity just for the bulk import path.
- **Debugging meant SSH into boxes and grep logs**, with no way to follow one request across components.

For a compliance product, a timeout on a filing day loses client trust fast. The company paid for the migration and the pipeline because faster, safer registration on deadline days is the product.

---

## 4. Words you need

**General terms**

| Term | Plain meaning |
|---|---|
| **Monolith** | One big application that holds every feature and deploys as one unit. Like a single restaurant kitchen where one cook does starters, mains and dessert. If he is stuck on one dish, everything waits. |
| **Microservices** | Many small services, each owning one job (auth, submit, bulk import, reconciliation), deployed separately. Like separate kitchen stations. |
| **Strangler fig pattern** | A way to replace an old system gradually. You put new code next to the old one and move traffic route by route until the old system has nothing left. Named after a fig vine that slowly grows around a tree and replaces it. |
| **Gateway** | The front door every request passes through. Here it was Nginx. It decides which backend gets each request. |
| **Canary release** | Sending a small slice of traffic (for example 5% or 10%) to new code first and watching errors and latency before sending more. From "canary in a coal mine": a small early warning. |
| **Non-blocking (async) IO** | A style where a thread starts a slow network call and is free to do other work while waiting, then resumes when the answer arrives. Like a waiter who takes the next table's order while the kitchen cooks, instead of standing at the kitchen door. |
| **Connection pooling** | Keeping a set of open database connections and reusing them, instead of opening a new one for every request. Like keeping a phone line open instead of redialling for every sentence. |
| **N+1 query** | A bug where code runs 1 query to fetch a list, then 1 more query per item. Fetching 50 invoices and their lines this way is 51 queries instead of 2. |
| **p95 latency** | The response time that 95% of requests are at or below. Explained with an example in section 7. |
| **Throughput** | How many requests the system completes per unit of time (here, per minute). |
| **Kafka** | A durable, ordered log of messages. Producers append messages. Consumers read at their own pace and remember their position. Messages stay for a retention period, so you can re-read them. |
| **Topic, partition, offset** | A topic is a named stream (like `irp.completed`). It is split into partitions for parallelism. Order is guaranteed only within one partition. The offset is a consumer's bookmark in a partition. |
| **Partition key** | The value used to choose a partition. Messages with the same key always go to the same partition, so they stay in order. |
| **Consumer group** | A team of consumers that share a topic's partitions. Different groups each get their own full copy of the stream. |
| **Replay** | Moving a consumer group's offset back so it reprocesses old messages, for example after fixing a bug. |
| **Sharding** | Splitting one large dataset into separate pieces (shards) by some rule, so each piece is smaller and can be managed on its own. |
| **Idempotency** | An operation is idempotent if doing it twice has the same effect as doing it once. Pressing a lift button five times still calls one lift. |
| **Idempotency key** | A unique ID attached to a piece of work so the system can recognise "I have already done this one". |
| **Dead-letter queue (DLQ)** | A side queue where messages that keep failing are parked, so they stop blocking the main flow and can be inspected and replayed later. Like a "problem parcels" shelf in a post office. |
| **Exponential backoff with jitter** | Waiting longer after each failed retry (1s, 2s, 4s, 8s), plus a random amount, so thousands of clients don't all retry at the same instant. |
| **Redis** | An in-memory key-value store, very fast. Used here as a cache. |
| **Cache-aside** | The app checks the cache first. On a miss it reads the database, stores the result in the cache with an expiry (TTL), then returns it. |
| **Cache stampede** | When a popular cache key expires and hundreds of requests all miss at once and hammer the database together. |
| **ELK** | Elasticsearch (stores and searches logs), Logstash (collects and parses logs), Kibana (the search and dashboard UI). |
| **New Relic** | An APM (Application Performance Monitoring) product. It shows how long each request takes, broken down into database calls, external calls and code. |
| **Request ID** | A unique ID stamped on a request at the front door and carried through every service, queue message and log line it touches, so you can find everything about one request with one search. |
| **Test coverage** | The percentage of code lines that run during automated tests. |
| **Deploy success rate** | The share of production deployments that go out without failing or needing a rollback. |

**Spring and Java terms used in this chapter**

| Term | Plain meaning |
|---|---|
| **Spring Boot** | A Java framework that starts a ready-to-run web service with sensible defaults: an embedded web server, configuration, database pooling, metrics. You write the business code and Spring wires the parts together. Like a fitted kitchen where the plumbing and wiring are already in, so you only bring the recipes. |
| **Bean / dependency injection** | Spring creates the objects your code needs (called beans) and hands them to the classes that ask for them in their constructor. You don't call `new` on a database client yourself. |
| **`@RestController`** | An annotation that marks a class as an HTTP API. Methods tagged `@PostMapping` or `@GetMapping` handle one route each, and their return values are turned into JSON. |
| **Bean Validation** | Annotations such as `@NotBlank`, `@Pattern` and `@NotNull` on request fields. Adding `@Valid` on a controller parameter makes Spring reject a bad request with a 400 before your code runs. Like a security guard who checks ID at the door so the people inside don't have to. |
| **Hibernate / JPA** | JPA (Java Persistence API) is the standard way to map Java classes to database tables. Hibernate is the library that implements it. An `@Entity` class is one table, and a repository interface gives you queries without hand-written SQL. |
| **HikariCP** | The connection pool Spring Boot uses by default. It keeps a fixed number of PostgreSQL connections open and lends them to requests. |
| **Spring Kafka** | Spring's Kafka integration. `KafkaTemplate` is the producer you call to publish a message. `@KafkaListener` marks a method that Spring calls for each message a consumer group receives. |
| **`DefaultErrorHandler` and `DeadLetterPublishingRecoverer`** | Spring Kafka's error handling. When a listener throws, the error handler retries the message on a back-off schedule. When retries run out, the recoverer publishes the message to a dead-letter topic and the consumer moves on. |
| **`ExponentialBackOff`** | A retry schedule object: start with a small wait, multiply it each time, stop at a maximum. |
| **Spring Batch** | A framework for large, restartable batch jobs. A "step" reads items, processes them and writes them in chunks (for example 500 rows at a time), and records progress so a crashed job can restart from the last finished chunk. |
| **`@Async` and `@Scheduled`** | `@Async` runs a method on a background thread pool so the caller doesn't wait. `@Scheduled` runs a method on a timer, like a cron job inside the service. |
| **WebClient** | Spring's non-blocking HTTP client, used here to call the IRP with strict timeouts. |
| **Servlet filter** | Code that runs on every HTTP request before it reaches a controller. A good place to stamp a request ID. |
| **MDC (Mapped Diagnostic Context)** | A per-thread map that the logging library adds to every log line. Put `request_id` in it once, and every log line on that thread carries it. |
| **`AbstractRoutingDataSource`** | A Spring class that picks one of several databases or schemas at runtime from a key you set, for example a tax quarter. |
| **JUnit 5, Mockito, JaCoCo** | JUnit 5 runs Java tests. Mockito creates fake versions of dependencies (a fake IRP client, a fake repository) so a test runs fast and offline. JaCoCo measures which lines the tests executed and can fail the build if coverage drops. |

---

## 5. Architecture

```mermaid
flowchart LR
  ERP["Client ERP or dashboard"] --> GW["Nginx gateway with per-route canary"]
  GW -->|"routes not yet migrated"| PHP["PHP monolith"]
  GW -->|"migrated routes"| API["Spring Boot services: auth, submit, bulk import, reconciliation"]
  API --> RD["Redis cache: client config, GSTIN masters, IRP tokens"]
  API --> PG["PostgreSQL sharded by tax quarter"]
  API --> S3["Amazon S3: uploaded bulk files"]
  API --> BATCH["Spring Batch import jobs: chunked validation"]
  API --> SIDE["Async and scheduled tasks: PDFs, emails, nightly jobs"]
  BATCH --> KF["Kafka topics"]
  API --> KF
  KF --> W1["IRP submit consumers"]
  W1 -->|"bounded concurrency, retries"| IRP["Government IRP"]
  W1 --> DLQ["Dead-letter topics"]
  KF --> W2["Persistence and webhook consumers"]
  W2 --> PG
  W2 --> MG["MongoDB: signed IRP response snapshots"]
  W2 --> HOOK["Client webhooks"]
  API --> OBS["ELK logs and New Relic traces, joined by request ID"]
  W1 --> OBS
```

*What to notice:* the PHP monolith and the Spring Boot services sit side by side behind one gateway during the migration. Everything that talks to the government IRP sits behind Kafka, consumers and retries, never inside a user's request thread.

**Walking through it box by box:**

- **Client ERP or dashboard.** Enterprise clients call our API from their accounting system, or upload bulk files through our dashboard.
- **Nginx gateway.** The front door. During the migration it decided, per route, whether a request went to the old PHP code or the new Spring Boot service, and what percentage went to each.
- **PHP monolith.** Kept serving any route not yet migrated. Over time it served less and less.
- **Spring Boot services.** Split by domain: auth, single e-invoice submit, bulk import and reconciliation. `@RestController` classes exposed the routes, and Bean Validation checked every request at the boundary.
- **Redis.** Held hot, repeated lookups: client configuration, GSTIN master data, tax-rate masters and IRP auth tokens.
- **PostgreSQL sharded by tax quarter.** The system of record for invoices and their IRP registration status. Each tax quarter had its own table set, and the data-access layer picked the right one from the invoice date. Hibernate handled the entity mapping.
- **Amazon S3.** Bulk files landed here first, so the upload request could return quickly.
- **Spring Batch import jobs.** Read an uploaded file in chunks, validated each row, and published accepted batches to Kafka.
- **Async and scheduled tasks.** Side work that does not need a replayable log: PDF generation, emails and nightly jobs, run with `@Async` and `@Scheduled`.
- **Kafka.** The event bus between pipeline stages: invoices accepted, submit jobs, IRP results, webhooks, and dead-letter topics.
- **IRP submit consumers.** `@KafkaListener` methods that read submit messages, called the IRP with a cap on how many calls run at once, retried with backoff, and parked failures in the dead-letter topic.
- **Persistence and webhook consumers.** Read IRP results, wrote the IRN and status to PostgreSQL, saved the full signed response in MongoDB, and notified the client by webhook.
- **MongoDB.** Stored the raw signed IRP responses and invoice payload snapshots. Their shape varies, and we needed them for audits.
- **ELK and New Relic.** Every component logged structured JSON with the request ID. New Relic traced requests end to end.

---

## 6. One job, step by step: a bulk import

**Sample job (illustrative data):** Acme Steel Pvt Ltd, GSTIN `29ABCDE1234F1Z5`, uploads `acme_oct_2023.xlsx` with 12,000 invoices for October 2023 two days before their filing deadline. Say the file is split into batches of 500 rows, which gives 24 batches. The batch size is illustrative. If asked for the real chunk size, keep it qualitative.

```mermaid
sequenceDiagram
  participant C as Client dashboard
  participant A as Spring Boot bulk service
  participant S as S3
  participant V as Spring Batch import job
  participant K as Kafka
  participant W as IRP submit consumers
  participant I as Government IRP
  participant P as PostgreSQL and MongoDB
  C->>A: POST bulk import with file
  A->>S: store file, compute fileHash
  A-->>C: 202 Accepted with import_id
  A->>V: launch chunked validation job
  V->>V: schema, GSTIN and duplicate checks per chunk
  V->>K: publish invoice.accepted, key is GSTIN
  K->>W: deliver message to submit group
  W->>P: check idempotency key, mark irp_pending
  W->>I: register invoice
  I-->>W: IRN and signed QR
  W->>K: publish irp.completed
  K->>P: persistence consumer writes IRN, status, snapshot
  P-->>C: progress and webhook to client
```

*What to notice:* the client gets an answer (202 plus an import ID) within the first request. All the slow work happens after that, and every IRP call is protected by an idempotency check first.

**The same flow in words:**

1. Acme uploads the file. The bulk service stores it in S3 and computes a SHA-256 hash of the file contents, the `fileHash`.
2. The service answers right away with `202 Accepted` and an `import_id`. The browser does not wait for 12,000 registrations.
3. A Spring Batch job validates the file chunk by chunk. Each row is checked for schema, the buyer's GSTIN format and master data, and duplicates. Each chunk is one batch and gets the idempotency key `client + fileHash + batchIndex`, for example `acme:9f2c...e1:7` for batch 7.
4. Valid batches are published to the Kafka topic `invoice.accepted` with the GSTIN as the partition key, so every Acme message stays in order on one partition.
5. An IRP submit consumer picks up the message. It first checks PostgreSQL. If this key is already `registered`, it skips the call. If not, it marks the row `irp_pending` and calls the IRP.
6. The IRP returns the IRN and signed QR. The consumer records `registered` and publishes `irp.completed`.
7. A persistence consumer writes the IRN and status into the right quarter table. Invoice `INV-2023-10-0457`, dated 14 October 2023, lands in the table for financial year 2023, quarter 3. The raw signed response goes to MongoDB.
8. The dashboard shows progress ("batch 7 of 24 done, 3 rows failed validation"), and a webhook tells Acme's ERP which invoices are registered.
9. If the IRP keeps failing for one batch, that batch goes to the dead-letter topic after a bounded number of retries. The other 23 batches carry on.

---

## 7. Each resume bullet decoded

### Bullet 1: the migration, latency and throughput

> "Reduced p95 API latency by **75%** (from **1.2s to 300ms**) across **1,500+** enterprise clients by spearheading the migration of a legacy PHP monolith to a **Spring Boot** microservices architecture. Mentored two engineers through the transition, optimizing backend design to drive overall system throughput from **700 to 4,000 requests per minute**."

#### In plain words

I led the move from one old PHP application to a set of small Java Spring Boot services. I did it gradually, so clients never saw a big-bang switch. Responses got much faster for the slowest requests, the system could handle almost six times as many requests per minute, and two engineers learned to extract and ship services on their own.

#### How it works: the strangler-fig migration

We never turned the monolith off in one go. New Spring Boot services went live behind the existing Nginx gateway one domain at a time: auth, e-invoice submit, bulk import, reconciliation. The monolith kept serving everything else.

```mermaid
flowchart LR
  C["Client request"] --> G["Nginx gateway"]
  G -->|"auth route: 100 percent new"| FA["Spring Boot auth service"]
  G -->|"submit route: 10 percent canary"| FS["Spring Boot submit service"]
  G -->|"submit route: 90 percent old"| P["PHP monolith"]
  G -->|"reconciliation: not migrated yet"| P
  FA --> DB["Shared database"]
  FS --> DB
  P --> DB
```

*What to notice:* the decision is per route, not per system. One route can be fully moved, another split 10/90, another untouched. All three read the same database, so there is only ever one source of truth. The percentages are illustrative.

The playbook, step by step:

1. **Pick one route.** Build the Spring Boot version.
2. **Contract tests first.** We recorded the monolith's responses for the top endpoints and asserted that the Spring Boot replacement returned the same fields, field for field. Clients never saw a payload change.
3. **Canary.** Nginx sent a small percentage of that route's traffic to the new service. We watched error rate and latency dashboards.
4. **Ramp or roll back.** If the numbers looked good, we raised the percentage step by step to 100. If not, rollback was a config change and an Nginx reload, not a redeploy.
5. **Shared database during cutover.** Old and new code read and wrote the same database while traffic moved. We split service-owned tables only after a route was fully on Spring Boot. We avoided dual writes on purpose.
6. **Async by default.** Anything that called a third party (the IRP, PDF generation, webhooks, email) went to background consumers or tasks with retries and idempotency keys, so request threads never waited on someone else's server.

One way to express a per-route canary in Nginx (illustrative, not our exact config):

```nginx
split_clients "${request_id}" $submit_backend {
    10%   springboot_submit;
    *     php_monolith;
}

location /api/v1/einvoice/submit {
    proxy_pass http://$submit_backend;
}
```

Rollback means changing `10%` to `0%` and reloading Nginx. That takes seconds and needs no build.

#### What a migrated route looks like in Spring Boot

Here is the single-invoice submit route as a Spring Boot controller (illustrative). The request is a Java record with Bean Validation annotations. `@Valid` makes Spring reject a malformed invoice with a 400 before any of our code runs, which matters because the government rejects bad payloads anyway. The controller does not call the IRP. It stores the invoice, publishes a Kafka message and answers `202 Accepted`.

```java
public record InvoiceRequest(
        @NotBlank @Pattern(regexp = "^[0-9]{2}[A-Z0-9]{13}$") String sellerGstin,
        @NotBlank String docNo,
        @NotNull @PastOrPresent LocalDate invoiceDate,
        @NotEmpty List<@Valid LineItem> lines) {}

@RestController
@RequestMapping("/api/v1/einvoice")
class EInvoiceController {
    private final SubmitService submit;

    EInvoiceController(SubmitService submit) { this.submit = submit; }   // injected by Spring

    @PostMapping("/submit")
    ResponseEntity<SubmitAccepted> submit(@RequestHeader("Idempotency-Key") String key,
                                          @Valid @RequestBody InvoiceRequest req) {
        return ResponseEntity.accepted().body(submit.accept(key, req));  // stores row, publishes to Kafka
    }
}
```

The GSTIN pattern above is simplified for the example. The real checks also validated the state code and checksum against master data.

#### What p95 means, with 100 requests

Latency is how long one request takes. An average hides the slow ones, so we use **percentiles**. Take 100 requests, sort them from fastest to slowest, and look at the 95th one. Its time is the **p95**. It means "95% of requests were this fast or faster".

Illustrative "before" picture, not real logs:

- 70 requests took around 300 to 500 ms (simple reads).
- 25 requests took 600 ms to 1.2 s (lists with N+1 queries, waiting for a free PHP worker).
- 5 requests took 2 to 6 seconds (stuck behind a slow IRP call).

Sorted, request number 95 sits at the top of the middle group, about **1.2 seconds**. That is the p95.

Illustrative "after" picture: the IRP calls left the request path, list queries were fixed, and hot reads came from Redis. Now 95 of 100 requests finish at or under about **300 ms**, so the p95 is 300 ms.

Why p95 and not average: a client with a 12,000-row import calls us thousands of times. Even a small share of slow calls hits them over and over. p95 tracks what the unluckiest regular users feel.

#### Where the 1.2 s to 300 ms win came from

Caching alone cannot do that. Four changes added up:

1. **Async, non-blocking IRP calls.** In PHP, a request that called the IRP held a worker for the whole round trip. When the IRP was slow, workers ran out and unrelated requests queued. In the Spring Boot services, IRP work moved off the request path entirely: the client gets `202 Accepted` and polls or receives a webhook, and Kafka consumers make the call. Those consumers used WebClient with strict timeouts and a fixed number of consumer threads, so a slow IRP could never eat every thread in the service. This mostly fixed the **tail**, the slowest requests.
2. **Connection pooling with HikariCP.** PHP-FPM opened database connections per request. Each Spring Boot service kept a HikariCP pool of open connections and reused them, which removed connection setup from every request.
3. **Query and index fixes found during the rewrite.** We added missing composite indexes like `(client_id, invoice_date)`, removed N+1 list queries, and added pagination to list endpoints.
4. **Redis for repeated reads.** Client config, tax-rate masters, GSTIN lookups and auth context came from cache. This mostly sped up the **body** of the distribution, the typical request.

A short way to say it: "Async IRP calls, pooling and query fixes moved the tail. Redis moved the body."

The pool is a few lines of Spring Boot configuration. The values here are illustrative:

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20      # connections kept open per service instance
      connection-timeout: 2000   # ms to wait for a free connection before failing fast
```

An N+1 fix in one picture (illustrative Hibernate). By default, touching `invoice.getLines()` on a lazy collection fires one query per invoice. Hibernate's `@BatchSize` tells it to load the lines for up to 50 invoices with one `IN (...)` query instead.

```java
// Before: 1 query for the page of invoices + 1 query per invoice for its lines
List<Invoice> page = invoiceRepo.findByClientIdOrderByInvoiceDateDesc(clientId, PageRequest.of(0, 50));
page.forEach(inv -> inv.getLines().size());   // lazy load, one query each

// After: 2 queries total, whatever the page size
@Entity
public class Invoice {
    @Id private Long id;

    @OneToMany(mappedBy = "invoice", fetch = FetchType.LAZY)
    @BatchSize(size = 50)            // lines for up to 50 invoices in one IN query
    private List<InvoiceLine> lines;
}
```

#### Throughput: 700 to 4,000 requests per minute

The arithmetic:

- 700 requests per minute ÷ 60 seconds = about **12 requests per second** (11.7).
- 4,000 requests per minute ÷ 60 seconds = about **67 requests per second** (66.7).
- 4,000 ÷ 700 = about **5.7 times** the capacity.

It went up for the same reasons latency went down. Threads were no longer pinned waiting on the IRP. Pooled connections were cheaper. Queries were lighter. Each service could scale on its own, and my notes also mention worker autoscaling on queue depth. This was sustained throughput of the gateway and services under load (HISTORICAL).

#### Mentoring two engineers

Two junior engineers each owned individual service extractions. I set the conventions everyone followed: controller, service and repository layers, Bean Validation on request DTOs (data transfer objects, the plain classes that describe a request or response) at the boundary, and shared retry and idempotency helpers. I reviewed every one of their PRs closely for the first months and paired with them on the first canary cutover. By the end both were shipping services on their own. This is **mentoring**, not people management.

#### Why this design

- **Why gradual instead of a rewrite?** It is a compliance product. A broken filing day is not acceptable. Per-route cutover meant any mistake affected one route, for a small percentage of traffic, and could be undone in seconds.
- **Why Spring Boot?** One framework covered every need of this system. Spring Kafka gave consumer groups, retries and dead-letter publishing with little custom code. Spring Batch gave restartable, chunked bulk imports. Bean Validation gave strict checks at the boundary, which matters when the government rejects bad payloads. Hibernate and HikariCP gave mapped entities and pooled connections out of the box. Strong typing helps when the code is full of tax rules and money fields. And each service stays small.
- **Why a shared database during cutover?** So there is one source of truth. Dual writes (old and new code each writing their own copy) create reconciliation problems, which is the worst kind of bug in a tax product.

#### Alternatives and why not

| Alternative | Why not |
|---|---|
| Big-bang rewrite and one switch-over day | One mistake breaks every route at once, on a product where a failed filing day hurts clients. No partial rollback. |
| Keep PHP and tune it | The core problem was synchronous IRP calls pinning workers. Tuning PHP-FPM worker counts only moves the cliff. |
| Django | Good framework, and I used it at GeeksforGeeks. Its strengths are an admin panel and a full ORM. Here the needs were Kafka consumers with retries and DLQs, restartable bulk imports and strict typed validation, which Spring Boot covers in one stack. |
| Dual writes to old and new databases | Two sources of truth during a money-and-tax migration. We avoided it on purpose. |

#### Trade-off

For a while we ran two stacks side by side, which meant more to monitor and two codebases to keep consistent. Contract tests and the shared database kept that manageable. The shared database also delayed clean service ownership of tables until after cutover.

#### What I'd do differently

I would build the request-ID logging and New Relic tracing before the first canary, not alongside it. Comparing old and new behaviour per route is much easier when both sides log the same fields.

#### The numbers

| Number | What it measures | How derived | How to say it |
|---|---|---|---|
| 75% | Drop in p95 API latency | (1.2 − 0.3) ÷ 1.2 = 0.9 ÷ 1.2 = 0.75 | "p95 went from 1.2 seconds to 300 milliseconds, a 75% cut." |
| 1,500+ | Enterprise clients on the platform | Client count (HISTORICAL) | "More than fifteen hundred enterprise clients." |
| 700 to 4,000 | Sustained requests per minute | HISTORICAL. About 12 to 67 per second | "From 700 to 4,000 requests a minute, roughly 12 to 67 a second." |
| 2 | Engineers I mentored | Headcount | "I mentored two engineers through it." |

Why it mattered: deadline days are when clients judge us. Faster responses and almost six times the headroom meant fewer timeouts exactly when clients needed us most.

<div class="callout warn">
<b>Don't say:</b> "2,500+ clients". That was an older resume figure and is not on the current PDF. Always say 1,500+. Don't say "I led a team". At Masters India I <b>mentored 2 engineers</b>. "Led 3 engineers" is the Uber FRM story. Keep them separate.
</div>

#### Questions they will ask

**"Why a strangler migration and not a rewrite?"**
Because it was a compliance product and a broken filing day was not an option. With per-route cutover, a mistake only affected one route, for a small canary percentage, and rollback was a config flip. A rewrite puts every route at risk on the same day. For example, our first canary on submit caught a timeout problem while only a small slice of traffic was exposed.

**"What actually drove p95 down? Caching can't do 75%."**
Agreed, caching alone can't. The tail came down because IRP calls stopped pinning workers. We moved them into Kafka consumers and returned 202 where the call could be slow. HikariCP pooling and query fixes, like composite indexes on client and invoice date and removing N+1 list queries, did the rest of the tail. Redis cut repeated reads, which helped the typical request. Async IRP calls and queries moved the tail, cache moved the body.
*Follow-up they may ask:* "How did you measure p95?" From New Relic and gateway latency dashboards per route, compared before and after each cutover.

**"Spring MVC gives each request its own thread. Doesn't a slow call still block a thread?"**
Yes, if the call sits inside the request, which is exactly why we took it out. The controller only validates, stores and publishes to Kafka, so the request thread is busy for milliseconds. The slow IRP call happens on Kafka consumer threads, and their number is fixed, so it caps concurrent IRP calls and can never starve the API. WebClient timeouts stop any single call from hanging forever.

**"Did you do dual writes during the migration?"**
No, on purpose. Old and new code shared one database during the traffic move, so there was always one source of truth. We split service-owned tables only after a route was fully on Spring Boot. Contract tests made sure the new service returned exactly what the old one did.

**"What did mentoring two engineers look like day to day?"**
Each of them owned a service extraction. I set the conventions: controller, service, repository layers, Bean Validation on DTOs at the boundary, shared retry and idempotency helpers. I reviewed their PRs closely early on and paired on the first canary cutover. By the end both were shipping services independently.

**"How do 700 to 4,000 per minute and 1M per day fit together?"**
They measure different things. 700 to 4,000 per minute is API capacity at the gateway, about 12 to 67 requests per second. 1M+ a day is government submissions through the pipeline, about 12 a second on average. One API call can carry many invoices in a bulk upload, so the two numbers don't have to match.

---

### Bullet 2: the bulk e-invoicing pipeline

> "Architected a **high-concurrency** bulk e-invoicing pipeline processing **1M+** daily government submissions by orchestrating a **Kafka** event bus and a **PostgreSQL** database horizontally sharded by tax quarter. Enforced exactly-once, **idempotent** processing for **100K+** concurrent imports with **fault-tolerant state management** via dead-letter queues and bounded retries against volatile state IRP portals."

#### In plain words

I designed the path that takes huge invoice files and registers every invoice with the government. Kafka moves work between stages. Invoices are stored in PostgreSQL tables split by tax quarter. Every unit of work has a unique key, so a retry can never register an invoice twice. Batches that keep failing get parked on the side instead of blocking everyone else. Over a million registrations went through it each day.

#### The numbers first

- **1M+ per day** = 1,000,000 ÷ 86,400 seconds in a day = **about 12 per second on average** (11.6). ESTIMATED arithmetic.
- **Peaks** near filing deadlines were roughly **8 to 10 times** the average. That gives 12 × 8 ≈ 93 up to 12 × 10 ≈ 116, so **around 100 per second at peak**. ESTIMATED. The average is easy. The deadline peak is what you size for.
- **100K+ concurrent imports.** My older prep notes describe this as bulk imports carrying 100K+ invoice rows, processed concurrently. Say it that way: "100K+ invoices in flight across concurrent bulk imports". Don't claim 100,000 separate files were uploaded at the same instant.

#### How it works: chunked bulk imports with Spring Batch

A 12,000-row file should not be processed in one giant transaction, and it should not start from zero if a pod restarts halfway. Spring Batch solves both. A **step** reads rows one by one, runs each through a **processor** (validation), and hands them to a **writer** in **chunks**. Each chunk commits on its own, and Spring Batch records which chunk finished last in its job tables, so a restarted job carries on from there. Think of a clerk who stamps a page number on every finished folder, so whoever takes over the shift knows exactly where to resume.

In our flow, one chunk is one batch. The processor stamps every valid row with the batch key, and the writer publishes the whole chunk as one Kafka message. Illustrative code, with 500 as an example chunk size:

```java
@Bean
Step validateAndPublish(JobRepository jobs, PlatformTransactionManager tx,
                        ItemReader<InvoiceRow> s3RowReader,         // streams rows from the file in S3
                        InvoiceRowValidator validator,              // returns null for a bad row after recording why
                        BatchPublisher publisher) {
    return new StepBuilder("validateAndPublish", jobs)
            .<InvoiceRow, ValidInvoice>chunk(500, tx)
            .reader(s3RowReader)
            .processor(validator)
            .writer(publisher)
            .build();
}

@Component
class BatchPublisher implements ItemWriter<ValidInvoice> {
    private final KafkaTemplate<String, InvoiceBatch> kafka;

    BatchPublisher(KafkaTemplate<String, InvoiceBatch> kafka) { this.kafka = kafka; }

    @Override
    public void write(Chunk<? extends ValidInvoice> chunk) {
        if (chunk.isEmpty()) return;
        ValidInvoice first = chunk.getItems().get(0);              // all rows share the batch key
        InvoiceBatch batch = new InvoiceBatch(first.idempotencyKey(), first.clientId(),
                                              first.gstin(), List.copyOf(chunk.getItems()));
        kafka.send("invoice.accepted", first.gstin(), batch).join(); // wait for the broker ack
    }
}
```

Waiting on `.join()` matters. If the broker does not acknowledge, the chunk fails and is not marked done, so the restart publishes it again. That second publish is harmless because the batch key is the same, which is the idempotency story below.

#### How it works: Kafka as the event bus

Think of Kafka as a set of conveyor belts that never lose a parcel and remember every parcel for a while. Each stage puts its output on a belt. The next stage picks it up at its own pace.

```mermaid
flowchart LR
  B["Bulk service and Spring Batch import job"] -->|"key GSTIN"| T1["topic invoice.accepted"]
  T1 --> G1["group: IRP submit consumers"]
  G1 -->|"bounded concurrency"| IRP["Government IRP"]
  G1 -->|"key GSTIN"| T2["topic irp.completed"]
  G1 -->|"retries exhausted or permanent error"| D1["topic irp.submit.dlq"]
  T2 --> G2["group: persistence to PostgreSQL and MongoDB"]
  T2 --> G3["group: webhook dispatcher"]
  T2 --> G4["group: audit projector and metrics"]
  G3 --> T3["topic client.webhook, key client_id"]
  D1 --> OP["Operator inspects, fixes, replays"]
```

*What to notice:* one `irp.completed` stream feeds three independent consumer groups. Persistence, webhooks and audit each read the full stream at their own pace. The dead-letter topic is a side exit, not a dead end. The topic names are the logical names from my notes.

The four Kafka ideas that matter:

1. **Topics per stage.** `invoice.accepted`, `irp.submit`, `irp.completed`, `client.webhook`, plus `.dlq` versions. Each stage is decoupled. If the webhook dispatcher is slow, registration does not slow down.
2. **Partition key = client GSTIN.** Every message for one taxpayer lands on the same partition, so submit, IRP result and webhook for that taxpayer are processed in order. Different taxpayers spread across partitions and run in parallel. In code this is just the second argument to `kafkaTemplate.send(topic, key, value)`.
3. **Consumer groups.** The IRP submit consumers are one group. Persistence, webhooks and the audit projector are separate groups reading the same results. In Spring Kafka each group is a `@KafkaListener` with its own `groupId`. Adding a new reader (say, a metrics job) does not touch the others.
4. **Replay.** Kafka keeps messages for a retention period. If a consumer had a bug, for example a parser that mis-read one field of the IRP response, we fix the code, move that group's offset back to before the bad window, and reprocess. For GST disputes and audits, being able to re-derive state from the log was valuable.

**Trade-off to name:** keying by GSTIN gives per-taxpayer ordering, but one very large client lands on one partition, which caps parallelism for that client. A refinement my notes mention is keying by GSTIN plus document type. If asked about partition counts, keep it qualitative.

#### Kafka vs RabbitMQ vs SQS

This question comes up often, especially since we were on AWS.

| Need | Kafka | RabbitMQ | AWS SQS |
|---|---|---|---|
| Per-taxpayer ordering | Yes, per partition by key | Possible per queue, harder at scale | Only with FIFO queues, which cap throughput per message group |
| Replay after a bug | Yes, move the offset back | No. Messages are gone once acknowledged | No. Messages are deleted on acknowledgement |
| Many independent readers of one stream | Yes, consumer groups | Needs fanout exchanges and a queue per reader | Needs SNS fan-out to multiple queues |
| Operational cost | Highest. Brokers, partitions, retention to manage | Medium | Lowest. Fully managed |

How I say it: "We needed three things together: per-client ordering, durable replay for compliance, and several independent consumers on the same stream. Kafka gives all three natively. SQS deletes on acknowledgement and FIFO caps throughput per group. RabbitMQ could honestly have handled task dispatch at our scale. We still picked Kafka because replay and multi-reader audit were first-class needs, and Spring Kafka gave us consumer groups, retries and dead-letter publishing with little custom code. The price was more operational work."

#### How it works: PostgreSQL sharded by tax quarter

**Sharding** means splitting one huge table into separate pieces by a rule, so each piece is smaller. Think of an accountant's filing cabinet with one drawer per quarter instead of one giant drawer.

**Why by tax quarter:**

- Our data access was period-scoped. Returns, reconciliation and audits all look at a tax period.
- Almost all **writes land in the current quarter**. Older quarters are mostly **read** for reconciliation and audits.
- So the hot table (current quarter) stays small, its indexes stay small, and inserts stay fast.
- A cold quarter can be archived as one unit without touching the hot write path.

**Routing in the data-access layer.** The API derived the quarter from `invoice_date` at the boundary and the data-access layer picked the matching table. India's financial year starts on 1 April, so April to June is Q1. An illustrative version:

```java
public final class TaxQuarter {
    public static String of(LocalDate d) {
        int fyStart = d.getMonthValue() >= 4 ? d.getYear() : d.getYear() - 1;
        int q = ((d.getMonthValue() - 4 + 12) % 12) / 3 + 1;
        return "fy" + fyStart + "_q" + q;
    }

    public static String invoiceTable(LocalDate d) {
        return "invoice_header_" + of(d);
    }
}
// 14 Oct 2023 -> "invoice_header_fy2023_q3"
// 10 Feb 2024 -> "invoice_header_fy2023_q4"
```

A Hibernate `@Entity` maps to one fixed table name, so a quarter-suffixed table is reached with a native query whose table name comes only from `TaxQuarter`, never from user text. Illustrative:

```java
@Repository
class InvoiceHeaderDao {
    @PersistenceContext private EntityManager em;

    @Transactional
    public int markRegistered(LocalDate invoiceDate, String gstin, String docNo, String irn) {
        String table = TaxQuarter.invoiceTable(invoiceDate);   // derived from a date, so safe to concatenate
        return em.createNativeQuery("UPDATE " + table
                        + " SET irn = :irn, status = 'registered' WHERE gstin = :gstin AND doc_no = :docNo")
                 .setParameter("irn", irn)
                 .setParameter("gstin", gstin)
                 .setParameter("docNo", docNo)
                 .executeUpdate();
    }
}
```

If the quarters live in separate schemas or databases instead of separate tables, Spring's `AbstractRoutingDataSource` does the same job one level down. The service sets the quarter key for the current call, and the routing data source hands Hibernate a connection to that quarter's schema. Either shape is an illustration of "routing in application code". `@Transactional` above means "run this method inside one database transaction, commit at the end, roll back on an exception".

If the client's declared filing period did not match the quarter derived from the invoice date, we rejected the request at the API. A **wrong-quarter write** is the main footgun of this design, so we stopped it at the front door.

**Trade-offs vs native partitioning.** PostgreSQL has built-in declarative partitioning (`PARTITION BY RANGE (invoice_date)`). The database routes rows automatically, prunes partitions in queries, and lets you detach an old partition.

| | Our app-routed quarter shards | Native PostgreSQL partitioning |
|---|---|---|
| Who routes rows | Our code | The database |
| Archive a quarter | Explicit, whole quarter, clear runbook | `DETACH PARTITION`, also clean |
| Cross-quarter queries | Our code must query several tables and combine | The database handles it |
| Risk | Wrong-quarter write if routing has a bug | Fewer moving parts |
| Flexibility | Quarters can be placed and managed separately | All partitions live in one database |
| Fit with Hibernate | Native queries or a routing data source | One `@Entity` on the parent table just works |

We chose app-level routing for explicit control over each quarter and clearer operational runbooks, and paid for it with more code.

<div class="callout note">
<b>Say this carefully.</b> The PDF says "horizontally sharded by tax quarter". My notes describe quarter tables or quarter schemas with routing in application code. If asked "were the quarters on separate servers?", don't claim separate database clusters unless you clearly remember that. Describe the routing and the reasons. The Java snippets in this section are illustrations of the routing idea, not copied production code.
</div>

**What I'd do differently:** today I would start with native declarative partitioning by quarter inside one PostgreSQL cluster, and only move to multi-server sharding if one node could not take the write load. It gives most of the same benefits with less custom routing code, and Hibernate can map the partitioned parent table as one ordinary entity.

#### How it works: idempotency, the "exactly-once" part

Here is the honest version of "exactly-once": Kafka and retries give **at-least-once delivery**, which means a message may arrive twice. We made **processing idempotent**, so a second arrival changes nothing. At-least-once delivery plus idempotent processing gives an exactly-once **effect**. The IRP is outside our database transaction, so true exactly-once delivery across systems is not possible. The idempotency key is what makes it safe.

The key for bulk work is `client + fileHash + batchIndex`:

- `client`: whose work it is.
- `fileHash`: SHA-256 of the uploaded file. If the client uploads the same file twice by mistake, the hash is identical.
- `batchIndex`: which slice of the file.

For single invoices, the client's own invoice reference plays the same role (an `Idempotency-Key` header and a unique constraint on the invoice record).

Illustrative code. The claim is one SQL statement, so it uses Spring's `NamedParameterJdbcTemplate` (a thin helper for running SQL with named parameters) rather than an entity:

```java
static String idempotencyKey(String clientId, byte[] fileBytes, int batchIndex)
        throws NoSuchAlgorithmException {
    byte[] digest = MessageDigest.getInstance("SHA-256").digest(fileBytes);
    return clientId + ":" + HexFormat.of().formatHex(digest) + ":" + batchIndex;
}

private static final String CLAIM_SQL = """
        INSERT INTO irp_job (idempotency_key, client_id, status)
        VALUES (:key, :clientId, 'irp_pending')
        ON CONFLICT (idempotency_key) DO NOTHING
        """;

public String claimOrGetStatus(String key, String clientId) {
    jdbc.update(CLAIM_SQL, Map.of("key", key, "clientId", clientId));
    return jdbc.queryForObject("SELECT status FROM irp_job WHERE idempotency_key = :key",
                               Map.of("key", key), String.class);   // irp_pending or registered
}
```

And the consumer that uses it. `@KafkaListener` tells Spring to call this method for every message the `irp-submit` group receives, and `concurrency` is how many consumer threads run in this instance:

```java
@Component
class IrpSubmitConsumer {
    private final IrpJobStore jobs;
    private final IrpClient irp;
    private final KafkaTemplate<String, Object> kafka;

    IrpSubmitConsumer(IrpJobStore jobs, IrpClient irp, KafkaTemplate<String, Object> kafka) {
        this.jobs = jobs; this.irp = irp; this.kafka = kafka;
    }

    @KafkaListener(topics = "invoice.accepted", groupId = "irp-submit", concurrency = "8")
    public void onBatch(InvoiceBatch batch) {
        if ("registered".equals(jobs.claimOrGetStatus(batch.key(), batch.clientId()))) {
            return;                                              // done before: skip the IRP call
        }
        IrpResult result = irp.register(batch);                  // throws on transient or permanent errors
        jobs.markRegistered(batch.key(), result);
        kafka.send("irp.completed", batch.gstin(), result);
    }
}
```

Worked example: Acme's batch 7 has key `acme:9f2c...e1:7`. The consumer claims it, calls the IRP, records `registered`, and crashes before committing the Kafka offset. Kafka redelivers the message. The new consumer runs the same claim, the `INSERT` hits the unique key and does nothing, the status read says `registered`, and it skips the IRP call. Result: one registration, not two. If Acme uploads the same file again an hour later, the same hash produces the same keys, so nothing is registered twice.

If asked "what if the call timed out and you don't know whether the IRP registered it?": the job stays `irp_pending` and any retry goes through the same key. The IRP also rejects a duplicate document number for the same GSTIN, which is a second safety net. Don't invent more specifics than that.

#### How it works: dead-letter queue and bounded retries

The IRP fails in two ways. **Transient** failures (timeouts, 5xx errors, rate limits) are worth retrying. **Permanent** failures (a malformed invoice, an invalid GSTIN) will fail every time. Retrying those forever just blocks everyone else.

- **Bounded retries:** try a fixed number of times, then stop.
- **Exponential backoff:** wait longer after each failure, so a struggling IRP gets room to recover.
- **Jitter:** add randomness to each wait, so thousands of workers don't all retry at the same second (that would be a "thundering herd").
- **Dead-letter queue:** after the last attempt, or on a permanent error, park the batch in `irp.submit.dlq` with the reason. The rest of the import continues. An operator inspects, fixes and replays it.

First, the IRP client sorts failures into the two kinds. WebClient lets you map HTTP status codes to exceptions. Illustrative, with a made-up path:

```java
public IrpResult register(InvoiceBatch batch) {
    return web.post().uri("/invoices/register")
            .headers(h -> h.setBearerAuth(irpTokens.current()))   // token cached in Redis
            .bodyValue(batch.payload())
            .retrieve()
            .onStatus(s -> s.value() == 429 || s.is5xxServerError(),
                      r -> Mono.error(new TransientIrpException(r.statusCode().value())))
            .onStatus(HttpStatusCode::is4xxClientError,
                      r -> r.bodyToMono(String.class).map(PermanentIrpException::new))
            .bodyToMono(IrpResult.class)
            .timeout(Duration.ofSeconds(10))
            .block();      // fine on a Kafka listener thread
}
```

Then Spring Kafka's error handler does the retrying and dead-lettering. When `onBatch` throws, `DefaultErrorHandler` waits according to the back-off and redelivers the same record. When the attempts run out, `DeadLetterPublishingRecoverer` publishes the record to the DLQ topic, with the exception message in its headers, and the consumer moves to the next record. Permanent errors are marked not-retryable, so they go straight to the DLQ. The attempt counts and delays are examples, not remembered production values:

```java
@Configuration
class KafkaErrorConfig {
    @Bean
    DefaultErrorHandler irpErrorHandler(KafkaTemplate<String, Object> template) {
        var toDlq = new DeadLetterPublishingRecoverer(template,
                (record, ex) -> new TopicPartition("irp.submit.dlq", -1)); // -1 lets Kafka pick the partition
        var backOff = new ExponentialBackOffWithMaxRetries(4);             // 1 try + 4 retries = 5 attempts
        backOff.setInitialInterval(500);
        backOff.setMultiplier(2.0);
        backOff.setMaxInterval(30_000);
        var handler = new DefaultErrorHandler(toDlq, backOff);
        handler.addNotRetryableExceptions(PermanentIrpException.class);   // bad payload: no retries
        return handler;
    }
}
```

`ExponentialBackOffWithMaxRetries` is Spring Kafka's `ExponentialBackOff` with a retry count cap instead of a time cap. Three details worth knowing if an interviewer goes deep:

- The plain exponential back-off has no jitter. Adding it means plugging in a small custom `BackOff` that randomises each wait. The idea is the same as the "full jitter" rule above.
- These retries are **blocking**: the consumer waits on that partition while it retries. The total wait must stay under Kafka's `max.poll.interval.ms`, or the broker thinks the consumer died. For long waits, Spring Kafka also offers non-blocking retry topics (`@RetryableTopic`), which move the record to a delayed retry topic so the partition keeps flowing.
- Blocking per partition is also what keeps per-GSTIN order intact during a retry.

Worked example: the IRP returns a timeout for batch 12. The handler waits about 0.5 s, then 1 s, then 2 s. On the third attempt it succeeds. Batch 15 has an invalid buyer GSTIN, so the IRP returns a 4xx, the client throws `PermanentIrpException`, and the batch goes straight to the DLQ with the reason. Acme's dashboard shows those rows as failed with a message. The other 22 batches finish normally.

**Bounded concurrency** is the other half. The number of in-flight IRP calls per service instance is capped by the listener's `concurrency` (the number of consumer threads). If calls were fanned out further, a fixed-size thread pool or a semaphore would set the cap. When the government portal is already struggling, flooding it makes everything worse.

A **circuit breaker**, which stops calling the IRP for a while when its error rate spikes, is something I can discuss as a design idea. It is not a resume metric, so present it as "here's what I'd add or discuss", not as a measured claim.

#### Background work outside Kafka: Spring Batch, `@Async` and scheduled jobs

Kafka is the conveyor belt between pipeline stages. Not every background job needs a replayable log, so the rest ran inside the Spring Boot services:

- **Spring Batch** for chunked validation of bulk files (schema, GSTIN, duplicates), shown above.
- **`@Async` tasks** on a bounded thread pool for side work: PDF generation of e-invoices, emails and some client notifications.
- **`@Scheduled` jobs** for periodic work such as refreshing masters and cleanup.

Illustrative configuration. `@EnableAsync` and `@EnableScheduling` switch the features on, and the named executor is the thread pool `@Async` methods run on:

```java
@Configuration
@EnableAsync
@EnableScheduling
class BackgroundConfig {
    @Bean("sideTasks")
    ThreadPoolTaskExecutor sideTasks() {
        var pool = new ThreadPoolTaskExecutor();
        pool.setCorePoolSize(4);
        pool.setMaxPoolSize(8);
        pool.setQueueCapacity(500);      // bounded: a full queue rejects work instead of eating memory
        pool.initialize();
        return pool;
    }
}

@Service
class InvoiceSideTasks {
    @Async("sideTasks")
    public void renderPdfAndEmail(String invoiceId) { /* build PDF, send email */ }

    @Scheduled(cron = "0 30 2 * * *")    // 02:30 every night
    public void refreshTaxRateMasters() { /* reload masters, evict cache */ }
}
```

The design rule behind the split: an `@Async` task lives only in memory, so if the pod restarts the task is gone. That is fine for re-sendable side work. Anything that must survive a restart, above all IRP registration, went through Kafka or Spring Batch, which both keep durable progress. One small trap: `@Async` works through a Spring proxy, so calling an `@Async` method from inside the same class runs it synchronously.

If asked exactly which step ran in Spring Batch, which in a Kafka consumer and which as an `@Async` task, keep it at that level: Kafka carried stage events, and consumers, batch jobs and background tasks did the work. Don't invent a finer split.

#### Why this design

Bulk imports are bursty, the IRP is unreliable, and a double registration is unrecoverable. The design answers each of those. Queues absorb bursts (this is called load leveling). Retries with backoff and DLQs handle the unreliable IRP. Idempotency keys make retries safe. Chunked, restartable imports mean a crash never restarts a 12,000-row file from zero. Quarter shards keep the hot write path small.

#### Alternatives and why not

| Alternative | Why not |
|---|---|
| Call the IRP inline from the upload request | A 12,000-row upload would hold a connection for minutes and time out. |
| Fire-and-forget retries without keys | Risk of double registration, which cannot be undone. |
| Infinite retries | A single poison batch blocks a partition forever. |
| One giant invoices table | Hot inserts compete with heavy audit reads, and indexes keep growing. |
| SQS or RabbitMQ only | Covered above. No cheap replay or multi-group reading. |
| Run bulk imports as `@Async` tasks | No durable progress. A restart loses the import and the client has to upload again. |

#### Trade-off

More moving parts: Kafka, consumers, batch jobs, a DLQ to monitor, and app-level shard routing. In return we got deadline-day survival and safe retries.

#### Questions they will ask

**"Why Kafka and not SQS, since you were on AWS?"**
We needed per-client ordering, durable replay for compliance, and several independent consumer groups on one stream. We keyed by GSTIN so everything for one taxpayer stayed in order. SQS deletes messages on acknowledgement, so there's no cheap replay, and FIFO queues cap throughput per message group. RabbitMQ could have dispatched tasks at our scale, honestly. Replay and multi-reader audit are what tipped it to Kafka.

**"How do you guarantee exactly-once?"**
Strictly, we didn't get exactly-once delivery. The IRP sits outside our transaction. We had at-least-once delivery plus idempotent processing, which gives an exactly-once effect. Every batch carries the key client plus fileHash plus batchIndex, and a unique constraint means a redelivered message finds the key and skips the IRP call. For example, if a consumer crashed after registering but before committing its offset, the redelivery is a no-op.
*Follow-up they may ask:* "What about Kafka transactions?" They give exactly-once between Kafka topics, but the IRP is an external HTTP call, so they can't cover it. The key in PostgreSQL is what protects the government side.

**"How do retries and the DLQ work in your consumer?"**
The listener just throws. Spring Kafka's `DefaultErrorHandler` retries the record with an exponential back-off and a fixed attempt limit. When attempts run out, a `DeadLetterPublishingRecoverer` publishes it to the DLQ topic with the error in its headers, and the consumer moves on. Permanent errors such as an invalid GSTIN are marked not-retryable, so they skip the retries and go straight to the DLQ.

**"Derive TPS from 1M a day. Do your numbers hang together?"**
1,000,000 divided by 86,400 seconds is about 11.6, so roughly 12 per second on average. Filing-deadline peaks were roughly 8 to 10 times that, so around 100 per second, which is my estimate. API throughput of 700 to 4,000 requests per minute is about 12 to 67 per second, and that measures a different thing: gateway requests, where one bulk request carries many invoices.

**"Why shard by quarter and not hash by client?"**
Our access pattern was time-scoped. Almost all writes go to the current quarter, and older quarters are read for reconciliation and audit. Quarter shards keep the hot table and its indexes small and let us archive a whole quarter cleanly. Hash by client would spread the current quarter's writes everywhere but make archiving old periods messy. The cost was routing in our own data-access layer, so we derived the quarter from the invoice date at the API and rejected mismatches.

**"What goes into the DLQ and what happens next?"**
Batches that hit a permanent error, like an invalid GSTIN, or that ran out of retries on transient errors. They're parked with the failure reason so the rest of the import continues. An operator looks at them, fixes the cause, and replays them through the same idempotency keys, so a replay can never double-register.

---

### Bullet 3: observability, caching and release quality

> "Decreased incident triage time by **70%** and lowered database read load by **30%** by instrumenting **ELK** and **New Relic** distributed tracing alongside a Redis caching layer. Hardened the CI/CD release cycle by driving test coverage from **35% to 82%**, achieving a **98%** deployment success rate across the microservices ecosystem."

#### In plain words

When something broke, we could find out why much faster, because every request carried one ID through every service and log. A cache in front of the database took away almost a third of its reads. More automated tests meant releases rarely failed.

#### How it works: ELK, New Relic and the request ID

- **ELK.** Every service wrote **structured JSON logs**, one JSON object per line with fields like `request_id`, `client_id`, `route`, `status` and `duration_ms`. Logstash shipped them to Elasticsearch, and we searched them in Kibana.
- **New Relic (APM).** Its Java agent traced each request through the service and showed where time went: database, external IRP call or our own code. We set alerts on error rate and latency.
- **Request ID.** The gateway or first service stamped a unique `X-Request-ID`. It went into every log line, every outgoing HTTP header, every Kafka message header and every background task. One search in Kibana for that ID showed the whole story across API, Kafka consumer and IRP call.

Illustrative servlet filter. `OncePerRequestFilter` is a Spring base class that runs exactly once per HTTP request, before the controller. It puts the ID in the MDC, so the JSON log encoder adds `request_id` to every line logged on that thread:

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
class RequestIdFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {
        String rid = Optional.ofNullable(req.getHeader("X-Request-ID"))
                             .orElseGet(() -> UUID.randomUUID().toString());
        MDC.put("request_id", rid);                 // every log line on this thread gets the field
        res.setHeader("X-Request-ID", rid);
        try {
            chain.doFilter(req, res);
        } finally {
            MDC.remove("request_id");               // threads are reused, so always clean up
        }
    }
}

// when publishing to Kafka, carry it along in a header
var record = new ProducerRecord<String, Object>("irp.submit", gstin, payload);
record.headers().add("request_id", MDC.get("request_id").getBytes(StandardCharsets.UTF_8));
kafkaTemplate.send(record);
```

On the consumer side, the listener reads the `request_id` header and puts it back into the MDC before doing any work. MDC is per thread, so `@Async` tasks need the same hand-off. A Spring `TaskDecorator` on the thread pool copies the MDC from the caller's thread into the worker thread.

Worked example: Acme says "invoice INV-2023-10-0457 never got an IRN". Before, someone had to SSH into several boxes and grep logs by guesswork. After, support finds the request ID from Acme's API response, searches Kibana, and in a minute sees: accepted at 10:02, submit consumer called the IRP at 10:03, IRP returned a timeout on every attempt, batch parked in the DLQ with the retries-exhausted reason. The fix is obvious: replay that batch.

#### The triage number

- **What it measures:** time from an incident being noticed to knowing the cause.
- **How derived:** the 70% cut is HISTORICAL. The baseline of **about 30 minutes to under 10 minutes** is ESTIMATED. 30 minutes down to 9 minutes is a 70% cut.
- **How to say it:** "Triage went from roughly half an hour to under ten minutes, about 70% faster, because one request ID joined everything."

<div class="callout warn">
<b>Say this carefully.</b> Claim on-call <b>alerting</b> and faster triage. Don't invent a formal pager rotation, an incident commander title or SLO numbers you can't back up. "Support tickets −35%" appeared on an older resume and is <b>not on the current PDF</b>. Don't use it.
</div>

#### How it works: Redis cache-aside

**Which keys:**

| Key | What it holds | Freshness rule |
|---|---|---|
| `client:config:{client_id}` | Client settings and feature flags | Deleted on every config write |
| `gstin:master:{gstin}` | GSTIN master lookup | Deleted on write |
| tax-rate masters | Rates by product category | TTL only, with jitter (they rarely change) |
| `irp:token:{env}` | IRP auth token | TTL set below the token's real lifetime, with a safety margin |

**Why 30% fewer reads is plausible:** in a 100K-row import, every row needs the same client config and many repeated GSTIN lookups. Without a cache that is the same handful of rows read from the database tens of thousands of times. With a cache, it is a few reads per TTL. The 30% is across total database read load, not per endpoint. In simple terms: for the same traffic, if the database used to serve 100 reads, it now serves about 70.

**TTL jitter:** if 10,000 keys were all cached at 9:00 with a 10-minute TTL, they would all expire at 9:10 and hit the database together. Adding a random 0 to 2 minutes spreads the expiries out.

**Stampede lock:** when a hot key expires, only one instance gets a short Redis lock and reloads from the database. In Redis terms that is `SET key value NX EX 5`, meaning "set only if it doesn't exist, expire in 5 seconds". In Spring Data Redis it is `setIfAbsent(key, value, Duration.ofSeconds(5))`. The others wait briefly and re-read the cache, or serve a slightly stale value.

Illustrative code with Spring Data Redis. `StringRedisTemplate` is Spring's ready-made Redis client for string keys and values. The TTL numbers are examples:

```java
@Service
class ClientConfigCache {
    private final StringRedisTemplate redis;
    private final ClientConfigRepository db;
    private final ObjectMapper json;

    ClientConfigCache(StringRedisTemplate redis, ClientConfigRepository db, ObjectMapper json) {
        this.redis = redis; this.db = db; this.json = json;
    }

    public ClientConfig get(String clientId) throws JsonProcessingException {
        String key = "client:config:" + clientId;
        String cached = redis.opsForValue().get(key);
        if (cached != null) return json.readValue(cached, ClientConfig.class);

        String lock = "lock:" + key;
        if (Boolean.TRUE.equals(redis.opsForValue().setIfAbsent(lock, "1", Duration.ofSeconds(5)))) {
            try {                                                         // only one rebuilder
                ClientConfig cfg = db.load(clientId);
                long ttl = 600 + ThreadLocalRandom.current().nextInt(121); // TTL jitter
                redis.opsForValue().set(key, json.writeValueAsString(cfg), Duration.ofSeconds(ttl));
                return cfg;
            } finally {
                redis.delete(lock);
            }
        }
        LockSupport.parkNanos(Duration.ofMillis(50).toNanos());           // others wait briefly
        cached = redis.opsForValue().get(key);
        return cached != null ? json.readValue(cached, ClientConfig.class) : db.load(clientId);
    }

    public void update(String clientId, ClientConfig cfg) {
        db.save(clientId, cfg);
        redis.delete("client:config:" + clientId);                       // invalidate on write
    }
}
```

For the slow-changing tax-rate masters, Spring's cache annotations are simpler. `@Cacheable` means "look in the cache first, and only run this method on a miss". Backed by a Redis cache manager with a TTL, it is cache-aside in one line:

```java
@Cacheable(cacheNames = "taxRates", key = "#category")
public TaxRate rateFor(String category) {
    return taxRateRepo.findByCategory(category);
}
```

Why not use `@Cacheable` for the hot config keys too? Its `sync = true` option only locks inside one JVM, so ten service instances could still all miss at once and hit the database. The explicit `setIfAbsent` lock in Redis works across every instance.

**Why cache-aside and not write-through everywhere:** most of our data was read far more than it was written, and only a few keys were hot. Cache-aside caches only what is actually read. Write-through would push every write into Redis, including data nobody reads again.

#### How it works: coverage and deploy success

- **Coverage from 35% to 82%.** We wrote JUnit 5 tests with Mockito, money paths first: registration, reconciliation and imports. That included the contract tests that pinned old PHP responses during migration. JaCoCo measured coverage in the Maven build, and its `check` goal was the CI gate, so a PR that dropped coverage could not merge. This is a rise of **47 percentage points**. Don't call it "a 134% increase", which is technically true but sounds like spin.
- **98% deployment success.** About 98 out of 100 production deploys went out without failing or needing a rollback (HISTORICAL). Higher coverage plus canary releases per route is what got us there.

What a money-path test looks like (illustrative). Mockito replaces the job store and the IRP client with fakes, so the test runs in milliseconds and proves the most important rule: a redelivered batch never calls the IRP again.

```java
@ExtendWith(MockitoExtension.class)
class IrpSubmitConsumerTest {
    @Mock IrpJobStore jobs;
    @Mock IrpClient irp;
    @Mock KafkaTemplate<String, Object> kafka;
    @InjectMocks IrpSubmitConsumer consumer;

    @Test
    void redeliveredBatchDoesNotCallIrpAgain() {
        when(jobs.claimOrGetStatus("acme:9f2c:7", "acme")).thenReturn("registered");

        consumer.onBatch(new InvoiceBatch("acme:9f2c:7", "acme", "29ABCDE1234F1Z5", List.of()));

        verifyNoInteractions(irp);
    }
}
```

#### Why this design

Faster triage needed correlation more than more logs. One ID across services, queues and background tasks is what turns "grep and guess" into "search and read". Redis targeted the specific reads that repeat on every row of every bulk import.

#### Alternatives and why not

| Alternative | Why not |
|---|---|
| Plain text logs on each box | No correlation across services. That was the "before" state. |
| Only New Relic, no ELK | APM shows timings well, but we needed full searchable log detail per request, including IRP error bodies. |
| Write-through cache | Caches data nobody reads. Cache-aside fits read-heavy, few-hot-keys data. |
| No invalidation, TTL only, for config | An admin changes a client's credentials and we keep using the old ones until expiry. Not acceptable for config. |

#### Trade-off

Caching adds staleness risk and invalidation code. We limited it by deleting config keys on write and using TTL-only only for slowly changing masters. Structured logging adds volume and ELK storage cost.

#### Questions they will ask

**"Is the 70% triage number real or vanity?"**
The 70% is from my work records, and the baseline of about 30 minutes to under 10 is my estimate of a typical incident. The mechanism is what makes it believable. Before, we SSH'd into boxes and grepped with no way to connect a request across services. After, one request ID went through the API, Kafka consumers and IRP calls, and New Relic showed where the time went. Finding the cause became one search.

**"How did the request ID follow a request across threads and Kafka?"**
A servlet filter stamped it and put it in the MDC, so every log line on the request thread carried it. When we published to Kafka we copied it into a message header, and the consumer put it back into its own MDC. For `@Async` work, a task decorator copied the MDC into the worker thread. So one ID showed up in API logs, consumer logs and background task logs alike.

**"Cache-aside: what about stampedes and stale data?"**
TTL jitter so keys don't expire together, and a Redis `setIfAbsent` lock so only one instance rebuilds a hot key while the others wait briefly or serve slightly stale data. Config and GSTIN keys were deleted inside the update path, so admins never got stale credentials. Slow-changing masters were TTL-only.

**"What does 98% deploy success mean?"**
About 98 of every 100 production deploys went out without failing or being rolled back. It came from the coverage gate in CI plus per-route canaries, which caught problems while only a small slice of traffic was exposed.

---

## 8. Tech used in this project and why

The resume's tech line for this role:

| Tech | What it is in one line | Why here | Alternative considered |
|---|---|---|---|
| Java | Statically typed language on the JVM with a large backend ecosystem | Strong typing for tax rules and money fields. Mature libraries for Kafka, batch jobs and databases | PHP (the legacy) |
| Spring Boot | Java framework for production-ready web services with sensible defaults | One stack for REST APIs, Kafka consumers, batch imports, validation and pooling | Django (admin and ORM focus), keeping PHP |
| Hibernate | The JPA implementation that maps Java entities to tables | Entity mapping and repositories for invoices and statuses. Native queries for quarter tables | Hand-written JDBC everywhere |
| Kafka | Durable, ordered, replayable message log | Per-GSTIN ordering, replay for audits, multiple consumer groups | RabbitMQ, SQS |
| PostgreSQL | Relational database with strong transactions | System of record for invoices and statuses. Sharded by tax quarter | One big table, native partitioning |
| MongoDB | Document database for flexible JSON | Signed IRP responses and payload snapshots vary in shape and are kept for audits | Forcing everything into PostgreSQL JSON columns |
| Redis | In-memory key-value store | Cache-aside for config, GSTIN masters, IRP tokens. Stampede locks | Hitting the database on every bulk row |
| Elasticsearch | Search engine over JSON documents | The "E" in ELK for logs. Also invoice search | Plain log files |
| Docker | Packages a service with its dependencies into a container | Same image from laptop to production for every microservice | Hand-configured servers |
| ELK | Elasticsearch, Logstash and Kibana for central logging | Searchable structured logs with request ID | SSH and grep |
| New Relic | APM and distributed tracing | Per-request timing breakdown and alerts | Logs only |
| AWS | Cloud provider | Company standard. Amazon S3 for uploaded bulk files | Not a choice I made |

Parts of the Spring ecosystem used inside these services (not separate items on the tech line):

| Piece | What it did here |
|---|---|
| Spring MVC (`@RestController`) and Bean Validation | Routes and strict request checks at the boundary |
| Spring Kafka | `KafkaTemplate` producers, `@KafkaListener` consumers, `DefaultErrorHandler` with back-off, dead-letter publishing |
| Spring Batch | Chunked, restartable validation of bulk files |
| `@Async` and `@Scheduled` | Side tasks (PDFs, emails) and nightly jobs |
| WebClient | IRP calls with timeouts and status-to-exception mapping |
| HikariCP | Database connection pool, Spring Boot's default |
| Spring Data Redis | `StringRedisTemplate` and `@Cacheable` for the cache layer |
| JUnit 5, Mockito, JaCoCo, Maven | Tests, fakes, coverage measurement and the CI coverage gate |

Where MongoDB and Elasticsearch fit, in one line: "PostgreSQL for transactional correctness, MongoDB for the variable-shaped signed responses, Elasticsearch for logs and search."

---

## 9. Hard problems and failure stories

### Story 1: the canary timeout mismatch

- **What broke:** on an early canary of the submit route, some requests that worked on PHP failed on the Spring Boot service.
- **How we found it:** the canary error-rate dashboard went up for the new service only, while only a small slice of traffic was on it.
- **Root cause:** PHP had a 60-second timeout. We had set 10 seconds on the new service. Some IRP calls legitimately took longer than 10 seconds, especially on busy days.
- **Fix:** instead of just raising the timeout, we moved the IRP call fully off the request path. The API returned `202 Accepted` with an invoice ID, and the client polled or got a webhook.
- **What I learned:** the old system's quirks are part of its contract, so contract tests should cover timeouts and slow paths, not just payloads. And canaries earn their keep. A small slice found this before every client did.

### Story 2: N+1 queries hiding in the monolith

- **What we found:** while rewriting list endpoints, several fetched a page of invoices and then queried lines or status per invoice.
- **Fix:** batch fetching in Hibernate (one extra query for all lines on the page), composite indexes on `(client_id, invoice_date)`, and pagination.
- **What I learned:** a rewrite is a good moment to profile every query. A lot of the p95 gain came from fixes like this, not from the new framework. It also taught the team to switch on Hibernate's SQL logging in tests, because lazy loading hides N+1 queries very well.

### Story 3: the same lookup on every row of a bulk import

- **What we saw:** a 100K-row import read the same client config and many of the same GSTIN masters over and over.
- **Fix:** Redis cache-aside with TTL jitter, a `setIfAbsent` stampede lock, and invalidation on write.
- **Result:** database read load down 30% (HISTORICAL).

### Design risks I planned around (not incident stories)

- **Wrong-quarter writes.** If routing derived the wrong quarter, an invoice would land in the wrong shard. We derived the quarter at the API from `invoice_date` and rejected mismatches.
- **Poison batches.** One bad batch must not block a partition. Bounded retries plus DLQ.
- **Unknown IRP outcome after a timeout.** Retry through the same idempotency key, and the IRP's own duplicate check is a backstop.

Present these as design decisions, not as dated incidents.

---

## 10. Say this / don't say this

<div class="callout warn">
<b>Say this</b>
<ul>
<li>"1,500+ enterprise clients."</li>
<li>"PHP monolith to Spring Boot microservices."</li>
<li>"p95 from 1.2 seconds to 300 milliseconds, a 75% cut."</li>
<li>"700 to 4,000 requests per minute, roughly 12 to 67 per second."</li>
<li>"1M+ government submissions a day, about 12 per second on average. Peaks around 8 to 10 times that, which is my estimate."</li>
<li>"At-least-once delivery plus idempotent processing, so the effect is exactly once."</li>
<li>"I mentored two engineers."</li>
<li>"Triage about 70% faster, roughly 30 minutes down to under 10. The baseline is my estimate."</li>
<li>"The migration was gradual, route by route, behind the gateway. People call it the strangler pattern."</li>
</ul>
<b>Don't say this</b>
<ul>
<li>"2,500+ clients" (older resume, not on the current PDF).</li>
<li>"Support tickets down 35%" (older resume, not on the current PDF).</li>
<li>"Zero message loss" or "true exactly-once delivery to the government".</li>
<li>"I led a team" at Masters India. Mentored 2 is Masters. Led 3 is Uber FRM.</li>
<li>Flink at Masters India. Flink belongs to the Uber Menu pipeline, which is a different Kafka system.</li>
<li>"Payments" or "money movement". This is tax compliance and invoice registration.</li>
<li>A circuit breaker as a measured result. It is a design idea to discuss.</li>
<li>TPS or RPS as if they are on the PDF. They are arithmetic I can show.</li>
<li>"100,000 separate files uploaded at once." Say "100K+ invoices in flight across concurrent bulk imports".</li>
<li>Exact partition counts, chunk sizes, retry counts, pool sizes, thread counts or TTLs as remembered facts. The ones in this chapter are illustrative.</li>
<li>The Java snippets as copied production code. They show how the mechanism works.</li>
</ul>
</div>

---

## 11. Practice drill

1. **What does Masters India do?**
It's a GST compliance and e-invoicing SaaS for Indian enterprises. Clients send us invoices, we validate them and register them with the government's Invoice Registration Portal, which returns an IRN and a signed QR code. We return those to the client by API or webhook.

2. **What is an IRN and why does it matter?**
The IRN is the unique reference number the government portal assigns when it registers an invoice. Together with the signed QR, it makes a B2B invoice legally valid. Without it the buyer can't safely claim tax credit.

3. **Why is a double registration so bad?**
Once registered, the invoice is a legal record. Cancellation is narrow and time-limited, and after that you need manual corrections through returns. Two registrations for one sale create a compliance mismatch for the client, so every retry had to be idempotent.

4. **Explain p95 with an example.**
Take 100 requests and sort them by time. The 95th one is the p95. If it's 300 milliseconds, 95% of requests finished in 300 milliseconds or less. Ours went from 1.2 seconds to 300 milliseconds.

5. **Where did the latency win come from?**
Mostly from taking slow IRP calls off the request path into Kafka consumers, plus HikariCP connection pooling and query fixes like composite indexes and removing N+1 queries. Redis cut repeated reads, which helped the typical request more than the slow tail.

6. **How did the canary rollout work?**
Nginx sent a small percentage of one route's traffic to the new Spring Boot service. We watched error rate and latency, then ramped up or rolled back. Rollback was a config change and reload, not a redeploy.

7. **Why not dual writes during the migration?**
Two sources of truth in a tax product cause reconciliation nightmares. We kept one shared database during the traffic move and split tables only after a route was fully migrated.

8. **Why is the partition key the GSTIN?**
So every message for one taxpayer lands on the same partition and is processed in order: submit, result, webhook. Different taxpayers still run in parallel. The risk is one giant client creating a hot partition.

9. **Kafka vs SQS, one sentence each.**
Kafka keeps an ordered, replayable log that many consumer groups can read independently. SQS is a simpler managed queue that deletes messages on acknowledgement, so there's no cheap replay, and its FIFO mode caps throughput per group.

10. **What is your idempotency key?**
Client plus fileHash plus batchIndex for bulk work, and the client's invoice reference for single invoices. A unique constraint means a redelivered message finds the existing key and skips the IRP call.

11. **Why backoff with jitter, and how is it wired in Spring?**
Backoff gives a struggling portal room to recover. Jitter spreads retries out so thousands of workers don't retry at the same second and knock it over again. In Spring Kafka it's a `DefaultErrorHandler` with an exponential back-off and an attempt limit, plus a `DeadLetterPublishingRecoverer` for the DLQ.

12. **What is a DLQ and why use one?**
A side queue for messages that keep failing. It stops one poison batch from blocking the rest of the import. An operator can inspect it, fix the cause and replay it safely through the same idempotency keys.

13. **Why shard by quarter?**
Writes go almost entirely to the current quarter, while older quarters are read for audits. Quarter shards keep the hot table small and make archiving a whole quarter clean. The cost is routing in the data-access layer.

14. **How did ELK and New Relic cut triage time?**
Every log line, HTTP header, Kafka message and background task carried one request ID, set by a servlet filter and kept in the logging MDC. One Kibana search showed a request's whole path, and New Relic showed where the time went. That took triage from roughly 30 minutes to under 10.

15. **What did the 35% to 82% coverage focus on?**
Money paths first: registration, reconciliation and imports, written as JUnit 5 and Mockito tests, including contract tests that pinned the old PHP responses. JaCoCo enforced coverage as a CI gate, which together with canaries helped us reach 98% deploy success.

---

## 12. 3-minute whiteboard script

**First (about 45 seconds): the business and the constraint.**
Draw three boxes in a row: "Client ERP", "Masters India", "Government IRP". Arrow from client to us, from us to IRP, and back with "IRN + signed QR".
Say: "Indian businesses must register every B2B invoice with the government. We sat in the middle for 1,500+ enterprise clients. The one rule that shaped everything: a double registration can't be undone, so every retry must be idempotent. And load spikes hard before filing deadlines."

**Second (about 60 seconds): the migration.**
Inside "Masters India", draw an "Nginx gateway" box splitting to "PHP monolith" and "Spring Boot services", both pointing to one "Shared DB". Write "10% canary" on one arrow.
Say: "The PHP monolith was synchronous. A slow IRP call pinned a worker. I led a gradual migration to Spring Boot, route by route, with canaries and rollback by config. The win came from moving IRP calls off the request path into async consumers, HikariCP connection pooling and query fixes, with Redis for repeated reads. p95 went from 1.2 seconds to 300 milliseconds, and throughput from 700 to 4,000 requests a minute. I mentored two engineers through it."

**Third (about 60 seconds): the bulk pipeline.**
Draw "S3 file" to "Spring Batch validation" to "Kafka (key = GSTIN)" to "IRP consumers" to "IRP". Branch from consumers to "DLQ". Branch from Kafka to "Postgres by quarter" and "Mongo snapshots" and "webhooks". Write the key `client + fileHash + batchIndex` next to the consumers.
Say: "Bulk files land in S3 and the client gets a 202 right away. A Spring Batch job validates the file in restartable chunks. Kafka carries each stage, keyed by GSTIN for per-taxpayer order, and it lets us replay after a bug. Consumers check the idempotency key before every IRP call, retry with exponential backoff, and park poison batches in a DLQ. Invoices land in PostgreSQL tables split by tax quarter. That's 1M+ submissions a day, about 12 a second on average and around 100 at deadline peaks, which is my estimate."

**Close (about 15 seconds): operations.**
Write "request ID" along the bottom, touching every box.
Say: "One request ID through every service, queue and background task, in ELK and New Relic, cut triage about 70%. Redis cache-aside cut database reads 30%. Coverage went from 35% to 82% with JUnit and a JaCoCo gate, and deploys succeeded 98% of the time."
