> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Plugins

Step Code distributes extensions, Skills, themes, agents, and MCP servers through resource packages and plugin marketplaces.

## Two distribution formats

| Format | Management | Content |
| - | - | - |
| Packages | `step install` and related commands | TypeScript extensions, Skills, prompt templates, themes |
| Plugin marketplace | `/plugin` | Declarative manifests, Skills, agents, commands, MCP |

## Packages: installation and management

These names and addresses illustrate source formats; replace them with trusted resources:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
step install npm:@example/package@1.0.0
step install git:github.com/example/repo@v1
step install https://github.com/example/repo
step install /absolute/path/to/package
step list
step remove npm:@example/package
step update --all
step update --extensions
```

* Installs default to user scope and write global configuration.
* `-l` writes project `.stepcode/config.toml`; trusted projects automatically install missing packages on startup.
* `step -e <source>` loads an extension temporarily without persisting configuration, but still executes its code.
* `step update --all` updates Step Code and all packages; `step update --extensions` updates only packages and pinned Git refs.

## Package sources and manifests

| Source | Behavior |
| - | - |
| `npm:` | Install with the package manager; version-specific entries remain pinned |
| `git:` or repository URL | Clone the repository; configured tags or commits do not automatically move to new refs |
| Local file | Load as a single extension |
| Local directory | Discover content using package conventions |

Declare `extensions`, `skills`, `prompts`, and `themes` resource paths in `package.json`, with glob and `!` exclusion support. Without a manifest, same-named conventional directories are used. Paths are relative to the package root.

User packages typically live in `~/.stepcode/agent/npm/` and `git/`; project packages in `.stepcode/npm/` or `.stepcode/git/`. Do not keep your only uncommitted changes in managed clones; updates may realign pinned refs.

See [Agent Skills](/docs/en/step-code/customization/skills) for the Skill format.

## Dependencies and bundling

Put runtime dependencies in `dependencies`; installation uses `npm install --omit=dev`. Put runtime-provided core packages in `peerDependencies: "*"` rather than bundling them again.

For dependencies on other Step packages, declare both `dependencies` and `bundledDependencies`, and reference resources through `node_modules/` paths.

## Filtering and enabling packages

Limit loaded resources in `config.toml`:

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
[[packages]]
source = "npm:@example/package"
extensions = ["extensions/*.ts", "!extensions/legacy.ts"]
```

Use glob patterns, `!` exclusions, and exact `+path` / `-path` controls. `step config` provides interactive management; Tab switches global and project scope.

Project entries override same-name global packages. Project resources remain subject to trust settings.

## Plugin marketplaces

| Command | Action |
| - | - |
| `/plugin` | Open the management menu |
| `/plugin install <plugin>` | Install a plugin |
| `/plugin remove <plugin>` | Uninstall a plugin |
| `/plugin marketplace list` | List marketplace sources |
| `/plugin marketplace add` | Add a marketplace |
| `/plugin marketplace update` | Refresh marketplace indexes |
| `/plugin marketplace remove` | Remove a marketplace |

The native manifest is `step.plugin.json`, with compatibility for `.claude-plugin/plugin.json` and marketplace manifests in `marketplace.json`. Fields include `id`, `name`, `description`, `version`, `entry`, `skills`, `agents`, `commands`, `mcpServers`, and `provision`. `id` is required; the manifest file size limit is 512 KiB. `entry` records an executable entry point but is not loaded.

Restart Step Code after installing or removing MCP plugins to start or stop their servers. Check results with `/mcp`.

See [MCP](/docs/en/step-code/customization/mcp) for MCP server configuration fields.

See [Agents and subagents](/docs/en/step-code/customization/agents) for the custom agent format.

## StepPage: publishing static websites

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
/plugin install steppage
```

The built-in `steppage` marketplace plugin publishes directories or ZIP files, lists sites and versions, promotes or rolls back versions, and generates preview links. It needs `STEPFUN_API_KEY` or a signed-in Step account. Missing `steppage-mcp` is installed through the official installer; automatic installation is not available on Windows. See [steppage](/docs/en/step-code/reference/steppage).

Manage sites at [platform.stepfun.com/sites](https://platform.stepfun.com/sites). The built-in marketplace also offers the `playwright` browser-control plugin, using `npx @playwright/mcp@latest`.

## Security notes

Extensions, packages, and stdio MCP servers can execute code with the current user's system permissions. Skill and agent instructions can also lead to command execution. Package and Git dependency installation may run package-manager operations. Review sources, versions, and install scripts. Install only trusted sources and provide the minimum necessary credentials.

Step Code has no file-based Hooks. Use extension events such as `tool_call`, `tool_result`, and `input` for equivalent automation and interception.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.