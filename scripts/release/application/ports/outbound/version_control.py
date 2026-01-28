from abc import abstractmethod

from forging_blocks.foundation import OutputPort
from scripts.release.domain.value_objects import ReleaseBranchName, TagName


class VersionControl(OutputPort):
    """Abstracts version control operations required by the release workflow.

    Must be non-interactive. All methods must raise on failure.
    """

    @abstractmethod
    def branch_exists(
        self,
        branch: ReleaseBranchName,
    ) -> bool:
        """Local branch existence check.
        """
        ...

    def checkout(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        """Checkout local branch.
        """
        ...

    def checkout_main(self) -> None:
        """Return to the main branch (or the configured default branch).
        """
        ...

    def commit_release_artifacts(
        self,
    ) -> None:
        """Commit the version bump and any generated artifacts (e.g., changelog).
        Must be non-interactive.
        """
        ...

    def create_branch(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        """Create local branch.
        """
        ...

    def create_tag(
        self,
        tag: TagName,
    ) -> None:
        """Create tag (prefer annotated tags).
        """
        ...

    def delete_tag(
        self,
        tag: TagName,
    ) -> None:
        """Delete tag locally and remotely (or define two methods if you prefer explicitness).
        """
        ...

    def delete_local_branch(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        """Delete local branch if present.
        """
        ...

    def delete_remote_branch(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        """Delete remote branch (origin) if present.
        Must be implemented as a non-interactive command (e.g., git push origin :branch).
        """
        ...

    def push(
        self,
        branch: ReleaseBranchName,
        *,
        push_tags: bool,
    ) -> None:
        """Push branch (and optionally tags).
        """
        ...

    @abstractmethod
    def remote_branch_exists(
        self,
        branch: ReleaseBranchName,
    ) -> bool:
        """Remote existence check (origin/<branch>).
        This is important for idempotency and avoiding non-fast-forward surprises.
        """
        ...

    @abstractmethod
    def tag_exists(
        self,
        tag: TagName,
    ) -> bool:
        """Local/remote tag existence check (your implementation decides, but document it).
        """
        ...
