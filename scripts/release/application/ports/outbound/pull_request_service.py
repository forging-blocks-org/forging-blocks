from dataclasses import dataclass
from typing import runtime_checkable

from forging_blocks.foundation.ports import OutputPort

from scripts.release.domain.value_objects import (
    PullRequestBase,
    PullRequestHead,
    PullRequestTitle,
    PullRequestBody,
)


@dataclass(frozen=True)
class OpenPullRequestInput:
    """
    DTO representing the input for opening a pull request.
    """

    base: PullRequestBase
    head: PullRequestHead
    title: PullRequestTitle
    body: PullRequestBody


@dataclass(frozen=True)
class OpenPullRequestOutput:
    """
    DTO representing the output of creating a pull request.
    """

    pr_id: str | None
    url: str | None


class PullRequestService(OutputPort):
    """
    Service that manages pull request creation in remote repository.
    """

    def open(self, input: OpenPullRequestInput) -> OpenPullRequestOutput:
        """
        Open a pull request and return its details.
        """
        ...
