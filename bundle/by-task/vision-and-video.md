---
card: vision-and-video
tier: by-task
status: verified
verified_on: 2026-10-08
source: corpus/guides/developer/image-chat.md, corpus/guides/developer/video-chat.md, corpus/guides/models/vision.md
---

# Vision and video input

Image and video understanding runs through **Chat Completions**
(`POST https://api.stepfun.ai/step_plan/v1/chat/completions` on the Step Plan
channel; standard channel — pay-as-you-go: `POST https://api.stepfun.ai/v1/chat/completions`).
Vision is **native** on both models below — no vision MCP or auxiliary model.

| Model | Image input | Video input | Context |
| --- | --- | --- | --- |
| `step-5-preview` | Yes — **recommended** | Yes | 1M tokens |
| `step-3.7-flash` | Yes | Yes | 256K tokens |
| `step-3.5-flash` / `step-3.5-flash-2603` | **No** | **No** | text only |

## Image input

Add an `image_url` item to the `user` message content, alongside your `text`
prompt. URLs are preferred over Base64 for performance.

| Rule | Value |
| --- | --- |
| Formats | JPG/JPEG, PNG, static GIF, WebP |
| Transport | http/https URL, Base64 data URL, or `stepfile://<File ID>` from the Files API |
| Images per request | `step-5-preview`: up to 60 (also subject to its context window); other models 10–50 |
| Combined upload size | keep within 20 MB |
| Resolution | keep longest side under 4096px; images are resized to optimal dimensions |
| `detail` | `step-3.7-flash` defaults to low (~169 tokens/image); set `detail: "high"` for fine detail — token usage scales with image size and latency increases |

Base64 data URL prefixes: `data:image/jpeg;base64,` (jpg) ·
`data:image/png;base64,` (png) · `data:image/gif;base64,` (gif) ·
`data:image/webp;base64,` (webp).

Negatives and gotchas:

- **Metadata is stripped** (path, filename, size, resolution, author, camera
  model, location) before inference, for privacy.
- Tiny fonts reduce recognition quality; rotated/cropped/incomplete images hurt
  recognition; numeric counts are estimates, not exact.
- `step-3.7-flash` renders transparent PNG regions as **black** — flatten onto a
  white background first.
- With many images, place images **early and instructions later** — in long
  contexts the model may prioritize later prompts.
- Over the image cap? Summarize images with the vision model first, then pass
  the summaries as text context.

Latency: the server downloads external URLs, so host images on CDN/high-bandwidth
storage. For reuse (few-shot), upload once via the Files API with
`purpose=storage` and reference the File ID as `stepfile://…` so the model
fetches from StepFun storage ([files.md](files.md)). To cut first-token latency,
resize (low/default detail: longest side 728px or 1280px; high: a multiple of
504px or 2688px) and compress at quality ~80.

## Video input

`step-5-preview` natively supports multimodal input: include a `video_url` item
with your prompt in the `user` message.

| Rule | Value |
| --- | --- |
| Transport | directly accessible video URL, inline Base64 (`data:video/mp4;base64,…`), or `stepfile://` after Files API upload (`purpose=storage`) |
| Containers | MP4, QuickTime, Matroska |
| Size | a single MP4 video URL under 128 MB (`step-5-preview` and `step-3.7-flash`) |

Negatives and gotchas:

- Place the **video before the instruction** in the message to improve results.
- Downloading and safety checks take time — show progress UI.
- Over 128 MB or another container? Split into sub-128MB MP4s with ffmpeg
  (`ffmpeg -i sample.mkv -codec copy sample.mp4` to convert; segment into
  120-second clips for large files), then summarize each clip.
- The server downloads your video — host on fast, publicly accessible storage
  (object storage with CDN) or reuse via `stepfile://`.

## Related cards

[chat-apis.md](chat-apis.md) (multipart message shapes) ·
[files.md](files.md) (uploads) · [images.md](images.md) (image *generation* —
different job, and retiring 2026-10-10) ·
[context-and-cache.md](context-and-cache.md) (caching reused images/video).
