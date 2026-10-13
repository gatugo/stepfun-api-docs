> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Pricing Overview

## Billing concepts

### Billing unit

Token: A token represents a common character sequence and is the basic unit models use to represent natural language. A single token can be a Chinese word, a Chinese phrase, or an English word.
For typical Chinese text, the ratio of tokens to characters is roughly 1:1.6. Use the model response to get exact counts from `usage.prompt_tokens`, `usage.completion_tokens`, and `usage.total_tokens`.

## Billing policy

### Billing logic

We charge by total tokens in the input and output. For multimodal models, images are billed at 400 tokens per image. Final cost is based on total tokens consumed.
Fees are deducted as `tokens used × model unit price`, drawing from free credit first, then paid balance. Free credit can expire, so please use it promptly.

### Rate limiting

Rate limits are common for APIs, with several purposes:

* Prevent abuse or misuse—for example, malicious floods that overload the service.
* Ensure fair access—one user’s excessive requests should not slow others.
* Protect infrastructure—limits help keep performance stable during traffic spikes.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.