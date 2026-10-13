> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Music Generation

The text-to-music endpoint uses an asynchronous "submit + query" model: first create a generation task and obtain a `task_id`, then poll the task status until it reaches the `SUCCESS` or `FAILED` terminal state.

<Note>
  Music generation is a long-running autoregressive task. Generating a complete song usually takes from tens of seconds to a few minutes.
</Note>

## Endpoint

`POST https://api.stepfun.ai/v1/audio/music`

## Capabilities

Three task types are provided, covering four use cases:

| Use case | `task` | Input | Output |
| :- | :- | :- | :- |
| Song generation | `text_to_music` | Style description + optional lyrics | A complete song with vocals |
| Instrumental generation | `text_to_music` + `instrumental=true` | Style description | Instrumental without vocals |
| Song cover / style transfer | `music_cover` | Reference song + style description + lyrics | A cover that follows the original melody |
| Vocal-to-music | `vocal_to_music` | Dry vocal without accompaniment + style description + lyrics | A complete song that preserves the input timbre |

When `text_to_music` is used without `lyrics`, the server generates the lyrics automatically.

## Common Conventions

### Request Headers

| Header | Required | Description |
| :- | :- | :- |
| `Authorization` | Yes | `Bearer $STEP_API_KEY` |
| `Content-Type` | Yes | `application/json; charset=utf-8` |

### Unified Error Response

All non-2xx responses use the following structure:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "error": {
    "message": "Error description",
    "type": "Error type identifier"
  }
}
```

Clients should branch programmatically on `error.type` and should not match against the `message` text.

The response also returns an `x-should-retry` header:

* Parameter, authentication, and resource errors (400 / 401 / 404): `false`
* Rate limiting and transient service failures (429 / 500 / 503): `true`
* Quota-related 429s cannot be resolved by retrying and must still be handled separately based on `error.type`.

Audio input fields use the Base64 string of the raw file bytes, without the `data:` prefix.

## Submit a Music Generation Task

`POST https://api.stepfun.ai/v1/audio/music/submit`

### Request Parameters

* `task` `string` ***required***<br />Task type. Supports `text_to_music`, `music_cover`, and `vocal_to_music`.
* `model_id` `string` ***required***<br />Music model identifier. Fixed to `stepaudio-3-music-preview`.
* `caption` `string` ***required***<br />Style description such as genre, vocals, emotion, and key.
* `lyrics` `string` ***optional***<br />Lyrics, with support for song-structure tags. Required for `music_cover` and `vocal_to_music`; for `text_to_music`, the server writes the lyrics automatically when omitted.
* `instrumental` `boolean` ***optional***<br />Whether to generate a pure instrumental. Default `false`. Only supported by `text_to_music`.
* `song_audio` `string` ***optional***<br />Base64 encoding of the complete reference song. Required for `music_cover`.
* `vocal_audio` `string` ***optional***<br />Base64 encoding of the dry vocal without accompaniment. Required for `vocal_to_music`.
* `response_format` `string` ***optional***<br />Output format. Supports `wav`, `flac`, `opus`, `mp3`, and `pcm`. Default `wav`.
* `sample_rate` `integer` ***optional***<br />Output sampling rate. Default `48000`; when omitted or set to `0`, the model's native sampling rate is kept.
* `bit_rate` `integer` ***optional***<br />MP3 / Opus bit rate, in kbps.
* `lyrics_rewrite` `boolean` ***optional***<br />Whether to rewrite the provided lyrics. Default `false`.
* `disable_caption_rewrite` `boolean` ***optional***<br />Whether to skip automatic rewriting of `caption`. Default `false`.
* `max_tokens` `integer` ***optional***<br />Upper limit on generated tokens. Default `16000`.
* `temperature` `number` ***optional***<br />Sampling temperature. Default `0.85`; `0` is not currently supported.
* `top_k` `integer` ***optional***<br />Sampling parameter. Default `80`.
* `top_p` `number` ***optional***<br />Sampling parameter. Default `0.92`.
* `repetition_penalty` `number` ***optional***<br />Repetition penalty. Default `1.08`.

### Parameter Applicability Matrix

| Parameter | `text_to_music` song | `text_to_music` instrumental | `music_cover` | `vocal_to_music` |
| :- | :- | :- | :- | :- |
| `caption` | Required | Required | Required | Required |
| `lyrics` | Optional; auto-written if empty | Must not be passed | Required | Required |
| `instrumental` | Omit or `false` | Must be `true` | Not supported | Not supported |
| `song_audio` | Not used | Not used | Required | Not used |
| `vocal_audio` | Not used | Not used | Not used | Required |

### Parameter Notes

#### Instrumental and Lyrics

