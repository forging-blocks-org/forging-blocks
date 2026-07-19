# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for the ErrorPresenter."""

import pytest

from forging_blocks.foundation import Error, ErrorMessage, ErrorMetadata
from forging_blocks.foundation.result import Err
from forging_blocks.presentation import ErrorPresenter, ErrorViewModel


@pytest.mark.unit
class TestErrorPresenter:
    """Behavioural tests for ErrorPresenter.to_view_model()."""

    def test_present_framework_error_returns_view_model_with_title(self) -> None:
        presenter = ErrorPresenter()
        error = Error(ErrorMessage("Something went wrong"))

        result = presenter.to_view_model(error)

        assert isinstance(result, ErrorViewModel)
        assert len(result.messages) == 1
        assert result.messages[0].title == "Something went wrong"

    def test_present_framework_error_includes_error_code(self) -> None:
        presenter = ErrorPresenter()
        error = Error(ErrorMessage("Boom"))

        result = presenter.to_view_model(error)

        assert result.messages[0].code == "Error"

    def test_present_framework_error_extracts_detail_from_metadata(self) -> None:
        presenter = ErrorPresenter()
        metadata = ErrorMetadata({"detail": "Please check your input"})
        error = Error(ErrorMessage("Validation failed"), metadata)

        result = presenter.to_view_model(error)

        assert result.messages[0].detail == "Please check your input"

    def test_present_framework_error_extracts_field_from_metadata(self) -> None:
        presenter = ErrorPresenter()
        metadata = ErrorMetadata({"field": "email"})
        error = Error(ErrorMessage("Invalid value"), metadata)

        result = presenter.to_view_model(error)

        assert result.messages[0].field == "email"

    def test_present_framework_error_without_detail_returns_none_detail(self) -> None:
        presenter = ErrorPresenter()
        error = Error(ErrorMessage("Oops"))

        result = presenter.to_view_model(error)

        assert result.messages[0].detail is None

    def test_present_framework_error_without_field_returns_none_field(self) -> None:
        presenter = ErrorPresenter()
        error = Error(ErrorMessage("Oops"))

        result = presenter.to_view_model(error)

        assert result.messages[0].field is None

    def test_present_result_err_unwraps_inner_error(self) -> None:
        presenter = ErrorPresenter()
        inner = Error(ErrorMessage("Inner failure"))
        err_result = Err(inner)

        result = presenter.to_view_model(err_result)

        assert len(result.messages) == 1
        assert result.messages[0].title == "Inner failure"
        assert result.messages[0].code == "Error"

    def test_present_result_err_with_nested_framework_error(self) -> None:
        """An Err wrapping a framework Error should yield the framework error details."""
        presenter = ErrorPresenter()
        metadata = ErrorMetadata({"detail": "Nested issue", "field": "username"})
        inner = Error(ErrorMessage("Nested error"), metadata)
        err_result = Err(inner)

        result = presenter.to_view_model(err_result)

        message = result.messages[0]
        assert message.title == "Nested error"
        assert message.detail == "Nested issue"
        assert message.field == "username"

    def test_present_plain_exception_uses_str_as_title(self) -> None:
        presenter = ErrorPresenter()
        exc = ValueError("invalid literal")

        result = presenter.to_view_model(exc)

        assert len(result.messages) == 1
        assert result.messages[0].title == "invalid literal"
        assert result.messages[0].code == "ValueError"

    def test_present_plain_exception_with_no_args(self) -> None:
        presenter = ErrorPresenter()
        exc = RuntimeError()

        result = presenter.to_view_model(exc)

        assert result.messages[0].title == ""
        assert result.messages[0].code == "RuntimeError"

    def test_present_unknown_object_uses_str_fallback(self) -> None:
        presenter = ErrorPresenter()
        unknown = 42

        result = presenter.to_view_model(unknown)

        assert len(result.messages) == 1
        assert result.messages[0].title == "42"
        assert result.messages[0].code == "UnknownError"

    def test_present_none_returns_fallback(self) -> None:
        presenter = ErrorPresenter()

        result = presenter.to_view_model(None)

        assert result.messages[0].title == "None"
        assert result.messages[0].code == "UnknownError"

    def test_present_combined_errors_decomposes_into_individual_messages(self) -> None:
        from forging_blocks.foundation import CombinedErrors

        presenter = ErrorPresenter()
        inner1 = Error(ErrorMessage("First error"))
        inner2 = Error(ErrorMessage("Second error"))
        combined = CombinedErrors([inner1, inner2])

        result = presenter.to_view_model(combined)

        assert len(result.messages) == 2
        assert result.messages[0].title == "First error"
        assert result.messages[1].title == "Second error"

    def test_present_combined_errors_preserves_child_details(self) -> None:
        from forging_blocks.foundation import CombinedErrors

        presenter = ErrorPresenter()
        metadata = ErrorMetadata({"detail": "Child detail", "field": "child_field"})
        inner = Error(ErrorMessage("Child error"), metadata)
        combined = CombinedErrors([inner])

        result = presenter.to_view_model(combined)

        assert len(result.messages) == 1
        assert result.messages[0].title == "Child error"
        assert result.messages[0].detail == "Child detail"
        assert result.messages[0].field == "child_field"

    def test_present_empty_combined_errors_produces_fallback_message(self) -> None:
        from forging_blocks.foundation import CombinedErrors

        presenter = ErrorPresenter()
        combined = CombinedErrors([])

        result = presenter.to_view_model(combined)

        assert len(result.messages) == 1
        assert result.messages[0].title == "No errors specified"
        assert result.messages[0].code == "CombinedErrors"

    def test_present_combined_validation_errors_decomposes_correctly(self) -> None:
        from forging_blocks.foundation import (
            CombinedValidationErrors,
            FieldReference,
            ValidationError,
            ValidationFieldErrors,
        )

        presenter = ErrorPresenter()
        inner1 = ValidationFieldErrors(
            FieldReference("name"), [ValidationError(ErrorMessage("Too short"))]
        )
        inner2 = ValidationFieldErrors(
            FieldReference("email"), [ValidationError(ErrorMessage("Invalid format"))]
        )
        combined = CombinedValidationErrors([inner1, inner2])

        result = presenter.to_view_model(combined)

        assert len(result.messages) == 2
        assert result.messages[0].title == "Too short"
        assert result.messages[1].title == "Invalid format"

    def test_present_combined_rule_violation_errors_decomposes_correctly(self) -> None:
        from forging_blocks.foundation import (
            CombinedRuleViolationErrors,
            RuleViolationError,
        )

        presenter = ErrorPresenter()
        inner = RuleViolationError(ErrorMessage("Rule broken"))
        combined = CombinedRuleViolationErrors([inner])

        result = presenter.to_view_model(combined)

        assert len(result.messages) == 1
        assert result.messages[0].title == "Rule broken"
        assert result.messages[0].code == "RuleViolationError"

    def test_present_combined_errors_inside_err_decomposes_correctly(self) -> None:
        from forging_blocks.foundation import CombinedErrors

        presenter = ErrorPresenter()
        inner1 = Error(ErrorMessage("Err-wrapped 1"))
        inner2 = Error(ErrorMessage("Err-wrapped 2"))
        combined = CombinedErrors([inner1, inner2])
        err_result = Err(combined)

        result = presenter.to_view_model(err_result)

        assert len(result.messages) == 2
        assert result.messages[0].title == "Err-wrapped 1"
        assert result.messages[1].title == "Err-wrapped 2"

    def test_present_field_errors_decomposes_with_parent_field(self) -> None:
        from forging_blocks.foundation import FieldErrors, FieldReference

        presenter = ErrorPresenter()
        inner = Error(ErrorMessage("Invalid value"))
        field_errors = FieldErrors(FieldReference("username"), [inner])

        result = presenter.to_view_model(field_errors)

        assert len(result.messages) == 1
        assert result.messages[0].title == "Invalid value"
        assert result.messages[0].field == "username"

    def test_present_field_errors_preserves_inner_field_when_present(self) -> None:
        from forging_blocks.foundation import FieldErrors, FieldReference

        presenter = ErrorPresenter()
        metadata = ErrorMetadata({"field": "product_id"})
        inner = Error(ErrorMessage("Not found"), metadata)
        field_errors = FieldErrors(FieldReference("order"), [inner])

        result = presenter.to_view_model(field_errors)

        assert len(result.messages) == 1
        assert result.messages[0].field == "product_id"

    def test_present_field_errors_applies_parent_field_when_child_has_none(
        self,
    ) -> None:
        from forging_blocks.foundation import FieldErrors, FieldReference

        presenter = ErrorPresenter()
        inner = Error(ErrorMessage("Missing"))
        field_errors = FieldErrors(FieldReference("email"), [inner])

        result = presenter.to_view_model(field_errors)

        assert result.messages[0].field == "email"

    def test_present_field_errors_with_multiple_children(self) -> None:
        from forging_blocks.foundation import FieldErrors, FieldReference

        presenter = ErrorPresenter()
        inner1 = Error(ErrorMessage("Too short"))
        inner2 = Error(ErrorMessage("Invalid character"))
        field_errors = FieldErrors(FieldReference("password"), [inner1, inner2])

        result = presenter.to_view_model(field_errors)

        assert len(result.messages) == 2
        assert result.messages[0].title == "Too short"
        assert result.messages[0].field == "password"
        assert result.messages[1].title == "Invalid character"
        assert result.messages[1].field == "password"
