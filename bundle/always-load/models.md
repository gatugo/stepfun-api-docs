---
card: models
tier: always-load
status: verified
verified_on: 2026-10-13
source: _account/live-calls/2026-10-13-models.md, _account/live-calls/2026-10-13-image-api-retired.md, corpus/guides/models/overview.md
---

# Models available on this account

> **Two channels, different allowlists.** The same key works on both, but each
> channel returns a different model set. The table below is verified by live call
> on 2026-10-13. Where a model is channel-specific, both columns are shown.
>
> ⚠️ **The image API is retired and dead.** A second live pass on 2026-10-13
> confirmed `POST /v1/images/generations` and `POST /step_plan/v1/images/generations`
> both return **HTTP 400 `model step-image-edit-2 not supported`**, and
> `step-image-edit-2` has dropped out of the Step Plan model list. Evidence:
> [`../../_account/live-calls/2026-10-13-image-api-retired.md`](../../_account/live-calls/2026-10-13-image-api-retired.md).

## Verified model allowlist — 15 callable on Standard, 6 on Step Plan

| Model ID | Channel | Type | Context | Input | Protocols |
|---|---|---|---|---|---|
| `step-5-preview` | both | Flagship, agentic | 1M | text, image, video | chat, messages, responses |
| `step-3.7-flash` | both | High-speed multimodal reasoning | 256K | text, image, video | chat, messages, responses |
| `step-3.5-flash` | both | High-speed general reasoning | 256K | text | chat, messages |
| `step-3.5-flash-2603` | both | High-frequency agent build | 256K | text | chat, messages |
| `stepaudio-2.5-tts` | both | Text to speech | — | text ≤ 1,000 chars | — |
| `stepaudio-2.5-asr` | both | Speech recognition | — | audio | — |
| `stepaudio-2.5-chat` | **Standard only** | Audio-in → text-out (understands tone) | — | audio | — |
| `stepaudio-2.5-realtime` | **Standard only** | Full-duplex speech-to-speech | — | audio | — |
| `stepaudio-2.5-asr-stream` | **Standard only** | Streaming ASR (WebSocket) | — | audio | — |
| `stepaudio-3-asr-max` | **Standard only** | High-quality ASR (StepAudio 3) | — | audio | — |
| `stepaudio-3-chat-preview` | **Standard only** | Real-time voice chat (StepAudio 3) | — | audio | — |
| `stepaudio-3-gen-preview` | **Standard only** | Audio generation (StepAudio 3) | — | text | — |
| `stepaudio-3-music-preview` | **Standard only** | Music generation (StepAudio 3) | — | text | — |
| `stepaudio-3-realtime-preview` | **Standard only** | Full-duplex speech-to-speech (StepAudio 3) | — | audio | — |
| `stepaudio-3-tts` | **Standard only** | Text to speech (StepAudio 3) | — | text ≤ 1,000 chars | — |

> **Step Plan allowlist: 6 models** (the 6 "both" rows above minus the 8 Standard-only).
> `stepaudio-2.5-asr-stream` is **not callable on Step Plan** (HTTP 404 confirmed
> 2026-10-13); all others absent from Step Plan are unverified there.
>
> **Standard-only models are unverified for actual API calls** (transcription,
> generation, etc.) — only the model list endpoint was queried. Confirm per-model
> behaviour before relying on them in production.

## Reasoning effort — verified by live calls

| Model | Effort levels | Channel | Status |
|---|---|---|---|
| `step-5-preview` | `low` / `medium` / `high` | both | Official |
| `step-3.7-flash` | `low` / `medium` / `high` | both | Official |
| `step-3.5-flash-2603` | `low` / `medium` / `high` | Step Plan | Verified 2026-10-08 |
| `step-3.5-flash` | `low` / `medium` / `high` | Step Plan | Verified 2026-10-08 |
| `step-3.5-flash-2603` | `low` / `medium` / `high` | Standard | Verified 2026-10-13 (HTTP 200 with `medium`) |
| `step-3.5-flash` | `low` / `medium` / `high` | Standard | Verified 2026-10-13 (HTTP 200 with `medium`) |

Chat Completions sets `reasoning_effort`; the Messages API sets `output_config.effort`. `step-5-preview` maps client `xhigh`/`max` down to `high`.

