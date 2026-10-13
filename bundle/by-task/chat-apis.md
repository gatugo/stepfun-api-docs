---
card: chat-apis
tier: by-task
status: draft
verified_on: 2026-10-13 (both channels live-verified)
source: corpus/api-reference/chat/chat-completion-create.md, corpus/api-reference/chat/messages-create.md, corpus/api-reference/responses/responses-create.md
---

# Chat APIs: Completions, Messages, Responses

Three chat endpoints. Pick by the client wire format you must support: **Chat Completions** (OpenAI), **Messages** (Anthropic), **Responses** (OpenAI Responses format).

| Endpoint | Wire format | Pipeline URL (Step Plan channel) | Standard URL (standard channel — pay-as-you-go) |
| --- | --- | --- | --- |
| Chat Completions | OpenAI | `POST https://api.stepfun.ai/step_plan/v1/chat/completions` (Step Plan base URL `https://api.stepfun.ai/step_plan/v1`) | `POST https://api.stepfun.ai/v1/chat/completions` |
| Messages | Anthropic | `POST https://api.stepfun.ai/step_plan/v1/messages` | `POST https://api.stepfun.ai/v1/messages` |
| Responses | OpenAI Responses | `POST https://api.stepfun.ai/step_plan/v1/responses` — live-verified 200 (docs do not mention it) | `POST https://api.stepfun.ai/v1/responses` |

## Which models each endpoint takes

| Endpoint | Models | Channel |
| --- | --- | --- |
| Chat Completions (this account) | `step-5-preview`, `step-3.7-flash`, `step-3.5-flash`, `step-3.5-flash-2603` | both |
| Messages | `step-5-preview`, `step-3.7-flash`, `step-3.5-flash`; `step-router-v1` is Step Plan only, reference-only, and NOT on this account | both (except `step-router-v1`) |
| Responses | `step-5-preview` and `step-3.7-flash` only | both — Standard documented, Step Plan live-verified 2026-10-13 |

The public docs also show `stepaudio-2.5-chat` as an example model — it exists in the docs but is NOT on this account (reference-only).

## Chat Completions — request parameters

| Field | Type | Required | Default / range | Notes |
| --- | --- | --- | --- | --- |
| `model` | string | Yes | — | see model table above |
| `messages` | object array | Yes | — | roles `system` / `user` / `assistant` / `tool`; `user` content is a string or a multipart array |
| `tools` | object array | No | — | function calling — see [tool-calling.md](tool-calling.md) |
| `max_tokens` | int | No | `INF` — no limit applied; the model determines output length | input + output still bounded by the model's max context length |
| `temperature` | float | No | 0.0–2.0, default 0.5 | |
| `top_p` | float | No | default 0.9 | |
| `n` | int | No | default 1 | no hard max; suggested up to 5 |
| `stream` | bool | No | default false | see [streaming.md](streaming.md) |
| `stop` | string or string array | No | empty | stops on any listed content |
| `frequency_penalty` | float | No | 0.0–1.0, default 0 | |
| `response_format` | object | No | `{"type":"text"}` | `{"type":"json_object"}` enables JSON Mode — see [structured-output.md](structured-output.md) |
| `reasoning_format` | string | No | `general` | `general` → `reasoning` field; `deepseek-style` → `reasoning_content` — see [reasoning.md](reasoning.md) |
| `reasoning_effort` | string | No | — | see [reasoning.md](reasoning.md); the 3.5-variant level mapping was disputed (Q01) and is now resolved by live call |

### Minimal call — non-streaming

The default (`stream=false`) returns one complete `chat.completion` object.

```python
import os
from openai import OpenAI

# Step Plan channel — the base URL alone selects the billing channel.
# Same key, different base URL = a different channel (see ../always-load/auth.md).
client = OpenAI(
    base_url="https://api.stepfun.ai/step_plan/v1",
    api_key=os.environ["STEP_API_KEY"],
)

completion = client.chat.completions.create(
    model="step-5-preview",
    messages=[{"role": "user", "content": "How is the All Seasons hotel?"}],
)

print(completion.choices[0].message.content)
print(completion.choices[0].finish_reason)   # "stop" = normal end
print(completion.usage.total_tokens)
```

