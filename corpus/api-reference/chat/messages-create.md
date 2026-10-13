> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Messages API

Call Step models using an Anthropic Messages API-compatible format, with support for streaming, tool calls, image input, and reasoning effort configuration.

## Endpoint

Claude Code and the Anthropic SDK use the configuration Base URL and append `/v1/messages`. Use the full request URL with curl. For tool setup, see the [Claude Code integration guide](/docs/en/guides/developer/integrations/claude-code).

| Channel | Configuration Base URL | Full request URL |
| - | - | - |
| Standard API | `https://api.stepfun.ai` | `POST https://api.stepfun.ai/v1/messages` |
| Step Plan | `https://api.stepfun.ai/step_plan` | `POST https://api.stepfun.ai/step_plan/v1/messages` |

## Request Parameters

The request supports the following top-level fields:

| Field | Type | Required | Description |
| - | - | - | - |
| `model` | string | Yes | Model ID, such as `step-5-preview`, `step-3.7-flash`, or `step-3.5-flash`. `step-router-v1` is available only through [Step Plan](/docs/en/step-plan/overview); see its field restrictions below. |
| `messages` | object array | Yes | Conversation messages; at least one. Each message contains `role` (`user` / `assistant`) and `content` (plain text or a content block array). |
| `max_tokens` | int | Yes | Maximum number of generated tokens; must be greater than 0. |
| `system` | string or array | No | System prompt, as a string or an array of text blocks. |
| `tools` | object array | No | Tool definitions. Each entry contains `name`, `description`, and `input_schema` (JSON Schema). |
| `output_config` | object | No | Output configuration. `effort` controls reasoning depth: models supporting three levels accept `low` / `medium` / `high`; `step-3.5-flash-2603` accepts `low` and `high`. |
| `stream` | boolean | No | Whether to stream the response. Defaults to non-streaming. |
| `temperature` | float | No | Sampling temperature, from 0 to 2. |
| `top_p` | float | No | Nucleus sampling parameter, greater than 0 and at most 1. |
| `top_k` | int | No | Top-k parameter, from 0 to 500. |
| `stop_sequences` | string array | No | Generation stops when any sequence in this list appears in the output. |

### Message Content Format

The `content` field of each entry in `messages` accepts plain text (a string) or an array of the following content blocks:

| Block | type | Fields |
| - | - | - |
| Text | `text` | `text`: text content. |
| Image | `image` | `source` supports a URL, `{"type":"url","url":"https://..."}`, or Base64, `{"type":"base64","media_type":"image/png","data":"..."}`. |
| Tool call (from the model) | `tool_use` | `id`: unique identifier; `name`: tool name; `input`: argument object. |
| Tool result (from the caller) | `tool_result` | `tool_use_id`: matching call ID; `content`: execution result; `is_error`: whether execution failed. |

## step-router-v1 Field Restrictions

`step-router-v1` is available only through Step Plan and routes between `deepseek-v4-pro` and `step-3.7-flash`. The restrictions below apply only to this model; other fields follow the request parameters above.

| Field | Behavior when calling step-router-v1 |
| - | - |
| `model` | The router model ID is `step-router-v1`; an invalid router model name returns HTTP 400 `request_params_invalid`. |
| `max_tokens` | Maximum: 250K. |
| Image / document blocks in `messages.content` | Not supported; returns `unsupported_content_type`. |
| `web_search` in `tools` | Not supported; returns `unsupported_content_type`. |
| `output_config.effort` | Ignored. |

## Response

### Non-streaming response

`Content-Type: application/json`

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
    "id": "msg_xxx",
    "type": "message",
    "role": "assistant",
    "model": "step-5-preview",
    "stop_reason": "end_turn",
    "usage": {
        "input_tokens": 20,
        "output_tokens": 12
    },
    "content": [
        {
            "type": "text",
            "text": "I'm an AI assistant."
        }
    ]
}
```

#### Response Fields

| Field | Type | Description |
| - | - | - |
| `id` | string | Unique message identifier. |
| `type` | string | Object type, always `message`. |
| `role` | string | Role, always `assistant`. |
| `model` | string | Model ID used for this response. |
| `content` | object array | Response blocks, which may include `text`, `thinking`, or `tool_use`. |
| `stop_reason` | string | Why generation stopped: `end_turn`, `tool_use`, or `max_tokens`. |
| `usage` | object | Token usage, including `input_tokens` and `output_tokens`. Cache usage fields may also be present. |

### Streaming response

`Content-Type: text/event-stream`

Streaming uses standard SSE format. Each event has an `event:` line and a `data:` line; `data:` is JSON.

Common event types: `message_start`, `content_block_start`, `content_block_delta`, `content_block_stop`, `message_delta`, `message_stop`, `ping`.

When streaming tool-call arguments, `content_block_delta.delta.type` may be `input_json_delta`.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
event: message_start
data: {"type":"message_start","message":{"id":"msg_xxx","type":"message","role":"assistant","model":"step-5-preview","content":[],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":20,"output_tokens":1}}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Hello"}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null},"usage":{"output_tokens":12}}

event: message_stop
data: {"type":"message_stop"}
```

