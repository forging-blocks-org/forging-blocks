# Release Guide
## Releasing projects that use ForgingBlocks

This guide describes a **simple, repeatable process** for releasing a project that uses ForgingBlocks.

It does not depend on any particular tooling, but examples refer to common tools such as **Poetry** and **PyPI**.

---

## 1. Decide the kind of release

Use semantic-style versioning as a guideline:

- **PATCH** – bug fixes, internal changes, or documentation only.
- **MINOR** – new features added in a backward-compatible way.
- **MAJOR** – breaking changes to public contracts or behaviors.

Example: `0.3.1` → `0.3.2`, `0.4.0`, or `1.0.0`.

---

## 2. Update version metadata

If you are using `pyproject.toml`:

```toml
[project]
name = "your-project-name"
version = "0.4.0"
```

Also review:

- the changelog,
- important documentation pages,
- examples and tests.

Make sure they describe the new behavior accurately.

---

## 3. Run checks

Before releasing, run your full check pipeline:

- tests
- linters
- type checkers
- documentation build (if you publish docs)

Example with Poetry:

```bash
poetry run pytest
poetry run mypy .
poetry run poe docs:build  # if you use poe + MkDocs
```

Adapt these commands to your own setup.

---

## 4. Build the distribution

If you publish a library:

```bash
poetry build
```

This should create artifacts (such as `.whl` and `.tar.gz`) in the `dist/` directory.

If you publish a service or application, this step may be replaced by building an image or packaging an artifact in another format.

---

## 5. Publish (optional)

To upload to PyPI or another index:

```bash
poetry publish --repository pypi
```

If you are unsure, test with a private index or TestPyPI first.

For internal services, this step might mean:

- pushing a container image,
- deploying to a staging environment,
- or tagging a release in your internal Git server.

---

## 6. Tag the release

Tagging helps track what changed and when:

```bash
git tag -a v0.4.0 -m "Release 0.4.0"
git push origin v0.4.0
```

You can also create GitHub/GitLab release entries that link to your changelog.

---

## 7. Communicate the changes

Especially when others depend on your project:

- document breaking changes clearly,
- give examples of new features,
- mention any migration steps.

ForgingBlocks aims to keep changes incremental and explicit, so that teams can upgrade with confidence.

---

## 8. Releasing ForgingBlocks itself

If you are working on ForgingBlocks or a similar toolkit, the same ideas apply:

- be clear about what changed,
- keep reference and guide documentation updated,
- maintain examples that showcase new capabilities,
- treat your building blocks as contracts that other developers rely on.

Good releases are not just about publishing artifacts; they are about **setting clear expectations** for the people who will use your work.
