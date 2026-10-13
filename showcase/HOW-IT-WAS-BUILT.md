# How this was built

The [CHANGELOG](../CHANGELOG.md) records *what* changed and
[decisions.md](../decisions.md) records *why* each shape was chosen. This page is
the third piece: the sequence, end to end, and what it taught.

Four moves, repeated until the gates pass.

---

## Move 1 — fetch, don't paste

The vendor corpus is 115 pages pulled from the docs' `llms.txt` by
[`_core/fetch.py`](../_core/fetch.py). Deterministic, no LLM, no guessing. Run it
again whenever the docs change and it re-downloads and rewrites the manifest.

The manifest is a state machine, not a list: every page is `[x]` fetched or
`[ ]` failed, and the integrity gate fails the build if a card cites a page that
isn't there. A missing page is loud, not silent.

**Why fetch rather than paste.** A fetch is repeatable and diffable. When the
vendor ships a change you re-run one command and compare. A pasted copy is a
photograph — it goes stale and nothing tells you.

## Move 2 — tier the facts

Not every fact is needed for every task, so the bundle is layered by how often a
fact is required:

| Tier | Cards | Read when |
|---|---|---|
| `bundle/always-load/` | 6 | every task |
| `bundle/by-task/` | 16 | the one card matching the task |
| `bundle/evidence/` | 5 | only when a fact is disputed |
| `_account/` | — | outranks everything |

Two more layers sit outside the bundle proper: `corpus/` (rank 2 — vendor truth)
and `_account/` (rank 1 — live-call facts about *this subscription*).

**The ranking is the whole trick.** When the docs and a live call disagree, the
live call wins — and the disagreement gets written down instead of quietly
resolved. Every dispute in
[`bundle/evidence/source-contradictions.md`](../bundle/evidence/source-contradictions.md)
carries both values, the evidence, and the rule that settled it.

`CLAUDE.md` is a map, not a document. It is capped at 60 lines by a script and
holds only a routing table. If it grows, the content belongs in a card.

## Move 3 — settle every dispute with a live call

The docs are wrong in specific, findable ways. Each one was settled by an HTTP
call and recorded with the date and the result — never by picking the answer that
looked more plausible.

| The docs say | Reality, settled by |
|:-|:-|
| The Responses API is Standard-channel-only | **HTTP 200 on Step Plan too** — the docs are incomplete, not the endpoint |
| `stepaudio-2.5-asr-stream` is a Step Plan model | **404 on Step Plan**, Standard only |
| The image API *retires* 2026-10-10 | **Already dead** — HTTP 400 on both channels, and the model dropped off the list |
| A 429 means the endpoint is missing | **A 429 is a throttle.** `step-3.5-flash` returned 429 three times, then 200, while everything else in the same minute succeeded |

Two rules came out of that work and now govern the bundle:

1. **Only a 404 proves absence.** A 429 proves nothing except that you were
   rate-limited. Concluding "unavailable" from a 429 produces false negatives.
2. **A card verified *after* a deadline it never re-checked is a bug.** One card
   was marked `verified_on: 2026-10-13` while still trusting a model whose
   retirement date had passed three days earlier. The gates check internal
   consistency, not freshness — only a live call caught it.

## Move 4 — prove it with scripts, not discipline

Two gates, both deterministic, neither containing an LLM:

```bash
python3 _core/check_integrity.py    # 6 structural checks
python3 _core/cold_walk.py          # 23 routing probes
```

`check_integrity.py` verifies the routing files stay under their line budgets,
that every card carries its frontmatter, that every card's cited source page
exists in the corpus, that every internal link resolves, that no credential or
off-plan model ID appears anywhere, and that the manifest matches the corpus.

`cold_walk.py` asks whether a fresh agent with no memory can route from the map
alone — 23 probes, each naming a file the routing table must point at.

**The third practice is the one that found the most.** A cold-reader test: three
agents with empty context, no web access, and real developer questions — then
every citation checked by hand against the file it named. That test found the
missing non-streaming Python example, the wrong environment variable in a
model-API example, the undocumented retry mechanics, and four question IDs that
five cards cited and nothing had ever defined. You can run it yourself in ten
minutes: [TRY-IT.md](TRY-IT.md).

---

## What the process got wrong, and what changed

Worth recording, because these are the failure modes rather than the successes.

- **A documentation promise the code never kept.** The docs claimed that a fetch
  flips affected cards to `stale`. [`_core/fetch.py`](../_core/fetch.py) rewrites
  `corpus/` and the manifest only — it has never touched a card. The claim was
  corrected and the limitation stated plainly.
- **A demo script that overstated itself.** `showcase/demo.sh` closed with "every
  number above came from this tree, live" while its final section was hardcoded
  text. Now labelled as recorded evidence with its date.
- **Numbers typed instead of measured.** Token figures drifted — 5,700 became
  6,000, 42× became 40× — because they were written into prose by hand. They are
  now computed by the script and the prose points at it.
- **A gate that agreed with a stale fact.** `check_integrity.py` hardcoded a model
  in its allowlist after the live list had dropped it, so the gate was enforcing
  the past. Removed.

The lesson, stated once: **gates catch inconsistency, not staleness.** Anything
that can drift should be measured, not typed, and re-verified by a live call
rather than trusted because it passed a check.

## The two-tree model

| Tree | Role |
|---|---|
| **Private** — `stepfun-api-v2-standard/` | Working desk. Full history, `HANDOFF.md`, `_session/` scratch. **Edited here.** |
| **Public** — `stepfun-api-v2-standard-public/` | **Generated output.** Rebuilt by [`_core/make_public.py`](../_core/make_public.py). Never hand-edited. |

The golden rule: fix things in the private repo, then regenerate. The public copy
is a build artifact, like `showcase/_site/`.

The public copy is its own repository with a **single commit and no history**. The
working history contains session scratch, and at one point a live credential that
had to be purged from it — so the published repo was initialised fresh rather
than cloned, which makes it structurally impossible for anything in the working
history to ride along.

## Rebuild it for another API

The StepFun content is the worked example. The method — ranked sources, tiered
cards, scripted gates, live-call arbitration, "state the negative, never invent"
— is the transferable part, and it works for any API whose docs are large,
self-contradictory, or describe a platform rather than your subscription.

The fastest correct rebuild is Path 3 in [HOW-TO-USE.md](HOW-TO-USE.md). The
guard rules in [`_config/guard-rules.md`](../_config/guard-rules.md) are numbered
G0–G10 precisely so they can be lifted wholesale.

---

## Next

- [HOW-IT-WORKS.md](HOW-IT-WORKS.md) — the architecture, layer by layer
- [TRY-IT.md](TRY-IT.md) — verify every claim in here yourself
- [HOW-TO-USE.md](HOW-TO-USE.md) — adopt or rebuild the method
- [DEMO.md](DEMO.md) — the measured numbers
- [../CONTRIBUTING.md](../CONTRIBUTING.md) — how to submit a correction
