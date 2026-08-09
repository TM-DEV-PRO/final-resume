# Selenium + anti-bot scraping

## What
Browser automation for Uber Eats menu ingestion on GCP.

## How used here
Owned Eats menu ingestion end to end: Selenium → Kafka → Flink cuts onboarding 24h→2h / $600K+/yr at 30K+ menus/month. Raised successful menu ingestions to 95%+ with IP rotation, dynamic proxy pools, adaptive retries. Pairs with LangChain RAG + Gemini + Milvus schema-gated extraction.

## Tradeoffs
Scraper fragility vs incomplete partner APIs. Need monitoring and rapid selector fixes.

## Failure modes
- DOM changes
- Bot detection
- Proxy pool exhaustion

## Likely questions
How do you detect breakage? Ethical/legal constraints? Why not only APIs? How does backoff work?
