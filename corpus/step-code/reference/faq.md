> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# FAQ

## Installation and upgrades

### The step command is not found after installation

Open a new terminal so PATH changes take effect. The default installation directory is `~/.stepcode/bin`, or `%USERPROFILE%\.stepcode\bin` on Windows. Check that the executable exists and whether you chose a custom path.

The installer writes a marked PATH block. Check the corresponding shell login configuration.

### How do I upgrade?

Run `step update`. The process includes checksum verification, a smoke test, and rollback on failure.

## Login and models

### Which platform should I choose in /login?

Choose Step Plan for a subscription on `platform.stepfun.com`, or Step Plan Oversea for a subscription on `platform.stepfun.ai`. For pay-as-you-go, use the Open Platform API key for the account's platform. Choose other providers' own entries; do not mix their keys.

### Why is an old key used after I update an environment variable?

Check for saved provider credentials in `~/.stepcode/auth.json`. File credentials override environment variables, and CLI `--api-key` overrides both. Restart from the terminal where the variable is set.

### Why does a custom model not appear in /model?

Check JSON syntax, model IDs, and provider settings in `models.json`. Local services without authentication still need a nonempty `apiKey` placeholder. Reopen `/model` after saving; restart if login or environment variables changed.

### Why did usage increase after switching models?

The new model may not reuse the previous prompt cache, and pricing and tokenization can differ. Check the model, session usage, and account bill rather than estimating costs from conversation length alone.

## Interaction

### Shift+Enter sends a message instead of a newline

Use Ctrl+J or Alt+Enter. Some terminals intercept key combinations; adjust terminal forwarding or Step Code keybindings.

### Why do tools run without approval prompts?

Bypass is the default. Choose Ask in `/permissions`, or Read Only to restrict tools. Operations matched by dangerous-command rules receive separate handling, but those rules are not a sandbox covering every risk.

### Pasting an image fails

Use Ctrl+V, or Alt+V on Windows / WSL. Confirm that the clipboard contains an image, shortcuts do not conflict, and the model accepts images. Alternatively, reference a file with `step @screenshot.png`.

## MCP and plugins

### An MCP server shows failed

Run `step mcp get <name>`. For stdio, check command paths, arguments, dependencies, and variables. For HTTP, check the endpoint, credential variables, and authorization. Do not include real tokens in feedback.

### MCP did not change after installing a plugin

Restart Step Code after installing or removing a plugin, then check `/mcp`. Confirm the program is installed, the project is trusted, and the server is not set to `enabled = false`.

## Data and privacy

### Where is data saved?

Global data defaults to `~/.stepcode/`; project resources use the project's `.stepcode/`. See [Data paths](/docs/en/step-code/configuration/data-paths) for the layout and cleanup.

### Does a local agent mean code is never sent out?

No. Model calls send task-related content, and tools or plugins may access external services. Read-only tools do not modify files, but their results can enter model context. Confirm providers, data-handling requirements, and access scope before working on sensitive projects.

### How do I disable telemetry?

Set this in global `config.toml`:

```toml theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
[telemetry]
enabled = false
```

Telemetry contains device and account identifiers, not prompts, code, or paths. Disabling it does not stop model requests or replace reviewing manually submitted feedback.

## Feedback

Use `/feedback`. Include `step --version`, OS and terminal details, reproduction steps, and redacted errors. Review code, paths, and credentials before sharing session exports or logs.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.