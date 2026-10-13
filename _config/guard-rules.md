---
layer: 3
role: guard-rules
---

# Guard rules — hard constraints

Layer 3. These are the boundaries an agent must not cross, stated as rules rather
than as suggestions. Where a rule can be checked by a script, it is —
see `_core/check_integrity.py`. Where it cannot, it is stated here and enforced
by reading it before acting.

## Never do these

| # | Rule | Why |
| --- | --- | --- |
| G0 | Never resolve an availability question from a `corpus/` page alone | The docs describe the platform; `_account/` is what this subscription can call. `step-router-v1` proves they differ. |
| G1 | Never edit anything under `corpus/` by hand | It is generated truth. Regenerate with `python3 _core/fetch.py`. |
| G2 | Never read `_archive/` unless the human names a file inside it | Retired work poisons live answers. |
| G3 | Never write a credential, API key, or token into any file here | The bundle is a readable, shareable artifact. |
| G4 | Never answer a StepFun question without reading `bundle/always-load/` first | That is where "don't guess the plan" is enforced. |
| G5 | Never claim a model works on this plan without checking `always-load/models.md` | Docs list 115 platform pages; Step Plan serves a subset. |
| G6 | Never silently substitute a standard-channel Base URL for a Step Plan one | Different billing channel. A success there spends nothing. |
| G7 | Never `promote` or `rollback` a live site without human confirmation | Public-facing, irreversible-ish. |
| G8 | Never delete a `corpus/` page to "fix" a fetch failure | Failures belong in the manifest, not in absence. |
| G9 | Never duplicate a fact across cards | One fact, one home — or the two copies drift and the model picks one at random. |
| G10 | Never mark a card `verified` without reading its `source` page this session | Undated trust is how documentation rot starts. |

## Always do these

| # | Rule |
| --- | --- |
| A1 | Say "not confirmed on this plan" rather than guessing, when the model list is silent. |
| A2 | Log any corpus-vs-card conflict in `decisions.md` before resolving it. |
| A3 | Park unknowns in `open_questions.md` instead of inventing an answer. |
| A4 | Quote Credit economics for this account, not dollar-per-million, unless the per-token figure is explicitly labelled a standard-channel rate. |
| A5 | Admit when the corpus is silent. An honest "the docs don't say" beats a confident invention. |

## Escalation

If a task requires doing something G1–G10 forbid, stop and ask the human. Do not
work around a guard.
