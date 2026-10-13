> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Built-in tools

Step Code provides tools for reading, writing, editing, commands, and file search. Configuration (`defaultTools` / `--tools`) uses allowlist names such as `read` and `bash`; model-facing names include `read_file` and `run_command`.

## Tool overview

| Configuration name | Purpose | Model-facing name |
| - | - | - |
| `read` | Read text and images | `read_file` |
| `write` | Create or overwrite files | `write_file` |
| `edit` | Exact text replacement | `edit_file` |
| `bash`, `powershell` | Run shell commands | `run_command` |
| `grep` | Search file contents | `search_files` |
| `find` | Find files by name or glob | `find_files` |
| `ls` | List directories | `list_directory` |

`bash` / `powershell` correspond to platform shells. Use the left column for configuration. Extensions and MCP can add other tools.

## read

Reads text and JPG, PNG, GIF, WebP, and BMP images. Long text is truncated at the line or KB limit, whichever comes first. Use `offset` / `limit` to read sections.

Images are attached to model requests and resized to within 2,000 px by default.

## bash (powershell on Windows)

Commands run in the working directory and stream output. Configure the environment with `shellPath` and `shellCommandPrefix`.

Using `run_command` with `run_in_background` starts a detached command and immediately returns its PID and log file. Read the log to check readiness and use `kill` to stop it. Processes still running at session end are cleaned up. This differs from the input box's `!` prefix.

The shell has the same system permissions as the account running Step Code. Check working directories, credentials, and side effects before execution.

See [Keyboard shortcuts](/docs/en/step-code/reference/keyboard-shortcuts) for shortcuts for displaying tool output.

## edit

Performs exact replacements in a single file. Each `oldText` must match uniquely, and edits must not overlap. Combine adjacent changes into one replacement. If a match fails, reread the file rather than editing from stale content.

## write

Creates or completely overwrites a file, creating parent directories as needed. To preserve existing content, use a partial edit or confirm the complete replacement first.

## grep

Parameters include `pattern`, `path`, `ignoreCase`, `literal`, and `glob`, supporting literal or regex searches. Backend order is ripgrep (downloaded or system), `git grep` inside a Git repository, then POSIX `grep`. If none are available, it reports an error.

See [Built-in tool cache](/docs/en/step-code/configuration/data-paths#built-in-tool-cache) for cache and network details.

## find

Finds paths by filename or glob, including dotfiles. Use a read tool to inspect returned files.

## ls

Lists entries alphabetically, marks directories with `/`, and includes dotfiles. Long output is truncated; narrow the directory scope to continue.

## Enabling and disabling tools

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
defaultTools = ["read", "grep", "find", "ls"]
```

`defaultTools` controls the built-in allowlist. An empty array leaves extension tools. Launch options override configuration for one session:

| Option | Effect |
| - | - |
| `--tools` | Allowlist for all tools |
| `--exclude-tools` | Exclude named tools |
| `--no-builtin-tools` | Disable only built-in tools |
| `--no-tools` | Disable all tools |

In Bypass mode, tools can still modify files or access networks; ordinary calls do not require individual approval. See [Approval flow](/docs/en/step-code/guides/interaction#approval-flow).

See [The step command](/docs/en/step-code/reference/cli) for the full set of launch options.

See [Slash commands](/docs/en/step-code/reference/slash-commands) for interactive commands.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.