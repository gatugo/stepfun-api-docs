---
card: client-setup
tier: by-task
status: draft
verified_on: 2026-10-08 (Step Plan verified; Standard column unverified)
source: corpus/guides/developer/integrations/claude-code.md, corpus/guides/developer/integrations/cursor.md, corpus/guides/developer/integrations/cline.md, corpus/guides/developer/integrations/pi.md, corpus/guides/developer/integrations/roo-code.md
---

# Client Setup: 16 Developer Tools

> **Status: draft.** Standard-channel base URLs are noted where sources document
> them. Verify per tool before pointing production pipelines at the standard
> channel.

**Use the Step Plan channel and a Step Plan API key for every tool below** unless
explicitly noted otherwise. The standard `https://api.stepfun.ai/v1` addresses
are the pay-as-you-go channel and are only listed where a source documents them.

Three base URL families cover all 16 tools:

| Family | Step Plan Base URL | Standard Base URL | Client appends | Used by |
| --- | --- | --- | --- | --- |
| Anthropic Messages | `https://api.stepfun.ai/step_plan` | `https://api.stepfun.ai/v1` | `/v1/messages` | Claude Code, Pi, Oh My Pi |
| OpenAI Chat Completions | `https://api.stepfun.ai/step_plan/v1` | `https://api.stepfun.ai/v1` | `/chat/completions` | Cline, Roo Code, Kilo Code, OpenCode, Cursor, Goose, Zed, Cherry Studio, CodeGPT, DeepSeek Harness, Hermes Agent, OpenClaw |
| OpenAI Responses | `https://api.stepfun.ai/step_plan/v1/responses` | `https://api.stepfun.ai/v1/responses` | nothing — this is the request path | Codex CLI |

Prerequisite for every tool: an active Step Plan subscription with quota and access to the chosen model. Create the key in the console; never commit it.

## Tool index

| Tool | Type | Channel | Base URL |
| :- | :- | :- | :- |
| Claude Code | terminal agent (Anthropic) | Step Plan | `https://api.stepfun.ai/step_plan` |
| Pi | terminal agent (Anthropic Messages) | Step Plan | `https://api.stepfun.ai/step_plan` |
| Oh My Pi | Pi extension (roles/skills) | Step Plan | `https://api.stepfun.ai/step_plan` |
| Cline | VS Code / Cursor agent | Step Plan | `https://api.stepfun.ai/step_plan/v1` |
| Roo Code | VS Code / Cursor agent | Step Plan | `https://api.stepfun.ai/step_plan/v1` |
| Kilo Code | VS Code / Cursor agent | Step Plan | `https://api.stepfun.ai/step_plan/v1` |
| OpenCode | terminal agent | Step Plan | `https://api.stepfun.ai/step_plan/v1` |
| Cursor | IDE (BYOK) | both (sources list standard) | `https://api.stepfun.ai/step_plan/v1` (Step Plan) / `https://api.stepfun.ai/v1` (Standard) |
| Codex CLI | terminal agent (Responses API) | Step Plan | `https://api.stepfun.ai/step_plan/v1/responses` |
| Goose | agent client (OpenAI Compatible) | Step Plan | `https://api.stepfun.ai/step_plan/v1` |
| Zed | editor AI Assistant | Step Plan | `https://api.stepfun.ai/step_plan/v1` |
| Cherry Studio | desktop client | Step Plan | `https://api.stepfun.ai/step_plan/v1` |
| CodeGPT | VS Code extension | Step Plan | `https://api.stepfun.ai/step_plan/v1` |
| DeepSeek Harness (dsh) | terminal agent (preview) | both (sources list standard) | `https://api.stepfun.ai/step_plan/v1` (Step Plan) / `https://api.stepfun.ai/v1` (Standard) |
| Hermes Agent | agent framework (custom endpoint) | Step Plan | `https://api.stepfun.ai/step_plan/v1` |
| OpenClaw | instruction-driven agent | Step Plan | `https://api.stepfun.ai/step_plan/v1` |

> Cursor and dsh are the only tools in this set where the corpus explicitly
> documents a standard-channel URL. For all others, the Step Plan base URL is
> the only confirmed path.

## Per-tool gotchas

