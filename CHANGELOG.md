## [0.3.24] - 2026-05-31

### Refactor

- **create_github_release**: Delegate logic to functions
- **create_github_release**: Redirect log outputs

### Miscellaneous Tasks

- **scripts/pipeline**: Impl create_github_release
- **workflows**: New job to create github release
## [0.3.22] - 2026-05-30

### Features

- **infrastructure**: Impl infrastructure errors
- **infrastructure**: Impl InMemoryMessageBus
- **infrastructure**: Impl UnitOfWork
- **infrastructure**: Impl InMemoryReadRepository and InMemoryWriteRepository
- **domain**: Defien abstractmethod apply
- **foundation**: Defined Identified
- **foundation**: Impl FinalABCMeta
- **domain/aggregate_root**: Impl replay method to allow ES usage
- **foundation/meta**: Impl validate_no_runtime_final_override function

### Bug Fixes

- **infrastructure/unit_of_work**: Import fix
- Adjuting infrastructure and pipeline to pr issue
- **domain**: DraftEntityIsNotHashableError error text improvement
- **domain**: AggregateRoot is not allowing falsy ids

### Refactor

- **pipeline**: Refactor in pipline script
- **infrastructure**: Improving infrastructure classes
- **application**: Improve types
- Improve types
- **infrastructure/unit_of_work**: Commit behavior marks rolled_back as false
- **domain/aggregate_root**: Make uncommitted_changes a property
- **domain**: Impl discard_events method of AggregateRoot
- **infrastructure/unit_of_work**: Discard_events in rollback
- **release**: Improve GitCliffChangelogGenerator
- **domain/aggregate_root**: Split aggregate_root into 2 files
- **infrastructure**: InMemoryWriteRepository uses Identified
- **foundation/value_object**: ValueObject now raises CantModifyImmutableAttributeError
- **foundation/meta**: Impl new magic method in FinalABCMeta
- **domain/aggregate_root**: Metaclass is now FinalABCMeta
- **foundation**: FinalABCMeta is now using validate_no_runtime_final_override

### Documentation

- Replace layer to block
- Remove RELEASE_GUIDE
- **infrastructure**: README.md for infrastructure block
- **RELEASE_GUIDE**: Align RELEASE_GUIDE with release automation
- Compliance docs with last version
- Sync docs with last version
- **foundation**: Improving consistency of docstrings

### Testing

- **infrastructure**: Remove unnecessary tests
- **git-cliff**: Impl git_cliff_scenarios
- **conftest**: Re-export fixtures
- **scripts/release**: Refactor mock_run
- **fixtures**: Create one more scenario
- **domain/entity**: Exercise draft entity in tests
- **infrastructure/unit_of_work**: Add apply method to stub
- **domain/errors**: Remove test_from_class_name_source_has_no_dead_code
- **infrastructure/unit_of_work**: Adjust test helper
- **foundation/meta**: Validate_no_runtime_final_override tests

### Continuous Integration

- **workflows**: Refactor to use created actions
- **workflows**: Deploy-docs now is using shared actions
- **workflows**: Release is using shared actiohs
- **workflows**: Defined lint workflow
- **workflows**: Defined prepare-release workflow
- **workflows**: Defined publish-release workflow
- **workflows**: Defined test separated workflow
- **workflows**: Defined validfate artifacts seaprated workflow
- **workflows**: Adding action ids to _GITHUB_BUILTIN
- **workflows**: Fix in test.yml
- **actions**: Install shellcheck using pip
- **scripts**: Fix pyright issues
- Update checkout actions to v6
- Update checkout actions to v6

### Miscellaneous Tasks

