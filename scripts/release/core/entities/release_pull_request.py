from forging_blocks.domain import Entity

from scripts.release.core.errors import InvalidReleasePullRequestError
from ..value_objects import (
    # ReleaseVersion,
    # BranchName,
    # TagName,
    PullRequestBase,
    PullRequestHead,
    PullRequestTitle,
    PullRequestBody,
)


class ReleasePullRequest(Entity[str]):
    """
    Represents the intent to publish a release.
    """

    __slots__ = ("_base", "_head", "_title", "_body")

    def __init__(
        self,
        *,
        base: PullRequestBase,
        head: PullRequestHead,
        title: PullRequestTitle,
        body: PullRequestBody,
        pr_id: str | None = None,
    ) -> None:
        if not base.is_main():
            raise InvalidReleasePullRequestError("Base branch must be main")

        if not head.is_release_branch():
            raise InvalidReleasePullRequestError("Head must be a release branch")

        super().__init__(pr_id)

        self._base = base
        self._head = head
        self._title = title
        self._body = body
