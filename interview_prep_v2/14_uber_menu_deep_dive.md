# Uber Menu Ingestion Deep Dive (v2 resume defense)

Numbers match `GROUND_TRUTH.md` and `09_metrics_derivations.md`. Rates tagged ESTIMATED where derived.

> **RESUME ALIGNMENT (Jul 2026, mandatory):** Kafka, Flink, Spark, and Pinot were deliberately REMOVED from the Menu Ingestion resume bullets. The 4yr resume is the source of truth: **Python + Selenium + GCP scraping**, RAG + Gemini 2.5 Pro + SFT extraction, IP rotation / dynamic proxy pools, and ANZ compliance automation (99.9%, 20h/week). Do NOT say you built or owned a Kafka/Flink/Spark/Pinot pipeline at Uber Menu. Kafka stays on the skills line because of Masters India (`AsyncIOKafka` messaging on the 2.5yr resume). If an interviewer asks about streaming at Uber, redirect: "Menu work was Selenium on GCP; my Kafka production experience is Masters India e-invoicing."

---

## What the system does

Uber Eats onboards restaurant menus from partner-authorized third-party platforms and unstructured PDFs/images into the catalog. A Python fleet on GCP drives Selenium scrapers through proxy pools, persists raw and normalized menu payloads, and routes messy PDFs/images through a RAG plus Gemini 2.5 Pro path with supervised fine tuning and schema validation. A separate Python automation track keeps ANZ driver and vehicle documents compliant. Success criteria: time to onboard, ingestion success rate, extraction fidelity, and ops hours saved on compliance.

---

## Bullet defenses

### 1. Python + Selenium + GCP, 30K menus/month, 24h to 2h, $600K+/yr

**Stack (HISTORICAL, 4yr resume).** Python workers on GCP run Selenium against JS-heavy vendor sites, write structured catalogs, and retry with proxy rotation. Not a streaming platform claim.

**Impact.** Onboarding 24h to 2h (90%). Eliminated a $2 per menu third-party tool at 30K menus/month = $600K+/yr (HISTORICAL arithmetic: 30K x $2 x 12 = $720K list; resume says $600K+).

### 2. RAG + Gemini, 98% fidelity, 100% schema consistency

Unstructured PDFs and images defeat rule-based parsers. Pipeline: chunk menu, retrieve similar labeled menus, generate structured items with Gemini, validate against schema (prices, currency, locale), low confidence goes to human review. SFT enforces schema. 98% fidelity and 100% schema consistency are offline/eval numbers. Say that.

### 3. +95% success (about 60% to 95%+), anti-bot

Anti bot: IP rotation, user agent spoofing, dynamic proxy pools, per source retry budgets. Baseline from about 60 to 65% to 95%+ (baseline ESTIMATED).

### 4. ANZ compliance 99.9%, 20h/week saved

Python automation checks driver and vehicle document freshness against local authority rules for Uber earners in ANZ. 99.9% compliance and 20 hours/week of manual verification saved (HISTORICAL, 4yr resume).

---

## End to end flow (resume-aligned)

```
Partner-authorized vendor sites / PDF+image menus
        |
        v
Selenium scrapers on GCP (proxy pool, UA rotation, retries)
        |
        +--> Structured catalog upsert (idempotent by vendor+menu version)
        |
        +--> RAG + Gemini 2.5 Pro + SFT --> Pydantic/JSON schema validate
        |         |
        |         +--> human review on low confidence
        |
        +--> ANZ document compliance automation (separate track)
```

---

## Rapid fire (Menu stack only)

- Why Selenium not requests+BS4? Vendor pages are JS-rendered SPAs; HTML fetch returns empty shells.
- Why not Playwright? Existing Uber/EPAM Selenium grid and fleet already ran; rewrites were risk without measured flake wins. Acknowledge Playwright is often better for greenfield.
- Ethics of scraping? Partner-authorized catalog sync under Uber partnership agreements, not open-web scraping.
- What breaks at 10x? Proxy pool capacity and per-source rate limits first.
- How is 98% fidelity measured? Offline labeled eval set (item name, price, category match), not live A/B.
- What is 100% schema consistency? Every accepted payload passes Pydantic/JSON Schema before catalog write.

