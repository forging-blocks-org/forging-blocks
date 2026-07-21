# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.application.ports.inbound.validation_service import ValidationService
from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.rule_violation_error import RuleViolationError


@pytest.mark.unit
class TestValidationService:
    async def test_when_concrete_implementation_then_returns_command_errors(self) -> None:
        class StrictValidator(ValidationService):
            async def validate_command(self, command: object) -> list[RuleViolationError]:
                return [RuleViolationError(ErrorMessage("invalid"))]

            async def validate_query(self, query: object) -> list[RuleViolationError]:
                del query
                return []

        service = StrictValidator()
        errors = await service.validate_command("data")

        assert len(errors) == 1
        assert str(errors[0]) == "RuleViolationError: invalid"

    async def test_when_valid_query_then_returns_empty(self) -> None:
        class PermissiveValidator(ValidationService):
            async def validate_command(self, command: object) -> list[RuleViolationError]:
                del command
                return []

            async def validate_query(self, query: object) -> list[RuleViolationError]:
                del query
                return []

        service = PermissiveValidator()
        errors = await service.validate_query("any")

        assert errors == []