- **actions**: Implemented dependencies and lint actions
- **domain**: Value_object re-exports foundation ValueObject
- **infrastructure**: Package initializer
- **infrastructure**: Strictly typing subtypes
- **pyproject**: Move to mypy to pyright
- **scripts**: Improve types
- **pyproject**: Update bandit to supports python 3.14.3
- **infrastructure**: Pr issues fix
- **scripts**: Fix GitCliffChangelogGenerator
- **scripts/release**: Fix in GitCliffChangelogGenerator
- **scripts**: Lint
- **scripts**: Normalize changelog
- **scripts/release**: PrepareReleaseService adjustment
- **scripts/release**: Adjustign line breaks
- **scripts/release**: TestTagName now catches the correct error
- **actions**: Merge install-dependencies and setup-poetry
- **actions**: Ci workflow use install-dependencies
- **actions**: Install twine deparated
- **scripts/pipeline**: Impl validate_publish_local
- **scripts/pipeline**: Readjusting pipeline scripts
- **workflows**: Simplifying workflows
- Pipeline update
- **pyproject**: Maintaining poe tasks
- Poetry lock
- **workflows**: Update checkout actions
- **foundation/ports**: Remove unnecessary types ignores
- **scripts/release**: Add dry_run flag to infrastructure services
- **pyproject**: Adjust ci:simulate poe task
## [0.3.22] - 2026-03-24

### Features

- Updating to python 3.14
- **foundation**: Re-exporting messages in foundation

### Bug Fixes

- **scripts/release**: Adjust changelog generation to use current version

### Refactor

- **messages**: Move messages to foundation block
- **domain**: Adjust imports to be compatible with new structure
- **value_object**: Moving value_object to foundation block
- **application**: Adjusting imports to foundation instead of domain

### Documentation

- **domain-foundation**: Reference adjustments to reflect current structure

### Testing

- Fix for warnings and incompatible python314 tests
- **foundation**: Move message tests to foundation

### Continuous Integration

- **scripts**: Check if package version already exists on PyPI before uploading to TestPyPI
- **pipeline**: Add act-release.sh script for local testing of release workflow

### Miscellaneous Tasks

- **changelog**: Adjust changelog for recent changes
- Remove unnecessary files from repository
- Remove .github/events/release_event.json
- **gitignore**: Adding local-validate-publish.yml and .secrets.act to .gitignore
- **workflows**: Inject TEST_PYPY_TOKEN
## [0.3.21] - 2026-03-21

### Bug Fixes

- Lint scripts are now correct
- Ensure generated changelog ends with a single newline
- Update PyPI token secret name in CI and release workflows
- Validate token authentication URLs

### Continuous Integration

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
- Enforce PyPI token validation for all pull requests
- Fix typo in PyPI token secret name
- Using OIDC token for PyPI authentication

### Miscellaneous Tasks

- Enforce presence and validity of PyPI tokens in CI
- Harden PyPI publishing by validating environment contracts and PUBLISH_VERSION
- Enforce PyPI dependencies for types-pyyaml and pyyaml
- Pipeline scripts are now sharing common logging and error handling utilities
- Improving smoke test script by enforcing required environment variables
## [0.3.20] - 2026-03-20

### Continuous Integration

- Add a new ci linting step for yamllint
- Installl int tools for CI workflow
- Add yamllint configuration to prevent duplicate keys in YAML files
- Fix poorly action
- Remove environment for test-pypi
- Add shellcheck validate_publish for pipeline scripts

### Miscellaneous Tasks

- Fixing typo in release.yml
- Improving github workflows
## [0.3.19] - 2026-03-20

### Miscellaneous Tasks

- Add username to PyPI publish action
- Fix typo in release workflow
## [0.3.17] - 2026-03-20

### Continuous Integration

- Tweak GitHub Actions workflows for better validation and release process
- Fix syntax for GitHub Actions environment variable output
- Add --sync flag to poetry install in validate_publish.sh
- Add validation step to publish workflow

### Miscellaneous Tasks

- Fix GitHub Actions workflow for PyPI publishing
- Fix GitHub Actions workflow for PyPI publishing
- Another fix for GitHub Actions
- Fix in ci.yml for install git-cliff action
- Add workflow step to lint GitHub Actions workflow files
## [0.3.16] - 2026-03-20

