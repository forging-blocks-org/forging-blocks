# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.foundation.permission import Permission


@pytest.mark.unit
class TestPermission:
    def test_read_permission_is_read_string(self) -> None:
        assert Permission.READ == "read"

    def test_write_permission_is_write_string(self) -> None:
        assert Permission.WRITE == "write"

    def test_delete_permission_is_delete_string(self) -> None:
        assert Permission.DELETE == "delete"

    def test_admin_permission_is_admin_string(self) -> None:
        assert Permission.ADMIN == "admin"
