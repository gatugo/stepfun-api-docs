# Changelog

Dated, newest first. Structural changes and settled facts get a line; routine
card edits do not.

The method behind this history: vendor docs are fetched into `corpus/`, facts are
extracted into tiered cards, disputes are settled by live call, and two scripted
gates prove the result. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## 2026-10-13 — Security purge, retirement verification, showcase hardening

**Security**
- **Purged the live API key from git history.** It was committed at
  `test_q02_asr_stream.py:20` in three commits reachable from `main` and survived
  the earlier working-tree cleanup, which made a file scan read clean. History
  rewritten with `git filter-branch`, all reflogs expired, objects garbage-collected,
  and 0 hits verified across every blob. The published copy was never affected —
  it is generated from the working tree and has its own single-commit history.
- **Removed a leftover internal name.** `_core/fetch.py` still sent a
  `User-Agent` carrying an internal project name; the commit that claimed to strip
  that name only swept Markdown. Now `stepfun-docs-fetch/1.0`.

**Verified**
- **The image API is dead, not merely retiring.** Live calls to
  `/v1/images/generations` and `/step_plan/v1/images/generations` both returned
  HTTP 400 `model step-image-edit-2 not supported`, and the model dropped out of
  the Step Plan list. The Step Plan allowlist is **6 models, not 7** — corrected
  across ~20 files, and `step-image-edit-2` removed from the allowlist hardcoded
  in `_core/check_integrity.py` so the gate now agrees with reality. Evidence:
  `_account/live-calls/2026-10-13-image-api-retired.md`. Q04 answered in part.
- **A card verified *after* its own deadline.** `models.md` was marked
  `verified_on: 2026-10-13` while still trusting a model that retired on
  2026-10-10. The gates check internal consistency, not freshness; only a live
  call caught it.

**Fixed**
- `structured-output.md` used `STEPFUN_API_KEY` — the steppage *hosting*
  credential — inside a model-API curl example. Now `STEP_API_KEY`, and `auth.md`
  spells out that the two names belong to different products.
- `chat-apis.md` had no non-streaming Python example at all; the only complete
  Python in the routed bundle was streaming. Added a minimal call.
- The 429 retry gap was stated but unusable — no backoff, jitter, attempt cap, or
  `Retry-After`. Promoted to a labelled section with an explicit non-vendor
  default, and parked as **Q05**.
- `open_questions.md` was missing every question the cards cite: `Q01`–`Q04` were
  referenced from five files and defined nowhere. All four now recorded, and two
  stale "disputed" references corrected to their resolved state.
- `decisions.md` had one entry while `README.md` cited a 2026-10-08 decision that
  was never recorded. Both now logged, the older one marked as reconstructed.
- `HOW-TO-USE.md` claimed a fetch flips affected cards to `stale`.
  `_core/fetch.py` rewrites `corpus/` and the manifest only — it never touches a
  card. The claim is corrected and the limitation stated plainly.
- `demo.sh` closed with "every number above came from this tree, live" while
  section 4 was hardcoded text. Now labelled as recorded evidence.
- Token figures had drifted: measured **~6,000** per routed task (was 5,700) and
  **40×** reduction (was 42×). Updated in DEMO, FAQ, HOW-IT-WORKS, and README.

**Added**
- `showcase/TRY-IT.md` — a self-falsifying test: two gates, three questions with
  the expected correct answers and the files to check them against, plus a
  negative test that must return "not documented" rather than an invented number.
- `README.md` is now a GitHub landing page. Orientation and links only — no fact
  duplicated, the deploy runbook still lives solely in `skills/redeploy.md`, and
  the pointer role for agents is preserved. Logged in `decisions.md`.

**Gates:** `check_integrity.py` ✅ 25 cards, 115 corpus pages ·
`cold_walk.py` ✅ 23/23 probes route.

---

## 2026-10-13 — Showcase and public release

**Added**
- `showcase/` — README, HOW-IT-WORKS, HOW-TO-USE, DEMO, FAQ, and a reproducible
  `demo.sh`
