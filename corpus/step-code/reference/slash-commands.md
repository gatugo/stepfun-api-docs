> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Slash commands

Type `/` in Step Code's input box to see command completion. These commands run in the interactive interface, not in your shell.

## Sessions

| Command | Action |
| - | - |
| `/new`, `/clear` | Start a session |
| `/resume` | Browse and restore sessions |
| `/name` | Name the session |
| `/session` | Show path, ID, and usage |
| `/tree` | Browse the session tree |
| `/fork` | Fork a session |
| `/clone` | Copy the current branch into a new session |
| `/export [file]` | Export HTML or JSONL |
| `/import <file>` | Import JSONL |
| `/copy` | Copy response content |

Session operations do not roll back Git or disk changes. See [Sessions and context](/docs/en/step-code/guides/sessions).

See [The step command](/docs/en/step-code/reference/cli) for command-line session options.

## Models and thinking

| Command | Action |
| - | - |
| `/model` | Select a model; Ctrl+S saves the default |
| `/thinking`, `/effort` | Select thinking level; Ctrl+S saves the default |
| `/scoped-models` | Manage the Ctrl+P model set |
| `/llama` | Manage llama.cpp router models |

## Context and configuration

| Command | Action |
| - | - |
| `/compact [preservation-instructions]` | Compact context |
| `/settings` | Open settings |
| `/reload` | Reload configuration and resources |
| `/theme [name]` | Select a theme |
| `/trust` | Manage project trust |

See [Configuration files](/docs/en/step-code/configuration/files) for configuration field details.

## Permissions and modes

| Command | Action |
| - | - |
| `/permissions` | Choose tool approval mode |
| `/permissions cycle` | Cycle permission modes |
| `/plan [task]` | Toggle Plan mode or plan a task |

## Long tasks and multiple agents

| Command | Action |
| - | - |
| `/goal <goal>` | Set a goal |
| `/goal status` | Show the goal and status |
| `/goal pause`, `/goal resume` | Pause or resume |
| `/goal edit <goal>` | Edit the goal |
| `/goal clear` | Clear the goal |
| `/cron` | List and delete scheduled tasks |
| `/todos` | View the task list |

Goal mode continues long tasks. See [Agents and subagents](/docs/en/step-code/customization/agents#workflow-and-ultraloop) for orchestration and authorization.

<a id="ecosystem" />

## Extensions and project instructions

| Command | Action |
| - | - |
| `/plugin` | Manage plugins and marketplaces |
| `/mcp` | View MCP server status |
| `/init` | Generate `AGENTS.md` project instructions |
| `/skill:<name> [arguments]` | Invoke a loaded Skill |

Restart after installing or removing plugins that provide MCP servers.

## Accounts and other commands

| Command | Action |
| - | - |
| `/login`, `/logout` | Sign in to or out of a platform |
| `/status` | View session and model status |
| `/hotkeys` | View shortcuts |
| `/feedback` | Submit feedback |
| `/quit`, `/exit` | Exit |

Review feedback text and attachments for sensitive data before submission.

See [Keyboard shortcuts](/docs/en/step-code/reference/keyboard-shortcuts) for the complete shortcut list.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.