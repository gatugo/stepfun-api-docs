---
skill: redeploy
applies-to: moving, copying, or rebuilding this bundle in another folder
---

# Skill — redeploy this bundle

Use when this bundle is being **moved, copied, or rebuilt** into another folder.
The bundle is self-contained Markdown; relocation is a file operation, and the risk
is not breakage — it is *silent* breakage (a relative link that no longer resolves, a
path that only worked in the old location).

## 1. Before any move — commit

The bundle lives in a git repo. An uncommitted move risks losing the last good state.

```bash
cd /path/to/stepfun-api-v2-standard
git config user.email "you@example.com"   # once, if unset
git add -A && git commit -m "state before move $(date +%F)"
```

## 2. Before any move — confirm relocatability

The bundle contains **no absolute paths** — every internal reference is relative.
Verify it before believing it:

```bash
grep -rn '/home/\|/tmp/' --include='*.md' . || echo "clean — safe to move"
```

If that prints anything, fix the reference **before** moving, or the moved copy will
be wrong in a way no check catches.

## 3. The three scenarios

### Scenario A — relocate as-is to any folder

The bundle is self-contained; relocation is a file operation.

```bash
# move
mv /path/to/stepfun-api-v2-standard /any/target/stepfun-api-v2-standard

# or copy, leaving the original in place
rsync -a /path/to/stepfun-api-v2-standard/ /any/target/stepfun-api-v2-standard/
```

`.git/` travels with the directory — use `mv` or `rsync -a`, never a copy that skips
dotfiles. Nothing inside references the old location, so **no file edits are needed**.
Then run section 4.

### Scenario B — install into the official tree (`/path/to/workspace`)

The destination is a mature workspace with house rules that differ from this
bundle's defaults. **Do not drop the folder in unconformed** — the destination's
invariants (entry files route and never hold content; one front door; additions get
a dated log line) are enforced there, and an unconformed bundle reads as a second
source of truth.

**Recommended: install as its own desk**, beside the existing `stepfun-ai-docs/`.
Keep the desks separate rather than merging: `stepfun-ai-docs/` is a *knowledge
bundle* (raw corpus + task cards for answering questions); this bundle is the same
form for the Step Plan Oversea account. The forms compose; each keeps its invariants
at its own level.

**Procedure:**

1. **Settle the one cross-desk contradiction first** — the reasoning-effort mapping
   (Q01). Two desks asserting different `reasoning_effort` levels for
   `step-3.5-flash-2603` is exactly the failure the method exists to prevent. One
   real API call settles it; update both desks after.
2. **Move the bundle in:**
   ```bash
   mv /path/to/stepfun-api-v2-standard /path/to/workspace/<desk-name>
   ```
3. **Conformance pass on the moved bundle:**
   - `CLAUDE.md` — reduce to ≤ 60 lines, routing only. Keep the one orientation
     sentence (plan, region, default model) and the routing table. **Remove any
     restated facts** — the account model list and effort levels have their home in
     `bundle/always-load/models.md`; the orientation sentence points there instead of
     repeating values.
   - `CONTEXT.md` — keep it ≤ 80 lines and pointer-only; if it has grown into content,
     the content belongs in a card.
   - `README.md` stays as the humans-first explainer, but confirm it contains **no
     routing table** — a README that routes is a third front door.
   - Keep `_config/conventions.md`, `_config/guard-rules.md`,
     `_config/quality-standards.md` and the `_core/` tooling; they are what makes the
     bundle verifiable.
4. **Wire the desk into the parent tree:**
   - Append a **dated entry to the parent `CONTEXT.md`** recording the new desk, what
     it holds, and why it is separate from `stepfun-ai-docs/`.
   - Add the desk to the desk list in the parent `README.md` and update any
     user-guide that counts desks or names paths.
   - The parent root `CLAUDE.md` is a one-line pointer to `AGENTS.md`; add the desk
     there only if the parent's map enumerates desks.
5. **Keep the nested git repo.** The tree root is deliberately not a repo, but desks
   under it carry their own — a desk-level repo is accepted practice. Alternatively
   `git init` fresh at the new path if you prefer history to start at the move.
