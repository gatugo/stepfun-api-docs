---
skill: refresh-a-card
applies-to: writing or correcting a bundle card
---

# Skill — refresh a card

Use when a card is `stale`, wrong, or missing. This is the extraction pipeline:
corpus page → card.

## Procedure

1. **Name the task, not the page.** "How do I do structured output?" →
   `bundle/by-task/structured-output.md`. One card, one job.
2. **Read the corpus page(s) that cover it.** Note their exact paths.
3. **Check the current tier.** If the fact is needed on *every* task, it belongs
   in `always-load/`. If it's per-task, `by-task/`. If it's deep reference,
   `evidence/`.
4. **Write the card:**
   - frontmatter per `_config/conventions.md`, with today's date in `verified_on`
   - lead with the answer, not the background
   - tables over prose for anything with >2 attributes
   - link to sibling cards; never copy their facts
   - include the negatives ("not on this plan", "required", "default 0.5")
5. **Add the routing row** to `CLAUDE.md` if the task wasn't routable before.
   Keep `CLAUDE.md` ≤ 60 lines — if it overflows, the row is too detailed.
6. **Run the quality gate** in `_config/quality-standards.md`, then
   `python3 _core/check_integrity.py`.
7. **Log it** in `decisions.md` if the change alters the workspace's shape or a
   previously-stated fact.

## Splitting a card

A card is too big when a task needs only part of it, or when it has two jobs.
Split by job, not by length, and link the halves from
`bundle/by-task/index.md`.

## What not to do

- Don't write a card from memory, or from a different provider's docs.
- Don't create a second home for a fact that already has one (guard G9).
- Don't mark `verified` without reading the source in this session (guard G10).
- Don't leave a gap unrecorded — `open_questions.md` exists for exactly this.