`max_tokens` defaults to `INF` — no per-model hard output cap. The real ceiling
is *input + output ≤ the model's context window*, so set `max_tokens` explicitly
when you need a bound. For the streaming variant see
[streaming.md](streaming.md).

### Multimodal content in `user` messages

| Part | `type` | Constraints |
| --- | --- | --- |
| Text | `text` | `text` string |
| Image | `image_url` | `url`: http/https only, or base64 data URL; formats jpg/jpeg, png, webp, static gif; `detail` `low` (default, ~400 tokens) or `high` (token count varies) |
| Video | `video_url` | **nested** `video_url` object: `{"type":"video_url","video_url":{"url":"…"}}` — http/https or `data:video/mp4;base64,…`; under 128 MB; duration recommended under 5 minutes. A flat `"url"` sibling is rejected (HTTP 400 `Unrecognized chat message`). |
| Audio | `input_audio` | `data`: base64-encoded; mp3 and wav only |

`tool` messages carry `content` (the function result) plus `tool_call_id` from the previous assistant turn.

### Chat Completions response

Non-streaming (`stream=false`, default): one `chat.completion` object — `id`, `object` (always `chat.completion`), `model`, `created` (unix seconds), `choices[]`, `usage`.

`choices[].message`:

| Field | Notes |
| --- | --- |
| `role` | always `assistant` |
| `content` | message text |
| `reasoning` | present only for step reasoning models |
| `tool_calls` | optional; `id`, `type` always `function`, `function.name`, `function.arguments` (JSON string) |

`choices[].finish_reason` states why generation stopped. `usage`: `prompt_tokens`, `cached_tokens` (optional), `completion_tokens`, `total_tokens`.

Streaming (`stream=true`): a series of `chat.completion.chunk` objects with `choices[].delta` instead of `message` — see [streaming.md](streaming.md).

## Messages API (Anthropic format)

Claude Code and the Anthropic SDK use the configuration Base URL and append `/v1/messages`; curl uses the full request URL.

| Field | Type | Required | Default / range | Notes |
| --- | --- | --- | --- | --- |
| `model` | string | Yes | — | `step-router-v1` is Step Plan only and NOT on this account |
| `messages` | object array | Yes | at least one | each has `role` (`user`/`assistant`) and `content` (string or content-block array) |
| `max_tokens` | int | Yes | must be > 0 | |
| `system` | string or array | No | — | system prompt |
| `tools` | object array | No | — | each entry: `name`, `description`, `input_schema` (JSON Schema) |
| `output_config` | object | No | — | `effort` controls reasoning depth — see [reasoning.md](reasoning.md) |
| `stream` | boolean | No | non-streaming | |
| `temperature` | float | No | 0 to 2 | |
| `top_p` | float | No | > 0, at most 1 | |
| `top_k` | int | No | 0 to 500 | |
| `stop_sequences` | string array | No | — | stops when any sequence appears |

Content blocks in `messages[].content`: `text` (`text`) · `image` (`source`: URL object or `{"type":"base64","media_type":"image/png","data":"..."}`) · `tool_use` (`id`, `name`, `input`) · `tool_result` (`tool_use_id`, `content`, `is_error`).

Response: `id`, `type` always `message`, `role` always `assistant`, `model`, `content` blocks (may include `text`, `thinking`, `tool_use`), `stop_reason` (`end_turn` / `tool_use` / `max_tokens`), `usage` with `input_tokens` / `output_tokens` (cache usage fields may also be present).

Streaming is standard SSE — `Content-Type: text/event-stream`; events `message_start`, `content_block_start`, `content_block_delta`, `content_block_stop`, `message_delta`, `message_stop`, `ping`. Tool-call arguments stream with `content_block_delta.delta.type = input_json_delta`.

### step-router-v1 restrictions (Step Plan only, reference-only — NOT on this account)

Routes between `deepseek-v4-pro` and `step-3.7-flash`. Restrictions apply only to this model:

| Field | Behavior |
| --- | --- |
| `max_tokens` | maximum 250K |
| image / document blocks in `messages.content` | not supported — returns `unsupported_content_type` |
| `web_search` in `tools` | not supported — returns `unsupported_content_type` |
| `output_config.effort` | ignored |
| invalid router model name | HTTP 400 `request_params_invalid` |

## Responses API (OpenAI Responses format)

