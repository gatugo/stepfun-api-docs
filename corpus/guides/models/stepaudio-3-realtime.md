> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# StepAudio 3 Realtime

## Overview

StepFun offers two ways to build voice conversations. StepAudio 3 Realtime is the current flagship for real-time interaction, with major gains in full-duplex dialogue, think-while-speaking, and Voice Agent capabilities. [Technical report](https://arxiv.org/abs/2609.14005) · [View more demos](https://static.stepfun.com/blog/stepaudio3/realtime/) · [Voice Studio](https://audio.stepfun.ai/)

| Feature | Chat Completions API | Realtime API |
| - | - | - |
| Connection | HTTP request | Persistent WebSocket |
| Speech recognition (ASR) | Implement yourself or use a third-party service | Built in; user speech is transcribed automatically |
| Context management | Maintain the `messages` list yourself | Built in; conversation history managed automatically |
| Voice activity detection (VAD) | Implement yourself | Built in; user speech detected automatically |
| Web search | Implement the search interface yourself | Built-in `web_search` tool |
| Knowledge retrieval | Implement yourself | Built-in `retrieval` tool |
| Latency | Lower (streaming output) | Very low (bidirectional streaming) |
| Best for | Offline processing, batch jobs, simple integration | Real-time conversation, voice assistants, customer-service bots |

The models below can be accessed through the [Chat API](/docs/en/api-reference/chat/chat-completion-create) and the [Realtime API](/docs/en/api-reference/realtime/chat) respectively.

## Models

### StepAudio 3 Realtime

* Positioning: a full-duplex voice model for real-time interaction
* Capabilities: natural human-like interaction, full-duplex dialogue, adaptive reasoning, think-while-speaking, Voice Agent
* StepAudio 3 Realtime unifies real-time audio understanding, turn management, reasoning, and tool calling within a single conversation. It recognizes not only what the user says, but also tone, emotion, paralinguistic cues, and ambient sound.
* Supports natural interruption, backchannel recognition, and turn-taking coordination: the user and the model can speak at the same time; the model stops promptly when genuinely interrupted, and keeps the conversation coherent through natural pauses or casual backchannels.
* Responds quickly to simple questions; for complex tasks, it can adaptively engage in deeper reasoning and reduce perceived latency by thinking while speaking.
* The Voice Agent can call tools or run back-end tasks once intent is clear; the conversation continues while a task runs, and the result is woven back in naturally.

<Note>
  `stepaudio-3-realtime-preview` is the model name used during the free-trial period. When the free trial ends, this preview version will be retired and a formal paid version added. Billing and rate limits follow the [Pricing and Rate Limits](/docs/en/guides/pricing/details) page.
</Note>

### StepAudio 3 Chat

* Positioning: a speech-understanding and dialogue model for the Chat Completions API
* Capabilities: speech input, text dialogue, context understanding, tool calling
* Accessed through the [Chat API](/docs/en/api-reference/chat/chat-completion-create); suitable for submitting speech or text turn by turn and receiving text replies.
* Shares the Audio 3 series' voice understanding and reasoning; for streaming audio output and full-duplex interaction, use the Realtime API.

<Note>
  `stepaudio-3-chat-preview` is the model name used during the free-trial period. When the free trial ends, this preview version will be retired and a formal paid version added. Billing and rate limits follow the [Pricing and Rate Limits](/docs/en/guides/pricing/details) page.
</Note>

## Business scenarios

With its real-time interaction and emotional understanding, the Realtime API has been adopted across industries:

* **Smart cockpit**: a natural voice interface for in-vehicle systems—information lookup, casual conversation, and safety reminders while driving.
* **Smart devices**: real-time voice interaction for IoT hardware, improving how users interact with their devices.
* **Social and entertainment**: emotional-companion agents for social and entertainment apps.
* **Smart customer service**: highly human-like service that improves efficiency and customer satisfaction.
* **Financial mediation**: neutral, professional communication support in the handling of financial disputes.

## Quick start

<Columns cols={2}>
  <Card title="Realtime API reference" href="/docs/en/api-reference/realtime/chat">
    Request format, event fields, and interface details for the Realtime API.
  </Card>

  <Card title="Chat API reference" href="/docs/en/api-reference/chat/chat-completion-create">
    Submit speech or text and receive text replies over the Chat Completion API.
  </Card>

  <Card title="Realtime API Demo" href="https://github.com/stepfun-ai/Step-Realtime-Console">
    A reference front-end console for building a real-time voice conversation.
  </Card>
</Columns>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.