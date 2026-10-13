> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code

This guide explains how to connect Step models to Claude Code through the [Messages API](/docs/en/api-reference/chat/messages-create), configure Step Plan, reasoning effort, and a 1M context window, and verify conversations and tool calls.

## Requirements

### Environment

* macOS, Linux, or Windows. On Windows, use PowerShell or run Claude Code inside WSL.
* The npm installation method below requires Node.js 22 or later. Skip it if you already installed Claude Code with a native installer.

Before installing through npm, check that Node.js and npm are available:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
node -v
npm -v
```

### Subscribe to Step Plan

Confirm that your [Step Plan subscription](https://platform.stepfun.ai/step-plan) is active, has available quota, and provides access to the model. The configuration examples in this guide use the Step Plan channel.

### Get a Step API Key

Create an API key on the [Step platform API keys page](https://platform.stepfun.ai/interface-key).

## Configuration Steps

### Install Claude Code

Run the following command in your terminal:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
npm install -g @anthropic-ai/claude-code
```

After installation, verify the version:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
claude --version
```

Client compatibility was checked with **Claude Code 2.1.209**. The installation command installs the latest release; model alias resolution and context handling can vary by version.

### Create the Configuration File

<Tabs>
  <Tab title="Quick setup with the script">
    The commands below download the English scripts from the official Step repository, `stepfun-ai/Step-Cookbook`, and execute them only after a successful download.

    macOS / Linux / WSL (Bash)

    Install `jq` before running the Bash script. The script uses it to update the JSON configuration.

    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl -fsSL https://raw.githubusercontent.com/stepfun-ai/Step-Cookbook/main/scripts/claude-key-setup/en/configure_claude.sh -o configure_claude.sh &&
      bash configure_claude.sh
    ```

    Windows (PowerShell)

    Run the following commands in a regular PowerShell session as your current user. Administrator privileges are not required.

    ```powershell theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    & {
      $ErrorActionPreference = "Stop"
      Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
      Invoke-WebRequest -Uri "https://raw.githubusercontent.com/stepfun-ai/Step-Cookbook/main/scripts/claude-key-setup/en/configure_claude.ps1" -OutFile "configure_claude.ps1"
      & .\configure_claude.ps1
    }
    ```

    Select option **2** for **StepFun Step Plan (subscription)**, then enter your API key and model name when prompted. The script backs up an existing configuration, replaces the entire `env` object, and preserves other top-level fields. Any additional variables previously stored inside `env` are removed. Restart Claude Code after setup.
  </Tab>

  <Tab title="Edit the configuration file manually">
    Merge the following fields into the user-level `~/.claude/settings.json` file, preserving existing `permissions`, `hooks`, and other settings. On Windows, the path is `%USERPROFILE%\.claude\settings.json`. If `CLAUDE_CONFIG_DIR` is set, use `settings.json` in that directory. Create the directory if needed, then save the JSON below with `YOUR_STEP_API_KEY` replaced by your key:

    ```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    {
      "env": {
        "ANTHROPIC_AUTH_TOKEN": "YOUR_STEP_API_KEY",
        "ANTHROPIC_BASE_URL": "https://api.stepfun.ai/step_plan"
      },
      "model": "step-5-preview"
    }
    ```

    Model IDs include `step-5-preview`, `step-3.7-flash`, `step-3.5-flash-2603`, and `step-3.5-flash`.

    #### Configuration Fields

    | Field | Location | Purpose |
    | - | - | - |
    | `ANTHROPIC_AUTH_TOKEN` | `env` | Step API key for request authentication. |
    | `ANTHROPIC_BASE_URL` | `env` | Set to `https://api.stepfun.ai/step_plan`; Claude Code appends `/v1/messages`. |
    | `model` | Top level | Main conversation model; `--model` or `ANTHROPIC_MODEL` can override it. |
    | `ANTHROPIC_DEFAULT_OPUS_MODEL` and related aliases | `env`, optional | Map built-in model tiers to Step models. |
    | `CLAUDE_CODE_SUBAGENT_MODEL` | `env`, optional | Set the subagent model. |
    | `CLAUDE_CODE_MAX_CONTEXT_TOKENS` | `env`, optional | Override the client's assumed context window for a custom model. |
    | `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | `env`, optional | Set the auto-compaction window, capped at the model context window. |

    Optionally merge the following model aliases and subagent setting into `env`. Check models explicitly assigned to tasks separately.

    ```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    {
      "ANTHROPIC_DEFAULT_SONNET_MODEL": "step-5-preview",
      "ANTHROPIC_DEFAULT_OPUS_MODEL": "step-5-preview",
      "ANTHROPIC_DEFAULT_HAIKU_MODEL": "step-5-preview",
      "ANTHROPIC_DEFAULT_FABLE_MODEL": "step-5-preview",
      "CLAUDE_CODE_SUBAGENT_MODEL": "step-5-preview"
    }
    ```

    Verify the minimum configuration first, then add aliases and subagent settings as needed. If a background task still requests a built-in model name, check whether the task explicitly selects another model.

    When the same variable is set in a settings file's `env` and in the terminal, the settings value replaces the terminal value. After switching providers, check user settings, project settings, and shell profiles such as `.zshrc` or `.bashrc` for old URLs and credentials, then restart Claude Code.
  </Tab>
</Tabs>

### Set Reasoning Effort

`step-5-preview` supports the following reasoning effort levels:

| --effort | Suitable tasks |
| - | - |
| `low` | Simple tasks, prioritizing speed and lower token usage. |
| `medium` | General reasoning and multi-step tasks. |
| `high` | Complex reasoning, planning, and code analysis. |

For Step 5 Preview, Step maps `xhigh` and `max` to `high`. Claude Code sends the setting through the Messages API field `output_config.effort`.

Set the effort level when starting a session:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
claude --model step-5-preview --effort medium
```

