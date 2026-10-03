# 08. Questions actually asked in the OCI loop

These are the questions from the interview, in the order they were drilled, with a full answer for each one. Related follow-ups that sit on the same concepts are in the same files, marked **Likely follow-up**.

Say the short answer first, then the diagram, then one command or one trade-off. They kept going deeper on TCP. Do not jump to a tool name before you name the state.

| # | Question | File |
|---|---|---|
| 1–9 | Port bind, permissions, TIME_WAIT / CLOSE_WAIT / FIN_WAIT, FIN/ACK flow, SYN backlog vs accept queue | [08a](08a_linux_tcp_troubleshooting.md) |
| 10–18 | Django, BookMyShow schema and seat locking, fault tolerance, orchestration vs choreography, CAP, OCR + RAG | [08b](08b_backend_python_dsa.md) |
| 19–22 | Generators, 1..1000 without a list, bits for 1000 values | [08b](08b_backend_python_dsa.md) |
| 23–24 | Longest substring without repeating characters, example `ABCADCBED` | [08b](08b_backend_python_dsa.md) |
| 25–27 | Membership checks against a huge corpus, no horizontal scale, DB indexes | [08b](08b_backend_python_dsa.md) |
| 28–32 | P99 ~10s, CPU ~20%, load ~30, socket states, `ss` / `lsof` | [08a](08a_linux_tcp_troubleshooting.md) |
| HM 1–4 | Intro, why so soon, ownership, end to end, join by 26 May | [08c](08c_behavioral_terraform.md) |
| TF 5–6 | `count` vs `for_each`, migrate state with `moved` without recreate | [08c](08c_behavioral_terraform.md) |

**What this loop was testing**

- Can you debug a Linux box from symptoms (errno, socket state, load vs CPU), not from a dashboard name.
- Do you know TCP as a state machine, including which side sends FIN.
- Can you design a correct concurrent write (seats) and a real pipeline (OCR + RAG), not a single prompt.
- Do you change production infrastructure by changing **state addresses**, and prove it with `plan`, before you apply.

Deeper background that these answers assume: [02 JD map](02_jd_technical_map.md), [04 fundamentals](04_system_design_fundamentals.md), [05 LLD seat booking](05_lld_problems.md), [06 concurrency](06_concurrency.md), [07 projects](07_projects_deep_dive.md).
