# Masters India and GeeksforGeeks Deep Dive (v2 resume defense)

<div class="callout highlight">

**How to use this page**

- **What it covers:** the full depth behind the Masters India bullets (GST e-invoicing, PHP to Spring Boot migration, Kafka bulk pipeline, observability and caching) and the GeeksforGeeks bullets (Django migration, doubt-support APIs, influencer dashboard, scheduled workflows). Every term is defined, every number is derived, and every design choice has alternatives.
- **When to read it:** the week before a backend or system-design loop where interviewers will go deep on migrations, queues, idempotency, sharding or caching. For a quick refresher the morning of an interview, use the shorter pack: [`04_05_masters_gfg.md`](04_05_masters_gfg.md) or [`23c_masters_gfg_interview_packs.md`](../../../prep/23c_masters_gfg_interview_packs.md).
- **What to memorise:** the two one-minute versions, the Masters numbers (from 1.2 seconds to 300 milliseconds p95, 1,500+ clients, 700 to 4,000 requests per minute, 1M+ submissions a day, 100K+ per import, triage down 70%, DB reads down 30%, coverage from 35% to 82%, 98% deploy success), the GFG numbers (10K+ daily queries, 10x spikes, 20% premium lift, 30% course sales, 70% ops efficiency), and the "say this carefully" boxes.

</div>

**What the tags mean.** **HISTORICAL** means the number comes from my past work records and earlier resumes. **ESTIMATED** means arithmetic I can show, so I say "roughly" and give the derivation. **MEASURED** means a log, doc or code exists. **TARGET** means a design goal. Every number here traces to `GROUND_TRUTH.md` in the track's `prep/` folder.

<div class="callout note">

**Current resume bullets**

*Masters India, SDE 2, Noida, Dec 2022 to Jun 2024. GST Compliance and E-Invoicing Platform.*

- **MI1.** Reduced p95 API latency by **75%** (from **1.2s to 300ms**) across **1,500+** enterprise clients by spearheading the migration of a legacy PHP monolith to a **Spring Boot** microservices architecture. Mentored two engineers through the transition, optimizing backend design to drive overall system throughput from **700 to 4,000 requests per minute**.
- **MI2.** Architected a high-concurrency bulk e-invoicing pipeline processing **1M+** daily government submissions by orchestrating a **Kafka** event bus and a **PostgreSQL** database horizontally sharded by tax quarter. Enforced exactly-once, idempotent processing for **100K+** concurrent imports with fault-tolerant state management via dead-letter queues and bounded retries against volatile IRP portals.
- **MI3.** Decreased incident triage time by **70%** and lowered database read load by **30%** by instrumenting **ELK** and **New Relic** distributed tracing alongside a Redis caching layer. Hardened the CI/CD release cycle by driving test coverage from **35% to 82%**, achieving a **98%** deployment success rate across the microservices ecosystem.
- **Tech:** Java, Spring Boot, Hibernate, Kafka, PostgreSQL, MongoDB, Redis, Elasticsearch, Docker, ELK, New Relic, AWS.

*GeeksforGeeks, SDE, Noida, Aug 2021 to Nov 2022. Courses Platform and Influencer Dashboard.*

- **G1.** Stabilized the doubt-support platform to handle **10K+** daily queries and **10x** traffic spikes during live coding contests by migrating the backend to **Django**. Engineered high-throughput REST APIs for voting, pinning, and locking threads using MySQL, MongoDB, Redis, and Elasticsearch, driving a **20%** lift in premium subscriptions.
- **G2.** Accelerated course sales by **30%** by launching an influencer analytics and earnings dashboard to track transactions and affiliate coupon conversions. Increased engineering operational efficiency by **70%** by designing asynchronous scheduled workflows for video processing, user reminders, and data cleanup.
- **Tech:** Python, Django, MySQL, MongoDB, Redis, Elasticsearch.

</div>

<div class="callout warn">

**Older-resume details that are NOT on the current PDF**

- **Support tickets down 35%** (from a client usage dashboard and log downloads), **audit-log churn down 15%**, and **2,500+ clients** come from older resumes. None are on the current PDF. Never say 2,500+ clients. Do not volunteer tickets or audit churn.
- **"Premium up 15 to 20%"** is older wording. The current PDF says **20%**.
- **SMTP email sends 50% faster** (GFG) comes from the 1-year and 2.5-year resumes. Prep depth only.
- **p95 "1000 to 1200ms down to 300 to 400ms"** is the older-resume band. The PDF says from 1.2 seconds to 300 milliseconds.
- **Peak TPS and RPS** are not on the PDF. Verbal only, ESTIMATED.
- The older layout had four Masters bullets. The current PDF has three. Throughput (700 to 4,000 requests per minute) now sits in MI1, and Redis caching now sits in MI3.
- Do not merge "mentored 2" (Masters) with "led 3" (Uber FRM). Do not put Flink at Masters. Masters Kafka is a different product from Uber Menu Kafka.

</div>

---

# Part A. Masters India

## A1. The one-minute version (say this out loud)

"At Masters India I worked on a GST compliance and e-invoicing platform used by more than 1,500 enterprise clients. Businesses send us their invoices, we validate them and register them with the government's Invoice Registration Portal, and we hand back a signed invoice number and QR code.

I spearheaded the migration from a legacy PHP monolith to Spring Boot microservices in Java, using a strangler approach with per-route canaries, and mentored two engineers through it. That took p95 latency from 1.2 seconds to 300 milliseconds and throughput from 700 to 4,000 requests per minute.

I also architected the bulk pipeline: a Kafka event bus with PostgreSQL sharded by tax quarter, processing more than a million government submissions a day, with idempotency keys so 100K-plus-row imports never double-register an invoice, plus dead-letter queues and bounded retries against the flaky government portal. On the ops side, ELK and New Relic tracing cut incident triage by 70%, Redis caching cut database reads by 30%, and test coverage went from 35% to 82% with a 98% deployment success rate."

**Follow-up they may ask:** "What was hardest?" Answer: "Never registering the same invoice twice with the government. That's not recoverable, so idempotency was designed in from the start."

---

## A2. The business in plain English

**What GST e-invoicing is.** In India, businesses selling to other businesses (B2B) above a turnover threshold must register each invoice with a government portal before it is legally valid. The portal is the **IRP (Invoice Registration Portal)**. It checks the invoice and returns an **IRN (Invoice Reference Number)** and a **digitally signed QR code**. Without these, the buyer cannot claim tax credit.

**Who the users are.** Finance and accounts teams at large Indian enterprises. Their ERP systems (the software they run their business on) push invoices to our APIs, one at a time or in big bulk files.

**What they do with us.** Submit invoices, get IRNs and QR codes back, upload bulk files of tens of thousands of invoices, reconcile against their GST returns, and keep an audit trail.

**What hurt before.** The PHP monolith was synchronous. One slow call to the government portal held a server worker hostage for the whole round trip. Deploys were all-or-nothing, and scaling meant scaling everything. On filing-deadline days, traffic spikes caused queue pile-ups and timeouts. In a compliance product, a timeout on deadline day is the worst possible failure.

**Why the company paid for this.** Correctness and traceability matter more than raw speed, but slow or failed submissions lose clients. Faster, reliable, never-double-registered submissions are the product.

---

## A3. Words you need

