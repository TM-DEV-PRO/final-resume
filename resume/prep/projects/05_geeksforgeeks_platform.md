# GeeksforGeeks — Community & Courses Platform Backend

**Role:** Software Development Engineer · August 2021 – November 2022 · Noida
**Resume tech line:** Python, Django, MySQL, Redis, REST, Cron, AWS

---

## 1. Elevator pitch

"First job out of college. I worked on GeeksforGeeks' community and courses backend: migrated the community product from legacy PHP to Django serving 100K+ daily queries, built the data models and REST APIs for engagement features like voting and pinning that lifted premium subscription sales 15–20%, and built an influencer analytics dashboard that boosted course sales ~30%."

## 2. What to defend

- **PHP → Django migration:** re-modeled the community domain (posts, comments, votes, pins, reports) into normalized MySQL with Django ORM; API-first (DRF) so web + app clients share endpoints; Redis caching on hot read paths (feeds, counts).
- **Engagement features:** vote/pin data models designed for cheap aggregation (denormalized counters updated transactionally + periodic reconciliation cron) — the classic counter-consistency tradeoff; explain why exact-at-read counting doesn't scale and how reconciliation bounds drift.
- **Influencer dashboard:** attribution of course purchases to referral codes/links, near-real-time rollups; automated what was previously a manual monthly spreadsheet process.
- **Cron orchestration:** video-processing pipeline (transcode triggers, upload verification), automated class reminders, cloud-recording cleanup (storage cost) — raised ops efficiency ~70%.

## 3. Q&A

- **"100K daily queries — how did you keep it fast?"** Redis for hot feeds and counters, `select_related`/`prefetch_related` to kill N+1s, slow-query log review, composite indexes on (thread, created_at).
- **"What did you learn here that you still use?"** Denormalize deliberately and reconcile; measure before optimizing; cron jobs need idempotency and alerting just like services.
- **Junior-role framing:** own it as scope-appropriate — "I owned features end-to-end within a mentored team" — interviewers respect calibrated claims for a first job.
