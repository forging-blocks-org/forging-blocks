## [0.4.4] - 2026-07-02

### Features

- **domain**: Add EntityIdModificationError for immutable identity protection
- **domain**: Add EntityIdDeletionError to prevent identity deletion
- **domain**: Export EntityIdDeletionError and EntityIdModificationError
- **domain**: Re-export new entity error types from domain package
- **foundation**: Remove dead SupportsAutoFreeze protocol module
- **domain**: Add specification pattern with operator overloading
- **infrastructure**: Add generic repository base classes and aggregate repository
- **infrastructure**: Add event store and event bus ports with in-memory implementations
- **application**: Add service context, application service with middleware, and query service
- **infrastructure**: Add logger and file system ports with implementations
- **foundation**: Add specification pattern with composable operators
- **foundation**: Add message dataclass decorator and Serializable protocol
- **ports**: Add CachePort protocol for caching strategies
- **ports**: Add ExternalServicePort protocol for HTTP clients
- **infra**: Add InMemoryCache and URLLibClient adapters
- **infra**: Add MessageBusCommandSender, MessageBusEventPublisher, MessageBusQueryFetcher adapters

### Bug Fixes

- **scripts**: Correct redirect template asset prefixing and type hints
- **scripts**: Resolve ruff line length error in redirect template script
- **scripts**: Ensure favicon is extracted and prefixed in redirect template
- **build**: Restore mkdocs.yml after docs:build to keep working tree clean for pre-commit
- Make script tag regex handle edge cases in closing tags
- **domain**: Raise NotImplementedError in freeze_instance to satisfy linter and protocol
- **foundation/value-object**: Fix asymmetric instance check in equality comparison
- **foundation/value-object**: Fix pyright type errors in equality comparison
- **release**: Change _payload return type to dict[str, object]
- **release**: Add explicit ErrorMetadata type annotation
- **infrastructure**: Make InMemoryMessageBus.register generic with cast
- **release**: Change handler type from CommandHandler to MessageHandler
- **release**: Match ReleaseCommandBus interface with MessageHandler
- **release**: Remove type ignore comment from register call
- **foundation**: Satisfy pyright on decorator monkey-patching and frozen test
- Replace assert with explicit check; fix griffe docstring warning
- **tests**: Sanitize GIT_DIR env vars in test fixtures to prevent hook failures
- Set doc default to dev and fetch global versions.json instead of stale per-version copy

### Refactor

- **domain**: Auto freeze id of Entity subclasses
- **domain**: Use auto_freeze for selective _id freezing in Entity base class
- **foundation**: Simplify auto_freeze decorator to require only freeze_instance protocol
- **foundation**: Remove unfreeze_instance and should_use_internal_freezing from SupportsAutoFreeze protocol
- **foundation**: Remove unfreeze_instance and should_use_internal_freezing from ValueObject
- **foundation**: Skip auto_freeze for abstract classes to allow super().__init__ chaining
- **foundation**: Restore @auto_freeze on ValueObject base class for automatic immutability
- **foundation**: Make auto_freeze self-contained without protocol requirements
- **foundation**: Simplify ValueObject to use auto_freeze without protocol methods
- **domain**: Simplify Entity to use auto_freeze without protocol methods
- **foundation**: Remove SupportsAutoFreeze from autofreeze exports
- **domain**: Remove stale comments in Entity.__setattr__
- **foundation**: Remove stale comments in _AutoFreezeDecorator
- **message-bus**: Replace inspect.iscoroutine with asyncio.iscoroutine
- **application**: Relocate errors, move SpecificationRepository, drop service scaffolding
- **domain**: Remove duplicate specification in favor of foundation
- Replace string-quoted self-returning type hints with typing.Self
- **ports**: Rename all outbound port classes to use Port suffix
- **ports**: Update __init__.py exports with Port suffix names
- **scripts**: Update release scripts for Port suffix rename
- **domain**: Remove default EventPayloadType from AggregateRoot, require explicit type parameter
- **ports**: Remove behavior from ports, convert to pure protocols
- **ports**: Add @runtime_checkable to base Port protocol
- **ports**: Ensure all ports inherit InboundPort/OutboundPort
- Rename ReadOnlyRepository and WriteOnlyRepository with Port suffix
- Update BaseRepository classes to use renamed port interfaces
- Make message bus adapters explicitly extend protocol ports
- Rename outbound port files to match class names with _port suffix

