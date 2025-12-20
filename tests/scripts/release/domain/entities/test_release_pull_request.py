from unittest.mock import Mock
import pytest
from scripts.release.domain.entities import ReleasePullRequest
from scripts.release.domain.errors import InvalidReleasePullRequestError
from scripts.release.domain.value_objects import (
    PullRequestBase,
    PullRequestBody,
    PullRequestHead,
    PullRequestTitle,
    ReleaseBranchName,
    ReleaseVersion,
)


class TestReleasePullRequest:
    def test_init_when_base_is_main_and_head_is_release_then_success(self) -> None:
        pr = ReleasePullRequest(
            base=PullRequestBase("main"),
            head=PullRequestHead(ReleaseBranchName("release/v1.2.3")),
            title=PullRequestTitle("Release v1.2.3"),
            body=PullRequestBody("Release notes"),
        )

        assert pr.is_persisted() is False

    def test_init_when_base_is_not_main_then_error(self) -> None:
        with pytest.raises(InvalidReleasePullRequestError):
            ReleasePullRequest(
                base=PullRequestBase("develop"),
                head=PullRequestHead(ReleaseBranchName("release/v1.2.3")),
                title=PullRequestTitle("Release v1.2.3"),
                body=PullRequestBody("Release notes"),
            )

    def test_init_when_head_is_not_release_branch_then_error(self) -> None:
        # Assuming ReleaseBranchName enforces format,
        # this test documents the invariant at entity level.
        with pytest.raises(InvalidReleasePullRequestError):
            ReleasePullRequest(
                base=PullRequestBase("main"),
                head=Mock(spec=PullRequestHead, is_release_branch=lambda: False),
                title=PullRequestTitle("Release v1.2.3"),
                body=PullRequestBody("Release notes"),
            )

    def test_identity_when_pr_id_is_given_then_entity_is_persisted(self) -> None:
        pr = ReleasePullRequest(
            pr_id="123",
            base=PullRequestBase("main"),
            head=PullRequestHead(ReleaseBranchName("release/v1.2.3")),
            title=PullRequestTitle("Release v1.2.3"),
            body=PullRequestBody("Release notes"),
        )

        assert pr.is_persisted() is True

    def test_properties_return_correct_value_objects(self) -> None:
        version = ReleaseVersion(1, 2, 3)
        release_branch_name = ReleaseBranchName.from_version(version)

        base = PullRequestBase("main")
        head = PullRequestHead(release_branch_name)
        title = PullRequestTitle("release: 1.2.3")
        body = PullRequestBody("This is a release pull request.")

        pr = ReleasePullRequest(
            base=base,
            head=head,
            title=title,
            body=body,
        )

        assert pr.base == base
        assert pr.head == head
        assert pr.title == title
        assert pr.body == body
