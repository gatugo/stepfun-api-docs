# StepFun API — task-routed knowledge bundle

Documentation for the StepFun API, organised so an AI coding agent can find the
one answer it needs without loading 115 pages of vendor docs — and verified
against a live subscription rather than the marketing site.

## The problem this solves

The StepFun docs describe the **platform**. Your key can call a **subset** of it,
and that subset is written down nowhere in the docs. An agent that reads only the
docs will confidently hand you a model name that returns 404.

Three recorded examples, each settled by a live call and filed with its evidence:

| The docs say | Reality on this account |
| :- | :- |
| `step-router-v1` is "available only through Step Plan" | **Not callable on either channel** |
| The Responses API is Standard-channel-only | **Works on Step Plan too** — HTTP 200 |
| The image API retires 2026-10-10 | **Already dead** — HTTP 400 on both channels |

There is a second, cheaper-to-see problem: the docs are 115 pages. Pasting them
into context costs roughly **239,000 tokens per question**. A routed answer costs
roughly **6,000**.

## What this is

A layered set of Markdown cards, plus two deterministic gates that keep it honest:

```
CLAUDE.md              routing map — the one file an agent reads first
bundle/always-load/    6 cards, read on every task
bundle/by-task/        16 cards, one job each
bundle/evidence/       5 cards — contradictions and off-plan models
_account/              rank-1 facts from live calls — outranks the vendor docs
corpus/                115 vendor pages, fetched, never hand-edited
```

The `_account/` layer is what makes this correct for a *subscription* rather than
a platform. When the docs and a live call disagree, the live call wins, and the
disagreement is recorded instead of silently resolved.

Architecture: [`showcase/HOW-IT-WORKS.md`](showcase/HOW-IT-WORKS.md).

## Try it in ten minutes

[`showcase/TRY-IT.md`](showcase/TRY-IT.md) is a self-falsifying test: run two
scripts, ask an agent three questions, then open the cited file and check every
claim yourself.

```bash
python3 _core/check_integrity.py    # 6 structural checks, no LLM
python3 _core/cold_walk.py          # 23 routing probes
```

## Use it

| I want to… | Go to |
| :- | :- |
| Just ask questions in my agent | Clone it and point your agent at it — [`showcase/HOW-TO-USE.md`](showcase/HOW-TO-USE.md) |
| Adopt it into my project | [`showcase/HOW-TO-USE.md`](showcase/HOW-TO-USE.md), Path 2 |
| Rebuild the method for another API | [`showcase/HOW-TO-USE.md`](showcase/HOW-TO-USE.md), Path 3 |
| See the measured numbers | [`showcase/DEMO.md`](showcase/DEMO.md) |
| Know how it was built, end to end | [`showcase/HOW-IT-WAS-BUILT.md`](showcase/HOW-IT-WAS-BUILT.md) |
| Know what is still unsettled | [`open_questions.md`](open_questions.md) |
| Know what was decided, and when | [`decisions.md`](decisions.md) |
| Submit a correction | [`CONTRIBUTING.md`](CONTRIBUTING.md) |

## Status

Verified against a live StepFun subscription on 2026-10-13 — 25 cards, 115 corpus
pages, both gates green. 15 models callable on the Standard channel, 6 on Step
Plan. What the docs get wrong is tracked in
[`bundle/evidence/source-contradictions.md`](bundle/evidence/source-contradictions.md);
what nobody has answered yet is tracked in
[`open_questions.md`](open_questions.md).

---

<details>
<summary><strong>For agents</strong> — the read order</summary>

Read [`AGENTS.md`](AGENTS.md) first. It names the order: `CLAUDE.md` (routing map)
→ `bundle/always-load/` → the one `bundle/by-task/` card your task matches.

[`PURPOSE.md`](PURPOSE.md) says what this is;
[`skills/redeploy.md`](skills/redeploy.md) says how to stand it up in any folder.

</details>

---

*This file is the landing page, not a second front door. It carries orientation
and links; every substantive fact lives in exactly one card. See `decisions.md`,
2026-10-13.*
