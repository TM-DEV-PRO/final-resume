#!/usr/bin/env python3
"""Build per-track InterviewPrep.html hubs (isolated resume folders)."""
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
.mermaid{background:#12151c;border:1px solid var(--line);border-radius:10px;padding:16px;margin:14px 0;overflow-x:auto}
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

MERMAID_BOOT = """
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({ startOnLoad: true, theme: 'dark', securityLevel: 'loose' });
</script>
"""


def promote_mermaid(html: str) -> str:
    def repl(m):
        body = m.group(1)
        body = (
            body.replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&amp;", "&")
            .replace("&quot;", '"')
        )
        return f'<div class="mermaid">{body}</div>'

    return re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        repl,
        html,
        flags=re.DOTALL,
    )


def rewrite_md_hrefs_text(text):
    text = re.sub(
        r'(href=["\'])([^"\']+?)\.md(#[^"\']*)?(["\'])',
        lambda m: f"{m.group(1)}{m.group(2)}.html{m.group(3) or ''}{m.group(4)}",
        text,
    )
    text = re.sub(
        r"(\[[^\]]*\]\()([^)\s]+?)\.md(#[^)]*)?(\))",
        lambda m: f"{m.group(1)}{m.group(2)}.html{m.group(3) or ''}{m.group(4)}",
        text,
    )
    return text


def rewrite_md_hrefs(path):
    if not os.path.isfile(path):
        return
    text = open(path, encoding="utf-8").read()
    new = rewrite_md_hrefs_text(text)
    if new != text:
        open(path, "w", encoding="utf-8").write(new)
        print("rewrote links:", os.path.relpath(path, BASE))


SKIP_DIRS = {"artifacts", "output", "sections", "__pycache__", "node_modules"}


