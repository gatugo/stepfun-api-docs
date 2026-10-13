> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Step 3.5 Flash

`step-3.5-flash` is StepFun's flagship language reasoning model. It delivers top-tier reasoning quality and fast, reliable execution — decomposing and planning complex tasks, and reliably orchestrating tool calls. Suitable for logical reasoning, math, software engineering, deep research, and other complex workloads. Built on a 196B-parameter / 11B-activation sparse MoE architecture.

## Key facts

<Columns cols={3}>
  <Card title="Model type">
    Sparse MoE architecture<br />196B total params / 11B activated params
  </Card>

  <Card title="Context length">
    256K tokens
  </Card>

  <Card title="Best for">
    High-throughput reasoning + tool calling<br />Optimized for agent and coding workloads
  </Card>
</Columns>

## Core capabilities

<Columns cols={3}>
  <Card title="🚀 High-throughput reasoning">
    Sparse MoE architecture delivers high throughput and low latency, ideal for real-time agent workflows and high-volume calls.
  </Card>

  <Card title="🛠️ Tool calling">
    Reliable `tools` / `tool_choice` orchestration, supports multi-step task decomposition and plan execution.
  </Card>

  <Card title="🧠 Complex reasoning">
    Handles logical reasoning, math, software engineering, and deep research — a dependable foundation for long-chain agent reasoning.
  </Card>
</Columns>

## Model variants

<Columns cols={2}>
  <Card title="step-3.5-flash" icon="bolt">
    **Base version**: general-purpose reasoning and tool calling — well-suited to most Agent and complex-task scenarios.
  </Card>

  <Card title="step-3.5-flash-2603" icon="rocket">
    **Agent-optimized version**: tuned from `step-3.5-flash` for high-frequency agent scenarios. Better token efficiency and faster inference, with an optional low-reasoning mode that significantly reduces token consumption. Improved compatibility with coding workflows and agent frameworks. Supports the `reasoning_effort` field (`low` / `high`).
  </Card>
</Columns>

## API endpoint

<Columns cols={1}>
  <Card title="Chat Completion" href="/docs/en/api-reference/chat/chat-completion-create">
    `POST /v1/chat/completions`<br />OpenAI-compatible, with streaming and tool calling.
  </Card>
</Columns>

## Pricing

| Item | Price (per million tokens) |
| :- | :- |
| Input (cache miss) | \$0.10 |
| Input (cache hit) | \$0.02 |
| Output | \$0.30 |

[See full pricing details →](/docs/en/guides/pricing/details)

## Quickstart

<Tabs>
  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl https://api.stepfun.ai/v1/chat/completions \
      -H "Authorization: Bearer $STEP_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "step-3.5-flash",
        "messages": [
          {"role": "user", "content": "Hello, please introduce yourself."}
        ]
      }'
    ```
  </Tab>

  <Tab title="Python (OpenAI SDK)">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    from openai import OpenAI

    client = OpenAI(
        api_key="YOUR_STEP_API_KEY",
        base_url="https://api.stepfun.ai/v1",
    )

    response = client.chat.completions.create(
        model="step-3.5-flash",
        messages=[
            {"role": "user", "content": "Hello, please introduce yourself."}
        ],
    )

    print(response.choices[0].message.content)
    ```
  </Tab>
</Tabs>

## Related reading

<Columns cols={2}>
  <Card title="Reasoning model guide" href="/docs/en/guides/developer/reasoning">
    Recommended usage of reasoning models for complex tasks, tool calling, and long contexts.
  </Card>

  <Card title="Step 3.7 Flash — multimodal flagship" href="/docs/en/guides/models/step-3.7-flash">
    Building on Step 3.5 Flash with native image and video understanding.
  </Card>
</Columns>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.