## [list] - 2026-03-18

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