### Claude Code
`npm install -g @anthropic-ai/claude-code` (needs Node.js 22+). Setup script option **2 — StepFun Step Plan (subscription)** writes `ANTHROPIC_AUTH_TOKEN` and the base URL into the `env` object of `~/.claude/settings.json`; it **replaces the whole `env` object** (other variables inside it are removed) and backs up the previous config. Restart after setup. Verified with Claude Code 2.1.209.

Manual config: `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL` = `https://api.stepfun.ai/step_plan`, top-level `model`. Optional `ANTHROPIC_DEFAULT_{SONNET,OPUS,HAIKU,FABLE}_MODEL` and `CLAUDE_CODE_SUBAGENT_MODEL` must use real Step model IDs or background tasks/subagents fail. `effortLevel` goes at the **top level**, not in `env`. The script does **not** write `CLAUDE_CODE_MAX_CONTEXT_TOKENS` / `CLAUDE_CODE_AUTO_COMPACT_WINDOW`; add `"1000000"` (plain number, not `1M`/`1000k`) to `env` yourself for the 1M window of `step-5-preview`. `xhigh` and `max` map to `high`; the client sends effort via `output_config.effort`. A settings-file value overrides the same variable set in the terminal.

### Pi
`export STEP_API_KEY="YOUR_STEP_API_KEY"`, then add a custom provider in `~/.pi/agent/models.json` (or `models.json` under `$PI_CODING_AGENT_DIR`) with `"baseUrl": "https://api.stepfun.ai/step_plan"`. Requests land on `/step_plan/v1/messages`. Run: `pi --provider stepfun --model step-5-preview`.

### Oh My Pi (OMP)
npm `oh-my-pi`. Extends Pi with task categories, specialist roles, and skills; uses Pi's provider configuration and the same base URL. In 0.2.0 the oracle subagent only returns role instructions to the current session — model selection stays with Pi's `--provider` / `--model`.

### Cline
Extension ID `saoudrizwan.claude-dev`. Use the **StepFun Step Plan (Global)** preset: Base URL `https://api.stepfun.ai/step_plan/v1`, Model ID `step-5-preview`. No preset → pick `OpenAI Compatible` with the same values. Cline appends `/chat/completions`. The API key field takes the **raw key** — no `Bearer ` prefix, no leading/trailing spaces (some versions label it `OpenAI Compatible API Key`); the MCP header is the opposite and does require `Bearer `.

Model settings that matter for `step-5-preview`: Supports Images enabled, Context Window `1000000`, Max Output Tokens `65536` (a very small budget truncates output before visible text), Reasoning Effort default or `High` (`low`/`medium`/`high`).

Optional StepSearch MCP (gives `web_search` / `web_fetch`) in `cline_mcp_settings.json` — `type` must be spelled exactly `streamableHttp` (omitting it selects legacy SSE), `url` `https://api.stepfun.ai/step_plan/v1/mcp/web_search/mcp`, header `Authorization: Bearer <key>`. The MCP config stores the key in plain text — keep it in user config, do not commit.

### Roo Code
Base URL `https://api.stepfun.ai/step_plan/v1`, Model ID `step-5-preview`; keep the base URL ending at `/step_plan/v1`. **Roo Code 3.54.0 requires OpenAI-native tool calling (no XML fallback) — pick a function-calling model.**

### Kilo Code
Extension `kilocode.kilo-code`. The Step Plan preset appears under Providers; set `Settings > Models > Default Model` to `step-5-preview`. Missing preset → `Providers > Custom provider` with the standard base URL and key.

### OpenCode
Add to `~/.zshrc`: `export OPENAI_API_KEY="YOUR_STEP_API_KEY"` and `export OPENAI_BASE_URL="https://api.stepfun.ai/step_plan/v1"`.

### Cursor
Requires a **paid Cursor subscription (Pro/Teams) for BYOK — Free/Hobby accounts cannot use this**. Cursor 3.15.20+ recommended. Settings → Models: OpenAI API Key, **Use OpenAI API Key ON**, **Override OpenAI Base URL ON**, Base URL `https://api.stepfun.ai/step_plan/v1` (standard channel — pay-as-you-go: `https://api.stepfun.ai/v1`). Do not include `/chat/completions`. Add custom model IDs `step-5-preview`, `step-3.7-flash`, `step-3.5-flash-2603`, `step-3.5-flash`.

