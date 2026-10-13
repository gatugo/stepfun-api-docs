---
card: static-hosting
tier: by-task
status: draft
verified_on: 2026-10-08 (Step Plan verified; Standard channel steppage uses its own key, not the API key)
source: corpus/guides/static-hosting.md, corpus/guides/developer/static-hosting-cli-mcp.md, corpus/step-code/reference/steppage.md
---

# Static Hosting (steppage)

**Publish a built static site and get shareable preview links — no server, no CDN setup.** Three ways in: the **My Sites** console, the `steppage` CLI, or the Page MCP Server.

**Static files only — there is no server runtime.** PHP, Python, and Node.js server-side code is not executed. This is not for application backends or databases.

| Concept | Meaning |
| --- | --- |
| Site | An independent website project: name, URL, serving mode, multiple versions |
| Version | A snapshot of files created by a deployment (`v1`, `v2`, …); previewable, launchable, rollbackable |
| Preview link | Temporary shareable link for one version; does not change the live version; can expire or be revoked |
| Live version | The single version currently served to visitors |
| Root page | The file returned for `/`, usually `index.html` |

## Limits and file types

| Limit | Value |
| --- | --- |
| Total deployment size | ≤ **50 MB** |
| Files per deployment | ≤ **5,000** |
| Site name length | ≤ **64 characters** |
| Saved versions | Account quota; delete older versions when the limit is hit |

Supported extensions: `html`, `htm`, `css`, `js`, `mjs`, `json`, `map`, `txt`, `xml`, `svg`, `ico`, `png`, `jpg`, `jpeg`, `gif`, `webp`, `avif`, `woff`, `woff2`, `ttf`, `otf`, `eot`, `wasm`, `pdf`, `mp4`, `webm`, `mp3`, `wav`, `md`, `markdown`, `jsonl`, `tsx`, `jsx`.

**Prohibited (rejected):** `php`, `py`, `exe`, `sh`, `bat`, `cmd`, `dll`, `so`, `jsp`, `asp`, `aspx`, `cgi`, `pl`. Anything outside the supported list is rejected — including inside ZIP archives, which are re-checked after extraction. Upload a `dist`/`build` output, not source or `node_modules`.

## Console workflow (My Sites)

1. Sign in at `https://platform.stepfun.ai`, open **My Sites** → **New Site**. The list supports name search and filtering by All / Live / Draft / Error.
2. **Publish Site**: enter a title, drag in a single `.zip`, a folder, or multiple files. Uploading a **folder strips the outermost common directory** (`dist/index.html` → `index.html`).
3. **Root page**: `index.html` at the upload root is used automatically; otherwise pick an HTML file or choose **No root page** (404 at `/`).
4. **Publish** → **Open Preview** → find the version in history → **Launch** → confirm. The **first deployment generates a preview only**; the live URL appears after the first launch.

> **ZIP gotcha:** you cannot choose the root page in the upload window — put `index.html` at the archive root or the deployment fails.

## Serving modes

| Mode | Unknown routes | Use for |
| --- | --- | --- |
| **SPA** | Returns the root page (usually `index.html`) | React Router / Vue Router; refreshing `/about` hands off to the frontend |
| **Static** | Missing files return 404 | Sites where each URL maps to a real file |

Changing the serving mode takes effect immediately. Set it in **Site Settings**.

## Custom response headers

Put `page.config.json` in the **root directory** of the uploaded package:

```json
{
  "headers": [
    {"path": "/*",        "name": "X-Frame-Options", "value": "DENY"},
    {"path": "/assets/*", "name": "Cache-Control",   "value": "public, max-age=31536000, immutable"}
  ]
}
```

| Field | Meaning |
| --- | --- |
| `path` | Path pattern such as `/*` or `/assets/*` |
| `name` | Response header name |
| `value` | Response header value |

The parsed rules for the live version are shown read-only in the **Response Header Rules** tab; to change them, edit `page.config.json` and publish a new version. **A version with invalid configuration is rejected and cannot be launched.**

## Build-time environment variables

Configure in **Site Settings → Environment Variables** — up to **50 per site**. Names must start with an uppercase letter and contain only uppercase letters, numbers, and underscores (e.g. `API_BASE_URL`), unique per site. Values are one line, ≤ **2,048 characters**.

Reference them as `{{PAGE_ENV:VARIABLE_NAME}}`:

```js
const apiBase = '{{PAGE_ENV:API_BASE_URL}}'
```

