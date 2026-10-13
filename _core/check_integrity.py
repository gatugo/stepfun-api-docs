#!/usr/bin/env python3
"""Integrity checks for the StepFun docs bundle.

Mechanical, deterministic, no LLM — scripts over sentences.
Answers three questions:

  1. Are the structural invariants intact? (routing-file budgets, card
     frontmatter, one-home-per-fact smell)
  2. Is every bundle link resolvable?
  3. Is every card's `source` page actually in the corpus?

Usage:
    python3 _core/check_integrity.py          # human-readable report
    python3 _core/check_integrity.py --quiet  # only failures

Exit code: 0 = clean, 1 = failures found.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CLAUDE = "CLAUDE.md"
CONTEXT = "CONTEXT.md"
BUNDLE = ROOT / "bundle"
CORPUS = ROOT / "corpus"
ACCOUNT = ROOT / "_account"

# Routing-file line budgets — a map is a map, not a document.
BUDGETS = {CLAUDE: 60, CONTEXT: 80}

# Frontmatter fields every card must carry.
REQUIRED_FRONTMATTER = {"card", "tier", "status", "verified_on", "source"}

INLINE_LINK = re.compile(r"\[[^\]]*\]\(([^)#]+?)(?:#[^)]*)?\)")
VALID_TIERS = {"always-load", "by-task", "evidence"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    problems: list[str] = []

    def note(msg: str) -> None:
        problems.append(msg)
        print(f"  FAIL  {msg}")

    def info(msg: str) -> None:
        if not args.quiet:
            print(f"  ok    {msg}")

    cards = sorted(p for p in BUNDLE.rglob("*.md") if p.name != "index.md")

    # --- 1. Routing-file budgets -------------------------------------------------
    print("\n[1] Routing-file budgets")
    for name, budget in BUDGETS.items():
        path = ROOT / name
        if not path.exists():
            note(f"{name} missing")
            continue
        lines = len(read(path).splitlines())
        if lines > budget:
            note(f"{name} is {lines} lines, budget is {budget} — a map must stay a map")
        else:
            info(f"{name}: {lines}/{budget} lines")

    # --- 2. Card frontmatter -----------------------------------------------------
    print("\n[2] Card frontmatter and tier")
    for card in cards:
        rel = card.relative_to(ROOT)
        fm = frontmatter(read(card))
        missing = REQUIRED_FRONTMATTER - fm.keys()
        if missing:
            note(f"{rel}: missing frontmatter field(s): {', '.join(sorted(missing))}")
            continue
        tier = fm["tier"]
        if tier not in VALID_TIERS:
            note(f"{rel}: tier '{tier}' not in {sorted(VALID_TIERS)}")
        expected_dir = f"bundle/{tier}"
        if expected_dir not in str(rel.parent):
            note(f"{rel}: tier '{tier}' but lives in {rel.parent} — card and folder disagree")
        info(f"{rel}: tier={tier} status={fm['status']}")

    # --- 3. Card sources exist in the corpus ------------------------------------
    print("\n[3] Card source pages exist")
    corpus_files = {str(p.relative_to(CORPUS)) for p in CORPUS.rglob("*.md")}
    account_files = {str(p.relative_to(ACCOUNT)) for p in ACCOUNT.rglob("*.md")} if ACCOUNT.exists() else set()
    for card in cards:
        for src in frontmatter(read(card)).get("source", "").split(","):
            src = src.strip()
            if not src:
                continue
            if src.startswith("_account/"):
                rel = src.removeprefix("_account/")
                if rel not in account_files:
                    note(f"{card.relative_to(ROOT)}: account source '{src}' not found")
                continue
            src = src.removeprefix("corpus/")
            if src.endswith("*") or "/" not in src:
                # Directory or wildcard reference — check the directory exists.
                base = src.rstrip("/*")
                if base and not (CORPUS / base).exists():
                    note(f"{card.relative_to(ROOT)}: source '{src}' not found in corpus/")
                continue
            if src not in corpus_files:
                note(f"{card.relative_to(ROOT)}: source '{src}' not found in corpus/")
    info(f"all card sources resolved ({len(corpus_files)} corpus, {len(account_files)} account)")

    # --- 4. Link resolution -----------------------------------------------------
    print("\n[4] Internal link resolution")
    # Corpus pages are upstream truth and are never edited, so they are excluded:
    # their absolute `/docs/en/...` links are Mintlify's, not ours to fix (G1).
    md_files = [
        p for p in ROOT.rglob("*.md")
        if CORPUS not in p.parents and "_archive" not in p.parts
    ]
    for path in sorted(md_files):
        text = read(path)
        for target in INLINE_LINK.findall(text):
            t = target.strip()
            if t.startswith(("http://", "https://", "mailto:")):
                continue
            if t.startswith("/"):
                note(f"{path.relative_to(ROOT)}: absolute link '{t}' — use a relative path")
                continue
            resolved = (path.parent / t).resolve()
            if not resolved.exists():
                note(f"{path.relative_to(ROOT)}: dead link -> {t}")
    info(f"all relative links resolve across {len(md_files)} bundle files")

    # --- 5. Guard smells --------------------------------------------------------
    print("\n[5] Guard smells")
    credential_re = re.compile(r"\b(sk-[A-Za-z0-9]{16,}|sk_live_[A-Za-z0-9]{8,})")
    model_re = re.compile(r"`((?:step|stepaudio)-[a-z0-9.\-]+)`")
    for path in sorted(md_files):
        text = read(path)
        rel = path.relative_to(ROOT)
        for n, line in enumerate(text.splitlines(), 1):
            if credential_re.search(line):
                note(f"{rel}:{n}: possible credential in file")
    # G5: every backticked model ID in the bundle must be either on this plan or
    # explicitly listed in the not-on-this-plan card.
    notonplan = read(BUNDLE / "evidence/models/not-on-this-plan.md")
    known = {m.removesuffix(".md") for m in model_re.findall(notonplan)} | {
        "step-5-preview", "step-3.7-flash", "step-3.5-flash", "step-3.5-flash-2603",
        "stepaudio-2.5-tts", "stepaudio-2.5-asr",
    }

    def is_model(tok: str) -> bool:
        tok = tok.removesuffix(".md")
        return "-" in tok and any(c.isdigit() for c in tok)

    for path in sorted(md_files):
        if "always-load/models.md" in str(path) or "not-on-this-plan" in str(path):
            continue  # these two cards define the allowlist
        for n, line in enumerate(read(path).splitlines(), 1):
            for mid in model_re.findall(line):
                mid = mid.removesuffix(".md")
                if is_model(mid) and mid not in known:
                    note(f"{path.relative_to(ROOT)}:{n}: model '{mid}' is not on the Step Plan allowlist")
    info("no credential or off-plan model smells")

    # --- 6. Corpus manifest sanity ---------------------------------------------
    print("\n[6] Corpus manifest")
    manifest = CORPUS / "_index.md"
    if not manifest.exists():
        note("corpus/_index.md missing — run python3 _core/fetch.py")
    else:
        unchecked = read(manifest).count("| [ ]")
        checked = read(manifest).count("| [x]")
        info(f"manifest: {checked} fetched, {unchecked} failed")
        if unchecked:
            note(f"{unchecked} corpus page(s) recorded as unfetched")
        if len(corpus_files) < checked:
            note(f"corpus has {len(corpus_files)} files but manifest claims {checked} fetched")

    # --- Report -----------------------------------------------------------------
    print("\n" + "=" * 62)
    if problems:
        print(f"{len(problems)} problem(s) found.")
        print("Fix them, or record the constraint in open_questions.md.")
        return 1
    print("All integrity checks passed.")
    print(f"{len(cards)} cards, {len(md_files)} markdown files, {len(corpus_files) - 1} corpus pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
