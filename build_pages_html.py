#!/usr/bin/env python3
"""Mirror prep/campaign markdown to structured HTML for GitHub Pages.

Keeps .md in the repo for editing; publishes .html beside each file so
https://tm-dev-pro.github.io/final-resume/ serves readable pages, not raw markdown.
"""
from __future__ import annotations

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
.topbar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:12px 20px;background:var(--panel);border-bottom:1px solid var(--line);font-size:13px}
.topbar a{color:var(--acc);text-decoration:none}
.topbar .path{color:var(--mut);margin-left:auto}
.layout{display:grid;grid-template-columns:280px 1fr;min-height:calc(100vh - 46px)}
nav.toc{position:sticky;top:0;height:calc(100vh - 46px);overflow-y:auto;background:var(--panel);border-right:1px solid var(--line);padding:16px 12px}
nav.toc .brand{font-weight:700;color:var(--acc);margin-bottom:10px;font-size:13px}
nav.toc a{display:block;color:var(--mut);text-decoration:none;font-size:12.4px;padding:3px 8px;border-radius:6px;line-height:1.35}
nav.toc a:hover{color:var(--ink);background:#1d2330}
nav.toc a.lvl1{color:var(--ink);font-weight:600;margin-top:8px}
nav.toc a.lvl2{padding-left:18px}
main{padding:28px 40px 64px;max-width:980px}
h1{color:var(--acc);font-size:24px;border-bottom:2px solid var(--line);padding-bottom:8px;margin-top:8px}
h2{color:var(--acc2);font-size:19px;margin-top:28px}
h3{color:var(--ink);font-size:16px;margin-top:22px}
a{color:var(--acc)}
code{background:#1d2330;color:#c6d4f7;padding:1.5px 6px;border-radius:5px;font-size:.88em}
pre{background:#12151c;border:1px solid var(--line);border-radius:10px;padding:14px 16px;overflow-x:auto;font-size:12.6px;line-height:1.5}
pre code{background:none;padding:0}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:13.4px}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#1a1f2b;color:var(--acc)}
tr:nth-child(even){background:#141822}
blockquote{border-left:3px solid var(--acc);margin:12px 0;padding:6px 16px;background:#151a24;color:#c9cfdb;border-radius:0 8px 8px 0}
hr{border:none;border-top:1px solid var(--line);margin:28px 0}
strong{color:#fff}
.mermaid{background:#12151c;border:1px solid var(--line);border-radius:10px;padding:16px;margin:14px 0;overflow-x:auto}
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
        body = (
            m.group(1)
            .replace("&lt;", "<")
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

ROOTS = [
    "campaign_pygo_xyz",
    "interview_prep_v2",
    "interview_prep",
    "interview_prep_java",
]

SKIP_NAMES = {".git", "node_modules", "__pycache__"}


def md_to_html_links(text: str) -> str:
    """Rewrite markdown and HTML links that target .md → .html (keep anchors)."""
    text = re.sub(
        r"(\[[^\]]*\]\()([^)\s]+?)\.md(#[^)]*)?(\))",
        lambda m: f"{m.group(1)}{m.group(2)}.html{m.group(3) or ''}{m.group(4)}",
        text,
    )
    text = re.sub(
        r'(href=["\'])([^"\']+?)\.md(#[^"\']*)?(["\'])',
        lambda m: f"{m.group(1)}{m.group(2)}.html{m.group(3) or ''}{m.group(4)}",
        text,
    )
    return text


def rel_hub_links(rel_path: str) -> str:
    depth = rel_path.count("/")
    up = "../" * depth if depth else ""
    return (
        f'<a href="{up}index.html">← Hub</a>'
        f'<a href="{up}CampaignPyGo.html">Campaign</a>'
        f'<a href="{up}InterviewPrepV2.html">Prep v2</a>'
        f'<a href="{up}ApplicationKit.html">Application Kit</a>'
    )


def convert_file(md_path: str) -> str:
    rel = os.path.relpath(md_path, BASE)
    raw = open(md_path, encoding="utf-8").read()
    raw = md_to_html_links(raw)
    for d in (
        '<div class="callout note">',
        '<div class="callout warn">',
        '<div class="callout highlight">',
    ):
        raw = raw.replace(d, d[:-1] + ' markdown="1">')
    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "toc", "fenced_code", "tables"],
        output_format="html5",
    )
    body = md.convert(raw)
    body = md_to_html_links(body)
    body = promote_mermaid(body)
    nav = "\n".join(
        f'<a class="lvl{m.group(1)}" href="#{m.group(2)}">'
        f'{re.sub(r"<[^>]+>", "", m.group(3)).strip()}</a>'
        for m in re.finditer(r'<h([12]) id="([^"]+)">(.*?)</h\1>', body, flags=re.DOTALL)
    )
    title = os.path.basename(md_path).replace(".md", "")
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="noindex,nofollow"/>
<title>{title} — Tarun Mittal</title>
{CSS}
</head>
<body>
<div class="topbar">{rel_hub_links(rel)}<span class="path">{rel.replace(".md", ".html")}</span></div>
<div class="layout">
<nav class="toc"><div class="brand">On this page</div>{nav or '<span style="color:var(--mut);font-size:12px">No sections</span>'}</nav>
<main>{body}</main>
</div>
{MERMAID_BOOT}
</body>
</html>
"""
    out = md_path[:-3] + ".html" if md_path.endswith(".md") else md_path + ".html"
    open(out, "w", encoding="utf-8").write(page)
    return out


def iter_markdown() -> list[str]:
    found = []
    for root in ROOTS:
        abs_root = os.path.join(BASE, root)
        if not os.path.isdir(abs_root):
            continue
        for dirpath, dirnames, filenames in os.walk(abs_root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_NAMES and not d.startswith(".")]
            for name in filenames:
                if name.endswith(".md"):
                    found.append(os.path.join(dirpath, name))
    return sorted(found)


def rewrite_hub_file(path: str) -> None:
    if not os.path.isfile(path):
        return
    text = open(path, encoding="utf-8").read()
    new = md_to_html_links(text)
    if new != text:
        open(path, "w", encoding="utf-8").write(new)
        print("rewrote links:", os.path.relpath(path, BASE))


def write_folder_indexes() -> None:
    """Directory index.html listing sibling HTML pages (no raw .md links)."""
    dirs = set()
    for md in iter_markdown():
        dirs.add(os.path.dirname(md))
    for d in sorted(dirs):
        htmls = sorted(
            f for f in os.listdir(d)
            if f.endswith(".html") and f != "index.html"
        )
        if not htmls:
            continue
        rel = os.path.relpath(d, BASE)
        items = "\n".join(
            f'<li><a href="{h}">{h.replace(".html", "")}</a></li>' for h in htmls
        )
        page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="noindex,nofollow"/>
<title>{rel} — index</title>{CSS}</head>
<body>
<div class="topbar">{rel_hub_links(rel + "/x")}<span class="path">{rel}/</span></div>
<main style="padding:32px 40px">
<h1>{rel}</h1>
<p style="color:var(--mut)">HTML study pages (markdown sources stay in the git repo).</p>
<ul>{items}</ul>
</main></body></html>
"""
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)


def main() -> None:
    files = iter_markdown()
    outs = []
    for md in files:
        outs.append(convert_file(md))
    write_folder_indexes()
    for hub in (
        "CampaignPyGo.html",
        "ApplicationKit.html",
        "InterviewPrep.html",
        "InterviewPrepV2.html",
        "InterviewPrepJava.html",
        "index.html",
    ):
        rewrite_hub_file(os.path.join(BASE, hub))
    print(f"wrote {len(outs)} HTML mirrors + folder indexes")


if __name__ == "__main__":
    main()
