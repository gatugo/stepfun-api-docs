> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Static Hosting CLI & MCP

This guide is for developers and CI integrators who use StepFun Static Hosting in production. It covers the `steppage` command-line tool (CLI) and Page MCP Server.

The CLI is intended for manual operations and CI/CD pipelines. MCP is intended for MCP-compatible clients, allowing models to call the hosting tools directly. Both use the same Static Hosting API key. Run `steppage --version` to check the installed CLI version.

## Prerequisites

Both methods require **Node.js 20 or later** and a valid Static Hosting API key. You can get the key from the [StepFun Open Platform](https://platform.stepfun.ai) console. After authentication, the CLI and MCP can access only the sites owned by that key.

## steppage CLI

### Install

Install the production release with the one-line curl script:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
curl -fsSL https://dl.stepfun.com/steppage-cli/p/install.sh | bash
```

To pin a version, set the `VERSION` environment variable before the command. The default is `latest`:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
VERSION=v1.0.0 curl -fsSL https://dl.stepfun.com/steppage-cli/p/install.sh | bash
```

The installer downloads the self-contained bundle to `~/.steppage/bin/` and creates an executable wrapper at `~/.local/bin/steppage`. If the installer reports that `~/.local/bin` is not in PATH, add the following line to your shell configuration, such as `~/.zshrc`, and restart the terminal:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
export PATH="$HOME/.local/bin:$PATH"
```

Verify the installation:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
steppage --version
steppage --help
```

### Authenticate

We recommend logging in once to validate and save the key. Replace `YOUR_STEP_API_KEY` in the examples with your Static Hosting API key. `login` checks your identity with the server and saves the key to `~/.steppage/config.json` with file permission `600`:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
steppage login --key YOUR_STEP_API_KEY
steppage whoami
steppage logout
```

In CI and other stateless environments, skip `login` and provide the key through `STEPFUN_API_KEY`. All commands read this environment variable automatically.

### Quick start: deploy a directory

The `deploy` command uploads a build output and publishes a version. Use `--name` to create a site on the first deployment. Add `--go-live` to launch it immediately:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
steppage deploy ./dist --name my-site --go-live
```

To publish a new version to an existing site, use `--site <id>`. `deploy` accepts a directory, scanned recursively, or a single `.zip` archive. If the root of the uploaded directory or ZIP archive does not contain `index.html`, use `--root <file>` to specify the site root page or `--no-root-page` to declare that the site has no root page. Interactive terminals prompt for a root file; CI environments without a TTY require an explicit option.

### Command reference

| Command | Description | Key options |
| - | - | - |
| `login` | Validate and save the hosting API key | `--key YOUR_STEP_API_KEY` |
| `logout` | Clear the saved API key | — |
| `whoami` | Print the identity for the current key | — |
| `deploy <path>` | Upload a build output and publish it | `--site`, `--name`, `--root`, `--no-root-page`, `--go-live` |
| `list` | List your sites | — |
| `get` | View one site | `--site` (required) |
| `update` | Rename a site or change its serving mode | `--site` (required); at least one of `--name` or `--serving-mode` (`spa` or `static`) |
| `delete` | Delete a site permanently | `--site` (required), `--yes` (required in non-TTY environments) |
| `versions` | List site versions | `--site` (required) |
| `promote` | Launch a staged version | `--site`, `--version` (both required) |
| `rollback` | Roll back to an older version | `--site`, `--version` (both required) |
| `preview mint` | Get or create a persistent preview link | `--site`, `--version` (required) |
| `preview expiry` | Set or clear preview expiry | `--site`, `--version`, `--expires` (`never`, `<N>h`, or `<N>d`; all required) |
| `preview revoke` | Revoke a version's preview link | `--site`, `--version` (required) |
| `config --show` | Print the resolved environment and config path | — |

The global `--json` option writes machine-readable JSON to stdout for CI parsing. Use `-H, --header "Name: value"` to inject a custom HTTP header; the option can be repeated. Use `-v, --version` to print the version.

### Typical workflows

**Preview before launch:**

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
steppage deploy ./dist --site 123
steppage preview mint --site 123 --version 456
steppage promote --site 123 --version 456
```

**Rollback:**

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
steppage versions --site 123
steppage rollback --site 123 --version 400
```

**CI integration:**

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
export STEPFUN_API_KEY="YOUR_STEP_API_KEY"
steppage deploy ./dist --site 123 --go-live --json
```

`promote` and `rollback` change the live version. `delete` is irreversible. In an interactive terminal, `delete` requires entering the site name for confirmation; in a non-TTY CI environment, it requires `--yes`.

## Page MCP Server

Page MCP Server exposes deployment, launch, rollback, and inspection capabilities as MCP tools for clients such as Claude. It runs over stdio, uses environment-variable authentication only, and does not read or write the CLI configuration file.

### Install

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
curl -fsSL https://dl.stepfun.com/steppage-mcp/p/install.sh | bash
```

You can also pin a version with `VERSION=v1.0.0`. The installer places the bundle in `~/.steppage-mcp/bin/` and creates the wrapper `~/.local/bin/steppage-mcp`. Use this wrapper path as the MCP client's `command`.

### Configure an MCP client

In the client's MCP configuration, set `command` to the installed wrapper and pass the key through `env`. Example for Claude:

```json theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
{
  "mcpServers": {
    "steppage": {
      "command": "/Users/<you>/.local/bin/steppage-mcp",
      "env": {
        "STEPFUN_API_KEY": "YOUR_STEP_API_KEY"
      }
    }
  }
}
```

Replace `<you>` with your username. An absolute path is recommended. `STEPFUN_API_KEY` is the only required authentication field.

### Tool reference

| Tool | Description | Key parameters |
| - | - | - |
| `page_deploy` | Upload and publish a local directory or `.zip`, returning a preview URL | `path` (required), `site`, `name`, `root`, `noRootPage`, `goLive` |
| `page_list_sites` | List sites owned by the current key | — |
| `page_get_site` | View one site | `site` (required) |
| `page_update_site` | Rename a site or change its serving mode | `site` (required); at least one of `name` or `servingMode` (`spa` or `static`) |
| `page_delete_site` | Permanently delete a site | `site` (required) |
| `page_list_versions` | List site versions | `site` (required) |
| `page_promote` | Launch a staged version | `site`, `version` (both required) |
| `page_rollback` | Roll back to an older version | `site`, `version` (both required) |
| `page_inspect` | View serving configuration, response-header rules, and versions | `site` (required) |
| `page_preview_mint` | Get or create a persistent preview link | `site`, `version` (both required) |
| `page_preview_expiry` | Set or clear preview expiry | `site`, `version`, `expires` (all required) |
| `page_preview_revoke` | Revoke a version's preview link | `site`, `version` (both required) |
| `page_whoami` | View the identity for the current key | — |

ID parameters are numeric strings, and the tool handles them safely as big integers. If a multi-file output has no `index.html`, `page_deploy` requires `root` or `noRootPage` because MCP has no interactive prompt. `page_promote`, `page_rollback`, and `page_delete_site` are destructive operations. Confirm the target before calling them.

## Environment variables and language

| Variable | Applies to | Description |
| - | - | - |
| `STEPFUN_API_KEY` | CLI + MCP | The Static Hosting API key. The CLI can use it instead of `login`; MCP uses it as its only authentication method. |
| `STEPPAGE_OVERSEA` | CLI + MCP | Set to a truthy value to output English. The installer presets the default according to the region. |
| `VERSION` | Installer | Pin an installer version such as `v1.0.0`; the default is `latest`. |

## Troubleshooting

| Symptom | Resolution |
| - | - |
| The installer reports an old or missing Node.js version | Install or upgrade to Node.js 20 or later, then run the installer again. |
| `steppage: command not found` | Add `~/.local/bin` to PATH and restart the terminal. |
| The server rejects the API key | Confirm that the API key is valid and entered correctly. Run `login` again or check `STEPFUN_API_KEY`. |
| Deployment reports a missing `index.html` | Use `--root <file>` to specify the root page or `--no-root-page` to declare that there is no root page. |
| `delete` does nothing or fails in CI | In a non-TTY environment, deletion requires `--yes`. |


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.