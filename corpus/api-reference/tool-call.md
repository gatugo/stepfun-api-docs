> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Tool Call

Toolcall (Function Calling) is an advanced capability on the StepFun platform. It lets models decide which external tools or functions to invoke to satisfy a user request. By using the Toolcall API, you can extend model capabilities to cover more use cases and offer richer features. Below is a minimal JSON request example that must include three key parameters:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "model": "step-5-preview",
  "messages": [
    {
      "role": "user",
      "content": "Hey, can you calculate (80 + 20) / 5 for me?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "Calculator",
        "description": "This StepFun API provides basic arithmetic: addition, subtraction, multiplication, and division.",
        "parameters": {
          "properties": {
            "formula": {
              "type": "string",
              "description": "Expression to evaluate. Only integers are supported. Operators: +, -, *, /, and parentheses. Example: (1 + 2) * 3."
            }
          },
          "type": "object"
        }
      }
    }
  ]
}
```

## model: model name

The following models **support** Toolcall requests:

* step-5-preview
* step-3.7-flash
* step-3.5-flash
* step-3.5-flash-2603

## Official tools

Availability of built-in tools depends on the selected model. Support for function calling does not imply support for every built-in tool.

* Web search: the built-in Chat Completions `web_search` tool is not available on `step-5-preview`. Integrate an external search service through a function tool and return its results to the model.
* Knowledge base search: upload text to a knowledge base and search it to reduce hallucinations.

## tools: list of functions

Use `tools` to describe the functions available locally. Up to 128 tools are allowed. Each entry has type `function` and contains a `function` object with the name, description, and parameters.

* `name`: letters, numbers, `-`, `_`; ideally under 64 characters. Use a clear English name so the model understands it (regex guideline: `^[a-zA-Z*][a-zA-Z0-9-_]63$`).
* `parameters`: root `type` must be `object`. The content follows a subset of JSON Schema; keys follow the same naming rule. See [JSON Schema](https://json-schema.org/understanding-json-schema/reference/type) for supported `type` values. `description` explains each parameter.
* `description`: explains what the function does so the model can choose it; English or Chinese is supported.

## messages: conversation context

See [Chat Completion request object](/docs/en/api-reference/chat/chat-completion-create).

## Examples

<Tabs>
  <Tab title="python">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    from openai import OpenAI

    client = OpenAI(api_key="YOUR_STEP_API_KEY", base_url="https://api.stepfun.ai/v1")

    completion = client.chat.completions.create(
        model="step-5-preview",
        messages=[
            {
                "role": "user",
                "content": "Can you calculate (80 + 20) / 5 for me?"
            }
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "Calculator",
                    "description": "This StepFun API provides basic arithmetic: addition, subtraction, multiplication, and division.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "formula": {
                                "type": "string",
                                "description": "Expression to evaluate. Only integers are supported. Operators: +, -, *, /, and parentheses. Example: '(1 + 2) * 3'."
                            }
                        }
                    }
                }
            }
        ]
    )

    print(completion)
    ```
  </Tab>

  <Tab title="js">
    ```js theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    import OpenAI from "openai";

    const openai = new OpenAI({
        apiKey: "YOUR_STEP_API_KEY",
        baseURL: "https://api.stepfun.ai/v1"
    });

    async function main() {
        const completion = await openai.chat.completions.create({
            model: "step-5-preview",
            messages: [
                {
                    role: "user",
                    content: "Can you calculate (80 + 20) / 5 for me?"
                }
            ],
            tools: [
                {
                    type: "function",
                    function: {
                        name: "Calculator",
                        description: "This StepFun API provides basic arithmetic: addition, subtraction, multiplication, and division.",
                        parameters: {
                            type: "object",
                            properties: {
                                formula: {
                                    type: "string",
                                    description: "Expression to evaluate. Only integers are supported. Operators: +, -, *, /, and parentheses. Example: '(1 + 2) * 3'."
                                }
                            }
                        }
                    }
                }
            ]
        });

        console.log(JSON.stringify(completion));
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl https://api.stepfun.ai/v1/chat/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $STEP_API_KEY" \
      -d '{
        "model": "step-5-preview",
        "messages": [
          {
            "role": "user",
            "content": "Can you calculate (80 + 20) / 5 for me?"
          }
        ],
        "tools": [
          {
            "type": "function",
            "function": {
              "name": "Calculator",
              "description": "This StepFun API provides basic arithmetic: addition, subtraction, multiplication, and division.",
              "parameters": {
                "type": "object",
                "properties": {
                  "formula": {
                    "type": "string",
                    "description": "Expression to evaluate. Only integers are supported. Operators: +, -, *, /, and parentheses. Example: (1 + 2) * 3."
                  }
                }
              }
            }
          }
        ]
      }'
    ```
  </Tab>
</Tabs>

```json filename="Response" theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "id": "b7b56af0-52a6-483f-a589-948182676a1b",
  "object": "chat.completion",
  "created": 1717744611,
  "model": "step-5-preview",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "",
        "tool_calls": [
          {
            "id": "call_ybVBO_JASgipgJH8xWbhKg",
            "type": "function",
            "function": {
              "name": "Calculator",
              "arguments": "{\"formula\": \"(80 + 20) / 5\"}"
            }
          }
        ]
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 151,
    "completion_tokens": 25,
    "total_tokens": 176
  }
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.