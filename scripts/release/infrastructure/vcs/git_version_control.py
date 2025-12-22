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

    def checkout_main(self) -> None:
        run(["git", "checkout", "main"])

    def commit_release_artifacts(self) -> None:
        run(
            [
                "git",
                "commit",
                "-am",
                "chore(release): prepare release",
            ]
        )

    def create_branch(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        run(["git", "checkout", "-b", branch.value])

    def create_tag(
        self,
        tag: TagName,
    ) -> None:
        run(["git", "tag", tag.value])

    def delete_local_branch(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        run(["git", "branch", "-D", branch.value])

    def delete_remote_branch(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        run(["git", "push", "origin", "--delete", branch.value])

    def delete_tag(
        self,
        tag: TagName,
    ) -> None:
        run(["git", "tag", "-d", tag.value])
        run(["git", "push", "origin", "--delete", tag.value])

    def push(
        self,
        branch: ReleaseBranchName,
        *,
        push_tags: bool,
    ) -> None:
        run(["git", "push", "origin", branch.value])

        if push_tags:
            run(["git", "push", "origin", "--tags"])

    def remote_branch_exists(self, branch: ReleaseBranchName) -> bool:
        try:
            run(["git", "ls-remote", "--exit-code", "origin", branch.value])
            return True
        except RuntimeError:
            return False

    def tag_exists(
        self,
        tag: TagName,
    ) -> bool:
        try:
            run(["git", "rev-parse", "--verify", tag.value])
            return True
        except RuntimeError:
            return False