When `instrumental=true`, `lyrics` must not be passed at the same time. The `[Instrumental]` tag in lyrics indicates only a local instrumental section and cannot replace the top-level `instrumental=true`.

#### Cover

For `music_cover`, the melody follows the reference song, while `caption` controls the style, timbre, arrangement, and emotion. Providing lyrics consistent with the sung content of the original song is recommended.

#### Vocal-to-Music

For `vocal_to_music`, the melody mainly follows the dry vocal and preserves the vocal timbre of the input. The actual sung content of the dry vocal must be a subset or the full set of `lyrics`.

#### Caption Rewriting

By default, the server rewrites `caption` into a normalized English style prompt and returns it as `rewritten_caption` in the query endpoint.

`disable_caption_rewrite=true` cannot be used together with `lyrics_rewrite=true`; when used in a non-instrumental `text_to_music` scenario, lyrics must be provided explicitly.

#### Output Duration

The output duration is determined by the model and cannot be controlled precisely via parameters. The duration may differ across multiple generations from the same input, and is typically 1 to 3 minutes.

### Lyric Structure Tags

Each lyric structure tag must be on its own line.

Common tags:

* `[Intro]`
* `[Verse 1]`
* `[Pre-Chorus]`
* `[Chorus 1]`
* `[Bridge]`
* `[Instrumental]`
* `[Hook]`
* `[Break]`
* `[Drop]`
* `[Ad-lib]`
* `[Outro]`

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
[Verse 1]
The green peppers still carry morning dew
The tomato you picked rolls to your feet

[Instrumental]

[Chorus 1]
The early-autumn market is packed with crowds
Your figure grows smaller as you walk away
```

### Caption Writing Tips

`caption` supports Chinese or English. Describing the following dimensions is recommended:

| Dimension | Examples |
| :- | :- |
| Genre | lo-fi, R\&B, city pop, dance-pop |
| Vocals | female, male, warm, breathy, vibrato |
| Groove | slow, mid-tempo, upbeat, danceable |
| Timbre | warm, open, grainy, hazy |
| Emotion | nostalgic, wistful, uplifting, hopeful |
| Key | B minor, D minor, C major |

### Response

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "task_id": "01959f5e-0f31-7a2b-9c4d-1234567890ab"
}
```

`task_id` is used to query the task result and for troubleshooting.

### Error Codes

| HTTP | `error.type` | Trigger |
| :- | :- | :- |
| 400 | `request_params_invalid` | Invalid JSON, missing required fields, or invalid parameter values or combinations |
| 401 | `not_allowed` | Missing or invalid authentication token |
| 402 | `insufficient_credit` | Insufficient credit balance |
| 404 | `model_invalid` | Wrong model ID, or the account has no permission for the model |
| 429 | `rate_limited` | Request rate or concurrency exceeds the limit |
| 429 | `project_credit_limit_exceeded` / `member_project_credit_limit_exceeded` | The project or member has reached its credit limit |
| 503 | `service_unavailable` | Service overloaded or task enqueue failed |

Content moderation may return 451 synchronously at the submission stage, or return `FAILED` with `error.stage=censor` during task execution.

### Call Examples

<Tabs>
  <Tab title="Song generation">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl -X POST "https://api.stepfun.ai/v1/audio/music/submit" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $STEP_API_KEY" \
      -d '{
        "task": "text_to_music",
        "model_id": "stepaudio-3-music-preview",
        "caption": "A soul and R&B song, female vocal, D minor, warm and nocturnal",
        "lyrics": "[Verse 1]\n...\n[Chorus 1]\n...",
        "response_format": "mp3"
      }'
    ```
  </Tab>

  <Tab title="Instrumental">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl -X POST "https://api.stepfun.ai/v1/audio/music/submit" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $STEP_API_KEY" \
      -d '{
        "task": "text_to_music",
        "model_id": "stepaudio-3-music-preview",
        "instrumental": true,
        "caption": "A pop-style guzheng piece interwoven with flute and xiao, warm and expansive",
        "response_format": "mp3"
      }'
    ```
  </Tab>

  <Tab title="Song cover">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl -X POST "https://api.stepfun.ai/v1/audio/music/submit" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $STEP_API_KEY" \
      -d '{
        "task": "music_cover",
        "model_id": "stepaudio-3-music-preview",
        "caption": "Soul and R&B with funk influences, warm and breathy vocal",
        "lyrics": "[Verse 1]\n...",
        "song_audio": "<base64 of reference song>",
        "response_format": "mp3"
      }'
    ```
  </Tab>

  <Tab title="Vocal-to-music">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl -X POST "https://api.stepfun.ai/v1/audio/music/submit" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $STEP_API_KEY" \
      -d '{
        "task": "vocal_to_music",
        "model_id": "stepaudio-3-music-preview",
        "caption": "Vibrant dance-pop with uplifting R&B influences",
        "lyrics": "[Verse 1]\n...",
        "vocal_audio": "<base64 of dry vocal>",
        "response_format": "mp3"
      }'
    ```
  </Tab>
