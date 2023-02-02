#!/bin/bash

echo "The lastest version is:"
git describe --tags $(git rev-list --tags --max-count=1)

read -p "Enter commit message: " commit_message
read -p "Enter version tag: " version_tag

# Add changes to the local repository
git add .

# Commit changes to the local repository
git commit -m "$commit_message"

# Create a tag with the specified version
git tag "$version_tag"

# Push tags to remote repository
git push --tags

# Push changes to the remote repository
git push origin main

git log --oneline