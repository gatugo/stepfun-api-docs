---
card: images
tier: by-task
status: verified
verified_on: 2026-10-13
source: _account/live-calls/2026-10-13-image-api-retired.md, corpus/guides/image-offline-notice.md, corpus/guides/models/image.md, corpus/guides/models/step-image-edit-2.md, corpus/api-reference/images/image.md, corpus/api-reference/images/edits.md
---

# Image generation and editing — RETIRED 2026-10-10

⚠️ **The image-generation API retired on 2026-10-10 and is confirmed dead.** The
text-to-image, image-to-image, and image editing endpoints **stop serving
requests on both the Open Platform and Step Plan channels**. Live-verified
2026-10-13: `POST /v1/images/generations` and `POST /step_plan/v1/images/generations`
both return **HTTP 400 `model step-image-edit-2 not supported`**, and
`step-image-edit-2` has dropped out of the live Step Plan model list.

Image *understanding* (image/video input to chat models) is unaffected — see
[vision-and-video.md](vision-and-video.md).

| Item | Detail |
| --- | --- |
| Retirement date | **October 10, 2026** — passed |
| Retiring models | `step-2x-large`, `step-image-edit-2` |
| Already retired | `step-1x-edit` — no longer available |
| Retiring capabilities | text-to-image, image-to-image, image editing |
| On this account | **No image model is callable** — `step-image-edit-2` was the only one and it is now gone ([models.md](../always-load/models.md)) |
| Live status | HTTP 400 `model step-image-edit-2 not supported` on both channels, 2026-10-13 |

Evidence: [`../evidence/models/step-image-edit-2.md`](../evidence/models/step-image-edit-2.md)
and [`../../_account/live-calls/2026-10-13-image-api-retired.md`](../../_account/live-calls/2026-10-13-image-api-retired.md).

Affected endpoints (all stopped serving on 2026-10-10):

| Channel | Capability | Endpoint |
| --- | --- | --- |
| Open Platform (standard — pay-as-you-go) | text-to-image | `POST /v1/images/generations` |
| Open Platform (standard — pay-as-you-go) | image-to-image | `POST /v1/images/image2image` |
| Open Platform (standard — pay-as-you-go) | image editing | `POST /v1/images/edits` |
| Step Plan | text-to-image | `POST /step_plan/v1/images/generations` |
| Step Plan | image editing | `POST /step_plan/v1/images/edits` |

Other Step Plan models (text, reasoning, speech) are **not** affected. Studio
loses image generation too. Image download links kept their own validity
(2 hours) — anything needed long-term had to be stored before the retirement.

## The model, for reference (no longer callable)

One model covered both text-to-image and image editing; under 6B parameters,
1–2 seconds per edit, prompt max 512 characters.

| Param | Required | Default / range | Notes |
| --- | --- | --- | --- |
| `model` | Yes | — | `step-image-edit-2` — the only supported model on these endpoints |
| `prompt` | Yes | max 512 chars | |
| `image` | Yes (edits only) | — | one file; max input resolution 4096x4096; Base64 supported |
| `size` | No | `1024x1024` (generations) | generations: `1024x1024`, `768x1360`, `896x1184`, `1360x768`, `1184x896` — format is **height x width**; **ignored for edits** (result returns at the input image's size) |
| `n` | No | 1 | only one image per request |
| `response_format` | No | `url` | `b64_json` or `url`; URLs valid ~2 hours |
| `seed` | No | random | range `[0, 2147483647]` |
| `steps` | No | 8 | range `[1, 50]` |
| `cfg_scale` | No | 1.0 | must be ≥ 1.0, range `[1.0, 10.0]`; **when 1.0, `negative_prompt` is not passed to the model** |
| `negative_prompt` | No | `""` | up to 512 chars |
| `text_mode` | No | `False` | text-rendering optimization; enable as needed |

Pricing, for historical reference (standard channel — pay-as-you-go):
**$0.003 / image** for text-to-image and editing; on Step Plan, billed in Credits.

## Negatives

- **No replacement image model is offered in the sources** — nothing succeeds
  `step-image-edit-2` on this account, and the live endpoints now reject it.
- `step-1x-edit` is already gone; the legacy step-1x line (2B parameters, its own
  size list) is retired context.
- `step-2x-large` (text-to-image focused, stronger Chinese/English text
  rendering) is documented but **not on this account**, and retired with the API.
- `size` did nothing on edits; `negative_prompt` was dropped at `cfg_scale = 1.0`.
- **The endpoints answer 400, not 404.** An absence check that looks only for 404
  would wrongly conclude the endpoint was merely missing — see the 429-vs-404
  rule in [`../evidence/source-contradictions.md`](../evidence/source-contradictions.md).

## Related cards

[vision-and-video.md](vision-and-video.md) (image/video *input* — unaffected) ·
[models.md](../always-load/models.md) (availability) ·
[voice-pipeline.md](voice-pipeline.md) · [audio.md](audio.md).
