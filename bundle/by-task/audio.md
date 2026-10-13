---
card: audio
tier: by-task
status: draft
verified_on: 2026-10-13 (ASR one-shot + TTS one-shot live-verified on both channels; WebSocket untested)
source: corpus/guides/developer/tts.md, corpus/guides/models/audio.md, corpus/api-reference/audio/create-audio.md, corpus/api-reference/audio/asr-sse.md, corpus/api-reference/audio/ws-audio.md, corpus/api-reference/audio/create-voice.md, corpus/api-reference/audio/voices-preview.md
---

# Audio: TTS, ASR, and voice cloning

Two audio models are callable on this account: **`stepaudio-2.5-tts`** (text →
speech) and **`stepaudio-2.5-asr`** (speech → text, one-shot). Everything else in
the audio docs is reference-only — see the bottom of this card. For how the hops
chain into a voice agent, see [voice-pipeline.md](voice-pipeline.md).

| Capability | Model | Step Plan URL (pipeline code) | Standard URL (standard channel — pay-as-you-go) |
| --- | --- | --- | --- |
| Text-to-speech, one-shot | `stepaudio-2.5-tts` | `POST https://api.stepfun.ai/step_plan/v1/audio/speech` | `POST https://api.stepfun.ai/v1/audio/speech` |
| Text-to-speech, streaming | `stepaudio-2.5-tts` | `wss://api.stepfun.ai/step_plan/v1/realtime/audio` | `wss://api.stepfun.ai/v1/realtime/audio?model=stepaudio-2.5-tts` |
| Speech recognition, one-shot SSE | `stepaudio-2.5-asr` | `POST https://api.stepfun.ai/step_plan/v1/audio/asr/sse` | `POST https://api.stepfun.ai/v1/audio/asr/sse` |
| Voice clone preview | `stepaudio-2.5-tts` | `POST https://api.stepfun.ai/step_plan/v1/audio/voices/preview` | `POST https://api.stepfun.ai/v1/audio/voices/preview` |
| Voice clone, permanent | `stepaudio-2.5-tts` | not documented in sources | `POST https://api.stepfun.ai/v1/audio/voices` |
| ASR streaming (WebSocket) | `stepaudio-2.5-asr-stream` | — | `wss://api.stepfun.ai/v1/realtime/asr/stream` — **NOT on this account** |

## Text-to-Speech — `POST /v1/audio/speech`

Non-streaming; returns a complete audio file (best quality).

| Param | Required | Default / range | Channel | Notes |
| --- | --- | --- | --- | --- |
| `model` | Yes | — | both | `stepaudio-2.5-tts` — the only TTS model on this account. `stepaudio-3-tts` exists in the docs but is NOT callable here. An older TTS model name is deprecated but existing user requests continue to be served |
| `input` | Yes | max 1,000 chars | Parenthesized `()` content is treated as instructions and is NOT spoken |
| `voice` | Yes | — | official or custom cloned voice IDs (list below) |
| `language` | No | `en` | `zh` `en` `ja` `ko` `fr` `es`; ja/ko/fr/es in preview |
| `response_format` | No | `mp3` | `wav`, `mp3`, `flac`, `opus`, `pcm` |
| `speed` | No | 0.5–2.0, default 1.0 | 0.5 = half speed |
| `volume` | No | 0.1–2.0, default 1.0 | 0.1 = 10%, 2.0 = 200% |
| `instruction` | No | max 200 chars (500 for `stepaudio-3-tts`, not callable here) | global natural-language delivery guidance (tone, scene, persona) |
| `sample_rate` | No | `24000` | `8000`, `16000`, `22050`, `24000`, `48000` |
| `pronunciation_map` | No | — | per-character/symbol overrides; Chinese tones as digits 1–5, e.g. `["LOL/laugh out loudly"]` |
| `stream_format` | No | `audio` | `sse` returns `speech.audio.delta` … `speech.audio.done` events |
| `markdown_filter` | No | — | boolean |
| `return_url` | No | false | non-streaming only; returns a download URL valid **12 hours** instead of binary audio |

Inline context (parentheses inside `input`) fine-tunes per-sentence emotion,
pauses, and breathing; global context (`instruction`) sets the passage-level
delivery. You own the audio you generate (disclose AI generation to end users).

## TTS streaming — WebSocket `/v1/realtime/audio`

Send `tts.create` after `tts.connection.done`, stream text with `tts.text.delta`,
collect `tts.response.audio.delta` chunks. Idle connections auto-close after
**60 seconds**.

| Client event | Server event | Purpose |
| --- | --- | --- |
| `tts.create` | `tts.response.created` | open session (`session_id`, `voice_id` required) |
| `tts.text.delta` | `tts.response.audio.delta` | send text increments (max 1,000 chars); receive audio chunks |
| — | `tts.response.sentence.start` / `.sentence.end` | sentence generation boundaries (carry `request_id`) |
| `tts.text.flush` | `tts.text.flushed` | force all buffered audio out |
| `tts.text.done` | `tts.response.audio.done` | end the task; server releases the connection |
| — | `tts.response.error` | generation error (e.g. code `503`, engine overloaded) |

`tts.create` data: `session_id` (from `tts.connection.done`), `voice_id`,
`language`, `response_format` (adds streaming variants `mp3_stream`,
`opus_stream`, `flac_stream`; default `mp3`), `sample_rate`,
`pronunciation_map`, `speed_ratio` (0.5–2.0, default 1.0), `volume_ratio`
(0.1–2.0, default 1.0), `mode` (`default` = character-level, buffers into
sentences for LLM pairing; `sentence` = sentence-level for prepared text),
`instruction` (max 200 chars), `markdown_filter`.

