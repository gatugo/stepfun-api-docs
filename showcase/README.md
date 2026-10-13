# StepFun API — a task-routed knowledge bundle

**Stop re-reading the vendor docs. Stop shipping code that calls a model your key
can't reach.**

This is a local, agent-facing knowledge base for the StepFun platform
(`platform.stepfun.ai`). You drop it into your project, point your coding agent at
one file, and it answers StepFun questions correctly — from *your* subscription's
reality, not from the platform's marketing pages.

---

## The problem

You are building against the StepFun API. Four things go wrong:

**1. The docs describe the platform, not your subscription.**
The vendor corpus is 115 pages covering roughly 110 model IDs. Your key can call
15 on the Standard channel and 6 on Step Plan. `step-router-v1` is documented as
"available only through Step Plan" — it is **not callable on this account**. An
agent that reads the docs will confidently hand you a model name that 404s.

**2. One key, two channels, and the billing is silent.**
The same API key works on both channels. **The base URL alone decides whether a
call draws your monthly Credits or bills real USD per call.** Point a client at
the wrong base URL and you spend money believing you spent Credits. Nothing warns
you.

**3. The docs contradict themselves.**
`stepaudio-3-asr-max` is priced at $0.24/hour on its model page and $0.40/hour on
the pricing page. Images-per-request is "up to 60" and "10–50 depending on the
model" *in the same file*. Reasoning-effort levels are described differently in
the API reference than the model pages. Pick one at random and you are wrong half
the time.

**4. It costs ~239,000 tokens to find out.**
Pasting the corpus into context to answer one question is **40× more context than
a routed answer needs** — and the routed answer is more reliable, not less.

---

## What this is

A folder of Markdown cards, organised so an agent loads only the part it needs:

| Layer | What it holds | Loaded when |
|---|---|---|
| `CLAUDE.md` | Routing map — 50 lines, no content | always |
| `bundle/always-load/` | Facts needed on every task: plan, base URLs, auth, models | every task |
| `bundle/by-task/` | One card per job: streaming, tool calling, TTS, files… | the one card that matches |
| `bundle/evidence/` | Contradiction logs, off-plan allowlists, token-limit provenance | only when a fact is disputed |
| `_account/` | **What this subscription can actually call** | outranks everything |
| `corpus/` | The 115 fetched vendor pages — never hand-edited | reference only |

**Per task, an agent loads about 6,000 tokens. The corpus is about 239,000.**

---

## The 60-second version

```bash
# 1. Get it
git clone <this-repo> stepfun-api-v2-standard
cd stepfun-api-v2-standard

# 2. Prove it is internally consistent
python3 _core/check_integrity.py   # 6/6 checks
python3 _core/cold_walk.py         # 23/23 routing probes

# 3. Point your agent at it
#    Claude Code / Cursor / Cline / any agent that reads CLAUDE.md or AGENTS.md
```

Then ask your agent: *"Which StepFun models can I call, and what base URL do I
use for the Standard channel?"* It reads `CLAUDE.md`, routes to
`bundle/always-load/models.md`, and answers from verified facts — no guessing.

See [HOW-TO-USE.md](HOW-TO-USE.md) for the three adoption paths, from read-only
to full rebuild.

---

## Why it is trustworthy

This is the part that matters. A pile of Markdown is worthless if it drifts.

**Every card carries its provenance.** Frontmatter records `status`,
`verified_on`, and the exact `corpus/` page the fact came from. A card without a
source is an opinion, not knowledge.

**Sources are ranked, so "what can I call" never comes from the docs.**

| Rank | Source | Authority over |
|---|---|---|
| 1 | `_account/` — recorded live-call snapshots | **What this key can actually call** |
| 2 | `corpus/` — the vendor docs | How the API *behaves*: params, defaults, error codes |
| 3 | `bundle/` cards | Nothing — they are derived, and never beat their source |

This is the rule that stops `step-router-v1` from being recommended.

**Two gates run as scripts, not as good intentions.**

- `_core/check_integrity.py` — routing-file budgets, card frontmatter, every
  card's source page exists, every relative link resolves, no credentials, no
  off-plan model IDs, corpus manifest sanity.
- `_core/cold_walk.py` — the acid test: can an agent with **zero memory** route
  from the map alone? It checks 23 real probes ("how do I stream", "what
  replaces the retiring image model", "why do two sources disagree").

**Live calls settle disputes.** Facts that the docs get wrong were settled by
hitting the API and recording the result. Three examples, all verified on
2026-10-13:

| Claim | Reality |
|---|---|
| The API reference says `step-3.5-flash-2603` accepts only `low`/`high` effort | It accepts `low`/`medium`/`high` on **both** channels |
| The Responses API is Standard-channel-only | It also returns 200 on Step Plan — the docs are simply incomplete |
| The Files API exists on Step Plan | It returns a bare **404** — Files is genuinely Standard-only |

---

## What you get

- **15 verified callable models** on Standard, **6** on Step Plan, with a
  per-channel allowlist and context limits
- **Dual-column endpoint tables** on every task card — Step Plan URL and Standard
  URL side by side, so you never silently cross a billing boundary
- **Corrected facts** where the vendor docs are wrong, each with the live call
  that proved it
- **A documented off-plan allowlist**, so "not available here" is a stated fact
  rather than a guess
- **Reproducible verification** — both gates, runnable by you in seconds

---

## Where to go next

| If you want to… | Read |
|---|---|
| Understand the architecture | [HOW-IT-WORKS.md](HOW-IT-WORKS.md) |
| Know how it was built, end to end | [HOW-IT-WAS-BUILT.md](HOW-IT-WAS-BUILT.md) |
| Verify every claim yourself | [TRY-IT.md](TRY-IT.md) |
| Add this to your project | [HOW-TO-USE.md](HOW-TO-USE.md) |
| See the proof | [DEMO.md](DEMO.md) |
| Common questions | [FAQ.md](FAQ.md) |
| Browse the actual cards | [`../bundle/always-load/`](../bundle/always-load/) |
| Contribute a correction | [`../CONTRIBUTING.md`](../CONTRIBUTING.md) |

**License:** [MIT](../LICENSE). **Never commit an API key** — see
[`../bundle/always-load/auth.md`](../bundle/always-load/auth.md).
