from __future__ import annotations

from dataclasses import dataclass

from forging_blocks.application.ports import UseCase


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
