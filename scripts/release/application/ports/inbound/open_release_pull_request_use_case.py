from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass

from forging_blocks.application.ports import UseCase


@dataclass(frozen=True)
class OpenReleasePullRequestInput:
    """Request DTO for creating a release pull request.

    All values are raw primitives.
    Validation and conversion to Value Objects
    happens inside the use case.

    Future options (intentionally not modeled yet):
    - labels: list[str]
    - reviewers: list[str]
    - draft: bool
    """

    version: str
    branch: str
    dry_run: bool = False


@dataclass(frozen=True)
class OpenReleasePullRequestOutput:
    """Response DTO for creating a release pull request.
    """

    pr_id: str | None
    url: str | None


class OpenReleasePullRequestUseCase(
    UseCase[
        OpenReleasePullRequestInput,
        OpenReleasePullRequestOutput,
    ]
):
    """Creates the release pull request representing
    the intent to publish a new version.

    Notes:
    - The PR is the boundary between application logic and CI/CD
    - A merged PR triggers publishing and documentation deployment
    """

    @abstractmethod
    async def execute(
        self,
        request: OpenReleasePullRequestInput,
    ) -> OpenReleasePullRequestOutput: ...
