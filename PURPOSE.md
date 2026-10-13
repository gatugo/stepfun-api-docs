# StepFun API

## Purpose
Keep a local, task-routed working bundle for the **StepFun platform**
(`platform.stepfun.ai`), covering both the **Step Plan** (Credits) and
**Standard** (pay-as-you-go) channels. Any agent building against the API
never guesses the channel, the base URL, or the model list — and can assemble
a voice pipeline (ASR → reasoning → TTS) without re-deriving endpoints from
the vendor site.

## Structure

| Layer | Purpose |
|---|---|
| `CLAUDE.md` | Routing map — start here |
| `bundle/always-load/` | Cards needed on every task (plan, endpoints, auth, models, standard-channel) |
| `bundle/by-task/` | Per-task cards with dual-column endpoint tables |
| `bundle/evidence/` | Contradiction logs, token limits, off-plan allowlists |
| `_account/` | Account-specific facts (populate per channel) |
| `corpus/` | Fetched upstream docs — never hand-edit |

## Inputs
- `corpus/` — raw pages fetched from `platform.stepfun.ai/docs/llms.txt` by
  `python3 _core/fetch.py`. Upstream truth; never hand-edited.
- `_account/` — account-specific facts (keys, model allowlists). Outranks the
  corpus on what a given key can actually call. Populate for each channel.

## Output
- Cards written or corrected in `bundle/`, per `skills/refresh-a-card.md`.
- A routing row in `CLAUDE.md` when a task becomes routable (kept ≤ 60 lines).
- A dated entry in `decisions.md` when the workspace's shape or a stated fact
  changes.
- A resolved or newly-parked line in `open_questions.md`.