### Documentation

- **README**: Remove emoji
- Replace emoji to plain text
- **contributing**: Document pre-commit and pre-push hooks
- **foundation**: Update auto-freeze documentation for simplified SupportsAutoFreeze protocol
- **foundation**: Update auto-freeze docs for self-contained decorator
- Replace :class: with backticks in result_access_error.py
- Replace :class: and :meth: with backticks in result/ok.py
- Replace :class: with backticks in result/err.py
- Replace :class: with backticks in error.py
- Replace :class: with backticks in error.py
- Replace :class: and :meth: with backticks in multiple files
- **contributing**: Move quick summary to top and rename from 'In short'
- **index**: Add quick summary section
- **reference**: Add quick summary to reference index
- **reference**: Add quick summary to foundation
- **reference**: Add quick summary to domain
- **reference**: Add quick summary to application
- **reference**: Add quick summary to infrastructure
- **reference**: Add quick summary to presentation
- **reference**: Add quick summary to testing reference
- **guide**: Add quick summary and remove old 'In short' section
- **guide**: Add quick summary to getting started
- **guide**: Add quick summary to principles
- **guide**: Add quick summary to examples
- **guide**: Add quick summary to example tests
- **guide**: Add quick summary to architecture overview
- **guide**: Add quick summary to recommended blocks structure
- **guide**: Add quick summary to testing guide
- **arch-styles**: Add quick summary to architectural styles index
- **arch-styles**: Add quick summary and fix structure for clean architecture
- **arch-styles**: Add quick summary and fix structure for hexagonal architecture
- **arch-styles**: Add quick summary and fix structure for layered architecture
- **arch-styles**: Add quick summary and fix structure for CQRS
- **arch-styles**: Add quick summary and fix structure for event-driven
- **contributing**: Add quick summary and remove duplicate 'In short' section
- **contributing**: Add quick summary and separators to contributing index
- **reference**: Add quick summary to clean architecture reference
- Replace emoji tags with plain text in release guide, readme, and scripts readme
- **index**: Remove InputPort/OutputPort from Core Concepts table
- **guide**: Remove InputPort/OutputPort from Foundation block list
- **reference**: Remove InputPort/OutputPort aliases from Port documentation
- **reference**: Sync block documentation with current codebase
- Rm md file that was in a wrong path
- **reference**: Clarify Specification lives in Foundation block, not Domain
- Add architecture-agnostic disclaimer; DDD not required
- **domain**: Fix README - unclosed code fence, typos, outdated structure
- **presentation**: Fix README - typos, duplicate headers, unclear placement
- Remove /examples references (examples in separate repo)
- **guide**: Fix examples.md - add missing section header, remove unused Protocol import, add Self import; fix example_tests.md numbering
- **guide**: Update Example 2 to use Entity with auto_freeze explanation and cross-references
- **guide**: Fix relative paths in examples.md cross-references
- Sync port names with Port suffix rename

### Testing

- Cover script tag regex edge cases and fix CodeQL warning
- **foundation**: Update auto_freeze tests for simplified SupportsAutoFreeze protocol
- **foundation**: Remove tests for removed unfreeze_instance and should_use_internal_freezing methods
- **domain**: Update entity tests for EntityIdDeletionError and removed unfreeze_instance
- **foundation**: Update auto_freeze tests for self-contained implementation
- Evaluating issue related to issue-229
- **foundation**: Remove pyright suppressions and fix type errors
- **infrastructure**: Remove pyright suppressions and fix type errors
- **infrastructure**: Fix private usage with getattr for pyright compliance
- Add event store and event bus tests
- Add SimpleFakeCommandWithValue fixture for event bus tests
- **fixtures**: Remove unused typing.Any imports
- **infra**: Fix InMemoryEventBus tests to use shared fixtures
- **infra**: Fix InMemoryEventStore tests to import FakeEventWithName fixture
- **infra**: Replace inline fakes with fixtures in EventBus tests
- **infra**: Replace inline FakeEvent with fixture in AggregateRepository tests
- Update existing tests for Port suffix rename
- **ports**: Add contract tests for CachePort, ExternalServicePort, FileSystemPort, LoggerPort
- Replace isinstance Protocol checks with hasattr assertions

