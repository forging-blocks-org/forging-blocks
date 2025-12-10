# 🚢 Release Guide

This guide outlines a simple, repeatable process for releasing new versions of ForgingBlocks (or any project that uses it as a dependency). Adapt it to your own workflow, tooling, and automation.

---

## 1. Choose the Version Bump

Base your version bump on the nature of the changes:

- **PATCH** — bug fixes, internal refactoring, documentation only, no breaking changes.
- **MINOR** — new features or types added in a backward-compatible way.
- **MAJOR** — breaking changes to public APIs or contracts.

Example: from `0.3.1` to `0.3.2`, `0.4.0`, or `1.0.0`.

---

## 2. Update Version Metadata

If you use `pyproject.toml`:

```toml
[project]
name = "forging-blocks"
version = "0.4.0"
```

Also ensure that:

- Changelog is updated.
- Documentation reflects new concepts or changes.
- Any examples and tests are still valid.

---

## 3. Run the Full Check Suite

Before releasing, run:

- linters
- type checkers
- tests
- docs build, if applicable

Example with Poetry:

```bash
poetry run pytest
poetry run mypy .
poetry run poe docs:build  # if you use poe & MkDocs
```

Adjust commands to match your own tooling.

---

## 4. Build the Distribution

Using `python -m build` or a Poetry command, for example:

```bash
poetry build
```

This should produce `.whl` and `.tar.gz` artifacts under `dist/`.

---

## 5. Publish to Package Index (Optional)

If you publish to PyPI or a private index, you might use:

```bash
poetry publish --repository pypi
```

or your preferred upload command.

Use TestPyPI or an internal index if you want to validate distribution behavior before a public release.

---

## 6. Tag the Release

Tag the release in version control:

```bash
git tag -a v0.4.0 -m "Release 0.4.0"
git push origin v0.4.0
```

Tags make it easier to track what changed when and to generate release notes later.

---

## 7. Announce Changes

Ensure consumers of your project can see what changed:

- Update the changelog.
- Mention the release in your project README or docs.
- If relevant, highlight any migration notes for breaking changes.

ForgingBlocks itself aims to keep changes incremental, explicit, and well-documented so adopters can upgrade with confidence.
