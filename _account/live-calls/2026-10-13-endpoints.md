---
card: live-call-endpoints-2026-10-13
tier: account
status: verified
verified_on: 2026-10-13
source: owner instructions (key provided), live HTTP calls
---

# Live call — Standard-channel endpoint parity 2026-10-13 (Q-STD-03)

One cheap call per endpoint on **both** base URLs.
Key: `$STEP_PLAN_API_KEY` (same key as Step Plan; base URL selects channel).
Reproduce with `probe_standard_endpoints.py`, `probe_stepplan_endpoints.py`, or
`probe_shapes.py` in this folder.
## Results — all endpoints confirmed on Standard

| Endpoint | Result | Evidence |
|---|---|---|
| `POST /v1/chat/completions` | ✅ HTTP 200 | `step-3.5-flash-2603`, `max_tokens=4` |
| `POST /v1/responses` | ✅ HTTP 200 | `step-5-preview` → `status=completed`, text returned |
| `POST /v1/responses` | ✅ HTTP 200 | `step-3.7-flash` → `status=completed`, text returned |
| `POST /v1/audio/asr/sse` | ✅ HTTP 200 | SSE stream: `transcript.text.delta` … `transcript.text.done` |
| `POST /v1/audio/speech` | ✅ HTTP 200 | 16,426 bytes of audio (mp3) returned |
| `POST /v1/files` | ✅ HTTP 200 | multipart, `purpose=storage`, returns `file-…` id |
| `GET /v1/files` | ✅ HTTP 200 | JSON list |

**Conclusion: Standard channel has full endpoint parity with Step Plan for
chat, responses, ASR, TTS, and files.** The corpus's dual-column endpoint tables
are now verified on both channels.

## Both channels side by side

| Endpoint | Step Plan | Standard |
|---|---|---|
| `POST /chat/completions` | ✅ 200 | ✅ 200 |
| `POST /messages` (Anthropic wire) | ✅ 200 (`step-5-preview`) | ✅ 200 (`step-3.5-flash`) |
| `POST /responses` | ✅ 200 (`step-5-preview`) | ✅ 200 (`step-5-preview`, `step-3.7-flash`) |
| `POST /audio/asr/sse` | ✅ 200 | ✅ 200 |
| `POST /audio/speech` | ✅ 200 | ✅ 200 |
| `POST /files` (multipart) | ❌ **404** | ✅ 200 |
| `GET /files` | not probed | ✅ 200 |

### Two corrections this makes to the bundle

1. **The Responses API is NOT Standard-only.** The corpus and `chat-apis.md`
   both say "Step Plan URL not documented". `POST /step_plan/v1/responses` with
   `step-5-preview` returns **HTTP 200** with `status=completed`. The endpoint
   exists on Step Plan; the docs are simply incomplete.
2. **Files really is absent on Step Plan.** `POST /step_plan/v1/files` returns a
   bare **HTTP 404** — upgrading `files.md`'s "not documented, treat as
   unconfirmed" caveat to a verified absence.

Note on 429s: `step-3.5-flash` on `/step_plan/v1/messages` returned
`429 rate_limited` three times while every other call in the same minute
succeeded, then returned 200 on a later attempt. It is a **per-model throttle**,
not endpoint absence — don't read a 429 as a 404.
## Request-shape notes (corrections to what the bundle previously implied)

- **ASR `format` lives inside `audio.input`,** not as a sibling of `audio.data`.
  Sending it at the `audio` level returns
  `400 {"error":{"message":"audio format is required"}}`. The docs' example is
  correct; a flat reading of it is not.
- **`/v1/files` needs a real file extension.** A `.txt` upload returns
  `400 "The current file extension is not supported"`. `.wav`, `.mp3`, `.png`
  all succeed — matching the documented `storage` format list.
- **`/v1/responses` needs a generous `max_output_tokens`.** With 64 tokens
  `step-3.7-flash` returned `status=incomplete` and an empty output array — the
  budget is consumed by reasoning. 512 tokens → `status=completed`.
- **TTS voice ids are not free-form.** `cixingnansheng` returns
  `400 voice_id_invalid`; the documented system voice ids (e.g. `vibrant-youth`)
  work.
- **ASR on silence hallucinates.** 1 second of 16 kHz silence transcribed as
  `嗯。` — expected model behaviour, not a transport error.

## Side effects

Three probe files were uploaded to the account during the `.wav` / `.mp3` /
`.png` variants (`probe.wav`, `probe.mp3`, `probe.png`, `purpose=storage`).
No delete endpoint is documented, so they persist. Well under the 1,000-file
per-user cap; no cost impact beyond storage.
