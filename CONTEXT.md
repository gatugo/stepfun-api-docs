# Context — stepfun-api

Dated. One place for where you are. `Next:` is at the bottom.

## 2026-10-13 — standard-channel branch created

**What happened:** `stepfun-api-v2` (Step Plan only) was copied to
`stepfun-api-v2-standard` to add the Standard pay-as-you-go channel alongside
the existing Step Plan coverage. Two channels, one bundle.

**What changed:**
- `CLAUDE.md` — routing table now covers both channels; non-negotiable updated
- `PURPOSE.md` — genericised; no longer Step Plan-only
- `bundle/always-load/standard-channel.md` — new, skeleton, `draft`
- `bundle/always-load/models.md` — Channel column added (`step-plan | standard | both`), all status `draft`
- `bundle/by-task/*.md` — endpoint tables dual-column (Step Plan / Standard), all `draft`
- `_account/step-plan-access-info.md` — converted to a template

**Not yet done:** live verification of standard-channel endpoints (no standard
key available yet). All standard-channel cards are `draft` / `unverified`.

Next: populate `standard-channel.md` from corpus, then verify model allowlist
and endpoints once a standard API key is added.

## 2026-10-13 — Q-STD-03 resolved: endpoint parity, with two availability corrections

**What happened:** one cheap live call per endpoint on **both** base URLs. Chat
completions, messages, responses, ASR one-shot SSE, and TTS one-shot all
returned HTTP 200 on both channels. **Files is the one exception — Standard only
(Step Plan returns a bare 404).**

**What changed:**
- `_account/live-calls/2026-10-13-endpoints.md` — new evidence card + reproducible probes (both channels)
- `bundle/by-task/chat-apis.md`, `audio.md`, `files.md`, `bundle/always-load/endpoints.md` — both-channel verification recorded; four request-shape/availability corrections
- `open_questions.md` — Q-STD-03 resolved; fixed `bundbundle` link-label typos
- `HANDOFF.md` — remaining work is Q04 only; guardrails 4–5 rewritten

**Request-shape corrections found:** ASR `format` must sit inside `audio.input`
(a flat `audio.format` → `400 "audio format is required"`); `/v1/files` validates
the file extension (`.txt` rejected, `.wav`/`.mp3`/`.png` accepted);
`/v1/responses` needs ≥512 `max_output_tokens` or `step-3.7-flash` returns
`status="incomplete"` with empty output.

**Availability corrections found (the interesting part):**
- **Responses is not Standard-only.** Sources say the Step Plan URL is
  undocumented; `POST /step_plan/v1/responses` returns 200 with
  `status=completed`. Docs incomplete, not the endpoint.
- **Files really is Standard-only.** `POST /step_plan/v1/files` returns 404 —
  upgrading `files.md`'s "treat as unconfirmed" caveat to a verified absence.
- **A 429 is a throttle, not a 404.** `step-3.5-flash` on Step Plan `/messages`
  returned `429 rate_limited` three times while every other call in the same
  minute succeeded, then 200 on retry. Don't read rate limits as absence.

**Untested surface:** the streaming WebSocket endpoints
(`wss://…/realtime/audio`, `wss://…/realtime/asr/stream`) — out of scope for a
one-shot parity probe.

Next: Q04 — the deadline has passed. `step-image-edit-2` retired 2026-10-10 and
is confirmed dead (HTTP 400 on both channels, 2026-10-13); the model has dropped
out of the Step Plan list, which is now 6 models, not 7. No successor is named,
which remains a product decision rather than something a live call can settle.
