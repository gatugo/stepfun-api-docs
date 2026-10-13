> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# StepAudio 3 TTS

StepAudio 3 TTS produces natural, human-like speech from text, with fine-grained control over delivery and low-latency streaming. [Technical report](https://arxiv.org/abs/2609.12945) · [Voice Studio](https://audio.stepfun.ai/)

## Model information

| Item | Details |
| :- | :- |
| Model ID | `stepaudio-3-tts` |
| Input | Text |
| Output | Speech |
| Billing | \$0.36 / 10,000 characters |
| Voice cloning | \$1.50 / voice |

## Capabilities

* **Human-level speaking performance**: in timbre, intonation, rhythm, and breath, the model follows natural human speech—laughter, lip smacks, hesitation, stutters, repetition, self-correction—and shifts emotion and tone to fit the context, sounding like a person rather than a synthesized clip.
* **Ultra-low-latency streaming**: it outputs while generating, so playback can start before a full sentence is synthesized—ideal for real-time conversation and voice assistants.

Suitable for real-time conversation, voice assistants, and high-expressiveness content generation.

## API endpoints

<Columns cols={2}>
  <Card title="Non-streaming synthesis" href="/docs/en/api-reference/audio/create-audio">
    `POST /v1/audio/speech`
  </Card>

  <Card title="Streaming synthesis" href="/docs/en/api-reference/audio/ws-audio">
    `WebSocket /v1/realtime/audio`
  </Card>
</Columns>

## Related resources

<Columns cols={2}>
  <Card title="Audio models overview" icon="arrow-left" href="/docs/en/guides/models/audio">
    Back to the Audio 3 model overview.
  </Card>

  <Card title="StepAudio 3 Gen" icon="wand-magic-sparkles" href="/docs/en/guides/models/stepaudio-3-gen">
    Unified audio generation—voice, SFX, ambience, and music.
  </Card>

  <Card title="Full pricing details" icon="receipt" href="/docs/en/guides/pricing/details">
    Billing rules for all speech, text, and image models.
  </Card>

  <Card title="Voice list" icon="microphone" href="/docs/en/guides/developer/tts#system-voice-id-list">
    Official voices and parameter notes.
  </Card>

  <Card title="Voice Studio" icon="play" href="https://audio.stepfun.ai/">
    Try the full capabilities of StepAudio 3 TTS online.
  </Card>
</Columns>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.