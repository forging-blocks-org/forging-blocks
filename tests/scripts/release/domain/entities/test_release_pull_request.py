import pytest

from scripts.release.domain.entities import ReleasePullRequest
from scripts.release.domain.errors import InvalidReleasePullRequestError
from scripts.release.domain.value_objects import (
    ReleaseBranchName,
    ReleaseVersion,
)


@pytest.mark.unit
class TestReleasePullRequest:
    def test_init_when_base_is_main_and_head_is_release_then_success(self) -> None:
        pr = ReleasePullRequest(
            base="main",
            head=ReleaseBranchName("release/v1.2.3"),
            title="Release v1.2.3",
            body="Release notes",
        )

        assert pr.base == "main"
        assert pr.head.value == "release/v1.2.3"

    def test_init_when_base_is_not_main_then_error(self) -> None:
        with pytest.raises(InvalidReleasePullRequestError):
            ReleasePullRequest(
                base="develop",
                head=ReleaseBranchName("release/v1.2.3"),
                title="Release v1.2.3",
                body="Release notes",
            )

    def test_properties_return_correct_values(self) -> None:
        version = ReleaseVersion(1, 2, 3)
        release_branch_name = ReleaseBranchName.from_version(version)

        pr = ReleasePullRequest(
            base="main",
            head=release_branch_name,
            title="release: 1.2.3",
            body="This is a release pull request.",
        )

        assert pr.base == "main"
        assert pr.head == release_branch_name
        assert pr.title == "release: 1.2.3"
        assert pr.body == "This is a release pull request."
