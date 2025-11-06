"""Mapper Protocol for object transformation."""

from typing import Generic, Protocol, TypeVar

SourceType = TypeVar("SourceType", contravariant=True)
TargetType = TypeVar("TargetType", covariant=True)


class Mapper(Protocol, Generic[SourceType, TargetType]):
    """Maps an object of type SourceType to an object of type TargetType.

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
        ...         return User(name=source.username, contact_email=source.email)
    """

    def map(self, source: SourceType) -> TargetType:
        """Map an object of type SourceType to an object of type TargetType.

        Args:
            source (SourceType): The source object to map.

        Returns:
            TargetType: The mapped target object.
        """
        ...
