## [0.6.0] - 2026-10-09

### Features

- **ports**: Add PortLevel depth ordering base
- **ports**: Add level relation and comparator
- **ports**: Expose referenced ports from detector
- **ports**: Enforce inward-only port dependencies
- **autofreeze**: Enforce deletion immutability

### Bug Fixes

- **autofreeze**: Preserve private decorator import boundary
- **autofreeze**: Preserve domain mutator policies
- **messages**: Preserve internal protocol type boundary
- **release**: Reject malformed release versions
- **release**: Reject malformed release versions
- **release**: Validate artifact context and exports
- **api**: Export Debuggable from foundation facade
- **api**: Export TransactionError from application facade
- **api**: Export inbound ports from ports facade
- **api**: Declare root public manifest
- **release**: Align artifact export manifest
- **api**: Freeze public facade exports
- **release**: Reject skipped workflow evidence
- **release**: Reject skipped workflow evidence
- **application**: Define UnitOfWork failure contract
- **domain**: Separate state and publication events
- **infrastructure**: Persist only state events
- **infrastructure**: Roll back failed event publication
- **domain**: Define aggregate event lifecycle
- **ci**: Gate PR preview steps by event
- **ci**: Remove PR preview path detection

### Refactor

- **foundation**: Extract helpers from validate_no_runtime_final_override
- **foundation**: Extract dataclass and class resolution helpers in FieldResolver
- **foundation**: Extract sequence set and dict converters in HashableConverter
- **foundation**: Extract field resolution helpers in auto_hash
- **foundation**: Extract type collection helpers in PortReferenceDetector
- **domain**: Extract type and bound validation helpers in RangeValidator
- **domain**: Extract id modification guard helpers in Entity
- **domain**: Extract message dataclass wrapping and patching helpers
- **presentation**: Extract composite error handling in ErrorPresenter
- **presentation**: Extract request execution and error handling helpers in PresentationAdapter
- **autofreeze**: Extract frozen state config
- **autofreeze**: Rename frozen state manager
- **autofreeze**: Extract state constants
- **autofreeze**: Extract decorator implementation
- **messages**: Internalize patched message protocol

### Documentation

- **autofreeze**: Document deletion protection
- **test**: Document separate coverage gates
- **api**: Document root and nested facades
- **api**: Record frozen facade additions
- **api**: Wrap stability policy prose
- **api**: Clarify export manifest versioning
- Fix clean architecture example
- Align CQRS examples
- Align event-driven lifecycle
- Remove example suppressions
- Clarify layered example
- Update contribution commands
- Sync release workflow
- Sync usage examples
- Sync getting started
- Sync library structure
- Repair testing guide
- Update documentation index
- Sync application reference
- Sync application ports
- Sync use case reference
- Sync aggregate reference
- Sync entity reference
- Sync message reference
- Sync permission reference
- Sync foundation reference
- Sync identified reference
- Sync mapper reference
- Sync metadata reference
- Sync foundation ports
- Sync result reference
- Update reference index
- Sync infrastructure reference
- Sync adapter reference
- Sync messaging reference
- Sync persistence reference
- Sync presentation adapters
- Sync error handling reference
- Format dependency summary
- Separate dependency summary
- Format dependency rules
- Document read repository adapter

### Testing

- Use different PortLevel leafs to exercise super class
- **domain**: Test id assignment during entity construction before freeze
- **autofreeze**: Colocate state manager tests
- **autofreeze**: Cover custom mutation delegation
- **messages**: Mirror decorator test structure
- **autofreeze**: Cover custom deletion delegation
- **autofreeze**: Cover custom assignment delegation
- **autofreeze**: Add helper test package marker
- **entity**: Cover identity deletion error metadata
- **entity**: Cover identity modification error metadata
- **entity**: Organize identity behavior coverage
- **entity**: Cover draft lifecycle behavior
- **value-object**: Cover deletion and marker tampering
- **entity**: Keep identity tests in TestEntity
- **entity**: Move lifecycle fixture into test class
- **entity**: Isolate equality and hashing coverage
- **entity**: Isolate representation and copy coverage
- **entity**: Extract shared User fixture
- **entity**: Reuse shared User fixture in equality tests
- **entity**: Reuse shared User fixture in representation tests
- **entity**: Reuse shared fixtures in lifecycle tests
- **entity**: Add shared fixture package
- **entity**: Extract shared Order fixture
- **entity**: Extract User implementation fixture
- **entity**: Clarify order lifecycle coverage
- **autofreeze**: Correct custom setter annotation
- **autofreeze**: Complete Issue 327 immutability coverage
- **package**: Reject published console entry points
- **api**: Cover public facade exports
- **release**: Assert remote validator exit status
- **release**: Preserve colored output assertions
- **infrastructure**: Cover event persistence boundaries
- **infrastructure**: Cover failed publication cleanup
- **infrastructure**: Assert failed commit behavior

### Continuous Integration

- **test**: Enforce package-only coverage gate
- **release**: Verify built artifacts outside checkout
- **release**: Verify built artifacts outside checkout

### Miscellaneous Tasks

- Add forging-blocks route to homepage url

## [0.5.0] - 2026-08-06