### Miscellaneous Tasks

- **workflows**: Replace emoji to plain text
- **pre-commit-config**: Replace emoji to plain text
- Replace emoji to plain text
- **scripts**: Redirect template adjusts
- **scripts**: Redirect template adjusts
- **workflows**: Pr preview docs
- **tests**: Remove unused import in redirect template tests
- **git**: Move CI simulation to pre-push hook stage
- **tests**: Cleanup redirect template tests
- Pre-push
- **git**: Restrict mkdocs.yml check to only run when the file is changed
- **scripts**: Adjust regex
- **workflows**: Update setup-python action
- Strip v prefix
- **poetry**: Update pyright
- **domain**: Remove unnecessary future import from aggregate_root
- **domain**: Remove unnecessary future import from entity
- **domain**: Remove future import and use Self return type in draft_entity_is_not_hashable_error
- **domain**: Remove unnecessary future import from entity_id_deletion_error
- **domain**: Remove unnecessary future import from entity_id_modification_error
- **foundation**: Remove unnecessary future import from auto_freeze
- **foundation**: Remove unnecessary future import from cant_modify_immutable_attribute_error
- **foundation**: Remove unnecessary future import from message
- **foundation**: Remove unnecessary future import from final_abc_meta
- **infrastructure**: Remove unnecessary future import from repository_errors
- **infrastructure**: Remove unnecessary future import from in_memory_unit_of_work
- **foundation**: Remove InputPort/OutputPort from exports
- **foundation**: Remove InputPort/OutputPort class definitions
- **scripts**: Replace OutputPort with OutboundPort in PullRequestService
- **scripts**: Replace OutputPort with OutboundPort in VersionControl
- **scripts**: Replace OutputPort with OutboundPort in VersioningService
- Ignore B009 in tests for getattr pattern; fix test private usage
- Update package exports for new modules
- **github**: Add Copilot review instructions
- **infrastructure**: Suppress bandit B310 false positive in URLLibClient urlopen call
- **github**: Add Copilot review instructions
- Remove autodocs from gitignore

## [0.4.3] - 2026-06-14

### Features

- **docs**: Impl version-dropdown
- **docs/assets**: Impl version-dropdown.js

### Bug Fixes

- **docs**: Add extra.version.provider mike config so version selector renders in Material theme
- **scripts**: Include __md_scope init and font preconnect in redirect template
- **scripts**: Resolve ruff F841 and pyright strict-mode errors
- **build**: Align docs:deploy poe tasks with CI deploy pipeline
- **docs**: Use relative path for versions.json fetch
- **docs**: Resolve version from path by matching against known identifiers
- **docs**: Resolve versions.json and version from script location

### Refactor

- **docs**: Remove top-most version-dropdown
- **foundation**: Replace TypeVar and Generic with PEP 695 type parameters
- **foundation**: Migrate port protocols to PEP 695 type parameters
- **foundation**: Replace TypeVar and Generic with PEP 695 type parameters
- **domain**: Replace TypeVar and Generic with PEP 696 type params
- **domain**: PEP 696 type params compliant
- **application**: Modernize MessageHandler to PEP 695 inline generics; retain TypeVars for CommandHandler/QueryHandler/EventHandler TypeAlias definitions
- **application**: Modernize UseCase to PEP 695 inline generics; drop module-level TypeVar declarations
- **application**: Modernize MessageBus to PEP 695 inline generics; drop module-level TypeVar declarations
- **application**: Modernize Notifier to PEP 695 inline generics; drop module-level TypeVar declaration
- **application**: Modernize QueryFetcher to PEP 695 inline generics; drop module-level TypeVar declaration
- **application**: Modernize ReadOnlyRepository/WriteOnlyRepository/Repository to PEP 695 inline generics; drop module-level TypeVar declarations
- **infrastructure**: Modernize InMemoryMessageBus to PEP 695 inline generics; drop module-level TypeVar declarations
- **infrastructure**: Modernize InMemoryReadRepository to PEP 695 inline generics; drop module-level TypeVar declarations
- **infrastructure**: Modernize InMemoryWriteRepository to PEP 695 inline generics; drop module-level TypeVar declarations; add MutableMapping import

### Documentation