To save a default, merge `effortLevel` into the top level of `~/.claude/settings.json`, not into `env`:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "effortLevel": "medium"
}
```

Restart Claude Code after saving. If the setting does not take effect, check `CLAUDE_CODE_EFFORT_LEVEL`, launch flags, and project or organization settings.

### Enable 1M Context

[`step-5-preview`](/docs/en/guides/models/step-5-preview) has a **1M-token** context window. If `/context` treats it as an unrecognized model with a 200k window, merge the following fields into `~/.claude/settings.json`, preserving your existing configuration:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "YOUR_STEP_API_KEY",
    "ANTHROPIC_BASE_URL": "https://api.stepfun.ai/step_plan",
    "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "1000000",
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000"
  },
  "model": "step-5-preview"
}
```

Notes:

* `CLAUDE_CODE_MAX_CONTEXT_TOKENS` tells Claude Code to measure usage against a 1M window. Use the plain number `1000000`. Do not write `1M` or `1000k`.
* `CLAUDE_CODE_AUTO_COMPACT_WINDOW` aligns the auto-compact window to 1M. Valid range is `100000`–`1000000`, also as a plain number. Claude Code reserves space for output and internal processing, so compaction may occur before the window is full.
* Save the file, fully quit and restart Claude Code, then run `/context` and confirm the window is close to 1M instead of 200k.
* After you declare a window above 200k, a startup message such as "200K limit isn't enforced" is expected.

The official setup script does not write these two fields. Add them to `env` yourself after running the script.

### Start Claude Code

Enter any code project directory:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
cd your-project
```

Start Claude Code:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
claude
```

If `Do you want to use this API key?` appears on first launch, select `Yes`.

## Test the Integration

### Verify Client Conversations

1. Save the configuration, quit Claude Code completely, and restart it.
2. Run `/status` to check the model, authentication, and configuration source.
3. Send "Reply only with OK." Check the returned text and streaming output.

### Verify Agent Tool Calls

