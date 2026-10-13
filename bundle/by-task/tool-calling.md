---
card: tool-calling
tier: by-task
status: verified
verified_on: 2026-10-08
source: corpus/guides/developer/tool-call.md, corpus/api-reference/tool-call.md
---

# Tool Calling (Function Calling)

Tool calls let the model invoke your functions instead of inventing plausible-but-wrong answers — either to **fetch information** it was not trained on (news, weather, calculations, database lookups) or to **perform actions** through your local application logic (e.g. send an email).

## Flow (Chat Completions)

1. Implement the function locally (e.g. `get_weather(city)`).
2. Define the tool: `{"type": "function", "function": {"name", "description", "parameters": <JSON Schema>}}`.
3. Call Chat Completions with `tools=[...]` and `tool_choice="auto"`.
4. If the model triggers the tool, `message.content` is empty and `message.tool_calls[0].function` holds the `name` and JSON-string `arguments` — execute the function with those arguments.
5. Append the API result to `messages` and continue generation.

Request/response shapes for the Messages and Responses APIs live in [chat-apis.md](chat-apis.md).

## Tool definition rules

| Rule | Value |
| --- | --- |
| Max tools per request | 128 |
| `function.name` | letters, numbers, `-`, `_`; ideally under 64 characters (documented regex guideline: `^[a-zA-Z*][a-zA-Z0-9-_]63$`) |
| `function.parameters` | root `type` must be `object`; content follows a subset of JSON Schema; keys follow the same naming rule |
| `function.description` | what the function does so the model can choose it; English or Chinese |

## Model support

Tool calling is supported on `step-5-preview`, `step-3.7-flash`, `step-3.5-flash`, and `step-3.5-flash-2603` (per-model details: `specs/models/`).

## Built-in (official) tools

| Tool | Status |
| --- | --- |
| `web_search` (built-in Chat Completions tool) | NOT available on `step-5-preview` — integrate an external search service through a function tool and return its results to the model |
| Knowledge base search | Upload text to a knowledge base and search it to reduce hallucinations |

Support for function calling does not imply support for every built-in tool — availability depends on the selected model.

## Best practices

- Write clear function descriptions — the model decides when to call from them; clarity improves hit rate.
- Describe parameter fields clearly, including the expected language, so arguments come back valid.
- Keep `tool_choice="auto"` unless you need to force a specific call.

## Channel

Pipeline/integration code uses the Step Plan channel:

```python
from openai import OpenAI
client = OpenAI(base_url="https://api.stepfun.ai/step_plan/v1", api_key=STEP_API_KEY)
```

The public docs' examples use `https://api.stepfun.ai/v1` (standard channel — pay-as-you-go); do not use that base URL or its key for pipeline code.

## Negatives / gotchas

- A triggered tool call returns empty `content` — do not treat that as a failed generation.
- Built-in `web_search` is unavailable on `step-5-preview` even though the model supports function calling.
- Roo Code 3.54.0+ requires OpenAI-native tool calling with no XML fallback — choose a function-calling model.

## Related cards

[chat-apis.md](chat-apis.md) · [reasoning.md](reasoning.md) · [streaming.md](streaming.md)
