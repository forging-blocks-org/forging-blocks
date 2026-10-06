#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/pipeline/commons.sh
source "$SCRIPT_DIR/commons.sh"

log "Building package"
rm -rf dist
poetry build

log "Installing Twine"
python -m pip install --quiet twine

shopt -s nullglob
wheel_files=(dist/*.whl)
sdist_files=(dist/*.tar.gz)
[[ "${#wheel_files[@]}" -eq 1 ]] || fail "Expected exactly one wheel artifact"
[[ "${#sdist_files[@]}" -eq 1 ]] || fail "Expected exactly one source artifact"

log "Validating artifact metadata"
twine check "${wheel_files[0]}" "${sdist_files[0]}"

validation_dir="$(mktemp -d)"
trap 'rm -rf "$validation_dir"' EXIT

validate_installed_artifact() {
  local artifact="$1"
  local target_dir="$2"
  local expected_version
  expected_version="$(poetry version -s)"
  python -m pip install --quiet --no-deps --target "$target_dir" "$artifact"
  (
    cd "$validation_dir"
    EXPECTED_VERSION="$expected_version" PYTHONPATH="$target_dir" python - <<'PY'
import importlib
import os
from importlib.metadata import Distribution, distribution
from types import ModuleType
from typing import cast

expected_version: str = os.environ["EXPECTED_VERSION"]
package: Distribution = distribution("forging-blocks")
if package.version != expected_version:
    raise SystemExit(f"Artifact version mismatch: {package.version} != {expected_version}")
if package.metadata["Requires-Python"] != ">=3.14":
    raise SystemExit("Artifact Requires-Python metadata is incorrect")
if package.requires:
    raise SystemExit(f"Unexpected runtime dependencies: {package.requires}")
if list(package.entry_points):
    raise SystemExit("Unexpected console entry points found")

package_module: ModuleType = importlib.import_module("forging_blocks")
if package_module.__version__ != expected_version:
    raise SystemExit("Package __version__ does not match artifact metadata")

expected_exports: dict[str, tuple[str, ...]] = {
    "forging_blocks.foundation": (
        "auto_eq",
        "auto_freeze",
        "auto_hash",
        "ArchitectureError",
        "ConfigurationError",
        "CombinedErrors",
        "CombinedRuleViolationErrors",
        "CombinedValidationErrors",
        "CantModifyImmutableAttributeError",
        "Err",
        "Error",
        "ErrorMessage",
        "ErrorMetadata",
        "FieldErrors",
        "FieldReference",
        "FinalABCMeta",
        "FinalMeta",
        "Identified",
        "InboundPort",
        "Mapper",
        "NoneNotAllowedError",
        "Ok",
        "OutboundPort",
        "Permission",
        "Port",
        "Result",
        "ResultAccessError",
        "RuleViolatedError",
        "RuleViolationError",
        "runtime_final",
        "ValidationError",
        "ValidationFailedError",
        "ValidationFieldErrors",
        "ValidationRule",
    ),
    "forging_blocks.domain": (
        "AggregateRoot",
        "AggregateVersion",
        "AndSpecification",
        "Command",
        "CompositePermissionChecker",
        "CompositeValidationRule",
        "DraftEntityIsNotHashableError",
        "EmailValidator",
        "Entity",
        "EntityIdDeletionError",
        "EntityIdModificationError",
        "EntityIdNoneError",
        "Event",
        "ExpressionSpecification",
        "LengthValidator",
        "Message",
        "NotSpecification",
        "OrSpecification",
        "PermissionChecker",
        "Query",
        "RangeValidator",
        "RequiredValidator",
        "Specification",
        "ValueObject",
    ),
    "forging_blocks.application": (
        "ApplicationServicePort",
        "AuthorizationPort",
        "CachePort",
        "CommandHandlerPort",
        "CommandSenderPort",
        "ConcurrencyError",
        "EventBusError",
        "EventBusPort",
        "EventHandlerPort",
        "EventPublisherPort",
        "EventStoreError",
        "EventStorePort",
        "HttpClientPort",
        "FileSystemPort",
        "LoggerPort",
        "MessageBusPort",
        "MessageHandlerPort",
        "NotifierPort",
        "QueryFetcherPort",
        "QueryHandlerPort",
        "ReadOnlyRepositoryPort",
        "RepositoryPort",
        "SpecificationRepositoryPort",
        "TransactionManagerPort",
        "UnitOfWorkError",
        "UnitOfWorkPort",
        "UseCasePort",
        "ValidationPort",
        "WriteOnlyRepositoryPort",
    ),
    "forging_blocks.application.ports": (
        "CachePort",
        "CommandSenderPort",
        "CommandHandlerPort",
        "EventBusPort",
        "EventHandlerPort",
        "EventPublisherPort",
        "EventStorePort",
        "HttpClientPort",
        "FileSystemPort",
        "LoggerPort",
        "MessageBusPort",
        "MessageHandlerPort",
        "NotifierPort",
        "QueryFetcherPort",
        "ReadOnlyRepositoryPort",
        "RepositoryPort",
        "WriteOnlyRepositoryPort",
        "SpecificationRepositoryPort",
        "TransactionManagerPort",
        "UnitOfWorkPort",
        "QueryHandlerPort",
        "UseCasePort",
    ),
    "forging_blocks.infrastructure": (
        "AggregateRepository",
        "EventBusBase",
        "EventStoreBase",
        "InMemoryCache",
        "InMemoryEventBus",
        "InMemoryEventBusBase",
        "InMemoryEventStore",
        "InMemoryEventStoreBase",
        "InMemoryMessageBus",
        "InMemoryReadRepository",
        "InMemoryRepository",
        "InMemoryUnitOfWork",
        "InMemoryWriteRepository",
        "MessageBusCommandSender",
        "MessageBusEventPublisher",
        "MessageBusQueryFetcher",
        "OSFileSystem",
        "RepositoryError",
        "RepositoryNotFoundError",
        "DictMessageCodec",
        "MessageCodec",
        "StdlibLogger",
        "URLLibClient",
    ),
    "forging_blocks.presentation": (
        "ErrorHandlingMiddleware",
        "ErrorMessageModel",
        "ErrorPresenter",
        "ErrorStatusCodeMapper",
        "ErrorViewModel",
        "LoggingMiddleware",
        "Middleware",
        "NextHandler",
        "Pipeline",
        "PresentationAdapter",
        "PresenterPort",
        "RequestAdapter",
        "ResponseAdapter",
        "TimingMiddleware",
        "ValidationMiddleware",
    ),
}
for facade_name, expected_names in expected_exports.items():
    facade: ModuleType = importlib.import_module(facade_name)
    export_names: tuple[str, ...] = tuple(
        cast(tuple[str, ...], getattr(facade, "__all__", ()))
    )
    if export_names != expected_names:
        raise SystemExit(
            f"Export manifest mismatch for {facade_name}: "
            f"expected {expected_names}, got {export_names}"
        )
    for symbol_name in export_names:
        getattr(facade, symbol_name)
PY
  )
}

log "Installing and checking wheel outside source checkout"
validate_installed_artifact "${wheel_files[0]}" "$validation_dir/wheel"

log "Installing and checking source archive outside source checkout"
validate_installed_artifact "${sdist_files[0]}" "$validation_dir/sdist"

log "Artifacts validated successfully"
