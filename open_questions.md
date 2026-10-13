# Open questions

Never reopen a recorded decision without logging why here.

## Q-STD-01 — RESOLVED 2026-10-13: Standard-channel model allowlist

**Settled by live call** `GET https://api.stepfun.ai/v1/models`.

**Standard channel: 15 models** — all 6 Step Plan models plus 8 Standard-only:
`stepaudio-2.5-chat` · `stepaudio-2.5-realtime` · `stepaudio-2.5-asr-stream` ·
`stepaudio-3-asr-max` · `stepaudio-3-chat-preview` · `stepaudio-3-gen-preview` ·
`stepaudio-3-music-preview` · `stepaudio-3-realtime-preview` · `stepaudio-3-tts`

**Not on any channel:** `step-router-v1` · `step-2x-large` · `step-1x-edit` ·
`deepseek-v4-pro`

Full allowlist: [`bundle/always-load/models.md`](bundle/always-load/models.md),
[`bundle/evidence/models/not-on-this-plan.md`](bundle/evidence/models/not-on-this-plan.md).

## Q-STD-02 — RESOLVED 2026-10-13: Standard-channel reasoning effort parity

**Settled by live call** — `step-3.5-flash` and `step-3.5-flash-2603` both
returned HTTP 200 with `"reasoning_effort": "medium"` against
`https://api.stepfun.ai/v1`. **All four reasoning models accept `low`/`medium`/`high`**
on both channels.

Corrected the API reference's claim that `step-3.5-flash-2603` is `low`/`high`
only — disproved on both channels. Updated [`bundle/always-load/models.md`](bundle/always-load/models.md),
`bundle/evidence/source-contradictions.md`, `_account/step-plan-access-info.md`.

## Q-STD-03 — RESOLVED 2026-10-13: Standard-channel endpoint parity

**Settled by live calls** against `https://api.stepfun.ai/v1` — one cheap call per
endpoint. **All endpoints confirmed on Standard**, matching Step Plan:

| Endpoint | Result |
|---|---|
| `POST /v1/chat/completions` | ✅ HTTP 200 |
| `POST /v1/responses` | ✅ HTTP 200 (`step-5-preview` and `step-3.7-flash`, both `status=completed`) |
| `POST /v1/audio/asr/sse` | ✅ HTTP 200 (SSE `transcript.text.delta` → `.done`) |
| `POST /v1/audio/speech` | ✅ HTTP 200 (audio bytes returned) |
| `POST /v1/files` | ✅ HTTP 200 (multipart, `purpose=storage`) |
| `GET /v1/files` | ✅ HTTP 200 |

Full evidence: [`_account/live-calls/2026-10-13-endpoints.md`](_account/live-calls/2026-10-13-endpoints.md).

Three request-shape corrections came out of it (all recorded on that card):
ASR `format` must sit inside `audio.input`; `/v1/files` needs a real file
extension; `/v1/responses` needs a generous `max_output_tokens` or
`step-3.7-flash` returns `status=incomplete`.

**Remaining Standard gap (informational, not a question):** the streaming
WebSocket endpoints (`wss://…/realtime/audio`, `wss://…/realtime/asr/stream`)
are documented but not live-tested here — WebSocket probes are out of scope for
a one-shot parity check.

## Q05 — OPEN: what is StepFun's documented retry policy for 429?

**Question.** The sources say only "retry after a delay" for HTTP 429, 500, and
503. No backoff intervals, jitter strategy, maximum retry count, `Retry-After`
header, or rate-limit/quota headers appear anywhere in the corpus.

**Why it matters.** A developer cannot build a correct retry loop from the docs,
and the wrong choice either hammers the API or gives up too early.
[`bundle/by-task/errors-and-debugging.md`](bundle/by-task/errors-and-debugging.md)
carries a clearly-labelled non-vendor default — 1 s base, ×2 backoff, ±50%
jitter, 5 attempts — so nobody is blocked, but those numbers are this bundle's
choice, not StepFun's, and must not be quoted as vendor limits.

**How to close it.** Ask StepFun support for the documented rate-limit and retry
policy, or watch the API reference for a retry section. Until then, treat the
bundle's figures as a defensive default and not a contract.

**Opened:** 2026-10-13, after a cold-reader test found the bundle answered every
other question asked of it but could not answer this one.

---

## Closed questions

Cards and `HANDOFF.md` cite these IDs. They are recorded here so every citation
resolves. Do not reopen a closed question without logging why above.

### Q01 — RESOLVED 2026-10-08: `reasoning_effort` level mapping

**Question:** do `step-3.5-flash` and `step-3.5-flash-2603` accept only
`low`/`high`, as the API reference claims, or all three levels?

**Settled by live call.** HTTP 200 with `"reasoning_effort": "medium"` on both
3.5 variants, on both channels. **All four reasoning models accept
`low`/`medium`/`high`.** The API reference's claim is wrong, and so was the
earlier owner ruling (v1 ADR-005) that put base `step-3.5-flash` at `low`/`high`.

Resolution: [`bundle/by-task/reasoning.md`](bundle/by-task/reasoning.md) and
[`bundle/evidence/source-contradictions.md`](bundle/evidence/source-contradictions.md).

### Q02 — RESOLVED 2026-10-13: is `stepaudio-2.5-asr-stream` callable on Step Plan?

**Settled by live call.** Not callable — absent from the Step Plan model list,
and the streaming route is Standard-only. The confirmed ASR path on this account
is the one-shot `POST /v1/audio/asr/sse` against `stepaudio-2.5-asr`.

### Q03 — RESOLVED 2026-10-13: endpoint parity across the two channels

Superseded by **Q-STD-03** above, which settled it with one live call per
endpoint. Chat, Messages, Responses, ASR SSE, and TTS all return HTTP 200 on
**both** channels; **Files is Standard-only** (Step Plan returns a bare 404).

### Q04 — ANSWERED IN PART 2026-10-13: what replaces `step-image-edit-2`?

**Settled:** the deadline has passed and the model is dead. `step-image-edit-2`
retired 2026-10-10; live calls on 2026-10-13 returned **HTTP 400
`model step-image-edit-2 not supported`** from both `/v1/images/generations` and
`/step_plan/v1/images/generations`, and the model dropped out of the Step Plan
list, which went from 7 models to 6.

**Still open — a product decision, not verifiable by us:** no successor image
model is named in any source. A replacement could appear without the corpus
noticing, so re-check the dashboard before answering any image question.

Evidence: [`_account/live-calls/2026-10-13-image-api-retired.md`](_account/live-calls/2026-10-13-image-api-retired.md)
and [`bundle/evidence/models/step-image-edit-2.md`](bundle/evidence/models/step-image-edit-2.md).

