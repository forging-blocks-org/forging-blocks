"""Mapper Protocol for generic object transformation."""

from typing import Generic, Protocol, TypeVar

SourceType = TypeVar("SourceType", contravariant=True)
TargetType = TypeVar("TargetType", covariant=True)


class Mapper(Protocol, Generic[SourceType, TargetType]):
    """Protocol for mapping objects from one type to another.

    Mappers encapsulate transformation logic between types. This is a
    foundational abstraction that can be used across any context where
    object transformation is needed.

    The protocol uses variance annotations to ensure type safety:
    - SourceType is contravariant: accepts the declared type or supertypes
    - TargetType is covariant: returns the declared type or subtypes

    Type Parameters:
        SourceType: The input type to be transformed (contravariant)
        TargetType: The output type after transformation (covariant)

    Example:
        >>> class UserDTO:
        ...     def __init__(self, username: str, email: str):
        ...         self.username = username
        ...         self.email = email
        ...
        >>> class User:
        ...     def __init__(self, name: str, contact_email: str):
        ...         self.name = name
        ...         self.contact_email = contact_email
        ...
        >>> class UserMapper(Mapper[UserDTO, User]):
        ...     def map(self, source: UserDTO) -> User:
        ...         return User(
        ...             name=source.username,
        ...             contact_email=source.email
        ...         )
        ...
        >>> mapper = UserMapper()
        >>> dto = UserDTO(username="alice", email="alice@example.com")
        >>> user = mapper.map(dto)
    """

    def map(self, source: SourceType) -> TargetType:
        """Transform a source object into a target object.

        Args:
            source: The source object to be transformed.

        Returns:
            The transformed target object.
        """
        ...
