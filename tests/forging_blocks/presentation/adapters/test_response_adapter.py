# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for ResponseAdapter protocol."""

import pytest
from tests.forging_blocks.presentation.conftest import FakeResponseAdapter

from forging_blocks.presentation.errors.error_message_model import ErrorMessageModel
from forging_blocks.presentation.errors.error_view_model import ErrorViewModel


@pytest.mark.unit
class TestResponseAdapter:
    """Tests for ResponseAdapter protocol."""

    def test_adapter_translates_output_to_response(self) -> None:
        adapter = FakeResponseAdapter()

        result = adapter.adapt("hello")

        assert result.body == {"result": "hello"}
        assert result.status == 200

    def test_adapt_error_translates_view_model_to_response(self) -> None:
        adapter = FakeResponseAdapter()
        msg = ErrorMessageModel(title="Not found", code="NotFound", status_code=404)
        view_model = ErrorViewModel(messages=[msg])

        result = adapter.adapt_error(view_model)

        assert result.status == 404
        assert result.body == {
            "errors": [{"title": "Not found", "status_code": 404, "code": "NotFound"}]
        }
