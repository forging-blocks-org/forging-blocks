from scripts.release.domain.value_objects import PullRequestHead, ReleaseBranchName


class TestPullRequestHead:
    def test_init_when_given_release_branch_name_then_success(self) -> None:
        branch = ReleaseBranchName("release/v1.2.3")

        head = PullRequestHead(branch)

        assert head.value == "release/v1.2.3"
        assert head.is_release_branch() is True

    def test_equality_when_same_branch_then_equal(self) -> None:
        branch = ReleaseBranchName("release/v1.2.3")

        head_1 = PullRequestHead(branch)
        head_2 = PullRequestHead(branch)

        assert head_1 == head_2

    def test_equality_when_different_branch_then_not_equal(self) -> None:
        head_1 = PullRequestHead(ReleaseBranchName("release/v1.2.3"))
        head_2 = PullRequestHead(ReleaseBranchName("release/v2.0.0"))

        assert head_1 != head_2
