> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Bidirectional Realtime Voice

Enables real-time voice conversation. It accepts audio and text input and produces streaming audio (with a matching text transcript) as output, over a single WebSocket connection.

<Info>
  For model capabilities, supported voices, audio format, and a runnable quick-start, see [StepAudio 2.5 Realtime](/docs/en/guides/models/stepaudio-2.5-realtime). An open-source reference client is available at [Step-Realtime-Console](https://github.com/stepfun-ai/Step-Realtime-Console).
</Info>

## Protocol

WebSocket.

## Endpoint

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
wss://api.stepfun.ai/v1/realtime
```

The model is passed as a query parameter, e.g. `wss://api.stepfun.ai/v1/realtime?model=stepaudio-2.5-realtime`.

## Authentication

* `Authorization` `string` ***required***<br />Authentication token in the format `Bearer $STEPFUN_API_KEY`.

## Request Parameters

* `model` `string` ***required***<br />The model to use. Currently supports `stepaudio-3-realtime-preview` and `stepaudio-2.5-realtime`.

<Note>
  Artificial Analysis leaderboard figures are based on internal parameter configurations; actual API service behavior may differ from the leaderboard results, and the relevant configurations will be opened up progressively in future API versions.
</Note>

<Note>
  Real-time voice conversation supports Chinese and English only; other languages are not available on this endpoint.
</Note>

## Voices

Set the voice with `session.update` before the model produces audio. The following system voices are available:

| Voice ID | Voice |
| :- | :- |
| `soft-spoken-gentleman` | Calm, gentle male voice |
| `magnetic-voiced-male` | Deep, magnetic male voice |
| `vibrant-youth` | Youthful, energetic voice |
| `lively-girl` | Bright, lively female voice |
| `livelybreezy-female` | Light, breezy female voice |
| `elegantgentle-female` | Elegant, gentle female voice |
| `zixinnansheng` | Confident male voice |

You can also use a **cloned voice**: clone it via the [Voice cloning](/docs/en/api-reference/audio/create-voice) API with the `stepaudio-2.5-tts` model, then pass the returned voice ID as `voice`.

<Note>
  Only the voice IDs above (or a valid cloned voice ID) are accepted; other values are rejected with a `400` error. A session's voice cannot be changed once the model has produced audio.
</Note>

## How it works

After the WebSocket connection is established, the client sends **Client Events** and receives **Server Events** to drive the interaction.

### Common fields

The following fields are common to Client and Server Events:

| Field | Type | Description |
| - | - | - |
| `event_id` | string | Event ID |
| `type` | string | Event type (see the lists below) |

## Client Events

### Create / update session (session.update)

Send this event to create or update the session's default configuration. The client may send it at any time to update the session; any field may be updated at any time **except `voice`**. The server responds with a `session.updated` event.

* `modalities` `array<string>`<br />The set of modalities the model may use. Fixed to `["text", "audio"]`.

* `instructions` `string`<br />Default system instructions (i.e. the system message) prepended before the model call. Use this to guide the model's content and format (e.g. "be very concise", "be friendly") and its audio behavior (e.g. "speak quickly", "inject emotion into your voice"). The model is not guaranteed to follow the instructions, but they provide guidance on the desired behavior.

* `voice` `string`<br />The voice used for generation. See [Voices](#voices) for the available system voices and how to use a cloned voice. The voice cannot be changed once the model has produced audio.

* `turn_detection` `object` ***optional***<br />Server VAD configuration. Disabled by default.

  <Expandable>
    * `type` `string` ***required***<br />Currently supports `server_vad`; enables server-side VAD when set.
    * `prefix_padding_ms` `integer` ***optional***<br />Only valid when `type=server_vad`. Amount of audio (in ms) prepended when the start of speech is detected. Default `500`.
    * `silence_duration_ms` `integer` ***optional***<br />Only valid when `type=server_vad`. Silence duration (in ms) after which the user's speech is considered finished. Default `100`.
    * `energy_awakeness_threshold` `integer` ***optional***<br />Only valid when `type=server_vad`. Energy wake-up threshold, range `0–5000`, default `2500`. When audio energy exceeds this threshold the user is considered to have started speaking.
  </Expandable>

* `input_audio_format` `string`<br />Input audio format. Currently supports `pcm16`.

* `output_audio_format` `string`<br />Output audio format. Currently supports `pcm16`.

* `tools` `object array` ***optional***<br />The list of functions available for tool calling.

  <Expandable>
    * `type` `string`<br />Tool type, `function`.
    * `function` `object`<br />Function description.

        <Expandable>
          * `name` `string`<br />Function name. Letters, digits, and `_`/`-` only; keep it under 64 characters.
          * `description` `string`<br />Function description. Tells the model what the function does so it can decide when to call it.
          * `parameters` `object`<br />The function parameters.

                <Expandable>
                  * `type` `object`<br />Parameter schema, usually `object`.
                  * `properties` `object`<br />Parameter definitions, keyed by parameter name, each described by `type` and `description`. See [json-schema](https://json-schema.org/understanding-json-schema/reference/type).
                </Expandable>
        </Expandable>
  </Expandable>

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_abc",
    "type": "session.update",
    "session": {
        "modalities": ["text", "audio"],
        "instructions": "You are a helpful AI assistant. Answer briefly and warmly.",
        "voice": "soft-spoken-gentleman",
        "input_audio_format": "pcm16",
        "output_audio_format": "pcm16",
        "turn_detection": {
            "type": "server_vad",
            "prefix_padding_ms": 500
        }
    }
}
```

### Append audio (input\_audio\_buffer.append)

Append audio bytes to the input audio buffer. The server does not acknowledge this event. In Server VAD mode it triggers model inference.

* `audio` `string`<br />Base64-encoded audio bytes, in the format specified by `input_audio_format` in the session configuration.

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_abc",
    "type": "input_audio_buffer.append",
    "audio": "Base64EncodedAudioData"
}
```

### Commit audio (input\_audio\_buffer.commit)

Commit the user's input audio buffer for inference, creating a new user message item in the conversation. The server responds with an `input_audio_buffer.committed` event. If the input audio buffer is empty, this event produces an error.

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_abc",
    "type": "input_audio_buffer.commit"
}
```

### Clear audio (input\_audio\_buffer.clear)

Clear the user's input audio buffer. The server responds with an `input_audio_buffer.cleared` event.

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_abc",
    "type": "input_audio_buffer.clear"
}
```

### Create conversation item (conversation.item.create)

Add a new item to the conversation context, including messages, function calls, and function-call responses. Use it to populate conversation history or to add new items mid-session, but it cannot populate Assistant audio messages. On success the server responds with `conversation.item.created`; otherwise it sends an error event.

* `previous_item_id` `string`<br />The ID of the previous item.
* `item` `object`<br />The message item; see the message parameters.

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_abc",
    "type": "conversation.item.create",
    "item": {
        "id": "msg_001",
        "type": "message",
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": "Hello"
            }
        ]
    }
}
```

### Delete conversation item (conversation.item.delete)

Send this event to remove an item from the conversation history. The server responds with `conversation.item.deleted`. If the item does not exist, the server responds with an error.

* `item_id` `string`<br />The ID of the item to delete.

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_abc",
    "type": "conversation.item.delete",
    "item_id": "msg_003"
}
```

