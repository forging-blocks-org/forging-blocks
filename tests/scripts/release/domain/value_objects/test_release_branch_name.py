import pytest
from scripts.release.domain.errors.invalid_release_branch_name_error import (
    InvalidReleaseBranchNameError,
)
from scripts.release.domain.value_objects.release_branch_name import ReleaseBranchName


@pytest.mark.unit
class TestReleaseBranchName:
    @pytest.mark.parametrize(
        "value",
        [
            pytest.param("feature/v1.2.3", id="invalid_prefix"),
            pytest.param("release/v1.2", id="invalid_structure"),
            pytest.param("release/v1.-2.3", id="invalid_version"),
            pytest.param("release/v1.2", id="invalid_version"),
        ],
    )
    def test_init_when_invalid_value_then_error(self, value: str) -> None:
        with pytest.raises(InvalidReleaseBranchNameError):
            ReleaseBranchName(value)

    def test_equality_when_same_value_then_equal(self) -> None:
        assert ReleaseBranchName("release/v1.0.0") == ReleaseBranchName(
            "release/v1.0.0"
        )
