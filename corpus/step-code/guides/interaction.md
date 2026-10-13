> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Interaction and input

Use Step Code's input box to enter text, paste images, reference files, and run shell commands. Commands also let you change permission modes, toggle Plan mode, and manage goals. You can send messages while output streams.

## Input basics

| Action | Shortcut |
| - | - |
| Send a message | Enter |
| Insert a newline | Shift+Enter, Ctrl+J, or Alt+Enter |
| Browse input history | ↑ / ↓ with an empty input box |
| Jump forward to a character | Ctrl+] |
| Delete a word backward / forward | Ctrl+W / Alt+D |
| Delete to start / end of line | Ctrl+U / Ctrl+K |
| Restore deleted text | Ctrl+Y; Alt+Y cycles the kill ring |
| Undo | Ctrl+-; Ctrl+Z on Windows, Alt+Z on WSL |
| Exit | Ctrl+C to clear, then press again; Ctrl+D with empty input |
| Suspend to background | Ctrl+Z, except native Windows |

Windows Terminal also supports Ctrl+Enter for newlines. Customize `~/.stepcode/agent/keybindings.json`, then run `/reload`. See [Keyboard shortcuts](/docs/en/step-code/reference/keyboard-shortcuts).

See [Common use cases](/docs/en/step-code/guides/use-cases) for project task examples.

## Pasting images

Use Ctrl+V to paste an image, or Alt+V on Windows / WSL. Supported terminals also let you drag in an image path.

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step -p @screenshot.png "How do I fix the error in this screenshot?"
```

Select a model that accepts images. By default, large images are resized to within 2,000 px to reduce input size; adjust this in `[images]`. Inline terminal display and sending images to a model are separate capabilities. Disabling display does not prevent image transmission.

## Slash commands

Type `/` to open completion; Esc closes it.

| Command | Action |
| - | - |
| `/model` | Select a model |
| `/permissions` | Choose approval mode |
| `/thinking`, `/effort` | Change thinking level |
| `/plan` | Toggle Plan mode, or start planning an included task |
| `/new`, `/resume` | Create or restore a session |
| `/compact` | Compact context |
| `/goal`, `/cron` | Manage goals or scheduled tasks |
| `/tree`, `/fork` | Browse the session tree or fork a session |

Invoke Skills with `/skill:<name>`. See [Slash commands](/docs/en/step-code/reference/slash-commands) for the full list.

See [Sessions and context](/docs/en/step-code/guides/sessions) for session restoration and context compaction.

## File references

Type `@` to search project files and press Tab to complete paths. This works in Git and non-Git directories and on the command line:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step @README.md "Summarize this project's purpose and how to run it"
step @src/app.ts @src/app.test.ts "Review whether the implementation and tests agree"
```

Referenced files and files read by tools may enter model context. Check for keys, personal information, and sensitive business data before referencing them.

## Approval flow

In Ask mode, or when Autopilot encounters an item requiring confirmation, Step Code opens a dialog titled `Approve <tool>` or `Dangerous <tool>`. It shows the reason and a summary of the arguments. Approval starts execution; rejection cancels that call and returns the reason to the model. A batch may prompt for each call.

### Permission modes

| Mode | Ordinary tool calls |
| - | - |
| Ask | Safe read-only tools run directly; writes and commands require approval |
| Read Only | Only read-only and discovery tools are allowed |
| Bypass (default) | No per-call approval for ordinary tools |
| Autopilot | Skips ordinary approvals and automatically recovers from some transient model failures |

Use `/permissions` to choose, or `/permissions cycle` and Shift+Tab to cycle. Environment variables can override the initial mode; see [Environment variables](/docs/en/step-code/configuration/environment).

Operations identified by dangerous-command rules still require confirmation and are rejected in Read Only. These rules cannot cover every script or dangerous action and are not a sandbox.

Non-interactive mode (`step -p`) rejects calls requiring approval by default. Use `--approval-mode` to adjust ordinary-call policy; dangerous commands are not exempted. See [The step command](/docs/en/step-code/reference/cli).

## Switching modes

### Plan mode

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
/plan Map the authentication module's dependencies and propose a migration plan. Do not change application code yet.
```

`/plan` toggles the mode, `/plan <task>` starts planning a task, and `step --plan` starts in Plan mode. The model investigates and writes a plan before implementation.

In Plan mode, file edits are limited to the plan file. Shell commands remain subject to the normal permission policy. Approving the plan exits Plan mode and begins implementation.

### Direct shell commands

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
!npm run lint
!!git status --short
```

`!` runs a local command and sends its output to the model; `!!` runs it without sending the output. Each prefix applies to one command without switching modes. Commands entered this way do not support background execution. Output appears as a card; long output collapses automatically and can be expanded with Ctrl+O.

### Goal mode

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
/goal Migrate the tests to Vitest, keep existing cases passing, and summarize the changes.
```

Goal mode drives multiple turns until the goal is achieved or stopped manually. It suits hours-long tasks. Keep the Step Code process running during the task.

| Command | Action |
| - | - |
| `/goal status` | View the goal, status, and usage |
| `/goal pause` | Pause automatic continuation and interrupt its current turn |
| `/goal resume` | Resume the goal |
| `/goal edit` | Edit the goal |
| `/goal clear` | Clear the goal |

The status line shows active time, such as `Goal: active · 12m 3s`, counting only time when the goal is active.

Scheduled tasks use five-field cron expressions. Durable tasks are saved to `.stepcode/cron/tasks.json` in the project and require project trust. Durable tasks require the Step Code process to remain running.

See [Agents and subagents](/docs/en/step-code/customization/agents) for multi-agent orchestration and authorization.

## During streaming output

* Enter queues a message for delivery after the current assistant turn's tools finish.
* Esc interrupts the turn and restores queued messages to the input box.
* Alt+↑ retrieves queued messages; use Alt+Q on Windows / WSL.
* Ctrl+O collapses or expands tool output.

Configure `steeringMode` and `followUpMode` in settings. Follow-up delivery has no dedicated shortcut by default.

## External editor

Ctrl+G edits the current input in an external editor; the action is `app.editor.external`. Selection order is `externalEditor`, `VISUAL`, `EDITOR`, then Notepad on Windows or nano elsewhere.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.