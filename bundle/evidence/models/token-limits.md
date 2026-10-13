---
card: token-limits
tier: evidence
status: verified
verified_on: 2026-10-08
source: corpus/api-reference/chat/chat-completion-create.md, corpus/guides/models/step-5-preview.md
---

# Token limits — what is published, what is inferred

**Only `step-5-preview` has a published output limit. Everything else on this plan
is inferred.** The single home for input/output token limits across the four text
models. The short answer lives in
[`../../always-load/models.md`](../../always-load/models.md); this card is where its
numbers come from and which ones to distrust.

## The platform rule

`corpus/api-reference/chat/chat-completion-create.md`, the `max_tokens` parameter:

> `max_tokens` `int` *optional*. Maximum number of `tokens` to generate for the
> chat. Default is INF (no limit, determined automatically by the model). The total
> of input and generated `tokens` is limited by the specified model's maximum
> context length.

That is the whole enforcement mechanism, and it is re-stated on the model page
(`corpus/guides/models/step-5-preview.md`: "Output length — `max_tokens` defaults to
`INF`; no limit is applied and the model determines it automatically"). **There is
no per-model output cap in the API.** Output is bounded by
*input + output ≤ context window*.

## Per model

| Model | Max input | Max output | Source | Status |
| :- | :- | :- | :- | :- |
| `step-5-preview` | 1M tokens | **64k tokens** | `corpus/guides/models/step-5-preview.md` — "Maximum input **1M tokens**", "Maximum output **64k tokens**" | **Official, published** |
| `step-3.5-flash` | 256K tokens | 64k tokens | No figure in this corpus — carried from the prior bundle as an inference from StepFun's own paper (arXiv:2602.10604) | **Inferred — not a platform-docs figure** |
| `step-3.7-flash` | 256K tokens | 64k tokens | No figure in this corpus — family inference only | **Inferred, weakest of the four** |
| `step-3.5-flash-2603` | 256K tokens | 64k tokens | No page of its own; inherits from `step-3.5-flash` | **Inferred, two steps removed** |

`stepaudio-2.5-tts` / `stepaudio-2.5-asr` are not token-metered this way — see
[`../../by-task/audio.md`](../../by-task/audio.md).

**On the three inferred 64k figures:** this corpus publishes an output number for
`step-5-preview` and nothing for the rest. `step-3.5-flash`'s rests on a paper, not
the platform docs; `step-3.7-flash`'s rests on family resemblance alone;
`step-3.5-flash-2603`'s inherits from `step-3.5-flash`. They are working budgets,
not specifications, and they are the least-grounded numbers in the table.

## Numbers to reject

| Claim | Where it comes from | Why it is wrong |
| :- | :- | :- |
| "256k max output" for a 3.x Flash model | OpenRouter and similar routers | A **misreading of the 256K context window** as an output cap, or the router's own platform limit. Not a StepFun figure. |
| "8,192 max output" | Aggregators and some client configs | A **client budget, not a model capability**. Not a StepFun figure. |
| "131,072 max output" | One aggregator | Unverified. No StepFun source anywhere. |
| Any other third-party number | — | Inconsistent across aggregators, which is the tell that none of them are reading StepFun's spec. |

## The one legitimate corroboration — not present in this corpus

The prior bundle corroborated 64k as a sensible *client budget* with two corpus
pages (`step-plan/integrations/openclaw.md` for the "8192 is a budget" quote, and
Cline / Kilo Code configs showing `65536`). **Those pages do not exist in this
bundle's corpus** — `corpus/step-plan/integrations/` holds only
`reasoning-api.md`. Treat the corroboration as **not available here**: it supported
64k as a number to *set*, never as a cap, and it must be re-sourced before it is
quoted again.

## Open

The three inferred 64k figures are working assumptions. Worth one real call with a
large `max_tokens` against each model, or one look at the dashboard's model detail
page. Until then, quote `step-5-preview`'s 64k as published and the other three as
budgets — and never as enforced walls.
