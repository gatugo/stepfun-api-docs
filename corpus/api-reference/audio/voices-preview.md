> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Preview cloned voice

Generate a preview audio clip from a reference audio file (WAV or MP3) to quickly verify the voice cloning result. This endpoint **does not create a permanent voice asset** — it is only for previewing.

### Endpoint

`POST https://api.stepfun.ai/v1/audio/voices/preview`

<Note>
  For Step Plan, use `POST https://api.stepfun.ai/step_plan/v1/audio/voices/preview`
</Note>

### Request parameters

* `model` `string` ***required*** <br /> Model to use for cloning. Supports `stepaudio-2.5-tts`.

* `file_id` `string` ***required*** <br /> Reference audio file ID. Obtain via [file upload](/docs/en/api-reference/files/create); set `purpose` to `storage`.

* `text` `string` ***optional*** <br /> Transcript of the reference audio. If omitted, automatic speech recognition is used. For best results, we recommend providing the transcript.

* `sample_text` `string` ***required*** <br /> Text to synthesize for the preview. Recommended length: under 50 characters.

* `response_format` `string` ***optional*** <br /> Audio format for the response. Options: `wav`, `mp3`, `flac`, `opus`, `pcm`. Default: `mp3`.

* `speed` `float` ***optional*** <br /> Speaking rate. Range: 0.5–2.0. Default: 1.0.

* `volume` `float` ***optional*** <br /> Volume level. Range: 0.1–2.0. Default: 1.0.

* `instruction` `string` ***optional*** <br /> Global natural-language guidance for the `stepaudio-2.5-tts` model. Sets the overall emotional tone and character for the audio. Max length: 200 characters.

* `sample_rate` `integer` ***optional*** <br /> Sample rate in Hz. Options: 8000, 16000, 22050, 24000, 48000. Default: 24000. Higher values produce better quality but larger files.

* `pronunciation_map` `object array` ***optional*** <br /> Custom pronunciation rules for specific characters or symbols.
  * `tone` `string` ***required*** <br /> Pronunciation mapping separated by `/`. Example: `["word/wɜːrd"]`.

* `markdown_filter` `bool` ***optional*** <br /> Whether to enable Markdown filtering for the input text.

### Response

* `sample_text` `string` <br /> The text used for the preview audio.

* `sample_audio` `string` <br /> Preview audio in base64 format (WAV). Convert to a file for playback.

* `request_id` `string` <br /> Unique identifier for this request.

### Example

<Tabs>
  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl -L 'https://api.stepfun.ai/v1/audio/voices/preview' \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $STEP_API_KEY" \
    -d '{
        "file_id": "file-Ckyl3cV09A",
        "model": "stepaudio-2.5-tts",
        "text": "StepFun intelligence, amplifying every possibility tenfold",
        "sample_text": "Nice weather today",
        "instruction": "Gentle tone, slightly slow pace"
    }'
    ```
  </Tab>
</Tabs>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.