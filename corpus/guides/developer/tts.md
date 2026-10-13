> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Voice interaction developer guide

StepFun provides developers with voice interaction models that support audio generation and [voice cloning](/docs/en/api-reference/audio/create-voice). By integrating these models, applications can extend beyond standard large language model understanding and enable voice interaction.

## Quick Start

### Quickly Generate an Audio Clip

Copy the following code to quickly generate an audio file.

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
curl --location 'https://api.stepfun.ai/v1/audio/speech' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $STEP_API_KEY" \
--data '{
   "model":"stepaudio-2.5-tts",
   "input":"StepFun is building the next generation of AGI.",
   "voice":"lively-girl"
}'\
--output "step.mp3"
```

<div id="supported-voices" />

## Voice Recommendations by Scenario

StepFun offers a set of recommended voices across seven common scenarios. You can preview them here and call them via the API.
We also recommend [voice cloning](/docs/en/api-reference/audio/create-voice) with `stepaudio-2.5-tts` to create custom voices: about 3 seconds of reference audio is enough, and cloned voices keep full natural-language delivery control at no additional cost.

### 1. Marketing

Marketing scenarios require voices with charisma, persuasiveness, and warmth that can effectively convey product value and inspire purchase intent. Our TTS delivers full emotional expression, building trust and professionalism to make marketing content more compelling.

| Supported Models | Voice Name | Voice ID | Audio Samples |
| :- | :- | :- | :- |
| stepaudio-2.5-tts | Lively Breezy | livelybreezy-female | <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764227859773_6r0lga.wav" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764227873237_xbptdq.wav" target="_blank" rel="noopener noreferrer">Sample 2</a> |

### 2. Customer Service

Customer service scenarios require voices that are warm, patient, and professional, capable of calming users and providing clear solutions.

| Supported Models | Voice Name | Voice ID | Audio Samples |
| :- | :- | :- | :- |
| stepaudio-2.5-tts | Elegant Gentle | elegantgentle-female | <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764232963968_2lpzrh.wav" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764232975950_nb22zj.wav" target="_blank" rel="noopener noreferrer">Sample 2</a> |
| stepaudio-2.5-tts | Lively Breezy | livelybreezy-female | <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764233092953_7uj9hs.wav" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764233081037_2uelez.wav" target="_blank" rel="noopener noreferrer">Sample 2</a> |

### 3. Audiobook

Audiobooks require voices that are expressive and emotionally engaging, capable of vividly bringing different characters and story atmospheres to life. Our TTS stands out with its delicate emotional expression and versatile vocal styles, enabling listeners to fully immerse themselves in the world of the story.

| Supported Models | Voice Name | Voice ID | Audio Samples |
| :- | :- | :- | :- |
| stepaudio-2.5-tts | Lively Girl | lively-girl | <a href="https://static-openapi.stepfun.ai/static/platform-docs/resource/lively-girl_In.mp3" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.ai/static/platform-docs/resource/lively-girl_Years.mp3" target="_blank" rel="noopener noreferrer">Sample 2</a> |

### 4. Emotional Companionship

Emotional companionship requires voices that are warm, gentle, and empathetic, capable of providing users with comfort and psychological support. Our TTS features delicate, soothing voice timbres with strong emotional expressiveness, helping you create a safe and comforting interaction environment for users.

| Supported Models | Voice Name | Voice ID | Audio Samples |
| :- | :- | :- | :- |
| stepaudio-2.5-tts | Soft-spoken Gentleman | soft-spoken-gentleman | <a href="https://static-openapi.stepfun.ai/static/platform-docs/resource/Soft-spoken-Gentleman-1.wav" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.ai/static/platform-docs/resource/Soft-spoken-Gentleman-2.wav" target="_blank" rel="noopener noreferrer">Sample 2</a> |
| stepaudio-2.5-tts | Elegant Gentle | elegantgentle-female | <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764230170888_rpysp8.wav" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764230185710_01rt1x.wav" target="_blank" rel="noopener noreferrer">Sample 2</a> |
| stepaudio-2.5-tts | Lively Breezy | livelybreezy-female | <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764230220618_qbsx4o.wav" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764230236362_tfyy2l.wav" target="_blank" rel="noopener noreferrer">Sample 2</a> |

### 5. Voice Assistant

Voice assistant scenarios require voices that are clear, natural, and efficient, capable of accurately understanding and responding to user commands. Our TTS features natural prosody and full emotional expression, making your voice assistant both professional and approachable.

| Supported Models | Voice Name | Voice ID | Audio Samples |
| :- | :- | :- | :- |
| stepaudio-2.5-tts | Elegant Gentle | elegantgentle-female | <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764228832095_29ybp3.wav" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764228840760_7lfeif.wav" target="_blank" rel="noopener noreferrer">Sample 2</a> |
| stepaudio-2.5-tts | Lively Breezy | livelybreezy-female | <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764228850379_g5udri.wav" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764228867575_iogyx5.wav" target="_blank" rel="noopener noreferrer">Sample 2</a> |

### 6. Video Dubbing

Video dubbing requires voices that are expressive, rhythmic, and visually evocative, capable of blending seamlessly with visual content. Our TTS excels in precise emotional delivery and fine-grained speech rhythm control, enhancing the impact and overall appeal of your videos.

| Supported Models | Voice Name | Voice ID | Audio Samples |
| :- | :- | :- | :- |
| stepaudio-2.5-tts | Vibrant Youth | vibrant-youth | <a href="https://static-openapi.stepfun.ai/static/platform-docs/resource/vibrant-youth_Every.mp3" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.ai/static/platform-docs/resource/vibrant-youth_This.mp3" target="_blank" rel="noopener noreferrer">Sample 2</a> |
| stepaudio-2.5-tts | Magnetic-voiced Male | magnetic-voiced-male | <a href="https://static-openapi.stepfun.ai/static/platform-docs/resource/Magnetic-voiced-Male-1.wav" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.ai/static/platform-docs/resource/Magnetic-voiced-Male-2.wav" target="_blank" rel="noopener noreferrer">Sample 2</a> |

### 7. Education & Training

Education and training scenarios require voices that are clear, accurate, and inspiring, capable of effectively conveying knowledge and sparking learning interest. Our TTS excels at capturing the vocal characteristics of instructors across different emotional states.

| Supported Models | Voice Name | Voice ID | Audio Samples |
| :- | :- | :- | :- |
| stepaudio-2.5-tts | Elegant Gentle | elegantgentle-female | <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764228058073_102wb4.wav" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764228049743_8dc93a.wav" target="_blank" rel="noopener noreferrer">Sample 2</a> |
| stepaudio-2.5-tts | Lively Breezy | livelybreezy-female | <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764228115572_zfgvsz.wav" target="_blank" rel="noopener noreferrer">Sample 1</a> · <a href="https://static-openapi.stepfun.com/static/platform-docs/resource/1764228129774_s17gwn.wav" target="_blank" rel="noopener noreferrer">Sample 2</a> |

## System Voice ID List

| Voice Name | Voice ID | Supported Models | Recommended Use Cases |
| :- | :- | :- | :- |
| Vibrant Youth | vibrant-youth | stepaudio-2.5-tts | Audiobook, video dubbing |
| Lively Girl | lively-girl | stepaudio-2.5-tts | Audiobook, video dubbing |
| Soft-spoken Gentleman | soft-spoken-gentleman | stepaudio-2.5-tts | Emotional companionship, audiobook |
| Magnetic-voiced Male | magnetic-voiced-male | stepaudio-2.5-tts | Audiobook, video dubbing |
| Confident Male | zixinnansheng | stepaudio-2.5-tts | Audiobook, emotional companionship, education, marketing |
| Elegant Gentle | elegantgentle-female | stepaudio-2.5-tts | Customer service, voice-over, education, emotional companionship |
| Lively Breezy | livelybreezy-female | stepaudio-2.5-tts | Emotional companionship, customer service, education, marketing |

## Output Format

StepFun TTS models support audio output in `wav`, `mp3`, `flac`, `opus`, and `pcm` formats. The default format is `mp3`. You can choose the format that best suits your use case.

## Output Languages

StepFun TTS models support generating audio in Chinese, English, mixed Chinese-English, and Japanese.

## FAQ

**Do I own the audio I generate?**

Yes. You own the audio you create. However, we recommend informing your end users that the audio was generated by AI so they are aware of its nature.

**How do I adjust the volume of the generated audio?**

You can set the `volume` parameter when calling the generation API. Valid values range from 0.1 to 2.0, representing 10% volume to 200% volume.

**How do I adjust the speaking rate of the generated audio?**

You can set the `speed` parameter when calling the generation API. Valid values range from 0.5 to 2.0, representing half-speed to double-speed.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.