def rest_of_track(track_dir, already):
    """Every remaining markdown file in a track, so a hub is never a partial view.

    `already` fixes the reading order for the curated head; whatever is left gets
    appended alphabetically instead of being silently dropped from the hub.
    """
    seen = {os.path.abspath(p) for p in already}
    extra = []
    for dirpath, dirnames, filenames in os.walk(track_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            if os.path.abspath(path) not in seen:
                extra.append(path)
    return sorted(extra)


def relativize(text, src_dir, out_dir):
    """Re-base relative links so they still resolve from the hub's own directory.

    A hub concatenates files from `prep/` but is written at the track root, so a link
    like `GROUND_TRUTH.md` has to become `prep/GROUND_TRUTH.md`.
    """
    def fix(target):
        if not target or target.startswith(("http://", "https://", "mailto:", "#", "/")):
            return target
        return os.path.relpath(os.path.join(src_dir, target), out_dir).replace(os.sep, "/")

    text = re.sub(
        r"(\]\()([^)\s#]+)((?:#[^)]*)?\))",
        lambda m: f"{m.group(1)}{fix(m.group(2))}{m.group(3)}",
        text,
    )
    text = re.sub(
        r'(href=")([^"#]+)((?:#[^"]*)?")',
        lambda m: f"{m.group(1)}{fix(m.group(2))}{m.group(3)}",
        text,
    )
    return text


def build(order, out_path, title, brand, track_dir=None):
    if track_dir:
        order = list(order) + rest_of_track(track_dir, order)
    out_dir = os.path.dirname(os.path.abspath(out_path))
    parts = []
    for f in order:
        if os.path.exists(f):
            body = open(f, encoding="utf-8").read()
            parts.append(relativize(body, os.path.dirname(os.path.abspath(f)), out_dir))
    raw = "\n\n---\n\n".join(parts)
    for d in ('<div class="callout note">', '<div class="callout warn">', '<div class="callout highlight">'):
        raw = raw.replace(d, d[:-1] + ' markdown="1">')
    md = markdown.Markdown(extensions=["extra", "sane_lists", "toc", "fenced_code"], output_format="html5")
    html = md.convert(raw)
    html = rewrite_md_hrefs_text(html)
    html = promote_mermaid(html)
    nav = "\n".join(
        f'<a class="lvl{m.group(1)}" href="#{m.group(2)}">{re.sub(r"<[^>]+>", "", m.group(3)).strip()}</a>'
        for m in re.finditer(r'<h([12]) id="([^"]+)">(.*?)</h\1>', html, flags=re.DOTALL)
    )
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title}</title>{CSS}</head><body>
<div class="layout"><nav class="toc"><div class="brand">{brand}</div>{nav}</nav>
<main>{html}</main></div>{MERMAID_BOOT}</body></html>"""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    open(out_path, "w", encoding="utf-8").write(page)
    print("wrote", out_path, "| nav entries:", nav.count("lvl"), "| bytes:", len(page))


# Paths — only the three maintained final tracks
# (legacy resume/, resume_v2/, resume_java/, campaign_pygo_xyz/ removed)

# Final Java + AI (self-contained prep copy)
FJ = os.path.join(BASE, "final_java_ai")
FJ_PREP = os.path.join(FJ, "prep")
build(
    [os.path.join(FJ_PREP, "00_final_resume_map.md"), os.path.join(FJ_PREP, "00_index.md"),
     os.path.join(FJ_PREP, "GROUND_TRUTH.md")]
    + sorted(glob.glob(os.path.join(FJ_PREP, "projects", "*.md")))
    + [
        os.path.join(FJ, "ats", "00_ats_11_company_scorecard.md"),
        os.path.join(FJ, "ats", "company_notes_rubrik_databricks_planetscale.md"),
        os.path.join(FJ_PREP, "09_metrics_derivations.md"),
        os.path.join(FJ_PREP, "10_impact_analytics_deep_dive.md"),
        os.path.join(FJ_PREP, "11_uber_frm_deep_dive.md"),
        os.path.join(FJ_PREP, "12_masters_gfg_deep_dive.md"),
        os.path.join(FJ_PREP, "14_uber_menu_deep_dive.md"),
        os.path.join(FJ_PREP, "18_resume_number_catalog.md"),
        os.path.join(FJ_PREP, "21_ia_pivot_benchmark_source.md"),
        os.path.join(FJ_PREP, "22_application_questions.md"),
        os.path.join(FJ_PREP, "23a_ia_interview_pack.md"),
        os.path.join(FJ_PREP, "23b_uber_interview_packs.md"),
        os.path.join(FJ_PREP, "23c_masters_gfg_interview_packs.md"),
        os.path.join(FJ_PREP, "29_ia_ch_ddl_phase1_source.md"),
        os.path.join(FJ_PREP, "31_resume_deep_explain_map.md"),
        os.path.join(FJ_PREP, "32_common_interview_qa.md"),
        os.path.join(FJ_PREP, "37_senior_screen_deep_qa.md"),
        os.path.join(FJ, "campaign_extras", "interview_prep", "deployment_and_scale.md"),
        os.path.join(FJ_PREP, "33_architecture_diagrams.md"),
        os.path.join(FJ_PREP, "34_er_tables_tech_why.md"),
        os.path.join(FJ_PREP, "35_table_schemas_api_design.md"),
        os.path.join(FJ_PREP, "36_skills_ai_agents_defense.md"),
        os.path.join(FJ_PREP, "01_skills_trim_rationale.md"),
        os.path.join(FJ, "campaign_extras", "interview_prep", "tech_depth", "00_index.md"),
        os.path.join(FJ, "campaign_extras", "interview_prep", "tech_depth", "langgraph_mcp_rag.md"),
        os.path.join(FJ, "campaign_extras", "interview_prep", "tech_depth", "skills_fundamentals_map.md"),
        os.path.join(FJ, "campaign_extras", "interview_prep", "tech_depth", "observability_cloud.md"),
        os.path.join(FJ, "ApplicationKit.md"),
        os.path.join(FJ, "linkedin", "headline_about_experience.md"),
        os.path.join(FJ, "outreach", "recruiter_cold_email.md"),
        os.path.join(FJ, "outreach", "referrals_short_long.md"),
    ],
    os.path.join(FJ, "InterviewPrep.html"),
    "Tarun Mittal — Final Java + AI · Interview Prep",
    "Final Java+AI · Interview Prep",    track_dir=FJ,
)

# Final Java + AI (IA = Python/Go hybrid)
FJPI = os.path.join(BASE, "final_java_pygo_ia")
FJPI_PREP = os.path.join(FJPI, "prep")
build(
    [os.path.join(FJPI_PREP, "00_final_resume_map.md"), os.path.join(FJPI_PREP, "00_index.md"),
     os.path.join(FJPI_PREP, "GROUND_TRUTH.md")]
    + sorted(glob.glob(os.path.join(FJPI_PREP, "projects", "*.md")))
    + [
        os.path.join(FJPI, "ats", "00_ats_11_company_scorecard.md"),
        os.path.join(FJPI, "ats", "company_notes_rubrik_databricks_planetscale.md"),
        os.path.join(FJPI_PREP, "09_metrics_derivations.md"),
        os.path.join(FJPI_PREP, "10_impact_analytics_deep_dive.md"),
        os.path.join(FJPI_PREP, "11_uber_frm_deep_dive.md"),
        os.path.join(FJPI_PREP, "12_masters_gfg_deep_dive.md"),
        os.path.join(FJPI_PREP, "14_uber_menu_deep_dive.md"),
        os.path.join(FJPI_PREP, "18_resume_number_catalog.md"),
        os.path.join(FJPI_PREP, "21_ia_pivot_benchmark_source.md"),
        os.path.join(FJPI_PREP, "22_application_questions.md"),
        os.path.join(FJPI_PREP, "23a_ia_interview_pack.md"),
        os.path.join(FJPI_PREP, "23b_uber_interview_packs.md"),
        os.path.join(FJPI_PREP, "23c_masters_gfg_interview_packs.md"),
        os.path.join(FJPI_PREP, "29_ia_ch_ddl_phase1_source.md"),
        os.path.join(FJPI_PREP, "31_resume_deep_explain_map.md"),
        os.path.join(FJPI_PREP, "32_common_interview_qa.md"),
        os.path.join(FJPI_PREP, "37_senior_screen_deep_qa.md"),
        os.path.join(FJPI, "campaign_extras", "interview_prep", "deployment_and_scale.md"),
        os.path.join(FJPI_PREP, "33_architecture_diagrams.md"),
        os.path.join(FJPI_PREP, "34_er_tables_tech_why.md"),
        os.path.join(FJPI_PREP, "35_table_schemas_api_design.md"),
        os.path.join(FJPI_PREP, "36_skills_ai_agents_defense.md"),
        os.path.join(FJPI_PREP, "01_skills_trim_rationale.md"),
        os.path.join(FJPI, "campaign_extras", "interview_prep", "tech_depth", "00_index.md"),
        os.path.join(FJPI, "campaign_extras", "interview_prep", "tech_depth", "langgraph_mcp_rag.md"),
        os.path.join(FJPI, "campaign_extras", "interview_prep", "tech_depth", "skills_fundamentals_map.md"),
        os.path.join(FJPI, "campaign_extras", "interview_prep", "tech_depth", "observability_cloud.md"),
        os.path.join(FJPI, "ApplicationKit.md"),
        os.path.join(FJPI, "linkedin", "headline_about_experience.md"),
        os.path.join(FJPI, "outreach", "recruiter_cold_email.md"),
        os.path.join(FJPI, "outreach", "referrals_short_long.md"),
    ],
    os.path.join(FJPI, "InterviewPrep.html"),
    "Tarun Mittal — Final Java + AI (IA=Py/Go) · Interview Prep",
    "Final Java+PyGo IA · Interview Prep",    track_dir=FJPI,
)

# Final Python + Go + AI
FP = os.path.join(BASE, "final_pygo_ai")
FP_PREP = os.path.join(FP, "prep")
FP_EX = os.path.join(FP, "campaign_extras")
build(
    [
        os.path.join(FP_PREP, "00_final_resume_map.md"),
        os.path.join(FP_PREP, "00_index.md"),
        os.path.join(FP_PREP, "GROUND_TRUTH.md"),
        os.path.join(FP, "ats", "00_ats_11_company_scorecard.md"),
        os.path.join(FP, "ats", "company_notes_rubrik_databricks_planetscale.md"),
        os.path.join(FP_PREP, "09_metrics_derivations.md"),
        os.path.join(FP_PREP, "10_impact_analytics_deep_dive.md"),
        os.path.join(FP_PREP, "11_uber_frm_deep_dive.md"),
        os.path.join(FP_PREP, "12_masters_gfg_deep_dive.md"),
        os.path.join(FP_PREP, "14_uber_menu_deep_dive.md"),
        os.path.join(FP_PREP, "18_resume_number_catalog.md"),
        os.path.join(FP_PREP, "21_ia_pivot_benchmark_source.md"),
        os.path.join(FP_PREP, "22_application_questions.md"),
        os.path.join(FP_PREP, "23a_ia_interview_pack.md"),
        os.path.join(FP_PREP, "23b_uber_interview_packs.md"),
        os.path.join(FP_PREP, "23c_masters_gfg_interview_packs.md"),
        os.path.join(FP_PREP, "29_ia_ch_ddl_phase1_source.md"),
        os.path.join(FP_PREP, "31_resume_deep_explain_map.md"),
        os.path.join(FP_PREP, "32_common_interview_qa.md"),
        os.path.join(FP_PREP, "37_senior_screen_deep_qa.md"),
        os.path.join(FP_EX, "interview_prep", "deployment_and_scale.md"),
        os.path.join(FP_PREP, "33_architecture_diagrams.md"),
        os.path.join(FP_PREP, "34_er_tables_tech_why.md"),
        os.path.join(FP_PREP, "35_table_schemas_api_design.md"),
        os.path.join(FP_PREP, "36_skills_ai_agents_defense.md"),
        os.path.join(FP_PREP, "01_skills_trim_rationale.md"),
        os.path.join(FP_EX, "interview_prep", "architecture", "00_index.md"),
        os.path.join(FP_EX, "interview_prep", "architecture", "01_ia_assortsmart_hindsight.md"),
        os.path.join(FP_EX, "interview_prep", "design_decisions_tradeoffs.md"),
        os.path.join(FP_EX, "interview_prep", "numbers_defense.md"),
        os.path.join(FP_EX, "interview_prep", "tech_depth", "00_index.md"),
        os.path.join(FP_EX, "interview_prep", "tech_depth", "langgraph_mcp_rag.md"),
        os.path.join(FP_EX, "interview_prep", "tech_depth", "skills_fundamentals_map.md"),
        os.path.join(FP_EX, "interview_prep", "tech_depth", "observability_cloud.md"),
        os.path.join(FP_EX, "behavioral", "why_hire_you.md"),
        os.path.join(FP_EX, "behavioral", "intros_short_long.md"),
        os.path.join(FP, "ApplicationKit.md"),
        os.path.join(FP, "linkedin", "headline_about_experience.md"),
        os.path.join(FP, "outreach", "recruiter_cold_email.md"),
        os.path.join(FP, "outreach", "referrals_short_long.md"),
    ],
    os.path.join(FP, "InterviewPrep.html"),
    "Tarun Mittal — Final Python + Go + AI · Interview Prep",
    "Final PyGo+AI · Interview Prep",    track_dir=FP,
)

for hub in (
    os.path.join(FJ, "InterviewPrep.html"),
    os.path.join(FJPI, "InterviewPrep.html"),
    os.path.join(FP, "InterviewPrep.html"),
    os.path.join(FP, "ApplicationKit.html"),
    os.path.join(BASE, "index.html"),
):
    rewrite_md_hrefs(hub)

import build_pages_html  # noqa: E402

build_pages_html.main()
