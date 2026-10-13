---
card: structured-output
tier: by-task
status: verified
verified_on: 2026-10-08
source: corpus/guides/developer/json-mode.md
---

# Structured Output: JSON Mode & JSON Schema

Two ways to get parseable JSON from StepFun models — pick by whether you need API-level schema enforcement.

| Mode | Request parameters | When to use it |
| --- | --- | --- |
| JSON Mode | `response_format: {"type": "json_object"}` | You need parseable JSON without API-level constraints on specific fields or types |
| JSON Schema | `response_format.type: "json_schema"` with `json_schema.strict: true` | You need schema constraints on fields, types, and required properties |

## JSON Schema: constrain structure through the API

Applies to `step-5-preview`, `step-3.7-flash`, `step-3.5-flash`, and `step-3.5-flash-2603`.

Set `response_format.type` to `json_schema` and provide these fields in `response_format.json_schema`:

| Field | Notes |
| --- | --- |
| `name` | the schema's name |
| `strict` | set to `true` to enable strict mode |
| `schema` | the expected JSON structure, including properties, types, and required fields |

```bash
export STEP_API_KEY="YOUR_STEP_API_KEY"

# Step Plan channel — pipeline URL
curl --silent --show-error --fail-with-body \
  https://api.stepfun.ai/step_plan/v1/chat/completions \
  -H "Authorization: Bearer $STEP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "step-5-preview",
    "messages": [{"role": "user", "content": "Extract the person: Wang Ming, age 28."}],
    "stream": false,
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "person",
        "strict": true,
        "schema": {
          "type": "object",
          "additionalProperties": false,
          "required": ["name", "age"],
          "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
          }
        }
      }
    },
    "max_tokens": 1024
  }'
```

(The public docs' example uses `https://api.stepfun.ai/v1/chat/completions` — standard channel, pay-as-you-go.)

`choices[0].message.content` is a string containing JSON, e.g. `{"name": "Wang Ming", "age": 28}`. `required` makes both fields mandatory; `additionalProperties: false` disallows extra fields.

## JSON Mode: return parseable JSON

Three things:

1. Explicitly request JSON in the system prompt and describe the expected structure. You can include a JSON Schema as prompt guidance, but this does not provide strict schema constraints.
2. Set `response_format` to `{ "type": "json_object" }` so the model returns parsable JSON.
3. Parse the result and validate it. Once it matches expectations, pass it into your business logic.

## Negatives / gotchas

- A schema (or structure description) in the prompt does NOT provide API-level enforcement — use the `json_schema` parameter for strict constraints.
- With JSON Mode you must validate fields, types, and required properties yourself.
- For both modes, check the request succeeded and `finish_reason` is `stop`. If it is `length`, the output may have been truncated by `max_tokens` and must not be treated as complete JSON — increase the output limit and retry.
- Handle request failures, refusals, and missing usable `content` separately rather than parsing them as business data.
- Schema constraints do not guarantee factual or business-level correctness — validate the extracted values in your application.
- When using a proxy or gateway, ensure `response_format` and its nested fields reach the API server intact.

## Related cards

[chat-apis.md](chat-apis.md) (Responses API `text.format` json_schema variant) · [streaming.md](streaming.md) (streaming works with `json_object` too)