### Features

- **presentation**: Add PresenterPort protocol contract
- **presentation**: Add ErrorMessageModel
- **presentation**: Add ErrorPresenter
- **presentation**: Add ErrorViewModel
- **presentation**: Add presentation package __init__
- **presentation**: Add NextHandler type alias
- **presentation**: Add Middleware protocol
- **presentation**: Add Pipeline class
- **presentation**: Add status_code field to ErrorMessageModel
- **presentation**: Add RequestAdapter protocol
- **presentation**: Add ResponseAdapter protocol
- **presentation**: Add ErrorStatusCodeMapper
- **presentation**: Add PresentationAdapter orchestrator
- **presentation**: Export new adapter classes and protocols
- **foundation**: Add context types for service, authorization, and transaction
- **foundation**: Add IsolationLevel and Permission enums
- **foundation**: Add ValidationRule in rules module and re-export from foundation
- **domain**: Add validators — Required, Email, and Length
- **domain**: Add RangeValidator and CompositeValidationRule
- **domain**: Add permission checker protocol, role and resource implementations
- **domain**: Add CompositePermissionChecker and re-export from domain
- **application**: Add ApplicationService, ValidationService, and AuthorizationService ports
- **application**: Add TransactionManagerPort outbound port
- **application**: Add TransactionError
- **foundation**: Add auto_hash decorator for hashability
- **foundation**: Extract auto_hash helper and add NonHashableValueError
- **presentation**: Add ValidationMiddleware for request validation
- **presentation**: Add ErrorHandlingMiddleware for exception-to-response mapping
- **presentation**: Register ValidationMiddleware and ErrorHandlingMiddleware in builtin exports
- **presentation**: Export new builtin middlewares from presentation package
- **logger**: Make LoggerPort methods use concrete *args: str
- **foundation**: Add ArchitectureWarning via __init_subclass__ on InboundPort and OutboundPort
- **foundation**: Add ArchitectureError for dependency direction violations
- **foundation**: Add __init_subclass__ enforcement for port dependency rules
- **foundation**: Add ConfigurationError to public API
- Add reconstitute classmethod to AggregateRoot
- **scripts**: Add docstring import validation to autodoc generator
- **presentation**: Remove unused LoggerPort import from middleware docstrings
- **tests**: Add SimpleFakeQuery fixture for Query dispatch paths
- **application**: Add generic payload type params to ValidationPort
- **foundation**: Add ValueErrorMixin for catching errors as ValueError
- **foundation**: Add RuntimeErrorMixin for catching errors as RuntimeError
- **foundation**: Add mixins subpackage init with namespace exports
- **errors**: Export ValueErrorMixin and RuntimeErrorMixin from builtin/
- **errors**: Add ValueErrorMixin to ValidationError base
- **errors**: Add RuntimeErrorMixin to RuleViolationError base
- **errors**: Add ValueErrorMixin to ValidationFieldErrors
- **errors**: Add ValueErrorMixin to CombinedValidationErrors
- **errors**: Add RuntimeErrorMixin to CombinedRuleViolationErrors
- **errors**: Add ValueErrorMixin to NoneNotAllowedError
- **errors**: Add ValueErrorMixin to NonHashableValueError
- **errors**: Add ValueErrorMixin to NotCallablePredicateError
- **errors**: Add ValueErrorMixin to ConfigurationError
- **errors**: Add RuntimeErrorMixin to ArchitectureError
- **errors**: Add RuntimeErrorMixin to CantModifyImmutableAttributeError
- **errors**: Add RuntimeErrorMixin to ResultAccessError
- **errors**: Add RuntimeErrorMixin and fix Error[str] type in DraftEntityIsNotHashableError
- **errors**: Add RuntimeErrorMixin to EntityIdDeletionError
- **errors**: Add RuntimeErrorMixin to EntityIdModificationError
- **errors**: Add RuntimeErrorMixin to EventBusError
- **errors**: Add RuntimeErrorMixin to EventStoreError
- **errors**: Add RuntimeErrorMixin to TransactionError
- **errors**: Add RuntimeErrorMixin to UnitOfWorkError
- **errors**: Add RuntimeErrorMixin to RepositoryError
- **foundation**: Add Error.from_string factory for string-based errors

### Bug Fixes

