# GeeksforGeeks — Platform Backend (Java / Spring track)

**Role:** Software Development Engineer · August 2021 – November 2022 · Noida  
**Resume tech:** Java, Spring Boot, Spring MVC, Hibernate, MySQL, Redis, REST, Cron, AWS

---

## 1. Elevator pitch

"First job out of college. I worked on GeeksforGeeks' community and courses backend: migrated the community product from legacy PHP to Spring Boot serving 100K+ daily queries, and built data models and REST APIs for voting and pinning that lifted premium subscription sales 15–20%."

## 2. What to defend

- **PHP → Spring Boot:** re-modeled posts, comments, votes, pins, reports into normalized MySQL with Hibernate entities; REST controllers for web + app clients; Redis on hot feeds/counters.
- **Engagement features:** denormalized counters updated transactionally + periodic reconciliation cron — explain consistency tradeoff.
- **Cron:** video-processing triggers, reminders, cleanup — idempotent jobs with alerting.

## 3. Q&A

- **"100K daily queries — how fast?"** Redis for feeds/counters; avoid N+1 (`JOIN FETCH` / entity graphs); composite indexes; slow-query review.
- **"Junior framing?"** "Owned features end-to-end within a mentored team" — calibrate claims.
- **"Spring MVC vs Boot?"** Boot is the packaging; MVC is the web stack — we used Boot starters for MVC + Data JPA + Redis.
