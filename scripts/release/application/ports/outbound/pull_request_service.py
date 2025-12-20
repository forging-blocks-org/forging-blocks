from dataclasses import dataclass

from forging_blocks.foundation.ports import OutputPort

from scripts.release.domain.value_objects import (
    PullRequestBase,
    PullRequestHead,
    PullRequestTitle,
    PullRequestBody,
)


@dataclass(frozen=True)
class CreatePullRequestInput:
    """
    DTO representing the input for creating pull request.
    """

    base: PullRequestBase
    head: PullRequestHead
    title: PullRequestTitle
    body: PullRequestBody
    dry_run: bool


@dataclass(frozen=True)
class CreatePullRequestOutput:
    """
    DTO representing the output of creating a pull request.
    """

    pr_id: str | None
    url: str | None


class PullRequestService(OutputPort):
    """
    Servuce that manages pull request creation in remote repository.
    """

    def create(self, input: CreatePullRequestInput) -> CreatePullRequestOutput:
        """
        Create a pull request and return its details.
        """
        ...
