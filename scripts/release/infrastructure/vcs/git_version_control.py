from scripts.release.application.ports.outbound import VersionControl
from scripts.release.infrastructure.commons.process import CommandRunner, SubprocessCommandRunner
from scripts.release.domain.value_objects import (
    ReleaseBranchName,
    TagName,
)


class GitVersionControl(VersionControl):
    def __init__(self, runner: CommandRunner = SubprocessCommandRunner()) -> None:
        self._runner = runner

    def branch_exists(
        self,
        branch: ReleaseBranchName,
    ) -> bool:
        try:
            self._runner.run(["git", "rev-parse", "--verify", branch.value])
            return True
        except RuntimeError:
            return False

    def checkout(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        self._runner.run(["git", "checkout", branch.value])

    def checkout_main(self) -> None:
        self._runner.run(["git", "checkout", "main"])

    def commit_release_artifacts(self) -> None:
        self._runner.run(
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
        self._runner.run(["git", "checkout", "-b", branch.value])

    def create_tag(
        self,
        tag: TagName,
    ) -> None:
        self._runner.run(["git", "tag", tag.value])

    def delete_local_branch(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        self._runner.run(["git", "branch", "-D", branch.value])

    def delete_remote_branch(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        self._runner.run(["git", "push", "origin", "--delete", branch.value])

    def delete_tag(
        self,
        tag: TagName,
    ) -> None:
        self._runner.run(["git", "tag", "-d", tag.value])
        self._runner.run(["git", "push", "origin", "--delete", tag.value])

    def push(
        self,
        branch: ReleaseBranchName,
        *,
        push_tags: bool,
    ) -> None:
        self._runner.run(["git", "push", "origin", branch.value])

        if push_tags:
            self._runner.run(["git", "push", "origin", "--tags"])

    def remote_branch_exists(self, branch: ReleaseBranchName) -> bool:
        try:
            self._runner.run(["git", "ls-remote", "--exit-code", "origin", branch.value])
            return True
        except RuntimeError:
            return False

    def tag_exists(
        self,
        tag: TagName,
    ) -> bool:
        try:
            self._runner.run(["git", "rev-parse", "--verify", tag.value])
            return True
        except RuntimeError:
            return False
