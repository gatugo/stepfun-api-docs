# Contributing

This bundle is only worth having if it stays accurate. Corrections are the main
contribution, and there is a pipeline for them rather than free-hand edits.

## The rule that matters most

**Never resolve an availability question from the vendor docs alone.** The corpus
describes the *platform*; `_account/` describes what *your key* can call. When they
disagree, `_account/` wins and the disagreement gets recorded — not quietly
edited away.

## Before you start

```bash
python3 _core/check_integrity.py   # must be clean
python3 _core/cold_walk.py         # 23/23 probes
```

If these are red, fix that first.

## Correcting a fact

The extraction pipeline is a skill: [`skills/refresh-a-card.md`](skills/refresh-a-card.md).
In short:

1. **Name the task, not the page.** "How do I do structured output?" →
   `bundle/by-task/structured-output.md`. One card, one job.
2. **Read the corpus page(s)** that cover it. Note their exact paths.
3. **Pick the tier.** Needed on every task → `always-load/`. Per-task → `by-task/`.
   Deep reference → `evidence/`.
4. **Write the card** with frontmatter (`card`, `tier`, `status`, `verified_on`,
   `source`). Lead with the answer. Tables over prose for anything with more than
   two attributes. Link to siblings; never copy their facts.
5. **Add the routing row** to `CLAUDE.md` if the task was not routable before —
   keeping it under 60 lines.
6. **Run both gates.**
7. **Log it** in `decisions.md` if the change alters the workspace's shape or a
   previously-stated fact.

## Settling a dispute with a live call

This is the highest-value contribution you can make.

1. Make the call. Record the exact request, status code, and response.
2. Write the evidence to `_account/live-calls/<date>-<what>.md`.
3. Correct the card that carried the wrong value; bump its `verified_on`.
4. **Log the contradiction** in
   [`bundle/evidence/source-contradictions.md`](bundle/evidence/source-contradictions.md)
   with **both values, both sources, and which one won.**
5. Run both gates.

Step 4 is the one people skip. A silent overwrite destroys the information that
there was ever a dispute — and that is exactly the information the next reader
needs.

## Hard rules

| # | Rule |
|---|---|
| G1 | Never hand-edit anything under `corpus/` — regenerate with `python3 _core/fetch.py` |
| G3 | Never write a credential, API key, or token into any file |
| G9 | Never duplicate a fact across cards — one fact, one home |
| G10 | Never mark a card `verified` without reading its `source` page this session |
| — | Never invent a parameter, price, or limit. If a source is silent, write "not documented" and park it in `open_questions.md` |

The full set is in [`_config/guard-rules.md`](_config/guard-rules.md).

## Pull requests

- One logical change per PR.
- Both gates green — CI runs them automatically.
- If you changed a card, say which corpus page you read.
- If you settled a dispute, link the evidence file.

## Reporting a problem without a fix

Open an issue with: the question you asked, the answer the bundle gave, and what
you expected instead. That is enough to route it.
