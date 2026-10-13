---
card: streaming
tier: by-task
status: verified
verified_on: 2026-10-08
source: corpus/guides/developer/stream.md
---

# Streaming (SSE)

Pass `stream=True` to the Chat Completions API and the API returns SSE data; parse it and render chunks to your UI as they arrive (typewriter effect). Long generations can take 10+ seconds (e.g. a 1,000-word article) — without feedback users may think the app is broken and leave.

## Enable

```python
from openai import OpenAI

# Step Plan channel — use this base URL for pipeline code
client = OpenAI(base_url="https://api.stepfun.ai/step_plan/v1", api_key=STEP_API_KEY)

stream = client.chat.completions.create(
    model="step-5-preview",
    messages=[{"role": "user", "content": "How is the All Seasons hotel?"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

The public docs' example uses `https://api.stepfun.ai/v1` (standard channel — pay-as-you-go); for pipeline/integration code swap the base URL to `https://api.stepfun.ai/step_plan/v1` with the Step Plan API key.

## Chunk shape

Each chunk is a delta of the assistant message, not a full response:

| Field | Notes |
| --- | --- |
| `chunk.choices[0].delta.content` | incremental text fragment; can be `None` on the first/last chunks — always guard against it |
| `chunk.choices[0].delta.role` | present on the opening chunk |

Concatenate `delta.content` across chunks to build the full answer.

## Negatives / gotchas

- Streaming still has latency — first-token delay remains, so pair streamed output with a loading indicator for immediate feedback.
- `delta.content` may be `None` on the first/last chunks — unguarded access crashes.
- Video inputs add download and safety-check time before generation starts — see [vision-and-video.md](vision-and-video.md).

## Related cards

[chat-apis.md](chat-apis.md) (Messages / Responses streaming event shapes) · [context-and-cache.md](context-and-cache.md) (multi-turn history)
