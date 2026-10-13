> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Data paths

Step Code stores configuration, credentials, sessions, and logs under `~/.stepcode/` by default. Understand the directory layout before backing up or cleaning data.

## Data root

| System | Default path |
| - | - |
| macOS | `/Users/<username>/.stepcode` |
| Linux | `/home/<username>/.stepcode` |
| Windows | `C:\Users\<username>\.stepcode` |

`~` means your home directory. Agent configuration lives under `~/.stepcode/agent`. `.step-harness` is retired and no longer written; startup only reads old credentials for a one-time migration.

## Directory layout

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
~/.stepcode/
├── config.toml
├── auth.json
├── models.json
├── .credentials.json
├── device-id
├── models-store.json
├── bin/
├── logs/
├── marketplaces/
├── telemetry/
└── agent/
    ├── AGENTS.md
    ├── prompts/
    ├── skills/
    ├── agents/
    ├── themes/
    ├── extensions/
    ├── sessions/
    ├── trust.json
    ├── bin/
    ├── npm/
    └── git/
```

Some directories are created only when their feature is first used. `bin/` contains the main program and runtime resources; `agent/bin/` contains managed search tools.

## Key files

| File | Content |
| - | - |
| `config.toml` | Global settings and MCP server declarations |
| `auth.json` | API keys and OAuth credentials; key values support `!command` and `$VAR` resolution |
| `models.json` | Custom models and overrides, reloaded when `/model` opens |
| `.credentials.json` | MCP OAuth tokens, keyed by server name plus a vertical bar, written atomically |
| `models-store.json` | Model catalog cache |
| `agent/trust.json` | Project trust records |

Restrict credential files to the current user. POSIX systems use `0600`; check account-level file permissions on Windows. Do not commit or publicly upload the entire data directory.

See [Configuration files](/docs/en/step-code/configuration/files) for setting details.

## Session data

Sessions live in `agent/sessions/<encoded-working-directory>/`, one JSONL file per session, containing messages, tool calls, outputs, and summaries. Use `/session` for the exact current path.

Directory precedence is `--session-dir` > `sessionDir` in `config.toml`. Records contain `id` / `parentId`, with the current position as the active leaf. Compaction summaries, branch summaries, calls, and output share one file.

See [Sessions and context](/docs/en/step-code/guides/sessions). Do not edit internal records directly.

## Built-in tool cache

`rg` (ripgrep) and `fd` are downloaded on demand to `~/.stepcode/agent/bin/`, as `rg.exe` / `fd.exe` on Windows. Lookup order is an injected custom path > a downloaded local copy > system PATH.

Content search falls back from ripgrep to `git grep` inside Git repositories, then POSIX `grep`. It reports an error when none are available.

Deleting the cache may trigger another download. On restricted networks, check system PATH and download access first.

## Logs

* `logs/`: runtime logs; start here for startup, connection, and tool errors.
* `telemetry/`: telemetry buffers, separate from session records.

Logs can include error details and environment information. Review them before sharing.

Model calls, MCP, plugins, and deployment access external services as needed.

See [Environment variables](/docs/en/step-code/configuration/environment) for telemetry and proxy configuration.

## Project data

| Location | Content |
| - | - |
| `.stepcode/config.toml` | Project settings; requires trust |
| `.stepcode/cron/tasks.json` | Durable scheduled tasks |
| `.stepcode/workflows/runs/` | Workflow run records |
| `.stepcode/agents/`, `skills/`, `themes/`, `plugins/` | Project resources |
| `.stepcode/plans/` | Plan-mode session files |
| `.stepcode/npm/` | Project-scoped npm packages |

Share configuration and resources according to team conventions. Exclude runtime records, caches, private paths, and credentials; do not add the entire `.stepcode/` directory blindly.

## Cleaning up data

<Warning>
  Deleting a project's `.stepcode/` also deletes its configuration, tasks, and custom resources.
</Warning>

Exit Step Code and back up required configuration and sessions first.

| Goal | Action |
| - | - |
| Reset configuration | Back up and remove `config.toml` |
| Clear sessions | Remove unneeded contents of `agent/sessions/` |
| Clear logs | Delete old files in `logs/` |
| Redownload search tools | Remove the corresponding tool from `agent/bin/` |
| Sign out of a model platform | Use `/logout` |
| Clear MCP authorization | `step mcp logout <name>` |
| Clear telemetry buffers | Delete `telemetry/`; this does not disable telemetry |
| Refresh the model cache | Back up and remove `models-store.json` |
| Remove all data | Back up, delete Step Code's dedicated data directory, and clean up the installer's PATH entry |


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.