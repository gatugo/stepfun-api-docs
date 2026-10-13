> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshooting guide

For common issues, see [exception handling guidance](/docs/en/guides/developer/exception).

## Chat API

If you use [Chat API](/docs/en/api-reference/chat/chat-completion-create) / text-to-image / image-to-image / image edit / [audio generation](/docs/en/api-reference/audio/create-audio) / [voice cloning](/docs/en/api-reference/audio/create-voice), please share:

* `X-Trace-Id` from the response headers.
* The result ID (for example, `b7b56af0-52a6-483f-a589-948182676a1b`).

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
	"id": "b7b56af0-52a6-483f-a589-948182676a1b",
	"object": "chat.completion",
	"created": 1709893411,
	"model": "step-3.7-flash",
	"choices": [
		{
			"index": 0,
			"message": {
				"role": "assistant",
				"content": "Hello!"
			},
			"finish_reason": "stop"
		}
	],
	"usage": {
		"prompt_tokens": 83,
		"completion_tokens": 176,
		"total_tokens": 259
	}
}
```

## Streaming audio API

If you use the [streaming audio API](/docs/en/api-reference/audio/ws-audio), please share:

* The `session_id` from any event (e.g., `01956e7388477cfcbdc3aaabf364bc70`).

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
	"event_id": "01956e73888c7953896a6e176bf3d760",
	"type": "tts.connection.done",
	"data": {
		"session_id": "01956e7388477cfcbdc3aaabf364bc70"
	}
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.