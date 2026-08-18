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

# Every markdown file in the repo is mirrored to HTML, except sources under these
# directories (build inputs / binaries, not study pages).
SKIP_NAMES = {
    ".git",
    "node_modules",
    "__pycache__",
    "artifacts",
    "output",
    "sections",
    "KNOWLEDGE-MATERIAL",
}

# Hand-maintained rich pages the generic converter must never overwrite.
PROTECTED_HTML = {
    "final_pygo_ai/ApplicationKit.html",
}

# Track folder → label for the topbar and the site map.
TRACK_LABELS = [
    ("final_java_pygo_ia", "Final Java+PyGo IA"),
    ("final_java_ai", "Final Java+AI"),
    ("final_pygo_ai", "Final PyGo+AI"),
]


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
    """Topbar links back to the owning track (or root hub).

    `rel_path` is repo-relative (file or dir/...). Depth of `/` chooses `../` count
    so track-root pages and nested prep/outreach pages both resolve correctly.
    """
    depth = rel_path.count("/")  # resume_v2/foo.md → 1; resume_v2/prep/foo.md → 2
    track_up = "../" * max(depth - 1, 0)  # → owning track folder
    root_up = "../" * depth  # → repo root hub

    for folder, label in TRACK_LABELS:
        if rel_path.startswith(folder + "/"):
            return (
                f'<a href="{root_up}index.html">← All tracks</a>'
                f'<a href="{track_up}index.html">{label}</a>'
                f'<a href="{track_up}InterviewPrep.html">Prep hub</a>'
                f'<a href="{track_up}ApplicationKit.html">Application Kit</a>'
                f'<a href="{root_up}all_pages.html">All pages</a>'
            )
    # Repo-root page (README, cross-track ATS, …)
    return '<a href="index.html">← All tracks</a><a href="all_pages.html">All pages</a>'


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
    if os.path.relpath(out, BASE) in PROTECTED_HTML:
        return ""  # hand-maintained rich page — leave it alone
    open(out, "w", encoding="utf-8").write(page)
    return out


def iter_markdown() -> list[str]:
    """Every markdown file in the repo except build inputs (see SKIP_NAMES)."""
    found = []
    for dirpath, dirnames, filenames in os.walk(BASE):
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
    # Track landing pages owned by hand — do not overwrite.
    skip = {
        os.path.join(BASE, "final_java_ai"),
        os.path.join(BASE, "final_java_pygo_ia"),
        os.path.join(BASE, "final_pygo_ai"),
    }
    skip.add(BASE)  # repo root index.html is the hand-written track hub
    dirs = set()
    for md in iter_markdown():
        dirs.add(os.path.dirname(md))
    for d in sorted(dirs):
        if d in skip:
            continue
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


def iter_html_pages() -> list[str]:
    """Every published HTML page, repo-relative, sorted."""
    found = []
    for dirpath, dirnames, filenames in os.walk(BASE):
        dirnames[:] = [d for d in dirnames if d not in SKIP_NAMES and not d.startswith(".")]
        for name in filenames:
            if name.endswith(".html"):
                rel = os.path.relpath(os.path.join(dirpath, name), BASE)
                if rel not in ("all_pages.html",):
                    found.append(rel)
    return sorted(found)


def write_site_map() -> int:
    """Publish all_pages.html — every HTML page on the site, grouped by track."""
    pages = iter_html_pages()
    groups: dict[str, list[str]] = {}
    for rel in pages:
        top = rel.split("/")[0] if "/" in rel else "_root"
        groups.setdefault(top, []).append(rel)

    order = [f for f, _ in TRACK_LABELS]
    labels = dict(TRACK_LABELS)
    ordered_keys = ["_root"] + [k for k in order if k in groups]
    ordered_keys += [k for k in sorted(groups) if k not in ordered_keys]

    sections = []
    for key in ordered_keys:
        rels = groups.get(key)
        if not rels:
            continue
        heading = "Repo root" if key == "_root" else f"{labels.get(key, key)} <code>{key}/</code>"
        # sub-group by directory so prep/outreach/ats read as blocks
        by_dir: dict[str, list[str]] = {}
        for rel in rels:
            parent = os.path.dirname(rel) or "."
            by_dir.setdefault(parent, []).append(rel)
        blocks = []
        for parent in sorted(by_dir):
            items = "\n".join(
                f'<li><a href="{rel}">{os.path.basename(rel)[:-5]}</a></li>'
                for rel in sorted(by_dir[parent])
            )
            sub = "" if parent in (".", key) else f'<div class="dir">{parent}/</div>'
            blocks.append(f'{sub}<ul class="pagelist">{items}</ul>')
        sections.append(
            f'<section><h2>{heading} '
            f'<span class="count">{len(rels)} pages</span></h2>{"".join(blocks)}</section>'
        )

    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="noindex,nofollow"/>
<title>All pages — Tarun Mittal</title>{CSS}
<style>
main{{max-width:1100px}}
.count{{color:var(--mut);font-size:12px;font-weight:400;margin-left:8px}}
.dir{{color:var(--warn);font-size:12.5px;font-family:ui-monospace,monospace;margin:14px 0 4px}}
ul.pagelist{{list-style:none;padding:0;margin:0 0 6px;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:2px 14px}}
ul.pagelist li{{margin:0}}
ul.pagelist a{{display:block;padding:3px 8px;border-radius:6px;text-decoration:none;font-size:13px}}
ul.pagelist a:hover{{background:#1d2330}}
section{{margin-bottom:34px}}
</style></head>
<body>
<div class="topbar"><a href="index.html">← All tracks</a><span class="path">all_pages.html</span></div>
<main>
<h1>Every page on this site</h1>
<p style="color:var(--mut)">{len(pages)} HTML pages. Markdown sources stay in the git repo; every
one of them is mirrored here so nothing is reachable only as raw <code>.md</code>.</p>
{"".join(sections)}
</main>
</body></html>
"""
    open(os.path.join(BASE, "all_pages.html"), "w", encoding="utf-8").write(page)
    return len(pages)


def main() -> None:
    files = iter_markdown()
    outs = [o for o in (convert_file(md) for md in files) if o]
    write_folder_indexes()
    for hub in (
        os.path.join("final_java_ai", "InterviewPrep.html"),
        os.path.join("final_java_ai", "ApplicationKit_deep.html"),
        os.path.join("final_java_pygo_ia", "InterviewPrep.html"),
        os.path.join("final_java_pygo_ia", "ApplicationKit_deep.html"),
        os.path.join("final_pygo_ai", "InterviewPrep.html"),
        os.path.join("final_pygo_ai", "ApplicationKit.html"),
        "index.html",
    ):
        rewrite_hub_file(os.path.join(BASE, hub))
    total = write_site_map()
    print(f"wrote {len(outs)} HTML mirrors + folder indexes + site map ({total} pages)")


if __name__ == "__main__":
    main()
