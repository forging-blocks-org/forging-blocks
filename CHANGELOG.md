## [0.3.20] - 2026-03-20

### Bug Fixes

- Lint scripts are now correct

### CI

- Add a new ci linting step for yamllint
- Installl int tools for CI workflow
- Add yamllint configuration to prevent duplicate keys in YAML files
- Fix poorly action
- Remove environment for test-pypi
- Add shellcheck validate_publish for pipeline scripts
- Enforce presence of PyPI tokens for release PRs
- Impl env contract validation for pipeline scripts
- Enforce PyPI versioning in publish workflow
- Extract smoke test to separate script
- Improving readability of smoke test step in CI workflow
- Modularizing smoke test script
- Impl require_vars helper for pipeline scripts
- Enforce presence of required env vars for publish step
- Add shellcheck linting for pipeline scripts
- Add additional_files and shellcheck_options to action-shellcheck
- Improving shellcheck linting for pipeline scripts
- Fix CI workflow to check for existing version on TestPyPI before upload
- Impl check for existing version on TestPyPI before upload
- Testpypi-check is now delegating to a separate script
- Enforce that the package version is not already published on TestPyPI before uploading and running smoke tests
- Exporting logic from workflows to separate scripts
- Add validation scripts for release and publish versions
- Add linting for shell scripts and environment variable contracts

### Miscellaneous Tasks

- Improving github workflows
- Enforce presence and validity of PyPI tokens in CI
- Harden PyPI publishing by validating environment contracts and PUBLISH_VERSION
- Enforce PyPI dependencies for types-pyyaml and pyyaml
- Pipeline scripts are now sharing common logging and error handling utilities
- Improving smoke test script by enforcing required environment variables