- `LICENSE` (MIT), `.gitignore`, `CONTRIBUTING.md`, `CHANGELOG.md`
- `.github/workflows/verify.yml` — both gates plus the demo run on every push

**Fixed**
- `bundle/always-load/index.md` claimed "the 7 callable models" — stale since the
  Standard channel added a 15-model allowlist
- `_config/conventions.md` and `_config/guard-rules.md` had two numbered rules
  merged onto one line, breaking table rendering
- `skills/redeploy.md` carried absolute `/home/<user>/…` paths, violating its own
  relocatability rule, and named the pre-rename `stepfun-api-v2`
- `_config/guard-rules.md` said "~110 platform pages"; the corpus is 115

**Added**
- `_core/make_public.py` — generates a scrubbed public copy, asserts no personal
  data, and runs both gates in it

---

## 2026-10-13 — Q-STD-03 resolved: endpoint parity, with two availability corrections

**Verified by live call on both channels.** Chat completions, messages,
responses, ASR one-shot SSE, and TTS one-shot all return HTTP 200 on both base
URLs. **Files is the one exception — Standard only** (Step Plan returns a bare 404).

**Two availability corrections, both contradicting the vendor docs:**
- **The Responses API is not Standard-only.** The sources say the Step Plan URL is
  undocumented; `POST /step_plan/v1/responses` returns 200 with
  `status=completed`. The docs are incomplete, not the endpoint.
- **Files really is Standard-only.** `POST /step_plan/v1/files` returns 404,
  upgrading the card's "treat as unconfirmed" caveat to a verified absence.

**Four request-shape corrections:**
- ASR `format` must sit inside `audio.input`; a flat `audio.format` returns
  `400 "audio format is required"`
- `/v1/files` validates the file *extension*, not just MIME type
- `/v1/responses` needs at least 512 `max_output_tokens` or `step-3.7-flash`
  returns `status="incomplete"` with empty output
- TTS voice IDs are not free-form; undocumented IDs return `400 voice_id_invalid`

**Operational note.** A `429 rate_limited` is a per-model throttle, not evidence
that an endpoint is absent — one model 429'd three times while every other call in
the same minute succeeded, then returned 200 on retry.

**Added** `_account/live-calls/2026-10-13-endpoints.md` plus three reproducible
probe scripts.

---

## 2026-10-13 — Standard channel verified: 15 models, reasoning-effort parity

**Verified by live call.** `GET /v1/models` returns **15 models** — all 7 Step Plan
models plus 8 Standard-only audio models. `GET /step_plan/v1/models` returns 7.

**Not on any channel:** `step-router-v1`, `step-2x-large`, `step-1x-edit`,
`deepseek-v4-pro`.

**Q-STD-02 resolved — reasoning-effort parity.** `step-3.5-flash` and
`step-3.5-flash-2603` both returned HTTP 200 with `"reasoning_effort": "medium"`
on Standard. **All four reasoning models accept `low`/`medium`/`high` on both
channels**, disproving the API reference's claim that the 2603 variant is
`low`/`high` only.

**Added** `bundle/always-load/standard-channel.md` (promoted to `verified`), a
Channel column on `models.md`, and `_account/live-calls/2026-10-13-models.md`.

---

## 2026-10-12 — Standard-channel branch created

`stepfun-api-v2` (Step Plan only) was branched to add the Standard pay-as-you-go
channel alongside the existing Step Plan coverage. Two channels, one bundle.

- `CLAUDE.md` — routing table extended to both channels
- `PURPOSE.md`, `CONTEXT.md` — genericised, no longer Step Plan-only
- `bundle/always-load/standard-channel.md` — new card
- `bundle/always-load/models.md` — Channel column added
- `bundle/by-task/*.md` — endpoint tables made dual-column (Step Plan / Standard)
- `open_questions.md` — Q-STD-01/02/03 opened

---

## Earlier

Showcase-ready cleanup, credential redaction from the test script (key moved to
`STEP_API_KEY`), and `CLAUDE.md` orientation restored. See `git log` for detail.
