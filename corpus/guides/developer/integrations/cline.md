> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Cline

Cline is a coding agent for editors such as VS Code and Cursor, with Plan and Act modes, file editing, and terminal command execution. Its Step Plan provider connects the editor to Step models.

## Prerequisites

* VS Code or Cursor installed. The Python verification example also requires Python 3.
* An active [Step Plan subscription](https://platform.stepfun.ai/step-plan) with available quota and access to the selected model.
* An API key from the [StepFun platform API keys page](https://platform.stepfun.ai/interface-key).

## Install Cline

Find Cline in your editor's extension marketplace and install it. The extension ID is `saoudrizwan.claude-dev`.

## Configure Step Plan

### Select the provider

1. Open the Cline panel and select `API Configuration` in settings. On first launch, select `Configure your provider`.
2. Select `StepFun Step Plan (Global)` under `API Provider`.
3. Enter your API key and select `step-5-preview`. Check the remaining connection settings below.

| Setting | Value |
| - | - |
| `API Provider` | `StepFun Step Plan (Global)` |
| `Base URL` | `https://api.stepfun.ai/step_plan/v1`. Confirm that the preset uses this address. |
| `API Key` | Your Step API key, without a `Bearer ` prefix or leading or trailing spaces. Some versions label this field `OpenAI Compatible API Key`. |
| `Model ID` | `step-5-preview` |

If your version does not include a Step Plan preset, select `OpenAI Compatible` and enter the same base URL, API key, and model ID. Cline appends `/chat/completions`, producing `/step_plan/v1/chat/completions`.

### Check model settings

Expand `MODEL CONFIGURATION`. These settings apply to [Step 5 Preview](/docs/en/guides/models/step-5-preview). When using a preset, check its existing values.

| Setting | Value | Description |
| - | - | - |
| `Supports Images` | Enabled | Allows image input. |
| `Context Window` | `1000000` | Context window used by the client. |
| `Max Output Tokens` | `65536` | Leaves room for reasoning and visible output. Avoid setting a very small budget. |
| `Input / Output Price / 1M` | Default | Used for Cline's cost estimates; actual usage is determined by the platform. |
| `Temperature` | Default | No change is needed for this setup. |
| `Reasoning Effort` | Default, or `High` | Increase when the task needs more reasoning. Step 5 Preview supports `low`, `medium`, and `high`. |

When switching models, match the context window and output budget to the selected model. Save the settings and start a new task.

## Connect StepSearch MCP

StepSearch provides `web_search` and `web_fetch` through the Step Plan endpoint. Add it when you need web searches or page retrieval.

1. Open `MCP Servers` in the Cline panel, select `Configure`, then choose `Configure MCP Servers`.
2. Merge the following configuration into `cline_mcp_settings.json`, preserving other servers. Replace `YOUR_STEP_API_KEY` with your key:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "mcpServers": {
    "step-search": {
      "type": "streamableHttp",
      "url": "https://api.stepfun.ai/step_plan/v1/mcp/web_search/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_STEP_API_KEY"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

3. Save the file. Confirm that `step-search` is connected and its tool list includes `web_search` and `web_fetch`.
4. Start a new task and ask Cline to use either tool. Inspect the tool call and returned result.

Use Cline's exact `streamableHttp` spelling for `type`. Omitting it selects the legacy SSE transport. With `autoApprove: []`, approve tool calls when prompted.

<Warning>
  The MCP configuration stores the API key in plain text. Keep it in Cline's user configuration and do not commit or share the key. Anyone with the key may make requests using your permissions and consume quota.
</Warning>

## Verify the integration

### Test a conversation

Start a new task and enter `Reply only with OK.` Expected output: `OK`.

### Test tool calls

1. Create a separate test directory with a `README.md` containing `Cline Step Plan test`, then open it in the editor.
2. Select `Act` mode in Cline and enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Read README.md and create hello.py that prints "Hello, world!".
Run hello.py with an available Python interpreter and report the command and actual output.
Do not change README.md or any other existing files.
```

3. Approve the required file operations and commands. Inspect the tool records, confirm that `hello.py` exists and prints `Hello, world!`, and check that `README.md` is unchanged.

Auto-approval is optional. Manual approval is sufficient for this test.

### Check saved settings

Restart the editor, confirm that the provider and model selection are retained, and start another short conversation.

## Common questions

<AccordionGroup>
  <Accordion title="Q: What if the Step Plan provider is missing?">
    Update Cline, or select `OpenAI Compatible` with `https://api.stepfun.ai/step_plan/v1`, your API key, and `step-5-preview` or another model available to your account.
  </Accordion>

  <Accordion title="Q: What should I check after a Connection error?">
    Check the base URL, network connection, API key, and model permissions. The base URL ends at `/step_plan/v1`; do not add `Bearer ` to the API Key field. Use the full error to distinguish authentication, model, and request-parameter failures. A successful model-list request still needs a conversation test.
  </Accordion>

  <Accordion title="Q: What should I check after a 401 response?">
    Confirm that the key is complete, valid, and free of leading or trailing spaces, and belongs to the account for this endpoint. Enter the raw key in the model connection settings. The MCP header instead requires `Authorization: Bearer YOUR_STEP_API_KEY`.
  </Accordion>

  <Accordion title="Q: Why does Cline reply without editing files or running commands?">
    Select `Act` mode and open the target project. Check for pending tool approvals and approve the required operations. You do not need to enable all auto-approval options. Start a new task if you have just changed the configuration.
  </Accordion>

  <Accordion title="Q: Why is the response empty, truncated, or missing visible text during reasoning?">
    Reasoning may produce no visible text until it completes. If the request finishes without text, inspect the stop reason, errors, and output budget. A small budget may be exhausted before visible output begins. For Step 5 Preview, check the model settings above before adjusting them based on the error.
  </Accordion>

  <Accordion title="Q: Why is step-search or its tool list missing?">
    Check that the configuration is under `mcpServers`, `type` is `streamableHttp`, `disabled` is `false`, and the authorization header contains the `Bearer ` prefix and complete key. Save, reconnect the server, and inspect its connection log.
  </Accordion>
</AccordionGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.