⚠️ The docs warn `stepaudio-2.5-tts` may produce **significantly lower quality**
in WebSocket streaming mode than non-streaming HTTP — prefer the one-shot API
when latency is not critical.

## Speech recognition — `POST /v1/audio/asr/sse`

One-shot: Base64 audio in, transcription streamed back over SSE. Headers:
`Content-Type: application/json`, `Accept: text/event-stream`,
`Authorization: Bearer <key>`.

| Field | Required | Channel | Notes |
| --- | --- | --- | --- |
| `audio.data` | Yes | both | Base64-encoded audio |
| `audio.input.transcription.model` | — | both | `stepaudio-2.5-asr` on this account; the docs also list `stepaudio-3-asr-max` ("recommended") — **NOT callable here** |
| `audio.input.transcription.language` | No | defaults to English; `zh` `en` `ja` `ko` `fr` `es` (non-zh/en in preview; the model page documents Chinese and English) |
| `audio.input.transcription.enable_itn` | No | default `true` (inverse text normalization) |
| `audio.input.format` | — | `type` (`ogg` `mp3` `wav` `pcm` `m4a`), `codec` (e.g. `pcm_s16le`), `rate`, `bits`, `channel` — `rate`/`bits`/`channel` required for `pcm`, optional otherwise |

> ⚠️ **`format` lives inside `audio.input`, not beside `audio.data`.** Putting it
> at the `audio` level returns
> `400 {"error":{"message":"audio format is required"}}` — a flat reading of the
> docs' example gets this wrong (live-verified 2026-10-13).

Events: `transcript.text.delta` (incremental `delta`, `meta.session_id`,
`meta.timestamp`) → `transcript.text.done` (complete `text` plus `usage`) ·
`error` (carries `message`). The SSE endpoint no longer supports
`full_rerun_on_commit` — legacy clients sending it are ignored, not errored.

4B-parameter MTP architecture; ~400% throughput / ~60% lower latency vs.
traditional ASR; a 5-minute clip fully transcribes in ~1 second.

## Voice cloning

| Step | Endpoint | Channel | Key params | Result |
| --- | --- | --- | --- | --- |
| Upload reference audio | `POST /v1/files` ([files.md](files.md)) | Standard | `purpose=storage`; mp3/wav, 5–10 seconds | `file_id` |
| Preview (no permanent asset) | `POST /v1/audio/voices/preview` | Standard | `model`, `file_id`, `sample_text` (required, <50 chars), optional `text` (transcript; ASR used if omitted), `instruction` (≤200 chars), `response_format`, `speed`, `volume`, `sample_rate`, `pronunciation_map`, `markdown_filter` | `sample_audio` (base64 wav), `sample_text`, `request_id` |
| Create permanent voice ($1.50/voice, standard rate) | `POST /v1/audio/voices` | Standard | `model`, `file_id`, optional `text` (transcript recommended), optional `sample_text` (≤50 chars) | voice `id`, `object` (`audio.voice`), `duplicated`, `sample_audio` (base64 wav) |

Zero-shot cloning needs about **3 seconds** of reference audio per the model
page (the endpoint spec asks for 5–10 seconds); cloned voices keep full
global/inline context control at no additional cost. **Cloned voices support
`language` omitted / `zh` / `en` only** — any other language returns
`400 input_invalid` (`voice <voice_id> does not support language <language>`).

### System voices

| Voice name | Voice ID |
| --- | --- |
| Vibrant Youth | `vibrant-youth` |
| Lively Girl | `lively-girl` |
| Soft-spoken Gentleman | `soft-spoken-gentleman` |
| Magnetic-voiced Male | `magnetic-voiced-male` |
| Confident Male | `zixinnansheng` |
| Elegant Gentle | `elegantgentle-female` |
| Lively Breezy | `livelybreezy-female` |

All seven are `stepaudio-2.5-tts` voices (audiobook, dubbing, customer service,
companionship, education, marketing scenarios).

## Pricing — by channel

| Model | Step Plan | Standard | Notes |
|---|---|---|---|
| `stepaudio-2.5-tts` | Credits | $0.85 / 10,000 chars | |
| Voice cloning | Credits | $1.50 / voice | permanent voice |
| `stepaudio-2.5-asr` | Credits | $0.022 / hour | one-shot SSE |
| `stepaudio-2.5-asr-stream` | ❌ not on Step Plan | $0.18 / hour | streaming WS; model unverified on both channels |

## NOT callable on this account (reference-only in the docs)

`stepaudio-2.5-chat` (audio-in → text-out, understands tone) ·
`stepaudio-2.5-realtime` and `stepaudio-3-realtime-preview` (full-duplex
speech-to-speech) · `stepaudio-2.5-asr-stream` (streaming ASR WebSocket — Step
Plan: ❌ confirmed 2026-10-13; Standard: unverified) · `stepaudio-3-tts` ·
`stepaudio-3-asr-max` · the rest of the StepAudio 3 family (unified audio
generation, music). The realtime WebSocket endpoints
(`wss://api.stepfun.ai/v1/realtime/asr/stream`, `wss://api.stepfun.ai/v1/realtime`)
are documented against those models and are not usable with this key.
Availability authority: [models.md](../always-load/models.md); buildable
architecture: [voice-pipeline.md](voice-pipeline.md).
