#!/usr/bin/env python3
"""Build a static site from the showcase folder.

Plain HTML + CSS, no build step beyond this script, so the output is reviewable
as files. Reproducible: delete the output and re-run.

Usage:
    python3 showcase/build_site.py            # writes showcase/_site/
    python3 showcase/build_site.py --out DIR

Links that point outside the showcase (../bundle/..., ../CONTRIBUTING.md) are
rewritten to a non-navigable marker, because the site is standalone and those
paths only exist in the repo.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("python3 -m pip install markdown")

HERE = Path(__file__).resolve().parent

# (nav label, source markdown, output html)
PAGES = [
    ("Overview", "README.md", "index.html"),
    ("How it works", "HOW-IT-WORKS.md", "how-it-works.html"),
    ("How to use it", "HOW-TO-USE.md", "how-to-use.html"),
    ("Demo", "DEMO.md", "demo.html"),
    ("FAQ", "FAQ.md", "faq.html"),
]

CSS = """\
:root {
  --bg: #ffffff; --fg: #1a1d21; --muted: #5b6470; --line: #e3e7ec;
  --accent: #0b6bcb; --code-bg: #f5f7fa; --pre-bg: #1e2430;
}
@media (prefers-color-scheme: dark) {
  :root { --bg: #14171c; --fg: #e6e9ee; --muted: #9aa4b2; --line: #2a3038;
          --accent: #5aa9f8; --code-bg: #1c2129; --pre-bg: #0d1117; }
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font: 16px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        "Helvetica Neue", Arial, sans-serif;
}
.wrap { max-width: 860px; margin: 0 auto; padding: 0 24px 80px; }
header.site { border-bottom: 1px solid var(--line); margin-bottom: 36px; }
header.site .wrap { padding-bottom: 18px; }
.brand { font-weight: 650; font-size: 17px; letter-spacing: -.01em; }
.brand a { color: var(--fg); text-decoration: none; }
nav { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 4px 18px; }
nav a { color: var(--muted); text-decoration: none; font-size: 14.5px; }
nav a:hover { color: var(--accent); }
nav a.on { color: var(--accent); font-weight: 600; }
main h1 { font-size: 30px; line-height: 1.25; margin: 0 0 8px; letter-spacing: -.02em; }
main h2 { font-size: 21px; margin: 40px 0 12px; padding-bottom: 6px;
          border-bottom: 1px solid var(--line); letter-spacing: -.01em; }
main h3 { font-size: 17px; margin: 28px 0 8px; }
main p { margin: 0 0 14px; }
main ul, main ol { margin: 0 0 16px; padding-left: 24px; }
main li { margin: 4px 0; }
a { color: var(--accent); }
code { background: var(--code-bg); padding: 2px 5px; border-radius: 4px;
       font: 13.5px/1.5 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
pre { background: var(--pre-bg); color: #e6edf3; padding: 16px; border-radius: 8px;
      overflow-x: auto; margin: 0 0 18px; }
pre code { background: none; padding: 0; color: inherit; font-size: 13px; }
table { border-collapse: collapse; width: 100%; margin: 0 0 18px; font-size: 14.5px; }
th, td { border: 1px solid var(--line); padding: 8px 11px; text-align: left;
         vertical-align: top; }
th { background: var(--code-bg); font-weight: 600; }
blockquote { margin: 0 0 16px; padding: 10px 16px; border-left: 3px solid var(--accent);
             background: var(--code-bg); border-radius: 0 6px 6px 0; }
blockquote p { margin: 0; }
hr { border: none; border-top: 1px solid var(--line); margin: 34px 0; }
.repo-note { color: var(--muted); font-size: 13.5px; font-style: italic; }
footer.site { border-top: 1px solid var(--line); margin-top: 48px; padding-top: 18px;
              color: var(--muted); font-size: 13.5px; }
footer.site .wrap { padding-bottom: 0; }
"""

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — StepFun API knowledge bundle</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site"><div class="wrap">
  <div class="brand"><a href="index.html">StepFun API — task-routed knowledge bundle</a></div>
  <nav>{nav}</nav>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">
  Built from <code>showcase/</code> by <code>showcase/build_site.py</code>.
  Every figure on the Demo page is measured from the repository, not typed by hand.
</div></footer>
</body>
</html>
"""


def fix_links(html: str, current: str) -> str:
    """Point .md links at .html pages; neutralise links that leave the site."""
    for _, src, out in PAGES:
        html = html.replace(f'href="{src}"', f'href="{out}"')
    # Links out of the showcase (../bundle/..., ../CONTRIBUTING.md) cannot
    # resolve on a standalone site — mark them instead of shipping dead links.
    html = re.sub(
        r'<a href="(\.\./[^"]+)">(.*?)</a>',
        r'<span class="repo-note">\2 <em>(in the repository)</em></span>',
        html,
    )
    html = html.replace('href="demo.sh"', 'href="#"')
    return html


def build(out: Path) -> int:
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])

    nav_items = []
    for label, _, out_name in PAGES:
        nav_items.append((label, out_name))

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    for label, src, out_name in PAGES:
        src_path = HERE / src
        if not src_path.exists():
            print(f"  MISSING {src}")
            return 1
        md.reset()
        body = md.convert(src_path.read_text(encoding="utf-8"))
        body = fix_links(body, out_name)

        nav = " ".join(
            f'<a href="{n}" class="{"on" if n == out_name else ""}">{lbl}</a>'
            for lbl, n in nav_items
        )
        title = "Overview" if out_name == "index.html" else label
        (out / out_name).write_text(
            TEMPLATE.format(title=title, nav=nav, body=body), encoding="utf-8"
        )
        print(f"  wrote {out_name:<20} <- {src}")

    (out / "style.css").write_text(CSS, encoding="utf-8")
    print(f"  wrote style.css")
    print(f"\nSite ready: {out}")
    print("Open index.html locally, or deploy the folder.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "_site")
    args = ap.parse_args()
    return build(args.out)


if __name__ == "__main__":
    raise SystemExit(main())
