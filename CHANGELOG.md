## [0.3.16] - 2026-03-20

### Bug Fixes

- Update version in __init__.py
- Adjust release.yml to remove id-token permission

### CI

- Add release pipeline scripts
- Fix github workflow trigger on release event
- Fix on release.yml
- Ci.yml is now using yaananth/twine-upload@v1 for validation and version bumping
- Tweak GitHub Actions workflows for better validation and release process
- Fix syntax for GitHub Actions environment variable output
- Add --sync flag to poetry install in validate_publish.sh
- Add validation step to publish workflow

### Miscellaneous Tasks

- Refactor validate_publish.sh for better error handling and CI compatibility
- Refactor CI workflow to separate validation and publishing steps
- Fix in relase workflow
- Fix GitHub Actions workflow for PyPI publishing
- Fix GitHub Actions workflow for PyPI publishing
- Another fix for GitHub Actions
- Fix in ci.yml for install git-cliff action
- Add workflow step to lint GitHub Actions workflow files
