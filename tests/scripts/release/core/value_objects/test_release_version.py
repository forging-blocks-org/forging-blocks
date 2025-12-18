import pytest

from scripts.release.core.value_objects.release_version import ReleaseVersion
from scripts.release.core.errors.invalid_release_version_error import (
    InvalidReleaseVersionError,
)


class TestReleaseVersion:
    @pytest.mark.parametrize(
        "major, minor, patch", [(1, 1, -1), (1, -1, 1), (-1, 1, 1)]
    )
    def test_init_when_invalid_version_than_raise_invalid_relese_version_error(
        self, major: int, minor: int, patch: int
    ) -> None:
        with pytest.raises(InvalidReleaseVersionError):
            ReleaseVersion(major, minor, patch)

    @pytest.mark.parametrize(
        "major, minor, patch, expected",
        [(0, 4, 2, "0.4.2"), (1, 3, 2, "1.3.2"), (4, 1, 8, "4.1.8")],
    )
    def test_value_property_when_called_then_return_version_like_string(
        self, major: int, minor: int, patch: int, expected: str
    ) -> None:
        version = ReleaseVersion(major, minor, patch)

        version_value = version.value

        assert expected == version_value