- Add task issue template for github
- **foundation**: Add docstrings to auto-freeze decorator module, _AutoFreezeDecorator class, and auto_freeze function with protocol validation details and usage examples
- **foundation**: Document CantModifyImmutableAttributeError.__init__ class_name and attribute_name parameters
- **foundation**: Document CombinedErrors.__init__ errors iterable parameter explaining internal tuple storage
- **foundation**: Document Error.__init__ message and metadata parameters with default ErrorMetadata fallback
- **foundation**: Document FieldErrors.__init__ field and errors parameters including ValueError on empty input
- **foundation**: Document ResultAccessError.__init__ optional message parameter with default fallback message
- **foundation**: Remove redundant Args section from _AutoFreezeDecorator class docstring, merge detail into __init__
- **foundation**: Replace circular SupportsAutoFreeze example with traditional class, regular dataclass, and frozen dataclass examples
- **foundation**: Explain why ValueObject over frozen dataclass — freeze timing, natural __init__, selective equality
- **assets**: Version visual aesthetics
- **version-dropdown**: Appears in all routes
- **version-dropdown**: Appears locally ou in remote
- **versions.json**: Update version control json
- **versions**: Add newline
- **README**: Remove emoji
- Replace emoji to plain text

### Testing

- Implement smoke test pipeline script

### Continuous Integration

- **scripts**: Run mike set-default after each deploy
- Add workflow_dispatch to deploy-docs for manual version deployment

### Miscellaneous Tasks

- **actions**: Orhun/git-cliff-action
- **actions**: Update setup-python to v6
- **workflows**: Improve deploy-docs workflow
- **scripts**: Add retry strategy
- **actions**: Define deploy-doocs action
- Update deploy-docs action configuration
- Add git configuration action
- Update setup-poetry action workflow
- **actions**: Add smoke-test
- **actions/deploy-docs**: Ignore-remote-status
- **workflows**: Add if env.ACT to add compatibility with local act
- **workflows**: Add github_token
- **actions**: Change provider to taiki-e
- **actions/deploy-docs**: Rebase gh-pages
- **workflows/ci**: Add a validation pre-merge job
- **actions**: Add commit to deploy-docs action
- **actions/checkout**: Define checkout action
- **workflows**: Use internal checkout
- **actions**: Add description
- **actions**: Add shell
- **workflows**: Use internal checkout action
- **actions**: Remove shell
- Using actions/checkout
- **actions/deploy-docs**: Sync with gh-pages
- **actions/deploy-docs**: Sync deploy-docs
- **workflows/deploy-docs**: Fetch from gh-pages branch
- **workflows**: Add guard in case branch doesnt exists
- **mkdocs**: Default versions is latest
- **pyproject**: Poe tasks for mkdocs mike plugin
- **mkdocs**: Add mike config and js for versioned documentation
- **docs**: Versions.json created to mike versioned docs
- **scripts**: Integrate with mike
- **actions**: Deploying versioned documentations
- **workflows**: Release.yml also deploy docs
- **docs**: Correct version string in versions.json
- **scripts**: Add redirect template generator
- **docs**: Add custom redirect template for mike set-default
- **mkdocs**: Configure mike redirect alias type and template
- **docs**: Regenerate redirect template with __md_scope and preconnect
- **mkdocs**: Remove auto-generated API Reference nav section
- **scripts**: Update mike usage
- **workflows**: Add new line
- **pyproject**: Sync ci:simulate
- **workflows**: Replace emoji to plain text
- **pre-commit-config**: Replace emoji to plain text
- Replace emoji to plain text

## [0.4.2] - 2026-06-14

### Features

- **docs**: Impl version-dropdown
- **docs/assets**: Impl version-dropdown.js

### Bug Fixes

- **docs**: Add extra.version.provider mike config so version selector renders in Material theme
- **scripts**: Include __md_scope init and font preconnect in redirect template
- **scripts**: Resolve ruff F841 and pyright strict-mode errors
- **build**: Align docs:deploy poe tasks with CI deploy pipeline
- **docs**: Use relative path for versions.json fetch
- **docs**: Resolve version from path by matching against known identifiers
- **docs**: Resolve versions.json and version from script location

### Refactor

