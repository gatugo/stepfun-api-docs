---
card: step-code
tier: evidence
status: verified
verified_on: 2026-10-08
source: corpus/step-code/quickstart.md, corpus/step-code/reference/cli.md, corpus/step-code/configuration/files.md, corpus/step-code/customization/mcp.md, corpus/step-code/reference/steppage.md
---

# Step Code — the terminal agent, condensed

**Step Code is StepFun's terminal-based AI agent** for reading and changing code,
running commands, and completing software-development tasks. Built by StepFun,
optimized for Step models. macOS and Linux supported; Windows PowerShell is in beta
(WSL recommended). One reference card for install, login, the `step` command, slash
commands, config and data paths, MCP, and steppage.

## Install

| Platform | Command |
| :- | :- |
| macOS / Linux | `curl -fsSL https://static-openapi.stepfun.com/stepcode/install.sh \| bash` |
| Windows (PowerShell, beta) | `irm https://static-openapi.stepfun.com/stepcode/install.ps1 \| iex` |

- Installs to `~/.stepcode/bin` (Windows: `%USERPROFILE%\.stepcode\bin`), configures
  PATH, verifies the checksum, runs a smoke test.
- Managed `rg` / `fd` download on demand to `~/.stepcode/agent/bin`.
- Verify with `step --version`.
- Installer flags: `--version <vX.Y.Z|latest>`, `--install-dir <path>`. Overrides via
  `STEP_RELEASE_BASE_URL`, `STEP_INSTALL_DIR`, `STEP_CODING_AGENT_DIR`.
- Source repository: `github.com/stepfun-ai/Step-Code`.
- The installer runs a remote script — verify the source first, or download and
  inspect it.

## First launch and login

`cd /path/to/project` then `step`. First launch walks through login, MCP import
(detected from Claude Code / Codex config — importing does not modify the original
tool's configuration), and the theme selector. Other starts: `step -p "task"` (run
once and exit), `step -c` (continue most recent session).

`/login` in the interface, then choose a platform:

| Method | Action |
| :- | :- |
| Step Plan | sign in at `platform.stepfun.com` |
| **Step Plan Oversea** | sign in at `platform.stepfun.ai` — **this account's platform** |
| API key | select provider and enter a key, or set its env var before launch |

- OAuth credentials refresh automatically.
- API keys can be saved via `/login` to `~/.stepcode/auth.json` (0600), or set as env
  vars (e.g. `export ANTHROPIC_API_KEY=...`). `/logout` clears credentials.
- **Subscriptions and pay-as-you-go are separate billing channels — the model name
  alone does not determine which quota is used.**
- Credential priority: CLI `--api-key` > `auth.json` > environment variables.
- **Bypass is the default permission mode** — ordinary file changes and shell
  commands do not prompt. Use `/permissions` → Ask to require approval. Permission
  modes are not an OS sandbox.

## The `step` command

Usage: `step [options] [--] [@files...] [task...]` — inspect with `step --help` /
`step --version`.

### Model options

| Option | Description |
| :- | :- |
| `--provider <name>` | Provider such as `step`, `anthropic`, `openai` |
| `--model <model>` | Model ID or pattern; supports `provider/id` and a thinking-level suffix |
| `--api-key <key>` | Override other credentials (beware shell history and process-argument exposure) |
| `--thinking <level>` | `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max` — subject to model support |
| `--models <list>` | Comma-separated models for Ctrl+P cycling |
| `--list-models [search]` | List available models |

### Session options

`-c`/`--continue` · `-r`/`--resume` · `--session <path-or-ID>` · `--fork <path-or-ID>` ·
`--session-dir <directory>` · `--no-session` · `--name`/`-n <name>` · `-p`/`--print`
(run once and exit; accepts stdin and `@files`)

### Tool options

`--tools`/`-t <list>` (allowlist) · `--exclude-tools`/`-xt <list>` ·
`--no-builtin-tools`/`-nbt` · `--no-tools`/`-nt`

### Resource options

`-e`/`--extension <source>` · `--skill <path>` · `--prompt-template <path>` ·
`--theme <path>` · `--no-extensions` / `--no-skills` / `--no-prompt-templates` /
`--no-themes` · `--no-context-files`/`-nc` (disable project-instruction loading)

### Other options

`--plan` (start in Plan mode) · `--tui-mode <regular|fullscreen>` ·
`--approval-mode <mode>` · `--version` · `--use-theme <name>` ·
`--export <session-file> [output-file]` · `--` (end option parsing)

### Subcommands

| Command | Description |
| :- | :- |
| `step update` | Update to latest stable (alias `step upgrade`) |
| `step update <version>` | Install a specific release, e.g. `step update 0.4.0` |
| `step update --all` | Update Step Code and all packages |
| `step update --extensions` | Update only packages |
| `step install <source>` / `step remove <source>` / `step list` | Resource packages |
| `step config` | Manage resources interactively; Tab switches global and project scope |
| `step mcp` | MCP `list`, `get`, `add`, `remove`, `login`, `logout` |
| `step login` / `step logout` / `step login status` | Sign in to or out of Step; show login method and status |

