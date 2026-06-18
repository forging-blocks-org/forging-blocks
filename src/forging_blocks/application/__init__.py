"""ForgingBlocks for application-specific modules."""

from .application_service import ApplicationService, MiddlewarePipeline
from .errors import UnitOfWorkError
from .middleware import (
    MiddlewareBuilder,
    logging_middleware,
    transaction_middleware,
    validation_middleware,
)
from .ports import (
    CommandHandler,
    CommandSender,
    EventHandler,
    EventPublisher,
    MessageBus,
    MessageHandler,
    QueryFetcher,
    QueryHandler,
    Repository,
    UnitOfWork,
    UseCase,
)
from .query_service import (
    CachedQueryService,
    ProjectionService,
    QueryService,
    ReadModel,
    ReadModelRepository,
)
from .service_context import ServiceContext

__all__ = [
    "ApplicationService",
    "CachedQueryService",
    "CommandHandler",
    "CommandSender",
    "EventHandler",
    "EventPublisher",
    "MessageHandler",
    "MessageBus",
    "MiddlewareBuilder",
    "MiddlewarePipeline",
    "ProjectionService",
    "QueryFetcher",
    "QueryHandler",
    "QueryService",
    "ReadModel",
    "ReadModelRepository",
    "Repository",
    "ServiceContext",
    "UnitOfWork",
    "UnitOfWorkError",
    "UseCase",
    "logging_middleware",
    "transaction_middleware",
    "validation_middleware",
]
