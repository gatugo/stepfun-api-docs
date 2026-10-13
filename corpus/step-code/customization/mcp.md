> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Model Context Protocol (MCP)

Connect local or remote tools to Step Code through MCP. Once a server connects, the model can call its registered tools as needed.

## Connection methods

| Transport | Configuration | Use case |
| - | - | - |
| stdio | `command`, `args`, optional `env` | Start a local tool process |
| Streamable HTTP | `url` | Connect to a remote MCP service |

Legacy SSE transport is not supported. Plugins can also declare MCP servers; see [Plugins](/docs/en/step-code/customization/plugins).

See [Migrating from other agents](/docs/en/step-code/guides/migration) for importing configuration from other tools.

## Configuration

Declare servers under `[mcp_servers.<name>]` in global `~/.stepcode/config.toml`. Project-level MCP servers are overlaid from installed plugins' `mcpServers` manifests.

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
[mcp_servers.local-tools]
command = "node"
args = ["/absolute/path/to/mcp-server.js"]
env = { LOG_LEVEL = "info" }

[mcp_servers.remote]
url = "https://mcp.example.com/mcp"
bearer_token_env_var = "EXAMPLE_TOKEN"

[mcp_servers.remote.oauth]
callback_port = 8976
```

Replace the paths and endpoint with your service. Choose Bearer or OAuth as required; you do not need both.

| Field | Description |
| - | - |
| `command` | stdio command; choose this or `url` |
| `args`, `env`, `cwd` | Optional arguments, subprocess environment, and working directory |
| `url` | Streamable HTTP endpoint |
| `bearer_token_env_var` | Name of the environment variable holding a Bearer token |
| `http_headers` | Literal headers; avoid embedding real keys |
| `env_http_headers` | Environment variable names for headers; missing variables cause an error |
| `startup_timeout_sec` | Startup timeout, 30 seconds by default |
| `tool_timeout_sec` | Per-call timeout, 300 seconds by default |
| `enabled` | Enable the server; default `true` |
| `enabled_tools`, `disabled_tools` | Tool allowlist and denylist |

See [Configuration files](/docs/en/step-code/configuration/files) for global configuration details.

## Authentication

Read Bearer tokens from the environment running Step Code:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
export EXAMPLE_TOKEN="YOUR_MCP_TOKEN"
step
```

For OAuth services:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step mcp login <server-name>
step mcp logout <server-name>
```

OAuth uses dynamic client registration, PKCE, and a local callback. Tokens are stored atomically in `~/.stepcode/.credentials.json` with `0600` permissions, keyed by server name followed by a vertical bar (`<name>|`). Model-platform login and MCP authorization use separate credentials.

## Command-line management

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step mcp list
step mcp list --json
step mcp get <server-name>
step mcp add remote --url https://mcp.example.com/mcp
step mcp add local-tools -- node /absolute/path/to/mcp-server.js
step mcp remove <server-name>
```

`--url` and a local command are mutually exclusive. `--bearer-token-env-var` is HTTP-only. `--env` sets stdio subprocess variables, not HTTP headers.

## Viewing servers interactively

Use `/mcp` for server status and loaded tool counts. States include `connecting`, `connected`, and `failed`. Servers with `enabled = false` do not appear in the list.

If connection fails, check the command, environment variables, endpoint reachability, and authorization.

## Tool names and filtering

Names use `<server>__<tool>`, with invalid characters converted to underscores. `enabled_tools` and `disabled_tools` filter tools before registration. When an allowlist is set, other tools are unavailable to the model.

## Security

Connect only to trusted servers. stdio servers execute local processes; remote MCP services receive call arguments, and returned content may enter model context.

Bypass skips individual approval for ordinary MCP calls. Use Ask and disable unneeded tools for data transfer, writes, or administrative operations. Built-in command rules cannot infer every side effect of an external MCP service.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.