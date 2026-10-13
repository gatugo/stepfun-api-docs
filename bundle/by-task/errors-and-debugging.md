---
card: errors-and-debugging
tier: by-task
status: verified
verified_on: 2026-10-08
source: corpus/api-reference/error-codes.md, corpus/guides/developer/exception.md, corpus/guides/developer/troubleshooting.md
---

# Errors and Debugging

**Two error classes: HTTP status codes and `finish_reason`.** Handle both — HTTP errors mean the request failed, `finish_reason` means generation stopped early even on a 200 response.

## HTTP-level errors

| Status | Meaning | Recommended action |
| :- | :- | :- |
| 400 | Request exceeded parameter constraints / parameters invalid | Revisit the API docs and validate the request. If you accept UGC input, validate user input against StepFun's limits before sending it |
| 401 | Authentication failed, often an incorrect API key | Double-check the key; contact support if it persists |
| 402 | Insufficient balance for this call | Recharge on the StepFun console to resume requests |
| 404 | Request path incorrect, resource not found | Verify the path against the docs, including casing and special characters |
| 429 | Exceeded the allowed request rate | Retry after a delay; if that is not enough, recharge to raise your rate limit. For higher limits beyond recharge, contact StepFun |
| 451 | Request or model response failed a safety check | Add safety review upstream so users get early feedback about problematic content |
| 500 | Server-side issue | Wait briefly and retry; contact support if repeated retries fail |
| 503 | Server currently overloaded | Retry after a short delay |

**Common causes of 400:** (1) image cannot be downloaded, (2) image count exceeds the limit, (3) the model does not support video input, (4) model does not exist or you lack permission, (5) parameter value is invalid.

`500`, `503`, and `504` are all server-side issues: wait briefly and retry, and contact support if repeated retries keep failing.

## Model-level errors (`finish_reason`)

| `finish_reason` | Meaning | Handling |
| :- | :- | :- |
| `stop` | Normal completion | Process the message as-is |
| `length` | Output cut off by `max_tokens` | Treat the message as incomplete; raise the output limit and retry |
| `content_filter` | Response failed a safety check | Add a safety layer earlier so users see the issue sooner |
| `tool_calls` | The model wants to call a function | Execute it and pass the result into the next request |

For **streaming** requests, generation can end mid-stream — inspect the `finish_reason` on **each chunk** and react accordingly:

```python
completion = client.chat.completions.create()
for c in completion:
    for choice in c.choices:
        if choice.finish_reason == "stop":
            # Normal end; output directly
            print(c.to_dict())
        if choice.finish_reason == "content_filter":
            # Blocked by safety filter
            print(c.to_dict())
```

## What to send support

| API | Identifiers to share |
| - | - |
| Chat API / text-to-image / image-to-image / image edit / audio generation / voice cloning | `X-Trace-Id` from the response headers **and** the result ID — the `id` field of the completion (e.g. `b7b56af0-52a6-483f-a589-948182676a1b`) |
| Streaming audio API | The `session_id` from any event (e.g. `01956e7388477cfcbdc3aaabf364bc70`). Any event carries `session_id` inside `data`, so pull it from whichever event you captured |

The `id` field of a chat completion object is the result ID; `model`, `created`, `choices[].finish_reason`, and `usage` are also in the response body and useful when reporting.

## Retry policy

| Status | Retry? |
| --- | --- |
| 429, 500, 503 | Yes — retry after a short delay |
| 400, 401, 402, 404, 451 | No — fix the request, key, balance, path, or content first |
| `finish_reason: length` | Yes — with a higher output limit |

### 429 is a throttle, not an absence — the rule that matters most

**Only a 404 proves an endpoint or model is absent. A 429 proves nothing except
that you were rate-limited.** Live-verified 2026-10-13: `step-3.5-flash` on Step
Plan `/messages` returned 429 three times while every other call in the same
minute returned 200, then returned 200 on retry. Concluding "unavailable" from a
429 produces false negatives — see
[source-contradictions.md](../evidence/source-contradictions.md).

Note also that the image API answered **400, not 404**, when its model was
retired — so a 404-only absence check has a second failure mode. See
[images.md](images.md).

### What the sources do not document — and a safe default

The sources specify only "retry after a delay". They document **no** backoff
intervals, **no** jitter strategy, **no** maximum retry count, and **no**
`Retry-After`, rate-limit, or quota headers. You cannot read StepFun's intended
retry policy out of these docs.

**Bundle recommendation — not a vendor fact.** Until StepFun documents a policy,
use exponential backoff with jitter and a bounded attempt count:

| Parameter | Suggested value | Why |
| :- | :- | :- |
| Base delay | 1 second | long enough to clear a momentary burst |
| Backoff | ×2 per attempt | spreads retries without hammering |
| Jitter | ±50% of the computed delay | prevents synchronised retry storms |
| Max attempts | 5 | roughly 31 s of total waiting before you give up |
| On final failure | surface the error **with `X-Trace-Id`** | support can trace it — see below |

Do **not** treat these numbers as vendor limits or guarantees. They are a
defensive default chosen by this bundle because the sources are silent, and they
should be replaced by StepFun's documented policy if one ever appears (tracked
as **Q05** in [`../../open_questions.md`](../../open_questions.md)).

## Negatives

- The documented status-code list is **400, 401, 402, 404, 429, 451, 500, 503**. `504` is described as a server-side issue in the exception guide but has no row in the error-codes table.
- **Retry mechanics are undocumented** — no backoff, jitter, max attempts, or `Retry-After`/rate-limit/quota headers. See "What the sources do not document" above for the bundle's non-vendor default.
- No error-code strings beyond the HTTP status codes (no `request_params_invalid`-style codes) are documented in these sources.
- `finish_reason` values documented are only `stop`, `length`, `content_filter`, `tool_calls`.
- Client-specific errors (Claude Code, Cursor, Cline, steppage) are covered in [client-setup.md](client-setup.md) and [static-hosting.md](static-hosting.md).

## Related cards

[chat-apis.md](chat-apis.md) — response shapes and `usage` fields · [streaming.md](streaming.md) — chunk-level handling · [client-setup.md](client-setup.md) — client-specific errors · [static-hosting.md](static-hosting.md) — steppage troubleshooting
