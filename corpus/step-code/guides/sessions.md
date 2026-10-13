> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sessions and context

Step Code saves sessions automatically and supports restoring, navigating branches, forking, and exporting. Compact context as it approaches the model's window to retain important information and continue working.

## Session storage

Sessions are grouped by working directory under `~/.stepcode/agent/sessions/`. Each JSONL file is a tree whose records are linked by `id` and `parentId`.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
~/.stepcode/agent/sessions/
├── <encoded-working-directory-A>/
│   └── <session-file>.jsonl
└── <encoded-working-directory-B>/
    └── <session-file>.jsonl
```

Use `--session-dir <directory>` to override the location, or `--no-session` for a temporary session that is not saved. Session files use an internal format; do not edit them manually.

See [Data paths](/docs/en/step-code/configuration/data-paths) for the full storage layout and cleanup instructions.

## Starting and restoring sessions

| Command | Action |
| - | - |
| `step` | Start a new session in the current directory |
| `step -c` | Continue the most recent session |
| `step -r` | Browse history and choose a session |
| `step --session <path-or-ID>` | Restore a specific session, including by partial ID |
| `step --fork <path-or-ID>` | Fork an existing session into a new file |
| `step --name "Auth migration"` | Set the session name |

## Switching sessions in the TUI

| Command | Action |
| - | - |
| `/new`, `/clear` | Create a session and clear the current conversation context |
| `/resume` | Open the session picker |
| `/name` | Name the current session |
| `/session` | Show file path, ID, message count, token usage, and cost information |
| `/fork` | Fork an independent session |

Type to search in the session picker. Ctrl+S changes sorting, Ctrl+N filters named sessions, Ctrl+R renames, and Ctrl+D deletes. Confirm that you no longer need a record before deleting it.

See [Interaction and input](/docs/en/step-code/guides/interaction) for input controls and permission modes.

## Context compaction

Automatic compaction runs at safe points, such as after a tool batch, when context exceeds `contextWindow - reserveTokens`. You can also specify what to preserve manually:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
/compact Preserve the authentication migration goals, interface contracts, changed files, verification results, and unresolved issues.
```

Compaction retains recent messages totaling approximately `keepRecentTokens` tokens and summarizes older content into eight structured sections, including goals, changed files, verified conclusions, and failed attempts. Subsequent requests contain system instructions, the summary, and retained messages. Also record important agreements and acceptance results in project files.

Configure in `config.toml`:

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
[compaction]
enabled = true
reserveTokens = 16384
keepRecentTokens = 20000
```

`enabled = false` disables automatic compaction but leaves `/compact` available. Choose reserve and recent-message sizes appropriate for the model's context window.

## Session trees and forks

| Command | Behavior | Use case |
| - | - | - |
| `/tree` | Continue from a historical node in the same file | Try another approach from an earlier decision |
| `/fork` | Create a session from a selected user message | Separate conversation experiments |
| `/clone` | Copy the full current branch to a new session | Save the current state before continuing |

In `/tree`, navigate with arrow keys, select with Enter, cycle filters with Ctrl+O, and edit labels with Shift+L. Filters include default, no tools, user messages only, and labeled only. Selecting a user message can restore its text to the input box; edit and resend to form a branch.

When switching branches, you can generate a summary of the branch you are leaving. Configure this under `[branchSummary]`.

<Note>
  Session branches separate conversation records. They do not undo disk changes or create Git branches. Use Git branches or worktrees to isolate code experiments. Summaries and subsequent model calls may still consume tokens.
</Note>

See [Common use cases](/docs/en/step-code/guides/use-cases) for project task examples.

## Exporting and sharing

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
/export session.html
/export session.jsonl
/import session.jsonl
```

You can also export from the command line:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step --export /path/to/session.jsonl session.html
```

`/export [file]` defaults to HTML; a `.jsonl` extension exports JSONL. `/import <file>` restores it as the current session. Exports can contain code, command output, and paths; review them before sharing.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.