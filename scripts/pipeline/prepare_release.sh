#!/bin/bash
set -e

if ! command -v git &> /dev/null; then
    echo "Error: git is not installed in the container. Please use the 'Medium' act image."
    exit 1
fi

VERSION="${HEAD_REF#release/}"

if [[ -z "$VERSION" || "$VERSION" == "$HEAD_REF" ]]; then
  echo "Error: Could not extract version from branch: $HEAD_REF"
  exit 1
fi

echo "Extracted version: $VERSION"
echo "version=$VERSION" >> "$GITHUB_OUTPUT"

git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

if git ls-remote --tags origin "$VERSION" | grep -q .; then
  echo "Tag $VERSION already exists on remote. Skipping creation."
else
  echo "Creating tag $VERSION..."
  git tag "$VERSION"

  if [[ "$ACT" != "true" ]]; then
    git push origin "refs/tags/$VERSION"
  else
    echo "Local simulation detected. Skipping git push."
  fi
fi
