"""Mapper Protocol for generic object transformation."""

from typing import Protocol


class Mapper[SourceType, TargetType](Protocol):
    """Protocol for mapping objects from one type to another.

        Mappers encapsulate transformation logic between types. This is a
        foundational abstraction that can be used across any context where
        object transformation is needed.

        Variance is inferred automatically by the type checker from usage.

        ---
        **Type Parameters**
        -------------------
        - **SourceType** — The input type to be transformed.
        - **TargetType** — The output type after transformation.

        ---
        **Example**
        -----------

    ```python
        class UserDTO:
            def __init__(self, username: str, email: str):
                self.username = username
                self.email = email

        class User:
            def __init__(self, name: str, contact_email: str):
                self.name = name
                self.contact_email = contact_email

        class UserMapper(Mapper[UserDTO, User]):
            def map(self, source: UserDTO) -> User:
                return User(
                    name=source.username,
                    contact_email=source.email,
                )

        mapper = UserMapper()
        dto = UserDTO(username="alice", email="alice@example.com")
        user = mapper.map(dto)
    ```
    """

    def map(self, source: SourceType) -> TargetType:
        """Transform a source object into a target object.

        Args:
            source: The source object to be transformed.

        Returns:
            The transformed target object.

        """
        ...
