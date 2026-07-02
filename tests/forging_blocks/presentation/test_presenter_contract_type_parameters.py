# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
"""Tests for PresenterPort generic type parameters."""

import pytest

from forging_blocks.presentation import PresenterPort


@pytest.mark.unit
class TestPresenterContractTypeParameters:
    """Verify the generic type parameter is respected."""

    def test_different_response_types_can_be_used(self) -> None:
        class StringPresenter(PresenterPort[str]):
            def present(self, response: str) -> None:  # noqa: ARG002
                pass

            def present_error(self, error: object) -> None:  # noqa: ARG002
                pass

        presenter = StringPresenter()
        presenter.present("hello")
        assert isinstance(presenter, PresenterPort)
