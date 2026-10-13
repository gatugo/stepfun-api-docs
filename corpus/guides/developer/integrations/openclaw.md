> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# OpenClaw

## Prerequisites

Before configuring OpenClaw, make sure you have:

* [Subscribed to Step Plan](https://platform.stepfun.ai/step-plan)
* Logged in to [platform.stepfun.ai](https://platform.stepfun.ai) and created an API Key in the console.

## Install OpenClaw

If you haven't installed OpenClaw yet, complete the installation first.

Run one of the following commands in your terminal:

<Tabs>
  <Tab title="macOS / Linux / WSL2">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl -fsSL https://openclaw.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    powershell -c "irm https://openclaw.ai/install.ps1 | iex"
    ```
  </Tab>

  <Tab title="npm">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    npm i -g openclaw
    ```
  </Tab>
</Tabs>

## Configure the Step Model

After installation, the Onboard wizard launches automatically. If you've already installed OpenClaw, you can re-launch the Onboard wizard with:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
openclaw onboard
```

### Configure the model API key

Use the following settings:

* In **Model/auth provider**, select **StepFun**.
* In **StepFun auth method**, select **StepFun Step Plan API key**.
* In **Enter StepFun API key**, paste your API key.
* **Model configured** displays the default model under this auth method.
* In the **Default model** list, you can keep the default or pick another model.

### Complete the remaining configuration

Next, configure channel, search, skills, and hooks based on your needs.
After configuration, you can choose to launch in the terminal (TUI) or in the Web UI.

### Verify

After launching, ask any question and check whether OpenClaw responds in the interface.

### Other configuration methods

<Tabs>
  <Tab title="Quick setup via official script">
    #### macOS / Linux (Bash)

    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl -fsSL https://raw.githubusercontent.com/Zgh332358/openclaw-stepfun-installer/main/add_stepfun_smart.sh | bash
    ```

    #### Windows (PowerShell, administrator mode)

    **Note**: You must run this in PowerShell as administrator. Otherwise the script will print a notice and exit.

    1. Right-click the Windows Start menu and choose "Terminal (Admin)" or "Windows PowerShell (Admin)".

    2. Run the following command:

    ```powershell theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    irm https://raw.githubusercontent.com/Zgh332358/openclaw-stepfun-installer/main/add_stepfun_smart.ps1 | iex
    ```
  </Tab>

  <Tab title="Edit the configuration file manually">
    The OpenClaw configuration file is located at `~/.openclaw/openclaw.json`.

    Open it in your editor of choice and add or modify the following. This example uses the Step 5 Preview context window; set `<model_id>` to `step-5-preview`. For `step-3.7-flash` or the Step 3.5 Flash series, also change `contextWindow` to `256000`. The example's `maxTokens: 8192` is an output budget, not the model's maximum output capability.

    ```jsonc theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    {
      "agents": {
        "defaults": {
          "model": {
            "primary": "stepfun/<model_id>" // <model_id> can be step-5-preview, step-3.7-flash, step-3.5-flash-2603, or step-3.5-flash
          }
        }
      },
      "models": {
        "mode": "merge",
        "providers": {
          "stepfun": {
            "baseUrl": "https://api.stepfun.ai/step_plan/v1",
            "apiKey": "${STEP_API_KEY}",
            "api": "openai-completions",
            "models": [
              {
                "id": "<model_id>",
                "name": "<model_id>",
                "reasoning": true,
                "contextWindow": 1000000,
                "maxTokens": 8192
              }
            ]
          }
        }
      }
    }
    ```

    > Note: Fill in `<model_id>` with a model available to your account under Step Plan. Verified examples: `step-5-preview`, `step-3.7-flash`, `step-3.5-flash-2603`, `step-3.5-flash`. The models listed in the docs are not a complete availability list.
  </Tab>
</Tabs>

## FAQ

<AccordionGroup>
  <Accordion title="Q: 'Model is not allowed' after configuration">
    If you've configured `agents.defaults.models` (an allowlist), make sure `stepfun/<model_id>` is also added to that list, otherwise the model will be blocked. To fix:

    ```jsonc theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    {
      "agents": {
        "defaults": {
          "models": {
            "stepfun/<model_id>": {
              "alias": "Step Model"
            }
          }
        }
      }
    }
    ```

    Or simply remove the `agents.defaults.models` entry to disable the allowlist.
  </Accordion>

  <Accordion title="Q: Why does the `api` field use `openai-completions`?">
    StepFun's API is fully compatible with the OpenAI Chat Completions request format. When configuring a custom provider in OpenClaw, two API types are supported:

    * `openai-completions`: for providers compatible with the OpenAI format (most third-party providers)
    * `anthropic-messages`: for providers compatible with the Anthropic Messages format

    StepFun belongs to the former.
  </Accordion>

  <Accordion title="Q: Can I skip WSL2 on Windows?">
    Not recommended. OpenClaw depends on Linux toolchains (`make`, `g++`, etc.) and systemd service management; running natively on Windows runs into many compatibility issues. WSL2 is the officially recommended way to use OpenClaw on Windows.
  </Accordion>
</AccordionGroup>

## References

* [OpenClaw Documentation](https://docs.openclaw.ai)
* [OpenClaw Model Providers](https://docs.openclaw.ai/concepts/model-providers)
* [OpenClaw Models CLI](https://docs.openclaw.ai/concepts/models)
* [Step Plan subscription](https://platform.stepfun.ai/step-plan)


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.