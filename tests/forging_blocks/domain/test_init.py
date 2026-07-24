import importlib

import pytest


class TestDomainInit:
    def test_when_getattr_called_with_unknown_name_then_raises_attribute_error(self) -> None:
        domain = importlib.import_module("forging_blocks.domain")

        with pytest.raises(AttributeError):
            domain.__getattr__("NonExistent")
