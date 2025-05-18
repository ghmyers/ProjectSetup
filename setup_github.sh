#!/usr/bin/env bash
set -euo pipefail

########################################
# Usage: ./git_auto.sh "Commit message" [branch]
########################################

# 0. Verify we’re inside a repo
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo "❌  Not a Git repository."
  exit 1
fi

# 1. Parse arguments
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"Commit message\" [branch]"
  exit 1
fi
COMMIT_MSG="$1"
BRANCH="${2:-main}"

# 2. Create branch if needed and switch to it
# git switch --create "$BRANCH" 2>/dev/null || git switch "$BRANCH"
# 2. Create branch if needed and switch to it
if git rev-parse --verify HEAD >/dev/null 2>&1; then
    # Repo already has a commit → normal flow
    git switch --create "$BRANCH" 2>/dev/null || git switch "$BRANCH"
else
    # No commits yet → create an ORPHAN branch
    git switch --orphan "$BRANCH"
fi


# 3. OPTIONAL safety net: timestamped backup ref (cheap, 0 bytes on disk)
BACKUP_REF="backup/$BRANCH-$(date +%Y%m%d-%H%M%S)"
git branch "$BACKUP_REF" >/dev/null
echo "📦  Backup ref created at $BACKUP_REF"

# 4. Stage **everything**, but commit only if there are changes
if ! git diff --quiet --ignore-submodules --
then
  git add -A
  git commit -m "$COMMIT_MSG"
else
  echo "ℹ️  No changes to commit."
fi

# 5. If the branch exists on the server, pull--rebase; otherwise skip
if git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null; then
    git pull --rebase --autostash origin "$BRANCH"
else
    echo "ℹ️  Remote branch '$BRANCH' doesn't exist yet – skipping pull."
fi

# 6. Push
if git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null; then
    git push --ff-only origin "$BRANCH"        # fast-forward only
else
    git push -u origin "$BRANCH"               # creates remote branch & sets upstream
fi

echo "✅  Push complete.  Local branch $BRANCH is up to date with origin/$BRANCH."
