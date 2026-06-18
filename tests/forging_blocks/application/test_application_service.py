"""
Tests for the ApplicationService and middleware.
"""

import pytest

from forging_blocks.application.application_service import ApplicationService, MiddlewarePipeline
from forging_blocks.application.middleware import (
    MiddlewareBuilder,
    logging_middleware,
    transaction_middleware,
    validation_middleware,
)
from forging_blocks.application.ports.inbound.use_case import UseCase
from forging_blocks.application.ports.outbound.unit_of_work import UnitOfWork
from forging_blocks.application.service_context import ServiceContext


class TestRequest:
    """Test request for testing."""

    def __init__(self, value: str):
        self.value = value

    def validate(self) -> None:
        if not self.value:
            raise ValueError("Value cannot be empty")


class TestResponse:
    """Test response for testing."""

    def __init__(self, result: str):
        self.result = result


class TestUseCase(UseCase[TestRequest, TestResponse]):
    """Test use case for testing."""

    def __init__(self, should_fail: bool = False):
        self._should_fail = should_fail

    async def execute(self, request: TestRequest) -> TestResponse:
        if self._should_fail:
            raise ValueError("Use case failed")
        return TestResponse(f"Processed: {request.value}")


class TestUnitOfWork(UnitOfWork):
    """Test Unit of Work for testing."""

    def __init__(self):
        self._committed = False
        self._rolled_back = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    async def commit(self) -> None:
        self._committed = True

    async def rollback(self) -> None:
        self._rolled_back = True

    @property
    def committed(self) -> bool:
        return self._committed

    @property
    def rolled_back(self) -> bool:
        return self._rolled_back


class TestApplicationServiceImpl(ApplicationService[dict[str, object]]):
    """Test application service for testing."""

    pass


class TestServiceContext:
    """Tests for ServiceContext."""

    def test_context_creation(self):
        """Test creating a service context."""
        uow = TestUnitOfWork()
        context = ServiceContext(unit_of_work=uow)

        assert context.unit_of_work is uow
        assert context.event_publisher is None

    def test_context_with_event_publisher(self):
        """Test creating a service context with event publisher."""
        uow = TestUnitOfWork()
        context = ServiceContext(unit_of_work=uow, event_publisher=None)

        assert context.unit_of_work is uow
        assert context.event_publisher is None

    def test_context_data_operations(self):
        """Test getting and setting data in context."""
        uow = TestUnitOfWork()
        context = ServiceContext(unit_of_work=uow)

        context.set("key1", "value1")
        assert context.get("key1") == "value1"
        assert context.get("key2", "default") == "default"
        assert "key1" in context
        assert "key2" not in context


class TestApplicationService:
    """Tests for ApplicationService."""

    @pytest.fixture
    def context(self):
        """Create a test service context."""
        uow = TestUnitOfWork()
        return ServiceContext(unit_of_work=uow)

    @pytest.fixture
    def service(self, context):
        """Create a test application service."""
        return TestApplicationServiceImpl(context)

    @pytest.mark.asyncio
    async def test_execute_without_middleware(self, service):
        """Test executing a use case without middleware."""
        use_case = TestUseCase()
        request = TestRequest("test")

        response = await service.execute(use_case, request)

        assert isinstance(response, TestResponse)
        assert response.result == "Processed: test"

    @pytest.mark.asyncio
    async def test_execute_with_middleware(self, service):
        """Test executing a use case with middleware."""
        use_case = TestUseCase()
        request = TestRequest("test")

        executed = []

        async def test_middleware(req, ctx, next_handler):
            executed.append("before")
            result = await next_handler()
            executed.append("after")
            return result

        service.add_middleware(test_middleware)

        response = await service.execute(use_case, request)

        assert executed == ["before", "after"]
        assert response.result == "Processed: test"

    @pytest.mark.asyncio
    async def test_execute_multiple_middlewares(self, service):
        """Test executing with multiple middlewares."""
        use_case = TestUseCase()
        request = TestRequest("test")

        executed = []

        async def middleware1(req, ctx, next_handler):
            executed.append("m1_before")
            result = await next_handler()
            executed.append("m1_after")
            return result

        async def middleware2(req, ctx, next_handler):
            executed.append("m2_before")
            result = await next_handler()
            executed.append("m2_after")
            return result

        service.add_middleware(middleware1)
        service.add_middleware(middleware2)

        response = await service.execute(use_case, request)

        # Middlewares execute in order added, so m1 wraps m2
        assert executed == ["m1_before", "m2_before", "m2_after", "m1_after"]
        assert response.result == "Processed: test"

    @pytest.mark.asyncio
    async def test_execute_with_failing_use_case(self, service):
        """Test executing a failing use case."""
        use_case = TestUseCase(should_fail=True)
        request = TestRequest("test")

        with pytest.raises(ValueError, match="Use case failed"):
            await service.execute(use_case, request)


