> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Reasoning Model Integration

Step Plan supports accessing StepFun reasoning models via a dedicated path. All requests uniformly use the `/step_plan/v1/...` path prefix, and the domain name is fixed as `https://api.stepfun.ai`.

## Prerequisites

1. Subscribed to a [Step Plan](https://platform.stepfun.ai/step-plan).
2. Obtained an [API Key](https://platform.stepfun.ai/interface-key).

***

## Supported Models

| Model | Description |
| - | - |
| `step-5-preview` | Flagship model for agentic work, with text, image, and video input and a 1M-token context window. |
| `step-3.7-flash` | High-speed multimodal reasoning model with native image and video understanding. Supports three reasoning effort levels (low/medium/high) — well-suited to agent, coding, and multimodal workloads. |
| `step-3.5-flash-2603` | Optimized from Step 3.5 Flash for high-frequency Agent scenarios. Improved token efficiency and faster inference; can switch to low-inference mode to significantly reduce token consumption. |
| `step-3.5-flash` | Sparse MoE architecture with 196B total / 11B activated parameters. High-speed inference, optimized for agent and coding tasks. |

## Endpoint Paths

| Capability | Request Method | Step Plan Path |
| - | - | - |
| Chat Completion (OpenAI protocol) | POST | `https://api.stepfun.ai/step_plan/v1/chat/completions` |
| Messages (Anthropic protocol) | POST | `https://api.stepfun.ai/step_plan/v1/messages` |

<Info>
  The endpoint parameters are exactly the same as the open platform. For details, see the [Chat Completion API docs](/docs/en/api-reference/chat/chat-completion-create) and the Messages API docs.
</Info>

<Warning>
  The Anthropic SDK automatically appends `/v1/messages` to the base URL, so when using the Anthropic SDK, set the base URL to `https://api.stepfun.ai/step_plan` (without `/v1`). The OpenAI SDK uses `https://api.stepfun.ai/step_plan/v1`.
</Warning>

## Reasoning Effort

Models that support three reasoning effort levels accept `low`, `medium`, or `high` in the request. Chat Completion (OpenAI protocol) uses `reasoning_effort`; Messages (Anthropic protocol) uses `output_config.effort`.

| Effort | Recommended Use |
| - | - |
| `low` | Simple Q\&A, summarization, rewriting, information extraction |
| `medium` | Default recommendation; suits general reasoning and multi-step tasks |
| `high` | Complex reasoning, math, planning, code analysis |

## Billing

The billing logic is consistent with the open platform. The actual amount billed on the open platform is converted into Step Plan Credit consumption. For details on plan entitlements, see the [Step Plan overview](/docs/en/step-plan/overview).

## Integration Methods

### Direct API Calls

<Tabs>
  <Tab title="curl">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl -X POST 'https://api.stepfun.ai/step_plan/v1/chat/completions' \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $STEP_API_KEY" \
    -d '{
        "model": "step-5-preview",
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
        base_url="https://api.stepfun.ai/step_plan/v1",
    )

    response = client.chat.completions.create(
        model="step-5-preview",
        messages=[
            {"role": "user", "content": "Hello, please introduce yourself."}
        ],
    )

    print(response.choices[0].message.content)
    ```
  </Tab>

  <Tab title="Python (Anthropic SDK)">
    ```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    from anthropic import Anthropic

    # Note: The Anthropic SDK automatically appends /v1/messages; base_url should not include /v1
    client = Anthropic(
        api_key="YOUR_STEP_API_KEY",
        base_url="https://api.stepfun.ai/step_plan",
    )

    message = client.messages.create(
        model="step-5-preview",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello, please introduce yourself."}
        ],
    )

    print(message.content[0].text)
    ```
  </Tab>
</Tabs>

### Via Tool Integrations

Reasoning models can be integrated through a variety of Agent tools and coding assistants. Just set the Base URL to `https://api.stepfun.ai/step_plan/v1` and select `step-5-preview`, `step-3.7-flash`, `step-3.5-flash-2603`, `step-3.5-flash`, or `step-router-v1` as the model.

See the [Quick Start](/docs/en/step-plan/quick-start) and the individual tool integration guides:

<Columns cols={2}>
  <Card title="OpenClaw" href="/docs/en/guides/developer/integrations/openclaw">
    Command-driven Agents and initialization-based workflows.
  </Card>

  <Card title="Claude Code" href="/docs/en/guides/developer/integrations/claude-code">
    Coding, debugging, and engineering collaboration in the terminal.
  </Card>

  <Card title="Hermes-Agent" href="/docs/en/guides/developer/integrations/hermes-agent">
    Open-source AI Agent framework for terminals or messaging platforms.
  </Card>

  <Card title="Open Code" href="/docs/en/guides/developer/integrations/open-code">
    Drive development tasks in the terminal with natural language.
  </Card>
</Columns>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.