### Bug Fixes

- Adjust release.yml to remove id-token permission
## [0.3.15] - 2026-03-20

### Bug Fixes

- Changelog generation when using git-cliff
- Validate release workflow on remote CI/CD to ensure complete release pipeline is verified
- Idempotency check + retry install
- Update version in __init__.py

### Refactor

- Combine git push commands for branch and tag into a single command
- **release**: Removing tag creation from prepare release service

### Testing

- Solve merge conflicts in release script and update tests
- Git_version_control.py  tests updated to reflect the change in push command to include the tag in a single push
- **release**: Increasing consistency in release automation

### Continuous Integration

- Fix in release workflow to check for tag existence instead of creating it
- Including validation of remote CI/CD to poe release:validate sequence
- Validate release workflow now is a shell script
- **workflows**: Add validation workflow for release process
- Add build and artifact validation steps to CI and release workflows
- Remove any tag related operations from version control port
- **scripts**: Validate_publish.sh and remove validate_release.sh
- Validate package publish to TestPyPI on pull requests
- Fix yml githbu workflows
- Add release pipeline scripts
- Fix github workflow trigger on release event
- Fix on release.yml
- Ci.yml is now using yaananth/twine-upload@v1 for validation and version bumping

### Miscellaneous Tasks

- Validate_release_remote script to check if the release workflow passed on the remote CI/CD
- Poe task is now calling a shell script instead of a python script for validating the remote CI/CD for the latest release
- Validate release workflow script and add unit tests
- **pyproject**: Add validation for GitHub release workflow
- Fix in validate release workflow test script
- Still trying to validate the release workflow script
- Remove release validation workflows
- Validate artifacts before merging release PRs
- Improving validate_release.sh
- **pyproject**: Add testpypi source for testing package publishing
- **poetry**: Update poetry.lock with new content hash and python version
- **pyproject**: Fix testpypi url
- **pyproject**: Fix testpypi url
- Fix validate_publish.sh to use the correct python interpreter
- Refactor validate_publish.sh for better error handling and CI compatibility
- Refactor CI workflow to separate validation and publishing steps
- Fix in relase workflow
## [0.3.13] - 2026-03-18

### Bug Fixes

- GitVersionControl now stages all changes before committing to ensure untracked files are included
- GitCliffChangelogGenerator now writes output to CHANGELOG.md
- Ensure changelog is written with utf-8 encoding
- Improving github actions for release automation
- Ensure that the tag is created after the commit to avoid issues with detached HEAD state
- Replaced push_tags with tag in VersionControl.push() method
- Handle pre-commit hook failures when committing release artifacts

### Refactor

- **release**: Update push method to push specific tag

### Testing

- **release**: Add e2e tests for release workflow
- Fix imports in test_release_e2e.py
- **e2e**: Add end-to-end test for release script
- Fix release workflow test to check for errors

### Continuous Integration

- Install-git-cliff action defined
- Remove name from install-git-cliff action
- Add names to steps in CI workflow
- Add the install-git-cliff action to the release workflow

### Miscellaneous Tasks

- Update install-git-cliff action to use composite syntax
- Update git checkout logic to auto-detect default branch
- **prepare_release_service**: Add tag creation and deletion to transaction
## [0.3.12] - 2026-03-17

### Features

- ChangelogGenerator is now generated using git-cliff instead of raw git log parsing

### Bug Fixes

- **changelog**: Update changelog generator to use provided command runner
- **release**: Container now imports from scripts.release
- Update test for GitCliffChangelogGenerator to use instance mock

### Refactor

- Move container to infrastructure layer
- **poetry**: Remove default command runner for better testability
- **release**: Exposing ChangelogGenerationError in errors module
- Improve error handling in GitCliffChangelogGenerator
- Improve error handling in release presenter
- Improve release preparation readability and maintainability
- Improve GitCliffChangelogGenerator's tag resolution strategy

