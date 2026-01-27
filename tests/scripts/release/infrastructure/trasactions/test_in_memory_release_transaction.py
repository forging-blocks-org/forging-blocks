import pytest

from scripts.release.application.workflow import ReleaseStep
from scripts.release.infrastructure.transactions.in_memory_release_transaction import (
    InMemoryReleaseTransaction,
)


@pytest.mark.unit
class TestInMemoryReleaseTransaction:
    async def test_session_when_accessed_then_returns_true(self) -> None:
        transaction = InMemoryReleaseTransaction()

        async with transaction:
            session = transaction.session

        assert session is True

    async def test_commit_when_no_exception_then_commit_called(self) -> None:
        transaction = InMemoryReleaseTransaction()

        # Should not raise
        async with transaction:
            pass

    async def test_rollback_when_exception_then_undo_steps_in_reverse_order(
        self,
    ) -> None:
        transaction = InMemoryReleaseTransaction()
        undo_calls: list[int] = []

        transaction.register_step(ReleaseStep("step_1", lambda: undo_calls.append(1)))
        transaction.register_step(ReleaseStep("step_2", lambda: undo_calls.append(2)))
        transaction.register_step(ReleaseStep("step_3", lambda: undo_calls.append(3)))

        with pytest.raises(RuntimeError):
            async with transaction:
                raise RuntimeError("force rollback")

        assert undo_calls == [3, 2, 1]

    async def test_rollback_when_step_fails_then_continue_undoing(self) -> None:
        transaction = InMemoryReleaseTransaction()
        calls: list[str] = []

        transaction.register_step(ReleaseStep("ok_1", lambda: calls.append("1")))
        transaction.register_step(
            ReleaseStep("fail", lambda: (_ for _ in ()).throw(RuntimeError()))
        )
        transaction.register_step(ReleaseStep("ok_3", lambda: calls.append("3")))

        with pytest.raises(RuntimeError):
            async with transaction:
                raise RuntimeError("force rollback")

        assert calls == ["3", "1"]
