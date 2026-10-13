#!/usr/bin/env bash
# Regenerate the public copy and publish it as a single history-free commit.
#
# Why this exists: _core/make_public.py rebuilds the output directory from
# scratch on every run, which destroys the public copy's .git. That is correct
# for a generated artifact — but it means publishing is several steps that must
# happen in the right order, and getting them wrong is how a scrub failure
# reaches GitHub. This script makes the sequence atomic and abort-on-failure.
#
# Usage:
#     bash _core/publish.sh              # regenerate, commit, force-push
#     bash _core/publish.sh --dry-run    # regenerate and inspect, push nothing
#
# Requires STEPFUN_DOCS_REMOTE in the environment:
#     export STEPFUN_DOCS_REMOTE=https://github.com/<you>/stepfun-api-docs.git
#
# The generator runs FIRST and the script aborts if it fails, so a scrub
# failure never reaches the push. The author is pinned here rather than
# inherited from global git config — that is what keeps a real name out of the
# published commit.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PUBLIC="$ROOT/../stepfun-api-v2-standard-public"
# Deliberately not hardcoded: a username inside a repo URL is personal data, and
# this file ships in the public copy. Requiring it also means the script fails
# loudly rather than pushing to a guessed remote.
: "${STEPFUN_DOCS_REMOTE:?Set STEPFUN_DOCS_REMOTE, e.g. export STEPFUN_DOCS_REMOTE=https://github.com/<you>/stepfun-api-docs.git}"
REMOTE="$STEPFUN_DOCS_REMOTE"
MSG="Initial release: task-routed StepFun API knowledge bundle"
AUTHOR_NAME="stepfun-api-docs"
AUTHOR_EMAIL="stepfun-api-docs@users.noreply.github.com"

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

echo "==> regenerating public copy"
python3 "$ROOT/_core/make_public.py"

cd "$PUBLIC"

if [[ ! -d .git ]]; then
  echo "==> no git repo in the copy (make_public.py rebuilt it) — initialising"
  git init -q -b main
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "==> adding remote $REMOTE"
  git remote add origin "$REMOTE"
fi

echo "==> committing as a single history-free commit"
git add -A
if git rev-parse HEAD >/dev/null 2>&1; then
  git -c user.name="$AUTHOR_NAME" -c user.email="$AUTHOR_EMAIL" \
    commit -q --amend -m "$MSG"
else
  git -c user.name="$AUTHOR_NAME" -c user.email="$AUTHOR_EMAIL" \
    commit -q -m "$MSG"
fi

if [[ "$DRY_RUN" == "1" ]]; then
  echo "==> dry run — stopping before push"
  git --no-pager log --oneline -1
  echo "    $(git ls-files | wc -l) files, author $(git log -1 --format='%an <%ae>')"
  exit 0
fi

echo "==> force-pushing (single commit, no history)"
git push --force origin main

echo "==> published"
git --no-pager log --oneline -1
echo "    $(git ls-files | wc -l) files, author $(git log -1 --format='%an <%ae>')"
