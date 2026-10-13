---
card: account-access
tier: account
status: verified
verified_on: 2026-10-13
source: live call to GET /v1/models and GET /step_plan/v1/models, 2026-10-13; owner instructions
---

# Account facts — verified

> **This card outranks the corpus.** The vendor docs describe the platform's
> general capability set; this card describes *this subscription*. Where they
> disagree, this card wins — and the disagreement gets an evidence card, not a
> silent edit.
>
> **Example snapshot.** The values below were verified by live call on the date
> in the frontmatter. They are a worked example of what a filled-in rank-1 card
> looks like — replace them with the output of your own
> `GET /v1/models` and `GET /step_plan/v1/models` calls. Never paste your API key
> into this file; record only the model IDs it can reach.

## Region

| Fact | Value |
| :- | :- |
| Platform | **Overseas** — `platform.stepfun.ai` |

## One key, two channels

| | Step Plan | Standard |
|---|---|---|
| **Base URL** | `https://api.stepfun.ai/step_plan/v1` | `https://api.stepfun.ai/v1` |
| **Billing** | Credits (monthly allowance, ≈ $1 = 7M Credits, no rollover) | Pay-as-you-go USD (per-call rates) |
| **API key** | Same key used for both channels | Same key used for both channels |
| **How to select** | Use the `/step_plan/` base URL | Use the `/v1` base URL |

> **The key is identical.** Which channel a call lands in is determined entirely
> by which base URL is used. Step Plan Credits are only consumed when hitting a
> `/step_plan/` endpoint. Standard-channel calls always bill per-call in USD.

## Callable models — verified by live call 2026-10-13

**Step Plan: 6 models** — `step-5-preview` · `step-3.7-flash` · `step-3.5-flash` · `step-3.5-flash-2603` · `stepaudio-2.5-tts` · `stepaudio-2.5-asr`

**Standard: 15 models** — all 6 Step Plan models plus:
`stepaudio-2.5-chat` · `stepaudio-2.5-realtime` · `stepaudio-2.5-asr-stream` · `stepaudio-3-asr-max` · `stepaudio-3-chat-preview` · `stepaudio-3-gen-preview` · `stepaudio-3-music-preview` · `stepaudio-3-realtime-preview` · `stepaudio-3-tts`

Full capability table: [`../bundle/always-load/models.md`](../bundle/always-load/models.md).

## Channel rule — Rule 6

Pipeline and integration code **must use the correct base URL** for the intended
billing channel. Mixing them is silent and expensive: a standard-address request
enters the pay-as-you-go channel and does **not** consume Step Plan Credits.

| Intent | Use |
|---|---|
| Spend Credits | `https://api.stepfun.ai/step_plan/v1/...` |
| Spend USD | `https://api.stepfun.ai/v1/...` |

## Reasoning effort — verified by live calls

| Model | Effort levels | Step Plan | Standard |
|---|---|---|---|
| `step-5-preview` | `low` / `medium` / `high` | Official | Official |
| `step-3.7-flash` | `low` / `medium` / `high` | Official | Official |
| `step-3.5-flash-2603` | `low` / `medium` / `high` | Verified 2026-10-08 | Verified 2026-10-13 |
| `step-3.5-flash` | `low` / `medium` / `high` | Verified 2026-10-08 | Verified 2026-10-13 |

The API reference claims `step-3.5-flash-2603` is `low`/`high` only; live calls
disproved it on both channels. Resolution: `bundle/evidence/source-contradictions.md`.

## Not callable on this account

| Model | Step Plan | Standard | Notes |
|---|---|---|---|
| `step-router-v1` | ❌ | ❌ | smart routing |
| `step-2x-large` | ❌ | ❌ | retired 2026-10-10 |
| `step-1x-edit` | ❌ | ❌ | retired 2026-10-10 |
| `deepseek-v4-pro` | ❌ | ❌ | third-party model |
| `step-image-edit-2` | ❌ | ❌ | **retired 2026-10-10** — endpoints return HTTP 400 `model step-image-edit-2 not supported` |

The StepAudio 3 ASR, TTS, chat, realtime, music, and gen models are
**callable on Standard** — see the allowlist table in `models.md`.

Detail: [`../bundle/evidence/models/not-on-this-plan.md`](../bundle/evidence/models/not-on-this-plan.md).

## Hard deadline — PASSED

`step-image-edit-2` (and `step-2x-large`) retired **2026-10-10**. That date has
passed: text-to-image, image-to-image, and image editing **have stopped serving**
on both channels. Live-verified 2026-10-13 — `POST /v1/images/generations` and
`POST /step_plan/v1/images/generations` both return HTTP 400
`model step-image-edit-2 not supported`. Detail:
[`../bundle/evidence/models/step-image-edit-2.md`](../bundle/evidence/models/step-image-edit-2.md).