Placeholders are replaced during the deployment build in text files only (`.html`, `.htm`, `.js`, `.css`, `.json`, `.txt`, `.svg`, `.xml`). Images, fonts, audio, video, and PDF are untouched; **undefined placeholders stay as-is**. Saving a variable does not rewrite published versions — upload and publish a new build output after changing one; republishing an old version does not inject the new value.

> Do not put passwords, private keys, long-lived tokens, or other sensitive data in frontend environment variables — static files are sent to visitors, who can inspect injected values.

## Preview links, launch, rollback, republish

| Action | Behaviour |
| --- | --- |
| Preview expiry | `never` / `24 hours` / `7 days` / `30 days`; a revoked link returns 404 immediately, expired links stop working, a new link can be minted after revocation |
| Launch | Only non-live, non-rejected versions can be submitted; server-side validation decides the final result |
| Roll back | Pick an earlier version → Roll Back; it becomes live and the previous live version stays in history |
| Republish (no new files) | Reactivates the current live version |
| Republish (with new files) | Creates a new version — preview first, launch after review |

## steppage CLI

Requires **Node.js 20+** and a Static Hosting API key; after authentication it can access only sites owned by that key.

```bash
curl -fsSL https://dl.stepfun.com/steppage-cli/p/install.sh | bash
VERSION=v1.0.0 curl -fsSL https://dl.stepfun.com/steppage-cli/p/install.sh | bash   # pin a version
```

Installs to `~/.steppage/bin/` with a wrapper at `~/.local/bin/steppage`; add `export PATH="$HOME/.local/bin:$PATH"` if that directory is not on PATH.

```bash
steppage login --key YOUR_STEP_API_KEY   # saves key to ~/.steppage/config.json (chmod 600)
steppage whoami
steppage logout
```

In CI, skip `login` and export `STEPFUN_API_KEY`; all commands read it automatically.

| Command | Description | Key options |
| - | - | - |
| `login` | Validate and save the hosting API key | `--key` |
| `logout` | Clear the saved API key | — |
| `whoami` | Print the identity for the current key | — |
| `deploy <path>` | Upload a build output and publish it | `--site`, `--name`, `--root`, `--no-root-page`, `--go-live` |
| `list` | List your sites | — |
| `get` | View one site | `--site` (required) |
| `update` | Rename or change serving mode | `--site` (required); `--name` or `--serving-mode` (`spa`/`static`) |
| `delete` | Permanently delete a site | `--site` (required), `--yes` (required non-TTY) |
| `versions` | List site versions | `--site` (required) |
| `promote` | Launch a staged version | `--site`, `--version` (required) |
| `rollback` | Roll back to an older version | `--site`, `--version` (required) |
| `preview mint` | Get or create a persistent preview link | `--site`, `--version` (required) |
| `preview expiry` | Set or clear preview expiry | `--site`, `--version`, `--expires` (`never`, `<N>h`, `<N>d`) |
| `preview revoke` | Revoke a version's preview link | `--site`, `--version` (required) |
| `config --show` | Print resolved environment and config path | — |

Global `--json` writes machine-readable JSON to stdout; `-H, --header "Name: value"` injects a custom HTTP header (repeatable); `-v, --version` prints the version.

```bash
steppage deploy ./dist --name my-site --go-live          # create + launch
steppage deploy ./dist --site 123                        # new version on an existing site
steppage preview mint --site 123 --version 456           # preview before launch
steppage promote --site 123 --version 456
steppage versions --site 123 && steppage rollback --site 123 --version 400
export STEPFUN_API_KEY="..." && steppage deploy ./dist --site 123 --go-live --json   # CI
```

`deploy` accepts a recursively scanned directory or a single `.zip`. If the root has no `index.html`, use `--root <file>` or `--no-root-page`; interactive terminals prompt for a root file, **CI without a TTY requires an explicit option**.

## Page MCP Server

Exposes deployment, launch, rollback, and inspection as MCP tools for clients such as Claude. Runs over stdio, uses **environment-variable authentication only**, and does not read or write the CLI config file.

```bash
curl -fsSL https://dl.stepfun.com/steppage-mcp/p/install.sh | bash
```

