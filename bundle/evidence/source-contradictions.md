---
card: source-contradictions
tier: evidence
status: verified
verified_on: 2026-10-13 (live calls on both channels)
source: _account/step-plan-access-info.md, corpus/guides/developer/image-chat.md, corpus/guides/pricing/details.md, corpus/api-reference/chat/chat-completion-create.md
---

# Source contradictions — where the sources disagree

**Every place two sources assert different values for the same fact, with both
values, both sources, and the rule for which one to act on.** Nothing here is
silently resolved. A contradiction is recorded, not averaged, and not edited away.

Authority order for choosing a winner lives in `_config/conventions.md`: `_account/`
(rank 1, availability) → `corpus/` (rank 2, behaviour) → `bundle/` cards (rank 3,
derived, never beats its source).

## The register

| # | Contradiction | Value A | Value B | Resolution rule |
| :- | :- | :- | :- | :- |
| (a) | Reasoning-effort levels | **Live docs**: `corpus/api-reference/chat/messages-create.md` — `step-3.5-flash-2603` accepts `low` and `high`; models supporting three levels take `low`/`medium`/`high` | **Reality (verified 2026-10-08):** live calls with `"reasoning_effort": "medium"` returned **HTTP 200 on both 3.5 variants** — all four reasoning models accept `low`/`medium`/`high` | **RESOLVED — the docs are wrong.** The owner-ruled half (base `step-3.5-flash` = `low`/`high`) was disproved by the same test. Corrected in `../always-load/models.md` and `../by-task/reasoning.md`; v1 ADR-016. |
| (b) | Images per request | **60**: `corpus/guides/developer/image-chat.md` — "A single request supports up to 60 images"; also `corpus/guides/models/step-5-preview.md` — "Images per request: Up to 60 images" | **10–50**: the *same file*, `corpus/guides/developer/image-chat.md` — "Maximum images depend on the model (10–50 per request)" | **Unresolved — same source, two values, no reconciliation.** Treat 60 as the documented ceiling for the named models and 10–50 as the model-dependent range. Do not average them. Verify with a live call before promising a count. |
| (c) | `stepaudio-3-asr-max` pricing | **$0.24 / hour**: the model page, `corpus/guides/models/stepaudio-3-asr.md` — "Billing: \$0.24 / hour" | **$0.40 / hour**: the pricing page, `corpus/guides/pricing/details.md` — `stepaudio-3-asr-max` \| \$0.40 / hour | **Record as a range, $0.24–$0.40/hr, pending verification** (v1 ADR-009). The pricing page is the billing authority; the model page is the capability authority. Moot for this account either way — the model is not callable here. |
| (d) | Per-model JSON Mode support | **Named for one model only**: `corpus/guides/developer/json-mode.md` — "Step 5 Preview supports both JSON Mode and JSON Schema structured outputs"; `corpus/guides/models/step-5-preview.md` — "JSON Mode and JSON Schema supported" | **Nothing for the rest**: the per-model pages for `step-3.7-flash`, `step-3.5-flash`, and `step-3.5-flash-2603` record **no JSON Mode figure at all** | **Absence of a matrix is a gap, not a negative.** Do not assert "unsupported" for the other models — write "not documented" and route through [`../by-task/structured-output.md`](../by-task/structured-output.md). Open question. |
| (e) | Which models Step Plan serves | **Account list — 6 IDs** (`_account/step-plan-access-info.md`): `step-5-preview`, `step-3.7-flash`, `step-3.5-flash`, `step-3.5-flash-2603`, `stepaudio-2.5-tts`, `stepaudio-2.5-asr` | **Platform Step Plan list** (`corpus/step-plan/overview.md`, "Supported models"): the same six text/audio IDs **plus `step-router-v1`** — "smart routing model that dispatches requests by task complexity" — and **no image model** | **Rank 1 wins for availability: the account list.** `step-router-v1` is reference-only here; the lists now differ by exactly one entry. **Superseded in part, 2026-10-13:** the account list used to carry a 7th ID, `step-image-edit-2`, which made the two lists the exact inverse of each other on image models. The image API has since retired and the model dropped off the account list, so both lists now exclude image models. The disagreement gets this card, not a silent edit. |
| (f) | Responses API channel availability | **Sources**: Standard channel only — `corpus/api-reference/responses/responses-create.md` documents only `https://api.stepfun.ai/v1/responses`; `bundle/by-task/chat-apis.md` recorded "Step Plan URL not documented" | **Reality (verified 2026-10-13):** `POST https://api.stepfun.ai/step_plan/v1/responses` with `step-5-preview` returned **HTTP 200, `status=completed`** | **RESOLVED — the docs are incomplete, not the endpoint.** Responses works on **both** channels. Corrected in [`../by-task/chat-apis.md`](../by-task/chat-apis.md) and [`../always-load/endpoints.md`](../always-load/endpoints.md). |
| (g) | Files API on Step Plan | **Bundle, pre-verification**: "not documented in sources — treat as unconfirmed until a live call" | **Reality (verified 2026-10-13):** `POST https://api.stepfun.ai/step_plan/v1/files` returns a bare **HTTP 404** | **RESOLVED — verified absent.** Files is a **Standard-only** API. Corrected in [`../by-task/files.md`](../by-task/files.md) and [`../always-load/endpoints.md`](../always-load/endpoints.md). |

