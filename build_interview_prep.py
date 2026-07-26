#!/usr/bin/env python3
"""Build InterviewPrep*.html study hubs for all resume tracks."""
import glob
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

try:
    import markdown
except ImportError:
    os.system(f"{sys.executable} -m pip install markdown --break-system-packages -q")
    import markdown

CSS = """<style>
:root{--bg:#0f1115;--panel:#161a22;--ink:#e8eaf0;--mut:#9aa3b2;--acc:#7aa2f7;--acc2:#9ece6a;--warn:#e0af68;--line:#2a3040;}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
.layout{display:grid;grid-template-columns:300px 1fr;min-height:100vh}
nav.toc{position:sticky;top:0;height:100vh;overflow-y:auto;background:var(--panel);border-right:1px solid var(--line);padding:18px 14px}
nav.toc .brand{font-weight:700;color:var(--acc);margin-bottom:12px;font-size:14px;letter-spacing:.4px}
nav.toc a{display:block;color:var(--mut);text-decoration:none;font-size:12.6px;padding:3px 8px;border-radius:6px;line-height:1.4}
nav.toc a:hover{color:var(--ink);background:#1d2330}
nav.toc a.lvl1{color:var(--ink);font-weight:600;margin-top:10px}
nav.toc a.lvl2{padding-left:20px}
main{padding:34px 48px;max-width:1000px}
h1{color:var(--acc);font-size:26px;border-bottom:2px solid var(--line);padding-bottom:8px;margin-top:44px}
h2{color:var(--acc2);font-size:20px;margin-top:32px}
h3{color:var(--ink);font-size:16.5px;margin-top:24px}
a{color:var(--acc)}
code{background:#1d2330;color:#c6d4f7;padding:1.5px 6px;border-radius:5px;font-size:.88em}
pre{background:#12151c;border:1px solid var(--line);border-radius:10px;padding:14px 16px;overflow-x:auto;font-size:12.6px;line-height:1.5}
pre code{background:none;padding:0}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:13.6px}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#1a1f2b;color:var(--acc)}
tr:nth-child(even){background:#141822}
blockquote{border-left:3px solid var(--acc);margin:12px 0;padding:6px 16px;background:#151a24;color:#c9cfdb;border-radius:0 8px 8px 0}
.callout{border-radius:10px;padding:12px 16px;margin:14px 0;border:1px solid var(--line)}
.callout.note{background:#14202b;border-color:#28455e}
.callout.warn{background:#2b2114;border-color:#5e4a28}
.callout.highlight{background:#16281a;border-color:#2e5e3a}
.stage-badge{display:inline-block;background:#1d2330;color:var(--warn);border:1px solid var(--line);border-radius:999px;padding:3px 14px;font-size:12px;margin:6px 0}
hr{border:none;border-top:1px solid var(--line);margin:30px 0}
strong{color:#fff}
@media(max-width:900px){.layout{grid-template-columns:1fr}nav.toc{position:relative;height:auto}}
</style>"""


