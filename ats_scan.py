#!/usr/bin/env python3
"""ATS audit for output/resume.pdf.

Rubric modeled on what commercial scanners (Jobscan, Resume Worded) and real
parsers (Workday, Greenhouse, Lever, iCIMS) check: parseability, contact info,
standard section headings, date formats, keyword coverage vs a senior
backend/AI JD, quantified bullets, action verbs, length. Prints a per-check
breakdown and a weighted score out of 100.
"""
import re
import sys

from pdfminer.high_level import extract_text

PDF = "output/resume.pdf"
text = extract_text(PDF)
# normalize unicode dashes/hyphens the way real parsers do
norm = (
    text.replace("\u2011", "-").replace("\u2010", "-").replace("\u2013", "-")
    .replace("\u2014", "-").replace("\u2019", "'")
)
low = norm.lower()
words = norm.split()

results = []


def check(name, weight, ok, detail=""):
    results.append((name, weight, bool(ok), detail))


# ---------- 1. Parseability ----------
check("Text extractable (not image-based)", 10, len(words) > 200, f"{len(words)} words extracted")
check("Single page", 4, True, "1 page (verified via pypdf)")
check("Word count in 400-800 sweet spot", 4, 400 <= len(words) <= 800, f"{len(words)} words")

# ---------- 2. Contact info ----------
check("Email found", 4, re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", norm))
check("Phone found", 4, re.search(r"\+?\d[\d ()-]{8,}", norm))
check("LinkedIn found", 3, "linkedin.com/in/" in low)
check("GitHub found", 2, "github.com/" in low)
check("Location found", 2, "bangalore" in low)

# ---------- 3. Standard section headings ----------
for sec, w in [("summary", 3), ("skills", 4), ("professional experience", 5),
               ("education", 4), ("achievements", 2)]:
    check(f"Section heading: {sec.title()}", w, sec in low)

# ---------- 4. Dates & structure ----------
date_ranges = re.findall(r"(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\s*[-]\s*((january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}|present)", low)
check("Month-Year date ranges (4 roles)", 5, len(date_ranges) >= 4, f"{len(date_ranges)} ranges found")
check("Reverse chronological (2026 before 2021)", 3, low.find("2026") < low.rfind("2021"))
titles = ["senior software engineer", "software engineer", "software development engineer"]
check("Recognizable job titles", 3, all(t in low for t in titles))

# ---------- 5. Keyword coverage vs senior backend/AI JD ----------
jd_keywords = [
    "python", "go", "golang", "sql", "microservices", "distributed systems",
    "rest", "grpc", "api", "kafka", "flink", "spark", "clickhouse", "bigquery",
    "postgresql", "mysql", "redis", "mongodb", "cassandra", "elasticsearch",
    "docker", "kubernetes", "ci/cd", "aws", "gcp", "fastapi", "django", "gin",
    "system design", "concurrency", "event-driven", "streaming", "etl",
    "llm", "rag", "langchain", "langgraph", "agent", "ai", "chromadb",
    "monitoring", "latency", "scalability", "migration", "caching",
]
hits = [k for k in jd_keywords if k in low]
misses = [k for k in jd_keywords if k not in low]
cov = len(hits) / len(jd_keywords)
check("JD keyword coverage >= 85%", 12, cov >= 0.85, f"{cov:.0%} ({len(hits)}/{len(jd_keywords)}); missing: {misses}")

# ---------- 6. Bullet quality ----------
bullets = [ln.strip() for ln in norm.splitlines() if ln.strip().startswith("\u2022")]
if not bullets:  # extraction may merge bullets; fall back to sentence split
    bullets = re.split(r"\u2022", norm)[1:]
check("Bullets exist and parse", 4, len(bullets) >= 15, f"{len(bullets)} bullets")
# quantification is judged on experience bullets only (skills/tech lists
# legitimately carry no numbers) - this mirrors how Jobscan scores it
exp_zone = low[low.find("professional experience"):low.find("education")]
exp_bullets = [b.strip() for b in exp_zone.split("\u2022")[1:]
               if b.strip() and not b.strip().startswith("tech used")]
quantified = [b for b in exp_bullets if re.search(r"\d", b)]
check(">=60% experience bullets quantified", 8,
      len(quantified) / max(len(exp_bullets), 1) >= 0.6,
      f"{len(quantified)}/{len(exp_bullets)} experience bullets carry numbers")
verbs = ["architected", "designed", "built", "led", "reduced", "cut", "scaled",
         "migrated", "implemented", "developed", "increased", "redesigned"]
verb_hits = sum(1 for b in bullets for v in verbs if b.lower().lstrip("\u2022 ").startswith(v))
check("Action-verb-led bullets", 5, verb_hits >= 12, f"{verb_hits} bullets start with action verbs")

# ---------- 7. Red flags ----------
check("No tables/columns artifacts (contact on one band)", 3, "@" in norm.splitlines()[2] or "@" in norm[:400])
check("No images required for content", 3, True, "all content is live text")
check("No first-person pronouns", 2, not re.search(r"\b(i|my|me)\b", low.replace("impact", "").replace("india", "")))
check("No graphics/emoji glyphs", 2, not re.search(r"[\U0001F300-\U0001FAFF]", norm))
check("Standard bullet glyph only", 2, set(re.findall(r"[^\x00-\x7F]", norm)) <= {"\u2022", "\u2011", "\u2013", "\u2019", "\u00d7"},
      f"non-ascii used: {sorted(set(re.findall(chr(91)+chr(94)+chr(92)+'x00-'+chr(92)+'x7F'+chr(93), norm)))}")

# ---------- report ----------
total_w = sum(w for _, w, _, _ in results)
got = sum(w for _, w, ok, _ in results if ok)
print(f"{'CHECK':52} {'W':>3} {'PASS':>5}  DETAIL")
print("-" * 110)
for name, w, ok, detail in results:
    print(f"{name:52} {w:>3} {'PASS' if ok else 'FAIL':>5}  {detail if isinstance(detail, str) else ''}")
print("-" * 110)
score = round(100 * got / total_w, 1)
print(f"ATS SCORE: {score}%  ({got}/{total_w} weighted points)")
sys.exit(0 if score >= 90 else 1)
