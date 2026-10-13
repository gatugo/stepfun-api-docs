> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Kilo Code

Kilo Code is a coding agent for editors such as VS Code and Cursor, with support for multiple model providers, code changes, debugging, and terminal tasks. Its Step Plan provider connects these workflows to Step models.

## Prerequisites

* VS Code or Cursor installed. The Python verification example also requires Python 3.
* An active [Step Plan subscription](https://platform.stepfun.ai/step-plan) with available quota and access to the selected model.
* An API key from the [StepFun platform API keys page](https://platform.stepfun.ai/interface-key).

## Install Kilo Code

Find Kilo Code in your editor's extension marketplace and install it. The extension ID is `kilocode.kilo-code`. These steps use a version with `Providers` and `Models` settings pages.

## Configure Step Plan

### Connect the built-in provider

1. Open Kilo Code settings, select `Providers`, then choose `StepFun Step Plan (Global)`.
2. Enter your API key and click `Submit`. Do not include a `Bearer ` prefix or leading or trailing spaces in the API Key field.
3. Under `Settings > Models > Default Model`, select Step 5 Preview from that provider. Its model ID is `step-5-preview`.
4. Save and start a new task. Keep the built-in provider's model presets.

### Use a custom provider

If the Step Plan preset or your target model is missing, open `Providers > Custom provider` and enter:

| Setting | Value |
| - | - |
| `Provider ID` | `step-plan` |
| `Display name` | `Step Plan` |
| `Provider API` | `OpenAI Compatible` |
| `Base URL` | `https://api.stepfun.ai/step_plan/v1` |
| `API key` | Your Step API key, without a `Bearer ` prefix. |
| `Models` | Select or add `step-5-preview`. |

Click `Submit`, then select the model under your custom provider. This configuration uses Chat Completions at `/step_plan/v1/chat/completions`.

Manually added models also need context and output capacity information. If these fields are missing, merge the following into `kilo.json` or `kilo.jsonc`, preserving the provider's existing connection and authentication settings:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "provider": {
    "step-plan": {
      "models": {
        "step-5-preview": {
          "name": "Step 5 Preview",
          "limit": {
            "context": 1000000,
            "output": 65536
          }
        }
      }
    }
  }
}
```

These capacities apply to [Step 5 Preview](/docs/en/guides/models/step-5-preview). Match them to the model when switching. Reasoning models need room for both reasoning and visible output; a small output budget may produce empty or truncated text.

## Connect StepSearch MCP

StepSearch provides `web_search` and `web_fetch` through the Step Plan endpoint for web searches and page retrieval.

### Set the authentication variable

Fully quit the editor, then set the key and start the editor from your project's terminal. Replace `YOUR_STEP_API_KEY` with your key. For Cursor, replace `code .` with `cursor .`.

<Tabs>
  <Tab title="macOS / Linux / WSL">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    export STEP_API_KEY="YOUR_STEP_API_KEY"
    code .
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    $env:STEP_API_KEY = "YOUR_STEP_API_KEY"
    code .
    ```
  </Tab>
</Tabs>

If the editor command is unavailable, configure its command-line launcher first. The environment variable applies to this terminal and processes it starts. Make sure the editor can read `STEP_API_KEY` whenever you use this MCP server.

### Add the MCP server

1. Open `MCP Servers` in Kilo Code settings.
2. Edit `kilo.json` in the current project. If the project already uses `kilo.jsonc` or one of these files under `.kilo/`, merge into that file instead, preserving other settings:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "mcp": {
    "step-search": {
      "type": "remote",
      "url": "https://api.stepfun.ai/step_plan/v1/mcp/web_search/mcp",
      "headers": {
        "Authorization": "Bearer {env:STEP_API_KEY}"
      },
      "oauth": false,
      "enabled": true
    }
  }
}
```

3. Save and reconnect the server. Confirm that `step-search` is connected and lists `web_search` and `web_fetch`.
4. Start a new task using either tool, approve the call when prompted, and inspect the returned result.

The current format uses the top-level `mcp` key, `type: "remote"`, and `{env:STEP_API_KEY}` for environment-variable substitution. Remote connections try Streamable HTTP first and fall back to SSE if needed. This example authenticates through a request header, not OAuth.

<Warning>
  Keep the environment-variable reference in the project configuration. Do not replace it with a real key and commit the file. Anyone with the key may make requests using your permissions and consume quota.
</Warning>

## Verify the integration

### Test a conversation

Start a new task and enter `Reply only with OK.` Expected output: `OK`.

### Test tool calls

1. Create a separate test directory with a `README.md` containing `Kilo Code Step Plan test`, then open it in the editor.
2. Start a new task and enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Read README.md and create hello.py that prints "Hello, world!".
Run hello.py with an available Python interpreter and report the command and actual output.
Do not change README.md or any other existing files.
```

3. Approve the required file operations and commands. Inspect the tool records, confirm that `hello.py` exists and prints `Hello, world!`, and check that `README.md` is unchanged.

### Check saved settings

Restart the editor, confirm that the provider and model selection are retained, and start another short conversation.

## Common questions

<AccordionGroup>
  <Accordion title="Q: What if the Step Plan provider or Step 5 Preview is missing?">
    Update Kilo Code and check the provider list. Alternatively, open `Providers > Custom provider`, select `OpenAI Compatible`, enter the Step Plan base URL, and add `step-5-preview`. Save and select the model under that custom provider.
  </Accordion>

  <Accordion title="Q: What should I check after a Connection error or 401 response?">
    Inspect the full error, network connection, base URL, API key, and model permissions. Custom providers use `https://api.stepfun.ai/step_plan/v1`. The key must be complete, valid, and associated with the account for this endpoint. Use the server response to distinguish authentication, model, and request-parameter failures.
  </Accordion>

  <Accordion title="Q: Why is the response empty or truncated?">
    Check the stop reason and output budget. Reasoning may consume the budget before visible text is produced. Restore presets for a built-in model, or check capacity and request settings for a custom model, then adjust based on the actual error.
  </Accordion>

  <Accordion title="Q: Do I need the older Include max output tokens setting?">
    `Include max output tokens` and `Max Output Tokens = -1` belong to an older interface, not the current built-in provider setup. Current custom models describe capacity with `limit.context` and `limit.output`. Use valid capacities for your model rather than copying `-1` into `limit.output`.
  </Accordion>

  <Accordion title="Q: How should I handle an older .kilocode/mcp.json configuration?">
    The current setup uses `mcp` in `kilo.json` or `kilo.jsonc`. Migrate older `mcpServers`, `streamable-http`, and `disabled` fields to the current format, or keep a configuration matched to the older extension version. Do not mix the two schemas.
  </Accordion>

  <Accordion title="Q: Why is step-search or its tool list missing?">
    Check that you edited the configuration file loaded by the current project, with `type: "remote"` and `enabled: true`. Confirm that the editor process can read `STEP_API_KEY` and the header is `Bearer {env:STEP_API_KEY}`. Save, reconnect, and inspect the server log.
  </Accordion>

  <Accordion title="Q: Why does the model reply without performing file or terminal operations?">
    Open the target project, select a mode that allows file changes, and check for pending tool approvals. Approve the required operations; enabling every auto-approval option is unnecessary.
  </Accordion>
</AccordionGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.