| Term | Plain meaning | Analogy |
|---|---|---|
| **GST** | Goods and Services Tax, India's indirect tax. | VAT in Europe. |
| **GSTIN** | A business's 15-character GST identification number. | A tax passport number for a company. |
| **IRP** | Invoice Registration Portal, the government system that registers e-invoices. | The passport office that stamps your document as official. |
| **IRN and signed QR** | The unique reference number and digitally signed QR code the IRP returns. This is what makes the invoice valid. | The official stamp and hologram on the passport. |
| **Filing deadline spike** | Traffic jumps as everyone submits before the GST deadline. | Tax-day queues at the post office. |
| **Monolith** | One big application where every feature is deployed together. | One huge kitchen where a broken oven stops every dish. |
| **PHP, Laravel, PHP-FPM** | PHP is the language, Laravel the framework, PHP-FPM the process pool serving requests. Each worker handles one request at a time. | A row of cashiers who each must wait at their till until the card machine answers. |
| **Microservices** | Small services, each owning one domain, deployed independently. | Separate food stalls: one breaks, the others keep serving. |
| **Strangler pattern** | Replace a legacy system piece by piece behind the same front door until the old one can be switched off. | A strangler fig tree that grows around an old tree until it stands on its own. |
| **API gateway (Nginx)** | The front door that routes each request to the old or new service. | A receptionist directing visitors to the old wing or the new wing. |
| **Canary release** | Send a small percentage of traffic to the new version, watch it, then ramp up. | Miners sending a canary in first to check the air. |
| **Contract test** | A test that pins the exact response shape of an API, so a rewrite cannot silently change it. | Tracing paper over the old drawing to check the new one matches line for line. |
| **Java and the JVM** | Java is a statically typed language. The JVM (Java Virtual Machine) runs it and gives real operating-system threads, so one process can do many things at once. | One big kitchen with many cooks working in parallel, instead of one cook per kitchen. |
| **Spring Boot** | A Java framework that bundles an embedded web server (Tomcat), configuration and sensible defaults, so a service starts from one `main` method with almost no setup. | A pre-fitted kitchen module: plug it in and the oven, sink and wiring already work. |
| **Bean and dependency injection** | Spring creates your objects (called beans) at startup and hands each class the objects it needs through its constructor. You never call `new` on a service yourself. | A stage manager who puts the right props in each actor's hands before the scene starts. |
| **Annotation** | A tag in Java code starting with `@`, such as `@RestController`, that tells Spring how to treat a class or method. | A sticky label on a box saying "fragile" or "this side up". |
| **Spring MVC and `@RestController`** | The web layer of Spring. A class marked `@RestController` with methods marked `@PostMapping` or `@GetMapping` becomes an HTTP API. | The front counter where each window serves one type of request. |
| **Thread-per-request** | In Spring MVC each incoming request is served by one thread from the web server's pool (Tomcat's default maximum is 200). If that thread waits on a slow call, it is held for the whole wait. | A fixed number of cashiers. A cashier stuck on the phone serves no one else. |
| **Non-blocking HTTP client (WebClient)** | Spring's WebClient sends an HTTP call and frees the thread while it waits for the answer, with built-in timeouts and retry helpers. | Putting the kettle on and making toast while it boils. |
| **Bounded thread pool** | A fixed-size group of worker threads with a capped queue, so concurrency against a dependency never grows without limit. | A restaurant with ten tables: the eleventh party waits at the door instead of crowding the kitchen. |
| **Bean Validation (`@Valid`, `@NotNull`)** | A Java standard for declaring rules on request objects (DTOs, data transfer objects). Spring checks them before your code runs and returns 400 on failure. | A bouncer checking every ID at the door. |
| **Hibernate and Spring Data JPA** | Hibernate is an ORM (object-relational mapper): Java objects map to database rows. Spring Data JPA sits on top and writes simple queries for you from method names. | A translator between Java and SQL. |
| **Connection pooling (HikariCP)** | Reuse a fixed set of open database connections instead of opening one per request. HikariCP is the default pool in Spring Boot. | A taxi rank of waiting cabs instead of calling a new cab for every trip. |
| **N+1 query** | Fetching a list with one query, then one more query per item. | Going to the shop once for the list, then once per item on it. |
| **Composite index** | A database index on several columns together, such as `(client_id, invoice_date)`. | A phone book sorted by surname, then first name. |
| **p95 latency** | 95% of requests are faster than this. It measures the slow tail users actually feel. | The time by which 95 of 100 buses have arrived. |
| **RPM, RPS, TPS** | Requests per minute, requests per second, transactions per second. Divide RPM by 60 for RPS. | Cars per minute versus cars per second at a toll booth. |
| **Kafka** | A durable, ordered, replayable event log. | A conveyor belt with a recording you can rewind. |
| **Partition key** | The value that decides which Kafka partition a message goes to. Same key, same partition, same order. | Same surname always queues at the same counter. |
| **Consumer group** | A set of workers sharing a topic. Different groups each get their own full copy of the stream. | Several departments each reading the same newspaper at their own pace. |
| **Spring Kafka (`@KafkaListener`, `KafkaTemplate`)** | Spring's Kafka integration. A method marked `@KafkaListener` is called for each message on a topic. `KafkaTemplate` is the object you use to publish messages. | A mail room: the template drops letters in the chute, the listener is the clerk who opens each one. |
| **`DefaultErrorHandler`, `DeadLetterPublishingRecoverer`, `ExponentialBackOff`** | Spring Kafka's retry machinery. The error handler retries a failed message with a growing wait (the backoff), and after the last attempt the recoverer publishes it to a dead-letter topic. | Try the delivery three times, waiting longer each time, then leave the parcel at the depot. |
| **Spring Batch** | A Spring framework for chunked batch jobs: read N items, process them, write them, commit, and record progress in a job repository table, so a restart resumes from the last committed chunk. | Reading a long book and moving the bookmark after every chapter. |
| **`@Async` and `@Scheduled`** | `@Async` runs a method on a background thread pool and returns immediately. `@Scheduled` runs a method on a timer, like cron. | Handing a task to an assistant, versus setting an alarm clock. |
| **PostgreSQL** | An open-source relational database. | A very organised filing cabinet with strict rules. |
| **Sharding** | Splitting data across separate tables, schemas or databases by a key, with the application routing to the right one. | Filing invoices into a separate cabinet for each quarter of the year. |
| **Idempotency key** | A unique key per operation, so repeating it has no extra effect. | A raffle ticket number: you cannot win twice with the same ticket. |
| **Exactly-once processing** | The effect happens once even if the message is delivered more than once. In practice: at-least-once delivery plus idempotent writes. | The courier may ring twice, you sign once. |
| **DLQ (dead-letter queue)** | A side queue where messages that keep failing are parked for later inspection and replay. | A "problem parcels" shelf at the depot. |
| **Bounded retries and exponential backoff with jitter** | Retry a failed call a limited number of times, waiting longer each time, with randomness so clients don't all retry together. | If a line is busy, call back after 1, 2, then 4 minutes, at slightly random times. |
| **Circuit breaker (verbal only)** | Stop calling a failing dependency for a while once errors spike. | A fuse that trips so the whole house doesn't burn. |
| **MongoDB** | A document database storing flexible JSON-like documents. | A folder where each sheet can have a different layout. |
| **Redis** | An in-memory key-value store, very fast, used for caching. | A sticky note on your monitor instead of walking to the filing room. |
| **Cache-aside** | The app checks the cache first. On a miss it reads the database and puts the result in the cache with an expiry. | Check your sticky note first. If it's missing, look it up and write a new note. |
| **TTL and TTL jitter** | Time to live, how long a cached value lasts. Jitter adds randomness so many keys don't expire at the same moment. | Milk with slightly different expiry dates so you don't run out all at once. |
| **Cache stampede (thundering herd)** | Many requests miss the same key at once and all hit the database. | Everyone rushing the fridge the moment the milk runs out. |
| **SETNX and `setIfAbsent`** | Redis "set if not exists", used as a simple lock so only one worker rebuilds a cache entry. In Spring Data Redis the call is `opsForValue().setIfAbsent(key, value, ttl)`. | Grabbing the single talking stick. Whoever has it speaks. |
| **Elasticsearch** | A search engine for fast full-text search and log analytics. | A book's index, for every book at once. |
| **ELK** | Elasticsearch, Logstash and Kibana: collect, store, search and visualise logs. | A CCTV system for your servers, with a search bar. |
| **New Relic APM and distributed tracing** | Application performance monitoring. A trace follows one request across every service it touches. | A parcel tracking number you can follow through every depot. |
| **Request ID (correlation ID)** | A unique ID attached to a request and logged by every service it passes through. | A case number on every form in a file. |
| **Servlet filter and MDC** | A servlet filter is code that runs around every HTTP request before the controller. MDC (Mapped Diagnostic Context) is a per-thread map in the Java logging library; every log line written on that thread automatically includes its fields. | A receptionist who stamps a case number on the visitor's badge, and every office they visit copies it into its notes. |
| **Test coverage** | The share of code lines executed by automated tests. | The share of rooms a safety inspector actually walked into. |
| **JUnit 5, Mockito, JaCoCo** | JUnit 5 runs Java tests. Mockito creates fake versions of dependencies (mocks) so a class can be tested alone. JaCoCo measures coverage and can fail the build below a threshold. | The exam, the stand-in actors for a rehearsal, and the inspector's checklist. |
| **Deployment success rate** | The share of deploys that go out without rollback or failure. | The share of flights that land on schedule. |
| **Amazon S3** | Amazon's object storage for files. | A giant, cheap warehouse for boxes. |

---

## A4. Architecture

```mermaid
flowchart LR
    ERP["Client ERP or dashboard"] --> GW["Nginx gateway: canary percent per route"]
    GW -->|"migrated routes"| API["Spring Boot services: auth, submit, bulk import, recon"]
    GW -.->|"fallback, not yet migrated"| PHP["Legacy PHP monolith"]
    API --> RD["Redis cache: config, GSTIN, tokens"]
    API --> PG["PostgreSQL sharded by tax quarter"]
    API --> S3["Amazon S3: bulk import files"]
    API --> K["Kafka topics: chunks, IRP jobs, responses, webhooks, audit"]
    K --> W["Workers: Kafka consumers and Spring Batch jobs"]
    W -->|"bounded concurrency"| IRP["Government IRP"]
    W --> MG["MongoDB: payload and IRP response snapshots"]
    W --> PG
    W --> DLQ["Dead-letter queue"]
    API --> OBS["ELK logs with request ID, New Relic APM"]
    W --> OBS
```

*What to notice: the gateway lets old and new code serve traffic side by side, and the only path to the government portal goes through workers with bounded concurrency, never straight from a request thread.*

**Box by box.**

1. **Client ERP or dashboard.** Enterprises send single invoices or upload bulk files.
2. **Nginx gateway.** During the migration, each route is either still on PHP or sent, by percentage, to a Spring Boot service. Rollback is a config change, not a deploy.
3. **Spring Boot services.** Separate Java services for auth, e-invoice submit, bulk import and reconciliation. Each one is a Spring MVC app with `@RestController` classes, Bean Validation on the request DTOs, and Hibernate for PostgreSQL access. Request threads validate, record and publish. They never wait on the government portal.
4. **Redis.** Cache-aside for hot reads through Spring Data Redis: client config and feature flags, GSTIN masters, tax rates, IRP auth tokens.
5. **PostgreSQL sharded by tax quarter.** Hot writes land in the current quarter. Older quarters are mostly read for reconciliation and audit. Each service reaches it through a HikariCP connection pool.
6. **Amazon S3.** Bulk import files land here first.
7. **Kafka.** The event bus between stages: accepted import chunks, IRP submit jobs, signed-response persistence, client webhooks, and an audit projector. Partition key is the client GSTIN, so one taxpayer's events stay in order.
8. **Workers.** Spring Kafka `@KafkaListener` consumers call the IRP with bounded concurrency, exponential backoff and idempotency keys. Spring Batch jobs read and chunk bulk import files. Smaller background work (PDF generation, webhooks, email) runs as `@Async` tasks or `@Scheduled` jobs on bounded thread pools.
9. **MongoDB.** Stores flexible invoice payload snapshots and raw IRP responses.
10. **DLQ.** Batches that keep failing park here for operator replay, so the rest of the import continues. Spring Kafka's `DeadLetterPublishingRecoverer` does the parking.
11. **ELK and New Relic.** Structured JSON logs with a request ID, APM traces across API, consumer and worker.

**How Kafka and Spring Batch fit together.** Kafka is the durable event bus between stages, which is what the PDF claims. Spring Batch runs the chunked import step: it reads the uploaded file a chunk at a time, validates each row, and publishes one Kafka event per chunk, recording its progress so a crashed import restarts from the last committed chunk instead of from row one. Kafka consumers then do the IRP calls. If asked, say: "Kafka carried the events between stages. Kafka consumers and Spring Batch jobs did the work."

**Migration rule.** Shared database until 100% of a route's traffic is on Spring Boot. Only then carve out service-owned tables.

---

## A5. One invoice and one bulk import, step by step

### A single invoice (illustrative data)

Client "Acme Steel Pvt Ltd", GSTIN `27AAACA1234F1Z5`, invoice `INV-2024-00871`, dated 14 March 2024 (quarter Jan to Mar 2024).

1. Their ERP posts JSON to `POST /v1/einvoice`, with header `X-Request-ID: 7f3c…`.
2. Gateway routes this path to the Spring Boot e-invoice service (route fully migrated).
3. Spring validates the body with Bean Validation before the controller method runs: GSTIN format, required fields present. A custom validator checks that line amounts add up to the total. A failure returns `400` with the field errors.
4. The service looks up client config and the GSTIN master. Redis hit, so no database read.
5. It computes the idempotency key from the client and the client's invoice reference, and writes an "accepted" row in the Jan to Mar 2024 quarter shard. If the same invoice was already accepted, it returns the existing status instead.
6. It publishes an IRP submit job to Kafka through `KafkaTemplate` with key `27AAACA1234F1Z5`, and returns `202 Accepted` with a status URL (or waits briefly and returns the IRN if the IRP is fast).
7. A `@KafkaListener` consumer picks up the job and calls the IRP through WebClient with a timeout and backoff. The IRP returns IRN and signed QR.
8. The consumer stores the raw response in MongoDB, updates the PostgreSQL row to "registered", and publishes a webhook event.
9. The client gets the IRN and QR by webhook or by polling. Every log line from step 1 to 9 carries the same request ID.

