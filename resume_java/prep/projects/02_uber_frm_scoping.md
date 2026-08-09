# Uber (via EPAM) — FRM Scoping Platform (Java / Spring track)

**Role:** Software Development Engineer 2 · July 2024 – May 2026 · Bangalore  
**Resume tech:** Java, Spring Boot, Spring Data JPA, Hibernate, MySQL, JUnit, Docker

> Same domain and metrics as `../../resume_v2/prep/11_uber_frm_deep_dive.md`. Stack reframed to Spring Boot + JPA/Hibernate. Live implementation is FastAPI + SQLAlchemy 2.0; say that if pressed.

---

## 1. Elevator pitch

"I owned Uber's Financial Risk Management quarterly scoping backend — the system that decides which financial statement line items get audited each quarter. It replaced a Google Sheets workflow with a Spring-framed service used by FRM managers; the output feeds PwC audit work papers. Across 8 screens and 30+ REST APIs, at $340M group materiality, we targeted a 70% cut in manual reconciliation (~2 weeks to ~3-4 days ESTIMATED baseline; 70% is a TDD target). I designed the layered architecture on an 11-table MySQL schema, owned the Sheets-to-MySQL v2 recon migration (18 files), and led 3 engineers through design reviews and CI gates."

## 2. Architecture (Java telling)

```
React SPA
    │ REST
    ▼
frm-scoping-service
(controllers → services → Spring Data JPA repos)
    │
    ▼
MySQL (11 ORM models in the scoping service)
    ▲
    │ HFM extracts loaded by shared ETL (do not claim sole ETL ownership)
Oracle HFM
```

**Layering (strict):** `controller` → `service` → `repository` (Spring Data JPA) → entities. Controllers never touch repositories; services never throw raw HTTP exceptions without an `@ControllerAdvice`; repositories never compute business rules.

## 3. Resume bullets to defend

1. Owned platform across 8 screens / 30+ APIs, $340M materiality, targeting 70% cut.
2. Designed software architecture: 11-table MySQL on Spring Data JPA/Hibernate with controller/service/repository boundaries; auto-flag material items across 55 line items and 14 entities.
3. Owned Sheets to MySQL v2 recon migration (18 files); 10-Q validation; column-aliasing bug fix.
4. Led 3 engineers: design reviews, API contracts, CI quality gates.

## 4. Honesty guardrails

- Do **not** say 36 endpoints (code truth ~32 routes including health = 30+).
- Do **not** say 19M GL rows to 300K (UNSUPPORTED; dropped).
- 70% is a **TARGET**, not a measured cut.
- Map Spring vocabulary honestly: real code is Python/FastAPI/SQLAlchemy; architecture boundaries are the transferable claim.

## 5. Q&A

- **"Why JPA over jOOQ/MyBatis?"** Refactor safety and team velocity on a CRUD-heavy domain; complex aggregates stay explicit queries with labeled projections.
- **"N+1?"** `JOIN FETCH` / `@EntityGraph` / batch size; never leave lazy loads in hot request paths.
- **"What did ownership mean?"** I owned the recon v2 cutover plan, layer conventions, and review bar for the pod.
