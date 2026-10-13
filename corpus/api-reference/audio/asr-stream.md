> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Streaming Speech Recognition (Bidirectional Streaming)

WebSocket-based bidirectional streaming speech recognition: send audio chunks in real time and continuously receive incremental and final transcription results. Supports server-side VAD (voice activity detection), suitable for real-time conversations, voice assistants, live captioning, and similar scenarios. Recommended model: `stepaudio-2.5-asr-stream`.

<Info>
  To submit audio once over HTTP + SSE and receive streaming recognition results, see [Speech Recognition (Streaming Output)](/docs/en/api-reference/audio/asr-sse).
</Info>

## Endpoint

Connect via WebSocket: `wss://api.stepfun.ai/v1/realtime/asr/stream`

## Authentication

* `Authorization` `string` ***required***<br />Authentication token in the format `Bearer $STEPFUN_API_KEY`.

## Client Messages

### Session update (session.update)

Update the session configuration, including audio format and recognition parameters.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "event_id": "event_123",
  "type": "session.update",
  "session": {
    "audio": {
      "input": {
        "format": {
          "type": "pcm",
          "codec": "pcm_s16le",
          "rate": 16000,
          "bits": 16,
          "channel": 1
        },
        "transcription": {
          "model": "stepaudio-2.5-asr-stream",
          "language": "zh",
          "prompt": "Please transcribe the speech you hear.",
          "full_rerun_on_commit": true,
          "enable_itn": true
        },
        "turn_detection": {
          "type": "server_vad",
          "silence_duration_ms": 800,
          "threshold": 0.5
        }
      }
    }
  }
}
```

* `event_id` `string` ***required***<br />Event ID of the current message.

* `type` `string` ***required***<br />Message type. Fixed as `session.update`.

* `session.audio.input.format` `object`<br />Audio format.

  <Expandable>
    * `type` `string`<br />Audio container format. Supports `pcm`, `ogg`.
    * `codec` `string`<br />Audio codec; use `pcm_s16le` when `type=pcm`.
    * `rate` `integer`<br />Sample rate.
    * `bits` `integer`<br />Bit depth.
    * `channel` `integer`<br />Channel count.
  </Expandable>

* `session.audio.input.transcription` `object`<br />Recognition configuration.

  <Expandable>
    * `model` `string`<br />Transcription model name. Supports `stepaudio-2.5-asr-stream`.
    * `language` `string`<br />Recognition language; defaults to English when omitted. Supported values: `zh`, `en`, `ja`, `ko`, `fr`, `es`. Japanese, Korean, French, and Spanish are in preview.
    * `prompt` `string`<br />Prompt used to provide additional context or domain-specific terminology.
    * `full_rerun_on_commit` `boolean`<br />Whether to run a second-pass correction after commit. Default `false`.
    * `enable_itn` `boolean`<br />Whether to enable ITN (inverse text normalization).
  </Expandable>

* `session.audio.input.turn_detection` `object`<br />Voice activity detection (VAD) configuration.

  <Expandable>
    * `type` `string`<br />Detection type. Supports `server_vad`.
    * `silence_duration_ms` `integer`<br />Silence threshold; a sentence is considered finished after this duration of silence.
    * `threshold` `number`<br />VAD detection threshold; the higher the value, the stricter the detection.
  </Expandable>

Additional notes:

* Currently supports `stepaudio-2.5-asr-stream`.
* If `turn_detection.type=server_vad` is not set, the server does not perform VAD automatically; in that case the client must actively send `input_audio_buffer.commit`.

### Append audio (input\_audio\_buffer.append)

Send audio data for real-time recognition.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "event_id": "event_124",
  "type": "input_audio_buffer.append",
  "audio": "base64_encoded_audio_data"
}
```

* `event_id` `string` ***required***<br />Unique event identifier.
* `audio` `string` ***required***<br />Base64-encoded audio data (WAV format).

### Commit buffer (input\_audio\_buffer.commit)

Send this message only when `server_vad` is disabled, to ask the server to commit the audio buffer and trigger transcription.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "event_id": "event_125",
  "type": "input_audio_buffer.commit"
}
```

* `event_id` `string` ***required***<br />Unique event identifier.

## Server Messages

### Session created (session.created)

Confirms the session was created successfully.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "319612d9-aede-4456-a1fd-bb9c21493cd9",
    "type": "session.created",
    "meta": {
        "session_id": "test_trace_1766470129914296764",
        "timestamp": 1766468589040
    },
    "session": {
        "audio": {
            "input": {
                "transcription": {
                    "language": "zh"
                },
                "format": {
                    "type": "pcm",
                    "codec": "pcm_s16le",
                    "rate": 16000,
                    "bits": 16,
                    "channel": 1
                },
                "turn_detection": {
                    "type": "server_vad",
                    "silence_duration_ms": 800
                }
            }
        }
    }
}
```

### Session updated (session.updated)

Confirms the session configuration was updated successfully.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "319612d9-aede-4456-a1fd-bb9c21493cd9",
    "type": "session.updated",
    "meta": {
        "session_id": "test_trace_1766470129914296764",
        "timestamp": 1766468589040
    },
    "session": {
        "audio": {
            "input": {
                "transcription": {
                    "language": "zh"
                },
                "format": {
                    "type": "pcm",
                    "codec": "pcm_s16le",
                    "rate": 16000,
                    "bits": 16,
                    "channel": 1
                },
                "turn_detection": {
                    "type": "server_vad",
                    "silence_duration_ms": 800
                }
            }
        }
    }
}
```

### Speech started (input\_audio\_buffer.speech\_started)

Returned only when `server_vad` is enabled; indicates the server detected the start of speech.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "319612d9-aede-4456-a1fd-bb9c21493cd9",
    "type": "input_audio_buffer.speech_started",
    "meta": {
        "session_id": "test_trace_1766470129914296764",
        "timestamp": 1766470145337
    },
    "audio_start_ms": 15240,
    "item_id": "item_26cbd6a7-16e8-44c9-b6b4-d4d3b3c87b41"
}
```

