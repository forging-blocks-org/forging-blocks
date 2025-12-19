from scripts.release.domain.value_objects import PullRequestBase


class TestPullRequestBase:
    def test_init_when_value_is_main_then_is_main_returns_true(self) -> None:
        base = PullRequestBase("main")

        assert base.is_main() is True
        assert base.value == "main"

    def test_init_when_value_is_not_main_then_is_main_returns_false(self) -> None:
        base = PullRequestBase("develop")

        assert base.is_main() is False
        assert base.value == "develop"

    def test_equality_when_same_value_then_equal(self) -> None:
        base_1 = PullRequestBase("main")
        base_2 = PullRequestBase("main")

        assert base_1 == base_2

    def test_equality_when_different_value_then_not_equal(self) -> None:
        base_1 = PullRequestBase("main")
        base_2 = PullRequestBase("develop")

        assert base_1 != base_2
