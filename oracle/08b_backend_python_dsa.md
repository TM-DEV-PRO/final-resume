# 08b. Backend, Python, DSA, and lookup performance

Questions 10–27 from the OCI loop, plus follow-ups on the same ideas. Seat locking in more detail is also in [05 LLD](05_lld_problems.md). CAP and retries are also in [04 fundamentals](04_system_design_fundamentals.md).

---

## Q10. Explain Django structure / architecture

**What they are testing:** that you have actually used Django (GeeksforGeeks, the doubt-support platform), and that you know it is not "just MVC."

**Definitions**

- **Project:** the whole site. One `settings.py`, one root URLconf, one WSGI/ASGI entry.
- **App:** a Python package for one domain (`doubts`, `votes`, `billing`). A project is a set of apps. Apps are reusable. The project is not.
- **MVT, not MVC.** Django's authors say Model, View, Template. The **view** is the controller (it receives the request and decides what happens). The **template** is the presentation. There is no separate controller layer.
- **ORM:** `Model` classes map to tables. A `QuerySet` is lazy. It does not hit the database until you iterate it.
- **Middleware:** a chain of callables around every request and response. Order in `MIDDLEWARE` is the order of requests, and the reverse order of responses.
- **WSGI vs ASGI:** WSGI is one request per worker thread/process (Gunicorn, uWSGI). ASGI is async (Daphne, Uvicorn) for WebSockets and long-lived connections. My GFG work was the classic WSGI shape. I moved to FastAPI later because the GST product needed async IO for government API calls. Django was the right tool for a CMS-style product with admin, auth, and an ORM.

**The picture**

```
browser
   |
   v
web server (nginx) ---- static files
   |
   v
WSGI server (gunicorn workers)
   |
   v
django.core.handlers.wsgi
   |
   v
MIDDLEWARE  (security, session, auth, csrf, clickjacking, custom)
   |
   v
ROOT_URLCONF  ---- path("doubts/", include("doubts.urls"))
   |                     |
   |                     v
   |                  doubts.views.question_detail(request, id)
   |                     |
   |                     +--> Model / Manager / QuerySet --> DB connection
   |                     +--> Template render (or JsonResponse / DRF serializer)
   v
response walks back out through middleware
```

**What lives where**

| Piece | Role |
|---|---|
| `settings.py` | Installed apps, DB, middleware, templates, static root. Per-environment settings import a base and override. |
| `urls.py` | Route table only. No business logic. |
| `models.py` | Fields, constraints, `Meta.indexes`, custom managers. |
| `views.py` or `views/` | Request in, response out. Thin. Business rules in a service function or model method, not copied into three views. |
| `forms.py` / DRF `serializers.py` | Validation at the boundary. |
| `admin.py` | Staff UI over the same models. |
| `migrations/` | Ordered schema changes. Never edit a migration that has shipped. |
| `templates/` | HTML. Avoid putting queries in templates. |
| `apps.py` | App config, `ready()` for signal registration. |

**Request path in one sentence:** gunicorn calls Django, middleware runs, the URL resolver picks a view, the view uses the ORM, a template or serializer builds the body, middleware can still modify the response.

**What I would say about my GFG work, briefly:** we moved the doubt platform off PHP onto Django and DRF, page by page, behind the same URLs. Votes were a unique `(user, content)` constraint in MySQL, with a Redis counter for the hot read, reconciled back to MySQL so a popular post was not a single hot row. Contest days were about a 10× spike on a base of 10k+ daily queries. Django fit because we wanted admin, sessions, and an ORM, not because it is the fastest async runtime.

### Likely follow-ups

**ORM N+1.** A loop that touches `question.author` for each row issues one query per row. Fix: `select_related('author')` for a foreign key (SQL JOIN) and `prefetch_related('comments')` for a reverse relation or M2M (a second query, then join in Python). I hit the same class of bug at Masters: list endpoints with N+1 and a missing `(client_id, invoice_date)` index.

**`select_related` vs `prefetch_related`.** JOIN vs separate query. JOIN is wrong for many-to-many because it multiplies rows.

**Migrations.** `makemigrations` diffs models against the migration graph. `migrate` applies it in a transaction on Postgres. A column rename is add, backfill, switch, drop. Not one rename on a hot table.

