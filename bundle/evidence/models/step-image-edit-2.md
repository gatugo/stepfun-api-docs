---
card: step-image-edit-2
tier: evidence
status: verified
verified_on: 2026-10-13
source: _account/live-calls/2026-10-13-image-api-retired.md, corpus/guides/image-offline-notice.md, corpus/guides/models/step-image-edit-2.md, corpus/api-reference/images/image.md, corpus/api-reference/images/edits.md
---

# step-image-edit-2 — RETIRED 2026-10-10, no successor

**`step-image-edit-2` is retired and confirmed dead.** The image-generation API
retired on 2026-10-10 and the model has since dropped out of the live model list.
A second live pass on 2026-10-13 called the endpoints directly and both returned
**HTTP 400 `model step-image-edit-2 not supported`** — on Step Plan *and* on
Standard. The retirement notice names no replacement. Do not start new work on
it; anything already built needs a successor decision.

## Live verification — 2026-10-13

| Channel | Endpoint | Result |
|---|---|---|
| Step Plan | `POST /step_plan/v1/images/generations` | **HTTP 400** |
| Standard | `POST /v1/images/generations` | **HTTP 400** |

Response body, verbatim, identical on both channels:

```json
{"error":{"message":"model step-image-edit-2 not supported","type":"request_params_invalid","description":"请求参数错误"}}
```

Also confirmed the same day: the Step Plan model list dropped from **7 models to
6** — `step-image-edit-2` is gone from it. The Standard list still returns 15 and
never contained an image model.

Full record:
[`../../../_account/live-calls/2026-10-13-image-api-retired.md`](../../../_account/live-calls/2026-10-13-image-api-retired.md).

> **Note the failure mode.** The endpoints still *exist* — they answer 400, not
> 404. An absence check that only looks for 404 would wrongly conclude the
> endpoint was merely missing. See the 429-vs-404 rule in
> [`../source-contradictions.md`](../source-contradictions.md).

## The deadline

| Item | Value |
| :- | :- |
| Retirement date | **October 10, 2026** — passed |
| Retiring with it | `step-2x-large` (not on this account) |
| Already gone | `step-1x-edit` — no longer available |
| Capabilities that stopped | Text-to-image, image-to-image, image editing |
| Successor named | **None — not documented.** The notice lists no replacement model ID. |
| Still callable | **No** — HTTP 400 on both channels, verified 2026-10-13 |
| After the date | Confirmed: every call returns `request_params_invalid` |

`corpus/guides/image-offline-notice.md` carries the retirement date, the model list,
the capability list, and the affected-endpoint table. It asked that required business
changes be completed **before October 10, 2026** to keep production services running.

## Affected endpoints — both channels

| Service | Capability | Method | Endpoint |
| :- | :- | :- | :- |
| Open Platform API | Text-to-image | POST | `/v1/images/generations` |
| Open Platform API | Image-to-image | POST | `/v1/images/image2image` |
| Open Platform API | Image editing | POST | `/v1/images/edits` |
| **Step Plan** | Text-to-image | POST | `/step_plan/v1/images/generations` |
| **Step Plan** | Image editing | POST | `/step_plan/v1/images/edits` |

This account is on the **Step Plan** channel (Rule 6 — see
[`../../always-load/auth.md`](../../always-load/auth.md)), so the two
`/step_plan/...` rows are the ones that matter. Note the asymmetry: the Step Plan
column has **no image-to-image endpoint** — only generations and edits.

## Blast radius

| Not affected | Source |
| :- | :- |
| Other Step Plan models — text, reasoning, speech, smart routing | `corpus/guides/image-offline-notice.md`: "Other Step Plan models … are not affected" |
| Studio image generation | Affected: "Image generation will no longer be available" |
| Already-generated images | Image download links have their own validity limits, unrelated to this retirement — download and store anything long-lived yourself |

Image generation and editing are **no longer available on Step Plan at all**.
This card is now a member of
[`./not-on-this-plan.md`](./not-on-this-plan.md).

## The model, for reference (no longer callable)

Kept because cards still cite the spec and because anyone maintaining old code
needs to know what used to work.

| Spec | Value | Source |
| :- | :- | :- |
| Model ID | `step-image-edit-2` | model page |
| Scale | Under 6B parameters — lightweight generation and editing | model page |
| Latency | 1–2 seconds per editing task | model page |
| Prompt length | 512 characters | model page, and both API references |
| Input image limit | 4096 × 4096 (editing scenarios) | model page, `edits.md` |
| Text-to-image sizes | `1024x1024`, `768x1360`, `896x1184`, `1360x768`, `1184x896` — **format is `height x width`** | model page, `image.md` |
| `n` | **One image per request only** | `image.md` |
| `steps` | Range `[1, 50]`, default 8 | both API references |
| `cfg_scale` | Must be ≥ 1.0, range `[1.0, 10.0]`, default 1.0 | both API references |
| `seed` | Range `[0, 2147483647]`; server generates one if omitted | both API references |
| `negative_prompt` | Up to 512 characters, default `""`; **not passed to the underlying model when `cfg_scale = 1.0`** | both API references |
| `text_mode` | `bool`, default `False`; optimization for text-rendering scenarios | both API references |
| `size` on edits | **Ignored** — the result is returned at the same size as the input image | `edits.md` |
| `response_format` | `b64_json` or `url`, default `url`; the URL is valid for **2 hours** | both API references |
| `finish_reason` | `success`, or `content_filtered` (generated but stopped by content filtering) | both API references |
| Price | **$0.003 / image** for text-to-image / image editing | model page |

Endpoints were: text-to-image `POST /v1/images/generations`, image editing
`POST /v1/images/edits`. Editing is multipart (`-F image=@input.webp`); generation is
JSON.

## What to do instead

**There is no documented successor.** Options, in order:

1. **Do not migrate yet** — nothing to migrate *to* is named in the sources, and
   the live endpoints now reject the model outright.
2. **Download and store** any image you need to keep; URLs expired in 2 hours anyway.
3. **Re-check the dashboard** for a replacement before answering any image
   question — a successor could appear without the corpus noticing.

Any claim that a specific model replaces it would be invented — the sources are
silent, and the honest answer is "not documented".
