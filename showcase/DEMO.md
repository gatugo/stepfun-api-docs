# Demo — the proof

Everything below is measured from the tree, not typed by hand. Reproduce it with:

```bash
bash showcase/demo.sh
```

---

## 1. What an agent loads to answer one question

```
  CLAUDE.md (routing map)                2758 ch  ~   689 tok
  bundle/always-load/ (6 cards)         17993 ch  ~  4498 tok
  one bundle/by-task/ card               2052 ch  ~   513 tok
  ---------------------------------- --------    ------
  PER TASK                              22803 ch  ~  5700 tok

  corpus/ (115 vendor pages)           957549 ch  ~239387 tok

  Reduction: 40x less context for a routed answer.
```

**The claim, precisely:** to answer "how do I stream a response from StepFun", an
agent loads about **6,000 tokens**. Reading the vendor corpus instead costs about
**239,000** — 40× more, for an answer that is *less* reliable, because the corpus
describes the platform rather than your subscription.

---

## 2. Before and after, on a real question

**The question:** *"Which StepFun models can I call, and what base URL do I use
for the Standard channel?"*

### Without the bundle — an agent reading the vendor docs

```
✗ Reads 115 corpus pages, or guesses from the ones it happens to recall
✗ Answers "about 110 models" — describes the platform, not the key
✗ Recommends step-router-v1 (documented as "available only through Step Plan")
  → it is NOT callable on this account
✗ Gives the /v1 base URL without warning that it bills USD per call,
  not monthly Credits
✗ Cannot tell you the reasoning-effort levels are documented inconsistently
✗ Cost: ~239,000 tokens of context
```

### With the bundle

```
✓ Reads CLAUDE.md → routes to bundle/always-load/models.md
✓ Answers: 15 models on Standard, 6 on Step Plan, per-channel allowlist
✓ States explicitly that step-router-v1 is NOT callable here, with the
  evidence card that proves it
✓ Warns that the base URL alone selects the billing channel
✓ Carries the corrected effort levels, verified by live call
✓ Cost: ~6,000 tokens of context
```

---

## 3. The gates, running

```
$ python3 _core/check_integrity.py

[1] Routing-file budgets
  ok    CLAUDE.md: 50/60 lines
  ok    CONTEXT.md: 23/80 lines

[2] Card frontmatter and tier
  ok    bundle/always-load/auth.md: tier=always-load status=verified
  ok    bundle/always-load/endpoints.md: tier=always-load status=verified
  ok    bundle/always-load/models.md: tier=always-load status=verified
  ok    bundle/always-load/plan.md: tier=always-load status=verified
  ok    bundle/always-load/standard-channel.md: tier=always-load status=verified
  ... (20 more cards)

[3] Card source pages exist
  ok    all card sources resolved (116 corpus, 3 account)

[4] Internal link resolution
  ok    all relative links resolve across 44 bundle files

[5] Guard smells
  ok    no credential or off-plan model smells

[6] Corpus manifest
  ok    manifest: 115 fetched, 0 failed

==============================================================
All integrity checks passed.
25 cards, 50 markdown files, 115 corpus pages.
```

> *Transcript. The markdown-file count is tree-dependent — 50 in the published
> copy, higher in the working tree, which also carries `_session/` and
> `HANDOFF.md`. The card and corpus counts are the stable figures.*

```
$ python3 _core/cold_walk.py

CLAUDE.md is 50 lines (budget 60)

[3] Routing-table coverage of the probe list
  23 routing row(s) reference bundle cards
  ok    which plan am I on                     -> bundle/always-load/plan.md
  ok    how do I authenticate                  -> bundle/always-load/auth.md
  ok    which base URL do I use                -> bundle/always-load/endpoints.md
  ok    which models can I call                -> bundle/always-load/models.md
  ok    stream a response                      -> bundle/by-task/streaming.md
  ok    text to speech / transcribe            -> bundle/by-task/audio.md
  ok    is stepaudio-3 available               -> bundle/evidence/models/not-on-this-plan.md
  ... (16 more probes)

==============================================================
Cold walk passed the mechanical half.
```

**What these actually prove.** Not that the Markdown is pretty — that every link
resolves, every card cites a source that exists, no credential is present, no
unavailable model is named as available, the map has not bloated into a document,
and a fresh agent can route 23 real questions without help.

