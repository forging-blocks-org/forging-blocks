from __future__ import annotations

from unittest.mock import MagicMock, call, create_autospec

import pytest
from scripts.release.infrastructure.commons.process import CommandRunner
from scripts.release.infrastructure.git.git_version_control import GitVersionControl

from scripts.release.domain.value_objects import ReleaseBranchName


@pytest.mark.unit
class TestGitVersionControl:
    @pytest.fixture
    def command_runner_mock(self) -> MagicMock:
        mock = create_autospec(CommandRunner, instance=True)
        mock.run = MagicMock(return_value=None)
        return mock

    @pytest.fixture
    def version_control(self, command_runner_mock: MagicMock) -> GitVersionControl:
        return GitVersionControl(command_runner_mock)

    @pytest.fixture
    def branch_name(self) -> ReleaseBranchName:
        return ReleaseBranchName("release/v1.2.0")

    def test_branch_exists_when_branch_found_then_returns_true(
        self,
        version_control: GitVersionControl,
        command_runner_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        result = version_control.branch_exists(branch_name)

        assert result is True
        command_runner_mock.run.assert_called_once_with(
            ["git", "rev-parse", "--verify", "release/v1.2.0"], suppress_error_log=True
        )

    def test_branch_exists_when_branch_not_found_then_returns_false(
        self,
        version_control: GitVersionControl,
        command_runner_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        command_runner_mock.run.side_effect = RuntimeError()

        result = version_control.branch_exists(branch_name)

        assert result is False

    def test_checkout(
        self,
        version_control: GitVersionControl,
        command_runner_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        version_control.checkout(branch_name)

        command_runner_mock.run.assert_called_once_with(["git", "checkout", "release/v1.2.0"])

    def test_checkout_main_success(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock
    ) -> None:
        version_control.checkout_main()

        command_runner_mock.run.assert_called_once_with(["git", "checkout", "main"])

    def test_checkout_main_fallback(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock
    ) -> None:
        def side_effect(cmd, **kwargs):
            if cmd == ["git", "checkout", "main"]:
                raise RuntimeError()
            if cmd == ["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"]:
                return "origin/master"
            return ""

        command_runner_mock.run.side_effect = side_effect

        version_control.checkout_main()

        assert command_runner_mock.run.call_count == 3
        command_runner_mock.run.assert_called_with(["git", "checkout", "master"])

    def test_commit_release_artifacts(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock
    ) -> None:
        version_control.commit_release_artifacts()

        command_runner_mock.run.assert_has_calls(
            [
                call(["git", "add", "-A"]),
                call(["git", "commit", "-m", "chore(release): prepare release"]),
            ]
        )

    def test_commit_release_artifacts_retry_precommit(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock
    ) -> None:
        command_runner_mock.run.side_effect = [
            None,
            RuntimeError("pre-commit failure"),
            None,
            None,
        ]

        version_control.commit_release_artifacts()

        assert command_runner_mock.run.call_count == 4

    def test_commit_release_artifacts_failure(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock
    ) -> None:
        command_runner_mock.run.side_effect = [None, RuntimeError("error")]

        with pytest.raises(RuntimeError):
            version_control.commit_release_artifacts()

    def test_create_branch(
        self,
        version_control: GitVersionControl,
        command_runner_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        version_control.create_branch(branch_name)

        command_runner_mock.run.assert_called_once_with(["git", "checkout", "-b", "release/v1.2.0"])

    def test_delete_local_branch(
        self,
        version_control: GitVersionControl,
        command_runner_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        version_control.delete_local_branch(branch_name)

        command_runner_mock.run.assert_called_once_with(["git", "branch", "-D", "release/v1.2.0"])

    def test_delete_remote_branch(
        self,
        version_control: GitVersionControl,
        command_runner_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        version_control.delete_remote_branch(branch_name)

        command_runner_mock.run.assert_called_once_with(
            ["git", "push", "origin", "--delete", "release/v1.2.0"]
        )

    def test_push(
        self,
        version_control: GitVersionControl,
        command_runner_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        version_control.push(branch_name)

        command_runner_mock.run.assert_called_once_with(["git", "push", "origin", "release/v1.2.0"])

    def test_remote_branch_exists_true(
        self,
        version_control: GitVersionControl,
        command_runner_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        result = version_control.remote_branch_exists(branch_name)

        assert result is True

    def test_remote_branch_exists_false(
        self,
        version_control: GitVersionControl,
        command_runner_mock: MagicMock,
        branch_name: ReleaseBranchName,
    ) -> None:
        command_runner_mock.run.side_effect = RuntimeError()

        result = version_control.remote_branch_exists(branch_name)

        assert result is False
