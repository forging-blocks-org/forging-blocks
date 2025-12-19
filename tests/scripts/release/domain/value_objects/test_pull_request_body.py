import pytest

from scripts.release.domain.value_objects import PullRequestBody


class TestPullRequestBody:
    @pytest.fixture
    def body(self) -> PullRequestBody:
        return PullRequestBody("Foo")

    def test_init_when_called_then_cant_moodify_immutable_attribute_error(
        self, body: PullRequestBody
    ) -> None:
        pr_body = body

        with pytest.raises(AttributeError):
            pr_body._value = "Bar"

    def test_value_property_when_called_then_return_raw_value(
        self, body: PullRequestBody
    ) -> None:
        raw_value = body.value

        expected_value = "Foo"
        assert expected_value == raw_value
