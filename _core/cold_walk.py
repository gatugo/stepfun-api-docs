#!/usr/bin/env python3
"""Cold walk test — can an agent with zero memory route from the map alone?

The acid test: a fresh instance opens the workspace, reads only the entry map,
and must answer "where do I go for task X?" correctly. This script does the
mechanical half — it verifies the map is self-sufficient — and prints the probe
list a human (or a fresh agent session) should run.

Usage:
    python3 _core/cold_walk.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_PATH = ROOT / "CLAUDE.md"

# Probes a fresh agent must be able to route. Each names a file the routing
# table must point at. Add to this list whenever a new card is added.
PROBES = [
    ("which plan am I on", "bundle/always-load/plan.md"),
    ("how do I authenticate", "bundle/always-load/auth.md"),
    ("which base URL do I use", "bundle/always-load/endpoints.md"),
    ("which models can I call", "bundle/always-load/models.md"),
    ("connect Claude Code", "bundle/by-task/client-setup.md"),
    ("chat completions / messages / responses", "bundle/by-task/chat-apis.md"),
    ("force JSON output", "bundle/by-task/structured-output.md"),
    ("stream a response", "bundle/by-task/streaming.md"),
    ("call a tool / function", "bundle/by-task/tool-calling.md"),
    ("set reasoning effort", "bundle/by-task/reasoning.md"),
    ("multi-turn context / prompt cache", "bundle/by-task/context-and-cache.md"),
    ("send an image to a model", "bundle/by-task/vision-and-video.md"),
    ("text to speech / transcribe", "bundle/by-task/audio.md"),
    ("generate or edit an image", "bundle/by-task/images.md"),
    ("upload a file", "bundle/by-task/files.md"),
    ("I got a 404 / 429 / 400", "bundle/by-task/errors-and-debugging.md"),
    ("deploy a static site", "bundle/by-task/static-hosting.md"),
    ("port from OpenAI", "bundle/by-task/openai-migration.md"),
    ("step command flags", "bundle/evidence/reference/step-code.md"),
    ("is stepaudio-3 available", "bundle/evidence/models/not-on-this-plan.md"),
    ("build a voice pipeline", "bundle/by-task/voice-pipeline.md"),
    ("what replaces step-image-edit-2", "bundle/evidence/models/step-image-edit-2.md"),
    ("why do two sources disagree", "bundle/evidence/source-contradictions.md"),
]


def main() -> int:
    if not CLAUDE_PATH.exists():
        print("FAIL: CLAUDE.md missing — there is no map to walk")
        return 1

    text = CLAUDE_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    failures = 0

    print(f"CLAUDE.md is {len(lines)} lines (budget 60)\n")

    print("[1] Does the map name the plan identity?")
    for fact in ("Step Plan Oversea", "platform.stepfun.ai", "step-5-preview"):
        if fact in text:
            print(f"  ok    states: {fact}")
        else:
            print(f"  FAIL  does not state: {fact}")
            failures += 1

    print("\n[2] Does the map name its own layers?")
    for layer in ("always-load", "by-task", "evidence"):
        if layer in text:
            print(f"  ok    routes to tier: {layer}")
        else:
            print(f"  FAIL  no route to tier: {layer}")
            failures += 1

    print("\n[3] Routing-table coverage of the probe list")
    routing_rows = [l for l in lines if l.startswith("|") and "`bundle/" in l]
    print(f"  {len(routing_rows)} routing row(s) reference bundle cards")
    for task, expected in PROBES:
        target = ROOT / expected
        if not target.exists():
            print(f"  FAIL  {task}: card missing -> {expected}")
            failures += 1
            continue
        stem = Path(expected).stem
        if any(stem in row for row in routing_rows):
            print(f"  ok    {task:38s} -> {expected}")
        else:
            print(f"  FAIL  {task:38s} -> no routing row for {expected}")
            failures += 1

    print("\n[4] Is the map a map (not a document)?")
    budget = 60
    if len(lines) > budget:
        print(f"  FAIL  {len(lines)} lines exceeds {budget} — trim the map")
        failures += 1
    else:
        print(f"  ok    {len(lines)}/{budget} lines")
    prose = [l for l in lines if l.startswith((" ", "\t")) and len(l) > 120]
    if prose:
        print(f"  FAIL  {len(prose)} long indented prose block(s) — content belongs in a card")
        failures += 1
    else:
        print("  ok    no long prose blocks")

    print("\n[5] Model allowlist present")
    models = ROOT / "bundle/always-load/models.md"
    if models.exists() and re.search(r"step-5-preview", models.read_text(encoding="utf-8")):
        print("  ok    always-load/models.md defines the allowlist")
    else:
        print("  FAIL  always-load/models.md missing or empty")
        failures += 1

    print("\n" + "=" * 62)
    if failures:
        print(f"{failures} cold-walk failure(s). Fix CLAUDE.md, not the probe.")
        print("Then run a live check: open a fresh session here and ask")
        print('  "What is this folder and how do I <task>?"')
        return 1
    print("Cold walk passed the mechanical half.")
    print("Live half: open a brand-new agent session in this folder and ask")
    print('  "What is this folder, and how do I add streaming?"')
    print("It should read CLAUDE.md, name the plan, and route to")
    print("bundle/by-task/streaming.md with no help.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