**The API reference is wrong on this point.** It states "models that support three reasoning tiers accept `low`, `medium`, `high`; `step-3.5-flash-2603` accepts `low` and `high` only" — live calls on 2026-10-08 returned HTTP 200 with `medium` on both 3.5 variants. An earlier owner ruling (v1 ADR-005) that put base `step-3.5-flash` at `low`/`high` was disproved by the same test. Resolution and evidence: [`../evidence/source-contradictions.md`](../evidence/source-contradictions.md).

## Not on this account — by channel

| Model | Step Plan | Standard | Notes |
|---|---|---|---|
| `step-router-v1` | ❌ | ❌ | smart routing |
| `step-2x-large` | ❌ | ❌ | large text; retired 2026-10-10 |
| `step-1x-edit` | ❌ | ❌ | image edit; retired 2026-10-10 |
| `deepseek-v4-pro` | ❌ | ❌ | third-party model |
| `step-image-edit-2` | ❌ | ❌ | **retired 2026-10-10** — both endpoints now return HTTP 400 `model step-image-edit-2 not supported` |
| All `stepaudio-3` models **except** those in the allowlist | ❌ | ❌ | see allowlist above for the 6 Standard-callable ones |

Full allowlist: [`../evidence/models/not-on-this-plan.md`](../evidence/models/not-on-this-plan.md).

## Token limits

| Model | Max input (context) | Max output | Confidence |
|---|---|---|---|
| `step-5-preview` | 1M tokens | 64k tokens | **Official** |
| `step-3.7-flash` | 256K tokens | 64k | **Inferred** — family resemblance |
| `step-3.5-flash` | 256K tokens | 64k | **Inferred** — arXiv:2602.10604 |
| `step-3.5-flash-2603` | 256K tokens | 64k | **Inferred** — inherited from `step-3.5-flash` |

Audio models (`stepaudio-*`) have no documented context window — they process fixed-length inputs.

**The rule that governs output:** `max_tokens` defaults to **INF** — no per-model hard output cap on the Chat Completions API. Real ceiling is *input + output ≤ the context window*. The 64k figures are practical budgets, not enforced walls. Provenance: [`../evidence/models/token-limits.md`](../evidence/models/token-limits.md).

Claude Code assumes a 200k context and will mis-report `step-5-preview`; override in `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "1000000",
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000"
  }
}
```

Plain integers only — never `1M` or `1000k`. The auto-compact window range is `100000`–`1000000`.

## Prompt caching
Supported on `step-5-preview`, `step-3.7-flash`, `step-3.5-flash`, `step-3.5-flash-2603`. Not documented for the audio or image models. Detail: [`../by-task/context-and-cache.md`](../by-task/context-and-cache.md).

## Choose a model

| Task | Choose |
|---|---|
| Default / general agent work | `step-5-preview` |
| Deep reasoning, planning, code analysis | `step-5-preview` at `high` effort |
| Fast, cheap, high-frequency agent turns | `step-3.5-flash-2603` |
| Multimodal (image/video) at speed | `step-3.7-flash` |
| Text-only, speed-first, token-budget efficiency | `step-3.5-flash` |
| Text to speech | `stepaudio-2.5-tts` |
| Text to speech (StepAudio 3) | `stepaudio-3-tts` — Standard only |
| Transcribe audio | `stepaudio-2.5-asr` |
| Transcribe audio (high-quality) | `stepaudio-3-asr-max` — Standard only |
| Streaming ASR (WebSocket) | `stepaudio-2.5-asr-stream` — Standard only |
| Audio-in → text-out (tone understanding) | `stepaudio-2.5-chat` — Standard only |
| Full-duplex speech-to-speech | `stepaudio-2.5-realtime` — Standard only |
| Generate or edit an image | *Not available* — the image API **retired 2026-10-10**; both endpoints return HTTP 400 |
| "Pick something sensible for me" | *Not available* — `step-router-v1` is not on this account |

## Re-verify this list
Run `GET /v1/models` and `GET /step_plan/v1/models` and compare. The allowlist
is the live response, not the docs. When a new model appears, update this card
and log the change in `decisions.md`.
