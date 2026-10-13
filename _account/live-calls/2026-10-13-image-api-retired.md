---
card: live-call-image-api-retired-2026-10-13
tier: account
status: verified
verified_on: 2026-10-13
source: owner instructions (key provided), live HTTP call
---

# Live call — image API retirement verification 2026-10-13

**Why this call exists.** The cards verified earlier the same day still listed
`step-image-edit-2` as callable, while the retirement notice set the deadline at
2026-10-10. A card verified *after* a deadline it did not re-check is exactly the
failure mode this record closes.

## 1. Model lists re-queried (same day, later)

### Step Plan — `GET https://api.stepfun.ai/step_plan/v1/models`

**6 models returned** (was 7 in the earlier same-day pass):

| Model | Type |
|---|---|
| `step-5-preview` | 大语言模型 |
| `step-3.7-flash` | 大语言模型 |
| `step-3.5-flash` | 大语言模型 |
| `step-3.5-flash-2603` | 大语言模型 |
| `stepaudio-2.5-tts` | 语音合成 |
| `stepaudio-2.5-asr` | 语音识别 |

**`step-image-edit-2` is gone from the Step Plan list.**

### Standard — `GET https://api.stepfun.ai/v1/models`

**15 models returned** — unchanged from the earlier pass. No image model present.

## 2. The retired endpoints, called directly

| Channel | Endpoint | Result |
|---|---|---|
| Step Plan | `POST /step_plan/v1/images/generations` | **HTTP 400** |
| Standard | `POST /v1/images/generations` | **HTTP 400** |

Request body used (identical for both channels):

```json
{"model":"step-image-edit-2","prompt":"a red square","n":1,"size":"256x256"}
```

Response body, verbatim, both channels:

```json
{"error":{"message":"model step-image-edit-2 not supported","type":"request_params_invalid","description":"请求参数错误"}}
```

## What this settles

1. **The retirement is live, not pending.** Both channels reject the model with
   `request_params_invalid`. The endpoints still exist — they return 400, not
   404 — so a 404-based absence check would have wrongly concluded the endpoint
   was missing.
2. **Step Plan is 6 models, not 7.** Every "7 models" claim in the bundle is now
   wrong and was corrected in the same commit.
3. **Standard is still 15.** The Standard allowlist is unaffected.

## How to re-run

```bash
curl -s https://api.stepfun.ai/step_plan/v1/models \
  -H "Authorization: Bearer $STEP_API_KEY" | jq '.data[].id'
curl -s https://api.stepfun.ai/v1/models \
  -H "Authorization: Bearer $STEP_API_KEY" | jq '.data[].id'
```

**Key used:** same key for both channels; base URL selects channel. The key was
never written to any file in this repository.
