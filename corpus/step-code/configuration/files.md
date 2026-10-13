> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuration files

Use `config.toml` for default models, permissions, context compaction, the interface, and MCP servers. Temporary launch options do not automatically rewrite the file.

## Configuration locations

| Scope | Default location | Purpose |
| - | - | - |
| Global | `~/.stepcode/config.toml` | Applies across projects |
| Project | `<project>/.stepcode/config.toml` | Overrides global settings; requires project trust |

Project configuration merges nested objects key by key and replaces arrays as a whole. Settings marked global-only, such as the proxy and default project trust, cannot be overridden by a project.

The global file is created on first run. Writes use an atomic temporary-file-and-rename operation and preserve the leading comment block. TOML does not support `null`; unsupported expressions are stripped. Remove an optional key to unset it.

<a id="complete-example" />

See [Data paths](/docs/en/step-code/configuration/data-paths) for other local data locations.

## Configuration example

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
theme = "step-blue"
defaultProvider = "step"
defaultModel = "step-3.7-flash"
permissionPreset = "bypass"
autoResume = true

[telemetry]
enabled = true
```

This example uses the default Bypass mode. Change `permissionPreset` to `"ask"` to require individual approvals.

## Top-level fields

### Models and thinking

| Field | Description |
| - | - |
| `defaultProvider`, `defaultModel` | Default provider and model; save with Ctrl+S in `/model` |
| `defaultThinkingLevel` | Default thinking level |
| `modelThinkingLevels` | Per-model thinking levels keyed by `provider/modelId` |
| `thinkingBudgets` | Token budgets for thinking levels |
| `hideThinkingBlock` | Hide thinking-block display; default `false` |
| `showCacheMissNotices` | Show cache-miss and compaction-cost notices; default `false` |

Client levels are `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`. Available levels and their effective behavior depend on the provider and model.

See [Platforms and models](/docs/en/step-code/configuration/models) for provider setup and model selection.

### Interface

| Field | Default | Description |
| - | - | - |
| `theme` | `step-blue` | Theme name |
| `statusTips` | `true` | Show one working-line tip per turn; set to `false` to disable |
| `quietStartup` | `false` | Reduce startup output |
| `collapseChangelog` | `false` | Collapse the changelog |
| `doubleEscapeAction` | `tree` | Double-Esc action with empty input: `tree`, `fork`, `none` |
| `treeFilterMode` | `default` | `default`, `no-tools`, `user-only`, `labeled-only`, `all` |
| `editorPaddingX` | `0` | Horizontal input padding, 0–3 |
| `outputPad` | `1` | Horizontal output padding, 0 or 1 |
| `autocompleteMaxVisible` | `5` | Visible completion items, 3–20 |
| `showHardwareCursor` | `false` | Show the terminal hardware cursor |
| `externalEditor` | Unset | External editor; otherwise checks `VISUAL`, then `EDITOR` |

Disable working-line tips:

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
statusTips = false
```

### Sessions and networking

| Field | Default | Description |
| - | - | - |
| `sessionDir` | Unset | Custom session directory |
| `transport` | `auto` | Model transport: `auto`, `sse`, `websocket`, `websocket-cached`; requires provider support |
| `steeringMode`, `followUpMode` | `one-at-a-time` | Message delivery during streaming |
| `httpProxy` | Unset | Outbound proxy; global-only |
| `httpIdleTimeoutMs` | 300,000 | HTTP idle timeout in milliseconds; 0 disables |
| `websocketConnectTimeoutMs` | 15,000 | WebSocket connection timeout in milliseconds; 0 disables |

See [Environment variables](/docs/en/step-code/configuration/environment) for environment-based configuration.

### Shell and commands

| Field | Default | Description |
| - | - | - |
| `shellPath` | Unset | Custom shell path with `~` expansion, useful for environments such as Cygwin |
| `shellCommandPrefix` | Unset | Content prepended to each shell command, such as alias setup |
| `npmCommand` | Unset | npm command as argv, such as `["mise", "exec", "node@20", "--", "npm"]` |

### Projects and permissions

| Field | Default | Description |
| - | - | - |
| `permissionPreset` | `bypass` | `ask`, `read-only`, `bypass`, or `autopilot` |
| `defaultProjectTrust` | `ask` | Resource-loading policy for untrusted projects; global-only |
| `enableAnalytics` | `false` | Optional usage analytics, separate from feedback and other services |

