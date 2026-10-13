> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Migrating from other agents

Step Code can reuse Claude Code / Codex workflows: import MCP configuration on first launch, use the Claude Code plugin layout, and load existing `CLAUDE.md` instructions. Login credentials must be configured again.

## What migration does

On first launch, Step Code shows an import screen if it detects Claude Code or Codex MCP configuration. After confirmation, supported servers are written to `[mcp_servers]` in `~/.stepcode/config.toml`.

* Sources include `~/.claude.json` and `~/.codex/config.toml`.
* Source files are read-only: they are not moved, deleted, or overwritten.
* Step Code prompts once for each source, and duplicate content is not imported again.
* Same-name servers with different configurations receive `-claude` / `-codex` suffixes.
* Environment references retain variable names rather than expanding their values into configuration.
* Untranslatable fields generate warnings; review the imported result.

Supported transports are stdio and Streamable HTTP. SSE, WebSocket, and IDE-injected servers are not imported automatically. Configure Claude Code project-level `mcpServers` manually.

## Automatic MCP import

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step mcp list
step mcp get <server-name>
```

Use `/mcp` to inspect connection status and tool counts. Commands, environment variables, and remote permissions must be valid in the environment running Step Code.

Both tools can coexist. After import, the two configurations are maintained independently and are not synchronized automatically.

See [MCP](/docs/en/step-code/customization/mcp) for server management and authentication.

## Using Claude Code plugins

Step Code reads `.claude-plugin/plugin.json`, plus `.mcp.json`, `skills`, `commands`, and `agents` inside the plugin. Marketplace manifests are compatible with `.claude-plugin/marketplace.json`.

Most Claude Code plugins can be installed without changes. See [Plugins](/docs/en/step-code/customization/plugins).

## Project instruction files

Step Code searches from the current directory up to the filesystem root and selects the first matching instruction file in each directory, in the following order:

1. `AGENTS.override.md`
2. `AGENTS.md`
3. `CLAUDE.md`

Global instructions live at `~/.stepcode/agent/AGENTS.md`. Existing `CLAUDE.md` files do not need to be rewritten just to change their name; check that referenced tools, commands, and paths still apply.

Run `/reload` or restart after changes. `--no-context-files` disables automatic discovery; `/init` generates new instructions.

## What is not migrated

| Content | Action |
| - | - |
| Model-provider OAuth credentials | Run `/login` again |
| MCP OAuth authorization | Run `step mcp login <name>` |
| Source tool's project-level MCP configuration | Add it manually as needed |

Do not copy credential files in unknown formats or commit configurations containing keys.

See [Quickstart](/docs/en/step-code/quickstart) for installation and login steps.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.