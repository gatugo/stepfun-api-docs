---
card: reasoning
tier: by-task
status: verified
verified_on: 2026-10-08
source: corpus/guides/developer/reasoning.md, corpus/api-reference/chat/chat-completion-create.md
---

# Reasoning Models & Effort Control

Reasoning models expose their thinking process in a `reasoning` field and let you tune thinking depth with an effort parameter: **`reasoning_effort`** on the Chat Completions API, **`output_config.effort`** on the Messages API (request shapes: [chat-apis.md](chat-apis.md)).

## Reasoning model lineup

| Model | Profile | Context window (per these sources) |
| --- | --- | --- |
| `step-5-preview` | Recommended for software engineering, professional knowledge work, and multi-step agent tasks; text + image + video input | 1M tokens |
| `step-3.7-flash` | High-speed multimodal reasoning; native image and video understanding; supports three effort levels | not documented here — see [context-and-cache.md](context-and-cache.md) |
| `step-3.5-flash` | High-speed text reasoning built for extreme efficiency: sparse MoE, 196B params / ~11B activated per token; solid tool calling and multi-step agent capability | 256K tokens |
| `step-3.5-flash-2603` | Agent-optimized variant of `step-3.5-flash` | not documented here — see [context-and-cache.md](context-and-cache.md) |

## Effort levels

| Effort | Use cases |
| --- | --- |
| `low` | Simple Q&A, summarization, rewriting, information extraction |
| `medium` | Default recommendation — general reasoning and multi-step tasks |
| `high` | Complex reasoning, math, planning, code analysis |

Higher effort produces deeper reasoning but may take longer to respond.

**Which levels each model accepts differs — always check `specs/models/<model>.md` before setting a level.**

> ✅ **Verified by live calls 2026-10-08 (was open question Q01):** all four reasoning models — `step-5-preview`, `step-3.7-flash`, `step-3.5-flash`, `step-3.5-flash-2603` — accept `low`/`medium`/`high`. Live calls with `"reasoning_effort": "medium"` returned HTTP 200 on both 3.5 variants. The API reference's "2603 accepts low and high only" claim is wrong, and so was the earlier owner ruling that put base `step-3.5-flash` at `low`/`high`.

## Reading the reasoning content

| Scenario | Where the thinking text appears |
| --- | --- |
| Streaming | `chunk.choices[0].delta.reasoning` |
| Non-streaming | `completion.choices[0].message.reasoning` |

`reasoning_format` selects the field: `general` (default) returns a `reasoning` field; `deepseek-style` returns the DeepSeek-compatible `reasoning_content` field.

## Choosing a model

| Need | Model |
| --- | --- |
| Deep logic, long documents, agentic work | `step-5-preview` |
| Fast multimodal (image/video) reasoning | `step-3.7-flash` |
| High-frequency agent loops | `step-3.5-flash-2603` (token-efficient, low-reasoning mode) |
| Pure-text general reasoning | `step-3.5-flash` |

## Negatives / gotchas

- The `reasoning` field appears only for step reasoning models — check for its existence instead of assuming it.
- All four reasoning models accept every effort level (verified by live calls 2026-10-08); the effort table above is the whole matrix.
- Higher effort is not free — deeper reasoning can mean longer response times.

## Notes

- A Trace ID is added to model outputs — include it when reporting issues with reasoning behavior.

## Related cards

[chat-apis.md](chat-apis.md) · [tool-calling.md](tool-calling.md) · [context-and-cache.md](context-and-cache.md)
