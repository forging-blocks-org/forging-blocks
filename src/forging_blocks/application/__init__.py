"""Application block — orchestrates workflows and coordinates domain logic.

Exports inbound ports (UseCasePort, CommandHandlerPort, EventHandlerPort, QueryHandlerPort,
MessageHandlerPort, ApplicationServicePort, AuthorizationPort, ValidationPort),
outbound ports (RepositoryPort, UnitOfWorkPort, MessageBusPort, EventBusPort,
EventStorePort, CachePort, LoggerPort, FileSystemPort, NotifierPort,
HttpClientPort, TransactionManagerPort, and more), and application-level
errors (ConcurrencyError, EventBusError, EventStoreError, UnitOfWorkError).
"""

from .errors import ConcurrencyError, EventBusError, EventStoreError, UnitOfWorkError
from .ports import (
    CommandHandlerPort,
    CommandSenderPort,
    EventHandlerPort,
    EventPublisherPort,
    MessageBusPort,
    MessageHandlerPort,
    QueryFetcherPort,
    QueryHandlerPort,
    RepositoryPort,
    UnitOfWorkPort,
    UseCasePort,
)
from .ports.inbound import ApplicationServicePort, AuthorizationPort, ValidationPort
from .ports.outbound import (
    CachePort,
    EventBusPort,
    EventStorePort,
    FileSystemPort,
    HttpClientPort,
    LoggerPort,
    NotifierPort,
    ReadOnlyRepositoryPort,
    SpecificationRepositoryPort,
    TransactionManagerPort,
    WriteOnlyRepositoryPort,
)

__all__ = [
    "ApplicationServicePort",
    "AuthorizationPort",
    "CachePort",
    "CommandHandlerPort",
    "CommandSenderPort",
    "ConcurrencyError",
    "EventBusError",
    "EventBusPort",
    "EventHandlerPort",
    "EventPublisherPort",
    "EventStoreError",
    "EventStorePort",
    "HttpClientPort",
    "FileSystemPort",
    "LoggerPort",
    "MessageBusPort",
    "MessageHandlerPort",
    "NotifierPort",
    "QueryFetcherPort",
    "QueryHandlerPort",
    "ReadOnlyRepositoryPort",
    "RepositoryPort",
    "SpecificationRepositoryPort",
    "TransactionManagerPort",
    "UnitOfWorkError",
    "UnitOfWorkPort",
    "UseCasePort",
    "ValidationPort",
    "WriteOnlyRepositoryPort",
]
