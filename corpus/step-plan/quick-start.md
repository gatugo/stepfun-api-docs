> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Quick Start

export const stepPlanTools = [{
  title: "Claude Code",
  description: "Suitable for coding, debugging, and engineering collaboration in the terminal.",
  href: "/en/guides/developer/integrations/claude-code",
  logo: "/docs/images/stepplan/tools/claudecode-color.svg"
}, {
  title: "Hermes-Agent",
  description: "Suitable for running an open-source AI Agent framework in the terminal or messaging platforms.",
  href: "/en/guides/developer/integrations/hermes-agent",
  logo: "/docs/images/stepplan/tools/hermes-agent.svg"
}, {
  title: "Open Code",
  description: "Suitable for driving development tasks with natural language in the terminal.",
  href: "/en/guides/developer/integrations/open-code",
  logo: "/docs/images/stepplan/tools/opencode.svg"
}, {
  title: "OpenClaw",
  description: "Suitable for command-driven Agents and initialization-based workflows.",
  href: "/en/guides/developer/integrations/openclaw",
  logo: "/docs/images/stepplan/tools/openclaw-color.svg"
}, {
  title: "Goose",
  description: "Suitable for orchestrating tasks and tool calls through a local terminal agent.",
  href: "/en/guides/developer/integrations/goose",
  logo: "/docs/images/stepplan/tools/goose.svg"
}, {
  title: "Cline",
  description: "Suitable for code collaboration in VS Code or Cursor.",
  href: "/en/guides/developer/integrations/cline",
  logo: "/docs/images/stepplan/tools/cline.svg"
}, {
  title: "Roo Code",
  description: "Suitable for multi-turn task collaboration within an IDE.",
  href: "/en/guides/developer/integrations/roo-code",
  logo: "/docs/images/stepplan/tools/roocode.svg"
}, {
  title: "Kilo Code",
  description: "Suitable for code generation and debugging within an IDE.",
  href: "/en/guides/developer/integrations/kilo-code",
  logo: "/docs/images/stepplan/tools/kilocode.svg"
}, {
  title: "Cherry Studio",
  description: "Suitable for centrally managing multi-model workflows on the desktop.",
  href: "/en/guides/developer/integrations/cherry-studio",
  logo: "/docs/images/stepplan/tools/cherrystudio-color.svg"
}, {
  title: "Zed",
  description: "Suitable for using AI Assistant directly in a lightweight editor.",
  href: "/en/guides/developer/integrations/zed",
  logo: "/docs/images/stepplan/tools/zed-logo-blue.svg"
}];

## 1. Prepare Your Account and API Key

Before you start configuring, first make sure your account has an available Step Plan and that you have prepared a Step API Key. They determine whether you can enable calling capabilities normally, as well as the authentication and authorization of subsequent requests.

> Recommended order: first confirm that you have subscribed to or activated a Step Plan, then create an API Key, and finally integrate a specific tool.

### Subscribe to a Step Plan

If this is your first time using the open platform, it is recommended to first check whether your current account has completed Step Plan subscription or activation. In general, only after you have an available package, plan, or corresponding calling permissions will subsequent model calls, quota usage, and capability usage take effect properly.

If your account has already been enabled by your team, you can go directly to the next step. If it has not been enabled yet, it is recommended to first complete the subscription to the corresponding plan on the platform, and then continue to create an API Key and integrate third-party tools.

### Obtain an API Key

How to obtain it:

* [Stepfun Open Platform](https://platform.stepfun.ai/interface-key)

It is recommended that you create a new API Key in the console and keep it safe. Do not write it directly into your code repository.

For your first integration, it is recommended to prioritize using the following model for verification:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step-5-preview
```

In different tools, you will frequently see these configuration items:

* `API Provider`: Select the interface provider type, such as `OpenAI Compatible`
* `Base URL`: Choose the model service address based on the protocol used by the tool. For the Chat Completions API (OpenAI-compatible) or OpenAI Compatible tools, use `https://api.stepfun.ai/step_plan/v1`. For the Messages API (Anthropic-compatible), use `https://api.stepfun.ai/step_plan`.
* `API Key`: The key obtained from the Step platform
* `Model` or `Model ID`: Enter `step-5-preview`

> Note: When manually editing the Claude Code configuration file, set `ANTHROPIC_BASE_URL` to the Messages API (Anthropic-compatible) base URL: `https://api.stepfun.ai/step_plan` (without `/v1`). Claude Code automatically appends `/v1/messages` when making requests.

## 2. Choose an Integration Tool

If you have not yet decided which tool to use, you can first choose based on your way of working:

<div className="step-plan-tool-grid">
  {stepPlanTools.map((tool) => (
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

### Common Checks

If the call fails, check the following items first:

* Whether the API Key is entered correctly and belongs to the correct environment
* Whether the `Base URL` matches the tool protocol: use `https://api.stepfun.ai/step_plan/v1` for the Chat Completions API (OpenAI-compatible) or OpenAI Compatible tools, and `https://api.stepfun.ai/step_plan` for the Messages API (Anthropic-compatible) or Claude Code configuration files
* Whether `Model` or `Model ID` is set to `step-5-preview`
* Whether the tool has already saved the configuration and been restarted


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.