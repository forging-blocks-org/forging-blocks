# 🚀 Release Guide

This document describes how to safely create and publish a new release of **BuildingBlocks** to **PyPI**.

---

## 🧭 Step 1 — Increment the Version

Use **Poetry** to automatically bump the version number in `pyproject.toml`.

```bash
poetry version patch   # for small fixes (e.g., 0.3.5 → 0.3.6)
poetry version minor   # for new features (e.g., 0.3.5 → 0.4.0)
poetry version major   # for breaking changes (e.g., 0.3.5 → 1.0.0)
```

> Alternatively, if you use `uv`, run:
> ```bash
> uv version patch
> ```

---

## 🧩 Step 2 — Commit the Version Update

After bumping the version, commit the change:

```bash
git add pyproject.toml
git commit -m "chore: bump version to vX.Y.Z"
```

---

## 🏷️ Step 3 — Tag the Commit

Create an **annotated tag** (required for the GitHub Actions pipeline to trigger):

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

Verify the tag:

```bash
git tag --list
```

If needed, remove or re-create a tag:

```bash
git tag -d vX.Y.Z
git push --delete origin vX.Y.Z
git tag -a vX.Y.Z -m "Release vX.Y.Z (fixed)"
```

---

## ☁️ Step 4 — Push the Commit and Tag

Push both the branch and tag to trigger the GitHub Actions **Publish Package** workflow:

```bash
git push origin <branch-name>
git push origin vX.Y.Z
```

---

## 🧠 Notes

- Tags **must** match the pattern `v*.*.*` (e.g., `v0.3.6`) for the pipeline to publish.
- The workflow automatically detects whether to publish to **TestPyPI** or **PyPI**, depending on the tag type.
- The **publish.yml** workflow uses **OIDC authentication** — no API token is required in secrets.
- Typical availability on PyPI after release: **30–60 seconds**.

---

✅ Once complete, verify your package here:
👉 [https://pypi.org/project/building-blocks-toolkit/](https://pypi.org/project/building-blocks-toolkit/)