## (a) in full — the one that must be settled first

**Resolved 2026-10-08 by live calls.** `"reasoning_effort": "medium"` returned HTTP 200 against `step-3.5-flash-2603` **and** `step-3.5-flash` on the Step Plan channel (with `step-5-preview` as control). **All four reasoning models accept `low`/`medium`/`high`.**

| Model | Effort levels | Status |
| :- | :- | :- |
| `step-5-preview` | `low` / `medium` / `high` | Official |
| `step-3.7-flash` | `low` / `medium` / `high` | Official |
| `step-3.5-flash-2603` | `low` / `medium` / `high` | **Verified by live call** |
| `step-3.5-flash` | `low` / `medium` / `high` | **Verified by live call** |

Both prior positions were wrong in part: the API reference's "2603 = low/high only" exception, and the owner-ruled `low`/`high` for base `step-3.5-flash`. Corrected in [`../always-load/models.md`](../always-load/models.md) and [`../by-task/reasoning.md`](../by-task/reasoning.md), in v1 (ADR-016), and in the sibling `stepfun-ai-docs` desk — so no two desks assert different values.

## (e) in full — 7 vs the platform's list

The account card is rank 1 and wins, but the shape of the disagreement is worth
stating precisely: the two lists now differ by exactly **one** entry —
`step-router-v1`, which the platform documents and this subscription does not
serve. Both lists exclude image models, which was not true before 2026-10-13:
the account list then carried `step-image-edit-2` as a 7th ID, the exact inverse
of the platform list. `corpus/api-reference/chat/messages-create.md` compounds it
by documenting `step-router-v1` as "available only through Step Plan" — true of
the platform, false of this subscription.

> **Not sourced:** the platform's Step Plan supported-models list in
> `corpus/step-plan/overview.md` enumerates **seven** IDs, not eight. An earlier
> note in the project history described it as an eight-model list. No eighth entry
> exists in the source; treat seven as the verified count.

## Other disagreements on record

| Item | Position A | Position B | Rule |
| :- | :- | :- | :- |
| A `429 rate_limited` response | Reads like "endpoint missing" | `step-3.5-flash` on Step Plan `/messages` returned **429 three times** while every other call in the same minute returned 200, then returned 200 on retry | **A 429 is a per-model throttle, not a 404.** Retry with backoff and a different model before concluding an endpoint is absent. Only a 404 proves absence. |
| `stepaudio-2.5-asr-stream` | Documented as a streaming-ASR model ID (WebSocket, server VAD) | Not in the account's 6-model list | **Not callable here.** The confirmed ASR route is the one-shot `POST /v1/audio/asr/sse` path against `stepaudio-2.5-asr`. Tracked as Q02. |
| `stepaudio-2.5-chat` / `stepaudio-2.5-realtime` / the stepaudio-3 family | Documented across the model overview and per-model pages | Not on this account | Rank 1 wins — reference-only. See [`./models/not-on-this-plan.md`](./models/not-on-this-plan.md). |
| `step-image-edit-2` | Was on this account until the 2026-10-13 re-check | **Retired 2026-10-10** — HTTP 400 on both channels, no successor named | Was on-plan **and** doomed; now simply gone — see [`./models/step-image-edit-2.md`](./models/step-image-edit-2.md). |
| Session ledger location | An execution ledger lived at `<parent>/.superpowers/sdd/stepfun-api-workspace/progress.md` | It is session scratch, not project documentation, and does not travel with the workspace | **Resolved 2026-10-08 (owner): left in place.** Durable content already lives in `docs/decisions.md`. |

## How to use this card

Before asserting any value that appears above, check whether it is in dispute. If it
is, state both values and name the rule — never pick silently. When a contradiction
is settled by a live call, update this card, the card that carries the value, and
`open_questions.md` in the same pass.
