# Try it yourself — a 10-minute, self-falsifying test

This page exists so you do not have to take the bundle's word for anything. Every
claim below is checkable: run a command, or open the file the answer cites.

The test has four parts. The first is mechanical. The other three ask an agent
real questions and tell you exactly what a correct answer looks like — and what a
broken one looks like.

---

## Part 0 — get a copy

```bash
git clone <this-repo> stepfun-api-v2 && cd stepfun-api-v2
```

No install, no API key, no network access needed for parts 1–3.

## Part 1 — the mechanical proof (2 minutes)

```bash
python3 _core/check_integrity.py    # structure, links, sources, allowlist
python3 _core/cold_walk.py          # can an agent route from the map alone?
```

Expected: `All integrity checks passed. 25 cards … 115 corpus pages.` and
`Cold walk passed the mechanical half.`

These two scripts are deterministic and contain no LLM. They check that the
routing map stays under its line budget, that every card carries its frontmatter,
that every internal link resolves, that every card's cited source page actually
exists in the corpus, and that no model ID appears in the bundle unless it is
either callable on this account or explicitly listed as not-callable.

**If either script fails, stop** — the bundle is internally inconsistent and the
answers below are not trustworthy.

## Part 2 — the live proof (5 minutes)

Open a **fresh agent session inside that folder** — Claude Code, Cursor, Cline,
Roo, Zed, Codex, anything that reads `CLAUDE.md` or `AGENTS.md`. Fresh matters: a
session that already knows StepFun is not testing the bundle.

Ask these three questions, one at a time.

### Q1 — "Which StepFun models can I call, and what base URL do I use?"

**A correct answer** does all four of these:

1. Names **two channels**, not one — Step Plan (Credits) and Standard
   (pay-as-you-go).
2. Gives the Step Plan base URL as `https://api.stepfun.ai/step_plan/v1` and the
   Standard one as `https://api.stepfun.ai/v1`, and says the **base URL alone**
   picks the channel.
3. States the counts — **15 models on Standard, 6 on Step Plan**.
4. Names models that are **not** callable, rather than only listing what is.

**Verify it yourself:**

| Claim | File to open |
| :- | :- |
| Base URLs, channel rule | `bundle/always-load/endpoints.md`, `bundle/always-load/auth.md` |
| The allowlist and the counts | `bundle/always-load/models.md` |
| What is *not* callable, and why | `bundle/evidence/models/not-on-this-plan.md` |

**It is broken if** it gives a single base URL for both channels, or hands you a
model that is not on the account. `step-router-v1` is the classic trap — the
vendor docs call it "available only through Step Plan"; it is not callable here at
all, and an agent reading only the docs will confidently recommend it.

### Q2 — "Add streaming to a chat call."

**A correct answer** routes to `bundle/by-task/streaming.md`, shows
`stream=True`, and — this is the part that matters — warns that
`chunk.choices[0].delta.content` **can be `None` on the first and last chunks**,
so it must be guarded. An unguarded read crashes in production.

**Verify it yourself:** `bundle/by-task/streaming.md`.

**It is broken if** it invents a parameter, or ships the loop without the `None`
guard.

### Q3 — "Does the Responses API work on the Step Plan channel?"

This is the question that shows what the bundle is actually for.

**A correct answer says the vendor docs are wrong.** The docs describe the
Responses API as Standard-channel-only. A live call on 2026-10-13 returned
**HTTP 200, `status=completed`** from `POST /step_plan/v1/responses`. The bundle
records the disagreement, the resolution, and the authority rule that settled it.

**Verify it yourself:** `bundle/evidence/source-contradictions.md`, entry **(f)**,
and the correction block in `bundle/by-task/chat-apis.md`.

**It is broken if** it repeats "Standard-only." That is the website's answer. The
whole point of the `_account/` layer is that live evidence about *your*
subscription outranks documentation about the platform.

## Part 3 — the negative test (2 minutes)

This is the one most doc tools fail.

Ask: **"What retry backoff should I use when I get a 429?"**

**A correct answer says the sources do not document it.** StepFun's docs specify
only "retry after a delay" — no backoff intervals, no jitter, no maximum attempt
count, no `Retry-After` header. The bundle says so explicitly, offers a
clearly-labelled *non-vendor* default (1 s base, ×2 backoff, ±50% jitter, 5
attempts), and tracks the gap as open question **Q05**.

**Verify it yourself:** `bundle/by-task/errors-and-debugging.md` and
`open_questions.md`.

**It is broken if** it states a number as though StepFun documented it. Inventing
a plausible limit is the failure mode this bundle is built to avoid — an honest
"the docs don't say" is the correct answer.

## Part 4 — optional: verify the live claims yourself

The bundle's headline numbers came from real HTTP calls. You can reproduce them
with your own key:

```bash
export STEP_API_KEY="your-key-here"     # never commit this

curl -s https://api.stepfun.ai/step_plan/v1/models \
  -H "Authorization: Bearer $STEP_API_KEY" | jq '.data[].id'   # expect 6

curl -s https://api.stepfun.ai/v1/models \
  -H "Authorization: Bearer $STEP_API_KEY" | jq '.data[].id'   # expect 15
```

The recorded evidence lives in `_account/live-calls/`. Note that the image API is
**retired and dead** — both `/v1/images/generations` and
`/step_plan/v1/images/generations` return HTTP 400
`model step-image-edit-2 not supported`, which is why the Step Plan list is 6 and
not 7. See `bundle/evidence/models/step-image-edit-2.md`.

> **Never commit your key.** Put it in `STEP_API_KEY` in your environment.
> `_core/check_integrity.py` scans every file for key-shaped strings and fails the
> build on a hit.

---

## What a pass looks like

| Part | Pass condition |
| :- | :- |
| 1 | Both scripts exit 0 with no `FAIL` lines |
| 2 | All three answers match, and every claim traces to the cited file |
| 3 | The agent says "not documented" instead of inventing a number |

If all four pass, the bundle is doing the one thing it claims to do: giving an
agent answers that are correct **for your subscription**, with citations you can
check, and refusing to guess where the sources are silent.

## Where to go next

- [HOW-IT-WORKS.md](HOW-IT-WORKS.md) — the architecture behind these paths
- [HOW-TO-USE.md](HOW-TO-USE.md) — adopt it into your own project
- [DEMO.md](DEMO.md) — the measured numbers behind the claims
- [FAQ.md](FAQ.md) — including "does this work with my editor?"
- [../open_questions.md](../open_questions.md) — what is still genuinely unsettled
