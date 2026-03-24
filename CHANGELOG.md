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
