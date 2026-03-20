## [0.3.15] - 2026-03-20

### Bug Fixes

- Update version in __init__.py
- Adjust release.yml to remove id-token permission

### CI

- Add release pipeline scripts
- Fix github workflow trigger on release event
- Fix on release.yml
- Ci.yml is now using yaananth/twine-upload@v1 for validation and version bumping

### Miscellaneous Tasks

- Refactor validate_publish.sh for better error handling and CI compatibility
- Refactor CI workflow to separate validation and publishing steps
- Fix in relase workflow