Updates include download, checksum verification, a smoke test, and rollback on
failure.

## Slash commands

Type `/` in the input box for completion. These run in the interactive interface,
not in your shell. Session operations **do not** roll back Git or disk changes.

| Group | Commands |
| :- | :- |
| Sessions | `/new`, `/clear` · `/resume` · `/name` · `/session` · `/tree` · `/fork` · `/clone` · `/export [file]` · `/import <file>` · `/copy` |
| Models and thinking | `/model` (Ctrl+S saves default) · `/thinking`, `/effort` · `/scoped-models` · `/llama` |
| Context and config | `/compact [preservation-instructions]` · `/settings` · `/reload` · `/theme [name]` · `/trust` |
| Permissions and modes | `/permissions` · `/permissions cycle` · `/plan [task]` |
| Long tasks and agents | `/goal <goal>` · `/goal status` · `/goal pause` · `/goal resume` · `/goal edit <goal>` · `/goal clear` · `/cron` · `/todos` |
| Extensions and instructions | `/plugin` · `/mcp` · `/init` · `/skill:<name> [arguments]` |
| Accounts and other | `/login`, `/logout` · `/status` · `/hotkeys` · `/feedback` · `/quit`, `/exit` |

Restart after installing or removing plugins that provide MCP servers.

## Config and data paths

| Scope | Default location | Purpose |
| :- | :- | :- |
| Global | `~/.stepcode/config.toml` | Applies across projects |
| Project | `<project>/.stepcode/config.toml` | Overrides global; **requires project trust** |

Project config merges nested objects key by key and replaces arrays as a whole.
Settings marked global-only (`httpProxy`, `defaultProjectTrust`) cannot be
overridden by a project. The global file is created on first run; writes are atomic
(temp-file-and-rename) and preserve the leading comment block. TOML does not support
`null` — remove an optional key to unset it.

Data root is `~/.stepcode/` (`/home/<username>/.stepcode` on Linux,
`/Users/<username>/.stepcode` on macOS, `C:\Users\<username>\.stepcode` on Windows).
Agent configuration lives under `~/.stepcode/agent`.

| File | Content |
| :- | :- |
| `config.toml` | Global settings and MCP server declarations |
| `auth.json` | API keys and OAuth credentials; key values support `!command` and `$VAR` resolution |
| `models.json` | Custom models and overrides, reloaded when `/model` opens |
| `.credentials.json` | MCP OAuth tokens, keyed `<server-name>\|`, written atomically |
| `models-store.json` | Model catalog cache |
| `agent/trust.json` | Project trust records |
| `agent/sessions/<encoded-working-directory>/` | One JSONL file per session (messages, tool calls, outputs, summaries) |

Session-directory precedence: `--session-dir` > `sessionDir` in `config.toml`.
Built-in `rg`/`fd` are downloaded on demand to `~/.stepcode/agent/bin/`. Logs in
`logs/`; telemetry buffers in `telemetry/`.

Project data: `.stepcode/config.toml`, `.stepcode/cron/tasks.json`,
`.stepcode/workflows/runs/`, `.stepcode/agents/`, `skills/`, `themes/`, `plugins/`,
`.stepcode/plans/`, `.stepcode/npm/`.

**Retired locations — do not use:** `~/.stepcode/agent/settings.json`,
`~/.stepcode/agent/step-settings.json`, `~/.stepcode/agent/auth.json`,
`agent/models.json` (now at the `~/.stepcode` root), and `.step-harness` (read once
during startup migration, then never written).

### Config worth knowing

| Field | Default | Notes |
| :- | :- | :- |
| `permissionPreset` | `bypass` | `ask`, `read-only`, `bypass`, `autopilot` |
| `defaultProvider` / `defaultModel` | — | Save with Ctrl+S in `/model` |
| `defaultThinkingLevel` | — | Client levels: `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max` |
| `defaultTools` | — | Built-in allowlist: `read`, `bash`, `powershell`, `edit`, `write`, `grep`, `find`, `ls` |
| `enableSkillCommands` | `true` | Registers Skills as `/skill:<name>` |
| `httpProxy` | unset | Global-only; or use `HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY` |
| `sessionDir` | unset | Custom session directory |
| `[compaction]` | `enabled = true`, `reserveTokens = 16384`, `keepRecentTokens = 20000` | `enabled = false` only disables automatic compaction |
| `[retry]` | `enabled = true`, `maxRetries = 3`, `baseDelayMs = 2000` | Exponential backoff 2/4/8s; keep `provider.maxRetries` at its default `0` |
| `[telemetry]` | `enabled = true` | Device and account identifiers only — not prompts, code, or paths |

### Environment variables

