> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Handle exceptions to make your app more robust

Large models introduce some randomness, which can surface as errors. High request rates can also trigger platform limits. Build error handling into your app so it stays reliable.

Stepfun API exposes two kinds of errors:

1. HTTP-level errors
2. Model-level errors

## HTTP-level errors

Stepfun may return the following HTTP status codes. Add targeted handling in your app to improve resilience.

### 400

The request exceeded parameter constraints. Revisit the API docs and validate the request. If you accept UGC input, validate user input against Stepfun’s limits before sending it.

### 401

Authentication failed, often due to an incorrect API key. Double-check the key. If the issue persists, contact support for help.

### 402

Your balance is insufficient for this call. Recharge on the Stepfun console to resume requests.

### 404

The request path is incorrect and the resource cannot be found. Verify the path against the docs (including casing and special characters). If it still fails, review the documented resource structure. Contact support if you need further help.

### 429

You exceeded the allowed request rate. Retry after a delay. If that is not enough, recharge to raise your rate limit. For higher limits beyond recharge, contact us.

### 451

The request or model response failed a safety check. Add safety review upstream so users get early feedback about problematic content.

### 500 / 503 / 504

A server-side issue occurred. Wait briefly and retry. If repeated retries fail, contact us to investigate.

## Model-level errors

Generation may stop for several reasons. Handle the returned `finish_reason` accordingly:

* `stop`: normal completion. Process the message as-is.
* `length`: output was cut off by `max_tokens`.
* `content_filter`: the response failed a safety check. Add a safety layer earlier so users see the issue sooner.
* `tool_calls`: the model wants to call a function. Execute it and pass the result into the next request.

### Handling streaming responses

For streaming requests, generation can end mid-stream. Inspect the `finish_reason` on each chunk and react accordingly.

```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
completion = client.chat.completions.create()
for c in completion:
    for choice in c.choices:
        if choice.finish_reason == "stop":
            # Normal end; output directly
            print(c.to_dict())
        if choice.finish_reason == "content_filter":
            # Blocked by safety filter
            print(c.to_dict())
        ### .... more handling
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.