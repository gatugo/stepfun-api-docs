---
card: endpoints
tier: always-load
status: verified
verified_on: 2026-10-13 (both channels live-verified)
source: corpus/step-plan/overview.md, corpus/api-reference/chat/chat-completion-create.md
---

# Base URLs and endpoints

## Base URLs (overseas)

| Channel | Base URL | Notes |
|---|---|---|
| **Step Plan** | `https://api.stepfun.ai/step_plan/v1` | Credits; OpenAI SDK |
| **Step Plan** (Anthropic) | `https://api.stepfun.ai/step_plan` | Claude Code / Anthropic SDK; client appends `/v1/messages` |
| **Standard** | `https://api.stepfun.ai/v1` | Pay-as-you-go USD |

> **The same key works on both channels** — the base URL decides which quota is
> drawn. Standard-address requests do **not** consume Step Plan Credits (Rule 6).

> ✅ **Endpoint parity live-verified 2026-10-13** — chat completions, messages,
> responses, ASR one-shot SSE, and TTS one-shot all return HTTP 200 on **both**
> base URLs. **Files is the one exception: Standard only** (Step Plan files
> returns 404). Evidence: `_account/live-calls/2026-10-13-endpoints.md`. Only the
> streaming WebSocket endpoints remain untested by live call.
>
> ⚠️ The sources call the Responses API Standard-only, but
> `POST …/step_plan/v1/responses` also returns 200 — see
> [chat-apis.md](../by-task/chat-apis.md).

## Endpoint table

| Capability | Step Plan URL | Standard URL | Notes |
|---|---|---|---|
| Chat Completions | `POST …/step_plan/v1/chat/completions` | `POST …/v1/chat/completions` | |
| Messages (Anthropic) | `POST …/step_plan/v1/messages` | `POST …/v1/messages` | |
| Responses | `POST …/step_plan/v1/responses` — live-verified 200, docs omit it | `POST …/v1/responses` | docs say Standard-only; wrong |
| TTS (one-shot) | `POST …/step_plan/v1/audio/speech` | `POST …/v1/audio/speech` | same path, different billing |
| TTS (streaming WS) | `wss://…/step_plan/v1/realtime/audio` | `wss://…/v1/realtime/audio?model=stepaudio-2.5-tts` | |
| Voice clone preview | `POST …/step_plan/v1/audio/voices/preview` | `POST …/v1/audio/voices/preview` | |
| ASR (one-shot SSE) | `POST …/step_plan/v1/audio/asr/sse` | `POST …/v1/audio/asr/sse` | same path, different billing |
| ASR streaming (WS) | ❌ not on Step Plan | `wss://…/v1/realtime/asr/stream` | standard-only; model must be callable |
| Realtime speech-to-speech | ❌ not on Step Plan | `wss://…/v1/realtime` | standard-only |
| File upload | ❌ 404 — verified absent 2026-10-13 | `POST …/v1/files` | Standard-only |
| Token count | `POST …/step_plan/v1/token/count` | `POST …/v1/token/count` | note: standard-channel doc may say standard-only |

> ❌ = endpoint not available on this channel for this account. Per-endpoint
> parameters: [`../by-task/chat-apis.md`](../by-task/chat-apis.md),
> [`../by-task/audio.md`](../by-task/audio.md),
> [`../by-task/files.md`](../by-task/files.md).