class TestMiddlewarePipeline:
    """Tests for MiddlewarePipeline."""

    @pytest.mark.asyncio
    async def test_pipeline_execution(self):
        """Test executing a middleware pipeline."""
        pipeline = MiddlewarePipeline[TestRequest, TestResponse, dict[str, object]]()

        executed = []

        async def middleware1(req, ctx, next_handler):
            executed.append("m1_before")
            result = await next_handler()
            executed.append("m1_after")
            return result

        async def middleware2(req, ctx, next_handler):
            executed.append("m2_before")
            result = await next_handler()
            executed.append("m2_after")
            return result

        pipeline.add(middleware1).add(middleware2)

        uow = TestUnitOfWork()
        context = ServiceContext(unit_of_work=uow)

        async def handler():
            executed.append("handler")
            return TestResponse("done")

        response = await pipeline.execute(TestRequest("test"), context, handler)

        assert executed == ["m1_before", "m2_before", "handler", "m2_after", "m1_after"]
        assert response.result == "done"


class TestStandardMiddleware:
    """Tests for standard middleware implementations."""

    @pytest.mark.asyncio
    async def test_logging_middleware(self):
        """Test logging middleware."""
        executed = []

        async def handler():
            executed.append("handler")
            return TestResponse("done")

        uow = TestUnitOfWork()
        context = ServiceContext(unit_of_work=uow)

        response = await logging_middleware(TestRequest("test"), context, handler)

        assert executed == ["handler"]
        assert response.result == "done"

    @pytest.mark.asyncio
    async def test_transaction_middleware(self):
        """Test transaction middleware."""
        uow = TestUnitOfWork()
        context = ServiceContext(unit_of_work=uow)

        async def handler():
            return TestResponse("done")

        response = await transaction_middleware(TestRequest("test"), context, handler)

        assert response.result == "done"
        assert uow.committed is True
        assert uow.rolled_back is False

    @pytest.mark.asyncio
    async def test_transaction_middleware_rollback(self):
        """Test transaction middleware rolls back on exception."""
        uow = TestUnitOfWork()
        context = ServiceContext(unit_of_work=uow)

        async def handler():
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            await transaction_middleware(TestRequest("test"), context, handler)

        assert uow.committed is False
        assert uow.rolled_back is True

    @pytest.mark.asyncio
    async def test_validation_middleware(self):
        """Test validation middleware."""
        uow = TestUnitOfWork()
        context = ServiceContext(unit_of_work=uow)

        async def handler():
            return TestResponse("done")

        # Valid request
        response = await validation_middleware(TestRequest("valid"), context, handler)
        assert response.result == "done"

        # Invalid request
        with pytest.raises(ValueError, match="Value cannot be empty"):
            await validation_middleware(TestRequest(""), context, handler)

    @pytest.mark.asyncio
    async def test_validation_middleware_no_validate(self):
        """Test validation middleware with request without validate method."""
        uow = TestUnitOfWork()
        context = ServiceContext(unit_of_work=uow)

        class RequestWithoutValidate:
            pass

        async def handler():
            return TestResponse("done")

        response = await validation_middleware(RequestWithoutValidate(), context, handler)
        assert response.result == "done"


class TestMiddlewareBuilder:
    """Tests for MiddlewareBuilder."""

    def test_builder_fluent_api(self):
        """Test the fluent API of MiddlewareBuilder."""
        builder = MiddlewareBuilder[TestRequest, TestResponse, dict[str, object]]()

        middlewares = builder.add_logging().add_transaction().add_validation().build()

        assert len(middlewares) == 3

    def test_builder_custom_middleware(self):
        """Test adding custom middleware."""
        builder = MiddlewareBuilder[TestRequest, TestResponse, dict[str, object]]()

        async def custom_middleware(req, ctx, next_handler):
            return await next_handler()

        middlewares = builder.add(custom_middleware).build()

        assert len(middlewares) == 1
        assert middlewares[0] is custom_middleware
