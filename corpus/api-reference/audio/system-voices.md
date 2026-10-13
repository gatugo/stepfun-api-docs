> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Get system voices

## Overview

Use this API to retrieve the system default voices available for a given model. The response includes a list of voice IDs and detailed information (name, description, recommended scenarios) for each voice.

When exposed to an agent, the agent can use this catalog to pick the most appropriate voice for a given scenario.

<Info>
  This endpoint is the authoritative source for which voices your account can actually use. Voice IDs from other sources are rejected — see [Notes](#notes).
</Info>

## Request

### Method

`GET`

### Endpoint

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
GET https://api.stepfun.ai/v1/audio/system_voices
```

### Query parameters

| Parameter | Type | Required | Allowed values | Description |
| - | - | - | - | - |
| model | string | Yes | `stepaudio-2.5-tts` | The TTS model whose system voices to query. Any other value — including `stepaudio-2.5-realtime` — returns `400 invalid model`. |

Omitting `model` returns `400` with `model is required`.

### Request example

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
curl "https://api.stepfun.ai/v1/audio/system_voices?model=stepaudio-2.5-tts" \
  -H "Authorization: Bearer $STEPFUN_API_KEY"
```

## Response

### Format

`JSON`

### Response fields

| Field | Type | Description |
| - | - | - |
| voices | array\[string] | List of system voice IDs available under this model. |
| voices-details | object | Details per voice, keyed by voice ID. |
| voices-details.\<id>.voice-name | string | Voice display name. May be empty for some voices. |
| voices-details.\<id>.voice-description | string | Voice description, including gender and character. |
| voices-details.\<id>.recommended\_scene | string | Recommended use cases, separated by `、`. |

### Response example

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "voices": [
    "elegantgentle-female",
    "lively-girl",
    "livelybreezy-female",
    "magnetic-voiced-male",
    "soft-spoken-gentleman",
    "vibrant-youth",
    "zixinnansheng"
  ],
  "voices-details": {
    "elegantgentle-female": {
      "voice-name": "气质温婉",
      "voice-description": "女，真诚温柔，亲和力强，给人安全感",
      "recommended_scene": "客服与业务办理、口播（解说、新闻）、教育与培训、情感陪伴"
    },
    "lively-girl": {
      "voice-name": "Lively Girl",
      "voice-description": "女，英文音色，亲和感，有活力",
      "recommended_scene": "有声书、视频配音、语音助手"
    },
    "livelybreezy-female": {
      "voice-name": "活力轻快",
      "voice-description": "女，音色具有感染力、说服力和亲和力，有活力",
      "recommended_scene": "情感陪伴、教育与培训、营销"
    },
    "magnetic-voiced-male": {
      "voice-name": "Magnetic-voiced Male",
      "voice-description": "男，英文音色，强烈的沉稳厚重感",
      "recommended_scene": "有声书、视频配音"
    },
    "soft-spoken-gentleman": {
      "voice-name": "Soft-spoken Gentleman",
      "voice-description": "男，英文音色，沉稳温柔，给人安全感",
      "recommended_scene": "情感陪伴、有声书"
    },
    "vibrant-youth": {
      "voice-name": "Vibrant Youth",
      "voice-description": "男，英文音色，温柔亲和",
      "recommended_scene": "有声书、视频配音、语音助手"
    },
    "zixinnansheng": {
      "voice-name": "自信男声",
      "voice-description": "男，真诚亲和，有活力",
      "recommended_scene": "有声书、情感陪伴、教育与培训、营销"
    }
  }
}
```

<Note>
  `voice-description` and `recommended_scene` are returned in Chinese as-is from the service, and `voice-name` is Chinese for voices that do not have an English name. Use the voice ID (the key under `voices-details`) when calling the TTS API. See the table below for an English reference.
</Note>

### Voice reference

The same seven voices in English, in the order returned by the API. Four of them (`lively-girl`, `magnetic-voiced-male`, `soft-spoken-gentleman`, `vibrant-youth`) are purpose-built English voices.

| Voice ID | Voice | Recommended use cases |
| :- | :- | :- |
| `elegantgentle-female` | Elegant, gentle female voice — sincere and reassuring | Customer service, voice-over, education, emotional companionship |
| `lively-girl` | Bright, lively female voice (English) | Audiobook, video dubbing, voice assistant |
| `livelybreezy-female` | Light, breezy female voice — engaging and persuasive | Emotional companionship, education, marketing |
| `magnetic-voiced-male` | Deep, magnetic male voice (English) | Audiobook, video dubbing |
| `soft-spoken-gentleman` | Calm, gentle male voice (English) | Emotional companionship, audiobook |
| `vibrant-youth` | Warm, approachable young male voice (English) | Audiobook, video dubbing, voice assistant |
| `zixinnansheng` | Confident male voice — sincere, warm, energetic | Audiobook, emotional companionship, education, marketing |

## Notes

* Each ID in `voices` has a matching entry in `voices-details`; use the voice ID to look up its details.
* Languages other than `zh` / `en` are supported only by a subset of system voices; the exact list is whatever this endpoint returns. Cloned voices do not support languages other than `zh` / `en`.
* `recommended_scene` is informational only — pick the voice that best fits your use case.
* Only the voice IDs returned by this endpoint (or one of your own cloned voice IDs) are accepted by the TTS and Realtime APIs. Any other value is rejected with `400 voice_id_invalid`. To list your cloned voices, see [List cloned voices](/docs/en/api-reference/audio/list-voice).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.