- **docs**: Remove top-most version-dropdown
- **foundation**: Replace TypeVar and Generic with PEP 695 type parameters
- **foundation**: Migrate port protocols to PEP 695 type parameters
- **foundation**: Replace TypeVar and Generic with PEP 695 type parameters
- **domain**: Replace TypeVar and Generic with PEP 696 type params
- **domain**: PEP 696 type params compliant
- **application**: Modernize MessageHandler to PEP 695 inline generics; retain TypeVars for CommandHandler/QueryHandler/EventHandler TypeAlias definitions
- **application**: Modernize UseCase to PEP 695 inline generics; drop module-level TypeVar declarations
- **application**: Modernize MessageBus to PEP 695 inline generics; drop module-level TypeVar declarations
- **application**: Modernize Notifier to PEP 695 inline generics; drop module-level TypeVar declaration
- **application**: Modernize QueryFetcher to PEP 695 inline generics; drop module-level TypeVar declaration
- **application**: Modernize ReadOnlyRepository/WriteOnlyRepository/Repository to PEP 695 inline generics; drop module-level TypeVar declarations
- **infrastructure**: Modernize InMemoryMessageBus to PEP 695 inline generics; drop module-level TypeVar declarations
- **infrastructure**: Modernize InMemoryReadRepository to PEP 695 inline generics; drop module-level TypeVar declarations
- **infrastructure**: Modernize InMemoryWriteRepository to PEP 695 inline generics; drop module-level TypeVar declarations; add MutableMapping import

### Documentation

- Add task issue template for github
- **foundation**: Add docstrings to auto-freeze decorator module, _AutoFreezeDecorator class, and auto_freeze function with protocol validation details and usage examples
- **foundation**: Document CantModifyImmutableAttributeError.__init__ class_name and attribute_name parameters
- **foundation**: Document CombinedErrors.__init__ errors iterable parameter explaining internal tuple storage
- **foundation**: Document Error.__init__ message and metadata parameters with default ErrorMetadata fallback
- **foundation**: Document FieldErrors.__init__ field and errors parameters including ValueError on empty input
- **foundation**: Document ResultAccessError.__init__ optional message parameter with default fallback message
- **foundation**: Remove redundant Args section from _AutoFreezeDecorator class docstring, merge detail into __init__
- **foundation**: Replace circular SupportsAutoFreeze example with traditional class, regular dataclass, and frozen dataclass examples
- **foundation**: Explain why ValueObject over frozen dataclass — freeze timing, natural __init__, selective equality
- **assets**: Version visual aesthetics
- **version-dropdown**: Appears in all routes
- **version-dropdown**: Appears locally ou in remote
- **versions.json**: Update version control json
- **versions**: Add newline

### Testing

- Implement smoke test pipeline script

### Continuous Integration

- **scripts**: Run mike set-default after each deploy
- Add workflow_dispatch to deploy-docs for manual version deployment

### Miscellaneous Tasks

- **actions**: Orhun/git-cliff-action
- **actions**: Update setup-python to v6
- **workflows**: Improve deploy-docs workflow
- **scripts**: Add retry strategy
- **actions**: Define deploy-doocs action
- Update deploy-docs action configuration
- Add git configuration action
- Update setup-poetry action workflow
- **actions**: Add smoke-test
- **actions/deploy-docs**: Ignore-remote-status
- **workflows**: Add if env.ACT to add compatibility with local act
- **workflows**: Add github_token
- **actions**: Change provider to taiki-e
- **actions/deploy-docs**: Rebase gh-pages
- **workflows/ci**: Add a validation pre-merge job
- **actions**: Add commit to deploy-docs action
- **actions/checkout**: Define checkout action
- **workflows**: Use internal checkout
- **actions**: Add description
- **actions**: Add shell
- **workflows**: Use internal checkout action
- **actions**: Remove shell
- Using actions/checkout
- **actions/deploy-docs**: Sync with gh-pages
- **actions/deploy-docs**: Sync deploy-docs
- **workflows/deploy-docs**: Fetch from gh-pages branch
- **workflows**: Add guard in case branch doesnt exists
- **mkdocs**: Default versions is latest
- **pyproject**: Poe tasks for mkdocs mike plugin
- **mkdocs**: Add mike config and js for versioned documentation
- **docs**: Versions.json created to mike versioned docs
- **scripts**: Integrate with mike
- **actions**: Deploying versioned documentations
- **workflows**: Release.yml also deploy docs
- **docs**: Correct version string in versions.json
- **scripts**: Add redirect template generator
- **docs**: Add custom redirect template for mike set-default
- **mkdocs**: Configure mike redirect alias type and template
- **docs**: Regenerate redirect template with __md_scope and preconnect
- **mkdocs**: Remove auto-generated API Reference nav section
- **scripts**: Update mike usage
- **workflows**: Add new line
- **pyproject**: Sync ci:simulate

