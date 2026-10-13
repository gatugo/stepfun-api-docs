---
card: context-and-cache
tier: by-task
status: verified
verified_on: 2026-10-08
source: corpus/guides/developer/prompt-cache.md, corpus/guides/developer/multiple-round.md
---

# Multi-Turn Context & Prompt Cache

Two mechanisms for conversation-heavy apps: **multi-turn context** — send ordered history back to the model each turn; **prompt cache** — the platform automatically caches repeated prompt prefixes.

## Multi-turn conversations

The Chat Completions API accepts an array as the message list. Store user and assistant messages in order and send them back to the model to enable multi-turn dialogs: persist a Chat + Messages in your system, fetch messages in chronological order (store timestamps), and append the model's reply as another Message.

| Model | Context window |
| --- | --- |
| `step-5-preview` | 1M tokens |
| `step-3.7-flash`, Step 3.5 Flash series | 256K |

Manage history according to the selected model's window and reserve space for output. Conversation history counts toward input tokens and cost, so choose an appropriate history length rather than always sending the full conversation:

- Casual chat: keep roughly 10 turns.
- Deep, high-context scenarios: pass the full conversation to the model.

## Prompt cache

Automatic — nothing to enable. Caching activates when a request exceeds 256 tokens:

1. **Cache lookup** — the system checks for a cached prefix of your prompt.
2. **Cache hit** — if found, the cache is reused and only the uncached portion is processed.
3. **Cache miss** — if not found, the request is processed normally and the prompt prefix is cached for future use.

Supported models: `step-5-preview`, `step-3.7-flash`, `step-3.5-flash`, and `step-3.5-flash-2603`. For other models, check the corresponding model documentation and pricing table.

### What is cached

| Content | Condition |
| --- | --- |
| Conversation messages — the full array, including system prompt, user messages, and assistant messages | — |
| Images within user messages | same images reused |
| Video within user messages | same constraint |
| Tool calls and results — calls inside the conversation and their outputs | — |

Minimum cache unit: 256 tokens — prompts shorter than 256 tokens will not hit the cache.

### Detecting cache hits

A positive `response.usage.cached_tokens` indicates a cache hit and reports the number of cached input tokens; 0 means no input tokens were served from cache. Example: `prompt_tokens` 591 with `cached_tokens` 512 → 512 billed at the cache-hit input rate and 591 − 512 = 79 at the cache-miss rate. Caching does not reduce the actual input token count or make cached tokens free: input cost = `(79 × cache-miss input rate + 512 × cache-hit input rate) / 1,000,000`, with rates in USD per 1M tokens. Output tokens are billed separately.

### Billing

Cached input tokens are billed at the model's cache-hit input rate; discounts vary by model. Example from the docs: `step-5-preview` costs $0.05 / 1M cached input tokens — 5% of its cache-miss input rate ($1.00 / 1M tokens). There is no separate paid cache feature: uncached input tokens, including the first write to the cache, use the cache-miss input rate. Current prices: the platform pricing page.

### Tips

- Put static or repeated content at the beginning of the prompt, and dynamic parts at the end.
- Monitor ratios of `cached_tokens` vs `prompt_tokens`, latency, and hit rate to optimize prompt structure.
- Keep the prompt prefix stable — cache entries unused recently may be evicted (LRU; eviction is more aggressive during peak traffic, longer-lived off-peak).
- For long prompts, send them during off-peak hours to reduce evictions and improve hit rate.

### Troubleshooting cache misses

1. Ensure the cached portion stays identical across calls.
2. Verify calls are not spaced so far apart that the cache expires.
3. Provide at least 256 tokens of input.

### Negatives

- Manual cache clearing is not supported — modify the prompt if you need to avoid cache hits.
- Guaranteed cache hits are not supported.
- Caching does not affect model quality — each generation still uses the full prompt.

## Related cards

[chat-apis.md](chat-apis.md) · [streaming.md](streaming.md)