### Documentation

- **changelog**: GitCliffChangelogGenerator docstring clarification

### Testing

- Pytest fixtures to avoid code duplication in test_main_unit.py
- Improving test coverage for GitCliffChangelogGenerator and PrepareReleaseService
- Fix imports from test_prepare_release_service.py

### Continuous Integration

- Release back to pyproject.toml
- Add git-cliff setup to github CI workflow

### Miscellaneous Tasks

- Improve release automation tests
- Generate base changelog
## [0.3.7] - 2026-01-26

### Bug Fixes

- UI is now more readable
- Chore: remove versioning from common release script
- Raise InvalidReleaseBranchNameError from InvalidReleaseVersionError
- Correct test for process run with check=False
- Add missing subprocess.run patch decorator to logging test
- Improve changelog generation and test configuration
- Add missing push step before PR creation

### Refactor

- Adjust release scripts to improve modularity and testability
- Adjusting docs to new release script syntax

### Miscellaneous Tasks

- Update mkdocs.yml to use mike for versioning and improve structure
- Changing assets
- Updated pyproject.toml
- Adjusting release scripts and adding debug test command
## [0.3.6] - 2025-11-11

### Documentation

- Add release guide and update readme/index

### Miscellaneous Tasks

- Bump version to v0.3.6
## [0.3.5] - 2025-11-10

### Continuous Integration

- Switch to official OIDC publisher

### Miscellaneous Tasks

- **ci**: Fix PyPI publish workflow and align package name
- **ci**: Fix PyPI publish workflow and align package name
## [0.3.4] - 2025-11-10

### Bug Fixes

- Adjusting publish.yml
- Publish.yml
- **ci**: Use OIDC-only publish pipeline
- **ci**: Correct PyPI OIDC publish workflow
- **ci**: Correct PyPI OIDC workflow for release 0.3.4

### Miscellaneous Tasks

- Update publish workflow and bump version to 0.3.2
- Package name
## [0.3.1] - 2025-11-09

## [0.3.23] - 2026-05-31

### Refactor

- **create_github_release**: Delegate logic to functions
- **create_github_release**: Redirect log outputs

### Miscellaneous Tasks

- **scripts/pipeline**: Impl create_github_release
- **workflows**: New job to create github release
## [0.3.22] - 2026-05-30

### Features

- **infrastructure**: Impl infrastructure errors
- **infrastructure**: Impl InMemoryMessageBus
- **infrastructure**: Impl UnitOfWork
- **infrastructure**: Impl InMemoryReadRepository and InMemoryWriteRepository
- **domain**: Defien abstractmethod apply
- **foundation**: Defined Identified
- **foundation**: Impl FinalABCMeta
- **domain/aggregate_root**: Impl replay method to allow ES usage
- **foundation/meta**: Impl validate_no_runtime_final_override function

### Bug Fixes

- **infrastructure/unit_of_work**: Import fix
- Adjuting infrastructure and pipeline to pr issue
- **domain**: DraftEntityIsNotHashableError error text improvement
- **domain**: AggregateRoot is not allowing falsy ids

### Refactor

- **pipeline**: Refactor in pipline script
- **infrastructure**: Improving infrastructure classes
- **application**: Improve types
- Improve types
- **infrastructure/unit_of_work**: Commit behavior marks rolled_back as false
- **domain/aggregate_root**: Make uncommitted_changes a property
- **domain**: Impl discard_events method of AggregateRoot
- **infrastructure/unit_of_work**: Discard_events in rollback
- **release**: Improve GitCliffChangelogGenerator
- **domain/aggregate_root**: Split aggregate_root into 2 files
- **infrastructure**: InMemoryWriteRepository uses Identified
- **foundation/value_object**: ValueObject now raises CantModifyImmutableAttributeError
- **foundation/meta**: Impl new magic method in FinalABCMeta
- **domain/aggregate_root**: Metaclass is now FinalABCMeta
- **foundation**: FinalABCMeta is now using validate_no_runtime_final_override

