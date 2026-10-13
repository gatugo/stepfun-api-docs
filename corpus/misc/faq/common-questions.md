> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# FAQ

## Audio models

### What model should I use for text-to-speech?

Use `stepaudio-2.5-tts` — our flagship contextual TTS model with zero-shot voice cloning and natural-language control over emotion and style through the `instruction` field and inline `()` prompts. See [Audio Models](/docs/en/guides/models/audio) for details.

### Where can I find the TTS API parameters?

See [Generate audio](/docs/en/api-reference/audio/create-audio) for the full request schema and examples.

### What audio formats are supported?

`wav`, `mp3`, `flac`, `opus`, `pcm`. Default is `mp3`.

### Is there a limit on input length?

Yes. The maximum input length is 1,000 characters per request.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.