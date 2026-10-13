> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Pi

Pi is an open-source terminal coding agent maintained by earendil-works, with tools for reading files, editing code, and running commands. A custom provider connects it to Step Plan through the Anthropic Messages API.

## Requirements

* macOS, Linux, or Windows with Node.js 22.19 or later and npm.
* An active [Step Plan subscription](https://platform.stepfun.ai/step-plan), available quota, and access to the model.
* An API key from the [StepFun platform API keys page](https://platform.stepfun.ai/interface-key).

Run the following commands in your terminal to check your environment:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
node --version
npm --version
```

If your Node.js version is `v22.19.0` or later and npm successfully returns a version number, you can proceed with installing Pi.

## Install Pi

Install Pi 0.87.1:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@0.87.1
```

Check the installed version:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
pi --version
```

## Configure Step Plan

### Set the API key

Set the environment variable in the terminal that will launch Pi. Replace `YOUR_STEP_API_KEY` with your key.

<Tabs>
  <Tab title="macOS / Linux / WSL">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    export STEP_API_KEY="YOUR_STEP_API_KEY"
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    $env:STEP_API_KEY = "YOUR_STEP_API_KEY"
    ```
  </Tab>
</Tabs>

### Add models

1. Open `~/.pi/agent/models.json`. If `PI_CODING_AGENT_DIR` is set, use `models.json` in that directory instead.
2. Merge the following `providers.stepfun` entry into the file, preserving other providers. If the file does not exist, create the directory and save this JSON.

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "providers": {
    "stepfun": {
      "baseUrl": "https://api.stepfun.ai/step_plan",
      "api": "anthropic-messages",
      "apiKey": "$STEP_API_KEY",
      "models": [
        { "id": "step-5-preview", "input": ["text", "image"], "contextWindow": 1000000 },
        { "id": "step-3.7-flash", "input": ["text", "image"], "contextWindow": 256000 }
      ]
    }
  }
}
```

| Field | Description |
| - | - |
| `providers.stepfun` | Provider identifier, selected with `--provider stepfun`. |
| `baseUrl` | Step Plan configuration URL. Pi appends `/v1/messages`, producing `/step_plan/v1/messages`. |
| `api` | `anthropic-messages` selects the Anthropic Messages protocol. |
| `apiKey` | `$STEP_API_KEY` references the variable in the process environment. |
| `models[].input` | Input types the client may send. |
| `models[].contextWindow` | Context window used by the client, expressed as an integer token count. |

[Step 5 Preview](/docs/en/guides/models/step-5-preview) has a 1M-token context window; [Step 3.7 Flash](/docs/en/guides/models/step-3.7-flash) has a 256K-token window. The configuration uses `1000000` and `256000`, respectively.

### Set the default model

Merge these fields into `settings.json` in the same configuration directory:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "defaultProvider": "stepfun",
  "defaultModel": "step-5-preview"
}
```

## Start Pi

Run Pi from your project directory:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
pi
```

To select the provider and model at launch, use:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
pi --provider stepfun --model step-5-preview
```

## Verify the integration

### Check model configuration

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
pi auth check --provider stepfun --json
pi --list-models stepfun
```

An authentication status of `ready` means the client can resolve its credentials. The model list should include the configured IDs, with a 1M window for Step 5 Preview and a 256K window for Step 3.7 Flash.

### Test a conversation

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
pi --provider stepfun --model step-5-preview --print "Reply only with OK."
```

Expected output: `OK`.

### Test tool calls

Create a separate test directory on a machine with Python installed. Add a `README.md` containing `Pi Step Plan test`, start Pi from that directory, and enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Read README.md and create hello.py that prints exactly "Hello, StepFun!".
Run hello.py with an available Python interpreter and report the command and output.
Do not modify other files.
```

Check the file-reading, creation, and command records. Confirm that `hello.py` exists and outputs `Hello, StepFun!`.

### Check usage

In the [StepFun platform](https://platform.stepfun.ai) usage details, match the request time, model ID, and billing source to confirm that the call used Step Plan.

## Common questions

<AccordionGroup>
  <Accordion title="Q: Why are Step models missing from the list?">
    Check that the active configuration directory contains valid JSON in `models.json` and the correct IDs under `providers.stepfun.models`. Open `/model` to reload the file, or restart Pi and run `pi --list-models stepfun`.
  </Accordion>

  <Accordion title="Q: What if the API key cannot be resolved or authentication fails?">
    Set `STEP_API_KEY` in the terminal that launches Pi. Check that the key is complete, valid, and belongs to the account for the configured endpoint. A saved `stepfun` credential in `auth.json` takes precedence, so check that entry as well.
  </Accordion>

  <Accordion title="Q: How do I correct the request path?">
    Set `api` to `anthropic-messages` and `baseUrl` to `https://api.stepfun.ai/step_plan`. Pi appends `/v1/messages`; the configuration URL ends at `/step_plan`.
  </Accordion>

  <Accordion title="Q: Why does the context window differ from the model specification?">
    Check the model's `contextWindow`: use `1000000` for `step-5-preview` and `256000` for `step-3.7-flash`. Reload the model list after saving and select the model again.
  </Accordion>
</AccordionGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.