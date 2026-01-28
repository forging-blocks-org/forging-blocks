import pytest
from scripts.release.domain.value_objects.release_version import ReleaseVersion

from scripts.release.domain.errors import InvalidReleaseVersionError


@pytest.mark.unit
class TestReleaseVersion:
    @pytest.mark.parametrize(
        "major, minor, patch",
        [
            pytest.param(1, 1, -1, id="negative_patch"),
            pytest.param(1, -1, 1, id="negative_minor"),
            pytest.param(-1, 1, 1, id="negative_major"),
        ],
    )
    def test_init_when_negative_component_then_error(
        self,
        major: int,
        minor: int,
        patch: int,
    ) -> None:
        with pytest.raises(InvalidReleaseVersionError):
            ReleaseVersion(major, minor, patch)

    @pytest.mark.parametrize(
        "major, minor, patch, expected",
        [
            pytest.param(0, 4, 2, "0.4.2", id="valid_0.4.2"),
            pytest.param(1, 3, 2, "1.3.2", id="valid_1.3.2"),
            pytest.param(4, 1, 8, "4.1.8", id="valid_4.1.8"),
        ],
    )
    def test_init_when_valid_version_then_properties_are_consistent(
        self,
        major: int,
        minor: int,
        patch: int,
        expected: str,
    ) -> None:
        version = ReleaseVersion(major, minor, patch)

        assert (
            version.value,
            version.major,
            version.minor,
            version.patch,
        ) == (
            expected,
            major,
            minor,
            patch,
        )
