"""Tests for the InitParameterExtractor helper."""

from unittest.mock import patch

import pytest

from forging_blocks.foundation.ports.helpers._init_parameter_extractor import (
    InitParameterExtractor,
)


@pytest.mark.unit
class TestInitParameterExtractor:
    def test_extracts_annotated_parameters(self) -> None:
        """Returns a dict mapping parameter names to their type annotations."""

        class Target:
            def __init__(self, name: str, count: int) -> None: ...

        extractor = InitParameterExtractor(Target)
        params = extractor.extract()

        assert params == {"name": str, "count": int}

    def test_excludes_return_annotation(self) -> None:
        """The 'return' key is stripped from the result."""

        class Target:
            def __init__(self) -> None: ...

        extractor = InitParameterExtractor(Target)
        params = extractor.extract()

        assert "return" not in params

    def test_returns_empty_dict_when_get_type_hints_raises(self) -> None:
        """Returns {} when get_type_hints raises an exception (lines 24-25)."""

        class Crasher:
            def __init__(self, bad) -> None: ...

        with patch(
            "forging_blocks.foundation.ports.helpers._init_parameter_extractor.get_type_hints",
            side_effect=TypeError("cannot resolve"),
        ):
            extractor = InitParameterExtractor(Crasher)
            params = extractor.extract()

        assert params == {}