6. **Run section 4**, plus the destination's own guards where they apply
   (`_core/check_integrity.py`, `_core/cold_walk.py` are this bundle's tools — read
   them before pointing anything else's at this bundle).

### Scenario C — rebuild from scratch in an empty folder

Only needed when no copy exists. The structure is fully specified by the existing
tree; **the fastest correct rebuild is still Scenario A from any surviving copy**. A
from-scratch rebuild:

1. Create the skeleton:
   ```bash
   mkdir -p ws/_config ws/_core ws/_account ws/corpus \
            ws/bundle/always-load ws/bundle/by-task \
            ws/bundle/evidence/models ws/bundle/evidence/reference ws/skills
   ```
2. Write files **in layer order** — the router exists before the content it routes
   to: `CLAUDE.md` → `CONTEXT.md` → `_config/` → `_account/` → `corpus/` →
   `bundle/always-load/` → `bundle/by-task/` → `bundle/evidence/` → `skills/`.
3. Content sources, in priority order: (a) an existing copy of this bundle; (b) the
   live docs at `https://platform.stepfun.ai/docs/llms.txt` — fetch the `.md` form of
   any page; (c) the owner's instructions, recorded as ADRs. **Never invent a
   parameter, price, or limit** — if the source is silent, write "not documented" and
   open a question.
4. Owner-scoped facts that must be carried over verbatim (they are not in the vendor
   docs): the account model list (7 IDs), Rule 6 (Step Plan channel only), the
   ADR-005 effort ruling, the NOT-AVAILABLE banners, and the off-plan allowlist in
   `bundle/evidence/models/not-on-this-plan.md`.
5. Write the evidence cards in dependency order — `not-on-this-plan.md` **first**,
   because it defines the off-plan allowlist the rest of the bundle's integrity
   depends on.
6. `git init`, commit, then run section 4.

## 4. Verification suite — run after every deploy or structural change

```bash
cd /path/to/stepfun-api-v2-standard

# 1. Link integrity — every referenced bundle|corpus|_config|_account path must exist
missing=0
for f in $(grep -rhoE '(bundle|corpus|_config|_account|skills)/[A-Za-z0-9_./-]+\.md' --include='*.md' . | sort -u); do
  [ -f "$f" ] || { echo "MISSING  $f"; missing=1; }
done
[ "$missing" -eq 0 ] && echo "PASS: all referenced paths exist"

# 2. Relocatability — no absolute paths anywhere
grep -rn '/home/\|/tmp/' --include='*.md' . || echo "PASS: no absolute paths"

# 3. Provenance — every card names its source in frontmatter
for f in $(find bundle skills -name '*.md'); do
  head -8 "$f" | grep -q '^source:' || echo "NO SOURCE: $f"
done

# 4. Card frontmatter — tier, status, verified_on present on every evidence card
for f in $(find bundle/evidence -name '*.md'); do
  for k in card tier status verified_on source; do
    head -8 "$f" | grep -q "^$k:" || echo "MISSING FRONTMATTER $k: $f"
  done
done

# 5. Off-plan allowlist — every off-plan model ID present in the allowlist card
for id in stepaudio-2.5-chat stepaudio-2.5-realtime stepaudio-2.5-asr-stream \
           stepaudio-3-tts stepaudio-3-asr-max stepaudio-3-realtime-preview \
           step-router-v1 step-2x-large step-1x-edit deepseek-v4-pro; do
  grep -q "\`$id\`" bundle/evidence/models/not-on-this-plan.md || echo "MISSING OFF-PLAN ID: $id"
done

# 6. Repo tooling — the bundle's own guards
python3 _core/check_integrity.py
python3 _core/cold_walk.py
```

**Cold-walk test (the real gate):** open a fresh agent session with zero history,
point it at the bundle, and ask: *"What is this folder, where do I find X, what must
I never use, and what's next?"* It should answer correctly from `CLAUDE.md` +
`CONTEXT.md` alone. If it cannot, the router is wrong — fix the router, not the agent.

## What not to do

- Don't move without committing first (section 1).
- Don't copy in a way that drops `.git/` or other dotfiles.
- Don't drop the bundle into the official tree unconformed (Scenario B).
- Don't treat a passing link check as a passing deploy — the cold-walk test is the gate.
- Don't rewrite a contradiction to make two desks agree; settle it with a live call
  and update both.
