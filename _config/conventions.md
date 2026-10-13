---
layer: 3
role: factory-config
---

# Conventions — stable across every run

Layer 3. These rules do not change per task; the bundle's shape depends on them.

## Naming

| Thing | Rule | Example |
| --- | --- | --- |
| Task cards | `kebab-case.md`, one job per card | `structured-output.md` |
| Tier folders | `always-load/` → `by-task/` → `evidence/` | — |
| Corpus folders | mirror `llms.txt` sections | `step-plan/`, `step-code/`, `api-reference/` |
| Model IDs | verbatim, in backticks | `step-3.5-flash-2603` |
| Meta folders | underscore prefix = about the workspace, not of the work | `_config/`, `_core/`, `_archive/` |
| Retired work | `_archive/`, never read | — |

## Card frontmatter

Every card carries it:

```yaml
---
card: <kebab-case-name>
tier: always-load | by-task | evidence
status: verified | stale | disputed
verified_on: YYYY-MM-DD
source: corpus/<path>.md
---
```

`source` is mandatory. A card without a source is an opinion, not knowledge.

## Writing rules

1. **One fact, one home.** If two cards need the same fact, one links to the other.
2. **Link, don't copy.** `[`auth.md`](../bundle/always-load/auth.md)` beats pasting the Base URL.
3. **Never restate corpus prose.** Summarise and point. The corpus page is the evidence.
4. **State the negative when it matters.** "Not on this plan" is a fact worth a card —
   see `bundle/evidence/models/not-on-this-plan.md`.
5. **Keep routing files pointer-only.** `CLAUDE.md` ≤ 60 lines, `CONTEXT.md` ≤ 80.
   If a routing file grows, the content belongs in a card.
6. **Prefer a table over prose** for anything with more than two attributes.
7. **No credentials, ever** — not in a card, not in a commit message, not in
   `decisions.md`.

## Token discipline

Healthy load per task: **2,000–8,000 tokens**. Tier A ≈ 2.5k, one Tier B card
≈ 1–3k. If a task needs more than ~8k, the card is too broad — split it.

## Status lifecycle

`verified` (checked against corpus, dated) → `stale` (corpus newer than
`verified_on`, or a `fetch.py` run added/removed pages) → back to `verified`
after a re-read. `disputed` means corpus and card disagree — the **corpus wins**
until resolved; log the conflict in `decisions.md`.

## Authority order — which source wins

Used whenever two sources disagree about the same fact.

| Rank | Source | Authority over |
| --- | --- | --- |
| 1 | `_account/` — recorded dashboard snapshots | **What this account can call, and at what quota.** Outranks everything for availability. |
| 2 | `corpus/` — the platform docs | How the API behaves: params, defaults, endpoints, error codes. |
| 3 | `bundle/` cards | Nothing — they are derived. A card never beats its source. |

Worked example: `corpus/api-reference/chat/messages-create.md` says
`step-router-v1` is available only through Step Plan, but `_account/` does not
list it. Rule 1 wins → the model is treated as unavailable here, and the card is
marked `disputed` rather than silently rewritten.

Rule 2 still governs *behaviour*: a corpus page is right that `max_tokens` is
required on the Messages API even though the account snapshot says nothing about
it.
