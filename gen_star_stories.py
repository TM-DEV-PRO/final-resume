#!/usr/bin/env python3
"""Make each Java-wording track's prep/07 STAR bank self-contained.

The Python tracks already carry the full 10-story bank. The Java tracks only had a
23-line swap table pointing at resume/prep. This copies the canonical 10 stories in
full and injects a per-track stack-wording note under each story, so behavioral prep
is complete inside every track (Amazon LP + Googliness mapping intact).
"""
from __future__ import annotations

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(BASE, "resume", "prep", "07_behavioral_star_stories.md")

# Per-story wording swap. {writes} = AssortSmart write-plane for the track.
SWAPS = {
    1: "Decision process and PoC gates stay identical. Implementation plane on this track: "
       "the agentic planner is a **Python** service; the AssortSmart write APIs it calls are "
       "**{writes}**; the ClickHouse client and staging jobs sit behind them.",
    2: "Freshness design (atomic `REPLACE PARTITION`, reconciliation, staleness sentinel) is "
       "language-agnostic. If asked *who runs the load*, it is a scheduled **{writes}** job on "
       "this track, not a Python cron.",
    3: "The planner is a **Python / LangGraph** service, so keep the story as-is. The transferable "
       "principle — a deterministic contract around a probabilistic component — is exactly how you "
       "use **Bean Validation / schema checks** before a commit in a Spring service.",
    4: "Product/workflow content is unchanged; the copilot is a **Python FastAPI + LangGraph** "
       "microservice. The write-back into existing product tables goes through the **{writes}** APIs.",
    5: "Owning-the-mistake content is unchanged (it happened on the Uber Python codebase). On this "
       "track, describe the guardrail as a **JUnit** gate — \"the test that would have caught it\".",
    6: "Test-where-the-code-lives principle is unchanged. Java wording: **JUnit + Mockito**, "
       "changed-module coverage in CI, **Testcontainers** for DB-backed tests.",
    7: "Disagree-and-commit content is unchanged. Java framing: the boundary is **Hibernate / JPA** "
       "repositories vs. raw SQL — keep query mapping next to the entity so a rename fails the "
       "compiler, keep the repository a thin session wrapper.",
    8: "Deadline, sequencing, and every number stay identical. Java wording: **Spring Boot** "
       "strangler per endpoint, **Spring Batch** for the bulk IRP path, **Kafka + PostgreSQL** "
       "quarter sharding.",
    9: "Unchanged — this is **Selenium** acquisition with proxy pools and a measurement loop, "
       "regardless of the service language.",
    10: "Integrity content is unchanged. Java wording: idempotency key "
        "(`clientId + fileHash + batchIndex`) enforced in the **Spring Batch** writers and a DB "
        "unique constraint, plus a dead-letter replay path.",
}

JAVA_ADDENDUM = """

---

## Stack-wording quick answers (say these on this track)

- **CI gating:** the pipeline blocks a merge if **JUnit** fails or changed-module coverage drops;
  **Testcontainers** for DB-backed tests. (JUnit is on the FRM experience Tech line, not in Skills.)
- **Testability:** constructor-injected ports (repositories, clients), pure domain functions for
  tax/dedup rules, DTO validation at the boundary.
- **Idempotent retries:** `clientId + fileHash + batchIndex` recognized on replay — same guarantee
  as the main track, enforced in the **Spring Batch** writers plus a DB unique constraint.
- **Observability:** **Actuator + Micrometer** metrics, ELK correlation IDs, New Relic APM — the
  Masters India "triage 70% faster" story is unchanged.
"""

HYBRID_ADDENDUM = """

---

## Stack-wording quick answers (say these on this track)

- **Which language where:** Uber FRM and Masters India are **Spring Boot / Hibernate**; the
  AssortSmart write APIs are **Go / Gin**; the planner, RAG, and evals are **Python**. Say this
  first if an interviewer asks "so what did you write it in".
- **CI gating:** JUnit + Testcontainers on the Java services; `go test` + table-driven tests on the
  Go write APIs; changed-module coverage gate in CI. (JUnit is on the FRM experience Tech line, not
  in Skills.)
- **Idempotent retries:** `clientId + fileHash + batchIndex` recognized on replay — enforced in the
  Spring Batch writers plus a DB unique constraint.
- **Observability:** one OTEL `trace_id` stitched across the Go write plane, the Python agent tier,
  and the Java services; Actuator + Micrometer on the Spring side; New Relic APM.
"""

TRACKS = {
    "final_java_ai": dict(
        title="Behavioral / STAR stories — Final Java + AI",
        writes="Spring Boot",
        note="On this track the AssortSmart write plane is framed as **Spring Boot**; the agent "
             "plane (planner, RAG, evals) stays **Python**.",
        addendum=JAVA_ADDENDUM,
    ),
    "final_java_pygo_ia": dict(
        title="Behavioral / STAR stories — Final Java + PyGo IA (primary)",
        writes="Go / Gin",
        note="On this track Uber FRM and Masters India are **Spring Boot**; the AssortSmart write "
             "APIs are **Go / Gin**; the agent plane (planner, RAG, evals) stays **Python**.",
        addendum=HYBRID_ADDENDUM,
    ),
    "resume_java": dict(
        title="Behavioral / STAR stories — Java / Spring",
        writes="Spring Boot",
        note="Pure Java/Spring framing: non-agentic APIs are **Spring Boot / Hibernate**; the agent "
             "plane stays **Python**.",
        addendum=JAVA_ADDENDUM,
    ),
}

HEADER = """# {title}

**Self-contained** behavioral bank — the full 10 stories are below, so you never leave this track
to prep. Outcomes, Amazon Leadership Principle mapping, and Googliness signals are identical across
every resume track; only the **stack wording** differs. {note}

Tell each in 60–90 seconds: one line of Situation, one of Task, 3–4 concrete Actions, a quantified
Result, and a one-line Lesson. Never tell the same story twice in one loop — this bank gives you
coverage. Company-by-company LP mapping (Amazon, Google, Microsoft, LinkedIn, Apple, Netflix,
Atlassian, Salesforce) lives in `../campaign_extras/behavioral/company_behavior_guides.md`.

"""


def build(track: str, cfg: dict) -> str:
    raw = open(CANON, encoding="utf-8").read()
    # Drop the canonical H1 + its intro paragraph (first two non-empty blocks),
    # keep everything from the coverage matrix down.
    body = raw.split("**Coverage matrix**", 1)[1]
    body = "**Coverage matrix**" + body

    # Inject the per-story wording note right after each "## N. ..." heading.
    def inject(m):
        n = int(m.group(1))
        swap = SWAPS.get(n)
        if not swap:
            return m.group(0)
        swap = swap.format(writes=cfg["writes"])
        return f"{m.group(0)}\n\n> **{track} wording:** {swap}\n"

    body = re.sub(r"^## (\d+)\.[^\n]*$", inject, body, flags=re.MULTILINE)

    header = HEADER.format(title=cfg["title"], note=cfg["note"])
    return header + body.rstrip() + cfg.get("addendum", "") + "\n"


def main() -> None:
    for track, cfg in TRACKS.items():
        out = os.path.join(BASE, track, "prep", "07_behavioral_star_stories.md")
        open(out, "w", encoding="utf-8").write(build(track, cfg))
        print("wrote", os.path.relpath(out, BASE))


if __name__ == "__main__":
    main()