---

## Streaming context (DO NOT CLAIM ON RESUME)

Background only if an interviewer asks how Uber typically wires scrapers into catalog systems. Do not present this as your Menu ownership. For Kafka experience, use Masters India.

```
Scrapers --> (platform bus) --> normalize/dedup --> catalog
                          \--> health dashboards / backfills
```

If pressed on personal streaming work: "I did not own Kafka/Flink on Menu. My production Kafka is AsyncIOKafka at Masters India for e-invoice fan-out and replay."

## Mock interview: hardest questions with answers

**Interviewer:** You claim Selenium on GCP for 30K menus a month. Why not Playwright, and why not plain `requests` plus BeautifulSoup?

**Candidate:** Vendor menu pages were JS-heavy SPAs. A bare HTTP GET returned an empty shell, so BeautifulSoup alone could not see items or prices. Selenium was already the paved path in the Uber/EPAM automation fleet: shared grids, Chrome drivers, and ops runbooks. Playwright is often better for greenfield (auto-wait, lightweight contexts, native network interception), and I would pick it for a new scraper today. Rewriting a working fleet mid-onboarding would have burned weeks for unproven flake gains. So the choice was existing infra plus real browser rendering, not ideology.

**Interviewer:** Scraping at Uber sounds legally risky. How do you defend IP rotation and proxy pools without sounding like a bot farm?

**Candidate:** This was partner-authorized catalog sync under Uber Eats partnership agreements, not open-web scraping of random restaurants. Proxies and IP rotation existed because partner platforms still run anti-bot defenses that throttle datacenter IPs even for legitimate integrations. The pool rotated exit IPs, stuck sessions per vendor when needed, and backed off on 403/429 with per-source budgets. Ethics line I say out loud: we only hit sources we were contracted to ingest, logged every run, and respected rate limits we negotiated. Anti-bot work raised successful ingestions about 95% relative (HISTORICAL), from a rough 60 to 65% baseline (ESTIMATED) to 95%+.

**Interviewer:** Walk the $600K savings math. I will poke holes if the arithmetic is soft.

**Candidate:** Third-party menu tool cost was about $2 per menu. At 30K+ menus per month that is 30,000 x $2 = $60,000 per month, or $720,000 per year list. Resume says $600K+ annually, which is the conservative floor after volume mix and partial cutover months. Onboarding time fell from 24 hours to 2 hours (90%) because scrapers plus extraction replaced a slow manual or vendor-tool loop. Numbers are HISTORICAL from the 4yr resume; I do not invent a different unit cost.

**Interviewer:** Why Gemini 2.5 Pro with supervised fine tuning instead of prompt-only extraction?

**Candidate:** Prompt-only drifted on layout variants: multi-column PDFs, handwritten specials, mixed currencies, and image-only menus. RAG pulled similar labeled menus so the model saw the right shape before generating. SFT on schema-shaped examples forced field names, types, and required keys so the model stopped inventing columns. Prompt-only might hit high fidelity on easy PDFs and still fail schema validation; SFT is what pushed accepted outputs to 100% schema consistency on the eval set. Cost and latency of Gemini mattered less than catalog write failures from malformed JSON.

**Interviewer:** Define 98% fidelity and 100% schema consistency precisely. How were they measured?

**Candidate:** Schema consistency means every accepted payload passes Pydantic or JSON Schema validation before catalog write: required fields present, types correct, currency codes valid, price non-negative. That gate is binary, so we report 100% for accepted rows; rejects go to human review and do not count as consistent writes. Fidelity is offline eval against a labeled set: item name, price, and category matched within defined tolerances, about 98% on that set. I say offline eval out loud so nobody hears it as a live A/B or production SLA. Live traffic still has a review queue for low-confidence cases.

