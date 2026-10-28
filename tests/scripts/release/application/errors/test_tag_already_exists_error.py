import pytest

from scripts.release.application.errors import TagAlreadyExistsError


@pytest.mark.unit
class TestTagAlreadyExistsError:
    def test_tag_already_exists_error(self):
        error = TagAlreadyExistsError("v1.0.0")

        assert str(error) == "TagAlreadyExistsError: Tag 'v1.0.0' already exists."