## Examples

Replace `YOUR_STEP_API_KEY` with your key. Set `STEP_API_KEY` before running examples that use the environment variable, then select the standard API or Step Plan tab for your channel.

<Tabs>
  <Tab title="Basic chat">
    <Tabs>
      <Tab title="Standard API">
        <CodeGroup>
          ```python Python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          from anthropic import Anthropic

          client = Anthropic(api_key="YOUR_STEP_API_KEY", base_url="https://api.stepfun.ai")

          message = client.messages.create(
              model="step-5-preview",
              max_tokens=1024,
              system="You are an AI chat assistant provided by StepFun. You are fluent in English, Chinese, and many other languages. You answer user questions quickly and accurately while protecting user data.",
              messages=[
                  {
                      "role": "user",
                      "content": "Introduce yourself in one sentence."
                  }
              ],
          )

          print(message)
          ```

          ```js JavaScript theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          import Anthropic from "@anthropic-ai/sdk";

          const client = new Anthropic({
              apiKey: "YOUR_STEP_API_KEY",
              baseURL: "https://api.stepfun.ai"
          });

          async function main() {
              const message = await client.messages.create({
                  model: "step-5-preview",
                  max_tokens: 1024,
                  system: "You are an AI chat assistant provided by StepFun. You are fluent in English, Chinese, and many other languages. You answer user questions quickly and accurately while protecting user data.",
                  messages: [
                      {
                          role: "user",
                          content: "Introduce yourself in one sentence."
                      }
                  ]
              });

              console.log(JSON.stringify(message));
          }

          main();
          ```

          ```bash cURL theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          curl https://api.stepfun.ai/v1/messages \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $STEP_API_KEY" \
            -d '{
              "model": "step-5-preview",
              "max_tokens": 1024,
              "system": "You are an AI chat assistant provided by StepFun. You are fluent in English, Chinese, and many other languages. You answer user questions quickly and accurately while protecting user data.",
              "messages": [
                  {
                      "role": "user",
                      "content": "Introduce yourself in one sentence."
                  }
              ]
          }'
          ```
        </CodeGroup>

        ```json filename="Response Example" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
        {
            "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
            "type": "message",
            "role": "assistant",
            "model": "step-5-preview",
            "stop_reason": "end_turn",
            "usage": {
                "input_tokens": 35,
                "output_tokens": 20
            },
            "content": [
                {
                    "type": "text",
                    "text": "I'm an AI chat assistant by StepFun, ready to answer your questions in English, Chinese, and other languages quickly and accurately."
                }
            ]
        }
        ```
      </Tab>

      <Tab title="Step Plan">
        <CodeGroup>
          ```python Python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          import os
          from anthropic import Anthropic

          client = Anthropic(
              api_key=os.environ["STEP_API_KEY"],
              base_url="https://api.stepfun.ai/step_plan",
          )

          message = client.messages.create(
              model="step-5-preview",
              max_tokens=1024,
              messages=[
                  {
                      "role": "user",
                      "content": "Reply with OK."
                  }
              ],
          )

          print(message.content)
          ```

          ```js JavaScript theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          import Anthropic from "@anthropic-ai/sdk";

          const client = new Anthropic({
              apiKey: process.env.STEP_API_KEY,
              baseURL: "https://api.stepfun.ai/step_plan"
          });

          async function main() {
              const message = await client.messages.create({
                  model: "step-5-preview",
                  max_tokens: 1024,
                  messages: [
                      {
                          role: "user",
                          content: "Reply with OK."
                      }
                  ]
              });

              console.log(message.content);
          }

          main();
          ```

          ```bash cURL theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          export STEP_API_KEY="YOUR_STEP_API_KEY"

          curl https://api.stepfun.ai/step_plan/v1/messages \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${STEP_API_KEY}" \
            -d '{
              "model": "step-5-preview",
              "max_tokens": 1024,
              "messages": [
                  {
                      "role": "user",
                      "content": "Reply with OK."
                  }
              ]
          }'
          ```
        </CodeGroup>

        ```json filename="Response Example" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
        {
            "id": "msg_xxx",
            "type": "message",
            "role": "assistant",
            "model": "step-5-preview",
            "stop_reason": "end_turn",
            "usage": {
                "input_tokens": 20,
                "output_tokens": 1
            },
            "content": [
                {
                    "type": "text",
                    "text": "OK"
                }
            ]
        }
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="Streaming response">
    <Tabs>
      <Tab title="Standard API">
        <CodeGroup>
          ```python Python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          from anthropic import Anthropic

          client = Anthropic(api_key="YOUR_STEP_API_KEY", base_url="https://api.stepfun.ai")

          with client.messages.stream(
              model="step-5-preview",
              max_tokens=1024,
              messages=[
                  {
                      "role": "user",
                      "content": "Introduce yourself in one sentence."
                  }
              ],
          ) as stream:
              for text in stream.text_stream:
                  print(text, end="", flush=True)

          print()
          ```

          ```js JavaScript theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          import Anthropic from "@anthropic-ai/sdk";

          const client = new Anthropic({
              apiKey: "YOUR_STEP_API_KEY",
              baseURL: "https://api.stepfun.ai"
          });

          async function main() {
              const stream = client.messages.stream({
                  model: "step-5-preview",
                  max_tokens: 1024,
                  messages: [
                      {
                          role: "user",
                          content: "Introduce yourself in one sentence."
                      }
                  ]
              });

              for await (const event of stream) {
                  if (
                      event.type === "content_block_delta" &&
                      event.delta.type === "text_delta"
                  ) {
                      process.stdout.write(event.delta.text);
                  }
              }

              console.log();
          }

          main();
          ```

          ```bash cURL theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          curl https://api.stepfun.ai/v1/messages \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $STEP_API_KEY" \
            -d '{
              "model": "step-5-preview",
              "max_tokens": 1024,
              "stream": true,
              "messages": [
                  {
                      "role": "user",
                      "content": "Introduce yourself in one sentence."
                  }
              ]
          }'
          ```
        </CodeGroup>
      </Tab>

      <Tab title="Step Plan">
        <CodeGroup>
          ```python Python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          import os
          from anthropic import Anthropic

          client = Anthropic(
              api_key=os.environ["STEP_API_KEY"],
              base_url="https://api.stepfun.ai/step_plan",
          )

          with client.messages.stream(
              model="step-5-preview",
              max_tokens=1024,
              messages=[
                  {
                      "role": "user",
                      "content": "Reply with OK."
                  }
              ],
          ) as stream:
              for text in stream.text_stream:
                  print(text, end="", flush=True)

          print()
          ```

          ```js JavaScript theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          import Anthropic from "@anthropic-ai/sdk";

          const client = new Anthropic({
              apiKey: process.env.STEP_API_KEY,
              baseURL: "https://api.stepfun.ai/step_plan"
          });

          async function main() {
              const stream = client.messages.stream({
                  model: "step-5-preview",
                  max_tokens: 1024,
                  messages: [
                      {
                          role: "user",
                          content: "Reply with OK."
                      }
                  ]
              });

              for await (const event of stream) {
                  if (
                      event.type === "content_block_delta" &&
                      event.delta.type === "text_delta"
                  ) {
                      process.stdout.write(event.delta.text);
                  }
              }

              console.log();
          }

          main();
          ```

          ```bash cURL theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          export STEP_API_KEY="YOUR_STEP_API_KEY"

          curl https://api.stepfun.ai/step_plan/v1/messages \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${STEP_API_KEY}" \
            -d '{
              "model": "step-5-preview",
              "max_tokens": 1024,
              "stream": true,
              "messages": [
                  {
                      "role": "user",
                      "content": "Reply with OK."
                  }
              ]
          }'
          ```
        </CodeGroup>
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="Using output_config.effort">
    <Tabs>
      <Tab title="Standard API">
        <CodeGroup>
          ```python Python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          from anthropic import Anthropic

          client = Anthropic(api_key="YOUR_STEP_API_KEY", base_url="https://api.stepfun.ai")

          message = client.messages.create(
              model="step-5-preview",
              max_tokens=1024,
              messages=[
                  {
                      "role": "user",
                      "content": "Explain reinforcement learning in three sentences."
                  }
              ],
              extra_body={
                  "output_config": {
                      "effort": "medium"
                  }
              }
          )

          print(message)
          ```

          ```bash cURL theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          curl https://api.stepfun.ai/v1/messages \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $STEP_API_KEY" \
            -d '{
              "model": "step-5-preview",
              "max_tokens": 1024,
              "messages": [
                  {
                      "role": "user",
                      "content": "Explain reinforcement learning in three sentences."
                  }
              ],
              "output_config": {
                  "effort": "medium"
              }
          }'
          ```
        </CodeGroup>
      </Tab>

      <Tab title="Step Plan">
        <CodeGroup>
          ```python Python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          import os
          from anthropic import Anthropic

          client = Anthropic(
              api_key=os.environ["STEP_API_KEY"],
              base_url="https://api.stepfun.ai/step_plan",
          )

          message = client.messages.create(
              model="step-5-preview",
              max_tokens=1024,
              messages=[
                  {
                      "role": "user",
                      "content": "Explain reinforcement learning in three sentences."
                  }
              ],
              extra_body={
                  "output_config": {
                      "effort": "medium"
                  }
              }
          )

          print(message)
          ```

          ```bash cURL theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
          export STEP_API_KEY="YOUR_STEP_API_KEY"

          curl https://api.stepfun.ai/step_plan/v1/messages \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${STEP_API_KEY}" \
            -d '{
              "model": "step-5-preview",
              "max_tokens": 1024,
              "messages": [
                  {
                      "role": "user",
                      "content": "Explain reinforcement learning in three sentences."
                  }
              ],
              "output_config": {
                  "effort": "medium"
              }
          }'
          ```
        </CodeGroup>
      </Tab>
    </Tabs>
  </Tab>
</Tabs>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.