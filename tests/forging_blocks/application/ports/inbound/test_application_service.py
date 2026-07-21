import pytest

from forging_blocks.application.ports.inbound.application_service_port import ApplicationServicePort
from forging_blocks.foundation.result import Err, Ok


@pytest.mark.unit
class TestApplicationService:
    async def test_when_implementation_returns_ok_then_is_ok(self) -> None:
        class RegisterUserService:
            async def execute(self, request: str) -> Ok[str, object]:
                del request
                return Ok("user-42")

        service = RegisterUserService()
        assert isinstance(service, ApplicationServicePort)

        result = await service.execute("register")
        assert result.is_ok
        assert result.value == "user-42"

    async def test_when_implementation_returns_err_then_is_err(self) -> None:
        class FailingService:
            async def execute(self, request: str) -> Err[object, str]:
                del request
                return Err("failed")

        result = await FailingService().execute("boom")
        assert result.is_err
        assert result.error == "failed"

    async def test_when_protocol_not_implemented_then_not_instance(self) -> None:
        class NotAService:
            pass

        assert not isinstance(NotAService(), ApplicationServicePort)