Project trust controls loading configuration, extensions, and resources. It is not a filesystem sandbox.

## Section settings

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
[compaction]
enabled = true
reserveTokens = 16384
keepRecentTokens = 20000
contextProjection = "off"

[branchSummary]
reserveTokens = 16384
skipPrompt = false

[retry]
enabled = true
maxRetries = 3
baseDelayMs = 2000

[thinkingBudgets]
minimal = 1024
low = 4096
medium = 10240
high = 32768

[images]
autoResize = true
blockImages = false

[terminal]
showImages = true
imageWidthCells = 60
clearOnShrink = false
showTerminalProgress = false
hyperlinks = "auto"
images = "auto"
trueColor = "auto"

[markdown]
codeBlockIndent = "  "
mermaid = "streaming"
```

* `[compaction].enabled = false` only disables automatic compaction. `reserveTokens` reserves window space; `keepRecentTokens` controls recent messages retained.
* `[branchSummary].skipPrompt = true` skips the branch-switch prompt and does not generate a summary by default.
* `[retry].baseDelayMs = 2000` uses exponential backoff: 2, 4, and 8 seconds. Keep `provider.maxRetries` at its default `0`; positive values let SDK retries precede Step's quota handling and may wait until quota resets. `provider.timeoutMs` sets a per-request timeout.
* `[thinkingBudgets]` sets token budgets for thinking levels.
* `[images].autoResize = true` resizes images to within 2,000 px.
* `[images].blockImages = true` prevents sending images to models; `[terminal].showImages` only controls display.
* `[terminal].images` accepts `kitty`, `iterm2`, `auto`, or `false`; match it to terminal capabilities.
* `[terminal].imageWidthCells` measures inline width in terminal columns. `clearOnShrink` controls clearing after content shrinks, `showTerminalProgress` controls OSC 9;4 progress, and `hyperlinks` accepts `true`, `false`, or `"auto"`.
* `[markdown].mermaid` accepts `streaming`, `final`, or `off`.
* `[warnings].anthropicExtraUsage` defaults to `true` and controls Claude Pro/Max extra-usage notices.

## MCP servers

Declare servers in the global configuration:

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
[mcp_servers.local-tools]
command = "node"
args = ["/absolute/path/to/mcp-server.js"]
env = { LOG_LEVEL = "info" }
startup_timeout_sec = 30
tool_timeout_sec = 300
```

Replace the path with your server script. See [MCP](/docs/en/step-code/customization/mcp) for transports, authentication, and filtering.

## Tool and resource arrays

| Field | Purpose |
| - | - |
| `defaultTools` | Built-in allowlist: `read`, `bash`, `powershell`, `edit`, `write`, `grep`, `find`, `ls`; an empty array leaves only extension tools |
| `enabledModels` | Models cycled with Ctrl+P; supports glob patterns such as `["claude-*", "gpt-4o"]` |
| `packages` | Resource packages to install and load |
| `extensions`, `skills`, `prompts`, `themes` | Extra resource paths with glob, exclusion, and exact selection support |
| `enableSkillCommands` | Register Skills as `/skill:<name>`; default `true` |

Resource arrays accept files or directories, glob patterns, `!` exclusions, and exact `+path` / `-path` controls. Global relative paths resolve from `~/.stepcode/agent`; project paths resolve from `.stepcode`. See [Built-in tools](/docs/en/step-code/reference/tools) for launch options.

## TUI settings

| Field | Default | Description |
| - | - | - |
| `tuiMode` | `regular` | Also accepts experimental `fullscreen` |
| `fullscreenExitOutput` | `transcript` | Show the transcript on exit, or use `resume-hint` |
| `fullscreenScrollbar` | `auto` | Also accepts `always`, `hidden` |
| `fullscreenCopyOnSelect` | `true` | Copy on selection; use Ctrl+X when disabled |

## Deprecated settings

| Item | Status |
| - | - |
| `~/.stepcode/agent/settings.json` | Retired and no longer read or written; migrate settings manually to `config.toml` |
| `~/.stepcode/agent/step-settings.json` | Retired |
| `~/.stepcode/agent/auth.json`, `agent/models.json` | Old locations; now at the `~/.stepcode` root |
| `.step-harness` | Retired and no longer written; old credentials are read once during startup migration |


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.