**Interviewer:** How does dynamic proxy pool rotation actually work at fleet scale?

**Candidate:** Workers pull a proxy lease from a pool service keyed by source and geography. Sticky leases keep one exit IP for a short vendor session so login or pagination cookies stay valid. On hard blocks we release the lease, mark the IP cool-down, and retry with a different residential or partner IP. User-agent rotation and human-like pacing sit on top. The failure mode at 10x is pool exhaustion and source rate limits, not CPU on the scraper box.

**Interviewer:** Why is Kafka missing from your Menu bullets when older prep talked about Flink and Pinot?

**Candidate:** Deliberate resume correction. The 4yr resume documents Python, Selenium, and GCP for Menu, not a streaming platform I owned. Kafka, Flink, Spark, and Pinot were removed so the bullets match what I can defend. If you want Kafka production experience, Masters India used AsyncIOKafka for e-invoice messaging with ordering and replay. I will not claim I built Uber's Menu bus.

**Interviewer:** ANZ compliance to 99.9% and 20 hours a week saved. What did the automation actually check?

**Candidate:** Python jobs validated driver and vehicle document status against local authority rules for Uber earners in Australia and New Zealand: expiry, document type presence, and mismatch flags. Failures opened ops queues; successes auto-cleared. 99.9% compliance is the measured clear rate after automation (HISTORICAL). Manual verification dropped about 20 hours per week because humans only touched exceptions. I do not claim I wrote the government systems; I owned the Uber-side automation and reporting.

**Interviewer:** RAG retrieval for menus: what is indexed, and what happens on a retrieval miss?

**Candidate:** We embedded chunked labeled menus and catalog exemplars (cuisine, layout family, locale) in a vector store. At inference we retrieved nearest neighbors, stuffed them into the Gemini context, then generated structured items. On miss or low similarity we fell back to a stricter prompt, raised the confidence threshold, and routed more rows to human review instead of writing garbage. Retrieval quality mattered as much as the generator for fidelity.

**Interviewer:** Idempotent catalog writes: how do you avoid double-ingesting the same vendor menu during retries?

**Candidate:** Upsert key is vendor id plus menu version or content hash of the normalized item set. Scrapers retry freely; the write path is idempotent. Partial failures mark a run checkpoint so the next attempt resumes without duplicating already-written items. That pattern is what made aggressive proxy retries safe at 30K menus per month.

**Interviewer:** If Playwright is better today, what would you change in a redesign without rewriting everything?

**Candidate:** Pilot Playwright on the flakiest JS sources first, keep Selenium on stable sources, share the same proxy lease API and idempotent upsert contract. Measure flake rate, wall-clock per menu, and proxy burn before a fleet cutover. Greenfield preference for Playwright does not erase that Selenium plus proxies already delivered the 24h to 2h and $600K+ outcomes.

## Confidence audit

| Resume bullet | Rating | Fallback wording if pressed |
|---|---|---|
| Python + Selenium + GCP, 30K+ menus/month, 24h to 2h, $600K+/yr | SOLID | Keep $2/menu and 30K/month arithmetic; say "$600K+ after partial cutover" if they want exact finance sign-off. |
| RAG + Gemini 2.5 Pro + SFT, 98% fidelity, 100% schema consistency | NEEDS CARE | Always say "offline eval / accepted payloads." Fallback: "about 98% item match on a labeled set; 100% of writes that pass schema validation." |
| IP rotation + proxy pools, +95% successful ingestions | NEEDS CARE | +95% is relative lift (HISTORICAL); baseline ~60-65% is ESTIMATED. Fallback: "roughly doubled successful ingestions once proxies and rotation stabilized." |
| ANZ compliance 99.9%, 20h/week saved | SOLID | Stick to automation of document checks and exception queues; do not invent regulator API details. |