### Create response (response.create)

Instructs the server to create a Response, i.e. trigger model inference.

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_abc",
    "type": "response.create"
}
```

### Cancel response (response.cancel)

Cancel an in-progress response. The server returns a `response.cancelled` event, or an error if there is no response to cancel.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_abc",
    "type": "response.cancel"
}
```

## Server Events

### Error (error)

Returned when an error occurs during server processing. This may be a client or server problem; the session continues.

* `type` `string`<br />Error type (e.g. `invalid_request_error`, `server_error`).
* `code` `string`<br />Error code, if any.
* `message` `string`<br />Human-readable error message.
* `event_id` `string`<br />The `event_id` of the client event that caused the error, if applicable.

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_bcd",
    "type": "error",
    "error": {
        "type": "invalid_request_error",
        "code": "invalid_param",
        "message": "Incomplete audio content",
        "event_id": "event_567"
    }
}
```

### Session created (session.created)

Returned when the session is created, automatically emitted as the first server event when a new connection is established. Contains the default session configuration.

* `modalities` `array<string>`<br />The set of modalities the model may use. Fixed to `["text", "audio"]`.
* `instructions` `string`<br />Default system instructions prepended before the model call.
* `voice` `string`<br />The voice used for generation.
* `input_audio_format` `string`<br />Input audio format. Currently supports `pcm16`.
* `output_audio_format` `string`<br />Output audio format. Currently supports `pcm16`.
* `volume_ratio` `number`<br />Output volume ratio. Default `1`.

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_def",
    "type": "session.created",
    "session": {
        "id": "sess_001",
        "object": "realtime.session",
        "model": "stepaudio-2.5-realtime",
        "modalities": ["text", "audio"],
        "voice": "soft-spoken-gentleman",
        "input_audio_format": "pcm16",
        "output_audio_format": "pcm16",
        "volume_ratio": 1
    }
}
```

