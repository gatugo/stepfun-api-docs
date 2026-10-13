---
card: plan
tier: always-load
status: verified
verified_on: 2026-10-08
source: corpus/step-plan/overview.md, corpus/step-plan/quick-start.md
---

# Step Plan — the subscription

## What it is
Subscription access to StepFun models inside mainstream coding tools and agent platforms (Claude Code, Cursor, OpenClaw, and others). One valid Step API Key; a unified monthly **Credit** allowance across all models.

## Billing
- **Credits** are the single billing unit: ~$1 ≈ 7M Credits. The full month's Credits are issued at once, spendable any time within the month, **cleared at month end — no rollover**.
- Deduction order: whichever expires first — monthly-allowance Credits vs. booster-pack Credits (own 30-day cycles).
- **Booster packs** (active subscribers only): Small $6.99 / 400M Credits, Large $9.99 / 1,600M Credits.
- Step Plan is **not** subject to the platform's tiered RPM/TPM rate limits; usage is governed by the monthly Credit allowance.
- Step Plan Credits and account balance are separate systems — the balance can pay for a subscription but is never deducted by usage.
- Payment via Stripe or account balance; cancel any time (no refunds; service runs to the end of the cycle).

## Tiers

| Plan | Monthly Credits | Monthly | Quarterly | Yearly |
| --- | --- | --- | --- | --- |
| Flash Mini | 400M | $6.99 | $18.99 | $69.99 |
| Flash Plus | 1,600M | $9.99 | $26.99 | $95.99 |
| Flash Pro | 8,000M | $29 | $79 | $289 |
| Flash Max | 40,000M | $99 | $269 | $989 |

Every tier includes all flagship models, MCP tool coverage, and multi-device login; Flash Plus and above add priority API rates and priority support.

## Platform model list vs. this account

The platform's Step Plan page lists: `step-5-preview`, `step-3.7-flash`, `step-3.5-flash`, `step-3.5-flash-2603`, `stepaudio-2.5-tts`, `stepaudio-2.5-asr`, `step-router-v1`. **This account's list is narrower** — `step-router-v1` is absent. The account list in [`models.md`](models.md) is the authority; see [`../evidence/models/not-on-this-plan.md`](../evidence/models/not-on-this-plan.md).

## Channel
Step Plan traffic uses the `/step_plan/` base URLs (Rule 6 — [`endpoints.md`](endpoints.md)). Requests sent to the standard API address enter the pay-as-you-go channel and do **not** consume Step Plan Credits.
