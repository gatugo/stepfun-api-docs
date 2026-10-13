> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Audio Generation

Generate a wide range of sound elements—voices, sound effects, ambient sound, and background music—in a unified way from text descriptions.

## Endpoint

`POST https://api.stepfun.ai/v1/audio/generate`

## Request Headers

* `Content-Type` `string` ***required***<br />Fixed as `application/json`.
* `Authorization` `string` ***required***<br />Authentication token in the format `Bearer $STEP_API_KEY`.

## Request Parameters

* `model` `string` ***required***<br />Model name. Currently supports `stepaudio-3-gen-preview`.

* `task` `string` ***required***<br />Task type. Currently only `text_to_audio` is supported: design a voice with a natural-language description and generate voices, sound effects, background music, and other sound elements. When using this task, at least one of `scripts` or `instruction` is required; `roles` is optional.

* `roles` `array` ***optional***<br />The roles and voice descriptions used for generation. All `name` and `description` values together can be at most 500 characters.

  <Expandable>
    * `name` `string` ***optional***<br />A custom role or voice name, e.g. "Lead".
    * `description` `string` ***optional***<br />A custom role or voice description, e.g. "A man in his twenties, a slightly husky voice, with full breath when singing." `name` and `description` must both be provided or both left empty.
  </Expandable>

* `scripts` `array` ***optional***<br />The lines, sound-effect, or background-music descriptions to generate, at most 1,000 characters in total. A spoken line specifies its speaker via `speaker` and can use `()` to describe tone, style, and emotion; wrap sound-effect and background-music descriptions in `[]`, in which case `speaker` can be omitted.

  <Expandable>
    * `speaker` `string` ***optional***<br />The `roles.name` the line belongs to. Can be omitted for pure sound-effect or BGM descriptions.
    * `text` `string` ***required***<br />A spoken line, sound effect, or BGM description.
  </Expandable>

* `instruction` `string` ***optional***<br />Global natural-language guidance used to set the environment, BGM, and emotional tone. Up to 500 characters.

* `response_format` `string` ***optional***<br />Returned audio format. Supports `wav`, `mp3`, `flac`, `opus`, and `pcm`.

* `speed` `number` ***optional***<br />Speech speed. Range: 0.5 to 2.

* `volume` `number` ***optional***<br />Volume. Range: 0.1 to 2.0.

* `sample_rate` `integer` ***optional***<br />Sampling rate. Supports `8000`, `16000`, `22050`, `24000`, and `48000`.

* `pronunciation_map` `object` ***optional***<br />Pronunciation replacement rules.

* `text_normalization` `string` ***optional***<br />Text normalization strategy. Supports `standard` and `enhanced`.

* `stream_format` `string` ***optional***<br />Return mode. Default `audio`: `audio` returns the generated audio directly; `sse` continuously returns Base64-encoded audio chunks via Server-Sent Events.

* `return_url` `boolean` ***optional***<br />Whether to return the audio URL.

<Note>
  The reference-voice task (`reference_to_audio`), which synthesizes audio using an official or cloned voice, is not yet available; it will be added to this page once supported.
</Note>

## Request Example

### Audio generation

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
curl --location 'https://api.stepfun.ai/v1/audio/generate' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer '"$STEP_API_KEY" \
  --data '{
    "model": "stepaudio-3-gen-preview",
    "task": "text_to_audio",
    "roles": [
      { "name": "Ground crew", "description": "A man around thirty, crisp and efficient voice, fast pace, focused on apron work, raising his volume slightly to be heard over the engine noise" },
      { "name": "Captain", "description": "A middle-aged man, voice coming over the radio with the electronic compression and background static typical of aviation comms, calm and professional" },
      { "name": "Tower", "description": "A woman, voice also over the radio, clear and articulate with slight distortion, calmly issuing instructions" }
    ],
    "scripts": [
      { "text": "[The steady high-pitched whine of an airliner APU, mixed with the low rumble of a tug engine]" },
      { "speaker": "Ground crew", "text": "(into the headset, raising volume over the noise) Left engine intake check complete, chocks removed, ready for pushback." },
      { "speaker": "Captain", "text": "(radio voice, compressed and distorted) Roger, requesting pushback approval, watching for ground signals." },
      { "text": "[The radio clicks on with a burst of static, carrying a voice over the current]" },
      { "speaker": "Tower", "text": "(radio voice, calm) Pushback approved, runway two-three right, surface wind zero-nine-zero at three knots, have a good flight." },
      { "speaker": "Ground crew", "text": "(waving the marshalling wands, responding loudly) Understood, tug starting pushback, mind the left wingtip clearance!" }
    ],
    "instruction": "A nighttime airport apron; an airliner is running its final ground checks before departure",
    "response_format": "mp3"
  }'
```

## Limits and Compatibility

* The `instruction` and `roles` fields are limited to 500 characters, and the `scripts` field to 1,000 characters.
* `stepaudio-3-gen-preview` does not support the `voice`, `voice_label`, or `timestamp` parameters.
* The endpoint returns HTTP 400 when a length limit is exceeded or an unsupported parameter is passed.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.