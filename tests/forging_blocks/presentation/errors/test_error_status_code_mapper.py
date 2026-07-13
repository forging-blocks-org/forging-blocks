# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for ErrorStatusCodeMapper."""

import pytest

from forging_blocks.presentation import ErrorStatusCodeMapper
from forging_blocks.presentation.errors.error_message_model import ErrorMessageModel
from forging_blocks.presentation.errors.error_view_model import ErrorViewModel


@pytest.mark.unit
class TestErrorStatusCodeMapper:
    """Tests for ErrorStatusCodeMapper."""

    def test_maps_validation_error_to_400(self) -> None:
        mapper = ErrorStatusCodeMapper()
        msg = ErrorMessageModel(title="Invalid", code="ValidationError")
        view_model = ErrorViewModel(messages=[msg])

        result = mapper.map(view_model)

        assert result.messages[0].status_code == 400

    def test_maps_rule_violation_to_409(self) -> None:
        mapper = ErrorStatusCodeMapper()
        msg = ErrorMessageModel(title="Conflict", code="RuleViolationError")
        view_model = ErrorViewModel(messages=[msg])

        result = mapper.map(view_model)

        assert result.messages[0].status_code == 409

    def test_maps_combined_errors_to_422(self) -> None:
        mapper = ErrorStatusCodeMapper()
        msg = ErrorMessageModel(title="Multiple", code="CombinedErrors")
        view_model = ErrorViewModel(messages=[msg])

        result = mapper.map(view_model)

        assert result.messages[0].status_code == 422

    def test_maps_unknown_code_to_500(self) -> None:
        mapper = ErrorStatusCodeMapper()
        msg = ErrorMessageModel(title="Boom", code="SomethingElse")
        view_model = ErrorViewModel(messages=[msg])

        result = mapper.map(view_model)

        assert result.messages[0].status_code == 500

    def test_maps_none_code_to_500(self) -> None:
        mapper = ErrorStatusCodeMapper()
        msg = ErrorMessageModel(title="No code")
        view_model = ErrorViewModel(messages=[msg])

        result = mapper.map(view_model)

        assert result.messages[0].status_code == 500
