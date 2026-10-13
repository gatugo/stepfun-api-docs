---
card: openai-migration
tier: by-task
status: draft
verified_on: 2026-10-08 (Step Plan verified; Standard column unverified)
source: corpus/guides/developer/openai.md
---

# Migrating from OpenAI to StepFun

**Change three things: the base URL, the API key, and the model name.** StepFun is compatible with the OpenAI API spec, so the OpenAI SDKs work unchanged once those three are swapped.

| Change | From | To (Step Plan channel) | To (standard channel — pay-as-you-go) |
| --- | --- | --- | --- |
| Base URL | `https://api.openai.com/v1` | `https://api.stepfun.ai/step_plan/v1` | `https://api.stepfun.ai/v1` |
| API key | OpenAI key | StepFun API key (`STEP_API_KEY`) | StepFun API key |
| Model | OpenAI model name | a StepFun model ID | a StepFun model ID |

## Model name mapping

| OpenAI model | StepFun counterpart |
| --- | --- |
| `gpt-4o` | `step-3.7-flash` or `step-5-preview` |
| `gpt-4o-mini` | `step-3.5-flash-2603` |

| StepFun model | Notes |
| --- | --- |
| `step-5-preview` | flagship for agentic work; text, image, and video input; 1M-token context |
| `step-3.7-flash` | high-speed multimodal reasoning; native image and video understanding; three reasoning effort levels (low/medium/high) |
| `step-3.5-flash` | high-speed language reasoning; logical reasoning, math, software engineering, deep research |
| `step-image-edit-2` | **RETIRED 2026-10-10** — was unified text-to-image and image-editing; a single edit completed in 1–2 seconds |

> The image generation and image editing models (including `step-image-edit-2`) **retired on October 10, 2026**, and their APIs **have stopped** serving requests — live-verified 2026-10-13, HTTP 400 `model step-image-edit-2 not supported` on both channels.

## reasoning_effort by model

| Model | Accepted levels |
| --- | --- |
| `step-3.5-flash-2603` | `low` / `medium` / `high` — verified by live call 2026-10-08 |
| `step-5-preview` | `low` / `medium` / `high` |
| `step-3.7-flash` | `low` / `medium` / `high` |

## SDK changes

| SDK | What to change |
| --- | --- |
| OpenAI Python | `api_key` → StepFun key; add `base_url="https://api.stepfun.ai/v1"` (standard channel — pay-as-you-go) |
| OpenAI TypeScript | `apiKey` → StepFun key; add `baseURL: "https://api.stepfun.ai/v1"` (standard channel — pay-as-you-go) |
| LangChain | `ChatOpenAI`: update `openai_api_key`, `openai_api_base`, and `model_name` |
| LangChain.js | `ChatOpenAI`: update `modelName` and `openAIApiKey`, and pass `basePath` in the second argument |

The Step Plan base URL (`https://api.stepfun.ai/step_plan/v1`) replaces the standard one in all of the above for pipeline work.

## OpenAI-compatible API surface

Supported: Chat Completion · Upload file · List files · Retrieve file info · Retrieve file content · Delete file · List models · Retrieve a model · Generate images.

See [chat-apis.md](chat-apis.md) for the Chat Completions parameters, [files.md](files.md) for the Files endpoints, and [client-setup.md](client-setup.md) for editor/agent clients.

## Negatives

- The sources document migration **only** for these SDKs and these endpoints. Responses API, Embeddings, Moderations, Audio, and Fine-tuning migration are **not documented** here.
- **No image model is callable** on this account. `step-image-edit-2` was the only one and it retired 2026-10-10 — live-verified dead (HTTP 400 on both channels, 2026-10-13). No successor is named.
- All four reasoning models accept `low`/`medium`/`high` effort (verified by live calls 2026-10-08).
- The examples in the docs use the standard channel (`https://api.stepfun.ai/v1`); pipeline code should use `https://api.stepfun.ai/step_plan/v1`.
- No pricing, rate-limit, or token-limit comparison against OpenAI models is documented in these sources.

## Related cards

[chat-apis.md](chat-apis.md) · [client-setup.md](client-setup.md) · [files.md](files.md) · [errors-and-debugging.md](errors-and-debugging.md)
