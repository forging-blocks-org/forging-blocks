# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from types import TracebackType
from typing import Self
from unittest.mock import AsyncMock

import pytest
from pytest import fixture

from forging_blocks.application import UnitOfWorkPort


class FakeUnitOfWork(UnitOfWorkPort):
    """A fake Unit Of Work that provides the context-manager behaviour
    expected of a real implementation."""

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass


@pytest.mark.unit
class TestUnitOfWork:
    @fixture
    def unit_of_work(self) -> FakeUnitOfWork:
        return FakeUnitOfWork()

    async def test_aenter_when_context_manager_initialized_then_return_self(
        self, unit_of_work: FakeUnitOfWork
    ) -> None:
        """Tests that entering the context manager returns the UoW instance itself."""
        async with unit_of_work as uow:
            assert uow is unit_of_work

    async def test_aexit_when_no_exception_then_commit_is_called(
        self, unit_of_work: FakeUnitOfWork
    ) -> None:
        """Tests that `commit()` is called when exiting the context manager without an
        exception.
        """
        unit_of_work.commit = AsyncMock()  # type: ignore[method-assign]
        unit_of_work.rollback = AsyncMock()  # type: ignore[method-assign]

        async with unit_of_work:
            pass

        unit_of_work.commit.assert_called_once()
        unit_of_work.rollback.assert_not_called()

    async def test_aexit_when_exception_occurs_then_rollback_is_called(
        self, unit_of_work: FakeUnitOfWork
    ) -> None:
        """Tests that `rollback()` is called when exiting the context manager with an
        exception.
        """
        unit_of_work.commit = AsyncMock()  # type: ignore[method-assign]
        unit_of_work.rollback = AsyncMock()  # type: ignore[method-assign]

        class TestException(Exception):
            pass

        with pytest.raises(TestException):
            async with unit_of_work:
                raise TestException()

        unit_of_work.rollback.assert_called_once()
        unit_of_work.commit.assert_not_called()