### Session updated (session.updated)

Returned when the session is updated.

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_def",
    "type": "session.updated",
    "session": {
        "modalities": ["text", "audio"],
        "instructions": "You are a helpful AI assistant.",
        "voice": "soft-spoken-gentleman",
        "input_audio_format": "pcm16",
        "output_audio_format": "pcm16"
    }
}
```

### Speech started (input\_audio\_buffer.speech\_started)

Notifies that valid speech input has started; typically used for interruption scenarios. Emitted only when Server VAD is enabled.

* `audio_start_ms` `integer`<br />The start time of the speech within the audio.
* `item_id` `string`<br />The item ID.

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_bcd",
    "type": "input_audio_buffer.speech_started",
    "audio_start_ms": 1000,
    "item_id": "msg_003"
}
```

### Speech stopped (input\_audio\_buffer.speech\_stopped)

Notifies that valid speech input has ended. Emitted only when Server VAD is enabled.

* `audio_end_ms` `integer`<br />The end time of the speech within the audio.
* `item_id` `string`<br />The item ID.

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_1718",
    "type": "input_audio_buffer.speech_stopped",
    "audio_end_ms": 2000,
    "item_id": "msg_003"
}
```

### Response audio delta (response.audio.delta)

Returned as the model generates audio.

* `response_id` `string`<br />The response ID.
* `item_id` `string`<br />The item ID.
* `output_index` `int`<br />The index of the output item in the response.
* `delta` `string`<br />A Base64-encoded audio delta, in the `output_audio_format` set when the session was created.

**Sample**

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_bcd",
    "type": "response.audio.delta",
    "item_id": "msg_008",
    "delta": "Base64EncodedAudioDelta"
}
```

### Response audio done (response.audio.done)

Returned when the model's audio is complete. Also emitted when a response is interrupted, incomplete, or cancelled.

* `response_id` `string`<br />The response ID.
* `item_id` `string`<br />The item ID.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_bcd",
    "type": "response.audio.done",
    "response_id": "resp_001",
    "item_id": "msg_008"
}
```

### Audio transcript delta (response.audio\_transcript.delta)

Streams the text transcript of the model's audio output.

* `response_id` `string`<br />The response ID.
* `item_id` `string`<br />The item ID.
* `output_index` `int`<br />The index of the output item in the response.
* `delta` `string`<br />The transcript delta.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_bcd",
    "type": "response.audio_transcript.delta",
    "item_id": "msg_002",
    "output_index": 0,
    "delta": "Hello, how can I a"
}
```

### Audio transcript done (response.audio\_transcript.done)

Returned when the transcript of the model's audio output finishes streaming. Also emitted when a response is interrupted, incomplete, or cancelled.

* `response_id` `string`<br />The response ID.
* `item_id` `string`<br />The item ID.
* `output_index` `int`<br />The index of the output item in the response.
* `transcript` `string`<br />The complete transcript of the audio.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_4748",
    "type": "response.audio_transcript.done",
    "response_id": "resp_001",
    "item_id": "msg_008",
    "content_index": 0,
    "transcript": "Hello, how can I assist you today?"
}
```

### Thinking delta (response.thinking.delta)

Streams the model's reasoning process as it is generated.

* `response_id` `string`<br />The response ID.
* `item_id` `string`<br />The item ID.
* `output_index` `int`<br />The index of the output item in the response.
* `content_index` `int`<br />The index of the content part in the item's content array.
* `delta` `string`<br />The reasoning delta.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_thinking_delta",
    "type": "response.thinking.delta",
    "response_id": "resp_001",
    "item_id": "msg_008",
    "output_index": 0,
    "content_index": 0,
    "delta": "Analyzing the request..."
}
```

### Thinking done (response.thinking.done)

