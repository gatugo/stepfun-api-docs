> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# The step command

Use `step` to start sessions or manage installation, resource packages, and MCP servers.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step [options] [--] [@files...] [task...]
```

Inspect available options and the installed version:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step --help
step --version
```

## Model options

| Option | Description |
| - | - |
| `--provider <name>` | Provider such as `step`, `anthropic`, or `openai` |
| `--model <model>` | Model ID or pattern; supports `provider/id` and a thinking-level suffix |
| `--api-key <key>` | Override other credentials; beware of shell history and process-argument exposure |
| `--thinking <level>` | `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`, subject to model support |
| `--models <list>` | Comma-separated models for Ctrl+P cycling |
| `--list-models [search]` | List available models |

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step --provider step --model step-3.7-flash
step --list-models flash
```

See [Keyboard shortcuts](/docs/en/step-code/reference/keyboard-shortcuts) for model-switching shortcuts.

## Session options

| Option | Description |
| - | - |
| `-c`, `--continue` | Continue the most recent session |
| `-r`, `--resume` | Browse sessions; optionally supply a path or ID |
| `--session <path-or-ID>` | Select a session, including by partial ID |
| `--fork <path-or-ID>` | Fork a session |
| `--session-dir <directory>` | Override the session directory |
| `--no-session` | Do not save this session |
| `--name <name>`, `-n <name>` | Name the session |
| `-p`, `--print` | Run once and exit; accepts stdin and `@files` |

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step --name "Interface review" @README.md "Summarize the interface contracts"
step -p @screenshot.png "Explain the error in this screenshot"
step --no-session -p "Explain semantic versioning"
```

See [Slash commands](/docs/en/step-code/reference/slash-commands) for interactive session commands.

## Tool options

| Option | Description |
| - | - |
| `--tools <list>`, `-t <list>` | Comma-separated allowlist for built-in and extension tools |
| `--exclude-tools <list>`, `-xt <list>` | Exclude tools |
| `--no-builtin-tools`, `-nbt` | Disable built-in tools, keeping extensions |
| `--no-tools`, `-nt` | Disable all tools |

For example, allow file reading and search:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step --tools read,grep,find,ls -p "Check README against the project structure without modifying files"
```

See [Approval flow](/docs/en/step-code/guides/interaction#approval-flow) for permissions and dangerous operations.

## Resource options

| Option | Description |
| - | - |
| `-e <source>`, `--extension <source>` | Load an extension temporarily; repeatable |
| `--skill <path>` | Explicitly load a Skill; repeatable |
| `--prompt-template <path>` | Load a prompt template; repeatable |
| `--theme <path>` | Load a theme resource; repeatable |
| `--no-extensions`, `--no-skills`, `--no-prompt-templates`, `--no-themes` | Disable corresponding automatic discovery |
| `--no-context-files`, `-nc` | Disable automatic project-instruction loading |

Explicit resources can be combined with options disabling discovery. They must still come from trusted sources.

See [Configuration files](/docs/en/step-code/configuration/files) for persistent resource configuration.

## Other options

| Option | Description |
| - | - |
| `--plan` | Start in Plan mode |
| `--tui-mode <mode>` | `regular` or experimental `fullscreen` |
| `--approval-mode <mode>` | Approval policy for non-interactive mode |
| `--version` | Show version |
| `--use-theme <name>` | Theme for this launch |
| `--export <session-file> [output-file]` | Export a session to HTML |
| `--` | End option parsing; remaining arguments are messages or file references |

## Subcommands

| Command | Description |
| - | - |
| `step update` | Update to the latest stable version; alias `step upgrade` |
| `step update <version>` | Install a version, for example `step update 0.4.0` |
| `step update --all` | Update Step Code and all packages |
| `step update --extensions` | Update only packages |
| `step install <source>` | Install a resource package |
| `step remove <source>` | Remove a resource package |
| `step list` | List packages |
| `step config` | Manage resources interactively; Tab switches global and project scope |
| `step mcp` | MCP `list`, `get`, `add`, `remove`, `login`, `logout` |
| `step login`, `step logout` | Sign in to or out of Step |
| `step login status` | Show Step login method and status |

Updates include download, checksum verification, a smoke test, and rollback on failure. Replace the example `0.4.0` with the release you need. See [Plugins](/docs/en/step-code/customization/plugins) for package sources and pinning.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.