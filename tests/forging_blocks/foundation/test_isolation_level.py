# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.foundation.isolation_level import IsolationLevel


@pytest.mark.unit
class TestIsolationLevel:
    def test_read_uncommitted_is_correct_string(self) -> None:
        assert IsolationLevel.READ_UNCOMMITTED == "read_uncommitted"

    def test_read_committed_is_correct_string(self) -> None:
        assert IsolationLevel.READ_COMMITTED == "read_committed"

    def test_repeatable_read_is_correct_string(self) -> None:
        assert IsolationLevel.REPEATABLE_READ == "repeatable_read"

    def test_serializable_is_correct_string(self) -> None:
        assert IsolationLevel.SERIALIZABLE == "serializable"
