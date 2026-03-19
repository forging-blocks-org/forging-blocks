## [0.3.13] - 2026-03-19

### Bug Fixes

- Changelog generation when using git-cliff
- Validate release workflow on remote CI/CD to ensure complete release pipeline is verified
- Idempotency check + retry install

### CI

- Fix in release workflow to check for tag existence instead of creating it
- Including validation of remote CI/CD to poe release:validate sequence
- Validate release workflow now is a shell script
- *(workflows)* Add validation workflow for release process
- Add build and artifact validation steps to CI and release workflows
- Remove any tag related operations from version control port
- *(scripts)* Validate_publish.sh and remove validate_release.sh
- Validate package publish to TestPyPI on pull requests
- Fix yml githbu workflows

### Miscellaneous Tasks

- Validate_release_remote script to check if the release workflow passed on the remote CI/CD
- Poe task is now calling a shell script instead of a python script for validating the remote CI/CD for the latest release
- Validate release workflow script and add unit tests
- *(pyproject)* Add validation for GitHub release workflow
- Fix in validate release workflow test script
- Still trying to validate the release workflow script
- Remove release validation workflows
- Validate artifacts before merging release PRs
- Improving validate_release.sh
- *(pyproject)* Add testpypi source for testing package publishing
- *(poetry)* Update poetry.lock with new content hash and python version
- *(pyproject)* Fix testpypi url
- *(pyproject)* Fix testpypi url
- Fix validate_publish.sh to use the correct python interpreter

### Refactor

- Combine git push commands for branch and tag into a single command
- *(release)* Removing tag creation from prepare release service

### Testing

- Solve merge conflicts in release script and update tests
- Git_version_control.py  tests updated to reflect the change in push command to include the tag in a single push
- *(release)* Increasing consistency in release automation