Use a separate test directory on a machine with Python installed. Create `hello.py` containing a statement that prints `Hello, world!`, then send Claude Code this task:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Read hello.py in the current directory and add a command-line argument named name.
Print Hello, Step5 when no argument is provided, and Hello, Ada when the argument is Ada.
Use an available Python interpreter to run both cases and check their output.
If validation fails, fix the error and run it again. Do not modify other files.
Report the file changes, commands, and execution results.
```

Approve the required operations, then check the file-reading, editing, and execution records and both outputs. Ask a follow-up question to confirm that the conversation retains the task context.

### Verify Usage and Routing

In the [Step platform](https://platform.stepfun.ai), match request time, model, and response ID to confirm that the call used Step Plan and its quota.

## Common Issues

<AccordionGroup>
  <Accordion title="Q: Why do configuration changes not take effect?">
    Restart and run `/status` to check the model, authentication, and configuration source. Check project settings, `--model`, `ANTHROPIC_MODEL`, `CLAUDE_CONFIG_DIR`, and organization settings. Confirm that `settings.json` is valid JSON.

    This Bash / jq command shows relevant settings and whether credentials exist without printing their values:

    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    jq '{model, base_url: .env.ANTHROPIC_BASE_URL, context_window: .env.CLAUDE_CODE_MAX_CONTEXT_TOKENS, compact_window: .env.CLAUDE_CODE_AUTO_COMPACT_WINDOW, has_auth_token: (.env.ANTHROPIC_AUTH_TOKEN != null), has_api_key: (.env.ANTHROPIC_API_KEY != null)}' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"
    ```
  </Accordion>

  <Accordion title="Q: How do I resolve 401 invalid_api_key?">
    Put a valid Step API key in `ANTHROPIC_AUTH_TOKEN`. Check for typing errors, revoked keys, or a key from another site. If `ANTHROPIC_API_KEY` is also set, do not update only that variable while leaving an old `ANTHROPIC_AUTH_TOKEN`.

    If you previously signed in to another account with `/login`, use `/status` to check the credential source. To leave that login session, run `/logout`, restart, and verify the Step configuration again.
  </Accordion>

  <Accordion title="Q: How do I test the Messages API independently?">
    Use curl to check the endpoint, key, and model first. The command below uses Bash or Zsh; on Windows, run it in WSL or Git Bash.

    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    export STEP_API_KEY="YOUR_STEP_API_KEY"

    curl --silent --show-error --fail-with-body \
      --write-out '\nHTTP %{http_code}\n' \
      https://api.stepfun.ai/step_plan/v1/messages \
      -H "Authorization: Bearer ${STEP_API_KEY}" \
      -H "Content-Type: application/json" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "model": "step-5-preview",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": "Reply only with OK."}]
      }'
    ```

    **Pass criteria:** HTTP 200, response `type` is `message`, and `content` includes a `text` block containing `OK`. If only `thinking` blocks are returned with `stop_reason: max_tokens`, increase the output budget and retry.
  </Accordion>

  <Accordion title="Q: What if the URL fails, or curl works but Claude Code does not?">
    Claude Code appends `/v1/messages` to `ANTHROPIC_BASE_URL`. Check the URL against this table:

    | ANTHROPIC\_BASE\_URL | Request path | Result |
    | - | - | - |
    | `https://api.stepfun.ai/step_plan` | `/step_plan/v1/messages` | Step Plan Messages channel. |
    | `https://api.stepfun.ai/step_plan/v1` | `/step_plan/v1/v1/messages` | Duplicated `/v1`; incorrect URL. |
    | `https://api.stepfun.ai/step_plan/v1/messages` | `/step_plan/v1/messages/v1/messages` | Duplicated API path; incorrect URL. |
    | `https://api.stepfun.ai` | `/v1/messages` | Standard pay-as-you-go API; does not use Step Plan quota. |

    If curl works but the client fails, check whether project or user settings override terminal variables. Use `claude --debug` to inspect logs when further diagnosis is needed.
  </Accordion>

  <Accordion title="Q: Why do background tasks or subagents report model errors?">
    Check `ANTHROPIC_DEFAULT_HAIKU_MODEL`, `ANTHROPIC_DEFAULT_FABLE_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL`, and models explicitly assigned to tasks. They must use available Step model IDs. See the configuration fields above.
  </Accordion>

  <Accordion title="Q: Why does /context still show 200k?">
    Confirm that the model is `step-5-preview`, that you edited the correct configuration directory, and that `CLAUDE_CODE_MAX_CONTEXT_TOKENS` and `CLAUDE_CODE_AUTO_COMPACT_WINDOW` in `env` both equal `"1000000"`. Quit completely and restart. The setup script does not write these fields by default.
  </Accordion>

  <Accordion title="Q: How do I resolve model does not exist?">
    Check the model ID, account permissions, target channel, and subagent models. A client warning about an unrecognized custom model is not the same as a server rejection; inspect the actual request error.
  </Accordion>

  <Accordion title="Q: How do I resolve 402 quota_exceeded?">
    Confirm the request channel first. Check subscription status and Credits for Step Plan, or account balance and credits for the standard API.
  </Accordion>
</AccordionGroup>

For further help, provide the client version, error details, time of the failure, redacted configuration, and request ID to support.

## Related Documentation

* [Messages API](/docs/en/api-reference/chat/messages-create)
* [Step 5 Preview](/docs/en/guides/models/step-5-preview)
* [Step Plan Overview](/docs/en/step-plan/overview)


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.