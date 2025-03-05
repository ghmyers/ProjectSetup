#!/bin/bash

# Ensure a project name and path are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "❌ Error: Please provide a GitHub repository name and project path."
    echo "Usage: ./setup_github.sh <repo_name> <project_path>"
    exit 1
fi

PROJECT_NAME=$1
PROJECT_PATH=$2
GITHUB_USERNAME="finnmyers96"  # Replace with your GitHub username
GITHUB_REPO_URL="https://github.com/$GITHUB_USERNAME/$PROJECT_NAME.git"

# Navigate to project directory
cd "$PROJECT_PATH" || { echo "❌ Error: Project directory does not exist at $PROJECT_PATH."; exit 1; }

# Ensure GitHub CLI is authenticated
if ! gh auth status &>/dev/null; then
    echo "❌ GitHub CLI is not authenticated. Run 'gh auth login' and try again."
    exit 1
fi

# Create GitHub repository (if not already created)
echo "🚀 Creating new GitHub repository: $PROJECT_NAME"
gh repo create "$PROJECT_NAME" --private --confirm

# Initialize Git (if not already initialized)
if [ ! -d ".git" ]; then
    git init
fi

# Ensure the correct remote is set
if git remote | grep -q origin; then
    echo "⚠️ Remote 'origin' already exists. Resetting it..."
    git remote remove origin
fi

git remote add origin "$GITHUB_REPO_URL"

# Add all files and commit
git add .
git commit -m "Initial commit"

# Set branch to 'main' and push
git branch -M main
git push -u origin main

echo "✅ GitHub repository created and pushed for $PROJECT_NAME"