Illustrative controller and request DTO for steps 1 to 6 (teaching sketch, not production code):

```java
@RestController
@RequestMapping("/v1/einvoice")
class EInvoiceController {
    private final EInvoiceService service;

    EInvoiceController(EInvoiceService service) {   // Spring injects the service bean
        this.service = service;
    }

    @PostMapping
    ResponseEntity<SubmitStatus> submit(@Valid @RequestBody EInvoiceRequest req) {
        SubmitStatus status = service.accept(req);  // idempotent accept, then publish to Kafka
        return ResponseEntity.accepted().body(status);
    }
}

record EInvoiceRequest(
        @NotBlank @Pattern(regexp = "[0-9]{2}[A-Z0-9]{13}") String sellerGstin,
        @NotBlank String invoiceNo,
        @NotNull LocalDate invoiceDate,
        @NotEmpty List<@Valid LineItem> items) {}
```

*What to notice: `@Valid` makes Spring reject a bad body before `submit` runs, and the method returns 202 without ever calling the government portal.*

### A bulk import

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Spring Boot bulk service
    participant S as Amazon S3
    participant K as Kafka
    participant W as Kafka consumer
    participant I as IRP
    participant P as PostgreSQL quarter shard
    C->>A: upload 100,000-invoice file
    A->>S: store file, compute fileHash
    A->>K: Spring Batch step publishes chunk events, key = client GSTIN
    K->>W: chunk batchIndex 37
    W->>P: check idempotency key client + fileHash + 37
    W->>I: submit with bounded concurrency
    I-->>W: IRNs and signed QRs
    W->>P: mark registered
    W-->>C: progress update on dashboard
    Note over W,K: after max retries, the batch goes to the DLQ
```

*What to notice: the idempotency check happens before the IRP call, so a retried batch never registers twice.*

**Worked example.** A client uploads a 100,000-row file. We store it in S3 and compute `fileHash = sha256(file)`. A Spring Batch step reads it in chunks (say 1,000 rows each, purely illustrative), giving batch indexes 0 to 99. Each batch's key is `client_id + fileHash + batchIndex`. If the worker handling batch 37 crashes after submitting but before acknowledging, Kafka redelivers batch 37. The worker sees key `acme + 9b1e… + 37` already marked done and skips the IRP call. If batch 37 keeps failing because of a malformed row, it goes to the DLQ after the retry budget, and batches 38 to 99 carry on. An operator fixes and replays batch 37 later.

---

## A6. Bullet MI1 decoded: PHP to Spring Boot, latency, throughput, mentoring

> Reduced p95 API latency by 75% (from 1.2s to 300ms) across 1,500+ enterprise clients by spearheading the migration of a legacy PHP monolith to a Spring Boot microservices architecture. Mentored two engineers through the transition, optimizing backend design to drive overall system throughput from 700 to 4,000 requests per minute.

### In plain words

I led moving the product off an old PHP application onto Java services built with Spring Boot, one route at a time, without breaking anything for clients. The slowest 5% of requests got four times faster, the system handled almost six times more traffic, and I coached two engineers to ship services on their own.

### How it works: the migration playbook

1. **Strangler, not big bang.** New Spring Boot services went behind the existing gateway one domain at a time: auth, e-invoice submit, bulk import, reconciliation. The monolith kept serving everything not yet migrated.
2. **Route-level canary with fallback.** Nginx sent a small percentage of traffic per endpoint to the new service. We watched error rate and latency dashboards, then ramped to 100%. Rollback was a config change.
3. **Shared database first, then split.** New services read the same MySQL or PostgreSQL data as the monolith during the traffic cutover, to avoid a risky data migration at the same time. Only after traffic fully moved did we carve out service-owned tables.
4. **Contract tests pinned old PHP responses.** We recorded monolith responses for the top endpoints and asserted the Spring Boot replacements matched field for field, so clients never saw a payload change.
5. **Request threads never wait on third parties.** IRP calls went to Kafka consumers. PDF generation, webhooks and email went to `@Async` tasks and scheduled jobs on bounded thread pools. All of them used retries and idempotency keys.

A contract test in Spring is a MockMvc test. MockMvc calls the controller in-process, without a real network, and compares the JSON to the recorded PHP response (illustrative):

```java
@WebMvcTest(EInvoiceController.class)
class EInvoiceContractTest {
    @Autowired MockMvc mvc;
    @MockBean EInvoiceService service;

    @Test
    void statusResponseMatchesRecordedPhpPayload() throws Exception {
        when(service.status("INV-2024-00871")).thenReturn(Fixtures.registeredStatus());
        mvc.perform(get("/v1/einvoice/{ref}/status", "INV-2024-00871"))
           .andExpect(status().isOk())
           .andExpect(content().json(Fixtures.read("php/status_00871.json"), true)); // strict match
    }
}
```

*What to notice: `true` means strict comparison, so a missing or extra field fails the build before a client ever sees it.*

Illustrative Nginx canary split (teaching sketch, not the production config):

```nginx
split_clients "${request_id}" $einvoice_backend {
    10%   spring_einvoice;
    *     php_monolith;
}
location /v1/einvoice {
    proxy_pass http://$einvoice_backend;
}
```

Ramp from 10% to 50% to 100% by editing one number. Roll back by setting it to 0%.

### How it works: where the latency win came from

- **IRP calls taken off the request thread.** A PHP-FPM worker used to sit blocked for the whole IRP round trip. In Spring MVC a waiting request thread is just as stuck (thread-per-request), so the request path validates, records, publishes to Kafka and returns 202. Kafka consumers make the IRP call through WebClient with a timeout, and the listener's concurrency setting bounds how many calls are in flight.
- **Connection pooling with HikariCP** per service, instead of PHP-FPM's per-request connections, which caused connect storms under load.
- **Query fixes found during the rewrite:** composite indexes on `(client_id, invoice_date)`, N+1 removal in Hibernate, and pagination on list endpoints.
- **Redis caching of hot reads** (client config, tax rates, auth context). This mostly helped the median and read-heavy endpoints.

The honest split: **taking IRP calls off request threads, pooling and query fixes moved the p95 tail. Redis moved the body of the distribution.**

**The N+1 problem in Hibernate.** By default a `@ManyToOne` relation can be loaded lazily, which means Hibernate fires a separate SELECT the first time you touch it. Loop over 50 invoices and read each buyer, and you get 51 queries. The fix is to tell Spring Data JPA to fetch the buyer in the same query with an entity graph (illustrative):

```java
// Before: 1 query for invoices + 1 lazy SELECT per invoice for its buyer
List<Invoice> invoices = invoiceRepo.findByClientId(clientId);
invoices.forEach(inv -> inv.getBuyer().getName());

// After: one query with a join, using the (client_id, invoice_date) index, paginated
interface InvoiceRepository extends JpaRepository<Invoice, Long> {
    @EntityGraph(attributePaths = "buyer")
    Page<Invoice> findByClientIdOrderByInvoiceDateDesc(Long clientId, Pageable page);
}
Page<Invoice> page = invoiceRepo.findByClientIdOrderByInvoiceDateDesc(
        clientId, PageRequest.of(pageNo, 50));
```

*What to notice: Spring Data JPA writes the query from the method name, and `@EntityGraph` turns 51 round trips into one.*

**Connection pool sizing.** HikariCP is configured in `application.yml`. The numbers below are a teaching sketch, not the production values:

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20     # connections this instance may hold
      connection-timeout: 2000  # ms to wait for a free connection before failing fast
```

A small, fixed pool per instance protects PostgreSQL from connect storms. Failing fast when the pool is exhausted is better than letting requests queue until they time out.

### How it works: mentoring two engineers

Two junior engineers each owned individual service extractions. I set the conventions: controller, service and repository layering, Bean Validation on request DTOs at the boundary, shared retry and idempotency helpers. I reviewed every PR closely for the first months and paired with them on the first canary cutover (Nginx percentage route, watch errors and latency, ramp or roll back by config). By the end both were shipping services independently. The headcount of two is user-confirmed.

### Why this design

- **Why strangler over rewrite?** It is a compliance product with zero tolerance for a broken filing day. Strangler let us cut over per endpoint with instant rollback.
- **Why Spring Boot?** Four honest reasons. First, static typing for money and tax payloads: invoice DTOs are checked at compile time, and amounts use `BigDecimal` instead of floating point. Second, real threads on the JVM: bounded thread pools and a non-blocking WebClient let one instance keep many IRP calls in flight, where PHP-FPM needed one heavyweight process per waiting request. Third, the ecosystem for this exact pipeline lives in one place: Spring Kafka for listeners, retries and dead-letter publishing, Spring Batch for restartable chunked imports, Hibernate for PostgreSQL, Spring Data Redis for the cache, and Bean Validation at the boundary. Fourth, operability: the New Relic Java agent instruments Spring apps without code changes, and Spring Boot exposes health endpoints for the load balancer.
- **Why shared DB during cutover?** One source of truth. Dual writes create reconciliation nightmares.

### Alternatives and why not

| Alternative | Why not |
|---|---|
| Big-bang rewrite | One bad cutover on a filing day is unacceptable. No gradual rollback. |
| Keep PHP and scale horizontally | Each worker still blocks on IRP. You just buy more hostages. |
| A Python framework (Django or Flask) | Fast to build with, but a sync request model has the same blocking problem against a slow government API, and there is no Spring Batch or Spring Kafka equivalent in one place. |
| Go | Excellent for a lean, high-throughput edge. For a domain-heavy compliance backend we wanted the mature ORM, batch and Kafka integrations that Spring gives. |
| Dual writes during migration | Two sources of truth and reconciliation pain. |

**Trade-off of Spring Boot itself.** A Spring Boot service uses more memory and starts slower than a Go binary, and Java is more verbose. For long-running backend services that start rarely and stay up, that cost was acceptable. Say it plainly: "Python or Go could have hit the latency target too. The ecosystem for the bulk pipeline and typed contracts are what made Spring Boot the better fit."

### Trade-off and what I'd do differently

The strangler period means running two stacks and a shared database for a while, which is operational overhead. If I did it again, I would add the request-ID logging (from MI3) before the first canary, not after, so comparing old and new paths is easier from day one. *(A reflection, not a claim about what happened.)*

