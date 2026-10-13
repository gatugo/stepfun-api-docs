> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Speech Recognition (Streaming Output)

HTTP + SSE based speech recognition: submit the audio once, and the server continuously pushes incremental and final transcription results over SSE. Suitable for server-side calls, file transcription, and near-real-time processing. Recommended model: `stepaudio-3-asr-max`.

<Info>
  For WebSocket-based real-time bidirectional streaming recognition, see [Streaming Speech Recognition (Bidirectional Streaming)](/docs/en/api-reference/audio/asr-stream).
</Info>

## Endpoint

`POST https://api.stepfun.ai/v1/audio/asr/sse`

<Note>
  For Step Plan, use `POST https://api.stepfun.ai/step_plan/v1/audio/asr/sse`.
</Note>

## Request Headers

* `Content-Type` `string` ***required***<br />Must be `application/json`.
* `Accept` `string` ***required***<br />Must be `text/event-stream`.
* `Authorization` `string` ***required***<br />Authentication token in the format `Bearer $STEPFUN_API_KEY`.

## Request Parameters

* `audio` `object` ***required***<br />Audio data and recognition configuration.

  <Expandable>
    * `data` `string` ***required***<br />Base64-encoded audio data.
    * `input` `object` ***required***<br />Recognition and audio format configuration.

        <Expandable>
          * `transcription` `object`<br />Recognition configuration.

                <Expandable>
                  * `language` `string`<br />Target language; defaults to English when omitted. Supported values: `zh`, `en`, `ja`, `ko`, `fr`, `es`. Japanese, Korean, French, and Spanish are in preview.
                  * `model` `string`<br />Model name. Supports `stepaudio-3-asr-max` and `stepaudio-2.5-asr`.
                  * `enable_itn` `bool` ***optional***<br />Whether to enable ITN (inverse text normalization). Default `true`.
                </Expandable>

          * `format` `object`<br />Audio format.

                <Expandable>
                  * `type` `string`<br />Audio container format. Supports `ogg`, `mp3`, `wav`, `pcm`, `m4a`.
                  * `codec` `string`<br />Codec; when `type=pcm`, typically `pcm_s16le`.
                  * `rate` `int`<br />Sample rate; required for `pcm`, optional for other formats.
                  * `bits` `int`<br />Bit depth; required for `pcm`, optional for other formats.
                  * `channel` `int`<br />Channel count; required for `pcm`, optional for other formats.
                </Expandable>
        </Expandable>
  </Expandable>

### Request Example

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "audio": {
    "data": "audioData",
    "input": {
      "transcription": {
        "language": "zh",
        "model": "stepaudio-3-asr-max",
        "enable_itn": true
      },
      "format": {
        "type": "pcm",
        "codec": "pcm_s16le",
        "rate": 16000,
        "bits": 16,
        "channel": 1
      }
    }
  }
}
```

<Info>
  Compatibility note: The SSE endpoint no longer supports the `full_rerun_on_commit` (second-pass correction) parameter. If legacy clients still send it, the server ignores it without affecting the recognition result. For second-pass correction, use the WebSocket endpoint (see [Streaming Speech Recognition (Bidirectional Streaming)](/docs/en/api-reference/audio/asr-stream)).
</Info>

Additional notes:

* Audio data must be Base64-encoded.
* Supported audio formats: `ogg`, `mp3`, `wav`, `pcm`, `m4a`.
* When the audio format is `pcm`, `rate`, `bits`, and `channel` are required; for `ogg`, `mp3`, `wav`, and `m4a` they are optional.

## Response

SSE streaming response with the following event types.

### Delta event (transcript.text.delta)

Incremental transcription text.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "type": "transcript.text.delta",
  "meta": {
    "session_id": "sse_1642694400123456789",
    "timestamp": 1642694400123
  },
  "delta": "recognized "
}
```

* `type` `string`<br />Event type. Fixed as `transcript.text.delta`.
* `meta.session_id` `string`<br />Session ID.
* `meta.timestamp` `int64`<br />Server-side event Unix timestamp, in milliseconds.
* `delta` `string`<br />Incremental transcription text.

### Done event (transcript.text.done)

The complete transcription text has been generated.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "type": "transcript.text.done",
  "meta": {
    "session_id": "sse_1642694400123456789",
    "timestamp": 1642694400456
  },
  "text": "The complete recognized text",
  "usage": {
    "type": "tokens",
    "input_tokens": 1000,
    "input_token_details": {
      "text_tokens": 0,
      "audio_tokens": 1000
    },
    "output_tokens": 50,
    "total_tokens": 1050
  }
}
```

* `type` `string`<br />Event type. Fixed as `transcript.text.done`.
* `meta.session_id` `string`<br />Session ID.
* `meta.timestamp` `int64`<br />Unix timestamp, in milliseconds.
* `text` `string`<br />The complete transcription text.
* `usage` `object`<br />Usage statistics.

### Error event (error)

Returned when recognition fails.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "type": "error",
  "meta": {
    "session_id": "sse_1642694400123456789",
    "timestamp": 1642694400789
  },
  "message": "Error description"
}
```

* `type` `string`<br />Event type. Fixed as `error`.
* `meta.session_id` `string`<br />Session ID.
* `meta.timestamp` `int64`<br />Unix timestamp, in milliseconds.
* `message` `string`<br />Error description.

For the full list of error codes, see [Error Codes](/docs/en/api-reference/error-codes).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.