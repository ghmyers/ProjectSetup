#!/usr/bin/env bash
set -euo pipefail
##############################################################################
# git_auto.sh – stage → commit → push  (local history is source-of-truth)
# Usage examples
#   git_auto "Bug-fix: handle NaNs"          # current branch
#   git_auto Quick hotfix main               # msg = "Quick hotfix", branch = main
##############################################################################

# 0. safety check ------------------------------------------------------------
git rev-parse --is-inside-work-tree &>/dev/null ||
  { echo "❌  Not a Git repository"; exit 1; }

[[ $# -lt 1 ]] && {
  echo "Usage: $0 \"Commit message\" [branch]"; exit 1; }

# 1.  parse CLI ----------------------------------------------------------------
if [[ $# -eq 1 ]]; then                    # only a message was given
  COMMIT_MSG="$1"
  BRANCH="$(git symbolic-ref --quiet --short HEAD)"
else                                        # last arg = branch, rest = message
  BRANCH="${@: -1}"                        # bash: last positional parameter
  COMMIT_MSG="${*:1:$#-1}"                 # all but the last
fi

# 2.  switch / create branch ---------------------------------------------------
git switch --create "$BRANCH" 2>/dev/null || git switch "$BRANCH"

# 3.  safety ref (lightweight) -------------------------------------------------
git branch "backup/$BRANCH-$(date +%Y%m%d-%H%M%S)" >/dev/null

# 4.  stage & commit -----------------------------------------------------------
git add -A
git commit --allow-empty -m "$COMMIT_MSG"

# 5.  push local → remote (never pull) ----------------------------------------
if git ls-remote --exit-code --heads origin "$BRANCH" &>/dev/null; then
  git push --force-with-lease origin "$BRANCH"
else
  git push -u origin "$BRANCH"
fi

echo "✅  '$COMMIT_MSG' pushed to origin/$BRANCH"
