from dataclasses import dataclass
from forging_blocks.foundation.ports import OutputPort

from scripts.release.domain.value_objects import (
    ReleaseLevel,
    ReleaseVersion,
    ReleaseBranchName,
    TagName,
    PullRequestBase,
    PullRequestHead,
    PullRequestTitle,
    PullRequestBody,
)


class VersioningService(OutputPort):
    """
    Computes and applies semantic versions to the package definition.
    """

    def compute_next_version(
        self,
        level: ReleaseLevel,
    ) -> ReleaseVersion: ...

    def apply_version(
        self,
        version: ReleaseVersion,
    ) -> None: ...


class VersionControl(OutputPort):
    """
    Abstracts version control operations required by the release workflow.
    """

    def branch_exists(
        self,
        branch: ReleaseBranchName,
    ) -> bool: ...

    def checkout(
        self,
        branch: ReleaseBranchName,
    ) -> None: ...

    def create_branch(
        self,
        branch: ReleaseBranchName,
    ) -> None: ...

    def tag_exists(
        self,
        tag: TagName,
    ) -> bool: ...

    def create_tag(
        self,
        tag: TagName,
    ) -> None: ...

    def commit_release_artifacts(
        self,
    ) -> None: ...

    def push(
        self,
        branch: ReleaseBranchName,
        *,
        push_tags: bool,
    ) -> None: ...


@dataclass(frozen=True)
class PullRequestServiceOutput:
    """
    DTO representing the output of creating a pull request.
    """

    pr_id: str | None
    url: str | None


class PullRequestService(OutputPort):
    """
    Creates release pull requests in a hosting platform.
    """

    def create(
        self,
        *,
        base: PullRequestBase,
        head: PullRequestHead,
        title: PullRequestTitle,
        body: PullRequestBody,
        dry_run: bool,
    ) -> PullRequestServiceOutput: ...
