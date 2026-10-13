---
layer: 0
role: routing-map
lines_budget: 60
---

# StepFun API — Agent Map

Local working bundle for the **StepFun Step Plan Oversea** subscription
(`platform.stepfun.ai`), default model `step-5-preview`. Two channels — **Step Plan**
(Credits) and **Standard** (pay-as-you-go) — share the same key; the base URL picks
the channel. Read this file, then `bundle/always-load/`, then the one `by-task/`
card your task matches.

## Routing table

| When the task is… | Read these | Skip |
| --- | --- | --- |
| Any StepFun question | `CLAUDE.md`, `bundle/always-load/` | everything else |
| Plan / billing / credits / tiers | `bundle/always-load/plan.md` | `by-task/` |
| Base URLs / channel routing | `bundle/always-load/endpoints.md` | — |
| Credentials / wiring a client | `bundle/always-load/auth.md`, `bundle/by-task/client-setup.md` | — |
| Which model / is X available | `bundle/always-load/models.md`, `bundle/evidence/models/not-on-this-plan.md` | — |
| Token limits | `bundle/always-load/models.md`, `bundle/evidence/models/token-limits.md` | — |
| Chat / messages / responses API | `bundle/by-task/chat-apis.md` | — |
| Reasoning effort | `bundle/by-task/reasoning.md` | — |
| Tool calling | `bundle/by-task/tool-calling.md` | — |
| Streaming | `bundle/by-task/streaming.md` | — |
| JSON / structured output | `bundle/by-task/structured-output.md` | — |
| Multi-turn / prompt cache | `bundle/by-task/context-and-cache.md` | — |
| Voice pipeline (ASR → reasoning → TTS) | `bundle/by-task/voice-pipeline.md` | — |
| TTS / ASR / audio | `bundle/by-task/audio.md` | — |
| Images / video input | `bundle/by-task/vision-and-video.md` | — |
| Image generation / editing | `bundle/by-task/images.md`, `bundle/evidence/models/step-image-edit-2.md` | — |
| File upload | `bundle/by-task/files.md` | — |
| Errors / debugging | `bundle/by-task/errors-and-debugging.md` | — |
| Static hosting / steppage | `bundle/by-task/static-hosting.md` | — |
| Migrate from OpenAI | `bundle/by-task/openai-migration.md` | — |
| Step Code CLI | `bundle/evidence/reference/step-code.md` | — |
| Sources disagree | `bundle/evidence/source-contradictions.md` | — |
| Standard pay-as-you-go channel | `bundle/always-load/standard-channel.md` | — |

## Non-negotiables

1. **Two channels exist** — Step Plan (Credits) and Standard (pay-as-you-go, `/v1`).
   Use the right channel for the right key. (`endpoints.md`, `auth.md`)
2. **The model allowlist is account-specific.** Never infer availability from the docs
   alone — read `models.md` and the not-on-plan evidence card. (`models.md`)
3. **Never hand-edit `corpus/`**; never build on `_archive/`.
4. **One fact, one home** — link to a card, never copy its facts.
