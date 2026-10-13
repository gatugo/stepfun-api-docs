> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Roo Code

Roo Code is a coding agent for editors such as VS Code and Cursor, with file editing, terminal commands, and multi-step tool use. Its OpenAI Compatible provider connects to Step Plan through the Chat Completions API.

## Prerequisites

* VS Code or Cursor installed. The repair-and-test example also requires Python 3.
* An active [Step Plan subscription](https://platform.stepfun.ai/step-plan) with available quota and access to the selected model.
* An API key from the [StepFun platform API keys page](https://platform.stepfun.ai/interface-key).

## Install Roo Code

Find Roo Code in your editor's extension marketplace and check that its extension ID is `RooVeterinaryInc.roo-cline`. These settings apply to Roo Code 3.54.0. The upstream repository is archived, so check compatibility with your editor version.

## Configure Step Plan

### Configure the connection

1. Open the Roo Code panel and select `Providers` in settings.
2. Select `OpenAI Compatible` under `API Provider` and enter:

| Setting | Value |
| - | - |
| `API Provider` | `OpenAI Compatible` |
| `Base URL` | `https://api.stepfun.ai/step_plan/v1` |
| `API Key` | Your Step API key, without a `Bearer ` prefix or leading or trailing spaces. |
| `Model ID` | `step-5-preview` |

Roo Code appends `/chat/completions`, producing `/step_plan/v1/chat/completions`. Keep the base URL ending at `/step_plan/v1` rather than using the standard pay-as-you-go API address.

Roo Code 3.54.0 requires OpenAI-native tool calling and has no XML fallback. Select a model that supports function calling, such as [Step 5 Preview](/docs/en/guides/models/step-5-preview), used below.

### Check model settings

Expand `Model Configuration` and set the capabilities for Step 5 Preview:

| Setting | Value | Description |
| - | - | - |
| `Enable streaming` | Enabled | Use streamed responses. |
| `Context Window Size` | `1000000` | Context window used by the client. |
| `Include max output tokens` | `Off` | Omit an additional output limit from requests. |
| `Max Output Tokens` | `-1` | Use with the preceding option disabled, leaving output length to the service. |
| `Image Support` | Enabled | Allow image input. |

Version 3.54.0 sends `max_completion_tokens` when `Include max output tokens` is enabled. Disable that option for this configuration rather than changing the token value alone. If you set an output limit, leave enough room for reasoning and visible text.

Match the context window and input capabilities to the selected model when switching. Save the settings and start a new task.

## Connect StepSearch MCP

StepSearch provides `web_search` and `web_fetch` through the Step Plan endpoint. Add it when you need web searches or page retrieval.

1. Open `MCP Servers` in the Roo Code panel and choose to edit the global MCP configuration.
2. Merge the following entry, preserving other servers. Replace `YOUR_STEP_API_KEY` with your key:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "mcpServers": {
    "step-search": {
      "type": "streamable-http",
      "url": "https://api.stepfun.ai/step_plan/v1/mcp/web_search/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_STEP_API_KEY"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

3. Save and reconnect the server. Confirm that `step-search` is connected and lists `web_search` and `web_fetch`.
4. Start a task using either tool, approve the call when prompted, and inspect the returned result.

Roo Code requires an explicit `type` for URL-based MCP configurations. Use `streamable-http`, not Cline's `streamableHttp`. With `alwaysAllow: []`, approve each tool call when prompted.

The MCP configuration stores the API key in plain text. Do not commit or share a file containing a real key.

## Verify the integration

### Test a conversation

Start a new task and enter `Reply only with OK.` Expected output: `OK`.

### Test a repair

1. Create a separate test directory with the two files below. The addition function in `calc.py` intentionally contains a bug.

`calc.py`:

```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
def add(left, right):
    return left - right
```

`test_calc.py`:

```python theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
import unittest

from calc import add


class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
```

2. Open the directory in your editor, select `Code` mode to allow file changes, and send Roo Code this task:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Work only in this directory. Read calc.py and test_calc.py, then fix the bug causing test_add to fail.
Run python3 -m unittest test_calc -v. If it fails, fix the implementation and run the test again.
Do not change test_calc.py or other files. Report the change, command, and test result.
```

3. Approve the required file operations and commands. Confirm that `calc.py` now adds correctly, the test reports `OK`, and `test_calc.py` is unchanged.

Manual approval is sufficient; enabling every auto-approval option is unnecessary.

### Check saved settings

Restart the editor, confirm that the provider and model selection are retained, and start another short conversation.

## Common questions

<AccordionGroup>
  <Accordion title="Q: Why does the task stay on API Request...?">
    Check the extension-host log for `Could not find ripgrep binary`. In VS Code, run `Developer: Open Logs Folder` from the command palette and open the current window's `exthost/exthost.log`. Use the ripgrep workaround below only when that error is present. Otherwise, inspect the actual network, authentication, or request error.
  </Accordion>

  <Accordion title="Q: How can I resolve a missing ripgrep binary in Roo Code 3.54.0?">
    Version 3.54.0 does not search the `ripgrep-universal` layout used by some newer VS Code versions. Changing the workspace or user configuration directory does not change the editor installation path that Roo searches.

    For VS Code on macOS, the following temporary workaround adds a symbolic link inside the application installation. It detects Apple Silicon or Intel and refuses to overwrite an existing target. If the source binary is missing or the installation directory is not writable, stop rather than rerunning with elevated privileges.

    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    (
      set -eu
      APP="/Applications/Visual Studio Code.app/Contents/Resources/app"
      case "$(uname -m)" in
        arm64) ARCH="darwin-arm64" ;;
        x86_64) ARCH="darwin-x64" ;;
        *) printf '%s\n' 'Unsupported architecture'; exit 1 ;;
      esac
      RG="$APP/node_modules.asar.unpacked/@vscode/ripgrep-universal/bin/$ARCH/rg"
      TARGET="$APP/node_modules/@vscode/ripgrep/bin/rg"
      if [ ! -x "$RG" ]; then
        printf '%s\n' 'Bundled ripgrep was not found at the expected path.'
        exit 1
      fi
      if [ -e "$TARGET" ] || [ -L "$TARGET" ]; then
        printf '%s\n' 'The target already exists; no changes were made.'
        exit 1
      fi
      mkdir -p "$(dirname "$TARGET")"
      ln -s "$RG" "$TARGET"
      "$TARGET" --version
    )
    ```

    Run `Developer: Reload Window` afterward and start the task again. This command targets the stated VS Code installation on macOS; check the actual installation paths for Cursor or other systems. Editor updates may remove the link, so check again if the same log error returns.
  </Accordion>

  <Accordion title="Q: What should I check after a Connection error or 401 response?">
    Check the network connection, base URL, API key, and model permissions. Use `https://api.stepfun.ai/step_plan/v1` and a complete, valid key from the account for that endpoint. The model connection's API Key field takes the raw key, while the MCP `Authorization` header requires a `Bearer ` prefix.
  </Accordion>

  <Accordion title="Q: Why is the response empty, truncated, or missing visible text during reasoning?">
    Reasoning may produce no visible text until it completes. If the request finishes without text, inspect the stop reason, errors, and output settings. Confirm that `Include max output tokens` is disabled. If you set a budget deliberately, a small value may be exhausted by reasoning before visible output begins.
  </Accordion>

  <Accordion title="Q: Why does the model only reply with text, or why do tool calls fail?">
    Select a mode such as `Code` that allows task execution, open the target directory, and approve the required operations. The model must support OpenAI-native tool calling. Check the model ID and full error after a tool failure, and use tool records to verify execution rather than relying on the model's description.
  </Accordion>

  <Accordion title="Q: Why is step-search missing or timing out?">
    Check that the entry is under `mcpServers`, `type` is `streamable-http`, `disabled` is `false`, and the authorization header contains the complete key with a `Bearer ` prefix. Save, reconnect, and inspect the network and server logs. Distinguish authentication, connectivity, and transport failures before attributing a timeout to the client version.
  </Accordion>
</AccordionGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.