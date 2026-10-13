---
card: files
tier: by-task
status: draft
verified_on: 2026-10-13 (Standard URL live-verified; Step Plan URL still undocumented)
source: corpus/api-reference/files/create.md, corpus/api-reference/files/list.md, corpus/api-reference/files/object.md
---

# File upload and storage

Upload once, reference many times. The Files API exists so source images, video,
and reference audio stay addressable instead of being re-uploaded per request.

## Channel status

| Channel | URL | Status |
|---|---|---|
| **Standard** | `POST https://api.stepfun.ai/v1/files` | ✅ Live-verified 2026-10-13 (multipart `purpose=storage` → `file-…` id; `GET /v1/files` also 200) |
| **Step Plan** | `POST https://api.stepfun.ai/step_plan/v1/files` | ❌ **Verified absent** — HTTP 404 on a live call 2026-10-13. Files is a Standard-channel-only API. |

## Upload — `POST /v1/files`

Multipart form or JSON with a remote URL.

| Field | Required | Notes |
| --- | --- | --- |
| `purpose` | Yes | **only `storage` is supported** (image/video understanding, voice cloning, etc.) |
| `file` | No | binary upload; max **128 MB**; up to **1,000 files per user**; omit when using `url` |
| `url` | No | remote file URL; same supported formats as `file`; `file` takes precedence if both are provided |

Supported `storage` formats:

| Kind | Formats |
| --- | --- |
| Video | mp4 |
| Images | jpg/jpeg, png, webp, static gif |
| Audio | mp3, wav — for voice cloning use 5–10 seconds of audio |

> **Extension is validated, not just MIME type.** A `probe.txt` upload returns
> `400 "The current file extension is not supported"` even with
> `Content-Type: text/plain`. `.wav`, `.mp3`, and `.png` all succeed
> (live-verified 2026-10-13).

SDK: `client.files.create(file=open("clip.wav","rb"), purpose="storage")`.

## File object

| Field | Notes |
| --- | --- |
| `id` | unique File ID (`file-…`) |
| `object` | always `file` |
| `bytes` | file size in bytes |
| `created_at` | Unix timestamp (seconds) |
| `filename` | file name |
| `purpose` | upload purpose — only `storage` is supported |
| `status` | processing status: `success` or `processed` |

## List — `GET /v1/files`

No request parameters. Returns a list of File objects (`data` array plus
`object: "list"`). SDK: `client.files.list()`.

## What uploads are for

- **Voice cloning**: upload reference audio, then pass the returned `file_id` to
  the voice preview/create endpoints ([voice-pipeline.md](voice-pipeline.md),
  [audio.md](audio.md)).
- **Image / video input**: reference uploaded files as `stepfile://<File ID>` in
  chat messages so the model fetches from StepFun storage instead of
  re-downloading ([vision-and-video.md](vision-and-video.md)).
- **ASR/TTS assets**: keep source audio addressable instead of re-uploading per
  request ([audio.md](audio.md)).

## Negatives

- `purpose` accepts only `storage` — no fine-tune/assistants purposes are
  documented.
- Delete, retrieve-content, and per-purpose filters: **not documented** in the
  sources — the API surface here is upload + list only.
- A Step Plan channel URL for Files is not documented; treat `/v1/files` as
  standard-channel pay-as-you-go until confirmed (Q-STD-03).
- The `stepfile://` URI scheme for referencing uploaded files in chat is
  standard-channel documented; Step Plan behaviour is unconfirmed.
