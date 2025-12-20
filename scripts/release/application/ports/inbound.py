from __future__ import annotations

from dataclasses import dataclass

from forging_blocks.application.ports import UseCase


@dataclass(frozen=True)
class PrepareReleaseInput:
    """
    Request DTO for preparing a release.

    All values are raw primitives.
    Validation and conversion to Value Objects
    happens inside the use case.

    Future options (intentionally not modeled yet):
    - author: str            # release author / actor
    - dry_run_reason: str    # explanation for dry runs
    - allow_dirty: bool      # allow uncommitted changes
    """

    level: str  # "major" | "minor" | "patch"
    dry_run: bool = False  # if True, no side effects are executed


@dataclass(frozen=True)
class PrepareReleaseOutput:
    """
    Response DTO for preparing a release.

    Contains only serializable primitives so it can be:
    - printed by the CLI
    - logged
    - consumed by CI steps
    """

    version: str  # e.g. "1.4.0"
    branch: str  # e.g. "release/v1.4.0"
    tag: str  # e.g. "v1.4.0"


class PrepareReleaseUseCase(UseCase[PrepareReleaseInput, PrepareReleaseOutput]):
    """
    Prepares a release from the main branch.

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

    async def execute(
        self,
        request: PrepareReleaseInput,
    ) -> PrepareReleaseOutput: ...


@dataclass(frozen=True)
class CreateReleasePullRequestInput:
    """
    Request DTO for creating a release pull request.

    All values are raw primitives.
    Validation and conversion to Value Objects
    happens inside the use case.

    Future options (intentionally not modeled yet):
    - labels: list[str]
    - reviewers: list[str]
    - draft: bool
    """

    base: str  # expected: "main"
    head: str  # expected: "release/vX.Y.Z"
    title: str
    body: str
    dry_run: bool = False  # if True, PR is not created


@dataclass(frozen=True)
class CreateReleasePullRequestOutput:
    """
    Response DTO for creating a release pull request.
    """

    pr_id: str | None
    url: str | None


class CreateReleasePullRequestUseCase(
    UseCase[
        CreateReleasePullRequestInput,
        CreateReleasePullRequestOutput,
    ]
):
    """
    Creates the release pull request representing
    the intent to publish a new version.

    Notes:
    - The PR is the boundary between application logic and CI/CD
    - A merged PR triggers publishing and documentation deployment
    """

    async def execute(
        self,
        request: CreateReleasePullRequestInput,
    ) -> CreateReleasePullRequestOutput: ...