**Signals.** `post_save` hides control flow and breaks bulk `update()` / `bulk_create()` (those don't send per-row signals). I prefer an explicit service call over a signal for anything that must happen.

**Why FastAPI at Masters and Django at GFG.** 2021 product was a content site. The GST product spent its latency on outbound HTTP to the IRP. Django's sync worker model holds a process for the whole round trip. FastAPI plus a worker queue doesn't.

**DRF.** Serializers, viewsets, routers, auth classes. It is still Django underneath: same middleware, same ORM, same process model.

---

## Q11. Database schema for BookMyShow

**Assumptions to state:** one country, movies and live events later, seats are chosen by the user (not "best available"), one booking is one show, payment is a separate service, we need to know who sat where for entry, and a seat hold expires if payment is abandoned.

**What varies and should not be hard-coded:** seat type, price, venue layout. A cinema screen and a stadium are both "a show with labeled seats."

**Entities**

```
city
  id, name

cinema
  id, city_id, name

auditorium
  id, cinema_id, name

seat
  id, auditorium_id, row_label, number, seat_type
  UNIQUE (auditorium_id, row_label, number)
  -- a seat is a physical chair. It does not know about dates.

movie
  id, title, runtime_min, language, certification

show
  id, movie_id, auditorium_id, start_at, end_at, status
  -- status: scheduled, open, cancelled
  INDEX (auditorium_id, start_at)
  INDEX (movie_id, start_at)

show_seat
  id
  show_id
  seat_id
  price_cents          -- price can differ per show and per type
  status               -- FREE, HELD, BOOKED, BLOCKED
  hold_user_id         -- nullable
  hold_expires_at      -- nullable
  version              -- optimistic concurrency
  booking_id           -- nullable, set when BOOKED
  PRIMARY KEY (id)
  UNIQUE (show_id, seat_id)
  INDEX (show_id, status)
  INDEX (hold_expires_at)   -- sweeper

booking
  id, user_id, show_id, status, idempotency_key
  -- status: PENDING, CONFIRMED, CANCELLED, EXPIRED
  UNIQUE (user_id, idempotency_key)
  amount_cents, created_at

booking_seat
  booking_id, show_seat_id
  PRIMARY KEY (booking_id, show_seat_id)

payment
  id, booking_id, provider_ref, status, amount_cents
  UNIQUE (provider_ref)
```

**Why `show_seat` exists instead of a status column on `seat`.** The chair is reusable every show. The thing you lock is "seat A4 at the 7pm show," which is a row in `show_seat`. Generating those rows when the show is published makes locking a single-row update. Generating them lazily is fewer rows and a harder uniqueness race. I would generate them when the show opens.

**Why money is integer cents.** Floats drop precision. Currency is a separate column if you ever leave one country.

**Why `version`.** It is the optimistic lock in Q12. You can also do it with `status` in the `WHERE` clause, which is a form of the same idea.

**Blocked seats** (aisle, broken chair, house seats) are `BLOCKED` and never offered. That is data, not a special code path in the lock.

**Read path for the seat map.** `SELECT seat_id, status, price_cents FROM show_seat WHERE show_id = ?`. That is one index range. Cache the map for a second if the read QPS is high, and treat the cache as a hint. The write path in Q12 is the source of truth.

### Likely follow-up: how do you partition this?

`show_seat` is the hot table. Partition by `show_id` hash, or range by `start_at` if you prune old shows. A very hot show is one partition key. If one show is a celebrity release, that partition is hot. Mitigations: the row lock is per seat, so different seats don't block each other (InnoDB row locks). The hot **row** is the one seat everyone clicks. You cannot shard one row. You serialize that seat, which is what you want. The thing to watch is the **index page** and the connection pile-up, not the lock on seats nobody picked.

---

## Q12. Seat locking and concurrency

**The invariant:** two users never end in `BOOKED` for the same `show_seat`. A hold either converts to a booking or returns to `FREE`. A crashed browser does not lock the seat forever.

**The failure if you do nothing:** two transactions read `status=FREE`, both write `BOOKED`. That is a lost update. Isolation `READ COMMITTED` does not prevent it. You need a lock, a conditional update, or a single-threaded owner of that show.

**Approach I would ship: conditional update (optimistic) plus an expiry**

```sql
UPDATE show_seat
SET status = 'HELD',
    hold_user_id = :user,
    hold_expires_at = now() + interval '8 minutes',
    version = version + 1
WHERE show_id = :show
  AND seat_id = :seat
  AND version = :version_i_read
  AND (
        status = 'FREE'
        OR (status = 'HELD' AND hold_expires_at < now())
      );
```

If `rowcount` is 1, this user holds the seat. If it is 0, someone else won or the version moved. The database is the lock. There is no `SELECT FOR UPDATE` held across the payment call.

**Confirm, after payment:**

```sql
UPDATE show_seat
SET status = 'BOOKED', booking_id = :booking, version = version + 1
WHERE show_id = :show AND seat_id = :seat
  AND status = 'HELD' AND hold_user_id = :user
  AND hold_expires_at >= now();
```

Payment uses an idempotency key on `booking` so a retry does not double-charge. I used the same pattern at Uber FRM: `UPDATE ... WHERE version = ?` so two reviewers cannot overwrite each other, and at Masters: an idempotency key of client + file hash + batch index so a retry cannot double-file an invoice.

**Why the lock is not held during payment.** Payment takes seconds to minutes and calls a third party. A row lock held that long stalls everyone looking at that seat and can pile up connections. The hold is **data** (`status`, `hold_expires_at`), not a database lock.

**Expiry.** A sweeper every few seconds:

```sql
UPDATE show_seat
SET status = 'FREE', hold_user_id = NULL, hold_expires_at = NULL, version = version + 1
WHERE status = 'HELD' AND hold_expires_at < now();
```

The `WHERE` clause on the hold update already treats an expired hold as free, so a late sweeper is safe. The sweeper exists so the seat map is honest.

**Multiple seats in one booking.** Update all of them in **one transaction**, in a fixed seat-id order (deadlock avoidance). If any rowcount is 0, roll the transaction back. Don't hold seat 1 and then discover seat 2 is gone outside the transaction.

```
user taps seats
    |
    v
BEGIN
  UPDATE seat A ... WHERE free or expired   -- order by seat_id
  UPDATE seat B ...
  if any rowcount = 0: ROLLBACK, tell the user which seat is gone
  else: INSERT booking PENDING; COMMIT
    |
    v
payment (no DB row lock held)
    |
    +-- success: UPDATE seats SET BOOKED WHERE still HELD by this user
    +-- fail / timeout: sweeper or explicit cancel sets FREE
```

### Likely follow-up: `SELECT FOR UPDATE`

```sql
BEGIN;
SELECT * FROM show_seat WHERE show_id=? AND seat_id=? FOR UPDATE;
-- check status, then update, then COMMIT
```

This is a **pessimistic** lock. It is correct if the transaction is short. It is the wrong lock to hold across a payment redirect. `SKIP LOCKED` is for a worker claiming jobs from a queue ("give me any free seat"), not for "the user asked for A4." If they ask for A4 and you skip it, you have booked the wrong chair.

**Isolation.** `REPEATABLE READ` (MySQL InnoDB default) plus a unique key on `(show_id, seat_id)` stops a phantom duplicate row. The race on the **status column** still needs the conditional `UPDATE` or `FOR UPDATE`. The unique key stops two `show_seat` rows. It does not stop two updates of one row unless the `WHERE` clause is conditional.

---

## Q13. Seat locking without a database row lock

Say when each one wins. Don't present them as equal.

| Approach | How | When it is better | Cost |
|---|---|---|---|
| **Conditional UPDATE** (Q12) | The row changes only if status is still free. The "lock" is the row version. | Default. One source of truth. | Hot seats serialize on one row, which is correct. |
| **Redis `SET seat:{show}:{id} user NX PX 480000`** | `NX` fails if the key exists. TTL is the hold. A Lua script locks a set of seats or none. | The seat map is extremely hot and you want the DB out of the hold path. | Two sources of truth. Redis loss or eviction double-books unless the DB confirm is still conditional. Use Redis to **win the race**, and the DB conditional update to **commit**. |
| **In-process mutex / singleflight per seat** | A lock inside one app server. | Never as the real lock, unless there is exactly one process. | A second instance does not see the lock. I would mention it only to reject it. |
| **Partition owner** | All holds for `show_id % N` go to one service instance. Single-threaded per show. | You want to avoid distributed locks entirely. | That instance is a bottleneck and a failure domain. Reassign the partition with a lease and a fencing token. |
| **Queue** | The user submits "I want these seats." A single consumer per show applies them in order. | Fairness matters, or you need an audit log of attempts. | Latency of a queue round trip. Overkill for a normal cinema. Right for a ticket drop where 100k people hit one show. |
| **Database advisory lock** | `pg_advisory_xact_lock(show_id, seat_id)` | You don't want a schema change. | Still a DB lock. Held only inside the short transaction, same rule as `FOR UPDATE`. |
| **Optimistic version without a status column** | `UPDATE ... SET version=version+1 WHERE version=?` | Same as Q12. Status in the `WHERE` is enough even without `version`. Version helps the client detect a stale seat map. | |

**What I would actually say:** the conditional update is the lock I trust. Redis is a valid hold cache in front of it if the database becomes the bottleneck. I would not trust only Redis, and I would not trust a mutex in the web process. Payment stays outside the lock, with an idempotency key, because that is the same rule as not holding a DB transaction open across the IRP at Masters.

### Likely follow-up: what if Redis and the DB disagree?

The DB wins. If Redis says held and the conditional `UPDATE` says 0 rows, the user does not get the seat, and you delete the Redis key. If the process crashes after the DB hold and before the Redis key, the DB hold still expires. Design the DB so it is correct with Redis empty.

---

## Q14. How do you make microservices fault tolerant?

**Definition.** Fault tolerant means a dependency's failure does not take the caller down with it, and a restarted instance does not corrupt state. It does not mean every call succeeds.

**The list, in the order I implement them**

1. **Timeouts on every outbound call**, shorter than the caller's own deadline. In Go that is a `context` on the edge and derived contexts inward. A missing timeout is a thread stuck until the kernel's TCP timer, which is how you get a 10-second or multi-minute tail with idle CPU.
2. **Retries only when the operation is idempotent or has an idempotency key.** Exponential backoff with jitter. A budget (retries are a small fraction of traffic), not "three retries at every layer." Three layers of three retries is 27 calls.
3. **Circuit breaker.** After consecutive failures, fail fast and stop hammering the dependency. Half-open to probe. I did this in the Keep/Drop registry: a provider outage falls back to the deterministic score, and the run finishes.
4. **Bulkhead.** A separate pool per dependency so one slow database cannot occupy every thread. The API keeps serving the paths that don't need that database.
5. **Load shedding.** When the queue is past a limit, reject with 429/503 instead of accepting work you will time out.
6. **Idempotent consumers and a dead-letter queue.** At-least-once delivery plus a key you can dedupe. Poison messages go to the DLQ. Masters bulk import did this.
7. **Health checks that mean something.** Readiness fails when the process cannot do work (DB unreachable, pool exhausted). Liveness fails only when the process is wedged. Restarting a process whose dependency is down just crash-loops.
8. **Redundancy across failure domains.** More than one instance, spread so one host, rack, or zone is not the whole service. Stateless app servers make this easy. State stays in a store that has its own replication.
9. **Backwards-compatible deploys.** A new instance must tolerate the old message shape and the old schema. Expand, then migrate, then contract. That is how you restart a third of the fleet without a window.
10. **A client that can degrade.** Cached reads, a default, or a clear error. A timeout with no fallback is just a slower failure.

**What I would not say:** "we use Kubernetes so it's fault tolerant." A restart policy is not a timeout, and it is not idempotency.

### Likely follow-up: what do you measure?

Success rate, latency by dependency, timeout count, retry count, breaker state, pool wait time, DLQ depth. An alarm on "error rate of this API," not only on CPU. I want the breaker opening to be a page only if the fallback is also failing. Otherwise it is a ticket with a graph.

---

## Q15. Orchestration vs choreography

**Definitions.** Both are ways to implement a **saga**: a business transaction split across services, each with a local transaction and a compensating action if a later step fails. There is no single distributed lock across all of them.

| | Orchestration | Choreography |
|---|---|---|
| Who decides the next step | A **coordinator** (a process, a workflow engine) | Each service, when it sees an **event** |
| How data flows | The coordinator calls service A, then B, then C | A emits `SeatsHeld`. Payment consumes it and emits `PaymentCaptured`. Booking consumes that. |
| Good at | A flow you need to see, change, and time out in one place | A small number of steps, teams that should not depend on a central deployer |
| Failure mode | The coordinator is a dependency. If it dies, the flow must resume from persisted state. | You cannot point at one file and see the business process. A missed event or a new consumer changes behavior in a place you forgot. |
| Compensation | The coordinator runs the undo steps it knows about | Each service subscribes to the failure event and undoes its own step |

```
orchestration                         choreography

  coordinator                         seats service
     |  hold seats                         |  SeatsHeld
     v                                     v
  seats service                        payment service
     |  pay                                 |  PaymentCaptured
     v                                     v
  payment                              booking service
     |  confirm                            |
     v                                     +-- on PaymentFailed:
  seats service                               seats service releases the hold
     (or compensate: release)
```

**BookMyShow example.** I would **orchestrate** the booking: hold seats, take payment, confirm seats, and if payment fails or the hold expires, release seats. The steps and the timeout belong to one owner. I would **choreograph** the side effects: confirmation email, loyalty points, analytics. Those consumers can lag and must be idempotent. They must not be on the path that decides whether the seat is sold.

**My own systems.** The Keep/Drop registry is a small orchestrator: deterministic scoring, then LLM batches, checkpoints, a fallback if the provider fails. I did not pull in Temporal or Airflow, because the workflow lived inside one service and the resume state was a file plus a versioned ClickHouse write. I would use a workflow engine when **several teams** own steps and the process outlives one deploy. Uber menu was closer to choreography: scrapers publish to Kafka, Flink consumes, the catalog is an idempotent upsert. Nobody called a central "ingest this menu" function synchronously.

### Likely follow-up: how does the coordinator itself survive a crash?

Persist the step (`HELD`, `PAYING`, `CONFIRMED`) in the same database as the booking, and resume from that row on startup. A coordinator that keeps the step only in memory will double-charge or leave seats held after a restart. This is the same rule as the scoring checkpoints: the completed step is recorded before the next step starts.

### Likely follow-up: outbox

If the coordinator writes "payment captured" and then crashes before it publishes the event, consumers never hear it. Write the business row and an **outbox row** in one local transaction. A relay publishes the outbox. Consumers dedupe by event id.

---

## Q16. Explain CAP theorem

**Definition.** During a **network partition**, a distributed system can pick **consistency** or **availability**, not both. The P in CAP is not optional. Partitions happen. The real choice is what you do when they do.

Be precise about the words, because the casual versions are wrong.

| Letter | Actual meaning |
|---|---|
| **C, consistency** | Linearizability. A read sees the latest **completed** write, as if there were one copy. It does not mean "the database has constraints" and it does not mean ACID by itself. |
| **A, availability** | Every request to a **non-failed** node gets a response. Not "the cluster has a replica somewhere." |
| **P, partition tolerance** | The system keeps running when messages between nodes are lost or delayed. If you give this up, you are assuming a single node. |

**So:** if a partition splits the replicas, you either

- refuse writes or reads on the side that cannot be sure it is up to date (**CP**: etcd, ZooKeeper, a Raft group, Spanner's transactional path), or
- answer anyway and repair later (**AP**: Dynamo-style, Cassandra with a low consistency level, DNS).

You do not "choose CA." CA means "I assume the network does not partition," which is a single-node system or a system that is allowed to be wrong or down when the network splits.

**PACELC, if they push.** If there is a **P**artition, choose A or C. **E**lse, choose **L**atency or **C**onsistency. Even with a healthy network, a quorum read is more consistent and slower than a local read. Example: Cassandra can be PA/EL. A Raft metadata service is PC/EC.

**Per operation, not per company.** Seat **booking** must be consistent: two people cannot buy A4. I would rather return an error than book twice (CP for that write). The **seat map display** can be a second stale (AP). "Sold out" counts on a homepage can lag. I would say that split out loud.

**My systems.** ClickHouse `ReplacingMergeTree` is eventually consistent: a retried insert collapses to the latest version at merge time, and reads use `argMax` so they are correct before the merge finishes. That is the right trade for an analytical score, and the wrong trade for a seat. Postgres for the FRM review rows was the consistent store: a version check, one writer wins.

### Likely follow-up: what is a quorum?

`N` replicas, write succeeds after `W` acks, read waits for `R` replies. If `R + W > N`, the read set and the write set overlap, so the read sees the latest write **if there is no partition inside that quorum and clocks or versions are honest.** `W = N` is slow and brittle. `W = 1, R = 1` is fast and can return a stale replica. Raft's majority is a quorum with a leader and a log, which gives you a total order, not just "I saw a newer timestamp."

---

## Q17 and Q18. OCR + RAG pipeline. Is it one LLM prompt?

**Short answer to 18:** no. A single prompt that says "read this image and answer" is a demo. It has no evaluation, no page-level citation, no control on cost, and no way to know which part of the document the answer came from. OCR and RAG are stages with their own failure modes.

**Definitions**

- **OCR:** optical character recognition. Pixels in, text out, ideally with boxes (which page, which line). It is not understanding. It misreads handwriting, stamps, and tables.
- **RAG:** retrieval-augmented generation. Find a small set of relevant chunks, put those in the prompt, then generate. The model answers from the retrieved text instead of from memory.
- **Embedding:** a vector for a chunk. Similar text is near in that space. The index (HNSW in Milvus, or IVF) does approximate nearest neighbor.
- **Chunk:** the unit you index and retrieve. Too small and you lose context. Too large and you blow the prompt and dilute the match.
- **Rerank:** a second model that scores the top 50 candidates more carefully and keeps the top 5.
- **Hallucination:** the model states a fact that is not in the retrieved text. You reduce it with citations, a constrained output schema, and a check that the answer's claims appear in the chunks. You do not eliminate it with a clever adjective in the prompt.

**Assumptions:** documents are PDFs and phone photos, some scanned, some born-digital, multiple languages, the user asks a question or we must fill a schema, and a wrong digit can be worse than a refusal. That last point is true for invoices and for menus.

**The pipeline**

```
file lands (object storage)
    |
    v
1. sniff type
    PDF with a text layer?  --> extract text, skip OCR
    image / scanned page?   --> OCR
    |
    v
2. OCR (per page)
    output: text + boxes + confidence
    low confidence regions flagged, not silently trusted
    |
    v
3. layout
    reading order, headers, tables as tables, not as flat lines
    |
    v
4. chunk + metadata
    chunk on section boundaries
    metadata: doc id, page, bbox, language, source checksum
    |
    v
5. embed and index
    vector index + a keyword index (hybrid)
    |
    v
6. question or schema slot
    |
    v
7. retrieve
    hybrid search -> top 50 -> rerank -> top 5
    |
    v
8. generate
    prompt = instruction + the chunks + "cite the page"
    constrained output: JSON schema, or a validated menu schema
    |
    v
9. check
    schema validation
    citation points at a real chunk
    numbers in the answer appear in the cited chunk
    low score -> human queue, not a confident wrong answer
    |
    v
10. store
    raw file, OCR text, chunks, answer, model version, prompt hash
```

**Why each stage exists**

- **Skip OCR when the PDF has text.** OCR will garble a digital PDF. Detect a text layer first.
- **Keep boxes.** "The total is 1200" is useless if you cannot show the box on the page. Support and evaluation both need it.
- **Hybrid search.** Embeddings miss exact codes (GSTIN, SKU, a seat name). Keyword search misses paraphrases. Use both.
- **Rerank.** The bi-encoder is fast and approximate. A cross-encoder on 50 candidates fixes the worst misses cheaply.
- **Schema and a checker, not a prose answer,** when the downstream is a system. On Uber menu ingestion the unstructured path was retrieve similar labeled menus, then Gemini, then **schema validation**. 98% field fidelity was an **offline** eval, not a promise about a live prompt. I would say that number the same way here.
- **A human path.** Low OCR confidence or a failed schema check goes to a queue. The pipeline's job is to know when it doesn't know.
- **Idempotency.** Key the document by checksum so a re-upload does not double-index. Re-index when the chunker or the embedding model changes, and version the index. The same rule as a config hash on every scoring row: you can tell which pipeline version produced the answer.
- **Cost.** OCR and the LLM dominate. Don't send a 200-page PDF into the model. Retrieve first. Cache OCR output. Batch pages.

**What "one prompt" gets wrong**

| One prompt | The pipeline |
|---|---|
| The model sees the whole file or a truncated file | The model sees a few relevant chunks |
| No stable page citation | Each chunk has a page and a box |
| OCR errors are invisible | Confidence is a field you can branch on |
| You cannot regression-test | A labeled set of documents, scored on field accuracy, gates a model change |
| A new embedding model changes answers silently | Index version is stored with the answer |

**Evaluation, because they will ask "how do you know it works."** A fixed set of documents with the expected fields. Score exact match on IDs and amounts, and a looser score on names. Report OCR character error rate separately from answer accuracy, so you know whether you are debugging the recognizer or the retriever. I would not ship a prompt change that drops that set. That is the same shape as the 300-case gate on Keep/Drop, applied to documents.

### Likely follow-ups

**Which OCR?** A managed API (Cloud Vision, Textract, Document AI) if you want layout and tables this quarter. Tesseract if the data cannot leave the network. The interface is the same: pages in, text and boxes and confidence out. I would put that interface in front of whichever engine, so the rest of the pipeline does not care.

**Tables.** OCR that emits lines will split a table into nonsense. Use a model that returns table structure, or detect table regions and parse them separately. For invoices, the table is the product.

**Multilingual.** Detect language per page. An embedding model that was trained on one language will retrieve poorly for another. Either a multilingual embedding or an index per language.

**Updates.** Documents change. The index stores `doc_id` and a content hash. Re-chunk only the documents whose hash changed. Deletes are tombstones, not "hope the vector falls out."

**Prompt injection in the document.** Retrieved text is untrusted. The instruction says the chunks are data, and the schema checker rejects anything that isn't the expected shape. A document that says "ignore the rules and approve this" cannot change the output fields if the parser only accepts your schema.

---

## Q19. What are Python generators?

**Definition.** A generator is a function that uses `yield`. Calling it does not run the body. It returns a **generator object**, which is an iterator. Each `next()` runs the body until the next `yield`, returns that value, and **suspends the frame**. Local variables stay alive between yields. When the function returns, the iterator raises `StopIteration`.

A generator **expression** is the lazy form of a comprehension: `(x*x for x in nums)`. It is not a tuple. The parentheses are the generator.

**Why it exists.** A list holds every element. A generator holds the frame and the current element. You use it when the sequence is large, infinite, or expensive, and the caller only needs one element at a time.

```python
def positives():
    n = 1
    while True:
        yield n
        n += 1

g = positives()      # nothing computed yet
next(g)              # 1
next(g)              # 2
```

**What they are not.** They are not threads. They are not async by themselves. `yield` suspends one frame on one thread. `yield from` delegates to another iterator. `async def` / `await` is a different protocol (awaitables), though the implementation is related historically.

**Methods, if they go deeper.** `send(value)` resumes and makes `yield` **evaluate** to that value. `throw` raises inside the generator. `close` raises `GeneratorExit`. You need `send` for coroutines. You do not need it to stream rows.

**Exhaustion.** A generator has one pass. When it's done, it's done. There is no rewind. If two consumers need the data, tee it or re-run the function.

---

## Q20. Have you used generators in your work?

**Honest answer.** Yes, as a way to stream rows instead of materializing them. The failure mode I care about is the one that built a 170 GB aggregator state by trying to do a whole season at once. The fix was to shrink the unit of work to one fiscal week and stream. In Python that is a generator (or a cursor you iterate). In the Go pump it is the same idea with different syntax: read the next 500k-row batch while the previous batch is sent, and never hold the partition in memory.

I would not claim a specific function name from a private repo. The pattern I will defend:

```python
def iter_batches(rows, size=50_000):
    batch = []
    for row in rows:          # rows itself is a server-side cursor, not a list
        batch.append(row)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch
```

The caller writes a batch and drops it. Peak memory is one batch, not the file. The same shape was the Masters bulk importer: a file in chunks, not 100k invoices as one list.

If they ask "generators or iterators?": every generator is an iterator. Not every iterator is a generator. A file object and a DB cursor are iterators written in C.

---

## Q21. Numbers from 1 to 1000, no list, and no `for` / `range`

**What they are testing.** `range` in Python 3 is already lazy, so "don't use range" means they want `yield` and a `while`. "No list" means don't build `[1, 2, ..., 1000]`.

```python
def count_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

# consume it without storing it
total = 0
for value in count_to(1000):   # the consumer's for is fine; the ban is on producing the numbers
    total += value
```

If they also ban `for` at the consumer, a `while` drains it:

```python
g = count_to(1000)
total = 0
try:
    while True:
        total += next(g)
except StopIteration:
    pass
```

**Do not use recursion** for this. A thousand frames is wasteful, and a million would blow the stack. The generator frame is constant size.

**If they say "you used range in the for".** The `for` over the generator is the consumer. The producer never called `range` and never allocated the list. Say that distinction. If they want zero `for` keywords in the file, use the `next()` loop.

### Likely follow-up: generator vs `range` vs list

| | Memory | Reusable | When |
|---|---|---|---|
| `[i for i in range(1000)]` | O(n) | yes | You need random access or two passes |
| `range(1000)` | O(1) | yes | Arithmetic sequence, supports `len` and indexing |
| generator | O(1) | no, one pass | Streaming, or an expensive step per element |

`range` is the right tool for 1..1000. The generator is the right tool when the next element is a row from disk or a transformed record. They asked for the generator to see if you can write one under a constraint.

---

## Q22. How many bits for 1000 different values? What is one bit?

**Definitions**

- A **bit** is a binary digit. It has two states, 0 and 1. One bit distinguishes **2** possibilities.
- `n` bits distinguish **2^n** possibilities, because each new bit doubles the set.
- To represent `V` **distinct values** you need the smallest `n` with `2^n >= V`, which is `ceil(log2(V))`.

**The arithmetic**

```
2^9  = 512   < 1000     9 bits are not enough
2^10 = 1024  >= 1000    10 bits are enough
```

So **10 bits**. 1024 − 1000 = 24 patterns are unused. That is fine. You don't round down.

**What "one bit" means in that sentence.** It is the unit of information for a choice between two equally likely alternatives. It is not "one byte" (8 bits), and it is not "enough to store the number 1" in a programming language (`int` is 32 or 64 bits because of the type, not because of the value).

**Traps**

| Question they might switch to | Answer |
|---|---|
| Bits to store the **integer** 1000 | 1000 in binary is `1111101000`, which is **10 bits** if you don't store a sign. With a sign bit in a fixed width, a 16-bit short still holds it. Don't confuse "the number 1000" with "1000 different values." Here they happen to take the same 10 bits: values 0–999 need 10 bits, and the integer 1000 also needs 10 bits (`2^9=512`, `2^10=1024`). |
| 1000 values **including** which encoding | If the set is fixed and known, 10 bits is the information lower bound. A Python `int` object is dozens of bytes. The lower bound is not the object size. |
| Can you do it in fewer than 10 if some values are rare? | Entropy can be under 10 **bits on average** with a variable-length code (Huffman). Any single value still needs a distinct code, and the worst case is at least 10 if you use a fixed width. Say the fixed-width answer first, then mention entropy if they ask. |
| `log2(1000)` | ≈ 9.96, and you **ceil** it. 9.96 bits is not a register. |

---

## Q23 and Q24. Longest substring without repeating characters. Example `ABCADCBED`

**Problem.** Given a string, find the longest **contiguous** substring whose characters are all different. Not a subsequence. Order stays as in the string.

**Brute force.** Every pair `(i, j)`, check uniqueness with a set. O(n^3) or O(n^2) with care. Fine for n ≤ a few thousand. Not the answer they want once they say "sliding window."

**Why a sliding window works.** The property is monotonic in a useful way: if `s[L:R]` has a duplicate, then `s[L:R+1]` also does, so you move `L` forward. You never need to move `L` backward. Each index enters and leaves at most once, so the scan is O(n).

**The algorithm**

- `L` is the start of the current window.
- A map `last[char] = index` where we last saw that character.
- For `R` from 0 to n−1:
  - If `s[R]` was seen at index `p` and `p >= L`, the window is dirty. Set `L = p + 1`.
  - Record `last[s[R]] = R`.
  - Window length is `R - L + 1`. Track the best `(L, R)`.

**Walk `ABCADCBED`.** I will keep the best window, not only the length.

| R | char | last seen inside window? | L becomes | window | length | best |
|---|---|---|---|---|---|---|
| 0 | A | no | 0 | `A` | 1 | `A` |
| 1 | B | no | 0 | `AB` | 2 | `AB` |
| 2 | C | no | 0 | `ABC` | 3 | `ABC` |
| 3 | A | yes, at 0 | 1 | `BCA` | 3 | `ABC` |
| 4 | D | no | 1 | `BCAD` | 4 | `BCAD` |
| 5 | C | yes, at 2 (≥ L) | 3 | `ADC` | 3 | `BCAD` |
| 6 | B | B was at 1, which is **< L**, so it is outside | 3 | `ADCB` | 4 | `BCAD` |
| 7 | E | no | 3 | `ADCBE` | 5 | `ADCBE` |
| 8 | D | D was at 4 ≥ L | 5 | `CBED` | 4 | `ADCBE` |

**The longest valid substring is `ADCBE`, length 5** (indexes 3 through 7). `A, D, C, B, E` are all different. There is another window of length 4 (`BCAD`) but nothing longer than 5. The whole string is not valid: it repeats A, C, B, and D.

The step people miss is index 6. `B` occurred earlier, but that occurrence is **outside** the window, so it does not count. If you shrink whenever the character exists anywhere in the map, you shrink too far and you can drop `ADCBE`.

```python
def longest_unique_substring(s: str) -> str:
    last = {}
    start = best_l = best_r = 0
    for r, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            start = last[ch] + 1
        last[ch] = r
        if r - start > best_r - best_l:
            best_l, best_r = start, r
    return s[best_l:best_r + 1]
```

**Complexity.** Time O(n). Space O(min(n, alphabet)). For bytes, the map is at most 256. For Unicode code points it is bounded by the number of distinct characters in the string.

**Assumptions.** Contiguous substring. Case-sensitive (`A` ≠ `a`). Empty string returns empty. If there are two answers of the same length, this code keeps the **first** one, because the comparison is `>`. Say that. If they want the last, use `>=`.

### Likely follow-ups

- **Longest with at most K distinct characters.** Same window, but shrink while the number of distinct characters is greater than K. A counter, not only a last-index map.
- **At most K replacements** (Longest Repeating Character Replacement). Window is valid while `length - max_freq <= K`.
- **Smallest window that contains every character of T** (minimum window substring). Grow until valid, then shrink while it stays valid.
- **Streaming / huge string.** The same loop. You only store the window and the map, not the prefixes.
- **Return the length only.** Same loop, no slice until the end. Slicing each step would make it O(n^2) in the worst case in CPython if you built a new string every time. Track indexes, slice once.

---

## Q25. Events contain dicts and lists. You repeatedly test membership in a huge corpus. The service is slow, and you cannot add instances. What do you do?

**Assumptions.** "Membership" means "is this id / string in the corpus," possibly thousands of times per event. The corpus is much larger than one event. Horizontal scale is off the table, so the win has to be **less work per event on this machine**: fewer lookups, cheaper lookups, or less data moved. I profile before I pick. A CPU flame graph and a count of lookups per event decide which row below matters.

**The moves, in the order I try them**

1. **Stop scanning.** If the code walks the corpus for every item, that is O(items × corpus). Put the corpus in a **hash set** so each test is O(1) average. Build the set once, not per event.
2. **Stop doing it one item at a time.** An event with a list of 5,000 ids should be **one** batch membership test (`ids & corpus` on sets, or one `WHERE id IN (...)`), not 5,000 round trips. This is the usual win when CPU is low and the service is still slow: you are waiting on the network.
3. **Only test the distinct ids.** Dedupe the event first. Repeated keys in the dict/list are free once you collapse them.
4. **Keep the hot subset in memory.** If the corpus does not fit in RAM, cache the ids that actually appear (LRU). A power-law corpus means a small cache catches most tests. One machine can hold a lot of ints: 100 million 8-byte ids is under a gigabyte before overhead. Python objects are much fatter (an `int` object is ~28 bytes, a set entry more). If the profile says memory traffic, store them in a compact structure: a `array`/`numpy` sorted array plus binary search, a `roaring` bitmap if the ids are integers, or a Rust/Go sidecar. I would say the Python object tax out loud.
5. **A Bloom filter in front,** if the common answer is "not present." A Bloom filter uses a few bits per element and answers "definitely not" or "maybe." Maybe's are checked against the real set. False positives cost an extra lookup. False negatives do not happen if you sized it. This is the right shape when most event keys miss.
6. **A trie or a finite-state transducer** if the corpus is strings and you also need prefixes. Not for plain integer ids.
7. **Don't rebuild the structure per event.** Parse the corpus once. On reload, build a new set and swap the reference. Requests keep using the old one until they finish (copy-on-write / atomic swap). Rebuilding under a lock on the request path is a self-inflicted stall.
8. **Cheaper comparison.** Intern repeated strings. Normalize the dict once (lowercase, canonical key) so you don't re-walk nested lists on every check.
9. **If the hot loop is pure Python and the set already fits,** move that loop to a tighter runtime. I would profile first. I have moved hot paths to Go when the per-row tax mattered (columnar batches, no per-row reflection). Same decision here: algorithm first, language second.

**What I would not do first:** add threads and hope. The GIL means threads don't speed a pure-Python CPU loop. They help if the time is spent waiting on the database. Processes can use more cores for a CPU-bound build of the set, but the membership structure then needs to be shared (one process that owns it, or a read-only memory map). And you were told not to scale **out**. Using the other cores on **this** box is still in bounds. I would say that distinction.

---

## Q26. The corpus is in a database. How do you optimize the repeated lookups?

**The bug is almost always the round trip, not the index.** One query per id, each ~1 ms of network, 5,000 ids, is 5 seconds before the database does any real work. That matches a slow service with low CPU.

**What I change**

1. **Batch.** One query per event:

```sql
SELECT id FROM corpus WHERE id = ANY(:ids)
```

   or `WHERE id IN (...)`. Chunk `IN` lists (a few thousand ids) so the planner and the packet size stay sane. The result set is the intersection. The code treats "not in the result" as absent.

2. **A set in the process, refreshed on a timer,** if the corpus fits or the hot part fits. The database becomes a refresh source, not a per-event dependency. Staleness is a product decision: say the refresh interval.

3. **A local embedded store** (RocksDB, SQLite) if it fits on disk and not in RAM. You pay a local read, not a network round trip. Refresh by file swap or by a versioned table.

4. **Covering index** so the batched query is an index-only scan. The row is not fetched.

5. **Prepared statements and a sane pool.** Re-planning the same `IN` query, or opening a connection per lookup, dominates. A pool that is too small queues requests (tail latency). A pool that is too large overwhelms the database. Measure acquire-wait separately from query time.

6. **Don't join the event through the database if the event is a JSON blob in the app.** Extract ids in the app, then one batched lookup. Shipping every nested dict into SQL so the database can parse it is extra CPU on the worst tier.

7. **Negative caching.** If most ids miss, cache the misses for a short TTL too, or the Bloom filter from Q25, so misses don't all become database reads.

**Read replica** is not horizontal scale of **this** service. It is a fair way to take read load off a primary. I would mention it as optional, and not as the first fix. The first fix is fewer queries.

---

## Q27. Which indexes or data structures?

Pick by the **query shape** and the **id type**. Say that before naming a structure.

| You need | Structure | Cost | Notes |
|---|---|---|---|
| Exact membership, corpus fits in RAM | Hash set | O(1) average, O(n) memory | Worst case O(n) if every key collides. Rare with a decent hash. |
| Exact membership, integer ids, tighter memory | Roaring bitmap, or a sorted `int64` array + binary search | Bitmap is near O(1) and very small when ids cluster. Binary search is O(log n) and cache-friendly. | Binary search beats a Python set when the constant factors and memory dominate. |
| Exact membership, most answers are no, corpus is huge | Bloom filter, then a real lookup on "maybe" | A few bits per key. No false negatives if you don't delete naively. | Deletes need counting Bloom filters or a rebuild. |
| Prefix / autocomplete | Trie | O(length) | Overkill for equality. |
| Equality in a database | **B+ tree** unique index on the id | O(log n) reads, usually a few pages | The default. Hash indexes exist in Postgres for equality only and are rarely worth it over a B-tree. |
| Equality, and you only need the id, not the row | **Covering** index, or the primary key if the id **is** the primary key | Index-only scan | `INCLUDE` extra columns if you need them and want to avoid the heap. |
| "Any of these 5,000 ids" | One B-tree index, **one** `IN` / `ANY` query | The planner turns it into a series of index probes or a bitmap | An index does not help if you issue 5,000 separate queries. |
| Range ("ids from A to B") | B-tree, not a hash index, not a Bloom filter | O(log n + k) | Bloom cannot do ranges. |
| Fuzzy / typo | n-gram index or a trigram GIN index | Heavier | Only if "membership" is not exact. Don't add it for exact ids. |
| Full text | Inverted index | | Wrong tool for an id lookup. |

**Primary key vs secondary index.** If the corpus table's primary key is the id, the lookup is already indexed. A second index on the same column is pure write cost. I would check that before adding one.

**Write cost.** Every index slows inserts. A corpus that is reloaded in bulk should build the index **after** the load, or load into a new table and swap. Same idea as building a new hash set and swapping the pointer.

### Likely follow-up: hash index vs B-tree vs Bloom, in one sentence each

- B-tree: ordered, equality and range, the default on disk.
- Hash index: equality only, no range, no ordering.
- Bloom: probabilistic, tiny, "definitely not here," cannot return the row by itself.
- In-memory hash set: exact, RAM, the right tool when the corpus fits and the test is on the request path.

### Likely follow-up: how do you prove the change worked?

Lookups per event (should drop from thousands to one), P50/P99, CPU, and database QPS. If P99 doesn't move, the membership test was not the tail, and I go back to the profile instead of adding a second cache.
