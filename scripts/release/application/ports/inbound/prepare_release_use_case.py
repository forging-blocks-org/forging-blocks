from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass

from forging_blocks.application.ports import UseCase


@dataclass(frozen=True)
class PrepareReleaseInput:
    """Request DTO for preparing a release.

    All values are raw primitives.
    Validation and conversion to Value Objects
    happens inside the use case.

    Future options (intentionally not modeled yet):
    - author: str            # release author / actor
    - dry_run_reason: str    # explanation for dry runs
    - allow_dirty: bool      # allow uncommitted changes
    """

    level: str
    dry_run: bool = False


@dataclass(frozen=True)
class PrepareReleaseOutput:
    """Response DTO for preparing a release.

    Contains only serializable primitives so it can be:
    - printed by the CLI
    - logged
    - consumed by CI steps
    """

    version: str
    branch: str
    tag: str


class PrepareReleaseUseCase(UseCase[PrepareReleaseInput, PrepareReleaseOutput]):
    """Prepares a release from the main branch.

    Responsibilities:
    - validate release level
    - validate current branch is main
    - compute next version
    - create or resume release branch
    - apply version bump (unless dry_run=True)
    - create git tag (unless dry_run=True)
    - commit and push changes (unless dry_run=True)

    Notes:
    - The use case must remain idempotent
    - Dry runs must never mutate external state
    """

    @abstractmethod
    async def execute(
        self,
        request: PrepareReleaseInput,
    ) -> PrepareReleaseOutput: ...
