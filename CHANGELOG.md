## [unreleased]

### 🚀 Features

- ChangelogGenerator is now generated using git-cliff instead of raw git log parsing

### 🐛 Bug Fixes

- *(changelog)* Update changelog generator to use provided command runner
- *(release)* Container now imports from scripts.release
- Update test for GitCliffChangelogGenerator to use instance mock

### 💼 Other

- Add GitHub project setup, issue templates, and v1.0.0 roadmap

### 🚜 Refactor

- Move container to infrastructure layer
- *(poetry)* Remove default command runner for better testability
- *(release)* Exposing ChangelogGenerationError in errors module
- Improve error handling in GitCliffChangelogGenerator
- Improve error handling in release presenter

### 📚 Documentation

- *(changelog)* GitCliffChangelogGenerator docstring clarification

### 🧪 Testing

- Pytest fixtures to avoid code duplication in test_main_unit.py

### ⚙️ Miscellaneous Tasks

- Release back to pyproject.toml
- Improve release automation tests
- *(cliff)* Add cliff config file
- *(release)* Prepare release
## [0.3.7] - 2026-01-26

### 🐛 Bug Fixes

- UI is now more readable
- Chore: remove versioning from common release script
- Raise InvalidReleaseBranchNameError from InvalidReleaseVersionError
- Correct test for process run with check=False
- Add missing subprocess.run patch decorator to logging test
- Improve changelog generation and test configuration
- Add missing push step before PR creation

### 💼 Other

- 0.4.0
- 0.4.1
- Implement infrastructure layer
- Adjusting release scripts to use command bus pattern
- Server is now in pyproject.toml for local doc serving

### 🚜 Refactor

- Adjust release scripts to improve modularity and testability
- Adjusting docs to new release script syntax

### ⚙️ Miscellaneous Tasks

- Update mkdocs.yml to use mike for versioning and improve structure
- Changing assets
- Updated pyproject.toml
- *(release)* Prepare release
- Adjusting release scripts and adding debug test command
## [0.3.6] - 2025-11-11

### 📚 Documentation

- Add release guide and update readme/index

### ⚙️ Miscellaneous Tasks

- Bump version to v0.3.6
## [0.3.5] - 2025-11-10

### ⚙️ Miscellaneous Tasks

- *(ci)* Fix PyPI publish workflow and align package name
- *(ci)* Fix PyPI publish workflow and align package name
- Switch to official OIDC publisher
## [0.3.4] - 2025-11-10

### 🐛 Bug Fixes

- Adjusting publish.yml
- Publish.yml
- *(ci)* Use OIDC-only publish pipeline
- *(ci)* Correct PyPI OIDC publish workflow
- *(ci)* Correct PyPI OIDC workflow for release 0.3.4

### ⚙️ Miscellaneous Tasks

- Update publish workflow and bump version to 0.3.2
- Package name
## [0.3.1] - 2025-11-09

### 💼 Other

- Force update
- V0.3.1
