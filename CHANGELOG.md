## [Unreleased]

### Features

- **docs**: Versioned documentation with mike — each release gets its own immutable docs snapshot, `dev` updates on every push to main, version selector in nav
- **ci**: Release pipeline deploys versioned docs after PyPI publish

### Documentation

- Add versioned documentation management commands and updated release guide

## [0.4.0] - 2026-06-04

### Bug Fixes

- **domain/entity**: Hash relies on the class and id
- **domain**: Fix bug related to aggregate_root identity falsy
- **infrastructure**: Cast aggregate_id to TWriteId
- **foundation**: Fix issues reported in pr

### Refactor

- **application**: Remove session property from UnitOfWork
- **infrastructure**: Remove session property
- **foundation**: Extract ResultAccessError to its own file
- **foundation**: Re-export module initializer
- **foundation**: Remove methods that were not aggregating behavior

### Documentation

- **foundation**: Add module-level docstring

### Miscellaneous Tasks

- Pre-commit: always simulate CI before allowing commits
- **scripts/release**: Remove session property
- **foundation**: Remove pyright ignore clause
- **py.typed**: Add type marker file

## [0.3.23] - 2026-06-01

### Bug Fixes

- **scripts/release**: Preventing duplicate section in changelog

### Refactor

- **create_github_release**: Delegate logic to functions
- **create_github_release**: Redirect log outputs
- **scripts**: Add dry_run flag to ChangelogRequest
- **release/infrastructure**: Add dry_run flag
- GitCliffChangelogGenerator truncates duplicates

### Testing

- **conftest**: Extract fixtures
- **scripts**: Improving test fixture path for git repos
- **scripts/release**: Properly integration testing PoetryVersioningService
- **conftest**: Git fixture creates repo inside tmp_path
- **presentation**: E2e test relying on GitVersionControl fixture
- Inject TempPathFactory

### Miscellaneous Tasks

- **scripts/pipeline**: Impl create_github_release
- **workflows**: New job to create github release
- Improve release automation scripts
- **release/application**: Usecase output includes change_entries
- **release/infrastructure**: GitCliffChangelogGenerator adjusts
- **release/presentation**: Logging Changelog preview

## [0.3.22] - 2026-03-24

### Bug Fixes

- *(scripts/release)* Adjust changelog generation to use current version

### CI

- *(scripts)* Check if package version already exists on PyPI before uploading to TestPyPI
- *(pipeline)* Add act-release.sh script for local testing of release workflow

### Documentation

- *(domain-foundation)* Reference adjustments to reflect current structure

### Features

- Updating to python 3.14
- *(foundation)* Re-exporting messages in foundation

### Miscellaneous Tasks

- *(changelog)* Adjust changelog for recent changes
- Remove unnecessary files from repository
- Remove .github/events/release_event.json
- *(gitignore)* Adding local-validate-publish.yml and .secrets.act to .gitignore
- *(workflows)* Inject TEST_PYPY_TOKEN

### Refactor

- *(messages)* Move messages to foundation block
- *(domain)* Adjust imports to be compatible with new structure
- *(value_object)* Moving value_object to foundation block
- *(application)* Adjusting imports to foundation instead of domain

### Testing

- Fix for warnings and incompatible python314 tests
- *(foundation)* Move message tests to foundation
