from __future__ import annotations

import pytest
from unittest.mock import MagicMock, create_autospec

from scripts.release.infrastructure.git.git_version_control import GitVersionControl
from scripts.release.infrastructure.commons.process import CommandRunner
from scripts.release.domain.value_objects import ReleaseBranchName, TagName


class TestGitVersionControl:
    @pytest.fixture
    def command_runner_mock(self) -> MagicMock:
        mock = create_autospec(CommandRunner, instance=True)
        # Configure run method to accept the suppress_error_log parameter
        mock.run = MagicMock(return_value=None)
        return mock

    @pytest.fixture
    def version_control(self, command_runner_mock: MagicMock) -> GitVersionControl:
        return GitVersionControl(command_runner_mock)

    @pytest.fixture
    def branch_name(self) -> ReleaseBranchName:
        return ReleaseBranchName("release/v1.2.0")

    @pytest.fixture
    def tag_name(self) -> TagName:
        return TagName("v1.2.0")

    def test_init_when_called_then_sets_runner(self, command_runner_mock: MagicMock) -> None:
        version_control = GitVersionControl(command_runner_mock)
        
        assert version_control._runner == command_runner_mock

    def test_branch_exists_when_branch_found_then_returns_true(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, branch_name: ReleaseBranchName
    ) -> None:
        command_runner_mock.run.return_value = None
        
        result = version_control.branch_exists(branch_name)
        
        assert result is True
        command_runner_mock.run.assert_called_once_with(
            ["git", "rev-parse", "--verify", "release/v1.2.0"], suppress_error_log=True
        )

    def test_branch_exists_when_branch_not_found_then_returns_false(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, branch_name: ReleaseBranchName
    ) -> None:
        command_runner_mock.run.side_effect = RuntimeError("Branch not found")
        
        result = version_control.branch_exists(branch_name)
        
        assert result is False
        command_runner_mock.run.assert_called_once_with(
            ["git", "rev-parse", "--verify", "release/v1.2.0"], suppress_error_log=True
        )

    def test_checkout_when_called_then_runs_checkout_command(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, branch_name: ReleaseBranchName
    ) -> None:
        version_control.checkout(branch_name)
        
        command_runner_mock.run.assert_called_once_with(["git", "checkout", "release/v1.2.0"])

    def test_checkout_main_when_called_then_runs_checkout_main_command(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock
    ) -> None:
        version_control.checkout_main()
        
        command_runner_mock.run.assert_called_once_with(["git", "checkout", "main"])

    def test_commit_release_artifacts_when_called_then_runs_commit_command(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock
    ) -> None:
        version_control.commit_release_artifacts()
        
        command_runner_mock.run.assert_called_once_with([
            "git", "commit", "-am", "chore(release): prepare release"
        ])

    def test_create_branch_when_called_then_runs_checkout_b_command(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, branch_name: ReleaseBranchName
    ) -> None:
        version_control.create_branch(branch_name)
        
        command_runner_mock.run.assert_called_once_with(["git", "checkout", "-b", "release/v1.2.0"])

    def test_create_tag_when_called_then_runs_tag_command(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, tag_name: TagName
    ) -> None:
        version_control.create_tag(tag_name)
        
        command_runner_mock.run.assert_called_once_with(["git", "tag", "v1.2.0"])

    def test_delete_local_branch_when_called_then_runs_branch_delete_command(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, branch_name: ReleaseBranchName
    ) -> None:
        version_control.delete_local_branch(branch_name)
        
        command_runner_mock.run.assert_called_once_with(["git", "branch", "-D", "release/v1.2.0"])

    def test_delete_remote_branch_when_called_then_runs_push_delete_command(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, branch_name: ReleaseBranchName
    ) -> None:
        version_control.delete_remote_branch(branch_name)
        
        command_runner_mock.run.assert_called_once_with(["git", "push", "origin", "--delete", "release/v1.2.0"])

    def test_delete_tag_when_called_then_runs_tag_delete_and_push_delete_commands(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, tag_name: TagName
    ) -> None:
        version_control.delete_tag(tag_name)
        
        expected_calls = [
            (["git", "tag", "-d", "v1.2.0"],),
            (["git", "push", "origin", "--delete", "v1.2.0"],)
        ]
        assert command_runner_mock.run.call_count == 2
        actual_calls = [call[0] for call in command_runner_mock.run.call_args_list]
        assert actual_calls == expected_calls

    def test_push_when_called_without_tags_then_runs_push_command_only(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, branch_name: ReleaseBranchName
    ) -> None:
        version_control.push(branch_name, push_tags=False)
        
        command_runner_mock.run.assert_called_once_with(["git", "push", "origin", "release/v1.2.0"])

    def test_push_when_called_with_tags_then_runs_push_and_push_tags_commands(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, branch_name: ReleaseBranchName
    ) -> None:
        version_control.push(branch_name, push_tags=True)
        
        expected_calls = [
            (["git", "push", "origin", "release/v1.2.0"],),
            (["git", "push", "origin", "--tags"],)
        ]
        assert command_runner_mock.run.call_count == 2
        actual_calls = [call[0] for call in command_runner_mock.run.call_args_list]
        assert actual_calls == expected_calls

    def test_remote_branch_exists_when_branch_found_then_returns_true(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, branch_name: ReleaseBranchName
    ) -> None:
        command_runner_mock.run.return_value = None
        
        result = version_control.remote_branch_exists(branch_name)
        
        assert result is True
        command_runner_mock.run.assert_called_once_with(["git", "ls-remote", "--exit-code", "origin", "release/v1.2.0"])

    def test_remote_branch_exists_when_branch_not_found_then_returns_false(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, branch_name: ReleaseBranchName
    ) -> None:
        command_runner_mock.run.side_effect = RuntimeError("Branch not found")
        
        result = version_control.remote_branch_exists(branch_name)
        
        assert result is False
        command_runner_mock.run.assert_called_once_with(["git", "ls-remote", "--exit-code", "origin", "release/v1.2.0"])

    def test_tag_exists_when_tag_found_then_returns_true(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, tag_name: TagName
    ) -> None:
        command_runner_mock.run.return_value = None
        
        result = version_control.tag_exists(tag_name)
        
        assert result is True
        command_runner_mock.run.assert_called_once_with(
            ["git", "rev-parse", "--verify", "v1.2.0"], suppress_error_log=True
        )

    def test_tag_exists_when_tag_not_found_then_returns_false(
        self, version_control: GitVersionControl, command_runner_mock: MagicMock, tag_name: TagName
    ) -> None:
        command_runner_mock.run.side_effect = RuntimeError("Tag not found")
        
        result = version_control.tag_exists(tag_name)
        
        assert result is False
        command_runner_mock.run.assert_called_once_with(
            ["git", "rev-parse", "--verify", "v1.2.0"], suppress_error_log=True
        )


