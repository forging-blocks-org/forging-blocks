from unittest.mock import Mock
import pytest
from scripts.release.core.entities import ReleasePullRequest
from scripts.release.core.errors import InvalidReleasePullRequestError
from scripts.release.core.value_objects import (
    PullRequestBase,
    PullRequestBody,
    PullRequestHead,
    PullRequestTitle,
    ReleaseBranchName,
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
