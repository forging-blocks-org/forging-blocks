import pytest

from scripts.release.domain.value_objects import (
    PullRequestBase,
    PullRequestBody,
    PullRequestHead,
    ReleaseBranchName,
    ReleaseVersion,
)
from scripts.release.domain.value_objects.pull_request_title import PullRequestTitle
from scripts.release.domain.value_objects.common import (
    PullRequestTitleLengthBoundaries,
)
from scripts.release.domain.errors.invalid_pull_request_title_error import (
    InvalidPullRequestTitleError,
)


class TestPullRequestTitle:
    def test_init_when_valid_then_success(self) -> None:
        title = PullRequestTitle("release: 1.2.3")
        assert title.value == "release: 1.2.3"

    def test_init_invalid_then_raise_error(self) -> None:
        with pytest.raises(InvalidPullRequestTitleError):
            PullRequestTitle("")

    def test_given_too_short_title_when_construct_then_error(self) -> None:
        too_short = "a" * (PullRequestTitleLengthBoundaries.MIN - 1)

        with pytest.raises(InvalidPullRequestTitleError):
            PullRequestTitle(too_short)

    def test_given_too_long_title_when_construct_then_error(self) -> None:
        too_long = "a" * (PullRequestTitleLengthBoundaries.MAX + 1)

        with pytest.raises(InvalidPullRequestTitleError):
            PullRequestTitle(too_long)

    def test_given_boundary_min_length_when_construct_then_success(self) -> None:
        title = PullRequestTitle("a" * PullRequestTitleLengthBoundaries.MIN)
        assert len(title.value) == PullRequestTitleLengthBoundaries.MIN

    def test_given_boundary_max_length_when_construct_then_success(self) -> None:
        title = PullRequestTitle("a" * PullRequestTitleLengthBoundaries.MAX)
        assert len(title.value) == PullRequestTitleLengthBoundaries.MAX

    def test_given_same_value_when_compare_then_equal(self) -> None:
        assert PullRequestTitle("release: 1.0.0") == PullRequestTitle("release: 1.0.0")

    def test_given_different_value_when_compare_then_not_equal(self) -> None:
        assert PullRequestTitle("release: 1.0.0") != PullRequestTitle("release: 2.0.0")
