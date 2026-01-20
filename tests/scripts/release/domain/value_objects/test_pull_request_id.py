from typing import Any
import pytest

from forging_blocks.foundation.result import Err, Ok
from release.domain.errors import InvalidPullRequestIdError
from release.domain.value_objects.pull_request_id import PullRequestId


class TestPullRequestId:
    def test_instance_is_immutable(self) -> None:
        id = PullRequestId(5)

        with pytest.raises(AttributeError):
            id._value = "5" # type: ignore

    @pytest.mark.parametrize(
        "id_value, expected_type", [
            pytest.param(5, Ok(PullRequestId).__class__, id="valid_int_value"),
            pytest.param("5", Ok(PullRequestId).__class__, id="valid_str_value"),
            pytest.param(-5, Err(InvalidPullRequestIdError).__class__, id="invalid_int_value"),
            pytest.param("-5", Err(InvalidPullRequestIdError).__class__, id="invalid_str_value"),
            pytest.param(0, Err(InvalidPullRequestIdError).__class__, id="invalid_int_zero_value"),
            pytest.param("0", Err(InvalidPullRequestIdError).__class__, id="invalid_str_zero_value"),
        ],
    )
    def test_create(self, id_value: Any, expected_type: Any) -> None:
        result = PullRequestId.create(id_value)

        assert isinstance(result, expected_type)

    @pytest.mark.parametrize(
        "id_value, expected_value", [
            pytest.param(5, 5),
            pytest.param(-5, -5),
        ],
    )
    def test_value_property_when_called_then_return_original_value(
        self,
        id_value: Any,
        expected_value: Any
    ) -> None:
        id = PullRequestId(id_value)

        assert expected_value == id.value

    @pytest.mark.parametrize(
        "id_value, expected_equality_components, expected_type", [
            pytest.param(5, (5,), tuple[int]),
            pytest.param(-5, (-5,), tuple[int]),
            pytest.param("5", ("5",), tuple[str]),
            pytest.param("-5", ("-5",), tuple[str]),
        ],
    )
    def test_equality_components_when_called_then_return_tuple_with_the_original_value(
        self,
        id_value: int,
        expected_equality_components: Any,
        expected_type: Any,
    ) -> None:
        id = PullRequestId(id_value)

        assert expected_type == type(id)
        assert expected_type

