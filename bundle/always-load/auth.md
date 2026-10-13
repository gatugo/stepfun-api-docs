---
card: auth
tier: always-load
status: verified
verified_on: 2026-10-08
source: corpus/step-plan/quick-start.md, corpus/step-code/configuration/models.md
---

# Authentication

## One key, two channels

The **same API key** authenticates on both channels. Which channel is drawn is
determined entirely by the **base URL** used.

| Channel | Base URL | Billing | Auth header |
|---|---|---|---|
| Step Plan | `https://api.stepfun.ai/step_plan/v1` | Credits | `Authorization: Bearer <key>` |
| Standard | `https://api.stepfun.ai/v1` | USD per-call | `Authorization: Bearer <key>` |

> **Mixing them is silent and expensive.** A standard-address request enters
> the pay-as-you-go channel and does **not** consume Step Plan Credits. Always
> use the Step Plan base URL when Credits are intended.

## Storing the key

- Set `STEP_API_KEY` in your environment. **Never commit it** and never paste
  a real key into a card, a screenshot, or a chat.
- Credential priority (highest first): CLI `--api-key` → saved `auth.json` →
  `STEP_API_KEY` env var → custom provider key in `models.json`.

> **Two similarly-named variables, two different products.**
> `STEP_API_KEY` is the **model API** credential — every card in this bundle that
> shows a `chat/completions`, `messages`, `responses`, or audio call uses it.
> `STEPFUN_API_KEY` is the **steppage Static Hosting** credential and is used
> only by the steppage CLI and its MCP plugin
> ([`../by-task/static-hosting.md`](../by-task/static-hosting.md)). They are not
> interchangeable, and neither name implies the other. See
> [`../evidence/reference/step-code.md`](../evidence/reference/step-code.md).

## Step Code (the CLI agent)

- `/login` → choose **Step Plan Oversea** and sign in at `platform.stepfun.ai`.
  OAuth credentials refresh automatically; `/logout` clears them.
- Keys saved by `/login` live in `~/.stepcode/auth.json` with `0600` permissions.
- Beware `--api-key` on the command line — it lands in shell history and
  process arguments.
- Provider environment variables include `STEP_API_KEY`, `ANTHROPIC_API_KEY`,
  `OPENAI_API_KEY`, `GEMINI_API_KEY`, and others
  (`corpus/step-code/configuration/models.md`).