### The numbers

**p95 from 1.2 seconds to 300 milliseconds, a 75% cut (HISTORICAL).**
- *Measures:* the 95th-percentile API response time.
- *Derivation:* (1,200 − 300) ÷ 1,200 = 900 ÷ 1,200 = 75%.
- *Why it mattered:* the slow tail is what times out on deadline day.
- *Say it:* "p95 went from 1.2 seconds to 300 milliseconds, a 75% cut."
- *Don't say:* "average latency" (it's p95), or "caching did it".
- *Older band:* earlier resumes said 1,000 to 1,200 ms down to 300 to 400 ms. Use that only if an interviewer cites an older resume.

**1,500+ enterprise clients (HISTORICAL).** Always 1,500+. Never 2,500+ (older, dropped).

**700 to 4,000 requests per minute (HISTORICAL).**
- *Measures:* sustained gateway and service throughput under load and peaks.
- *Derivation:* 700 ÷ 60 ≈ 12 requests per second. 4,000 ÷ 60 ≈ 67 requests per second. That is about 5.7 times more.
- *Why it moved:* the Spring Boot rewrite freed request threads from IRP waits, plus worker autoscaling on queue depth.
- *Say it:* "From 700 to 4,000 requests per minute, so roughly 12 to 67 requests a second."

**Mentored 2 engineers.** Masters only. Never merge with "led 3 engineers" at Uber FRM.

### Questions they will ask

**Q: Caching alone can't take p95 from 1.2 seconds to 300 milliseconds. What did?**
"Right, caching wasn't the tail story. The tail came from PHP workers blocking on the government portal. In the Spring Boot services, request threads stopped waiting on the IRP: they published to Kafka and returned 202, and Kafka consumers made the call through WebClient with a timeout. Add HikariCP connection pooling, N+1 fixes in Hibernate and missing composite indexes, and that's what moved the p95. Redis cut redundant reads by about 30%, which helped the median."

**Q: How did you avoid dual writes during the migration?**
"We kept a shared database through the traffic cutover, so there was only ever one source of truth. Table ownership was split only after a route was 100% on Spring Boot. MockMvc contract tests pinned the PHP response shapes field for field."

**Q: Why Spring Boot and not something lighter?**
"Mostly the ecosystem for this pipeline. Spring Kafka gave us listeners, bounded retries and dead-letter publishing built in. Spring Batch gave restartable chunked imports. Hibernate and Bean Validation covered the database and the request boundary, and Java's static typing suits money and tax payloads. The cost is more memory and slower startup than Go, which didn't matter much for long-running services. Python or Go could have hit the latency target too."

**Q: What did mentoring look like day to day?**
"I set the conventions: controller, service, repository layering, Bean Validation DTOs at the boundary, shared retry and idempotency helpers. Each of the two engineers owned a service extraction. I reviewed their PRs heavily early on and paired on the first canary. By the end both were shipping independently."

**Q: What broke in an early canary?**
"A timeout mismatch. PHP allowed 60 seconds and we'd set 10 seconds on the new service. Some IRP calls legitimately took longer, so they failed on the new path. We moved those calls fully off the request thread onto Kafka consumers and returned 202 with polling. The canary caught it at a small percentage, before full ramp."

---

## A7. Bullet MI2 decoded: Kafka bulk pipeline, quarter sharding, idempotency

> Architected a high-concurrency bulk e-invoicing pipeline processing 1M+ daily government submissions by orchestrating a Kafka event bus and a PostgreSQL database horizontally sharded by tax quarter. Enforced exactly-once, idempotent processing for 100K+ concurrent imports with fault-tolerant state management via dead-letter queues and bounded retries against volatile IRP portals.

### In plain words

I designed the system that takes huge invoice files and registers every invoice with the government, more than a million a day, without ever registering one twice and without one bad batch blocking the rest. Data is split by tax quarter so the busy current quarter stays fast.

### How it works

**Kafka.** Topics for accepted import chunks, IRP submit jobs, signed-response persistence, client webhooks, and an audit projector. Partition key is the client GSTIN (sometimes GSTIN plus document type), so submit, IRN callback and webhook for one taxpayer stay ordered on one partition. Different consumer groups (IRP workers, audit projector, metrics) read the same topic independently.

**Publishing and consuming in Spring Kafka.** The producer side is one call on `KafkaTemplate`. The consumer side is a method marked `@KafkaListener`. Spring runs the listener on its own threads, and the `concurrency` attribute sets how many threads consume in parallel, which is also how many IRP calls one instance can have in flight (illustrative):

```java
// Producer, inside the bulk service: key = GSTIN keeps one taxpayer's events in order
kafka.send("irp-submit-jobs", job.gstin(), job);

// Consumer, inside the IRP worker service
@Component
class IrpSubmitListener {
    private final BatchClaims claims;
    private final IrpClient irp;
    private final KafkaTemplate<String, Object> kafka;

    IrpSubmitListener(BatchClaims claims, IrpClient irp, KafkaTemplate<String, Object> kafka) {
        this.claims = claims;
        this.irp = irp;
        this.kafka = kafka;
    }

    @KafkaListener(topics = "irp-submit-jobs", groupId = "irp-workers", concurrency = "4")
    void onJob(IrpSubmitJob job) {
        if (!claims.tryClaim(job)) return;           // already claimed or done: skip the IRP call
        IrpResult result = irp.submit(job);          // timeout + jittered backoff inside
        claims.markRegistered(job, result);
        kafka.send("irp-responses", job.gstin(), result);
    }
}
```

*What to notice: the claim happens before the IRP call, and if `onJob` throws, Spring Kafka's error handler (below) decides whether to retry or dead-letter it.*

**Quarter sharding in PostgreSQL.** Separate tables or schemas per tax quarter. The application derives the quarter from the invoice date at the API boundary and routes to that shard.

```java
// Illustrative quarter routing
static String quarterOf(LocalDate d) {
    int q = (d.getMonthValue() - 1) / 3 + 1;
    return "y" + d.getYear() + "_q" + q;          // 2024-03-14 -> "y2024_q1"
}

static String invoiceTable(LocalDate invoiceDate) {
    return "invoices_" + quarterOf(invoiceDate);
}
```

The routing lived in the data-access layer, and mismatched quarters were rejected at the boundary. A practical note if asked how this works with Hibernate: a JPA entity maps to one fixed table, so per-quarter routing is usually done with Spring's `JdbcTemplate` and a table name built only from the invoice date (never from user input), or with one schema per quarter. Keep the exact mechanism qualitative unless pressed.

**Idempotency.** The key is `client + fileHash + batchIndex`, plus the client's own invoice references for single invoices. A unique constraint makes the second attempt a no-op.

```sql
-- Illustrative: claim a batch exactly once
INSERT INTO import_batches (idem_key, client_id, file_hash, batch_index, status)
VALUES (:k, :client, :hash, :idx, 'processing')
ON CONFLICT (idem_key) DO NOTHING
RETURNING idem_key;
-- No row returned means another attempt already owns or finished this batch: skip the IRP call.
```

The same claim from Java, inside `BatchClaims.tryClaim`:

```java
int inserted = jdbc.update("""
        INSERT INTO import_batches (idem_key, client_id, file_hash, batch_index, status)
        VALUES (?, ?, ?, ?, 'processing')
        ON CONFLICT (idem_key) DO NOTHING
        """, job.idemKey(), job.clientId(), job.fileHash(), job.batchIndex());
if (inserted == 1) return true;                      // first time we have seen this batch
String status = jdbc.queryForObject(
        "SELECT status FROM import_batches WHERE idem_key = ?", String.class, job.idemKey());
return !"registered".equals(status);                 // skip only if already registered
```

On a conflict the worker looks up the existing row's status. It skips the IRP call only if the batch is already `registered`. A `processing` or failed batch (including a DLQ replay) retries through the same key, so the key prevents a double registration without blocking a legitimate retry.

**Bounded retries and the DLQ in Spring Kafka.** When a listener throws, Spring Kafka's `DefaultErrorHandler` retries the same message with an `ExponentialBackOff` (wait, then wait twice as long, up to a cap and a maximum attempt count). After the last attempt, a `DeadLetterPublishingRecoverer` publishes the message to a dead-letter topic, by default the original topic name plus `.DLT`. Exceptions that will never succeed on retry, such as a malformed invoice, skip the retries and go straight to the DLQ (illustrative values):

```java
@Bean
DefaultErrorHandler kafkaErrorHandler(KafkaTemplate<String, Object> template) {
    var recoverer = new DeadLetterPublishingRecoverer(template);   // -> irp-submit-jobs.DLT
    var backOff = new ExponentialBackOffWithMaxRetries(4);         // a subclass of ExponentialBackOff
    backOff.setInitialInterval(500);                               // ms
    backOff.setMultiplier(2.0);
    backOff.setMaxInterval(30_000);
    var handler = new DefaultErrorHandler(recoverer, backOff);
    handler.addNotRetryableExceptions(InvalidInvoiceException.class);
    return handler;
}
```

Spring Boot wires a single error-handler bean like this into its auto-configured Kafka listeners.

**Jitter on the IRP HTTP call.** Spring's `ExponentialBackOff` has no randomness, so the HTTP call to the IRP adds jitter itself. With WebClient, Reactor's retry spec has it built in (illustrative):

```java
IrpResult submit(IrpSubmitJob job) {
    return webClient.post().uri("/irp/submit")
            .bodyValue(job.payload())
            .retrieve()
            .bodyToMono(IrpResult.class)
            .timeout(Duration.ofSeconds(10))
            .retryWhen(Retry.backoff(3, Duration.ofMillis(500))
                    .maxBackoff(Duration.ofSeconds(30))
                    .jitter(0.5)                         // randomise waits so clients don't retry together
                    .filter(IrpErrors::isTransient))
            .block();                                    // fine here: the listener thread is the bound
}
```

Keep the retry budget small at each layer so the HTTP retries and the Kafka retries don't multiply into a retry storm against the portal.

**Dead-letter queue.** Poison batches (bad data, or repeated IRP rejections) park after the retry budget, so the rest of the import continues. Operators replay them after a fix by re-publishing from the `.DLT` topic.

**Spring Batch for the chunked import.** The bulk service reads the uploaded file with a Spring Batch step. A step is "read N rows, process them, write them, commit". Spring Batch records each committed chunk in its job repository tables, so if the service dies on chunk 37, a restart resumes at chunk 37 instead of row one (illustrative):

