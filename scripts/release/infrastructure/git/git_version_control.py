from scripts.release.application.ports.outbound import VersionControl
from scripts.release.infrastructure.commons.process import CommandRunner
from scripts.release.domain.value_objects import (
    ReleaseBranchName,
    TagName,
)
import logging


class GitVersionControl(VersionControl):
    def __init__(self, runner: CommandRunner) -> None:
        self._runner = runner

    def branch_exists(
        self,
        branch: ReleaseBranchName,
    ) -> bool:
        logging.info(f"Checking if branch {branch.value} exists...")
        try:
            self._runner.run(
                ["git", "rev-parse", "--verify", branch.value], suppress_error_log=True
            )
            logging.info(f"✓ Branch {branch.value} exists")
            return True
        except RuntimeError:
            logging.info(f"✓ Branch {branch.value} does not exist")
            return False

    def checkout(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        logging.info(f"Checking out branch {branch.value}...")
        self._runner.run(["git", "checkout", branch.value])
        logging.info(f"✓ Checked out branch {branch.value}")

    def checkout_main(self) -> None:
        logging.info("Checking out main branch...")
        # Try 'main' first, fall back to 'master' for compatibility
        try:
            self._runner.run(["git", "checkout", "main"])
            logging.info("✓ Checked out main branch")
        except RuntimeError:
            # Fallback to 'master' for older git repos or CI environments
            self._runner.run(["git", "checkout", "master"])
            logging.info("✓ Checked out master branch")

    def commit_release_artifacts(self) -> None:
        logging.info("Committing release artifacts...")
        self._runner.run(
            [
                "git",
                "commit",
                "-am",
                "chore(release): prepare release",
            ]
        )
        logging.info("✓ Committed release artifacts")

    def create_branch(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        logging.info(f"Creating release branch {branch.value}...")
        self._runner.run(["git", "checkout", "-b", branch.value])
        logging.info(f"✓ Created branch {branch.value}")

    def create_tag(
        self,
        tag: TagName,
    ) -> None:
        logging.info(f"Creating tag {tag.value}...")
        self._runner.run(["git", "tag", tag.value])
        logging.info(f"✓ Created tag {tag.value}")

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
        logging.info(f"Deleting tag {tag.value}...")
        self._runner.run(["git", "tag", "-d", tag.value])
        try:
            self._runner.run(["git", "push", "origin", "--delete", tag.value])
            logging.info(f"✓ Deleted remote tag {tag.value}")
        except RuntimeError:
            # Remote might not exist in test environment, that's OK
            logging.info(f"✓ Deleted local tag {tag.value} (remote not available)")
        logging.info(f"✓ Deleted tag {tag.value}")

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
            self._runner.run(
                ["git", "ls-remote", "--exit-code", "origin", branch.value]
            )
            return True
        except RuntimeError:
            return False

    def tag_exists(
        self,
        tag: TagName,
    ) -> bool:
        logging.info(f"Checking if tag {tag.value} exists...")
        try:
            self._runner.run(
                ["git", "rev-parse", "--verify", tag.value], suppress_error_log=True
            )
            logging.info(f"✓ Tag {tag.value} already exists")
            return True
        except RuntimeError:
            logging.info(f"✓ Tag {tag.value} is available")
            return False
