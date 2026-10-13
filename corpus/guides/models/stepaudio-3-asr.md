> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# StepAudio 3 ASR

The StepAudio 3 ASR family provides high-accuracy, low-latency speech transcription.

StepAudio 3 ASR Max is StepFun's largest ASR model to date. Built on a large language model, it fuses high-precision acoustic modeling with that model's context understanding, knowledge, and reasoning—moving speech recognition from recognizing sound toward understanding context. [Voice Studio](https://audio.stepfun.ai/)

## Model information

| Item | Details |
| :- | :- |
| Input | Audio |
| Output | Incremental and final text |
| Protocol | HTTP + SSE |
| Billing | \$0.24 / hour |

## Core capabilities

* **Context understanding**: combines the audio signal, contextual relationships, and domain knowledge to improve recognition of complex content such as person and place names, drug names, technical terms, and homophones.
* **Cross-language, cross-scenario recognition**: covers Chinese, English, dialects, mixed Chinese-English, long audio, and vertical domains, improving over the previous generation.
* **Professional-domain recognition**: understands specialized expressions using domain knowledge across 20+ vertical scenarios such as sports, pharmaceuticals, chemicals, automotive, legal, finance, and software development.
* **Complex audio handling**: supports whispering, very fast speech, slurred liaison, dragged pronunciation, ambient noise, singing, and background music.
* **Song and singing transcription**: handles complex singing scenarios such as a cappella and accompanied singing, transcribing song content directly.
* **Low misrecognition**: 99% accuracy on no-speech tests, reducing erroneous transcription caused by ambient sound, background music, and silent segments.

## Benchmark highlights

* **Contextual reasoning**: 0.57% error rate—down 64.2% from StepAudio 2.5 ASR's 1.59%, and down 43.0% from Doubao ASR 2.0's 1.00%.
* **Vertical-domain proper nouns**: covering 20+ domains such as sports, pharmaceuticals, chemicals, automotive, legal, finance, and software development, with a 3.81% average error rate.
* **Across-the-board gains over the previous generation**: average error rates down 9.3% for general Chinese and 25.0% for English, 22.3% for dialects, 42.1% for vertical domains, and 27.9% for mixed Chinese-English.
* **Long-context capability**: contextual-reasoning error rate down 64.2% versus the previous generation.
* **Versus leading commercial models**: compared with Doubao ASR 2.0, average error rates down 18.6% for general Chinese, 60.4% for English, 23.3% for heavy accents, 40.3% for long audio, and 43.0% for contextual reasoning.
* **Real-world complex audio**: 3.97% CER on the AISHELL-6 whisper test, better than the previous generation's 5.36%; stable recognition across very fast speech, slurring, liaison, and dragging tests.

## Use cases

StepAudio 3 ASR Max is offered through the API and can be used for meeting minutes, video subtitles, live-stream content understanding, smart customer service, in-vehicle interaction, medical records, financial services, and professional content production—making spoken content more accurately understood, searched, and used.

## API endpoint

<Card title="Speech Recognition (Streaming Output)" icon="waveform-lines" href="/docs/en/api-reference/audio/asr-sse">
  `POST /v1/audio/asr/sse`<br />Submit audio in one request; recognition text is returned as an SSE stream.
</Card>

## Related resources

<Columns cols={2}>
  <Card title="Audio models overview" icon="arrow-left" href="/docs/en/guides/models/audio">
    Back to the Audio 3 model overview.
  </Card>

  <Card title="Full pricing details" icon="receipt" href="/docs/en/guides/pricing/details">
    Billing rules for all speech, text, and image models.
  </Card>

  <Card title="Speech Recognition API" icon="file-lines" href="/docs/en/api-reference/audio/asr-sse">
    Request parameters, response events, and interface details.
  </Card>

  <Card title="Voice Studio" icon="play" href="https://audio.stepfun.ai/">
    Try the recognition of StepAudio 3 ASR online.
  </Card>
</Columns>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.