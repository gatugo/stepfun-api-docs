> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Stream responses for a smoother experience

Long generations can take time—for example, a 1,000-word article may take 10 seconds or more. Without feedback, users may think the app is broken and leave.

Use UX cues to show progress and keep users engaged until the result is ready.

Traditional APIs return only once, so developers rely on loading states or skeleton screens to communicate that work is in progress.

<img src="https://mintcdn.com/stepfun2/LB7Z4XEbvwu-9ERC/images/loading.gif?s=1e035da64686806b8b02ac182b2f088f" alt="" width="466" height="302" data-path="images/loading.gif" />

Stepfun’s [chat completion API](/docs/en/api-reference/chat/chat-completion-create) supports streaming, so you can render the text as it is produced (like a typewriter effect) and let users read along while the model generates.

<img src="https://mintcdn.com/stepfun2/LB7Z4XEbvwu-9ERC/images/typing_stepfun_short.gif?s=b591b1f40f7fa762b45af9e9a4704ff3" alt="" width="900" height="140" data-path="images/typing_stepfun_short.gif" />

## How to enable streaming

Pass `stream=True` to the Chat Completion API to enable streaming. The API returns SSE data; parse it and render the chunks to your UI.

### Code example

```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
from openai import OpenAI

# Initialize Stepfun client
STEPFUN_KEY = "YOUR_STEP_API_KEY"

client = OpenAI(base_url="https://api.stepfun.ai/v1", api_key=STEPFUN_KEY)

# Call the completion API with streaming
stream = client.chat.completions.create(
    model="step-5-preview",
    messages=[{"role": "user", "content": "How is the All Seasons hotel?"}],
    stream=True,
)

# Print/render streamed chunks
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

## Notes

* Even with streaming, there is still some latency. Use a loading indicator alongside streamed output so users receive immediate feedback.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.