## [0.4.1] - 2026-06-10

### Features

- **foundation**: Remove ResultMapper
- **foundation**: Result now mimics Rust's Result partially
- **foundation**: Implement auto-freeze mechanism for ValueObject
- **foundation**: Add SupportsAutoFreeze protocol for auto-freeze compatible classes
- **foundation**: Implement @auto_freeze decorator with _AutoFreezeDecorator class
- **foundation**: Export ValueObject from foundation top-level namespace
- **foundation**: Add demo script proving ValueObject subclasses need zero freeze code

- **docs**: Versioned documentation with mike — each release gets its own immutable docs snapshot, `dev` updates on every push to main, version selector in nav
- **ci**: Release pipeline deploys versioned docs after PyPI publish

### Bug Fixes

- **domain**: Add __slots__ and call super().__init__() in AggregateVersion
- **foundation**: Add __slots__ and call super().__init__() in Message classes
- **foundation**: Add missing overload and type-ignore for pyright strict mode

### Refactor

- **foundation**: Modernize Err
- **foundation**: Modernize Ok
- **foundation**: Split base.py into dedicated error modules
- **tests**: Remove explicit _freeze() calls from value object tests
- **release**: Remove explicit _freeze() calls - auto-freeze now handles it
- **foundation**: Migrate ValueObject to use @auto_freeze decorator
- **script**: Adjust regex and default params
- Simplify autodoc pages generator
- **scripts**: Add ensure_autodoc_index call

### Documentation

- Improve details in docstring of Result protocol
- Detailed docstrings for Ok implementation
- Detailed docstrings for Err implementation
- **foundation**: Expand reference with new abstractions and APIs
- **domain**: Note that ValueObject is implemented in foundation
- **foundation**: Sync core concepts table with current foundation API
- **foundation**: Refresh foundation examples in blocks structure guide
- **foundation**: Add ValueObject and Result fallback examples to getting started
- **foundation**: Add ValueObject and structured error examples
- **foundation**: Remove manual _freeze() call from getting-started ValueObject example
- **foundation**: Remove manual _freeze() call from ValueObject example
- **foundation**: Add Auto-freeze subsection to foundation reference
- **theme**: Adjusting css for auto-generated docs
- **foundation**: Convert SupportsAutoFreeze example from doctest to fenced code block
- **messages**: Convert Command example from doctest to fenced code block
- **messages**: Convert MessageMetadata example from doctest to fenced code block
- **messages**: Convert Query example from doctest to fenced code block
- **result**: Convert quick-start doctest to fenced code block with annotations
- **foundation**: Convert ValueObject example from doctest to fenced code block
- Update changelog, contributing and release guides for versioned docs
- Update version URLs in release guide
- Add detailed API Reference navigation structure to mkdocs.yml
- Clarify --dry-run behavior in deploy script
- **mkdocs**: Adjusting mkdocs.yml

- Add versioned documentation management commands and updated release guide

### Testing

- **foundation**: Add comprehensive unit tests for @auto_freeze decorator
- **foundation**: Update ValueObject tests for @auto_freeze migration
- **scripts**: Correct type

### Continuous Integration

- **deploy-docs**: Switch from mkdocs to mike for versioned dev docs
- **release**: Add versioned docs deployment job to release pipeline
- Add concurrency group to docs-deploy jobs

### Miscellaneous Tasks

- **pyproject**: Switch from mypy to pyright
- Pyright using pyright now
- **project**: Move Protocol exclusion from exclude_lines to exclude_also in coverage config
- **project**: Remove demo_auto_freeze.py exercise script
- **scripts**: Add deploy_versioned_docs.sh helper for mike
- **build**: Add mike versioned docs poe tasks
- **pyproject**: Modify addopts rules of pytest
- **scripts**: Tweaking import
- Set fetch-depth to 0 in workflows for full history fetching

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