| Variable | Purpose |
| :- | :- |
| `AI_AGENT=step` | Lets external tools identify Step Code subprocesses |
| `STEP_PERMISSION_PRESET`, `STEP_APPROVAL_MODE` | Override permission mode |
| `STEP_DISABLE_WORKFLOW` | `1` disables workflow / ultraloop registration |
| `STEPCODE_CONFIG_PATH` | JSON model config injected at startup without writing `models.json` |
| `STEP_API_KEY` | Default key variable for the `stepcode` platform |
| `STEP_MAX_CONTEXT_TOKENS` / `STEP_MAX_OUTPUT_TOKENS` | Override the injected model's context window / max output |
| `STEPFUN_API_KEY` | steppage hosting plugin credential — preserve this exact name |

## MCP

Connect local or remote tools; once a server connects the model can call its
registered tools.

| Transport | Configuration | Use case |
| :- | :- | :- |
| stdio | `command`, `args`, optional `env` | Start a local tool process |
| Streamable HTTP | `url` | Connect to a remote MCP service |

**Legacy SSE transport is not supported.** Plugins can also declare MCP servers.

Declare servers under `[mcp_servers.<name>]` in the global `~/.stepcode/config.toml`:

```toml
[mcp_servers.local-tools]
command = "node"
args = ["/absolute/path/to/mcp-server.js"]
env = { LOG_LEVEL = "info" }

[mcp_servers.remote]
url = "https://mcp.example.com/mcp"
bearer_token_env_var = "EXAMPLE_TOKEN"
```

Fields: `command` or `url` (mutually exclusive) · `args` / `env` / `cwd` ·
`bearer_token_env_var` · `http_headers` (avoid real keys) · `env_http_headers` ·
`startup_timeout_sec` (default 30) · `tool_timeout_sec` (default 300) · `enabled`
(default `true`) · `enabled_tools` / `disabled_tools`.

```bash
step mcp list [--json]
step mcp get <server-name>
step mcp add remote --url https://mcp.example.com/mcp
step mcp add local-tools -- node /absolute/path/to/mcp-server.js
step mcp remove <server-name>
```

`--url` and a local command are mutually exclusive. `--bearer-token-env-var` is
HTTP-only. `--env` sets stdio subprocess variables, not HTTP headers.

- Bearer tokens are read from the environment running Step Code
  (`export EXAMPLE_TOKEN=...`).
- OAuth services: `step mcp login <server-name>` / `step mcp logout <server-name>` —
  dynamic client registration, PKCE, local callback; tokens in
  `~/.stepcode/.credentials.json` (0600), keyed `<name>|`.
- **Model-platform login and MCP authorization use separate credentials.**
- `/mcp` shows server status (`connecting` / `connected` / `failed`) and loaded tool
  counts; servers with `enabled = false` do not appear.
- Tool names use `<server>__<tool>`; invalid characters become underscores.
  `enabled_tools` / `disabled_tools` filter before registration — with an allowlist
  set, other tools are unavailable to the model.
- Bypass mode skips per-call approval for ordinary MCP calls. Connect only to
  trusted servers.

## steppage — publish static websites

A Step Code plugin that publishes local static output to **StepFun Page** through the
`steppage-mcp` MCP server: deployment, site queries, version management, promotion,
and rollback. Accepts a local directory or ZIP for static hosting — **not**
application backends or databases.

| Item | Requirement |
| :- | :- |
| Credentials | `STEPFUN_API_KEY` (a signed-in Step account can provide fallback credentials) |
| Install | `/plugin install steppage` inside Step Code |
| Official installer | `https://dl.stepfun.com/steppage-mcp/p/install.sh` (overridable via `STEPCODE_STEPPAGE_INSTALLER_URL`); manual: `curl -fsSL https://dl.stepfun.com/steppage-mcp/p/install.sh \| sh` |
| Activation | Restart Step Code and check `/mcp` |
| Windows | No automatic MCP installation — use WSL or configure manually |

Deployment: build static output (e.g. `dist/`), verify entry pages, asset paths, and
contents, and exclude keys, private configuration, and user data. Then tell Step Code
what to publish — e.g. *"Publish ./dist as a website and generate a preview link."*
The model calls `page_deploy` to publish the directory or ZIP as a site version;
results automatically include the management link. Provide a precise site identifier
when updating an existing site.

Each deployment creates a version. `promote` makes a version live; `rollback` returns
to a specified version. Verify site and version identifiers before acting. Deleting a
site or version may be irreversible. Site management lives at
`platform.stepfun.com/sites`; hosting allowances, access rules, and limits are
governed by the static hosting documentation and your account — **not** by Step Plan
model allowances.

> **Warning:** deployment uploads artifacts to an external hosting service. Public
> links may be accessed and shared by others — review content and permissions before
> publishing.

## Project instructions

Create `AGENTS.md` at the project root. Step Code loads
`~/.stepcode/agent/AGENTS.md` plus instructions from the current directory and its
parents; per directory the first match wins: `AGENTS.override.md` > `AGENTS.md` >
`CLAUDE.md`. Run `/reload` or restart after changes. `/init` generates instructions
for review.

## Not covered by this card

Keyboard shortcuts, interaction and input, sessions and context, use cases,
migration, agents and subagents, themes, plugins, built-in tools, release notes, and
FAQ have their own pages in `corpus/step-code/` — this card is the install/login/CLI/
config/MCP/steppage slice only.
