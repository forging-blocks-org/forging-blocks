import pytest

from scripts.release.domain.errors import InvalidTagNameError
from scripts.release.domain.value_objects import ReleaseVersion, TagName


@pytest.mark.unit
class TestTagName:
    @pytest.mark.parametrize(
        "value",
        [
            pytest.param("1.2.3", id="missing_prefix"),
            pytest.param("version/1.2.3", id="wrong_prefix"),
        ],
    )
    def test_init_when_invalid_prefix_then_error(self, value: str) -> None:
        with pytest.raises(InvalidTagNameError):
            TagName(value)

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param("v1.2", id="too_few_parts"),
            pytest.param("v1.2.3.4", id="too_many_parts"),
        ],
    )
    def test_init_when_invalid_structure_then_error(self, value: str) -> None:
        with pytest.raises(InvalidTagNameError):
            TagName(value)

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param("v1.-2.3", id="negative_minor"),
            pytest.param("v1.a.3", id="non_numeric"),
        ],
    )
    def test_init_when_invalid_version_then_error(self, value: str) -> None:
        with pytest.raises(InvalidTagNameError):
            TagName(value)

    def test_for_version_when_valid_release_version_then_tag_created(self) -> None:
        version = ReleaseVersion(1, 2, 3)

        tag = TagName.for_version(version)

        assert tag.value == "v1.2.3"

    def test_equality_when_same_value_then_equal(self) -> None:
        assert TagName("v2.0.0") == TagName("v2.0.0")

    def test_equality_when_different_value_then_not_equal(self) -> None:
        assert TagName("v1.0.0") != TagName("v2.0.0")

    def test_value_when_called_then_returns_raw_value(self) -> None:
        tag = TagName("v1.2.3")

        assert tag.value == "v1.2.3"

    def test_init_when_created_then_cannot_modify_value(self) -> None:
        tag = TagName("v1.2.3")

        with pytest.raises(AttributeError):
            tag._value = "v9.9.9"  # type: ignore

    def test_debug_tagname_module(self) -> None:
        from scripts.release.domain.value_objects.tag_name import (
            TagName as DirectTagName,
        )

        from scripts.release.domain.value_objects import TagName as ImportedTagName

        assert DirectTagName is ImportedTagName

    def test_init_when_valid_tag_then_success(self) -> None:
        tag = TagName("v1.2.3")

        assert tag.value == "v1.2.3"

    def test_for_version_when_called_then_returns_tag(self) -> None:
        version = ReleaseVersion(2, 1, 0)

        tag = TagName.for_version(version)

        assert tag.value == "v2.1.0"

    def test_equality_components_when_called_then_returns_tuple(self) -> None:
        tag = TagName("v1.0.0")

        assert tag._equality_components() == ("v1.0.0",)
