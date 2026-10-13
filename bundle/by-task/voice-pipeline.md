---
card: voice-pipeline
tier: by-task
status: draft
verified_on: 2026-10-08 (Step Plan verified; Standard column unverified)
source: corpus/guides/models/audio.md, corpus/api-reference/audio/create-audio.md, corpus/api-reference/audio/asr-sse.md, corpus/api-reference/audio/ws-audio.md, corpus/step-plan/overview.md
---

# Voice pipeline: ASR → reasoning → TTS

The only voice architecture this account can build is a **three-hop pipeline**:
`stepaudio-2.5-asr` (transcribe) → a reasoning model → `stepaudio-2.5-tts` (speak).
There is no single-model shortcut on this account — see "NOT available" below.

| Stage | Model | Channel | Step Plan URL | Standard URL | Returns |
| --- | --- | --- | --- | --- | --- |
| 1. Transcribe | `stepaudio-2.5-asr` | both | `POST https://api.stepfun.ai/step_plan/v1/audio/asr/sse` | `POST https://api.stepfun.ai/v1/audio/asr/sse` | SSE: `transcript.text.delta` … `transcript.text.done` |
| 2. Reason | `step-5-preview` / `step-3.7-flash` / `step-3.5-flash` / `step-3.5-flash-2603` | both | `POST https://api.stepfun.ai/step_plan/v1/chat/completions` | `POST https://api.stepfun.ai/v1/chat/completions` | streamed text reply |
| 3. Speak | `stepaudio-2.5-tts` | both | `POST https://api.stepfun.ai/step_plan/v1/audio/speech` (one-shot) or `wss://api.stepfun.ai/step_plan/v1/realtime/audio` (streaming) | `POST https://api.stepfun.ai/v1/audio/speech` or `wss://api.stepfun.ai/v1/realtime/audio?model=stepaudio-2.5-tts` | audio file / audio chunks |

Full per-endpoint parameters and event payloads: [audio.md](audio.md).
Chat-hop parameters: [chat-apis.md](chat-apis.md).

## The three hops

**1. Transcribe.** POST Base64-encoded audio to the ASR SSE endpoint with
`audio.input.transcription` (`model`, `language`, `enable_itn`) and
`audio.input.format` (`type`/`codec`/`rate`/`bits`/`channel`). The server streams
`transcript.text.delta` events and ends with `transcript.text.done`. A 5-minute
clip transcribes in ~1 second; ASR one-shot formats are PCM / OGG / MP3 / WAV.

**2. Reason.** Send the transcript to Chat Completions with any of the four
reasoning models above and stream the reply. Reasoning effort per model is in
[reasoning.md](reasoning.md). For large contexts, count tokens first with
`POST /v1/token/count` (standard channel — pay-as-you-go).

**3. Speak.** Feed the reply to `stepaudio-2.5-tts`:

- **One-shot** `POST /v1/audio/speech` — max 1,000 chars/request; formats
  `wav`/`mp3`/`flac`/`opus`/`pcm`; `speed`, `volume`, `instruction` (≤200 chars),
  `sample_rate`, `pronunciation_map`.
- **Streaming** (lower latency) WebSocket
  `wss://api.stepfun.ai/v1/realtime/audio?model=stepaudio-2.5-tts` — send
  `tts.create`, stream text via `tts.text.delta`, receive
  `tts.response.audio.delta`; `tts.text.flush` forces remaining audio out;
  `tts.text.done` ends the task. **Default mode buffers text into sentences**
  (built for LLM+TTS pairing) — flush when the LLM stream ends so the tail is
  spoken.

## Step Plan URLs (overseas — draws on Credits)

Pipeline code uses the Step Plan channel exclusively — Step Plan API key plus
`/step_plan/` base URLs. Standard-address requests bill to pay-as-you-go, **not**
Credits (Rule 6 — [endpoints.md](../always-load/endpoints.md)).

| Hop | Step Plan URL | Standard URL |
| --- | --- | --- |
| Chat Completions base | `https://api.stepfun.ai/step_plan/v1` | `https://api.stepfun.ai/v1` |
| TTS streaming (WebSocket) | `wss://api.stepfun.ai/step_plan/v1/realtime/audio` | `wss://api.stepfun.ai/v1/realtime/audio` |
| Voice clone preview | `POST https://api.stepfun.ai/step_plan/v1/audio/voices/preview` | `POST https://api.stepfun.ai/v1/audio/voices/preview` |

Standard-channel equivalents (`https://api.stepfun.ai/v1`) draw on the
pay-as-you-go balance, NOT Step Plan Credits.

## Voice cloning (via `stepaudio-2.5-tts`)

1. Upload 5–10s reference audio (mp3/wav): `POST /v1/files` with
   `purpose=storage` → `file_id` ([files.md](files.md)).
2. **Preview** (no permanent asset): `POST /v1/audio/voices/preview` — `model`,
   `file_id`, `sample_text` (<50 chars), optional transcript `text`,
   `instruction`.
3. **Create permanent voice** ($1.50/voice, standard-channel rate):
   `POST /v1/audio/voices` — returns voice `id` plus base64 `sample_audio`.
4. Cloned voices support `language` omitted / `zh` / `en` only; other languages
   return `400 input_invalid`.

## NOT available on this account

The shortcut architectures that would collapse the three hops are
**reference-only in the docs and not callable with this key**:

| Shortcut model | What it would replace | Step Plan | Standard | Status |
| --- | --- | --- | --- | --- |
| `stepaudio-2.5-chat` | audio-in → text-out; removes the separate ASR hop (and adds tone understanding) | ❌ | *(unverified)* | not callable |
| `stepaudio-2.5-realtime` / `stepaudio-3-realtime-preview` | full-duplex speech-to-speech; replaces the whole pipeline | ❌ | *(unverified)* | not callable |
| `stepaudio-2.5-asr-stream` | streaming-ASR WebSocket | ❌ confirmed 2026-10-13 | *(unverified)* | model ID not on this account |
| `stepaudio-3-tts` | cheaper TTS | ❌ | *(unverified)* | not callable |
| `step-router-v1` | smart routing | ❌ | *(unverified)* | not callable |

Their specs live in the v1 workspace `specs/models/` with NOT-AVAILABLE banners —
reference only if the plan changes. Availability is governed by
[models.md](../always-load/models.md).

## Cost cheat sheet — by channel

| Stage | Model | Step Plan | Standard |
| --- | --- | --- | --- |
| ASR | `stepaudio-2.5-asr` | Credits | $0.022 / hour of audio |
| TTS | `stepaudio-2.5-tts` | Credits | $0.85 / 10,000 characters |
| Voice cloning | `stepaudio-2.5-tts` | Credits | $1.50 / voice |
| Reasoning (in / out per 1M tokens) | `step-5-preview` | Credits | *(fill in from pricing page)* |
| | `step-3.7-flash` | Credits | *(fill in)* |
| | `step-3.5-flash` / `step-3.5-flash-2603` | Credits | *(fill in)* |

## Guardrails

- TTS input ≤ 1,000 chars/request; `instruction` ≤ 200 chars.
- ASR one-shot formats: PCM / OGG / MP3 / WAV.
- Files: max 128 MB, 1,000 files per user; cloning audio 5–10 seconds
  ([files.md](files.md)).
- Prompt caching for repeated prefixes in the reasoning hop:
  [context-and-cache.md](context-and-cache.md).
- Errors, retries, idempotency: covered by the v1 guide
  `docs/guides/exception-handling.md`; no bundle card yet — not documented here.
- `step-image-edit-2` **retired 2026-10-10** — no image model is callable here
  now; see [images.md](images.md).
