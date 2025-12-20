from unittest.mock import patch

from scripts.release.infrastructure.vcs.git_version_control import (
    GitVersionControl,
)
from scripts.release.domain.value_objects import (
    ReleaseBranchName,
    TagName,
    ReleaseVersion,
)


class TestGitVersionControl:
    @patch("scripts.release.infrastructure.vcs.git_version_control.run")
    def test_branch_exists_when_branch_exists_then_true(
        self,
        run_mock,
    ) -> None:
        vcs = GitVersionControl()
        branch = ReleaseBranchName("release/v1.2.3")

        run_mock.return_value = ""

        assert vcs.branch_exists(branch) is True

        run_mock.assert_called_once_with(["git", "rev-parse", "--verify", branch.value])

    @patch("scripts.release.infrastructure.vcs.git_version_control.run")
    def test_branch_exists_when_branch_does_not_exist_then_false(
        self,
        run_mock,
    ) -> None:
        vcs = GitVersionControl()
        branch = ReleaseBranchName("release/v1.2.3")

        run_mock.side_effect = RuntimeError("not found")

        assert vcs.branch_exists(branch) is False

        run_mock.assert_called_once()

    @patch("scripts.release.infrastructure.vcs.git_version_control.run")
    def test_checkout_calls_git_checkout(
        self,
        run_mock,
    ) -> None:
        vcs = GitVersionControl()
        branch = ReleaseBranchName("release/v1.2.3")

        vcs.checkout(branch)

        run_mock.assert_called_once_with(["git", "checkout", branch.value])

    @patch("scripts.release.infrastructure.vcs.git_version_control.run")
    def test_create_branch_calls_git_checkout_b(
        self,
        run_mock,
    ) -> None:
        vcs = GitVersionControl()
        branch = ReleaseBranchName("release/v1.2.3")

        vcs.create_branch(branch)

        run_mock.assert_called_once_with(["git", "checkout", "-b", branch.value])

    @patch("scripts.release.infrastructure.vcs.git_version_control.run")
    def test_tag_exists_when_tag_exists_then_true(
        self,
        run_mock,
    ) -> None:
        vcs = GitVersionControl()
        tag = TagName.for_version(ReleaseVersion(1, 2, 3))

        run_mock.return_value = ""

        assert vcs.tag_exists(tag) is True

        run_mock.assert_called_once_with(["git", "rev-parse", "--verify", tag.value])

    @patch("scripts.release.infrastructure.vcs.git_version_control.run")
    def test_tag_exists_when_tag_does_not_exist_then_false(
        self,
        run_mock,
    ) -> None:
        vcs = GitVersionControl()
        tag = TagName.for_version(ReleaseVersion(1, 2, 3))

        run_mock.side_effect = RuntimeError("not found")

        assert vcs.tag_exists(tag) is False

        run_mock.assert_called_once()

    @patch("scripts.release.infrastructure.vcs.git_version_control.run")
    def test_create_tag_calls_git_tag(
        self,
        run_mock,
    ) -> None:
        vcs = GitVersionControl()
        tag = TagName.for_version(ReleaseVersion(1, 2, 3))

        vcs.create_tag(tag)

        run_mock.assert_called_once_with(["git", "tag", tag.value])

    @patch("scripts.release.infrastructure.vcs.git_version_control.run")
    def test_commit_release_artifacts_calls_git_commit(
        self,
        run_mock,
    ) -> None:
        vcs = GitVersionControl()

        vcs.commit_release_artifacts()

        run_mock.assert_called_once_with(
            [
                "git",
                "commit",
                "-am",
                "chore(release): prepare release",
            ]
        )

    @patch("scripts.release.infrastructure.vcs.git_version_control.run")
    def test_push_with_tags_calls_git_push_and_push_tags(
        self,
        run_mock,
    ) -> None:
        vcs = GitVersionControl()
        branch = ReleaseBranchName("release/v1.2.3")

        vcs.push(branch, push_tags=True)

        assert run_mock.call_count == 2
        run_mock.assert_any_call(["git", "push", "origin", branch.value])
        run_mock.assert_any_call(["git", "push", "origin", "--tags"])

    @patch("scripts.release.infrastructure.vcs.git_version_control.run")
    def test_push_without_tags_calls_git_push_only(
        self,
        run_mock,
    ) -> None:
        vcs = GitVersionControl()
        branch = ReleaseBranchName("release/v1.2.3")

        vcs.push(branch, push_tags=False)

        run_mock.assert_called_once_with(["git", "push", "origin", branch.value])
