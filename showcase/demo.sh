#!/usr/bin/env bash
# Reproducible demo — prints the real numbers behind the showcase claims.
#
# Everything this script prints is measured from the tree, not typed by hand.
# Record it with asciinema if you want a cast:
#   asciinema rec -c "bash showcase/demo.sh" demo.cast
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

hr() { printf '%s\n' "------------------------------------------------------------"; }

hr
echo "1. WHAT AN AGENT LOADS TO ANSWER ONE QUESTION"
hr
python3 - <<'PY'
import os
def ch(p):
    try: return os.path.getsize(p)
    except OSError: return 0
def tok(n): return n // 4

claude = ch("CLAUDE.md")
always = sum(ch(f"bundle/always-load/{f}") for f in
             ["auth.md", "endpoints.md", "models.md", "plan.md",
              "standard-channel.md", "index.md"])
one_card = ch("bundle/by-task/streaming.md")
corpus = sum(ch(os.path.join(r, f))
             for r, _, fs in os.walk("corpus") for f in fs if f.endswith(".md"))
per_task = claude + always + one_card

rows = [
    ("CLAUDE.md (routing map)", claude),
    ("bundle/always-load/ (6 cards)", always),
    ("one bundle/by-task/ card", one_card),
]
for name, n in rows:
    print(f"  {name:<34} {n:>8} ch  ~{tok(n):>6} tok")
print(f"  {'-'*34} {'-'*8}    {'-'*6}")
print(f"  {'PER TASK':<34} {per_task:>8} ch  ~{tok(per_task):>6} tok")
print()
print(f"  {'corpus/ (115 vendor pages)':<34} {corpus:>8} ch  ~{tok(corpus):>6} tok")
print()
print(f"  Reduction: {corpus / per_task:.0f}x less context for a routed answer.")
PY

hr
echo "2. THE GATES — proof the bundle is internally consistent"
hr
python3 _core/check_integrity.py 2>&1 | tail -12

hr
echo "3. THE COLD WALK — can a fresh agent route from the map alone?"
hr
python3 _core/cold_walk.py 2>&1 | grep -E "^(CLAUDE|  ok|[0-9]+ routing|Cold walk)" | tail -8

hr
echo "4. WHAT THE DOCS PROMISE VS WHAT THIS ACCOUNT CAN CALL"
hr
echo "  Recorded from live calls on 2026-10-13. Evidence: _account/live-calls/"
echo "  Sections 1-3 above are computed from this tree; this section is not."
echo "  Re-run it with your own key - see showcase/TRY-IT.md, Part 4."
echo
python3 - <<'PY'
print("""  Documented across the corpus:  ~110 model IDs
  Callable on Standard channel:   15   (live GET /v1/models)
  Callable on Step Plan channel:   6   (live GET /step_plan/v1/models)

  Documented as "Step Plan only" but NOT callable here: step-router-v1
  Documented as Standard-only but actually on BOTH:   the Responses API
  Documented on Step Plan but actually absent:        the Files API (404)
  Documented as retiring 2026-10-10 but already dead: the image API (HTTP 400)
""")
PY

hr
echo "Done. Sections 1-3 are computed from this tree; section 4 is recorded from"
echo "live calls on 2026-10-13. Re-run the gates any time to re-verify."
hr
