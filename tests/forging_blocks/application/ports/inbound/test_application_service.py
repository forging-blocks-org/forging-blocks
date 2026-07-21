import pytest

from forging_blocks.application.ports.inbound.application_service_port import ApplicationServicePort


@pytest.mark.unit
class TestApplicationService:
    async def test_execute_returns_direct_value(self) -> None:
        """An implementation returns the response type directly (no Result wrapper)."""

        class RegisterUserService(ApplicationServicePort[str, str]):
            async def execute(self, request: str) -> str:
                return f"created-{request}"

        service = RegisterUserService()
        assert isinstance(service, ApplicationServicePort)
        assert await service.execute("alice") == "created-alice"

    async def test_isinstance_requires_explicit_inheritance(self) -> None:
        """Without explicit inheritance, isinstance is False —
        there is no __subclasshook__ bypass."""

        class DuckTypedService:
            async def execute(self, request: str) -> str:
                del request
                return "result"

        assert not isinstance(DuckTypedService(), ApplicationServicePort)

    async def test_unimplemented_abstract_cannot_instantiate(self) -> None:
        """A class that inherits but does not implement execute
        cannot be instantiated."""

        class IncompleteService(ApplicationServicePort[str, str]):
            pass

        with pytest.raises(TypeError, match="abstract"):
            IncompleteService()  # pyright: ignore[reportAbstractUsage] — intentional runtime check
