from abc import abstractmethod
from dataclasses import dataclass

from forging_blocks.foundation.ports import OutputPort
from scripts.release.domain.entities import ReleasePullRequest


@dataclass(frozen=True)
class OpenPullRequestOutput:
    """DTO representing the output of creating a pull request.
    """

    pr_id: str | None
    url: str | None


class PullRequestService(OutputPort):
    """Service that manages pull request creation in remote repository.
    """

    @abstractmethod
    def open(self, pull_request: ReleasePullRequest) -> OpenPullRequestOutput:
        """Open a pull request and return its details.
        """
        ...
