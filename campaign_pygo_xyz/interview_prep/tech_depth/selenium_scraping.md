# Selenium + anti-bot scraping

## What
Browser automation for Uber Eats menu ingestion on GCP.

## How used here
Cut onboarding 24h→2h saved $600K+/yr on 30K+ menus/month. Raised successful ingestions to 95%+ via IP rotation dynamic proxies adaptive backoff. Pairs with RAG/Gemini extraction.

## Tradeoffs
Scraper fragility vs incomplete partner APIs. Need monitoring and rapid selector fixes.

## Failure modes
- DOM changes
- Bot detection
- Proxy pool exhaustion

## Likely questions
How do you detect breakage? Ethical/legal constraints? Why not only APIs? How does backoff work?
