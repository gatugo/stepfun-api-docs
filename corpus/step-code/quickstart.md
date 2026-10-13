> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Quickstart

<a id="what-is-step-code" />

## Product overview

Step Code is a terminal AI agent for software development and everyday terminal tasks. It reads and edits code, executes shell commands, searches files, fetches web pages, and plans its next steps based on execution feedback. Built by StepFun, it is optimized for Step models.

* Write code: implement features, fix bugs, add tests, and refactor.
* Understand projects: map directories, dependencies, entry points, and local setup.
* Automate tasks: run one-off scripts, batch changes, and scheduled tasks.
* Manage long tasks: use `/goal` for hours-long tasks and return to check progress and results.
* Run agents in parallel: use workflow to coordinate multiple subagents.
* Publish static websites: deploy build output with the `steppage` plugin.

## Installation

Use a modern terminal such as Kitty, Ghostty, iTerm2, or Windows Terminal. Image display, true color, and some key combinations depend on terminal configuration.

<Note>
  These commands execute a remote script. Verify the source first, or download and inspect the script before running it.
</Note>

<Tabs>
  <Tab title="macOS / Linux">
    ```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    curl -fsSL https://static-openapi.stepfun.com/stepcode/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows">
    Run in PowerShell:

    ```powershell theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
    irm https://static-openapi.stepfun.com/stepcode/install.ps1 | iex
    ```

    PowerShell support is in beta. On Windows, installing in WSL with the Linux command is recommended.
  </Tab>
</Tabs>

The program and runtime resources are installed to `~/.stepcode/bin` by default. The installer configures PATH, verifies the checksum, and runs a smoke test. Managed `rg` / `fd` tools are downloaded on demand to `~/.stepcode/agent/bin`.

For zsh, bash, and POSIX login configuration, it appends a marked PATH block. For fish, it uses `fish_add_path`. On Windows, it updates the registry and broadcasts the change; the default installation directory is `%USERPROFILE%\.stepcode\bin`.

Open a new terminal after installation and check the installed version:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step --version
```

The installer supports `--version <vX.Y.Z|latest>` and `--install-dir <path>`. Use `STEP_RELEASE_BASE_URL`, `STEP_INSTALL_DIR`, and `STEP_CODING_AGENT_DIR` to override the release source and directories. Source repository: [Step-Code](https://github.com/stepfun-ai/Step-Code).

## First launch

Open your project directory:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
cd /path/to/project
step
```

First launch walks through login, MCP import, the theme selector, and the main interface. The import screen appears when Claude Code or Codex MCP configuration is detected. Highlight a theme to preview it. Importing does not modify the original tool's configuration.

Other ways to start:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step -p "How do I run this project?"
step -c
```

`-p` runs one task and exits. `-c` continues the most recent session.

## Login

Enter `/login` in the interactive interface and choose the appropriate platform:

| Method | Action |
| - | - |
| Step Plan | Select Step Plan and sign in at `platform.stepfun.com` |
| Step Plan Oversea | Select Step Plan Oversea and sign in at `platform.stepfun.ai` |
| API key | Select the provider and enter a key, or set its environment variable before launch |

OAuth credentials refresh automatically. For API keys, set a variable such as `export ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY"`, or use `/login` to save the key to `~/.stepcode/auth.json`. Use `/logout` to clear the corresponding credentials. See [Platforms and models](/docs/en/step-code/configuration/models) for all connection methods.

Subscriptions and pay-as-you-go API usage are separate billing channels. Choose the platform for your region and billing method; the model name alone does not determine which quota is used.

## Your first conversation

Enter a task and press Enter:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
What technology stack does this project use? What is each directory responsible for? How do I run it locally?
```

The model uses `read` to read files, `write` to write them, `edit` to change them, and `bash` to run shell commands. Read-only search tools such as `grep`, `find`, and `ls` can be enabled in settings. See [Built-in tools](/docs/en/step-code/reference/tools) for configuration and model-facing names.

<Warning>
  Bypass is the default permission mode: ordinary file changes and shell commands do not prompt for individual approval. To require approval, run `/permissions` and choose Ask. Permission modes are not an OS sandbox. Run in trusted directories; use an isolated container or VM for untrusted projects or unattended work.
</Warning>

After confirming the scope, try a task that writes a file:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Create a table for the error codes in src/api/errors.ts, including each code, its meaning, and when it occurs. Save it to docs/errors.md.
```

## Add project instructions

Create `AGENTS.md` at the project root:

```markdown theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
# Project instructions

- Run npm run check after changing code.
- Do not run production migrations locally.
- Keep responses concise.
```

Step Code loads `~/.stepcode/agent/AGENTS.md` and instructions from the current directory and its parents. In each directory, it selects the first match in this order: `AGENTS.override.md`, `AGENTS.md`, `CLAUDE.md`. Run `/reload` or restart after changes.

You can also run `/init` to have the model inspect the project and generate instructions. Review the content before saving it.

## Common commands and shortcuts

| Command or shortcut | Action |
| - | - |
| `/model` | Select a model |
| `/permissions` | Change tool approval mode |
| `/thinking`, `/effort` | Set thinking level |
| `/plan` | Toggle Plan mode; optionally include a task |
| Esc | Interrupt output or close a dialog |
| Ctrl+C | Clear input; press again with empty input to exit |
| Shift+Tab | Cycle permission modes |
| Ctrl+L | Redraw the screen |
| Ctrl+O | Collapse or expand tool output |
| Enter during streaming | Queue a message for delivery after the current turn's tools finish |

See [Slash commands](/docs/en/step-code/reference/slash-commands) and [Keyboard shortcuts](/docs/en/step-code/reference/keyboard-shortcuts) for the complete lists.

## Where data is stored

Configuration, credentials, and sessions are stored locally under `~/.stepcode/` by default. Project resources live in the project's `.stepcode/` directory. See [Data paths](/docs/en/step-code/configuration/data-paths).

Model calls send prompts, relevant code, and tool results; MCP, plugins, feedback, and deployment may also access external services. Do not send sensitive data to services that are not authorized to receive it.

## Upgrade and uninstall

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step update
```

`step update` installs the latest stable version, including checksum verification, a smoke test, and rollback on failure. `step update 0.4.0` illustrates installing a specific version; replace the version with the release you need. `step upgrade` is an alias. See [The step command](/docs/en/step-code/reference/cli) for package updates.

For a script installation, remove the `step` executable from the installation directory, or `step.exe` on Windows, and remove the installer's PATH entry. This does not delete configuration, credentials, or sessions. Back them up before following the [cleanup instructions](/docs/en/step-code/configuration/data-paths#cleaning-up-data). Do not delete directories shared with other tools.

## Next steps

* [Interaction and input](/docs/en/step-code/guides/interaction): file references, approvals, Plan mode, and goals.
* [Sessions and context](/docs/en/step-code/guides/sessions): restore, compact, and export sessions.
* [Common use cases](/docs/en/step-code/guides/use-cases): ready-to-use task examples.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.