Returned when the model's reasoning process finishes.

* `response_id` `string`<br />The response ID.
* `item_id` `string`<br />The item ID.
* `output_index` `int`<br />The index of the output item in the response.
* `content_index` `int`<br />The index of the content part in the item's content array.
* `thinking` `string`<br />The complete reasoning text.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_thinking_done",
    "type": "response.thinking.done",
    "response_id": "resp_001",
    "item_id": "msg_008",
    "output_index": 0,
    "content_index": 0,
    "thinking": "Complete reasoning process..."
}
```

### Response text delta (response.text.delta)

Returned as the model generates text output.

* `response_id` `string`<br />The response ID.
* `item_id` `string`<br />The response item ID.
* `output_index` `int`<br />The index of the output item in the response.
* `content_index` `int`<br />The index of the content part containing the text.
* `delta` `string`<br />The generated text delta.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_4950",
    "type": "response.text.delta",
    "response_id": "resp_001",
    "item_id": "msg_009",
    "output_index": 0,
    "content_index": 0,
    "delta": "Sure, "
}
```

### Response text done (response.text.done)

Returned when the model's text output is complete. Also emitted when a response is interrupted, incomplete, or cancelled.

* `response_id` `string`<br />The response ID.
* `item_id` `string`<br />The response item ID.
* `output_index` `int`<br />The index of the output item in the response.
* `content_index` `int`<br />The index of the content part containing the text.
* `text` `string`<br />The complete generated text.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_5152",
    "type": "response.text.done",
    "response_id": "resp_001",
    "item_id": "msg_009",
    "output_index": 0,
    "content_index": 0,
    "text": "Sure, I can help with that."
}
```

### Conversation item created (conversation.item.created)

Returned when a conversation item is created.

* `id` `string`<br />The unique ID of the message. Optional; the server generates one if the client does not provide it.
* `type` `string`<br />The item type, usually `message`.
* `role` `string`<br />The role of the sender (`user`, `assistant`, `system`); applies to message items only.
* `status` `string`<br />The item status (`completed`, `incomplete`).
* `content` `array`<br />The message content; applies to message items.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_bcd",
    "type": "conversation.item.created",
    "previous_item_id": "msg_001",
    "item": {
        "id": "msg_002",
        "object": "realtime.item",
        "type": "message",
        "status": "completed",
        "role": "user",
        "content": [{
            "type": "input_text",
            "transcript": "Hello"
        }]
    }
}
```

### Conversation item deleted (conversation.item.deleted)

Returned when the client deletes a conversation item with `conversation.item.delete`. Used to keep the server's conversation history in sync with the client.

* `item_id` `string`<br />The conversation item ID.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_bcd",
    "type": "conversation.item.deleted",
    "item_id": "msg_001"
}
```

### Input audio transcription completed (conversation.item.input\_audio\_transcription.completed)

The output of the automatic speech recognition (ASR) of the user's input audio. Transcription starts when the client commits the buffer, or when the buffer is committed in Server VAD mode. It runs asynchronously with response creation, so this event may arrive before or after the response events.

* `item_id` `string`<br />The conversation item ID.
* `content_index` `int`<br />The index of the audio content part.
* `transcript` `string`<br />The complete transcript of the audio.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_2122",
    "type": "conversation.item.input_audio_transcription.completed",
    "item_id": "msg_003",
    "content_index": 0,
    "transcript": "Hello"
}
```

### Audio buffer committed (input\_audio\_buffer.committed)

Returned when the client commits the input audio buffer.

* `previous_item_id` `string`<br />The previous item ID in the conversation.
* `item_id` `string`<br />The conversation item ID.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_bcd",
    "type": "input_audio_buffer.committed",
    "previous_item_id": "msg_001",
    "item_id": "msg_002"
}
```

### Audio buffer cleared (input\_audio\_buffer.cleared)

Returned when the client clears the input audio buffer with `input_audio_buffer.clear`.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_1314",
    "type": "input_audio_buffer.cleared"
}
```

### Response output item added (response.output\_item.added)

Returned when a new item is created during response generation.

