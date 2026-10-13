> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Codex CLI

Codex CLI is OpenAI's open-source terminal coding agent for reading files, editing code, and running commands in local projects. A custom provider connects it to Step Plan models.

## Prerequisites

* Node.js, npm, `curl`, and Python 3 installed. The shell commands below use Bash or zsh; on Windows, run them in WSL.
* An active [Step Plan subscription](https://platform.stepfun.ai/step-plan) with available quota and access to the selected model.
* An API key from the [StepFun platform API keys page](https://platform.stepfun.ai/interface-key).

## Connection requirements

* Codex CLI 0.154.0 supports the Responses API with `wire_api = "responses"`. Step Plan exposes `/step_plan/v1/responses`, so no protocol-conversion proxy is needed. Chat Completions is not supported by this Codex version.
* User configuration belongs in `$CODEX_HOME/config.toml`. `CODEX_HOME` defaults to `~/.codex`. Supply the API key through an environment variable or `.env` in that directory, not in `config.toml`.
* Codex's built-in catalog primarily supplies metadata for OpenAI models. The `model_catalog_json` configuration below defines Step model names, context windows, and input capabilities so the models appear in `/model`. A dedicated Step profile limits the catalog override to Step sessions.

## Install Codex CLI

Install Codex CLI 0.154.0:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
npm install -g @openai/codex@0.154.0
```

Check the installed version:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
codex --version
```

Expected output: `codex-cli 0.154.0`.

## Configure Step Plan

### Set the configuration directory

Preserve an existing `CODEX_HOME` value, or use the default directory if it is unset:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME"
export CODEX_HOME="$(cd "$CODEX_HOME" && pwd)"
```

To keep the setup separate from your existing configuration, use a dedicated directory before continuing:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
export CODEX_HOME="$HOME/.codex-step-plan"
mkdir -p "$CODEX_HOME"
```

Complete the remaining steps in the same terminal. When using the dedicated directory in a later session, set `CODEX_HOME` again before starting Codex.

### Add the provider

Merge this configuration into `$CODEX_HOME/config.toml`, preserving existing settings. If `[model_providers.stepfun]` already exists, update that table instead of adding a duplicate.

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
[model_providers.stepfun]
name = "StepFun Step Plan"
base_url = "https://api.stepfun.ai/step_plan/v1"
env_key = "STEP_API_KEY"
wire_api = "responses"
```

| Field | Description |
| - | - |
| `model_providers.stepfun` | Provider identifier, selected with `model_provider = "stepfun"`. |
| `base_url` | Step Plan base URL. Codex appends `/responses`, producing `/step_plan/v1/responses`. |
| `env_key` | Name of the environment variable containing the API key, not the key itself. |
| `wire_api` | Set to `responses` to use the Responses API. |

Define the provider in user-level configuration. Codex ignores `model_provider` and `model_providers` in a project's `.codex/config.toml`. The built-in identifiers `openai`, `ollama`, and `lmstudio` are reserved.

### Set the API key

Replace `YOUR_STEP_API_KEY` with your key and use either method below.

Set an environment variable in the terminal that starts Codex:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
export STEP_API_KEY="YOUR_STEP_API_KEY"
```

Alternatively, add or update the following entry in `$CODEX_HOME/.env`, which Codex loads at startup:

```dotenv theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
STEP_API_KEY=YOUR_STEP_API_KEY
```

Restrict access to the file:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
chmod 600 "$CODEX_HOME/.env"
```

`.env` stores the API key in plain text. Do not commit or share the file.

### Create the model catalog

1. Download the default agent instructions for Codex CLI 0.154.0. The catalog uses this content as `base_instructions`:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
curl -fsSL https://raw.githubusercontent.com/openai/codex/rust-v0.154.0/codex-rs/protocol/src/prompts/base_instructions/default.md \
  -o "$CODEX_HOME/default.md"
```

2. Confirm that the file is not empty:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
test -s "$CODEX_HOME/default.md" && wc -c "$CODEX_HOME/default.md"
```

3. Generate `$CODEX_HOME/step-catalog.json`:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
python3 - <<'PY'
import json
import os

home = os.environ["CODEX_HOME"]

with open(os.path.join(home, "default.md"), encoding="utf-8") as instructions_file:
    base_instructions = instructions_file.read()

def entry(slug, name, description, context_window, input_modalities):
    return {
        "slug": slug,
        "display_name": name,
        "description": description,
        "context_window": context_window,
        "input_modalities": input_modalities,
        "base_instructions": base_instructions,
        "visibility": "list",
        "supported_in_api": True,
        "priority": 1,
        "availability_nux": None,
        "upgrade": None,
        "default_reasoning_level": "medium",
        "supported_reasoning_levels": [
            {"effort": "low", "description": "Lower reasoning effort"},
            {"effort": "medium", "description": "Medium reasoning effort (default)"},
            {"effort": "high", "description": "Higher reasoning effort"},
        ],
        "supports_reasoning_summaries": True,
        "default_reasoning_summary": "auto",
        "support_verbosity": False,
        "default_verbosity": None,
        "apply_patch_tool_type": "freeform",
        "web_search_tool_type": "text",
        "shell_type": "shell_command",
        "truncation_policy": {"mode": "tokens", "limit": 10000},
        "supports_parallel_tool_calls": False,
        "supports_image_detail_original": False,
        "effective_context_window_percent": 95,
        "experimental_supported_tools": [],
        "supports_search_tool": False,
    }

models = [
    entry("step-5-preview", "Step 5 Preview", "StepFun 1M multimodal", 1000000, ["text", "image"]),
    entry("step-3.7-flash", "Step 3.7 Flash", "StepFun 256K", 256000, ["text", "image"]),
    entry("step-3.5-flash", "Step 3.5 Flash", "StepFun 256K", 256000, ["text"]),
]

catalog_path = os.path.join(home, "step-catalog.json")

with open(catalog_path, "w", encoding="utf-8") as catalog_file:
    json.dump({"models": models}, catalog_file, ensure_ascii=False, indent=2)

print("Created:", catalog_path)
print("Models:", [model["slug"] for model in models])
PY
```

The output should list `step-5-preview`, `step-3.7-flash`, and `step-3.5-flash`. Add or remove `entry(...)` items to match your account's access. Catalog fields depend on the Codex version; check compatibility when upgrading.

### Create a Step profile

Create `$CODEX_HOME/step.config.toml`. Use this command for a new file; if the file already exists, merge the settings instead of overwriting it.

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
cat > "$CODEX_HOME/step.config.toml" <<EOF
model = "step-5-preview"
model_provider = "stepfun"
model_catalog_json = "$CODEX_HOME/step-catalog.json"
web_search = "disabled"
EOF
```

Check that `model_catalog_json` contains an absolute path:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
cat "$CODEX_HOME/step.config.toml"
```

`--profile step` layers `step.config.toml` over the base `config.toml` and uses the provider defined there. Because `model_catalog_json` replaces the startup model catalog, keep it in the dedicated profile. Starting Codex without `--profile step` leaves this profile unloaded.

## Start Codex CLI

1. Confirm that the required files exist:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
ls "$CODEX_HOME"/config.toml \
   "$CODEX_HOME"/step.config.toml \
   "$CODEX_HOME"/step-catalog.json
```

2. Start Codex from your project directory:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
codex --profile step
```

3. Confirm that the model is `step-5-preview` and the provider is `stepfun`. Open `/model` to check that the Step models from the catalog are available.

When resuming a Step session, select the same profile. Replace `YOUR_SESSION_ID` with the session ID:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
codex resume --profile step YOUR_SESSION_ID
```

`/model` switches models within the current provider. To use another provider, start a separate session with its profile.

## Connect StepSearch MCP

StepSearch provides `web_search` and `web_fetch` for web searches and page retrieval. Add it through the Step Plan endpoint when you need these tools.

1. Confirm that `STEP_API_KEY` is configured, then register the server:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
codex mcp add step-search \
  --url https://api.stepfun.ai/step_plan/v1/mcp/web_search/mcp \
  --bearer-token-env-var STEP_API_KEY
```

2. Check the registered server:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
codex mcp list
```

3. Restart `codex --profile step`. Use `/mcp` to check the connection and tools, then run a search or page-retrieval task and inspect the tool call and returned result.

`codex mcp add` uses the current `CODEX_HOME`; the resulting configuration is not limited to the `step` profile. Use a dedicated configuration directory to keep MCP settings separate. The Step profile disables built-in web search with `web_search = "disabled"` and uses StepSearch MCP for search tools.

## Verify the integration

### Test a conversation

Enter `Reply only with OK.` in an interactive session. Expected output: `OK`. For a read-only check from your project directory, run:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
codex exec --profile step --sandbox read-only "Reply only with OK." < /dev/null
```

### Test tool calls

Create a separate test directory with a `README.md` containing `Codex Step Plan test`. Start Codex there and enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Read README.md and create hello.py that prints "Hello, world!".
Run hello.py with an available Python interpreter and report the command and actual output.
Do not change README.md or any other existing files.
```

Approve the required operations and inspect the file and command records. Confirm that `hello.py` exists, prints `Hello, world!`, and that `README.md` is unchanged.

## Common questions

<AccordionGroup>
  <Accordion title="Q: Why does Codex ask me to sign in with ChatGPT?">
    Check `CODEX_HOME`, the `model_provider = "stepfun"` setting in `step.config.toml`, and the `--profile step` startup argument. Confirm that the provider is defined in the user-level `config.toml` and that the API key is available through the environment or `.env`. Set `CODEX_HOME` again before starting Codex if you use a dedicated directory.
  </Accordion>

  <Accordion title="Q: Why are Step models missing from /model, or why does Model metadata not found appear?">
    Check that the selected profile's `model_catalog_json` points to a valid absolute path and that the catalog contains the correct model IDs. Restart after changes. If the old list remains, exit Codex, remove `models_cache.json` from the active `CODEX_HOME`, and try again.
  </Accordion>

  <Accordion title="Q: How do I resolve a missing field error in the model catalog?">
    Regenerate `step-catalog.json` using the structure required by your Codex version. Confirm that `default.md` downloaded successfully and is not empty. A reduced catalog from another version may omit required fields.
  </Accordion>

  <Accordion title="Q: What should I check after a connection failure, repeated reconnects, or a 401 response?">
    Inspect the full error, network connection, API key status, and model permissions. Use `https://api.stepfun.ai/step_plan/v1` for `base_url` and `responses` for `wire_api`. Confirm that `env_key` matches the environment variable and that the key belongs to the account for this endpoint.
  </Accordion>

  <Accordion title="Q: Why does codex exec keep waiting for standard input?">
    If it stops at `Reading additional input from stdin...` and you do not need to supply input through stdin, append `< /dev/null` to the command.
  </Accordion>

  <Accordion title="Q: Why is the response empty or marked incomplete?">
    Inspect the response status, error details, and token usage. Reasoning can consume the available output budget before visible text is produced. Identify the cause before adjusting parameters supported by your client version and the service.
  </Accordion>

  <Accordion title="Q: Why are search tools missing even though the MCP server is registered?">
    Check that registration and startup use the same `CODEX_HOME`, and verify `STEP_API_KEY`. Inspect `codex mcp list`, restart an interactive session, and check `/mcp`. If you use `codex exec`, verify tool loading and invocation in that mode separately.
  </Accordion>
</AccordionGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.