- **docs**: Handle nested nav structure in autodoc generator regex
- **docs**: Update broken anchors after reference restructuring
- **presentation**: Re-raise original error instead of wrapping in RuntimeError
- **ci**: Prevent gh-pages race conditions across workflows
- **ci**: Guarantee PR preview cleanup on close regardless of docs state
- **ci**: Remove unused GIT_COMMITTER_* env vars and misleading description from configure-git action
- **infrastructure**: Replace EventPayloadType with Any in AggregateRoot bound
- **infrastructure**: Add cast bridge for EventPayloadType in AggregateRepository
- **infrastructure**: Reorder save to write event store before snapshot
- **infrastructure**: Propagate event store errors in get_by_id
- **foundation**: Remove redundant frozen=True from context dataclasses
- **presentation**: Make Result unwrapping opt-in, split error handling
- **presentation**: Add __slots__, make status map class constant
- **presentation**: Export NextHandler, document PII in logging
- **foundation**: Apply auto_hash to context types for hashability
- **presentation**: Use tuple for ErrorViewModel.messages
- **foundation**: Restore Mapper re-export from top-level package
- **foundation**: Harden HashableConverter and fix docs
- **autofreeze**: Use id()-keyed fallback dicts with weakref GC cleanup
- **autohash**: Handle single-string __slots__ and soften immutability docstring
- **autohash**: Use frozenset for dict key-value pair conversion
- **autohash**: Apply meta-review fixes — docstring consistency, test coverage, wraps robustness
- **presentation**: Convert ErrorViewModel messages to tuple after auto-hash merge
- **presentation**: Add %s placeholder to ErrorHandlingMiddleware log call
- **callers**: Update implementations and tests for generic port signatures
- **middleware**: Pass concrete values to LoggerPort *args: str
- **docs**: Deploy dev before serve so local docs reflect working tree
- **application**: Complete __all__ exports and update module docstring
- **infrastructure**: Add Serializable to __all__ and update docstring
- **ci**: Remove self-referencing trigger from docs change detection
- **ci**: Address review feedback on Semgrep SAST workflow
- **infrastructure**: Remove inbound port imports from InMemoryEventBus
- **infrastructure**: Remove inbound port imports from InMemoryEventBusBase
- **foundation**: Add __init_subclass__ to Port to fix Protocol structural contract
- **infrastructure**: Add URL scheme validation to prevent SSRF (CodeQL #7)
- **infrastructure**: Use ConfigurationError in URLLibClient instead of ValueError
- **release**: Remove generic params from release outbound ports, fix handler type
- **infrastructure**: Replace urlopen with http.client to prevent SSRF
- **test**: Restrict TLS to v1.2+ in https_echo_server fixture
- **docs**: Clean stale autodoc pages before regeneration
- **infrastructure**: Tighten DictMessageCodec type constraint and fix created_at fallback
- **infrastructure**: Remove unnecessary cast after type constraint tightening
- **infrastructure**: Cache reconstituted aggregates after event replay
- **foundation**: Remove duplicate Args block and dead frozen param from docstring
- **infrastructure**: Remove collect_events call from AggregateRepository.save
- **infrastructure**: Raise descriptive errors for missing metadata keys in DictMessageCodec
- **foundation**: Guard against unknown fields in from_payload_fields
- **foundation**: Replace misleading or-pattern with explicit None checks
- **autohash**: Add missing return statement, close docstring, replace em-dashes
- **messages**: Apply auto_hash/auto_eq unconditionally in Message.__init_subclass__
- **scripts**: Dedent code blocks when validating docstring imports
- **domain**: Lazify aggregate_root import to break circular dependency
- **auto-eq, auto-hash**: Use type.__setattr__ for attribute assignment on ABCMeta classes
- **aggregate-repository**: Use UUID | None instead of unbounded TId
- **foundation**: Prevent FieldErrors iterator exhaustion on has_errors check
- **infrastructure**: Consolidate InMemoryRepository diamond init storage assignment
- **foundation**: Add auto_freeze to foundation package exports and __all__
- **foundation**: Remove dead OkType TypeVar from Ok result variant
- **foundation**: Remove dead ErrType TypeVar from Err result variant
- **infrastructure**: Wrap mkdir call in asyncio.to_thread for async consistency
- **foundation**: Tighten FieldErrors truthiness guard and use RuleViolationError
- **foundation**: Use field.value in FieldErrors message, not FieldReference repr
- **application**: Bound MetadataType on Mapping[str, object] in event_bus_error
- **application**: Bound MetadataType on Mapping[str, object] in unit_of_work_error
- **foundation**: Bound MetadataType on Mapping[str, object] in result_access_error
- **foundation**: Bound MetadataType on Mapping[str, object] in non_hashable_value_error
- **foundation**: Correct Raises docstring to say RuleViolatedError
- **scripts**: Extend RuleViolatedError not abstract RuleViolationError
- **scripts**: Extend RuleViolatedError not abstract RuleViolationError
- **scripts**: Extend ValidationFailedError not abstract ValidationError
- **scripts**: Extend ValidationFailedError not abstract ValidationError
- **scripts**: Extend ValidationFailedError not abstract ValidationError
- **scripts**: Extend ValidationFailedError, use ErrorMetadata[str]
- **scripts**: Extend ValidationFailedError not abstract ValidationError
- **scripts**: Use Error[str] instead of Error[dict[str,object]]
- **foundation**: Add runtime guard to prevent direct instantiation of RuleViolationError
- **foundation**: Add runtime guard to prevent direct instantiation of ValidationError
- **auto_hash**: Traverse MRO for __annotations__ when resolving hash fields
- **auto_eq**: Traverse MRO for __annotations__ when resolving eq fields
- **pre-commit**: Block only generated autodoc nav in mkdocs.yml
- **domain**: Make error metadata annotations generic
- **foundation**: Make error types generic and fix docstrings
- **autohash**: Make autohash/autoeq helpers generic and fix docstrings
- **infrastructure**: Fix adapter and app error annotations and docstrings
- Export NotCallablePredicateError
- **docs**: Correct broken Example code across all layers
- **docs**: Add missing ```python fences to 8 Example sections
- **docs**: Correct type signatures in result.py and message_handler_port.py Example sections
- **foundation**: Correct auto_eq docstring example field name
- **foundation**: Fix is_ok() to is_ok property in Result example
- **infrastructure**: Fix RepositoryError docstring example attribute
- **infrastructure**: Fix DictMessageCodec example signature in docstring
- **presentation**: Fix ErrorPresenter example to reference real error

### Refactor

- **presentation**: Use auto_freeze instead of dataclass frozen=True
- **ci**: Deduplicate git config into reusable configure-git action
- **ports**: Convert ports from ABC to Protocol
- **infra**: Extract typed event bus and event store with base classes
- **infrastructure**: Rename abstract/abc classes to Base suffix
- **infrastructure**: Merge duplicate AggregateRepository files
- **infrastructure**: Add EventPayloadType generic to AggregateRepository
- **presentation**: Reorganize src into topic-based subdirectories
- **foundation**: Extract auto_freeze helpers into internal subpackage
- **foundation**: Rewrite auto_freeze and auto_hash to use extracted helpers
- **foundation**: Remove redundant @auto_freeze from context types
- **presentation**: Replace @auto_freeze with @auto_hash on presentation types
- **context**: Convert context types to ValueObject subclasses
- **foundation**: Remove SQL-specific IsolationLevel enum
- **context**: Replace Any with Hashable in metadata types
- **context**: Default collection fields to empty tuples
- **presentation**: Importing from error sub module
- **ports**: Replace object with generic type parameters on port contracts
- **foundation**: Split ports module into ports/ package
- **application**: Rename inbound ports to match file convention
- **application**: Add OutboundPort/ABC bases to outbound ports
- **application**: Update outbound __init__ exports
- **application**: Update application __init__ and inbound exports
- **presentation**: Update adapter port references for renamed ports
- **scripts**: Update release scripts port references
- **foundation**: Restructure Port hierarchy — drop generic params, enforce runtime-final init_subclass
- **presentation**: Remove generics from PresenterPort, inline subclasshook
- **application**: Remove generic params from inbound ports, expand docstrings
- **application**: Remove generic params from outbound ports, expand docstrings
- **application**: Merge UseCasePort into ApplicationServicePort as type alias
- **coverage**: Remove Protocol coverage exclusions and empty specs re-export
- **application**: Replace object concretions with PEP 695 generics in event bus ports
- **ports**: Restructure repository_port.py into subdirectory package
- **repos**: Rename base_repository to InMemoryRepository classes
- **repos**: Update infrastructure __init__.py exports for rename
- **serialization**: Use generic param for Serializable dict value type
- **infrastructure**: Narrow MutableMapping to Mapping in InMemoryWriteRepository
- **infrastructure**: Narrow MutableMapping to Mapping in InMemoryRepository
- **infrastructure**: Replace type ignore with cast(TId, ...) in InMemoryWriteRepository
- Restructure Message into message/ subpackage with abstract from_payload_fields
- Replace Serializable with MessageCodec/DictMessageCodec in infrastructure
- Rename _from_payload_fields to from_payload_fields across tests and scripts
- **infrastructure**: Promote encode/decode to public abstract methods
- **infrastructure**: Use ABC base class instead of FinalABCMeta metaclass
- **value-object**: Replace _equality_components with @auto_hash
- **message**: Break Message from ValueObject inheritance
- **subclass-vos**: Remove _equality_components from all ValueObject subclasses
- **autohash**: Decouple auto_hash from auto_freeze, apply independently in ValueObject
- **autohash**: Split __eq__ out of auto_hash into standalone auto_eq
- **foundation**: Integrate auto_eq, replace type: ignore with cast()
- **domain**: Move ValueObject, Messages, and Specifications from foundation to domain
- **domain**: Update source imports from foundation to domain modules
- **domain**: Update test imports from foundation to domain modules
- **domain**: Update script imports from foundation to domain modules
- **domain**: Keep TYPE_CHECKING + __getattr__ for circular import safety
- **foundation**: Remove concrete context value objects
- **domain**: Remove concrete permission checker implementations
- Generify permission and port interfaces with domain type parameters
- **infrastructure**: Remove unnecessary lambda in OSFileSystem
- **foundation**: Extract abstract error bases into base/ subpackage
- **foundation**: Extract combined error classes into combined/ subpackage
- **foundation**: Remove old flat error files after subpackage migration
- **foundation**: Update error re-exports to use new subpackage paths
- **foundation**: Update leaf error imports to use base/ subpackage
- **domain**: Migrate validators to concrete RuleViolated and ValidationFailed
- **domain**: Update domain error imports to new base/ path
- **application**: Update application error imports to base/ path
- Update infrastructure and presentation error imports
- Update remaining stale imports after error subpackage migration
- **foundation**: Rename RuleViolated → RuleViolatedError, ValidationFailed → ValidationFailedError
- **auto_hash**: Replace @staticmethod with @classmethod on _collect_annotations
- **auto_eq**: Replace @staticmethod with @classmethod on _collect_annotations
- **domain**: Replace type ignore with cast in Entity.__eq__
- **repos**: Rename id parameter to entity_id to avoid builtin shadowing
- **presentation**: Convert isinstance to match/case in error_presenter

### Documentation

- Add reference docs for new presentation adapter classes
- Enrich infrastructure and presentation reference docs
- Restructure reference docs with overviews and sub-docs
- Apply review fixes to reference docs
- Restore "what it does not do" sections to all overviews
- Flesh out domain errors with concrete types and expand domain sub-pages
- **foundation**: Split into overview and 10 sub-docs
- **foundation**: Clarify auto-freeze vs ValueObject trade-offs
- Break up crowded lines into clear paragraphs and bullets
- Focus when-to-use sections on library features, not modeling advice
- Add when-to-use guidance to all sub-docs
- Fix inaccuracies flagged in PR review
- **infrastructure**: Deduplicate serialization description
- **presentation**: Adjust docstring
- **domain**: Add permissions and validators reference pages
- **foundation**: Add context and rules reference pages
- **foundation**: Fix broken relative link to domain validators page
- **infrastructure**: Document cross-TypeVar bound limitation in AggregateRepository
- **middleware**: Add Example blocks to class docstrings
- **reference**: Document built-in middleware and adapter contracts
- Set dev as default version for local docs serving
- **middleware**: Fix Example block rendering to avoid mkdocs link warnings
- **middleware**: Fix autodoc link warning in Middleware base class
- **middleware**: Use fenced code blocks in Example sections
- **guide**: Merge reference content, remove volatile test metrics
- **reference**: Delete testing.md — merged into guide
- **reference**: Remove testing link from reference index
- **reference**: Add API stability policy page
- **application**: Fix stale type references in README
- **infrastructure**: Fix stale type references in EventBusBase docstring
- Update docs and test fixtures for port renames
- **application**: Remove comment lines from README code blocks
- **ports**: Update foundation and application port docs to match current source
- Rename UseCasePort to ApplicationServicePort across docs
- **ports**: Document required generic type params with inheritance examples
- **guide**: Fix code examples — await/async def, Port→Protocol, ValueObject conventions
- **domain**: Remove stale "deleted" lifecycle claim from entities reference
- **application**: Remove empty Notes section from list_all docstring
- **reference**: Correct Port classification from Protocol to ABC
- **cqrs**: Update repository references to use Port suffix
- **application**: Update README to reflect actual directory structure
- **infrastructure**: Update repository references to use Port suffix
- **application**: Fix ApplicationServicePort self-reference alias
- **outbound**: Replace stale protocol language in CachePort docstring
- **outbound**: Replace stale protocol language in docstring
- **outbound**: Replace stale protocol language in docstring
- **outbound**: Replace stale protocol language in docstring
- **outbound**: Replace stale protocol language in docstring
- **outbound**: Replace stale protocol language in docstring
- **outbound**: Replace stale protocol language in docstring
- **copilot**: Rewrite Port hierarchy to ABC-based convention
- **copilot**: Fix three more stale Protocol references
- **guide**: Fix parse_reciprocal to use flat_map and rename data->request in CreateTaskService
- Fix stale Base Repository heading and method names in persistence.md
- **guide**: Use OutboundPort in examples.md port/adapter example
- **guide**: Use OutboundPort in testing.md port example
- **application**: Fix list_all docstring — use sequence terminology instead of list-like
- **application**: Fix directory tree — repository_port.py → repository_port/
- Update reference docs for message and serialization API changes
- Document ABC interaction in message_dataclass decorator
- **foundation**: Fix MessageMetadata class docstring and _payload docs
- **foundation**: Clarify that MessageMetadata.created_at preserves input as-is
- **foundation**: Include Query subtype in Message base class docstring
- Remove _equality_components references after ValueObject refactor
- Remove remaining _equality_components references from copilot instructions and test names
- **autohash**: Standardize docstrings to match auto_freeze style
- **autoeq**: Standardize docstrings to match auto_freeze style
- **guide**: Replace RST :func: roles with backtick code spans
- **guide**: Replace RST :func: roles with backtick code spans
- **reference**: Replace RST :class: role with backtick code span
- **aggregate-root**: Replace RST :meth: role with backtick code span
- **permissions**: Replace RST :class: role with backtick code span
- **permissions**: Replace RST :class: role with backtick code span
- **permissions**: Replace RST :class: role with backtick code span
- **autoeq**: Replace RST :func: roles with backtick code spans
- **autofreeze**: Replace RST :func: role with backtick code span
- **autofreeze**: Replace RST :class:/:attr: roles with backtick code spans
- **autohash**: Replace RST :func: roles with backtick code spans
- **autohash**: Replace RST :func: roles with backtick code spans
- **autohash**: Replace RST :class: roles with backtick code spans
- **errors**: Replace RST :class: role with backtick code span
- **messages**: Replace RST :class: roles with backtick code spans
- **messages**: Replace RST :func:/:class: roles with backtick code spans
- **meta**: Replace RST :func: role with backtick code span
- **value-object**: Replace RST :func: roles with backtick code spans
- **aggregate-repository**: Replace RST :meth: role with backtick code span
- **copilot-instructions**: Replace RST :func: roles with backtick code spans
- **autofreeze**: Remove domain-specific Entity references from docstring
- **reference**: Add auto-generated auto-eq and auto-hash reference pages
- **autofreeze**: Remove unused CantModifyImmutableAttributeError import from docstring example
- **domain**: Update reference pages and fix links for domain module move
- Sync mkdocs nav entries with domain module move
- **foundation**: Create comprehensive auto-decorators reference page
- **foundation**: Remove individual auto decorator reference pages
- Update cross-references to auto-decorators page
- **foundation**: Clean auto-freeze module docstring examples
- **foundation**: Clean auto-eq module docstrings and README
- **foundation**: Clean auto-hash module docstrings and README
- **infrastructure**: Correct exception types in URLLibClient docstring Raises section
- **infrastructure**: Fix urllib_client docstrings for http.client migration
- **infra**: Add naming-backwards-compat note to URLLibClient docstring
- **infra**: Qualify HTTPException as http.client.HTTPException in docstrings
- Reflect generic type params on ValidationPort
- **guide**: Describe forging-blocks internal structure instead of prescribing user organization
- **guide**: Use descriptive language in architecture overview
- **arch-styles**: Add ForgingBlocks-in-practice code examples to style pages
- **arch-styles**: Add MVC architectural style page with index entry
- **nav**: Add MVC to architectural styles navigation
- **reference**: Add teachable intro paragraphs to reference pages
- Correct block attributions for Messages, Specification, and ValueObject
- **ports**: Remove implementation guidance from port docstrings
- **repositories**: Remove CQRS and implementation framing from repository docstrings
- **reference**: Add built-in taxonomy section to foundation errors page
- **reference**: Document RuntimeErrorMixin for domain errors
- **reference**: Document RuntimeErrorMixin for application errors
- **reference**: Create infrastructure errors reference page
- **reference**: Link infrastructure errors page from overview
- **mkdocs**: Add infrastructure errors to nav
- **errors**: Improve UnitOfWorkError module docstring
- **errors**: Improve TransactionError module docstring
- **errors**: Improve EventStoreError module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **errors**: Improve module docstring
- **release-guide**: Move full content into docs/contributing/
- **contributing**: Move full content into docs/contributing/ with fixed links
- **contributing**: Document single-step hook install
- **domain**: Correct EntityIdNoneError inheritance in errors reference
- **domain**: Enrich EntityIdNoneError class and init docstrings
- **domain**: Enrich EntityIdDeletionError class docstring
- **domain**: Enrich EntityIdModificationError class docstring
- **domain**: Enrich DraftEntityIsNotHashableError class and factory docstrings
- **foundation**: Remove consumer refs from ArchitectureError docstring
- **application**: Enrich ConcurrencyError module and init docstrings
- **infrastructure**: Remove port name from repository errors module docstring
- Remove test mermaid file
- Update reference index with accurate cross-links
- Update foundation reference links and descriptions
- Document combined error types in foundation errors
- Update domain reference with corrected types
- Update domain errors reference
- Add MessageMetadata to domain messages reference
- Update specifications reference
- Update validators reference
- Update application reference
- Add TransactionError to application errors
- Update infrastructure reference
- Update messaging adapter class names
- Fix InMemoryWriteRepository description
- Update presentation reference
- **presentation**: Add mermaid sequence diagram to middleware pipeline
- **reference**: Add Presentation-to-Foundation dependency edge in block diagram
- **guide**: Add missing block dependency edges to diagram (P→F, I→A)
- **domain**: Convert >>> doctest to Example: with fenced code block in ExpressionSpecification
- **presentation**: Convert Usage:: to Example: with fenced code block in Pipeline
- **foundation**: Convert reST Example header to canonical format in Mapper
- **foundation**: Replace Quick start with Example in Result class docstring
- **domain**: Convert Example:: to Example: with fenced code block in decorators.py
- **infra**: Add Example docstrings to error, cache, logging, fs, http classes
- **infra**: Add Example docstrings to event store and event bus classes
- **domain**: Add Example docstrings to validator classes
- **domain**: Add Example docstrings to permission and aggregate classes
- **foundation**: Add Example docstrings to Permission and FinalABCMeta classes
- **presentation**: Replace docstring type ignores with cast in Middleware and PresentationAdapter
- Add autodoc navigation entries for all API modules
- Replace object generic params with named types in Example docstrings
- **autohash**: Replace examples with standalone Point2D and Record
- **foundation**: Add Example sections to abstract class docstrings
- **domain**: Add Example sections to abstract class docstrings
- **ports-inbound**: Add Example sections to inbound port docstrings
- **ports-outbound**: Add Example sections to outbound port docstrings
- **ports-outbound**: Add Example sections to repository port docstrings
- **infrastructure**: Add Example sections to base class docstrings
- **presentation**: Add Example sections to adapter docstrings
- Remove unused imports from docstring code examples
- **foundation**: Inline types in auto_freeze Example docstring
- **foundation**: Inline types in auto_hash Example docstring
- **foundation**: Inline types in auto_eq Example docstring
- **foundation**: Inline imports in Example docstrings across foundation layer
- **domain**: Inline imports in Example docstrings across domain layer
- **ports-inbound**: Inline imports in Example docstrings for inbound ports
- **ports-outbound**: Inline imports in Example docstrings for outbound ports
- **infrastructure**: Inline imports in Example docstrings across infrastructure layer
- **presentation**: Inline imports in Example docstrings across presentation layer
- Inline imports in remaining Example docstrings
- **foundation-errors-core**: Add Example sections to core error classes
- **foundation-errors**: Add Example sections to guard error classes
- **foundation-errors-combined**: Add Example sections to combined/field error classes
- **foundation-result**: Add Example sections to validation errors, result, and meta classes
- **foundation-ports**: Add Example sections to port base classes and helpers
- **foundation-auto**: Add Example sections to auto-eq/freeze/hash helpers
- **domain**: Add Example sections to domain entity, errors, and messages
- **application**: Add Example sections to application errors and ports
- **presentation**: Add Example sections to presentation error models
- **foundation**: Fix orphaned type vars T/E -> ValueType/ErrorType in result.py Example
- **application**: Fix invalid UUID literals in event_store_port.py Example
- **infra**: Fix invalid UUID literals in event_store_base.py Example
- **application**: Add Example blocks to application errors and outbound ports
- **domain**: Add Example blocks to domain errors, messages, and specifications
- **foundation**: Add Example blocks to foundation layer classes
- **infrastructure**: Add Example blocks to infrastructure implementations
- **presentation**: Add Example blocks to presentation layer classes
- **domain**: Add ExpressionSpecification.__init__ to Example stub for self-containment
- **domain**: Add ExpressionSpecification.__init__ to Example stub for self-containment
- **application**: Rename ErrorMessage to Msg in Example stub for self-containment
- **infra**: Add missing Example section header for self-containment
- **application**: Use from_string in TransactionError example
- **application**: Use from_string in UnitOfWorkError example
- **foundation**: Use from_string in RuleViolationError example
- **foundation**: Use from_string in ValidationError example
- **foundation**: Use from_string and FieldReference in FieldErrors example
- **domain**: Add self-contained Example with from_payload_fields to Command
- **domain**: Add self-contained Example with from_payload_fields to Event
- **domain**: Add self-contained Example with from_payload_fields to Query
- **domain**: Add import for self-contained Message example
- **domain**: Flesh out stub class bodies in AndSpecification example
- **domain**: Flesh out stub class bodies in NotSpecification example
- **domain**: Flesh out stub class bodies in OrSpecification example
- **domain**: Add inline event stubs for self-contained AggregateRoot examples
- **foundation**: Add __init_subclass__ stub for self-contained Port example
- **infrastructure**: Add inline port stubs for self-contained AggregateRepository example
- **presentation**: Use ErrorViewModel in ErrorHandlingMiddleware example
- Replace recommended_blocks_structure to library-structure
- **guide**: Rename to library-structure.md and add Foundation naming guard
- Update Blocks Overview link to Library Structure
- **guide**: Update Recommended Blocks Structure link to Library Structure
- **architectural-styles**: Fill empty Important admonition for Layered Architecture
- **guide**: Clarify library block naming conventions are not a template

### Testing

- **presentation**: Add PresenterPort type parameter tests
- **presentation**: Add ErrorViewModel tests
- **presentation**: Add integration tests for PresentationAdapter
- **foundation**: Add tests for IsolationLevel and Permission enums
- **foundation**: Add tests for context objects
- **foundation**: Add tests for ValidationRule
- **domain**: Add test for PermissionChecker protocol
- **domain**: Add tests for RoleBasedPermissionChecker
- **domain**: Add tests for ResourcePermissionChecker and CompositePermissionChecker
- **domain**: Add tests for Required, Email, and Length validators
- **domain**: Add tests for RangeValidator and CompositeValidationRule
- **application**: Add test for TransactionError
- **application**: Add tests for inbound port protocols
- **fixtures**: Add FakeCommandRunner, FakeEventPublisher, and FakeMessageBus
- **message-bus**: Replace MagicMock with FakeMessageBus fixture
- **unit-of-work**: Replace AsyncMock with FakeEventPublisher fixture
- **http-client**: Add local echo server fixture achieving 100% coverage
- **release-bus**: Replace AsyncMock with FakeHandler and FakeCommand fixtures
- **release-infra**: Replace create_autospec with FakeCommandRunner fixture
- **release-handler**: Replace create_autospec with FakeOpenReleasePullRequestUseCase
- **process**: Replace @patch with real subprocess-driven tests
- **e2e**: Replace MagicMock/AsyncMock with FakePullRequestService
- Align tests with typed infrastructure APIs
- **infrastructure**: Add behavior tests for AggregateRepository
- **presentation**: Reorganize tests into topic-based subdirectories
- **presentation**: Strengthen middleware test coverage
- **presentation**: Add shared builtin test doubles
- **foundation**: Add tests for helper extraction, freeze composition, and edge cases
- **context**: Update tests for ValueObject-based context types
- **presentation**: Cover request-adapter failure and non-exception Result.Err propagation paths
- **presentation**: Add tests for ValidationMiddleware
- **presentation**: Add tests for ErrorHandlingMiddleware
- **file-system**: Fix read signature assertion for generic ContentType return
- **middleware**: Adapt assertions for *args: str contract
- **revert**: Adapt test expectations for concrete port types
- **foundation**: Cover FrozenStateManager stale fallback entry cleanup
- **foundation**: Cover HashableConverter frozenset branch
- **foundation**: Cover message_dataclass TypeError on _PatchedMessage check
- **infrastructure**: Cover InMemoryEventBus send handler exception path
- **infrastructure**: Cover InMemoryEventBusBase publish/send handler exception paths
- **infrastructure**: Cover AggregateRepository event store error paths
- **infrastructure**: Cover InMemoryUnitOfWork context manager and None id guard
- **foundation**: Remove comments from auto_freeze tests
- **foundation**: Remove comments from auto_hash tests
- **infrastructure**: Change unit → integration marker in test_in_memory_cache
- **infrastructure**: Change unit → integration marker in test_repository_errors
- **infrastructure**: Change unit → integration marker in test_in_memory_event_bus
- **infrastructure**: Change unit → integration marker in test_in_memory_event_store
- **infrastructure**: Change unit → integration marker in test_in_memory_message_bus
- **infrastructure**: Change unit → integration marker in test_aggregate_repository
- **infrastructure**: Change unit → integration marker in test_in_memory_read_repository
- **infrastructure**: Change unit → integration marker in test_in_memory_write_repository
- **infrastructure**: Replace patch.object with draft_aggregate fixture in UoW test
- **inbound**: Update tests for renamed inbound port classes
- **outbound**: Use concrete fixtures over MagicMock, add http_client tests
- **infrastructure**: Update tests for port renames and new port contracts
- Update port tests for restructured hierarchy
- **init**: Add unit tests for package version resolution
- **urllib_client**: Replace mock-based HTTPS test with real fixture
- Rename test_base_repository.py to test_in_memory_repository.py
- Reorganize message tests into decorators, metadata, and serialization modules
- **foundation**: Add regression tests for message equality and hashing
- **equality**: Update tests after ValueObject/Message refactor
- Remove type: ignore, use cast() for strict pyright compliance
- Add FieldResolver, DictMessageCodec, and domain init coverage tests
- **field-resolver**: Add coverage for string-form __slots__ conversion
- **decorators**: Add coverage for from_payload_fields, get_payload_fields, and frozen enforcement
- **infrastructure**: Add missing assertion after message bus query dispatch
- **foundation**: Update FieldErrors tests for RuleViolationError
- **foundation**: Use Error instance not raw ErrorMessage in FieldErrors null-field test
- Update test imports to match error subpackage reorganization
- **presentation**: Use Error[object] instead of Error[dict[str,object]]
- **application**: Update ValidationPort tests for generic payload params
- **errors**: Add builtin/ test package init
- **errors**: Add ValueErrorMixin taxonomy tests
- **errors**: Add RuntimeErrorMixin taxonomy tests
- **test_rule_violation_error**: Add RuntimeError mixin catchability assertion
- **test_validation_error**: Add ValueError mixin catchability assertion
- **test_combined_rule_violation_errors**: Add behavioral tests for iteration, catchability, and string representation
- **test_validation_field_errors**: Add behavioral tests for field storage, iteration, guards, and catchability
- **test_combined_validation_errors**: Add behavioral tests for aggregation, iteration, and catchability
- **autoeq**: Add MRO and slots tests; update autohash test types
- **foundation**: Add test for from_string method

### Miscellaneous Tasks

- Stop tracking autodoc generated files
- **application**: Add dtos package init
- **scripts**: Exclude helpers directories from autodoc generation
- **mkdocs**: Add key pages that were missing
- **mkdocs**: Remove old refenrece testing page
- **mkdocs**: Add api-stability new page
- **docs**: Remove stale v0.4.1 from versions.json
- **ci**: Remove emojis from static analysis workflow output
- **ci**: Trigger static analysis workflow re-run
- **pyright**: Exclude scripts/ from type checking
- **pyright**: Exclude tests directory from type checking
- **mkdocs**: Replace auto freeze to auto decorators
- Pin debug-statements hook to Python 3.14 for PEP 695 syntax
- Fix stale error imports in scripts and .github after subpackage migration
- **errors**: Split core.py into core/ subpackage
- **errors**: Move concrete errors into parent-named subpackages
- Remove .github/copilot-instructions.md
- **errors**: Rename builtin/ __init__.py from mixins/ directory
- **errors**: Rename RuntimeErrorMixin file from mixins/ to builtin/
- **errors**: Rename ValueErrorMixin file from mixins/ to builtin/
- **readme**: Condense to pitch with docs links
- **release-guide**: Condense to concise stub with docs link
- **contributing**: Condense to concise stub with docs links
- **pre-commit**: Install pre-commit and pre-push by default
- **pre-commit**: Rename ruff hook to ruff-check
- **docs**: Fix broken link in contributing.md
- **scripts**: Group autodocs nav section
- Site_url points to forging-blocks route
- Remove autodoc nav entries from mkdocs.yml
- **docs**: Add background-color to sidebar header

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
