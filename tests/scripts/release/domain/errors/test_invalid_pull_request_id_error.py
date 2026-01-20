from scripts.release.domain.errors.invalid_pull_request_id_error import InvalidPullRequestIdError


class TestInvalidPullRequestIdError:
    def test_invalid_pull_request_error_message(self) -> None:
        pull_request_id = "123"

        error = InvalidPullRequestError("PR #123 is invalid.")

        assert str(error) == "PR #123 is invalid."
