> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Step 3.7 Flash

export const frameworkTools = [{
  title: "Claude Code",
  description: "Coding, debugging, refactoring, and project management in your terminal",
  href: "/en/guides/developer/integrations/claude-code",
  logo: "https://platform.stepfun.com/docs/images/stepplan/tools/claudecode-color.svg"
}, {
  title: "OpenClaw",
  description: "Instruction-driven Agent and initialization workflows",
  href: "/en/guides/developer/integrations/openclaw",
  logo: "https://platform.stepfun.com/docs/images/stepplan/tools/openclaw-color.svg"
}, {
  title: "Hermes Agent",
  description: "Open-source AI Agent framework for the terminal or messaging platforms",
  href: "/en/guides/developer/integrations/hermes-agent",
  logo: "https://platform.stepfun.com/docs/images/stepplan/tools/hermes-agent.svg"
}, {
  title: "Cline",
  description: "Multi-turn code collaboration in VS Code or Cursor",
  href: "/en/guides/developer/integrations/cline",
  logo: "https://platform.stepfun.com/docs/images/stepplan/tools/cline.svg"
}, {
  title: "Roo Code",
  description: "Code generation, debugging, and file edits in your IDE",
  href: "/en/guides/developer/integrations/roo-code",
  logo: "https://platform.stepfun.com/docs/images/stepplan/tools/roocode.svg"
}, {
  title: "Kilo Code",
  description: "Code generation, modification, and debugging in your IDE",
  href: "/en/guides/developer/integrations/kilo-code",
  logo: "https://platform.stepfun.com/docs/images/stepplan/tools/kilocode.svg"
}, {
  title: "Open Code",
  description: "Natural-language-driven code generation and project analysis in your terminal",
  href: "/en/guides/developer/integrations/open-code",
  logo: "https://platform.stepfun.com/docs/images/stepplan/tools/opencode.svg"
}];

StepFun's flagship multimodal reasoning model. Powered by a 198B-parameter / 11B-activation sparse MoE architecture, with native support for image and video understanding.

## Key facts

<Columns cols={3}>
  <Card title="Model type">
    Sparse MoE architecture<br />198B total params / 11B activated params
  </Card>

  <Card title="Context length">
    256K tokens
  </Card>

  <Card title="Best for">
    High-throughput reasoning + native multimodal<br />Optimized for agent and coding workloads
  </Card>
</Columns>

## Core capabilities

<Columns cols={2}>
  <Card title="👁️ Native multimodal">
    Native support for image and video understanding. Drop a file straight into the chat — no separate vision model required inside your Agent framework.
  </Card>

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

## Reasoning effort

`step-3.7-flash` supports three reasoning effort levels — pick one to match task complexity:

| Effort | Best for |
| :- | :- |
| `low` | Simple Q\&A, summarization, rewriting, information extraction |
| `medium` | Default. General reasoning and multi-step tasks |
| `high` | Complex reasoning, math, planning, code analysis |

<Info>
  The Chat Completions API uses `reasoning_effort` to control the effort level; the Messages API uses `output_config.effort`. See the [Quickstart](/docs/en/quickstart/overview) for basic call examples.
</Info>

## Get started

<Columns cols={3}>
  <Card title="Quickstart" href="/docs/en/quickstart/overview">
    Get started with images, video, local files, and reasoning-effort control.
  </Card>

  <Card title="Cookbook" href="/docs/en/guides/models/step-3.7-flash-cookbook">
    Task templates for whiteboard-to-plan, chart-to-data, receipt-to-table, and more.
  </Card>

  <Card title="Mobile Agent" href="/docs/en/guides/models/step-3.7-flash-mobile-agent">
    Connect to a real Android device via GELab-Zero and let the model plan operations from screenshots.
  </Card>

  <Card title="Chat Completion" href="/docs/en/api-reference/chat/chat-completion-create">
    `POST /v1/chat/completions`<br />OpenAI-compatible, with streaming and tool calling.
  </Card>
</Columns>

## Pricing

| Item | Price (per million tokens) |
| :- | :- |
| Input (cache hit) | \$0.04 |
| Input (cache miss) | \$0.20 |
| Output | \$1.15 |

## Framework support

`step-3.7-flash` plugs reliably into popular Coding and Agent tools, well-suited to code generation, file editing, and complex task coordination in the terminal, IDE, or Agent workflows.

<div className="step-plan-tool-grid">
  {frameworkTools.map((tool) => (
      <a key={tool.href} className="step-plan-tool-card step-plan-tool-card--link" href={tool.href}>
        <div className="step-plan-tool-card__top">
          <span className="step-plan-tool-card__logo-shell" aria-hidden="true">
            <img className="step-plan-tool-card__logo" src={tool.logo} alt="" loading="lazy" />
          </span>
        </div>
        <div className="step-plan-tool-card__body">
          <h3>{tool.title}</h3>
          <p>{tool.description}</p>
        </div>
      </a>
    ))}
</div>

[View Step Plan integration guide →](/docs/en/step-plan/quick-start)

## Related reading

<Columns cols={2}>
  <Card title="Reasoning model guide" href="/docs/en/guides/developer/reasoning">
    Recommended usage of reasoning models for complex tasks, tool calling, and long contexts.
  </Card>

  <Card title="Image understanding best practices" href="/docs/en/guides/developer/image-chat">
    A deeper look at image understanding API params, the detail setting, and best practices.
  </Card>

  <Card title="Video understanding best practices" href="/docs/en/guides/developer/video-chat">
    A deeper look at video understanding API params, file limits, and common pitfalls.
  </Card>
</Columns>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.