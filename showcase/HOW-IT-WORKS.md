# How it works

Three ideas. They are the whole design, and each one exists because of a specific
way naive agent-docs setups fail.

---

## Idea 1 — Tier the knowledge so an agent loads only what the task needs

A flat pile of documentation forces a choice: load everything (expensive) or guess
(unsafe). This bundle removes the choice by sorting every fact into a tier by
*when it is needed*.

```
                    ┌─────────────────────────────┐
   every question → │  CLAUDE.md  (routing map)   │  ~690 tok
                    └──────────────┬──────────────┘
                                   │ routes to a tier
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
    ┌──────────────────┐  ┌────────────────┐  ┌──────────────────┐
    │  always-load/    │  │   by-task/     │  │    evidence/     │
    │  loaded on EVERY │  │  the ONE card  │  │  only when a     │
    │  task            │  │  that matches  │  │  fact is disputed│
    │  ~4,500 tok      │  │  ~500 tok      │  │  on demand       │
    └──────────────────┘  └────────────────┘  └──────────────────┘
              │                    │                    │
              └────────────────────┴────────────────────┘
                                   │ facts trace back to
                    ┌──────────────▼──────────────┐
                    │  corpus/  (115 vendor pages)│  ~239,000 tok
                    │  _account/ (live-call facts)│  rank 1
                    └─────────────────────────────┘
```

**The routing map is a map, not a document.** `CLAUDE.md` is capped at 60 lines
and holds *only* a routing table — no facts, no code, no prose. If it grows, the
content belongs in a card. This is enforced by a script, not by discipline.

A routing table row looks like this:

| When the task is… | Read these |
|---|---|
| Which model can I call | `bundle/always-load/models.md` |
| Stream a response | `bundle/by-task/streaming.md` |
| Why do two sources disagree | `bundle/evidence/source-contradictions.md` |

**One fact, one home.** If two cards need the same fact, one links to the other
rather than repeating it. Two copies drift, and then an agent picks one at random
and you cannot tell which. This is a hard rule (G9) and the most important one in
the set.

---

## Idea 2 — Rank the sources, so availability never comes from the docs

This is the idea that makes the bundle worth having.

Vendor documentation describes **the platform**. It cannot describe **your
subscription**. Those are different things, and conflating them is the single most
common failure when an agent answers API questions from public docs.

So every fact has a rank:

| Rank | Source | Authority over | Example |
|---|---|---|---|
| **1** | `_account/` | **What this key can actually call, and at what quota** | Recorded live-call snapshots |
| **2** | `corpus/` | How the API *behaves* — params, defaults, error codes | `max_tokens` is required on the Messages API |
| **3** | `bundle/` cards | Nothing — they are derived | Never beats its own source |

**The worked example.** `corpus/api-reference/chat/messages-create.md` documents
`step-router-v1` as "available only through Step Plan". The account snapshot does
not list it. Rank 1 wins → the model is treated as **unavailable here**, and the
card is marked `disputed` rather than silently rewritten. The disagreement gets an
evidence card, not a quiet edit.

Note that rank 2 still governs *behaviour*: the corpus is right that `max_tokens`
is required even though the account snapshot says nothing about it. Ranking is
about *which question* is being asked, not about which file is more trustworthy in
general.

---

## Idea 3 — Prove it with scripts instead of trust

Documentation rots. The only defence is a check that runs.

### Every card carries provenance

```yaml
---
card: models
tier: always-load
status: verified
verified_on: 2026-10-13
source: _account/live-calls/2026-10-13-models.md, corpus/guides/models/overview.md
---
```

`status` moves through a lifecycle: `verified` → `stale` (when the corpus is newer
than `verified_on`, or a fetch added/removed pages) → back to `verified` after a
re-read. `disputed` means the corpus and the card disagree, and the **corpus wins
until resolved**.

A card without a `source` is an opinion, not knowledge — the integrity gate fails
on it.

### Gate 1 — `_core/check_integrity.py`

Six mechanical checks, no LLM:

1. **Routing-file budgets** — `CLAUDE.md` ≤ 60 lines, `CONTEXT.md` ≤ 80. A map
   must stay a map.
2. **Card frontmatter and tier** — every card has `card`, `tier`, `status`,
   `verified_on`, `source`, and lives in the folder its tier names.
3. **Card sources exist** — every `source:` path resolves to a real corpus page
   or account file.
4. **Internal link resolution** — every relative link across all 44 bundle files
   resolves.
5. **Guard smells** — no credentials, and no backticked model ID that is not on
   the allowlist or in the off-plan card.
6. **Corpus manifest** — the fetched-page count matches the files on disk.

### Gate 2 — `_core/cold_walk.py`

The acid test, and the one that actually matters.

It asks: *open a brand-new agent session with zero memory, point it at this
folder, and ask "how do I do X?"* — can it route correctly from `CLAUDE.md` alone?

The script does the mechanical half: it verifies that the routing table covers
23 real probes, from "which base URL do I use" to "is this model available" to
"what replaces the model that retires next week". The live half is a human
opening a fresh session and asking.

**If the cold walk fails, fix the router — not the agent.** A routing failure is a
map defect, and trimming the map or adding the missing row is the whole fix.

### Live calls settle disputes

When the docs are wrong, a live HTTP call settles it and the result is recorded as
evidence in `_account/live-calls/`. That is how the reasoning-effort dispute was
resolved: the API reference claimed one model accepts only two effort levels; a
live call returned 200 with the third level, on both channels. The docs lost, the
card was corrected, and the contradiction was logged rather than quietly edited
away.

---

## The refresh loop

```
   vendor publishes a change
              │
              ▼
   python3 _core/fetch.py          ← re-fetch corpus/ from llms.txt
              │
              ▼
   a card goes `stale`
              │
              ▼
   skills/refresh-a-card.md        ← corpus page → card, one job per card
              │
              ▼
   both gates run green
              │
              ▼
   decisions.md gets a dated line  ← only if the workspace's shape changed
```

The extraction pipeline is a skill, not tribal knowledge: name the task (not the
page), read the corpus pages that cover it, pick the right tier, write the card
with frontmatter, add the routing row, run the gate, log the decision.

---

## What it deliberately does *not* do

- **It does not restate corpus prose.** Cards summarise and point. The corpus page
  is the evidence; the card is the index.
- **It does not invent.** If a source is silent, the card says "not documented"
  and the gap goes to `open_questions.md`. An honest "the docs don't say" beats a
  confident invention.
- **It does not hold credentials.** Not in a card, not in a commit message, not in
  a screenshot.
- **It does not hand-edit `corpus/`.** That is generated truth; it is regenerated.

---

## Next

- [HOW-TO-USE.md](HOW-TO-USE.md) — three ways to adopt this, from read-only to
  full rebuild for any API
- [DEMO.md](DEMO.md) — the numbers, live
- [`../_config/conventions.md`](../_config/conventions.md) — the full rule set
- [`../_config/guard-rules.md`](../_config/guard-rules.md) — the hard constraints