---

## 4. Documented vs actually callable

The part that makes the bundle worth having. All figures verified by live HTTP
call on 2026-10-13.

```
  Documented across the corpus:  ~110 model IDs
  Callable on Standard channel:   15   (live GET /v1/models)
  Callable on Step Plan channel:   6   (live GET /step_plan/v1/models)
```

| Documented as… | Actually… | Settled by |
|---|---|---|
| `step-router-v1` is "available only through Step Plan" | **Not callable on either channel** | `GET /v1/models`, `GET /step_plan/v1/models` |
| `stepaudio-2.5-asr-stream` works on Step Plan | **404 on Step Plan**, Standard only | live call |
| The Responses API is Standard-channel-only | **Works on Step Plan too** — the docs are incomplete | `POST /step_plan/v1/responses` → 200 |
| The image API retires 2026-10-10 | **Already dead** — HTTP 400 `model step-image-edit-2 not supported` on both channels, and the model has dropped out of the Step Plan list (7 → 6) | `POST /v1/images/generations`, 2026-10-13 |
| The Files API exists on Step Plan | **404 — genuinely Standard-only** | `POST /step_plan/v1/files` |
| `step-3.5-flash-2603` accepts only `low`/`high` effort | Accepts `low`/`medium`/`high` on **both** channels | live call → 200 with `medium` |

That last group is the argument for the whole design. Every one of those facts is
wrong in the vendor docs, and an agent reading the docs gets it wrong. A live call
settles it, the card is corrected, and the contradiction is **logged rather than
quietly edited away** — so the next reader can see both the claim and the verdict.

---

## 5. Docs drift, with a dated diff

One concrete example of the correction loop, end to end.

**The dispute.** `corpus/api-reference/chat/messages-create.md` states that
`step-3.5-flash-2603` accepts `low` and `high` reasoning effort, while models
supporting three levels take `low`/`medium`/`high`. A second reading — from the
owner's own instructions — said the base `step-3.5-flash` was `low`/`high` only.

**Both were partly wrong.** The live call sent `"reasoning_effort": "medium"`
against both 3.5 variants on the Step Plan channel. Both returned **HTTP 200**.

```
  BEFORE (card, status: disputed)
  | step-3.5-flash-2603 | low / high            | docs claim, unverified |

  AFTER (card, status: verified, verified_on: 2026-10-13)
  | step-3.5-flash-2603 | low / medium / high   | verified by live call |
```

**What happened to the record.** The contradiction got an entry in
`bundle/evidence/source-contradictions.md` with both values, both sources, and the
resolution rule — not a silent overwrite. The corrected card, the evidence card,
and `open_questions.md` were updated in the same pass, so no two cards assert
different values.

---

## 6. The shape of the tree

```
stepfun-api-v2-standard/
├── CLAUDE.md                  routing map, 50 lines, no content
├── CONTEXT.md                 dated "where you are", ≤ 80 lines
├── PURPOSE.md                 what this is, for humans
├── AGENTS.md                  the one start file
├── README.md                  pointer, not a second front door
├── decisions.md               dated lines when the shape changes
├── open_questions.md          parked unknowns, never invented answers
├── LICENSE                    MIT
│
├── _config/                   conventions, guard rules, quality gate
├── _core/                     fetch.py, check_integrity.py, cold_walk.py
├── _account/                  rank-1 facts: what YOUR key can call
├── corpus/                    115 fetched vendor pages — never hand-edited
├── bundle/
│   ├── always-load/           5 cards, loaded on every task
│   ├── by-task/              16 cards, one job each
│   └── evidence/             contradictions, off-plan allowlist, provenance
├── skills/                    refresh-a-card, redeploy
└── showcase/                  this folder
```

---

## Try it yourself

```bash
git clone <this-repo> stepfun-api-v2-standard
cd stepfun-api-v2-standard
bash showcase/demo.sh
```

Then open a **brand-new** agent session in that folder — zero prior context — and
ask: *"What is this folder, and how do I add streaming?"*

It should name the plan, read `CLAUDE.md`, and route to
`bundle/by-task/streaming.md` without help. If it cannot, the router is wrong —
and fixing the router is the entire fix.