</Tabs>

## Query the Task Result

`POST https://api.stepfun.ai/v1/audio/music/query`

Polling once every 5 seconds until `status` reaches a terminal state is recommended; save the audio promptly once it succeeds.

### Request Parameters

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "task_id": "01959f5e-0f31-7a2b-9c4d-1234567890ab"
}
```

| Parameter | Type | Required | Description |
| :- | :- | :- | :- |
| `task_id` | string | Yes | The task ID returned by the submit endpoint |

### Task Status

| Status | Description |
| :- | :- |
| `PENDING` | The task has been enqueued |
| `RUNNING` | The task is being processed |
| `SUCCESS` | Generation complete; the audio can be retrieved |
| `FAILED` | Generation failed; will not fall back |

### In-Progress Response

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "status": "RUNNING",
  "task": "text_to_music",
  "caption": "A soul and R&B song, female vocal, D minor",
  "lyrics": "[Verse 1]\n...",
  "response_format": "mp3",
  "sample_rate": 48000
}
```

### Success Response

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "status": "SUCCESS",
  "task": "text_to_music",
  "caption": "A soul and R&B song, female vocal, D minor",
  "lyrics": "[Verse 1]\n...",
  "response_format": "mp3",
  "sample_rate": 48000,
  "audio": "<base64-encoded generated audio>",
  "rewritten_caption": "A soul and R&B song, female vocal, D minor, warm and nocturnal",
  "rewritten_lyrics": "[Verse 1]\n...\n[Chorus 1]\n..."
}
```

### Failure Response

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "status": "FAILED",
  "task": "music_cover",
  "caption": "...",
  "lyrics": "...",
  "response_format": "mp3",
  "error": {
    "stage": "audio_transcode",
    "message": "unsupported audio format"
  }
}
```

`FAILED` is a business terminal state; the HTTP status code is still 200.

### Response Fields

| Field | Type | Description |
| :- | :- | :- |
| `status` | string | `PENDING`, `RUNNING`, `SUCCESS`, `FAILED` |
| `task` | string | The task type from submission |
| `caption` | string | The style description from submission |
| `lyrics` | string | The submitted or generated lyrics |
| `response_format` | string | Output format |
| `sample_rate` | integer | Output sampling rate |
| `audio` | string (Base64) | The generated audio; returned only on `SUCCESS` |
| `rewritten_caption` | string | The server-rewritten style description; returned only on `SUCCESS` |
| `rewritten_lyrics` | string | The server-generated or rewritten lyrics; returned only on `SUCCESS` |
| `error` | object | The failure reason; returned only on `FAILED` |

### Failure Stages

| `error.stage` | Meaning | Suggested Handling |
| :- | :- | :- |
| `audio_transcode` | Audio cannot be decoded or transcoded, or the sampling rate is invalid | Check the audio format, file, and parameters |
| `no_speech_detected` | No valid vocal detected in the dry vocal | Replace with a clear dry vocal with less silence |
| `censor` | The text or audio was blocked by safety moderation | Adjust the content and resubmit |
| `internal` | Internal server error | Retry later and keep the `task_id` |

### Query Error Codes

| HTTP | `error.type` | Trigger |
| :- | :- | :- |
| 400 | `request_params_invalid` | Invalid request body or missing `task_id` |
| 401 | `not_allowed` | Missing or invalid authentication header |
| 404 | `task_not_found` | The task does not exist or has exceeded its retention period |
| 429 | `rate_limited` | Querying too frequently |
| 503 | `service_unavailable` | Service overloaded or result read failed |

### Query Example

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
curl -X POST "https://api.stepfun.ai/v1/audio/music/query" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $STEP_API_KEY" \
  -d '{
    "task_id": "01959f5e-0f31-7a2b-9c4d-1234567890ab"
  }'
```

## Audio and Output Constraints

| Item | Constraint |
| :- | :- |
| Input encoding | Base64 of the raw audio bytes, without the `data:` prefix |
| Input container | `wav`, `flac`, `opus`, `mp3` |
| Output format | `wav`, `flac`, `opus`, `mp3`, `pcm` |
| Output sampling rate | Native 48 kHz stereo, with server-side resampling supported |

Using MP3 output to reduce the response size is recommended. PCM is a headerless raw stream and must be parsed as 48 kHz, 16-bit, stereo on your own.

## Compliance Notice

When generated content is distributed, published, or used for commercial purposes externally, the caller should add an AI-generated-content label in accordance with applicable laws and regulations.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.