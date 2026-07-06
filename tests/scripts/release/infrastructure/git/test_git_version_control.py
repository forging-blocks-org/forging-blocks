# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from __future__ import annotations

import pytest
from scripts.release.infrastructure.git.git_version_control import GitVersionControl

from scripts.release.domain.value_objects import ReleaseBranchName
from tests.fixtures.fake_command_runner import FakeCommandRunner


@pytest.mark.unit
class TestGitVersionControl:
    @pytest.fixture
    def runner(self) -> FakeCommandRunner:
        return FakeCommandRunner()

    @pytest.fixture
    def version_control(self, runner: FakeCommandRunner) -> GitVersionControl:
        return GitVersionControl(runner)

    @pytest.fixture
    def branch_name(self) -> ReleaseBranchName:
        return ReleaseBranchName("release/v1.2.0")

    def test_branch_exists_when_branch_found_then_returns_true(
        self,
        version_control: GitVersionControl,
        runner: FakeCommandRunner,
        branch_name: ReleaseBranchName,
    ) -> None:
        result = version_control.branch_exists(branch_name)

        assert result is True
        assert len(runner.calls) == 1
        assert runner.calls[0] == (
            ["git", "rev-parse", "--verify", "release/v1.2.0"],
            True,
            True,  # suppress_error_log
        )

    def test_branch_exists_when_branch_not_found_then_returns_false(
        self,
        version_control: GitVersionControl,
        runner: FakeCommandRunner,
        branch_name: ReleaseBranchName,
    ) -> None:
        runner.configured_outputs = [RuntimeError()]

        result = version_control.branch_exists(branch_name)

        assert result is False

    def test_checkout(
        self,
        version_control: GitVersionControl,
        runner: FakeCommandRunner,
        branch_name: ReleaseBranchName,
    ) -> None:
        version_control.checkout(branch_name)

        assert len(runner.calls) == 1
        assert runner.calls[0][0] == ["git", "checkout", "release/v1.2.0"]

    def test_checkout_main_success(
        self, version_control: GitVersionControl, runner: FakeCommandRunner
    ) -> None:
        version_control.checkout_main()

        assert len(runner.calls) == 1
        assert runner.calls[0][0] == ["git", "checkout", "main"]

    def test_checkout_main_fallback(
        self, version_control: GitVersionControl, runner: FakeCommandRunner
    ) -> None:
        runner.configured_outputs = [
            RuntimeError(),  # checkout main fails
            "origin/master",  # symbolic-ref
            "",  # checkout master
        ]

        version_control.checkout_main()

        assert len(runner.calls) == 3
        assert runner.calls[0][0] == ["git", "checkout", "main"]
        assert runner.calls[1][0] == ["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"]
        assert runner.calls[2][0] == ["git", "checkout", "master"]

    def test_commit_release_artifacts(
        self, version_control: GitVersionControl, runner: FakeCommandRunner
    ) -> None:
        version_control.commit_release_artifacts()

        assert len(runner.calls) == 2
        assert runner.calls[0][0] == ["git", "add", "-A"]
        assert runner.calls[1][0] == ["git", "commit", "-m", "chore(release): prepare release"]

    def test_commit_release_artifacts_retry_precommit(
        self, version_control: GitVersionControl, runner: FakeCommandRunner
    ) -> None:
        runner.configured_outputs = [
            "",  # git add -A
            RuntimeError("pre-commit failure"),  # first commit attempt
            "",  # git add -A (retry)
            "",  # second commit attempt
        ]

        version_control.commit_release_artifacts()

        assert len(runner.calls) == 4

    def test_commit_release_artifacts_failure(
        self, version_control: GitVersionControl, runner: FakeCommandRunner
    ) -> None:
        runner.configured_outputs = ["", RuntimeError("error")]

        with pytest.raises(RuntimeError):
            version_control.commit_release_artifacts()

    def test_create_branch(
        self,
        version_control: GitVersionControl,
        runner: FakeCommandRunner,
        branch_name: ReleaseBranchName,
    ) -> None:
        version_control.create_branch(branch_name)

        assert len(runner.calls) == 1
        assert runner.calls[0][0] == ["git", "checkout", "-b", "release/v1.2.0"]

    def test_delete_local_branch(
        self,
        version_control: GitVersionControl,
        runner: FakeCommandRunner,
        branch_name: ReleaseBranchName,
    ) -> None:
        version_control.delete_local_branch(branch_name)

        assert len(runner.calls) == 1
        assert runner.calls[0][0] == ["git", "branch", "-D", "release/v1.2.0"]

    def test_delete_remote_branch(
        self,
        version_control: GitVersionControl,
        runner: FakeCommandRunner,
        branch_name: ReleaseBranchName,
    ) -> None:
        version_control.delete_remote_branch(branch_name)

        assert len(runner.calls) == 1
        assert runner.calls[0][0] == ["git", "push", "origin", "--delete", "release/v1.2.0"]

    def test_push(
        self,
        version_control: GitVersionControl,
        runner: FakeCommandRunner,
        branch_name: ReleaseBranchName,
    ) -> None:
        version_control.push(branch_name)

        assert len(runner.calls) == 1
        assert runner.calls[0][0] == ["git", "push", "origin", "release/v1.2.0"]

    def test_remote_branch_exists_true(
        self,
        version_control: GitVersionControl,
        runner: FakeCommandRunner,
        branch_name: ReleaseBranchName,
    ) -> None:
        result = version_control.remote_branch_exists(branch_name)

        assert result is True

    def test_remote_branch_exists_false(
        self,
        version_control: GitVersionControl,
        runner: FakeCommandRunner,
        branch_name: ReleaseBranchName,
    ) -> None:
        runner.configured_outputs = [RuntimeError()]

        result = version_control.remote_branch_exists(branch_name)

        assert result is False