Installs to `~/.steppage-mcp/bin/` with wrapper `~/.local/bin/steppage-mcp` (use as the MCP client's `command`; `VERSION=v1.0.0` pins a version).

```json
{
  "mcpServers": {
    "steppage": {
      "command": "/Users/<you>/.local/bin/steppage-mcp",
      "env": {"STEPFUN_API_KEY": "YOUR_STEP_API_KEY"}
    }
  }
}
```

| Tool | Description | Key parameters |
| - | - | - |
| `page_deploy` | Upload and publish a local directory or `.zip`, returning a preview URL | `path` (required), `site`, `name`, `root`, `noRootPage`, `goLive` |
| `page_list_sites` | List sites owned by the current key | — |
| `page_get_site` | View one site | `site` (required) |
| `page_update_site` | Rename or change serving mode | `site` (required); `name` or `servingMode` (`spa`/`static`) |
| `page_delete_site` | Permanently delete a site | `site` (required) |
| `page_list_versions` | List site versions | `site` (required) |
| `page_promote` | Launch a staged version | `site`, `version` (required) |
| `page_rollback` | Roll back to an older version | `site`, `version` (required) |
| `page_inspect` | View serving config, response-header rules, versions | `site` (required) |
| `page_preview_mint` | Get or create a persistent preview link | `site`, `version` (required) |
| `page_preview_expiry` | Set or clear preview expiry | `site`, `version`, `expires` (required) |
| `page_preview_revoke` | Revoke a version's preview link | `site`, `version` (required) |
| `page_whoami` | View the identity for the current key | — |

ID parameters are numeric strings handled as big integers. If a multi-file output has no `index.html`, `page_deploy` requires `root` or `noRootPage` — **MCP has no interactive prompt**. `page_promote`, `page_rollback`, and `page_delete_site` are destructive: confirm the target first.

## Step Code plugin

`/plugin install steppage` inside Step Code, then restart and check `/mcp`. Credentials: `STEPFUN_API_KEY` (a signed-in Step account can provide fallback credentials). Official installer `https://dl.stepfun.com/steppage-mcp/p/install.sh`, overridable via `STEPCODE_STEPPAGE_INSTALLER_URL`. **Windows has no automatic MCP installation — use WSL or configure manually.** Then tell Step Code e.g. "Publish ./dist as a website and generate a preview link." Site management lives at `https://platform.stepfun.com/sites`.

> **Warning:** deployment uploads artifacts to an external hosting service. Public links may be accessed and shared by others — review content and permissions before publishing.

## Environment variables

| Variable | Applies to | Description |
| - | - | - |
| `STEPFUN_API_KEY` | CLI + MCP | Static Hosting API key; CLI alternative to `login`, MCP's only auth method |
| `STEPPAGE_OVERSEA` | CLI + MCP | Truthy value outputs English; installer presets the default per region |
| `VERSION` | Installer | Pin an installer version such as `v1.0.0`; default `latest` |

## Troubleshooting

| Symptom | Resolution |
| - | - |
| Installer reports old/missing Node.js | Install or upgrade to Node.js 20+, then rerun the installer |
| `steppage: command not found` | Add `~/.local/bin` to PATH and restart the terminal |
| Server rejects the API key | Confirm the key is valid and correctly entered; rerun `login` or check `STEPFUN_API_KEY` |
| Deployment reports missing `index.html` | Use `--root <file>` or `--no-root-page` |
| `delete` fails in CI | Non-TTY deletion requires `--yes` |
| `/` returns 404 | `index.html` at the upload root; correct root page selected for file/folder uploads; site not set to No root page; site is live, not preview-only |
| Refreshing a frontend route returns 404 | Switch the serving mode to SPA — Static mode returns only files that exist |
| Deployment rejects a file type | Check the file name/extension in the error message, remove prohibited or unsupported files, and publish again; ZIP contents are checked too |
| Environment variables not updated | Replaced at build time — confirm the variable is saved, upload a new build output, and publish a new version |
| Preview link does not open | Check expiry/revocation and mint a new one; links cannot be restored after the version or site is deleted |
| A new version cannot be launched | Check the version status label — review rejection, submission failure, or a rejected `page.config.json` can block launch |

**Deleting** requires typing the full site name in the confirmation dialog and is permanent: the site, all versions, the live URL, and preview links become invalid. Back up needed versions with the version download feature first. CLI `delete` needs `--yes` in non-TTY environments.

## Deployment checklist

- [ ] Entry file and resource paths are relative with matching case
- [ ] Root directory has `index.html`, or another root page is explicitly selected
- [ ] Serving mode matches the app type (SPA or Static)
- [ ] `node_modules`, source code, and server-side scripts removed
- [ ] Package ≤ 50 MB and ≤ 5,000 files
- [ ] Environment variables saved and free of sensitive information

## Related cards

[client-setup.md](client-setup.md) — MCP clients that can call the steppage tools · [errors-and-debugging.md](errors-and-debugging.md)
