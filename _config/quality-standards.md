---
layer: 3
role: quality-gate
---

# Quality standards — the acceptance gate

A card is not done until it passes these. Same gate for every card, every tier.

## Every card

- [ ] Has frontmatter with `card`, `tier`, `status`, `verified_on`, `source`.
- [ ] Its `source` path exists under `corpus/` and was actually read.
- [ ] Every factual claim traces to that source — nothing inferred, nothing
      carried over from a different model or plan.
- [ ] States which plan/channel/model it applies to, or is explicitly plan-agnostic.
- [ ] Links to sibling cards rather than repeating their facts.
- [ ] Passes the token budget: A ≤ 4k, B ≤ 4k, C ≤ 6k.

## Step Plan-specific gates (this bundle only)

- [ ] Base URLs are written with the correct `/v1` handling for the SDK family.
- [ ] Any model named appears in `bundle/always-load/models.md`.
- [ ] Any pricing figure is either (a) quoted as a standard pay-as-you-go rate
      *and labelled as such*, or (b) expressed in Credits. Never mixed silently.
- [ ] If the answer depends on the plan, it names **Step Plan Oversea /
      `platform.stepfun.ai`** explicitly.
- [ ] Any availability claim (which model this account can call) is sourced to
      `_account/` or to `always-load/models.md`, never to a `corpus/` page alone.
- [ ] Any time-sensitive fact (retirement dates, deprecations) names its date and
      is checked against today.

## Routing files

- [ ] `CLAUDE.md` ≤ 60 lines, pointer-only.
- [ ] `CONTEXT.md` ≤ 80 lines, pointer-only.
- [ ] Every task an agent could plausibly receive has a row in the routing table.
- [ ] No routing file contains a content payload (long prose, big code, tables of
      facts that belong in a card).

## The fresh-session test

Open a brand-new session in this folder and ask: *"What is this folder, and how
do I do <task>?"* A correct answer routes through `CLAUDE.md` to one card without
human help. If it fails, do not blame the agent — trim the map or add the
missing row, then log the fix in `decisions.md`.

## When a card fails the gate

Mark it `status: stale`, add the gap to `open_questions.md`, and leave it in
place. A wrong-but-flagged card is recoverable; a wrong card that looks verified
is not.
