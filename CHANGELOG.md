## [0.3.13] - 2026-03-18

### Bug Fixes

- GitVersionControl now stages all changes before committing to ensure untracked files are included
- GitCliffChangelogGenerator now writes output to CHANGELOG.md
- Ensure changelog is written with utf-8 encoding
- Improving github actions for release automation
- Ensure that the tag is created after the commit to avoid issues with detached HEAD state
- Replaced push_tags with tag in VersionControl.push() method
- Handle pre-commit hook failures when committing release artifacts

### CI

- Install-git-cliff action defined
- Remove name from install-git-cliff action
- Add names to steps in CI workflow
- Add the install-git-cliff action to the release workflow

### Miscellaneous Tasks

- Update install-git-cliff action to use composite syntax
- Update git checkout logic to auto-detect default branch
- *(prepare_release_service)* Add tag creation and deletion to transaction

### Refactor

- *(release)* Update push method to push specific tag

### Testing

- *(release)* Add e2e tests for release workflow
- Fix imports in test_release_e2e.py
- *(e2e)* Add end-to-end test for release script
- Fix release workflow test to check for errors

---

## [0.3.7] - 2026-02-10

### Bug Fixes

- Fix handling of annotated tags during release
- Correct version bump logic for pre-release identifiers

### CI

- Update release workflow to use latest checkout action
- Cache Python dependencies to speed up CI runs

### Miscellaneous Tasks

- Improve logging around release preparation


## [0.3.6] - 2026-01-25

### Bug Fixes

- Resolve race condition when creating release tags

### Testing

- Add unit tests for version control helper functions

### Miscellaneous Tasks

- Update documentation for release process