@pytest.mark.integration
class TestGitVersionControlIntegration:
    def test_branch_lifecycle_when_created_then_exists_and_deleted(
        self,
        git_repo: GitTestRepository,
    ) -> None:
        # Arrange
        from scripts.release.infrastructure.commons.process import SubprocessCommandRunner
        version_control = GitVersionControl(SubprocessCommandRunner())
        branch = ReleaseBranchName("release/v1.2.0")

        # Act
        exists_before = version_control.branch_exists(branch)
        version_control.create_branch(branch)
        exists_after = version_control.branch_exists(branch)

        version_control.checkout_main()
        version_control.delete_local_branch(branch)

        # Assert
        assert exists_before is False
        assert exists_after is True
        assert version_control.branch_exists(branch) is False

    def test_tag_lifecycle_when_created_then_exists_and_deleted(
        self,
        git_repo: GitTestRepository,
    ) -> None:
        # Arrange
        from scripts.release.infrastructure.commons.process import SubprocessCommandRunner
        version_control = GitVersionControl(SubprocessCommandRunner())
        tag = TagName("v1.2.0")

        # Act
        exists_before = version_control.tag_exists(tag)
        version_control.create_tag(tag)
        exists_after = version_control.tag_exists(tag)
        version_control.delete_tag(tag)

        # Assert
        assert exists_before is False
        assert exists_after is True
        assert version_control.tag_exists(tag) is False

    def test_commit_release_artifacts_when_file_changed_then_commit_created(
        self,
        git_repo: GitTestRepository,
    ) -> None:
        # Arrange
        from scripts.release.infrastructure.commons.process import SubprocessCommandRunner
        version_control = GitVersionControl(SubprocessCommandRunner())
        git_repo.write_file("CHANGELOG.md", "changes")
        git_repo.commit("Add CHANGELOG.md")

        # Modify the tracked file
        git_repo.write_file("CHANGELOG.md", "updated changes")
        
        # Check status before commit
        import subprocess
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=git_repo._path,
            capture_output=True,
            text=True
        )
        print(f"Git status before commit: '{result.stdout.strip()}'")

        # Act (this should commit the modified tracked file using -am)
        try:
            version_control.commit_release_artifacts()
        except Exception as e:
            print(f"Exception during commit: {e}")
            raise

        # Check status after commit
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=git_repo._path,
            capture_output=True,
            text=True
        )
        print(f"Git status after commit: '{result.stdout.strip()}'")

        # Assert
        assert git_repo.last_commit_message() == "chore(release): prepare release"
