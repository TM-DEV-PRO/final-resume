# Uber Menu Ingestion (Java track note)

**Resume tech:** Python, Selenium, Gemini, RAG, SFT, GCP, Docker  
**No Spring / Kafka / Flink / Spark / Pinot claim on this project.**

> Same facts as `../interview_prep_v2/14_uber_menu_deep_dive.md`. Menu stays Python on the Java resume.

## Elevator pitch

"Uber Eats onboarding from partner-authorized vendor sites was slow and expensive. I built a Python + Selenium ingestion fleet on GCP with proxy rotation, plus a RAG + Gemini 2.5 Pro extraction path for PDFs and images. Onboarding fell from 24 hours to about 2 hours at 30K+ menus/month. Killing a roughly $2/menu third-party tool saved $600K+ a year (30K × $2 × 12 = $720K list; resume floors at $600K+). Offline eval hit 98% fidelity and 100% schema consistency. Separately, ANZ driver document automation reached 99.9% compliance and saved about 20 hours/week."

## Spark / Flink decision

Deliberately **not** on the resume. Earlier drafts overclaimed a streaming platform. The 4yr resume source of truth is scraping + extraction. Kafka production depth for interviews is **Masters India**, not Menu. Study-only Spark/Flink material: `../interview_prep_v2/17_senior_systems_study_only.md`.

## Money math

| Step | Number |
|---|---|
| Third-party unit cost | ~$2 / menu |
| Volume | 30,000+ menus / month |
| Monthly list | $60,000 |
| Annual list | $720,000 |
| Resume claim | **$600K+** (conservative floor) |

## Q&A

- **"Why no Kafka here?"** Menu was Selenium on GCP. My Kafka ownership is Masters India e-invoicing.
- **"Is $600K finance-signed?"** HISTORICAL resume arithmetic from unit cost × volume; use the conservative floor and show $720K list if pressed.