### Documentation

- Replace layer to block
- Remove RELEASE_GUIDE
- **infrastructure**: README.md for infrastructure block
- **RELEASE_GUIDE**: Align RELEASE_GUIDE with release automation
- Compliance docs with last version
- Sync docs with last version
- **foundation**: Improving consistency of docstrings

### Testing

- **infrastructure**: Remove unnecessary tests
- **git-cliff**: Impl git_cliff_scenarios
- **conftest**: Re-export fixtures
- **scripts/release**: Refactor mock_run
- **fixtures**: Create one more scenario
- **domain/entity**: Exercise draft entity in tests
- **infrastructure/unit_of_work**: Add apply method to stub
- **domain/errors**: Remove test_from_class_name_source_has_no_dead_code
- **infrastructure/unit_of_work**: Adjust test helper
- **foundation/meta**: Validate_no_runtime_final_override tests

### Continuous Integration

- **workflows**: Refactor to use created actions
- **workflows**: Deploy-docs now is using shared actions
- **workflows**: Release is using shared actiohs
- **workflows**: Defined lint workflow
- **workflows**: Defined prepare-release workflow
- **workflows**: Defined publish-release workflow
- **workflows**: Defined test separated workflow
- **workflows**: Defined validfate artifacts seaprated workflow
- **workflows**: Adding action ids to _GITHUB_BUILTIN
- **workflows**: Fix in test.yml
- **actions**: Install shellcheck using pip
- **scripts**: Fix pyright issues
- Update checkout actions to v6
- Update checkout actions to v6

### Miscellaneous Tasks

- **actions**: Implemented dependencies and lint actions
- **domain**: Value_object re-exports foundation ValueObject
- **infrastructure**: Package initializer
- **infrastructure**: Strictly typing subtypes
- **pyproject**: Move to mypy to pyright
- **scripts**: Improve types
- **pyproject**: Update bandit to supports python 3.14.3
- **infrastructure**: Pr issues fix
- **scripts**: Fix GitCliffChangelogGenerator
- **scripts/release**: Fix in GitCliffChangelogGenerator
- **scripts**: Lint
- **scripts**: Normalize changelog
- **scripts/release**: PrepareReleaseService adjustment
- **scripts/release**: Adjustign line breaks
- **scripts/release**: TestTagName now catches the correct error
- **actions**: Merge install-dependencies and setup-poetry
- **actions**: Ci workflow use install-dependencies
- **actions**: Install twine deparated
- **scripts/pipeline**: Impl validate_publish_local
- **scripts/pipeline**: Readjusting pipeline scripts
- **workflows**: Simplifying workflows
- Pipeline update
- **pyproject**: Maintaining poe tasks
- Poetry lock
- **workflows**: Update checkout actions
- **foundation/ports**: Remove unnecessary types ignores
- **scripts/release**: Add dry_run flag to infrastructure services
- **pyproject**: Adjust ci:simulate poe task
## [0.3.22] - 2026-03-24

### Features

- Updating to python 3.14
- **foundation**: Re-exporting messages in foundation

### Bug Fixes

- **scripts/release**: Adjust changelog generation to use current version

### Refactor

- **messages**: Move messages to foundation block
- **domain**: Adjust imports to be compatible with new structure
- **value_object**: Moving value_object to foundation block
- **application**: Adjusting imports to foundation instead of domain

### Documentation

- **domain-foundation**: Reference adjustments to reflect current structure

### Testing

- Fix for warnings and incompatible python314 tests
- **foundation**: Move message tests to foundation

### Continuous Integration

- **scripts**: Check if package version already exists on PyPI before uploading to TestPyPI
- **pipeline**: Add act-release.sh script for local testing of release workflow

### Miscellaneous Tasks

