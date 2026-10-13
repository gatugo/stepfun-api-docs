# FAQ

## "Why not just paste the vendor docs into my project?"

Because the vendor docs describe the **platform**, not your **subscription**.

They are 115 pages covering roughly 110 model IDs. Your key can call 15 on the
Standard channel and 6 on Step Plan. The docs document `step-router-v1` as
"available only through Step Plan" — it is not callable here at all. An agent
reading the docs will hand you that model name with total confidence, and your
request will 404.

Pasting the docs in also costs about **239,000 tokens of context per question**,
versus about **6,000** for a routed answer. You pay 40× more for a worse answer.

The bundle exists to answer one question the docs cannot: *what can **my key**
actually do?*

---

## "Does this work with my editor / agent?"

Yes, if it reads `CLAUDE.md` or `AGENTS.md`. That covers Claude Code, Cursor,
Cline, Roo Code, Zed, Codex, and most others. There is no configuration and no
plugin — it is Markdown in a folder, and the file names are the convention.

If your tool looks for `map.md` instead of `CONTEXT.md`, there is a thin alias at
the repo root that points at the real map. One fact, one home.

---

## "Is my API key safe?"

The bundle never asks for it and never stores it.

- Put it in `STEP_API_KEY` in your environment, or in your client's own config.
- Never commit it, never paste it into a card, a screenshot, or a chat.
- `_core/check_integrity.py` scans every file for key-shaped strings and **fails
  the build** on a hit, so a leaked key breaks CI rather than shipping.

The `_account/` layer records *which models your key can call* — not the key
itself. If you publish a copy of this repo, replace `_account/` with your own
template; the shipped version describes one specific subscription.

---

## "What happens when the API changes?"

```bash
python3 _core/fetch.py
```

That re-fetches the vendor corpus from the docs' `llms.txt`. It rewrites `corpus/`
and the manifest **only** — it does not flag any card, so nothing is silently
wrong and nothing is automatically right either. Compare the new manifest's page
count against the old one, or diff the corpus, to see what actually changed.

Then either re-read the affected cards yourself, or open a fresh agent session and
ask it to refresh them via [`../skills/refresh-a-card.md`](../skills/refresh-a-card.md).
Both gates run again. If the change alters a previously-stated fact, it gets a
dated line in `decisions.md`.

A wrong-but-flagged card is recoverable. A wrong card that still says `verified`
is the thing this design exists to prevent.

---

## "The docs are wrong about something. What do I do?"

Settle it with a live call, then record it. In order:

1. Make the call. Note the exact request, the status code, and the response.
2. Write the evidence into `_account/live-calls/<date>-<what>.md`.
3. Correct the card that carried the wrong value, and bump its `verified_on`.
4. **Log the contradiction** in `bundle/evidence/source-contradictions.md` with
   both values, both sources, and which one won. Do not quietly overwrite the old
   claim — the next reader needs to see that there was a dispute.
5. Run both gates.

Step 4 is the one people skip, and it is the one that keeps the bundle honest.
See [`../CONTRIBUTING.md`](../CONTRIBUTING.md).

---

## "Can I use this for a different API?"

Yes — that is the point of the method. The StepFun content is the worked example.

Tiered cards, ranked sources, and scripted gates work for any API whose docs are
large, self-contradictory, or describe a platform rather than a subscription. Most
doc sites publish an `llms.txt` you can fetch the `.md` form from.

The parts you reuse wholesale: `_core/check_integrity.py`, `_core/cold_walk.py`,
`_config/conventions.md`, `_config/guard-rules.md`, and
`skills/refresh-a-card.md`. The parts you rewrite: the corpus and the cards.

See Path 3 in [HOW-TO-USE.md](HOW-TO-USE.md).

---

## "Why is `CLAUDE.md` only 50 lines? It seems short."

Because a routing map is a map, not a document. It holds one orientation sentence
and a routing table — no facts, no code, no prose.

If it grows past 60 lines, the content belongs in a card, and a script fails the
build until you move it. This is enforced mechanically because a map that slowly
becomes a document is the most common way these setups rot: the agent starts
reading the map as content, and now every question pays for facts it did not need.

---

## "What is the difference between Step Plan and Standard?"

| | Step Plan | Standard |
|---|---|---|
| Base URL | `https://api.stepfun.ai/step_plan/v1` | `https://api.stepfun.ai/v1` |
| Billing | Monthly Credits | USD per call |
| Callable models | 7 | 15 |
| Files API | **Not available** (404) | Available |

**The same API key works on both.** The base URL alone selects the channel — which
is why pointing a client at the wrong one spends real money while you believe you
are spending Credits. Every task card carries both URLs side by side for this
reason.

---

## "What is still unverified?"

The bundle says so explicitly rather than guessing:

- **Streaming WebSocket endpoints** are documented but not live-tested — a
  one-shot parity probe does not cover them.
- **Standard-only models** were confirmed present in the model list, but their
  actual transcription/generation behaviour was not exercised per-model.
- **`step-image-edit-2` is retired and confirmed dead** — live-verified 2026-10-13:
  HTTP 400 on both channels, and the model has dropped out of the Step Plan list.
  No successor is named anywhere, which remains a product decision.

Open items live in [`../open_questions.md`](../open_questions.md). An honest "the
docs don't say" is a valid answer and is preferred over a confident invention.

---

## "How big is it?"

| | |
|---|---|
| Vendor corpus | 115 pages, ~1.3 MB |
| Bundle cards | 25 cards, ~208 KB |
| Verification tooling | 3 Python scripts, ~500 lines |
| Loaded per task | ~6,000 tokens |

---

## Where to go next

- [README.md](README.md) — the overview
- [HOW-IT-WORKS.md](HOW-IT-WORKS.md) — the architecture
- [HOW-TO-USE.md](HOW-TO-USE.md) — three adoption paths
- [DEMO.md](DEMO.md) — the numbers, live
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — submit a correction