def build(order, out_name, title, brand):
    parts = []
    for f in order:
        if os.path.exists(f):
            parts.append(open(f, encoding="utf-8").read())
    raw = "\n\n---\n\n".join(parts)
    for d in ('<div class="callout note">', '<div class="callout warn">', '<div class="callout highlight">'):
        raw = raw.replace(d, d[:-1] + ' markdown="1">')
    md = markdown.Markdown(extensions=["extra", "sane_lists", "toc", "fenced_code"], output_format="html5")
    html = md.convert(raw)
    nav = "\n".join(
        f'<a class="lvl{m.group(1)}" href="#{m.group(2)}">{re.sub(r"<[^>]+>", "", m.group(3)).strip()}</a>'
        for m in re.finditer(r'<h([12]) id="([^"]+)">(.*?)</h\1>', html, flags=re.DOTALL)
    )
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title}</title>{CSS}</head><body>
<div class="layout"><nav class="toc"><div class="brand">{brand}</div>{nav}</nav>
<main>{html}</main></div></body></html>"""
    out = os.path.join(BASE, out_name)
    open(out, "w", encoding="utf-8").write(page)
    print("wrote", out, "| nav entries:", nav.count("lvl"), "| bytes:", len(page))


IP = os.path.join(BASE, "interview_prep")
build(
    [os.path.join(IP, "00_index.md")]
    + sorted(glob.glob(os.path.join(IP, "projects", "*.md")))
    + [os.path.join(IP, "06_tech_deep_dives.md"), os.path.join(IP, "07_behavioral_star_stories.md"),
       os.path.join(IP, "08_role_targeting_and_rapid_fire.md"),
       os.path.join(IP, "09_metrics_derivations.md")]
    + sorted(glob.glob(os.path.join(IP, "agentic_assort_playbook", "*.md"))),
    "InterviewPrep.html",
    "Tarun Mittal — Final Resume · Interview Prep Hub",
    "Final Resume · Interview Prep",
)

IPJ = os.path.join(BASE, "interview_prep_java")
IPV2 = os.path.join(BASE, "interview_prep_v2")
build(
    [os.path.join(IPJ, "00_index.md"), os.path.join(IPJ, "GROUND_TRUTH.md"),
     os.path.join(IPJ, "README.md")]
    + sorted(glob.glob(os.path.join(IPJ, "projects", "*.md")))
    + [os.path.join(IPJ, "06_tech_deep_dives.md"), os.path.join(IPJ, "07_behavioral_star_stories.md"),
       os.path.join(IPJ, "08_role_targeting_and_rapid_fire.md"),
       os.path.join(IPJ, "09_metrics_derivations.md"),
       # Shared grounded deep dives (same facts; map layers to Spring in interviews)
       os.path.join(IPV2, "10_impact_analytics_deep_dive.md"),
       os.path.join(IPV2, "11_uber_frm_deep_dive.md"),
       os.path.join(IPV2, "12_masters_gfg_deep_dive.md"),
       os.path.join(IPV2, "13_behavioral_why_switch.md"),
       os.path.join(IPV2, "14_uber_menu_deep_dive.md"),
       os.path.join(IPV2, "17_senior_systems_study_only.md"),
       os.path.join(IPV2, "18_resume_number_catalog.md"),
       os.path.join(IPV2, "22_application_questions.md"),
       os.path.join(IPV2, "23_project_interview_packs.md"),
       os.path.join(IPV2, "23a_ia_interview_pack.md"),
       os.path.join(IPV2, "23b_uber_interview_packs.md"),
       os.path.join(IPV2, "23c_masters_gfg_interview_packs.md")],
    "InterviewPrepJava.html",
    "Tarun Mittal — Java/Spring · Interview Prep Hub",
    "Java/Spring · Interview Prep",
)

IPV2 = os.path.join(BASE, "interview_prep_v2")
build(
    [os.path.join(IPV2, "00_index.md"),
     os.path.join(IPV2, "GROUND_TRUTH.md"),
     os.path.join(IPV2, "01_skills_trim_rationale.md"),
     os.path.join(IPV2, "02_mongodb_elasticsearch.md"),
     os.path.join(IPV2, "03_uber_menu_streaming_numbers.md"),
     os.path.join(IPV2, "08_role_targeting_and_rapid_fire.md"),
     os.path.join(IPV2, "09_metrics_derivations.md"),
     os.path.join(IPV2, "10_impact_analytics_deep_dive.md"),
     os.path.join(IPV2, "11_uber_frm_deep_dive.md"),
     os.path.join(IPV2, "12_masters_gfg_deep_dive.md"),
     os.path.join(IPV2, "13_behavioral_why_switch.md"),
     os.path.join(IPV2, "14_uber_menu_deep_dive.md"),
     os.path.join(IPV2, "15_judge_loop_report.md"),
     os.path.join(IPV2, "16_ats_recruiter_report.md"),
     os.path.join(IPV2, "17_senior_systems_study_only.md"),
     os.path.join(IPV2, "18_resume_number_catalog.md"),
     os.path.join(IPV2, "19_ia_ch_pg_poc_source.md"),
     os.path.join(IPV2, "20_ia_lineplanning_benchmark_source.md"),
     os.path.join(IPV2, "21_ia_pivot_benchmark_source.md"),
     os.path.join(IPV2, "22_application_questions.md"),
     os.path.join(IPV2, "23_project_interview_packs.md"),
     os.path.join(IPV2, "23a_ia_interview_pack.md"),
     os.path.join(IPV2, "23b_uber_interview_packs.md"),
     os.path.join(IPV2, "23c_masters_gfg_interview_packs.md"),
     os.path.join(IPV2, "07_behavioral_star_stories.md")],
    "InterviewPrepV2.html",
    "Tarun Mittal — Python/Go v2 · Interview Prep",
    "Python/Go v2 · Interview Prep",
)