```java
@Bean
Step splitImport(JobRepository jobs, PlatformTransactionManager tx,
                 ItemReader<InvoiceRow> s3RowReader,
                 ItemProcessor<InvoiceRow, InvoiceRow> rowValidator,
                 ItemWriter<InvoiceRow> chunkPublisher) {
    return new StepBuilder("splitImport", jobs)
            .<InvoiceRow, InvoiceRow>chunk(1_000, tx)   // illustrative chunk size
            .reader(s3RowReader)                        // streams rows from the S3 file
            .processor(rowValidator)                    // Bean Validation per row
            .writer(chunkPublisher)                     // one Kafka event per chunk, with its batchIndex
            .build();
}
```

*What to notice: Spring Batch gives restartable progress for reading the file, and Kafka plus the idempotency key gives safe processing after that. They solve different halves of the problem.*

**Circuit breaker (verbal only).** Open when the IRP error rate spikes, serve a degraded "pending" status to clients. This is prep depth, not a resume metric.

**Why "exactly-once" holds.** Say this carefully: Kafka delivers at-least-once. The idempotency key and unique constraint make the effect exactly-once. Double registration with the government is not recoverable, which is why this was non-negotiable.

### Why this design

- **Why Kafka?** We needed per-client ordering, durable replay for GST disputes and audit reprocessing, and independent consumer groups on one log. Spring Kafka also gave us listeners, bounded retries and dead-letter publishing without writing that plumbing ourselves.
- **Why shard by quarter?** GST returns and filing spikes are quarter-scoped. Writes land in the current quarter. Older quarters are reconciliation and audit reads. Quarter tables keep hot indexes small and make archiving a cold quarter clean.
- **Why idempotency plus DLQ, not fire-and-forget retries?** A double IRP registration cannot be undone, and one poison batch must not block a 100K-row import.

### Alternatives and why not

| Alternative | Why not |
|---|---|
| SQS | Deletes on acknowledgement, so no cheap multi-consumer replay. SQS FIFO caps throughput per message group. |
| RabbitMQ | Honestly, it could have dispatched tasks at our scale. Kafka won on replay, audit reprocessing and multiple consumer groups without fan-out exchange plumbing. |
| One big table | Hot indexes grow forever. Archiving a quarter means huge deletes. |
| Hash-only sharding | Spreads load, but a quarter's data is scattered, so archive and reconciliation by quarter get harder. |
| Native PostgreSQL RANGE partitioning | A fair option. We owned routing in application code, which is more moving parts, but gave explicit drop and archive of a whole quarter and clearer runbooks. |
| Partition key = random or invoice id | Loses per-taxpayer ordering for submit, callback and webhook. |

### Trade-off and what I'd do differently

Kafka costs operational effort, and application-level shard routing has a footgun: writing to the wrong quarter. We mitigated it by deriving the quarter at the boundary and rejecting mismatches. Today I would evaluate native declarative partitioning first, since it removes the routing code.

### The numbers

**1M+ daily government submissions (HISTORICAL).**
- *Derivation of the rate:* 1,000,000 ÷ 86,400 seconds ≈ 11.6, so about 12 per second on average (ESTIMATED).
- *Peaks:* filing deadlines are the real sizing problem. Peaks were roughly 8 to 10 times the average, so about 100+ per second (ESTIMATED). Queue-based load leveling absorbed them.
- *Say it:* "More than a million submissions a day. That averages around 12 a second, but deadline peaks were 8 to 10 times that."
- *Don't put TPS on the resume.* It's verbal only.

**100K+ concurrent imports (HISTORICAL).** Imports of 100K+ invoices, processed concurrently, with idempotent batches.

**How 1M a day and 4,000 a minute fit together.** They measure different things. Requests per minute is gateway and service capacity (MI1). Daily submissions are IRP-registered documents. They're complementary, not the same meter.

### Questions they will ask

**Q: Why Kafka over SQS or RabbitMQ?**
"We needed three things together: per-client ordering, durable replay for compliance, and several independent consumers on the same stream. Partitioning by GSTIN kept one taxpayer's submit, callback and webhook in order. SQS deletes on ack and FIFO caps throughput per group. RabbitMQ could honestly have handled the task dispatch at our scale, but replay and multi-reader audit were first-class for GST disputes, and Spring Kafka gave us retries and dead-letter publishing out of the box. Kafka's ops cost was the trade-off."

**Q: Why shard by quarter instead of plain partitioning?**
"GST is quarter-scoped and deadline-driven. Writes concentrate in the current quarter, older quarters are mostly reconciliation reads. Quarter tables keep hot indexes small and let us archive a whole quarter cleanly. The cost is routing in application code, and the risk is a wrong-quarter write, which we blocked by deriving the quarter from the invoice date at the API boundary."

**Q: What's your idempotency key and why?**
"Client plus file hash plus batch index. The file hash means re-uploading the same file maps to the same keys, and the batch index pins each chunk. A unique constraint makes a second attempt a no-op, so a retry after a crash can't register twice with the government."

---

## A8. Bullet MI3 decoded: observability, Redis, coverage, deploy success

> Decreased incident triage time by 70% and lowered database read load by 30% by instrumenting ELK and New Relic distributed tracing alongside a Redis caching layer. Hardened the CI/CD release cycle by driving test coverage from 35% to 82%, achieving a 98% deployment success rate.

### In plain words

When something broke, we used to SSH into servers and grep logs. I made every request carry an ID through every service and worker, shipped structured logs to ELK, and added New Relic tracing, so finding the cause got much faster. A Redis cache removed a lot of repeated database reads. And I raised automated test coverage so deploys almost never failed.

### How it works: observability

- **Before:** SSH into boxes and grep, with no correlation between services.
- **After:** structured JSON logs with a request ID, shipped to ELK. New Relic APM traces. Alert rules on error rate and latency.
- **The real win is correlation.** One request ID follows a transaction across API, Kafka consumer and IRP worker.

**How the request ID gets onto every log line.** A servlet filter runs before every controller. It reads the incoming `X-Request-ID` header or makes a new one, and puts it into the MDC. Because the MDC is attached to the thread, every log statement made while serving that request includes the ID without anyone passing it around. A JSON log encoder (for example logstash-logback-encoder) writes MDC fields into each line that ships to ELK (illustrative):

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
class RequestIdFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                    FilterChain chain) throws ServletException, IOException {
        String rid = Optional.ofNullable(req.getHeader("X-Request-ID"))
                             .orElseGet(() -> UUID.randomUUID().toString());
        MDC.put("request_id", rid);
        res.setHeader("X-Request-ID", rid);
        try {
            chain.doFilter(req, res);
        } finally {
            MDC.remove("request_id");    // threads are pooled, so always clean up
        }
    }
}
```

**Carrying it across Kafka.** The MDC lives on one thread, so it does not cross a Kafka hop by itself. The producer copies it into a message header, and the consumer puts it back into its own MDC (illustrative):

```java
// Producer
var record = new ProducerRecord<String, Object>("irp-submit-jobs", job.gstin(), job);
record.headers().add("X-Request-ID", MDC.get("request_id").getBytes(StandardCharsets.UTF_8));
kafka.send(record);

// Consumer: the listener method takes the header as an extra parameter
@KafkaListener(topics = "irp-submit-jobs", groupId = "irp-workers")
void onJob(IrpSubmitJob job, @Header("X-Request-ID") byte[] rid) {
    MDC.put("request_id", new String(rid, StandardCharsets.UTF_8));
    try { /* claim, call IRP, record */ } finally { MDC.remove("request_id"); }
}
```

*What to notice: one ID goes from the HTTP filter, through the Kafka header, into the worker's logs, so one Kibana search shows the whole journey.*

### How it works: Redis cache-aside

Classic cache-aside: on a miss, read the database, then SET with a TTL.

- **Hot keys:** IRP auth tokens (TTL set below the token's lifetime, with a safety margin), client config and feature flags, GSTIN master lookups, tax-rate masters, session and auth lookups.
- **Invalidation:** config and GSTIN keys are deleted inside the update path, so admins never see stale credentials. Slow-changing masters use TTL only, with jitter so expiries don't line up.
- **Stampede control:** TTL jitter plus a SETNX lock (`setIfAbsent` in Spring Data Redis), so one worker recomputes while others wait briefly or serve slightly stale data.

```java
// Illustrative cache-aside with a setIfAbsent single-flight lock
ClientConfig getClientConfig(long clientId) throws JsonProcessingException {
    String key = "cfg:" + clientId;
    String hit = redis.opsForValue().get(key);                  // redis is a StringRedisTemplate
    if (hit != null) return json.readValue(hit, ClientConfig.class);

    String lock = "lock:" + key;
    if (Boolean.TRUE.equals(redis.opsForValue().setIfAbsent(lock, "1", Duration.ofSeconds(5)))) {
        try {
            ClientConfig cfg = configRepo.load(clientId);
            Duration ttl = Duration.ofSeconds(3600 + ThreadLocalRandom.current().nextInt(301));
            redis.opsForValue().set(key, json.writeValueAsString(cfg), ttl);   // TTL with jitter
            return cfg;
        } finally {
            redis.delete(lock);
        }
    }
    sleepQuietly(Duration.ofMillis(50));                        // someone else is rebuilding
    String after = redis.opsForValue().get(key);
    return after != null ? json.readValue(after, ClientConfig.class) : configRepo.load(clientId);
}
```

*What to notice: `setIfAbsent` with a 5-second expiry is Redis `SET NX EX`, so only one caller across all instances rebuilds the key, and a crashed holder can't keep the lock forever.*

**Why not just `@Cacheable`?** Spring's `@Cacheable` annotation does cache-aside in one line, and `@Cacheable(sync = true)` stops a stampede inside one JVM. It does not coordinate across instances, so with many worker instances hitting the same key during a bulk import, the explicit cross-instance lock is the safer pattern for the hottest keys.

**Why 30% fewer reads is plausible.** The same client config and GSTIN validation ran on every invoice in a bulk import. Across 100K-row imports, caching those lookups removes a huge duplicate read fan-out.

### How it works: coverage and deploy success

Coverage went from 35% to 82% with JUnit 5 and Mockito, measured by JaCoCo and enforced as a CI gate: the JaCoCo check fails the build if coverage drops below the agreed threshold. Focus was money paths first: registration, reconciliation, imports. Deployment success reached 98%.

A typical unit test mocks every dependency and checks one rule. This one proves a duplicate batch never reaches the government portal (illustrative):

```java
@ExtendWith(MockitoExtension.class)
class IrpSubmitListenerTest {
    @Mock BatchClaims claims;
    @Mock IrpClient irp;
    @Mock KafkaTemplate<String, Object> kafka;
    @InjectMocks IrpSubmitListener listener;

