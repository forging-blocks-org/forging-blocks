from typing import Any
from unittest.mock import AsyncMock

import pytest
from pytest import fixture

from building_blocks.application.ports.outbound.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    @property
    def session(self) -> Any | None:
        return None

    async def commit(self):
        print("committed")

    async def rollback(self):
        print("rolled back")


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

    @pytest.mark.asyncio
    async def test_aexit_when_no_exception_then_commit_is_called(
        self, unit_of_work: FakeUnitOfWork
    ) -> None:
        """Tests that `commit()` is called when exiting the context manager without an
        exception.
        """
        unit_of_work.commit = AsyncMock()
        unit_of_work.rollback = AsyncMock()

        async with unit_of_work:
            pass

        unit_of_work.commit.assert_called_once()
        unit_of_work.rollback.assert_not_called()

    @pytest.mark.asyncio
    async def test_aexit_when_exception_occurs_then_rollback_is_called(
        self, unit_of_work: FakeUnitOfWork
    ) -> None:
        """Tests that `rollback()` is called when exiting the context manager with an
        exception.
        """
        unit_of_work.commit = AsyncMock()
        unit_of_work.rollback = AsyncMock()

        class TestException(Exception):
            pass

        with pytest.raises(TestException):
            async with unit_of_work:
                raise TestException()

        unit_of_work.rollback.assert_called_once()
        unit_of_work.commit.assert_not_called()