Models: `step-5-preview` and `step-3.7-flash` only. Standard-channel URL only
(`POST https://api.stepfun.ai/v1/responses`); a Step Plan URL for this endpoint
is not documented in the sources.

> ⚠️ **Correction (live-verified 2026-10-13):** the sources say this endpoint is
> Standard-only, but `POST /step_plan/v1/responses` also returns **HTTP 200**
> (`step-5-preview`, `status=completed`). Treat Responses as available on **both
> channels**; the docs are simply incomplete on the Step Plan side.
>
> ✅ Also live-verified on Standard 2026-10-13 — `step-3.7-flash` with
> `max_output_tokens=64` came back `status="incomplete"` with an empty `output`
> array because reasoning ate the whole budget. Use ≥512 tokens to get a
> `status="completed"` message.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `model` | string | Yes | `step-5-preview` or `step-3.7-flash` |
| `input` | string or object array | Yes | plain text = single `role=user` message; or an ordered array of messages / events |
| `instructions` | string | No | top-level system instructions |
| `stream` | bool | No | default `false` |
| `temperature` | float | No | 0.0–2.0 |
| `top_p` | float | No | |
| `max_output_tokens` | int | No | limits reasoning AND final output; if insufficient, `status="incomplete"` and `output` may contain only a `reasoning` item |
| `reasoning` | object | No | `effort`: `low` / `medium` / `high` |
| `tools` | object array | No | `function`-type tools only; optional `strict` boolean makes output arguments strictly match the schema |
| `tool_choice` | string or object | No | only the string `"auto"` is supported |
| `text` | object | No | `format.type`: `text`, `json_object`, or `json_schema` (`name`, `strict`, `schema` for `json_schema`) — see [structured-output.md](structured-output.md) |

Multi-turn function calling: pass the model's `function_call` item back verbatim plus a `function_call_output` item (`call_id` + `output`).

Response: `id` (`resp_xxx`), `object` always `response`, `created_at` / `completed_at` (unix seconds), `status` (`completed` / `incomplete` / `failed`), `error` (non-null only when failed), `incomplete_details` (commonly `{ "reason": "max_output_tokens" }`), `model`, `output[]`, `usage`. Output items: `reasoning`, `message` (content blocks of type `output_text`), `function_call` (`call_id` pairs with the subsequent `function_call_output`). `usage`: `input_tokens` (+ `input_tokens_details.cached_tokens`), `output_tokens` (+ `output_tokens_details.reasoning_tokens`, `tool_output_tokens`), `total_tokens`. The response echoes `instructions`, `max_output_tokens`, `reasoning`, `temperature`, `top_p`, `text`, `tool_choice`, `tools`.

Streaming events (`stream=true`): `response.created`, `response.in_progress`, `response.output_item.added`, `response.reasoning_part.added`, `response.reasoning_text.delta`, `response.reasoning_text.done`, `response.reasoning_part.done`, `response.content_part.added`, `response.output_text.delta`, `response.output_text.done`, `response.content_part.done`, `response.function_call_arguments.delta`, `response.function_call_arguments.done`, `response.output_item.done`, `response.completed`, `response.incomplete`, `response.failed`, `error`. Each event's `data` payload carries `type` and a `sequence_number` starting at 0.

## Negatives / gotchas

- Messages **requires** `max_tokens` (> 0); Chat Completions `max_tokens` defaults to `INF` (no limit).
- Responses supports only `step-5-preview` and `step-3.7-flash`, and `tool_choice` only as the string `"auto"`. Standard documented; **Step Plan URL also works** (live-verified 200) despite the sources omitting it.
- `step-router-v1` is Step Plan only and not on this account; its `output_config.effort` is ignored.
- `reasoning_effort` levels were disputed across models (Q01); live calls on 2026-10-08 settled it — all four reasoning models accept `low`/`medium`/`high`; see [reasoning.md](reasoning.md).
- The Responses endpoint is documented as **Standard-only**, but a Step Plan URL also returns 200 (live-verified 2026-10-13).

## Related cards

[reasoning.md](reasoning.md) · [tool-calling.md](tool-calling.md) · [streaming.md](streaming.md) · [structured-output.md](structured-output.md) · [context-and-cache.md](context-and-cache.md)
