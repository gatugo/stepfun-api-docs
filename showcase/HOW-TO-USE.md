# How to use it

Three adoption paths, by how much of the method you want to take on. All three
start the same way, and none of them require you to trust anything you cannot
verify yourself.

```bash
git clone <this-repo> stepfun-api-v2-standard
cd stepfun-api-v2-standard
```

---

## Path 1 — Read-only (5 minutes)

You want the answers, not the machinery. Clone the repo, point your agent at it,
ask questions.

Any agent that reads `CLAUDE.md` or `AGENTS.md` works out of the box — Claude
Code, Cursor, Cline, Roo Code, Zed, Codex, and others. No configuration.

```bash
# Prove it is internally consistent before you rely on it
python3 _core/check_integrity.py   # 6/6 checks
python3 _core/cold_walk.py         # 23/23 routing probes
```

Then, in your agent session opened in that folder:

> *"Which StepFun models can I call on the Standard channel, and what base URL do
> I use?"*

It reads `CLAUDE.md`, routes to `bundle/always-load/models.md`, and answers from
verified facts — including which models are **not** available on your key.

**Keep it current** with one command:

```bash
python3 _core/fetch.py    # re-fetch the vendor corpus from llms.txt
```

A fetch **rewrites `corpus/` and the manifest only** — it does not mark any card
stale. To see what changed, diff the corpus or compare the new manifest's page
count against the old one, then re-read the affected cards yourself, or open a
fresh session and ask the agent to refresh them via
[`../skills/refresh-a-card.md`](../skills/refresh-a-card.md).

**Staleness detection is not automated, and that is a real limitation.** The two
gates prove the bundle is *internally consistent*, not that it is *current*. The
retired image API is exactly that failure mode: a card marked `verified_on:
2026-10-13` still trusted a model whose deadline had passed on 2026-10-10, and
only a live call caught it. Treat a fetch as the start of a review, not the end
of one.

---

## Path 2 — Adopt into your project (30 minutes)

You want the cards to travel with your codebase, so a teammate or a CI agent gets
the same answers without cloning a second repo.

The bundle is self-contained Markdown with **no absolute paths** — every internal
reference is relative. Relocation is a file operation.

```bash
# from your project root
cp -r /path/to/stepfun-api-v2-standard/bundle  ./stepfun-docs-bundle
cp -r /path/to/stepfun-api-v2-standard/_core   ./stepfun-docs-bundle/_core
cp -r /path/to/stepfun-api-v2-standard/_config ./stepfun-docs-bundle/_config
cp    /path/to/stepfun-api-v2-standard/CLAUDE.md ./CLAUDE.md
```

Then make the `_account/` layer yours — **this is the part that makes it correct
for your subscription**:

1. Delete the shipped `_account/step-plan-access-info.md` and replace it with your
   own. Fill in your platform, region, and base URLs.
2. Run one live call per channel and record the result:

```bash
curl -s https://api.stepfun.ai/v1/models \
  -H "Authorization: Bearer $STEP_API_KEY" | jq '.data[].id'
```

3. Paste that list into your `_account/` card. That list now **outranks the vendor
   docs** for what your key can call — which is the whole point.

4. Run both gates. They will tell you if your new facts contradict the cards.

> **Do not commit your key.** Put it in `STEP_API_KEY` in your environment. See
> [`../bundle/always-load/auth.md`](../bundle/always-load/auth.md).

### Editing a card

Use the extraction pipeline rather than free-hand edits:

```bash
python3 _core/check_integrity.py    # after every change
```

The rules that matter most when you write a card:

- **One fact, one home.** Link, don't copy. If two cards need a fact, one links to
  the other.
- **Never restate corpus prose.** Summarise and point.
- **State the negative.** "Not available on this plan" is a fact worth a card.
- **Say "not documented"** when a source is silent, and park the gap in
  `open_questions.md`. Never invent a parameter, price, or limit.

---

## Path 3 — Rebuild for any API (the reusable part)

The StepFun content is the worked example. The *method* — tiered cards, ranked
sources, scripted gates — works for any API whose docs are large, self-
contradictory, or describe a platform rather than your subscription.

The fastest correct rebuild is still Path 1 from a surviving copy. If you are
starting from an empty folder:

```bash
mkdir -p ws/_config ws/_core ws/_account ws/corpus \
         ws/bundle/always-load ws/bundle/by-task \
         ws/bundle/evidence/models ws/bundle/evidence/reference ws/skills
```

Write files **in layer order** — the router exists before the content it routes
to:

```
CLAUDE.md → CONTEXT.md → _config/ → _account/ → corpus/ →
bundle/always-load/ → bundle/by-task/ → bundle/evidence/ → skills/
```

Then:

1. **Fetch the corpus.** Most doc sites publish a `llms.txt`; fetch the `.md` form
   of each page into `corpus/`, mirroring the site's sections. Write
   `_core/fetch.py` to do it, and record failures in a manifest rather than
   letting pages silently go missing.
2. **Record what *your* key can call** in `_account/`, from a live call. This is
   rank 1 and it is the only source that can answer availability.
3. **Write the evidence cards first** — specifically the off-plan allowlist,
   because the integrity gate depends on it to validate every model ID in the
   bundle.
4. **Copy the two gates.** `check_integrity.py` and `cold_walk.py` are generic;
   change the probe list and the allowlist and they work for any API.
5. **Log decisions** in `decisions.md` whenever the workspace's shape changes, and
   park unknowns in `open_questions.md` instead of inventing answers.

The guard rules in [`../_config/guard-rules.md`](../_config/guard-rules.md) are
written as numbered rules (G0–G10) precisely so they can be lifted wholesale.

---

## Credentials — the one rule with no exceptions

| Do | Don't |
|---|---|
| Put the key in `STEP_API_KEY` | Commit it to any file |
| Pass it via your client's config | Paste it into a card, a screenshot, or a chat |
| Rotate it if it ever lands in a file | Put it in a commit message |

`_core/check_integrity.py` scans every file for key-shaped strings and fails the
build on a hit. That is a backstop, not a licence to be careless.

---

## Cheat sheet

| I want to… | Command / file |
|---|---|
| Know if the bundle is healthy | `python3 _core/check_integrity.py` |
| Know if an agent can route in it | `python3 _core/cold_walk.py` |
| Refresh the vendor docs | `python3 _core/fetch.py` |
| Fix or write a card | [`../skills/refresh-a-card.md`](../skills/refresh-a-card.md) |
| See the numbers | [`DEMO.md`](DEMO.md) · `bash showcase/demo.sh` |
| Know what is still unsettled | [`../open_questions.md`](../open_questions.md) |
| Know what was decided | [`../decisions.md`](../decisions.md) |
| Move the bundle | [`../skills/redeploy.md`](../skills/redeploy.md) |

---

## Next

- [HOW-IT-WORKS.md](HOW-IT-WORKS.md) — the architecture behind these paths
- [FAQ.md](FAQ.md) — including "does this work with my editor?"
- [../CONTRIBUTING.md](../CONTRIBUTING.md) — how to submit a correction
