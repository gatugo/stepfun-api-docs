> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# StepAudio 3 Gen

StepAudio 3 Gen creates comprehensive audio content from natural language. Describe roles, timbre, and emotion, and it generates expressive, controllable voice—then adds sound effects, ambient sound, background music, and singing, orchestrated into a single finished clip. [Technical report](https://arxiv.org/abs/2609.12945) · [More demos](https://static.stepfun.com/blog/stepaudio3/gen/) · [Voice Studio](https://audio.stepfun.ai/)

## Model information

| Item | Details |
| :- | :- |
| Model ID | `stepaudio-3-gen-preview` |
| Input | Text, audio, role and script descriptions |
| Output | Unified audio |
| Billing | Free (limited time) |

<Note>
  `stepaudio-3-gen-preview` is the model name used during the free-trial period. When the free trial ends, this preview version will be retired and a formal paid version added.
</Note>

## Capabilities

* **Fine-grained voice design and control**: control multi-role lines, timbre, speaking manner, emotion, and dialect through natural language, along with paralinguistic features like laughter, breathing, and pauses. Describe several roles and their interactions in one instruction, and the model organizes the dialogue and transitions for coherent, expressive results.
* **All-element generation and temporal orchestration**: beyond voice, it also generates sound effects, ambient sound, background music, and singing, and lets you specify where and in what order each element appears—coordinated generation and seamless clip stitching for complete audio productions.

## Use cases

* **Professional content production**: for film, games, animation, radio drama, and audiobooks—design each role's timbre and delivery to quickly produce character dubbing and multi-role dialogue, plus the ambient sound, sound effects, and background music you need, cutting the coordination and post-production cost of traditional workflows.
* **Short video and self-media**: for creators' short-video dubbing—no professional software or audio experience required; a single natural-language description generates style-controllable voiceover that matches the video, with background music and sound effects added on demand.

## API endpoint

<Card title="Audio Generation API" href="/docs/en/api-reference/audio/generate">
  `POST /v1/audio/generate`
</Card>

## Related resources

<Columns cols={2}>
  <Card title="Audio models overview" icon="arrow-left" href="/docs/en/guides/models/audio">
    Back to the Audio 3 model overview.
  </Card>

  <Card title="StepAudio 3 TTS" icon="microphone" href="/docs/en/guides/models/stepaudio-3-tts">
    Human-level text-to-speech from the same series.
  </Card>

  <Card title="Full pricing details" icon="receipt" href="/docs/en/guides/pricing/details">
    Billing rules for all speech, text, and image models.
  </Card>

  <Card title="Voice Studio" icon="play" href="https://audio.stepfun.ai/">
    Try StepAudio 3 Gen online.
  </Card>
</Columns>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.