- **changelog**: Adjust changelog for recent changes
- Remove unnecessary files from repository
- Remove .github/events/release_event.json
- **gitignore**: Adding local-validate-publish.yml and .secrets.act to .gitignore
- **workflows**: Inject TEST_PYPY_TOKEN
## [0.3.21] - 2026-03-21

### Bug Fixes

- Lint scripts are now correct
- Ensure generated changelog ends with a single newline
- Update PyPI token secret name in CI and release workflows
- Validate token authentication URLs

### Continuous Integration

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
- Enforce PyPI token validation for all pull requests
- Fix typo in PyPI token secret name
- Using OIDC token for PyPI authentication

### Miscellaneous Tasks

- Enforce presence and validity of PyPI tokens in CI
- Harden PyPI publishing by validating environment contracts and PUBLISH_VERSION
- Enforce PyPI dependencies for types-pyyaml and pyyaml
- Pipeline scripts are now sharing common logging and error handling utilities
- Improving smoke test script by enforcing required environment variables
## [0.3.20] - 2026-03-20

### Continuous Integration

- Add a new ci linting step for yamllint
- Installl int tools for CI workflow
- Add yamllint configuration to prevent duplicate keys in YAML files
- Fix poorly action
- Remove environment for test-pypi
- Add shellcheck validate_publish for pipeline scripts

### Miscellaneous Tasks

- Fixing typo in release.yml
- Improving github workflows
## [0.3.19] - 2026-03-20

### Miscellaneous Tasks

- Add username to PyPI publish action
- Fix typo in release workflow
## [0.3.17] - 2026-03-20

### Continuous Integration

- Tweak GitHub Actions workflows for better validation and release process
- Fix syntax for GitHub Actions environment variable output
- Add --sync flag to poetry install in validate_publish.sh
- Add validation step to publish workflow

### Miscellaneous Tasks

- Fix GitHub Actions workflow for PyPI publishing
- Fix GitHub Actions workflow for PyPI publishing
- Another fix for GitHub Actions
- Fix in ci.yml for install git-cliff action
- Add workflow step to lint GitHub Actions workflow files
## [0.3.16] - 2026-03-20

### Bug Fixes

- Adjust release.yml to remove id-token permission
## [0.3.15] - 2026-03-20

### Bug Fixes

- Changelog generation when using git-cliff
- Validate release workflow on remote CI/CD to ensure complete release pipeline is verified
- Idempotency check + retry install
- Update version in __init__.py

### Refactor

- Combine git push commands for branch and tag into a single command
- **release**: Removing tag creation from prepare release service

### Testing

- Solve merge conflicts in release script and update tests
- Git_version_control.py  tests updated to reflect the change in push command to include the tag in a single push
- **release**: Increasing consistency in release automation

### Continuous Integration

- Fix in release workflow to check for tag existence instead of creating it
- Including validation of remote CI/CD to poe release:validate sequence
- Validate release workflow now is a shell script
- **workflows**: Add validation workflow for release process
- Add build and artifact validation steps to CI and release workflows
- Remove any tag related operations from version control port
- **scripts**: Validate_publish.sh and remove validate_release.sh
- Validate package publish to TestPyPI on pull requests
- Fix yml githbu workflows
- Add release pipeline scripts
- Fix github workflow trigger on release event
- Fix on release.yml
- Ci.yml is now using yaananth/twine-upload@v1 for validation and version bumping

### Miscellaneous Tasks

- Validate_release_remote script to check if the release workflow passed on the remote CI/CD
- Poe task is now calling a shell script instead of a python script for validating the remote CI/CD for the latest release
- Validate release workflow script and add unit tests
- **pyproject**: Add validation for GitHub release workflow
- Fix in validate release workflow test script
- Still trying to validate the release workflow script
- Remove release validation workflows
- Validate artifacts before merging release PRs
- Improving validate_release.sh
- **pyproject**: Add testpypi source for testing package publishing
- **poetry**: Update poetry.lock with new content hash and python version
- **pyproject**: Fix testpypi url
- **pyproject**: Fix testpypi url
- Fix validate_publish.sh to use the correct python interpreter
- Refactor validate_publish.sh for better error handling and CI compatibility
- Refactor CI workflow to separate validation and publishing steps
- Fix in relase workflow
## [0.3.13] - 2026-03-18

