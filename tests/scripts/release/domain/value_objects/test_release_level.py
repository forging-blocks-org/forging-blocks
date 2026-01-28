import pytest
from scripts.release.domain.errors.invalid_release_level_error import (
    InvalidReleaseLevelError,
)
from scripts.release.domain.value_objects.release_level import (
    ReleaseLevel,
    ReleaseLevelEnum,
)


@pytest.mark.unit
class TestReleaseLevel:
    def test_init_when_valid_enum_then_success(self) -> None:
        level = ReleaseLevel(ReleaseLevelEnum.PATCH)

        assert level.value == "patch"

    def test_from_str_when_valid_patch_then_release_level_created(self) -> None:
        level = ReleaseLevel.from_str("PATCH")

        assert level.value == "patch"

    def test_from_str_when_valid_minor_then_release_level_created(self) -> None:
        level = ReleaseLevel.from_str("MINOR")

        assert level.value == "minor"

    def test_from_str_when_valid_major_then_release_level_created(self) -> None:
        level = ReleaseLevel.from_str("MAJOR")

        assert level.value == "major"

    def test_from_str_when_invalid_value_then_error(self) -> None:
        with pytest.raises(InvalidReleaseLevelError):
            ReleaseLevel.from_str("hotfix")

    def test_equality_components_when_same_level_then_equal(self) -> None:
        level_1 = ReleaseLevel.from_str("PATCH")
        level_2 = ReleaseLevel.from_str("PATCH")

        assert level_1 == level_2

    def test_equality_components_when_different_level_then_not_equal(self) -> None:
        level_1 = ReleaseLevel.from_str("PATCH")
        level_2 = ReleaseLevel.from_str("MINOR")

        assert level_1 != level_2
