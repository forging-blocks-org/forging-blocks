# Release Guide

This document explains **how releases work in ForgingBlocks**, **why the process is designed this way**, and **how contributors should perform a release safely and correctly**.

The goal is to make releases:
- predictable
- auditable
- reproducible
- fully automated

> **Important principle**
> Contributors *never* publish packages or deploy documentation manually.
> All publishing happens in **GitHub Actions**, triggered by a Git tag.

---

## Mental Model (Read This First)

ForgingBlocks follows a **tag-driven release model**:

- A **Git tag (`vX.Y.Z`) is the single release signal**
- Local tooling (Poe) is responsible only for:
  - validating the release
  - bumping the version
  - creating and pushing the tag
- GitHub Actions is responsible for:
  - publishing to PyPI
  - deploying versioned documentation
  - creating the GitHub Release

If no tag is pushed, **no release happens**.

---

## Quick Start

```bash
git checkout main
git pull origin main
poetry run poe release:patch   # or release:minor / release:major
```

Once the command finishes, **GitHub Actions takes over automatically**.

---

## What Happens During a Release

### 1. Validation
- Ensures you are on `main`
- Ensures working tree is clean
- Ensures local `main` matches `origin/main`
- Runs linting, typing, tests, docs build, and package build

### 2. Version Bump
- Updates `pyproject.toml`
- Updates `poetry.lock` if needed

### 3. Commit and Tag
- Commits: `release: X.Y.Z`
- Tags: `vX.Y.Z`
- Pushes commit + tag to `origin/main`

---

## Automation in GitHub Actions

On tag push:
1. CI re-validates the release
2. Package is published to PyPI
3. Docs are deployed using `mike`
4. `latest` alias is updated
5. GitHub Release is created

Monitor progress at:
https://github.com/forging-blocks-org/forging-blocks/actions

---

## Release FAQ (Common Mistakes)

### ❓ I ran `poe release:*` but nothing was published
**Cause:** The Git tag was not pushed.
**Fix:** Ensure the command completed successfully and pushed `vX.Y.Z` to GitHub.

---

### ❓ Can I publish manually with Poetry or MkDocs?
**No.** Manual publishing bypasses validation and breaks reproducibility.
All publishing must be performed by GitHub Actions.

---

### ❓ Why must I release from `main`?
Releases must reflect an exact, reproducible state of the default branch.
Releasing from feature branches introduces ambiguity and risk.

---

### ❓ CI failed after I pushed a tag — what now?
Fix the issue on `main`, then create a **new version** (never reuse tags).

---

### ❓ Can I edit the version manually?
No. Always use `poe release:*` to ensure version, tag, and CI stay consistent.

---

## Maintainer Release Checklist

### Before Running a Release
- [ ] All intended changes are merged into `main`
- [ ] CI is green on `main`
- [ ] No uncommitted changes locally
- [ ] Version change matches SemVer intent
- [ ] Documentation reflects the changes

### During the Release
- [ ] Run `poe release:patch | minor | major`
- [ ] Verify the tag `vX.Y.Z` was pushed
- [ ] Watch the GitHub Actions workflow

### After the Release
- [ ] PyPI package is published
- [ ] Docs are deployed and `latest` is updated
- [ ] GitHub Release exists with notes
- [ ] Install test succeeds:
  ```bash
  pip install forging-blocks==X.Y.Z
  ```

---

## Versioning Strategy

ForgingBlocks follows **Semantic Versioning**.

| Type | Command | When |
|-----|--------|------|
| Patch | `poe release:patch` | Bug fixes, docs |
| Minor | `poe release:minor` | New features |
| Major | `poe release:major` | Breaking changes |

---

## Summary

1. Update `main`
2. Run one release command
3. GitHub Actions publishes everything
4. Verify artifacts
5. Done

This process enforces the same **explicit boundaries and automation discipline**
that ForgingBlocks promotes in application architecture.
