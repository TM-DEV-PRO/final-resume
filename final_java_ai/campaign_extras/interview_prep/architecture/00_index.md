# Architecture index (Final Java + AI)

<div class="callout note">
<b>How to use this page</b>
<ul>
<li><b>What it covers:</b> one architecture page per resume project, each built the same way so you can compare them side by side.</li>
<li><b>When to read it:</b> before any system design round or any "walk me through the architecture of X" question. Read the project page, then practise the 3-minute whiteboard script at the bottom of it out loud.</li>
<li><b>What to memorise:</b> for each project, the diagram (five to eight boxes), one request traced end to end, and the two or three numbers tied to that diagram.</li>
</ul>
</div>

**This track.** Resume PDF: `Tarun_Mittal_SSE_5yr_Java_AI.pdf`. Summary line: "Expertise in Java and Python microservices". Uber FRM and Masters India run on Java and Spring Boot. Impact Analytics is Go/Gin plus Python agents. Uber Menu is Python. GeeksforGeeks is Django.

## What every architecture page contains

Each page below follows the same template. That way, once you have learned one, the others are easy to read, and in an interview you can answer any "draw it" question with the same rhythm.

1. **The one-paragraph version.** What the system is, who uses it, and what problem it solves, in plain English.
2. **Words you need.** Every technical term used on the page, defined in one or two sentences with an everyday analogy.
3. **The diagram.** A mermaid flowchart with a one-line caption saying what to notice.
4. **Box-by-box walkthrough.** Each box in the diagram explained: what it is, why it exists, and what technology sits there and why.
5. **One request or one job, step by step.** A concrete example with real-looking sample data so the flow is not abstract.
6. **Design decisions.** For each big choice: what, why, alternatives and why not, the trade-off, and what I would do differently.
7. **Numbers on this diagram.** What each number measures, how it was derived, and how to say it out loud.
8. **Failure modes.** What breaks, how you notice, and what the system does about it.
9. **Say this, not that.** The honesty box.
10. **How to draw it in 3 minutes.** What to draw first, second and third, and what to say while drawing.

## Honesty tags used on every page

Some numbers carry a tag. The tags mean:

- **MEASURED** means there is a log, a document or code that shows the number.
- **ESTIMATED** means it is arithmetic I can show on a whiteboard. Say "roughly, derived from...".
- **TARGET** means a design goal, not a result. Say "targeting".
- **HISTORICAL** means it comes from my past work records and was not re-measured for this prep.

## The project pages

| Project | What the system does | Page |
|---|---|---|
| Impact Analytics, AssortSmart (Platform and AI) | Retail assortment planning SaaS: Go/Gin platform on ClickHouse plus a Python agent plane for Keep/Drop decisions and the Ask Iris copilot. Hindsight is described separately as verbal-only depth. | [01_ia_assortsmart_hindsight.md](01_ia_assortsmart_hindsight.md) |
| Uber via EPAM, FRM Scoping Platform | Finance tool that replaced a Google Sheets quarterly close with a Java Spring Boot and MySQL system of record. | [02_uber_frm.md](02_uber_frm.md) |
| Uber via EPAM, Menu Ingestion (Uber Eats) | Scrapes and extracts restaurant menus, streams them through Kafka and Flink, and uses Gemini with RAG for unstructured PDFs. | [03_uber_menu.md](03_uber_menu.md) |
| Masters India, GST e-invoicing | Registers Indian business invoices with the government portal at high volume, after moving a PHP monolith to Spring Boot microservices. | [04_masters_gst.md](04_masters_gst.md) |
| GeeksforGeeks, doubt support and dashboards | Django backend for a coding Q&A platform plus an influencer earnings dashboard and scheduled workflows. | [05_geeksforgeeks.md](05_geeksforgeeks.md) |

## Rules that apply across all five diagrams

Interviewers sometimes try to merge projects. These separations keep you honest.

- **Kafka and Flink live on Uber Menu.** Kafka also appears at Masters India, but it is a different product with different reasons. Neither Kafka nor Flink appears on Impact Analytics.
- **Milvus (a vector database) is Uber Menu only.** Impact Analytics has no vector database on the resume.
- **ClickHouse is Impact Analytics only.** Menu used Kafka and Flink, not ClickHouse.
- **Impact Analytics APIs are Go with the Gin framework.** The agent side is Python (FastAPI and LangGraph). Spring Boot is Uber FRM and Masters India only, never Impact Analytics.
- **No Kubernetes cluster operations claims anywhere.** Kubernetes is skills-level literacy.
- **"Led 3 engineers" is Uber FRM. "Mentored 2 engineers" is Masters India.** Do not add them together.
- **Uber is always "Uber via EPAM".**

## Related reading

- Design trade-offs across projects: [../design_decisions_tradeoffs.md](../design_decisions_tradeoffs.md)
- Every resume number with its derivation: [../numbers_defense.md](../numbers_defense.md)
- Technology deep dives: [../tech_depth/00_index.md](../tech_depth/00_index.md)
- Deployment and scale notes: [../deployment_and_scale.md](../deployment_and_scale.md)
- Project interview packs: [../projects/01_impact_analytics.md](../projects/01_impact_analytics.md), [../projects/02_frm_deep_dive.md](../projects/02_frm_deep_dive.md), [../projects/03_menu_deep_dive.md](../projects/03_menu_deep_dive.md), [../projects/04_masters_gfg_deep_dive.md](../projects/04_masters_gfg_deep_dive.md)
- Canonical resume wording for Impact Analytics: `docs/ASSORTSMART_TAB_RESUME.md` at the repo root.
