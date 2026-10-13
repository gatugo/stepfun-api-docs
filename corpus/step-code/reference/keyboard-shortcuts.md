> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Keyboard shortcuts

Use `/hotkeys` to view current shortcuts. Some combinations depend on the OS and terminal; use alternatives or rebind keys when conflicts occur.

## Input and editing

| Shortcut | Action |
| - | - |
| Enter | Send input |
| Shift+Enter, Alt+Enter, Ctrl+J | Insert a newline |
| ↑ / ↓ with empty input | Browse history |
| Home / Ctrl+A; End / Ctrl+E | Move to line start / end |
| Alt+← / →, Ctrl+← / → | Move by word |
| Ctrl+] / Ctrl+Alt+] | Jump forward / backward to a character |
| Backspace; Delete / Ctrl+D | Delete backward / forward |
| Ctrl+W / Alt+Backspace; Alt+D | Delete a word backward / forward |
| Ctrl+U; Ctrl+K | Delete to line start / end |
| Ctrl+Y, Alt+Y | Restore deleted text or cycle the kill ring |
| Ctrl+- | Undo; Ctrl+Z on Windows, Alt+Z on WSL |

See [Interaction and input](/docs/en/step-code/guides/interaction) for input and message queue behavior.

## Global and application shortcuts

| Shortcut | Action |
| - | - |
| Esc | Interrupt output or cancel |
| Ctrl+C | Clear input; exit when input is empty |
| Ctrl+D | Exit with empty input |
| Ctrl+Z | Suspend the process; not supported on native Windows |
| Ctrl+G | Open the external editor |
| Ctrl+V | Paste an image; Alt+V on Windows / WSL |

## Models and output

| Shortcut | Action |
| - | - |
| Ctrl+L | Redraw the screen |
| Ctrl+P | Next selected model |
| Shift+Ctrl+P | Previous model; Alt+P on Windows / WSL |
| Shift+Tab | Cycle permission modes |
| Ctrl+T | Collapse or expand thinking |
| Ctrl+O | Collapse or expand tool output |
| Ctrl+X | Copy a response, selected message, or fullscreen selection depending on context |
| Alt+↑ | Retrieve queued messages; Alt+Q on Windows / WSL |

See [Slash commands](/docs/en/step-code/reference/slash-commands) for the corresponding interactive commands.

## Transcript scrolling and search (fullscreen)

| Shortcut | Action |
| - | - |
| PageUp / PageDown | Scroll by page |
| Ctrl+Shift+F | Search the transcript; Ctrl+F on Windows / WSL |
| Enter / Ctrl+G | Next search result |
| Shift+Enter | Previous search result |
| Ctrl+Shift+↑ / ↓ | Previous / next marked message |

Fullscreen is experimental. Start it with `step --tui-mode fullscreen`.

## Inside /tree

| Shortcut | Action |
| - | - |
| ↑ / ↓ | Browse nodes |
| Enter | Select a node |
| Ctrl+← / →, Alt+← / → | Collapse or expand jumps |
| Shift+L | Edit a label |
| Ctrl+O | Cycle filters |

## Common picker shortcuts

Use arrows and PageUp / PageDown to browse, Enter to confirm, and Esc to cancel.

In `/resume`, Ctrl+S changes sorting, Ctrl+N filters named sessions, Ctrl+R renames, and Ctrl+D deletes. Ctrl+S in model and thinking-level pickers saves the default.

## Customization

Edit `~/.stepcode/agent/keybindings.json`, then run `/reload`. Action names include `tui.input.newLine` and `app.model.select`. For example:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "tui.input.newLine": ["shift+enter", "ctrl+j"]
}
```

Override only the actions you need, avoiding duplicate bindings in the same context. If a binding fails, check terminal interception, action names, and JSON syntax.

See [Configuration files](/docs/en/step-code/configuration/files) for other interface settings.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.