### Speech stopped (input\_audio\_buffer.speech\_stopped)

Returned only when `server_vad` is enabled; indicates the server detected the end of speech.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "406d719a-3392-4ca4-88b3-9f12d8189b74",
    "type": "input_audio_buffer.speech_stopped",
    "meta": {
        "session_id": "test_trace_1766470129914296764",
        "timestamp": 1766470143512
    },
    "audio_start_ms": 13480,
    "item_id": "item_8228b4a6-f127-4a60-8f33-20fcb7d9ff7d"
}
```

### Buffer committed (input\_audio\_buffer.committed)

Confirms the audio buffer was committed.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "event_id": "event_xxx",
  "type": "input_audio_buffer.committed",
  "meta": {
    "session_id": "sess_xxx",
    "timestamp": 1642694400000
  },
  "item_id": "item_xxx",
  "previous_item_id": "item_yyy"
}
```

### Conversation item created (conversation.item.created)

A new conversation item (transcription result) has been created.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "event_id": "event_xxx",
  "type": "conversation.item.created",
  "meta": {
    "session_id": "sess_xxx",
    "timestamp": 1642694400000
  },
  "previous_item_id": "item_yyy",
  "item": {
    "id": "item_xxx",
    "object": "realtime.item",
    "type": "message",
    "status": "in_progress",
    "role": "user",
    "content": [
      {
        "type": "input_audio"
      }
    ]
  }
}
```

### Transcription delta (conversation.item.input\_audio\_transcription.delta)

Returns incremental transcription results (streaming output).

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "event_id": "event_xxx",
  "type": "conversation.item.input_audio_transcription.delta",
  "meta": {
    "session_id": "sess_xxx",
    "timestamp": 1642694400000
  },
  "item_id": "item_xxx",
  "content_index": 0,
  "text": "你好请问有什么可以帮助您的",
  "stash": "退款",
  "language": "zh",
  "words": [
    { "word": "你", "start": 0.00, "end": 0.20, "final": true },
    { "word": "好", "start": 0.20, "end": 0.45, "final": true },
    { "word": "退", "start": 1.80, "end": 1.95, "final": false },
    { "word": "款", "start": 1.95, "end": 2.10, "final": false }
  ]
}
```

* `item_id` `string`<br />Conversation item ID.
* `content_index` `int`<br />Content index.
* `text` `string`<br />The cumulative full text up to now (including corrections to earlier text). The client should replace the displayed text as a whole rather than appending to it.
* `stash` `string`<br />The correctable trailing text (the last few characters, which may be rewritten later). Consider displaying it in a style distinct from `text`.
* `language` `string`<br />Detected language of the recognized text.
* `words` `list`<br />Per-word timing array; each element is `{ "word", "start", "end", "final" }`. `start` / `end` are in seconds (float). `final=false` indicates the word is still in the `stash` region and its timing is a temporary estimate.

### Transcription completed (conversation.item.input\_audio\_transcription.completed)

Returns the complete transcription result.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "event_id": "event_xxx",
  "type": "conversation.item.input_audio_transcription.completed",
  "meta": {
    "session_id": "sess_xxx",
    "timestamp": 1642694400000
  },
  "item_id": "item_xxx",
  "content_index": 0,
  "transcript": "你好，世界",
  "language": "zh",
  "words": [
    { "word": "你", "start": 0.00, "end": 0.20, "final": true },
    { "word": "好", "start": 0.20, "end": 0.45, "final": true }
  ],
  "reason": "commit",
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 10,
    "total_tokens": 10
  }
}
```

* `item_id` `string`<br />Conversation item ID.
* `content_index` `int`<br />Content index.
* `transcript` `string`<br />The complete transcription text.
* `language` `string`<br />Detected language of the transcription.
* `words` `list`<br />Per-word timing for the segment; same structure as in `delta`, with `final` always `true`.
* `reason` `string`<br />The reason the transcription was finalized, e.g. `commit`.
* `usage` `object`<br />Usage statistics.

### Error (error)

Returns error information.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "event_id": "event_xxx",
  "type": "error",
  "meta": {
    "session_id": "sess_xxx",
    "timestamp": 1642694400000
  },
  "error": {
    "type": "invalid_request_error",
    "code": "invalid_value",
    "message": "Error description",
    "param": "audio",
    "event_id": "event_xxx"
  }
}
```

Error types:

| Type | Description |
| - | - |
| `invalid_request_error` | Invalid request parameters |
| `internal_error` | Internal server error |
| `risk` | Content safety risk |

Error codes:

| Code | Description |
| - | - |
| `invalid_value` | Invalid parameter value |
| `missing_param` | Missing required parameter |
| `internal_error` | Internal error |
| `max_idle_timeout` | Idle timeout |
| `pong_timeout` | Heartbeat timeout |
| `risk_blocked` | Content blocked |

## Troubleshooting

* Connection failed: check that the service is reachable and that the endpoint and authentication are correct.
* No recognition result: verify the audio format, codec, and quality.
* Low recognition accuracy: try using the `prompt` field or a different model.
* High latency: reduce the audio chunk size.

For the full list of error codes, see [Error Codes](/docs/en/api-reference/error-codes).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.