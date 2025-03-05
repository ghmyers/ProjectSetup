#!/bin/bash

# Ensure script is run inside a Git repo
if [ ! -d .git ]; then
    echo "❌ Error: This is not a Git repository!"
    exit 1
fi

# Ensure commit message is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide a commit message."
    echo "Usage: ./git_auto.sh \"Your commit message\" [branch_name]"
    exit 1
fi

# Capture the full commit message (all arguments except the last one if a branch is provided)
if [ -n "$2" ]; then
    BRANCH_NAME="${@: -1}"  # Last argument is the branch name
    COMMIT_MESSAGE="${@:1:$#-1}"  # All but the last argument is the commit message
else
    BRANCH_NAME="main"
    COMMIT_MESSAGE="$1"
fi

# Ensure the branch exists or create it
if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
    git checkout "$BRANCH_NAME"
else
    git checkout -b "$BRANCH_NAME"
fi

# Add all changes, commit, and push
git add .
git commit -m "$COMMIT_MESSAGE"
git push origin "$BRANCH_NAME"

echo "✅ Changes pushed to GitHub on branch: $BRANCH_NAME"