The override is global and applies to **Chat and Agent only** — code completion (Tab) keeps using Cursor's built-in models. To go back: disable the override, disable the key toggle if needed, and start a **new** conversation; changing the model selector alone does not disable the custom base URL.

### Codex CLI
Custom provider using the **Responses** API: set `wire_api = "responses"` against `https://api.stepfun.ai/step_plan/v1/responses` — no protocol-conversion proxy needed. Codex 0.154.0 does not support Chat Completions here. `model_catalog_json` defines Step model names, context windows, and input capabilities so models appear in `/model`; a dedicated Step profile scopes the catalog override. `CODEX_HOME` holds the config.

### Goose
Open-source agent client (Block). Add an OpenAI Compatible provider with Base/API URL `https://api.stepfun.ai/step_plan/v1`.

### Zed
Editor AI Assistant: custom API Endpoint with API URL `https://api.stepfun.ai/step_plan/v1` and a Model Name from your plan — verified examples: `step-5-preview`, `step-3.7-flash`, `step-3.5-flash-2603`, `step-3.5-flash`.

### Cherry Studio
Desktop client. In the model provider list select **StepFun** and set the base URL `https://api.stepfun.ai/step_plan/v1`.

### CodeGPT
VS Code extension. Manage AI Models → custom (OpenAI-compatible) provider with Base URL `https://api.stepfun.ai/step_plan/v1`; CodeGPT appends `/chat/completions`. Uses Step Plan subscription quota.

### DeepSeek Harness (dsh)
Developer preview — read the project's safety notice first and use a trusted working directory. Step Plan Base URL `https://api.stepfun.ai/step_plan/v1` (standard channel — pay-as-you-go: `https://api.stepfun.ai/v1`), Model ID e.g. `step-5-preview`.

### Hermes Agent
Open-source agent framework (Nous Research). **"More providers" → "Custom endpoint"**, Base URL `https://api.stepfun.ai/step_plan/v1`, then the Model ID.

### OpenClaw
Instruction-driven agent. In Model/auth provider select **StepFun**. The config file sets `contextWindow` (`1000000` for `step-5-preview`; `256000` for `step-3.7-flash` and the Step 3.5 Flash series) and `maxTokens` — an **output budget, not the model's maximum output capability** (e.g. 8192).

## Negatives

- **Do not point these tools at `https://api.stepfun.ai/v1`** or use a regular pay-as-you-go key for pipeline/integration work — standard-address requests enter the pay-as-you-go channel and do not consume Step Plan Credits. Sources only document the standard address for dsh and Cursor, as a billing choice.
- Anthropic-format base URL is `https://api.stepfun.ai/step_plan` with **no `/v1`** — the client appends `/v1/messages`. Adding `/v1` or `/v1/messages` yourself duplicates the path and fails.
- Chat-Completions base URLs stop at `/step_plan/v1` — never append `/chat/completions` in the setting.
- Claude Code's setup script wipes the existing `env` object and does not write the 1M-context fields.
- Cursor: free/hobby accounts cannot BYOK; Tab completion never uses Step models.
- dsh is a developer preview, not a supported release.
- Model IDs available on this account: `step-5-preview`, `step-3.7-flash`, `step-3.5-flash`, `step-3.5-flash-2603`, `stepaudio-2.5-tts`, `stepaudio-2.5-asr`. Everything else in the docs (`stepaudio-2.5-chat`, `step-router-v1`, `deepseek-v4-pro`, `step-image-edit-2`, etc.) is reference-only and not callable here — `step-image-edit-2` retired 2026-10-10.
- Per-tool retry/rate-limit behaviour and client-specific error codes: not documented in these sources.
- **Standard-channel base URLs are unverified** for most tools — only Cursor and dsh have explicit corpus documentation. Confirm before using in production (Q-STD-03).

## Related cards

[chat-apis.md](chat-apis.md) · [openai-migration.md](openai-migration.md) · [errors-and-debugging.md](errors-and-debugging.md) · [reasoning.md](reasoning.md) · [static-hosting.md](static-hosting.md)
