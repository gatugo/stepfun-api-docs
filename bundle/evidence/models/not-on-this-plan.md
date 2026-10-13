---
card: not-on-this-plan
tier: evidence
status: verified
verified_on: 2026-10-13
source: _account/live-calls/2026-10-13-models.md, _account/live-calls/2026-10-13-image-api-retired.md, _account/step-plan-access-info.md, corpus/guides/models/overview.md
---

# Not on this plan — channel-specific allowlists

> **This card tracks which models are absent from each channel.** A model absent
> from Step Plan may be callable on Standard, and vice-versa. The two allowlists
> are defined in [`../../always-load/models.md`](../../always-load/models.md).

## On this account — by channel

| Model | Step Plan | Standard |
|---|---|---|
| `step-5-preview` | ✅ | ✅ |
| `step-3.7-flash` | ✅ | ✅ |
| `step-3.5-flash` | ✅ | ✅ |
| `step-3.5-flash-2603` | ✅ | ✅ |
| `stepaudio-2.5-tts` | ✅ | ✅ |
| `stepaudio-2.5-asr` | ✅ | ✅ |
| `step-image-edit-2` | ❌ | ❌ — **retired 2026-10-10**; endpoints return HTTP 400 |
| `stepaudio-2.5-chat` | ❌ | ✅ |
| `stepaudio-2.5-realtime` | ❌ | ✅ |
| `stepaudio-2.5-asr-stream` | ❌ | ✅ |
| `stepaudio-3-asr-max` | ❌ | ✅ |
| `stepaudio-3-chat-preview` | ❌ | ✅ |
| `stepaudio-3-gen-preview` | ❌ | ✅ |
| `stepaudio-3-music-preview` | ❌ | ✅ |
| `stepaudio-3-realtime-preview` | ❌ | ✅ |
| `stepaudio-3-tts` | ❌ | ✅ |
| `step-router-v1` | ❌ | ❌ |
| `step-2x-large` | ❌ | ❌ — retired 2026-10-10 |
| `step-1x-edit` | ❌ | ❌ — retired |
| `deepseek-v4-pro` | ❌ | ❌ |

> ✅ = confirmed callable by live model-list call 2026-10-13
> ❌ = not present in the live model-list response for that channel

**Not on any channel** (absent from both model-list responses):
`step-router-v1` · `step-2x-large` · `step-1x-edit` · `deepseek-v4-pro`

**Step Plan only (absent from Standard)** — none; every Step Plan model appears
on Standard.

**Standard only (absent from Step Plan):** `stepaudio-2.5-chat` ·
`stepaudio-2.5-realtime` · `stepaudio-2.5-asr-stream` · `stepaudio-3-asr-max` ·
`stepaudio-3-chat-preview` · `stepaudio-3-gen-preview` · `stepaudio-3-music-preview` ·
`stepaudio-3-realtime-preview` · `stepaudio-3-tts`

These 9 models are callable on Standard but absent from the 6-model Step Plan
allowlist. They are **not violations** — they are the documented Standard-only
set. Reference them freely in Standard-channel context.
