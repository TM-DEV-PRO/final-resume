# Uber Menu Ingestion (Java track note)

**Resume tech (matches the PDF Tech line exactly):** Python, Selenium, Kafka, Flink, LangChain, Gemini, RAG, Milvus, GCP, Docker

**Not on the PDF — do not claim:** Spark and SFT/fine-tuning. Spark backfills are study-only depth; the extraction path is RAG over Milvus embeddings into Gemini, not a fine-tuned model.

**No Spring claim.** Same stack as v2.

> Full defense: `../../resume_v2/prep/14_uber_menu_deep_dive.md`.

## Elevator pitch

"Uber Eats menu onboarding used Selenium scrapers on GCP publishing into Kafka (~200–500 peak events/sec estimated during fleet runs). Flink normalized, deduped, and routed online; Spark handled backfills and reprocess windows. RAG + Gemini covered PDF/image menus. Onboarding fell from 24h to 2h at 30K+ menus/month. Killing a ~$2/menu tool saved $600K+/yr ($720K list). Offline eval hit 98% fidelity and 100% schema consistency."

## Why Flink + Spark here (not Masters / IA)

Menu has bursty scrape ingress and both online freshness and historical rewrite shapes. Masters already claims Kafka for e-invoice. IA is ClickHouse POC.

## Money math

| Step | Number |
|---|---|
| Unit cost | ~$2 / menu |
| Volume | 30,000+ / month |
| Annual list | $720,000 |
| Resume | **$600K+** floor |
