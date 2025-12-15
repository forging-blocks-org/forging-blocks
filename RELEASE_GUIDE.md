# Release Guide

This guide explains how to release a new version of ForgingBlocks.

---

## Quick Start

### Patch Release (Bug Fixes)

```bash
git checkout main
git pull origin main
poetry run poe release:patch
```

Creates a PR for version `0.1.0` → `0.1.1`

---

### Minor Release (New Features)

```bash
git checkout main
git pull origin main
poetry run poe release:minor
```

Creates a PR for version `0.1.1` → `0.2.0`

---

### Major Release (Breaking Changes)

```bash
git checkout main
git pull origin main
poetry run poe release:major
```

Creates a PR for version `0.2.0` → `1.0.0`

---

## Detailed Steps

### Step 1: Update Local Main

```bash
git checkout main
git pull origin main
```

Ensure you're on the latest `main` branch.

---

### Step 2: Create Release Branch

Run the appropriate release command:

```bash
poetry run poe release:patch   # For bug fixes
poetry run poe release:minor   # For new features
poetry run poe release:major   # For breaking changes
```

**What happens:**
1. Creates branch `release/v<version>`
2. Bumps version in `pyproject.toml`
3. Commits with message `release: <version>`
4. Creates tag `v<version>`
5. Pushes branch and tag to GitHub
6. Displays PR creation link

---

### Step 3: Create Pull Request

1. Click the GitHub PR link from the command output
2. Or go to GitHub and click **"Compare & pull request"**
3. Review the changes (should only be version bump)
4. Click **"Create pull request"**

---

### Step 4: Merge Pull Request

1. Wait for CI checks to pass
2. Get required approvals (if applicable)
3. Click **"Merge pull request"**

---

### Step 5: Verify Release

After merging, GitHub Actions automatically:
- Validates the release
- Publishes to PyPI
- Deploys documentation

Monitor at: https://github.com/forging-blocks-org/forging-blocks/actions

Verify:
- Package on PyPI: https://pypi.org/project/forging-blocks/
- Documentation is updated

---

## Complete Example

```bash
# 1. Update main
git checkout main
git pull origin main

# 2. Current version is 0.1.0, releasing 0.1.1
poetry run poe release:patch

# Output:
# Bumping version from 0.1.0 to 0.1.1
# Switched to a new branch 'release/v0.1.1'
# [release/v0.1.1 abc123] release: 0.1.1
# ✓ Release branch created: release/v0.1.1
# ✓ Now create a PR: https://github.com/.../compare/release/v0.1.1

# 3. Click the link, create PR

# 4. Review and merge the PR

# 5. GitHub Actions publishes automatically
# Monitor: https://github.com/.../actions

# 6. Verify on PyPI and test
pip install forging-blocks==0.1.1
```

---

## Version Strategy

Follow [Semantic Versioning](https://semver.org/):

| Release Type | Command | When to Use | Example |
|--------------|---------|-------------|---------|
| **Patch** | `poe release:patch` | Bug fixes only | `0.1.0` → `0.1.1` |
| **Minor** | `poe release:minor` | New features, backward compatible | `0.1.1` → `0.2.0` |
| **Major** | `poe release:major` | Breaking changes | `0.2.0` → `1.0.0` |

---

## Handling New Files

If your release includes new files, add them before creating the release:

```bash
git checkout main
git pull origin main

# Add new files
git add src/forging_blocks/new_module.py

# Create release
poetry run poe release:patch
```

---

## What to Include in Each Release Type

### Patch Release (0.0.x)
- Bug fixes
- Documentation corrections
- Minor performance improvements
- No API changes

### Minor Release (0.x.0)
- New features
- New APIs (backward compatible)
- Deprecations (with warnings)
- Significant documentation updates

### Major Release (x.0.0)
- Breaking API changes
- Removal of deprecated features
- Major architectural changes
- Incompatible changes

---

## That's It!

The release process is:

1. `git checkout main && git pull origin main`
2. `poetry run poe release:patch` (or minor/major)
3. Create PR from GitHub
4. Merge PR
5. Done! (GitHub Actions handles the rest)
