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
# If no remote called "origin" exists yet, create one that points to GitHub
GITHUB_USER="ghmyers"                    
REPO_NAME="${PWD##*/}"                    # directory name → repo name
REMOTE_URL="git@github.com:${GITHUB_USER}/${REPO_NAME}.git"



if ! git remote | grep -q '^origin$'; then
  git remote add origin "$REMOTE_URL"
  echo "🔗  Added remote 'origin' → $REMOTE_URL"
fi

# Create github repository
if ! gh repo view "${GITHUB_USER}/${REPO_NAME}" &>/dev/null; then
  echo "🌐  Creating repository ${GITHUB_USER}/${REPO_NAME} on GitHub…"
  gh repo create "${GITHUB_USER}/${REPO_NAME}" --private --confirm
fi


# 1. Parse arguments
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"Commit message\" [branch]"
  exit 1
fi
COMMIT_MSG="$1"
BRANCH="${2:-main}"

# 2. Create branch if needed and switch to it
if git rev-parse --verify HEAD >/dev/null 2>&1; then
  # Repo already has at least one commit
  git switch --create "$BRANCH" 2>/dev/null || git switch "$BRANCH"
else
  # Unborn HEAD – make an orphan branch
  git switch --orphan "$BRANCH"
fi


# 3. OPTIONAL safety net: timestamped backup ref (cheap, 0 bytes on disk)
if git rev-parse --verify HEAD >/dev/null 2>&1; then
  BACKUP_REF="backup/$BRANCH-$(date +%Y%m%d-%H%M%S)"
  git branch "$BACKUP_REF" >/dev/null
  echo "📦  Backup ref created at $BACKUP_REF"
fi

# 4. Stage **everything**, but commit only if there are changes
# if ! git diff --quiet --ignore-submodules --
# then
#   git add -A
#   git commit -m "$COMMIT_MSG"
# else
#   echo "ℹ️  No changes to commit."
# fi
if [ -n "$(git status --porcelain)" ]; then
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