* `output_index` `int`<br />The index of the output item in the response.
* `item` `object`<br />The output item.

  <Expandable>
    * `id` `string`<br />The item ID.
    * `object` `string`<br />Always `realtime.item`.
    * `type` `string`<br />The item type; currently only `message`.
    * `status` `string`<br />The item status: `completed`, `incomplete`, `in_progress`.
    * `role` `string`<br />The role of the item (message items only): `user`, `assistant`, `system`.
    * `content` `array`<br />The message content. A `system` item supports `input_text`; a `user` item supports `input_text` and `input_audio`; an `assistant` item supports text content.
  </Expandable>

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_3334",
    "type": "response.output_item.added",
    "response_id": "resp_001",
    "output_index": 0,
    "item": {
        "id": "msg_007",
        "object": "realtime.item",
        "type": "message",
        "status": "in_progress",
        "role": "assistant",
        "content": []
    }
}
```

### Response output item done (response.output\_item.done)

Returned when an item is completed. Also emitted when the response is `interrupted`, `incomplete`, or `cancelled`.

* `output_index` `int`<br />The index of the output item in the response.
* `item` `object`<br />The output item (same structure as in `response.output_item.added`).

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_3536",
    "type": "response.output_item.done",
    "response_id": "resp_001",
    "output_index": 0,
    "item": {
        "id": "msg_007",
        "object": "realtime.item",
        "type": "message",
        "status": "completed",
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "Sure, I can help with that."
            }
        ]
    }
}
```

### Response content part added (response.content\_part.added)

Returned when a new content part is added to an assistant message item during response generation.

* `response_id` `string`<br />The response ID.
* `item_id` `string`<br />The corresponding item ID.
* `content_index` `int`<br />The index of the content part in the item's content array.
* `output_index` `int`<br />The index of the output item in the response.
* `part` `object`

  <Expandable>
    * `type` `string`<br />The content type: `text`, `audio`, or `thinking`.
    * `audio` `string`<br />Base64-encoded audio data (present when `type=audio`).
    * `text` `string`<br />The generated text (present when `type=text`).
    * `thinking` `string`<br />The generated reasoning content (present when `type=thinking`).
    * `transcript` `string`<br />The transcript of the audio (present when `type=audio`).
  </Expandable>

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_3738",
    "type": "response.content_part.added",
    "response_id": "resp_001",
    "item_id": "msg_007",
    "output_index": 0,
    "content_index": 0,
    "part": {
        "type": "text",
        "text": ""
    }
}
```

### Response content part done (response.content\_part.done)

Returned when a content part is completed. Also emitted when the corresponding response is `interrupted`, `incomplete`, or `cancelled`.

* `response_id` `string`<br />The response ID.
* `item_id` `string`<br />The corresponding item ID.
* `content_index` `int`<br />The index of the content part in the item's content array.
* `output_index` `int`<br />The index of the output item in the response.
* `part` `object`<br />Same structure as in `response.content_part.added`.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_3940",
    "type": "response.content_part.done",
    "response_id": "resp_001",
    "item_id": "msg_007",
    "output_index": 0,
    "content_index": 0,
    "part": {
        "type": "text",
        "text": "Sure, I can help with that."
    }
}
```

### Response created (response.created)

Returned when a new Response is created. This is the first event of response creation, with an initial status of `in_progress`.

* `id` `string`<br />The unique ID of the response.
* `object` `string`<br />The object type, `realtime.response`.
* `status` `string`<br />The response status (`in_progress`, `completed`, `cancelled`, `failed`, `incomplete`).
* `output` `list`<br />The list of output items generated by the response.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_3132",
    "type": "response.created",
    "response": {
        "id": "resp_001",
        "object": "realtime.response",
        "status": "in_progress",
        "status_details": null,
        "output": []
    }
}
```

### Response done (response.done)

Returned when the Response finishes streaming. Always emitted, regardless of the final status. The Response object includes all output items but omits the raw audio data.

* `id` `string`<br />The unique ID of the response.
* `object` `string`<br />The object type, `realtime.response`.
* `status` `string`<br />The final status (`completed`, `cancelled`, `failed`, `incomplete`).
* `output` `list`<br />The list of output items generated by the response.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "event_id": "event_bcd",
    "type": "response.done",
    "response": {
        "id": "resp_001",
        "object": "realtime.response",
        "status": "completed",
        "status_details": null,
        "output": [
            {
                "id": "msg_006",
                "object": "realtime.item",
                "type": "message",
                "status": "completed",
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Sure, how can I assist you today?"
                    }
                ]
            }
        ]
    }
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.