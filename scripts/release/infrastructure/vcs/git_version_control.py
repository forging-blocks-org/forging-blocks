from scripts.release.application.ports.outbound import VersionControl
from scripts.release.infrastructure.commons.process import run
from scripts.release.domain.value_objects import (
    ReleaseBranchName,
    TagName,
)


class GitVersionControl(VersionControl):
    def branch_exists(
        self,
        branch: ReleaseBranchName,
    ) -> bool:
        try:
            run(["git", "rev-parse", "--verify", branch.value])
            return True
        except RuntimeError:
            return False

    def checkout(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        run(["git", "checkout", branch.value])

    def create_branch(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        run(["git", "checkout", "-b", branch.value])

    def tag_exists(
        self,
        tag: TagName,
    ) -> bool:
        try:
            run(["git", "rev-parse", "--verify", tag.value])
            return True
        except RuntimeError:
            return False

    def create_tag(
        self,
        tag: TagName,
    ) -> None:
        run(["git", "tag", tag.value])

    def commit_release_artifacts(self) -> None:
        run(
            [
                "git",
                "commit",
                "-am",
                "chore(release): prepare release",
            ]
        )

    def push(
        self,
        branch: ReleaseBranchName,
        *,
        push_tags: bool,
    ) -> None:
        run(["git", "push", "origin", branch.value])

        if push_tags:
            run(["git", "push", "origin", "--tags"])
