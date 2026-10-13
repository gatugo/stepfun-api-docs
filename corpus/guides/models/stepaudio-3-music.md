> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# StepAudio 3 Music

From a natural-language description, lyrics, vocals, or reference audio, the model covers the full arc of music creation—from a rough idea to a finished song to intelligent scoring. [Technical report](https://arxiv.org/abs/2609.16034) · [View more demos](https://static.stepfun.com/blog/stepaudio3/music/) · [Voice Studio](https://audio.stepfun.ai/)

## Model information

| Item | Details |
| :- | :- |
| Model ID | `stepaudio-3-music-preview` |
| Input | Natural language, lyrics, vocals, or reference audio |
| Output | Music |
| Protocol | HTTP asynchronous task |
| Billing | Free (limited time) |

<Note>
  `stepaudio-3-music-preview` is the model name used during the free-trial period. When the free trial ends, this preview version will be retired and a formal paid version added.
</Note>

## Model architecture

StepMusic uses a unified architecture for music understanding and high-fidelity generation. Trained on large-scale song and music-understanding data, it learns melody, harmony, rhythm, structure, timbre, and vocal information through a self-developed unsupervised music-representation encoder, and completes the final audio synthesis with generation and rendering modules.

* **Music semantic understanding**: maps text descriptions, lyrics, and reference audio into a unified music semantic space, understanding the relationships among content, style, and vocal requirements.
* **Multi-condition control**: combines conditions such as lyrics, music description, vocals, melody, or a reference song by task, supporting multiple generation modes.
* **Music structure modeling**: learns structures such as intro, verse, chorus, bridge, interlude, and outro, along with melodic and energy development across sections.
* **High-fidelity audio rendering**: reconstructs audio detail through generation architectures such as DiT, balancing vocals, instruments, spatiality, and overall production quality.

## Core capabilities

* **Lyrics to song**: from a music description and lyrics, generate a complete song with vocals, melody, arrangement, and mixing.
* **Instrumental generation**: from a style, mood, scene, or instrument description, generate instrumental music with no vocals.
* **Intelligent scoring from dry vocals**: analyze the melody, rhythm, and mood of an a cappella or dry vocal and automatically generate a matching accompaniment and arrangement.
* **Natural-language music control**: describe style and genre, vocals and singing style, melody and rhythm, instruments and arrangement, mood and scene, and production quality.
* **Reference-audio driven**: use timbre, humming, an original track, or dry vocals as reference input for more precise, more personalized generation.
* **ABC notation input**: music generation from ABC melody notation (coming soon).

## Use cases

* **Music creation and demos**: quickly validate lyrics, melody, genre, and arrangement directions, providing draft material for songwriters, producers, and singers.
* **Short video and content platforms**: generate original songs or background music by video theme, mood, and duration, improving content-production efficiency.
* **Film, games, and advertising**: generate theme music, scene music, and ad music around characters, plot, world-building, or brand tone.
* **Virtual characters and digital humans**: generate songs with a character's timbre to strengthen the character's vocal identity and sustain content supply.
* **Personalized entertainment**: generate custom songs using your own voice, lyrics, or humming for keepsakes, greetings, and social sharing.
* **Music education and inspiration**: quickly turn a melodic idea into versions in different styles, helping to understand arrangement, genre, and emotional expression.

## Input tips

* **Be specific**: rather than "generate a nice song," also state the genre, tempo, vocals, instruments, mood, and production quality to more easily get results that match your expectations.
* **Use clear lyric structure**: use section tags such as `[Intro]`, `[Verse]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, and `[Outro]` to help the model understand the song structure.
* **Adjust key variables round by round**: settle the overall genre and vocal direction first, then gradually adjust instruments, arrangement density, and production detail to compare versions.

## Compliance notes

For voice cloning, song covers, and reference-audio generation, ensure you have obtained lawful authorization from the voice subject and the relevant rights holders of the lyrics, composition, and recording. Before public distribution or commercial use, complete the necessary copyright, personality-rights, and content-safety review according to your region, platform rules, and use case.

## API endpoint

<Card title="Music API" href="/docs/en/api-reference/audio/music">
  `POST /v1/audio/music`
</Card>

## Related resources

<Columns cols={2}>
  <Card title="Audio models overview" icon="arrow-left" href="/docs/en/guides/models/audio">
    Back to the Audio 3 model overview.
  </Card>

  <Card title="Full pricing details" icon="receipt" href="/docs/en/guides/pricing/details">
    Billing rules for all speech, text, and image models.
  </Card>

  <Card title="Music API" icon="music" href="/docs/en/api-reference/audio/music">
    View the Music API request parameters.
  </Card>

  <Card title="Voice Studio" icon="play" href="https://audio.stepfun.ai/">
    Try the music generation of StepAudio 3 Music online.
  </Card>
</Columns>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.