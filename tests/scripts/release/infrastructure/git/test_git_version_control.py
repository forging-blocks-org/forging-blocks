from __future__ import annotations

from scripts.release.infrastructure.git.git_version_control import GitVersionControl
from scripts.release.domain.value_objects import ReleaseBranchName, TagName


class TestGitVersionControlIntegration:
    def test_branch_lifecycle_when_created_then_exists_and_deleted(
        self,
        git_repo: GitTestRepository,
    ) -> None:
        # Arrange
        version_control = GitVersionControl()
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
        version_control = GitVersionControl()
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
        version_control = GitVersionControl()
        git_repo.write_file("CHANGELOG.md", "changes")

        # Act
        version_control.commit_release_artifacts()

        # Assert
        assert git_repo.last_commit_message() == "chore(release): prepare release"
