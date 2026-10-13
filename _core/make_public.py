#!/usr/bin/env python3
"""Generate a scrubbed, publishable copy of this bundle.

The private original is never modified. Everything happens on the copy, and the
script fails loudly rather than shipping a leak.

Usage:
    python3 _core/make_public.py              # build ../stepfun-api-v2-standard-public
    python3 _core/make_public.py --out PATH   # build somewhere else
    python3 _core/make_public.py --no-gates   # skip running gates in the copy

What it does:
  1. Copies the tree, excluding .git/, __pycache__/, *.pyc. .github/ is KEPT —
     CI should run on the public copy.
  2. Drops HANDOFF.md (internal working state) and strips links that pointed at it.
  3. Rewrites any absolute /home/<user>/... paths to generic /path/to/...
  4. Asserts the copy contains no personal data. Fails on any hit.
  5. Runs both gates in the copy and reports.

Idempotent: the output directory is rebuilt from scratch each run.

Note on _account/: it is KEPT intact. It holds live-call evidence — HTTP status
codes, model IDs, endpoint shapes — which contains no personal data and is the
bundle's strongest asset. The scrub assertion below is what actually protects it:
if a key, home path, address, or email ever lands in there, the build fails.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT.parent / "stepfun-api-v2-standard-public"

# Files/dirs that never ship in the public copy.
# _site is the generated static site (showcase/build_site.py output) — it is
# gitignored upstream and regenerable, so it does not belong in a repo people
# clone. Anyone who wants the HTML runs the build script.
# _session is working scratch — where we left off, not part of the product.
EXCLUDE_DIRS = {".git", "__pycache__", "_site", "_session"}
EXCLUDE_FILES = {"HANDOFF.md"}

# ---------------------------------------------------------------------------
# Scrub patterns. Anything matching these fails the build.
# ---------------------------------------------------------------------------
SCRUB_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("Linux home path", re.compile(r"/home/[A-Za-z0-9._-]+"),
     "use a relative path or /path/to/<project>"),
    ("API key", re.compile(r"\b(sk-[A-Za-z0-9]{16,}|sk_live_[A-Za-z0-9]{8,})"),
     "keys live in the environment, never in a file"),
    ("Private IP", re.compile(r"\b(192\.168\.|10\.0\.0\.|172\.(1[6-9]|2\d|3[01])\.)"),
     "no network addresses in docs"),
    ("Personal email", re.compile(r"\b[A-Za-z0-9._%+-]+@(?!stepfun\.com|example\.com|example\.org)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
     "no personal addresses"),
]

# Known-safe literal that must survive the email check. The noreply address is
# the pinned author of the published commit — see _core/publish.sh.
SAFE_EMAILS = {"platform@stepfun.com", "you@example.com",
               "stepfun-api-docs@users.noreply.github.com"}


def ignore(_dir: str, names: list[str]) -> set[str]:
    dropped = set()
    for n in names:
        if n in EXCLUDE_DIRS or n in EXCLUDE_FILES:
            dropped.add(n)
        elif n.endswith((".pyc", ".pyo")):
            dropped.add(n)
    return dropped


def rewrite_paths(text: str) -> str:
    """Absolute home paths -> generic. Also de-references the bundle by name."""
    text = re.sub(r"/home/[A-Za-z0-9._-]+/[^\s`)\"']*stepfun-api-v2-standard",
                  "/path/to/stepfun-api-v2-standard", text)
    text = re.sub(r"/home/[A-Za-z0-9._-]+/dev/workspaces?",
                  "/path/to/workspace", text)
    text = re.sub(r"/home/[A-Za-z0-9._-]+(?=/|\b|$)", "/path/to/home", text)
    return text


def strip_handoff_links(text: str) -> str:
    """Remove markdown links that pointed at the dropped HANDOFF.md."""
    text = re.sub(r"\s*\[[^\]]*\]\([^)]*HANDOFF\.md\)", "", text)
    text = re.sub(r"\s*\[[^\]]*\]\(\.\./[^)]*HANDOFF\.md\)", "", text)
    return text


def build(out: Path, run_gates: bool) -> int:
    if not ROOT.name or ROOT == out:
        print(f"refusing to write to {out}", file=sys.stderr)
        return 1

    if out.exists():
        print(f"removing existing {out}")
        shutil.rmtree(out)

    print(f"copying {ROOT.name}/ -> {out.name}/")
    shutil.copytree(ROOT, out, ignore=ignore)

    problems: list[str] = []

    # --- 1. Scrub paths in every markdown and script file ------------------
    scrubbed = 0
    for path in sorted(out.rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".py", ".sh", ".yml"}:
            continue
        if ".git" in path.parts:
            continue
        original = path.read_text(encoding="utf-8", errors="replace")
        updated = rewrite_paths(original)
        updated = strip_handoff_links(updated)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            scrubbed += 1
    print(f"scrubbed absolute paths in {scrubbed} file(s)")

    # --- 2. Assert the copy is clean ---------------------------------------
    print("\nscrub assertions")
    for path in sorted(out.rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".py", ".sh", ".yml", ".txt"}:
            continue
        if ".git" in path.parts:
            continue
        rel = path.relative_to(out)
        for n, line in enumerate(path.read_text(encoding="utf-8",
                                                errors="replace").splitlines(), 1):
            for label, pattern, advice in SCRUB_PATTERNS:
                m = pattern.search(line)
                if m and m.group(0) not in SAFE_EMAILS:
                    problems.append(f"{rel}:{n}: {label} ({m.group(0)!r}) — {advice}")

    if problems:
        print("\n".join(f"  FAIL  {p}" for p in problems))
        print(f"\n{len(problems)} personal-data hit(s). Refusing to ship.")
        return 1
    print("  ok    no home paths, keys, private IPs, or personal emails")

    # --- 3. Gates in the copy ----------------------------------------------
    if run_gates:
        for script in ("check_integrity.py", "cold_walk.py"):
            print(f"\n$ python3 _core/{script}   (in {out.name}/)", flush=True)
            r = subprocess.run([sys.executable, f"_core/{script}"], cwd=out)
            if r.returncode != 0:
                problems.append(f"{script} failed in the public copy")

    print("\n" + "=" * 62)
    if problems:
        print(f"{len(problems)} problem(s).")
        return 1
    print(f"Public copy ready: {out}")
    print("Review it, then commit it as its own repo if you want it public.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--no-gates", action="store_true")
    args = ap.parse_args()
    return build(args.out, run_gates=not args.no_gates)


if __name__ == "__main__":
    raise SystemExit(main())