    @Test
    void skipsIrpWhenBatchAlreadyClaimed() {
        IrpSubmitJob job = Fixtures.job("acme", "9b1e", 37);
        when(claims.tryClaim(job)).thenReturn(false);

        listener.onJob(job);

        verifyNoInteractions(irp);           // no second registration
    }
}
```

Database-heavy paths, such as the idempotent claim and quarter routing, are better tested against a real PostgreSQL started in Docker by Testcontainers, because a mock cannot prove that `ON CONFLICT` behaves as expected. That is general good practice; keep it qualitative if asked how many such tests existed.

### Why this design

- **Why ELK plus New Relic?** ELK gives searchable logs. New Relic gives traces and APM. Together, an alert in New Relic leads straight to the request ID's logs in Kibana.
- **Why cache-aside and not write-through everywhere?** Most hot data is read far more than written. Cache-aside only caches what's actually requested and is simple to reason about.
- **Why a coverage gate on money paths first?** Bugs there are the expensive ones in a compliance product.

### Alternatives and why not

| Alternative | Why not |
|---|---|
| Keep SSH and grep | No correlation across services, slow triage. |
| Write-through cache everywhere | More write-path complexity for data that's rarely written. |
| No stampede control | A popular key expiring during a 100K import sends every worker to the database at once. |
| Chasing 100% coverage | Diminishing returns. Covering the money paths was the high-value target. |

### The numbers

**Triage down 70% (HISTORICAL cut, ESTIMATED baseline).**
- *Measures:* time from an alert to finding the cause.
- *Derivation:* roughly 30 minutes before to under 10 minutes after. 30 to 9 minutes is a 70% cut. The 30-minute baseline is an estimate.
- *Say it:* "Triage got about 70% faster, roughly from half an hour to under ten minutes."
- *Don't say:* that I was an incident commander or owned a formal pager rotation. Claim alerting and faster triage.

**Database read load down 30% (HISTORICAL).** From Redis cache-aside on hot lookups.

**Coverage from 35% to 82% (HISTORICAL).** JUnit 5 and Mockito, measured by JaCoCo, CI gate, money paths first.

**98% deployment success (HISTORICAL).** Under the CI gates.

**Not on the PDF:** support tickets down 35% (older resume, client usage dashboard and log downloads) and audit-log churn down 15%. Don't volunteer them. If an interviewer brings up tickets from an older resume, say it was ops attribution from that time, and I owned the dashboard engineering, not every ticket outcome.

### Questions they will ask

**Q: Prove the 70% triage cut isn't a vanity metric.**
"Before, we SSH'd into boxes and grepped, with no way to connect logs across services. After, a servlet filter put a request ID into the logging MDC, Kafka headers carried it to the consumers, and it followed each request through the API, the Kafka consumer and the IRP worker, with structured logs in ELK, New Relic traces and alerts on error rate and latency. Going from roughly half an hour to under ten minutes is my estimate of the baseline behind the 70% figure. The real change was correlation."

**Q: Cache-aside: keys, TTLs, invalidation, thundering herd?**
"Hot keys were IRP auth tokens, client config and flags, GSTIN masters and tax rates. Config and GSTIN were deleted on write. Masters used TTL with jitter. For stampedes, jitter plus a SETNX lock, `setIfAbsent` in Spring Data Redis, so one worker rebuilds and the rest wait or serve slightly stale. The 30% read cut makes sense because every row of a 100K import hit the same lookups."

---

## A9. Design decisions at a glance

| Decision | Chose | Rejected | Why |
|---|---|---|---|
| Migration shape | Strangler plus gateway canaries | Big-bang rewrite | Zero tolerance on filing days. Rollback is a config flip. |
| Service framework | Spring Boot services plus Kafka consumers | A Python framework, or keep PHP | IRP calls must never pin request threads. Spring Kafka and Spring Batch cover the pipeline. |
| Event bus | Kafka | SQS or RabbitMQ alone | Per-GSTIN ordering, durable replay, multiple consumer groups. |
| Partition key | Client GSTIN (optionally plus doc type) | Random or invoice id | Per-taxpayer order for submit, callback, webhook. |
| Data during cutover | Shared DB, then split | Dual writes | One source of truth. |
| Shard strategy | PostgreSQL by tax quarter | One big table, or hash only | GST is quarter-scoped. Cold quarters archive cleanly. |
| Fault model | Idempotency, `DefaultErrorHandler` backoff, DLQ | Fire-and-forget retries | Double IRP registration is unrecoverable. |
| Bulk import | Spring Batch chunked step, then Kafka | One long loop over the file | A crash resumes at the last committed chunk. |
| Cache | Cache-aside Redis plus `setIfAbsent` lock | Write-through everywhere | Hot config and GSTIN on every bulk row. Stampede control. |

---

## A10. Tech used and why

| Tech | One line | Why here | Alternative |
|---|---|---|---|
| Java | Statically typed JVM language. | Typed money and tax payloads, real threads, mature backend ecosystem. | PHP (the legacy). |
| Spring Boot | Java service framework with an embedded web server. | REST controllers, Bean Validation, Spring Kafka, Spring Batch, Spring Data Redis in one stack. | A Python framework, Go. |
| Hibernate | Java ORM, used through Spring Data JPA. | Entity mapping and repositories for PostgreSQL. N+1 fixes with entity graphs. | Plain JDBC everywhere. |
| Kafka | Replayable event log. | Ordering per GSTIN, replay, multiple consumers. Spring Kafka for listeners, retries and DLQ. | SQS, RabbitMQ. |
| PostgreSQL | Relational database. | Strong consistency for invoice state, quarter sharding. | MySQL (the monolith's shared DB during cutover). |
| MongoDB | Document store. | Flexible invoice payload snapshots and raw IRP and vendor responses. | JSON columns in PostgreSQL. |
| Redis | In-memory cache. | Cache-aside for hot lookups, `setIfAbsent` locks. | Memcached. |
| Elasticsearch | Search engine. | Invoice search and the ELK log store. | PostgreSQL full-text search. |
| Docker | Containers. | One image per service. | Bare VMs. |
| ELK | Log pipeline and search. | Structured logs with request IDs from the MDC. | Grep on boxes. |
| New Relic | APM and tracing. | Java agent traces and alerts across services. | Datadog. |
| AWS | Cloud. | Hosting, Amazon S3 for import files. | Other clouds. |

**Supporting pieces inside the Spring Boot services** (not separate items on the tech line): Spring Batch for chunked imports, `@Async` and `@Scheduled` for PDFs, email and webhooks, HikariCP for connection pooling, WebClient for the IRP, and JUnit 5, Mockito and JaCoCo for tests and coverage.

**Why both MongoDB and Elasticsearch?** Mongo held flexible invoice payload snapshots and vendor responses. Elasticsearch powered invoice search and the ELK stack.

---

## A11. Hard problems and failure stories

**The canary timeout mismatch.** *What broke:* the new Spring Boot route timed out on some legitimate IRP calls. *How we found it:* the canary at a small percentage showed a higher error rate than PHP. *Cause:* PHP allowed 60 seconds, we had set 10. *Fix:* moved IRP calls fully off the request thread onto Kafka consumers and returned 202 with polling. *Lesson:* canaries exist to catch exactly this before it hits all clients, and timeouts are part of the API contract.

**Never double-register.** *Risk:* a worker crashes after the IRP accepted an invoice but before we recorded it, and the retry registers again. *Fix:* claim the batch with an idempotency key and unique constraint before calling the IRP, and skip if already claimed or done. *Lesson:* when a side effect can't be undone, idempotency is designed in, not bolted on.

**A poison batch blocking an import.** *Risk:* one malformed batch retried forever stalls a 100K import. *Fix:* bounded retries through `DefaultErrorHandler`, then the `DeadLetterPublishingRecoverer` parks it on the DLQ. Malformed data is marked not-retryable so it goes there immediately. The rest of the import continues, and operators replay after a fix.

**Cache stampede during bulk imports.** *Risk:* a hot config key expires mid-import and every worker hits the database. *Fix:* TTL jitter plus a `setIfAbsent` single-flight lock.

**Wrong-quarter writes.** *Risk:* application routing writes an invoice into the wrong quarter shard. *Fix:* derive the quarter from the invoice date at the API boundary and reject mismatches.

---

## A12. Say this carefully (Masters)

<div class="callout warn">

| Say this | Don't say this |
|---|---|
| "1,500+ enterprise clients." | "2,500+ clients." |
| "Mentored two engineers." | "Led three engineers" (that's Uber FRM). |
| "Exactly-once in effect: at-least-once delivery plus idempotency keys." | "Kafka guarantees exactly-once to the government." |
| "About 12 a second on average, 8 to 10 times that at deadline peaks, estimated." | Putting TPS or RPS on the resume. |
| "Taking IRP calls off request threads, pooling and query fixes moved p95. Redis moved the median." | "Caching cut p95 by 75%." |
| "Kafka carried the events. Kafka consumers and Spring Batch jobs did the work." | "Kafka did everything" or "Spring Batch made it exactly-once" (idempotency keys did). |
| "Claimed alerting and faster triage." | "I was the incident commander" or "owned the pager rotation." |
| "Circuit breaker is how I'd describe the degraded mode." | Quoting a circuit-breaker metric. |
| Kafka at Masters is a different product from Uber Menu. | Flink at Masters. |

</div>

---

# Part B. GeeksforGeeks

## B1. The one-minute version (say this out loud)

"At GeeksforGeeks, my first role, I worked on the courses platform. The doubt-support system, where learners post questions on articles and courses, ran on legacy PHP and struggled during live coding contests. I migrated its backend to Django, which stabilised it at 10K plus daily queries and 10x contest spikes. I built the REST APIs for voting, pinning and locking threads across MySQL, MongoDB, Redis and Elasticsearch, and the growth team attributed a 20% lift in premium subscriptions to that work.

I also launched an influencer analytics and earnings dashboard that tracked transactions and affiliate coupon conversions, which the business tied to a 30% lift in course sales. And I designed asynchronous scheduled workflows for video processing, reminders and data cleanup, which raised engineering operational efficiency by about 70%. I owned the engineering. The business team attributed the lifts."

---

## B2. The business in plain English

**Who the users are.** Learners on GeeksforGeeks courses and articles, and influencer partners (content creators) who promote courses with affiliate coupons.

**What they do.** Learners post doubts (questions), vote on helpful answers, and read pinned answers. During live coding contests, traffic jumps about tenfold. Influencers want to see how their coupons convert and what they've earned.

**What hurt before.** The PHP doubt-support backend lacked transactions and validation discipline and buckled during contest spikes. Influencer reporting and ops chores (video handoffs, reminders, recording cleanup) were manual.

**Why the company paid for this.** A reliable doubt-support experience is a premium feature, so it drives subscriptions. Good influencer analytics keeps partners promoting, which drives course sales. Automating ops chores frees engineers.

---

## B3. Words you need (GFG)

| Term | Plain meaning | Analogy |
|---|---|---|
| **Doubt-support platform** | The Q&A layer on articles and courses where learners ask and answer questions. | A class noticeboard for questions. |
| **Django and DRF** | Django is a "batteries included" Python web framework (ORM, admin, auth). DRF (Django REST Framework) builds REST APIs on top. | A fully equipped kitchen versus buying every pan separately. |
| **ORM** | Object-relational mapper: work with database rows as Python objects. | A translator between Python and SQL. |
| **REST API** | Web endpoints using standard HTTP verbs on resources, such as `POST /doubts/42/vote`. | A menu of standard orders a waiter understands. |
| **Voting** | Users upvote helpful answers. One vote per user per item. | A show of hands where each person has one hand. |
| **Pinning** | Moderators or authors pin an answer to the top of a thread. | Pinning a notice to the top of the noticeboard. |
| **Locking a thread** | Closing a thread to new replies. | Putting "closed" on the noticeboard question. |
| **Hot row** | One database row updated so often it becomes a bottleneck, such as a vote counter on a viral post. | One checkout lane everyone insists on using. |
| **Source of truth** | The system whose data wins if copies disagree. | The original contract, not the photocopies. |
| **Affiliate coupon conversion** | A purchase made using an influencer's coupon code. | A referral code at a gym. |
| **Cron / scheduled workflow** | A job that runs on a schedule. | An alarm clock for code. |
| **Lease or advisory lock** | A short-lived lock so only one host runs a given job at a time. | A "room booked" sign on the door. |

MySQL, MongoDB, Redis and Elasticsearch are defined in Part A.

---

## B4. Architecture (GFG)

```mermaid
flowchart LR
    U["Learners and influencers"] --> DJ["Django and DRF: doubt APIs, votes, pins, locks, dashboard"]
    DJ --> MY["MySQL: threads, permissions, votes, source of truth"]
    DJ --> RD["Redis: counters, badges, unread"]
    DJ --> MG["MongoDB: flexible bodies and attachments"]
    DJ --> ES["Elasticsearch: doubt and content search"]
    CR["Scheduled workers with lease lock"] --> VID["Video processing handoff"]
    CR --> REM["Reminders over reused SMTP connection"]
    CR --> CLN["Recording and data cleanup"]
    CR --> MY
