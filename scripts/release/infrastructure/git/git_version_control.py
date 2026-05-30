import logging

from scripts.release.application.ports.outbound import VersionControl
from scripts.release.domain.value_objects import (
    ReleaseBranchName,
)
from scripts.release.infrastructure.commons.process import CommandRunner


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
        try:
            self._runner.run(["git", "checkout", "main"])
            logging.info("✓ Checked out main branch")
        except RuntimeError:
            raw = self._runner.run(
                ["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"]
            ).strip()
            default_branch = raw.split("/")[-1]
            self._runner.run(["git", "checkout", default_branch])
            logging.info(f"✓ Checked out {default_branch} branch")

    def commit_release_artifacts(self) -> None:
        logging.info("Committing release artifacts...")
        try:
            self._runner.run(["git", "add", "-A"])
            self._runner.run(["git", "commit", "-m", "chore(release): prepare release"])
            logging.info("✓ Committed release artifacts")
        except RuntimeError as e:
            error_msg = str(e)

            if self._is_pre_commit_failure(error_msg):
                self._runner.run(["git", "add", "-A"])
                self._runner.run(["git", "commit", "-m", "chore(release): prepare release"])
                logging.info("✓ Committed release artifacts")
            else:
                raise

    def create_branch(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        logging.info(f"Creating release branch {branch.value}...")
        self._runner.run(["git", "checkout", "-b", branch.value])
        logging.info(f"✓ Created branch {branch.value}")

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

    def push(
        self,
        branch: ReleaseBranchName,
    ) -> None:
        self._runner.run(["git", "push", "origin", branch.value])

    def remote_branch_exists(self, branch: ReleaseBranchName) -> bool:
        try:
            self._runner.run(["git", "ls-remote", "--exit-code", "origin", branch.value])
            return True
        except RuntimeError:
            return False

    def _is_pre_commit_failure(self, error_msg: str) -> bool:
        indicators = ["pre-commit", "hook", "end-of-file-fixer", "ruff", "trim trailing"]
        return any(indicator in error_msg.lower() for indicator in indicators)
