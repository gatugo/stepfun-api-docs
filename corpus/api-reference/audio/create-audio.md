> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Text-to-Speech

This API allows you to generate audio using our Text-to-Speech (TTS) model.

### Endpoint

`POST https://api.stepfun.ai/v1/audio/speech`

<Note>
  For Step Plan, use `POST https://api.stepfun.ai/step_plan/v1/audio/speech`
</Note>

### Request body

* `model` `string` ***required***<br />The ID of the model to use. Currently supports `stepaudio-3-tts` and `stepaudio-2.5-tts`.

  <Note>The `step-tts-vivid` model name is deprecated but existing user requests will continue to be supported.</Note>

* `input` `string` ***required***<br />The text to generate audio for. The maximum length is 1,000 characters. When using `stepaudio-2.5-tts` or `stepaudio-3-tts`, content inside parentheses `()` will be treated as instructions and will not be spoken. If you need the text itself to be spoken, do not wrap it in parentheses.

* `voice` `string` ***required***<br />The voice to use for generation. Supports both [official voices](/docs/en/guides/developer/tts#system-voice-id-list) and custom cloned voices.

* `language` `string` ***optional***<br />Target language; defaults to English when omitted. Supported values: `zh`, `en`, `ja`, `ko`, `fr`, `es`. Japanese, Korean, French, and Spanish are in preview.

* `response_format` `string` ***optional***<br />The audio format for the returned output. Supported formats: `wav`, `mp3`, `flac`, `opus`, `pcm`. Default: `mp3`.

* `speed` `float` ***optional***<br />The speed of the generated audio. Range: 0.5 to 2.0. Default: 1.0. 0.5 means half speed.

* `volume` `float` ***optional***<br />The volume of the generated audio. Range: 0.1 to 2.0. Default: 1.0. 0.1 reduces the volume to 10%; 2.0 increases it to 200%.

* `instruction` `string` ***optional***<br />Global natural-language guidance for the `stepaudio-2.5-tts` and `stepaudio-3-tts` models. Used to set the overall emotional tone, character persona, etc. for the entire audio. Maximum length: 200 characters for `stepaudio-2.5-tts`, 500 characters for `stepaudio-3-tts`.

* `sample_rate` `integer` ***optional***<br />The sampling rate. Supports `8000`, `16000`, `22050`, `24000`, `48000`. Default: `24000`. Higher rates improve audio quality but increase file size. `48000` was added in recent iterations.

* `pronunciation_map` `object array` ***optional*** <br />Defines a pronunciation rule to annotate or override the reading of specific characters or symbols. In Chinese text, tones are represented by numbers: 1 for the first tone, 2 for the second tone, 3 for the third tone, 4 for the fourth tone, and 5 for the neutral tone.
  * `tone` `string` ***required*** <br /> Specific pronunciation mapping rules, separated by `/`. Example: `["LOL/laugh out loudly"]`.

* `stream_format` `string` ***optional*** <br /> Streaming return mode. By default, audio is returned directly. Supported values: `sse`, `audio`. Default: `audio`. When `sse` is specified, audio is returned via Server-Sent Events (SSE) with the following data packet format:

  ```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
  data: {"type":"speech.audio.delta","audio":"<BASE64-encoded audio chunk>"}

  data: {"type":"speech.audio.delta","audio":"<BASE64-encoded audio chunk>"}

  data: {"type":"speech.audio.done","audio":""}

  data: [DONE]
  ```

  Event types:

  * `speech.audio.delta`: Audio chunk. The `audio` field contains the BASE64-encoded binary data of this chunk; concatenate all chunks to form the complete audio.
  * `speech.audio.done`: Generation complete; `audio` is an empty string.
  * `speech.audio.error`: An error occurred during generation.

* `markdown_filter` `bool` ***optional*** <br /> Whether to enable Markdown filtering.

* `return_url` `bool` ***optional*** <br /> Only effective for non-streaming requests. When set to `true`, returns a URL to the audio file instead of the binary audio stream. The URL is valid for 12 hours.

### Response

By default the response body is the synthesized audio file (a binary stream).

When `return_url=true`, the response is JSON instead:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "created": 1786678674,
  "data": {
    "url": "https://.../xxxx.mp3"
  }
}
```

* `created` `int`<br />Response creation time, as a Unix timestamp in seconds.
* `data.url` `string`<br />Download URL for the synthesized audio file, valid for 12 hours.

### Examples

<Tabs>
  <Tab title="python">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    from pathlib import Path
    from openai import OpenAI

    speech_file_path = Path(__file__).parent / "step-tts.mp3"

    client = OpenAI(
        api_key="YOUR_STEP_API_KEY",
        base_url="https://api.stepfun.ai/v1"
    )
    response = client.audio.speech.create(
        model="stepaudio-2.5-tts",
        voice="zixinnansheng",
        # Max length <= 1000 characters. Content in () is treated as instructions (not spoken).
        input="(cold laugh) Do you think our technology at StepFun is a joke?!",
        extra_body={
            "volume": 1.0,  # volume is in extra_body
            # Global instruction (max 200 characters)
            "instruction": "Extremely angry tone, strong pressure, slightly fast pace",
            "pronunciation_map": {
                "tone": [
                    "LOL/laugh out loudly"
                ]
            }
        }
    )
    response.stream_to_file(speech_file_path)
    ```
  </Tab>

  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl --location 'https://api.stepfun.ai/v1/audio/speech' \
      --header 'Content-Type: application/json' \
      --header "Authorization: Bearer $STEP_API_KEY" \
      --data '{
        "model": "stepaudio-2.5-tts",
        "input": "StepFun is building the next generation of AGI.",
        "voice": "zixinnansheng"
      }' \
      --output "step.mp3"
    ```
  </Tab>
</Tabs>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.