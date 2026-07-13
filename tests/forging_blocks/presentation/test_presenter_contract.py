# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
"""Tests for PresenterPort contract."""

import pytest

from forging_blocks.presentation import PresenterPort


class FakeResponse:
    """A simple response type used in tests."""

    def __init__(self, summary: str) -> None:
        self.summary = summary


class StubPresenter(PresenterPort[FakeResponse]):
    """A stub implementation of PresenterPort for testing."""

    def __init__(self) -> None:
        self.presented: list[FakeResponse] = []
        self.errors: list[object] = []

    def present(self, response: FakeResponse) -> None:
        self.presented.append(response)

    def present_error(self, error: object) -> None:
        self.errors.append(error)


@pytest.mark.unit
class TestPresenterContract:
    """Verify that PresenterPort can be implemented and used via the protocol."""

    def test_present_delegates_to_implementation(self) -> None:
        presenter = StubPresenter()
        response = FakeResponse("all good")

        presenter.present(response)

        assert presenter.presented == [response]

    def test_present_error_delegates_to_implementation(self) -> None:
        presenter = StubPresenter()
        error = RuntimeError("boom")

        presenter.present_error(error)

        assert presenter.errors == [error]

    def test_implementation_satisfies_protocol(self) -> None:
        """StubPresenter must be recognised as a PresenterPort at runtime."""
        presenter = StubPresenter()
        assert isinstance(presenter, PresenterPort)

    def test_different_response_types_can_be_used(self) -> None:
        class StringPresenter(PresenterPort[str]):
            def present(self, response: str) -> None:  # noqa: ARG002
                pass

            def present_error(self, error: object) -> None:  # noqa: ARG002
                pass

        presenter = StringPresenter()
        presenter.present("hello")
        assert isinstance(presenter, PresenterPort)
