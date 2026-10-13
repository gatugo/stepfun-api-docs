> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# steppage: publish static websites

Publish local static output to StepFun Page with the `steppage` plugin, get preview links, and manage versions.

<a id="what-is-steppage" />

The plugin connects through the `steppage-mcp` MCP server to provide deployment, site queries, version management, promotion, and rollback. It accepts a local directory or ZIP for static hosting, not application backends or databases.

## Prerequisites

| Item | Requirement |
| - | - |
| Credentials | `STEPFUN_API_KEY`; a signed-in Step account can provide fallback credentials |
| MCP program | `steppage-mcp`; installed through the official installer if missing |
| Activation | Restart Step Code and check `/mcp` |
| Windows | No automatic MCP installation; use WSL or configure manually |

Install inside Step Code:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
/plugin install steppage
```

The official installer is `https://dl.stepfun.com/steppage-mcp/p/install.sh`, overridable with `STEPCODE_STEPPAGE_INSTALLER_URL`. To run it manually:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
curl -fsSL https://dl.stepfun.com/steppage-mcp/p/install.sh | sh
```

For Bash / Zsh environment-based credentials:

```bash theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
export STEPFUN_API_KEY="YOUR_STEP_API_KEY"
step
```

Replace the placeholder with your key and restart after changing environment variables. See [Static hosting CLI and MCP](/docs/en/guides/developer/static-hosting-cli-mcp) for standalone usage.

See [Plugins](/docs/en/step-code/customization/plugins) for plugin installation and management.

See [MCP](/docs/en/step-code/customization/mcp) for MCP connections and authentication.

## Deployment

<Warning>
  Deployment uploads artifacts to an external hosting service. Public links may be accessed and shared by others. Review content and permissions before publishing.
</Warning>

1. Build your frontend into static output, such as `dist/`.
2. Check entry pages, asset paths, and output contents. Exclude keys, private configuration, and user data.
3. Tell Step Code which directory to publish and whether it should go live.
4. Check the returned preview URL, version, and management link. Open the page in a browser and verify its assets.

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
Publish ./dist as a website and generate a preview link.
```

The model uses `page_deploy` to publish a directory or ZIP as a site version. Results automatically include the management link. Provide a precise site identifier when updating an existing site.

See [Common use cases](/docs/en/step-code/guides/use-cases) for other project task examples.

## Versions and rollback

* Each deployment creates a version; list sites and versions as needed.
* `promote` makes a version live; `rollback` returns to a specified version.
* Verify site and version identifiers before acting, then revisit the page.
* Confirm the target before deleting a site or version; this action may be irreversible.

Example:

```text theme={"theme":{"light":"light-plus","dark":"dark-plus"}}
List this site's recent versions and the current live version. Propose a rollback to the previous stable version, but do not execute it yet.
```

## Management

Use [site management](https://platform.stepfun.com/sites) for sites, versions, and publication status. Hosting allowances, access rules, and limits are governed by the [static hosting documentation](/docs/en/guides/static-hosting) and your account, not by Step Plan model allowances.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.