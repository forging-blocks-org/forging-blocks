from unittest.mock import MagicMock, create_autospec

import pytest

from scripts.release.infrastructure.commons.process import CommandRunner
from scripts.release.infrastructure.vcs.git_version_control import (
    GitVersionControl,
)
from scripts.release.domain.value_objects import (
    ReleaseBranchName,
    TagName,
    ReleaseVersion,
)


class TestGitVersionControl:
    @pytest.fixture
    def runner_mock(self) -> MagicMock:
        """Fixture to create a mock for the CommandRunner."""
        return create_autospec(spec=CommandRunner, instance=True)

    def test_branch_exists_when_branch_exists_then_true(
        self,
        runner_mock: MagicMock,
    ) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        branch = ReleaseBranchName("release/v1.2.3")

        runner_mock.run.return_value = ""

        # Act
        result = vcs.branch_exists(branch)

        # Assert
        assert result is True
        runner_mock.run.assert_called_once_with(
            ["git", "rev-parse", "--verify", branch.value]
        )

    def test_branch_exists_when_branch_does_not_exist_then_false(
        self,
        runner_mock: MagicMock,
    ) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        branch = ReleaseBranchName("release/v1.2.3")

        runner_mock.run.side_effect = RuntimeError("git error: branch not found")

        # Act
        result = vcs.branch_exists(branch)

        # Assert
        assert result is False
        runner_mock.run.assert_called_once_with(
            ["git", "rev-parse", "--verify", branch.value]
        )

    def test_checkout_calls_git_checkout(
        self,
        runner_mock: MagicMock,
    ) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        branch = ReleaseBranchName("release/v1.2.3")

        # Act
        vcs.checkout(branch)

        # Assert
        runner_mock.run.assert_called_once_with(["git", "checkout", branch.value])

    def test_create_branch_calls_git_checkout_b(
        self,
        runner_mock: MagicMock,
    ) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        branch = ReleaseBranchName("release/v1.2.3")

        # Act
        vcs.create_branch(branch)

        # Assert
        runner_mock.run.assert_called_once_with(["git", "checkout", "-b", branch.value])

    def test_tag_exists_when_tag_exists_then_true(
        self,
        runner_mock: MagicMock,
    ) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        tag = TagName.for_version(ReleaseVersion(1, 2, 3))
        runner_mock.run.return_value = ""  # Simulate successful run

        # Act
        result = vcs.tag_exists(tag)

        # Assert
        assert result is True
        runner_mock.run.assert_called_once_with(["git", "rev-parse", "--verify", tag.value])

    def test_tag_exists_when_tag_does_not_exist_then_false(
        self,
        runner_mock: MagicMock,
    ) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        tag = TagName.for_version(ReleaseVersion(1, 2, 3))
        runner_mock.run.side_effect = RuntimeError("not found")  # Simulate failure

        # Act
        result = vcs.tag_exists(tag)

        # Assert
        assert result is False
        runner_mock.run.assert_called_once_with(["git", "rev-parse", "--verify", tag.value])

    def test_create_tag_calls_git_tag(
        self,
        runner_mock: MagicMock,
    ) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        tag = TagName.for_version(ReleaseVersion(1, 2, 3))

        # Act
        vcs.create_tag(tag)

        # Assert
        runner_mock.run.assert_called_once_with(["git", "tag", tag.value])

    def test_commit_release_artifacts_calls_git_commit(
        self,
        runner_mock: MagicMock,
    ) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)

        # Act
        vcs.commit_release_artifacts()

        # Assert
        runner_mock.run.assert_called_once_with(
            ["git", "commit", "-am", "chore(release): prepare release"]
        )

    def test_push_with_tags_calls_git_push_and_push_tags(
        self,
        runner_mock: MagicMock,
    ) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        branch = ReleaseBranchName("release/v1.2.3")

        # Act
        vcs.push(branch, push_tags=True)

        # Assert
        assert runner_mock.run.call_count == 2
        runner_mock.run.assert_any_call(["git", "push", "origin", branch.value])
        runner_mock.run.assert_any_call(["git", "push", "origin", "--tags"])

    def test_push_without_tags_calls_git_push_only(
        self,
        runner_mock: MagicMock,
    ) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        branch = ReleaseBranchName("release/v1.2.3")

        # Act
        vcs.push(branch, push_tags=False)

        # Assert
        runner_mock.run.assert_called_once_with(["git", "push", "origin", branch.value])

    def test_checkout_main_calls_git_checkout_main(self, runner_mock: MagicMock) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)

        # Act
        vcs.checkout_main()

        # Assert
        runner_mock.run.assert_called_once_with(["git", "checkout", "main"])

    def test_delete_local_branch_calls_git_branch_d(self, runner_mock: MagicMock) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        branch = ReleaseBranchName("release/v1.2.3")

        # Act
        vcs.delete_local_branch(branch)

        # Assert
        runner_mock.run.assert_called_once_with(["git", "branch", "-D", branch.value])

    def test_delete_remote_branch_calls_git_push_delete(self, runner_mock: MagicMock) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        branch = ReleaseBranchName("release/v1.2.3")

        # Act
        vcs.delete_remote_branch(branch)

        # Assert
        runner_mock.run.assert_called_once_with(["git", "push", "origin", "--delete", branch.value])

    def test_delete_tag_deletes_local_and_remote_tag(self, runner_mock: MagicMock) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        tag = TagName.for_version(ReleaseVersion(1, 2, 3))

        # Act
        vcs.delete_tag(tag)

        # Assert
        assert runner_mock.run.call_count == 2
        runner_mock.run.assert_any_call(["git", "tag", "-d", tag.value])
        runner_mock.run.assert_any_call(["git", "push", "origin", "--delete", tag.value])

    def test_remote_branch_exists_when_exists_then_true(self, runner_mock: MagicMock) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        branch = ReleaseBranchName("release/v1.2.3")
        runner_mock.run.return_value = ""  # Simulate success

        # Act
        result = vcs.remote_branch_exists(branch)

        # Assert
        assert result is True
        runner_mock.run.assert_called_once_with(
            ["git", "ls-remote", "--exit-code", "origin", branch.value]
        )

    def test_remote_branch_exists_when_not_exists_then_false(self, runner_mock: MagicMock) -> None:
        # Arrange
        vcs = GitVersionControl(runner_mock)
        branch = ReleaseBranchName("release/v1.2.3")
        runner_mock.run.side_effect = RuntimeError("not found")  # Simulate error

        # Act
        result = vcs.remote_branch_exists(branch)

        # Assert
        assert result is False
        runner_mock.run.assert_called_once_with(
            ["git", "ls-remote", "--exit-code", "origin", branch.value]
        )
