> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Create cloned voice

Clone a voice from a previously uploaded WAV or MP3 file so it can be used for [TTS audio generation](/docs/en/api-reference/audio/create-audio) or [Realtime voice conversation](/docs/en/api-reference/realtime/chat).

<Warning>
  Cloned voices can be used only with `language` omitted, `zh`, or `en`. Calling Text-to-Speech with any other language and a cloned voice returns `400 input_invalid` (`voice <voice_id> does not support language <language>`). For other languages, use a system voice that supports the language (see [Get system voices](/docs/en/api-reference/audio/system-voices)).
</Warning>

### Endpoint

`POST https://api.stepfun.ai/v1/audio/voices`

### Request parameters

* `model` `string` ***required***<br /> Cloning model. Use `stepaudio-2.5-tts` to clone a voice for use with StepAudio 2.5 TTS or Realtime.

* `text` `string` ***optional***<br /> Transcript of the source audio file. If omitted, automatic speech recognition is used. For best results, we recommend providing the transcript.

* `file_id` `string` ***required*** <br /> File ID of the source audio used for cloning. Obtain the ID via [file upload](/docs/en/api-reference/files/create); set `purpose` to `storage`. Supported formats: mp3, wav. Audio length should be 5–10 seconds.

* `sample_text` `string` **optional**<br /> Text (max 50 characters) used to create a preview clip.

### Response

* `id` `string`<br /> Voice ID for subsequent audio generation.

* `object` `string`<br /> Object type, always `audio.voice`.

* `duplicated` `boolean`<br /> Indicates the request was duplicated (returned on repeated calls).

* `sample_text` `string`<br /> Text used for the preview audio.

* `sample_audio` `string` <br /> Preview audio in base64 (wav). Convert to a file to play.

### Example

<Tabs>
  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl -L 'https://api.stepfun.ai/v1/audio/voices' \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $STEP_API_KEY" \
    -d '{
        "file_id":"file-Ckyl3cV09A",
        "model":"stepaudio-2.5-tts",
        "text":"StepFun intelligence, 10x possibilities for everyone.",
        "sample_text":"Nice weather today"
    }'
    ```
  </Tab>
</Tabs>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.