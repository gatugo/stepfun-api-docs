# Decisions

A dated line whenever the workspace's shape or a stated fact changes.

## 2026-10-13 — `README.md` becomes the GitHub landing page

**What:** the root `README.md` was rewritten from a bare pointer into a landing
page: what the bundle is, the problem it solves, the ten-minute test, and a table
of where to go next.

**Why:** GitHub renders the repository's root `README.md` as its landing page.
A visitor who clones the repo sees that file first and nothing else, so a bare
pointer gives a stranger no way to judge what they are looking at. The previous
form was correct for an agent opening the folder and wrong for a human arriving
from a repo listing.

**What was deliberately *not* done:** no fact was duplicated. The landing page
carries orientation and links only; every substantive fact still lives in exactly
one card. The 2026-10-08 concern that motivated the pointer — a deploy runbook
riding along in the front door — is untouched, and the runbook still lives solely
in `skills/redeploy.md`. The pointer role for agents is preserved in a collapsed
section at the foot of the file, and `AGENTS.md` remains the one start file.

**Gates:** `check_integrity.py` ✅ · `cold_walk.py` ✅.

## 2026-10-13 — image API confirmed retired; Step Plan allowlist drops 7 → 6

**What:** a second live pass called the image endpoints directly. Both
`POST /v1/images/generations` and `POST /step_plan/v1/images/generations` returned
**HTTP 400 `model step-image-edit-2 not supported`**, and `step-image-edit-2`
dropped out of the live Step Plan model list, which went from 7 models to 6.

**Why it matters:** `models.md` was marked `verified_on: 2026-10-13` yet still
listed a model whose retirement date (2026-10-10) had already passed three days
earlier. A card verified *after* a deadline it never re-checked is the failure
mode this closes. Corrected across ~20 files; evidence recorded in
`_account/live-calls/2026-10-13-image-api-retired.md`.

**Also settled:** `step-image-edit-2` removed from the allowlist hardcoded in
`_core/check_integrity.py`, so the gate now agrees with reality. Q04 answered in
part — no successor is named anywhere, which remains a product decision.

**Gates:** `check_integrity.py` ✅ · `cold_walk.py` ✅.

## 2026-10-13 — standard-channel branch created

**What:** `stepfun-api-v2` (Step Plan only) was copied to `stepfun-api-v2-standard`
to add the Standard pay-as-you-go channel alongside the existing Step Plan
coverage. Two channels, one bundle.

**Structural changes:**
- `CLAUDE.md` — routing table now covers both channels; non-negotiable updated
- `PURPOSE.md` — genericised; no longer Step Plan-only
- `bundle/always-load/standard-channel.md` — new, skeleton, `draft`
- `bundle/always-load/models.md` — Channel column added (`step-plan | standard | both`), status `draft`
- `bundle/by-task/*.md` — endpoint tables dual-column (Step Plan / Standard), status `draft`
- `_account/step-plan-access-info.md` — converted to a template

**Gates:** `check_integrity.py` ✅ 25 cards, 42 files, 115 corpus pages, all checks clean.
`cold_walk.py` ✅ 23/23 probes route.

## 2026-10-08 — `README.md` reduced to a pointer *(entry reconstructed 2026-10-13)*

**What:** an earlier draft of the root `README.md` carried a full project README
with a deploy runbook, carried over from v1. It was reduced to a pointer.

**Why:** the runbook is a procedure, not a front door. It moved to
`skills/redeploy.md`, and every other fact in the draft already had a home in the
bundle — so the README was duplicating content rather than orienting a reader.

**Note on this entry:** the 2026-10-08 README cited "`decisions.md`, 2026-10-08"
as its authority, but no such entry existed in this file — the decision log had
been lost or never carried across from v1. This entry is reconstructed from the
wording of that README rather than from an original record, and is marked as such.
The 2026-10-13 entry above supersedes the pointer-only form for the GitHub case
while keeping its underlying principle intact.


