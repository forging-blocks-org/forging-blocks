"""Application block — orchestrates workflows and coordinates domain logic.

Exports inbound ports (UseCase, CommandHandler, EventHandler, QueryHandler,
MessageHandler, ApplicationService, AuthorizationService, ValidationService),
outbound ports (RepositoryPort, UnitOfWorkPort, MessageBusPort, EventBusPort,
EventStorePort, CachePort, LoggerPort, FileSystemPort, NotifierPort,
ExternalServicePort, TransactionManagerPort, and more), and application-level
errors (ConcurrencyError, EventBusError, EventStoreError, UnitOfWorkError).
"""

from .errors import ConcurrencyError, EventBusError, EventStoreError, UnitOfWorkError
from .ports import (
    CommandHandler,
    CommandSenderPort,
    EventHandler,
    EventPublisherPort,
    MessageBusPort,
    MessageHandler,
    QueryFetcherPort,
    QueryHandler,
    RepositoryPort,
    UnitOfWorkPort,
    UseCase,
)
from .ports.inbound import ApplicationService, AuthorizationService, ValidationService
from .ports.outbound import (
    CachePort,
    EventBusPort,
    EventStorePort,
    ExternalServicePort,
    FileSystemPort,
    LoggerPort,
    NotifierPort,
    ReadOnlyRepositoryPort,
    SpecificationRepositoryPort,
    TransactionManagerPort,
    WriteOnlyRepositoryPort,
)

__all__ = [
    "ApplicationService",
    "AuthorizationService",
    "CachePort",
    "CommandHandler",
    "CommandSenderPort",
    "ConcurrencyError",
    "EventBusError",
    "EventBusPort",
    "EventHandler",
    "EventPublisherPort",
    "EventStoreError",
    "EventStorePort",
    "ExternalServicePort",
    "FileSystemPort",
    "LoggerPort",
    "MessageBusPort",
    "MessageHandler",
    "NotifierPort",
    "QueryFetcherPort",
    "QueryHandler",
    "ReadOnlyRepositoryPort",
    "RepositoryPort",
    "SpecificationRepositoryPort",
    "TransactionManagerPort",
    "UnitOfWorkError",
    "UnitOfWorkPort",
    "UseCase",
    "ValidationService",
    "WriteOnlyRepositoryPort",
]