```

*What to notice: MySQL is the truth for votes and threads, Redis only serves fast display counters, and every scheduled job takes a lease first so two hosts never run it twice.*

**Scale honesty.** 10K+ daily queries averages well under one request a second (10,000 ÷ 86,400 ≈ 0.12, ESTIMATED). Contest days are about 10 times that, concentrated into contest windows. The story is reliability and surviving spikes, not "Uber scale".

---

## B5. One vote, step by step (illustrative)

1. Learner 9917 taps upvote on answer 5521. The app calls `POST /api/answers/5521/vote`.
2. Django checks the thread isn't locked and the user is allowed to vote (some interactions were gated behind premium).
3. Insert into `votes (user_id, content_id)` with a unique constraint. If the user already voted, the constraint makes it a no-op or an update, never a double count.
4. Increment the Redis display counter `votes:5521`.
5. A periodic job reconciles Redis counters to MySQL counts, so drift is corrected and MySQL stays the truth.

```sql
-- Illustrative vote table
CREATE TABLE votes (
  user_id    BIGINT NOT NULL,
  content_id BIGINT NOT NULL,
  value      TINYINT NOT NULL,
  created_at DATETIME NOT NULL,
  PRIMARY KEY (user_id, content_id)
);
INSERT INTO votes (user_id, content_id, value, created_at)
VALUES (9917, 5521, 1, NOW())
ON DUPLICATE KEY UPDATE value = VALUES(value);
```

---

## B6. Bullet G1 decoded: Django migration, doubt APIs, 20% premium lift

> Stabilized the doubt-support platform to handle 10K+ daily queries and 10x traffic spikes during live coding contests by migrating the backend to Django. Engineered high-throughput REST APIs for voting, pinning, and locking threads utilizing MySQL, MongoDB, Redis, and Elasticsearch, driving a 20% lift in premium subscriptions.

### In plain words

I moved the doubt-support backend from PHP to Django so it stopped falling over during contests, and built the APIs that let learners vote, pin and lock threads. The growth team credited that work with a 20% relative lift in premium subscriptions.

### How it works

**The migration.** Incremental, page by page, behind the same URLs, to Django with DRF. Reliability came from ORM-managed transactions, request validation, separating read views from write endpoints, and staging plus code review discipline the PHP stack lacked.

**Voting.** Unique `(user_id, content_id)` so a double submit is idempotent. Display counters in Redis, reconciled asynchronously to MySQL, so viral posts don't create hot-row contention.

**Pinning.** Per-context ordering columns, so a pinned answer sorts first within its thread, not a free-for-all sort.

**Locking threads.** Locking closes a thread to new replies. The bullet names it as one of the APIs. If asked for implementation detail beyond "a locked state checked on the reply path", keep it qualitative.

**The data split.** MySQL holds relational threads, permissions and votes (source of truth). MongoDB holds flexible doubt bodies and attachments whose shape varies. Elasticsearch powers search across doubts and content. Redis serves hot reads: counters, badges, unread counts.

**Unread counts.** Per-user counters in Redis for the badge, durable rows in MySQL for threads and messages. Increment on a new reply, clear on read. A periodic reconcile from MySQL fixes drift.

### Why this design

- **Why Django?** In 2021 this was a CMS-style product. Django's admin, auth and ORM came built in. (Masters later needed high-concurrency calls to government APIs and an event-driven bulk pipeline, which is why Spring Boot with Spring Kafka and Spring Batch fit there.)
- **Why a unique constraint plus Redis?** The constraint guarantees correctness. Redis keeps the display fast without hammering one MySQL row.
- **Why four data stores?** Each does one job: relational truth, flexible documents, search, and hot reads.

### Alternatives and why not

| Alternative | Why not |
|---|---|
| Big-bang rewrite or staying on PHP | Outage risk, or the same instability. |
| Counter only in Redis | Fast, but can drift or be lost. Needs a source of truth. |
| Update the MySQL counter on every vote | Viral posts melt one hot row. |
| Store everything in MySQL JSON columns | Search and flexible document shapes are different jobs. |

### The numbers

**10K+ daily queries (standardised).** Order of ten thousand daily interactions. Never 100K. Older resumes said "1,000+ doubts a day" (a narrower metric) or 100K (dropped).

**10x traffic spikes (ESTIMATED shape).** Contest days run about ten times normal traffic.

**20% lift in premium subscriptions (HISTORICAL, relative, attributed by growth).**
- *Say it:* "A 20% relative lift in premium subscriptions, attributed by the growth team. I owned the APIs and the reliability."
- *Don't say:* "15 to 20%" (older wording) or that I alone caused it.

### Questions they will ask

**Q: Design unread counts for 10K+ daily queries without melting MySQL.**
"Per-user counters in Redis for the badge, durable threads and messages in MySQL. Increment on a new reply, clear on read. A periodic job reconciles from MySQL to fix drift. The Django migration gave us the transactional write path the PHP stack lacked."

**Q: Voting idempotency and hot rows?**
"A unique constraint on user and content makes a double submit a no-op. Display counts live in Redis and reconcile to MySQL asynchronously, so a viral post doesn't hammer one row. MySQL stays the truth."

---

## B7. Bullet G2 decoded: influencer dashboard and scheduled workflows

> Accelerated platform course sales by 30% by launching an influencer analytics and earnings dashboard to dynamically track transactions and affiliate coupon conversions. Increased engineering operational efficiency by 70% by designing asynchronous scheduled workflows for automated video processing, user reminders, and data cleanup.

### In plain words

I built a dashboard where influencers see their coupon sales and earnings, which helped them promote courses better. The business tied it to a 30% rise in course sales. I also automated the chores the team did by hand, such as video processing handoffs, reminders and cleanup, which saved about 70% of that effort.

### How it works

**Dashboard.** Near-real-time counters in Redis plus daily rollups computed by scheduled jobs, showing transactions, affiliate coupon conversions and earnings per partner.

**Scheduled workflows.** Jobs covered video processing handoffs, automated reminders, payment processing, and cloud recording deletion and data cleanup. Reliability pattern:
- a lease or database advisory lock so two hosts never double-run a job,
- idempotent job keys,
- structured success and failure logs,
- retry or dead-letter for partial batches.

```python
# Illustrative lease so only one host runs a job
def run_once(job_name, fn):
    if not redis.set(f"lease:{job_name}", host_id, nx=True, ex=900):
        return  # another host holds the lease
    try:
        fn()
    finally:
        if redis.get(f"lease:{job_name}") == host_id:
            redis.delete(f"lease:{job_name}")