### Bug Fixes

- GitVersionControl now stages all changes before committing to ensure untracked files are included
- GitCliffChangelogGenerator now writes output to CHANGELOG.md
- Ensure changelog is written with utf-8 encoding
- Improving github actions for release automation
- Ensure that the tag is created after the commit to avoid issues with detached HEAD state
- Replaced push_tags with tag in VersionControl.push() method
- Handle pre-commit hook failures when committing release artifacts

### Refactor

- **release**: Update push method to push specific tag

### Testing

- **release**: Add e2e tests for release workflow
- Fix imports in test_release_e2e.py
- **e2e**: Add end-to-end test for release script
- Fix release workflow test to check for errors

### Continuous Integration

- Install-git-cliff action defined
- Remove name from install-git-cliff action
- Add names to steps in CI workflow
- Add the install-git-cliff action to the release workflow

### Miscellaneous Tasks

- Update install-git-cliff action to use composite syntax
- Update git checkout logic to auto-detect default branch
- **prepare_release_service**: Add tag creation and deletion to transaction
## [0.3.12] - 2026-03-17

### Features

- ChangelogGenerator is now generated using git-cliff instead of raw git log parsing

### Bug Fixes

- **changelog**: Update changelog generator to use provided command runner
- **release**: Container now imports from scripts.release
- Update test for GitCliffChangelogGenerator to use instance mock

### Refactor

- Move container to infrastructure layer
- **poetry**: Remove default command runner for better testability
- **release**: Exposing ChangelogGenerationError in errors module
- Improve error handling in GitCliffChangelogGenerator
- Improve error handling in release presenter
- Improve release preparation readability and maintainability
- Improve GitCliffChangelogGenerator's tag resolution strategy

### Documentation

- **changelog**: GitCliffChangelogGenerator docstring clarification

### Testing

- Pytest fixtures to avoid code duplication in test_main_unit.py
- Improving test coverage for GitCliffChangelogGenerator and PrepareReleaseService
- Fix imports from test_prepare_release_service.py

### Continuous Integration

- Release back to pyproject.toml
- Add git-cliff setup to github CI workflow

### Miscellaneous Tasks

- Improve release automation tests
- Generate base changelog
## [0.3.7] - 2026-01-26

### Bug Fixes

- UI is now more readable
- Chore: remove versioning from common release script
- Raise InvalidReleaseBranchNameError from InvalidReleaseVersionError
- Correct test for process run with check=False
- Add missing subprocess.run patch decorator to logging test
- Improve changelog generation and test configuration
- Add missing push step before PR creation

### Refactor

- Adjust release scripts to improve modularity and testability
- Adjusting docs to new release script syntax

### Miscellaneous Tasks

- Update mkdocs.yml to use mike for versioning and improve structure
- Changing assets
- Updated pyproject.toml
- Adjusting release scripts and adding debug test command
## [0.3.6] - 2025-11-11

### Documentation

- Add release guide and update readme/index

### Miscellaneous Tasks

- Bump version to v0.3.6
## [0.3.5] - 2025-11-10

### Continuous Integration

- Switch to official OIDC publisher

### Miscellaneous Tasks

- **ci**: Fix PyPI publish workflow and align package name
- **ci**: Fix PyPI publish workflow and align package name
## [0.3.4] - 2025-11-10

### Bug Fixes

- Adjusting publish.yml
- Publish.yml
- **ci**: Use OIDC-only publish pipeline
- **ci**: Correct PyPI OIDC publish workflow
- **ci**: Correct PyPI OIDC workflow for release 0.3.4

### Miscellaneous Tasks

- Update publish workflow and bump version to 0.3.2
- Package name
## [0.3.1] - 2025-11-09

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
