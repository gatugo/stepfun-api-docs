> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Custom themes

Step Code includes six themes and supports custom colors in JSON. Place a file in a theme directory to select it in `/theme`. Editing the active theme reloads it immediately.

## Built-in themes

| Theme | Purpose |
| - | - |
| `step-blue` | Default blue theme |
| `step-violet` | Purple for dark terminals |
| `step-violet-light` | Purple for light terminals |
| `dark`, `light` | General dark and light themes |
| `sage` | Green for dark terminals |

## Theme files

| Scope | Path |
| - | - |
| User | `~/.stepcode/agent/themes/*.json` |
| Project | `.stepcode/themes/*.json`; requires trust |
| Package | Theme directory in a resource package |
| Launch option | `--theme <path>`, repeatable |

The filename is the theme name, such as `my-theme.json`. Custom themes appear alongside built-in themes in `/theme`. Start from a complete theme and retain all color fields while adjusting the palette.

See [Plugins](/docs/en/step-code/customization/plugins) for distributing themes in resource packages.

## Theme JSON format

A theme has `name`, reusable `vars`, and a `colors` mapping. This example illustrates fields; it is not a complete replacement theme:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "name": "my-theme",
  "vars": {"primary": "#7aa2f7"},
  "colors": {
    "accent": "primary",
    "text": "#c0caf5",
    "mdTableHeader": "#9d7cd8",
    "syntaxKeyword": "#bb9af7"
  }
}
```

A complete theme defines all 52 color tokens, covering core UI, backgrounds and content, Markdown, diffs, syntax highlighting, thinking borders, and bashMode.

| Value | Meaning |
| - | - |
| `"#ff0000"` | Six-digit hexadecimal color |
| `39` | xterm 256-color index |
| `"primary"` | Reference a variable in `vars` |
| `""` | Use the terminal default |

True-color terminals use 24-bit colors; others may fall back to nearby 256-color values. Use brighter, saturated colors on dark terminals and darker, muted colors on light terminals. Put shared base colors in `vars`.

## Switching themes

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
/theme
/theme my-theme
```

Set the default in configuration:

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
theme = "my-theme"
```

For one launch only:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step --use-theme light
```

`/theme` opens the picker; custom themes are available without restarting. `/theme <name>` switches directly. Editing the active file hot-reloads it.

<a id="statustips" />

Working-line tips are controlled by `statusTips` in `config.toml`. See [Configuration files](/docs/en/step-code/configuration/files).

## Error behavior

Invalid colors fail the entire theme and fall back to built-in `dark`. A transient error during hot reload retains the active theme. Check JSON syntax, color values, variable references, and field completeness.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.