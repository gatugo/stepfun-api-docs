> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Audio Models

Find the right model for voice agents, translation, transcription, speech generation, and music creation.

This page summarizes what each model does; see the individual model pages for specs and quick-start code. Try them in [Voice Studio](https://audio.stepfun.ai/).

Language support:

* TTS and ASR — Chinese, English, Japanese, Korean, French, Spanish
* Realtime — Chinese, English

> Note: All languages except Chinese and English are in preview. More languages are on the way.

## Choose a model

| Model | Description | Input → Output | Details |
| - | - | - | - |
| `stepaudio-3-tts` | Natural, context-aware speech with low-latency streaming | Text → Audio | [StepAudio 3 TTS](/docs/en/guides/models/stepaudio-3-tts) |
| `stepaudio-3-asr-max` | Context-aware speech recognition via HTTP or SSE | Audio → Text | [StepAudio 3 ASR](/docs/en/guides/models/stepaudio-3-asr) |
| `stepaudio-3-realtime-preview` | Full-duplex voice interaction with adaptive reasoning | Audio or text → Audio + text | [StepAudio 3 Realtime](/docs/en/guides/models/stepaudio-3-realtime) |
| `stepaudio-3-gen-preview` | Unified generation of speech, sound effects, ambience, and background music | Text → Audio | [StepAudio 3 Gen](/docs/en/guides/models/stepaudio-3-gen) |
| `stepaudio-3-music-preview` | Music generation from text, lyrics, and audio | Text, audio → Music | [StepAudio 3 Music](/docs/en/guides/models/stepaudio-3-music) |
| `stepaudio-2.5-chat` | Understands speech (including tone and emotion) and responds in text through an OpenAI-compatible Chat Completion API | Audio or text → Text | [StepAudio 2.5 Chat](/docs/en/guides/models/stepaudio-2.5-chat) |
| `stepaudio-2.5-realtime` | Real-time speech-to-speech conversation over a WebSocket Realtime API | Audio or text → Audio + text | [StepAudio 2.5 Realtime](/docs/en/guides/models/stepaudio-2.5-realtime) |
| `stepaudio-2.5-tts` | Contextual text-to-speech with natural-language control over delivery and zero-shot voice cloning | Text → Audio | [StepAudio 2.5 TTS](/docs/en/guides/models/stepaudio-2.5-tts) |
| `stepaudio-2.5-asr` | Speech recognition (one-shot, HTTP + SSE) | Audio → Text | [StepAudio 2.5 ASR](/docs/en/guides/models/stepaudio-2.5-asr) |
| `stepaudio-2.5-asr-stream` | Real-time bidirectional streaming speech recognition | Audio → Text | [StepAudio 2.5 ASR](/docs/en/guides/models/stepaudio-2.5-asr) |

## StepAudio 3 TTS

Generate natural, expressive speech—including laughter, hesitation, and self-correction—with low-latency streaming and fine-grained control over context. [Learn more about StepAudio 3 TTS](/docs/en/guides/models/stepaudio-3-tts).

## StepAudio 3 ASR

Context-aware transcription for proper names, specialized terminology, dialects, Chinese–English code-switching, and challenging audio such as whispers and singing. [Learn more about StepAudio 3 ASR](/docs/en/guides/models/stepaudio-3-asr).

## StepAudio 3 Realtime

Full-duplex real-time voice: build natural, real-time voice agents that handle interruptions, take turns smoothly, reason while speaking, and call tools. [Learn more about StepAudio 3 Realtime](/docs/en/guides/models/stepaudio-3-realtime).

## StepAudio 3 Gen

Create speech, singing, sound effects, ambience, and background music in a single clip from a natural-language prompt. [Learn more about StepAudio 3 Gen](/docs/en/guides/models/stepaudio-3-gen).

## StepAudio 3 Music

Turn lyrics, style prompts, or dry vocals into complete songs, instrumentals, covers, and soundtracks. [Learn more about StepAudio 3 Music](/docs/en/guides/models/stepaudio-3-music).

## StepAudio 2.5 Chat

An end-to-end speech-understanding model served through an OpenAI-compatible Chat Completion API. It accepts audio or text input and returns a text response, interpreting not just the words but also vocal cues such as intonation, hesitation, and laughter.

* **Paralinguistic understanding**: captures a speaker's emotional state and intent from vocal cues a text transcript would miss.
* **Unified text and audio input**: typed and spoken turns share the same endpoint, so one conversation can mix both.
* For spoken replies, pass the text output to a text-to-speech model such as StepAudio 2.5 TTS.

Common use cases: voice assistants and conversational agents, call and meeting analysis, and voice message triage.

## StepAudio 2.5 Realtime

An end-to-end speech-to-speech model served over a WebSocket Realtime API. It takes streaming audio or text and responds with streaming audio and a matching text transcript—no separate transcription or synthesis step—keeping latency low enough for natural back-and-forth conversation.

* **Paralinguistic understanding**: interprets vocal cues such as intonation, pacing, and hesitation in addition to the spoken words.
* **Natural turn-taking**: server-side voice activity detection (VAD) lets the model reply at the right moment and be interrupted mid-response.
* **System voices**: a set of English system voices selectable per session; see the [voices list](/docs/en/guides/models/stepaudio-2.5-realtime#voices).

Common use cases: voice agents for customer support, live hands-free assistants, and interactive phone and IVR systems.

## StepAudio 2.5 TTS

A text-to-speech model that brings context understanding into the entire generation pipeline. Instead of matching preset tags, you describe the delivery you want in natural language, at two levels:

* **Global context** sets the overall mood, scene, and character relationships for an entire passage.
* **Inline context** fine-tunes how individual words and phrases are delivered.

It supports layered, mixed delivery intents, such as "restrained sadness, no sobbing, with a slight tremble". The model renders pauses, stress, rhythm, and tonal transitions accordingly, producing speech with natural breathing, dynamic emphasis, and emotional arcs.

**Zero-shot voice cloning**: about 3 seconds of reference audio is enough to clone a voice precisely, and cloned voices keep full global and inline context control, with no fixed voice library or preset characters required.

Common use cases: audiobooks, dubbing, ad narration, emotional storytelling, and other content that demands high vocal expressiveness.

## StepAudio 2.5 ASR

A new-generation speech recognition model built on a 4B-parameter Multi-Token Prediction (MTP) architecture, maintaining SOTA transcription accuracy while sharply reducing latency. Supports Chinese and English recognition with ITN text normalization. It offers two access methods:

* **One-shot recognition (`stepaudio-2.5-asr`)**: submit audio over HTTP + SSE and receive the transcription streamed back incrementally.
* **Real-time bidirectional streaming (`stepaudio-2.5-asr-stream`)**: stream audio over WebSocket and receive incremental and final results with per-word timing; supports server-side VAD.
* Suitable for live captions, voice input, meeting transcription, and back-end batch processing.

## Usage limits

* **Text-to-speech input**: up to 1,000 characters per request.
* **Text-to-speech output formats**: `wav`, `mp3`, `flac`, `opus`, `pcm`; the default is `mp3`.
* **StepAudio 3 Gen input limits**: the `instruction` and `roles` fields are capped at 500 characters and `scripts` at 1,000 characters; exceeding a limit returns HTTP 400.
* **StepAudio 3 Gen delivery**: currently supports HTTP `audio` / `sse` return; bidirectional WebSocket streaming is not supported.

## Next steps

<Columns cols={2}>
  <Card title="StepAudio 3 TTS" href="/docs/en/guides/models/stepaudio-3-tts">
    Human-level, low-latency text-to-speech.
  </Card>

  <Card title="StepAudio 3 ASR" href="/docs/en/guides/models/stepaudio-3-asr">
    Context-aware recognition on a large language model foundation.
  </Card>

  <Card title="StepAudio 3 Realtime" href="/docs/en/guides/models/stepaudio-3-realtime">
    Full-duplex real-time voice with adaptive reasoning and Voice Agent.
  </Card>

  <Card title="StepAudio 3 Gen" href="/docs/en/guides/models/stepaudio-3-gen">
    Unified audio generation—voice, SFX, ambience, and music.
  </Card>

  <Card title="StepAudio 3 Music" href="/docs/en/guides/models/stepaudio-3-music">
    Generate songs, instrumentals, covers, and scoring from dry vocals.
  </Card>

  <Card title="StepAudio 2.5 Chat Overview" href="/docs/en/guides/models/stepaudio-2.5-chat">
    Explore the end-to-end speech-understanding model with audio and text input.
  </Card>

  <Card title="StepAudio 2.5 Realtime Overview" href="/docs/en/guides/models/stepaudio-2.5-realtime">
    Explore the end-to-end speech-to-speech model with real-time conversation over WebSocket.
  </Card>

  <Card title="StepAudio 2.5 TTS Overview" href="/docs/en/guides/models/stepaudio-2.5-tts">
    Explore the contextual TTS model with dual-level context control and zero-shot voice cloning.
  </Card>

  <Card title="StepAudio 2.5 ASR Overview" href="/docs/en/guides/models/stepaudio-2.5-asr">
    Explore the new-generation 4B MTP ASR model with one-shot SSE and real-time bidirectional streaming.
  </Card>

  <Card title="Voice interaction developer guide" href="/docs/en/guides/developer/tts">
    Get started with speech generation, voice cloning, and automatic speech recognition.
  </Card>
</Columns>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.