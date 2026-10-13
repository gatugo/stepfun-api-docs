---
card: standard-channel
tier: always-load
status: verified
verified_on: 2026-10-13
source: _account/live-calls/2026-10-13-models.md, _account/live-calls/2026-10-13-image-api-retired.md, corpus/guides/pricing/intro.md, corpus/guides/pricing/details.md
---

# Standard pay-as-you-go channel

Verified by live model-list call on 2026-10-13. The Standard channel returns
**15 models** vs 6 on Step Plan — see [`models.md`](models.md) for the
full allowlist.

## Base URL

```
https://api.stepfun.ai/v1
```

## The key

The **same API key** used for Step Plan authenticates here. The channel is
selected by base URL alone — no separate key needed. Standard-channel calls
bill per-call in USD; they do **not** consume Step Plan Credits.

## Model allowlist — verified 2026-10-13

| Model | Notes |
|---|---|
| `step-5-preview` | Flagship; 1M context |
| `step-3.7-flash` | Multimodal reasoning |
| `step-3.5-flash` | General reasoning |
| `step-3.5-flash-2603` | High-frequency agent build |
| `stepaudio-2.5-tts` | Text to speech |
| `stepaudio-2.5-asr` | Speech recognition (one-shot SSE) |
| `stepaudio-2.5-chat` | Audio-in → text-out (tone understanding) |
| `stepaudio-2.5-realtime` | Full-duplex speech-to-speech |
| `stepaudio-2.5-asr-stream` | Streaming ASR (WebSocket) |
| `stepaudio-3-asr-max` | High-quality ASR (StepAudio 3) |
| `stepaudio-3-chat-preview` | Real-time voice chat (StepAudio 3) |
| `stepaudio-3-gen-preview` | Audio generation (StepAudio 3) |
| `stepaudio-3-music-preview` | Music generation (StepAudio 3) |
| `stepaudio-3-realtime-preview` | Full-duplex speech-to-speech (StepAudio 3) |
| `stepaudio-3-tts` | Text to speech (StepAudio 3) |

8 Standard-only models (absent from Step Plan): `stepaudio-2.5-chat`,
`stepaudio-2.5-realtime`, `stepaudio-2.5-asr-stream`, and the 6-model
StepAudio 3 family (`stepaudio-3-asr-max`, `stepaudio-3-chat-preview`,
`stepaudio-3-gen-preview`, `stepaudio-3-music-preview`,
`stepaudio-3-realtime-preview`, `stepaudio-3-tts`).

Not on any channel: `step-router-v1` · `step-2x-large` · `step-1x-edit` ·
`deepseek-v4-pro` · `step-image-edit-2` (**retired 2026-10-10** — endpoints
return HTTP 400 `model step-image-edit-2 not supported`)

## Pricing (standard channel — pay-as-you-go USD)

| Model | Price |
|---|---|
| `step-5-preview` | *(see corpus/guides/pricing/details.md)* |
| `step-3.7-flash` | *(fill in)* |
| `step-3.5-flash` / `step-3.5-flash-2603` | *(fill in)* |
| `stepaudio-2.5-tts` | $0.85 / 10,000 characters |
| `stepaudio-2.5-asr` | $0.022 / hour of audio |
| `stepaudio-2.5-asr-stream` | $0.18 / hour of audio |
| `stepaudio-3-tts` | *(fill in from pricing page)* |
| `stepaudio-3-asr-max` | *(fill in)* |
| Voice cloning (`stepaudio-2.5-tts`) | $1.50 / voice |

Full pricing: `corpus/guides/pricing/details.md`.

## What still needs live verification (Q-STD-03)

The model list endpoint is confirmed. The following need a live call to
confirm the Standard-channel endpoint shapes and actual model behaviour:

| Endpoint | Blocker |
|---|---|
| Chat Completions (`POST /v1/chat/completions`) | no live call yet |
| ASR one-shot (`POST /v1/audio/asr/sse`) | no live call yet |
| TTS one-shot (`POST /v1/audio/speech`) | no live call yet |
| Files (`POST /v1/files`) | no live call yet |
| Responses API (`POST /v1/responses`) | no live call yet |
| Reasoning effort parity for `step-3.5-flash*` | confirmed ✅ |
| `stepaudio-3-tts`, `stepaudio-3-asr-max`, etc. | unverified |
