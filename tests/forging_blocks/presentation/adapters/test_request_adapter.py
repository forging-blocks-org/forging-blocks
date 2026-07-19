# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for RequestAdapter protocol."""

import pytest
from tests.forging_blocks.presentation.conftest import (
    DictRequest,
    FakeRequestAdapter,
)


@pytest.mark.unit
class TestRequestAdapter:
    """Tests for RequestAdapter protocol."""

    def test_adapter_translates_raw_to_input(self) -> None:
        adapter = FakeRequestAdapter()

        result = adapter.adapt(DictRequest({"name": "Alice"}))

        assert result == "Alice"
