"""Mapper module.

Auto-generated minimal module docstring.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

SourceType = TypeVar("SourceType")
TargetType = TypeVar("TargetType")


class Mapper(ABC, Generic[SourceType, TargetType]):
    """A generic contract for mapping objects from one representation to another.

    This abstraction can be implemented in any layer of an application—
    for example, it can map:
      - an HTTP request DTO to an internal service request model,
      - a domain entity to a persistence/infrastructure model,
      - a service response to an HTTP response DTO,
      - any source type to any target type.

    Example usages:
      >>> # HTTP request DTO to service request
      >>> class HttpToServiceRequestMapper(Mapper[HttpRequest, ServiceRequest]):
      ...     def map(self, source: HttpRequest) -> ServiceRequest:
      ...         return ServiceRequest(id=source.id, data=source.body)

      >>> # Domain entity to infrastructure model
      >>> class DomainToPersistenceMapper(Mapper[User, UserRecord]):
      ...     def map(self, source: User) -> UserRecord:
      ...         return UserRecord(pk=source.user_id, name=source.name)
    """

    @abstractmethod
    def map(self, source: SourceType) -> TargetType:
        """Map a source object of type SourceType to a target object of type TargetType.

        Args:
            source (SourceType): The source object to be mapped.

        Returns:
            TargetType: The mapped target object.
        """
        pass