```

**SMTP reuse (older-resume detail, not on the PDF).** Reminder and promo batches reused one SMTP connection instead of a new TCP and TLS handshake per message. Handshakes often cost 100 to 400 ms each, so amortising them cut wall-clock send time roughly in half. The "50% faster" claim is from the 1-year and 2.5-year resumes and is prep depth only.

### The numbers

**Course sales up 30% (HISTORICAL, business attribution).** "The business team attributed it. I owned the engineering."

**Engineering ops efficiency up 70% (HISTORICAL).** Framed as time saved on the manual video, reminder and cleanup workflows.

### Questions they will ask

**Q: How do you keep scheduled jobs reliable?**
"A lease so only one host runs each job, idempotent job keys so a rerun is safe, structured logs, and retry or dead-letter for partial batches. The 70% is time saved on those manual workflows."

**Q: Is the 30% sales lift yours?**
"I built the dashboard. The business team measured and attributed the 30% lift. I'm careful to own the engineering and let them own the causality."

---

## B8. Hard problems and lessons (GFG)

- **Hot rows on viral posts.** Solved with Redis display counters plus async reconcile.
- **Contest spikes.** The Django migration's transactions, validation and read/write separation are what made the 10x spikes survivable.
- **Double-running crons across hosts.** Solved with leases and idempotent job keys.

**What I'd change today.** Put vote events on a queue with event-sourced counters, make idempotency keys the default on reminder jobs, and set clearer latency targets for contest days. The Django migration and vote and pin models were the right call in 2021. The event patterns I later owned at Masters are what I'd backport.

## B9. Say this carefully (GFG)

<div class="callout warn">

- Say **20%** premium lift, relative, attributed by growth. Not 15 to 20%.
- Say **10K+ daily queries**. Not 100K.
- Own the engineering. The business attributed the 30% sales and 70% efficiency figures.
- SMTP 50% is older-resume prep depth, not a PDF claim, and it's GFG, not Masters.

</div>

---

# Part C. Mock interview: hardest questions

### Masters India

**Interviewer:** You were on AWS. Why Kafka instead of RabbitMQ or SQS?
**Candidate:** "We needed per-client ordering, durable replay for compliance, and independent consumer groups together. The partition key was the client GSTIN, sometimes plus document type, so submit, IRN callback and webhook for one taxpayer stayed ordered. Kafka lets us reset offsets and reprocess after a parser bug. SQS deletes on ack, has no cheap multi-consumer replay, and FIFO caps throughput per group. RabbitMQ could have worked for task dispatch at our scale, and I say that honestly. Kafka won because replay was first-class for GST disputes, multiple groups could read one topic without fan-out plumbing, and Spring Kafka gave us listeners, bounded retries and dead-letter publishing out of the box. Ops cost was the trade-off."

**Interviewer:** Derive TPS and RPS from your numbers. Do they hang together?
**Candidate:** "A million a day is 1,000,000 over 86,400 seconds, about 11.6, so roughly 12 a second on average. Filing deadlines were the sizing problem, roughly 8 to 10 times that, so 100-plus a second at peak. Those are estimates. Throughput went from 700 to 4,000 requests a minute, which is about 12 to 67 requests a second. They measure different things: requests per minute is gateway and service capacity, daily submissions are registered documents."

**Interviewer:** What drove p95 from 1.2 seconds to 300 milliseconds? Caching alone can't.
**Candidate:** "Agreed. Caching helped the median and read-heavy endpoints. The tail was PHP workers blocking on the government portal. In the Spring Boot services, request threads publish to Kafka and return 202, and Kafka consumers call the IRP through WebClient with timeouts. HikariCP pooling ended connect storms, and N+1 fixes in Hibernate plus composite indexes on client and invoice date sped up lists. Redis cut redundant reads by about 30%. Freeing request threads, pooling and queries moved the tail. The cache moved the body."

**Interviewer:** Cache-aside specifics. Make the 30% plausible.
**Candidate:** "Miss, read the database, set with a TTL. Hot keys were IRP auth tokens with a TTL below the token lifetime, client config and flags, GSTIN masters and tax rates. Config and GSTIN were deleted on write. Masters were TTL with jitter. Stampedes were handled with jitter plus a SETNX lock, which is `setIfAbsent` in Spring Data Redis. 30% is plausible because every row of a 100K import ran the same config and GSTIN lookups."

**Interviewer:** Why shard by quarter instead of plain partitioning?
**Candidate:** "GST is quarter-scoped and deadline-driven. Writes concentrate in the current quarter, older quarters are reconciliation reads. Quarter tables keep hot indexes small and let us archive a whole quarter cleanly. Versus native range partitioning, we owned the routing in application code, more moving parts but explicit archive and clear runbooks. The footgun is wrong-quarter writes, so we derived the quarter from the invoice date at the API boundary and rejected mismatches."

**Interviewer:** Sketch the IRP path and where Kafka sits.
**Candidate:** "The client's ERP posts invoice JSON. We validate schema and GSTIN and register with the IRP, which returns a signed IRN and QR, and that's what makes a B2B invoice valid. Kafka carries the async stages: accepted chunks, IRP submit jobs, persisting responses to Mongo snapshots, and client webhooks. Idempotency keys plus client references stop double registration, which is not recoverable. Bulk files go to S3, a Spring Batch step chunks them, Kafka consumers send them to the IRP with bounded concurrency, and progress streams to the dashboard."

**Interviewer:** What did "mentored 2" mean day to day?
**Candidate:** "Strangler behind the gateway, not big bang. I owned the conventions and shared helpers. Each engineer extracted a service. I reviewed their early PRs closely and paired on the first canary: Nginx percentage route, watch errors and latency, ramp or roll back by config. Shared DB during cutover avoided dual writes."

**Interviewer:** ELK plus New Relic cut triage 70%. Prove it's not vanity.
**Candidate:** "Before, SSH and grep, no correlation. After, structured logs with request IDs in Elasticsearch and Kibana, New Relic traces, alerts on error rate and latency. Roughly 30 minutes to under 10 is my estimated baseline behind the 70% figure. The real win was one request ID across the API, the Kafka consumer and the IRP worker. Coverage went from 35% to 82% on money paths and deploy success reached 98%."

### GeeksforGeeks

**Interviewer:** Doubt support at 10K+ daily queries. Design unread counts without melting MySQL.
**Candidate:** "10K a day is well under one request a second on average, with contest days about 10 times that. Redis per-user counters serve the badge, MySQL holds threads and messages. Increment on a reply, clear on read, and reconcile periodically from MySQL. The Django migration gave us transactions and validation the PHP stack lacked."

**Interviewer:** Voting idempotency and the four-store split?
**Candidate:** "Unique user and content constraint for idempotency. Redis counters reconciled to MySQL to avoid hot rows. MySQL for threads, permissions and truth, Mongo for variable bodies and attachments, Elasticsearch for search. Pinning is per-context ordering. The 20% premium lift is the growth team's relative attribution."

**Interviewer:** Crons claimed +70% ops efficiency. How do you keep crons honest?
**Candidate:** "Leases so two hosts don't double-run, idempotent job keys, structured logs, and retry or dead-letter for partial batches. The 70% is time saved on manual video, reminder and cleanup work. The 30% course sales is business attribution on the influencer dashboard."

**Interviewer:** You also cut email send time 50% with SMTP changes. Real?
**Candidate:** "That's from my earlier resumes, not the current one. We reused one SMTP connection across a batch instead of a TCP and TLS handshake per message, which is often 100 to 400 milliseconds each. Amortising that roughly halves wall-clock time for reminder and promo batches. It's a GFG detail, not a Masters claim."

---

# Part D. Confidence audit

| Resume claim | Rating | Fallback wording if pressed |
|---|---|---|
| MI1: Spring Boot migration, mentored 2, p95 from 1.2s to 300ms, 1,500+ clients, 700 to 4,000 rpm | Solid | Older band 1,000 to 1,200 ms to 300 to 400 ms if they cite old resumes. Never 2,500+. |
| MI2: Kafka, quarter sharding, 1M+ a day, 100K+ idempotent imports, DLQ, bounded retries | Solid on pattern. Needs care on peak TPS | About 12 a second average and 100+ peak, both ESTIMATED. Admit RabbitMQ could work at that scale. |
| MI3: ELK and New Relic, triage down 70%, reads down 30%, coverage 35 to 82%, 98% deploys | Solid on coverage and deploys. Needs care on triage baseline | Claim alerting, not pager ownership. Baseline about 30 to under 10 minutes is ESTIMATED. |
| G1: Django, 10K+ daily, 10x spikes, voting, pinning, locking, 20% premium | Solid on engineering. Needs care on attribution | "Relative lift attributed by growth. I owned the APIs and reliability." |
| G2: dashboard, 30% sales, scheduled workflows, 70% ops | Needs care on attribution | Own the engineering. Sales and efficiency are business-attributed HISTORICAL figures. |

---

# Part E. Practice drill

1. **What does Masters India do?** GST e-invoicing for Indian enterprises: we validate invoices and register them with the government IRP, which returns a signed IRN and QR.
2. **Why migrate off PHP?** Synchronous workers blocked on slow IRP calls, deploys were all-or-nothing, and deadline spikes caused timeouts.
3. **How did the migration avoid risk?** Strangler with per-route Nginx canaries, shared database during cutover, contract tests pinning PHP responses, rollback by config.
4. **What actually cut p95?** Taking IRP calls off request threads (Kafka consumers with WebClient timeouts), HikariCP connection pooling, N+1 and index fixes. Redis helped the median.
5. **Derive the 75%.** From 1,200 ms to 300 ms saves 900, and 900 ÷ 1,200 is 75%.
6. **Convert 700 and 4,000 requests per minute.** About 12 and 67 requests a second.
7. **Why Kafka?** Per-GSTIN ordering, replay for disputes, and independent consumer groups on one log.
8. **Why shard by tax quarter?** GST is quarter-scoped. Hot writes in the current quarter, small indexes, clean archiving.
9. **What's the idempotency key?** Client plus file hash plus batch index, with a unique constraint, checked before calling the IRP.
10. **Is it truly exactly-once?** In effect: at-least-once delivery plus idempotent writes.
11. **What does the DLQ do?** Parks poison batches after bounded retries so the rest of the import continues, for operator replay.
12. **Where does 70% triage come from?** Request IDs across services, ELK and New Relic. Roughly 30 minutes to under 10, baseline estimated.
13. **Why did Redis cut reads 30%?** Every row of a bulk import hit the same config and GSTIN lookups.
14. **GFG: why Django?** In 2021 a CMS-style product benefits from Django's admin, auth and ORM.
15. **GFG: how are votes idempotent?** Unique user and content constraint. Redis counters reconcile to MySQL.

---

# Part F. 3-minute whiteboard script (Masters India)

**First (30 seconds): the problem.** Write "Invoice in, signed IRN out". Say: "Enterprises must register B2B invoices with the government IRP. We had 1,500+ clients, a synchronous PHP monolith, and deadline spikes that caused timeouts."

**Second (90 seconds): draw the system.** Client ERP, then Nginx gateway with a split arrow to "PHP (old)" and "Spring Boot (new)". From Spring Boot draw Redis, PostgreSQL by quarter, S3, and Kafka. From Kafka draw Workers (Kafka consumers and Spring Batch), then IRP. Add a DLQ box off Workers and ELK and New Relic underneath. Say: "Strangler with per-route canaries took p95 from 1.2 seconds to 300 milliseconds and throughput from 700 to 4,000 requests a minute. Bulk imports go S3, Kafka keyed by GSTIN, workers with bounded concurrency to the IRP. Idempotency key client plus file hash plus batch index means a retry never double-registers. Poison batches go to the DLQ. Over a million submissions a day."

**Third (60 seconds): numbers and caveats.** Write "12/s avg, 8–10x peak (est.)", "triage −70%", "reads −30%", "coverage 35→82%, 98% deploys". Say: "Freeing request threads from IRP waits, pooling and query fixes moved p95, Redis moved the median. Exactly-once means at-least-once plus idempotency. I mentored two engineers through the migration."

**GFG in 30 seconds if asked:** draw Django in the middle with MySQL, Redis, MongoDB and Elasticsearch around it. Say: "PHP to Django for reliability at 10K+ daily queries and 10x contest spikes. Votes idempotent by unique constraint, Redis counters reconciled to MySQL. 20% premium lift attributed by growth."
